"""
Cross-Correlation Pass — identifies thematic clusters across leaders.

Takes all classified events across all leaders, finds thematic clusters
where 2+ leaders are involved, and recommends whether Phase 0 (global
context) should be triggered.
"""

import logging
import re
from dataclasses import dataclass

from ..agents.base import complete
from ..agents.event_clustering import ProcessedEvent
from ..config import LeaderConfig, MODEL_SYNTHESIS

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a thematic clustering engine for a weekly intelligence
pipeline. You will receive a chronological list of classified
news events across multiple national leaders.

Your task is to identify events that share themes, entities, or
represent parallel actions across 2+ leaders — even when the
leaders use different terminology or framing for similar actions.

Produce two outputs:

OUTPUT 1 — THEMATIC CLUSTERS BRIEF
Group events into 3-8 thematic clusters where 2+ leaders are
involved. For each cluster:
- Cluster title (concise, descriptive)
- Leaders involved
- Brief description of the shared theme or parallel action
- Assessment: ROUTINE (expected regional coordination) or
  NOTABLE (represents convergence, divergence, or coordinated
  response worth highlighting)

Only include clusters involving 2+ leaders. Ignore events that
are purely domestic with no cross-leader dimension.

OUTPUT 2 — PHASE 0 TRIGGER RECOMMENDATION
Assess whether any cluster is significant enough to warrant a
shared Global Context Brief. Criteria:
- 3+ leaders responding to the same external event or crisis
- A cluster marked NOTABLE that involves a major shift in
  regional dynamics
- A systemic event (summit, crisis, institutional decision)
  that multiple leaders must respond to

Respond with: TRIGGER PHASE 0: [Yes/No]
If yes, identify which cluster(s) warrant the Global Context Brief."""

USER_PROMPT_TEMPLATE = """\
## GLOBAL EVENT TIMELINE
Week of {date_start} to {date_end}

{chronological_event_list}"""


@dataclass
class CrossCorrelationResult:
    """Result of the cross-correlation pass."""

    clusters_brief: str  # Full thematic clusters text for Phase 2
    trigger_phase_0: bool
    triggered_clusters: str  # Text of clusters that triggered Phase 0 (empty if not triggered)


def format_event_list(
    events_by_leader: dict[str, list[ProcessedEvent]],
    leaders: list[LeaderConfig],
) -> str:
    """
    Format all events into a chronological list for the LLM prompt.

    Each line: [LEADER/COUNTRY]: [Event title] — Score: X.XX, Sources: N
    """
    leader_country = {lc.name: lc.country for lc in leaders}

    lines: list[str] = []
    for leader_name, events in events_by_leader.items():
        country = leader_country.get(leader_name, "Unknown")
        for event in events:
            line = (
                f"[{leader_name}/{country}]: {event.title} "
                f"— Score: {event.score:.2f}, Sources: {event.source_count}"
            )
            lines.append(line)

    return "\n".join(lines)


def parse_output(text: str) -> CrossCorrelationResult:
    """
    Parse the LLM output to extract clusters brief, trigger decision,
    and triggered cluster text.
    """
    # Find the trigger line (case-insensitive)
    trigger_match = re.search(
        r"TRIGGER\s+PHASE\s+0\s*:\s*(Yes|No)",
        text,
        re.IGNORECASE,
    )

    if trigger_match:
        trigger_phase_0 = trigger_match.group(1).strip().lower() == "yes"
        trigger_line_end = trigger_match.end()

        # Everything before the trigger line is the clusters brief
        clusters_brief = text[: trigger_match.start()].strip()

        # If triggered, everything after the trigger line is the triggered clusters text
        if trigger_phase_0:
            triggered_clusters = text[trigger_line_end:].strip()
        else:
            triggered_clusters = ""
    else:
        # No trigger line found — treat entire output as clusters brief, no trigger
        logger.warning("No 'TRIGGER PHASE 0' line found in cross-correlation output")
        clusters_brief = text.strip()
        trigger_phase_0 = False
        triggered_clusters = ""

    return CrossCorrelationResult(
        clusters_brief=clusters_brief,
        trigger_phase_0=trigger_phase_0,
        triggered_clusters=triggered_clusters,
    )


async def run_cross_correlation(
    events_by_leader: dict[str, list[ProcessedEvent]],
    leaders: list[LeaderConfig],
    date_start: str,
    date_end: str,
) -> CrossCorrelationResult:
    """
    Run the cross-correlation pass across all leaders' events.

    Makes a single LLM call to identify thematic clusters and
    determine whether Phase 0 (global context) should be triggered.
    """
    # Handle empty input
    total_events = sum(len(evts) for evts in events_by_leader.values())
    if total_events == 0:
        logger.warning("No events provided for cross-correlation")
        return CrossCorrelationResult(
            clusters_brief="",
            trigger_phase_0=False,
            triggered_clusters="",
        )

    # Format the event list
    event_list_text = format_event_list(events_by_leader, leaders)

    user_prompt = USER_PROMPT_TEMPLATE.format(
        date_start=date_start,
        date_end=date_end,
        chronological_event_list=event_list_text,
    )

    logger.info(
        f"Running cross-correlation on {total_events} events "
        f"across {len(events_by_leader)} leaders"
    )

    response = await complete(
        prompt=user_prompt,
        system=SYSTEM_PROMPT,
        model=MODEL_SYNTHESIS,
        max_tokens=8000,
    )

    result = parse_output(response)

    logger.info(
        f"Cross-correlation complete: {len(result.clusters_brief)} chars of clusters, "
        f"Phase 0 trigger: {result.trigger_phase_0}"
    )

    return result
