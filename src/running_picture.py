"""
Running Analytical Picture — file management layer.

Each leader has a single markdown file containing weekly analytical entries,
most recent first. The pipeline reads the latest N entries as context and
appends new entries after each cycle.

File layout:
    running_pictures/
        emmanuel_macron.md
        keir_starmer.md
        ...
        archive/
            emmanuel_macron_archive.md
            ...
"""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import LeaderConfig

logger = logging.getLogger(__name__)

RUNNING_PICTURES_DIR = Path("running_pictures")

# Delimiter between entries — a horizontal rule preceded by a blank line
ENTRY_DELIMITER = "\n---\n"

# Required sections in a valid running picture entry
REQUIRED_SECTIONS = [
    "Activity Level",
    "Key Actions",
    "Commitments & Positions",
    "Relationships",
    "Developing Threads",
]

# Sections where content is optional (may legitimately be empty)
OPTIONAL_SECTIONS = [
    "Domestic Political Position",
    "Structural Claim Check",
    "Analytical Notes",
]


@dataclass
class RunningPictureEntry:
    """A single parsed entry from a running picture file."""

    leader: str
    country: str
    week_of: str  # YYYY-MM-DD
    generated_at: str  # ISO timestamp
    event_count: int
    source_count: int
    raw_text: str  # Full markdown text of the entry (including frontmatter)

    # Parsed sections (populated by _parse_sections)
    activity_level: str = ""
    key_actions: str = ""
    commitments: str = ""
    relationships: str = ""
    domestic_position: str = ""
    developing_threads: str = ""
    structural_claim_check: str = ""
    analytical_notes: str = ""


@dataclass
class ValidationResult:
    """Result of validating a running picture entry."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def leader_slug(name: str) -> str:
    """Convert a leader name to a filesystem-safe slug."""
    return name.lower().replace(" ", "_")


def _running_picture_path(leader_name: str, base_dir: Optional[Path] = None) -> Path:
    """Get the path to a leader's running picture file."""
    base = base_dir or RUNNING_PICTURES_DIR
    return base / f"{leader_slug(leader_name)}.md"


def load_running_picture(
    leader_name: str,
    max_entries: int = 10,
    base_dir: Optional[Path] = None,
) -> list[RunningPictureEntry]:
    """
    Load the most recent entries from a leader's running picture file.

    Returns an empty list if the file doesn't exist (bootstrap case).
    Entries are returned most-recent-first.
    """
    path = _running_picture_path(leader_name, base_dir)

    if not path.exists():
        logger.debug(f"No running picture for {leader_name} (bootstrap)")
        return []

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return []

    raw_entries = _split_entries(content)
    entries = []

    for raw in raw_entries[:max_entries]:
        try:
            entry = _parse_entry(raw)
            entries.append(entry)
        except ValueError as e:
            logger.warning(f"Skipping malformed entry in {path}: {e}")

    logger.debug(f"Loaded {len(entries)} running picture entries for {leader_name}")
    return entries


def load_running_picture_text(
    leader_name: str,
    max_entries: int = 10,
    base_dir: Optional[Path] = None,
) -> str:
    """
    Load the raw markdown text of the most recent entries.

    This is what gets injected into the LLM prompt as running context.
    Returns empty string if no entries exist.
    """
    entries = load_running_picture(leader_name, max_entries, base_dir)
    if not entries:
        return ""
    return ENTRY_DELIMITER.join(e.raw_text for e in entries)


def append_entry(
    leader_name: str,
    entry_text: str,
    base_dir: Optional[Path] = None,
) -> Path:
    """
    Prepend a new entry to the top of a leader's running picture file.

    Creates the file and directory if they don't exist.
    Returns the path to the file.
    """
    path = _running_picture_path(leader_name, base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    entry_text = entry_text.strip()

    if path.exists():
        existing = path.read_text(encoding="utf-8").strip()
        if existing:
            content = entry_text + ENTRY_DELIMITER + existing
        else:
            content = entry_text
    else:
        content = entry_text

    path.write_text(content + "\n", encoding="utf-8")
    logger.info(f"Appended running picture entry for {leader_name}")
    return path


def validate_entry(entry_text: str) -> ValidationResult:
    """
    Validate a running picture entry against the schema.

    Checks:
    - Frontmatter is present with required fields
    - All required sections exist
    - Key Actions have source attributions
    - Developing Threads have "Watch for" fields
    - Commitments with SHIFTED/WALKED BACK reference original dates
    """
    errors = []
    warnings = []

    # Check frontmatter
    fm = _extract_frontmatter(entry_text)
    if fm is None:
        errors.append("Missing frontmatter (--- delimited YAML block)")
    else:
        for required_field in ["leader", "country", "week_of", "generated_at"]:
            if required_field not in fm:
                errors.append(f"Missing frontmatter field: {required_field}")

        if "week_of" in fm and not re.match(r"\d{4}-\d{2}-\d{2}", fm["week_of"]):
            errors.append(f"Invalid week_of format: {fm['week_of']} (expected YYYY-MM-DD)")

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if f"### {section}" not in entry_text:
            errors.append(f"Missing required section: ### {section}")

    # Check Key Actions have source attributions
    key_actions_match = re.search(
        r"### Key Actions\n(.*?)(?=\n### |\Z)", entry_text, re.DOTALL
    )
    if key_actions_match:
        actions_text = key_actions_match.group(1)
        numbered_items = re.findall(r"^\d+\.", actions_text, re.MULTILINE)
        source_refs = re.findall(r"Source:", actions_text)
        if numbered_items and len(source_refs) < len(numbered_items):
            warnings.append(
                f"Key Actions: {len(numbered_items)} items but only "
                f"{len(source_refs)} Source attributions"
            )

    # Check Developing Threads have "Watch for"
    threads_match = re.search(
        r"### Developing Threads\n(.*?)(?=\n### |\Z)", entry_text, re.DOTALL
    )
    if threads_match:
        threads_text = threads_match.group(1)
        thread_items = re.findall(r"^- \[", threads_text, re.MULTILINE)
        watch_refs = re.findall(r"Watch for:", threads_text)
        if thread_items and len(watch_refs) < len(thread_items):
            warnings.append(
                f"Developing Threads: {len(thread_items)} items but only "
                f"{len(watch_refs)} 'Watch for' fields"
            )

    # Check SHIFTED/WALKED BACK commitments reference dates
    commitments_match = re.search(
        r"### Commitments & Positions\n(.*?)(?=\n### |\Z)", entry_text, re.DOTALL
    )
    if commitments_match:
        commitments_text = commitments_match.group(1)
        shifted = re.findall(
            r"Status:\s*(SHIFTED|WALKED BACK)", commitments_text
        )
        if shifted:
            date_refs = re.findall(r"\d{4}-\d{2}-\d{2}", commitments_text)
            if not date_refs:
                warnings.append(
                    "Commitments with SHIFTED/WALKED BACK status should "
                    "reference the original commitment date"
                )

    # Structural Claim Check: warn if zero or too many
    claim_match = re.search(
        r"### Structural Claim Check\n(.*?)(?=\n### |\Z)", entry_text, re.DOTALL
    )
    if claim_match:
        claims_text = claim_match.group(1).strip()
        claim_items = re.findall(r"^- \[", claims_text, re.MULTILINE)
        if len(claim_items) > 5:
            warnings.append(
                f"Structural Claim Check has {len(claim_items)} items "
                f"(expected 1-3; >5 suggests over-flagging)"
            )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )


