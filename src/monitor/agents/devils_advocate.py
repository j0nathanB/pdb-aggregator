"""
Devil's advocate agent: argues against the country agent's assessments.

Separate call per deep-dive country. Input is the country agent's weekly entry
(before ledger write) plus the country ledger for narrative persistence checks.
Output is the devils_advocate section appended to the entry.
"""

import json
import logging
import re
from datetime import date
from typing import Optional

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    Depth,
    Movement,
    SignalCategory,
    load_prompt,
)
from ..models import CountryLedger, DevilsAdvocate, WeeklyEntry

logger = logging.getLogger(__name__)


# =============================================================================
# System prompt template
# =============================================================================

DEVILS_ADVOCATE_SYSTEM_PROMPT_TEMPLATE = load_prompt("devils_advocate")


def _build_system_prompt(country: str) -> str:
    """Fill template variables in the system prompt."""
    return load_prompt("devils_advocate", COUNTRY=country)


# =============================================================================
# Prompt construction
# =============================================================================

def _build_devils_advocate_prompt(
    entry: WeeklyEntry,
    country: str,
    ledger: Optional[CountryLedger] = None,
) -> str:
    """Format the weekly entry and ledger context for devil's advocate review."""
    lines = [f"## Country Agent Weekly Entry: {country}\n"]
    lines.append(f"Week: {entry.week.isoformat()}")
    lines.append(f"Date range: {entry.date_range}")

    if entry.activity_level:
        lines.append(f"Activity level: {entry.activity_level.get('rating', 'unknown')} — "
                      f"{entry.activity_level.get('rationale', '')}")
    lines.append("")

    # Category movements
    if entry.category_movements:
        lines.append("## CATEGORY ASSESSMENTS\n")
        for cat, mov in entry.category_movements.items():
            lines.append(f"### {cat.value}: movement={mov.movement.value}")
            if mov.developments:
                for d in mov.developments:
                    lines.append(f"  - {d.headline} (source: {d.source}, tier {d.source_tier})")
                    if d.summary:
                        lines.append(f"    {d.summary}")
            if mov.prior_assessment:
                lines.append(f"  Prior: {mov.prior_assessment}")
            if mov.updated_assessment:
                lines.append(f"  Updated: {mov.updated_assessment}")
            if mov.confidence_change:
                lines.append(
                    f"  Confidence: {mov.confidence_change.from_} → {mov.confidence_change.to} "
                    f"({mov.confidence_change.reason})"
                )
            lines.append("")

    # Unexpected developments
    if entry.unexpected_developments:
        lines.append("## UNEXPECTED DEVELOPMENTS\n")
        for u in entry.unexpected_developments:
            lines.append(f"- {u.headline} (source: {u.source}, tier {u.source_tier})")
            if u.assessment:
                lines.append(f"  Assessment: {u.assessment}")
        lines.append("")

    # Absence checks
    if entry.absence_check:
        lines.append("## ABSENCE CHECKS\n")
        for a in entry.absence_check:
            status = "occurred" if a.occurred else "did NOT occur"
            lines.append(f"- Expected: {a.expected} — {status}")
            if a.significance:
                lines.append(f"  Significance: {a.significance}")
            lines.append(f"  Confidence: {a.confidence}")
        lines.append("")

    # Self-corrections
    if entry.self_corrections:
        lines.append("## SELF-CORRECTIONS\n")
        for sc in entry.self_corrections:
            lines.append(f"- {sc.category.value} (prior week {sc.prior_week}): {sc.correction[:200]}")
            lines.append(f"  Root cause: {sc.root_cause}")
        lines.append("")

    # Structural claim checks
    if entry.structural_claim_checks:
        lines.append("## STRUCTURAL CLAIM CHECKS\n")
        for c in entry.structural_claim_checks:
            lines.append(f"- [{c.claim_ref}] status={c.status.value}: {c.claim_text[:150]}")
            if c.evidence:
                lines.append(f"  Evidence: {c.evidence}")
        lines.append("")

    # Ledger context for narrative persistence checks
    if ledger:
        lines.append("## COUNTRY LEDGER CONTEXT\n")

        # Prior assessments for narrative persistence comparison
        lines.append("### Prior Signal Category Assessments")
        for cat, assessment in ledger.signal_categories.items():
            lines.append(f"  {cat.value}: {assessment.current_assessment[:200]}")
            lines.append(f"    Confidence: {assessment.confidence}")
        lines.append("")

        # Recent entries for pattern detection
        recent = ledger.weekly_entries[-3:] if ledger.weekly_entries else []
        if recent:
            lines.append(f"### Recent Weekly Entries (last {len(recent)})")
            for prev_entry in reversed(recent):
                lines.append(f"\n  Week of {prev_entry.week.isoformat()} ({prev_entry.depth.value})")
                if prev_entry.category_movements:
                    for cat, mov in prev_entry.category_movements.items():
                        if mov.movement != Movement.NONE:
                            lines.append(f"    {cat.value}: {mov.movement.value}")
                            if mov.updated_assessment:
                                lines.append(f"      → {mov.updated_assessment[:150]}")
                # Prior DA challenges
                if prev_entry.devils_advocate and prev_entry.devils_advocate.challenges:
                    lines.append("    Prior devil's advocate challenges:")
                    for challenge in prev_entry.devils_advocate.challenges:
                        lines.append(f"      - {challenge[:200]}")
            lines.append("")

        # Structural claims for scrutiny checks
        if ledger.structural_claim_status:
            lines.append("### Structural Claim Status")
            for claim in ledger.structural_claim_status:
                lines.append(
                    f"  [{claim.claim_ref}] {claim.status.value} "
                    f"(last checked: {claim.last_checked}, "
                    f"under pressure: {claim.weeks_under_pressure} weeks)"
                )
            lines.append("")

    return "\n".join(lines)


