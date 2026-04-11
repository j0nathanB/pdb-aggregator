"""
Triage agent: Brave News wire + domestic sweep → depth decisions.

Phase 1: Per-country Brave News scan (parallel) — wire sweep (no goggles)
         + domestic sweep (with goggles) collect headlines.
Phase 2: Triage decision (single LLM call) — decides deep_dive or maintenance.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta

import anthropic

from ..rate_limit import anthropic_limiter

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    STALENESS_THRESHOLD_WEEKS,
    WIRE_DOMAINS,
    CountryConfig,
    Depth,
    SignalCategory,
    load_prompt,
)
from ..collection.brave import BraveNewsClient
from ..models import CountryLedger, GlobalLedger
from ..sanitize import extract_json, safe_enum

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
    # Raw Brave results preserved for downstream story map
    wire_results: list = field(default_factory=list)  # list[BraveNewsResult]
    domestic_results: list = field(default_factory=list)  # list[BraveNewsResult]


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
    scan_results: list[ScanResult] = field(default_factory=list)
    summary: str = ""

    @property
    def deep_dive_countries(self) -> list[str]:
        return [d.code for d in self.decisions if d.depth == Depth.DEEP_DIVE]

    @property
    def maintenance_countries(self) -> list[str]:
        return [d.code for d in self.decisions if d.depth == Depth.MAINTENANCE]

    @property
    def scan_map(self) -> dict[str, ScanResult]:
        """Scan results keyed by country code for easy lookup."""
        return {s.code: s for s in self.scan_results}


# =============================================================================
# Phase 1: Brave News scan
# =============================================================================

def _is_wire_domain(source_domain: str | None) -> bool:
    """Check if a domain matches a known wire service."""
    if not source_domain:
        return False
    source = source_domain.lower()
    return any(wd in source for wd in WIRE_DOMAINS)


def _primary_actor_term(config: CountryConfig) -> str:
    """Return the first search term of the primary actor, or the country name."""
    for actor in config.actors:
        if actor.primary and actor.search_terms:
            return actor.search_terms[0]
    return config.country


async def scan_country(
    config: CountryConfig,
    brave_client: BraveNewsClient,
    end_date: date | None = None,
    semaphore=None,
) -> ScanResult:
    """
    Run wire + domestic headline scan for a single country using Brave News API.

    Wire sweep: ungoggled search for country name → filter to wire domains.
    Domestic sweep: goggled search for primary actor → all results.
    """
    end_date = end_date or date.today()
    start_date = end_date - timedelta(days=6)
    freshness = f"{start_date.isoformat()}to{end_date.isoformat()}"
    primary_term = _primary_actor_term(config)

    async def _do_scan() -> ScanResult:
        wire_headlines: list[str] = []
        domestic_headlines: list[str] = []
        wire_results = []
        domestic_results = []
        errors: list[str] = []

        # --- Wire sweep: no goggles, no country params ---
        try:
            wire_resp = await brave_client.search_news(
                f'"{config.country}"',
                freshness=freshness,
                count=50,
            )
            for r in wire_resp.results:
                if _is_wire_domain(r.source_domain):
                    wire_headlines.append(f"{r.title}, {r.source_domain}")
                    wire_results.append(r)
            logger.info(
                "Triage scan %s: wire sweep — %d raw results, %d wire matches",
                config.code, wire_resp.total_count, len(wire_headlines),
            )
            for h in wire_headlines:
                logger.debug("Triage scan %s: wire — %s", config.code, h)
        except Exception as e:
            logger.warning("Triage scan %s: wire sweep failed: %s", config.code, e)
            errors.append(f"wire: {e}")

        # --- Domestic sweep: with goggles + country params ---
        try:
            goggle_url = brave_client.country_configs.get(config.code)
            if goggle_url:
                goggle_url = goggle_url.goggle_url()

            domestic_resp = await brave_client.search_news(
                primary_term,
                country_code=config.code,
                freshness=freshness,
                count=50,
                goggles=goggle_url,
            )
            for r in domestic_resp.results:
                domestic_headlines.append(f"{r.title}, {r.source_domain or '?'}")
                domestic_results.append(r)
            logger.info(
                "Triage scan %s: domestic sweep — q=%r, %d results",
                config.code, primary_term, domestic_resp.total_count,
            )
            for h in domestic_headlines[:10]:
                logger.debug("Triage scan %s: domestic — %s", config.code, h)
            if len(domestic_headlines) > 10:
                logger.debug(
                    "Triage scan %s: ... and %d more domestic headlines",
                    config.code, len(domestic_headlines) - 10,
                )
        except Exception as e:
            logger.warning("Triage scan %s: domestic sweep failed: %s", config.code, e)
            errors.append(f"domestic: {e}")

        error_str = "; ".join(errors) if errors else ""
        # Only mark as error if both sweeps failed
        if len(errors) == 2:
            return ScanResult(
                code=config.code,
                country=config.country,
                error=error_str,
            )

        return ScanResult(
            code=config.code,
            country=config.country,
            wire_headlines=wire_headlines,
            domestic_headlines=domestic_headlines,
            wire_results=wire_results,
            domestic_results=domestic_results,
            scan_summary=f"Wire: {len(wire_headlines)} headlines. Domestic: {len(domestic_headlines)} headlines.",
        )

    if semaphore:
        async with semaphore.acquire(config.code):
            return await _do_scan()
    return await _do_scan()


async def scan_all_countries(
    configs: list[CountryConfig],
    brave_client: BraveNewsClient,
    end_date: date | None = None,
    max_concurrent: int = 10,
) -> list[ScanResult]:
    """Run Brave News scans for all countries with concurrency limit."""
    from ..timing import TrackedSemaphore
    semaphore = TrackedSemaphore(max_concurrent, "triage_scan")
    tasks = [
        scan_country(c, brave_client, end_date, semaphore)
        for c in configs
    ]
    return await asyncio.gather(*tasks)


# =============================================================================
# Phase 2: Triage decision
# =============================================================================

TRIAGE_SYSTEM_PROMPT = load_prompt("agents/triage_decision")


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
                block += f"Domestic headlines ({len(scan.domestic_headlines)} total, showing top 15):\n"
                for h in scan.domestic_headlines[:15]:
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
    data = extract_json(response_text, context="triage")

    decisions = []
    for d in data["decisions"]:
        decisions.append(TriageDecision(
            country=d["country"],
            code=d["code"],
            depth=safe_enum(Depth, d.get("depth", "maintenance"), Depth.MAINTENANCE, context="triage_decision"),
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
    end_date: date | None = None,
) -> TriageOutput:
    """
    Phase 2: Make depth decisions for all countries based on scan results + context.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    end_date = end_date or date.today()
    prompt = _build_triage_prompt(scan_results, ledgers, global_ledger)

    from ..timing import with_heartbeat
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        response = await with_heartbeat(
            client.messages.create(
                model=MODEL,
                max_tokens=12096,
                temperature=1,  # required for extended thinking
                thinking={
                    "type": "enabled",
                    "budget_tokens": 8000,
                },
                system=[{"type": "text", "text": load_prompt("agents/triage_decision")}],
                messages=[{"role": "user", "content": prompt}],
            ),
            "Triage decision: API call",
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

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    save_raw_response(
        "triage", "decisions", end_date,
        system_prompt=load_prompt("agents/triage_decision"),
        user_message=prompt,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
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

    update_trace_parsed(
        "triage", "decisions", end_date,
        parsed_output={"decisions": [d.__dict__ for d in decisions], "summary": summary},
    )

    return TriageOutput(
        triage_date=end_date,
        decisions=decisions,
        summary=summary,
    )


async def run_triage(
    configs: list[CountryConfig],
    ledgers: dict[str, CountryLedger],
    global_ledger: GlobalLedger | None = None,
    end_date: date | None = None,
    max_concurrent: int = 10,
    brave_client: BraveNewsClient | None = None,
) -> TriageOutput:
    """
    Full triage: scan all countries via Brave News, then decide depth for each.

    This is the main entry point for the triage step.
    """
    if brave_client is None:
        raise ValueError("BraveNewsClient required for triage scan")

    logger.info("Triage: starting for %d countries", len(configs))

    # Phase 1: parallel Brave News scans
    scan_results = await scan_all_countries(configs, brave_client, end_date, max_concurrent)

    scan_ok = [s for s in scan_results if not s.error]
    scan_errors = [s for s in scan_results if s.error]
    logger.info(
        "Triage scan phase: %d succeeded, %d failed",
        len(scan_ok), len(scan_errors),
    )
    if scan_errors:
        logger.warning("Triage scan errors: %s", [s.code for s in scan_errors])
    for s in scan_ok:
        logger.debug(
            "Triage scan %s: %d wire headlines, %d domestic headlines",
            s.code, len(s.wire_headlines), len(s.domestic_headlines),
        )

    # Phase 2: triage decision
    output = await triage_decide(scan_results, ledgers, global_ledger, end_date=end_date)
    output.scan_results = scan_results

    logger.info(
        "Triage complete: %d deep dives %s, %d maintenance %s",
        len(output.deep_dive_countries), output.deep_dive_countries,
        len(output.maintenance_countries), output.maintenance_countries,
    )
    for d in output.decisions:
        logger.debug(
            "Triage decision %s (%s): %s — triggers=%s",
            d.code, d.country, d.depth.value, d.triggered_by,
        )
    return output
