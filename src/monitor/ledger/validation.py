"""
Cross-reference validation for country and global ledgers.

These checks go beyond Pydantic field validation to verify referential integrity
across the ledger's internal structures.
"""

from ..config import SignalCategory, STALENESS_THRESHOLD_WEEKS
from ..models import CountryLedger, GlobalLedger


def validate_ledger_integrity(ledger: CountryLedger) -> list[str]:
    """
    Validate cross-references and internal consistency of a country ledger.

    Returns a list of error strings. Empty list means the ledger is valid.
    """
    errors = []

    # 1. All five signal categories present in assessments
    missing_cats = set(SignalCategory) - set(ledger.signal_categories.keys())
    if missing_cats:
        errors.append(f"Missing signal category assessments: {missing_cats}")

    # 2. All five signal categories present in posture summary
    missing_posture = set(SignalCategory) - set(ledger.posture_summary.category_status.keys())
    if missing_posture:
        errors.append(f"Missing posture category statuses: {missing_posture}")

    # 3. Structural claim refs are unique
    claim_refs = [c.claim_ref for c in ledger.structural_claim_status]
    dupes = [r for r in claim_refs if claim_refs.count(r) > 1]
    if dupes:
        errors.append(f"Duplicate structural claim refs: {set(dupes)}")

    # 4. Weekly entries are in chronological order
    weeks = [e.week for e in ledger.weekly_entries]
    for i in range(1, len(weeks)):
        if weeks[i] < weeks[i - 1]:
            errors.append(
                f"Weekly entries out of order: {weeks[i-1]} > {weeks[i]} at index {i}"
            )

    # 5. Consecutive maintenance weeks accuracy
    if ledger.weekly_entries:
        actual_consecutive = 0
        for entry in reversed(ledger.weekly_entries):
            if entry.depth.value == "maintenance":
                actual_consecutive += 1
            else:
                break
        recorded = ledger.posture_summary.consecutive_maintenance_weeks
        if recorded != actual_consecutive:
            errors.append(
                f"consecutive_maintenance_weeks mismatch: "
                f"recorded={recorded}, actual={actual_consecutive}"
            )

    # 6. Self-corrections in weekly entries reference valid categories
    for entry in ledger.weekly_entries:
        for sc in entry.self_corrections:
            if sc.category not in SignalCategory:
                errors.append(
                    f"Week {entry.week}: self-correction references unknown "
                    f"category {sc.category}"
                )
            if not sc.root_cause:
                errors.append(
                    f"Week {entry.week}: self-correction for {sc.category.value} "
                    f"missing root_cause"
                )

    # 7. Structural claim checks reference known claim refs
    known_refs = {c.claim_ref for c in ledger.structural_claim_status}
    for entry in ledger.weekly_entries:
        for check in entry.structural_claim_checks:
            if check.claim_ref not in known_refs:
                errors.append(
                    f"Week {entry.week}: claim check references unknown "
                    f"claim_ref '{check.claim_ref}'"
                )

    # 8. Corrections log entries reference valid categories
    for cl_entry in ledger.corrections_log:
        if cl_entry.category_affected not in SignalCategory:
            errors.append(
                f"Corrections log: unknown category {cl_entry.category_affected}"
            )

    return errors


def validate_global_ledger_integrity(ledger: GlobalLedger) -> list[str]:
    """
    Validate cross-references and internal consistency of the global ledger.

    Returns a list of error strings. Empty list means the ledger is valid.
    """
    errors = []

    # 1. Dynamic IDs are unique among active dynamics
    active_ids = [d.dynamic_id for d in ledger.active_dynamics]
    dupes = [i for i in active_ids if active_ids.count(i) > 1]
    if dupes:
        errors.append(f"Duplicate active dynamic IDs: {set(dupes)}")

    # 2. No overlap between active and archived dynamic IDs
    archived_ids = {d.dynamic_id for d in ledger.archived_dynamics}
    overlap = set(active_ids) & archived_ids
    if overlap:
        errors.append(f"Dynamic IDs in both active and archived: {overlap}")

    # 3. Confidence inheritance: dynamic confidence <= lowest supporting country confidence
    for d in ledger.active_dynamics:
        if d.evidence_strength.supporting_country_confidences:
            lowest = min(d.evidence_strength.supporting_country_confidences.values())
            if d.evidence_strength.confidence > lowest:
                errors.append(
                    f"Dynamic {d.dynamic_id} ({d.title}): confidence "
                    f"{d.evidence_strength.confidence} exceeds lowest supporting "
                    f"country confidence {lowest}"
                )

    # 4. Weekly entries in chronological order
    weeks = [e.week for e in ledger.weekly_entries]
    for i in range(1, len(weeks)):
        if weeks[i] < weeks[i - 1]:
            errors.append(
                f"Global weekly entries out of order: {weeks[i-1]} > {weeks[i]} "
                f"at index {i}"
            )

    # 5. Country codes in dynamics should be 2-letter lowercase
    import re
    code_pattern = re.compile(r"^[a-z]{2}$")
    for d in ledger.active_dynamics:
        for code in d.countries_involved:
            if not code_pattern.match(code):
                errors.append(
                    f"Dynamic {d.dynamic_id}: invalid country code '{code}'"
                )

    # 6. Triage implications reference valid country codes
    for d in ledger.active_dynamics:
        for code in d.triage_implications.countries_to_flag:
            if not code_pattern.match(code):
                errors.append(
                    f"Dynamic {d.dynamic_id} triage implications: "
                    f"invalid country code '{code}'"
                )

    return errors
