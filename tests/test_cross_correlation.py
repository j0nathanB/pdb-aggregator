"""
Tests for the cross-correlation pass (event formatting, output parsing, edge cases).
"""

from dataclasses import dataclass, field

import pytest

from src.phases.cross_correlation import (
    CrossCorrelationResult,
    format_event_list,
    parse_output,
    run_cross_correlation,
)
from src.config import LeaderConfig


@dataclass
class FakeEvent:
    """Minimal stand-in for ProcessedEvent in tests."""

    id: str = "evt-1"
    title: str = "Test Event"
    articles: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    summary: str = ""
    score: float = 0.85
    rank: int = 1
    source_count: int = 3
    has_wire: bool = True
    embedding: list = None


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def leaders():
    return [
        LeaderConfig(name="Alice Smith", title="President", country="Freedonia", region="europe"),
        LeaderConfig(name="Bob Jones", title="Prime Minister", country="Ruritania", region="europe"),
    ]


@pytest.fixture
def sample_events():
    return {
        "Alice Smith": [
            FakeEvent(id="a1", title="Signed trade deal with Ruritania", score=0.92, source_count=5),
            FakeEvent(id="a2", title="Announced climate policy", score=0.78, source_count=2),
        ],
        "Bob Jones": [
            FakeEvent(id="b1", title="Ratified trade agreement with Freedonia", score=0.88, source_count=4),
        ],
    }


# ---------------------------------------------------------------------------
# Event formatting
# ---------------------------------------------------------------------------

class TestFormatEventList:

    def test_basic_formatting(self, sample_events, leaders):
        result = format_event_list(sample_events, leaders)
        assert "[Alice Smith/Freedonia]" in result
        assert "[Bob Jones/Ruritania]" in result
        assert "Signed trade deal with Ruritania" in result
        assert "Score: 0.92" in result
        assert "Sources: 5" in result

    def test_all_events_present(self, sample_events, leaders):
        result = format_event_list(sample_events, leaders)
        lines = [l for l in result.strip().split("\n") if l.strip()]
        assert len(lines) == 3  # 2 from Alice + 1 from Bob

    def test_score_formatting(self, leaders):
        events = {
            "Alice Smith": [FakeEvent(score=0.10, source_count=1, title="Low score event")],
        }
        result = format_event_list(events, leaders)
        assert "Score: 0.10" in result

    def test_empty_events(self, leaders):
        result = format_event_list({}, leaders)
        assert result == ""

    def test_unknown_leader_country(self):
        """Leader not in leaders list gets 'Unknown' country."""
        events = {"Mystery Leader": [FakeEvent(title="Something happened")]}
        leaders = []
        result = format_event_list(events, leaders)
        assert "[Mystery Leader/Unknown]" in result


# ---------------------------------------------------------------------------
# Output parsing
# ---------------------------------------------------------------------------

class TestParseOutput:

    def test_trigger_yes(self):
        text = (
            "## THEMATIC CLUSTERS\n\n"
            "### 1. Trade Deals\n"
            "Leaders: Alice, Bob\n"
            "Assessment: NOTABLE\n\n"
            "TRIGGER PHASE 0: Yes\n"
            "Cluster 1 (Trade Deals) warrants a Global Context Brief."
        )
        result = parse_output(text)
        assert result.trigger_phase_0 is True
        assert "Trade Deals" in result.clusters_brief
        assert "warrants a Global Context Brief" in result.triggered_clusters

    def test_trigger_no(self):
        text = (
            "## THEMATIC CLUSTERS\n\n"
            "### 1. Climate Policy\n"
            "Leaders: Alice, Bob\n"
            "Assessment: ROUTINE\n\n"
            "TRIGGER PHASE 0: No"
        )
        result = parse_output(text)
        assert result.trigger_phase_0 is False
        assert result.triggered_clusters == ""
        assert "Climate Policy" in result.clusters_brief

    def test_trigger_case_insensitive(self):
        text = "Some clusters.\n\ntrigger phase 0: yes\nDetails here."
        result = parse_output(text)
        assert result.trigger_phase_0 is True
        assert "Details here." in result.triggered_clusters

    def test_no_trigger_line(self):
        text = "Some random output without any trigger line."
        result = parse_output(text)
        assert result.trigger_phase_0 is False
        assert result.triggered_clusters == ""
        assert result.clusters_brief == text.strip()

    def test_trigger_yes_no_trailing_text(self):
        text = "Clusters here.\n\nTRIGGER PHASE 0: Yes"
        result = parse_output(text)
        assert result.trigger_phase_0 is True
        assert result.triggered_clusters == ""

    def test_trigger_no_with_trailing_text(self):
        """Trailing text after 'No' is ignored."""
        text = "Clusters here.\n\nTRIGGER PHASE 0: No\nSome extra text."
        result = parse_output(text)
        assert result.trigger_phase_0 is False
        assert result.triggered_clusters == ""

    def test_clusters_brief_excludes_trigger_line(self):
        text = "Line 1\nLine 2\nTRIGGER PHASE 0: No"
        result = parse_output(text)
        assert "TRIGGER" not in result.clusters_brief
        assert "Line 1" in result.clusters_brief
        assert "Line 2" in result.clusters_brief


# ---------------------------------------------------------------------------
# Empty events handling
# ---------------------------------------------------------------------------

class TestEmptyEvents:

    @pytest.mark.asyncio
    async def test_empty_events_returns_empty_result(self):
        result = await run_cross_correlation(
            events_by_leader={},
            leaders=[],
            date_start="2026-03-01",
            date_end="2026-03-07",
        )
        assert isinstance(result, CrossCorrelationResult)
        assert result.clusters_brief == ""
        assert result.trigger_phase_0 is False
        assert result.triggered_clusters == ""

    @pytest.mark.asyncio
    async def test_leaders_with_empty_event_lists(self):
        result = await run_cross_correlation(
            events_by_leader={"Alice": [], "Bob": []},
            leaders=[],
            date_start="2026-03-01",
            date_end="2026-03-07",
        )
        assert result.trigger_phase_0 is False
        assert result.clusters_brief == ""
