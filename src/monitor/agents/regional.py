"""
Regional synthesis agent: stateless cross-country pattern detection.

Input: Country analyses for constituent countries in the region.
Output: Regional report with cross-cutting dynamics, confidence inheritance.
No regional persistence — runs fresh each week.
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    Depth,
    Movement,
    Region,
    SignalCategory,
)
from ..models import CountryLedger, WeeklyEntry

logger = logging.getLogger(__name__)


# =============================================================================
# Data structures
# =============================================================================

@dataclass
class CrossCuttingDynamic:
    """A pattern visible across multiple countries in a region."""
    title: str
    countries_involved: list[str]
    signal_categories: list[str]
    pattern_type: str  # parallel | interaction | institutional | contradiction
    assessment: str
    significance: str
    trend: str  # emerging | developing | established | declining
    confidence: int
    confidence_inherited_from: dict[str, int]
    weakest_link: str
    evidence_against_linkage: str
    linkage_strength: str  # strong | moderate | weak | speculative
    linkage_justification: str
    competing_interpretation: str


@dataclass
class RejectedDynamic:
    """A candidate dynamic that was considered and rejected."""
    candidate_dynamic: str
    countries: list[str]
    reason_rejected: str


@dataclass
class Gap:
    """An expected dynamic from the regional framework that isn't appearing."""
    expected_dynamic: str
    observed: str
    assessment: str


@dataclass
class LowConfidenceItem:
    """A finding inherited from a country assessment with confidence <= 2."""
    item: str
    origin: str
    confidence: int
    note: str


@dataclass
class RegionalReport:
    """Output of a regional synthesis call."""
    region: Region
    week: date
    cross_cutting_dynamics: list[CrossCuttingDynamic] = field(default_factory=list)
    dynamics_considered_and_rejected: list[RejectedDynamic] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    low_confidence_items: list[LowConfidenceItem] = field(default_factory=list)


# =============================================================================
# Region → country mapping
# =============================================================================

REGION_COUNTRIES: dict[Region, list[str]] = {
    Region.AMERICAS: ["ca", "mx", "br", "cl"],
    Region.WESTERN_EUROPE: ["fr", "de", "gb", "it", "es", "no", "se"],
    Region.FRONTLINE_EASTERN_EUROPE: ["ua", "pl", "fi", "ee", "lt", "lv", "cz", "ro"],
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: ["tr", "sa", "ae", "in"],
    Region.ASIA_PACIFIC: ["tw", "jp", "kr", "au", "id"],
}

REGION_DISPLAY_NAMES: dict[Region, str] = {
    Region.AMERICAS: "Americas",
    Region.WESTERN_EUROPE: "Western Europe",
    Region.FRONTLINE_EASTERN_EUROPE: "Frontline & Eastern Europe",
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: "Middle East, Turkey & South Asia",
    Region.ASIA_PACIFIC: "Asia-Pacific",
}


def get_region_countries(region: Region) -> list[str]:
    return REGION_COUNTRIES.get(region, [])


# =============================================================================
# System prompt template
# =============================================================================

