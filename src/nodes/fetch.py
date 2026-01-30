"""
Fetch node - fetches articles for a leader.
"""

import logging
from typing import Any

from ..config import Article, LeaderConfig
from ..state import LeaderProcessingState
from ..agents.source_fetcher import SourceFetcherAgent
from ..debug import save_fetch_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def fetch_articles_for_leader(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Fetch articles for a single leader.

    Args:
        state: Leader processing state with leader config and date range

    Returns:
        Updated state with articles field populated
    """
    leader = state["leader"]
    date_start = state["date_range_start"]
    date_end = state["date_range_end"]

    logger.info(f"Fetching articles for {leader.name}")

    try:
        fetcher = SourceFetcherAgent()
        articles = await fetcher.fetch_for_leader(
            leader=leader,
            date_start=date_start,
            date_end=date_end,
        )
        await fetcher.close()

        logger.info(f"Fetched {len(articles)} articles for {leader.name}")

        # Save debug output
        if is_debug_enabled():
            # Build source breakdown
            source_breakdown = {}
            for article in articles:
                src = article.source_name
                source_breakdown[src] = source_breakdown.get(src, 0) + 1

            save_fetch_results(
                leader_name=leader.name,
                articles=articles,
                source_breakdown=source_breakdown,
            )

        return {"articles": articles}

    except Exception as e:
        logger.error(f"Failed to fetch articles for {leader.name}: {e}")
        return {
            "articles": [],
            "error": f"Fetch failed: {e}",
        }
