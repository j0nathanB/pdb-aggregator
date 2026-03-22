"""
Government source agent: processes Layer 2 content for all 28 countries.

Sits between Layer 2 discovery/extraction and the country agent. Classifies
government publications as ground truth or intent signal, tags with signal
categories, and extracts analytical essentials.

Runs every week for all 28 countries, before triage.
"""

from __future__ import annotations

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
    THINKING_BUDGET_TOKENS,
    CountryConfig,
    GovernmentDomainConfig,
    SignalCategory,
    load_prompt,
)

logger = logging.getLogger(__name__)


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

SYSTEM_PROMPT = load_prompt("gov_source_agent")

OUTPUT_SCHEMA = load_prompt("gov_source_agent_output_schema")


def _render_system_prompt(country_name: str) -> str:
    """Render the system prompt with country-specific template variables."""
    return load_prompt("gov_source_agent", COUNTRY=country_name)


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
        "gov_source_agent_output_schema",
        COUNTRY_CODE=country_config.code,
        ANALYSIS_DATE=processing_date,
    )
    parts.append(f"\n{schema}")

    return "\n".join(parts)


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
    """Run the government source agent for a single country.

    Args:
        country_config: The country's configuration.
        extracted_content: Layer 2 extracted content (list of dicts with
            url, domain, title, text, extraction_failed, snippet keys).
        processing_date: The date of processing.
        information_culture: The country's information culture tag
            (transparent, managed, controlled).
        dossier_excerpt: Optional excerpt from the country dossier for
            structural context (relevant sections only).
        source_intel_map: Optional source intelligence map (government section).
        discovery_gaps: Optional list of domains with no search results.
        extraction_failures: Optional list of extraction failures from Layer 2.
        model: Override the default model.

    Returns:
        GovernmentAgentOutput with classified findings.
    """
    date_str = processing_date.isoformat()

    # If no content, no gaps, and no failures, return empty output
    if not extracted_content and not discovery_gaps and not extraction_failures:
        return GovernmentAgentOutput.empty(
            country_config.code, date_str, information_culture
        )

    # Build the user message
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

    # Render system prompt with country name
    system_prompt = _render_system_prompt(country_config.country)

    # Call the LLM
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    try:
        response = await client.messages.create(
            model=model or MODEL,
            max_tokens=4096,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET_TOKENS,
            },
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

        # Extract text from response
        text_content = ""
        for block in response.content:
            if block.type == "text":
                text_content = block.text
                break

        # Parse JSON from response
        parsed = _parse_response(text_content)

        # Build findings
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

        # Build discovery gaps from LLM response + any passed in
        gaps = []
        for g in parsed.get("discovery_gaps", []):
            gaps.append(DiscoveryGap(
                domain=g.get("domain", ""),
                institution=g.get("institution", ""),
                priority=g.get("priority", "P2"),
                assessment=g.get("assessment", ""),
            ))

        # Build extraction failures from LLM response + any passed in
        failures = []
        for f in parsed.get("extraction_failures", []):
            failures.append(ExtractionFailure(
                source_institution=f.get("source_institution", ""),
                url=f.get("url", ""),
                error=f.get("error", ""),
                content_available=f.get("content_available", ""),
                note=f.get("note", ""),
            ))

        return GovernmentAgentOutput(
            country=country_config.code,
            processing_date=date_str,
            information_culture=parsed.get("information_culture", information_culture),
            items_processed=parsed.get("items_processed", len(extracted_content)),
            items_with_findings=parsed.get("items_with_findings", len(findings)),
            findings=findings,
            discovery_gaps=gaps,
            extraction_failures=failures,
        )

    except Exception as e:
        logger.error(
            "Government source agent failed for %s: %s",
            country_config.code, e,
        )
        # Non-blocking — return empty output with the failure logged
        output = GovernmentAgentOutput.empty(
            country_config.code, date_str, information_culture
        )
        output.extraction_failures.append(ExtractionFailure(
            source_institution="government_agent",
            url="",
            error=str(e),
            content_available="",
            note="Agent call failed. Country agent proceeds with Layer 1 data only.",
        ))
        return output


def _parse_response(text: str) -> dict:
    """Parse JSON from the LLM response, handling markdown code blocks."""
    # Try to find JSON in markdown code block
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    # Try raw JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.warning("Could not parse government agent response as JSON")
        return {"findings": [], "discovery_gaps": [], "extraction_failures": []}
