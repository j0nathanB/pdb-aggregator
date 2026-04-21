"""
Regional synthesis agent: stateless cross-country pattern detection.

Input: Country analyses for constituent countries in the region.
Output: Regional report with cross-cutting dynamics, confidence inheritance.
No regional persistence — runs fresh each week.
"""

import logging
import os
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

import anthropic

from ..rate_limit import anthropic_limiter

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    Depth,
    Movement,
    Region,
    SignalCategory,
    load_prompt,
)
from ..models import CountryLedger, WeeklyEntry
from ..sanitize import _record_fallback, extract_json

logger = logging.getLogger(__name__)

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"

REGIONAL_SYNTHESIS_TOOL_NAME = "record_regional_synthesis"
REGIONAL_SYNTHESIS_TOOL = {
    "name": REGIONAL_SYNTHESIS_TOOL_NAME,
    "description": (
        "Record the regional synthesis output. Call exactly once when the "
        "full analysis is complete."
    ),
    "input_schema": {
        "type": "object",
        "required": ["regional_overview"],
        "properties": {
            "regional_overview": {"type": "string"},
            "regional_highlights": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["country", "headline"],
                    "properties": {
                        "country": {"type": "string"},
                        "headline": {"type": "string"},
                        "key_facts": {"type": "array", "items": {"type": "string"}},
                        "signal_categories": {"type": "array", "items": {"type": "string"}},
                        "tension": {"type": "string"},
                        "confidence": {"type": "integer"},
                    },
                },
            },
            "cross_cutting_dynamics": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["title", "countries_involved", "assessment", "confidence"],
                    "properties": {
                        "title": {"type": "string"},
                        "countries_involved": {"type": "array", "items": {"type": "string"}},
                        "signal_categories": {"type": "array", "items": {"type": "string"}},
                        "pattern_type": {"type": "string"},
                        "assessment": {"type": "string"},
                        "significance": {"type": "string"},
                        "trend": {"type": "string"},
                        "confidence": {"type": "integer"},
                        "confidence_inherited_from": {
                            "type": "object",
                            "additionalProperties": {"type": "integer"},
                        },
                        "weakest_link": {"type": "string"},
                        "evidence_against_linkage": {"type": "string"},
                        "linkage_strength": {"type": "string"},
                        "linkage_justification": {"type": "string"},
                        "competing_interpretation": {"type": "string"},
                    },
                },
            },
            "dynamics_considered_and_rejected": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["reason_rejected"],
                    "properties": {
                        "candidate_dynamic": {"type": "string"},
                        "countries": {"type": "array", "items": {"type": "string"}},
                        "reason_rejected": {"type": "string"},
                    },
                },
            },
            "gaps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["expected_dynamic"],
                    "properties": {
                        "expected_dynamic": {"type": "string"},
                        "observed": {"type": "string"},
                        "assessment": {"type": "string"},
                    },
                },
            },
            "low_confidence_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "item": {"type": "string"},
                        "origin": {"type": "string"},
                        "confidence": {"type": "integer"},
                        "note": {"type": "string"},
                    },
                },
            },
        },
    },
}


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
class RegionalHighlight:
    """A significant single-country development highlighted at regional level."""
    country: str
    headline: str
    key_facts: list[str] = field(default_factory=list)
    signal_categories: list[str] = field(default_factory=list)
    tension: str = ""
    confidence: int = 3


@dataclass
class RegionalReport:
    """Output of a regional synthesis call."""
    region: Region
    week: date
    regional_overview: str = ""
    regional_highlights: list[RegionalHighlight] = field(default_factory=list)
    cross_cutting_dynamics: list[CrossCuttingDynamic] = field(default_factory=list)
    dynamics_considered_and_rejected: list[RejectedDynamic] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    low_confidence_items: list[LowConfidenceItem] = field(default_factory=list)


# =============================================================================
# Region → country mapping
# =============================================================================

REGION_COUNTRIES: dict[Region, list[str]] = {
    Region.CENTRAL_EASTERN_EUROPE: ["ua", "pl", "cz", "ro", "hu"],
    Region.NORDIC_BALTIC: ["fi", "ee", "lt", "lv", "no", "se"],
    Region.WESTERN_EUROPE: ["fr", "de", "gb", "it", "es"],
    Region.ASIA_PACIFIC: ["tw", "jp", "kr", "au", "id"],
    Region.NEAR_EAST_SOUTH_ASIA: ["tr", "sa", "ae", "in", "pk"],
    Region.AMERICAS: ["ca", "mx", "br", "cl"],
}

REGION_DISPLAY_NAMES: dict[Region, str] = {
    Region.CENTRAL_EASTERN_EUROPE: "Central-Eastern Europe",
    Region.NORDIC_BALTIC: "Nordic-Baltic",
    Region.WESTERN_EUROPE: "Western Europe",
    Region.ASIA_PACIFIC: "Asia-Pacific",
    Region.NEAR_EAST_SOUTH_ASIA: "Near East and South Asia",
    Region.AMERICAS: "Americas",
}


def get_region_countries(region: Region) -> list[str]:
    return REGION_COUNTRIES.get(region, [])


