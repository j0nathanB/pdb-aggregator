"""
Dossier node - builds leader dossier from classified articles.
"""

import logging
from typing import Any

from ..state import LeaderProcessingState
from ..agents.dossier_builder import DossierBuilderAgent
from ..debug import save_dossier_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def build_dossier(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Build a dossier for the leader from classified articles.

    Uses bottom-up approach - no GlobalPulse context required.

    Args:
        state: Leader processing state with classified articles

    Returns:
        Updated state with dossier field populated
    """
    articles = state.get("classified_articles", [])
    leader = state["leader"]

    logger.info(f"Building dossier for {leader.name} from {len(articles)} articles")

    try:
        builder = DossierBuilderAgent()

        # Build dossier WITHOUT global_context (bottom-up architecture)
        dossier = await builder.build(
            leader=leader,
            articles=articles,
            global_context=None,  # Bottom-up: no top-down context
        )

        logger.info(
            f"Built dossier for {leader.name}: "
            f"{len(dossier.key_actions)} actions, "
            f"{len(dossier.underlying_events)} events"
        )

        # Save debug output
        if is_debug_enabled():
            save_dossier_results(
                leader_name=leader.name,
                dossier=dossier,
            )

        return {"dossier": dossier}

    except Exception as e:
        logger.error(f"Dossier building failed for {leader.name}: {e}")
        return {
            "dossier": None,
            "error": f"Dossier building failed: {e}",
        }
