"""
Context assembly for Phase 1 per-leader LLM calls.

Builds the system prompt (cached, identical for Call A and Call B)
and user prompts (role-specific) from baseline docs, running picture,
events, and thread checklist.
"""

from typing import Optional

from ..config import LeaderConfig
from ..agents.event_clustering import ProcessedEvent
from .claims import extract_claims, format_claims_index, get_valid_claim_refs, Claim
from ..running_picture.schema import RunningPictureEntry, ConsolidationSummary
from ..running_picture.extraction import (
    extract_thread_checklist,
    format_thread_checklist,
    extract_commitment_ledger,
    format_commitment_ledger,
)
from ..running_picture.storage import load_weekly_entries, load_weekly_text, load_consolidation


def build_system_prompt(
    country_dossier: str,
    leader_profile: str,
    country: str,
    leader_name: str,
) -> str:
    """
    Build the cached system prompt for Phase 1 Call A and Call B.

    This prompt is identical for both calls per leader to maximize
    prompt cache hits. Role-specific instructions go in user prompts.

    Args:
        country_dossier: Full markdown text of the country structural dossier
        leader_profile: Full markdown text of the leader operational profile
        country: Country name (e.g., "Mexico")
        leader_name: Leader name (e.g., "Claudia Sheinbaum")

    Returns:
        Complete system prompt string.
    """
    structural_claims = extract_claims(country_dossier, "STRUC")
    profile_claims = extract_claims(leader_profile, "PROF")
    claims_index = format_claims_index(
        structural_claims, profile_claims, country, leader_name,
    )

    return (
        f"## STRUCTURAL CONTEXT: {country}\n\n"
        f"{country_dossier}\n\n"
        f"---\n\n"
        f"## LEADER CONTEXT: {leader_name}\n\n"
        f"{leader_profile}\n\n"
        f"---\n\n"
        f"{claims_index}"
    )


def build_call_a_user_prompt(
    leader: LeaderConfig,
    events: list[ProcessedEvent],
    date_start: str,
    date_end: str,
    running_picture_text: str,
    thread_checklist: str,
    global_context: Optional[str] = None,
) -> str:
    """
    Build the user prompt for Phase 1 Call A (structured data logger).

    Args:
        leader: Leader configuration
        events: Classified events for this leader this week
        date_start: Week start date (YYYY-MM-DD)
        date_end: Week end date (YYYY-MM-DD)
        running_picture_text: Formatted recent entries text
        thread_checklist: Formatted thread checklist from prior entry
        global_context: Optional global context brief from Phase 0

    Returns:
        Complete user prompt string.
    """
    events_text = _format_events(events)

    parts = [
        "You are a structured intelligence data logger. Process this week's\n"
        "events and produce a Running Picture Entry following the schema\n"
        "exactly.\n"
        "\n"
        "Requirements:\n"
        "- Key Actions must be concrete and verifiable with source attribution\n"
        "- Commitments must include Audience and Binding Force fields\n"
        "- Use [STRUC-XX] and [PROF-XX] prefixes for all claim references\n"
        "- Address every thread in the Thread Checklist below\n"
        "- Analytical Notes must NOT repeat insights from previous 3 weeks\n"
        "  unless material new evidence exists\n"
        "\n"
        "---\n"
        "\n"
        f"## RUNNING CONTEXT: {leader.name} — Recent Weeks\n"
        "\n"
        f"{running_picture_text}\n"
        "\n"
        "---",
    ]

    if global_context:
        parts.append(
            f"\n## GLOBAL CONTEXT: Week of {date_start}\n"
            f"\n"
            f"{global_context}\n"
            f"\n"
            f"---"
        )

    parts.append(
        f"\n## THIS WEEK'S EVENTS: {leader.name}\n"
        f"Reporting period: {date_start} to {date_end}\n"
        f"\n"
        f"{events_text}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## THREAD CHECKLIST (from prior entry — you MUST address each)\n"
        f"{thread_checklist}\n"
        f"\n"
        f"For each: provide updated status in the Missing Thread Audit\n"
        f"(ACTIVE / DORMANT / RESOLVED / MERGED)\n"
        f"\n"
        f"---\n"
        f"\n"
        f"Produce the Running Picture Entry for {leader.name} ({leader.title},\n"
        f"{leader.country}) for the week of {date_start} to {date_end}."
    )

    return "\n".join(parts)