REGIONAL_SYSTEM_PROMPT_TEMPLATE = """\
## Role

You are a regional intelligence analyst producing a cross-country assessment for \
{{REGION}}. Your job is to find patterns, interactions, and contradictions that are \
invisible when reading any single country's analysis in isolation but become visible \
when the reports are read together.

You are not a summarizer. If a development is relevant to only one country with no \
cross-cutting implications, it does not belong in your output. The country desk \
already covered it. Your value is exclusively in what emerges from reading the reports \
side by side.

---

## Your Inputs

**COUNTRY ANALYSES** — The weekly entries from each country desk in this region. \
These include: activity level, category movements with developments and confidence \
scores, absence checks, devil's advocate challenges, and self-corrections. You \
receive only the current week's entries — you have no memory of prior weeks' regional \
analyses.

The countries in {{REGION}} are:
{{COUNTRY_LIST}}

---

## What You Are Looking For

### Parallel Behavior

Are multiple countries doing similar things in the same signal category? If so, \
determine which explanation fits:

- **Coordination:** The countries are deliberately acting in concert. Evidence would \
include: joint statements, synchronized timing that can't be coincidental, shared \
institutional mechanisms (EU council decisions, NATO planning cycles), or diplomatic \
communication preceding parallel action.
- **Contagion:** One country's action triggered others to follow. Evidence would \
include: clear temporal sequence (Country A acted first, B and C followed), explicit \
references to Country A's action in B and C's justifications, or media framing in B \
and C that references A.
- **Coincidence:** The countries are responding independently to the same structural \
condition. Evidence would include: different stated motivations, different institutional \
mechanisms, no diplomatic coordination, and a shared external pressure (e.g., US policy \
change, commodity price shock) that would independently produce similar responses.

You must evaluate all three before concluding. Do not default to the most interesting \
explanation.

### Interaction Effects

Is Country A's action creating consequences in Country B? This is directional — \
identify the causal chain. A French defense procurement decision might change Poland's \
calculus about European defense autonomy. A Turkish diplomatic move might constrain or \
enable India's positioning. Interaction effects are the highest-value regional findings \
because they reveal structural relationships that persist beyond any single week's events.

### Institutional Dynamics

How are regional institutions being shaped by individual country developments? Are \
members pulling in the same direction or fragmenting? Is institutional capacity being \
built, eroded, or redirected? For EU/NATO countries, is there a gap between institutional \
commitments and observed behavior?

### Contradictions

Are stated positions consistent with observed behavior? Is a country saying one thing at \
summits and doing another in bilateral channels? Are allies coherent with each other — or \
is one ally's action undermining another's stated position?

### Gaps

What dynamics does the regional framework predict should be active but aren't appearing? \
A predicted dynamic that doesn't materialize is analytically significant — it either means \
the structural conditions have changed (which should be flagged) or the country desks have \
a collection gap in that area.

---

## Critical Rules

### 1. Confidence Inheritance

You cannot make a regional claim with confidence higher than the lowest confidence score \
among its supporting country-level assessments. This is absolute.

If Mexico's alignment_diplomatic assessment has confidence 4 and Canada's has confidence \
2, any dynamic linking them is capped at 2. Document the inheritance: list which country \
assessments support the dynamic and their confidence scores. Identify the weakest link — \
the specific country assessment that caps the regional confidence.

### 2. Low-Confidence Quarantine

Country-level assessments with confidence scores of 1 or 2 must not be synthesized into \
regional dynamics without an explicit disclaimer. List them separately in \
`low_confidence_items`. They are included for awareness — the executive analyst may choose \
to investigate further — but they are not robust enough to support cross-country claims.

### 3. Apophenia Check

For every cross-cutting dynamic you identify, you must provide:

- **evidence_against_linkage**: Reasons these events may be unrelated. This is not \
optional. If you cannot articulate why the pattern might be spurious, you haven't thought \
hard enough about it.
- **linkage_strength**: strong, moderate, weak, or speculative.
  - *Strong*: Direct evidence of connection (shared institutional mechanism, explicit \
coordination, documented causal chain).
  - *Moderate*: Circumstantial evidence of connection (temporal proximity with plausible \
mechanism, shared structural pressures with parallel responses).
  - *Weak*: Pattern exists but connection is ambiguous (similar actions in the same \
timeframe without clear mechanism).
  - *Speculative*: Interesting parallel but no evidence beyond surface similarity.
- **linkage_justification**: Why these events are connected beyond temporal coincidence \
or surface-level similarity. What mechanism links them?

### 4. Rejection Log

You must record dynamics you considered but rejected in `dynamics_considered_and_rejected`. \
This is mandatory. An empty rejection log tells the executive analyst that you did not \
critically evaluate candidate patterns — you either accepted everything you saw or didn't \
look hard enough.

For each rejected candidate, explain specifically why you rejected it. "Insufficient \
evidence" is not specific enough. "The temporal overlap between Brazil's trade announcement \
and Chile's mining regulation was coincidental — Brazil's announcement was scheduled months \
ago per their legislative calendar, and Chile's regulation responds to a domestic \
environmental ruling, not regional trade dynamics" — that's a rejection.

---

## Your Output

```json
{
  "region": "{{REGION}}",
  "analysis_date": "{{ANALYSIS_DATE}}",
  "source_reports": ["mx_{{ANALYSIS_DATE}}", "ca_{{ANALYSIS_DATE}}", ...],

  "cross_cutting_dynamics": [
    {
      "title": "Descriptive title of the dynamic",
      "countries_involved": ["mx", "ca"],
      "signal_categories": ["alignment_diplomatic", "economic_tech"],
      "pattern_type": "parallel | interaction | institutional | contradiction",
      "assessment": "What is happening across countries...",
      "significance": "Why this matters at the regional level...",
      "trend": "emerging | developing | established | declining",
      "confidence": 3,
      "confidence_inherited_from": {
        "mx_alignment_diplomatic": 4,
        "ca_alignment_diplomatic": 3
      },
      "weakest_link": "Canada's assessment rests on single wire report...",
      "evidence_against_linkage": "Reasons these events may be unrelated...",
      "linkage_strength": "moderate",
      "linkage_justification": "Why these events are connected beyond coincidence...",
      "competing_interpretation": "Alternative explanation for the apparent pattern..."
    }
  ],

  "dynamics_considered_and_rejected": [
    {
      "candidate_dynamic": "Pattern that was considered",
      "countries": ["br", "cl"],
      "reason_rejected": "Specific explanation..."
    }
  ],

  "gaps": [
    {
      "expected_dynamic": "What the regional framework predicts should be active...",
      "observed": "What appeared or didn't...",
      "assessment": "What the gap means..."
    }
  ],

  "low_confidence_items": [
    {
      "item": "Any finding inherited from a country assessment with confidence <= 2",
      "origin": "Which country and signal category",
      "confidence": 2,
      "note": "Included for awareness, not synthesized into dynamics"
    }
  ]
}
```

---

## What You Must Not Do

- Do not summarize country reports. The reader has access to them. Your job is to find \
what no single report reveals on its own.
- Do not include single-country developments unless they have cross-cutting implications.
- Do not force dynamics to fill the regional framework. If the framework predicts five \
dynamics and you find two, report two.
- Do not synthesize low-confidence country assessments into regional dynamics without \
quarantining them. Confidence 1-2 findings go in `low_confidence_items`, not in \
`cross_cutting_dynamics`.
- Do not assign a regional confidence higher than the lowest supporting country \
confidence. This rule has no exceptions.

No commentary outside the JSON."""


