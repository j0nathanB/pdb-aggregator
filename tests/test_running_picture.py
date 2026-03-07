"""
Tests for running picture file management.

Tests parsing, validation, append/load cycle, and edge cases.
"""

import textwrap
from pathlib import Path

import pytest

from src.running_picture import (
    RunningPictureEntry,
    ValidationResult,
    append_entry,
    entry_count,
    leader_slug,
    load_running_picture,
    load_running_picture_text,
    validate_entry,
    _extract_frontmatter,
    _parse_entry,
    _split_entries,
)


# =============================================================================
# FIXTURES
# =============================================================================

VALID_ENTRY = textwrap.dedent("""\
    ---
    leader: Emmanuel Macron
    country: France
    week_of: 2026-03-02
    generated_at: 2026-03-06T10:00:00
    event_count: 5
    source_count: 12
    ---

    ### Activity Level
    High
    Dominated by NATO summit preparations and bilateral meetings with Baltic leaders.

    ### Key Actions
    1. 2026-03-03 BILATERAL MEETING: Met with Estonian PM Kristen Michal in Paris to discuss NATO eastern flank reinforcement.
       Source: Reuters
       Significance: Reinforces France's pivot toward Baltic security concerns [STRUC-04]

    2. 2026-03-05 POLICY ANNOUNCEMENT: Announced EUR 2 billion increase in defense spending for 2027 budget.
       Source: Le Monde
       Significance: Continues trend of defense budget increases since 2022 [PROF-02]

    ### Commitments & Positions
    - NATO eastern flank reinforcement: Pledged additional French troops for Baltic rotational presence, committing to 500 additional personnel by Q3 2026.
      Status: NEW

    - EU defense autonomy: Reiterated support for European strategic autonomy in defense procurement.
      Status: REINFORCED

    ### Relationships
    - Bilateral meeting with Kristen Michal (Estonia): In-person bilateral in Paris, focused on NATO eastern flank and EU defense procurement coordination. Joint statement issued.
      Assessment: Strengthening direct bilateral channel; historically France has engaged Baltics primarily through EU multilateral forums.

    ### Domestic Political Position
    - National Assembly budget vote: Survived confidence vote on 2027 budget framework with support from centrist coalition. Margin narrower than previous votes (12 votes).
      Impact: Constrains fiscal room for additional defense commitments but demonstrates enough political capital to sustain current trajectory.

    ### Developing Threads
    - [EU defense procurement directive]: Commission draft expected in April. France pushing for preferential treatment of European manufacturers.
      Watch for: Commission draft publication; positions of Germany and Italy on domestic preference clauses.
      Originated: 2026-02-03

    - [NATO summit preparation]: June summit in The Hague. France lobbying for permanent Baltic deployment language in communique.
      Watch for: Pre-summit ministerial meetings; draft communique language leaks.
      Originated: 2026-02-17

    ### Structural Claim Check
    - [STRUC-04]: REINFORCED
      Evidence: Macron's bilateral with Estonian PM and troop commitment pledge align with structural claim about France's post-2022 eastward security pivot.
      Recommendation: No update needed.

    ### Analytical Notes
    The combination of a narrowing domestic political margin and expanding international defense commitments creates a tension worth monitoring. Macron's capacity to deliver on the Baltic troop pledge depends on the 2027 budget surviving parliamentary review — a thread that connects his domestic position directly to his NATO credibility. The pattern of bilateral engagement with individual Baltic leaders (rather than the traditional EU-wide approach) suggests a deliberate strategy to build personal diplomatic capital ahead of the NATO summit.""")


VALID_ENTRY_2 = textwrap.dedent("""\
    ---
    leader: Emmanuel Macron
    country: France
    week_of: 2026-02-23
    generated_at: 2026-02-27T10:00:00
    event_count: 3
    source_count: 8
    ---

    ### Activity Level
    Moderate
    Quiet week domestically; focus on EU Council preparation.

    ### Key Actions
    1. 2026-02-24 EU COUNCIL: Attended EU Council meeting in Brussels focused on migration policy.
       Source: AP News
       Significance: Routine engagement [STRUC-01]

    ### Commitments & Positions
    - EU migration reform: Supported proposed border processing regulation.
      Status: REINFORCED

    ### Relationships
    - EU Council multilateral: Standard multilateral engagement with Meloni, Merz, Tusk.
      Assessment: No notable bilateral developments.

    ### Developing Threads
    - [EU defense procurement directive]: Commission draft timeline confirmed for April.
      Watch for: Commission draft publication.
      Originated: 2026-02-03

    ### Structural Claim Check
    - [STRUC-01]: REINFORCED
      Evidence: Standard EU institutional engagement consistent with France's central EU role.
      Recommendation: No update needed.

    ### Analytical Notes
    A consolidation week. No new commitments or shifts. The quiet posture is consistent with pre-summit diplomatic positioning.""")


MINIMAL_ENTRY = textwrap.dedent("""\
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

    ### Developing Threads
    [No active threads.]""")


# =============================================================================
# UNIT TESTS
# =============================================================================


class TestLeaderSlug:
    def test_basic(self):
        assert leader_slug("Emmanuel Macron") == "emmanuel_macron"

    def test_special_chars(self):
        assert leader_slug("Evika Siliņa") == "evika_siliņa"

    def test_single_name(self):
        assert leader_slug("Zelenskyy") == "zelenskyy"


