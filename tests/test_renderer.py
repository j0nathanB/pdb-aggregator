"""
Tests for Phase 2 — Publication Renderer.

Verifies key evidence extraction, prompt assembly, conditional prior brief
inclusion, and metadata parsing from rendered brief output. No LLM calls.
"""

import asyncio
import inspect

import pytest

from src.config import LeaderConfig
from src.phases.prefilter import Tier, TieredLeader
from src.phases.renderer import (
    SYSTEM_PROMPT,
    Phase2Result,
    _build_key_evidence_appendix,
    _build_renderer_user_prompt,
    _extract_key_evidence,
    _parse_brief_metadata,
    run_renderer,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_leader(name: str = "Alice Smith", title: str = "President",
                 country: str = "Freedonia", region: str = "europe") -> LeaderConfig:
    return LeaderConfig(name=name, title=title, country=country, region=region)


def _make_tiered_leader(
    tier: Tier = Tier.TIER_1,
    name: str = "Alice Smith",
    country: str = "Freedonia",
    call_b_output: str = "",
    call_a_output: str = "",
    rendered: str = "",
) -> TieredLeader:
    leader = _make_leader(name=name, country=country)
    return TieredLeader(
        leader=leader,
        tier=tier,
        call_b_output=call_b_output,
        call_a_output=call_a_output,
        rendered=rendered or f"Rendered content for {name}",
    )


SAMPLE_CALL_B_WITH_EVIDENCE = """\
**ACTIVITY SUMMARY**
Active week for the leader with multiple diplomatic events.

**EVENT ANALYSIS**
Event 1: Signed trade deal — SIGNIFICANT SHIFT
Event 2: Climate speech — CONTINUITY

**CROSS-LEADER RELEVANCE**
Connection to Bob Jones on trade policy.

**BETWEEN THE LINES**
The trade deal represents a pivot away from traditional partners.

**FALSIFICATION**
Watch for: reversal of trade commitments within 90 days.

**ATTENTION FLAGS**
STRUCTURAL — trade realignment challenges founding assumptions.

**KEY EVIDENCE FOR PHASE 2**
1. "We are building new partnerships for a new era" — Reuters — 2026-03-03
2. Signed MOU with Ruritania covering $2B in bilateral trade — AP — 2026-03-04
3. Cabinet reshuffle moved trade-skeptic minister to lesser portfolio — Freedonia Times — 2026-03-05
"""

SAMPLE_CALL_B_NO_EVIDENCE = """\
**ACTIVITY SUMMARY**
Quiet week with routine diplomatic activity.

**EVENT ANALYSIS**
Event 1: Routine parliamentary session — CONTINUITY

**ATTENTION FLAGS**
(None)
"""


@pytest.fixture
def tier_1_leader():
    return _make_tiered_leader(
        tier=Tier.TIER_1,
        name="Alice Smith",
        country="Freedonia",
        call_b_output=SAMPLE_CALL_B_WITH_EVIDENCE,
        rendered="Full assessment for Alice Smith...",
    )


@pytest.fixture
def tier_2_leader():
    return _make_tiered_leader(
        tier=Tier.TIER_2,
        name="Bob Jones",
        country="Ruritania",
        call_b_output=SAMPLE_CALL_B_WITH_EVIDENCE.replace("Alice", "Bob"),
        rendered="Condensed summary for Bob Jones...",
    )


@pytest.fixture
def tier_3_leader():
    return _make_tiered_leader(
        tier=Tier.TIER_3,
        name="Carol White",
        country="Elbonia",
        call_b_output=SAMPLE_CALL_B_NO_EVIDENCE,
        rendered="## Carol White\n**President, Elbonia**\nActivity Level: Low\nQuiet week.",
    )


@pytest.fixture
def all_leaders(tier_1_leader, tier_2_leader, tier_3_leader):
    return [tier_1_leader, tier_2_leader, tier_3_leader]


# ---------------------------------------------------------------------------
# Key evidence extraction
# ---------------------------------------------------------------------------

class TestExtractKeyEvidence:

    def test_extracts_evidence_block(self):
        result = _extract_key_evidence(SAMPLE_CALL_B_WITH_EVIDENCE)
        assert "We are building new partnerships" in result
        assert "Signed MOU with Ruritania" in result
        assert "Cabinet reshuffle" in result

    def test_returns_empty_when_no_section(self):
        result = _extract_key_evidence(SAMPLE_CALL_B_NO_EVIDENCE)
        assert result == ""

    def test_returns_empty_for_empty_input(self):
        result = _extract_key_evidence("")
        assert result == ""

    def test_strips_whitespace(self):
        text = "**KEY EVIDENCE FOR PHASE 2**\n  Some evidence here.  \n"
        result = _extract_key_evidence(text)
        assert result == "Some evidence here."

    def test_stops_at_next_bold_section(self):
        text = (
            "**KEY EVIDENCE FOR PHASE 2**\n"
            "Evidence line 1.\n"
            "Evidence line 2.\n"
            "\n**ANOTHER SECTION**\n"
            "Should not appear."
        )
        result = _extract_key_evidence(text)
        assert "Evidence line 1." in result
        assert "Evidence line 2." in result
        assert "Should not appear" not in result


# ---------------------------------------------------------------------------
# Key evidence appendix
# ---------------------------------------------------------------------------

class TestBuildKeyEvidenceAppendix:

    def test_includes_tier_1_and_tier_2(self, tier_1_leader, tier_2_leader, tier_3_leader):
        leaders = [tier_1_leader, tier_2_leader, tier_3_leader]
        result = _build_key_evidence_appendix(leaders)
        assert "Alice Smith" in result
        assert "Bob Jones" in result
        assert "Carol White" not in result

    def test_excludes_tier_3(self, tier_3_leader):
        result = _build_key_evidence_appendix([tier_3_leader])
        assert result == ""

    def test_empty_list(self):
        result = _build_key_evidence_appendix([])
        assert result == ""

    def test_skips_leaders_without_evidence(self):
        leader = _make_tiered_leader(
            tier=Tier.TIER_1,
            call_b_output=SAMPLE_CALL_B_NO_EVIDENCE,
        )
        result = _build_key_evidence_appendix([leader])
        assert result == ""

    def test_formats_with_leader_header(self, tier_1_leader):
        result = _build_key_evidence_appendix([tier_1_leader])
        assert "### Alice Smith (President, Freedonia)" in result


# ---------------------------------------------------------------------------
# User prompt assembly
# ---------------------------------------------------------------------------

class TestBuildRendererUserPrompt:

    def test_contains_all_tier_sections(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Some clusters", "2026-03-01", "2026-03-07"
        )
        assert "### TIER 1: Full Assessments" in result
        assert "### TIER 2: Condensed Summaries" in result
        assert "### TIER 3: Quiet Weeks" in result

    def test_contains_rendered_content(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "Full assessment for Alice Smith" in result
        assert "Condensed summary for Bob Jones" in result
        assert "Carol White" in result

    def test_contains_clusters_brief(self, all_leaders):
        clusters = "Cluster 1: Trade realignment across Freedonia and Ruritania (NOTABLE)"
        result = _build_renderer_user_prompt(
            all_leaders, clusters, "2026-03-01", "2026-03-07"
        )
        assert "## THEMATIC CLUSTERS BRIEF" in result
        assert clusters in result

    def test_contains_key_evidence_appendix(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "## KEY EVIDENCE APPENDIX" in result
        assert "We are building new partnerships" in result

    def test_contains_date_range(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "2026-03-01" in result
        assert "2026-03-07" in result

    def test_contains_instructions(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "## INSTRUCTIONS" in result
        assert "SIGNAL STORIES" in result
        assert "AI ASSESSMENT SELECTION" in result
        assert "ALSO TRACKING" in result
        assert "Writing Guidelines" in result

    def test_no_prior_brief_by_default(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "PRIOR WEEK'S BRIEF" not in result

    def test_prior_brief_included_when_provided(self, all_leaders):
        prior = "# The Middle Powers Monitor\n\n## Week of 2026-02-22 to 2026-02-28\n\nLast week's content..."
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07",
            prior_brief=prior,
        )
        assert "## PRIOR WEEK'S BRIEF (for continuity)" in result
        assert "Last week's content..." in result

    def test_prior_brief_excluded_when_none(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07",
            prior_brief=None,
        )
        assert "PRIOR WEEK'S BRIEF" not in result

    def test_prior_brief_excluded_when_empty_string(self, all_leaders):
        result = _build_renderer_user_prompt(
            all_leaders, "Clusters", "2026-03-01", "2026-03-07",
            prior_brief="",
        )
        assert "PRIOR WEEK'S BRIEF" not in result

    def test_empty_tier_shows_placeholder(self):
        """When a tier has no leaders, a placeholder message appears."""
        leaders = [_make_tiered_leader(tier=Tier.TIER_1)]
        result = _build_renderer_user_prompt(
            leaders, "Clusters", "2026-03-01", "2026-03-07"
        )
        assert "(No Tier 2 leaders this week.)" in result
        assert "(No Tier 3 leaders this week.)" in result


# ---------------------------------------------------------------------------
# Metadata parsing from rendered brief
# ---------------------------------------------------------------------------

SAMPLE_BRIEF = """\
# The Middle Powers Monitor

## Week of 2026-03-01 to 2026-03-07

A significant week for middle power coordination as Freedonia pivoted
its trade policy and Baltic states responded to new security pressures.

---

## This Week's Signal

### CA Freedonia Pivots Trade Policy Toward New Partners

**BLUF:** Freedonia signed a landmark trade agreement with Ruritania,
signaling a shift away from traditional economic partners.

- Signed MOU covering $2B in bilateral trade with Ruritania
- Cabinet reshuffle moved trade-skeptic minister to lesser portfolio
- "We are building new partnerships for a new era" — PM Smith

**AI Assessment:** The trade pivot represents the most significant
realignment in Freedonia's economic policy in a decade. Watch for
whether the new MOU includes binding arbitration mechanisms.

### 🇱🇹 Baltic Defense Coordination Intensifies

**BLUF:** Estonia and Latvia announced joint procurement of air defense
systems amid heightened regional tensions.

- Joint procurement announcement for medium-range air defense
- Coordinated naval exercises in Gulf of Riga

**AI Assessment:** The procurement move accelerates Baltic defense
integration beyond NATO minimum commitments. Watch for whether
Lithuania joins the procurement framework.

---

## Regional Briefs

### Europe

#### CA Freedonia / Alice Smith

- Signed landmark trade MOU with Ruritania covering $2B
- Reshuffled cabinet to align with new trade priorities
- Attended EU foreign ministers meeting in Brussels

**AI Assessment:** Smith's trade pivot challenges Freedonia's
traditional alignment with Western European partners.

#### RU Ruritania / Bob Jones

- Ratified trade agreement with Freedonia
- Hosted trilateral summit with Elbonia and Borduria

**AI Assessment:** Jones leveraged the Freedonia deal to position
Ruritania as a regional trade hub.

### Baltic States

#### EE Elbonia / Carol White

- Routine parliamentary session
- Annual budget review on schedule

---

## Also Tracking

- **Elbonia:** Annual military readiness review completed with no changes to force posture.
- **Borduria:** Foreign minister visited Brussels for routine EU consultations.
- **Syldavia:** Parliamentary recess continues; no significant developments.

---

*Monitoring 15 leaders across 15 countries. 847 sources processed.
Week of 2026-03-01 to 2026-03-07. No significant source gaps noted.*
"""


class TestParseBriefMetadata:

    def test_signal_count(self):
        result = _parse_brief_metadata(SAMPLE_BRIEF)
        assert result.signal_count == 2

    def test_leaders_with_assessment(self):
        result = _parse_brief_metadata(SAMPLE_BRIEF)
        assert "Alice Smith" in result.leaders_with_assessment
        assert "Bob Jones" in result.leaders_with_assessment

    def test_leaders_without_assessment_excluded(self):
        result = _parse_brief_metadata(SAMPLE_BRIEF)
        assert "Carol White" not in result.leaders_with_assessment

    def test_also_tracking_countries(self):
        result = _parse_brief_metadata(SAMPLE_BRIEF)
        assert "Elbonia" in result.also_tracking
        assert "Borduria" in result.also_tracking
        assert "Syldavia" in result.also_tracking

    def test_brief_text_preserved(self):
        result = _parse_brief_metadata(SAMPLE_BRIEF)
        assert result.brief_text == SAMPLE_BRIEF

    def test_zero_signals_when_no_section(self):
        brief = "# Brief\n\nSome content with no signal section."
        result = _parse_brief_metadata(brief)
        assert result.signal_count == 0

    def test_empty_also_tracking(self):
        brief = "# Brief\n\n## Also Tracking\n\n(Nothing to track this week.)"
        result = _parse_brief_metadata(brief)
        assert result.also_tracking == []

    def test_empty_brief(self):
        result = _parse_brief_metadata("")
        assert result.signal_count == 0
        assert result.leaders_with_assessment == []
        assert result.also_tracking == []


# ---------------------------------------------------------------------------
# System prompt content
# ---------------------------------------------------------------------------

class TestSystemPrompt:

    def test_contains_role(self):
        assert "production editor" in SYSTEM_PROMPT
        assert "Middle Powers Monitor" in SYSTEM_PROMPT

    def test_contains_tier_descriptions(self):
        assert "TIER 1" in SYSTEM_PROMPT
        assert "TIER 2" in SYSTEM_PROMPT
        assert "TIER 3" in SYSTEM_PROMPT

    def test_contains_critical_rule(self):
        assert "CRITICAL RULE" in SYSTEM_PROMPT
        assert "traceable" in SYSTEM_PROMPT

    def test_renderer_not_analyst(self):
        assert "NOT generating new analysis" in SYSTEM_PROMPT


# ---------------------------------------------------------------------------
# run_renderer signature
# ---------------------------------------------------------------------------

class TestRunRendererSignature:

    def test_is_coroutine_function(self):
        assert asyncio.iscoroutinefunction(run_renderer)

    def test_has_docstring(self):
        assert run_renderer.__doc__ is not None
        assert "Middle Powers Monitor" in run_renderer.__doc__

    def test_accepts_expected_params(self):
        sig = inspect.signature(run_renderer)
        params = list(sig.parameters.keys())
        assert "tiered_leaders" in params
        assert "clusters_brief" in params
        assert "date_start" in params
        assert "date_end" in params
        assert "prior_brief" in params

    def test_prior_brief_is_optional(self):
        sig = inspect.signature(run_renderer)
        param = sig.parameters["prior_brief"]
        assert param.default is None