def _build_system_prompt(region: Region) -> str:
    """Fill template variables in the system prompt."""
    display_name = REGION_DISPLAY_NAMES.get(region, region.value)
    country_codes = get_region_countries(region)
    country_list = ", ".join(c.upper() for c in country_codes)

    prompt = REGIONAL_SYSTEM_PROMPT_TEMPLATE
    prompt = prompt.replace("{{REGION}}", display_name)
    prompt = prompt.replace("{{COUNTRY_LIST}}", country_list)
    return prompt


# =============================================================================
# Prompt construction
# =============================================================================

def _format_country_analysis(
    code: str,
    ledger: CountryLedger,
    entry: Optional[WeeklyEntry],
) -> str:
    """Format a single country's analysis for regional synthesis input."""
    lines = [f"### {ledger.country} ({code.upper()}) — {entry.depth.value if entry else 'no entry'}\n"]

    # Posture summary
    lines.append(f"Posture: {ledger.posture_summary.text}")
    lines.append("")

    if entry is None:
        lines.append("No weekly entry available.\n")
        return "\n".join(lines)

    # Activity level
    if entry.activity_level:
        lines.append(f"Activity: {entry.activity_level.get('rating', 'unknown')} — "
                      f"{entry.activity_level.get('rationale', '')}")

    # Category movements
    if entry.category_movements:
        for cat, mov in entry.category_movements.items():
            if mov.movement != Movement.NONE:
                lines.append(f"\n**{cat.value}**: {mov.movement.value}")
                if mov.updated_assessment:
                    lines.append(f"  Assessment: {mov.updated_assessment}")
                if mov.confidence_change:
                    lines.append(
                        f"  Confidence: {mov.confidence_change.from_} → {mov.confidence_change.to}"
                    )
                for d in mov.developments:
                    lines.append(f"  - {d.headline} ({d.source}, tier {d.source_tier})")
            else:
                # Still note the current assessment for "none" movements
                lines.append(f"\n**{cat.value}**: no movement")

    # Signal category confidences (for inheritance)
    lines.append("\nConfidence levels:")
    for cat, assessment in ledger.signal_categories.items():
        lines.append(f"  {cat.value}: {assessment.confidence}")

    # Devil's advocate highlights
    if entry.devils_advocate and entry.devils_advocate.challenges:
        lines.append("\nDevil's advocate challenges:")
        for c in entry.devils_advocate.challenges[:3]:
            lines.append(f"  - {c[:200]}")

    lines.append("")
    return "\n".join(lines)


