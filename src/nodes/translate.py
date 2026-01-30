"""
Translate node - translates non-English articles.
"""

import logging
from typing import Any

from ..state import LeaderProcessingState
from ..agents.translator import TranslatorAgent
from ..debug import save_translate_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def translate_articles(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Translate non-English articles.

    Args:
        state: Leader processing state with articles

    Returns:
        Updated state with translated_articles field populated
    """
    articles = state.get("articles", [])

    if not articles:
        return {"translated_articles": []}

    leader = state["leader"]
    logger.info(f"Translating articles for {leader.name}")

    try:
        translator = TranslatorAgent()
        translated = await translator.translate_batch(articles)

        # Count translations
        translated_count = sum(
            1 for a in translated
            if a.translated_content and a.original_language != "en"
        )
        logger.info(f"Translated {translated_count} non-English articles for {leader.name}")

        # Save debug output
        if is_debug_enabled():
            save_translate_results(
                leader_name=leader.name,
                articles=translated,
                translated_count=translated_count,
            )

        return {"translated_articles": translated}

    except Exception as e:
        logger.error(f"Translation failed for {leader.name}: {e}")
        # Return original articles on failure
        return {"translated_articles": articles}
