"""
Ledger consolidation: compress older weekly entries into summaries.

Triggered when entry count exceeds retention window (8 weeks).
Preserves: category assessment changes, corrections, structural claim changes,
executive-relevant findings.
Discards: individual article references, full development details, source URLs.
"""

import json
import logging
import re
from datetime import date
from typing import Optional

import anthropic

from ..rate_limit import anthropic_limiter
from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    ClaimStatus,
    Depth,
    Movement,
    SignalCategory,
    load_prompt,
)
from ..models import CountryLedger, GlobalLedger, WeeklyEntry

logger = logging.getLogger(__name__)


CONSOLIDATION_SYSTEM_PROMPT = load_prompt("ledger/consolidation")


def _format_entries_for_consolidation(entries: list[WeeklyEntry], country: str) -> str:
    """Format weekly entries for the consolidation prompt."""
    lines = [f"Country: {country}"]
    lines.append(f"Period: {entries[0].week.isoformat()} to {entries[-1].week.isoformat()}")
    lines.append(f"Entries: {len(entries)}\n")

    for entry in entries:
        lines.append(f"### Week of {entry.week.isoformat()} ({entry.depth.value})")

        if entry.activity_level:
            lines.append(f"Activity: {entry.activity_level.get('rating', '?')}")

        if entry.category_movements:
            for cat, mov in entry.category_movements.items():
                if mov.movement != Movement.NONE:
                    lines.append(f"  {cat.value}: {mov.movement.value}")
                    if mov.updated_assessment:
                        lines.append(f"    → {mov.updated_assessment[:300]}")
                    if mov.confidence_change:
                        lines.append(
                            f"    Confidence: {mov.confidence_change.from_} → {mov.confidence_change.to}"
                        )

        if entry.self_corrections:
            for sc in entry.self_corrections:
                lines.append(f"  CORRECTION ({sc.category.value}): {sc.correction[:200]}")

        if entry.structural_claim_checks:
            for check in entry.structural_claim_checks:
                if check.status != ClaimStatus.CONFIRMED:
                    lines.append(f"  CLAIM [{check.claim_ref}]: {check.status.value}")

        lines.append("")

    return "\n".join(lines)


async def consolidate_entries(
    entries: list[WeeklyEntry],
    country: str,
) -> str:
    """
    Compress a batch of weekly entries into a consolidated summary.

    Args:
        entries: Weekly entries to compress (typically the oldest entries being archived).
        country: Country name for context.

    Returns:
        Consolidated summary text.
    """
    if not entries:
        return ""

    if not ANTHROPIC_API_KEY:
        # Fallback: mechanical summary without LLM
        return _mechanical_consolidation(entries, country)

    prompt = _format_entries_for_consolidation(entries, country)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async with anthropic_limiter():
        response = await client.messages.create(
            model=MODEL,
            max_tokens=6048,
            temperature=1,
            thinking={
                "type": "enabled",
                "budget_tokens": 4000,
            },
            system=[{"type": "text", "text": CONSOLIDATION_SYSTEM_PROMPT}],
            messages=[{"role": "user", "content": prompt}],
        )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]

    result = "\n".join(text_parts).strip()

    logger.info(
        f"Consolidation {country}: {len(entries)} entries → summary, "
        f"input={response.usage.input_tokens}, output={response.usage.output_tokens}"
    )

    from ..trace import save_raw_response, extract_thinking, extract_usage
    run_date = entries[0].week if entries else date.today()
    save_raw_response(
        "consolidation", country.lower().replace(" ", "_"), run_date,
        system_prompt=CONSOLIDATION_SYSTEM_PROMPT,
        user_message=prompt,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return result


def _mechanical_consolidation(entries: list[WeeklyEntry], country: str) -> str:
    """Fallback consolidation without LLM — extracts key changes mechanically."""
    if not entries:
        return f"Consolidated history for {country}: 0 entries."

    lines = [
        f"Consolidated history for {country}: "
        f"{entries[0].week.isoformat()} to {entries[-1].week.isoformat()} "
        f"({len(entries)} entries)."
    ]

    deep_dives = [e for e in entries if e.depth == Depth.DEEP_DIVE]
    maintenance = [e for e in entries if e.depth == Depth.MAINTENANCE]
    lines.append(f"{len(deep_dives)} deep dives, {len(maintenance)} maintenance weeks.")

    # Collect significant movements
    movements = []
    for entry in entries:
        if entry.category_movements:
            for cat, mov in entry.category_movements.items():
                if mov.movement == Movement.SIGNIFICANT:
                    movements.append(f"{entry.week}: {cat.value} — {mov.updated_assessment[:150]}")
    if movements:
        lines.append("Significant movements: " + "; ".join(movements[:10]))

    # Collect corrections
    corrections = []
    for entry in entries:
        for sc in entry.self_corrections:
            corrections.append(f"{entry.week}: {sc.category.value} — {sc.correction[:100]}")
    if corrections:
        lines.append("Corrections: " + "; ".join(corrections[:5]))

    # Collect claim changes
    claim_changes = []
    for entry in entries:
        for check in entry.structural_claim_checks:
            if check.status != ClaimStatus.CONFIRMED:
                claim_changes.append(f"[{check.claim_ref}] → {check.status.value}")
    if claim_changes:
        lines.append("Claim status changes: " + "; ".join(claim_changes[:10]))

    return " ".join(lines)


async def run_consolidation(
    ledger: CountryLedger,
    keep: int = 8,
) -> CountryLedger:
    """
    Consolidate a country ledger if it has more entries than the retention window.

    Archives older entries, generates consolidated summary, updates ledger.
    """
    if len(ledger.weekly_entries) <= keep:
        return ledger

    to_consolidate = ledger.weekly_entries[:-keep]
    logger.info(
        f"Consolidating {ledger.code}: {len(to_consolidate)} entries "
        f"({to_consolidate[0].week} to {to_consolidate[-1].week})"
    )

    # Generate consolidated summary
    new_summary = await consolidate_entries(to_consolidate, ledger.country)

    # Append to existing consolidated history
    if ledger.consolidated_history:
        ledger.consolidated_history += f"\n\n---\n\n{new_summary}"
    else:
        ledger.consolidated_history = new_summary

    # Archive via storage layer (which also trims entries)
    from .storage import archive_weekly_entries
    ledger = archive_weekly_entries(ledger, keep=keep)

    return ledger
