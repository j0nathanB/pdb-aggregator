"""
Triage agent: wire scan + domestic headline check → depth decisions.

Phase 1: Per-country scan (parallel) — Claude with web_search tool collects headlines.
Phase 2: Triage decision (single call) — LLM decides deep_dive or maintenance for each country.
"""

import asyncio
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import date, timedelta

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    STALENESS_THRESHOLD_WEEKS,
    CountryConfig,
    Depth,
    SignalCategory,
)
from ..models import CountryLedger, GlobalLedger

logger = logging.getLogger(__name__)


# =============================================================================
# Data structures
# =============================================================================

@dataclass
class ScanResult:
    """Headlines collected for a single country."""
    code: str
    country: str
    wire_headlines: list[str] = field(default_factory=list)
    domestic_headlines: list[str] = field(default_factory=list)
    scan_summary: str = ""
    error: str = ""


@dataclass
class TriageDecision:
    """Depth decision for a single country."""
    country: str
    code: str
    depth: Depth
    rationale: str
    triggered_by: list[str] = field(default_factory=list)
    signal_categories_flagged: list[str] = field(default_factory=list)


@dataclass
class TriageOutput:
    """Full triage output for all countries."""
    triage_date: date
    decisions: list[TriageDecision]
    summary: str = ""

    @property
    def deep_dive_countries(self) -> list[str]:
        return [d.code for d in self.decisions if d.depth == Depth.DEEP_DIVE]

    @property
    def maintenance_countries(self) -> list[str]:
        return [d.code for d in self.decisions if d.depth == Depth.MAINTENANCE]


# =============================================================================
# Phase 1: Per-country scan
# =============================================================================

SCAN_SYSTEM_PROMPT = """\
You are a news scanner for a geopolitical monitoring system. Your job is to find \
recent headlines (last 7 days) about a specific country's key actors and institutions.

Search wire services (Reuters, AP, AFP) and the specified domestic outlets. \
Report only headlines and brief snippets — do NOT analyze or interpret.

Respond with a JSON object:
{
  "wire_headlines": ["headline 1", "headline 2", ...],
  "domestic_headlines": ["headline 1", "headline 2", ...],
  "scan_summary": "One sentence summarizing what you found or 'No significant coverage found.'"
}

Rules:
- Include only developments from the past 7 days.
- Each headline should be a single concise line: what happened, who was involved, source.
- If a search returns no relevant results, return empty arrays.
- Do NOT fabricate headlines. Only report what you actually find.
- Respond with valid JSON only. No markdown fencing."""


def _build_scan_prompt(
    config: CountryConfig,
    end_date: date,
    wire_domains: list[str] | None = None,
    triage_domains: list[str] | None = None,
) -> str:
    start_date = end_date - timedelta(days=7)

    actor_terms = []
    for a in config.actors:
        terms = ", ".join(f'"{t}"' for t in a.search_terms)
        actor_terms.append(f"- {a.name} ({a.role}): {terms}")
    actors_block = "\n".join(actor_terms)

    wire_list = wire_domains or []
    wire_block = "\n".join(
        f"- {d}" for d in wire_list
    ) if wire_list else "- reuters.com\n- apnews.com"

    triage_list = triage_domains or []
    domestic_block = "\n".join(
        f"- {d}" for d in triage_list
    ) if triage_list else "- No triage sources configured"

    return f"""\
Scan for recent news about {config.country} ({config.code.upper()}).

Date range: {start_date.isoformat()} to {end_date.isoformat()}

Key actors and search terms:
{actors_block}

Wire services to check:
{wire_block}

Domestic outlets to check (headlines only):
{domestic_block}

Search for these actors and institutions in the wire services and domestic outlets. \
Report what you find as structured JSON."""


def _parse_scan_response(response: anthropic.types.Message, code: str, country: str) -> ScanResult:
    """Extract structured scan result from Claude's response."""
    text_parts = []
    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)

    full_text = "\n".join(text_parts)

    # Try to parse JSON from the response
    try:
        # Strip markdown fencing if present
        cleaned = full_text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
            cleaned = re.sub(r"\n?```\s*$", "", cleaned)

        data = json.loads(cleaned)
        return ScanResult(
            code=code,
            country=country,
            wire_headlines=data.get("wire_headlines", []),
            domestic_headlines=data.get("domestic_headlines", []),
            scan_summary=data.get("scan_summary", ""),
        )
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Failed to parse scan response for {code}: {e}")
        return ScanResult(
            code=code,
            country=country,
            scan_summary=full_text[:500],
            error=f"Parse error: {e}",
        )


