"""
Synthesis nodes - source quality assessment.

Executive summary and regional contexts have been replaced by
the story-centric AggregateBriefingBuilder (in nodes/threads.py).
"""

import logging
from typing import Any

from ..config import LeaderDossier
from ..state import PDBState
from ..agents.synthesizer import SynthesizerAgent
from ..debug import save_synthesis_results, is_debug_enabled

logger = logging.getLogger(__name__)


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
