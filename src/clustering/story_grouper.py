"""
Story Grouper - LLM-based cross-leader story validation.

Confirms that entity-matched stories from different leaders are thematically related.
"""

import logging

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


