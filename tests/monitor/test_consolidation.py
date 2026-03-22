"""Tests for ledger consolidation: entry compression and mechanical fallback."""

from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    Movement,
    SignalCategory,
)
from src.monitor.ledger.consolidation import (
    _format_entries_for_consolidation,
    _mechanical_consolidation,
)
from src.monitor.models import (
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    DevilsAdvocate,
    PostureSummary,
    SelfCorrection,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    WeeklyEntry,
)


# ---- Helpers ----

def _all_category_status():
    return {c: CategoryStatus.QUIET for c in SignalCategory}


def _all_category_assessments():
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Baseline for {c.value}",
            confidence=3,
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }


def _maintenance_entry(week: date) -> WeeklyEntry:
    return WeeklyEntry(
        week=week,
        date_range=f"{week}",
        depth=Depth.MAINTENANCE,
    )


def _deep_dive_entry(
    week: date,
    significant_cat: SignalCategory = None,
    correction: bool = False,
    claim_change: bool = False,
) -> WeeklyEntry:
    movements = {c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory}
    if significant_cat:
        movements[significant_cat] = CategoryMovement(
            movement=Movement.SIGNIFICANT,
            updated_assessment=f"Significant change in {significant_cat.value} on {week}.",
            confidence_change=ConfidenceChange(**{"from": 3, "to": 4, "reason": "new evidence"}),
        )

    corrections = []
    if correction:
        corrections.append(SelfCorrection(
            category=SignalCategory.DOMESTIC_REGIME,
            prior_week=date(2026, 1, 1),
            original_claim="Original claim.",
            correction="Corrected assessment.",
            root_cause="New data.",
        ))

    claim_checks = []
    if claim_change:
        claim_checks.append(StructuralClaimCheck(
            claim_ref="STRUC-05",
            claim_text="Test claim.",
            status="under_pressure",
            evidence="Test evidence.",
            confidence_in_claim=3,
        ))

    return WeeklyEntry(
        week=week,
        date_range=f"{week}",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "test"},
        category_movements=movements,
        self_corrections=corrections,
        structural_claim_checks=claim_checks,
        devils_advocate=DevilsAdvocate(challenges=["c1"]),
    )


# ---- Format for consolidation ----

class TestFormatEntries:
    def test_includes_country_and_period(self):
        entries = [_maintenance_entry(date(2026, 1, 7)), _maintenance_entry(date(2026, 2, 7))]
        text = _format_entries_for_consolidation(entries, "Mexico")
        assert "Mexico" in text
        assert "2026-01-07" in text
        assert "2026-02-07" in text

    def test_includes_significant_movements(self):
        entries = [_deep_dive_entry(date(2026, 1, 14), SignalCategory.ALIGNMENT_DIPLOMATIC)]
        text = _format_entries_for_consolidation(entries, "Mexico")
        assert "alignment_diplomatic" in text
        assert "significant" in text

    def test_includes_corrections(self):
        entries = [_deep_dive_entry(date(2026, 1, 14), correction=True)]
        text = _format_entries_for_consolidation(entries, "Mexico")
        assert "CORRECTION" in text
        assert "Corrected assessment" in text

    def test_includes_claim_changes(self):
        entries = [_deep_dive_entry(date(2026, 1, 14), claim_change=True)]
        text = _format_entries_for_consolidation(entries, "Mexico")
        assert "STRUC-05" in text
        assert "under_pressure" in text

    def test_skips_no_movement(self):
        entries = [_deep_dive_entry(date(2026, 1, 14))]
        text = _format_entries_for_consolidation(entries, "Mexico")
        # No movement categories shouldn't appear
        assert "significant" not in text


# ---- Mechanical consolidation (no LLM) ----

class TestMechanicalConsolidation:
    def test_basic_summary(self):
        entries = [
            _maintenance_entry(date(2026, 1, 7)),
            _deep_dive_entry(date(2026, 1, 14)),
            _maintenance_entry(date(2026, 1, 21)),
        ]
        result = _mechanical_consolidation(entries, "Mexico")
        assert "Mexico" in result
        assert "1 deep dives" in result
        assert "2 maintenance" in result

    def test_captures_significant_movements(self):
        entries = [
            _deep_dive_entry(date(2026, 1, 14), SignalCategory.ALIGNMENT_DIPLOMATIC),
        ]
        result = _mechanical_consolidation(entries, "Mexico")
        assert "alignment_diplomatic" in result

    def test_captures_corrections(self):
        entries = [_deep_dive_entry(date(2026, 1, 14), correction=True)]
        result = _mechanical_consolidation(entries, "Mexico")
        assert "Corrections" in result

    def test_captures_claim_changes(self):
        entries = [_deep_dive_entry(date(2026, 1, 14), claim_change=True)]
        result = _mechanical_consolidation(entries, "Mexico")
        assert "STRUC-05" in result
        assert "under_pressure" in result

    def test_empty_entries(self):
        result = _mechanical_consolidation([], "Mexico")
        assert "Mexico" in result
        assert "0 entries" in result

    def test_all_maintenance(self):
        entries = [_maintenance_entry(date(2026, 1, i * 7 + 7)) for i in range(4)]
        result = _mechanical_consolidation(entries, "Mexico")
        assert "0 deep dives" in result
        assert "4 maintenance" in result
