"""Tests for ledger initialization: mechanical extraction and LLM response parsing."""

import json
from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    SignalCategory,
    load_country_config,
)
from src.monitor.ledger.initialize import (
    extract_structural_claims,
    mechanical_extract,
    parse_init_response,
)


# ---- Mechanical Extraction ----

class TestExtractStructuralClaims:
    @pytest.fixture
    def mexico_dossier(self):
        config = load_country_config("mx")
        return config.dossier_path.read_text()

    def test_extracts_claims_from_mexico(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        assert len(claims) >= 20  # Mexico has ~29 claims

    def test_claim_ref_format(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        for c in claims:
            assert c["claim_ref"].startswith("STRUC-")
            # Verify two-digit numbering
            num = c["claim_ref"].split("-")[1]
            assert len(num) == 2

    def test_claim_has_required_fields(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        for c in claims:
            assert "claim_ref" in c
            assert "claim_text" in c
            assert "dossier_section" in c
            assert "status" in c
            assert c["status"] == ClaimStatus.CONFIRMED

    def test_dossier_sections_are_integers(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        for c in claims:
            assert isinstance(c["dossier_section"], int)

    def test_claims_span_multiple_sections(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        sections = {c["dossier_section"] for c in claims}
        assert len(sections) >= 3  # Should span many dossier sections

    def test_claim_text_not_empty(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        for c in claims:
            assert len(c["claim_text"]) > 10

    def test_empty_dossier_yields_no_claims(self):
        claims = extract_structural_claims("# Empty Dossier\n\nNo claims here.")
        assert claims == []

    def test_confidence_markers_stripped(self, mexico_dossier):
        claims = extract_structural_claims(mexico_dossier)
        for c in claims:
            assert "HIGH CONFIDENCE" not in c["claim_text"]
            assert "MODERATE CONFIDENCE" not in c["claim_text"]


class TestMechanicalExtract:
    def test_produces_valid_skeleton(self):
        config = load_country_config("mx")
        skeleton = mechanical_extract(config)
        assert skeleton["country"] == "Mexico"
        assert skeleton["code"] == "mx"
        assert skeleton["tier"] == "periphery"
        assert len(skeleton["actors"]) == 10
        assert len(skeleton["structural_claim_status"]) >= 20
        assert skeleton["weekly_entries"] == []
        assert skeleton["corrections_log"] == []

    def test_actors_match_config(self):
        config = load_country_config("mx")
        skeleton = mechanical_extract(config)
        actor_names = {a.name for a in skeleton["actors"]}
        assert "Claudia Sheinbaum" in actor_names
        assert "SEDENA" in actor_names

    def test_primary_actor_preserved(self):
        config = load_country_config("mx")
        skeleton = mechanical_extract(config)
        primaries = [a for a in skeleton["actors"] if a.primary]
        assert len(primaries) >= 1
        assert primaries[0].name == "Claudia Sheinbaum"

    def test_dates_set_to_today(self):
        config = load_country_config("mx")
        skeleton = mechanical_extract(config)
        today = date.today()
        assert skeleton["last_updated"] == today
        assert skeleton["created"] == today


# ---- LLM Response Parsing ----

class TestParseInitResponse:
    VALID_RESPONSE = json.dumps({
        "posture_text": "Mexico is a middle-income country navigating US proximity. "
                        "The Sheinbaum administration governs with a supermajority. "
                        "Security challenges from cartel fragmentation dominate.",
        "categories": {
            "alignment_diplomatic": {
                "current_assessment": "Mexico maintains a defensive posture toward the US "
                                     "while seeking limited diversification.",
                "confidence_rationale": "Baseline from dossier, not yet tested.",
            },
            "security_defense": {
                "current_assessment": "Military expansion under 4T continues. "
                                     "Cartel fragmentation creates instability.",
                "confidence_rationale": "Baseline from dossier.",
            },
            "economic_tech": {
                "current_assessment": "USMCA dependency structures economic positioning. "
                                     "Nearshoring creates opportunity.",
                "confidence_rationale": "Baseline from dossier.",
            },
            "institutional": {
                "current_assessment": "Judicial reform reshapes institutional landscape. "
                                     "Multilateral engagement selective.",
                "confidence_rationale": "Baseline from dossier.",
            },
            "domestic_regime": {
                "current_assessment": "Morena supermajority enables constitutional changes. "
                                     "Opposition structurally weakened.",
                "confidence_rationale": "Baseline from dossier.",
            },
        },
    })

    def test_parses_valid_response(self):
        result = parse_init_response(self.VALID_RESPONSE)
        assert "posture_summary" in result
        assert "signal_categories" in result

    def test_posture_summary_fields(self):
        result = parse_init_response(self.VALID_RESPONSE)
        ps = result["posture_summary"]
        assert "Mexico" in ps.text
        assert ps.as_of == date.today()
        assert ps.consecutive_maintenance_weeks == 0
        assert ps.last_deep_dive is None
        # All categories present in status
        assert len(ps.category_status) == 5

    def test_all_five_categories(self):
        result = parse_init_response(self.VALID_RESPONSE)
        cats = result["signal_categories"]
        assert set(cats.keys()) == set(SignalCategory)

    def test_baseline_confidence_is_3(self):
        result = parse_init_response(self.VALID_RESPONSE)
        for cat, assessment in result["signal_categories"].items():
            assert assessment.confidence == 3

    def test_category_status_defaults_to_quiet(self):
        result = parse_init_response(self.VALID_RESPONSE)
        ps = result["posture_summary"]
        for cat, status in ps.category_status.items():
            assert status == CategoryStatus.QUIET

    def test_strips_markdown_fencing(self):
        fenced = f"```json\n{self.VALID_RESPONSE}\n```"
        result = parse_init_response(fenced)
        assert "posture_summary" in result

    def test_invalid_json_raises(self):
        with pytest.raises((json.JSONDecodeError, ValueError)):
            parse_init_response("not json at all")

    def test_missing_category_raises(self):
        data = json.loads(self.VALID_RESPONSE)
        del data["categories"]["domestic_regime"]
        with pytest.raises(KeyError):
            parse_init_response(json.dumps(data))

    def test_roundtrip_to_country_ledger(self):
        """Verify that parsed output + mechanical skeleton produces a valid ledger."""
        from src.monitor.models import CountryLedger
        config = load_country_config("mx")
        skeleton = mechanical_extract(config)
        llm_output = parse_init_response(self.VALID_RESPONSE)
        skeleton["posture_summary"] = llm_output["posture_summary"]
        skeleton["signal_categories"] = llm_output["signal_categories"]
        ledger = CountryLedger(**skeleton)
        assert ledger.code == "mx"
        assert len(ledger.signal_categories) == 5
        assert len(ledger.structural_claim_status) >= 20
