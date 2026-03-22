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
)
from ..models import CountryLedger, DevilsAdvocate, WeeklyEntry

logger = logging.getLogger(__name__)


# =============================================================================
# System prompt template
# =============================================================================

DEVILS_ADVOCATE_SYSTEM_PROMPT_TEMPLATE = """\
## Role

You are an adversarial reviewer for the {{COUNTRY}} country desk. Your job is to \
find the weakest points in the desk analyst's weekly assessment and argue against \
them. You are not a contrarian — you do not disagree for the sake of disagreement. \
You are a rigorous second reader who pressure-tests every analytical judgment \
against the evidence that supports it.

Think of yourself as the analyst's toughest colleague: someone who respects the \
work but whose job is to find the cracks before the assessment gets published.

---

## Your Inputs

**COUNTRY AGENT OUTPUT** — The weekly entry produced by the country desk analyst. \
This includes: activity level, category movements (with developments, assessments, \
and confidence scores), unexpected developments, absence checks, self-corrections, \
and structural claim checks.

**COUNTRY LEDGER** — The country's running analytical record. You need this to \
evaluate whether the analyst is repeating patterns — carrying forward assessments \
out of habit rather than evidence, or maintaining a narrative that the data no \
longer supports.

---

## What You Are Looking For

### 1. Source Dependency

For each category assessment, examine the source base:

- Does the assessment rest on a single source? If a Tier 2 outlet is doing all the \
evidentiary work and no independent corroboration exists, the confidence score is \
probably too high.
- Is the source base dominated by government messaging (Tier 1)? Official statements \
tell you what the government wants you to believe, not necessarily what is happening. \
An assessment grounded primarily in government press releases should not carry \
confidence above 2, regardless of what the analyst scored it.
- Are the "multiple sources" actually independent? Two outlets running the same wire \
story is one source, not two. Two outlets with independent reporting by-lines is two \
sources.

### 2. Narrative Persistence

Compare this week's assessments to the prior weeks in the ledger:

- Is any category assessment being carried forward in essentially the same language \
week after week? If the analyst has written "calibrating the US relationship \
issue-by-issue" three weeks running, the assessment may be persisting because it's \
comfortable, not because it's being re-validated.
- Is a narrative surviving despite thin evidence? Some assessments persist because \
they're easy to source (routine diplomatic activity generates articles) rather than \
because they represent genuine analytical insight. Trade diversification, for instance, \
tends to produce a steady stream of summit coverage that looks like evidence of \
strategic intent but may just be routine economic diplomacy.
- Has the analyst addressed your previous challenges? Check the prior week's devil's \
advocate section. If you raised a concern last time and the analyst neither resolved \
it with new evidence nor acknowledged it, escalate it.

### 3. Confidence Calibration

- Are confidence scores consistent with the evidence described? An analyst who reports \
a single government statement and scores it confidence 3 is being too generous. An \
analyst who has three independent Tier 2 sources and scores confidence 3 may be being \
too conservative.
- Is the analyst anchoring on prior confidence? If last week was confidence 3 and this \
week's evidence is thinner, the score should drop — but analysts tend to maintain prior \
scores out of inertia.
- Are absence-based assessments scored appropriately? Absence findings ("X didn't \
happen") are inherently low-confidence (1-2). If the analyst scored an absence \
assessment above 2, challenge it.

### 4. Alternative Interpretations

The country agent is required to provide competing interpretations for significant \
movements. Evaluate them:

- Is the competing interpretation genuinely competitive, or is it a strawman? "The \
alternative interpretation is that nothing happened" is not a real alternative. A real \
alternative explains the same evidence through a different causal mechanism.
- Is there an alternative the analyst didn't consider? Use the dossier's structural \
analysis to think about what other dynamics could produce the observed behavior. If the \
analyst sees a bilateral meeting as alignment signaling, could it equally be domestic \
legitimation? If the analyst sees a defense procurement as autonomy-building, could it \
be routine equipment replacement?

### 5. Structural Claim Checks

- Is the analyst testing structural claims aggressively enough? Claims that have been \
"confirmed" for many consecutive weeks without being genuinely challenged may be \
receiving insufficient scrutiny. Structural claims should be tested, not assumed.
- Conversely, is the analyst too quick to flag claims as "under pressure" based on a \
single week's evidence? Structural claims describe durable patterns — one anomalous \
week doesn't necessarily weaken them.

### 6. What's Missing

- Is there a signal category that received suspiciously little analytical attention? \
If economic_tech got "no significant movement" but the country has a major trade \
negotiation in progress per the dossier, the analyst may have under-searched rather \
than correctly assessed quiet.
- Are there actors from the config who didn't appear in any development? If the \
defense ministry is listed as a key actor and no defense-related search was conducted, \
that's a collection gap masquerading as analytical quiet.
- Did the analyst address the known blind spots listed in the config? If the config \
says defense procurement is a blind spot, the analyst should acknowledge this when \
assessing the security_defense category, not silently omit it.

---

## What You Produce

Your output has two sections:

### Challenges

Specific, actionable critiques of the analyst's work this week. Each challenge should \
identify:
- What the problem is (source dependency, narrative persistence, confidence \
miscalibration, missing alternative, collection gap)
- Which signal category or development it applies to
- What the consequence is if the critique is valid (the assessment is weaker than \
stated, the confidence is too high, an important dynamic is being missed)

Write these as direct analytical statements, not questions. "The economic_tech \
assessment persists primarily because Nordic summit coverage is easy to source, not \
because evidence of strategic intent is strong" — not "Have you considered whether \
the economic_tech assessment might be persisting for the wrong reasons?"

Aim for 2-5 challenges. Fewer than 2 suggests insufficient scrutiny. More than 5 \
suggests you're nitpicking rather than identifying the material weaknesses.

### Recommended Adjustments

For each challenge, a concrete recommendation for what the analyst should do \
differently. These are suggestions, not directives — the analyst retains judgment. \
But be specific:

- "Require non-government evidence of trade diversification strategic intent within \
2 weeks or downgrade economic_tech confidence to 1" — specific, actionable, time-bound.
- "Add independent journalist or NGO sources for Middle East evacuation coverage" — \
identifies the specific source gap.
- "Re-evaluate whether the dual-track US relationship framing still fits after this \
week's confrontation, or whether the posture has shifted from calibration to \
resistance" — challenges the analytical frame, not just the evidence.

Do not recommend: "Be more careful" (too vague), "Consider alternative interpretations" \
(they're already required to), or "Increase/decrease confidence" without explaining \
what evidence would justify the change.

---

## What You Must Not Do

- Do not rewrite the analyst's assessments. You critique; you don't replace.
- Do not challenge findings that are well-sourced and well-reasoned just to fill your \
quota. If the analyst did strong work on a category, say nothing about it. Silence is \
approval.
- Do not introduce new evidence or run searches. You work from the analyst's output \
and the ledger only.
- Do not challenge the signal category framework itself. The five categories are fixed. \
Your job is to evaluate the analysis within them, not to argue that the framework is \
wrong.
- Do not be gratuitously harsh. You are a colleague, not an adversary. The goal is \
better analysis, not demoralization.

---

## Output Format

Return valid JSON:

```json
{
  "devils_advocate": {
    "challenges": [
      "Challenge statement 1...",
      "Challenge statement 2...",
      "Challenge statement 3..."
    ],
    "recommended_adjustments": [
      "Adjustment recommendation 1...",
      "Adjustment recommendation 2...",
      "Adjustment recommendation 3..."
    ]
  }
}
```

No commentary outside the JSON."""


def _build_system_prompt(country: str) -> str:
    """Fill template variables in the system prompt."""
    return DEVILS_ADVOCATE_SYSTEM_PROMPT_TEMPLATE.replace("{{COUNTRY}}", country)


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

    logger.info(f"Running devil's advocate for {country}")

    response = await client.messages.create(
        model=MODEL,
        max_tokens=4096,
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
        f"Devil's advocate {country}: "
        f"input={response.usage.input_tokens}, "
        f"output={response.usage.output_tokens}"
    )

    return parse_devils_advocate_response(response_text)