async def scan_country(
    config: CountryConfig,
    end_date: date | None = None,
    semaphore: asyncio.Semaphore | None = None,
    allowed_domains: list[str] | None = None,
    wire_domains: list[str] | None = None,
    triage_domains: list[str] | None = None,
) -> ScanResult:
    """
    Run wire + domestic headline scan for a single country.

    Uses Claude with web_search tool to find recent headlines.

    Args:
        config: Country configuration.
        end_date: End of the analysis window.
        semaphore: Concurrency limiter.
        allowed_domains: Domains for web_search tool. If None, uses
            wire_domains + triage_domains.
        wire_domains: Wire service domains (e.g., reuters.com).
        triage_domains: Domestic triage source domains.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    end_date = end_date or date.today()

    # Build allowed domains for focused searching
    if allowed_domains is None:
        allowed_domains = list(wire_domains or []) + list(triage_domains or [])

    async def _do_scan() -> ScanResult:
        client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
        try:
            response = await client.messages.create(
                model=MODEL,
                max_tokens=2048,
                system=[{"type": "text", "text": SCAN_SYSTEM_PROMPT}],
                messages=[{
                    "role": "user",
                    "content": _build_scan_prompt(
                        config, end_date,
                        wire_domains=wire_domains,
                        triage_domains=triage_domains,
                    ),
                }],
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": config.search.triage_queries_max + 2,
                    "allowed_domains": allowed_domains,
                }],
            )
            logger.debug(
                f"Scan {config.code}: input={response.usage.input_tokens}, "
                f"output={response.usage.output_tokens}"
            )
            return _parse_scan_response(response, config.code, config.country)
        except Exception as e:
            logger.error(f"Scan failed for {config.code}: {e}")
            return ScanResult(
                code=config.code,
                country=config.country,
                error=str(e),
            )

    if semaphore:
        async with semaphore:
            return await _do_scan()
    return await _do_scan()


async def scan_all_countries(
    configs: list[CountryConfig],
    end_date: date | None = None,
    max_concurrent: int = 10,
) -> list[ScanResult]:
    """Run scans for all countries in parallel with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [scan_country(c, end_date, semaphore) for c in configs]
    return await asyncio.gather(*tasks)


# =============================================================================
# Phase 2: Triage decision
# =============================================================================

