"""
Tests for running picture infrastructure (v3 schema).

Covers schema parsing, storage, validation, and thread/commitment extraction.
"""

import textwrap
from pathlib import Path

import pytest

from src.running_picture.schema import (
    RunningPictureEntry,
    ConsolidationSummary,
    leader_slug,
    parse_frontmatter,
    parse_entry,
    parse_consolidation,
    parse_sections,
)
from src.running_picture.storage import (
    load_weekly_entries,
    load_weekly_text,
    save_weekly_entry,
    load_consolidation,
    save_consolidation,
    load_dormant_threads,
    save_dormant_threads,
    entry_count,
    archive_old_entries,
)
from src.running_picture.validation import validate_entry, ValidationResult
from src.running_picture.extraction import (
    extract_thread_checklist,
    format_thread_checklist,
    extract_commitment_ledger,
    format_commitment_ledger,
)


# =============================================================================
# FIXTURES
# =============================================================================

VALID_ENTRY_V3 = textwrap.dedent("""\
    ---
    leader: Claudia Sheinbaum
    country: Mexico
    week_of: 2026-03-02
    generated_at: 2026-03-06T10:00:00
    event_count: 5
    source_count: 12
    ---

    ### Activity Level
    High
    Dominated by USMCA review preparations and bilateral meeting with Canadian PM.

    ### Key Actions
    1. 2026-03-03 BILATERAL MEETING: Met with Canadian PM Carney in Mexico City to coordinate USMCA review positions.
       Source: Reuters
       Significance: Strengthens trilateral coordination ahead of July review [STRUC-05]

    2. 2026-03-05 POLICY ANNOUNCEMENT: Announced Plan Mexico Phase 2 with $50B infrastructure package.
       Source: El Financiero
       Significance: Continues nearshoring strategy to reduce US dependency [PROF-12]

    ### Commitments & Positions
    - [USMCA coordination with Canada]: Pledged joint position paper on automotive rules of origin for April ministerial.
      Status: NEW
      Audience: Bilateral meeting
      Binding force: MODERATE (public pledge to international audience)

    - [Plan Mexico expansion]: Committed to 45% renewable electricity by 2030.
      Status: REINFORCED
      Audience: Domestic press conference
      Binding force: LOW (domestic rhetoric, aspirational statement)

    ### Relationships
    - Bilateral meeting with Mark Carney (Canada): In-person bilateral in Mexico City, focused on USMCA joint strategy. Joint communique issued.
      Assessment: Significant warming from early friction; shared concern over US tariff posture driving convergence.

    ### Domestic Political Position
    No material change this week.

    ### Developing Threads

    ACTIVE THREADS:
    - [USMCA review preparation]: Joint Mexico-Canada position paper in development. US signals may withhold renewal.
      Watch for: April ministerial meeting; USTR draft demands
      Originated: 2026-01-13
      Last updated: This week

    - [Post-El Mencho cartel realignment]: CJNG fragmentation ongoing. Violence declined from peak but remains elevated in Jalisco, Michoacan.
      Watch for: Emergence of successor leadership; territorial shifts between CJNG fragments and Sinaloa
      Originated: 2026-02-24
      Last updated: This week

    DORMANT THREADS:
    - [Cuba oil policy]: Paused shipments under US pressure in January. No developments since.
      Dormant since: 2026-02-10
      Reactivation trigger: Resumption of shipments or new Trump pressure on Cuba

    ### Missing Thread Audit
    - [USMCA review preparation]: ACTIVE — updated with Canada bilateral developments
    - [Post-El Mencho cartel realignment]: ACTIVE — updated with declining violence trajectory
    - [Cuba oil policy]: DORMANT — no new developments, maintained as dormant

    ### Structural Claim Check
    - [STRUC-05]: REINFORCED
      Evidence: Canada bilateral on USMCA coordination aligns with structural claim about Mexico's trade dependency creating alliance imperatives.
      Recommendation: No update needed.

    - [PROF-12]: REINFORCED
      Evidence: Plan Mexico Phase 2 continues the nearshoring/diversification strategy described in profile.
      Recommendation: No update needed.

    ### Analytical Notes
    The Canada bilateral marks a significant evolution — from early mutual suspicion (Canada initially sought separate USMCA deal) to coordinated positioning. This convergence is driven by shared structural exposure to US tariff policy rather than ideological alignment. The speed of this pivot suggests both governments assess the USMCA review risk as materially higher than public rhetoric indicates.""")


