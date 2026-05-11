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

    def test_claim_check_with_invalid_enum_status_maps_to_confirmed(self):
        """LLM returning 'unchanged' / 'maintained' for status used to throw
        ValidationError and drop the claim; now coerces to CONFIRMED."""
        data = _valid_agent_response()
        data["weekly_entry"]["structural_claim_checks"] = [{
            "claim_ref": "STRUC-01",
            "claim_text": "Test claim",
            "status": "unchanged",       # invalid enum value
            "confidence_in_claim": 4,
        }]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        from src.monitor.config import ClaimStatus
        assert len(output.weekly_entry.structural_claim_checks) == 1
        assert output.weekly_entry.structural_claim_checks[0].status == ClaimStatus.CONFIRMED

    def test_claim_check_with_word_confidence_coerced_to_int(self):
        """LLM returning 'high' / 'medium' / 'low' for confidence_in_claim used
        to throw ValidationError; now coerces to 5/3/1."""
        data = _valid_agent_response()
        data["weekly_entry"]["structural_claim_checks"] = [{
            "claim_ref": "STRUC-02",
            "claim_text": "Test",
            "status": "confirmed",
            "confidence_in_claim": "high",
        }]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        assert len(output.weekly_entry.structural_claim_checks) == 1
        assert output.weekly_entry.structural_claim_checks[0].confidence_in_claim == 5

    def test_missing_signal_category_carries_forward_from_ledger(self):
        """If LLM omits a category in updated_signal_categories, fall back
        to the prior ledger assessment instead of throwing KeyError."""
        data = _valid_agent_response()
        # Drop alignment_diplomatic from the LLM's response
        del data["updated_signal_categories"]["alignment_diplomatic"]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        # Ledger baseline should be preserved
        ad = output.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC]
        assert ad is not None  # not a placeholder
        # Ledger's assessment came through
        ledger = _test_ledger()
        assert ad.current_assessment == ledger.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC].current_assessment

    def test_assessment_missing_required_field_falls_back_to_ledger(self):
        """If LLM returns an assessment entry but omits current_assessment,
        fall back to ledger rather than throwing KeyError."""
        data = _valid_agent_response()
        # Keep the key but strip the required field
        data["updated_signal_categories"]["alignment_diplomatic"] = {"confidence": 3}
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        ad = output.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC]
        ledger = _test_ledger()
        # current_assessment carried forward from ledger
        assert ad.current_assessment == ledger.signal_categories[SignalCategory.ALIGNMENT_DIPLOMATIC].current_assessment

    def test_posture_missing_category_status_falls_back_to_ledger(self):
        """If LLM posture omits category_status, fall back to ledger's."""
        data = _valid_agent_response()
        up_key = "updated_posture_summary" if "updated_posture_summary" in data else "updated_posture"
        del data[up_key]["category_status"]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        ledger = _test_ledger()
        # All categories present from ledger
        assert set(output.posture_summary.category_status.keys()) == set(SignalCategory)

    def test_posture_missing_text_falls_back_to_ledger(self):
        """If LLM posture omits text, fall back to ledger's posture text."""
        data = _valid_agent_response()
        up_key = "updated_posture_summary" if "updated_posture_summary" in data else "updated_posture"
        del data[up_key]["text"]
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        ledger = _test_ledger()
        assert output.posture_summary.text == ledger.posture_summary.text

    def test_posture_entirely_missing_falls_back_to_ledger(self):
        """If LLM omits the updated_posture_summary entirely, carry forward
        ledger rather than throwing."""
        data = _valid_agent_response()
        for key in ("updated_posture_summary", "updated_posture"):
            data.pop(key, None)
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        ledger = _test_ledger()
        assert output.posture_summary.text == ledger.posture_summary.text

    def test_malformed_self_correction_skipped(self):
        """A self_correction entry that fails construction shouldn't kill
        the country — other corrections (and the rest of parsing) survive."""
        data = _valid_agent_response()
        # Inject one bad entry (missing dict fields entirely; could fail
        # if the schema gets tighter; we use a non-dict to force Exception)
        data["weekly_entry"]["self_corrections"] = [
            "not a dict — will throw",
        ]
        # Should not raise — bad entry skipped
        output = parse_country_response(json.dumps(data), date(2026, 3, 14), "w1", _test_ledger())
        assert isinstance(output, CountryAgentOutput)
        assert output.weekly_entry.self_corrections == []


