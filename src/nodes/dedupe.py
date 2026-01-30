"""
Dedupe node - summarizes and deduplicates articles.

Reduces 15-20 articles to 8-12 unique stories by merging duplicates.
"""

import logging
from typing import Any

from ..config import Article, LeaderConfig
from ..state import LeaderProcessingState
from ..agents.classifier import ClassifierAgent
from ..debug import save_dedupe_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def summarize_and_dedupe(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Reduce articles to unique stories by merging duplicates.

    This step identifies articles covering the SAME underlying event
    and consolidates them into unique stories.

    Args:
        state: Leader processing state with translated articles

    Returns:
        Updated state with deduped_articles field populated
    """
    articles = state.get("translated_articles", [])

    if not articles:
        return {"deduped_articles": []}

    leader = state["leader"]
    original_count = len(articles)
    logger.info(f"Deduplicating {original_count} articles for {leader.name}")

    try:
        classifier = ClassifierAgent()
        deduped = await classifier.summarize_and_dedupe(articles, leader)

        logger.info(f"Reduced {original_count} to {len(deduped)} unique stories for {leader.name}")

        # Save debug output
        if is_debug_enabled():
            save_dedupe_results(
                leader_name=leader.name,
                original_count=original_count,
                deduped_articles=deduped,
            )

        return {"deduped_articles": deduped}

    except Exception as e:
        logger.error(f"Deduplication failed for {leader.name}: {e}")
        # Return original articles on failure
        return {"deduped_articles": articles}
