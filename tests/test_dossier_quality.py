"""
Dossier quality regression tests.

Makes real API calls, replays fixtures through dossier builder.
Run with: pytest tests/test_dossier_quality.py -v --timeout=600

These tests validate structural invariants of dossier output:
- Classification fields are present and valid
- Story counts are within expected ranges
- Dateline formatting follows AP style
- Multilingual leaders produce English output
"""

import pytest
import asyncio

from src.agents.dossier_builder import DossierBuilderAgent
from src.config import EventType, LeaderRole, ImpactLevel


@pytest.fixture
def builder():
    return DossierBuilderAgent()


@pytest.mark.timeout(600)
class TestMergedPromptClassification:
    """Verify merged synthesis+classification produces valid classifications."""

    @pytest.mark.asyncio
    async def test_merged_prompt_produces_valid_classification(
        self, builder, carney_events, carney_config
    ):
        """Every story has a non-None classification with valid enum values and priority_score > 0."""
        top_events, rest_events = carney_events
        dossier = await builder.build_from_events(
            leader=carney_config,
            top_events=top_events,
            remaining_events=rest_events,
        )

        all_stories = (
            dossier.main_stories
            + dossier.international_stories
            + dossier.domestic_stories
        )
        assert len(all_stories) > 0, "Dossier should have at least one story"

        for story in all_stories:
            assert story.classification is not None, (
                f"Story '{story.title}' has no classification"
            )
            assert isinstance(story.classification.event_type, EventType), (
                f"Invalid event_type for '{story.title}': {story.classification.event_type}"
            )
            assert isinstance(story.classification.leader_role, LeaderRole), (
                f"Invalid leader_role for '{story.title}': {story.classification.leader_role}"
            )
            assert isinstance(story.classification.impact_level, ImpactLevel), (
                f"Invalid impact_level for '{story.title}': {story.classification.impact_level}"
            )
            assert story.classification.priority_score > 0, (
                f"priority_score should be > 0 for '{story.title}', "
                f"got {story.classification.priority_score}"
            )


@pytest.mark.timeout(600)
class TestStoryStructure:
    """Verify story counts and structural invariants."""

    @pytest.mark.asyncio
    async def test_story_count_preserved(
        self, builder, carney_events, carney_config
    ):
        """Dossier has stories, main <= 5, BTL >= 2, has exec summary."""
        top_events, rest_events = carney_events
        dossier = await builder.build_from_events(
            leader=carney_config,
            top_events=top_events,
            remaining_events=rest_events,
        )

        total = (
            len(dossier.main_stories)
            + len(dossier.international_stories)
            + len(dossier.domestic_stories)
        )
        assert total > 0, "Dossier should have at least one story"
        assert len(dossier.main_stories) <= 5, (
            f"Main stories should be <= 5, got {len(dossier.main_stories)}"
        )
        assert len(dossier.between_the_lines) >= 2, (
            f"Should have >= 2 BTL bullets, got {len(dossier.between_the_lines)}"
        )
        assert dossier.executive_summary, "Executive summary should be non-empty"


@pytest.mark.timeout(600)
class TestDatelineFormatting:
    """Verify AP-style dateline formatting."""

    @pytest.mark.asyncio
    async def test_dateline_formatting(
        self, builder, carney_events, carney_config
    ):
        """>=80% of story narratives contain a dateline (em dash in first 80 chars)."""
        top_events, rest_events = carney_events
        dossier = await builder.build_from_events(
            leader=carney_config,
            top_events=top_events,
            remaining_events=rest_events,
        )

        all_stories = (
            dossier.main_stories
            + dossier.international_stories
            + dossier.domestic_stories
        )
        assert len(all_stories) > 0

        dateline_count = 0
        for story in all_stories:
            # Check for em dash or regular dash in the first 80 characters
            first_80 = story.narrative[:80]
            if "—" in first_80 or " -- " in first_80 or " - " in first_80:
                dateline_count += 1

        ratio = dateline_count / len(all_stories)
        assert ratio >= 0.8, (
            f"Only {dateline_count}/{len(all_stories)} ({ratio:.0%}) stories "
            f"have datelines, expected >= 80%"
        )


@pytest.mark.timeout(600)
class TestMultilingualOutput:
    """Verify non-English leaders produce English output."""

    @pytest.mark.asyncio
    async def test_multilingual_leader_english_output(
        self, builder, sheinbaum_events, sheinbaum_config
    ):
        """Stories for Sheinbaum contain English markers."""
        top_events, rest_events = sheinbaum_events
        dossier = await builder.build_from_events(
            leader=sheinbaum_config,
            top_events=top_events,
            remaining_events=rest_events,
        )

        all_stories = (
            dossier.main_stories
            + dossier.international_stories
            + dossier.domestic_stories
        )
        assert len(all_stories) > 0, "Sheinbaum dossier should have stories"

        english_markers = {"the", "said", "and", "for", "with", "that", "has", "was"}
        for story in all_stories:
            words = set(story.narrative.lower().split())
            matches = words & english_markers
            assert len(matches) >= 2, (
                f"Story '{story.title}' may not be in English. "
                f"Only {len(matches)} English markers found in narrative."
            )
