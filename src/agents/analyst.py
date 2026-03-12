"""
Phase 1 Analyst Agent — per-leader analysis producing running picture entries
and analytical assessments.

Call A: Structured running picture entry (data logging)
Call B: Analytical assessment (interpretive analysis, uses Call A output)

v3 architecture: system prompt is cached dossier+profile+claims (identical
for Call A and Call B). Role-specific instructions go in the user prompt.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Optional

from ..config import LeaderConfig, MODEL_SYNTHESIS, THINKING_SYNTHESIS, THINKING_ANALYTICAL
from ..context.assembly import (
    build_system_prompt,
    build_call_a_user_prompt,
    build_call_b_user_prompt,
)
from ..context.claims import extract_claims, get_valid_claim_refs
from ..running_picture.schema import RunningPictureEntry, parse_entry
from ..running_picture.storage import (
    load_weekly_entries,
    load_weekly_text,
    load_consolidation,
    save_weekly_entry,
)
from ..running_picture.extraction import (
    extract_thread_checklist,
    format_thread_checklist,
)
from ..running_picture.validation import validate_entry
from .base import complete, with_retry
from .event_clustering import ProcessedEvent

logger = logging.getLogger(__name__)


class AnalystAgent:
    """Phase 1 analyst agent for per-leader weekly analysis."""

    async def run_call_a(
        self,
        leader: LeaderConfig,
        events: list[ProcessedEvent],
        date_start: str,
        date_end: str,
        country_dossier: str,
        leader_profile: str,
        global_context: Optional[str] = None,
        base_dir=None,
    ) -> tuple[str, RunningPictureEntry]:
        """
        Phase 1 Call A: Produce a structured Running Picture entry.

        The system prompt (dossier+profile+claims) is cached and identical
        for Call A and Call B. Role instructions go in the user prompt.

        Auto-retries once on validation failure with correction prompt.

        Returns:
            Tuple of (raw entry text, parsed RunningPictureEntry)
        """
        # Build cached system prompt
        system = build_system_prompt(
            country_dossier, leader_profile, leader.country, leader.name,
        )

        # Load running context
        running_text = load_weekly_text(leader.name, max_entries=3, base_dir=base_dir)
        if not running_text:
            running_text = "[No prior entries — this is the inaugural analysis.]"

        # Build thread checklist from prior entry
        prior_entries = load_weekly_entries(leader.name, max_entries=1, base_dir=base_dir)
        consolidation = load_consolidation(leader.name, base_dir=base_dir)
        prior_entry = prior_entries[0] if prior_entries else None

        checklist_items = extract_thread_checklist(prior_entry, consolidation)
        thread_checklist = format_thread_checklist(checklist_items)
        prior_thread_count = len(checklist_items) if checklist_items else None

        # Build valid claim refs for validation
        structural_claims = extract_claims(country_dossier, "STRUC")
        profile_claims = extract_claims(leader_profile, "PROF")
        valid_claims = get_valid_claim_refs(structural_claims, profile_claims)

        # Build user prompt
        user_prompt = build_call_a_user_prompt(
            leader=leader,
            events=events,
            date_start=date_start,
            date_end=date_end,
            running_picture_text=running_text,
            thread_checklist=thread_checklist,
            global_context=global_context,
        )

        logger.info(f"Running Phase 1 Call A for {leader.name}")

        response = await _call_llm(system, user_prompt)
        entry_text = _extract_entry(response, leader, date_start)

        # Validate
        validation = validate_entry(
            entry_text,
            prior_thread_count=prior_thread_count,
            valid_claims=valid_claims if valid_claims else None,
        )

        # Auto-retry once on validation failure
        if not validation.valid:
            logger.warning(
                f"Call A for {leader.name} failed validation: {validation.errors}. Retrying."
            )
            correction = validation.correction_prompt
            retry_prompt = f"{user_prompt}\n\n---\n\n{correction}"

            response = await _call_llm(system, retry_prompt)
            entry_text = _extract_entry(response, leader, date_start)

            validation = validate_entry(
                entry_text,
                prior_thread_count=prior_thread_count,
                valid_claims=valid_claims if valid_claims else None,
            )
            if not validation.valid:
                logger.warning(
                    f"Call A retry for {leader.name} still has errors: "
                    f"{validation.errors}. Accepting with warning."
                )

        if validation.warnings:
            logger.info(f"Call A for {leader.name} warnings: {validation.warnings}")

        # Parse into structured entry
        try:
            parsed = parse_entry(entry_text)
        except ValueError as e:
            logger.error(f"Failed to parse Call A entry for {leader.name}: {e}")
            parsed = RunningPictureEntry(
                leader=leader.name,
                country=leader.country,
                week_of=_monday_of_week(date_start),
                generated_at=datetime.now().isoformat(timespec="seconds"),
                event_count=len(events),
                source_count=sum(len(e.articles) for e in events),
                raw_text=entry_text,
            )

        return entry_text, parsed

    async def run_call_a_and_save(
        self,
        leader: LeaderConfig,
        events: list[ProcessedEvent],
        date_start: str,
        date_end: str,
        country_dossier: str,
        leader_profile: str,
        global_context: Optional[str] = None,
        base_dir=None,
    ) -> tuple[str, RunningPictureEntry]:
        """Run Call A and save the entry to the leader's running picture directory."""
        entry_text, parsed = await self.run_call_a(
            leader=leader,
            events=events,
            date_start=date_start,
            date_end=date_end,
            country_dossier=country_dossier,
            leader_profile=leader_profile,
            global_context=global_context,
            base_dir=base_dir,
        )

        save_weekly_entry(
            leader.name, parsed.week_of, entry_text, base_dir=base_dir,
        )

        return entry_text, parsed

    async def run_call_b(
        self,
        leader: LeaderConfig,
        call_a_output: str,
        events: list[ProcessedEvent],
        date_start: str,
        date_end: str,
        country_dossier: str,
        leader_profile: str,
        global_context: Optional[str] = None,
        base_dir=None,
    ) -> str:
        """
        Phase 1 Call B: Produce an analytical assessment.

        Uses the same cached system prompt as Call A (prompt cache hit).

        Returns:
            Analytical assessment text.
        """
        system = build_system_prompt(
            country_dossier, leader_profile, leader.country, leader.name,
        )

        running_text = load_weekly_text(leader.name, max_entries=3, base_dir=base_dir)
        if not running_text:
            running_text = "[No prior entries.]"

        user_prompt = build_call_b_user_prompt(
            leader=leader,
            call_a_output=call_a_output,
            events=events,
            date_start=date_start,
            date_end=date_end,
            running_picture_text=running_text,
            global_context=global_context,
        )

        logger.info(f"Running Phase 1 Call B for {leader.name}")

        response = await _call_llm(
            system, user_prompt,
            thinking_budget=THINKING_ANALYTICAL,
        )

        return response.strip()