VALID_ENTRY_V3_OLDER = textwrap.dedent("""\
    ---
    leader: Claudia Sheinbaum
    country: Mexico
    week_of: 2026-02-24
    generated_at: 2026-02-28T10:00:00
    event_count: 8
    source_count: 20
    ---

    ### Activity Level
    High
    Dominated by El Mencho killing and nationwide cartel retaliation.

    ### Key Actions
    1. 2026-02-23 SECURITY OPERATION: Military killed CJNG leader El Mencho in Jalisco operation with US intelligence support.
       Source: Reuters
       Significance: Definitive break from AMLO's "abrazos no balazos" doctrine [PROF-21]

    ### Commitments & Positions
    - [Security crackdown continuation]: Pledged sustained operations against cartel leadership.
      Status: NEW
      Audience: Domestic press conference
      Binding force: HIGH (backed by military operational commitment)

    ### Relationships
    - Intelligence coordination with US: Joint operation producing El Mencho killing. Deepest US-Mexico security cooperation of Sheinbaum presidency.
      Assessment: Operational cooperation exceeds public rhetoric on sovereignty.

    ### Domestic Political Position
    - Approval surge: Rally-around-flag effect from El Mencho operation, though insecurity remains top public concern.

    ### Developing Threads

    ACTIVE THREADS:
    - [USMCA review preparation]: Preparations ongoing. Canada bilateral planned for next week.
      Watch for: April ministerial meeting
      Originated: 2026-01-13
      Last updated: This week

    - [Post-El Mencho cartel realignment]: CJNG retaliatory violence across 20 states. 250+ roadblocks in first 48 hours.
      Watch for: Emergence of successor leadership; fragmentation vs clean succession
      Originated: 2026-02-24
      Last updated: This week

    - [Cuba oil policy]: Paused shipments under US pressure.
      Watch for: Any resumption or new Trump pressure
      Originated: 2026-01-27
      Last updated: 2026-02-10

    ### Missing Thread Audit
    - [USMCA review preparation]: ACTIVE — ongoing
    - [Cuba oil policy]: ACTIVE — no change this week, will move to DORMANT if no activity by next entry

    ### Structural Claim Check
    - [PROF-21]: CHALLENGED
      Evidence: El Mencho operation represents clear departure from the non-confrontational security posture described in the profile baseline.
      Recommendation: Profile Section 7 (crisis behavior) should be updated to reflect this new operational doctrine.

    ### Analytical Notes
    The El Mencho operation is the single most consequential security decision of Sheinbaum's presidency. It signals a fundamental reorientation of security strategy — from AMLO's containment approach to active decapitation targeting.""")


MINIMAL_ENTRY_V3 = textwrap.dedent("""\
    ---
    leader: Test Leader
    country: Testland
    week_of: 2026-01-05
    generated_at: 2026-01-09T10:00:00
    event_count: 0
    source_count: 0
    ---

    ### Activity Level
    Quiet
    No significant developments.

    ### Key Actions
    [No significant actions this week.]

    ### Commitments & Positions
    [No new commitments.]

    ### Relationships
    [No significant interactions.]

    ### Domestic Political Position
    No material change this week.

    ### Developing Threads
    [No active threads.]

    ### Missing Thread Audit
    [No threads from prior entry.]

    ### Structural Claim Check
    No structural or profile claims materially affected.

    ### Analytical Notes
    Inaugural entry. No running context for trajectory analysis.""")


