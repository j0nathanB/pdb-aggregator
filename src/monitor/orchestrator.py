"""
Country desk orchestrator: Layer 2 → triage → parallel country agents → devil's advocate → ledger write.

This module wires the full weekly desk pipeline (before regional synthesis):
1. Layer 2: SearchAPI gov queries → extraction → government source agent (all countries, parallel)
2. Domain assembly: Brave media sources + government domains → allowed_domains per country
3. Triage: wire scan + domestic headlines → depth decisions
4. Country agents: deep-dive analysis (parallel) with allowed_domains
5. Devil's advocate: adversarial review (parallel)
6. Ledger write + maintenance write
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

from .agents.country import CountryAgentOutput, run_country_agent
from .agents.devils_advocate import run_devils_advocate
from .agents.expansion import ExpansionResult, expand_all_countries
from .agents.government import GovernmentAgentOutput, run_government_agent
from .agents.story_map import StoryMapOutput, run_story_map_agent
from .agents.triage import TriageOutput, run_triage, ScanResult
from .collection.brave import BraveNewsClient
from .collection.extract import ExtractionOrchestrator, ExtractionResult
from .collection.searchapi import SearchAPIClient, SearchAPIResponse
from .retry import RetryExhausted, with_retry
from .run_recorder import RunRecorder
from .validation import validate_source_attribution
from .config import (
    CountryConfig,
    Depth,
    GovernmentDomainConfig,
    SignalCategory,
    load_all_country_configs,
    load_country_config,
    load_government_config,
)
from .ledger.initialize import initialize_country_ledger
from .ledger.storage import (
    archive_weekly_entries,
    country_ledger_exists,
    init_global_ledger,
    global_ledger_exists,
    load_country_ledger,
    load_global_ledger,
    save_country_ledger,
    save_global_ledger,
)
from .models import (
    CorrectionLogEntry,
    CountryLedger,
    Depth as DepthEnum,
    GlobalLedger,
    StoryClusterSummary,
    WeeklyEntry,
)

logger = logging.getLogger(__name__)


# =============================================================================
# Pipeline result
# =============================================================================

@dataclass
class CountryResult:
    """Result of processing a single country through the desk pipeline."""
    code: str
    country: str
    depth: Depth
    success: bool
    weekly_entry: Optional[WeeklyEntry] = None
    output: Optional[CountryAgentOutput] = None
    error: Optional[str] = None


@dataclass
class Layer2Result:
    """Result of Layer 2 collection for a single country."""
    code: str
    search_responses: list[SearchAPIResponse] = field(default_factory=list)
    extraction_results: list[ExtractionResult] = field(default_factory=list)
    gov_output: Optional[GovernmentAgentOutput] = None
    error: Optional[str] = None


@dataclass
class DeskPipelineResult:
    """Result of the full desk pipeline (triage + country agents + ledger writes)."""
    triage: Optional[TriageOutput] = None
    country_results: list[CountryResult] = field(default_factory=list)
    layer2_results: dict[str, Layer2Result] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def deep_dive_results(self) -> list[CountryResult]:
        return [r for r in self.country_results if r.depth == Depth.DEEP_DIVE and r.success]

    @property
    def maintenance_results(self) -> list[CountryResult]:
        return [r for r in self.country_results if r.depth == Depth.MAINTENANCE and r.success]

    @property
    def failed_results(self) -> list[CountryResult]:
        return [r for r in self.country_results if not r.success]


# =============================================================================
# Domain assembly
# =============================================================================

def assemble_country_domains(
    config: CountryConfig,
    gov_config: GovernmentDomainConfig | None = None,
    brave_client: BraveNewsClient | None = None,
) -> dict[str, list[str]]:
    """Assemble domain lists for a country from Brave sources + government domains.

    Returns a dict with keys:
        - allowed_domains: all domains (for web_search tool)
        - wire_domains: wire service domains
        - triage_domains: domestic triage source domains
        - gov_domains: government institution domains
    """
    gov_domains = []
    if gov_config:
        gov_domains = [d.domain for d in gov_config.domains]

    media_domains = []
    wire_domains = ["reuters.com", "apnews.com", "france24.com"]
    triage_domains = []

    if brave_client:
        sources = brave_client.get_indexed_sources(config.code)
        media_domains = [s.domain for s in sources]
        # Use all media domains as triage sources (triage scan is lightweight)
        triage_domains = media_domains[:10]  # top 10 for triage

    allowed_domains = list(set(wire_domains + media_domains + gov_domains))

    return {
        "allowed_domains": allowed_domains,
        "wire_domains": wire_domains,
        "triage_domains": triage_domains,
        "gov_domains": gov_domains,
    }


# =============================================================================
# Layer 2: Government source collection
# =============================================================================

async def collect_layer2_country(
    config: CountryConfig,
    gov_config: GovernmentDomainConfig,
    searchapi_client: SearchAPIClient,
    extractor: ExtractionOrchestrator,
    processing_date: date,
) -> Layer2Result:
    """Run Layer 2 pipeline for a single country: SearchAPI → extraction → gov agent."""
    code = config.code
    result = Layer2Result(code=code)

    try:
        # Build domain query list from government config
        domains = []
        for dom in gov_config.domains:
            queries = gov_config.query_terms if gov_config.query_terms else [""]
            domains.append({"domain": dom.domain, "queries": queries})

        # SearchAPI: query government domains (past week)
        start_date = processing_date - timedelta(days=7)
        time_min = start_date.strftime("%m/%d/%Y")
        time_max = processing_date.strftime("%m/%d/%Y")
        logger.info(f"Layer 2 search: {code} ({len(domains)} domains)")
        result.search_responses = await searchapi_client.search_country_government(
            domains=domains,
            time_period_min=time_min,
            time_period_max=time_max,
        )

        # Collect all discovered URLs
        all_urls = []
        for resp in result.search_responses:
            for sr in resp.results:
                if sr.url not in all_urls:
                    all_urls.append(sr.url)

        if not all_urls:
            logger.info(f"Layer 2: no URLs found for {code}")

        # Extraction: fetch full text for discovered URLs
        if all_urls:
            logger.info(f"Layer 2 extract: {code} ({len(all_urls)} URLs)")
            result.extraction_results = await extractor.extract_batch(all_urls)

        # Build extracted_content for government agent
        extracted_content = []
        url_to_snippet: dict[str, str] = {}
        for resp in result.search_responses:
            for sr in resp.results:
                url_to_snippet[sr.url] = sr.snippet or ""

        for er in result.extraction_results:
            extracted_content.append({
                "url": er.url,
                "domain": _domain_from_url(er.url),
                "title": er.title or "",
                "text": er.text or "",
                "extraction_failed": not er.success,
                "snippet": url_to_snippet.get(er.url, ""),
            })

        # Identify discovery gaps (domains with no results)
        domains_with_results = set()
        for resp in result.search_responses:
            for sr in resp.results:
                domains_with_results.add(_domain_from_url(sr.url))

        discovery_gaps = []
        for dom in gov_config.domains:
            if dom.domain not in domains_with_results:
                discovery_gaps.append({
                    "domain": dom.domain,
                    "institution": ", ".join(dom.institutions),
                    "priority": dom.priority,
                })

        # Identify extraction failures
        extraction_failures = []
        for er in result.extraction_results:
            if not er.success:
                extraction_failures.append({
                    "source_institution": _domain_from_url(er.url),
                    "url": er.url,
                    "error": er.error or f"Method: {er.method}",
                    "content_available": "snippet" if url_to_snippet.get(er.url) else "none",
                })

        # Government source agent
        logger.info(f"Layer 2 agent: {code}")
        result.gov_output = await run_government_agent(
            country_config=config,
            extracted_content=extracted_content,
            processing_date=processing_date,
            information_culture=gov_config.information_culture,
            gov_domain_config=gov_config,
            discovery_gaps=discovery_gaps or None,
            extraction_failures=extraction_failures or None,
        )

    except Exception as e:
        logger.error(f"Layer 2 failed for {code}: {e}", exc_info=True)
        result.error = str(e)

    return result


async def collect_layer2(
    configs: dict[str, CountryConfig],
    processing_date: date,
    max_concurrent: int = 5,
) -> dict[str, Layer2Result]:
    """Run Layer 2 pipeline for all countries in parallel.

    Returns dict of code → Layer2Result. Countries without government configs
    or where Layer 2 fails get empty/error results (non-blocking).
    """
    results: dict[str, Layer2Result] = {}

    # Load government configs
    gov_configs: dict[str, GovernmentDomainConfig] = {}
    for code in configs:
        try:
            gov_configs[code] = load_government_config(code)
        except FileNotFoundError:
            logger.warning(f"No government config for {code}, skipping Layer 2")
            results[code] = Layer2Result(code=code)

    if not gov_configs:
        return results

    semaphore = asyncio.Semaphore(max_concurrent)

    try:
        async with SearchAPIClient() as searchapi_client:
            async with ExtractionOrchestrator() as extractor:

                async def _collect(code: str) -> Layer2Result:
                    async with semaphore:
                        return await collect_layer2_country(
                            config=configs[code],
                            gov_config=gov_configs[code],
                            searchapi_client=searchapi_client,
                            extractor=extractor,
                            processing_date=processing_date,
                        )

                tasks = [_collect(code) for code in gov_configs]
                layer2_results = await asyncio.gather(*tasks, return_exceptions=True)

                for code, lr in zip(gov_configs.keys(), layer2_results):
                    if isinstance(lr, Exception):
                        logger.error(f"Layer 2 exception for {code}: {lr}")
                        results[code] = Layer2Result(code=code, error=str(lr))
                    else:
                        results[code] = lr

    except ValueError as e:
        # SearchAPI or extraction client initialization failure (missing API key)
        logger.warning(f"Layer 2 collection unavailable: {e}")
        for code in gov_configs:
            if code not in results:
                results[code] = Layer2Result(code=code, error=str(e))

    return results


def _domain_from_url(url: str) -> str:
    """Extract domain from URL."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


