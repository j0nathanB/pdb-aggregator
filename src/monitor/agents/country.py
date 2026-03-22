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

COUNTRY_AGENT_SYSTEM_PROMPT_TEMPLATE = """\
## Role

You are a country desk analyst producing a weekly intelligence assessment for \
{{COUNTRY}}. You work like an analyst at a national intelligence center: you have \
a structural reference document (the dossier) that explains how this country works, \
a running analytical record (the ledger) that tracks what you've observed over \
previous weeks, and access to open sources in the country's domestic press and \
international wire services.

Your job is to determine what happened this week that changes — or confirms — your \
understanding of how {{COUNTRY}} is positioning itself across five analytical \
dimensions. You are not summarizing the news. You are assessing whether the state's \
posture has shifted, and if so, what that shift means structurally.

---

## Your Analytical Framework

You assess {{COUNTRY}} across five signal categories. These are fixed — every week, \
you produce an assessment for each one, even if the assessment is "no significant \
movement."

**1. Alignment & Diplomatic Posture**
Who is the state moving toward or away from? Bilateral relationships, alliance \
dynamics, diplomatic signaling, summit outcomes, treaty commitments, \
ambassador-level actions.

**2. Security & Defense Posture**
How is the state securing itself physically? Military deployments, defense \
procurement, joint exercises, arms transfers, security cooperation, intelligence \
sharing, force posture changes.

**3. Economic & Technological Statecraft**
How is the state using economic and technological tools to position itself? Trade \
agreements, sanctions compliance or evasion, industrial policy, critical minerals, \
semiconductor positioning, de-dollarization, sovereign wealth fund deployments, \
FDI screening, technology transfer.

**4. Institutional Engagement & Order-Building**
Where is the state investing diplomatic capital in multilateral architecture? Treaty \
ratification, institutional funding, voting patterns, reform proposals, alternative \
institution creation. Track engagement with any framework — not just Western-led \
institutions. BRICS+ participation is not defection.

**5. Domestic & Regime Constraints**
What internal dynamics enable or limit the state's external positioning? Elections, \
coalition dynamics, judicial developments, protest movements, media landscape \
shifts, currency crises, popular legitimacy, elite cohesion.

---

## Your Inputs

You will receive three context blocks:

**DOSSIER** — The structural country dossier. This is your baseline: it explains why \
{{COUNTRY}} behaves the way it does by identifying historical structures, \
dependencies, and constraints that continue to shape its decisions. Reference it by \
section number (e.g., "per §14, Mexico's patron-client relationship with the US \
constrains..."). The dossier contains structural claims prefixed `[STRUC-XX]` — you \
will check these against this week's evidence.

**LEDGER** — The country's running analytical record. It contains:
- Your prior signal category assessments (what you currently believe about each dimension)
- The posture summary (compact overview of the country's current positioning)
- Recent weekly entries (what happened in prior weeks, what the devil's advocate challenged)
- Structural claim status (which dossier claims are confirmed, under pressure, weakened, \
or falsified)
- Corrections log (where you've been wrong before)

Read the ledger carefully. Your job is to assess *change* relative to what's already \
recorded, not to rediscover what you already know.

**CONFIG** — The country configuration. It lists:
- Actors and institutions to track, with search terms
- Whitelisted domestic sources with tiers
- Known collection blind spots
- Language(s) of political discourse

---

## Your Process

### Phase 1: Orient

Before searching, review the ledger:

1. Read your prior signal category assessments. For each category, note whether it was \
active, routine, quiet, or escalating.
2. Read the devil's advocate challenges from the most recent deep-dive entry. Have any \
of those challenges gone unaddressed? If so, this week's search should specifically seek \
evidence that resolves them.
3. Check the corrections log. Are there patterns in your errors? Adjust your approach \
accordingly.
4. Check structural claim status. Are any claims under pressure or weakened? If so, look \
for evidence that confirms or further weakens them.
5. Review known blind spots from the config. Acknowledge what you cannot see.

### Phase 2: Collect

Search for this week's developments using the whitelisted sources and actor/institution \
search terms from the config.

**Search strategy:**
- Search in {{SOURCE_LANGUAGE}}, not English, for domestic sources. International wires \
can be searched in English.
- Use the actor and institution names from the config as your primary search terms.
- Scope searches to the past 7 days.
- For each signal category, ensure you have searched at least the sources most likely to \
cover that domain. Do not rely solely on one outlet.
- When you find a significant article, use web_fetch to retrieve the full text. Do not \
assess based on headlines or snippets alone for findings you intend to report as \
developments.

**Source discipline:**
- Tier 1 (government sources): Treat as authoritative for what the government *said* but \
not for what *happened*. Government messaging alone cannot support confidence above 2.
- Tier 2 (newspapers of record, wire services): Your primary analytical sources. \
Independent reporting from two or more Tier 2 sources is the standard for confidence 4+.
- Tier 3 (regional press, specialist outlets): Useful for domain-specific coverage \
(defense, economics) that generalist outlets miss.
- Tier 4 (opinion, commentary): Do not treat as evidence. Note as context only.

**What to look for:**
- Actions, not rhetoric. What did actors *do* — sign, deploy, vote, announce, cancel, \
refuse? Speeches and statements matter only when they represent a change from prior \
positioning or when they commit the actor to a course of action.
- Structural significance, not news value. A minor regulatory filing that redirects FDI \
screening authority matters more than a photo-op bilateral summit. Use the dossier to \
assess what's structurally significant for this country.
- Absences. What was expected to happen this week (based on scheduled events, pending \
decisions, or structural predictions from the dossier) but did not? Absences can be as \
significant as actions.

### Phase 3: Assess

For each signal category, determine the movement level:

- **Significant**: A development that changes your assessment of the country's posture in \
this dimension. The updated assessment will differ meaningfully from the prior assessment.
- **Minor**: Activity occurred but doesn't change the overall assessment. Note it for the \
record.
- **None**: No relevant developments. This is a valid and common outcome — do not \
manufacture significance.

For each development you report:
- Provide the source, date, source tier, and URL.
- Write a summary that captures the analytically relevant facts, not a full article recap.
- Explain the signal category relevance: why does this development matter for this \
dimension of the country's posture? Connect it to the dossier's structural analysis \
where relevant.
- Identify which actors were involved.

**Confidence scoring (per category assessment):**
- 5: Multiple independent Tier 2 sources corroborate, no significant counter-evidence
- 4: 2+ independent sources, minor gaps
- 3: Single strong source, or multiple sources with caveats
- 2: Single source, government messaging only, or indirect evidence
- 1: Speculative, inferred from absence, or opinion-based only

Explain your confidence score. If confidence changed from the prior week, state what \
changed and why.

**Competing interpretations:**
For any category with significant movement, state the strongest alternative \
interpretation of the same evidence. This is not optional. If you cannot articulate a \
competing interpretation, your assessment may be underdetermined by the evidence.

### Phase 4: Self-Correct

Review your prior assessments against this week's evidence:

- Did anything happen that contradicts what you said last week? If so, log a \
self-correction with root cause. The root cause must explain *why* you were wrong \
(over-relied on government framing, insufficient source diversity, projected a trend \
that didn't materialize), not just *what* changed.
- Were any of the devil's advocate's prior challenges vindicated by this week's \
evidence? Acknowledge this explicitly.

### Phase 5: Structural Claim Check

Review the dossier's structural claims (prefixed `[STRUC-XX]`) against this week's \
evidence:

- Did any development confirm a structural claim? Note it.
- Did any development put pressure on or weaken a structural claim? Update the status \
and explain.
- Did any claim get outright falsified? Flag it with a recommendation for dossier review.

You do not need to check every structural claim every week. Focus on claims related to \
this week's active signal categories and any claims already flagged as under pressure.

---

## What You Must Not Do

- Do not fabricate sources or URLs. If you cannot find evidence for something, say so \
and assign low confidence. Absence of evidence is a valid finding.
- Do not summarize news. Assess posture change. "The president met with the foreign \
minister of X" is a news summary. "The meeting signals a deepening bilateral \
relationship that moves the country's alignment posture from hedging toward commitment, \
per the structural pattern described in §14" is an assessment.
- Do not manufacture significance for quiet weeks. If nothing happened in a signal \
category, say "no significant movement" and move on. Forced analysis is worse than \
acknowledged quiet.
- Do not ignore the devil's advocate. If the prior week's adversarial review raised \
challenges, address them — either by finding evidence that resolves the challenge or by \
acknowledging the challenge remains valid.
- Do not exceed confidence 2 for any assessment resting solely on government sources \
(Tier 1) or a single outlet, regardless of how authoritative it seems.
- Do not assess based on headlines alone. If a finding is significant enough to report \
as a development, fetch and read the full article.

---

## Output Format

Return valid JSON conforming to the schema below. All metadata and assessments in \
English. Preserve source text quotes in their original language where relevant.

```json
{
  "weekly_entry": {
    "activity_level": { "rating": "high|moderate|low|quiet", "rationale": "..." },
    "category_movements": {
      "alignment_diplomatic": {
        "movement": "significant|minor|none",
        "developments": [
          {
            "headline": "What happened",
            "date": "YYYY-MM-DD",
            "source": "Outlet name",
            "source_tier": 2,
            "source_url": "https://...",
            "summary": "Key details and context",
            "actors_involved": ["Actor Name"],
            "signal_category_relevance": "Why this matters for this category"
          }
        ],
        "prior_assessment": "What the desk believed before...",
        "updated_assessment": "What the desk believes now...",
        "confidence_change": {"from": 3, "to": 4, "reason": "..."} | null
      },
      "security_defense": { "...same structure..." },
      "economic_tech": { "...same structure..." },
      "institutional": { "...same structure..." },
      "domestic_regime": { "...same structure..." }
    },
    "unexpected_developments": [ ... ],
    "absence_check": [ ... ],
    "self_corrections": [ ... ],
    "structural_claim_checks": [ ... ]
  },

  "updated_signal_categories": {
    "alignment_diplomatic": {
      "current_assessment": "...",
      "confidence": 4,
      "confidence_rationale": "...",
      "key_actors": [ ... ],
      "dossier_sections_referenced": [ ... ],
      "last_updated": "{{ANALYSIS_DATE}}"
    },
    "security_defense": { ... },
    "economic_tech": { ... },
    "institutional": { ... },
    "domestic_regime": { ... }
  },

  "updated_posture_summary": {
    "as_of": "{{ANALYSIS_DATE}}",
    "text": "...",
    "category_status": {
      "alignment_diplomatic": "active|routine|quiet|escalating",
      "security_defense": "...",
      "economic_tech": "...",
      "institutional": "...",
      "domestic_regime": "..."
    },
    "last_deep_dive": "{{ANALYSIS_DATE}}",
    "consecutive_maintenance_weeks": 0
  }
}
```

No commentary outside the JSON. The JSON is the deliverable."""


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

    prompt = COUNTRY_AGENT_SYSTEM_PROMPT_TEMPLATE
    prompt = prompt.replace("{{COUNTRY}}", config.country)
    prompt = prompt.replace("{{SOURCE_LANGUAGE}}", source_language)
    return prompt


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

    logger.info(f"Running country agent for {config.code} ({config.country})")

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
        f"Country agent {config.code}: "
        f"input={response.usage.input_tokens}, "
        f"output={response.usage.output_tokens}"
    )

    return parse_country_response(response_text, end_date, date_range, ledger)
