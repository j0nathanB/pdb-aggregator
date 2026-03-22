"""Tests for the government source agent."""

from __future__ import annotations

import json
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitor.agents.government import (
    SYSTEM_PROMPT,
    DiscoveryGap,
    ExtractionFailure,
    GovernmentAgentOutput,
    GovernmentFinding,
    _build_user_message,
    _parse_response,
    _render_system_prompt,
    run_government_agent,
)
from src.monitor.config import (
    Actor,
    BlindSpot,
    BraveParams,
    CountryConfig,
    GovernmentDiscovery,
    GovernmentDomain,
    GovernmentDomainConfig,
    Languages,
    NewsDiscovery,
    Region,
    Tier,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mx_config():
    return CountryConfig(
        country="Mexico",
        code="mx",
        tier=Tier.PERIPHERY,
        region=Region.AMERICAS,
        actors=[
            Actor(name="Claudia Sheinbaum", role="President", primary=True,
                  search_terms=["Sheinbaum"]),
            Actor(name="SRE", role="Foreign Affairs Secretariat", primary=False,
                  search_terms=["SRE"]),
            Actor(name="SEDENA", role="National Defense Secretariat", primary=False,
                  search_terms=["SEDENA"]),
        ],
        languages=Languages(primary="es"),
        news_discovery=NewsDiscovery(
            goggle_file="assets/country_goggles/mx.goggle",
            brave_params=BraveParams(country="MX", search_lang="es"),
        ),
        government_discovery=GovernmentDiscovery(
            config_file="assets/government/mx.yaml",
        ),
    )


@pytest.fixture
def mx_gov_config():
    return GovernmentDomainConfig(
        country="Mexico",
        code="mx",
        information_culture="managed",
        domains=[
            GovernmentDomain(domain="gob.mx", institutions=["Presidency", "SEDENA", "SRE"], priority="P1"),
            GovernmentDomain(domain="sre.gob.mx", institutions=["Foreign Ministry"], priority="P1"),
        ],
        query_terms=["comunicado"],
    )


@pytest.fixture
def sample_extracted_content():
    return [
        {
            "url": "https://sre.gob.mx/comunicados/089",
            "domain": "sre.gob.mx",
            "title": "Comunicado No. 089",
            "text": "La Secretaría de Relaciones Exteriores informa sobre la firma del acuerdo bilateral de cooperación en seguridad con Canadá.",
            "extraction_failed": False,
        },
        {
            "url": "https://www.gob.mx/sedena/acciones/adquisicion-helicopteros",
            "domain": "gob.mx",
            "title": "SEDENA anuncia adquisición de helicópteros Black Hawk",
            "text": "La Secretaría de la Defensa Nacional informa sobre la adquisición de 12 helicópteros UH-60M Black Hawk de Lockheed Martin para operaciones contra el narcotráfico.",
            "extraction_failed": False,
        },
    ]


SAMPLE_LLM_RESPONSE = json.dumps({
    "country": "mx",
    "processing_date": "2026-03-14",
    "information_culture": "managed",
    "items_processed": 2,
    "items_with_findings": 2,
    "findings": [
        {
            "source_institution": "SRE (Foreign Ministry)",
            "source_category": "foreign_ministry",
            "source_url": "https://sre.gob.mx/comunicados/089",
            "publication_date": "2026-03-12",
            "content_type": "both",
            "signal_categories": ["alignment_diplomatic"],
            "what_happened": "SRE published the text of a revised bilateral security cooperation framework with Canada.",
            "structural_significance": "Bilateral security frameworks have historically been the mechanism through which Mexico manages US expectations about security cooperation scope.",
            "framing_note": "Press release frames this as 'deepening hemispheric security architecture' — multilateral framing, not bilateral hedge.",
            "information_culture_note": "Publication timing (mid-week, full text) suggests deliberate visibility, consistent with managed information culture where SRE controls the narrative.",
            "cross_reference": "Check Reforma and El Universal for domestic media framing.",
        },
        {
            "source_institution": "SEDENA (Defense Ministry)",
            "source_category": "defense_ministry",
            "source_url": "https://www.gob.mx/sedena/acciones/adquisicion-helicopteros",
            "publication_date": "2026-03-14",
            "content_type": "ground_truth",
            "signal_categories": ["security_defense"],
            "what_happened": "SEDENA announced procurement of 12 Black Hawk helicopters from Lockheed Martin.",
            "structural_significance": "US-origin defense procurement reinforces operational cooperation track of the dual-track US relationship.",
            "framing_note": "",
            "information_culture_note": "",
            "cross_reference": "Check whether any Layer 1 source picked this up.",
        },
    ],
    "discovery_gaps": [
        {
            "domain": "banxico.org.mx",
            "institution": "Banxico (Central Bank)",
            "priority": "P2",
            "assessment": "Expected — next scheduled decision is March 27.",
        },
    ],
    "extraction_failures": [],
})


# =============================================================================
# GovernmentAgentOutput tests
# =============================================================================


class TestGovernmentAgentOutput:
    def test_empty_output(self):
        output = GovernmentAgentOutput.empty("mx", "2026-03-14")
        assert output.country == "mx"
        assert output.information_culture == "managed"
        assert output.items_processed == 0
        assert output.findings == []
        assert output.discovery_gaps == []
        assert output.extraction_failures == []
        assert output.has_significant_findings is False

    def test_empty_output_transparent(self):
        output = GovernmentAgentOutput.empty("de", "2026-03-14", "transparent")
        assert output.information_culture == "transparent"

    def test_has_significant_findings_ground_truth(self):
        output = GovernmentAgentOutput(
            country="mx",
            processing_date="2026-03-14",
            information_culture="managed",
            items_processed=1,
            items_with_findings=1,
            findings=[
                GovernmentFinding(
                    source_institution="SRE",
                    source_category="foreign_ministry",
                    source_url="https://sre.gob.mx/test",
                    publication_date="2026-03-12",
                    content_type="ground_truth",
                    signal_categories=["alignment_diplomatic"],
                    what_happened="Treaty signed.",
                    structural_significance="Important.",
                    framing_note="",
                    information_culture_note="",
                    cross_reference="",
                ),
            ],
            discovery_gaps=[],
            extraction_failures=[],
        )
        assert output.has_significant_findings is True

    def test_has_significant_findings_intent_only(self):
        output = GovernmentAgentOutput(
            country="mx",
            processing_date="2026-03-14",
            information_culture="managed",
            items_processed=1,
            items_with_findings=1,
            findings=[
                GovernmentFinding(
                    source_institution="SRE",
                    source_category="foreign_ministry",
                    source_url="https://sre.gob.mx/test",
                    publication_date="2026-03-12",
                    content_type="intent_signal",
                    signal_categories=["alignment_diplomatic"],
                    what_happened="Press release.",
                    structural_significance="",
                    framing_note="Framing note.",
                    information_culture_note="",
                    cross_reference="",
                ),
            ],
            discovery_gaps=[],
            extraction_failures=[],
        )
        assert output.has_significant_findings is False

    def test_to_dict(self):
        output = GovernmentAgentOutput(
            country="mx",
            processing_date="2026-03-14",
            information_culture="managed",
            items_processed=2,
            items_with_findings=1,
            findings=[
                GovernmentFinding(
                    source_institution="SRE",
                    source_category="foreign_ministry",
                    source_url="https://sre.gob.mx/test",
                    publication_date="2026-03-12",
                    content_type="ground_truth",
                    signal_categories=["alignment_diplomatic"],
                    what_happened="Treaty signed.",
                    structural_significance="Important.",
                    framing_note="",
                    information_culture_note="",
                    cross_reference="Check Layer 1.",
                ),
            ],
            discovery_gaps=[
                DiscoveryGap(
                    domain="banxico.org.mx",
                    institution="Banxico",
                    priority="P2",
                    assessment="Expected — normal silence.",
                ),
            ],
            extraction_failures=[
                ExtractionFailure(
                    source_institution="DOF",
                    url="https://dof.gob.mx/nota_detalle.php?codigo=123",
                    error="Playwright timeout after 30s",
                    content_available="headline_only",
                    note="Assessment may be incomplete.",
                ),
            ],
        )

        d = output.to_dict()
        assert d["country"] == "mx"
        assert d["information_culture"] == "managed"
        assert len(d["findings"]) == 1
        assert d["findings"][0]["content_type"] == "ground_truth"
        assert d["findings"][0]["source_category"] == "foreign_ministry"
        assert len(d["discovery_gaps"]) == 1
        assert d["discovery_gaps"][0]["domain"] == "banxico.org.mx"
        assert len(d["extraction_failures"]) == 1
        assert d["extraction_failures"][0]["content_available"] == "headline_only"


# =============================================================================
# _render_system_prompt tests
# =============================================================================


class TestRenderSystemPrompt:
    def test_country_substitution(self):
        rendered = _render_system_prompt("Mexico")
        assert "content for Mexico" in rendered
        assert "{{COUNTRY}}" not in rendered

    def test_retains_analytical_constraints(self):
        rendered = _render_system_prompt("Mexico")
        assert "Do not assess posture change" in rendered
        assert "Do not search for additional context" in rendered
        assert "Do not compare to the ledger" in rendered


# =============================================================================
# _build_user_message tests
# =============================================================================


class TestBuildUserMessage:
    def test_with_content(self, mx_config, mx_gov_config, sample_extracted_content):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=sample_extracted_content,
            processing_date="2026-03-14",
            gov_domain_config=mx_gov_config,
        )

        assert "Mexico (mx)" in msg
        assert "periphery" in msg
        assert "managed" in msg
        assert "Claudia Sheinbaum" in msg
        assert "SRE" in msg
        assert "SEDENA" in msg
        assert "sre.gob.mx" in msg
        assert "Comunicado No. 089" in msg
        assert "Black Hawk" in msg

    def test_without_content(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
        )

        assert "No government content was discovered this week" in msg

    def test_with_dossier_excerpt(self, mx_config, sample_extracted_content):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=sample_extracted_content,
            processing_date="2026-03-14",
            dossier_excerpt="Mexico has a dual-track US relationship.",
        )

        assert "Dossier Context" in msg
        assert "dual-track" in msg

    def test_with_source_intel_map(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
            source_intel_map="SRE publishes comunicados weekly. Ground truth for treaties.",
        )

        assert "Source Intelligence Map" in msg
        assert "comunicados weekly" in msg

    def test_with_discovery_gaps(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
            discovery_gaps=[
                {"domain": "banxico.org.mx", "institution": "Banxico", "priority": "P2"},
            ],
        )

        assert "Discovery Gaps" in msg
        assert "banxico.org.mx" in msg

    def test_with_extraction_failures(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
            extraction_failures=[
                {"url": "https://dof.gob.mx/nota.php", "domain": "dof.gob.mx",
                 "error": "Playwright timeout", "content_available": "snippet"},
            ],
        )

        assert "Extraction Failures" in msg
        assert "dof.gob.mx" in msg
        assert "Playwright timeout" in msg

    def test_truncates_long_text(self, mx_config):
        long_content = [{
            "url": "https://example.com",
            "domain": "example.com",
            "title": "Long doc",
            "text": "A" * 5000,
            "extraction_failed": False,
        }]

        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=long_content,
            processing_date="2026-03-14",
        )

        assert "[...truncated...]" in msg

    def test_extraction_failed_shows_snippet(self, mx_config):
        content = [{
            "url": "https://example.com",
            "domain": "example.com",
            "title": "Failed extraction",
            "text": "",
            "snippet": "Brief summary from search",
            "extraction_failed": True,
        }]

        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=content,
            processing_date="2026-03-14",
        )

        assert "Extraction failed" in msg
        assert "Brief summary from search" in msg

    def test_includes_output_schema(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
        )
        assert "content_type" in msg
        assert "signal_categories" in msg
        assert "source_category" in msg
        assert "information_culture_note" in msg
        assert "discovery_gaps" in msg

    def test_schema_has_country_code_filled(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
        )
        assert '"mx"' in msg
        assert '"2026-03-14"' in msg
        assert "{{COUNTRY_CODE}}" not in msg
        assert "{{ANALYSIS_DATE}}" not in msg

    def test_information_culture_transparent(self, mx_config):
        msg = _build_user_message(
            country_config=mx_config,
            extracted_content=[],
            processing_date="2026-03-14",
            information_culture="transparent",
        )
        assert "Information culture: transparent" in msg