CONSOLIDATION_SAMPLE = textwrap.dedent("""\
    ---
    leader: Claudia Sheinbaum
    country: Mexico
    period: 2026-01-06 to 2026-02-03
    generated_at: 2026-02-07T10:00:00
    consolidates_entries: 2026-01-06, 2026-01-13, 2026-01-20, 2026-01-27
    ---

    ### Period Trajectory
    First month of 2026 defined by escalating US trade pressure and the Cuba oil
    policy reversal. Sheinbaum consolidated the "cool head" doctrine established
    in late 2025 into a systematic negotiating framework.

    ### Stable Assessments
    1. Trump management via absorb-then-engage pattern remains consistent (weeks 1-4).
    2. Plan Mexico rhetoric outpaces implementation capacity (weeks 2-3).

    ### Resolved Threads
    - [Tariff pause negotiation]: Resolved. 90-day pause secured January 15.

    ### Escalated Threads
    - [USMCA review preparation]: Elevated from routine to high priority after USTR signals.

    ### Newly Dormant Threads
    - [G20 follow-up]: No developments since November summit.
      Reactivation trigger: New multilateral initiative or Brazilian outreach.

    ### Commitment Ledger Update
    Active commitments: USMCA coordination, Plan Mexico Phase 1, tariff retaliation (delayed).

    ### Structural Claim Status
    - [STRUC-05]: Flagged 2 times — MONITOR

    ### Analytical Inertia Check
    - "Cool head doctrine is effective": VALIDATED — four consecutive crises managed successfully.

    ### Slow-Burn Review
    No slow-burn deviations detected. The Cuba oil reversal was correctly flagged in real time.""")


# =============================================================================
# SCHEMA TESTS
# =============================================================================


class TestLeaderSlug:
    def test_basic(self):
        assert leader_slug("Claudia Sheinbaum") == "claudia_sheinbaum"

    def test_special_chars(self):
        assert leader_slug("Evika Siliņa") == "evika_siliņa"


class TestFrontmatter:
    def test_extract(self):
        fm = parse_frontmatter(VALID_ENTRY_V3)
        assert fm["leader"] == "Claudia Sheinbaum"
        assert fm["country"] == "Mexico"
        assert fm["week_of"] == "2026-03-02"
        assert fm["event_count"] == "5"

    def test_missing(self):
        assert parse_frontmatter("no frontmatter") is None

    def test_empty_block(self):
        assert parse_frontmatter("---\n---\ncontent") == {}


class TestParseEntry:
    def test_valid_v3(self):
        entry = parse_entry(VALID_ENTRY_V3)
        assert entry.leader == "Claudia Sheinbaum"
        assert entry.country == "Mexico"
        assert entry.week_of == "2026-03-02"
        assert entry.event_count == 5
        assert "High" in entry.activity_level
        assert "BILATERAL MEETING" in entry.key_actions
        assert "Audience:" in entry.commitments
        assert "Binding force:" in entry.commitments

    def test_developing_threads_parsed(self):
        entry = parse_entry(VALID_ENTRY_V3)
        assert "ACTIVE THREADS:" in entry.developing_threads
        assert "DORMANT THREADS:" in entry.developing_threads
        assert "Cuba oil policy" in entry.developing_threads

    def test_missing_thread_audit(self):
        entry = parse_entry(VALID_ENTRY_V3)
        assert "USMCA review preparation" in entry.missing_thread_audit
        assert "ACTIVE" in entry.missing_thread_audit

    def test_no_frontmatter_raises(self):
        with pytest.raises(ValueError):
            parse_entry("just text with no frontmatter")


class TestParseConsolidation:
    def test_valid(self):
        consol = parse_consolidation(CONSOLIDATION_SAMPLE)
        assert consol.leader == "Claudia Sheinbaum"
        assert consol.period_start == "2026-01-06"
        assert consol.period_end == "2026-02-03"
        assert len(consol.consolidates_entries) == 4
        assert "cool head" in consol.period_trajectory.lower()
        assert "Tariff pause" in consol.resolved_threads


# =============================================================================
# STORAGE TESTS
# =============================================================================