# ---- Tool-use hydration ----


class TestHydrateCountryOutput:
    def test_hydrates_valid_tool_input(self):
        from src.monitor.agents.country import hydrate_country_output
        tool_input = _valid_agent_response()
        output = hydrate_country_output(
            tool_input, date(2026, 3, 14), "2026-03-07 to 2026-03-14", _test_ledger(),
        )
        assert isinstance(output, CountryAgentOutput)
        assert set(output.signal_categories.keys()) == set(SignalCategory)
        assert output.posture_summary.text  # non-empty

    def test_hydrated_claim_check_uses_enum(self):
        from src.monitor.agents.country import hydrate_country_output
        from src.monitor.config import ClaimStatus
        tool_input = _valid_agent_response()
        output = hydrate_country_output(
            tool_input, date(2026, 3, 14), "w1", _test_ledger(),
        )
        # The valid-response fixture has STRUC-05 at confirmed
        checks = output.weekly_entry.structural_claim_checks
        if checks:
            assert isinstance(checks[0].status, ClaimStatus)

    def test_record_country_analysis_tool_schema_has_no_refs(self):
        """Belt-and-suspenders: the tool's input_schema must be fully inlined."""
        import json as _json
        from src.monitor.agents.country import RECORD_COUNTRY_ANALYSIS_TOOL
        j = _json.dumps(RECORD_COUNTRY_ANALYSIS_TOOL)
        assert "$ref" not in j
        assert "$defs" not in j

    def test_record_country_analysis_requires_all_signal_categories(self):
        """The schema must require all 5 signal categories as explicit keys."""
        from src.monitor.agents.country import RECORD_COUNTRY_ANALYSIS_TOOL
        schema = RECORD_COUNTRY_ANALYSIS_TOOL["input_schema"]
        sig_cats = schema["properties"]["updated_signal_categories"]
        assert set(sig_cats["required"]) == {c.value for c in SignalCategory}


# ---- System Prompt ----

class TestBuildSystemPrompt:
    def test_is_byte_identical_across_countries(self):
        """The country agent system prompt MUST be byte-identical across
        countries — that's what lets cache_control on the system block reuse
        across the parallel x30 calls in a weekly run. If this fails, someone
        reintroduced per-country interpolation and cross-country cache reuse
        will drop to 0% (see country.py:973 comment for context)."""
        mx = _build_system_prompt(load_country_config("mx"))
        jp = _build_system_prompt(load_country_config("jp"))
        de = _build_system_prompt(load_country_config("de"))
        assert mx == jp == de

    def test_no_template_variables_remain(self):
        config = load_country_config("mx")
        prompt = _build_system_prompt(config)
        assert "{{" not in prompt
        assert "}}" not in prompt

    def test_does_not_name_specific_countries(self):
        """The system prompt should not bake in any particular country name —
        country identity is delivered via the user message."""
        prompt = _build_system_prompt(load_country_config("mx"))
        # These are countries we analyze; none should appear in the cached prefix.
        for name in ("Mexico", "Japan", "Germany", "Brazil", "Indonesia"):
            assert name not in prompt, f"system prompt leaks country name: {name}"

    def test_contains_analytical_phases(self):
        prompt = _build_system_prompt(load_country_config("mx"))
        assert "Phase 1: Orient" in prompt
        assert "Phase 2: Read the Evidence" in prompt
        assert "Phase 3: Assess" in prompt
        assert "Phase 4: Self-Correct" in prompt
        assert "Phase 5: Structural Claim Check" in prompt

    def test_contains_competing_interpretations(self):
        prompt = _build_system_prompt(load_country_config("mx"))
        assert "Competing interpretations" in prompt

    def test_contains_output_schema_keys(self):
        prompt = _build_system_prompt(load_country_config("mx"))
        assert "weekly_entry" in prompt
        assert "updated_signal_categories" in prompt
        assert "updated_posture_summary" in prompt