# =============================================================================
# Single-country processing
# =============================================================================

async def process_deep_dive(
    config: CountryConfig,
    ledger: CountryLedger,
    end_date: date,
    allowed_domains: list[str] | None = None,
    story_map: Optional[StoryMapOutput] = None,
    extracted_articles: Optional[list[ExtractionResult]] = None,
    gov_findings: str = "",
    recorder: RunRecorder | None = None,
) -> CountryResult:
    """Run country agent + devil's advocate for a single deep-dive country."""
    try:
        # Country agent (with retry)
        logger.info(f"Deep dive: {config.code} ({config.country})")
        output = await with_retry(
            run_country_agent, config, ledger, end_date, allowed_domains,
            story_map=story_map,
            extracted_articles=extracted_articles,
            gov_findings=gov_findings,
            context=f"country_agent_{config.code}",
        )

        # Attach story map clusters to the weekly entry for newsletter rendering
        if story_map and story_map.stories:
            output.weekly_entry.story_clusters = [
                StoryClusterSummary(
                    headline=sc.headline,
                    summary=sc.summary,
                    source_url=sc.representative_urls[0] if sc.representative_urls else "",
                    source_name=sc.sources[0] if sc.sources else "",
                )
                for sc in story_map.stories
            ]

        if recorder:
            recorder.write("07a_country_agent", {
                "code": config.code,
                "weekly_entry": output.weekly_entry,
                "signal_categories": output.signal_categories,
                "posture_summary": output.posture_summary,
            }, suffix=f"_{config.code}")

        # Devil's advocate (with retry, non-blocking on failure)
        logger.info(f"Devil's advocate: {config.code}")
        try:
            devils_advocate = await with_retry(
                run_devils_advocate, output.weekly_entry, config.country, ledger,
                context=f"devils_advocate_{config.code}",
            )
            output.weekly_entry.devils_advocate = devils_advocate
            if recorder:
                recorder.write("07b_devils_advocate", devils_advocate, suffix=f"_{config.code}")
        except (RetryExhausted, Exception) as da_err:
            logger.warning(
                f"Devil's advocate failed for {config.code}, proceeding without: {da_err}"
            )

        # Validate completeness (devil's advocate missing is a warning, not a failure)
        errors = output.weekly_entry.validate_complete()
        if errors:
            logger.warning(f"Validation warnings for {config.code}: {errors}")

        # Source attribution check
        attribution = validate_source_attribution(
            config.code, output.weekly_entry, extracted_articles,
        )
        if recorder and not attribution.clean:
            recorder.write("07c_attribution_flags", {
                "code": config.code,
                "developments_checked": attribution.developments_checked,
                "developments_flagged": attribution.developments_flagged,
                "flags": [
                    {
                        "category": f.category,
                        "headline": f.headline,
                        "unattributed_entities": f.unattributed_entities,
                        "cited_source_urls": f.cited_source_urls,
                        "severity": f.severity,
                    }
                    for f in attribution.flags
                ],
            }, suffix=f"_{config.code}")

        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.DEEP_DIVE,
            success=True,
            weekly_entry=output.weekly_entry,
            output=output,
        )

    except Exception as e:
        logger.error(f"Deep dive failed for {config.code}: {e}", exc_info=True)
        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.DEEP_DIVE,
            success=False,
            error=str(e),
        )


