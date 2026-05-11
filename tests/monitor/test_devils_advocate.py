"""Tests for devil's advocate agent: prompt construction and response parsing."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    Movement,
    SignalCategory,
)
from src.monitor.agents.devils_advocate import (
    _build_devils_advocate_prompt,
    _build_system_prompt,
    parse_devils_advocate_response,
)
from src.monitor.models import (
    AbsenceCheck,
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    DevilsAdvocate,
    Development,
    PostureSummary,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    StructuralClaimStatus,
    UnexpectedDevelopment,
    WeeklyEntry,
)


def _test_entry() -> WeeklyEntry:
    """A realistic deep-dive entry for testing."""
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "Wire coverage on US confrontation."},
        category_movements={
            SignalCategory.ALIGNMENT_DIPLOMATIC: CategoryMovement(
                movement=Movement.SIGNIFICANT,
                developments=[
                    Development(
                        headline="Sheinbaum rejects US military proposal",
                        date=date(2026, 3, 12),
                        source="Reuters",
                        source_tier=2,
                        source_url="https://reuters.com/example",
                        summary="Rejection of US ops on Mexican soil.",
                        actors_involved=["Sheinbaum"],
                    ),
                ],
                prior_assessment="Defensive posture.",
                updated_assessment="Active confrontation.",
                confidence_change=ConfidenceChange(**{"from": 3, "to": 4, "reason": "Multiple sources."}),
            ),
            SignalCategory.SECURITY_DEFENSE: CategoryMovement(movement=Movement.NONE),
            SignalCategory.ECONOMIC_TECH: CategoryMovement(movement=Movement.NONE),
            SignalCategory.INSTITUTIONAL: CategoryMovement(movement=Movement.NONE),
            SignalCategory.DOMESTIC_REGIME: CategoryMovement(
                movement=Movement.MINOR,
                developments=[
                    Development(
                        headline="Morena internal poll shows declining support",
                        date=date(2026, 3, 10),
                        source="Animal Político",
                        source_tier=3,
                        summary="Internal party polling suggests erosion.",
                        actors_involved=["Morena"],
                    ),
                ],
                prior_assessment="Supermajority stable.",
                updated_assessment="First signals of internal strain.",
            ),
        },
        unexpected_developments=[
            UnexpectedDevelopment(
                headline="CJNG successor named",
                date=date(2026, 3, 11),
                source="Proceso",
                source_tier=3,
                signal_category=SignalCategory.SECURITY_DEFENSE,
                assessment="Could reshape cartel dynamics.",
            ),
        ],
        absence_check=[
            AbsenceCheck(
                expected="USMCA review statement",
                signal_category=SignalCategory.ECONOMIC_TECH,
                occurred=False,
                significance="Silence may indicate negotiations.",
                confidence=2,
            ),
        ],
        structural_claim_checks=[
            StructuralClaimCheck(
                claim_ref="STRUC-05",
                claim_text="US-Mexico border is a hard constraint.",
                status="confirmed",
                evidence="Tariff threats reinforce dependency.",
                confidence_in_claim=4,
            ),
        ],
    )


class TestBuildPrompt:
    def test_includes_country(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "Mexico" in prompt

    def test_includes_category_assessments(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "alignment_diplomatic" in prompt
        assert "significant" in prompt
        assert "Active confrontation" in prompt

    def test_includes_development_details(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "Sheinbaum rejects US military proposal" in prompt
        assert "Reuters" in prompt
        assert "tier 2" in prompt

    def test_includes_confidence_changes(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "3 → 4" in prompt

    def test_includes_unexpected_developments(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "CJNG successor" in prompt

    def test_includes_absence_checks(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "USMCA" in prompt
        assert "did NOT occur" in prompt

    def test_includes_structural_claims(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "STRUC-05" in prompt

    def test_includes_single_source_developments(self):
        """Devil's advocate should see single-source info to flag it."""
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        # Morena poll from Tier 3 Animal Político — single source
        assert "Animal Político" in prompt
        assert "tier 3" in prompt


