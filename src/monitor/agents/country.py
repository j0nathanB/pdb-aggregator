"""
Country agent (deep dive): search, extract, analyze across five signal categories.

Input: Country dossier + country ledger + whitelisted sources (via web_search).
Output: WeeklyEntry (without devils_advocate) + updated signal categories + posture summary.
"""

import json
import logging
import re
from datetime import date, timedelta
from typing import Optional

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CategoryStatus,
    CountryConfig,
    Depth,
    Movement,
    SignalCategory,
    load_prompt,
)
from ..models import (
    AbsenceCheck,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    Development,
    PostureSummary,
    SelfCorrection,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    UnexpectedDevelopment,
    WeeklyEntry,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Output structure
# =============================================================================

class CountryAgentOutput:
    """Parsed output from the country agent."""

    def __init__(
        self,
        weekly_entry: WeeklyEntry,
        signal_categories: dict[SignalCategory, SignalCategoryAssessment],
        posture_summary: PostureSummary,
    ):
        self.weekly_entry = weekly_entry
        self.signal_categories = signal_categories
        self.posture_summary = posture_summary


# =============================================================================
# System prompt template
# =============================================================================

COUNTRY_AGENT_SYSTEM_PROMPT_TEMPLATE = load_prompt("country_agent")


def _build_system_prompt(config: CountryConfig) -> str:
    """Fill template variables in the system prompt."""
    primary_lang = config.languages.primary

    # Map language codes to readable names for the prompt
    lang_names = {
        "es": "Spanish", "pt": "Portuguese", "fr": "French", "de": "German",
        "ja": "Japanese", "ko": "Korean", "zh": "Chinese", "ar": "Arabic",
        "tr": "Turkish", "uk": "Ukrainian", "pl": "Polish", "cs": "Czech",
        "ro": "Romanian", "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian",
        "fi": "Finnish", "sv": "Swedish", "no": "Norwegian", "it": "Italian",
        "hi": "Hindi", "id": "Indonesian", "en": "English",
    }
    source_language = lang_names.get(primary_lang, primary_lang)

    return load_prompt(
        "country_agent",
        COUNTRY=config.country,
        SOURCE_LANGUAGE=source_language,
    )


# =============================================================================
# Prompt construction
# =============================================================================

def _build_ledger_context(ledger: CountryLedger, max_entries: int = 4) -> str:
    """Build a compact representation of the ledger for prompt injection."""
    lines = []

    # Posture summary
    ps = ledger.posture_summary
    lines.append("## CURRENT POSTURE SUMMARY")
    lines.append(f"As of: {ps.as_of.isoformat()}")
    lines.append(ps.text)
    lines.append("Category status: " + ", ".join(
        f"{c.value}={s.value}" for c, s in ps.category_status.items()
    ))
    if ps.last_deep_dive:
        lines.append(f"Last deep dive: {ps.last_deep_dive.isoformat()}")
    lines.append("")

    # Signal category assessments
    lines.append("## CURRENT SIGNAL CATEGORY ASSESSMENTS")
    for cat, assessment in ledger.signal_categories.items():
        lines.append(f"\n### {cat.value}")
        lines.append(f"Assessment: {assessment.current_assessment}")
        lines.append(f"Confidence: {assessment.confidence}")
        if assessment.confidence_rationale:
            lines.append(f"Rationale: {assessment.confidence_rationale}")
        if assessment.key_actors:
            lines.append(f"Key actors: {', '.join(assessment.key_actors)}")
    lines.append("")

    # Recent weekly entries (most recent first, capped)
    recent = ledger.weekly_entries[-max_entries:] if ledger.weekly_entries else []
    if recent:
        lines.append(f"## RECENT WEEKLY ENTRIES (last {len(recent)})")
        for entry in reversed(recent):
            lines.append(f"\n### Week of {entry.week.isoformat()} ({entry.depth.value})")
            if entry.activity_level:
                lines.append(f"Activity: {entry.activity_level.get('rating', 'unknown')}")
            if entry.category_movements:
                for cat, mov in entry.category_movements.items():
                    if mov.movement != Movement.NONE:
                        lines.append(f"  {cat.value}: {mov.movement.value}")
                        if mov.updated_assessment:
                            lines.append(f"    → {mov.updated_assessment[:200]}")
            # Include devil's advocate challenges from prior deep dives
            if entry.devils_advocate and entry.devils_advocate.challenges:
                lines.append("  Devil's advocate challenges:")
                for challenge in entry.devils_advocate.challenges:
                    lines.append(f"    - {challenge[:200]}")
    elif ledger.consolidated_history:
        lines.append("## CONSOLIDATED HISTORY")
        lines.append(ledger.consolidated_history[:2000])

    # Corrections log
    if ledger.corrections_log:
        lines.append(f"\n## CORRECTIONS LOG ({len(ledger.corrections_log)} entries)")
        for cl_entry in ledger.corrections_log[-5:]:
            lines.append(
                f"- {cl_entry.correction_date}: {cl_entry.category_affected.value} — "
                f"{cl_entry.corrected_to[:150]} (root cause: {cl_entry.root_cause[:100]})"
            )

    # Structural claims to check
    active_claims = [
        c for c in ledger.structural_claim_status
        if c.status != "falsified"
    ]
    if active_claims:
        lines.append(f"\n## ACTIVE STRUCTURAL CLAIMS ({len(active_claims)} total)")
        # Show claims under pressure first, then sample of confirmed
        priority_claims = [c for c in active_claims if c.status != "confirmed"]
        sample_confirmed = [c for c in active_claims if c.status == "confirmed"][:5]
        for c in priority_claims + sample_confirmed:
            lines.append(f"- [{c.claim_ref}] (§{c.dossier_section}, {c.status.value}): {c.claim_text[:150]}")

    return "\n".join(lines)


def _build_country_prompt(
    config: CountryConfig,
    ledger: CountryLedger,
    dossier_text: str,
    end_date: date,
    allowed_domains: list[str] | None = None,
) -> str:
    start_date = end_date - timedelta(days=7)

    actor_lines = []
    for a in config.actors:
        terms = ", ".join(f'"{t}"' for t in a.search_terms)
        marker = " (PRIMARY)" if a.primary else ""
        actor_lines.append(f"- {a.name} ({a.role}){marker}: search terms: {terms}")
    actors_block = "\n".join(actor_lines)

    # Build source display from allowed_domains list
    domains = allowed_domains or []
    sources_block = "\n".join(f"- {d}" for d in domains) if domains else "- No sources configured"

    blind_spots_block = ""
    if config.blind_spots:
        blind_spots_block = "\nKnown blind spots:\n" + "\n".join(
            f"- {b.domain}: {b.reason} (signal lives in: {b.where_signal_lives})"
            for b in config.blind_spots
        )

    ledger_context = _build_ledger_context(ledger)

    language_note = ""
    lang = config.languages.primary
    if lang and lang != "en":
        language_note = (
            f"\nIMPORTANT: This country's primary language is {lang}. "
            f"Search domestic sources in {lang} for better coverage. "
            f"Translate findings to English in your output."
        )

    return f"""\
Deep-dive analysis for {config.country} ({config.code.upper()}).

Tier: {config.tier.value}
Region: {config.region.value}
Date range: {start_date.isoformat()} to {end_date.isoformat()}

## KEY ACTORS AND INSTITUTIONS
{actors_block}

## WHITELISTED SOURCES

{sources_block}
{blind_spots_block}
{language_note}

## CURRENT LEDGER STATE

{ledger_context}

--- BEGIN COUNTRY DOSSIER ---

{dossier_text}

--- END COUNTRY DOSSIER ---

Search the whitelisted sources for developments involving the key actors and institutions \
during {start_date.isoformat()} to {end_date.isoformat()}. Analyze across all five signal \
categories and produce the JSON output as specified in your instructions."""


# =============================================================================
# Response parsing
# =============================================================================

def parse_country_response(
    response_text: str,
    week_date: date,
    date_range: str,
    ledger: CountryLedger,
) -> CountryAgentOutput:
    """Parse the country agent's JSON response into structured output."""
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    data = json.loads(text)

    # Support both wrapped and unwrapped formats
    entry_data = data.get("weekly_entry", data)

    # Parse category movements
    category_movements = {}
    for cat in SignalCategory:
        cat_data = entry_data["category_movements"][cat.value]
        developments = [
            Development(
                headline=d["headline"],
                date=date.fromisoformat(d["date"]) if isinstance(d["date"], str) else d["date"],
                source=d["source"],
                source_tier=d["source_tier"],
                source_url=d.get("source_url", ""),
                summary=d.get("summary", ""),
                actors_involved=d.get("actors_involved", []),
                signal_category_relevance=d.get("signal_category_relevance", ""),
            )
            for d in cat_data.get("developments", [])
        ]
        conf_change = None
        if cat_data.get("confidence_change"):
            cc = cat_data["confidence_change"]
            conf_change = ConfidenceChange(**cc)

        category_movements[cat] = CategoryMovement(
            movement=Movement(cat_data["movement"]),
            developments=developments,
            prior_assessment=cat_data.get("prior_assessment", ""),
            updated_assessment=cat_data.get("updated_assessment", ""),
            confidence_change=conf_change,
        )

    # Parse unexpected developments
    unexpected = [
        UnexpectedDevelopment(
            headline=u["headline"],
            date=date.fromisoformat(u["date"]) if isinstance(u["date"], str) else u["date"],
            source=u["source"],
            source_tier=u["source_tier"],
            signal_category=SignalCategory(u["signal_category"]),
            assessment=u.get("assessment", ""),
            disposition=u.get("disposition", "logged"),
        )
        for u in entry_data.get("unexpected_developments", [])
    ]

    # Parse absence checks
    absence_checks = [
        AbsenceCheck(
            expected=a["expected"],
            signal_category=SignalCategory(a["signal_category"]),
            occurred=a["occurred"],
            significance=a.get("significance", ""),
            confidence=a.get("confidence", 2),
        )
        for a in entry_data.get("absence_check", [])
    ]

    # Parse self-corrections
    self_corrections = [
        SelfCorrection(
            category=SignalCategory(s["category"]),
            prior_week=date.fromisoformat(s["prior_week"]) if isinstance(s["prior_week"], str) else s["prior_week"],
            original_claim=s["original_claim"],
            correction=s["correction"],
            root_cause=s["root_cause"],
        )
        for s in entry_data.get("self_corrections", [])
    ]

    # Parse structural claim checks
    claim_checks = [
        StructuralClaimCheck(
            claim_ref=c["claim_ref"],
            claim_text=c["claim_text"],
            status=c["status"],
            evidence=c.get("evidence", ""),
            confidence_in_claim=c.get("confidence_in_claim", 3),
        )
        for c in entry_data.get("structural_claim_checks", [])
    ]

    # Build weekly entry (without devils_advocate — added by separate agent)
    weekly_entry = WeeklyEntry(
        week=week_date,
        date_range=date_range,
        depth=Depth.DEEP_DIVE,
        activity_level=entry_data["activity_level"],
        category_movements=category_movements,
        unexpected_developments=unexpected,
        absence_check=absence_checks,
        self_corrections=self_corrections,
        structural_claim_checks=claim_checks,
        devils_advocate=None,  # Populated by devil's advocate agent
    )

    # Parse updated signal category assessments
    # Support both key names
    assessments_data = data.get("updated_signal_categories", data.get("updated_assessments", {}))
    updated_assessments = {}
    for cat in SignalCategory:
        ua = assessments_data[cat.value]
        updated_assessments[cat] = SignalCategoryAssessment(
            current_assessment=ua["current_assessment"],
            confidence=ua["confidence"],
            confidence_rationale=ua.get("confidence_rationale", ""),
            key_actors=ua.get("key_actors", []),
            dossier_sections_referenced=ua.get("dossier_sections_referenced", []),
            last_updated=date.fromisoformat(ua["last_updated"]) if ua.get("last_updated") else week_date,
        )

    # Parse updated posture summary
    # Support both key names
    up = data.get("updated_posture_summary", data.get("updated_posture", {}))
    posture_summary = PostureSummary(
        as_of=date.fromisoformat(up["as_of"]) if up.get("as_of") else week_date,
        text=up["text"],
        category_status={
            SignalCategory(k): CategoryStatus(v)
            for k, v in up["category_status"].items()
        },
        last_deep_dive=date.fromisoformat(up["last_deep_dive"]) if up.get("last_deep_dive") else week_date,
        consecutive_maintenance_weeks=up.get("consecutive_maintenance_weeks", 0),
    )

    return CountryAgentOutput(
        weekly_entry=weekly_entry,
        signal_categories=updated_assessments,
        posture_summary=posture_summary,
    )


# =============================================================================
# Main entry point
# =============================================================================

async def run_country_agent(
    config: CountryConfig,
    ledger: CountryLedger,
    end_date: date | None = None,
    allowed_domains: list[str] | None = None,
) -> CountryAgentOutput:
    """
    Run the country desk deep-dive analysis.

    Uses web_search to find recent developments, then produces structured
    analysis across all five signal categories.

    Args:
        config: Country configuration.
        ledger: Current country ledger state.
        end_date: End of the analysis window.
        allowed_domains: Domains for web_search tool. Assembled by the
            orchestrator from brave_sources + government domain config.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    end_date = end_date or date.today()
    start_date = end_date - timedelta(days=7)
    date_range = f"{start_date.isoformat()} to {end_date.isoformat()}"

    dossier_text = config.dossier_path.read_text()
    prompt = _build_country_prompt(
        config, ledger, dossier_text, end_date,
        allowed_domains=allowed_domains,
    )
    system_prompt = _build_system_prompt(config)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    logger.info("Country agent %s: starting deep dive, date_range=%s", config.code, date_range)
    logger.debug(
        "Country agent %s: %d allowed_domains, dossier=%d chars, prompt=%d chars",
        config.code, len(allowed_domains or []), len(dossier_text), len(prompt),
    )
    logger.debug(
        "Country agent %s: ledger has %d weekly entries, posture as_of=%s",
        config.code, len(ledger.weekly_entries),
        ledger.posture_summary.as_of.isoformat(),
    )

    response = await client.messages.create(
        model=MODEL,
        max_tokens=16384,
        temperature=1,  # required for extended thinking
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": prompt}],
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": config.search.deep_dive_queries_max,
            "allowed_domains": allowed_domains or [],
        }],
    )

    # Extract text blocks
    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        "Country agent %s: API complete — input=%d, output=%d tokens",
        config.code, response.usage.input_tokens, response.usage.output_tokens,
    )

    result = parse_country_response(response_text, end_date, date_range, ledger)
    active_cats = [
        c.value for c, m in result.weekly_entry.category_movements.items()
        if m.movement != Movement.NONE
    ]
    logger.info(
        "Country agent %s: parsed — activity=%s, active_categories=%s, %d developments, %d claim_checks",
        config.code,
        result.weekly_entry.activity_level.get("rating", "?") if result.weekly_entry.activity_level else "?",
        active_cats or "none",
        sum(len(m.developments) for m in result.weekly_entry.category_movements.values()),
        len(result.weekly_entry.structural_claim_checks),
    )
    return result
