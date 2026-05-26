"""Tests for the desk pipeline orchestrator: ledger application and pipeline wiring."""

from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    Movement,
    SignalCategory,
)
from src.monitor.models import (
    AbsenceCheck,
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CorrectionLogEntry,
    CountryLedger,
    DevilsAdvocate,
    Development,
    PostureSummary,
    SelfCorrection,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    StructuralClaimStatus,
    WeeklyEntry,
)
from src.monitor.agents.country import CountryAgentOutput
from src.monitor.config import (
    Actor,
    BraveParams,
    CountryConfig,
    GovernmentDiscovery,
    GovernmentDomain,
    GovernmentDomainConfig,
    Languages,
    NewsDiscovery,
    QueryVocabulary,
)
from src.monitor.orchestrator import (
    CountryResult,
    DeskPipelineResult,
    Layer2Result,
    _collect_layer2_inputs,
    apply_to_ledger,
    assemble_country_domains,
)


# ---- Helpers ----

def _all_category_status(status=CategoryStatus.QUIET):
    return {c: status for c in SignalCategory}


def _all_category_assessments(d=date(2026, 3, 14)):
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            last_updated=d,
        )
        for c in SignalCategory
    }


def _all_category_movements(movement=Movement.NONE):
    return {c: CategoryMovement(movement=movement) for c in SignalCategory}


def _test_ledger(**overrides) -> CountryLedger:
    defaults = dict(
        country="Mexico",
        code="mx",
        tier="periphery",
        actors=[ActorRef(name="Sheinbaum", role="President", primary=True)],
        last_updated=date(2026, 3, 7),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 7),
            text="Test posture.",
            category_status=_all_category_status(),
            last_deep_dive=date(2026, 3, 7),
            consecutive_maintenance_weeks=0,
        ),
        signal_categories=_all_category_assessments(date(2026, 3, 7)),
        structural_claim_status=[
            StructuralClaimStatus(
                claim_ref="STRUC-05",
                claim_text="Border constraint.",
                dossier_section=2,
                status=ClaimStatus.CONFIRMED,
                last_checked=date(2026, 3, 7),
            ),
        ],
    )
    defaults.update(overrides)
    return CountryLedger(**defaults)


def _deep_dive_entry() -> WeeklyEntry:
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "test"},
        category_movements=_all_category_movements(),
        devils_advocate=DevilsAdvocate(
            challenges=["Challenge 1"],
            recommended_adjustments=["Adjust 1"],
        ),
        structural_claim_checks=[
            StructuralClaimCheck(
                claim_ref="STRUC-05",
                claim_text="Border constraint.",
                status="under_pressure",
                evidence="Tariff threats.",
                confidence_in_claim=3,
            ),
        ],
        self_corrections=[
            SelfCorrection(
                category=SignalCategory.DOMESTIC_REGIME,
                prior_week=date(2026, 3, 7),
                original_claim="Stable supermajority.",
                correction="Internal strain detected.",
                root_cause="New polling data.",
            ),
        ],
    )


def _deep_dive_output() -> CountryAgentOutput:
    return CountryAgentOutput(
        weekly_entry=_deep_dive_entry(),
        signal_categories={
            c: SignalCategoryAssessment(
                current_assessment=f"Updated for {c.value}",
                confidence=4,
                last_updated=date(2026, 3, 14),
            )
            for c in SignalCategory
        },
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Updated posture after deep dive.",
            category_status=_all_category_status(CategoryStatus.ACTIVE),
            last_deep_dive=date(2026, 3, 14),
            consecutive_maintenance_weeks=0,
        ),
    )


def _maintenance_entry() -> WeeklyEntry:
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.MAINTENANCE,
    )


# ---- apply_to_ledger ----

