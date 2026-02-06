"""
Event Clustering Agent - Clusters search results into distinct events.

Pipeline:
1. Fetch snippets from all sources (SerpAPI only)
2. Embed snippets
3. Cluster with HDBSCAN
4. Score clusters by importance
5. Select top events for full fetch
"""
import logging
from typing import Optional
from dataclasses import dataclass

from ..config import (
    LeaderConfig, WIRE_SERVICES,
    EMBEDDING_MODEL, MULTILINGUAL_EMBEDDING_MODEL,
    leader_needs_multilingual,
)
from ..fetcher.core import fetch_snippets_for_leader, fetch_full_articles
from ..fetcher.diffbot_nlp import extract_nlp, extract_high_salience_entities, get_summary
from ..clustering import (
    SnippetEmbedder, EventClusterer, EventScorer,
    filter_relevant, separate_opinions, deduplicate_clusters,
)

logger = logging.getLogger(__name__)


@dataclass
class ProcessedEvent:
    """A fully processed event with articles and NLP analysis."""
    id: str
    title: str
    articles: list[dict]
    entities: list[dict]  # High-salience entities across all articles
    summary: str  # Synthesized from Diffbot summaries
    score: float
    rank: int
    source_count: int
    has_wire: bool


class EventClusteringAgent:
    """
    Orchestrates the event clustering pipeline for a single leader.
    """

    def __init__(
        self,
        embedder: Optional[SnippetEmbedder] = None,
        clusterer: Optional[EventClusterer] = None,
        scorer: Optional[EventScorer] = None,
    ):
        self._default_embedder = embedder
        self.clusterer = clusterer or EventClusterer()
        self.scorer = scorer or EventScorer()

    def _get_embedder(self, leader: LeaderConfig) -> SnippetEmbedder:
        """Get the appropriate embedder for this leader's language mix."""
        if self._default_embedder is not None:
            return self._default_embedder

        if leader_needs_multilingual(leader):
            model_name = MULTILINGUAL_EMBEDDING_MODEL
            logger.info(f"Using multilingual model for {leader.name}")
        else:
            model_name = EMBEDDING_MODEL

        return SnippetEmbedder(model_name=model_name)

    async def process_leader(
        self,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
        max_events_for_brief: int = 5,
        max_articles_per_event: int = 3,
    ) -> tuple[list[ProcessedEvent], list[ProcessedEvent], list[dict]]:
        """
        Full pipeline: fetch -> cluster -> score -> fetch full articles.

        Args:
            leader: Leader configuration
            date_start: Start date
            date_end: End date
            max_events_for_brief: Max events for executive summary
            max_articles_per_event: Max full articles to fetch per event

        Returns:
            Tuple of (top_events, remaining_events, opinions)
        """
        # 1. Build source list (wire + domestic)
        sources = self._build_source_list(leader)

        # 2. Fetch snippets (cheap - SerpAPI only)
        logger.info(f"Fetching snippets for {leader.name}")
        snippets = await fetch_snippets_for_leader(
            leader_name=leader.name,
            sources=sources,
            date_start=date_start,
            date_end=date_end,
        )

        if not snippets:
            logger.warning(f"No snippets found for {leader.name}")
            return [], [], []

        logger.info(f"Found {len(snippets)} raw snippets for {leader.name}")

        # 3. Pre-filter: relevance + opinion separation
        snippets = filter_relevant(snippets, leader.name)
        snippets, opinions = separate_opinions(snippets)

        if not snippets:
            logger.warning(f"No relevant news snippets for {leader.name}")
            return [], [], opinions

        # 4. Embed snippets (model selected based on leader's source languages)
        embedder = self._get_embedder(leader)
        embedded = embedder.embed_snippets(snippets, leader_name=leader.name)

        # 5. Cluster into events
        clusters = self.clusterer.cluster(embedded)

        # 5.5 LLM-based deduplication pass
        # Catches same-event clusters that HDBSCAN failed to merge
        if len(clusters) >= 2:
            clusters = await deduplicate_clusters(clusters, leader.name)
            logger.info(f"After dedup: {len(clusters)} clusters for {leader.name}")

        # 6. Score events
        scored = self.scorer.score_events(clusters)

        # 7. Split into top/rest
        top_scored, rest_scored = self.scorer.filter_top_events(
            scored, max_events=max_events_for_brief
        )

        # 8. Fetch full articles for top events
        top_events = await self._process_events(top_scored, max_articles_per_event)

        # For remaining events, only fetch full articles for those with 3+ sources
        # (matches the corroboration threshold used in also_noted filtering)
        rest_corroborated = [s for s in rest_scored if s.cluster.unique_source_count >= 3]
        rest_thin = [s for s in rest_scored if s.cluster.unique_source_count < 3]
        rest_events = await self._process_events(rest_corroborated, max_articles_per_event)
        rest_events += await self._process_events(rest_thin, max_articles_per_event=1)

        return top_events, rest_events, opinions

    def _build_source_list(self, leader: LeaderConfig) -> list[dict]:
        """Combine wire services with leader's domestic sources."""
        sources = []

        # Wire services
        for wire in WIRE_SERVICES:
            sources.append({
                "name": wire.name,
                "url": wire.url,
                "source_type": "wire",
                "language": "en",
            })

        # Domestic sources
        for domestic in leader.domestic_sources:
            sources.append({
                "name": domestic.name,
                "url": domestic.url,
                "source_type": "domestic",
                "language": domestic.language,
            })

        return sources

    async def _process_events(
        self,
        scored_events: list,
        max_articles_per_event: int,
    ) -> list[ProcessedEvent]:
        """Fetch full articles and extract NLP for scored events."""
        processed = []

        for scored in scored_events:
            cluster = scored.cluster

            # Select URLs to fetch (prioritize wire, then diversity)
            urls_to_fetch = self._select_urls(cluster, max_articles_per_event)

            # Build source metadata map
            source_meta = {
                s.url: {
                    "source_name": s.source_name,
                    "source_type": s.source_type,
                }
                for s in cluster.snippets
            }

            # Fetch full articles
            articles = await fetch_full_articles(urls_to_fetch, source_meta)

            # Extract NLP from each article
            all_entities = []
            summaries = []

            for article in articles:
                nlp = await extract_nlp(article.get("content", ""))
                if nlp:
                    entities = extract_high_salience_entities(nlp)
                    all_entities.extend(entities)
                    summaries.append(get_summary(nlp))

            # Dedupe entities by URI
            unique_entities = self._dedupe_entities(all_entities)

            processed.append(ProcessedEvent(
                id=cluster.id,
                title=cluster.representative_title,
                articles=articles,
                entities=unique_entities,
                summary=" | ".join(summaries),
                score=scored.score,
                rank=scored.rank,
                source_count=cluster.unique_source_count,
                has_wire=cluster.has_wire_coverage,
            ))

        return processed

    def _select_urls(self, cluster, max_count: int) -> list[str]:
        """Select URLs to fetch, prioritizing wire services and source diversity."""
        wire_urls = [s.url for s in cluster.snippets if s.source_type == "wire"]
        domestic_urls = [s.url for s in cluster.snippets if s.source_type == "domestic"]

        # Start with 1 wire for baseline, then alternate domestic for diversity,
        # then backfill with remaining wire if domestic exhausted
        selected = []

        if wire_urls:
            selected.append(wire_urls[0])

        for url in domestic_urls:
            if len(selected) >= max_count:
                break
            if url not in selected:
                selected.append(url)

        # Backfill with additional wire URLs if we still have room
        for url in wire_urls[1:]:
            if len(selected) >= max_count:
                break
            if url not in selected:
                selected.append(url)

        return selected

    def _dedupe_entities(self, entities: list[dict]) -> list[dict]:
        """Deduplicate entities by URI, keeping highest salience."""
        by_uri = {}
        for e in entities:
            uri = e.get("uri", e.get("name"))
            if uri not in by_uri or e["salience"] > by_uri[uri]["salience"]:
                by_uri[uri] = e
        return list(by_uri.values())