def entry_count(
    leader_name: str,
    base_dir: Optional[Path] = None,
) -> int:
    """Return the number of entries in a leader's running picture file."""
    path = _running_picture_path(leader_name, base_dir)
    if not path.exists():
        return 0
    content = path.read_text(encoding="utf-8")
    return len(_split_entries(content))


# =============================================================================
# INTERNAL HELPERS
# =============================================================================


def _split_entries(content: str) -> list[str]:
    """
    Split a running picture file into individual entries.

    Entries are separated by `---` on its own line. But `---` also appears
    in frontmatter, so we split on `---` that appears between entries
    (after the closing frontmatter `---` of one entry and before the
    opening frontmatter `---` of the next).
    """
    # Each entry starts with a frontmatter block: ---\n...\n---
    # We split on the pattern: closing content + \n---\n + opening ---
    # Strategy: find all frontmatter-opening positions and split there
    entries = []
    # Find all positions where a new entry starts (--- followed by key: value lines)
    pattern = re.compile(r"^---\s*\n(?=\w+:)", re.MULTILINE)
    starts = [m.start() for m in pattern.finditer(content)]

    if not starts:
        # No valid entries found
        return []

    for i, start in enumerate(starts):
        if i + 1 < len(starts):
            entry_text = content[start : starts[i + 1]].strip()
            # Remove trailing --- delimiter
            entry_text = re.sub(r"\n---\s*$", "", entry_text)
        else:
            entry_text = content[start:].strip()

        if entry_text:
            entries.append(entry_text)

    return entries


def _extract_frontmatter(entry_text: str) -> Optional[dict[str, str]]:
    """
    Extract YAML-like frontmatter from an entry.

    Expects --- delimited block at the start of the entry.
    Returns a dict of key-value pairs, or None if no frontmatter found.
    """
    match = re.match(r"^---\s*\n(.*?)\n---", entry_text, re.DOTALL) or re.match(r"^---\s*\n---", entry_text)
    if not match:
        return None

    fm = {}
    body = match.group(1) if match.lastindex and match.lastindex >= 1 else ""
    for line in body.strip().split("\n") if body.strip() else []:
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()

    return fm


def _parse_entry(raw_text: str) -> RunningPictureEntry:
    """
    Parse a raw markdown entry into a RunningPictureEntry.

    Raises ValueError if frontmatter is missing or malformed.
    """
    fm = _extract_frontmatter(raw_text)
    if fm is None:
        raise ValueError("Entry has no frontmatter")

    entry = RunningPictureEntry(
        leader=fm.get("leader", ""),
        country=fm.get("country", ""),
        week_of=fm.get("week_of", ""),
        generated_at=fm.get("generated_at", ""),
        event_count=int(fm.get("event_count", 0)),
        source_count=int(fm.get("source_count", 0)),
        raw_text=raw_text,
    )

    # Parse sections
    sections = _parse_sections(raw_text)
    entry.activity_level = sections.get("Activity Level", "")
    entry.key_actions = sections.get("Key Actions", "")
    entry.commitments = sections.get("Commitments & Positions", "")
    entry.relationships = sections.get("Relationships", "")
    entry.domestic_position = sections.get("Domestic Political Position", "")
    entry.developing_threads = sections.get("Developing Threads", "")
    entry.structural_claim_check = sections.get("Structural Claim Check", "")
    entry.analytical_notes = sections.get("Analytical Notes", "")

    return entry


def _parse_sections(entry_text: str) -> dict[str, str]:
    """Extract ### sections from an entry into a dict."""
    sections = {}
    pattern = re.compile(r"^### (.+?)$", re.MULTILINE)
    matches = list(pattern.finditer(entry_text))

    for i, match in enumerate(matches):
        section_name = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(entry_text)
        sections[section_name] = entry_text[start:end].strip()

    return sections
