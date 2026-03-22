"""Tests for country ledger and global ledger Pydantic models."""

from datetime import date

import pytest
from src.monitor.config import (
    ActivityRating,
    CategoryStatus,
    ClaimStatus,
    Depth,
    DynamicStatus,
    LinkageType,
    Movement,
    SignalCategory,
)
from src.monitor.models import (
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    DevilsAdvocate,
    Development,
    GlobalLedger,
    GlobalPostureSummary,
    GlobalWeeklyEntry,
    PostureSummary,
    RejectedItem,
    SignalCategoryAssessment,
    SignalEnvironment,
    WeeklyEntry,
)


# ---- Helpers ----

def _all_category_status():
    return {c: CategoryStatus.QUIET for c in SignalCategory}


def _all_category_assessments(d: date = date(2026, 3, 14)):
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            last_updated=d,
        )
        for c in SignalCategory
    }


def _all_category_movements():
    return {
        c: CategoryMovement(movement=Movement.NONE)
        for c in SignalCategory
    }


def _minimal_country_ledger(**overrides) -> CountryLedger:
    defaults = dict(
        country="Mexico",
        code="mx",
        tier="periphery",
        actors=[ActorRef(name="Sheinbaum", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Baseline posture.",
            category_status=_all_category_status(),
        ),
        signal_categories=_all_category_assessments(),
    )
    defaults.update(overrides)
    return CountryLedger(**defaults)


# ---- Country Ledger ----

class TestCountryLedger:
    def test_minimal_valid(self):
        ledger = _minimal_country_ledger()
        assert ledger.code == "mx"
        assert len(ledger.signal_categories) == 5

    def test_missing_signal_category_rejected(self):
        cats = _all_category_assessments()
        del cats[SignalCategory.DOMESTIC_REGIME]
        with pytest.raises(ValueError, match="Missing signal categories"):
            _minimal_country_ledger(signal_categories=cats)

    def test_missing_posture_category_rejected(self):
        status = _all_category_status()
        del status[SignalCategory.ECONOMIC_TECH]
        with pytest.raises(ValueError, match="Missing signal categories"):
            PostureSummary(
                as_of=date(2026, 3, 14),
                text="Test",
                category_status=status,
            )

    def test_needs_deep_dive_after_staleness(self):
        ledger = _minimal_country_ledger()
        ledger.posture_summary.consecutive_maintenance_weeks = 4
        assert ledger.needs_deep_dive

    def test_no_deep_dive_needed_when_fresh(self):
        ledger = _minimal_country_ledger()
        ledger.posture_summary.consecutive_maintenance_weeks = 2
        assert not ledger.needs_deep_dive

    def test_needs_consolidation(self):
        entries = [
            WeeklyEntry(
                week=date(2026, 1, i + 1),
                date_range=f"2026-01-{i:02d} to 2026-01-{i+1:02d}",
                depth=Depth.MAINTENANCE,
            )
            for i in range(9)
        ]
        ledger = _minimal_country_ledger(weekly_entries=entries)
        assert ledger.needs_consolidation

    def test_latest_entry(self):
        e1 = WeeklyEntry(week=date(2026, 3, 7), date_range="w1", depth=Depth.MAINTENANCE)
        e2 = WeeklyEntry(week=date(2026, 3, 14), date_range="w2", depth=Depth.MAINTENANCE)
        ledger = _minimal_country_ledger(weekly_entries=[e1, e2])
        assert ledger.latest_entry().week == date(2026, 3, 14)

    def test_empty_ledger_latest_entry(self):
        ledger = _minimal_country_ledger()
        assert ledger.latest_entry() is None


class TestWeeklyEntry:
    def test_maintenance_entry_minimal(self):
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.MAINTENANCE,
        )
        assert entry.depth == Depth.MAINTENANCE

    def test_deep_dive_requires_category_movements(self):
        with pytest.raises(ValueError, match="category_movements"):
            WeeklyEntry(
                week=date(2026, 3, 14),
                date_range="2026-03-07 to 2026-03-14",
                depth=Depth.DEEP_DIVE,
            )

    def test_deep_dive_requires_all_five_categories(self):
        partial = {SignalCategory.ALIGNMENT_DIPLOMATIC: CategoryMovement(movement=Movement.NONE)}
        with pytest.raises(ValueError, match="missing"):
            WeeklyEntry(
                week=date(2026, 3, 14),
                date_range="2026-03-07 to 2026-03-14",
                depth=Depth.DEEP_DIVE,
                category_movements=partial,
            )

    def test_deep_dive_without_devils_advocate_creates_but_fails_validation(self):
        """Entry can be created without devils_advocate but validate_complete catches it."""
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.DEEP_DIVE,
            category_movements=_all_category_movements(),
        )
        errors = entry.validate_complete()
        assert len(errors) == 1
        assert "devils_advocate" in errors[0]

    def test_complete_deep_dive_passes_validation(self):
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.DEEP_DIVE,
            activity_level={"rating": "high", "rationale": "test"},
            category_movements=_all_category_movements(),
            devils_advocate=DevilsAdvocate(challenges=["c1"]),
        )
        assert entry.validate_complete() == []

    def test_valid_deep_dive(self):
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.DEEP_DIVE,
            activity_level={"rating": "high", "rationale": "test"},
            category_movements=_all_category_movements(),
            devils_advocate=DevilsAdvocate(
                challenges=["Challenge 1"],
                recommended_adjustments=["Adjust 1"],
            ),
        )
        assert entry.depth == Depth.DEEP_DIVE


