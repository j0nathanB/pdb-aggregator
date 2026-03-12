"""
Data classes for Running Analytical Picture entries and consolidation summaries.

Matches the v3 schema from runtime_pipeline_prompts_v3.md.
"""

import re
from dataclasses import dataclass, field
from typing import Optional


class ThreadStatus:
    """Thread lifecycle states."""
    NEW = "NEW"
    ACTIVE = "ACTIVE"
    DORMANT = "DORMANT"
    REACTIVATED = "REACTIVATED"
    RESOLVED = "RESOLVED"
    MERGED = "MERGED"


@dataclass
class RunningPictureEntry:
    """A single parsed weekly entry from a running picture file."""

    # Frontmatter fields
    leader: str
    country: str
    week_of: str  # YYYY-MM-DD
    generated_at: str  # ISO timestamp
    event_count: int = 0
    source_count: int = 0

    # Raw text (full markdown including frontmatter)
    raw_text: str = ""

    # Parsed sections
    activity_level: str = ""
    key_actions: str = ""
    commitments: str = ""
    relationships: str = ""
    domestic_position: str = ""
    developing_threads: str = ""  # Full section (ACTIVE + DORMANT)
    missing_thread_audit: str = ""
    structural_claim_check: str = ""
    analytical_notes: str = ""


@dataclass
class ConsolidationSummary:
    """A 4-week consolidation summary."""

    leader: str
    country: str
    period_start: str  # YYYY-MM-DD
    period_end: str  # YYYY-MM-DD
    generated_at: str
    consolidates_entries: list[str] = field(default_factory=list)  # week_of dates
    raw_text: str = ""

    # Parsed sections
    period_trajectory: str = ""
    stable_assessments: str = ""
    resolved_threads: str = ""
    escalated_threads: str = ""
    newly_dormant_threads: str = ""
    commitment_ledger: str = ""
    structural_claim_status: str = ""
    analytical_inertia_check: str = ""
    slow_burn_review: str = ""


def leader_slug(name: str) -> str:
    """Convert a leader name to a filesystem-safe slug."""
    return name.lower().replace(" ", "_")


def parse_frontmatter(text: str) -> Optional[dict[str, str]]:
    """
    Extract YAML-like frontmatter from markdown text.

    Returns dict of key-value pairs, or None if no frontmatter block found.
    """
    # Handle empty frontmatter (---\n---)
    empty_match = re.match(r"^---\s*\n---", text)
    if empty_match:
        return {}

    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None

    fm = {}
    body = match.group(1).strip()
    if not body:
        return fm

    for line in body.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()

    return fm


def parse_sections(text: str) -> dict[str, str]:
    """Extract ### sections from markdown text into a dict."""
    sections = {}
    pattern = re.compile(r"^### (.+?)$", re.MULTILINE)
    matches = list(pattern.finditer(text))

    for i, match in enumerate(matches):
        section_name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[section_name] = text[start:end].strip()

    return sections


def parse_entry(raw_text: str) -> RunningPictureEntry:
    """
    Parse raw markdown into a RunningPictureEntry.

    Raises ValueError if frontmatter is missing.
    """
    fm = parse_frontmatter(raw_text)
    if fm is None:
        raise ValueError("Entry has no frontmatter")

    sections = parse_sections(raw_text)

    return RunningPictureEntry(
        leader=fm.get("leader", ""),
        country=fm.get("country", ""),
        week_of=fm.get("week_of", ""),
        generated_at=fm.get("generated_at", ""),
        event_count=int(fm.get("event_count", 0)),
        source_count=int(fm.get("source_count", 0)),
        raw_text=raw_text,
        activity_level=sections.get("Activity Level", ""),
        key_actions=sections.get("Key Actions", ""),
        commitments=sections.get("Commitments & Positions", ""),
        relationships=sections.get("Relationships", ""),
        domestic_position=sections.get("Domestic Political Position", ""),
        developing_threads=sections.get("Developing Threads", ""),
        missing_thread_audit=sections.get("Missing Thread Audit", ""),
        structural_claim_check=sections.get("Structural Claim Check", ""),
        analytical_notes=sections.get("Analytical Notes", ""),
    )


def parse_consolidation(raw_text: str) -> ConsolidationSummary:
    """
    Parse raw markdown into a ConsolidationSummary.

    Raises ValueError if frontmatter is missing.
    """
    fm = parse_frontmatter(raw_text)
    if fm is None:
        raise ValueError("Consolidation summary has no frontmatter")

    # Parse consolidates_entries from frontmatter
    # Stored as comma-separated or bracketed list
    entries_raw = fm.get("consolidates_entries", "")
    entries_raw = entries_raw.strip("[]")
    consolidates = [e.strip() for e in entries_raw.split(",") if e.strip()]

    # Parse period from frontmatter
    period = fm.get("period", "")
    period_start = ""
    period_end = ""
    if " to " in period:
        parts = period.split(" to ")
        period_start = parts[0].strip()
        period_end = parts[1].strip()

    sections = parse_sections(raw_text)

    return ConsolidationSummary(
        leader=fm.get("leader", ""),
        country=fm.get("country", ""),
        period_start=period_start,
        period_end=period_end,
        generated_at=fm.get("generated_at", ""),
        consolidates_entries=consolidates,
        raw_text=raw_text,
        period_trajectory=sections.get("Period Trajectory", ""),
        stable_assessments=sections.get("Stable Assessments", ""),
        resolved_threads=sections.get("Resolved Threads", ""),
        escalated_threads=sections.get("Escalated Threads", ""),
        newly_dormant_threads=sections.get("Newly Dormant Threads", ""),
        commitment_ledger=sections.get("Commitment Ledger Update", ""),
        structural_claim_status=sections.get("Structural Claim Status", ""),
        analytical_inertia_check=sections.get("Analytical Inertia Check", ""),
        slow_burn_review=sections.get("Slow-Burn Review", ""),
    )