async def process_maintenance(
    config: CountryConfig,
    ledger: CountryLedger,
    scan: Optional[ScanResult],
    end_date: date,
    gov_findings: str = "",
) -> CountryResult:
    """Log maintenance entry for a country (no full analysis).

    Records triage scan results (wire headlines, domestic headline count)
    and government source findings for the historical record.
    """
    start_date = end_date - timedelta(days=7)
    date_range = f"{start_date.isoformat()} to {end_date.isoformat()}"

    try:
        # Build maintenance rationale from scan + gov findings
        rationale_parts = []
        if scan and not scan.error:
            if scan.wire_headlines:
                rationale_parts.append(
                    f"Wire coverage ({len(scan.wire_headlines)}): "
                    + "; ".join(scan.wire_headlines[:5])
                )
                if len(scan.wire_headlines) > 5:
                    rationale_parts.append(
                        f"  ... and {len(scan.wire_headlines) - 5} more wire headlines"
                    )
            else:
                rationale_parts.append("No wire coverage this week.")
            rationale_parts.append(
                f"Domestic headlines: {len(scan.domestic_headlines)} found."
            )
        elif scan and scan.error:
            rationale_parts.append(f"Triage scan error: {scan.error}")
        else:
            rationale_parts.append("No triage scan data.")

        if gov_findings:
            rationale_parts.append(f"Government sources: {gov_findings}")

        rationale = "\n".join(rationale_parts)

        entry = WeeklyEntry(
            week=end_date,
            date_range=date_range,
            depth=Depth.MAINTENANCE,
            activity_level={
                "rating": "quiet" if not (scan and scan.wire_headlines) else "low",
                "rationale": rationale,
            },
        )

        logger.info(
            "Maintenance %s: wire=%d, domestic=%d, gov_findings=%s",
            config.code,
            len(scan.wire_headlines) if scan else 0,
            len(scan.domestic_headlines) if scan else 0,
            "yes" if gov_findings else "no",
        )

        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.MAINTENANCE,
            success=True,
            weekly_entry=entry,
        )

    except Exception as e:
        logger.error(f"Maintenance failed for {config.code}: {e}")
        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.MAINTENANCE,
            success=False,
            error=str(e),
        )