class TestStorage:
    def test_save_and_load(self, tmp_path):
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)

        entries = load_weekly_entries("Claudia Sheinbaum", base_dir=tmp_path)
        assert len(entries) == 1
        assert entries[0].leader == "Claudia Sheinbaum"
        assert entries[0].week_of == "2026-03-02"

    def test_ordering(self, tmp_path):
        save_weekly_entry("Claudia Sheinbaum", "2026-02-24", VALID_ENTRY_V3_OLDER, base_dir=tmp_path)
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)

        entries = load_weekly_entries("Claudia Sheinbaum", base_dir=tmp_path)
        assert len(entries) == 2
        assert entries[0].week_of == "2026-03-02"  # Most recent first
        assert entries[1].week_of == "2026-02-24"

    def test_max_entries(self, tmp_path):
        save_weekly_entry("Claudia Sheinbaum", "2026-01-05", MINIMAL_ENTRY_V3, base_dir=tmp_path)
        save_weekly_entry("Claudia Sheinbaum", "2026-02-24", VALID_ENTRY_V3_OLDER, base_dir=tmp_path)
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)

        entries = load_weekly_entries("Claudia Sheinbaum", max_entries=2, base_dir=tmp_path)
        assert len(entries) == 2

    def test_load_nonexistent(self, tmp_path):
        assert load_weekly_entries("Nobody", base_dir=tmp_path) == []

    def test_load_text(self, tmp_path):
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)
        text = load_weekly_text("Claudia Sheinbaum", base_dir=tmp_path)
        assert "### Key Actions" in text
        assert "Claudia Sheinbaum" in text

    def test_load_text_empty(self, tmp_path):
        assert load_weekly_text("Nobody", base_dir=tmp_path) == ""

    def test_entry_count(self, tmp_path):
        assert entry_count("Claudia Sheinbaum", base_dir=tmp_path) == 0
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)
        assert entry_count("Claudia Sheinbaum", base_dir=tmp_path) == 1

    def test_consolidation_roundtrip(self, tmp_path):
        save_consolidation("Claudia Sheinbaum", "2026-02-03", CONSOLIDATION_SAMPLE, base_dir=tmp_path)
        consol = load_consolidation("Claudia Sheinbaum", base_dir=tmp_path)
        assert consol is not None
        assert consol.leader == "Claudia Sheinbaum"
        assert "cool head" in consol.period_trajectory.lower()

    def test_consolidation_none(self, tmp_path):
        assert load_consolidation("Nobody", base_dir=tmp_path) is None

    def test_dormant_threads_roundtrip(self, tmp_path):
        text = "- [G20 follow-up]: Dormant since 2025-11\n"
        save_dormant_threads("Claudia Sheinbaum", text, base_dir=tmp_path)
        loaded = load_dormant_threads("Claudia Sheinbaum", base_dir=tmp_path)
        assert "G20 follow-up" in loaded

    def test_archive(self, tmp_path):
        for i in range(6):
            date = f"2026-01-{(i+1)*7:02d}"
            save_weekly_entry("Claudia Sheinbaum", date, MINIMAL_ENTRY_V3, base_dir=tmp_path)

        assert entry_count("Claudia Sheinbaum", base_dir=tmp_path) == 6
        archived = archive_old_entries("Claudia Sheinbaum", keep=4, base_dir=tmp_path)
        assert len(archived) == 2
        assert entry_count("Claudia Sheinbaum", base_dir=tmp_path) == 4

    def test_directory_structure(self, tmp_path):
        save_weekly_entry("Claudia Sheinbaum", "2026-03-02", VALID_ENTRY_V3, base_dir=tmp_path)
        expected_path = tmp_path / "weekly" / "claudia_sheinbaum" / "2026-03-02.md"
        assert expected_path.exists()


# =============================================================================
# VALIDATION TESTS
# =============================================================================