class TestParseResponse:
    VALID_RESPONSE = json.dumps({
        "challenges": [
            "The alignment_diplomatic upgrade from 3 to 4 rests on Reuters coverage "
            "of the Sheinbaum rejection, but this may be routine sovereignty rhetoric "
            "rather than a genuine policy escalation.",
            "The domestic_regime assessment of 'first signals of internal strain' relies "
            "on a single Tier 3 source (Animal Político internal poll). Internal party "
            "polls are notoriously unreliable and may reflect factional messaging.",
            "The CJNG successor report from Proceso (Tier 3) is unconfirmed. Cartel "
            "succession claims frequently prove premature or wrong.",
        ],
        "recommended_adjustments": [
            "Downgrade alignment_diplomatic confidence from 4 to 3 until a second "
            "independent source confirms the rejection represents policy, not rhetoric.",
            "Flag domestic_regime assessment as single-source. Do not upgrade from "
            "'routine' to 'active' until corroborated by a second outlet.",
            "Mark CJNG successor report as unverified in the unexpected developments "
            "section. Cap any downstream confidence at 2.",
        ],
    })

    def test_parses_valid_response(self):
        da = parse_devils_advocate_response(self.VALID_RESPONSE)
        assert len(da.challenges) == 3
        assert len(da.recommended_adjustments) == 3

    def test_challenges_are_substantive(self):
        da = parse_devils_advocate_response(self.VALID_RESPONSE)
        # Each challenge references specific evidence
        assert any("Reuters" in c for c in da.challenges)
        assert any("Animal Político" in c for c in da.challenges)

    def test_adjustments_are_actionable(self):
        da = parse_devils_advocate_response(self.VALID_RESPONSE)
        assert any("downgrade" in a.lower() for a in da.recommended_adjustments)
        assert any("single-source" in a.lower() for a in da.recommended_adjustments)

    def test_strips_markdown_fencing(self):
        fenced = f"```json\n{self.VALID_RESPONSE}\n```"
        da = parse_devils_advocate_response(fenced)
        assert len(da.challenges) == 3

    def test_empty_challenges_parses(self):
        response = json.dumps({"challenges": [], "recommended_adjustments": []})
        da = parse_devils_advocate_response(response)
        assert da.challenges == []
        assert da.recommended_adjustments == []

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_devils_advocate_response("not json")

    def test_parses_wrapped_format(self):
        """Spec wraps output in {"devils_advocate": {...}}."""
        wrapped = json.dumps({
            "devils_advocate": {
                "challenges": ["Challenge 1"],
                "recommended_adjustments": ["Adjust 1"],
            }
        })
        da = parse_devils_advocate_response(wrapped)
        assert len(da.challenges) == 1
        assert da.challenges[0] == "Challenge 1"

    def test_attaches_to_weekly_entry(self):
        """Verify the parsed output can be attached to a weekly entry."""
        da = parse_devils_advocate_response(self.VALID_RESPONSE)
        entry = _test_entry()
        entry.devils_advocate = da
        assert entry.validate_complete() == []


# ---- System Prompt ----

class TestSystemPrompt:
    def test_is_country_agnostic_and_stable(self):
        """The devil's advocate system prompt is country-agnostic so it
        cache-hits across all parallel country reviews in a weekly run.
        Calling _build_system_prompt() repeatedly must return the same
        byte string; no template variables should remain."""
        p1 = _build_system_prompt()
        p2 = _build_system_prompt()
        assert p1 == p2
        assert "{{" not in p1
        assert "}}" not in p1

    def test_does_not_name_specific_countries(self):
        prompt = _build_system_prompt()
        for name in ("Mexico", "Japan", "Germany", "Brazil", "Indonesia"):
            assert name not in prompt, f"system prompt leaks country name: {name}"

    def test_contains_review_criteria(self):
        prompt = _build_system_prompt()
        assert "Source Dependency" in prompt
        assert "Narrative Persistence" in prompt
        assert "Confidence Calibration" in prompt
        assert "Alternative Interpretations" in prompt
        assert "Structural Claim Checks" in prompt
        assert "What's Missing" in prompt


# ---- Ledger Context ----

def _test_ledger() -> CountryLedger:
    return CountryLedger(
        country="Mexico",
        code="mx",
        tier="periphery",
        actors=[ActorRef(name="Sheinbaum", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text="Mexico navigates US proximity.",
            category_status={c: CategoryStatus.QUIET for c in SignalCategory},
            consecutive_maintenance_weeks=0,
        ),
        signal_categories={
            c: SignalCategoryAssessment(
                current_assessment=f"Baseline for {c.value}",
                confidence=3,
                last_updated=date(2026, 3, 7),
            )
            for c in SignalCategory
        },
        structural_claim_status=[
            StructuralClaimStatus(
                claim_ref="STRUC-05",
                claim_text="US-Mexico border is a hard constraint.",
                dossier_section=2,
                status=ClaimStatus.UNDER_PRESSURE,
                last_checked=date(2026, 3, 7),
                weeks_under_pressure=2,
            ),
        ],
    )


class TestLedgerContext:
    def test_includes_prior_assessments(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico", _test_ledger())
        assert "COUNTRY LEDGER CONTEXT" in prompt
        assert "Prior Signal Category Assessments" in prompt
        assert "Baseline for alignment_diplomatic" in prompt

    def test_includes_structural_claim_status(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico", _test_ledger())
        assert "STRUC-05" in prompt
        assert "under_pressure" in prompt
        assert "2 weeks" in prompt

    def test_works_without_ledger(self):
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico")
        assert "Mexico" in prompt
        assert "COUNTRY LEDGER CONTEXT" not in prompt

    def test_includes_prior_da_challenges(self):
        ledger = _test_ledger()
        prior_entry = WeeklyEntry(
            week=date(2026, 3, 7),
            date_range="w0",
            depth=Depth.DEEP_DIVE,
            category_movements={c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory},
            devils_advocate=DevilsAdvocate(
                challenges=["Prior challenge about single-source dependency."],
            ),
        )
        ledger.weekly_entries = [prior_entry]
        prompt = _build_devils_advocate_prompt(_test_entry(), "Mexico", ledger)
        assert "Prior challenge about single-source dependency" in prompt
