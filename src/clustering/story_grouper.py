"""
Story Grouper - LLM-based story relationship detection.

Two use cases:
1. Story Arc Detection (per-leader): Merge multi-day developing stories
2. Cross-Leader Validation (aggregate): Confirm entity-matched stories are thematically related
"""

import logging
from typing import Optional

from ..agents.base import complete, extract_json_from_response
from ..config import MODEL_ANALYTICAL, THINKING_ANALYTICAL

logger = logging.getLogger(__name__)


GROUPER_SYSTEM = """You are a senior news editor building a developing story timeline. \
Your job is to group distinct events into a single causal "Story Arc."

A Story Arc requires a causal or direct narrative link:
- "Event A happens" → "Actor reacts to Event A" → "Consequences of Event A"
- A multi-day state visit: arrival → meetings → departure
- An ongoing negotiation: proposal → counter-proposal → deal

DO NOT group events just because they share a broad theme:
- Do not group all "diplomatic visits" together unless part of the same trip
- Do not group all "military/defense" stories unless causally linked
- A leader meeting with different people about different topics = different arcs
- A news roundup that mentions an event is NOT part of that event's arc

Return your answer as JSON."""


async def detect_story_arcs(
    event_titles: list[str],
    leader_name: str,
    dates: list[str] | None = None,
    snippets: list[str] | None = None,
    model: str = MODEL_ANALYTICAL,
    thinking_budget: int = THINKING_ANALYTICAL,
) -> list[list[int]]:
    """
    Detect story arcs: groups of events that are part of the same developing story.

    Deprecated: Use cluster_reasoning.reason_about_clusters() instead, which combines
    dedup + arc detection in a single LLM call. Kept for fallback/standalone use.

    Args:
        event_titles: List of event titles/descriptions
        leader_name: Name of the leader
        dates: Optional list of date strings (e.g., "5 days ago") per event
        snippets: Optional list of snippet text per event

    Returns:
        List of index groups that should be merged. Each group is a list of indices
        into event_titles. Events not in any group remain standalone.

    Example:
        Input: ["Orsi arrives in China", "Orsi meets Xi", "Orsi visits Shanghai port"]
        Output: [[0, 1, 2]]  # All three are the same China visit story
    """
    if len(event_titles) < 2:
        return []

    # Format events with optional dates and snippets
    event_lines = []
    for i, title in enumerate(event_titles):
        date_tag = f" [{dates[i]}]" if dates and i < len(dates) and dates[i] else ""
        line = f"{i}.{date_tag} {title}"
        if snippets and i < len(snippets) and snippets[i]:
            line += f"\n   {snippets[i][:200]}"
        event_lines.append(line)

    events_text = "\n\n".join(event_lines)

    date_instruction = ""
    if dates and any(dates):
        date_instruction = "\nIMPORTANT: Pay close attention to the publication dates to determine causal flow.\n"

    prompt = f"""Analyze these distinct news events about {leader_name} from the past week.
{date_instruction}
EVENTS:
{events_text}

Identify which events are part of the SAME developing story arc. \
A story arc requires a causal or direct narrative link between events, \
not just a shared theme.

Return JSON:
{{
    "story_arcs": [
        {{
            "indices": [0, 2, 5],
            "theme": "Brief description of the arc",
            "causal_link": "Event 0 is the initial announcement, Event 2 is the reaction, Event 5 is the policy consequence."
        }}
    ]
}}

If no events should be grouped, return: {{"story_arcs": []}}
"""

    try:
        response = await complete(
            prompt=prompt,
            system=GROUPER_SYSTEM,
            temperature=0.2,
            model=model,
            thinking_budget=thinking_budget,
        )
        data = extract_json_from_response(response)

        if data and "story_arcs" in data:
            arcs = []
            for arc in data["story_arcs"]:
                indices = arc.get("indices", [])
                if len(indices) >= 2:
                    # Validate indices are in range
                    valid_indices = [i for i in indices if 0 <= i < len(event_titles)]
                    if len(valid_indices) >= 2:
                        arcs.append(valid_indices)
                        logger.info(
                            f"Story arc detected for {leader_name}: "
                            f"{arc.get('theme', 'unknown')} ({len(valid_indices)} events)"
                        )
            return arcs

    except Exception as e:
        logger.warning(f"Story arc detection failed for {leader_name}: {e}")

    return []


async def validate_cross_leader_match(
    story_summaries: list[tuple[str, str, str]],
    model: str = MODEL_ANALYTICAL,
    thinking_budget: int = THINKING_ANALYTICAL,
) -> bool:
    """
    Validate that stories from different leaders are thematically related.

    Deprecated for aggregate flow: _validate_and_synthesize_group() in aggregate_builder
    now combines validation + synthesis in a single call. Kept for standalone use.

    Args:
        story_summaries: List of (leader_name, title, narrative_excerpt) tuples

    Returns:
        True if stories are about the same topic/situation, False otherwise
    """
    if len(story_summaries) < 2:
        return True  # Single story, nothing to validate

    # Format stories for prompt
    stories_text = "\n\n".join(
        f"**{leader}**: {title}\n{narrative[:200]}..."
        for leader, title, narrative in story_summaries
    )

    prompt = f"""Are these news stories from different leaders about the SAME topic or situation?

STORIES:
{stories_text}

Rules:
- Same topic = same event, negotiation, crisis, or policy area
- Different topic = stories that just happen to mention the same country/person but cover different issues
- Example SAME: Both stories about US-Canada trade tensions
- Example DIFFERENT: One story about trade, another about immigration, even if both mention same countries

Return JSON:
{{
    "same_topic": true or false,
    "reason": "Brief explanation"
}}
"""

    try:
        response = await complete(
            prompt=prompt,
            system=GROUPER_SYSTEM,
            temperature=0.1,
            model=model,
            thinking_budget=thinking_budget,
        )
        data = extract_json_from_response(response)

        if data and "same_topic" in data:
            result = data["same_topic"]
            if not result:
                logger.info(
                    f"Cross-leader match rejected: {data.get('reason', 'no reason')}"
                )
            return result

    except Exception as e:
        logger.warning(f"Cross-leader validation failed: {e}")

    # Default to True (allow match) on failure to avoid breaking existing behavior
    return True


