"""
Compile node - assembles final WeeklyBrief from all components.
"""

import logging
from datetime import datetime
from typing import Any

from ..config import WeeklyBrief
from ..state import PDBState
from ..persistence import save_brief
from ..debug import save_final_brief, create_pipeline_summary, is_debug_enabled

logger = logging.getLogger(__name__)


async def compile_brief(state: PDBState) -> dict[str, Any]:
    """
    Compile all components into the final WeeklyBrief.

    Args:
        state: PDB state with all synthesized components

    Returns:
        Updated state with brief field populated
    """
    date_start = state.get("date_range_start", "")
    date_end = state.get("date_range_end", "")
    dossiers = state.get("dossiers", {})
    threads = state.get("all_threads", [])
    executive_summary = state.get("executive_summary", "")
    regional_contexts = state.get("regional_contexts", {})
    source_quality_notes = state.get("source_quality_notes", "")

    logger.info("Compiling final brief")

    # Generate methodology notes
    methodology_notes = _generate_methodology_notes(dossiers)

    # Create brief
    brief = WeeklyBrief(
        date_range=f"{date_start} to {date_end}",
        generated_at=datetime.now(),
        global_pulse=None,  # Bottom-up: no top-down context
        executive_summary=executive_summary,
        cross_cutting_threads=threads,
        leader_dossiers=list(dossiers.values()),
        regional_context=regional_contexts,
        methodology_notes=methodology_notes,
        source_quality_notes=source_quality_notes,
    )

    # Save brief
    try:
        brief_path = save_brief(brief)
        logger.info(f"Brief saved to {brief_path}")
    except Exception as e:
        logger.error(f"Failed to save brief: {e}")

    # Save debug outputs
    if is_debug_enabled():
        # Save final brief
        save_final_brief(brief)

        # Create pipeline summary
        leader_stats = {
            "total": len(dossiers),
            "by_region": {},
        }
        for name, dossier in dossiers.items():
            region = dossier.leader.region
            if region not in leader_stats["by_region"]:
                leader_stats["by_region"][region] = []
            leader_stats["by_region"][region].append({
                "name": name,
                "article_count": len(dossier.articles),
                "action_count": len(dossier.key_actions),
                "event_count": len(dossier.underlying_events),
            })

        thread_stats = {
            "total": len(threads),
            "multi_leader": sum(1 for t in threads if not t.is_singleton),
            "singletons": sum(1 for t in threads if t.is_singleton),
        }

        create_pipeline_summary(
            leader_stats=leader_stats,
            thread_stats=thread_stats,
        )

    return {"brief": brief}


def _generate_methodology_notes(dossiers: dict) -> str:
    """Generate methodology disclosure."""
    total_articles = sum(len(d.articles) for d in dossiers.values())
    sources = set()
    for d in dossiers.values():
        for a in d.articles:
            sources.add(a.source_name)

    return f"""
**Methodology**

This brief was generated using an automated multi-agent system that:
1. Fetched {total_articles} articles from {len(sources)} sources
2. Translated non-English content using LLM translation
3. Deduplicated articles covering the same underlying events
4. Classified articles using the Paragon taxonomy
5. Filtered to priority score >= 0.4
6. Built per-leader dossiers using bottom-up synthesis
7. Detected cross-cutting threads (multi-leader + singletons)
8. Synthesized findings into narrative sections

**Architecture**: Bottom-up approach where narrative emerges from leader
actions rather than top-down global context framing.

**Limitations**: Automated classification may miss nuance. Non-English
translation may lose political subtlety. Thread detection uses semantic
similarity and may over- or under-cluster.
"""
