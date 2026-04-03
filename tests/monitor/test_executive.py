"""Tests for executive agent: prompt construction, response parsing, ledger updates."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    DynamicStatus,
    LinkageType,
    Region,
    SignalCategory,
)
from src.monitor.agents.executive import (
    EXECUTIVE_SYSTEM_PROMPT,
    _build_executive_prompt,
    _format_global_ledger_state,
    _format_regional_report,
    apply_executive_output,
    parse_executive_response,
)
from src.monitor.agents.regional import CrossCuttingDynamic, RegionalReport, RejectedDynamic
from src.monitor.models import (
    ActiveDynamic,
    EvidenceStrength,
    GlobalLedger,
    GlobalPostureSummary,
    SignalEnvironment,
    TriageImplication,
    WatchlistItem,
)


# ---- Helpers ----

def _empty_global_ledger() -> GlobalLedger:
    return GlobalLedger(
        last_updated=date(2026, 3, 7),
        created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 7),
            text="Prior week posture.",
            signal_environment=SignalEnvironment(),
        ),
    )


def _global_ledger_with_dynamic() -> GlobalLedger:
    gl = _empty_global_ledger()
    gl.active_dynamics.append(ActiveDynamic(
        dynamic_id=1,
        title="US pressure on Americas",
        created_week=date(2026, 3, 7),
        last_updated=date(2026, 3, 7),
        status=DynamicStatus.DEVELOPING,
        current_assessment="Prior assessment.",
        countries_involved=["mx", "br"],
        signal_categories_touched=[SignalCategory.ALIGNMENT_DIPLOMATIC],
        evidence_strength=EvidenceStrength(confidence=3),
        weeks_active=1,
        consecutive_unchanged_weeks=0,
    ))
    return gl


def _test_regional_report(region=Region.AMERICAS) -> RegionalReport:
    return RegionalReport(
        region=region,
        week=date(2026, 3, 14),
        cross_cutting_dynamics=[
            CrossCuttingDynamic(
                title="Coordinated pushback",
                countries_involved=["mx", "br"],
                signal_categories=["alignment_diplomatic"],
                pattern_type="parallel",
                assessment="Both countries escalating sovereignty rhetoric.",
                significance="Tests hemispheric leverage.",
                trend="developing",
                confidence=3,
                confidence_inherited_from={"mx": 4, "br": 3},
                weakest_link="Brazil single-source.",
                evidence_against_linkage="Independent domestic pressures.",
                linkage_strength="moderate",
                linkage_justification="Shared US tariff pressure.",
                competing_interpretation="Independent responses.",
            ),
        ],
        dynamics_considered_and_rejected=[
            RejectedDynamic(
                candidate_dynamic="X",
                countries=["mx"],
                reason_rejected="Insufficient.",
            ),
        ],
    )


def _valid_delta_response() -> dict:
    """Old delta-based format (dynamics_to_create/update/archive)."""
    return {
        "global_posture_summary": {
            "text": "Americas pushback dominates. Europe quiet. Asia-Pacific stable.",
            "signal_environment": {
                "most_active_categories": ["alignment_diplomatic"],
                "quietest_categories": ["institutional"],
                "geographic_hotspots": ["americas"],
                "geographic_quiet_zones": ["asia_pacific"],
            },
        },
        "dynamics_to_create": [
            {
                "title": "New dynamic: European defense autonomy",
                "status": "emerging",
                "current_assessment": "France and Germany accelerating defense coordination.",
                "countries_involved": ["fr", "de"],
                "signal_categories_touched": ["security_defense"],
                "evidence_strength": {
                    "confidence": 3,
                    "supporting_country_confidences": {"fr": 4, "de": 3},
                    "weakest_link": "German coalition instability.",
                    "linkage_type": "parallel_behavior",
                    "linkage_assessment": "Both responding to US retrenchment.",
                },
                "competing_interpretation": "Budget-driven, not strategic.",
                "what_to_watch": "Joint procurement announcements.",
                "triage_implications": {
                    "countries_to_flag": ["pl", "it"],
                    "reason": "Check if Poland and Italy mirror.",
                },
            }
        ],
        "dynamics_to_update": [
            {
                "dynamic_id": 1,
                "status": "established",
                "current_assessment": "Americas pushback now includes coordinated rhetoric.",
                "countries_involved": ["mx", "br", "cl"],
                "evidence_strength": {
                    "confidence": 3,
                    "supporting_country_confidences": {"mx": 4, "br": 3, "cl": 2},
                    "weakest_link": "Chile evidence is single-source.",
                    "linkage_type": "parallel_behavior",
                    "linkage_assessment": "Parallel but not coordinated.",
                },
                "triage_implications": {
                    "countries_to_flag": ["ca"],
                    "reason": "Check if Canada joins pushback.",
                },
            }
        ],
        "dynamics_to_archive": [],
        "watchlist_add": [
            {
                "item": "BRICS expansion summit announced",
                "signal_category": "institutional",
                "countries": ["br", "in", "sa"],
                "why_it_matters": "Could reshape institutional order.",
                "trigger": "Formal invitation to new members.",
            }
        ],
        "watchlist_remove_indices": [],
        "executive_briefing_items": [
            {
                "title": "Americas pushback crystallizes",
                "regions_involved": ["americas"],
                "what": "Mexico and Brazil have moved from defensive to active resistance.",
                "why_it_matters": "Challenges US ability to maintain hemispheric leverage.",
                "what_to_watch": "G20 preparatory meetings.",
                "confidence": 3,
                "confidence_note": "Brazil evidence is moderate.",
            }
        ],
        "items_considered_rejected": [
            {
                "candidate": "Global de-dollarization trend",
                "reason_rejected": "Evidence too scattered across regions to constitute a pattern.",
            }
        ],
        "self_corrections": [],
    }


def _valid_full_state_response() -> dict:
    """New full-state format (global_ledger_update wrapper)."""
    return {
        "global_ledger_update": {
            "global_posture_summary": {
                "as_of": "2026-03-14",
                "text": "Americas pushback dominates. Europe quiet. Asia-Pacific stable.",
                "signal_environment": {
                    "most_active_categories": ["alignment_diplomatic"],
                    "quietest_categories": ["institutional"],
                    "geographic_hotspots": ["americas"],
                    "geographic_quiet_zones": ["asia_pacific"],
                },
            },
            "active_dynamics": [
                {
                    "dynamic_id": 1,
                    "title": "US pressure on Americas",
                    "created_week": "2026-03-07",
                    "last_updated": "2026-03-14",
                    "status": "established",
                    "current_assessment": "Americas pushback now includes coordinated rhetoric.",
                    "countries_involved": ["mx", "br", "cl"],
                    "signal_categories_touched": ["alignment_diplomatic"],
                    "evidence_strength": {
                        "confidence": 3,
                        "supporting_country_confidences": {"mx": 4, "br": 3, "cl": 2},
                        "weakest_link": "Chile evidence is single-source.",
                        "linkage_type": "parallel_behavior",
                        "linkage_assessment": "Parallel but not coordinated.",
                    },
                    "competing_interpretation": "Independent responses.",
                    "what_to_watch": "G20 preparatory meetings.",
                    "triage_implications": {
                        "countries_to_flag": ["ca"],
                        "reason": "Check if Canada joins pushback.",
                    },
                    "weeks_active": 2,
                    "consecutive_unchanged_weeks": 0,
                },
                {
                    "dynamic_id": 2,
                    "title": "European defense autonomy",
                    "created_week": "2026-03-14",
                    "last_updated": "2026-03-14",
                    "status": "emerging",
                    "current_assessment": "France and Germany accelerating defense coordination.",
                    "countries_involved": ["fr", "de"],
                    "signal_categories_touched": ["security_defense"],
                    "evidence_strength": {
                        "confidence": 3,
                        "supporting_country_confidences": {"fr": 4, "de": 3},
                        "weakest_link": "German coalition instability.",
                        "linkage_type": "parallel_behavior",
                        "linkage_assessment": "Both responding to US retrenchment.",
                    },
                    "competing_interpretation": "Budget-driven, not strategic.",
                    "what_to_watch": "Joint procurement announcements.",
                    "triage_implications": {
                        "countries_to_flag": ["pl", "it"],
                        "reason": "Check if Poland and Italy mirror.",
                    },
                    "weeks_active": 1,
                    "consecutive_unchanged_weeks": 0,
                },
            ],
            "watchlist": [
                {
                    "item": "BRICS expansion summit announced",
                    "signal_category": "institutional",
                    "countries": ["br", "in", "sa"],
                    "why_it_matters": "Could reshape institutional order.",
                    "trigger": "Formal invitation to new members.",
                    "added_week": "2026-03-14",
                }
            ],
            "weekly_entry": {
                "week": "2026-03-14",
                "executive_briefing_items": [
                    {
                        "title": "Americas pushback crystallizes",
                        "regions_involved": ["americas"],
                        "what": "Mexico and Brazil have moved from defensive to active resistance.",
                        "why_it_matters": "Challenges US ability to maintain hemispheric leverage.",
                        "what_to_watch": "G20 preparatory meetings.",
                        "confidence": 3,
                        "confidence_note": "Brazil evidence is moderate.",
                    }
                ],
                "dynamics_created": [2],
                "dynamics_updated": [1],
                "dynamics_archived": [],
                "items_considered_rejected": [
                    {
                        "candidate": "Global de-dollarization trend",
                        "reason_rejected": "Evidence too scattered.",
                    }
                ],
                "self_corrections": [],
            },
        }
    }


# ---- System Prompt ----

class TestSystemPrompt:
    def test_contains_role(self):
        assert "executive analyst" in EXECUTIVE_SYSTEM_PROMPT

    def test_contains_phases(self):
        assert "Phase 1: Identify Candidates" in EXECUTIVE_SYSTEM_PROMPT
        assert "Phase 2: Evaluate Against Prior State" in EXECUTIVE_SYSTEM_PROMPT
        assert "Phase 3: Synthesize" in EXECUTIVE_SYSTEM_PROMPT
        assert "Phase 4: Update the Global Ledger" in EXECUTIVE_SYSTEM_PROMPT
        assert "Phase 5: Rejection Log" in EXECUTIVE_SYSTEM_PROMPT

    def test_contains_dynamic_lifecycle(self):
        for status in ["emerging", "developing", "established", "monitoring", "weakening", "resolved"]:
            assert status in EXECUTIVE_SYSTEM_PROMPT

    def test_contains_constraints(self):
        assert "3 consecutive weeks" in EXECUTIVE_SYSTEM_PROMPT
        assert "8 triage implications" in EXECUTIVE_SYSTEM_PROMPT
        assert "confidence provenance" in EXECUTIVE_SYSTEM_PROMPT

    def test_contains_tone_guidance(self):
        assert "Foreign Affairs" in EXECUTIVE_SYSTEM_PROMPT
        assert "sophisticated generalist" in EXECUTIVE_SYSTEM_PROMPT


# ---- Format helpers ----

class TestFormatRegionalReport:
    def test_includes_region(self):
        text = _format_regional_report(_test_regional_report())
        assert "americas" in text

    def test_includes_dynamics(self):
        text = _format_regional_report(_test_regional_report())
        assert "Coordinated pushback" in text
        assert "mx" in text
        assert "br" in text

    def test_includes_confidence(self):
        text = _format_regional_report(_test_regional_report())
        assert "3" in text

    def test_includes_rejected_dynamics(self):
        text = _format_regional_report(_test_regional_report())
        assert "Rejected dynamics" in text
        assert "Insufficient" in text

    def test_includes_pattern_type(self):
        text = _format_regional_report(_test_regional_report())
        assert "parallel" in text


class TestFormatGlobalLedgerState:
    def test_includes_posture(self):
        text = _format_global_ledger_state(_empty_global_ledger())
        assert "Prior week posture" in text

    def test_includes_dynamics(self):
        text = _format_global_ledger_state(_global_ledger_with_dynamic())
        assert "US pressure on Americas" in text
        assert "Dynamic #1" in text

    def test_flags_stale_dynamics(self):
        gl = _global_ledger_with_dynamic()
        gl.active_dynamics[0].consecutive_unchanged_weeks = 3
        text = _format_global_ledger_state(gl)
        assert "STALE" in text

    def test_empty_dynamics(self):
        text = _format_global_ledger_state(_empty_global_ledger())
        assert "No active dynamics" in text


# ---- Build prompt ----

class TestBuildExecutivePrompt:
    def test_includes_all_regions(self):
        reports = {Region.AMERICAS: _test_regional_report()}
        prompt = _build_executive_prompt(reports, _empty_global_ledger())
        # Should mention all regions, even missing ones
        assert "americas" in prompt
        assert "No report available" in prompt  # for missing regions

    def test_includes_global_state(self):
        reports = {}
        prompt = _build_executive_prompt(reports, _global_ledger_with_dynamic())
        assert "US pressure on Americas" in prompt


# ---- Parse response ----

class TestParseExecutiveResponse:
    def test_parses_valid_delta(self):
        data = parse_executive_response(json.dumps(_valid_delta_response()))
        assert "global_posture_summary" in data

    def test_parses_valid_full_state(self):
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        assert "global_posture_summary" in data
        assert "active_dynamics" in data

    def test_unwraps_global_ledger_update(self):
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        # Should be unwrapped — no global_ledger_update key
        assert "global_ledger_update" not in data
        assert "active_dynamics" in data

    def test_strips_fencing(self):
        fenced = f"```json\n{json.dumps(_valid_delta_response())}\n```"
        data = parse_executive_response(fenced)
        assert "global_posture_summary" in data

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_executive_response("not json")


# ---- Apply delta format (backward compat) ----

class TestApplyDeltaFormat:
    def test_updates_posture_summary(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert "Americas pushback" in updated.global_posture_summary.text
        assert updated.global_posture_summary.as_of == date(2026, 3, 14)

    def test_updates_signal_environment(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        se = updated.global_posture_summary.signal_environment
        assert SignalCategory.ALIGNMENT_DIPLOMATIC in se.most_active_categories
        assert "americas" in se.geographic_hotspots

    def test_creates_new_dynamic(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.active_dynamics) == 2
        new_dynamic = next(d for d in updated.active_dynamics if d.title == "New dynamic: European defense autonomy")
        assert new_dynamic.status == DynamicStatus.EMERGING
        assert new_dynamic.weeks_active == 1
        assert set(new_dynamic.countries_involved) == {"fr", "de"}

    def test_new_dynamic_gets_unique_id(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        ids = [d.dynamic_id for d in updated.active_dynamics]
        assert len(ids) == len(set(ids))

    def test_new_dynamic_triage_implications(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        new_d = next(d for d in updated.active_dynamics if "European defense" in d.title)
        assert set(new_d.triage_implications.countries_to_flag) == {"pl", "it"}

    def test_updates_existing_dynamic(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        d1 = next(d for d in updated.active_dynamics if d.dynamic_id == 1)
        assert d1.status == DynamicStatus.ESTABLISHED
        assert "coordinated rhetoric" in d1.current_assessment
        assert d1.weeks_active == 2
        assert d1.consecutive_unchanged_weeks == 0

    def test_untouched_dynamic_increments_unchanged(self):
        gl = _global_ledger_with_dynamic()
        gl.active_dynamics.append(ActiveDynamic(
            dynamic_id=99,
            title="Untouched",
            created_week=date(2026, 3, 7),
            last_updated=date(2026, 3, 7),
            status=DynamicStatus.MONITORING,
            current_assessment="Stable.",
            weeks_active=3,
            consecutive_unchanged_weeks=1,
        ))
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        d99 = next(d for d in updated.active_dynamics if d.dynamic_id == 99)
        assert d99.consecutive_unchanged_weeks == 2
        assert d99.weeks_active == 4

    def test_archives_dynamics(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        data["dynamics_to_archive"] = [1]
        data["dynamics_to_update"] = []
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        active_ids = [d.dynamic_id for d in updated.active_dynamics]
        assert 1 not in active_ids
        archived_ids = [d.dynamic_id for d in updated.archived_dynamics]
        assert 1 in archived_ids
        assert updated.archived_dynamics[0].status == DynamicStatus.RESOLVED

    def test_adds_watchlist_item(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.watchlist) == 1
        assert "BRICS" in updated.watchlist[0].item

    def test_removes_watchlist_item(self):
        gl = _empty_global_ledger()
        gl.watchlist.append(WatchlistItem(
            item="Old item",
            signal_category=SignalCategory.INSTITUTIONAL,
            countries=["br"],
            added_week=date(2026, 3, 7),
        ))
        data = _valid_delta_response()
        data["watchlist_remove_indices"] = [0]
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.watchlist) == 1
        assert "BRICS" in updated.watchlist[0].item

    def test_creates_weekly_entry(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.weekly_entries) == 1
        we = updated.weekly_entries[0]
        assert we.week == date(2026, 3, 14)
        assert len(we.executive_briefing_items) == 1
        assert len(we.items_considered_rejected) == 1

    def test_briefing_items_in_weekly_entry(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        we = updated.weekly_entries[0]
        assert we.executive_briefing_items[0].title == "Americas pushback crystallizes"
        assert we.executive_briefing_items[0].confidence == 3

    def test_updates_last_updated(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert updated.last_updated == date(2026, 3, 14)

    def test_dynamics_created_tracked(self):
        gl = _empty_global_ledger()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        we = updated.weekly_entries[0]
        assert len(we.dynamics_created) == 1

    def test_dynamics_updated_tracked(self):
        gl = _global_ledger_with_dynamic()
        data = _valid_delta_response()
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        we = updated.weekly_entries[0]
        assert 1 in we.dynamics_updated


# ---- Apply full-state format (new spec) ----

class TestApplyFullStateFormat:
    def test_updates_posture_summary(self):
        gl = _global_ledger_with_dynamic()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert "Americas pushback" in updated.global_posture_summary.text

    def test_replaces_active_dynamics(self):
        gl = _global_ledger_with_dynamic()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.active_dynamics) == 2
        ids = {d.dynamic_id for d in updated.active_dynamics}
        assert ids == {1, 2}

    def test_dynamic_fields_parsed(self):
        gl = _global_ledger_with_dynamic()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        d1 = next(d for d in updated.active_dynamics if d.dynamic_id == 1)
        assert d1.status == DynamicStatus.ESTABLISHED
        assert d1.weeks_active == 2
        assert d1.consecutive_unchanged_weeks == 0
        assert "coordinated rhetoric" in d1.current_assessment
        assert d1.created_week == date(2026, 3, 7)

    def test_new_dynamic_parsed(self):
        gl = _global_ledger_with_dynamic()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        d2 = next(d for d in updated.active_dynamics if d.dynamic_id == 2)
        assert d2.status == DynamicStatus.EMERGING
        assert d2.title == "European defense autonomy"
        assert set(d2.triage_implications.countries_to_flag) == {"pl", "it"}

    def test_replaces_watchlist(self):
        gl = _global_ledger_with_dynamic()
        gl.watchlist.append(WatchlistItem(
            item="Old item",
            signal_category=SignalCategory.INSTITUTIONAL,
            countries=["br"],
            added_week=date(2026, 3, 7),
        ))
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        # Old item replaced by new list
        assert len(updated.watchlist) == 1
        assert "BRICS" in updated.watchlist[0].item

    def test_creates_weekly_entry(self):
        gl = _global_ledger_with_dynamic()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        assert len(updated.weekly_entries) == 1
        we = updated.weekly_entries[0]
        assert we.week == date(2026, 3, 14)
        assert len(we.executive_briefing_items) == 1
        assert we.dynamics_created == [2]
        assert we.dynamics_updated == [1]

    def test_archives_dynamics(self):
        gl = _global_ledger_with_dynamic()
        # Add a second dynamic that will be archived (not in output active list)
        gl.active_dynamics.append(ActiveDynamic(
            dynamic_id=99,
            title="To be archived",
            created_week=date(2026, 3, 1),
            last_updated=date(2026, 3, 7),
            status=DynamicStatus.WEAKENING,
            current_assessment="Fading.",
            weeks_active=2,
            consecutive_unchanged_weeks=1,
        ))
        # Build response that archives dynamic 99
        resp = _valid_full_state_response()
        resp["global_ledger_update"]["weekly_entry"]["dynamics_archived"] = [99]
        data = parse_executive_response(json.dumps(resp))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        # Active dynamics should only have the 2 from the output
        assert len(updated.active_dynamics) == 2
        # Archived should include dynamic 99
        archived_ids = [d.dynamic_id for d in updated.archived_dynamics]
        assert 99 in archived_ids

    def test_evidence_strength_parsed(self):
        gl = _empty_global_ledger()
        data = parse_executive_response(json.dumps(_valid_full_state_response()))
        updated = apply_executive_output(gl, data, date(2026, 3, 14))
        d1 = next(d for d in updated.active_dynamics if d.dynamic_id == 1)
        assert d1.evidence_strength.confidence == 3
        assert d1.evidence_strength.linkage_type == LinkageType.PARALLEL_BEHAVIOR
        assert "Chile" in d1.evidence_strength.weakest_link