def apply_to_ledger(
    ledger: CountryLedger,
    result: CountryResult,
) -> CountryLedger:
    """Apply a country result to its ledger and return the updated ledger."""
    if not result.success or result.weekly_entry is None:
        return ledger

    # Append weekly entry
    ledger.weekly_entries.append(result.weekly_entry)
    ledger.last_updated = result.weekly_entry.week

    if result.depth == Depth.DEEP_DIVE and result.output is not None:
        # Update signal categories and posture from country agent output
        ledger.signal_categories = result.output.signal_categories
        ledger.posture_summary = result.output.posture_summary

        # Update structural claim status from weekly checks
        for check in result.weekly_entry.structural_claim_checks:
            for claim in ledger.structural_claim_status:
                if claim.claim_ref == check.claim_ref:
                    claim.status = check.status
                    claim.last_checked = result.weekly_entry.week
                    claim.evidence_summary = check.evidence
                    if check.status in ("under_pressure", "weakened"):
                        claim.weeks_under_pressure += 1
                    elif check.status == "confirmed":
                        claim.weeks_under_pressure = 0

        # Log self-corrections
        for sc in result.weekly_entry.self_corrections:
            ledger.corrections_log.append(CorrectionLogEntry(
                correction_date=result.weekly_entry.week,
                original_week=sc.prior_week,
                original_claim=sc.original_claim,
                corrected_to=sc.correction,
                category_affected=sc.category,
                root_cause=sc.root_cause,
            ))

    elif result.depth == Depth.MAINTENANCE:
        # Increment maintenance counter
        ledger.posture_summary.consecutive_maintenance_weeks += 1
        ledger.posture_summary.as_of = result.weekly_entry.week

    # Archive if needed
    if ledger.needs_consolidation:
        ledger = archive_weekly_entries(ledger)

    return ledger


