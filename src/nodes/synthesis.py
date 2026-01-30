"""
Synthesis nodes - generate executive summary, regional contexts, and source quality.
"""

import logging
from typing import Any

from ..config import LeaderDossier, CrossCuttingThread
from ..state import PDBState
from ..agents.synthesizer import SynthesizerAgent
from ..debug import save_synthesis_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def generate_executive_summary(state: PDBState) -> dict[str, Any]:
    """
    Generate executive summary from threads and dossiers.

    Args:
        state: PDB state with all_threads and dossiers

    Returns:
        Updated state with executive_summary field populated
    """
    threads = state.get("all_threads", [])
    dossiers = state.get("dossiers", {})
    date_start = state.get("date_range_start", "")
    date_end = state.get("date_range_end", "")
    date_range = f"{date_start} to {date_end}"

    logger.info("Generating executive summary")

    try:
        synthesizer = SynthesizerAgent()

        # Generate summary WITHOUT global_pulse (bottom-up)
        summary = await synthesizer.generate_executive_summary(
            threads=threads,
            dossiers=dossiers,
            global_pulse=None,  # Bottom-up: no top-down context
            date_range=date_range,
        )

        logger.info(f"Generated executive summary ({len(summary)} chars)")

        # Save debug output
        if is_debug_enabled():
            save_synthesis_results(
                step="executive_summary",
                content={
                    "summary": summary,
                    "thread_count": len(threads),
                    "dossier_count": len(dossiers),
                    "date_range": date_range,
                },
            )

        return {"executive_summary": summary}

    except Exception as e:
        logger.error(f"Executive summary generation failed: {e}")
        return {"executive_summary": "Executive summary generation failed."}


async def generate_regional_contexts(state: PDBState) -> dict[str, Any]:
    """
    Generate regional context sections.

    Args:
        state: PDB state with dossiers and all_threads

    Returns:
        Updated state with regional_contexts field populated
    """
    dossiers = state.get("dossiers", {})
    threads = state.get("all_threads", [])

    logger.info("Generating regional contexts")

    try:
        synthesizer = SynthesizerAgent()

        contexts = await synthesizer.generate_regional_contexts(
            dossiers=dossiers,
            threads=threads,
        )

        logger.info(f"Generated {len(contexts)} regional contexts")

        # Save debug output
        if is_debug_enabled():
            save_synthesis_results(
                step="regional_contexts",
                content=contexts,
            )

        return {"regional_contexts": contexts}

    except Exception as e:
        logger.error(f"Regional context generation failed: {e}")
        return {"regional_contexts": {}}


async def assess_source_quality(state: PDBState) -> dict[str, Any]:
    """
    Assess source quality across all dossiers.

    Args:
        state: PDB state with dossiers

    Returns:
        Updated state with source_quality_notes field populated
    """
    dossiers = state.get("dossiers", {})

    logger.info("Assessing source quality")

    try:
        synthesizer = SynthesizerAgent()

        quality_notes = await synthesizer.generate_source_quality_assessment(dossiers)

        # Save debug output
        if is_debug_enabled():
            save_synthesis_results(
                step="source_quality",
                content=quality_notes,
            )

        return {"source_quality_notes": quality_notes}

    except Exception as e:
        logger.error(f"Source quality assessment failed: {e}")
        return {"source_quality_notes": "Source quality assessment failed."}
