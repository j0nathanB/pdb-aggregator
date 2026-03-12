"""
Tests for context assembly (system and user prompt construction).
"""

from dataclasses import dataclass, field

import pytest

from src.context.assembly import (
    build_system_prompt,
    build_call_a_user_prompt,
    build_call_b_user_prompt,
    _format_events,
)
from src.config import LeaderConfig


@dataclass
class FakeEvent:
    """Minimal stand-in for ProcessedEvent in tests."""
    id: str = "evt-1"
    title: str = "Test Event"
    articles: list = field(default_factory=lambda: [{"source": "Reuters", "title": "Headline"}])
    entities: list = field(default_factory=list)
    summary: str = "Something happened."
    score: float = 0.85
    rank: int = 1
    source_count: int = 3
    has_wire: bool = True
    embedding: list = None


DOSSIER = """# Country Dossier

## Section 1: Overview

Some text.

**STRUCTURAL CLAIMS:**
1. First structural claim. **[HIGH CONFIDENCE]**
2. Second structural claim. **[MODERATE CONFIDENCE]**
"""

PROFILE = """# Leader Profile

## SECTION 1: Background

Some text.

**PROFILE CLAIMS:**
1. First profile claim. [HIGH CONFIDENCE]
2. Second profile claim. [ASSESSED]
"""

LEADER = LeaderConfig(
    name="Test Leader",
    title="President",
    country="Testland",
    region="europe",
)


class TestBuildSystemPrompt:
    def test_contains_structural_context(self):
        prompt = build_system_prompt(DOSSIER, PROFILE, "Testland", "Test Leader")
        assert "## STRUCTURAL CONTEXT: Testland" in prompt

    def test_contains_leader_context(self):
        prompt = build_system_prompt(DOSSIER, PROFILE, "Testland", "Test Leader")
        assert "## LEADER CONTEXT: Test Leader" in prompt

    def test_contains_claims_index(self):
        prompt = build_system_prompt(DOSSIER, PROFILE, "Testland", "Test Leader")
        assert "## CLAIMS INDEX (for reference)" in prompt
        assert "[STRUC-01]:" in prompt
        assert "[PROF-01]:" in prompt

    def test_identical_for_same_inputs(self):
        """System prompt must be identical for Call A and Call B."""
        p1 = build_system_prompt(DOSSIER, PROFILE, "Testland", "Test Leader")
        p2 = build_system_prompt(DOSSIER, PROFILE, "Testland", "Test Leader")
        assert p1 == p2


class TestBuildCallAUserPrompt:
    def test_contains_role_instructions(self):
        prompt = build_call_a_user_prompt(
            LEADER, [FakeEvent()], "2026-03-01", "2026-03-07",
            "[No prior entries]", "[No threads from prior entry to carry forward.]",
        )
        assert "structured intelligence data logger" in prompt

    def test_contains_events(self):
        prompt = build_call_a_user_prompt(
            LEADER, [FakeEvent(title="Big Event")], "2026-03-01", "2026-03-07",
            "", "",
        )
        assert "Big Event" in prompt
        assert "THIS WEEK'S EVENTS: Test Leader" in prompt

    def test_contains_thread_checklist(self):
        checklist = "1. [Trade Talks] — Status as of last week: Active negotiations"
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", "", checklist,
        )
        assert "THREAD CHECKLIST" in prompt
        assert "Trade Talks" in prompt

    def test_contains_running_context(self):
        rp_text = "### Entry for 2026-02-22\nSome prior context."
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", rp_text, "",
        )
        assert "RUNNING CONTEXT: Test Leader" in prompt
        assert "Some prior context" in prompt

    def test_global_context_included(self):
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", "", "",
            global_context="US tariff escalation affecting all leaders.",
        )
        assert "GLOBAL CONTEXT: Week of 2026-03-01" in prompt
        assert "US tariff escalation" in prompt

    def test_global_context_omitted_when_none(self):
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", "", "",
        )
        assert "GLOBAL CONTEXT" not in prompt

    def test_contains_date_range(self):
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", "", "",
        )
        assert "2026-03-01 to 2026-03-07" in prompt

    def test_contains_leader_identity(self):
        prompt = build_call_a_user_prompt(
            LEADER, [], "2026-03-01", "2026-03-07", "", "",
        )
        assert "Test Leader (President," in prompt
        assert "Testland)" in prompt


class TestBuildCallBUserPrompt:
    def test_contains_analytical_method(self):
        prompt = build_call_b_user_prompt(
            LEADER, "Call A output here.", [], "2026-03-01", "2026-03-07", "",
        )
        assert "intelligence analyst" in prompt
        assert "WHAT HAPPENED" in prompt
        assert "STRUCTURAL FIT" in prompt
        assert "FALSIFICATION" in prompt

    def test_contains_call_a_output(self):
        prompt = build_call_b_user_prompt(
            LEADER, "Call A structured entry content.", [],
            "2026-03-01", "2026-03-07", "",
        )
        assert "THIS WEEK'S STRUCTURED SUMMARY" in prompt
        assert "Call A structured entry content" in prompt

    def test_contains_raw_events(self):
        prompt = build_call_b_user_prompt(
            LEADER, "call a", [FakeEvent(title="Raw Event")],
            "2026-03-01", "2026-03-07", "",
        )
        assert "RAW EVENTS (for reference)" in prompt
        assert "Raw Event" in prompt

    def test_contains_output_structure(self):
        prompt = build_call_b_user_prompt(
            LEADER, "", [], "2026-03-01", "2026-03-07", "",
        )
        assert "**ACTIVITY SUMMARY**" in prompt
        assert "**EVENT ANALYSIS**" in prompt
        assert "**CROSS-LEADER RELEVANCE**" in prompt
        assert "**BETWEEN THE LINES**" in prompt
        assert "**ATTENTION FLAGS**" in prompt
        assert "**KEY EVIDENCE FOR PHASE 2**" in prompt

    def test_global_context_conditional(self):
        without = build_call_b_user_prompt(
            LEADER, "", [], "2026-03-01", "2026-03-07", "",
        )
        with_gc = build_call_b_user_prompt(
            LEADER, "", [], "2026-03-01", "2026-03-07", "",
            global_context="Global context brief.",
        )
        assert "GLOBAL CONTEXT" not in without
        assert "GLOBAL CONTEXT" in with_gc


class TestFormatEvents:
    def test_empty_events(self):
        result = _format_events([])
        assert "No classified events" in result

    def test_event_formatting(self):
        events = [FakeEvent(title="Summit Meeting", score=0.92, source_count=5)]
        result = _format_events(events)
        assert "### Event 1: Summit Meeting" in result
        assert "Score: 0.92" in result
        assert "Sources: 5" in result
        assert "Wire: Yes" in result
        assert "Reuters" in result

    def test_multiple_events(self):
        events = [
            FakeEvent(id="1", title="First"),
            FakeEvent(id="2", title="Second"),
        ]
        result = _format_events(events)
        assert "### Event 1: First" in result
        assert "### Event 2: Second" in result
