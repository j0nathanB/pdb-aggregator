"""
Tests for claims extraction from country dossiers and leader profiles.

Tests against the Mexico sample documents in docs/samples/.
"""

from pathlib import Path

import pytest

from src.context.claims import (
    Claim,
    extract_claims,
    format_claims_index,
    get_valid_claim_refs,
)

SAMPLES_DIR = Path(__file__).parent.parent / "docs" / "samples"


@pytest.fixture
def mexico_dossier():
    return (SAMPLES_DIR / "country_sample_mexico.md").read_text()


@pytest.fixture
def mexico_profile():
    return (SAMPLES_DIR / "leader_sample_mexico.md").read_text()


class TestExtractClaims:
    """Test extraction from real sample documents."""

    def test_structural_claims_count(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        assert len(claims) == 29

    def test_profile_claims_count(self, mexico_profile):
        claims = extract_claims(mexico_profile, "PROF")
        assert len(claims) == 25

    def test_structural_ref_format(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        assert claims[0].ref == "[STRUC-01]"
        assert claims[-1].ref == "[STRUC-29]"

    def test_profile_ref_format(self, mexico_profile):
        claims = extract_claims(mexico_profile, "PROF")
        assert claims[0].ref == "[PROF-01]"
        assert claims[-1].ref == "[PROF-25]"

    def test_sequential_numbering(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        refs = [c.ref for c in claims]
        expected = [f"[STRUC-{i:02d}]" for i in range(1, 30)]
        assert refs == expected

    def test_confidence_extraction(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        # First claim is HIGH CONFIDENCE
        assert claims[0].confidence == "HIGH CONFIDENCE"
        # Count confidence levels
        high = sum(1 for c in claims if c.confidence == "HIGH CONFIDENCE")
        moderate = sum(1 for c in claims if c.confidence == "MODERATE CONFIDENCE")
        assessed = sum(1 for c in claims if c.confidence == "ASSESSED")
        assert high == 23
        assert moderate == 5
        assert assessed == 1

    def test_profile_confidence(self, mexico_profile):
        claims = extract_claims(mexico_profile, "PROF")
        high = sum(1 for c in claims if c.confidence == "HIGH CONFIDENCE")
        moderate = sum(1 for c in claims if c.confidence == "MODERATE CONFIDENCE")
        assessed = sum(1 for c in claims if c.confidence == "ASSESSED")
        assert high == 14
        assert moderate == 8
        assert assessed == 3

    def test_text_cleanliness(self, mexico_dossier, mexico_profile):
        """Confidence markers and formatting artifacts should be stripped."""
        for claim in extract_claims(mexico_dossier, "STRUC"):
            assert "**" not in claim.text
            assert "[HIGH CONFIDENCE]" not in claim.text
            assert "[MODERATE CONFIDENCE]" not in claim.text
            assert "[ASSESSED]" not in claim.text

        for claim in extract_claims(mexico_profile, "PROF"):
            assert "**" not in claim.text
            assert "[HIGH CONFIDENCE]" not in claim.text
            assert "[MODERATE CONFIDENCE]" not in claim.text

    def test_text_ends_with_period(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        for claim in claims:
            assert claim.text.endswith("."), f"{claim.ref} text doesn't end with period: ...{claim.text[-20:]}"

    def test_section_populated(self, mexico_dossier):
        claims = extract_claims(mexico_dossier, "STRUC")
        for claim in claims:
            assert claim.section, f"{claim.ref} has empty section"

    def test_empty_document(self):
        claims = extract_claims("", "STRUC")
        assert claims == []

    def test_no_claims_blocks(self):
        text = "# Some Document\n\nJust regular text without claims.\n"
        claims = extract_claims(text, "STRUC")
        assert claims == []


class TestFormatClaimsIndex:
    def test_basic_format(self):
        struc = [
            Claim(ref="[STRUC-01]", text="First claim.", confidence="HIGH CONFIDENCE", section="S1"),
            Claim(ref="[STRUC-02]", text="Second claim.", confidence="MODERATE CONFIDENCE", section="S1"),
        ]
        prof = [
            Claim(ref="[PROF-01]", text="Profile claim one.", confidence="HIGH CONFIDENCE", section="P1"),
        ]
        result = format_claims_index(struc, prof, "Mexico", "Claudia Sheinbaum")

        assert "## CLAIMS INDEX (for reference)" in result
        assert "### Country Structural Claims (Mexico)" in result
        assert "### Leader Profile Claims (Claudia Sheinbaum)" in result
        assert "[STRUC-01]: First claim." in result
        assert "[STRUC-02]: Second claim." in result
        assert "[PROF-01]: Profile claim one." in result

    def test_empty_claims(self):
        result = format_claims_index([], [], "Mexico", "Sheinbaum")
        assert "[No structural claims available]" in result
        assert "[No profile claims available]" in result

    def test_with_real_data(self, mexico_dossier, mexico_profile):
        struc = extract_claims(mexico_dossier, "STRUC")
        prof = extract_claims(mexico_profile, "PROF")
        result = format_claims_index(struc, prof, "Mexico", "Claudia Sheinbaum")

        assert "[STRUC-01]:" in result
        assert "[STRUC-29]:" in result
        assert "[PROF-01]:" in result
        assert "[PROF-25]:" in result


class TestGetValidClaimRefs:
    def test_valid_refs(self, mexico_dossier, mexico_profile):
        struc = extract_claims(mexico_dossier, "STRUC")
        prof = extract_claims(mexico_profile, "PROF")
        refs = get_valid_claim_refs(struc, prof)

        assert "[STRUC-01]" in refs
        assert "[STRUC-29]" in refs
        assert "[PROF-01]" in refs
        assert "[PROF-25]" in refs
        assert "[STRUC-30]" not in refs
        assert "[PROF-26]" not in refs
        assert len(refs) == 54  # 29 + 25

    def test_empty(self):
        refs = get_valid_claim_refs([], [])
        assert refs == set()