TRIAGE_SYSTEM_PROMPT = """\
## Role

You are the intake officer for a 28-country intelligence monitoring operation. Every \
week, before the country desk analysts begin their work, you decide which countries \
need full analytical attention and which can be held at maintenance. You are the \
gatekeeper for the pipeline's most expensive resource: analyst time and search budget.

Your decisions determine what gets investigated this week. A false positive (flagging \
a quiet country for deep dive) wastes resources. A false negative (leaving an active \
country at maintenance) means a significant development goes unanalyzed until it \
surfaces on wires or triggers a flag next week. Err toward false positives — it's \
better to over-investigate than to miss something.

---

## Your Inputs

You receive three blocks of information:

### Wire and Domestic Scan Results

For each of the 28 countries, a compact packet:
- **Wire headlines:** 0-5 recent headlines from Reuters, AP, and AFP mentioning this \
country's tracked actors or institutions. May be empty for quiet countries.
- **Domestic headlines:** 0-3 recent headlines from the country's top domestic outlets \
(those marked `triage_source: true` in the config). May be empty.

These are headlines and snippets only — you have not read the full articles and should \
not infer details beyond what the headlines state.

### Country Posture Summaries

For each country, the current posture summary from its ledger:
- `text`: 3-5 sentence analytical summary of current posture
- `category_status`: per-category status (active, routine, quiet, escalating)
- `last_deep_dive`: date of most recent deep-dive analysis
- `consecutive_maintenance_weeks`: how many weeks since the last deep dive

### Global Ledger Context

The global analytical picture:
- `global_posture_summary`: current text summary and signal environment (most active \
categories, geographic hotspots, quiet zones)
- `active_dynamics`: each with `triage_implications` listing countries the executive \
analyst wants flagged and why

---

## Your Decision Framework

For each country, assign one of two depths:

**DEEP DIVE** — The country desk analyst will run a full sweep of domestic sources, \
produce assessments across all five signal categories, and receive adversarial review.

**MAINTENANCE** — Wire and domestic headline findings will be logged to the country \
ledger. The posture summary gets a light update. No full sweep, no devil's advocate.

### Flag for DEEP DIVE when any of the following apply:

**1. Wire or domestic headlines indicate posture-relevant activity.**
A development that could change the country's positioning in any signal category: a new \
defense agreement, a diplomatic realignment, a major domestic political event, an \
unexpected bilateral meeting, a significant policy announcement, a military deployment \
or exercise.

Not every headline warrants a deep dive. Filter for *structural significance*: does this \
development, if confirmed, change what we believe about how this country is positioning \
itself? A routine bilateral meeting between long-standing allies is not significant. The \
same meeting between historically adversarial states is.

**2. Headlines contradict the current posture summary.**
The posture summary says "stable US relationship" but wires report a trade confrontation. \
The summary says "quiet on defense" but headlines mention a procurement announcement. \
Contradiction between observed coverage and the standing assessment demands investigation.

**3. Analytically significant absence.**
The country had a scheduled event (summit, vote, policy deadline, military exercise) that \
should have generated coverage but didn't. Or the global ledger flags an expected dynamic \
that isn't appearing. Absence can be as significant as activity — but only when you have \
reason to expect activity. A country with no expected events and no coverage is genuinely \
quiet, not suspiciously silent.

**4. Global ledger triage implications.**
The executive analyst's active dynamics include `triage_implications` that name specific \
countries. If a country appears in any dynamic's triage implications, flag it for deep \
dive unless the rationale clearly doesn't apply this week. The executive analyst has \
identified these countries as worth investigating for specific analytical reasons — \
respect that judgment.

**5. Staleness override.**
If `consecutive_maintenance_weeks` >= 4, flag for deep dive regardless of other factors. \
Analysis that hasn't been refreshed in a month may be drifting from reality. Even if the \
country appears quiet, a periodic full check prevents silent degradation of the ledger's \
accuracy.

### Assign MAINTENANCE when:

- Wire and domestic coverage shows only routine activity consistent with the posture summary
- No headlines and no global ledger flags
- Coverage is exclusively domestic/routine with no foreign policy or structural implications
- Last deep dive was recent and no intervening changes suggest the analysis needs updating

### Judgment Calls

Some weeks will be ambiguous. A headline might be significant or might be routine — you \
can't tell from the headline alone. In these cases:

- If the country hasn't had a deep dive in 3+ weeks, lean toward flagging it.
- If the ambiguous headline touches a signal category that the global ledger identifies \
as globally active, lean toward flagging it.
- If the country is in a tier (Shield, Next Test, Pivot) where developments have outsized \
systemic implications, lean toward flagging it.
- When genuinely uncertain, flag for deep dive. The cost of an unnecessary deep dive is \
~$2. The cost of missing a significant development is an analytically stale ledger entry \
that propagates through regional and executive synthesis.

---

## What You Must Not Do

- Do not read full articles or run searches. You work from headlines and summaries only.
- Do not make analytical assessments. You decide *whether* a country needs analysis, not \
*what* that analysis should conclude.
- Do not override the staleness threshold. If a country has been at maintenance for 4+ \
weeks, it gets a deep dive regardless of how quiet it looks.
- Do not ignore global ledger triage implications. If the executive analyst flagged a \
country, you need a strong reason not to flag it — and "the wires are quiet" is not \
sufficient, because the whole point of the implication may be to investigate an absence.
- Do not flag every country for deep dive. The triage exists to focus resources. If \
you're flagging 20+ countries, you're not triaging — you're rubber-stamping. A typical \
week should produce 8-12 deep dives. If the global situation genuinely warrants more, \
explain why in the summary.

---

## Your Output

Produce a JSON object with a decision for each country:

```json
{
  "triage_date": "{{ANALYSIS_DATE}}",
  "summary": {
    "deep_dive_count": 10,
    "maintenance_count": 18,
    "assessment": "Brief 2-3 sentence characterization of the global signal environment \
this week — where activity is concentrated, what's quiet, any notable patterns in the \
triage decisions."
  },
  "decisions": [
    {
      "country": "Country Name",
      "code": "xx",
      "depth": "deep_dive",
      "rationale": "1-3 sentences explaining the decision...",
      "triggered_by": ["wire_coverage", "category_escalation"],
      "signal_categories_flagged": ["alignment_diplomatic"]
    },
    {
      "country": "Country Name",
      "code": "yy",
      "depth": "maintenance",
      "rationale": "1-3 sentences explaining why the country is quiet.",
      "triggered_by": []
    }
  ]
}
```

### Field Specifications

**`triggered_by`** — Array of zero or more trigger types. Use these labels:
- `wire_coverage` — wire headlines show significant activity
- `domestic_coverage` — domestic headlines show significant activity
- `category_escalation` — activity in a category already marked active or escalating
- `posture_contradiction` — headlines contradict the posture summary
- `significant_absence` — expected activity didn't appear
- `global_ledger_implication` — named in a global ledger dynamic's triage implications
- `staleness_override` — consecutive_maintenance_weeks >= 4

Empty array for maintenance decisions.

**`signal_categories_flagged`** — Which signal categories the triage evidence points \
toward. This helps the country agent prioritize its search effort. Only present for \
deep-dive decisions. Omit for maintenance.

**`rationale`** — 1-3 sentences explaining the decision. For deep-dive decisions, \
explain what triggered the flag. For maintenance decisions, briefly note why the \
country is quiet.

---

## Calibration

Across a normal month of operations:
- **8-12 deep dives per week** is typical
- **15+ deep dives** suggests a genuinely active global week or insufficient filtering
- **Fewer than 6 deep dives** suggests you may be under-flagging — check whether any \
Pivot or Shield countries with active posture summaries are being left at maintenance \
without justification

No commentary outside the JSON."""


