"""
Phase 0 — Global Context Brief.

Triggered conditionally by the Cross-Correlation Pass when a major event
affects multiple monitored leaders. Produces a shared baseline brief that
gets injected into all Phase 1 per-leader analytical calls.
"""

import logging

from ..agents.base import complete, with_retry
from ..config import MODEL_SYNTHESIS, THINKING_SYNTHESIS

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are producing a concise Global Context Brief for a weekly
intelligence production cycle. A major event this week affects
multiple national leaders being monitored. Your brief will be
injected into per-leader analytical calls so that each analyst
has a shared baseline understanding of the event without
describing it independently.

Produce a factual, analytical summary of the shared event:
- What happened (concrete facts, dates, key actors)
- Why it matters for the international system
- What decisions or responses it demands from national leaders

Do NOT assess individual leaders' responses — that is the job of
the per-leader analysts.

Target length: 500-800 words."""

USER_PROMPT_TEMPLATE = """\
## CROSS-CUTTING EVENTS THIS WEEK

The following event clusters were identified as requiring shared
context across multiple monitored leaders:

{triggered_clusters}

Produce the Global Context Brief for this week's cycle."""


def format_user_prompt(triggered_clusters: str) -> str:
    """Format the Phase 0 user prompt with triggered cluster events."""
    return USER_PROMPT_TEMPLATE.format(triggered_clusters=triggered_clusters)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

@with_retry(max_attempts=2)
async def run_phase_0(triggered_clusters: str) -> str:
    """
    Produce a Global Context Brief from triggered cluster events.

    Args:
        triggered_clusters: Text describing the cross-cutting events
            that triggered Phase 0 (from CrossCorrelationResult.triggered_clusters)

    Returns:
        Global Context Brief text (500-800 words)
    """
    user_prompt = format_user_prompt(triggered_clusters)

    logger.info("Phase 0: generating Global Context Brief")

    brief = await complete(
        prompt=user_prompt,
        system=SYSTEM_PROMPT,
        model=MODEL_SYNTHESIS,
        thinking_budget=THINKING_SYNTHESIS,
    )

    logger.info("Phase 0: Global Context Brief generated (%d chars)", len(brief))
    return brief
