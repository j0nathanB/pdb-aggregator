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
    main_stories = state.get("aggregate_main_stories", [])
    intl_stories = state.get("aggregate_intl_stories", [])
    dom_stories = state.get("aggregate_dom_stories", [])
    btl = state.get("aggregate_btl", [])
    source_quality_notes = state.get("source_quality_notes", "")

    logger.info("Compiling final brief")

    # Generate methodology notes
    methodology_notes = _generate_methodology_notes(dossiers)

    # Create brief
    brief = WeeklyBrief(
        date_range=f"{date_start} to {date_end}",
        generated_at=datetime.now(),
        main_stories=main_stories,
        international_stories=intl_stories,
        domestic_stories=dom_stories,
        between_the_lines=btl,
        leader_dossiers=list(dossiers.values()),
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
        save_final_brief(brief)

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
                "story_count": len(dossier.main_stories)
                    + len(dossier.international_stories)
                    + len(dossier.domestic_stories),
            })

        aggregate_stats = {
            "main_stories": len(main_stories),
            "international_stories": len(intl_stories),
            "domestic_stories": len(dom_stories),
            "between_the_lines": len(btl),
        }

        create_pipeline_summary(
            leader_stats=leader_stats,
            thread_stats=aggregate_stats,
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
1. Fetched snippets from {len(sources)} sources via SearchAPI
2. Embedded snippets using sentence-transformers (English or multilingual model per leader)
3. Clustered snippets into events using HDBSCAN
4. Scored events by source diversity and wire coverage
5. Fetched {total_articles} full articles for top events via Diffbot
6. Extracted entities and summaries via Diffbot NLP
7. Built per-leader story-centric dossiers from processed events
8. Matched overlapping stories across leaders via entity overlap
9. Synthesized aggregate briefing with shared multi-leader stories

**Architecture**: Story-centric pipeline where events are synthesized into
stories, then matched across leaders for aggregate briefing.

**Limitations**: Embedding-based clustering may miss nuance in short
snippets. Non-English content processed after extraction. Entity-based
story matching may miss thematic connections without shared entities.
"""
