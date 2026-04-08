"""Tests for cross-reference validation of country and global ledgers."""

from datetime import date

from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    DynamicStatus,
    LinkageType,
    Movement,
    SignalCategory,
)
from src.monitor.ledger.validation import (
    validate_global_ledger_integrity,
    validate_ledger_integrity,
)
from src.monitor.models import (
    ActiveDynamic,
    ActorRef,
    CategoryMovement,
    CountryLedger,
    EvidenceStrength,
    GlobalLedger,
    GlobalPostureSummary,
    GlobalWeeklyEntry,
    PostureSummary,
    RejectedItem,
    SelfCorrection,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    StructuralClaimStatus,
    TriageImplication,
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


def _valid_country_ledger(**overrides) -> CountryLedger:
    defaults = dict(
        country="Mexico",
        code="mx",
        tier="pivot",
        actors=[ActorRef(name="Leader", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Stable.",
            category_status=_all_category_status(),
            consecutive_maintenance_weeks=0,
        ),
        signal_categories=_all_category_assessments(),
        structural_claim_status=[
            StructuralClaimStatus(
                claim_ref="STRUC-01",
                claim_text="Test claim",
                dossier_section=1,
                status=ClaimStatus.CONFIRMED,
                last_checked=date(2026, 3, 14),
            ),
        ],
    )
    defaults.update(overrides)
    return CountryLedger(**defaults)


def _valid_global_ledger(**overrides) -> GlobalLedger:
    defaults = dict(
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 14),
            text="Stable.",
        ),
    )
    defaults.update(overrides)
    return GlobalLedger(**defaults)


def _deep_dive_entry(week: date) -> WeeklyEntry:
    return WeeklyEntry(
        week=week,
        date_range=str(week),
        depth=Depth.DEEP_DIVE,
        category_movements={
            c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory
        },
    )


def _maintenance_entry(week: date) -> WeeklyEntry:
    return WeeklyEntry(
        week=week,
        date_range=str(week),
        depth=Depth.MAINTENANCE,
    )


# ---- Country Ledger Validation ----

class TestCountryLedgerValidation:
    def test_valid_ledger_passes(self):
        ledger = _valid_country_ledger()
        assert validate_ledger_integrity(ledger) == []

    def test_detects_duplicate_claim_refs(self):
        claims = [
            StructuralClaimStatus(
                claim_ref="STRUC-01",
                claim_text="Claim A",
                dossier_section=1,
                status=ClaimStatus.CONFIRMED,
                last_checked=date(2026, 3, 14),
            ),
            StructuralClaimStatus(
                claim_ref="STRUC-01",
                claim_text="Claim B",
                dossier_section=2,
                status=ClaimStatus.CONFIRMED,
                last_checked=date(2026, 3, 14),
            ),
        ]
        ledger = _valid_country_ledger(structural_claim_status=claims)
        errors = validate_ledger_integrity(ledger)
        assert any("Duplicate structural claim refs" in e for e in errors)

    def test_detects_out_of_order_entries(self):
        entries = [
            _maintenance_entry(date(2026, 3, 14)),
            _maintenance_entry(date(2026, 3, 7)),  # earlier than previous
        ]
        ledger = _valid_country_ledger(weekly_entries=entries)
        errors = validate_ledger_integrity(ledger)
        assert any("out of order" in e for e in errors)

    def test_chronological_entries_pass(self):
        entries = [
            _maintenance_entry(date(2026, 3, 7)),
            _maintenance_entry(date(2026, 3, 14)),
        ]
        ledger = _valid_country_ledger(weekly_entries=entries)
        errors = validate_ledger_integrity(ledger)
        assert not any("out of order" in e for e in errors)

    def test_detects_maintenance_weeks_mismatch(self):
        entries = [
            _maintenance_entry(date(2026, 3, 7)),
            _maintenance_entry(date(2026, 3, 14)),
        ]
        ledger = _valid_country_ledger(
            weekly_entries=entries,
            posture_summary=PostureSummary(
                as_of=date(2026, 3, 14),
                text="Stable.",
                category_status=_all_category_status(),
                consecutive_maintenance_weeks=5,  # Wrong: should be 2
            ),
        )
        errors = validate_ledger_integrity(ledger)
        assert any("consecutive_maintenance_weeks mismatch" in e for e in errors)

    def test_correct_maintenance_weeks_passes(self):
        entries = [
            _deep_dive_entry(date(2026, 3, 7)),
            _maintenance_entry(date(2026, 3, 14)),
        ]
        ledger = _valid_country_ledger(
            weekly_entries=entries,
            posture_summary=PostureSummary(
                as_of=date(2026, 3, 14),
                text="Stable.",
                category_status=_all_category_status(),
                consecutive_maintenance_weeks=1,
            ),
        )
        errors = validate_ledger_integrity(ledger)
        assert not any("consecutive_maintenance_weeks" in e for e in errors)

    def test_detects_unknown_claim_ref_in_weekly_check(self):
        entry = _deep_dive_entry(date(2026, 3, 14))
        entry.structural_claim_checks = [
            StructuralClaimCheck(
                claim_ref="STRUC-99",
                claim_text="Unknown claim",
                status=ClaimStatus.CONFIRMED,
                evidence="test",
            ),
        ]
        ledger = _valid_country_ledger(weekly_entries=[entry])
        errors = validate_ledger_integrity(ledger)
        assert any("unknown claim_ref 'STRUC-99'" in e for e in errors)

    def test_known_claim_ref_passes(self):
        entry = _deep_dive_entry(date(2026, 3, 14))
        entry.structural_claim_checks = [
            StructuralClaimCheck(
                claim_ref="STRUC-01",
                claim_text="Test claim",
                status=ClaimStatus.CONFIRMED,
                evidence="test",
            ),
        ]
        ledger = _valid_country_ledger(weekly_entries=[entry])
        errors = validate_ledger_integrity(ledger)
        assert not any("unknown claim_ref" in e for e in errors)

    def test_empty_ledger_passes(self):
        ledger = _valid_country_ledger()
        assert validate_ledger_integrity(ledger) == []