# =============================================================================
# Full pipeline
# =============================================================================

async def run_desk_pipeline(
    country_codes: list[str] | None = None,
    end_date: date | None = None,
    max_concurrent: int = 5,
    skip_triage: bool = False,
    force_deep_dive: bool = False,
    skip_layer2: bool = False,
    recorder: RunRecorder | None = None,
) -> DeskPipelineResult:
    """
    Run the full desk pipeline:
    Layer 2 → triage → country agents → devil's advocate → ledger write.

    Args:
        country_codes: Specific countries to process. None = all configured.
        end_date: End of the analysis week. None = today.
        max_concurrent: Max concurrent country agent calls.
        skip_triage: Skip triage and process all countries as deep dive.
        force_deep_dive: Force all countries to deep dive (ignores triage).
        skip_layer2: Skip Layer 2 government source collection.
    """
    end_date = end_date or date.today()
    result = DeskPipelineResult()

    # Load configs
    if country_codes:
        configs = {code: load_country_config(code) for code in country_codes}
    else:
        configs = load_all_country_configs()

    if not configs:
        result.errors.append("No country configs found")
        return result

    logger.info(f"Desk pipeline: {len(configs)} countries, end_date={end_date}")

    # Ensure global ledger exists
    global_ledger = None
    if global_ledger_exists():
        global_ledger = load_global_ledger()
    else:
        global_ledger = init_global_ledger()

    # Load or initialize country ledgers
    ledgers: dict[str, CountryLedger] = {}
    for code, config in configs.items():
        if country_ledger_exists(code):
            ledgers[code] = load_country_ledger(code)
        else:
            logger.info(f"Initializing ledger for {code}")
            ledger = await initialize_country_ledger(config)
            save_country_ledger(ledger)
            ledgers[code] = ledger

    # --- Step 1: Layer 2 (government source collection) ---
    layer2_results: dict[str, Layer2Result] = {}
    if not skip_layer2:
        logger.info("Running Layer 2: government source collection")
        layer2_results = await collect_layer2(configs, end_date, max_concurrent)
        result.layer2_results = layer2_results
        l2_ok = sum(1 for lr in layer2_results.values() if lr.gov_output and not lr.error)
        l2_err = sum(1 for lr in layer2_results.values() if lr.error)
        logger.info(f"Layer 2 complete: {l2_ok} successful, {l2_err} errors")
        if recorder:
            for code, lr in layer2_results.items():
                recorder.write("01_layer2", {
                    "code": code,
                    "search_result_count": sum(len(r.results) for r in lr.search_responses),
                    "extraction_count": len(lr.extraction_results),
                    "extraction_successes": sum(1 for r in lr.extraction_results if r.success),
                    "gov_findings": lr.gov_output.to_dict() if lr.gov_output else None,
                    "error": lr.error,
                }, suffix=f"_{code}")

    # --- Step 2: Assemble domain lists ---
    # Load government configs for domain assembly
    gov_configs: dict[str, GovernmentDomainConfig] = {}
    for code in configs:
        try:
            gov_configs[code] = load_government_config(code)
        except FileNotFoundError:
            pass

    # Assemble per-country domain lists
    brave_client = None
    try:
        brave_client = BraveNewsClient()
    except Exception as e:
        logger.warning(f"Brave client unavailable for domain assembly: {e}")

    domain_maps: dict[str, dict[str, list[str]]] = {}
    for code, config in configs.items():
        domain_maps[code] = assemble_country_domains(
            config,
            gov_config=gov_configs.get(code),
            brave_client=brave_client,
        )
    if recorder:
        recorder.write("02_domains", {
            code: {k: len(v) for k, v in dm.items()} for code, dm in domain_maps.items()
        })

    # --- Step 3: Triage ---
    if skip_triage or force_deep_dive:
        depth_map = {code: Depth.DEEP_DIVE for code in configs}
        scan_map: dict[str, ScanResult] = {}
    elif brave_client is None:
        logger.warning("Brave client unavailable — skipping triage, all deep dives")
        depth_map = {code: Depth.DEEP_DIVE for code in configs}
        scan_map = {}
    else:
        triage = await run_triage(
            list(configs.values()),
            ledgers,
            global_ledger,
            end_date,
            max_concurrent,
            brave_client=brave_client,
        )
        result.triage = triage
        depth_map = {d.code: d.depth for d in triage.decisions}
        scan_map = triage.scan_map
        if recorder:
            recorder.write("03a_triage_decisions", {
                d.code: {"depth": d.depth.value, "rationale": d.rationale, "triggered_by": d.triggered_by}
                for d in triage.decisions
            })
            recorder.write("03b_triage_scans", {
                s.code: {
                    "wire_headlines": s.wire_headlines,
                    "domestic_headlines": s.domestic_headlines,
                    "wire_result_count": len(s.wire_results),
                    "domestic_result_count": len(s.domestic_results),
                    "error": s.error,
                }
                for s in triage.scan_results
            })

    # --- Step 4: Deep-dive search expansion ---
    deep_dive_codes = [code for code, depth in depth_map.items() if depth == Depth.DEEP_DIVE]
    expansion_map: dict[str, ExpansionResult] = {}

    if deep_dive_codes and brave_client is not None:
        deep_dive_configs = [configs[code] for code in deep_dive_codes if code in configs]
        logger.info("Expansion: running for %d deep-dive countries", len(deep_dive_configs))
        expansion_map = await expand_all_countries(
            deep_dive_configs,
            brave_client,
            scan_map,
            end_date,
            max_concurrent,
        )
        for code, exp in expansion_map.items():
            logger.info(
                "Expansion %s: %d total results (wire=%d, domestic=%d, actor=%d, vocab=%d)",
                code, exp.total_count, *exp.source_counts.values(),
            )
        if recorder:
            for code, exp in expansion_map.items():
                recorder.write("04_expansion", {
                    "code": exp.code,
                    "country": exp.country,
                    "source_counts": exp.source_counts,
                    "total_count": exp.total_count,
                    "queries_run": exp.queries_run,
                    "dedup_record": exp.dedup_record,
                    "results": [
                        {"title": r.title, "url": r.url, "source_domain": r.source_domain, "age": r.age}
                        for r in exp.all_results
                    ],
                }, suffix=f"_{code}")
    elif deep_dive_codes:
        logger.warning("Brave client unavailable — skipping expansion")

    # --- Step 5: Story map ---
    story_maps: dict[str, StoryMapOutput] = {}

    if expansion_map:
        story_map_semaphore = asyncio.Semaphore(max_concurrent)

        async def _run_story_map(code: str) -> tuple[str, StoryMapOutput | None]:
            async with story_map_semaphore:
                try:
                    output = await run_story_map_agent(
                        configs[code],
                        expansion_map[code],
                        end_date,
                    )
                    return code, output
                except Exception as e:
                    logger.error("Story map failed for %s: %s", code, e, exc_info=True)
                    return code, None

        logger.info("Story map: running for %d deep-dive countries", len(expansion_map))
        sm_tasks = [_run_story_map(code) for code in expansion_map]
        sm_results = await asyncio.gather(*sm_tasks)
        for code, sm_output in sm_results:
            if sm_output is not None:
                story_maps[code] = sm_output
                logger.info(
                    "Story map %s: %d stories, %d single-source, %d URLs for extraction",
                    code, sm_output.stories_identified,
                    len(sm_output.single_source_items),
                    sm_output.extraction_url_count,
                )
        if recorder:
            for code, sm in story_maps.items():
                recorder.write("05_story_map", sm, suffix=f"_{code}")

    # --- Step 6: Selective extraction (story map representative URLs) ---
    extraction_map: dict[str, list[ExtractionResult]] = {}

    if story_maps:
        try:
            async with ExtractionOrchestrator() as extractor:
                for code, sm in story_maps.items():
                    urls = sm.all_representative_urls
                    if urls:
                        logger.info("Extraction %s: %d representative URLs", code, len(urls))
                        try:
                            extraction_map[code] = await extractor.extract_batch(urls)
                            success = sum(1 for r in extraction_map[code] if r.success)
                            logger.info(
                                "Extraction %s: %d/%d succeeded",
                                code, success, len(extraction_map[code]),
                            )
                        except Exception as e:
                            logger.error("Extraction failed for %s: %s", code, e, exc_info=True)
        except Exception as e:
            logger.warning("Extractor unavailable — skipping article extraction: %s", e)

    if recorder and extraction_map:
        for code, extractions in extraction_map.items():
            recorder.write("06_extraction", {
                "code": code,
                "total": len(extractions),
                "succeeded": sum(1 for r in extractions if r.success),
                "articles": [
                    {
                        "url": r.url,
                        "method": r.method,
                        "success": r.success,
                        "title": r.title,
                        "text_length": len(r.text) if r.text else 0,
                    }
                    for r in extractions
                ],
            }, suffix=f"_{code}")

    # --- Step 7: Process countries ---
    # Format government findings per country
    gov_findings_map: dict[str, str] = {}
    for code, l2 in layer2_results.items():
        if l2.gov_output and l2.gov_output.findings:
            findings_text = []
            for f in l2.gov_output.findings:
                findings_text.append(
                    f"- [{f.source_institution}] {f.what_happened} "
                    f"(type: {f.content_type}, categories: {', '.join(f.signal_categories)})"
                )
            if findings_text:
                gov_findings_map[code] = "\n".join(findings_text)

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _process(code: str) -> CountryResult:
        async with semaphore:
            config = configs[code]
            ledger = ledgers[code]
            depth = depth_map.get(code, Depth.DEEP_DIVE)  # default deep dive for unknown

            if depth == Depth.DEEP_DIVE:
                domains = domain_maps.get(code, {})
                return await process_deep_dive(
                    config, ledger, end_date,
                    allowed_domains=domains.get("allowed_domains"),
                    story_map=story_maps.get(code),
                    extracted_articles=extraction_map.get(code),
                    gov_findings=gov_findings_map.get(code, ""),
                    recorder=recorder,
                )
            else:
                scan = scan_map.get(code)
                return await process_maintenance(
                    config, ledger, scan, end_date,
                    gov_findings=gov_findings_map.get(code, ""),
                )

    # Run all countries in parallel (bounded by semaphore)
    tasks = [_process(code) for code in configs]
    country_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Collect results and write ledgers
    for cr in country_results:
        if isinstance(cr, Exception):
            result.errors.append(str(cr))
            continue

        result.country_results.append(cr)

        if cr.success and cr.code in ledgers:
            ledger = apply_to_ledger(ledgers[cr.code], cr)
            save_country_ledger(ledger)
            logger.info(f"Ledger updated: {cr.code} ({cr.depth.value})")
        elif not cr.success:
            logger.warning(f"Quarantined: {cr.code} — {cr.error}")

    # Summary
    logger.info(
        f"Desk pipeline complete: "
        f"{len(result.deep_dive_results)} deep dives, "
        f"{len(result.maintenance_results)} maintenance, "
        f"{len(result.failed_results)} failed"
    )

    if recorder:
        recorder.write_summary({
            "end_date": end_date.isoformat(),
            "countries": list(configs.keys()),
            "deep_dives": [r.code for r in result.deep_dive_results],
            "maintenance": [r.code for r in result.maintenance_results],
            "failed": [{"code": r.code, "error": r.error} for r in result.failed_results],
            "errors": result.errors,
        })

    return result