class TestFrontmatter:
    def test_extract(self):
        fm = _extract_frontmatter(VALID_ENTRY)
        assert fm is not None
        assert fm["leader"] == "Emmanuel Macron"
        assert fm["country"] == "France"
        assert fm["week_of"] == "2026-03-02"
        assert fm["event_count"] == "5"

    def test_missing(self):
        assert _extract_frontmatter("no frontmatter here") is None

    def test_empty_block(self):
        assert _extract_frontmatter("---\n---\ncontent") == {}


class TestParseEntry:
    def test_valid(self):
        entry = _parse_entry(VALID_ENTRY)
        assert entry.leader == "Emmanuel Macron"
        assert entry.country == "France"
        assert entry.week_of == "2026-03-02"
        assert entry.event_count == 5
        assert entry.source_count == 12
        assert "High" in entry.activity_level
        assert "BILATERAL MEETING" in entry.key_actions
        assert "NATO eastern flank" in entry.commitments

    def test_developing_threads_parsed(self):
        entry = _parse_entry(VALID_ENTRY)
        assert "EU defense procurement directive" in entry.developing_threads
        assert "Watch for" in entry.developing_threads

    def test_no_frontmatter_raises(self):
        with pytest.raises(ValueError):
            _parse_entry("just some text\nwith no frontmatter")


class TestSplitEntries:
    def test_single_entry(self):
        entries = _split_entries(VALID_ENTRY)
        assert len(entries) == 1

    def test_multiple_entries(self):
        combined = VALID_ENTRY + "\n---\n" + VALID_ENTRY_2
        entries = _split_entries(combined)
        assert len(entries) == 2
        # Most recent first in the file
        assert "2026-03-02" in entries[0]
        assert "2026-02-23" in entries[1]

    def test_empty(self):
        assert _split_entries("") == []
        assert _split_entries("   \n\n  ") == []


class TestValidation:
    def test_valid_entry(self):
        result = validate_entry(VALID_ENTRY)
        assert result.valid
        assert len(result.errors) == 0

    def test_missing_frontmatter(self):
        result = validate_entry("### Activity Level\nHigh\n### Key Actions\n1. Something")
        assert not result.valid
        assert any("frontmatter" in e.lower() for e in result.errors)

    def test_missing_section(self):
        # Remove Key Actions section
        broken = VALID_ENTRY.replace("### Key Actions", "### Actions")
        result = validate_entry(broken)
        assert not result.valid
        assert any("Key Actions" in e for e in result.errors)

    def test_minimal_valid(self):
        result = validate_entry(MINIMAL_ENTRY)
        assert result.valid

    def test_invalid_week_of(self):
        bad_date = VALID_ENTRY.replace("week_of: 2026-03-02", "week_of: March 2")
        result = validate_entry(bad_date)
        assert not result.valid
        assert any("week_of" in e for e in result.errors)


class TestFileOperations:
    def test_append_and_load(self, tmp_path):
        append_entry("Emmanuel Macron", VALID_ENTRY, base_dir=tmp_path)

        entries = load_running_picture("Emmanuel Macron", base_dir=tmp_path)
        assert len(entries) == 1
        assert entries[0].leader == "Emmanuel Macron"
        assert entries[0].week_of == "2026-03-02"

    def test_append_prepends(self, tmp_path):
        # Append older entry first, then newer
        append_entry("Emmanuel Macron", VALID_ENTRY_2, base_dir=tmp_path)
        append_entry("Emmanuel Macron", VALID_ENTRY, base_dir=tmp_path)

        entries = load_running_picture("Emmanuel Macron", base_dir=tmp_path)
        assert len(entries) == 2
        # Most recent should be first
        assert entries[0].week_of == "2026-03-02"
        assert entries[1].week_of == "2026-02-23"

    def test_max_entries(self, tmp_path):
        # Append 3 entries, load only 2
        append_entry("Emmanuel Macron", MINIMAL_ENTRY, base_dir=tmp_path)
        append_entry("Emmanuel Macron", VALID_ENTRY_2, base_dir=tmp_path)
        append_entry("Emmanuel Macron", VALID_ENTRY, base_dir=tmp_path)

        entries = load_running_picture("Emmanuel Macron", max_entries=2, base_dir=tmp_path)
        assert len(entries) == 2

    def test_load_nonexistent(self, tmp_path):
        entries = load_running_picture("Nobody", base_dir=tmp_path)
        assert entries == []

    def test_load_text(self, tmp_path):
        append_entry("Emmanuel Macron", VALID_ENTRY, base_dir=tmp_path)
        text = load_running_picture_text("Emmanuel Macron", base_dir=tmp_path)
        assert "Emmanuel Macron" in text
        assert "### Key Actions" in text

    def test_load_text_empty(self, tmp_path):
        text = load_running_picture_text("Nobody", base_dir=tmp_path)
        assert text == ""

    def test_entry_count(self, tmp_path):
        assert entry_count("Emmanuel Macron", base_dir=tmp_path) == 0
        append_entry("Emmanuel Macron", VALID_ENTRY, base_dir=tmp_path)
        assert entry_count("Emmanuel Macron", base_dir=tmp_path) == 1
        append_entry("Emmanuel Macron", VALID_ENTRY_2, base_dir=tmp_path)
        assert entry_count("Emmanuel Macron", base_dir=tmp_path) == 2

    def test_creates_directory(self, tmp_path):
        subdir = tmp_path / "nested" / "dir"
        append_entry("Test", MINIMAL_ENTRY, base_dir=subdir)
        assert (subdir / "test.md").exists()
