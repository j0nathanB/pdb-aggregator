"""Tests for triage agent: prompt construction, response parsing, overrides."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    Depth,
    DynamicStatus,
    SignalCategory,
    Tier,
    Region,
    CountryConfig,
    Actor,
)
from src.monitor.agents.triage import (
    ScanResult,
    TriageDecision,
    TriageOutput,
    _build_triage_prompt,
    _is_wire_domain,
    _primary_actor_term,
    parse_triage_response,
)
from src.monitor.models import (
    ActiveDynamic,
    ActorRef,
    CountryLedger,
    EvidenceStrength,
    GlobalLedger,
    GlobalPostureSummary,
    PostureSummary,
    SignalCategoryAssessment,
    SignalEnvironment,
    TriageImplication,
)


# ---- Helpers ----

def _mexico_config() -> CountryConfig:
    from src.monitor.config import load_country_config
    return load_country_config("mx")


def _all_category_status(status=CategoryStatus.QUIET):
    return {c: status for c in SignalCategory}


def _all_category_assessments():
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }


def _test_ledger(code="mx", country="Mexico", maintenance_weeks=0) -> CountryLedger:
    return CountryLedger(
        country=country,
        code=code,
        tier="periphery",
        actors=[ActorRef(name="Test", role="Leader", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text=f"Test posture for {country}.",
            category_status=_all_category_status(),
            last_deep_dive=date(2026, 3, 7),
            consecutive_maintenance_weeks=maintenance_weeks,
        ),
        signal_categories=_all_category_assessments(),
    )


def _test_global_ledger(flagged_countries=None) -> GlobalLedger:
    dynamics = []
    if flagged_countries:
        dynamics.append(ActiveDynamic(
            dynamic_id=1,
            title="Test dynamic",
            created_week=date(2026, 3, 7),
            last_updated=date(2026, 3, 14),
            status=DynamicStatus.DEVELOPING,
            current_assessment="Test",
            countries_involved=["mx"],
            triage_implications=TriageImplication(
                countries_to_flag=flagged_countries,
                reason="Testing triage implications",
            ),
        ))
    return GlobalLedger(
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 14),
            text="Global test posture.",
            signal_environment=SignalEnvironment(),
        ),
        active_dynamics=dynamics,
    )


# ---- Wire Domain Filter ----

class TestWireDomainFilter:
    def test_matches_wire_domain(self):
        assert _is_wire_domain("reuters.com") is True
        assert _is_wire_domain("apnews.com") is True
        assert _is_wire_domain("bbc.co.uk") is True

    def test_rejects_non_wire(self):
        assert _is_wire_domain("reforma.com") is False
        assert _is_wire_domain("eluniversal.com.mx") is False

    def test_case_insensitive(self):
        assert _is_wire_domain("Reuters.com") is True
        assert _is_wire_domain("BBC.COM") is True

    def test_subdomain_match(self):
        assert _is_wire_domain("www.reuters.com") is True
        assert _is_wire_domain("news.bbc.co.uk") is True

    def test_none_and_empty(self):
        assert _is_wire_domain(None) is False
        assert _is_wire_domain("") is False


# ---- Primary Actor Term ----

class TestPrimaryActorTerm:
    def test_returns_first_search_term(self):
        config = _mexico_config()
        term = _primary_actor_term(config)
        assert "Sheinbaum" in term

    def test_fallback_to_country_name(self):
        """If no primary actor has search terms, fall back to country name."""
        from src.monitor.config import Actor, CountryConfig
        config = _mexico_config()
        # Strip search_terms from all actors
        for a in config.actors:
            a.search_terms = []
        term = _primary_actor_term(config)
        assert term == "Mexico"


# ---- Triage Prompt ----

class TestBuildTriagePrompt:
    def test_includes_scan_results(self):
        scans = [ScanResult(
            code="mx", country="Mexico",
            wire_headlines=["Sheinbaum meets US envoy — Reuters"],
            domestic_headlines=["Reforma: SEDENA expands border ops"],
            scan_summary="Active week for Mexico.",
        )]
        prompt = _build_triage_prompt(scans, {}, None)
        assert "Sheinbaum meets US envoy" in prompt
        assert "SEDENA expands border ops" in prompt

    def test_includes_posture_summary(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        ledgers = {"mx": _test_ledger()}
        prompt = _build_triage_prompt(scans, ledgers, None)
        assert "Test posture for Mexico" in prompt

    def test_includes_maintenance_weeks(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        ledgers = {"mx": _test_ledger(maintenance_weeks=3)}
        prompt = _build_triage_prompt(scans, ledgers, None)
        assert "Consecutive maintenance weeks: 3" in prompt

    def test_staleness_warning(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        ledgers = {"mx": _test_ledger(maintenance_weeks=4)}
        prompt = _build_triage_prompt(scans, ledgers, None)
        assert "STALENESS OVERRIDE" in prompt

    def test_no_ledger_message(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        prompt = _build_triage_prompt(scans, {}, None)
        assert "No ledger exists" in prompt
        assert "mandatory deep dive" in prompt

    def test_includes_global_dynamics(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        gl = _test_global_ledger(flagged_countries=["br", "tr"])
        prompt = _build_triage_prompt(scans, {}, gl)
        assert "Test dynamic" in prompt
        assert "br, tr" in prompt

    def test_empty_scan_shows_none_found(self):
        scans = [ScanResult(code="mx", country="Mexico")]
        prompt = _build_triage_prompt(scans, {}, None)
        assert "None found" in prompt

    def test_scan_error_shown(self):
        scans = [ScanResult(code="mx", country="Mexico", error="API timeout")]
        prompt = _build_triage_prompt(scans, {}, None)
        assert "API timeout" in prompt


# ---- Response Parsing ----

class TestParseTriageResponse:
    VALID_RESPONSE = json.dumps({
        "triage_date": "2026-03-14",
        "summary": {
            "deep_dive_count": 1,
            "maintenance_count": 1,
            "assessment": "Active week in Americas, quiet elsewhere.",
        },
        "decisions": [
            {
                "country": "Mexico",
                "code": "mx",
                "depth": "deep_dive",
                "rationale": "Wire coverage shows Sheinbaum-Trump confrontation.",
                "triggered_by": ["wire_coverage"],
                "signal_categories_flagged": ["alignment_diplomatic"],
            },
            {
                "country": "Estonia",
                "code": "ee",
                "depth": "maintenance",
                "rationale": "No wire mentions, no domestic activity.",
                "triggered_by": [],
            },
        ]
    })

    def test_parses_valid_response(self):
        decisions, summary = parse_triage_response(self.VALID_RESPONSE)
        assert len(decisions) == 2

    def test_parses_summary(self):
        decisions, summary = parse_triage_response(self.VALID_RESPONSE)
        assert "Active week" in summary

    def test_deep_dive_parsed(self):
        decisions, _ = parse_triage_response(self.VALID_RESPONSE)
        mx = next(d for d in decisions if d.code == "mx")
        assert mx.depth == Depth.DEEP_DIVE
        assert "wire_coverage" in mx.triggered_by
        assert "alignment_diplomatic" in mx.signal_categories_flagged

    def test_maintenance_parsed(self):
        decisions, _ = parse_triage_response(self.VALID_RESPONSE)
        ee = next(d for d in decisions if d.code == "ee")
        assert ee.depth == Depth.MAINTENANCE

    def test_strips_markdown_fencing(self):
        fenced = f"```json\n{self.VALID_RESPONSE}\n```"
        decisions, _ = parse_triage_response(fenced)
        assert len(decisions) == 2

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_triage_response("not json")

    def test_invalid_depth_falls_back_to_maintenance(self):
        bad = json.dumps({"decisions": [{
            "country": "X", "code": "xx", "depth": "invalid",
            "rationale": "test",
        }]})
        decisions, _ = parse_triage_response(bad)
        assert decisions[0].depth == Depth.MAINTENANCE

    def test_no_summary_ok(self):
        """Backward compat: responses without summary still parse."""
        data = json.dumps({"decisions": [{
            "country": "Mexico", "code": "mx", "depth": "deep_dive",
            "rationale": "test", "triggered_by": ["wire_coverage"],
        }]})
        decisions, summary = parse_triage_response(data)
        assert len(decisions) == 1
        assert summary == ""


# ---- TriageOutput ----

class TestTriageOutput:
    def test_deep_dive_countries(self):
        output = TriageOutput(
            triage_date=date(2026, 3, 14),
            decisions=[
                TriageDecision(country="Mexico", code="mx", depth=Depth.DEEP_DIVE, rationale="test"),
                TriageDecision(country="Estonia", code="ee", depth=Depth.MAINTENANCE, rationale="test"),
                TriageDecision(country="France", code="fr", depth=Depth.DEEP_DIVE, rationale="test"),
            ],
        )
        assert set(output.deep_dive_countries) == {"mx", "fr"}
        assert output.maintenance_countries == ["ee"]

    def test_scan_map_property(self):
        scans = [
            ScanResult(code="mx", country="Mexico", wire_headlines=["Reuters: Sheinbaum"]),
            ScanResult(code="ee", country="Estonia"),
        ]
        output = TriageOutput(
            triage_date=date(2026, 3, 14),
            decisions=[],
            scan_results=scans,
        )
        assert "mx" in output.scan_map
        assert "ee" in output.scan_map
        assert output.scan_map["mx"].wire_headlines == ["Reuters: Sheinbaum"]

    def test_scan_results_default_empty(self):
        output = TriageOutput(triage_date=date(2026, 3, 14), decisions=[])
        assert output.scan_results == []
        assert output.scan_map == {}


# ---- System Prompt ----

class TestTriageSystemPrompt:
    def test_contains_decision_framework(self):
        from src.monitor.agents.triage import TRIAGE_SYSTEM_PROMPT
        assert "Decision Framework" in TRIAGE_SYSTEM_PROMPT
        assert "DEEP DIVE" in TRIAGE_SYSTEM_PROMPT
        assert "MAINTENANCE" in TRIAGE_SYSTEM_PROMPT

    def test_contains_trigger_labels(self):
        from src.monitor.agents.triage import TRIAGE_SYSTEM_PROMPT
        for label in ["wire_coverage", "domestic_coverage", "category_escalation",
                       "posture_contradiction", "significant_absence",
                       "global_ledger_implication", "staleness_override"]:
            assert label in TRIAGE_SYSTEM_PROMPT

    def test_contains_calibration(self):
        from src.monitor.agents.triage import TRIAGE_SYSTEM_PROMPT
        assert "8-12 deep dives" in TRIAGE_SYSTEM_PROMPT
        assert "Calibration" in TRIAGE_SYSTEM_PROMPT

    def test_contains_judgment_calls(self):
        from src.monitor.agents.triage import TRIAGE_SYSTEM_PROMPT
        assert "Judgment Calls" in TRIAGE_SYSTEM_PROMPT


# ---- Staleness and First-Cycle Overrides ----

class TestOverrides:
    """Test the programmatic overrides applied after LLM triage decision."""

    @pytest.mark.asyncio
    async def test_staleness_override_upgrades_maintenance(self):
        """If LLM says maintenance but country has 4+ maintenance weeks, force deep dive."""
        from src.monitor.agents.triage import triage_decide
        from unittest.mock import AsyncMock, patch

        scan_results = [ScanResult(code="mx", country="Mexico")]
        ledgers = {"mx": _test_ledger(maintenance_weeks=5)}

        # Mock the API call to return maintenance decision
        mock_response_text = json.dumps({
            "decisions": [{
                "country": "Mexico", "code": "mx", "depth": "maintenance",
                "rationale": "No activity.", "triggered_by": [],
            }]
        })

        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(type="text", text=mock_response_text)]
        mock_response.usage = AsyncMock(input_tokens=100, output_tokens=50)

        with patch("src.monitor.agents.triage.anthropic.AsyncAnthropic") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client

            output = await triage_decide(scan_results, ledgers)

        mx = next(d for d in output.decisions if d.code == "mx")
        assert mx.depth == Depth.DEEP_DIVE
        assert "staleness_override" in mx.triggered_by

    @pytest.mark.asyncio
    async def test_first_cycle_forces_deep_dive(self):
        """Countries without ledgers always get deep dive."""
        from src.monitor.agents.triage import triage_decide
        from unittest.mock import AsyncMock, patch

        scan_results = [ScanResult(code="mx", country="Mexico")]
        ledgers = {}  # no ledger exists

        mock_response_text = json.dumps({
            "decisions": [{
                "country": "Mexico", "code": "mx", "depth": "maintenance",
                "rationale": "Quiet.", "triggered_by": [],
            }]
        })

        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(type="text", text=mock_response_text)]
        mock_response.usage = AsyncMock(input_tokens=100, output_tokens=50)

        with patch("src.monitor.agents.triage.anthropic.AsyncAnthropic") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client

            output = await triage_decide(scan_results, ledgers)

        mx = next(d for d in output.decisions if d.code == "mx")
        assert mx.depth == Depth.DEEP_DIVE
        assert "first_cycle" in mx.triggered_by

    @pytest.mark.asyncio
    async def test_missing_country_added_as_deep_dive(self):
        """If LLM omits a country from output, add it as deep dive (first cycle)."""
        from src.monitor.agents.triage import triage_decide
        from unittest.mock import AsyncMock, patch

        scan_results = [
            ScanResult(code="mx", country="Mexico"),
            ScanResult(code="br", country="Brazil"),
        ]
        ledgers = {}

        # LLM only returns Mexico, omits Brazil
        mock_response_text = json.dumps({
            "decisions": [{
                "country": "Mexico", "code": "mx", "depth": "deep_dive",
                "rationale": "Active.", "triggered_by": ["wire_coverage"],
            }]
        })

        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(type="text", text=mock_response_text)]
        mock_response.usage = AsyncMock(input_tokens=100, output_tokens=50)

        with patch("src.monitor.agents.triage.anthropic.AsyncAnthropic") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.messages.create = AsyncMock(return_value=mock_response)
            mock_client_cls.return_value = mock_client

            output = await triage_decide(scan_results, ledgers)

        codes = {d.code for d in output.decisions}
        assert "br" in codes
        br = next(d for d in output.decisions if d.code == "br")
        assert br.depth == Depth.DEEP_DIVE
        assert "first_cycle" in br.triggered_by
