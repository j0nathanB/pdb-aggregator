"""
Deep-dive search expansion: targeted Brave queries to fill gaps beyond triage.

Triage runs 2 queries per country (wire sweep + primary actor domestic).
Expansion adds actor-specific and signal-category vocabulary queries for
deep-dive countries, producing 150-250 additional results that merge with
triage results for the story map agent.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..collection.brave import BraveNewsClient, BraveNewsResult
from ..config import CountryConfig
from .triage import ScanResult

logger = logging.getLogger(__name__)


# =============================================================================
# Data structures
# =============================================================================

@dataclass
class ExpansionResult:
    """Combined triage + expansion results for a single country."""
    code: str
    country: str
    # Triage results (forwarded)
    triage_wire: list[BraveNewsResult] = field(default_factory=list)
    triage_domestic: list[BraveNewsResult] = field(default_factory=list)
    # Expansion results (new queries)
    actor_results: list[BraveNewsResult] = field(default_factory=list)
    vocab_results: list[BraveNewsResult] = field(default_factory=list)
    # Metadata
    queries_run: list[str] = field(default_factory=list)

    @property
    def all_results(self) -> list[BraveNewsResult]:
        """All results deduplicated by URL, preserving order."""
        seen: set[str] = set()
        out: list[BraveNewsResult] = []
        for r in (
            self.triage_wire
            + self.triage_domestic
            + self.actor_results
            + self.vocab_results
        ):
            if r.url not in seen:
                seen.add(r.url)
                out.append(r)
        return out

    @property
    def total_count(self) -> int:
        return len(self.all_results)

    @property
    def raw_count(self) -> int:
        """Total results before deduplication."""
        return (
            len(self.triage_wire)
            + len(self.triage_domestic)
            + len(self.actor_results)
            + len(self.vocab_results)
        )

    @property
    def source_counts(self) -> dict[str, int]:
        """Count of results by source: triage_wire, triage_domestic, actor, vocab."""
        return {
            "triage_wire": len(self.triage_wire),
            "triage_domestic": len(self.triage_domestic),
            "actor": len(self.actor_results),
            "vocab": len(self.vocab_results),
        }

    @property
    def dedup_record(self) -> dict:
        """Record of URL deduplication: which sources found each URL."""
        url_sources: dict[str, list[str]] = {}
        for label, results in [
            ("triage_wire", self.triage_wire),
            ("triage_domestic", self.triage_domestic),
            ("actor", self.actor_results),
            ("vocab", self.vocab_results),
        ]:
            for r in results:
                url_sources.setdefault(r.url, []).append(label)

        duplicates = {url: sources for url, sources in url_sources.items() if len(sources) > 1}
        return {
            "raw_total": self.raw_count,
            "unique_urls": self.total_count,
            "duplicates_removed": self.raw_count - self.total_count,
            "urls_found_by_multiple_sources": len(duplicates),
            "duplicate_urls": {
                url: {"count": len(sources), "found_in": sources}
                for url, sources in duplicates.items()
            },
        }


# =============================================================================
# Query building
# =============================================================================

def _build_actor_queries(
    config: CountryConfig,
    has_triage: bool = True,
) -> list[str]:
    """Build one query per actor using their first search term.

    When triage results are available, the primary actor is already covered
    by the triage domestic sweep and is skipped. When triage was skipped
    (has_triage=False), the primary actor gets a dedicated query.
    """
    queries = []
    for actor in config.actors:
        if actor.primary and has_triage:
            continue
        if actor.search_terms:
            queries.append(actor.search_terms[0])
    return queries


def _build_vocab_queries(config: CountryConfig) -> list[str]:
    """Build one query per signal-category vocabulary group.

    Combines the top terms from each category into a single query string
    that Brave can match broadly.
    """
    vocab = config.news_discovery.query_vocabulary
    queries = []

    category_terms = {
        "diplomatic_alignment": vocab.diplomatic_alignment,
        "security_defense": vocab.security_defense,
        "economic_tech": vocab.economic_tech,
        "institutional": vocab.institutional,
        "domestic_constraints": vocab.domestic_constraints,
    }

    for category, terms in category_terms.items():
        if not terms:
            continue
        # Use top 2-3 terms joined with OR for broader matching
        top_terms = terms[:3]
        query = " OR ".join(f'"{t}"' for t in top_terms)
        queries.append(query)

    return queries


# =============================================================================
# Expansion execution
# =============================================================================

async def expand_country(
    config: CountryConfig,
    brave_client: BraveNewsClient,
    triage_scan: ScanResult | None = None,
    end_date: date | None = None,
    semaphore: asyncio.Semaphore | None = None,
) -> ExpansionResult:
    """Run expansion queries for a single deep-dive country.

    Merges triage scan results (if provided) with targeted actor and
    vocabulary queries.
    """
    end_date = end_date or date.today()
    start_date = end_date - timedelta(days=7)
    freshness = f"{start_date.isoformat()}to{end_date.isoformat()}"

    # Resolve goggle URL
    cc = brave_client.country_configs.get(config.code)
    goggle_url = cc.goggle_url() if cc else None

    result = ExpansionResult(
        code=config.code,
        country=config.country,
    )

    # Forward triage results
    if triage_scan:
        result.triage_wire = list(triage_scan.wire_results)
        result.triage_domestic = list(triage_scan.domestic_results)

    # Build query lists
    has_triage = triage_scan is not None
    actor_queries = _build_actor_queries(config, has_triage=has_triage)
    vocab_queries = _build_vocab_queries(config)
    all_queries = actor_queries + vocab_queries

    if not all_queries:
        logger.info("Expansion %s: no queries to run", config.code)
        return result

    logger.info(
        "Expansion %s: %d actor queries + %d vocab queries",
        config.code, len(actor_queries), len(vocab_queries),
    )

    async def _run_queries() -> None:
        for i, query in enumerate(actor_queries):
            result.queries_run.append(query)
            try:
                resp = await brave_client.search_news(
                    query,
                    country_code=config.code,
                    freshness=freshness,
                    count=50,
                    goggles=goggle_url,
                )
                result.actor_results.extend(resp.results)
                logger.debug(
                    "Expansion %s: actor query %d/%d q=%r → %d results",
                    config.code, i + 1, len(actor_queries), query, len(resp.results),
                )
            except Exception as e:
                logger.warning(
                    "Expansion %s: actor query failed q=%r: %s",
                    config.code, query, e,
                )

        for i, query in enumerate(vocab_queries):
            result.queries_run.append(query)
            try:
                resp = await brave_client.search_news(
                    query,
                    country_code=config.code,
                    freshness=freshness,
                    count=50,
                    goggles=goggle_url,
                )
                result.vocab_results.extend(resp.results)
                logger.debug(
                    "Expansion %s: vocab query %d/%d q=%r → %d results",
                    config.code, i + 1, len(vocab_queries), query, len(resp.results),
                )
            except Exception as e:
                logger.warning(
                    "Expansion %s: vocab query failed q=%r: %s",
                    config.code, query, e,
                )

    if semaphore:
        async with semaphore:
            await _run_queries()
    else:
        await _run_queries()

    deduped_count = result.total_count
    raw_count = (
        len(result.triage_wire)
        + len(result.triage_domestic)
        + len(result.actor_results)
        + len(result.vocab_results)
    )
    logger.info(
        "Expansion %s complete: %d raw results → %d deduplicated "
        "(wire=%d, domestic=%d, actor=%d, vocab=%d)",
        config.code, raw_count, deduped_count,
        len(result.triage_wire), len(result.triage_domestic),
        len(result.actor_results), len(result.vocab_results),
    )

    return result


async def expand_all_countries(
    configs: list[CountryConfig],
    brave_client: BraveNewsClient,
    scan_map: dict[str, ScanResult],
    end_date: date | None = None,
    max_concurrent: int = 5,
) -> dict[str, ExpansionResult]:
    """Run expansion for multiple deep-dive countries with concurrency limit.

    Returns results keyed by country code.
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [
        expand_country(
            config, brave_client,
            triage_scan=scan_map.get(config.code),
            end_date=end_date,
            semaphore=semaphore,
        )
        for config in configs
    ]
    results = await asyncio.gather(*tasks)
    return {r.code: r for r in results}