# =============================================================================
# HELPERS
# =============================================================================


@with_retry(max_attempts=2)
async def _call_llm(
    system: str,
    user_prompt: str,
    thinking_budget: int = THINKING_SYNTHESIS,
) -> str:
    """Call the LLM with rate limiting and retry."""
    return await complete(
        prompt=user_prompt,
        system=system,
        model=MODEL_SYNTHESIS,
        max_tokens=8000,
        thinking_budget=thinking_budget,
    )


def _monday_of_week(date_str: str) -> str:
    """Return the Monday of the week containing the given date."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    monday = dt - timedelta(days=dt.weekday())
    return monday.strftime("%Y-%m-%d")


def _extract_entry(
    response: str,
    leader: LeaderConfig,
    date_start: str,
) -> str:
    """
    Extract the running picture entry from the LLM response.

    Strips code block fences and ensures frontmatter is present.
    """
    text = response.strip()

    # Strip markdown code block fences if present
    text = re.sub(r"^```(?:markdown|md)?\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    text = text.strip()

    # Ensure frontmatter is present
    if not text.startswith("---"):
        week_of = _monday_of_week(date_start)
        generated_at = datetime.now().isoformat(timespec="seconds")
        frontmatter = (
            f"---\n"
            f"leader: {leader.name}\n"
            f"country: {leader.country}\n"
            f"week_of: {week_of}\n"
            f"generated_at: {generated_at}\n"
            f"event_count: 0\n"
            f"source_count: 0\n"
            f"---"
        )
        text = frontmatter + "\n\n" + text

    return text