def _build_regional_prompt(
    region: Region,
    ledgers: dict[str, CountryLedger],
    entries: dict[str, Optional[WeeklyEntry]],
    week: Optional[date] = None,
) -> str:
    region_codes = get_region_countries(region)

    country_sections = []
    for code in region_codes:
        if code in ledgers:
            entry = entries.get(code)
            country_sections.append(_format_country_analysis(code, ledgers[code], entry))

    if not country_sections:
        return f"No country analyses available for {region.value}."

    countries_block = "\n".join(country_sections)
    analysis_date = (week or date.today()).isoformat()

    return f"""\
Regional synthesis for: {REGION_DISPLAY_NAMES.get(region, region.value)}
Analysis date: {analysis_date}

Countries in this region: {', '.join(c.upper() for c in region_codes)}

## COUNTRY ANALYSES

{countries_block}

Identify cross-country patterns, apply confidence inheritance, quarantine low-confidence \
assessments, and produce the JSON output as specified in your instructions."""


# =============================================================================
# Response parsing
# =============================================================================

def parse_regional_response(response_text: str, region: Region, week: date) -> RegionalReport:
    """Parse the regional synthesis JSON response."""
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    data = json.loads(text)

    dynamics = []
    for d in data.get("cross_cutting_dynamics", []):
        dynamics.append(CrossCuttingDynamic(
            title=d["title"],
            countries_involved=d["countries_involved"],
            signal_categories=d["signal_categories"],
            pattern_type=d.get("pattern_type", d.get("linkage_type", "parallel")),
            assessment=d["assessment"],
            significance=d.get("significance", ""),
            trend=d.get("trend", "emerging"),
            confidence=d["confidence"],
            confidence_inherited_from=d["confidence_inherited_from"],
            weakest_link=d.get("weakest_link", ""),
            evidence_against_linkage=d.get("evidence_against_linkage", ""),
            linkage_strength=d.get("linkage_strength", "moderate"),
            linkage_justification=d.get("linkage_justification", ""),
            competing_interpretation=d.get("competing_interpretation", ""),
        ))

    # Parse rejected dynamics (support both key names)
    rejected_raw = data.get("dynamics_considered_and_rejected", data.get("rejection_log", []))
    rejected = [
        RejectedDynamic(
            candidate_dynamic=r.get("candidate_dynamic", r.get("candidate", "")),
            countries=r.get("countries", r.get("countries_considered", [])),
            reason_rejected=r["reason_rejected"],
        )
        for r in rejected_raw
    ]

    # Parse gaps
    gaps = [
        Gap(
            expected_dynamic=g["expected_dynamic"],
            observed=g.get("observed", ""),
            assessment=g.get("assessment", ""),
        )
        for g in data.get("gaps", [])
    ]

    # Parse low confidence items (support both key names)
    lc_raw = data.get("low_confidence_items", data.get("low_confidence_quarantine", []))
    low_confidence = [
        LowConfidenceItem(
            item=lc.get("item", lc.get("assessment", "")),
            origin=lc.get("origin", f"{lc.get('country', '?')}_{lc.get('category', '?')}"),
            confidence=lc.get("confidence", 2),
            note=lc.get("note", lc.get("reason_quarantined", "")),
        )
        for lc in lc_raw
    ]

    return RegionalReport(
        region=region,
        week=week,
        cross_cutting_dynamics=dynamics,
        dynamics_considered_and_rejected=rejected,
        gaps=gaps,
        low_confidence_items=low_confidence,
    )


# =============================================================================
# Entry point
# =============================================================================

async def run_regional_synthesis(
    region: Region,
    ledgers: dict[str, CountryLedger],
    entries: dict[str, Optional[WeeklyEntry]],
    week: date | None = None,
) -> RegionalReport:
    """
    Run stateless regional synthesis for a single editorial region.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    week = week or date.today()
    prompt = _build_regional_prompt(region, ledgers, entries, week)
    system_prompt = _build_system_prompt(region)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    logger.info(f"Regional synthesis: {region.value}")

    response = await client.messages.create(
        model=MODEL,
        max_tokens=8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000,
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
        f"Regional synthesis {region.value}: "
        f"input={response.usage.input_tokens}, "
        f"output={response.usage.output_tokens}"
    )

    return parse_regional_response(response_text, region, week)


async def run_all_regional_syntheses(
    ledgers: dict[str, CountryLedger],
    entries: dict[str, Optional[WeeklyEntry]],
    week: date | None = None,
    max_concurrent: int = 5,
) -> dict[Region, RegionalReport]:
    """Run regional synthesis for all 5 regions in parallel."""
    import asyncio

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _run(region: Region) -> tuple[Region, RegionalReport]:
        async with semaphore:
            report = await run_regional_synthesis(region, ledgers, entries, week)
            return region, report

    tasks = [_run(region) for region in Region]
    results = await asyncio.gather(*tasks)
    return dict(results)
