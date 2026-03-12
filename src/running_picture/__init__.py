"""
Running Analytical Picture — persistent per-leader analytical context.

Package structure:
- schema: Data classes for entries, consolidation summaries, threads
- storage: Read/write/archive operations
- validation: Schema validation and quality checks
- extraction: Thread checklist and commitment ledger extraction for prompts
"""

from .schema import (
    RunningPictureEntry,
    ConsolidationSummary,
    ThreadStatus,
    leader_slug,
)
from .storage import (
    load_weekly_entries,
    load_weekly_text,
    save_weekly_entry,
    load_consolidation,
    save_consolidation,
    load_dormant_threads,
    save_dormant_threads,
    entry_count,
)
from .validation import validate_entry, ValidationResult
from .extraction import (
    extract_thread_checklist,
    extract_commitment_ledger,
)

__all__ = [
    "RunningPictureEntry",
    "ConsolidationSummary",
    "ThreadStatus",
    "leader_slug",
    "load_weekly_entries",
    "load_weekly_text",
    "save_weekly_entry",
    "load_consolidation",
    "save_consolidation",
    "load_dormant_threads",
    "save_dormant_threads",
    "entry_count",
    "validate_entry",
    "ValidationResult",
    "extract_thread_checklist",
    "extract_commitment_ledger",
]
