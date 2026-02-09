"""
Aggregate briefing node - builds story-centric aggregate from leader dossiers.

Replaces the old thread detection nodes (detect_multi_leader_threads,
detect_singletons, merge_threads) with a single aggregate builder step.
"""

import logging
from typing import Any

from ..config import LeaderDossier, Story
from ..state import PDBState
from ..agents.aggregate_builder import AggregateBriefingBuilder
from ..debug import save_synthesis_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def build_aggregate_briefing(state: PDBState) -> dict[str, Any]:
    """
    Build aggregate briefing from all leader dossiers.

    Replaces the three-phase thread detection (multi-leader, singletons, merge)
    with story-centric aggregate builder.

    Args:
        state: PDB state with dossiers

    Returns:
        Updated state with aggregate story lists and BTL
    """
    dossiers = state.get("dossiers", {})

    if not dossiers:
        logger.warning("No dossiers available for aggregate briefing")
        return {
            "aggregate_main_stories": [],
            "aggregate_intl_stories": [],
            "aggregate_dom_stories": [],
            "aggregate_btl": [],
            "aggregate_executive_summary": "",
        }

    logger.info(f"Building aggregate briefing from {len(dossiers)} dossiers")

    try:
        builder = AggregateBriefingBuilder()
        main_stories, intl_stories, dom_stories, btl, executive_summary = await builder.build(dossiers)

        logger.info(
            f"Aggregate: {len(main_stories)} main, "
            f"{len(intl_stories)} intl, {len(dom_stories)} dom, "
            f"{len(btl)} BTL"
        )

        # Save debug output
        if is_debug_enabled():
            save_synthesis_results("aggregate_briefing", {
                "main_stories": len(main_stories),
                "international_stories": len(intl_stories),
                "domestic_stories": len(dom_stories),
                "between_the_lines": btl,
                "executive_summary": executive_summary[:100] + "..." if len(executive_summary) > 100 else executive_summary,
            })

        return {
            "aggregate_main_stories": main_stories,
            "aggregate_intl_stories": intl_stories,
            "aggregate_dom_stories": dom_stories,
            "aggregate_btl": btl,
            "aggregate_executive_summary": executive_summary,
        }

    except Exception as e:
        logger.error(f"Aggregate briefing build failed: {e}")
        return {
            "aggregate_main_stories": [],
            "aggregate_intl_stories": [],
            "aggregate_dom_stories": [],
            "aggregate_btl": [],
            "aggregate_executive_summary": "",
        }
