"""
Government source agent: processes Layer 2 content for all 28 countries.

Sits between Layer 2 discovery/extraction and the country agent. Classifies
government publications as ground truth or intent signal, tags with signal
categories, and extracts analytical essentials.

Runs every week for all 28 countries, before triage.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Optional, Union

import anthropic

from ..rate_limit import anthropic_limiter
from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CountryConfig,
    GovernmentDomainConfig,
    SignalCategory,
    load_prompt,
)

from ..sanitize import _record_fallback, extract_json

logger = logging.getLogger(__name__)

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"

GOVERNMENT_AGENT_TOOL_NAME = "record_government_findings"
GOVERNMENT_AGENT_TOOL = {
    "name": GOVERNMENT_AGENT_TOOL_NAME,
    "description": (
        "Record the government source agent's classified findings, "
        "discovery gaps, and extraction failures. Call exactly once when "
        "analysis is complete."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "information_culture": {"type": "string"},
            "items_processed": {"type": "integer"},
            "items_with_findings": {"type": "integer"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source_institution": {"type": "string"},
                        "source_category": {"type": "string"},
                        "source_url": {"type": "string"},
                        "publication_date": {"type": "string"},
                        "content_type": {"type": "string"},
                        "signal_categories": {"type": "array", "items": {"type": "string"}},
                        "what_happened": {"type": "string"},
                        "structural_significance": {"type": "string"},
                        "framing_note": {"type": "string"},
                        "information_culture_note": {"type": "string"},
                        "cross_reference": {"type": "string"},
                    },
                },
            },
            "discovery_gaps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "institution": {"type": "string"},
                        "priority": {"type": "string"},
                        "assessment": {"type": "string"},
                    },
                },
            },
            "extraction_failures": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "source_institution": {"type": "string"},
                        "url": {"type": "string"},
                        "error": {"type": "string"},
                        "content_available": {"type": "string"},
                        "note": {"type": "string"},
                    },
                },
            },
        },
    },
}


# =============================================================================
# Output schema
# =============================================================================


@dataclass
class GovernmentFinding:
    """A single classified government source finding."""

    source_institution: str
    source_category: str  # foreign_ministry, defense_ministry, etc.
    source_url: str
    publication_date: str
    content_type: str  # ground_truth, intent_signal, both
    signal_categories: list[str]
    what_happened: str
    structural_significance: str
    framing_note: str
    information_culture_note: str
    cross_reference: str


@dataclass
class DiscoveryGap:
    """Record of a government domain with no search results this week."""

    domain: str
    institution: str
    priority: str  # P1, P2
    assessment: str  # Expected — ..., Unexpected — ..., Uncertain — ...


@dataclass
class ExtractionFailure:
    """Record of a URL discovered but not fully extracted."""

    source_institution: str
    url: str
    error: str
    content_available: str  # headline_only, snippet, partial_text
    note: str


@dataclass
class GovernmentAgentOutput:
    """Complete output from the government source agent for one country."""

    country: str
    processing_date: str
    information_culture: str  # transparent, managed, controlled
    items_processed: int
    items_with_findings: int
    findings: list[GovernmentFinding]
    discovery_gaps: list[DiscoveryGap]
    extraction_failures: list[ExtractionFailure]

    def to_dict(self) -> dict:
        """Serialize to dict for JSON output."""
        return {
            "country": self.country,
            "processing_date": self.processing_date,
            "information_culture": self.information_culture,
            "items_processed": self.items_processed,
            "items_with_findings": self.items_with_findings,
            "findings": [
                {
                    "source_institution": f.source_institution,
                    "source_category": f.source_category,
                    "source_url": f.source_url,
                    "publication_date": f.publication_date,
                    "content_type": f.content_type,
                    "signal_categories": f.signal_categories,
                    "what_happened": f.what_happened,
                    "structural_significance": f.structural_significance,
                    "framing_note": f.framing_note,
                    "information_culture_note": f.information_culture_note,
                    "cross_reference": f.cross_reference,
                }
                for f in self.findings
            ],
            "discovery_gaps": [
                {
                    "domain": g.domain,
                    "institution": g.institution,
                    "priority": g.priority,
                    "assessment": g.assessment,
                }
                for g in self.discovery_gaps
            ],
            "extraction_failures": [
                {
                    "source_institution": f.source_institution,
                    "url": f.url,
                    "error": f.error,
                    "content_available": f.content_available,
                    "note": f.note,
                }
                for f in self.extraction_failures
            ],
        }

    @classmethod
    def empty(
        cls,
        country_code: str,
        processing_date: str,
        information_culture: str = "managed",
    ) -> GovernmentAgentOutput:
        """Create an empty output for countries with no Layer 2 content."""
        return cls(
            country=country_code,
            processing_date=processing_date,
            information_culture=information_culture,
            items_processed=0,
            items_with_findings=0,
            findings=[],
            discovery_gaps=[],
            extraction_failures=[],
        )

    @property
    def has_significant_findings(self) -> bool:
        """Whether this output contains findings that should influence triage."""
        return any(
            f.content_type in ("ground_truth", "both")
            for f in self.findings
        )


# =============================================================================
# Prompt
# =============================================================================

SYSTEM_PROMPT = load_prompt("agents/gov_source_agent")

OUTPUT_SCHEMA = load_prompt("agents/gov_source_agent_output_schema")


def _render_system_prompt() -> str:
    """Return the gov source agent system prompt.

    Country-agnostic so the cached prefix is byte-identical across all 30
    parallel calls in a weekly run. The country is delivered via the user
    message (see _build_user_message — `## Country: ...` line).
    """
    return SYSTEM_PROMPT


# =============================================================================
# Agent
# =============================================================================


def _build_user_message(
    country_config: CountryConfig,
    extracted_content: list[dict],
    processing_date: str,
    information_culture: str = "managed",
    gov_domain_config: GovernmentDomainConfig | None = None,
    dossier_excerpt: str = "",
    source_intel_map: str = "",
    discovery_gaps: list[dict] | None = None,
    extraction_failures: list[dict] | None = None,
) -> str:
    """Build the user message for the government source agent."""
    parts = []

    # Country context
    parts.append(f"## Country: {country_config.country} ({country_config.code})")
    parts.append(f"Tier: {country_config.tier.value}")
    parts.append(f"Region: {country_config.region.value}")
    parts.append(f"Information culture: {information_culture}")
    parts.append(f"Processing date: {processing_date}")
    parts.append("")

    # Actors for context
    parts.append("## Key Actors")
    for actor in country_config.actors:
        marker = " (primary)" if actor.primary else ""
        parts.append(f"- {actor.name}: {actor.role}{marker}")
    parts.append("")

    # Government sources being monitored
    parts.append("## Monitored Government Sources")
    if gov_domain_config:
        for dom in gov_domain_config.domains:
            institutions = ", ".join(dom.institutions)
            parts.append(f"- {institutions} ({dom.domain}) — {dom.priority}")
    parts.append("")

    # Source intelligence map
    if source_intel_map:
        parts.append("## Source Intelligence Map (Government Section)")
        parts.append(source_intel_map)
        parts.append("")

    # Dossier excerpt for structural context
    if dossier_excerpt:
        parts.append("## Dossier Context (for structural significance assessment)")
        parts.append(dossier_excerpt)
        parts.append("")

    # Extracted government content
    parts.append("## Layer 2 Content (Government Publications)")
    if not extracted_content:
        parts.append("No government content was discovered this week.")
    else:
        for i, item in enumerate(extracted_content, 1):
            parts.append(f"### Item {i}")
            parts.append(f"URL: {item.get('url', 'unknown')}")
            parts.append(f"Domain: {item.get('domain', 'unknown')}")
            parts.append(f"Title: {item.get('title', 'No title')}")
            if item.get("extraction_failed"):
                parts.append(f"[Extraction failed — snippet only: {item.get('snippet', '')}]")
            else:
                text = item.get("text", "")
                # Truncate very long texts
                if len(text) > 3000:
                    text = text[:3000] + "\n[...truncated...]"
                parts.append(f"Text:\n{text}")
            parts.append("")

    # Discovery gaps (domains with no search results)
    if discovery_gaps:
        parts.append("## Discovery Gaps")
        parts.append("The following government domains returned no SearchAPI results this week:")
        for gap in discovery_gaps:
            parts.append(
                f"- {gap.get('domain', 'unknown')} ({gap.get('institution', 'unknown')}) "
                f"— Priority: {gap.get('priority', 'P2')}"
            )
        parts.append("")

    # Extraction failures (URLs discovered but not fully extracted)
    if extraction_failures:
        parts.append("## Extraction Failures")
        parts.append("SearchAPI discovered these URLs but extraction failed or was partial:")
        for fail in extraction_failures:
            parts.append(
                f"- {fail.get('url', 'unknown')} ({fail.get('domain', 'unknown')}): "
                f"{fail.get('error', 'unknown error')} — "
                f"Content available: {fail.get('content_available', 'none')}"
            )
        parts.append("")

    # Output schema with template variables filled
    schema = load_prompt(
        "agents/gov_source_agent_output_schema",
        COUNTRY_CODE=country_config.code,
        ANALYSIS_DATE=processing_date,
    )
    parts.append(f"\n{schema}")

    return "\n".join(parts)


@dataclass
class GovernmentAgentBuilt:
    """A built but not-yet-executed government agent request.

    Returned by `build_government_agent_request`, consumed by
    `process_government_agent_response`. Holds the API params plus the side
    channels (system_prompt, user_message, processing_date,
    information_culture, items_count) needed for trace writing and the
    failure-fallback output after the response arrives.
    """

    country_config: CountryConfig
    processing_date: date
    information_culture: str
    items_processed: int
    custom_id: str
    params: dict[str, Any]
    system_prompt: str
    user_message: str


def build_government_agent_request(
    country_config: CountryConfig,
    extracted_content: list[dict],
    processing_date: date,
    information_culture: str = "managed",
    gov_domain_config: GovernmentDomainConfig | None = None,
    dossier_excerpt: str = "",
    source_intel_map: str = "",
    discovery_gaps: list[dict] | None = None,
    extraction_failures: list[dict] | None = None,
    model: str | None = None,
) -> Union[GovernmentAgentBuilt, GovernmentAgentOutput]:
    """Build the API params for one government agent call, or short-circuit
    with an empty output if there's nothing to process.

    Returns GovernmentAgentBuilt if the caller should issue an API call;
    returns GovernmentAgentOutput.empty(...) directly if there's no content,
    no gaps, and no failures (no API call needed).
    """
    date_str = processing_date.isoformat()

    if not extracted_content and not discovery_gaps and not extraction_failures:
        logger.debug(
            "Gov agent %s: no content, gaps, or failures — returning empty",
            country_config.code,
        )
        return GovernmentAgentOutput.empty(
            country_config.code, date_str, information_culture
        )

    user_message = _build_user_message(
        country_config=country_config,
        extracted_content=extracted_content,
        processing_date=date_str,
        information_culture=information_culture,
        gov_domain_config=gov_domain_config,
        dossier_excerpt=dossier_excerpt,
        source_intel_map=source_intel_map,
        discovery_gaps=discovery_gaps,
        extraction_failures=extraction_failures,
    )

    system_prompt = _render_system_prompt()

    logger.info(
        "Gov agent %s: %d items, %d gaps, %d extraction failures, culture=%s",
        country_config.code, len(extracted_content),
        len(discovery_gaps or []), len(extraction_failures or []),
        information_culture,
    )
    logger.debug(
        "Gov agent %s: user message length=%d chars",
        country_config.code, len(user_message),
    )

    params: dict[str, Any] = dict(
        model=model or MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 4096,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user_message}],
    )
    if USE_TOOL_SCHEMA:
        params["tools"] = [GOVERNMENT_AGENT_TOOL]

    return GovernmentAgentBuilt(
        country_config=country_config,
        processing_date=processing_date,
        information_culture=information_culture,
        items_processed=len(extracted_content),
        custom_id=country_config.code,
        params=params,
        system_prompt=system_prompt,
        user_message=user_message,
    )


def _empty_with_failure(
    country_code: str, date_str: str, information_culture: str, error: Exception
) -> GovernmentAgentOutput:
    """Build the empty-with-failure output that the agent returns on any
    response-processing exception. Kept separate so both sync and batch
    paths produce identical fallback shape."""
    output = GovernmentAgentOutput.empty(country_code, date_str, information_culture)
    output.extraction_failures.append(ExtractionFailure(
        source_institution="government_agent",
        url="",
        error=str(error),
        content_available="",
        note="Agent call failed. Country agent proceeds with Layer 1 data only.",
    ))
    return output


def process_government_agent_response(
    built: GovernmentAgentBuilt,
    response: Any,
) -> GovernmentAgentOutput:
    """Parse the response and hydrate the structured output.

    On any exception, returns an empty output with the failure logged —
    matches the non-blocking behavior of the original run_government_agent.
    """
    date_str = built.processing_date.isoformat()
    try:
        text_content = ""
        for block in response.content:
            if block.type == "text":
                text_content = block.text
                break

        tool_input: dict | None = None
        if USE_TOOL_SCHEMA:
            for block in response.content:
                if (getattr(block, "type", None) == "tool_use"
                        and getattr(block, "name", None) == GOVERNMENT_AGENT_TOOL_NAME):
                    tool_input = getattr(block, "input", None)
                    break

        logger.debug(
            "Gov agent %s: API response — input=%d, output=%d tokens%s",
            built.country_config.code,
            response.usage.input_tokens, response.usage.output_tokens,
            " [tool_use]" if tool_input else "",
        )

        from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage

        if tool_input is not None:
            import json as _json
            save_raw_response(
                "government", built.country_config.code, built.processing_date,
                system_prompt=built.system_prompt,
                user_message=built.user_message,
                response_text=_json.dumps(tool_input, indent=2, ensure_ascii=False),
                thinking_text=extract_thinking(response),
                usage=extract_usage(response),
            )
            parsed = tool_input
        else:
            if USE_TOOL_SCHEMA:
                logger.warning(
                    "Gov agent %s: tool_use enabled but no valid block; falling back",
                    built.country_config.code,
                )
                _record_fallback("government_tool_use_fallback")
            save_raw_response(
                "government", built.country_config.code, built.processing_date,
                system_prompt=built.system_prompt,
                user_message=built.user_message,
                response_text=text_content,
                thinking_text=extract_thinking(response),
                usage=extract_usage(response),
            )
            parsed = _parse_response(text_content)

        findings = []
        for f in parsed.get("findings", []):
            findings.append(GovernmentFinding(
                source_institution=f.get("source_institution", ""),
                source_category=f.get("source_category", ""),
                source_url=f.get("source_url", ""),
                publication_date=f.get("publication_date", ""),
                content_type=f.get("content_type", "ground_truth"),
                signal_categories=f.get("signal_categories", []),
                what_happened=f.get("what_happened", ""),
                structural_significance=f.get("structural_significance", ""),
                framing_note=f.get("framing_note", ""),
                information_culture_note=f.get("information_culture_note", ""),
                cross_reference=f.get("cross_reference", ""),
            ))

        gaps = []
        for g in parsed.get("discovery_gaps", []):
            gaps.append(DiscoveryGap(
                domain=g.get("domain", ""),
                institution=g.get("institution", ""),
                priority=g.get("priority", "P2"),
                assessment=g.get("assessment", ""),
            ))

        failures = []
        for f in parsed.get("extraction_failures", []):
            failures.append(ExtractionFailure(
                source_institution=f.get("source_institution", ""),
                url=f.get("url", ""),
                error=f.get("error", ""),
                content_available=f.get("content_available", ""),
                note=f.get("note", ""),
            ))

        output = GovernmentAgentOutput(
            country=built.country_config.code,
            processing_date=date_str,
            information_culture=parsed.get("information_culture", built.information_culture),
            items_processed=parsed.get("items_processed", built.items_processed),
            items_with_findings=parsed.get("items_with_findings", len(findings)),
            findings=findings,
            discovery_gaps=gaps,
            extraction_failures=failures,
        )
        logger.info(
            "Gov agent %s: %d findings (%d significant), %d gaps, %d failures",
            built.country_config.code, len(findings),
            sum(1 for f in findings if f.content_type in ("ground_truth", "both")),
            len(gaps), len(failures),
        )

        update_trace_parsed(
            "government", built.country_config.code, built.processing_date,
            parsed_output=parsed,
        )
        return output

    except Exception as e:
        logger.error(
            "Government source agent failed for %s: %s",
            built.country_config.code, e,
        )
        return _empty_with_failure(
            built.country_config.code, date_str, built.information_culture, e
        )


async def run_government_agent(
    country_config: CountryConfig,
    extracted_content: list[dict],
    processing_date: date,
    information_culture: str = "managed",
    gov_domain_config: GovernmentDomainConfig | None = None,
    dossier_excerpt: str = "",
    source_intel_map: str = "",
    discovery_gaps: list[dict] | None = None,
    extraction_failures: list[dict] | None = None,
    model: str | None = None,
) -> GovernmentAgentOutput:
    """Run the government source agent for a single country (sync path).

    Composes build_government_agent_request and process_government_agent_response
    with a sync API call. Non-blocking: returns an empty-with-failure output
    on any error rather than raising. The orchestrator's batch path uses the
    same two halves but submits `built.params` via the Batch API.
    """
    built = build_government_agent_request(
        country_config=country_config,
        extracted_content=extracted_content,
        processing_date=processing_date,
        information_culture=information_culture,
        gov_domain_config=gov_domain_config,
        dossier_excerpt=dossier_excerpt,
        source_intel_map=source_intel_map,
        discovery_gaps=discovery_gaps,
        extraction_failures=extraction_failures,
        model=model,
    )
    if isinstance(built, GovernmentAgentOutput):
        return built  # short-circuited — no API call needed

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    try:
        from ..timing import with_heartbeat
        async with anthropic_limiter():
            response = await with_heartbeat(
                client.messages.create(**built.params),
                f"Government agent {country_config.code}: API call",
            )
    except Exception as e:
        # Match prior non-blocking behavior: transport / API failures return
        # the empty-with-failure output instead of raising.
        logger.error(
            "Government source agent failed for %s: %s",
            country_config.code, e,
        )
        return _empty_with_failure(
            country_config.code, processing_date.isoformat(), information_culture, e
        )

    return process_government_agent_response(built, response)


def _parse_response(text: str) -> dict:
    """Parse JSON from the LLM response, handling markdown code blocks."""
    try:
        return extract_json(text, context="government")
    except ValueError:
        logger.warning("Could not parse government agent response as JSON")
        return {"findings": [], "discovery_gaps": [], "extraction_failures": []}