def build_call_b_user_prompt(
    leader: LeaderConfig,
    call_a_output: str,
    events: list[ProcessedEvent],
    date_start: str,
    date_end: str,
    running_picture_text: str,
    global_context: Optional[str] = None,
) -> str:
    """
    Build the user prompt for Phase 1 Call B (analytical assessment).

    Args:
        leader: Leader configuration
        call_a_output: Raw text output from Call A
        events: Classified events (included as raw reference)
        date_start: Week start date (YYYY-MM-DD)
        date_end: Week end date (YYYY-MM-DD)
        running_picture_text: Formatted recent entries text
        global_context: Optional global context brief from Phase 0

    Returns:
        Complete user prompt string.
    """
    events_text = _format_events(events)

    parts = [
        "You are an intelligence analyst producing a weekly analytical\n"
        "assessment. You have structural context, a leader profile,\n"
        "running analytical picture, and a structured summary of this\n"
        "week's developments.\n"
        "\n"
        "Analytical method — apply to each significant event:\n"
        "\n"
        "1. WHAT HAPPENED: State the concrete action from this week's\n"
        "   reporting.\n"
        "\n"
        "2. STRUCTURAL FIT: Does this align with or deviate from\n"
        "   persistent patterns in the country dossier and leader\n"
        "   profile? Cite specific [STRUC-XX] and [PROF-XX] claims.\n"
        "\n"
        "3. TRAJECTORY FIT: Does this continue, escalate, reverse, or\n"
        "   break from the recent trajectory in the running picture?\n"
        "   Reference specific prior entries or threads.\n"
        "\n"
        "4. COMBINED ASSESSMENT: What does the intersection of structural\n"
        "   context and recent trajectory tell you? Classify as:\n"
        "   CONTINUITY / DEVIATION (with level: TACTICAL ADJUSTMENT /\n"
        "   SIGNIFICANT SHIFT / POTENTIAL STRUCTURAL CHANGE)\n"
        "\n"
        "5. FALSIFICATION: What would you expect to see in the next\n"
        "   1-2 weeks if your assessment is WRONG?\n"
        "\n"
        "Anti-anchoring discipline:\n"
        "- Do not default to CONTINUITY simply because the running\n"
        "  picture establishes a strong prior\n"
        "- Genuinely novel signals can emerge at any time\n"
        "\n"
        "---\n"
        "\n"
        f"## RUNNING CONTEXT: {leader.name} — Recent Weeks\n"
        "\n"
        f"{running_picture_text}\n"
        "\n"
        "---",
    ]

    if global_context:
        parts.append(
            f"\n## GLOBAL CONTEXT: Week of {date_start}\n"
            f"\n"
            f"{global_context}\n"
            f"\n"
            f"---"
        )

    parts.append(
        f"\n## THIS WEEK'S STRUCTURED SUMMARY\n"
        f"\n"
        f"{call_a_output}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"## RAW EVENTS (for reference)\n"
        f"\n"
        f"{events_text}\n"
        f"\n"
        f"---\n"
        f"\n"
        f"Produce an analytical assessment for {leader.name} ({leader.title},\n"
        f"{leader.country}) for the week of {date_start} to {date_end}.\n"
        f"\n"
        f"Structure:\n"
        f"\n"
        f"**ACTIVITY SUMMARY**\n"
        f"One paragraph: what they did, what it means, trajectory fit.\n"
        f"\n"
        f"**EVENT ANALYSIS**\n"
        f"For each significant event:\n"
        f"- Context: [STRUC-XX] and [PROF-XX] references\n"
        f"- Running picture fit: thread connection, trajectory\n"
        f"- Assessment: CONTINUITY or DEVIATION (level)\n"
        f"- Falsification: If wrong, what would I see next? [1-2 sentences]\n"
        f"- Forward implications: [Flag as PROJECTION]\n"
        f"\n"
        f"**CROSS-LEADER RELEVANCE**\n"
        f"- Which leader(s) affected?\n"
        f"- Nature of connection\n"
        f"- What should the aggregate brief highlight?\n"
        f"\n"
        f"**BETWEEN THE LINES**\n"
        f"1-3 observations requiring full context stack. Must reference\n"
        f"specific claims or running picture entries. Do not repeat prior\n"
        f"weeks' observations.\n"
        f"\n"
        f"**ATTENTION FLAGS**\n"
        f"- WATCH: Developing situation\n"
        f"- ALERT: Significant deviation\n"
        f"- STRUCTURAL: Challenges foundational assumption\n"
        f"\n"
        f"**KEY EVIDENCE FOR PHASE 2**\n"
        f"3 most significant direct quotes, actions, or data points.\n"
        f"Format: [Leader action/quote] — [Source] — [Date]"
    )

    return "\n".join(parts)


def _format_events(events: list[ProcessedEvent]) -> str:
    """Format classified events for prompt injection."""
    if not events:
        return "[No classified events for this leader this week.]"

    lines = []
    for i, event in enumerate(events, 1):
        lines.append(f"### Event {i}: {event.title}")
        lines.append(f"Score: {event.score:.2f} | Sources: {event.source_count} | Wire: {'Yes' if event.has_wire else 'No'}")
        lines.append(f"Summary: {event.summary}")
        if event.articles:
            lines.append("Sources:")
            for article in event.articles[:5]:
                source = article.get("source", "Unknown")
                title = article.get("title", "")
                lines.append(f"  - [{source}] {title}")
        lines.append("")

    return "\n".join(lines).rstrip()
