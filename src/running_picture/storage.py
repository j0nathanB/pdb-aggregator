"""
Running Picture file storage — read/write/archive operations.

Directory structure (from v3 spec):

    running_picture/
    +-- weekly/
    |   +-- macron/
    |   |   +-- 2026-03-03.md
    |   |   +-- 2026-02-24.md
    |   |   +-- 2026-02-17.md
    +-- consolidation/
    |   +-- macron/
    |   |   +-- 2026-02-24_consolidation.md
    +-- dormant_threads/
    |   +-- macron_dormant.md
    +-- archive/
    +-- cross_correlation/
        +-- 2026-03-03_clusters.md
"""

import logging
from pathlib import Path
from typing import Optional

from .schema import (
    RunningPictureEntry,
    ConsolidationSummary,
    leader_slug,
    parse_entry,
    parse_consolidation,
)

logger = logging.getLogger(__name__)

RUNNING_PICTURE_DIR = Path("running_picture")


def _weekly_dir(leader_name: str, base_dir: Optional[Path] = None) -> Path:
    base = base_dir or RUNNING_PICTURE_DIR
    return base / "weekly" / leader_slug(leader_name)


def _consolidation_dir(leader_name: str, base_dir: Optional[Path] = None) -> Path:
    base = base_dir or RUNNING_PICTURE_DIR
    return base / "consolidation" / leader_slug(leader_name)


def _dormant_path(leader_name: str, base_dir: Optional[Path] = None) -> Path:
    base = base_dir or RUNNING_PICTURE_DIR
    return base / "dormant_threads" / f"{leader_slug(leader_name)}_dormant.md"


def load_weekly_entries(
    leader_name: str,
    max_entries: int = 3,
    base_dir: Optional[Path] = None,
) -> list[RunningPictureEntry]:
    """
    Load the most recent weekly entries for a leader.

    Returns entries sorted most-recent-first.
    Default max_entries=3 per v3 spec (3 entries + consolidation).
    Returns empty list if no entries exist (bootstrap case).
    """
    weekly_dir = _weekly_dir(leader_name, base_dir)

    if not weekly_dir.exists():
        logger.debug(f"No weekly entries for {leader_name} (bootstrap)")
        return []

    # List .md files, sort by name descending (YYYY-MM-DD.md sorts chronologically)
    files = sorted(weekly_dir.glob("*.md"), reverse=True)

    entries = []
    for f in files[:max_entries]:
        try:
            raw = f.read_text(encoding="utf-8")
            entry = parse_entry(raw)
            entries.append(entry)
        except (ValueError, OSError) as e:
            logger.warning(f"Skipping malformed entry {f}: {e}")

    logger.debug(f"Loaded {len(entries)} weekly entries for {leader_name}")
    return entries


def load_weekly_text(
    leader_name: str,
    max_entries: int = 3,
    base_dir: Optional[Path] = None,
) -> str:
    """
    Load raw markdown text of recent entries for LLM prompt injection.

    Returns entries separated by horizontal rules. Empty string if none exist.
    """
    entries = load_weekly_entries(leader_name, max_entries, base_dir)
    if not entries:
        return ""
    return "\n\n---\n\n".join(e.raw_text for e in entries)


def save_weekly_entry(
    leader_name: str,
    week_of: str,
    entry_text: str,
    base_dir: Optional[Path] = None,
) -> Path:
    """
    Save a weekly entry to the leader's directory.

    Creates the directory structure if it doesn't exist.
    File is named by week_of date: YYYY-MM-DD.md

    Returns path to the saved file.
    """
    weekly_dir = _weekly_dir(leader_name, base_dir)
    weekly_dir.mkdir(parents=True, exist_ok=True)

    path = weekly_dir / f"{week_of}.md"
    path.write_text(entry_text.strip() + "\n", encoding="utf-8")

    logger.info(f"Saved weekly entry for {leader_name} week of {week_of}")
    return path


def load_consolidation(
    leader_name: str,
    base_dir: Optional[Path] = None,
) -> Optional[ConsolidationSummary]:
    """
    Load the most recent consolidation summary for a leader.

    Returns None if no consolidation exists.
    """
    consol_dir = _consolidation_dir(leader_name, base_dir)

    if not consol_dir.exists():
        return None

    files = sorted(consol_dir.glob("*_consolidation.md"), reverse=True)
    if not files:
        return None

    try:
        raw = files[0].read_text(encoding="utf-8")
        return parse_consolidation(raw)
    except (ValueError, OSError) as e:
        logger.warning(f"Failed to load consolidation for {leader_name}: {e}")
        return None


def save_consolidation(
    leader_name: str,
    period_end: str,
    text: str,
    base_dir: Optional[Path] = None,
) -> Path:
    """
    Save a consolidation summary.

    File is named: YYYY-MM-DD_consolidation.md
    """
    consol_dir = _consolidation_dir(leader_name, base_dir)
    consol_dir.mkdir(parents=True, exist_ok=True)

    path = consol_dir / f"{period_end}_consolidation.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")

    logger.info(f"Saved consolidation for {leader_name} ending {period_end}")
    return path


def load_dormant_threads(
    leader_name: str,
    base_dir: Optional[Path] = None,
) -> str:
    """
    Load dormant threads file content.

    Returns empty string if no dormant threads file exists.
    """
    path = _dormant_path(leader_name, base_dir)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def save_dormant_threads(
    leader_name: str,
    text: str,
    base_dir: Optional[Path] = None,
) -> Path:
    """Save dormant threads file."""
    path = _dormant_path(leader_name, base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    logger.info(f"Saved dormant threads for {leader_name}")
    return path


def entry_count(
    leader_name: str,
    base_dir: Optional[Path] = None,
) -> int:
    """Return number of weekly entries for a leader."""
    weekly_dir = _weekly_dir(leader_name, base_dir)
    if not weekly_dir.exists():
        return 0
    return len(list(weekly_dir.glob("*.md")))


def archive_old_entries(
    leader_name: str,
    keep: int = 4,
    base_dir: Optional[Path] = None,
) -> list[Path]:
    """
    Move entries older than the most recent `keep` to the archive.

    Returns list of archived file paths.
    """
    weekly_dir = _weekly_dir(leader_name, base_dir)
    if not weekly_dir.exists():
        return []

    base = base_dir or RUNNING_PICTURE_DIR
    archive_dir = base / "archive" / leader_slug(leader_name)

    files = sorted(weekly_dir.glob("*.md"), reverse=True)
    to_archive = files[keep:]

    if not to_archive:
        return []

    archive_dir.mkdir(parents=True, exist_ok=True)
    archived = []

    for f in to_archive:
        dest = archive_dir / f.name
        f.rename(dest)
        archived.append(dest)
        logger.debug(f"Archived {f.name} for {leader_name}")

    logger.info(f"Archived {len(archived)} entries for {leader_name}")
    return archived
