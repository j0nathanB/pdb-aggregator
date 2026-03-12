"""
Tests for the consolidation phase module.

Covers needs_consolidation logic, prompt assembly, and entry loading.
"""

import textwrap
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.phases.consolidation import (
    needs_consolidation,
    _build_user_prompt,
    _extract_newly_dormant_threads,
    run_consolidation,
)
from src.running_picture.storage import (
    save_weekly_entry,
    save_consolidation,
    load_weekly_entries,
    entry_count,
)
from src.config import LeaderConfig


# =============================================================================
# FIXTURES
# =============================================================================

MINIMAL_ENTRY = textwrap.dedent("""\
    ---
    leader: Test Leader
    country: Testland
    week_of: {week_of}
    generated_at: 2026-01-09T10:00:00
    event_count: 3
    source_count: 8
    ---

    ### Activity Level
    Moderate

    ### Key Actions
    1. 2026-01-06 POLICY ANNOUNCEMENT: Test action.
       Source: Reuters
       Significance: Test significance [STRUC-01]

    ### Commitments & Positions
    [No new commitments.]

    ### Relationships
    [No significant interactions.]

    ### Domestic Political Position
    No material change this week.

    ### Developing Threads

    ACTIVE THREADS:
    - [Test thread]: Ongoing developments.
      Watch for: Next milestone
      Originated: 2026-01-01
      Last updated: This week

    ### Missing Thread Audit
    - [Test thread]: ACTIVE — updated

    ### Structural Claim Check
    No structural or profile claims materially affected.

    ### Analytical Notes
    Standard weekly entry for testing.""")

CONSOLIDATION_OUTPUT = textwrap.dedent("""\
    ---
    leader: Test Leader
    country: Testland
    period: 2026-01-06 to 2026-02-03
    generated_at: 2026-02-07T10:00:00
    consolidates_entries: 2026-01-06, 2026-01-13, 2026-01-20, 2026-01-27
    ---

    ### Period Trajectory
    A stable month with incremental policy developments.

    ### Stable Assessments
    1. Test assessment held across all 4 weeks.

    ### Resolved Threads
    - [Old thread]: Resolved. Outcome achieved January 20.

    ### Escalated Threads
    - [Test thread]: Elevated from routine monitoring to active tracking.

    ### Newly Dormant Threads
    - [Side project]: No developments since week 2.
      Reactivation trigger: New funding announcement.

    ### Commitment Ledger Update
    Active commitments: Test commitment (ongoing).

    ### Structural Claim Status
    - [STRUC-01]: Flagged 1 time — MONITOR

    ### Analytical Inertia Check
    - "Test assessment": VALIDATED — consistent evidence across period.

    ### Slow-Burn Review
    No slow-burn deviations detected.""")


@pytest.fixture
def leader():
    return LeaderConfig(
        name="Test Leader",
        title="President",
        country="Testland",
        region="europe",
    )


def _save_entries(tmp_path: Path, count: int) -> list[str]:
    """Save N minimal entries and return their week_of dates."""
    dates = [f"2026-01-{(i + 1) * 7:02d}" for i in range(count)]
    for date in dates:
        entry_text = MINIMAL_ENTRY.format(week_of=date)
        save_weekly_entry("Test Leader", date, entry_text, base_dir=tmp_path)
    return dates


# =============================================================================
# NEEDS CONSOLIDATION
# =============================================================================


class TestNeedsConsolidation:
    def test_no_entries(self, tmp_path):
        assert needs_consolidation("Test Leader", base_dir=tmp_path) is False

    def test_fewer_than_four(self, tmp_path):
        _save_entries(tmp_path, 3)
        assert needs_consolidation("Test Leader", base_dir=tmp_path) is False

    def test_exactly_four(self, tmp_path):
        _save_entries(tmp_path, 4)
        assert needs_consolidation("Test Leader", base_dir=tmp_path) is True

    def test_more_than_four(self, tmp_path):
        _save_entries(tmp_path, 6)
        assert needs_consolidation("Test Leader", base_dir=tmp_path) is True


# =============================================================================
# PROMPT ASSEMBLY
# =============================================================================


class TestPromptAssembly:
    def test_contains_weekly_entries(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index="## CLAIMS INDEX\n[STRUC-01]: Test claim",
            leader=leader,
        )
        assert "## ENTRIES TO CONSOLIDATE" in prompt
        assert "### Activity Level" in prompt
        assert "### Key Actions" in prompt

    def test_contains_prior_consolidation_placeholder(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index="",
            leader=leader,
        )
        assert "No prior consolidation" in prompt

    def test_contains_dormant_threads_placeholder(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index="",
            leader=leader,
        )
        assert "No dormant threads on file" in prompt

    def test_contains_dormant_threads_content(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="- [G20 follow-up]: Dormant since November",
            claims_index="",
            leader=leader,
        )
        assert "G20 follow-up" in prompt
        assert "No dormant threads" not in prompt

    def test_contains_claims_index(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        claims = "## CLAIMS INDEX\n[STRUC-01]: Test structural claim"
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index=claims,
            leader=leader,
        )
        assert "CLAIMS INDEX" in prompt
        assert "[STRUC-01]" in prompt

    def test_contains_leader_metadata(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index="",
            leader=leader,
        )
        assert "Test Leader" in prompt
        assert "President" in prompt
        assert "Testland" in prompt

    def test_period_dates_from_entries(self, tmp_path, leader):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        prompt = _build_user_prompt(
            entries=entries,
            prior_consolidation=None,
            dormant_threads="",
            claims_index="",
            leader=leader,
        )
        # Entries sorted most-recent-first: period_end is first, period_start is last
        assert entries[0].week_of in prompt  # period_end
        assert entries[-1].week_of in prompt  # period_start


# =============================================================================
# DORMANT THREAD EXTRACTION
# =============================================================================


class TestDormantThreadExtraction:
    def test_extracts_section(self):
        result = _extract_newly_dormant_threads(CONSOLIDATION_OUTPUT)
        assert "Side project" in result
        assert "Reactivation trigger" in result

    def test_empty_when_missing(self):
        text = "### Period Trajectory\nSome text.\n\n### Stable Assessments\nMore."
        result = _extract_newly_dormant_threads(text)
        assert result == ""


# =============================================================================
# ENTRY LOADING
# =============================================================================


class TestEntryLoading:
    def test_loads_four_entries(self, tmp_path):
        dates = _save_entries(tmp_path, 5)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        assert len(entries) == 4
        # Most recent first
        assert entries[0].week_of == dates[-1]

    def test_entries_have_correct_leader(self, tmp_path):
        _save_entries(tmp_path, 4)
        entries = load_weekly_entries("Test Leader", max_entries=4, base_dir=tmp_path)
        for entry in entries:
            assert entry.leader == "Test Leader"
            assert entry.country == "Testland"

    def test_no_entries_returns_empty(self, tmp_path):
        entries = load_weekly_entries("Nonexistent", max_entries=4, base_dir=tmp_path)
        assert entries == []
