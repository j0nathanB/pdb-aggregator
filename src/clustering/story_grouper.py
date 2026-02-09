"""
Story Grouper - LLM-based story relationship detection.

Two use cases:
1. Story Arc Detection (per-leader): Merge multi-day developing stories
2. Cross-Leader Validation (aggregate): Confirm entity-matched stories are thematically related
"""

import logging
from typing import Optional

from ..agents.base import complete, extract_json_from_response

logger = logging.getLogger(__name__)


GROUPER_SYSTEM = """You are an experienced news editor analyzing story relationships.
Your job is to identify when separate news items are actually part of the same story.

Be precise:
- Same story = same situation, event, or developing narrative
- Different story = different topics, even if same actors are involved
- A leader meeting with different people about different topics = different stories
- A leader's multi-day trip covering the same visit = same story
"""


async def detect_story_arcs(
    event_titles: list[str],
    leader_name: str,
) -> list[list[int]]:
    """
    Detect story arcs: groups of events that are part of the same developing story.

    Used during per-leader processing to merge multi-day coverage of the same situation.

    Args:
        event_titles: List of event titles/descriptions
        leader_name: Name of the leader

    Returns:
        List of index groups that should be merged. Each group is a list of indices
        into event_titles. Events not in any group remain standalone.

    Example:
        Input: ["Orsi arrives in China", "Orsi meets Xi", "Orsi visits Shanghai port"]
        Output: [[0, 1, 2]]  # All three are the same China visit story
    """
    if len(event_titles) < 2:
        return []

    # Format events for prompt
    events_text = "\n".join(f"{i}. {title}" for i, title in enumerate(event_titles))

    prompt = f"""Analyze these news events about {leader_name} from the past week.

EVENTS:
{events_text}

Identify which events are part of the SAME developing story (e.g., a multi-day trip, an ongoing negotiation, a crisis with multiple updates).

Rules:
- Only group events that are clearly the same ongoing situation
- A leader's activities on different topics are DIFFERENT stories, even if on the same day
- A multi-day state visit to one country = same story
- Trade negotiations with country A vs. meetings about country B = different stories

Return JSON:
{{
    "story_arcs": [
        {{
            "indices": [0, 2, 5],
            "theme": "Brief description of what ties these together"
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
            max_tokens=800,
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
) -> bool:
    """
    Validate that stories from different leaders are thematically related.

    Used during aggregate processing to confirm entity-matched stories should be merged.

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
            max_tokens=300,
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


async def merge_story_arc_titles(
    titles: list[str],
    leader_name: str,
) -> str:
    """
    Generate a merged title for a story arc.

    Args:
        titles: List of event titles in the arc
        leader_name: Name of the leader

    Returns:
        A single title that encompasses the full arc
    """
    if len(titles) == 1:
        return titles[0]

    titles_text = "\n".join(f"- {t}" for t in titles)

    prompt = f"""These events about {leader_name} are part of the same developing story.
Write a single headline that encompasses the full story arc.

EVENTS:
{titles_text}

Return JSON:
{{
    "merged_title": "Single headline covering the full arc, max 12 words"
}}
"""

    try:
        response = await complete(
            prompt=prompt,
            system=GROUPER_SYSTEM,
            temperature=0.2,
            max_tokens=200,
        )
        data = extract_json_from_response(response)

        if data and "merged_title" in data:
            return data["merged_title"]

    except Exception as e:
        logger.warning(f"Title merge failed: {e}")

    # Fallback: use the first title
    return titles[0]
