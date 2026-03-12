"""
Pre-filter — Pure Python tier assignment after Phase 1 completes.

Reads Call A (thread tracking) and Call B (analytical assessment) outputs
for each leader and assigns them to one of three tiers:

- Tier 1 (Full Assessment): High-signal leaders needing full Phase 2 treatment
- Tier 2 (Condensed Summary): Moderate-signal leaders getting condensed output
- Tier 3 (Minimal Stub): Low-signal leaders reduced to a stub

No LLM calls — all logic is regex parsing and rule evaluation.
"""

import logging
import random
import re
from dataclasses import dataclass
from enum import IntEnum

from ..config import LeaderConfig

logger = logging.getLogger(__name__)


# =============================================================================
# Data types
# =============================================================================

class Tier(IntEnum):
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3


@dataclass
class TieredLeader:
    leader: LeaderConfig
    tier: Tier
    call_b_output: str  # Full Call B output
    call_a_output: str  # Full Call A output (for thread info)
    rendered: str  # Full for T1, condensed for T2, stub for T3


# =============================================================================
# Section extraction helpers
# =============================================================================

def _extract_section(text: str, section_name: str, *, bold: bool = True) -> str:
    """
    Extract content between a section header and the next section header.

    Args:
        text: Full output text to parse.
        section_name: Name of the section (e.g. "ATTENTION FLAGS").
        bold: If True, look for **SECTION NAME** markers (Call B format).
              If False, look for ### Section Name markers (Call A format).

    Returns:
        The section body text, or empty string if not found.
    """
    if bold:
        # Call B format: **SECTION NAME**
        pattern = re.compile(
            r"\*\*" + re.escape(section_name) + r"\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\Z)",
            re.DOTALL,
        )
    else:
        # Call A format: ### Section Name
        pattern = re.compile(
            r"###\s+" + re.escape(section_name) + r"\s*\n(.*?)(?=\n###\s|\Z)",
            re.DOTALL,
        )
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


# =============================================================================
# Extraction functions
# =============================================================================

def extract_attention_flags(call_b_text: str) -> list[str]:
    """
    Parse the ATTENTION FLAGS section from Call B output.

    Returns a list of flag types found (e.g. ["WATCH", "STRUCTURAL", "ALERT"]).
    Only returns recognized flag types; unrecognized tokens are ignored.
    """
    section = _extract_section(call_b_text, "ATTENTION FLAGS")
    if not section:
        return []

    valid_flags = {"WATCH", "ALERT", "STRUCTURAL"}
    # Look for flag keywords — they appear as standalone tokens or labels
    found = []
    for flag in valid_flags:
        if re.search(r"\b" + flag + r"\b", section, re.IGNORECASE):
            found.append(flag)
    return sorted(found)


def extract_deviation_classifications(call_b_text: str) -> list[str]:
    """
    Parse the EVENT ANALYSIS section for deviation classifications.

    Returns list of classifications found (e.g. ["CONTINUITY", "SIGNIFICANT SHIFT"]).
    """
    section = _extract_section(call_b_text, "EVENT ANALYSIS")
    if not section:
        return []

    valid_classifications = [
        "POTENTIAL STRUCTURAL CHANGE",
        "SIGNIFICANT SHIFT",
        "TACTICAL ADJUSTMENT",
        "CONTINUITY",
    ]
    found = []
    for classification in valid_classifications:
        if re.search(r"\b" + re.escape(classification) + r"\b", section, re.IGNORECASE):
            found.append(classification)
    return found


def count_cross_leader_mentions(
    leader_name: str, all_call_b_outputs: dict[str, str]
) -> int:
    """
    Count how many OTHER leaders mention this leader in their
    CROSS-LEADER RELEVANCE section.
    """
    count = 0
    for other_name, other_text in all_call_b_outputs.items():
        if other_name == leader_name:
            continue
        section = _extract_section(other_text, "CROSS-LEADER RELEVANCE")
        if section and re.search(re.escape(leader_name), section):
            count += 1
    return count


