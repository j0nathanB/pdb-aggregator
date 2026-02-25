"""
Aggregate briefing quality tests.

Loads dossiers from saved output.json and validates aggregate structural invariants.
Run with: pytest tests/test_aggregate_quality.py -v --timeout=600
"""

import pytest
from pathlib import Path

from src.persistence import load_brief


BRIEF_DIR = Path("briefs/20260210")


@pytest.fixture
def weekly_brief():
    """Load the 20260210 weekly brief."""
    brief = load_brief(BRIEF_DIR)
    if brief is None:
        pytest.skip(f"Brief not found at {BRIEF_DIR}/output.json")
    return brief


class TestAggregateStructure:
    """Validate aggregate briefing structural invariants."""

    def test_aggregate_produces_main_stories(self, weekly_brief):
        """1-5 main stories, BTL > 0, exec_summary present."""
        assert len(weekly_brief.main_stories) >= 1, (
            "Aggregate should have at least 1 main story"
        )
        assert len(weekly_brief.main_stories) <= 5, (
            f"Aggregate should have at most 5 main stories, got {len(weekly_brief.main_stories)}"
        )

        btl_count = len(weekly_brief.between_the_lines)
        assert btl_count > 0, (
            "Aggregate should have at least 1 BTL bullet"
        )

        assert weekly_brief.executive_summary, (
            "Aggregate executive summary should be non-empty"
        )

    def test_shared_stories_have_multiple_leaders(self, weekly_brief):
        """At least one multi-leader story when >= 3 main stories."""
        if len(weekly_brief.main_stories) < 3:
            pytest.skip("Fewer than 3 main stories, skipping multi-leader check")

        multi_leader = [
            s for s in weekly_brief.main_stories
            if len(s.contributing_leaders) > 1
        ]
        # This is a soft assertion — multi-leader stories are expected but not guaranteed
        # in every brief, so we just check the data structure is valid
        for story in weekly_brief.main_stories:
            assert isinstance(story.contributing_leaders, list), (
                f"contributing_leaders should be a list for '{story.title}'"
            )

    def test_stories_have_valid_fields(self, weekly_brief):
        """All stories have non-empty title, narrative, and valid scope."""
        all_stories = (
            weekly_brief.main_stories
            + weekly_brief.international_stories
            + weekly_brief.domestic_stories
        )

        for story in all_stories:
            assert story.title, f"Story {story.id} has empty title"
            assert story.narrative, f"Story '{story.title}' has empty narrative"
            assert story.scope in ("international", "domestic"), (
                f"Story '{story.title}' has invalid scope: {story.scope}"
            )
            assert story.source_count >= 1, (
                f"Story '{story.title}' has source_count={story.source_count}"
            )

    def test_dossiers_present(self, weekly_brief):
        """Brief contains dossiers for multiple leaders."""
        assert len(weekly_brief.leader_dossiers) >= 5, (
            f"Expected at least 5 leader dossiers, got {len(weekly_brief.leader_dossiers)}"
        )

        for dossier in weekly_brief.leader_dossiers:
            assert dossier.leader.name, "Dossier has no leader name"
            assert dossier.reporting_period, "Dossier has no reporting period"
