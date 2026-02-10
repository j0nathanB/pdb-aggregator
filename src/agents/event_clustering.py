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
from dataclasses import dataclass, asdict

from ..config import (
    LeaderConfig, WIRE_SERVICES,
    EMBEDDING_MODEL, MULTILINGUAL_EMBEDDING_MODEL,
    leader_needs_multilingual,
)
from ..fetcher.core import fetch_snippets_for_leader, fetch_full_articles
from ..fetcher.diffbot_nlp import extract_nlp, extract_high_salience_entities, get_summary
from ..clustering import (
    SnippetEmbedder, EventClusterer, EventScorer, EventCluster,
    filter_relevant, deduplicate_clusters,
    detect_story_arcs, merge_story_arc_titles,
)
from ..debug import is_debug_enabled, save_debug_output

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
        leader_slug = leader.name.lower().replace(" ", "_")

        # 1. Build source list (wire + domestic)
        sources = self._build_source_list(leader)

        # 2. Fetch snippets (cheap - SerpAPI only, with opinion filtering)
        logger.info(f"Fetching snippets for {leader.name}")
        snippets, opinions = await fetch_snippets_for_leader(
            leader_name=leader.name,
            sources=sources,
            date_start=date_start,
            date_end=date_end,
        )

        if not snippets and not opinions:
            logger.warning(f"No snippets found for {leader.name}")
            return [], [], []

        logger.info(f"Found {len(snippets)} news + {len(opinions)} opinion snippets for {leader.name}")

        # Debug: save raw snippets (after opinion filtering)
        if is_debug_enabled():
            save_debug_output(f"00_raw_snippets_{leader_slug}", {
                "leader": leader.name,
                "news_count": len(snippets),
                "opinion_count": len(opinions),
                "news_snippets": snippets,
                "opinion_snippets": opinions,
            })

        # 3. Pre-filter: relevance check (opinions already filtered at fetch)
        raw_count = len(snippets) + len(opinions)
        snippets = filter_relevant(snippets, leader.name)

        # Debug: save prefilter results
        if is_debug_enabled():
            save_debug_output(f"01_prefilter_{leader_slug}", {
                "leader": leader.name,
                "raw_count": raw_count,
                "after_relevance": len(snippets) + len(opinions),
                "news_count": len(snippets),
                "opinion_count": len(opinions),
                "news_snippets": snippets,
                "opinion_snippets": opinions,
            })

        if not snippets:
            logger.warning(f"No relevant news snippets for {leader.name}")
            return [], [], opinions

        # 4. Embed snippets (model selected based on leader's source languages)
        embedder = self._get_embedder(leader)
        embedded = embedder.embed_snippets(snippets, leader_name=leader.name)

        # 5. Cluster into events
        clusters = self.clusterer.cluster(embedded)

        # Debug: save initial clusters
        if is_debug_enabled():
            save_debug_output(f"02_clusters_{leader_slug}", {
                "leader": leader.name,
                "cluster_count": len(clusters),
                "clusters": self._clusters_to_debug(clusters),
            })

        # 5.5 LLM-based deduplication pass
        # Catches same-event clusters that HDBSCAN failed to merge
        pre_dedup_count = len(clusters)
        if len(clusters) >= 2:
            clusters = await deduplicate_clusters(clusters, leader.name)
            logger.info(f"After dedup: {len(clusters)} clusters for {leader.name}")

        # Debug: save after dedup
        if is_debug_enabled() and pre_dedup_count != len(clusters):
            save_debug_output(f"03_dedup_{leader_slug}", {
                "leader": leader.name,
                "before": pre_dedup_count,
                "after": len(clusters),
                "clusters": self._clusters_to_debug(clusters),
            })

        # 5.6 Story arc detection
        # Merges multi-day developing stories (e.g., Orsi's week-long China visit)
        pre_arc_count = len(clusters)
        if len(clusters) >= 2:
            clusters = await self._merge_story_arcs(clusters, leader.name)

        # Debug: save after story arc merge
        if is_debug_enabled() and pre_arc_count != len(clusters):
            save_debug_output(f"04_story_arcs_{leader_slug}", {
                "leader": leader.name,
                "before": pre_arc_count,
                "after": len(clusters),
                "clusters": self._clusters_to_debug(clusters),
            })

        # 6. Score events
        scored = self.scorer.score_events(clusters)

        # Debug: save scored events
        if is_debug_enabled():
            save_debug_output(f"05_scored_{leader_slug}", {
                "leader": leader.name,
                "event_count": len(scored),
                "events": [
                    {
                        "rank": s.rank,
                        "score": s.score,
                        "title": s.cluster.representative_title,
                        "source_count": s.cluster.unique_source_count,
                        "has_wire": s.cluster.has_wire_coverage,
                        "snippet_count": len(s.cluster.snippets),
                    }
                    for s in scored
                ],
            })

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

        # Debug: save final processed events
        if is_debug_enabled():
            save_debug_output(f"06_processed_{leader_slug}", {
                "leader": leader.name,
                "top_event_count": len(top_events),
                "rest_event_count": len(rest_events),
                "top_events": [asdict(e) for e in top_events],
                "rest_events": [asdict(e) for e in rest_events],
            })

        return top_events, rest_events, opinions

    def _clusters_to_debug(self, clusters: list[EventCluster]) -> list[dict]:
        """Convert clusters to debug-friendly format (without embeddings)."""
        return [
            {
                "id": c.id,
                "title": c.representative_title,
                "source_count": c.unique_source_count,
                "has_wire": c.has_wire_coverage,
                "snippets": [
                    {
                        "title": s.title,
                        "source_name": s.source_name,
                        "source_type": s.source_type,
                        "url": s.url,
                    }
                    for s in c.snippets
                ],
            }
            for c in clusters
        ]

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

            # NOTE: Diffbot NLP API disabled (500 calls/month limit is too restrictive)
            # Entity extraction and summaries skipped - dossier builder handles
            # summarization implicitly during LLM synthesis. Cross-leader entity
            # matching in aggregate_builder will be degraded without entities.
            unique_entities = []

            processed.append(ProcessedEvent(
                id=cluster.id,
                title=cluster.representative_title,
                articles=articles,
                entities=unique_entities,
                summary="",  # NLP summaries disabled; dossier builder synthesizes from full content
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

    async def _merge_story_arcs(
        self,
        clusters: list[EventCluster],
        leader_name: str,
    ) -> list[EventCluster]:
        """
        Detect and merge story arcs (multi-day developing stories).

        E.g., "Orsi arrives in China", "Orsi meets Xi", "Orsi visits Shanghai"
        all become one merged cluster about Orsi's China visit.
        """
        if len(clusters) < 2:
            return clusters

        # Get titles for arc detection
        titles = [c.representative_title for c in clusters]

        # Detect arcs
        arcs = await detect_story_arcs(titles, leader_name)

        if not arcs:
            return clusters

        # Track which clusters have been merged
        merged_indices: set[int] = set()
        result: list[EventCluster] = []

        for arc_indices in arcs:
            if not arc_indices:
                continue

            # Get clusters in this arc
            arc_clusters = [clusters[i] for i in arc_indices if i < len(clusters)]
            if len(arc_clusters) < 2:
                continue

            # Merge into one cluster
            merged = await self._merge_clusters(arc_clusters, leader_name)
            result.append(merged)
            merged_indices.update(arc_indices)

            logger.info(
                f"Merged story arc for {leader_name}: "
                f"{len(arc_clusters)} events -> '{merged.representative_title}'"
            )

        # Add clusters that weren't merged
        for i, cluster in enumerate(clusters):
            if i not in merged_indices:
                result.append(cluster)

        logger.info(
            f"After story arc merge: {len(clusters)} -> {len(result)} clusters "
            f"for {leader_name}"
        )

        return result

    async def _merge_clusters(
        self,
        clusters: list[EventCluster],
        leader_name: str,
    ) -> EventCluster:
        """Merge multiple clusters into one."""
        import numpy as np

        # Combine all snippets
        all_snippets = []
        for c in clusters:
            all_snippets.extend(c.snippets)

        # Compute new centroid as mean of all snippet embeddings
        embeddings = np.array([s.embedding for s in all_snippets])
        merged_centroid = np.mean(embeddings, axis=0)
        merged_centroid = merged_centroid / np.linalg.norm(merged_centroid)

        # Use first cluster's ID with suffix
        merged_id = f"{clusters[0].id}_arc"

        return EventCluster(
            id=merged_id,
            snippets=all_snippets,
            centroid=merged_centroid,
        )