# ---- Global Ledger Validation ----

class TestGlobalLedgerValidation:
    def test_valid_global_ledger_passes(self):
        ledger = _valid_global_ledger()
        assert validate_global_ledger_integrity(ledger) == []

    def test_detects_duplicate_active_dynamic_ids(self):
        dynamics = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test", countries_involved=["mx"],
            ),
            ActiveDynamic(
                dynamic_id=1, title="B", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test", countries_involved=["br"],
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=dynamics)
        errors = validate_global_ledger_integrity(ledger)
        assert any("Duplicate active dynamic IDs" in e for e in errors)

    def test_detects_active_archived_overlap(self):
        active = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test",
            ),
        ]
        archived = [
            ActiveDynamic(
                dynamic_id=1, title="A archived", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.RESOLVED,
                current_assessment="test",
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=active, archived_dynamics=archived)
        errors = validate_global_ledger_integrity(ledger)
        assert any("both active and archived" in e for e in errors)

    def test_detects_confidence_inheritance_violation(self):
        dynamics = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test",
                evidence_strength=EvidenceStrength(
                    confidence=4,
                    supporting_country_confidences={"mx": 3, "br": 2},
                ),
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=dynamics)
        errors = validate_global_ledger_integrity(ledger)
        assert any("exceeds lowest supporting country confidence" in e for e in errors)

    def test_valid_confidence_inheritance_passes(self):
        dynamics = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test",
                evidence_strength=EvidenceStrength(
                    confidence=2,
                    supporting_country_confidences={"mx": 3, "br": 2},
                ),
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=dynamics)
        errors = validate_global_ledger_integrity(ledger)
        assert not any("exceeds" in e for e in errors)

    def test_detects_invalid_country_codes(self):
        dynamics = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test",
                countries_involved=["Mexico"],  # Should be "mx"
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=dynamics)
        errors = validate_global_ledger_integrity(ledger)
        assert any("invalid country code 'Mexico'" in e for e in errors)

    def test_detects_out_of_order_global_entries(self):
        entries = [
            GlobalWeeklyEntry(
                week=date(2026, 3, 14),
                items_considered_rejected=[RejectedItem(candidate="x", reason_rejected="y")],
            ),
            GlobalWeeklyEntry(
                week=date(2026, 3, 7),
                items_considered_rejected=[RejectedItem(candidate="x", reason_rejected="y")],
            ),
        ]
        ledger = _valid_global_ledger(weekly_entries=entries)
        errors = validate_global_ledger_integrity(ledger)
        assert any("out of order" in e for e in errors)

    def test_valid_country_codes_pass(self):
        dynamics = [
            ActiveDynamic(
                dynamic_id=1, title="A", created_week=date(2026, 3, 7),
                last_updated=date(2026, 3, 14), status=DynamicStatus.EMERGING,
                current_assessment="test",
                countries_involved=["mx", "br"],
            ),
        ]
        ledger = _valid_global_ledger(active_dynamics=dynamics)
        errors = validate_global_ledger_integrity(ledger)
        assert not any("invalid country code" in e for e in errors)