def _build_triage_prompt(
    scan_results: list[ScanResult],
    ledgers: dict[str, CountryLedger],
    global_ledger: GlobalLedger | None,
) -> str:
    sections = []

    # Global context
    if global_ledger:
        gl_section = "## GLOBAL CONTEXT\n\n"
        gl_section += f"Global posture: {global_ledger.global_posture_summary.text}\n\n"

        if global_ledger.active_dynamics:
            gl_section += "Active dynamics with triage implications:\n"
            for d in global_ledger.active_dynamics:
                if d.triage_implications.countries_to_flag:
                    flags = ", ".join(d.triage_implications.countries_to_flag)
                    gl_section += (
                        f"- Dynamic #{d.dynamic_id}: {d.title}\n"
                        f"  Countries to flag: {flags}\n"
                        f"  Reason: {d.triage_implications.reason}\n"
                    )
        sections.append(gl_section)

    # Per-country blocks
    sections.append("## COUNTRY SCAN RESULTS AND POSTURE SUMMARIES\n")

    for scan in sorted(scan_results, key=lambda s: s.code):
        block = f"### {scan.country} ({scan.code.upper()})\n\n"

        # Scan results
        if scan.error:
            block += f"Scan error: {scan.error}\n"
        else:
            if scan.wire_headlines:
                block += "Wire headlines:\n"
                for h in scan.wire_headlines:
                    block += f"- {h}\n"
            else:
                block += "Wire headlines: None found\n"

            if scan.domestic_headlines:
                block += "Domestic headlines:\n"
                for h in scan.domestic_headlines:
                    block += f"- {h}\n"
            else:
                block += "Domestic headlines: None found\n"

            if scan.scan_summary:
                block += f"Scan summary: {scan.scan_summary}\n"

        # Posture summary from ledger
        if scan.code in ledgers:
            ledger = ledgers[scan.code]
            ps = ledger.posture_summary
            block += f"\nCurrent posture: {ps.text}\n"
            block += "Category status: " + ", ".join(
                f"{c.value}={s.value}" for c, s in ps.category_status.items()
            ) + "\n"
            if ps.last_deep_dive:
                block += f"Last deep dive: {ps.last_deep_dive.isoformat()}\n"
            block += f"Consecutive maintenance weeks: {ps.consecutive_maintenance_weeks}\n"

            if ps.consecutive_maintenance_weeks >= STALENESS_THRESHOLD_WEEKS:
                block += "⚠ STALENESS OVERRIDE: 4+ consecutive maintenance weeks — deep dive required.\n"
        else:
            block += "\nNo ledger exists — first cycle, mandatory deep dive.\n"

        sections.append(block)

    return "\n".join(sections)


