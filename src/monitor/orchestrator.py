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
import os
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

import anthropic

from .agents.country import (
    CountryAgentOutput,
    build_country_agent_request,
    process_country_agent_response,
    run_country_agent,
)
from .agents.devils_advocate import run_devils_advocate
from .agents.expansion import ExpansionResult, expand_all_countries
from .agents.government import (
    GovernmentAgentOutput,
    build_government_agent_request,
    process_government_agent_response,
    run_government_agent,
)
from .agents.story_map import (
    StoryMapOutput,
    _empty_story_map,
    build_story_map_request,
    process_story_map_response,
    run_story_map_agent,
)
from .batch import BatchRequest, run_batch
from .agents.triage import TriageOutput, run_triage, scan_all_countries, ScanResult
from .collection.brave import BraveNewsClient
from .collection.extract import ExtractionOrchestrator, ExtractionResult
from .collection.searchapi import SearchAPIClient, SearchAPIResponse
from .retry import RetryExhausted, with_retry
from .run_recorder import RunRecorder
from .timing import TrackedSemaphore
from .validation import validate_source_attribution
from .config import (
    ClaimStatus,
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
    save_story_map,
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

# Opt-in flag for Batch API mode. When set, story_map (and in future country
# and government) submits as a batch — flat 50% off input + output for any
# job ending within 24h. The pipeline is weekly so latency doesn't matter.
# Off by default to preserve the existing async-parallel behavior for dev
# runs and emergency rollback.
USE_BATCH = os.getenv("MPM_USE_BATCH", "0") == "1"


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

@dataclass
class _Layer2Inputs:
    """Inputs prepared for the government source agent — search responses,
    extracted content, gaps, failures. Built by _collect_layer2_inputs;
    consumed by run_government_agent in the sync path or batched in the
    USE_BATCH path."""

    config: CountryConfig
    gov_config: GovernmentDomainConfig
    processing_date: date
    result: Layer2Result  # search_responses + extraction_results, error if any
    extracted_content: list[dict]
    discovery_gaps: list[dict]
    extraction_failures: list[dict]
    information_culture: str


async def _collect_layer2_inputs(
    config: CountryConfig,
    gov_config: GovernmentDomainConfig,
    searchapi_client: SearchAPIClient,
    extractor: ExtractionOrchestrator,
    processing_date: date,
) -> _Layer2Inputs:
    """Run SearchAPI + extraction for one country and build the gov-agent
    inputs. Does not invoke the agent. On any failure, returns a
    _Layer2Inputs whose `result.error` is set and whose content lists are
    empty — the agent step is skipped downstream."""
    code = config.code
    result = Layer2Result(code=code)
    extracted_content: list[dict] = []
    discovery_gaps: list[dict] = []
    extraction_failures: list[dict] = []

    try:
        # Build domain query list from government config
        domains = []
        for dom in gov_config.domains:
            queries = gov_config.query_terms if gov_config.query_terms else [""]
            domains.append({"domain": dom.domain, "queries": queries})

        # SearchAPI: query government domains (past week)
        start_date = processing_date - timedelta(days=6)
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

        # Government domains publish 10–20 distinct items per week (press
        # releases, MFA statements); the news default of 5 drops primary content.
        if all_urls:
            logger.info(f"Layer 2 extract: {code} ({len(all_urls)} URLs)")
            result.extraction_results = await extractor.extract_batch(
                all_urls, max_per_domain=20
            )

        # Build extracted_content for government agent
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

        for dom in gov_config.domains:
            if dom.domain not in domains_with_results:
                discovery_gaps.append({
                    "domain": dom.domain,
                    "institution": ", ".join(dom.institutions),
                    "priority": dom.priority,
                })

        # Identify extraction failures
        for er in result.extraction_results:
            if not er.success:
                extraction_failures.append({
                    "source_institution": _domain_from_url(er.url),
                    "url": er.url,
                    "error": er.error or f"Method: {er.method}",
                    "content_available": "snippet" if url_to_snippet.get(er.url) else "none",
                })

    except Exception as e:
        logger.error(f"Layer 2 inputs failed for {code}: {e}", exc_info=True)
        result.error = str(e)

    return _Layer2Inputs(
        config=config,
        gov_config=gov_config,
        processing_date=processing_date,
        result=result,
        extracted_content=extracted_content,
        discovery_gaps=discovery_gaps,
        extraction_failures=extraction_failures,
        information_culture=gov_config.information_culture,
    )


async def collect_layer2_country(
    config: CountryConfig,
    gov_config: GovernmentDomainConfig,
    searchapi_client: SearchAPIClient,
    extractor: ExtractionOrchestrator,
    processing_date: date,
) -> Layer2Result:
    """Sync path: collect inputs and invoke the gov agent for one country."""
    inputs = await _collect_layer2_inputs(
        config, gov_config, searchapi_client, extractor, processing_date,
    )
    if inputs.result.error:
        return inputs.result

    try:
        logger.info(f"Layer 2 agent: {config.code}")
        inputs.result.gov_output = await run_government_agent(
            country_config=config,
            extracted_content=inputs.extracted_content,
            processing_date=processing_date,
            information_culture=inputs.information_culture,
            gov_domain_config=gov_config,
            discovery_gaps=inputs.discovery_gaps or None,
            extraction_failures=inputs.extraction_failures or None,
        )
    except Exception as e:
        # run_government_agent itself returns non-blocking on internal
        # failures; this catches the truly unexpected (e.g. anthropic
        # transport error before the agent's own try wrapped the call).
        logger.error(f"Layer 2 agent failed for {config.code}: {e}", exc_info=True)
        inputs.result.error = str(e)

    return inputs.result


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

    semaphore = TrackedSemaphore(max_concurrent, "layer2")

    try:
        async with SearchAPIClient() as searchapi_client:
            async with ExtractionOrchestrator() as extractor:
                if USE_BATCH:
                    await _collect_layer2_batched(
                        configs, gov_configs, searchapi_client, extractor,
                        processing_date, semaphore, results,
                    )
                else:
                    async def _collect(code: str) -> Layer2Result:
                        async with semaphore.acquire(code):
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
                            logger.error("Layer 2 exception for %s: %s", code, lr, exc_info=lr)
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


async def _collect_layer2_batched(
    configs: dict[str, CountryConfig],
    gov_configs: dict[str, GovernmentDomainConfig],
    searchapi_client: SearchAPIClient,
    extractor: ExtractionOrchestrator,
    processing_date: date,
    semaphore: TrackedSemaphore,
    results: dict[str, Layer2Result],
) -> None:
    """Batched Layer 2 path: collect search+extract inputs for all countries
    in parallel (bounded by semaphore), then batch the gov-agent calls in a
    single Anthropic Batch API submission. Writes into `results` in place
    (matches the sync path's contract)."""
    from .config import ANTHROPIC_API_KEY

    # Phase A: collect inputs for all countries (HTTP I/O parallelism)
    async def _inputs_for(code: str) -> _Layer2Inputs:
        async with semaphore.acquire(code):
            return await _collect_layer2_inputs(
                config=configs[code],
                gov_config=gov_configs[code],
                searchapi_client=searchapi_client,
                extractor=extractor,
                processing_date=processing_date,
            )

    input_tasks = [_inputs_for(code) for code in gov_configs]
    input_outcomes = await asyncio.gather(*input_tasks, return_exceptions=True)

    inputs_by_code: dict[str, _Layer2Inputs] = {}
    for code, outcome in zip(gov_configs.keys(), input_outcomes):
        if isinstance(outcome, Exception):
            logger.error("Layer 2 inputs exception for %s: %s", code, outcome, exc_info=outcome)
            results[code] = Layer2Result(code=code, error=str(outcome))
            continue
        if outcome.result.error:
            # _collect_layer2_inputs already logged; record and skip the agent.
            results[code] = outcome.result
            continue
        inputs_by_code[code] = outcome

    if not inputs_by_code:
        logger.info("Layer 2 batch: no countries with usable inputs")
        return

    # Phase B: build gov-agent requests; short-circuit empties to their
    # final Layer2Result without batching.
    builts: dict[str, object] = {}
    for code, inputs in inputs_by_code.items():
        built_or_output = build_government_agent_request(
            country_config=inputs.config,
            extracted_content=inputs.extracted_content,
            processing_date=inputs.processing_date,
            information_culture=inputs.information_culture,
            gov_domain_config=inputs.gov_config,
            discovery_gaps=inputs.discovery_gaps or None,
            extraction_failures=inputs.extraction_failures or None,
        )
        if isinstance(built_or_output, GovernmentAgentOutput):
            # No content / no gaps / no failures — no API call needed.
            inputs.result.gov_output = built_or_output
            results[code] = inputs.result
        else:
            builts[code] = built_or_output

    if not builts:
        return

    # Phase C: submit batch
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")
    logger.info(
        "Layer 2 agent: submitting batch for %d countries (%d short-circuited)",
        len(builts), len(inputs_by_code) - len(builts),
    )
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    requests = [BatchRequest(b.custom_id, b.params) for b in builts.values()]
    batch_results = await run_batch(client, requests, label="government")

    # Phase D: dispatch responses, with sync fallback on batch failures.
    async def _dispatch(code: str) -> None:
        built = builts[code]
        inputs = inputs_by_code[code]
        br = batch_results.get(code)
        gov_output: GovernmentAgentOutput | None = None
        try:
            if br is not None and br.succeeded:
                gov_output = process_government_agent_response(built, br.message)
            else:
                logger.warning(
                    "Government agent %s: batch %s — retrying sync",
                    code, br.error_type if br else "missing",
                )
        except Exception as e:
            logger.warning(
                "Government agent %s: response processing failed (%s) — retrying sync",
                code, e,
            )

        if gov_output is None:
            # run_government_agent is itself non-blocking (returns
            # empty-with-failure rather than raising) — match the sync
            # path's behavior on any further failure.
            gov_output = await run_government_agent(
                country_config=inputs.config,
                extracted_content=inputs.extracted_content,
                processing_date=inputs.processing_date,
                information_culture=inputs.information_culture,
                gov_domain_config=inputs.gov_config,
                discovery_gaps=inputs.discovery_gaps or None,
                extraction_failures=inputs.extraction_failures or None,
            )

        inputs.result.gov_output = gov_output
        results[code] = inputs.result

    await asyncio.gather(*[_dispatch(code) for code in builts])


def _domain_from_url(url: str) -> str:
    """Extract domain from URL."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


# =============================================================================
# Story map orchestration (sync + batch paths)
# =============================================================================

async def _run_story_map_sync(
    configs: dict[str, CountryConfig],
    expansion_map: dict[str, ExpansionResult],
    end_date: date,
    max_concurrent: int,
) -> dict[str, StoryMapOutput]:
    """Original async-parallel story_map path: one API call per country,
    bounded by a semaphore, with a single retry on transient failure."""
    story_map_semaphore = TrackedSemaphore(max_concurrent, "story_map")
    out: dict[str, StoryMapOutput] = {}

    async def _run_one(code: str) -> tuple[str, StoryMapOutput | None]:
        async with story_map_semaphore.acquire(code):
            for attempt in range(2):
                try:
                    return code, await run_story_map_agent(
                        configs[code], expansion_map[code], end_date,
                    )
                except Exception as e:
                    if attempt == 0:
                        logger.warning(
                            "Story map failed for %s (attempt 1), retrying: %s", code, e,
                        )
                    else:
                        logger.error(
                            "Story map failed for %s after retry: %s", code, e, exc_info=True,
                        )
            return code, None

    logger.info("Story map: running for %d deep-dive countries (sync)", len(expansion_map))
    sm_tasks = [_run_one(code) for code in expansion_map]
    for code, sm in await asyncio.gather(*sm_tasks):
        if sm is not None:
            out[code] = sm
    return out


async def _run_story_map_batched(
    configs: dict[str, CountryConfig],
    expansion_map: dict[str, ExpansionResult],
    end_date: date,
) -> dict[str, StoryMapOutput]:
    """Batch API story_map path: 50% off input + output, single submission
    for all countries with non-empty search results.

    Countries with zero search results short-circuit to an empty output (no
    API call needed — preserves the sync-path behavior). Countries whose
    batch response succeeded are processed through process_story_map_response
    with a sync fallback callable (covers partial tool_use the same way the
    sync path does). Countries whose batch response failed fall back to a
    full sync run_story_map_agent call.
    """
    from .config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    builts = {}
    out: dict[str, StoryMapOutput] = {}
    for code, expansion in expansion_map.items():
        if expansion.total_count == 0:
            out[code] = _empty_story_map(configs[code], end_date)
            continue
        builts[code] = build_story_map_request(configs[code], expansion, end_date)

    if not builts:
        return out

    logger.info(
        "Story map: submitting batch for %d countries (%d short-circuited as empty)",
        len(builts), len(out),
    )
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    requests = [BatchRequest(b.custom_id, b.params) for b in builts.values()]
    batch_results = await run_batch(client, requests, label="story_map")

    async def _sync_fallback_call(params: dict) -> object:
        """Per-request sync retry for partial tool_use: replays a single
        non-streaming messages.create with the supplied (tools-stripped) params."""
        return await client.messages.create(**params)

    # Process responses; fall back to full sync for whole-request failures.
    pending_fallback: list[str] = []
    for code, built in builts.items():
        br = batch_results.get(code)
        if br is not None and br.succeeded:
            try:
                out[code] = await process_story_map_response(
                    built, br.message, fallback_call=_sync_fallback_call,
                )
            except Exception as e:
                logger.error(
                    "Story map %s: post-response processing failed: %s",
                    code, e, exc_info=True,
                )
                pending_fallback.append(code)
        else:
            logger.warning(
                "Story map %s: batch result missing or failed (%s) — retrying sync",
                code, br.error_type if br else "no_result",
            )
            pending_fallback.append(code)

    if pending_fallback:
        logger.info(
            "Story map: %d countries failed in batch, retrying via sync path",
            len(pending_fallback),
        )
        sync_tasks = [
            run_story_map_agent(configs[code], expansion_map[code], end_date)
            for code in pending_fallback
        ]
        sync_results = await asyncio.gather(*sync_tasks, return_exceptions=True)
        for code, result in zip(pending_fallback, sync_results):
            if isinstance(result, Exception):
                logger.error(
                    "Story map %s: sync fallback also failed: %s", code, result, exc_info=result,
                )
                continue
            out[code] = result

    return out


# =============================================================================
# Country agent orchestration (batch path)
# =============================================================================

async def _run_country_agents_batched(
    deep_dive_codes: list[str],
    configs: dict[str, CountryConfig],
    ledgers: dict[str, CountryLedger],
    end_date: date,
    domain_maps: dict[str, dict],
    story_maps: dict[str, StoryMapOutput],
    extraction_map: dict[str, list[ExtractionResult]],
    gov_findings_map: dict[str, str],
    recorder: RunRecorder | None,
) -> list[CountryResult]:
    """Batch the country_agent stage for all deep-dive countries, then run
    _post_country_agent per country in parallel.

    Per-request batch failures fall back to a full sync run_country_agent
    (with the existing retry policy). A complete batch failure (raised by
    the driver, e.g. transport error or timeout) propagates — the caller
    decides whether to retry or fall back to the sync path.
    """
    from .config import ANTHROPIC_API_KEY
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    builts: dict[str, object] = {}
    for code in deep_dive_codes:
        domains = domain_maps.get(code, {})
        builts[code] = build_country_agent_request(
            configs[code], ledgers[code], end_date,
            allowed_domains=domains.get("allowed_domains"),
            story_map=story_maps.get(code),
            extracted_articles=extraction_map.get(code),
            gov_findings=gov_findings_map.get(code, ""),
        )

    logger.info("Country agent: submitting batch for %d deep-dive countries", len(builts))
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    requests = [BatchRequest(b.custom_id, b.params) for b in builts.values()]
    batch_results = await run_batch(client, requests, label="country")

    async def _dispatch(code: str) -> CountryResult:
        built = builts[code]
        br = batch_results.get(code)
        output: CountryAgentOutput | None = None
        try:
            if br is not None and br.succeeded:
                output = process_country_agent_response(built, br.message)
            else:
                logger.warning(
                    "Country agent %s: batch %s — retrying sync",
                    code, br.error_type if br else "missing",
                )
        except Exception as e:
            logger.warning(
                "Country agent %s: response processing failed (%s) — retrying sync",
                code, e,
            )

        if output is None:
            try:
                domains = domain_maps.get(code, {})
                output = await with_retry(
                    run_country_agent,
                    configs[code], ledgers[code], end_date,
                    domains.get("allowed_domains"),
                    story_map=story_maps.get(code),
                    extracted_articles=extraction_map.get(code),
                    gov_findings=gov_findings_map.get(code, ""),
                    context=f"country_agent_{code}",
                )
            except Exception as e:
                logger.error(
                    f"Country agent failed for {code} (batch + sync fallback): {e}",
                    exc_info=True,
                )
                return CountryResult(
                    code=code,
                    country=configs[code].country,
                    depth=Depth.DEEP_DIVE,
                    success=False,
                    error=str(e),
                )

        return await _post_country_agent(
            configs[code], ledgers[code], end_date, output,
            story_maps.get(code), extraction_map.get(code), recorder,
        )

    return await asyncio.gather(*[_dispatch(code) for code in builts])


# =============================================================================
# Single-country processing
# =============================================================================

async def _post_country_agent(
    config: CountryConfig,
    ledger: CountryLedger,
    end_date: date,
    output: CountryAgentOutput,
    story_map: Optional[StoryMapOutput],
    extracted_articles: Optional[list[ExtractionResult]],
    recorder: RunRecorder | None,
) -> CountryResult:
    """Per-country pipeline after the country agent has produced its output:
    story-cluster attachment, story_map sidecar save, recorder write, devil's
    advocate, validation, source attribution. Called from both the sync
    process_deep_dive path and the batch country-agent dispatch path so the
    per-country contract is in one place."""
    try:
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

        # Persist full story map as sidecar (all sources per cluster)
        if story_map and story_map.stories:
            try:
                save_story_map(config.code, end_date, story_map)
            except Exception as e:
                logger.warning("Failed to save story map for %s: %s", config.code, e)

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

        # Source attribution check (non-blocking — a validation failure
        # should not discard an entire country's agent work).
        try:
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
                            "unattributed_figures": f.unattributed_figures,
                            "cited_source_urls": f.cited_source_urls,
                            "severity": f.severity,
                        }
                        for f in attribution.flags
                    ],
                }, suffix=f"_{config.code}")
        except Exception as attr_err:
            logger.warning(
                f"Source attribution check failed for {config.code}, proceeding without: {attr_err}"
            )

        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.DEEP_DIVE,
            success=True,
            weekly_entry=output.weekly_entry,
            output=output,
        )

    except Exception as e:
        logger.error(f"Deep dive post-processing failed for {config.code}: {e}", exc_info=True)
        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.DEEP_DIVE,
            success=False,
            error=str(e),
        )


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
    """Run country agent + per-country post-processing for one deep-dive country."""
    logger.info(f"Deep dive: {config.code} ({config.country})")
    try:
        output = await with_retry(
            run_country_agent, config, ledger, end_date, allowed_domains,
            story_map=story_map,
            extracted_articles=extracted_articles,
            gov_findings=gov_findings,
            context=f"country_agent_{config.code}",
        )
    except Exception as e:
        logger.error(f"Country agent failed for {config.code}: {e}", exc_info=True)
        return CountryResult(
            code=config.code,
            country=config.country,
            depth=Depth.DEEP_DIVE,
            success=False,
            error=str(e),
        )
    return await _post_country_agent(
        config, ledger, end_date, output, story_map, extracted_articles, recorder,
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
    start_date = end_date - timedelta(days=6)
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

    # Upsert weekly entry (replace if same week already exists)
    existing_idx = next(
        (i for i, e in enumerate(ledger.weekly_entries) if e.week == result.weekly_entry.week),
        None,
    )
    if existing_idx is not None:
        logger.warning("Replacing existing entry for %s week %s", ledger.code, result.weekly_entry.week)
        ledger.weekly_entries[existing_idx] = result.weekly_entry
    else:
        ledger.weekly_entries.append(result.weekly_entry)
    ledger.last_updated = result.weekly_entry.week

    if result.depth == Depth.DEEP_DIVE and result.output is not None:
        # Update signal categories and posture from country agent output
        ledger.signal_categories = result.output.signal_categories
        ledger.posture_summary = result.output.posture_summary
        # Unconditional reset on deep-dive — don't rely on LLM output for this
        ledger.posture_summary.consecutive_maintenance_weeks = 0
        ledger.posture_summary.last_deep_dive = result.weekly_entry.week

        # Update structural claim status from weekly checks
        for check in result.weekly_entry.structural_claim_checks:
            for claim in ledger.structural_claim_status:
                if claim.claim_ref == check.claim_ref:
                    claim.status = check.status
                    claim.last_checked = result.weekly_entry.week
                    claim.evidence_summary = check.evidence
                    if check.status in (ClaimStatus.UNDER_PRESSURE, ClaimStatus.WEAKENED):
                        claim.weeks_under_pressure += 1
                    elif check.status == ClaimStatus.CONFIRMED:
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
    force_deep_dive: bool = True,
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
    # The triage SCAN (wire + domestic Brave sweeps) populates scan_map for
    # story_map downstream. The LLM-based depth DECISION runs on top of the
    # scan only when neither force_deep_dive nor skip_triage is set.
    scan_map: dict[str, ScanResult] = {}

    if skip_triage:
        logger.info("skip_triage=True — skipping triage scan")
        depth_map = {code: Depth.DEEP_DIVE for code in configs}
    elif brave_client is None:
        logger.warning("Brave client unavailable — skipping triage scan, all deep dives")
        depth_map = {code: Depth.DEEP_DIVE for code in configs}
    elif force_deep_dive:
        # Scan to feed story_map, but skip the LLM decision.
        scan_results = await scan_all_countries(
            list(configs.values()), brave_client, end_date, max_concurrent,
        )
        scan_map = {s.code: s for s in scan_results}
        scan_ok = sum(1 for s in scan_results if not s.error)
        logger.info(
            "Triage scan (force_deep_dive): %d/%d successful",
            scan_ok, len(scan_results),
        )
        depth_map = {code: Depth.DEEP_DIVE for code in configs}
        if recorder:
            recorder.write("03b_triage_scans", {
                s.code: {
                    "wire_headlines": s.wire_headlines,
                    "domestic_headlines": s.domestic_headlines,
                    "wire_result_count": len(s.wire_results),
                    "domestic_result_count": len(s.domestic_results),
                    "error": s.error,
                }
                for s in scan_results
            })
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
        if USE_BATCH:
            story_maps = await _run_story_map_batched(
                configs, expansion_map, end_date,
            )
        else:
            story_maps = await _run_story_map_sync(
                configs, expansion_map, end_date, max_concurrent,
            )
        for code, sm in story_maps.items():
            logger.info(
                "Story map %s: %d stories, %d single-source, %d URLs for extraction",
                code, sm.stories_identified,
                len(sm.single_source_items),
                sm.extraction_url_count,
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

    deep_dive_codes = [
        code for code in configs
        if depth_map.get(code, Depth.DEEP_DIVE) == Depth.DEEP_DIVE
    ]
    maintenance_codes = [
        code for code in configs
        if depth_map.get(code, Depth.DEEP_DIVE) != Depth.DEEP_DIVE
    ]

    if USE_BATCH and deep_dive_codes:
        # Batch the country_agent stage for all deep-dive countries; run
        # maintenance countries (no country_agent) through the existing sync
        # semaphore path so their behavior is unchanged.
        try:
            deep_dive_results: list[CountryResult] = await _run_country_agents_batched(
                deep_dive_codes, configs, ledgers, end_date,
                domain_maps, story_maps, extraction_map, gov_findings_map,
                recorder,
            )
        except Exception as e:
            # Whole-batch failure (transport / timeout) — fall back to the
            # full sync per-country path rather than dropping the run.
            logger.error(
                "Country agent batch failed (%s) — falling back to sync for all deep-dives",
                e, exc_info=True,
            )
            deep_dive_results = []  # rebuilt below via the sync loop
            maintenance_codes = list(configs.keys())  # re-run everything sync

        maint_semaphore = TrackedSemaphore(max_concurrent, "country_agents_maint")

        async def _process_maint(code: str) -> CountryResult:
            async with maint_semaphore.acquire(code):
                config = configs[code]
                ledger = ledgers[code]
                depth = depth_map.get(code, Depth.DEEP_DIVE)
                if depth == Depth.DEEP_DIVE:
                    # Reached only when the batch fell back wholesale (above).
                    domains = domain_maps.get(code, {})
                    return await process_deep_dive(
                        config, ledger, end_date,
                        allowed_domains=domains.get("allowed_domains"),
                        story_map=story_maps.get(code),
                        extracted_articles=extraction_map.get(code),
                        gov_findings=gov_findings_map.get(code, ""),
                        recorder=recorder,
                    )
                scan = scan_map.get(code)
                return await process_maintenance(
                    config, ledger, scan, end_date,
                    gov_findings=gov_findings_map.get(code, ""),
                )

        maint_results = await asyncio.gather(
            *[_process_maint(code) for code in maintenance_codes],
            return_exceptions=True,
        )
        country_results = list(deep_dive_results) + list(maint_results)
    else:
        semaphore = TrackedSemaphore(max_concurrent, "country_agents")

        async def _process(code: str) -> CountryResult:
            async with semaphore.acquire(code):
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
            logger.error("Country task failed: %s: %s", type(cr).__name__, cr, exc_info=cr)
            result.errors.append(f"{type(cr).__name__}: {cr}")
            continue

        result.country_results.append(cr)

        if cr.success and cr.code in ledgers:
            ledger = apply_to_ledger(ledgers[cr.code], cr)
            save_country_ledger(ledger)
            logger.info(f"Ledger updated: {cr.code} ({cr.depth.value})")
        elif not cr.success:
            logger.warning(f"Quarantined: {cr.code} — {cr.error}")

    # Summary
    brave_calls = brave_client.api_call_count if brave_client else 0
    logger.info(
        f"Desk pipeline complete: "
        f"{len(result.deep_dive_results)} deep dives, "
        f"{len(result.maintenance_results)} maintenance, "
        f"{len(result.failed_results)} failed, "
        f"{brave_calls} Brave API calls"
    )

    if recorder:
        recorder.write_summary({
            "end_date": end_date.isoformat(),
            "countries": list(configs.keys()),
            "deep_dives": [r.code for r in result.deep_dive_results],
            "maintenance": [r.code for r in result.maintenance_results],
            "failed": [{"code": r.code, "error": r.error} for r in result.failed_results],
            "errors": result.errors,
            "brave_api_calls": brave_calls,
        })

    return result
