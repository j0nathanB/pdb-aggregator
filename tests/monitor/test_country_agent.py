"""Tests for the country agent: prompt construction and response parsing."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    Movement,
    SignalCategory,
    load_country_config,
)
from src.monitor.agents.country import (
    CountryAgentOutput,
    _build_country_prompt,
    _build_ledger_context,
    _build_system_prompt,
    parse_country_response,
)
from src.monitor.models import (
    ActorRef,
    CategoryMovement,
    CountryLedger,
    DevilsAdvocate,
    PostureSummary,
    SignalCategoryAssessment,
    StructuralClaimStatus,
    WeeklyEntry,
)


# ---- Helpers ----

def _all_category_status(status=CategoryStatus.QUIET):
    return {c: status for c in SignalCategory}


def _all_category_assessments():
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            confidence_rationale="Baseline from dossier.",
            key_actors=["Sheinbaum"],
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }


def _test_ledger(**overrides) -> CountryLedger:
    defaults = dict(
        country="Mexico",
        code="mx",
        tier="periphery",
        actors=[ActorRef(name="Sheinbaum", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Mexico navigates US proximity under Sheinbaum.",
            category_status=_all_category_status(),
            last_deep_dive=date(2026, 3, 7),
            consecutive_maintenance_weeks=0,
        ),
        signal_categories=_all_category_assessments(),
        structural_claim_status=[
            StructuralClaimStatus(
                claim_ref="STRUC-01",
                claim_text="Mexico's foundational geopolitical trauma.",
                dossier_section=1,
                status=ClaimStatus.CONFIRMED,
                last_checked=date(2026, 3, 7),
            ),
            StructuralClaimStatus(
                claim_ref="STRUC-05",
                claim_text="US-Mexico border is a hard constraint.",
                dossier_section=2,
                status=ClaimStatus.UNDER_PRESSURE,
                last_checked=date(2026, 3, 7),
                evidence_summary="Tariff escalation testing this.",
            ),
        ],
    )
    defaults.update(overrides)
    return CountryLedger(**defaults)


def _valid_agent_response() -> dict:
    """A complete valid response matching the country agent output schema."""
    cat_movement = {
        "movement": "none",
        "developments": [],
        "prior_assessment": "No change.",
        "updated_assessment": "No change.",
        "confidence_change": None,
    }
    return {
        "weekly_entry": {
            "activity_level": {"rating": "moderate", "rationale": "Some wire coverage."},
            "category_movements": {
                "alignment_diplomatic": {
                    "movement": "significant",
                    "developments": [
                        {
                            "headline": "Sheinbaum rejects US military proposal",
                            "date": "2026-03-12",
                            "source": "Reuters",
                            "source_tier": 2,
                            "source_url": "https://reuters.com/example",
                            "summary": "Sheinbaum rejected proposal for US military ops on Mexican soil.",
                            "actors_involved": ["Sheinbaum", "SRE"],
                            "signal_category_relevance": "Direct challenge to US bilateral relationship.",
                        }
                    ],
                    "prior_assessment": "Defensive posture toward US.",
                    "updated_assessment": "Active confrontation with US on sovereignty issues.",
                    "confidence_change": {"from": 3, "to": 4, "reason": "Multiple wire sources confirm."},
                },
                "security_defense": cat_movement.copy(),
                "economic_tech": cat_movement.copy(),
                "institutional": cat_movement.copy(),
                "domestic_regime": cat_movement.copy(),
            },
            "unexpected_developments": [
                {
                    "headline": "CJNG successor named",
                    "date": "2026-03-11",
                    "source": "Proceso",
                    "source_tier": 3,
                    "signal_category": "security_defense",
                    "assessment": "Could reshape cartel dynamics.",
                    "disposition": "logged",
                }
            ],
            "absence_check": [
                {
                    "expected": "USMCA review statement",
                    "signal_category": "economic_tech",
                    "occurred": False,
                    "significance": "Silence may indicate behind-the-scenes negotiations.",
                    "confidence": 2,
                }
            ],
            "self_corrections": [],
            "structural_claim_checks": [
                {
                    "claim_ref": "STRUC-05",
                    "claim_text": "US-Mexico border is a hard constraint.",
                    "status": "confirmed",
                    "evidence": "Tariff threats reinforce dependency.",
                    "confidence_in_claim": 4,
                }
            ],
        },
        "updated_posture_summary": {
            "as_of": "2026-03-14",
            "text": "Mexico actively confronting US on sovereignty. Sheinbaum escalating rhetoric. Economic dependency unchanged.",
            "category_status": {
                "alignment_diplomatic": "escalating",
                "security_defense": "active",
                "economic_tech": "routine",
                "institutional": "quiet",
                "domestic_regime": "routine",
            },
            "last_deep_dive": "2026-03-14",
            "consecutive_maintenance_weeks": 0,
        },
        "updated_signal_categories": {
            "alignment_diplomatic": {
                "current_assessment": "Active confrontation with US. Sovereignty rhetoric escalating.",
                "confidence": 4,
                "confidence_rationale": "Multiple wire sources confirm rejection.",
                "key_actors": ["Sheinbaum", "SRE", "de la Fuente"],
                "dossier_sections_referenced": ["§14", "§17"],
                "last_updated": "2026-03-14",
            },
            "security_defense": {
                "current_assessment": "CJNG succession uncertainty. Monitoring.",
                "confidence": 3,
                "confidence_rationale": "Single Tier 3 source.",
                "key_actors": ["SEDENA", "García Harfuch"],
                "dossier_sections_referenced": ["§12"],
                "last_updated": "2026-03-14",
            },
            "economic_tech": {
                "current_assessment": "USMCA dependency stable. No new developments.",
                "confidence": 3,
                "confidence_rationale": "Absence of expected statement noted.",
                "key_actors": ["Banxico"],
                "dossier_sections_referenced": ["§6"],
                "last_updated": "2026-03-14",
            },
            "institutional": {
                "current_assessment": "No significant institutional engagement changes.",
                "confidence": 3,
                "confidence_rationale": "Baseline unchanged.",
                "key_actors": [],
                "dossier_sections_referenced": ["§11"],
                "last_updated": "2026-03-14",
            },
            "domestic_regime": {
                "current_assessment": "Morena supermajority stable. No election-related shifts.",
                "confidence": 3,
                "confidence_rationale": "Baseline unchanged.",
                "key_actors": ["Morena"],
                "dossier_sections_referenced": ["§6", "§13"],
                "last_updated": "2026-03-14",
            },
        },
    }


# ---- Ledger Context ----

class TestBuildLedgerContext:
    def test_includes_posture_summary(self):
        context = _build_ledger_context(_test_ledger())
        assert "Mexico navigates US proximity" in context

    def test_includes_category_assessments(self):
        context = _build_ledger_context(_test_ledger())
        assert "alignment_diplomatic" in context
        assert "Baseline for" in context

    def test_includes_structural_claims(self):
        context = _build_ledger_context(_test_ledger())
        assert "STRUC-01" in context
        assert "STRUC-05" in context

    def test_shows_claims_under_pressure_first(self):
        context = _build_ledger_context(_test_ledger())
        struc05_pos = context.find("STRUC-05")
        struc01_pos = context.find("STRUC-01")
        # Under pressure claims should appear before confirmed
        assert struc05_pos < struc01_pos

    def test_includes_recent_entries(self):
        entries = [
            WeeklyEntry(
                week=date(2026, 3, 7),
                date_range="w1",
                depth=Depth.DEEP_DIVE,
                activity_level={"rating": "high", "rationale": "test"},
                category_movements={
                    c: CategoryMovement(movement=Movement.NONE)
                    for c in SignalCategory
                },
                devils_advocate=DevilsAdvocate(challenges=["c1"]),
            )
        ]
        ledger = _test_ledger(weekly_entries=entries)
        context = _build_ledger_context(ledger)
        assert "Week of 2026-03-07" in context

    def test_caps_entries(self):
        entries = [
            WeeklyEntry(week=date(2026, 1, i + 1), date_range=f"w{i}", depth=Depth.MAINTENANCE)
            for i in range(10)
        ]
        ledger = _test_ledger(weekly_entries=entries)
        context = _build_ledger_context(ledger, max_entries=4)
        # Should only show last 4
        assert "2026-01-10" in context
        assert "2026-01-01" not in context

    def test_empty_ledger(self):
        context = _build_ledger_context(_test_ledger())
        # Should still produce valid output
        assert "CURRENT POSTURE SUMMARY" in context


# ---- Country Prompt ----

class TestBuildCountryPrompt:
    def test_includes_country_info(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier text", date(2026, 3, 14))
        assert "Mexico" in prompt
        assert "MX" in prompt
        assert "periphery" in prompt

    def test_includes_date_range(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14))
        assert "2026-03-07" in prompt
        assert "2026-03-14" in prompt

    def test_includes_actors_with_search_terms(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14))
        assert "Sheinbaum" in prompt
        assert "SEDENA" in prompt
        assert "(PRIMARY)" in prompt

    def test_includes_all_source_types(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        domains = ["eluniversal.com.mx", "gob.mx", "reuters.com"]
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14),
                                       allowed_domains=domains)
        assert "eluniversal.com.mx" in prompt
        assert "gob.mx" in prompt
        assert "reuters.com" in prompt

    def test_includes_blind_spots(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14))
        assert "Defense procurement" in prompt
        assert "blind spot" in prompt.lower() or "blind_spot" in prompt.lower() or "Blind" in prompt

    def test_includes_language_note(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14))
        assert "es" in prompt  # Spanish

    def test_includes_dossier(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Full dossier content here", date(2026, 3, 14))
        assert "Full dossier content here" in prompt

    def test_includes_ledger_context(self):
        config = load_country_config("mx")
        ledger = _test_ledger()
        prompt = _build_country_prompt(config, ledger, "# Dossier", date(2026, 3, 14))
        assert "CURRENT POSTURE SUMMARY" in prompt
        assert "Mexico navigates US proximity" in prompt


# ---- Response Parsing ----

class TestParseCountryResponse:
    def test_parses_valid_response(self):
        response = json.dumps(_valid_agent_response())
        ledger = _test_ledger()
        output = parse_country_response(response, date(2026, 3, 14), "2026-03-07 to 2026-03-14", ledger)
        assert isinstance(output, CountryAgentOutput)

    def test_weekly_entry_is_deep_dive(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert output.weekly_entry.depth == Depth.DEEP_DIVE

    def test_weekly_entry_has_all_categories(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert set(output.weekly_entry.category_movements.keys()) == set(SignalCategory)

    def test_significant_movement_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        ad = output.weekly_entry.category_movements[SignalCategory.ALIGNMENT_DIPLOMATIC]
        assert ad.movement == Movement.SIGNIFICANT
        assert len(ad.developments) == 1
        assert "Sheinbaum" in ad.developments[0].headline

    def test_confidence_change_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        ad = output.weekly_entry.category_movements[SignalCategory.ALIGNMENT_DIPLOMATIC]
        assert ad.confidence_change is not None
        assert ad.confidence_change.from_ == 3
        assert ad.confidence_change.to == 4

    def test_unexpected_developments_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert len(output.weekly_entry.unexpected_developments) == 1
        assert "CJNG" in output.weekly_entry.unexpected_developments[0].headline

    def test_absence_check_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert len(output.weekly_entry.absence_check) == 1
        assert output.weekly_entry.absence_check[0].occurred is False

    def test_structural_claim_checks_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert len(output.weekly_entry.structural_claim_checks) == 1
        assert output.weekly_entry.structural_claim_checks[0].claim_ref == "STRUC-05"

    def test_devils_advocate_is_none(self):
        """Country agent doesn't produce devils_advocate — that's a separate call."""
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert output.weekly_entry.devils_advocate is None

    def test_updated_posture_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert "confronting US" in output.posture_summary.text
        assert output.posture_summary.category_status[SignalCategory.ALIGNMENT_DIPLOMATIC] == CategoryStatus.ESCALATING
        assert output.posture_summary.consecutive_maintenance_weeks == 0
        assert output.posture_summary.last_deep_dive == date(2026, 3, 14)

    def test_updated_assessments_parsed(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert set(output.signal_categories.keys()) == set(SignalCategory)
        ad = output.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC]
        assert ad.confidence == 4
        assert "confrontation" in ad.current_assessment.lower()
        assert "Sheinbaum" in ad.key_actors

    def test_strips_markdown_fencing(self):
        response = f"```json\n{json.dumps(_valid_agent_response())}\n```"
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert isinstance(output, CountryAgentOutput)

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_country_response("not json", date(2026, 3, 14), "w1", _test_ledger())

    def test_missing_category_defaults_to_none(self):
        data = _valid_agent_response()
        del data["weekly_entry"]["category_movements"]["domestic_regime"]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        from src.monitor.config import Movement, SignalCategory
        assert output.weekly_entry.category_movements[SignalCategory.DOMESTIC_REGIME].movement == Movement.NONE

    def test_last_updated_parsed_from_response(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        ad = output.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC]
        assert ad.last_updated == date(2026, 3, 14)

    def test_posture_as_of_from_response(self):
        response = json.dumps(_valid_agent_response())
        output = parse_country_response(response, date(2026, 3, 14), "w1", _test_ledger())
        assert output.posture_summary.as_of == date(2026, 3, 14)


# ---- System Prompt ----

class TestBuildSystemPrompt:
    def test_substitutes_country_name(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "Mexico" in prompt
        assert "{{COUNTRY}}" not in prompt

    def test_substitutes_source_language(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "Spanish" in prompt
        assert "{{SOURCE_LANGUAGE}}" not in prompt

    def test_contains_analytical_phases(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "Phase 1: Orient" in prompt
        assert "Phase 2: Read the Evidence" in prompt
        assert "Phase 3: Assess" in prompt
        assert "Phase 4: Self-Correct" in prompt
        assert "Phase 5: Structural Claim Check" in prompt

    def test_contains_competing_interpretations(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "Competing interpretations" in prompt

    def test_contains_output_schema_keys(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "weekly_entry" in prompt
        assert "updated_signal_categories" in prompt
        assert "updated_posture_summary" in prompt
