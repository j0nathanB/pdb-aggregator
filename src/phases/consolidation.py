"""
Consolidation Task — compresses 4 weekly entries into a period summary.

Runs every 4 weeks per leader. The consolidation summary replaces the
4 individual entries as context for future analysis, keeping the running
picture manageable over time.
"""

import logging
import re
from typing import Optional
from pathlib import Path

from ..config import LeaderConfig, MODEL_SYNTHESIS, THINKING_ANALYTICAL
from ..agents.base import complete, with_retry
from ..running_picture.storage import (
    load_weekly_entries,
    load_consolidation,
    load_dormant_threads,
    save_consolidation,
    save_dormant_threads,
    archive_old_entries,
    entry_count,
)
from ..running_picture.schema import RunningPictureEntry, ConsolidationSummary
from ..context.claims import extract_claims, format_claims_index

logger = logging.getLogger(__name__)

# =============================================================================
# PROMPTS
# =============================================================================

SYSTEM_PROMPT = """\
You are a consolidation engine for a running analytical picture.
You will receive 4 weeks of structured weekly entries for a single
leader, plus the prior consolidation summary and dormant thread
archive.

Your task is to compress these 4 weeks into a single period
summary following the schema exactly. This summary replaces the
4 individual entries as context for future analysis.

Key responsibilities:
- Synthesize the period trajectory (not just summarize week by week)
- Identify stable assessments that held across the period
- Track thread lifecycle: resolve completed threads, escalate
  growing ones, move inactive ones to dormant
- Update the commitment ledger with current status
- Check for analytical inertia (assessments that persisted without
  fresh evidence)
- Conduct slow-burn review (gradual shifts missed in weekly analysis)
- Flag structural claims for refresh if challenged 3+ times

Use [STRUC-XX] and [PROF-XX] claim references throughout."""

USER_PROMPT_TEMPLATE = """\
## ENTRIES TO CONSOLIDATE

{weekly_entries}

---

## PRIOR CONSOLIDATION (if any)

{prior_consolidation}

---

## DORMANT THREAD ARCHIVE

{dormant_threads}

---

## CLAIMS INDEX (for reference)

{claims_index}

---

Produce the Consolidation Summary for {leader_name} ({title}, \
{country}) covering {period_start} to {period_end}."""


# =============================================================================
# HELPERS
# =============================================================================


def needs_consolidation(leader_name: str, base_dir: Optional[Path] = None) -> bool:
    """Check if a leader needs consolidation (4+ entries since last consolidation)."""
    count = entry_count(leader_name, base_dir=base_dir)
    return count >= 4


def _extract_newly_dormant_threads(consolidation_text: str) -> str:
    """
    Extract the Newly Dormant Threads section from consolidation output.

    Returns the section content, or empty string if not found.
    """
    match = re.search(
        r"### Newly Dormant Threads\s*\n(.*?)(?=\n### |\Z)",
        consolidation_text,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    return ""


def _build_user_prompt(
    entries: list[RunningPictureEntry],
    prior_consolidation: Optional[ConsolidationSummary],
    dormant_threads: str,
    claims_index: str,
    leader: LeaderConfig,
) -> str:
    """Assemble the user prompt for the consolidation LLM call."""
    # Format weekly entries
    entries_text = "\n\n---\n\n".join(e.raw_text for e in entries)

    # Format prior consolidation
    if prior_consolidation:
        prior_text = prior_consolidation.raw_text
    else:
        prior_text = "[No prior consolidation — this is the first cycle.]"

    # Format dormant threads
    dormant_text = dormant_threads if dormant_threads.strip() else "[No dormant threads on file.]"

    # Determine period bounds from entries (sorted most-recent-first)
    period_end = entries[0].week_of if entries else "unknown"
    period_start = entries[-1].week_of if entries else "unknown"

    return USER_PROMPT_TEMPLATE.format(
        weekly_entries=entries_text,
        prior_consolidation=prior_text,
        dormant_threads=dormant_text,
        claims_index=claims_index,
        leader_name=leader.name,
        title=leader.title,
        country=leader.country,
        period_start=period_start,
        period_end=period_end,
    )


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================


@with_retry(max_attempts=2)
async def _call_consolidation_llm(prompt: str) -> str:
    """Make the LLM call for consolidation (wrapped with retry)."""
    return await complete(
        prompt=prompt,
        system=SYSTEM_PROMPT,
        model=MODEL_SYNTHESIS,
        max_tokens=16000,
        thinking_budget=THINKING_ANALYTICAL,
    )


async def run_consolidation(
    leader: LeaderConfig,
    country_dossier: str,
    leader_profile: str,
    base_dir: Optional[Path] = None,
) -> str:
    """
    Run consolidation for a single leader.

    Loads the last 4 weekly entries, produces a consolidation summary,
    saves it, and archives old entries.

    Returns the consolidation summary text.
    """
    logger.info(f"Starting consolidation for {leader.name}")

    # Load inputs
    entries = load_weekly_entries(leader.name, max_entries=4, base_dir=base_dir)
    if len(entries) < 4:
        logger.warning(
            f"Only {len(entries)} entries for {leader.name}, "
            f"need 4 for consolidation"
        )

    prior = load_consolidation(leader.name, base_dir=base_dir)
    dormant = load_dormant_threads(leader.name, base_dir=base_dir)

    # Build claims index from baseline documents
    structural_claims = extract_claims(country_dossier, namespace="STRUC")
    profile_claims = extract_claims(leader_profile, namespace="PROF")
    claims_index = format_claims_index(
        structural_claims, profile_claims,
        country=leader.country, leader_name=leader.name,
    )

    # Assemble prompt and call LLM
    user_prompt = _build_user_prompt(
        entries=entries,
        prior_consolidation=prior,
        dormant_threads=dormant,
        claims_index=claims_index,
        leader=leader,
    )

    consolidation_text = await _call_consolidation_llm(user_prompt)

    # Determine period end for file naming
    period_end = entries[0].week_of if entries else "unknown"

    # 1. Save consolidation summary
    save_consolidation(
        leader.name, period_end, consolidation_text, base_dir=base_dir,
    )

    # 2. Extract and save newly dormant threads
    newly_dormant = _extract_newly_dormant_threads(consolidation_text)
    if newly_dormant:
        # Append new dormant threads to existing archive
        existing_dormant = load_dormant_threads(leader.name, base_dir=base_dir)
        if existing_dormant.strip():
            updated_dormant = existing_dormant.rstrip() + "\n\n" + newly_dormant
        else:
            updated_dormant = newly_dormant
        save_dormant_threads(leader.name, updated_dormant, base_dir=base_dir)

    # 3. Archive old entries
    archive_old_entries(leader.name, keep=4, base_dir=base_dir)

    logger.info(f"Consolidation complete for {leader.name}")
    return consolidation_text