class TestApplyDeepDive:
    def test_appends_weekly_entry(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        assert len(updated.weekly_entries) == 1
        assert updated.weekly_entries[0].depth == Depth.DEEP_DIVE

    def test_updates_signal_categories(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        for cat in SignalCategory:
            assert updated.signal_categories[cat].confidence == 4
            assert "Updated" in updated.signal_categories[cat].current_assessment

    def test_updates_posture_summary(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        assert "Updated posture" in updated.posture_summary.text
        assert updated.posture_summary.consecutive_maintenance_weeks == 0

    def test_updates_structural_claim_status(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        claim = updated.structural_claim_status[0]
        assert claim.status == ClaimStatus.UNDER_PRESSURE
        assert claim.weeks_under_pressure == 1
        assert claim.last_checked == date(2026, 3, 14)

    def test_logs_self_corrections(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        assert len(updated.corrections_log) == 1
        assert updated.corrections_log[0].category_affected == SignalCategory.DOMESTIC_REGIME
        assert updated.corrections_log[0].root_cause == "New polling data."

    def test_updates_last_updated(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=_deep_dive_entry(), output=_deep_dive_output(),
        )
        updated = apply_to_ledger(ledger, result)
        assert updated.last_updated == date(2026, 3, 14)

    def test_confirmed_claim_resets_pressure_counter(self):
        ledger = _test_ledger()
        ledger.structural_claim_status[0].weeks_under_pressure = 3
        entry = _deep_dive_entry()
        entry.structural_claim_checks[0] = StructuralClaimCheck(
            claim_ref="STRUC-05",
            claim_text="Border constraint.",
            status="confirmed",
            evidence="Confirmed.",
            confidence_in_claim=4,
        )
        output = _deep_dive_output()
        output.weekly_entry = entry
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=True, weekly_entry=entry, output=output,
        )
        updated = apply_to_ledger(ledger, result)
        assert updated.structural_claim_status[0].weeks_under_pressure == 0


class TestApplyMaintenance:
    def test_appends_maintenance_entry(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.MAINTENANCE,
            success=True, weekly_entry=_maintenance_entry(),
        )
        updated = apply_to_ledger(ledger, result)
        assert len(updated.weekly_entries) == 1
        assert updated.weekly_entries[0].depth == Depth.MAINTENANCE

    def test_increments_maintenance_counter(self):
        ledger = _test_ledger()
        ledger.posture_summary.consecutive_maintenance_weeks = 2
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.MAINTENANCE,
            success=True, weekly_entry=_maintenance_entry(),
        )
        updated = apply_to_ledger(ledger, result)
        assert updated.posture_summary.consecutive_maintenance_weeks == 3

    def test_does_not_change_signal_categories(self):
        ledger = _test_ledger()
        original_assessments = {
            c: a.current_assessment for c, a in ledger.signal_categories.items()
        }
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.MAINTENANCE,
            success=True, weekly_entry=_maintenance_entry(),
        )
        updated = apply_to_ledger(ledger, result)
        for cat in SignalCategory:
            assert updated.signal_categories[cat].current_assessment == original_assessments[cat]


class TestApplyFailure:
    def test_failed_result_leaves_ledger_unchanged(self):
        ledger = _test_ledger()
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.DEEP_DIVE,
            success=False, error="API timeout",
        )
        updated = apply_to_ledger(ledger, result)
        assert len(updated.weekly_entries) == 0
        assert updated.last_updated == date(2026, 3, 7)  # unchanged


class TestApplyArchival:
    def test_triggers_archival_when_over_limit(self):
        ledger = _test_ledger(
            weekly_entries=[
                WeeklyEntry(
                    week=date(2026, 1, i + 1),
                    date_range=f"w{i}",
                    depth=Depth.MAINTENANCE,
                )
                for i in range(8)
            ]
        )
        result = CountryResult(
            code="mx", country="Mexico", depth=Depth.MAINTENANCE,
            success=True, weekly_entry=_maintenance_entry(),
        )
        # Redirect archive dir to tmp
        import src.monitor.ledger.storage as storage
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            original_archive = storage.LEDGER_ARCHIVE_DIR
            storage.LEDGER_ARCHIVE_DIR = Path(tmp)
            try:
                updated = apply_to_ledger(ledger, result)
                # 9 entries total, archive should trim to 8
                assert len(updated.weekly_entries) == 8
            finally:
                storage.LEDGER_ARCHIVE_DIR = original_archive


# ---- DeskPipelineResult ----

class TestDeskPipelineResult:
    def test_deep_dive_results(self):
        result = DeskPipelineResult(
            country_results=[
                CountryResult(code="mx", country="Mexico", depth=Depth.DEEP_DIVE, success=True),
                CountryResult(code="ee", country="Estonia", depth=Depth.MAINTENANCE, success=True),
                CountryResult(code="fr", country="France", depth=Depth.DEEP_DIVE, success=False, error="fail"),
            ]
        )
        assert len(result.deep_dive_results) == 1
        assert result.deep_dive_results[0].code == "mx"

    def test_maintenance_results(self):
        result = DeskPipelineResult(
            country_results=[
                CountryResult(code="mx", country="Mexico", depth=Depth.DEEP_DIVE, success=True),
                CountryResult(code="ee", country="Estonia", depth=Depth.MAINTENANCE, success=True),
            ]
        )
        assert len(result.maintenance_results) == 1
        assert result.maintenance_results[0].code == "ee"

    def test_failed_results(self):
        result = DeskPipelineResult(
            country_results=[
                CountryResult(code="fr", country="France", depth=Depth.DEEP_DIVE, success=False, error="fail"),
            ]
        )
        assert len(result.failed_results) == 1

    def test_layer2_results_default_empty(self):
        result = DeskPipelineResult()
        assert result.layer2_results == {}


# ---- Layer2Result ----

class TestLayer2Result:
    def test_default_fields(self):
        lr = Layer2Result(code="mx")
        assert lr.code == "mx"
        assert lr.search_responses == []
        assert lr.extraction_results == []
        assert lr.gov_output is None
        assert lr.error is None

    def test_with_error(self):
        lr = Layer2Result(code="mx", error="API key missing")
        assert lr.error == "API key missing"


# ---- Domain Assembly ----

def _test_country_config() -> CountryConfig:
    return CountryConfig(
        country="Mexico",
        code="mx",
        tier="periphery",
        region="americas",
        actors=[Actor(name="Sheinbaum", role="President", primary=True)],
        languages=Languages(primary="es"),
        news_discovery=NewsDiscovery(
            goggle_file="assets/country_goggles/mx.goggle",
            brave_params=BraveParams(country="MX", search_lang="es"),
        ),
        government_discovery=GovernmentDiscovery(
            config_file="assets/government/mx.yaml",
        ),
    )


def _test_gov_config() -> GovernmentDomainConfig:
    return GovernmentDomainConfig(
        country="Mexico",
        code="mx",
        information_culture="managed",
        domains=[
            GovernmentDomain(
                domain="gob.mx",
                institutions=["Presidency", "SEDENA"],
                priority="P1",
            ),
            GovernmentDomain(
                domain="sre.gob.mx",
                institutions=["Foreign Ministry"],
                priority="P1",
            ),
            GovernmentDomain(
                domain="banxico.org.mx",
                institutions=["Central Bank"],
                priority="P2",
            ),
        ],
        query_terms=["comunicado", "decreto"],
    )


class TestAssembleCountryDomains:
    def test_gov_domains_included(self):
        config = _test_country_config()
        gov_config = _test_gov_config()
        result = assemble_country_domains(config, gov_config=gov_config)
        assert "gob.mx" in result["gov_domains"]
        assert "sre.gob.mx" in result["gov_domains"]
        assert "banxico.org.mx" in result["gov_domains"]

    def test_gov_domains_in_allowed_domains(self):
        config = _test_country_config()
        gov_config = _test_gov_config()
        result = assemble_country_domains(config, gov_config=gov_config)
        for gd in result["gov_domains"]:
            assert gd in result["allowed_domains"]

    def test_wire_domains_default(self):
        config = _test_country_config()
        result = assemble_country_domains(config)
        assert "reuters.com" in result["wire_domains"]
        assert "apnews.com" in result["wire_domains"]

    def test_wire_domains_in_allowed_domains(self):
        config = _test_country_config()
        result = assemble_country_domains(config)
        for wd in result["wire_domains"]:
            assert wd in result["allowed_domains"]

    def test_no_gov_config_empty_gov_domains(self):
        config = _test_country_config()
        result = assemble_country_domains(config)
        assert result["gov_domains"] == []

    def test_no_brave_client_empty_triage_domains(self):
        config = _test_country_config()
        result = assemble_country_domains(config)
        assert result["triage_domains"] == []

    def test_no_duplicates_in_allowed_domains(self):
        config = _test_country_config()
        gov_config = _test_gov_config()
        result = assemble_country_domains(config, gov_config=gov_config)
        assert len(result["allowed_domains"]) == len(set(result["allowed_domains"]))


class TestCollectLayer2Inputs:
    @pytest.mark.asyncio
    async def test_extract_batch_uses_gov_per_domain_limit(self):
        """Gov Layer 2 must call extract_batch with max_per_domain=20 (not the
        news default of 5). Without this, official press-release feeds get
        silently truncated — see orchestrator.py:_collect_layer2_inputs."""
        from unittest.mock import AsyncMock, MagicMock

        from src.monitor.collection.searchapi import (
            SearchAPIResponse,
            SearchResult,
        )

        config = _test_country_config()
        gov_config = _test_gov_config()

        urls = [f"https://gob.mx/news/{i}" for i in range(10)]
        search_resp = SearchAPIResponse(
            query="site:gob.mx",
            results=[
                SearchResult(
                    title=f"item {i}", url=u, snippet="", domain="gob.mx"
                )
                for i, u in enumerate(urls)
            ],
        )
        searchapi_client = MagicMock()
        searchapi_client.search_country_government = AsyncMock(
            return_value=[search_resp]
        )

        extractor = MagicMock()
        extractor.extract_batch = AsyncMock(return_value=[])

        await _collect_layer2_inputs(
            config=config,
            gov_config=gov_config,
            searchapi_client=searchapi_client,
            extractor=extractor,
            processing_date=date(2026, 5, 24),
        )

        extractor.extract_batch.assert_awaited_once()
        _, kwargs = extractor.extract_batch.call_args
        assert kwargs.get("max_per_domain") == 20, (
            f"Gov Layer 2 should pass max_per_domain=20 to override the news "
            f"default of 5; got {kwargs!r}"
        )
