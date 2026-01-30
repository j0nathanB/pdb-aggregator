"""
Classify node - applies Paragon taxonomy to articles.
"""

import logging
from typing import Any

from ..config import RELEVANCE_THRESHOLD
from ..state import LeaderProcessingState
from ..agents.classifier import ClassifierAgent
from ..debug import save_classify_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def classify_articles(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Classify articles using the Paragon taxonomy.

    Args:
        state: Leader processing state with deduped articles

    Returns:
        Updated state with classified_articles field populated
    """
    articles = state.get("deduped_articles", [])

    if not articles:
        return {"classified_articles": []}

    leader = state["leader"]
    logger.info(f"Classifying {len(articles)} articles for {leader.name}")

    try:
        classifier = ClassifierAgent()
        classified = await classifier.classify_batch(articles, leader)

        # Filter by relevance threshold
        relevant = [
            a for a in classified
            if a.classification and a.classification.priority_score >= RELEVANCE_THRESHOLD
        ]

        logger.info(
            f"Classified {len(articles)} articles, {len(relevant)} meet threshold "
            f"({RELEVANCE_THRESHOLD}) for {leader.name}"
        )

        # Save debug output (all classified articles, showing what passed/failed)
        if is_debug_enabled():
            save_classify_results(
                leader_name=leader.name,
                articles=classified,
                filtered_count=len(relevant),
                threshold=RELEVANCE_THRESHOLD,
            )

        return {"classified_articles": relevant}

    except Exception as e:
        logger.error(f"Classification failed for {leader.name}: {e}")
        return {"classified_articles": []}
