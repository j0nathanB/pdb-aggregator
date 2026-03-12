"""
Extract structured data from running picture entries for prompt injection.

Thread checklists and commitment ledgers are computed by Python (not LLM)
and injected into the Call A user prompt as hard-coded context.
"""

import re
from dataclasses import dataclass
from typing import Optional

from .schema import RunningPictureEntry, ConsolidationSummary


@dataclass
class ThreadChecklistItem:
    """A single thread to be accounted for in the Missing Thread Audit."""
    number: int
    title: str
    status: str  # Last known status text
    section: str  # "ACTIVE" or "DORMANT"


def extract_thread_checklist(
    entry: Optional[RunningPictureEntry] = None,
    consolidation: Optional[ConsolidationSummary] = None,
) -> list[ThreadChecklistItem]:
    """
    Extract all active and dormant threads from the most recent entry
    (and optionally consolidation) as a numbered checklist.

    This checklist is injected into Call A's user prompt so the LLM
    must account for every thread in its Missing Thread Audit.

    Args:
        entry: Most recent weekly entry (primary source)
        consolidation: Most recent consolidation (for dormant threads)

    Returns:
        Numbered list of ThreadChecklistItems
    """
    items = []
    counter = 1

    if entry and entry.developing_threads:
        # Parse ACTIVE THREADS
        active_threads = _extract_thread_items(
            entry.developing_threads, "ACTIVE THREADS:"
        )
        for title, status in active_threads:
            items.append(ThreadChecklistItem(
                number=counter,
                title=title,
                status=status,
                section="ACTIVE",
            ))
            counter += 1

        # Parse DORMANT THREADS
        dormant_threads = _extract_thread_items(
            entry.developing_threads, "DORMANT THREADS:"
        )
        for title, status in dormant_threads:
            items.append(ThreadChecklistItem(
                number=counter,
                title=title,
                status=status,
                section="DORMANT",
            ))
            counter += 1

    # Also pick up dormant threads from consolidation if not already covered
    if consolidation and consolidation.newly_dormant_threads:
        existing_titles = {item.title.lower() for item in items}
        dormant_from_consol = _extract_bullet_items(consolidation.newly_dormant_threads)
        for title, status in dormant_from_consol:
            if title.lower() not in existing_titles:
                items.append(ThreadChecklistItem(
                    number=counter,
                    title=title,
                    status=status,
                    section="DORMANT",
                ))
                counter += 1

    return items


def format_thread_checklist(items: list[ThreadChecklistItem]) -> str:
    """
    Format thread checklist for injection into the Call A user prompt.

    Output format (per v3 spec):
    1. [Thread title] -- Status as of last week: [status text]
    2. ...
    """
    if not items:
        return "[No threads from prior entry to carry forward.]"

    lines = []
    for item in items:
        lines.append(
            f"{item.number}. [{item.title}] — "
            f"Status as of last week: {item.status} ({item.section})"
        )
    return "\n".join(lines)


@dataclass
class CommitmentItem:
    """A single commitment from the running picture."""
    description: str
    status: str
    audience: str
    binding_force: str
    week_of: str  # When this commitment was recorded


def extract_commitment_ledger(
    entries: list[RunningPictureEntry],
) -> list[CommitmentItem]:
    """
    Build a cumulative commitment ledger from recent entries.

    Scans all entries and collects commitments, tracking status changes.
    Most recent status wins for duplicate commitments.
    """
    commitments = []

    for entry in entries:
        if not entry.commitments:
            continue

        # Parse individual commitment items
        items = _parse_commitments(entry.commitments, entry.week_of)
        commitments.extend(items)

    return commitments


def format_commitment_ledger(items: list[CommitmentItem]) -> str:
    """Format commitment ledger for prompt injection."""
    if not items:
        return "[No active commitments in the running picture window.]"

    lines = []
    for item in items:
        lines.append(f"- {item.description}")
        lines.append(f"  Status: {item.status} (as of {item.week_of})")
        if item.audience:
            lines.append(f"  Audience: {item.audience}")
        if item.binding_force:
            lines.append(f"  Binding force: {item.binding_force}")
    return "\n".join(lines)


# =============================================================================
# INTERNAL HELPERS
# =============================================================================


def _extract_thread_items(
    threads_text: str,
    section_header: str,
) -> list[tuple[str, str]]:
    """
    Extract thread items from a section within Developing Threads.

    Returns list of (title, status_text) tuples.
    """
    results = []

    # Find the section
    header_pos = threads_text.find(section_header)
    if header_pos < 0:
        return results

    # Find end of section (next section header or end of text)
    section_start = header_pos + len(section_header)
    # Look for next section header (ACTIVE THREADS: or DORMANT THREADS:)
    next_header = re.search(
        r"\n(?:ACTIVE|DORMANT) THREADS:",
        threads_text[section_start:],
    )
    section_end = section_start + next_header.start() if next_header else len(threads_text)
    section_text = threads_text[section_start:section_end]

    # Parse items: "- [THREAD TITLE]: status text"
    pattern = re.compile(r"^- \[(.+?)\]:\s*(.+?)$", re.MULTILINE)
    for match in pattern.finditer(section_text):
        title = match.group(1).strip()
        # Collect all text until next "- [" or end
        status_start = match.end()
        next_item = re.search(r"\n- \[", section_text[status_start:])
        if next_item:
            full_status = section_text[match.start(2):status_start + next_item.start()]
        else:
            full_status = section_text[match.start(2):]

        # Extract just the first line as status summary
        status = match.group(2).strip()
        results.append((title, status))

    return results


def _extract_bullet_items(text: str) -> list[tuple[str, str]]:
    """Extract bullet items as (title, description) from markdown list."""
    results = []
    pattern = re.compile(r"^- \[(.+?)\]:\s*(.+?)$", re.MULTILINE)
    for match in pattern.finditer(text):
        results.append((match.group(1).strip(), match.group(2).strip()))
    return results


def _parse_commitments(
    commitments_text: str,
    week_of: str,
) -> list[CommitmentItem]:
    """Parse commitments section into CommitmentItem list."""
    items = []

    # Split on bullet points
    bullets = re.split(r"\n(?=- \[)", commitments_text)

    for bullet in bullets:
        bullet = bullet.strip()
        if not bullet.startswith("- ["):
            continue

        # Extract description
        desc_match = re.match(r"- \[(.+?)\]:\s*(.+?)$", bullet, re.MULTILINE)
        if not desc_match:
            continue

        description = f"{desc_match.group(1)}: {desc_match.group(2)}"

        # Extract fields
        status_match = re.search(r"Status:\s*(.+?)$", bullet, re.MULTILINE)
        audience_match = re.search(r"Audience:\s*(.+?)$", bullet, re.MULTILINE)
        binding_match = re.search(r"Binding force:\s*(.+?)$", bullet, re.MULTILINE | re.IGNORECASE)

        items.append(CommitmentItem(
            description=description,
            status=status_match.group(1).strip() if status_match else "",
            audience=audience_match.group(1).strip() if audience_match else "",
            binding_force=binding_match.group(1).strip() if binding_match else "",
            week_of=week_of,
        ))

    return items