def count_active_threads(call_a_text: str) -> int:
    """
    Count items under the active threads portion of the Developing Threads
    section in Call A output.

    Active threads are listed as bullet points (- or *) or numbered items
    under an "Active Threads" or "ACTIVE THREADS" sub-heading.
    """
    # First try to find an explicit "Active Threads" sub-section
    active_match = re.search(
        r"(?:ACTIVE THREADS|Active Threads)[:\s]*\n(.*?)(?=\n(?:Resolved|RESOLVED|Dormant|DORMANT|###|\*\*[A-Z])|\Z)",
        call_a_text,
        re.DOTALL,
    )
    if active_match:
        block = active_match.group(1)
    else:
        # Fall back to the full Developing Threads section
        block = _extract_section(call_a_text, "Developing Threads", bold=False)
        if not block:
            block = _extract_section(call_a_text, "DEVELOPING THREADS")

    if not block:
        return 0

    # Count bullet points or numbered items
    items = re.findall(r"^\s*(?:[-*]|\d+[.)]) .+", block, re.MULTILINE)
    return len(items)


def extract_thread_titles(call_a_text: str) -> list[str]:
    """
    Extract active thread titles from the Developing Threads section of Call A.

    Returns list of thread title strings.
    """
    active_match = re.search(
        r"(?:ACTIVE THREADS|Active Threads)[:\s]*\n(.*?)(?=\n(?:Resolved|RESOLVED|Dormant|DORMANT|###|\*\*[A-Z])|\Z)",
        call_a_text,
        re.DOTALL,
    )
    if active_match:
        block = active_match.group(1)
    else:
        block = _extract_section(call_a_text, "Developing Threads", bold=False)
        if not block:
            block = _extract_section(call_a_text, "DEVELOPING THREADS")

    if not block:
        return []

    titles = []
    for line in block.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+[.)]) (.+)", line)
        if m:
            raw = m.group(1).strip()
            # Strip bold markers
            raw = re.sub(r"\*\*(.+?)\*\*", r"\1", raw)
            # Take only the title part (before first colon if present)
            title = raw.split(":")[0].strip()
            titles.append(title)
    return titles


def extract_activity_summary(call_b_text: str) -> str:
    """Extract the ACTIVITY SUMMARY paragraph from Call B output."""
    return _extract_section(call_b_text, "ACTIVITY SUMMARY")


def extract_activity_level(call_a_text: str) -> str:
    """Extract activity level from Call A output (### Activity Level section)."""
    section = _extract_section(call_a_text, "Activity Level", bold=False)
    if not section:
        # Try bold format as fallback
        section = _extract_section(call_a_text, "ACTIVITY LEVEL")
    return section.strip() if section else "Unknown"


# =============================================================================
# Rendering functions
# =============================================================================

_CONDENSED_SECTIONS = [
    "ACTIVITY SUMMARY",
    "CROSS-LEADER RELEVANCE",
    "BETWEEN THE LINES",
    "FALSIFICATION",
    "ATTENTION FLAGS",
    "KEY EVIDENCE FOR PHASE 2",
]


def compress_assessment(call_b_text: str) -> str:
    """
    Produce a Tier 2 condensed version of Call B output.

    Retains:
    - Activity Summary paragraph
    - All Cross-Leader Relevance entries (full)
    - All Between the Lines observations (full)
    - All Falsification criteria (full)
    - Attention flags
    - Key Evidence for Phase 2 block
    """
    parts: list[str] = []
    for section_name in _CONDENSED_SECTIONS:
        body = _extract_section(call_b_text, section_name)
        if body:
            parts.append(f"**{section_name}**\n{body}")
    return "\n\n".join(parts)


def generate_stub(leader: LeaderConfig, call_a_text: str, call_b_text: str) -> str:
    """
    Produce a Tier 3 minimal stub.

    Contains:
    - Leader name, title, country
    - Activity level
    - One-sentence activity summary
    - Active developing thread titles (list only)
    """
    activity_level = extract_activity_level(call_a_text)
    activity_summary = extract_activity_summary(call_b_text)

    # Take just the first sentence of the activity summary
    first_sentence = activity_summary
    if activity_summary:
        m = re.match(r"([^.!?]+[.!?])", activity_summary)
        if m:
            first_sentence = m.group(1).strip()

    thread_titles = extract_thread_titles(call_a_text)
    thread_list = ""
    if thread_titles:
        thread_list = "\n".join(f"- {t}" for t in thread_titles)

    lines = [
        f"## {leader.name}",
        f"**{leader.title}, {leader.country}**",
        f"Activity Level: {activity_level}",
        "",
        first_sentence,
    ]
    if thread_list:
        lines.extend(["", "**Active Threads:**", thread_list])

    return "\n".join(lines)


# =============================================================================
# Tier assignment logic
# =============================================================================