# =============================================================================
# System prompt template
# =============================================================================

REGIONAL_SYSTEM_PROMPT_TEMPLATE = load_prompt("agents/regional_synthesis")


def _build_system_prompt(region: Region) -> str:
    """Fill template variables in the system prompt."""
    display_name = REGION_DISPLAY_NAMES.get(region, region.value)
    country_codes = get_region_countries(region)
    country_list = ", ".join(c.upper() for c in country_codes)

    return load_prompt(
        "agents/regional_synthesis",
        REGION=display_name,
        COUNTRY_LIST=country_list,
    )


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

def parse_regional_data(data: dict, region: Region, week: date) -> RegionalReport:
    """Build a RegionalReport from an already-parsed data dict."""
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

    # Parse regional highlights
    highlights = [
        RegionalHighlight(
            country=h.get("country", ""),
            headline=h.get("headline", ""),
            key_facts=h.get("key_facts", []),
            signal_categories=h.get("signal_categories", []),
            tension=h.get("tension", ""),
            confidence=h.get("confidence", 3),
        )
        for h in data.get("regional_highlights", [])
    ]

    return RegionalReport(
        region=region,
        week=week,
        regional_overview=data.get("regional_overview", ""),
        regional_highlights=highlights,
        cross_cutting_dynamics=dynamics,
        dynamics_considered_and_rejected=rejected,
        gaps=gaps,
        low_confidence_items=low_confidence,
    )


def parse_regional_response(response_text: str, region: Region, week: date) -> RegionalReport:
    """Parse the regional synthesis JSON response."""
    data = extract_json(response_text, context=f"regional_{region.value}")
    return parse_regional_data(data, region, week)


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

    countries_in = sorted(ledgers.keys())
    entries_with_data = [k for k, v in entries.items() if v is not None]
    logger.info(
        "Regional synthesis %s: %d country ledgers, %d entries with data",
        region.value, len(ledgers), len(entries_with_data),
    )
    logger.debug("Regional %s: countries=%s, prompt=%d chars", region.value, countries_in, len(prompt))

    from ..timing import with_heartbeat
    create_kwargs: dict = dict(
        model=MODEL,
        max_tokens=18192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": prompt}],
    )
    if USE_TOOL_SCHEMA:
        create_kwargs["tools"] = [REGIONAL_SYNTHESIS_TOOL]

    async with anthropic_limiter():
        response = await with_heartbeat(
            client.messages.create(**create_kwargs),
            f"Regional synthesis {region.value}: API call",
        )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    tool_input: dict | None = None
    if USE_TOOL_SCHEMA:
        for block in response.content:
            if (getattr(block, "type", None) == "tool_use"
                    and getattr(block, "name", None) == REGIONAL_SYNTHESIS_TOOL_NAME):
                tool_input = getattr(block, "input", None)
                break

    logger.info(
        "Regional synthesis %s: API complete — input=%d, output=%d tokens%s",
        region.value, response.usage.input_tokens, response.usage.output_tokens,
        " [tool_use]" if tool_input else "",
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage

    if tool_input is not None:
        import json as _json
        save_raw_response(
            "regional", region.value, week,
            system_prompt=system_prompt,
            user_message=prompt,
            response_text=_json.dumps(tool_input, indent=2, ensure_ascii=False),
            thinking_text=extract_thinking(response),
            usage=extract_usage(response),
        )
        result = parse_regional_data(tool_input, region, week)
    else:
        if USE_TOOL_SCHEMA:
            logger.warning(
                "Regional synthesis %s: tool_use enabled but no valid block; falling back",
                region.value,
            )
            _record_fallback("regional_tool_use_fallback")
        save_raw_response(
            "regional", region.value, week,
            system_prompt=system_prompt,
            user_message=prompt,
            response_text=response_text,
            thinking_text=extract_thinking(response),
            usage=extract_usage(response),
        )
        result = parse_regional_response(response_text, region, week)

    logger.info(
        "Regional %s: %d cross-cutting dynamics, %d gaps",
        region.value, len(result.cross_cutting_dynamics), len(result.gaps),
    )
    update_trace_parsed("regional", region.value, week, parsed_output=result)

    return result


async def run_all_regional_syntheses(
    ledgers: dict[str, CountryLedger],
    entries: dict[str, Optional[WeeklyEntry]],
    week: date | None = None,
    max_concurrent: int = 5,
    regions: list[Region] | None = None,
) -> dict[Region, RegionalReport]:
    """Run regional synthesis for all 6 regions in parallel.

    Args:
        regions: Optional filter — only synthesize these regions. Default
            (None) processes every member of the Region enum.
    """
    import asyncio

    from ..timing import TrackedSemaphore
    semaphore = TrackedSemaphore(max_concurrent, "regional")

    async def _run(region: Region) -> tuple[Region, RegionalReport]:
        async with semaphore.acquire(region.value):
            report = await run_regional_synthesis(region, ledgers, entries, week)
            return region, report

    target_regions = regions if regions is not None else list(Region)
    tasks = [_run(region) for region in target_regions]
    results = await asyncio.gather(*tasks)
    return dict(results)
