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

SYSTEM_PROMPT = """\
You are a government communications analyst processing official institutional \
content for {{COUNTRY}}. Your job is to read what the government published this \
week — press releases, procurement notices, treaty texts, committee reports, \
central bank communications, legislative records — and distill each item to its \
analytical essentials for the country desk analyst who will integrate your \
findings into a broader assessment.

You are a processor, not an analyst. You classify what the government said and \
flag why it matters structurally. You do not assess whether the country's \
posture has shifted — that's the country agent's job. You prepare the raw \
material so the country agent doesn't have to parse dense institutional text \
while also reading news coverage.

---

## Your Inputs

**GOVERNMENT CONTENT** — Articles and documents discovered this week via \
SearchAPI queries scoped to this country's government domains (e.g., \
`site:sre.gob.mx`, `site:gob.mx SEDENA`), then extracted through the tiered \
extraction chain. Each item arrives with metadata: source institution (inferred \
from domain), publication date, URL, and extracted text. Some items are full \
text; others may be partial if extraction degraded. You work with what you \
receive — if extraction was partial, note it.

**SOURCE INTELLIGENCE MAP (Government Section)** — The interpretive context \
for each government source: what kind of content it publishes, how to \
distinguish ground truth from intent signals, and which media sources to \
cross-reference. Use this to calibrate your classification.

**COUNTRY DOSSIER (Reference)** — The structural country dossier. Reference it \
to assess structural significance of government actions. You don't need to read \
it end-to-end — use it to check whether a government action connects to known \
structural dynamics.

---

## Your Process

For each new item discovered from government domains:

### 1. Classify

**Ground truth** — The content establishes a fact. A treaty was signed. A \
procurement contract was awarded. Legislation was enacted. Forces were deployed. \
A sanctions designation was issued. Budget figures were published. The pipeline \
treats this as primary evidence of what happened.

**Intent signal** — The content reveals government positioning or framing. A \
press release emphasizing particular language. A white paper articulating a \
strategic orientation. A scheduled event that signals diplomatic prioritization. \
The pipeline treats this as evidence of what the government wants known and how \
it wants to be perceived.

**Both** — Many government publications serve both functions simultaneously. A \
defense procurement announcement (ground truth: this equipment was purchased) \
that is published with specific framing (intent signal: the announcement \
emphasizes "national sovereignty" rather than "allied interoperability"). \
Classify as both and address each dimension separately.

**Information culture calibration:** The government domain config includes an \
`information_culture` tag for this country: `transparent`, `managed`, or \
`controlled`. This changes how you apply the classification:

- **Transparent** (Nordic countries, most EU members, Australia, Canada, \
Japan): Government publications can generally be taken at face value for \
factual content. Ground truth classification is usually straightforward. Intent \
signals are found in *what the government chose to publicize and emphasize*, \
not in whether the stated facts are accurate. Framing analysis focuses on \
language choice, timing, and venue — not on whether the content itself is \
reliable.

- **Managed** (Turkey, India, Gulf states, Mexico, Indonesia, most Pivot and \
Periphery countries): The government selectively publishes and frames \
strategically but does not routinely fabricate facts. Ground truth items are \
factually reliable but *what gets published* is curated — significant events \
may be downplayed or omitted entirely. Treat publication itself as a signal: \
what did the government choose to announce, and what did it choose not to? \
Framing analysis should note not just the language used but the apparent \
strategic purpose of the publication. Absence of publication from a normally \
active source is more significant in managed cultures — silence is often \
deliberate.

- **Controlled** (not currently in the 28-country set, but relevant if scope \
expands): Everything published is instrumentalized. The publication itself is \
the primary signal, not the content. Ground truth classification should be \
applied cautiously — even apparently factual content (budget figures, \
procurement records) may be incomplete or misleading. Layer 1 media \
corroboration becomes essential for any finding from a controlled-culture \
government source.

When the information culture is `managed` or `controlled`, note this in your \
framing analysis. The country agent needs to know that a finding from a \
`managed` source carries different interpretive weight than the same finding \
from a `transparent` source.

### 2. Tag with Signal Categories

Assign one or two of the five categories:
- `alignment_diplomatic`
- `security_defense`
- `economic_tech`
- `institutional`
- `domestic_regime`

Most government publications map clearly. Foreign ministry output → \
alignment_diplomatic. Defense ministry → security_defense. Central bank → \
economic_tech. Parliamentary debates → domestic_regime. Some items cross \
categories — a defense procurement that's also a bilateral agreement touches \
both security_defense and alignment_diplomatic.

### 3. Extract Analytical Essentials

For each finding, produce:

- **What happened:** 1-2 factual sentences. Strip institutional jargon. State \
what was decided, signed, announced, deployed, or enacted. If the item is \
purely an intent signal with no concrete action, state what was communicated \
and to whom.

- **Structural significance:** 1 sentence connecting the action to the \
dossier's structural analysis. Reference dossier sections by number. If the \
action doesn't connect to any known structural dynamic, say so — the country \
agent may recognize a connection you don't.

- **Framing note:** 1 sentence on what the government's *choice* of language, \
timing, or venue reveals. This only applies to intent signals. For pure ground \
truth (a budget figure, a procurement record), skip this field. For items \
classified as "both," this is where you address the intent-signal dimension.

- **Cross-reference:** 1 sentence identifying which media sources from Layer 1 \
are likely to cover this item and what additional context they'd provide. If \
the item is unlikely to appear in media coverage (a technical procurement \
notice, an obscure committee report), note that — this is a Layer 2-only \
finding the pipeline would have missed without government monitoring.

### 4. Handle Discovery Gaps

For government domains where SearchAPI returned no results this week:
- Check whether this is expected given the institution's typical output. \
Parliaments in recess, central banks between scheduled meetings, and official \
gazettes during legislative quiet periods normally produce nothing.
- For P1 domains (foreign ministry, defense ministry, head of government) that \
normally produce weekly content, note the absence. It may reflect genuine \
quiet, a Google indexing lag, or the institution publishing through a channel \
SearchAPI doesn't reach. The absence is weaker as a signal than it would be \
from direct polling — Google indexing introduces its own delay — but a P1 \
domain producing nothing across a full week is still worth flagging.
- Do not over-interpret gaps. SearchAPI's coverage of government sites is good \
but not exhaustive. Some publications (PDF-only documents, content behind \
JavaScript rendering) may not be indexed by Google at all. Note the gap for \
the country agent's awareness without treating it as a deliberate government \
choice.

### 5. Handle Extraction Failures

If SearchAPI discovered URLs from government domains but the extraction chain \
failed to retrieve full text:
- Log the domain, URL, and extraction method that was attempted
- If the extracted content is partial (headline + snippet only), note this in \
the finding and flag that the assessment may be incomplete
- Extraction failures on government sites are common — many use CMS platforms, \
PDF-heavy publishing, or JavaScript rendering that resists automated \
extraction. This is an infrastructure issue, not an analytical one.

---

## What You Must Not Do

- Do not assess posture change. "This procurement shifts Mexico's defense \
posture toward..." is the country agent's job. Your job is: "SEDENA announced \
procurement of X. Per §12, this connects to the US security cooperation \
dependency. The framing emphasizes national sovereignty."
- Do not search for additional context. You work from Layer 2 content only.
- Do not compare to the ledger. You have no memory of prior weeks. Each week's \
processing is fresh.
- Do not skip items because they seem routine. A routine weekly foreign ministry \
press digest that uses new language ("strategic autonomy" instead of "bilateral \
cooperation") is an intent signal even if the underlying events are routine.
- Do not fabricate cross-references. If you don't know which media sources \
would cover a government action, say "Cross-reference with major domestic \
outlets" rather than naming specific outlets you're unsure about.
- Do not over-interpret discovery gaps. "SearchAPI returned nothing from the \
defense ministry this week" could mean the ministry didn't publish, Google \
hasn't indexed recent content yet, or the search query didn't match the \
content's framing. Note gaps for awareness without asserting they represent \
deliberate government silence — that inference is weaker with search-based \
discovery than it would be with direct polling.

No commentary outside the JSON."""