def _has_any_deviation_above_continuity(classifications: list[str]) -> bool:
    """Return True if any classification is above CONTINUITY."""
    above_continuity = {
        "TACTICAL ADJUSTMENT",
        "SIGNIFICANT SHIFT",
        "POTENTIAL STRUCTURAL CHANGE",
    }
    return any(c.upper() in above_continuity for c in classifications)


def _assign_tier(
    leader_name: str,
    flags: list[str],
    classifications: list[str],
    cross_mentions: int,
    active_thread_count: int,
    deviations_above_continuity: bool,
) -> Tier:
    """
    Determine the tier for a single leader based on parsed signals.

    Tier 1 — Full Assessment (any ONE of):
    - Any attention flag of STRUCTURAL or ALERT
    - Any event classified as POTENTIAL STRUCTURAL CHANGE or SIGNIFICANT SHIFT
    - Named in 1+ other leaders' Cross-Leader Relevance AND has deviation above CONTINUITY
    - Named in 3+ other leaders' Cross-Leader Relevance (hub threshold)

    Tier 3 — Minimal Stub (ALL of):
    - No attention flags
    - All events classified as CONTINUITY
    - Not named in any other leader's Cross-Leader Relevance
    - Fewer than 3 active developing threads

    Tier 2 — everything else (also elevated if 3+ active threads)
    """
    flags_upper = {f.upper() for f in flags}

    # --- Tier 1 checks ---
    if flags_upper & {"STRUCTURAL", "ALERT"}:
        return Tier.TIER_1

    high_classifications = {"POTENTIAL STRUCTURAL CHANGE", "SIGNIFICANT SHIFT"}
    if any(c.upper() in high_classifications for c in classifications):
        return Tier.TIER_1

    if cross_mentions >= 1 and deviations_above_continuity:
        return Tier.TIER_1

    if cross_mentions >= 3:
        return Tier.TIER_1

    # --- Tier 3 checks (all must be true) ---
    no_flags = len(flags) == 0
    all_continuity = all(c.upper() == "CONTINUITY" for c in classifications) if classifications else True
    not_mentioned = cross_mentions == 0
    few_threads = active_thread_count < 3

    if no_flags and all_continuity and not_mentioned and few_threads:
        return Tier.TIER_3

    # --- Default: Tier 2 ---
    return Tier.TIER_2


# =============================================================================
# Main entry point
# =============================================================================

def run_prefilter(
    leaders: list[LeaderConfig],
    call_a_outputs: dict[str, str],  # leader_name -> Call A text
    call_b_outputs: dict[str, str],  # leader_name -> Call B text
) -> list[TieredLeader]:
    """
    Assign leaders to tiers and produce rendered output for Phase 2.

    Returns list of TieredLeader sorted by tier (1 first), randomized within tiers.
    """
    results: list[TieredLeader] = []

    for leader in leaders:
        name = leader.name
        call_a = call_a_outputs.get(name, "")
        call_b = call_b_outputs.get(name, "")

        flags = extract_attention_flags(call_b)
        classifications = extract_deviation_classifications(call_b)
        cross_mentions = count_cross_leader_mentions(name, call_b_outputs)
        thread_count = count_active_threads(call_a)
        deviations_above = _has_any_deviation_above_continuity(classifications)

        tier = _assign_tier(
            leader_name=name,
            flags=flags,
            classifications=classifications,
            cross_mentions=cross_mentions,
            active_thread_count=thread_count,
            deviations_above_continuity=deviations_above,
        )

        # Render output based on tier
        if tier == Tier.TIER_1:
            rendered = call_b  # Full output
        elif tier == Tier.TIER_2:
            rendered = compress_assessment(call_b)
        else:
            rendered = generate_stub(leader, call_a, call_b)

        logger.info(
            "Pre-filter: %s -> Tier %d (flags=%s, classifications=%s, "
            "cross_mentions=%d, threads=%d)",
            name, tier, flags, classifications, cross_mentions, thread_count,
        )

        results.append(TieredLeader(
            leader=leader,
            tier=tier,
            call_b_output=call_b,
            call_a_output=call_a,
            rendered=rendered,
        ))

    # Sort by tier, randomize within each tier
    by_tier: dict[Tier, list[TieredLeader]] = {t: [] for t in Tier}
    for tl in results:
        by_tier[tl.tier].append(tl)

    ordered: list[TieredLeader] = []
    for tier in sorted(by_tier.keys()):
        group = by_tier[tier]
        random.shuffle(group)
        ordered.extend(group)

    return ordered