def parse_devils_advocate_response(response_text: str) -> DevilsAdvocate:
    """Parse the devil's advocate JSON response."""
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    data = json.loads(text)

    # Support both wrapped and unwrapped formats
    da_data = data.get("devils_advocate", data)

    return DevilsAdvocate(
        challenges=da_data.get("challenges", []),
        recommended_adjustments=da_data.get("recommended_adjustments", []),
    )


async def run_devils_advocate(
    entry: WeeklyEntry,
    country: str,
    ledger: Optional[CountryLedger] = None,
) -> DevilsAdvocate:
    """
    Run the devil's advocate against a country agent's weekly entry.

    Args:
        entry: The weekly entry to review.
        country: Country name.
        ledger: Country ledger for narrative persistence checks.

    Returns a DevilsAdvocate object to attach to the entry.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    prompt = _build_devils_advocate_prompt(entry, country, ledger)
    system_prompt = _build_system_prompt(country)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    logger.info("Devil's advocate: starting for %s", country)
    logger.debug(
        "Devil's advocate %s: entry week=%s, %d category movements, prompt=%d chars",
        country, entry.week.isoformat(),
        sum(1 for m in (entry.category_movements or {}).values() if m.movement != Movement.NONE),
        len(prompt),
    )

    response = await client.messages.create(
        model=MODEL,
        max_tokens=12096,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": 8000,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": prompt}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        "Devil's advocate %s: API complete — input=%d, output=%d tokens",
        country, response.usage.input_tokens, response.usage.output_tokens,
    )

    result = parse_devils_advocate_response(response_text)
    logger.info(
        "Devil's advocate %s: %d challenges, %d adjustments",
        country, len(result.challenges), len(result.recommended_adjustments),
    )

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "devils_advocate", country.lower().replace(" ", "_"), entry.week,
        system_prompt=system_prompt,
        user_message=prompt,
        response_text=response_text,
        parsed_output=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return result