class TestValidation:
    def test_valid_entry(self):
        result = validate_entry(VALID_ENTRY_V3)
        assert result.valid, f"Errors: {result.errors}"

    def test_missing_frontmatter(self):
        result = validate_entry("### Activity Level\nHigh")
        assert not result.valid
        assert any("frontmatter" in e.lower() for e in result.errors)

    def test_missing_section(self):
        broken = VALID_ENTRY_V3.replace("### Missing Thread Audit", "### Audit")
        result = validate_entry(broken)
        assert not result.valid
        assert any("Missing Thread Audit" in e for e in result.errors)

    def test_minimal_valid(self):
        result = validate_entry(MINIMAL_ENTRY_V3)
        assert result.valid, f"Errors: {result.errors}"

    def test_invalid_week_of(self):
        bad = VALID_ENTRY_V3.replace("week_of: 2026-03-02", "week_of: March 2")
        result = validate_entry(bad)
        assert not result.valid

    def test_key_actions_missing_source(self):
        bad = VALID_ENTRY_V3.replace("Source: Reuters", "").replace("Source: El Financiero", "")
        result = validate_entry(bad)
        assert any("Source" in e for e in result.errors)

    def test_thread_audit_count_check(self):
        # Entry has 3 threads but audit should match
        result = validate_entry(VALID_ENTRY_V3, prior_thread_count=3)
        assert result.valid

    def test_thread_audit_count_mismatch(self):
        result = validate_entry(VALID_ENTRY_V3, prior_thread_count=10)
        assert any("Missing Thread Audit" in w for w in result.warnings)

    def test_claim_validation(self):
        valid_claims = {"[STRUC-05]", "[PROF-12]"}
        result = validate_entry(VALID_ENTRY_V3, valid_claims=valid_claims)
        assert result.valid

    def test_invalid_claim_reference(self):
        valid_claims = {"[STRUC-01]"}  # STRUC-05 and PROF-12 not in set
        result = validate_entry(VALID_ENTRY_V3, valid_claims=valid_claims)
        assert any("not found" in w for w in result.warnings)

    def test_correction_prompt(self):
        result = validate_entry("no frontmatter")
        assert not result.valid
        prompt = result.correction_prompt
        assert "ERROR" in prompt
        assert "frontmatter" in prompt.lower()


# =============================================================================
# EXTRACTION TESTS
# =============================================================================


class TestThreadExtraction:
    def test_extract_from_entry(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_thread_checklist(entry=entry)
        assert len(items) == 3  # 2 active + 1 dormant
        titles = [i.title for i in items]
        assert "USMCA review preparation" in titles
        assert "Post-El Mencho cartel realignment" in titles
        assert "Cuba oil policy" in titles

    def test_checklist_sections(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_thread_checklist(entry=entry)
        active = [i for i in items if i.section == "ACTIVE"]
        dormant = [i for i in items if i.section == "DORMANT"]
        assert len(active) == 2
        assert len(dormant) == 1

    def test_format_checklist(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_thread_checklist(entry=entry)
        text = format_thread_checklist(items)
        assert "1. [USMCA review preparation]" in text
        assert "ACTIVE" in text
        assert "DORMANT" in text

    def test_empty_checklist(self):
        text = format_thread_checklist([])
        assert "No threads" in text

    def test_bootstrap_no_prior(self):
        items = extract_thread_checklist(entry=None)
        assert items == []


class TestCommitmentExtraction:
    def test_extract_commitments(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_commitment_ledger([entry])
        assert len(items) == 2
        assert any("USMCA" in c.description for c in items)
        assert any("Plan Mexico" in c.description for c in items)

    def test_commitment_fields(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_commitment_ledger([entry])
        usmca = next(c for c in items if "USMCA" in c.description)
        assert usmca.status == "NEW"
        assert "Bilateral" in usmca.audience
        assert "MODERATE" in usmca.binding_force

    def test_format_ledger(self):
        entry = parse_entry(VALID_ENTRY_V3)
        items = extract_commitment_ledger([entry])
        text = format_commitment_ledger(items)
        assert "USMCA" in text
        assert "Status:" in text

    def test_empty_ledger(self):
        text = format_commitment_ledger([])
        assert "No active commitments" in text