def parse_triage_response(response_text: str) -> tuple[list[TriageDecision], str]:
    """Parse the triage LLM response into TriageDecision objects and summary.

    Returns (decisions, summary_assessment).
    """
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    data = json.loads(text)

    decisions = []
    for d in data["decisions"]:
        decisions.append(TriageDecision(
            country=d["country"],
            code=d["code"],
            depth=Depth(d["depth"]),
            rationale=d["rationale"],
            triggered_by=d.get("triggered_by", []),
            signal_categories_flagged=d.get("signal_categories_flagged", []),
        ))

    summary = ""
    if "summary" in data:
        summary = data["summary"].get("assessment", "") if isinstance(data["summary"], dict) else str(data["summary"])

    return decisions, summary


async def triage_decide(
    scan_results: list[ScanResult],
    ledgers: dict[str, CountryLedger],
    global_ledger: GlobalLedger | None = None,
) -> TriageOutput:
    """
    Phase 2: Make depth decisions for all countries based on scan results + context.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    prompt = _build_triage_prompt(scan_results, ledgers, global_ledger)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    response = await client.messages.create(
        model=MODEL,
        max_tokens=8192,
        temperature=1,  # required for extended thinking
        thinking={
            "type": "enabled",
            "budget_tokens": 8000,
        },
        system=[{"type": "text", "text": TRIAGE_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": prompt}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        f"Triage decision: input={response.usage.input_tokens}, "
        f"output={response.usage.output_tokens}"
    )

    decisions, summary = parse_triage_response(response_text)

    # Apply staleness overrides that the LLM might have missed
    decided_codes = {d.code for d in decisions}
    for scan in scan_results:
        if scan.code in ledgers:
            ledger = ledgers[scan.code]
            if ledger.needs_deep_dive:
                # Find and upgrade if needed
                for d in decisions:
                    if d.code == scan.code and d.depth == Depth.MAINTENANCE:
                        logger.warning(
                            f"Staleness override: forcing {scan.code} to deep_dive "
                            f"({ledger.posture_summary.consecutive_maintenance_weeks} "
                            f"consecutive maintenance weeks)"
                        )
                        d.depth = Depth.DEEP_DIVE
                        if "staleness_override" not in d.triggered_by:
                            d.triggered_by.append("staleness_override")
                        d.rationale += (
                            f" [Auto-override: {ledger.posture_summary.consecutive_maintenance_weeks} "
                            f"consecutive maintenance weeks.]"
                        )

        # Countries without ledgers get mandatory deep dive (first cycle)
        if scan.code not in decided_codes:
            decisions.append(TriageDecision(
                country=scan.country,
                code=scan.code,
                depth=Depth.DEEP_DIVE,
                rationale="No ledger exists — first cycle, mandatory deep dive.",
                triggered_by=["first_cycle"],
            ))
        elif scan.code not in ledgers:
            for d in decisions:
                if d.code == scan.code:
                    d.depth = Depth.DEEP_DIVE
                    if "first_cycle" not in d.triggered_by:
                        d.triggered_by.append("first_cycle")

    return TriageOutput(
        triage_date=date.today(),
        decisions=decisions,
        summary=summary,
    )


async def run_triage(
    configs: list[CountryConfig],
    ledgers: dict[str, CountryLedger],
    global_ledger: GlobalLedger | None = None,
    end_date: date | None = None,
    max_concurrent: int = 10,
) -> TriageOutput:
    """
    Full triage: scan all countries, then decide depth for each.

    This is the main entry point for the triage step.
    """
    logger.info(f"Starting triage for {len(configs)} countries")

    # Phase 1: parallel scans
    scan_results = await scan_all_countries(configs, end_date, max_concurrent)

    scan_errors = [s for s in scan_results if s.error]
    if scan_errors:
        logger.warning(f"{len(scan_errors)} scan errors: {[s.code for s in scan_errors]}")

    # Phase 2: triage decision
    output = await triage_decide(scan_results, ledgers, global_ledger)

    logger.info(
        f"Triage complete: {len(output.deep_dive_countries)} deep dives, "
        f"{len(output.maintenance_countries)} maintenance"
    )
    return output