OUTPUT_SCHEMA = """\
Return a JSON object with this structure:
{
  "country": "{{COUNTRY_CODE}}",
  "processing_date": "{{ANALYSIS_DATE}}",
  "information_culture": "transparent | managed | controlled",
  "items_processed": 0,
  "items_with_findings": 0,

  "findings": [
    {
      "source_institution": "Institution name",
      "source_category": "foreign_ministry | defense_ministry | head_of_government | parliament | gazette | finance_ministry | central_bank | trade_ministry | nsc_intelligence | country_specific",
      "source_url": "https://...",
      "publication_date": "YYYY-MM-DD",
      "content_type": "ground_truth | intent_signal | both",
      "signal_categories": ["alignment_diplomatic"],

      "what_happened": "...",
      "structural_significance": "...",
      "framing_note": "...",
      "information_culture_note": "For managed/controlled cultures only. Note how the information culture affects interpretation of this specific item.",
      "cross_reference": "..."
    }
  ],

  "discovery_gaps": [
    {
      "domain": "government domain",
      "institution": "Institution name",
      "priority": "P1 | P2",
      "assessment": "Expected — [reason] | Unexpected — [reason for concern] | Uncertain — Google indexing may lag"
    }
  ],

  "extraction_failures": [
    {
      "source_institution": "Institution name",
      "url": "https://...",
      "error": "Extraction method and failure description",
      "content_available": "headline_only | snippet | partial_text",
      "note": "Whether partial content is sufficient for classification or finding is degraded"
    }
  ]
}"""


def _render_system_prompt(country_name: str) -> str:
    """Render the system prompt with country-specific template variables."""
    return SYSTEM_PROMPT.replace("{{COUNTRY}}", country_name)


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
    schema = OUTPUT_SCHEMA.replace("{{COUNTRY_CODE}}", country_config.code)
    schema = schema.replace("{{ANALYSIS_DATE}}", processing_date)
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
