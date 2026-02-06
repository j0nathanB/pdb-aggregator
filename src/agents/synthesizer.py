"""
Synthesizer Agent - Source quality assessment.

Executive summary and regional contexts have been replaced by
the story-centric AggregateBriefingBuilder.
"""

import logging

from ..config import LeaderDossier
from .base import complete, with_retry

logger = logging.getLogger(__name__)


class SynthesizerAgent:
    """
    Generates source quality assessment for the weekly brief.

    Executive summary and regional context generation have been removed
    in favor of the story-centric aggregate briefing structure.
    """

    async def generate_source_quality_assessment(
        self,
        dossiers: dict[str, LeaderDossier],
    ) -> str:
        """
        Generate a source quality assessment section.

        Notes any gaps, biases, or reliability concerns.
        """
        concerns = []

        for name, dossier in dossiers.items():
            # Check for state media
            state_media_count = sum(
                1 for a in dossier.articles
                if a.source_type == "state_media"
            )
            if state_media_count > 0:
                concerns.append(
                    f"**{name}**: {state_media_count} state media articles included - "
                    "content may reflect official messaging rather than ground truth."
                )

            # Check for limited coverage
            if len(dossier.articles) < 3:
                concerns.append(
                    f"**{name}**: Limited source coverage ({len(dossier.articles)} articles) - "
                    "assessment confidence is lower."
                )

            # Include any dossier-specific notes
            if dossier.source_quality_notes and "Good source" not in dossier.source_quality_notes:
                concerns.append(f"**{name}**: {dossier.source_quality_notes}")

        if not concerns:
            return "Source coverage was adequate across all leaders with no significant gaps or reliability concerns."

        return "\n".join(concerns)
