"""Tests for regional synthesis agent: prompt construction, parsing, confidence inheritance."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    Depth,
    Movement,
    Region,
    SignalCategory,
)
from src.monitor.agents.regional import (
    CrossCuttingDynamic,
    Gap,
    LowConfidenceItem,
    RegionalReport,
    RejectedDynamic,
    REGION_COUNTRIES,
    REGION_DISPLAY_NAMES,
    _build_regional_prompt,
    _build_system_prompt,
    _format_country_analysis,
    get_region_countries,
    parse_regional_response,
)
from src.monitor.models import (
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    Development,
    DevilsAdvocate,
    PostureSummary,
    SignalCategoryAssessment,
    WeeklyEntry,
)


# ---- Helpers ----

def _all_category_status(status=CategoryStatus.QUIET):
    return {c: status for c in SignalCategory}


def _all_category_assessments(confidence=3):
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Assessment for {c.value}",
            confidence=confidence,
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }


def _test_ledger(code="mx", country="Mexico", confidence=3) -> CountryLedger:
    return CountryLedger(
        country=country,
        code=code,
        tier="periphery",
        actors=[ActorRef(name="Leader", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text=f"{country} test posture.",
            category_status=_all_category_status(),
        ),
        signal_categories=_all_category_assessments(confidence),
    )


def _deep_dive_entry(movement=Movement.NONE) -> WeeklyEntry:
    movements = {c: CategoryMovement(movement=movement) for c in SignalCategory}
    if movement != Movement.NONE:
        movements[SignalCategory.ALIGNMENT_DIPLOMATIC] = CategoryMovement(
            movement=movement,
            developments=[
                Development(
                    headline="Test development",
                    date=date(2026, 3, 12),
                    source="Reuters",
                    source_tier=2,
                ),
            ],
            updated_assessment="Updated assessment.",
            confidence_change=ConfidenceChange(**{"from": 3, "to": 4, "reason": "test"}),
        )
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "test"},
        category_movements=movements,
        devils_advocate=DevilsAdvocate(challenges=["Challenge 1"]),
    )


# ---- Region mapping ----

class TestRegionCountries:
    def test_all_regions_defined(self):
        for region in Region:
            assert region in REGION_COUNTRIES
            assert len(REGION_COUNTRIES[region]) > 0

    def test_americas(self):
        assert set(get_region_countries(Region.AMERICAS)) == {"ca", "mx", "br", "cl"}

    def test_total_countries(self):
        all_codes = set()
        for codes in REGION_COUNTRIES.values():
            all_codes.update(codes)
        assert len(all_codes) == 30


# ---- System prompt ----

class TestBuildSystemPrompt:
    def test_includes_region_name(self):
        prompt = _build_system_prompt(Region.AMERICAS)
        assert "Americas" in prompt

    def test_includes_country_list(self):
        prompt = _build_system_prompt(Region.AMERICAS)
        assert "CA" in prompt
        assert "MX" in prompt
        assert "BR" in prompt

    def test_no_template_variables(self):
        prompt = _build_system_prompt(Region.AMERICAS)
        assert "{{REGION}}" not in prompt
        assert "{{COUNTRY_LIST}}" not in prompt

    def test_contains_critical_rules(self):
        prompt = _build_system_prompt(Region.AMERICAS)
        assert "Confidence Inheritance" in prompt
        assert "Low-Confidence Quarantine" in prompt
        assert "Apophenia Check" in prompt
        assert "Rejection Log" in prompt

    def test_display_names(self):
        for region in Region:
            assert region in REGION_DISPLAY_NAMES
            prompt = _build_system_prompt(region)
            assert REGION_DISPLAY_NAMES[region] in prompt


# ---- Format country analysis ----

class TestFormatCountryAnalysis:
    def test_includes_country_name(self):
        text = _format_country_analysis("mx", _test_ledger(), _deep_dive_entry())
        assert "Mexico" in text
        assert "MX" in text

    def test_includes_posture(self):
        text = _format_country_analysis("mx", _test_ledger(), _deep_dive_entry())
        assert "test posture" in text

    def test_includes_movements(self):
        entry = _deep_dive_entry(Movement.SIGNIFICANT)
        text = _format_country_analysis("mx", _test_ledger(), entry)
        assert "significant" in text
        assert "Updated assessment" in text

    def test_includes_confidence_levels(self):
        text = _format_country_analysis("mx", _test_ledger(confidence=4), _deep_dive_entry())
        assert "4" in text

    def test_includes_devils_advocate(self):
        text = _format_country_analysis("mx", _test_ledger(), _deep_dive_entry())
        assert "Challenge 1" in text

    def test_handles_no_entry(self):
        text = _format_country_analysis("mx", _test_ledger(), None)
        assert "no entry" in text.lower() or "No weekly entry" in text

    def test_shows_depth(self):
        text = _format_country_analysis("mx", _test_ledger(), _deep_dive_entry())
        assert "deep_dive" in text


# ---- Build regional prompt ----

class TestBuildRegionalPrompt:
    def test_includes_region_name(self):
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}
        prompt = _build_regional_prompt(Region.AMERICAS, ledgers, entries)
        assert "Americas" in prompt

    def test_includes_country_codes(self):
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}
        prompt = _build_regional_prompt(Region.AMERICAS, ledgers, entries)
        assert "MX" in prompt

    def test_includes_country_analyses(self):
        ledgers = {
            "mx": _test_ledger("mx", "Mexico"),
            "br": _test_ledger("br", "Brazil"),
        }
        entries = {
            "mx": _deep_dive_entry(),
            "br": _deep_dive_entry(),
        }
        prompt = _build_regional_prompt(Region.AMERICAS, ledgers, entries)
        assert "Mexico" in prompt
        assert "Brazil" in prompt

    def test_empty_region(self):
        prompt = _build_regional_prompt(Region.AMERICAS, {}, {})
        assert "No country analyses" in prompt


# ---- Parse response ----

class TestParseRegionalResponse:
    VALID_RESPONSE = json.dumps({
        "cross_cutting_dynamics": [
            {
                "title": "Coordinated pushback on US tariff threats",
                "countries_involved": ["mx", "br"],
                "signal_categories": ["alignment_diplomatic", "economic_tech"],
                "pattern_type": "parallel",
                "assessment": "Both Mexico and Brazil have escalated sovereignty rhetoric in response to US pressure.",
                "significance": "Indicates potential Americas-wide realignment on trade policy.",
                "trend": "developing",
                "confidence": 3,
                "confidence_inherited_from": {"mx": 4, "br": 3},
                "weakest_link": "Brazil's assessment rests on single BRICS wire report.",
                "evidence_against_linkage": "Both countries are responding independently to domestic pressures rather than coordinating.",
                "linkage_strength": "moderate",
                "linkage_justification": "Shared US tariff pressure and temporal proximity of responses.",
                "competing_interpretation": "Both countries are responding independently to domestic pressures rather than coordinating.",
            }
        ],
        "dynamics_considered_and_rejected": [
            {
                "candidate_dynamic": "Coordinated Americas trade bloc response to China",
                "countries": ["mx", "br", "cl"],
                "reason_rejected": "Chile's engagement is too uncertain (confidence 2) and Canada shows no parallel movement.",
            }
        ],
        "gaps": [
            {
                "expected_dynamic": "Pacific Alliance trade coordination",
                "observed": "No coordinated trade activity observed.",
                "assessment": "Pacific Alliance appears dormant this week.",
            }
        ],
        "low_confidence_items": [
            {
                "item": "Chile may be reconsidering Pacific Alliance engagement.",
                "origin": "cl_institutional",
                "confidence": 2,
                "note": "Single government source, no independent corroboration.",
            }
        ],
    })

    def test_parses_valid_response(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert report.region == Region.AMERICAS
        assert report.week == date(2026, 3, 14)

    def test_cross_cutting_dynamics(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.cross_cutting_dynamics) == 1
        d = report.cross_cutting_dynamics[0]
        assert d.title == "Coordinated pushback on US tariff threats"
        assert set(d.countries_involved) == {"mx", "br"}
        assert d.pattern_type == "parallel"
        assert d.linkage_strength == "moderate"
        assert d.significance != ""
        assert d.weakest_link != ""
        assert d.linkage_justification != ""

    def test_confidence_inheritance(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        d = report.cross_cutting_dynamics[0]
        assert d.confidence == 3  # min of mx=4, br=3
        assert d.confidence_inherited_from == {"mx": 4, "br": 3}

    def test_low_confidence_items(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.low_confidence_items) == 1
        lc = report.low_confidence_items[0]
        assert lc.origin == "cl_institutional"
        assert lc.confidence == 2
        assert "Pacific Alliance" in lc.item

    def test_dynamics_considered_and_rejected(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.dynamics_considered_and_rejected) == 1
        r = report.dynamics_considered_and_rejected[0]
        assert "Chile" in r.reason_rejected
        assert set(r.countries) == {"mx", "br", "cl"}

    def test_gaps(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.gaps) == 1
        g = report.gaps[0]
        assert "Pacific Alliance" in g.expected_dynamic
        assert g.assessment != ""

    def test_competing_interpretation_required(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        for d in report.cross_cutting_dynamics:
            assert d.competing_interpretation != ""

    def test_evidence_against_linkage_required(self):
        report = parse_regional_response(self.VALID_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        for d in report.cross_cutting_dynamics:
            assert d.evidence_against_linkage != ""

    def test_strips_markdown_fencing(self):
        fenced = f"```json\n{self.VALID_RESPONSE}\n```"
        report = parse_regional_response(fenced, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.cross_cutting_dynamics) == 1

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_regional_response("not json", Region.AMERICAS, date(2026, 3, 14))

    def test_empty_dynamics_parses(self):
        response = json.dumps({
            "cross_cutting_dynamics": [],
            "dynamics_considered_and_rejected": [
                {"candidate_dynamic": "X", "countries": ["mx"], "reason_rejected": "No evidence."}
            ],
            "gaps": [],
            "low_confidence_items": [],
        })
        report = parse_regional_response(response, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.cross_cutting_dynamics) == 0
        assert len(report.dynamics_considered_and_rejected) == 1


# ---- Backward compatibility ----

class TestBackwardCompatParsing:
    """Verify the parser handles old-format JSON keys from prior versions."""

    OLD_FORMAT_RESPONSE = json.dumps({
        "regional_summary": "The Americas region shows divergent responses.",
        "cross_cutting_dynamics": [
            {
                "title": "Test dynamic",
                "countries_involved": ["mx", "br"],
                "signal_categories": ["alignment_diplomatic"],
                "assessment": "Test assessment.",
                "evidence_summary": "Test evidence.",
                "confidence": 3,
                "confidence_inherited_from": {"mx": 4, "br": 3},
                "linkage_type": "parallel_behavior",
                "linkage_strength": "moderate",
                "competing_interpretation": "Alt explanation.",
                "what_to_watch": "Next steps.",
            }
        ],
        "low_confidence_quarantine": [
            {
                "country": "cl",
                "category": "institutional",
                "confidence": 2,
                "assessment": "Chile uncertain.",
                "reason_quarantined": "Single source.",
            }
        ],
        "rejection_log": [
            {
                "candidate": "Old candidate",
                "countries_considered": ["mx", "br"],
                "reason_rejected": "Not supported.",
            }
        ],
    })

    def test_old_format_parses(self):
        report = parse_regional_response(self.OLD_FORMAT_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.cross_cutting_dynamics) == 1

    def test_old_linkage_type_mapped_to_pattern_type(self):
        report = parse_regional_response(self.OLD_FORMAT_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        d = report.cross_cutting_dynamics[0]
        assert d.pattern_type == "parallel_behavior"

    def test_old_rejection_log_mapped(self):
        report = parse_regional_response(self.OLD_FORMAT_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.dynamics_considered_and_rejected) == 1
        r = report.dynamics_considered_and_rejected[0]
        assert r.candidate_dynamic == "Old candidate"
        assert set(r.countries) == {"mx", "br"}

    def test_old_quarantine_mapped(self):
        report = parse_regional_response(self.OLD_FORMAT_RESPONSE, Region.AMERICAS, date(2026, 3, 14))
        assert len(report.low_confidence_items) == 1
        lc = report.low_confidence_items[0]
        assert lc.confidence == 2
        assert "Chile uncertain" in lc.item
        assert "cl_institutional" in lc.origin