class TestDevelopment:
    def test_source_tier_bounds(self):
        with pytest.raises(ValueError):
            Development(
                headline="Test",
                date=date(2026, 3, 14),
                source="Test Source",
                source_tier=5,
            )

    def test_valid_development(self):
        dev = Development(
            headline="Sheinbaum meets US envoy",
            date=date(2026, 3, 14),
            source="Reuters",
            source_tier=2,
            source_url="https://reuters.com/example",
            actors_involved=["Sheinbaum"],
        )
        assert dev.source_tier == 2


class TestConfidenceChange:
    def test_alias_from(self):
        cc = ConfidenceChange(**{"from": 2, "to": 4, "reason": "new evidence"})
        assert cc.from_ == 2
        assert cc.to == 4


# ---- Global Ledger ----

def _minimal_global_ledger(**overrides) -> GlobalLedger:
    defaults = dict(
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 14),
            text="Initial global posture.",
            signal_environment=SignalEnvironment(),
        ),
    )
    defaults.update(overrides)
    return GlobalLedger(**defaults)


class TestGlobalLedger:
    def test_minimal_valid(self):
        gl = _minimal_global_ledger()
        assert gl.created == date(2026, 3, 1)

    def test_next_dynamic_id_empty(self):
        gl = _minimal_global_ledger()
        assert gl.next_dynamic_id() == 1

    def test_triage_flagged_countries(self):
        from src.monitor.models import ActiveDynamic, EvidenceStrength, TriageImplication
        gl = _minimal_global_ledger(
            active_dynamics=[
                ActiveDynamic(
                    dynamic_id=1,
                    title="Test dynamic",
                    created_week=date(2026, 3, 7),
                    last_updated=date(2026, 3, 14),
                    status=DynamicStatus.DEVELOPING,
                    current_assessment="Test",
                    countries_involved=["mx", "br"],
                    triage_implications=TriageImplication(
                        countries_to_flag=["tr", "in"],
                        reason="Testing",
                    ),
                )
            ]
        )
        assert gl.triage_flagged_countries == {"tr", "in"}

    def test_rejection_log_required(self):
        with pytest.raises(ValueError, match="items_considered_rejected"):
            GlobalWeeklyEntry(
                week=date(2026, 3, 14),
                items_considered_rejected=[],
            )

    def test_valid_global_weekly_entry(self):
        entry = GlobalWeeklyEntry(
            week=date(2026, 3, 14),
            items_considered_rejected=[
                RejectedItem(candidate="Test pattern", reason_rejected="Insufficient evidence")
            ],
        )
        assert len(entry.items_considered_rejected) == 1