# =============================================================================
# _parse_response tests
# =============================================================================


class TestParseResponse:
    def test_parse_raw_json(self):
        result = _parse_response(SAMPLE_LLM_RESPONSE)
        assert len(result["findings"]) == 2
        assert result["findings"][0]["source_institution"] == "SRE (Foreign Ministry)"
        assert result["findings"][0]["source_category"] == "foreign_ministry"

    def test_parse_markdown_code_block(self):
        wrapped = f"Here is the analysis:\n```json\n{SAMPLE_LLM_RESPONSE}\n```"
        result = _parse_response(wrapped)
        assert len(result["findings"]) == 2

    def test_parse_invalid_json(self):
        result = _parse_response("This is not JSON at all.")
        assert result["findings"] == []
        assert result["discovery_gaps"] == []
        assert result["extraction_failures"] == []

    def test_parse_empty_response(self):
        result = _parse_response('{"findings": [], "discovery_gaps": [], "extraction_failures": []}')
        assert result["findings"] == []


# =============================================================================
# run_government_agent tests
# =============================================================================


class TestRunGovernmentAgent:
    @pytest.mark.asyncio
    async def test_empty_input_returns_empty(self, mx_config):
        """No content, no gaps, no failures → empty output without API call."""
        output = await run_government_agent(
            country_config=mx_config,
            extracted_content=[],
            processing_date=date(2026, 3, 14),
        )

        assert output.country == "mx"
        assert output.information_culture == "managed"
        assert output.items_processed == 0
        assert output.findings == []

    @pytest.mark.asyncio
    async def test_successful_processing(self, mx_config, sample_extracted_content):
        """Mock the Anthropic API and verify output parsing."""
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(type="text", text=SAMPLE_LLM_RESPONSE),
        ]

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.monitor.agents.government.anthropic.AsyncAnthropic", return_value=mock_client):
            output = await run_government_agent(
                country_config=mx_config,
                extracted_content=sample_extracted_content,
                processing_date=date(2026, 3, 14),
                information_culture="managed",
            )

        assert output.country == "mx"
        assert output.information_culture == "managed"
        assert output.items_processed == 2
        assert output.items_with_findings == 2
        assert len(output.findings) == 2
        assert output.findings[0].source_institution == "SRE (Foreign Ministry)"
        assert output.findings[0].source_category == "foreign_ministry"
        assert output.findings[0].content_type == "both"
        assert "alignment_diplomatic" in output.findings[0].signal_categories
        assert output.findings[0].information_culture_note != ""
        assert output.findings[1].content_type == "ground_truth"
        assert len(output.discovery_gaps) == 1
        assert output.discovery_gaps[0].institution == "Banxico (Central Bank)"
        assert output.has_significant_findings is True

    @pytest.mark.asyncio
    async def test_system_prompt_rendered_with_country(self, mx_config, sample_extracted_content):
        """Verify the system prompt is rendered with the country name."""
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(type="text", text=SAMPLE_LLM_RESPONSE),
        ]

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.monitor.agents.government.anthropic.AsyncAnthropic", return_value=mock_client):
            await run_government_agent(
                country_config=mx_config,
                extracted_content=sample_extracted_content,
                processing_date=date(2026, 3, 14),
            )

        # Check the system prompt was rendered with "Mexico"
        call_kwargs = mock_client.messages.create.call_args[1]
        assert "Mexico" in call_kwargs["system"]
        assert "{{COUNTRY}}" not in call_kwargs["system"]

    @pytest.mark.asyncio
    async def test_api_failure_returns_graceful_output(self, mx_config, sample_extracted_content):
        """API failure should not crash — returns empty output with failure logged."""
        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(
            side_effect=Exception("API rate limit exceeded")
        )

        with patch("src.monitor.agents.government.anthropic.AsyncAnthropic", return_value=mock_client):
            output = await run_government_agent(
                country_config=mx_config,
                extracted_content=sample_extracted_content,
                processing_date=date(2026, 3, 14),
            )

        assert output.country == "mx"
        assert output.findings == []
        assert len(output.extraction_failures) >= 1
        assert any(
            f.source_institution == "government_agent"
            for f in output.extraction_failures
        )

    @pytest.mark.asyncio
    async def test_discovery_gaps_trigger_agent(self, mx_config):
        """Discovery gaps alone (no content) should still trigger the agent."""
        gaps = [
            {"domain": "sre.gob.mx", "institution": "SRE", "priority": "P1"},
        ]

        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(type="text", text=json.dumps({
                "country": "mx",
                "processing_date": "2026-03-14",
                "information_culture": "managed",
                "items_processed": 0,
                "items_with_findings": 0,
                "findings": [],
                "discovery_gaps": [
                    {"domain": "sre.gob.mx", "institution": "SRE",
                     "priority": "P1", "assessment": "Unexpected — SRE normally publishes weekly."},
                ],
                "extraction_failures": [],
            })),
        ]

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.monitor.agents.government.anthropic.AsyncAnthropic", return_value=mock_client):
            output = await run_government_agent(
                country_config=mx_config,
                extracted_content=[],
                processing_date=date(2026, 3, 14),
                discovery_gaps=gaps,
            )

        # Agent was called (not short-circuited to empty)
        assert mock_client.messages.create.called
        assert len(output.discovery_gaps) == 1
        assert output.discovery_gaps[0].priority == "P1"

    @pytest.mark.asyncio
    async def test_extraction_failures_passed_through(self, mx_config):
        """Extraction failures from Layer 2 should appear in user message."""
        ext_failures = [
            {"url": "https://dof.gob.mx/nota.php", "domain": "dof.gob.mx",
             "error": "Playwright timeout", "content_available": "snippet"},
        ]

        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(type="text", text=json.dumps({
                "country": "mx",
                "processing_date": "2026-03-14",
                "information_culture": "managed",
                "items_processed": 0,
                "items_with_findings": 0,
                "findings": [],
                "discovery_gaps": [],
                "extraction_failures": [
                    {"source_institution": "DOF", "url": "https://dof.gob.mx/nota.php",
                     "error": "Playwright timeout", "content_available": "snippet",
                     "note": "Snippet may be sufficient for classification."},
                ],
            })),
        ]

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.monitor.agents.government.anthropic.AsyncAnthropic", return_value=mock_client):
            output = await run_government_agent(
                country_config=mx_config,
                extracted_content=[],
                processing_date=date(2026, 3, 14),
                extraction_failures=ext_failures,
            )

        assert len(output.extraction_failures) == 1
        assert output.extraction_failures[0].source_institution == "DOF"

    @pytest.mark.asyncio
    async def test_system_prompt_contents(self):
        """Verify key constraints are in the system prompt."""
        assert "ground truth" in SYSTEM_PROMPT.lower()
        assert "intent signal" in SYSTEM_PROMPT.lower()
        assert "Do not assess posture change" in SYSTEM_PROMPT
        assert "Do not search for additional context" in SYSTEM_PROMPT
        assert "Do not compare to the ledger" in SYSTEM_PROMPT
        assert "alignment_diplomatic" in SYSTEM_PROMPT
        assert "security_defense" in SYSTEM_PROMPT
        assert "information_culture" in SYSTEM_PROMPT.lower()
        assert "transparent" in SYSTEM_PROMPT
        assert "managed" in SYSTEM_PROMPT
        assert "controlled" in SYSTEM_PROMPT
        assert "{{COUNTRY}}" in SYSTEM_PROMPT
