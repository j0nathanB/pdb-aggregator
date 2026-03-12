"""Tests for the pre-filter tier assignment logic."""

import pytest

from src.config import LeaderConfig
from src.phases.prefilter import (
    Tier,
    TieredLeader,
    compress_assessment,
    count_active_threads,
    count_cross_leader_mentions,
    extract_activity_level,
    extract_activity_summary,
    extract_attention_flags,
    extract_deviation_classifications,
    extract_thread_titles,
    generate_stub,
    run_prefilter,
)

# =============================================================================
# Fixtures
# =============================================================================

SAMPLE_CALL_B = """\
**ACTIVITY SUMMARY**
Leader X held bilateral talks with France and signed a trade agreement. \
Domestic opposition challenged the new budget proposal.

**EVENT ANALYSIS**
1. Bilateral trade agreement with France
   - Classification: SIGNIFICANT SHIFT
   - This represents a major departure from previous isolationist trade policy.
2. Budget opposition in parliament
   - Classification: TACTICAL ADJUSTMENT
   - Routine parliamentary maneuvering within expected bounds.

**CROSS-LEADER RELEVANCE**
- Emmanuel Macron: Direct counterpart in trade negotiations. The agreement \
strengthens Macron's EU trade agenda.
- Keir Starmer: May face pressure to match the trade terms offered.

**BETWEEN THE LINES**
The trade pivot suggests Leader X is hedging against reliance on traditional \
partners. Watch for follow-up signals with Asian markets.

**FALSIFICATION**
- If Leader X reverses trade terms within 60 days, the "strategic pivot" \
thesis is falsified.
- If parliament blocks the budget without concessions, the "weak opposition" \
thesis needs revision.

**ATTENTION FLAGS**
- STRUCTURAL: Trade policy reversal represents a fundamental shift in \
economic orientation.

**KEY EVIDENCE FOR PHASE 2**
- Trade agreement text provisions on tariff schedules
- Parliamentary vote tallies on budget amendments
"""

SAMPLE_CALL_B_WATCH_ONLY = """\
**ACTIVITY SUMMARY**
Leader Y attended a routine EU summit and made standard diplomatic statements.

**EVENT ANALYSIS**
1. EU summit attendance
   - Classification: CONTINUITY
   - No departure from established positions.
2. Domestic press conference
   - Classification: TACTICAL ADJUSTMENT
   - Minor rhetorical shift on immigration framing.

**CROSS-LEADER RELEVANCE**
- No significant cross-leader dynamics this period.

**BETWEEN THE LINES**
Nothing notable beyond surface-level activity.

**FALSIFICATION**
- Standing criteria remain unchanged.

**ATTENTION FLAGS**
- WATCH: Immigration rhetoric shift merits monitoring.

**KEY EVIDENCE FOR PHASE 2**
- Summit communiqué language on defense spending
"""

SAMPLE_CALL_B_QUIET = """\
**ACTIVITY SUMMARY**
Leader Z had a quiet week with no significant public engagements.

**EVENT ANALYSIS**
1. Routine cabinet meeting
   - Classification: CONTINUITY
   - Standard weekly governance activity.

**CROSS-LEADER RELEVANCE**
No cross-leader relevance identified.

**BETWEEN THE LINES**
No notable observations.

**FALSIFICATION**
No active falsification criteria.

**KEY EVIDENCE FOR PHASE 2**
None.
"""

SAMPLE_CALL_A = """\
### Activity Level
Moderate

### Developing Threads
ACTIVE THREADS:
- **EU Trade Negotiations**: Ongoing bilateral talks with multiple partners.
- **Budget Reform**: Parliamentary committee reviewing proposed changes.
- **Military Procurement**: New defense contract under negotiation.

Resolved Threads:
- **Election Certification**: Completed without incident.
"""

SAMPLE_CALL_A_FEW_THREADS = """\
### Activity Level
Low

### Developing Threads
ACTIVE THREADS:
- **Routine Governance**: Standard weekly activities.

Resolved Threads:
- None
"""

SAMPLE_CALL_A_NO_THREADS = """\
### Activity Level
Minimal

### Developing Threads
No active developing threads identified.
"""


def _make_leader(name: str, title: str = "President", country: str = "Testland") -> LeaderConfig:
    return LeaderConfig(name=name, title=title, country=country, region="europe")


# =============================================================================
# Test extraction helpers
# =============================================================================

class TestExtractAttentionFlags:
    def test_structural_flag(self):
        flags = extract_attention_flags(SAMPLE_CALL_B)
        assert "STRUCTURAL" in flags

    def test_watch_flag(self):
        flags = extract_attention_flags(SAMPLE_CALL_B_WATCH_ONLY)
        assert "WATCH" in flags
        assert "STRUCTURAL" not in flags
        assert "ALERT" not in flags

    def test_no_flags_section(self):
        text = "**ACTIVITY SUMMARY**\nSome text.\n"
        flags = extract_attention_flags(text)
        assert flags == []

    def test_empty_text(self):
        assert extract_attention_flags("") == []


class TestExtractDeviationClassifications:
    def test_multiple_classifications(self):
        classifications = extract_deviation_classifications(SAMPLE_CALL_B)
        assert "SIGNIFICANT SHIFT" in classifications
        assert "TACTICAL ADJUSTMENT" in classifications

    def test_continuity_only(self):
        classifications = extract_deviation_classifications(SAMPLE_CALL_B_QUIET)
        assert classifications == ["CONTINUITY"]

    def test_empty_text(self):
        assert extract_deviation_classifications("") == []


class TestCountCrossLeaderMentions:
    def test_mentioned_in_other_leader(self):
        outputs = {
            "Leader A": SAMPLE_CALL_B,  # mentions Macron and Starmer
            "Emmanuel Macron": "**CROSS-LEADER RELEVANCE**\nNo mentions.",
        }
        count = count_cross_leader_mentions("Emmanuel Macron", outputs)
        assert count == 1

    def test_not_mentioned(self):
        outputs = {
            "Leader A": SAMPLE_CALL_B,
            "Leader B": SAMPLE_CALL_B_QUIET,
        }
        count = count_cross_leader_mentions("Leader Z", outputs)
        assert count == 0

    def test_self_not_counted(self):
        outputs = {
            "Emmanuel Macron": "**CROSS-LEADER RELEVANCE**\nEmmanuel Macron is central.",
        }
        count = count_cross_leader_mentions("Emmanuel Macron", outputs)
        assert count == 0

    def test_multiple_mentions(self):
        outputs = {
            "A": "**CROSS-LEADER RELEVANCE**\nLeader X is relevant.",
            "B": "**CROSS-LEADER RELEVANCE**\nLeader X appeared in talks.",
            "C": "**CROSS-LEADER RELEVANCE**\nNo connection to Leader X.",
            "Leader X": "**CROSS-LEADER RELEVANCE**\nSelf.",
        }
        count = count_cross_leader_mentions("Leader X", outputs)
        assert count == 3


class TestCountActiveThreads:
    def test_three_threads(self):
        assert count_active_threads(SAMPLE_CALL_A) == 3

    def test_one_thread(self):
        assert count_active_threads(SAMPLE_CALL_A_FEW_THREADS) == 1

    def test_no_threads(self):
        assert count_active_threads(SAMPLE_CALL_A_NO_THREADS) == 0


class TestExtractThreadTitles:
    def test_extracts_titles(self):
        titles = extract_thread_titles(SAMPLE_CALL_A)
        assert len(titles) == 3
        assert "EU Trade Negotiations" in titles
        assert "Budget Reform" in titles
        assert "Military Procurement" in titles

    def test_no_threads(self):
        assert extract_thread_titles(SAMPLE_CALL_A_NO_THREADS) == []


class TestExtractActivitySummary:
    def test_extracts_paragraph(self):
        summary = extract_activity_summary(SAMPLE_CALL_B)
        assert "bilateral talks" in summary
        assert "budget proposal" in summary

    def test_empty(self):
        assert extract_activity_summary("") == ""


class TestExtractActivityLevel:
    def test_extracts_level(self):
        level = extract_activity_level(SAMPLE_CALL_A)
        assert level == "Moderate"

    def test_fallback(self):
        assert extract_activity_level("") == "Unknown"


# =============================================================================
# Test rendering
# =============================================================================

class TestCompressAssessment:
    def test_retains_required_sections(self):
        condensed = compress_assessment(SAMPLE_CALL_B)
        assert "**ACTIVITY SUMMARY**" in condensed
        assert "**CROSS-LEADER RELEVANCE**" in condensed
        assert "**BETWEEN THE LINES**" in condensed
        assert "**FALSIFICATION**" in condensed
        assert "**ATTENTION FLAGS**" in condensed
        assert "**KEY EVIDENCE FOR PHASE 2**" in condensed

    def test_excludes_event_analysis(self):
        condensed = compress_assessment(SAMPLE_CALL_B)
        assert "**EVENT ANALYSIS**" not in condensed


class TestGenerateStub:
    def test_contains_leader_info(self):
        leader = _make_leader("Leader Z", "President", "Testland")
        stub = generate_stub(leader, SAMPLE_CALL_A, SAMPLE_CALL_B_QUIET)
        assert "Leader Z" in stub
        assert "President" in stub
        assert "Testland" in stub

    def test_contains_activity_level(self):
        leader = _make_leader("Leader Z")
        stub = generate_stub(leader, SAMPLE_CALL_A, SAMPLE_CALL_B_QUIET)
        assert "Moderate" in stub

    def test_contains_thread_titles(self):
        leader = _make_leader("Leader Z")
        stub = generate_stub(leader, SAMPLE_CALL_A, SAMPLE_CALL_B_QUIET)
        assert "EU Trade Negotiations" in stub
        assert "Budget Reform" in stub

    def test_one_sentence_summary(self):
        leader = _make_leader("Leader Z")
        stub = generate_stub(leader, SAMPLE_CALL_A_NO_THREADS, SAMPLE_CALL_B_QUIET)
        # Should have only one sentence from activity summary
        assert "quiet week" in stub
        # Should NOT contain the full multi-sentence summary
        lines = [l for l in stub.splitlines() if l.strip() and not l.startswith(("##", "**", "Activity", "-"))]
        # The activity summary line should be a single sentence
        assert len(lines) <= 1


# =============================================================================
# Test tier assignment
# =============================================================================

class TestTierAssignment:
    def test_tier1_structural_flag(self):
        """STRUCTURAL flag -> Tier 1"""
        leaders = [_make_leader("Leader X")]
        result = run_prefilter(
            leaders,
            {"Leader X": SAMPLE_CALL_A},
            {"Leader X": SAMPLE_CALL_B},
        )
        assert result[0].tier == Tier.TIER_1

    def test_tier1_alert_flag(self):
        """ALERT flag -> Tier 1"""
        call_b = SAMPLE_CALL_B.replace("STRUCTURAL", "ALERT")
        leaders = [_make_leader("Leader X")]
        result = run_prefilter(
            leaders,
            {"Leader X": SAMPLE_CALL_A},
            {"Leader X": call_b},
        )
        assert result[0].tier == Tier.TIER_1

    def test_tier1_significant_shift(self):
        """SIGNIFICANT SHIFT event classification -> Tier 1"""
        call_b = """\
**EVENT ANALYSIS**
1. Major event
   - Classification: SIGNIFICANT SHIFT

**ATTENTION FLAGS**
No flags.
"""
        leaders = [_make_leader("X")]
        result = run_prefilter(leaders, {"X": ""}, {"X": call_b})
        assert result[0].tier == Tier.TIER_1

    def test_tier1_potential_structural_change(self):
        """POTENTIAL STRUCTURAL CHANGE -> Tier 1"""
        call_b = """\
**EVENT ANALYSIS**
1. Major event
   - Classification: POTENTIAL STRUCTURAL CHANGE

**ATTENTION FLAGS**
No flags.
"""
        leaders = [_make_leader("X")]
        result = run_prefilter(leaders, {"X": ""}, {"X": call_b})
        assert result[0].tier == Tier.TIER_1

    def test_tier1_cross_mention_with_deviation(self):
        """Named in 1+ cross-leader sections AND deviation above CONTINUITY -> Tier 1"""
        call_b_target = """\
**EVENT ANALYSIS**
1. Event
   - Classification: TACTICAL ADJUSTMENT

**ATTENTION FLAGS**
No flags.

**CROSS-LEADER RELEVANCE**
Nothing.
"""
        call_b_other = """\
**CROSS-LEADER RELEVANCE**
- Target Leader: Relevant due to trade talks.

**EVENT ANALYSIS**
Nothing.
"""
        leaders = [_make_leader("Target Leader"), _make_leader("Other")]
        result = run_prefilter(
            leaders,
            {"Target Leader": "", "Other": ""},
            {"Target Leader": call_b_target, "Other": call_b_other},
        )
        target = [r for r in result if r.leader.name == "Target Leader"][0]
        assert target.tier == Tier.TIER_1

    def test_tier1_hub_threshold(self):
        """Named in 3+ cross-leader sections -> Tier 1 (regardless of deviations)"""
        call_b_target = """\
**EVENT ANALYSIS**
1. Event
   - Classification: CONTINUITY

**ATTENTION FLAGS**
No flags.
"""
        mention = "**CROSS-LEADER RELEVANCE**\n- Hub Leader: Important.\n"
        leaders = [
            _make_leader("Hub Leader"),
            _make_leader("A"),
            _make_leader("B"),
            _make_leader("C"),
        ]
        outputs = {
            "Hub Leader": call_b_target,
            "A": mention,
            "B": mention,
            "C": mention,
        }
        result = run_prefilter(
            leaders,
            {l.name: "" for l in leaders},
            outputs,
        )
        hub = [r for r in result if r.leader.name == "Hub Leader"][0]
        assert hub.tier == Tier.TIER_1

    def test_tier3_all_quiet(self):
        """No flags, all CONTINUITY, no mentions, few threads -> Tier 3"""
        leaders = [_make_leader("Quiet Leader")]
        result = run_prefilter(
            leaders,
            {"Quiet Leader": SAMPLE_CALL_A_FEW_THREADS},
            {"Quiet Leader": SAMPLE_CALL_B_QUIET},
        )
        assert result[0].tier == Tier.TIER_3

    def test_tier2_watch_flag(self):
        """WATCH flag only, mixed classifications -> Tier 2"""
        leaders = [_make_leader("Watch Leader")]
        result = run_prefilter(
            leaders,
            {"Watch Leader": SAMPLE_CALL_A_FEW_THREADS},
            {"Watch Leader": SAMPLE_CALL_B_WATCH_ONLY},
        )
        assert result[0].tier == Tier.TIER_2

    def test_tier2_thread_elevation(self):
        """3+ active threads elevates from what would be Tier 3 -> Tier 2"""
        # Quiet Call B (would be Tier 3) but 3 active threads
        leaders = [_make_leader("Threaded Leader")]
        result = run_prefilter(
            leaders,
            {"Threaded Leader": SAMPLE_CALL_A},  # 3 threads
            {"Threaded Leader": SAMPLE_CALL_B_QUIET},
        )
        assert result[0].tier == Tier.TIER_2

    def test_rendered_tier1_is_full(self):
        """Tier 1 rendered output is the full Call B text."""
        leaders = [_make_leader("Leader X")]
        result = run_prefilter(
            leaders,
            {"Leader X": SAMPLE_CALL_A},
            {"Leader X": SAMPLE_CALL_B},
        )
        assert result[0].rendered == SAMPLE_CALL_B

    def test_rendered_tier2_is_condensed(self):
        """Tier 2 rendered output is condensed (no EVENT ANALYSIS)."""
        leaders = [_make_leader("Watch Leader")]
        result = run_prefilter(
            leaders,
            {"Watch Leader": SAMPLE_CALL_A_FEW_THREADS},
            {"Watch Leader": SAMPLE_CALL_B_WATCH_ONLY},
        )
        assert "**EVENT ANALYSIS**" not in result[0].rendered
        assert "**ACTIVITY SUMMARY**" in result[0].rendered

    def test_rendered_tier3_is_stub(self):
        """Tier 3 rendered output is a stub with leader info."""
        leaders = [_make_leader("Quiet Leader", "President", "Quietland")]
        result = run_prefilter(
            leaders,
            {"Quiet Leader": SAMPLE_CALL_A_FEW_THREADS},
            {"Quiet Leader": SAMPLE_CALL_B_QUIET},
        )
        assert "Quiet Leader" in result[0].rendered
        assert "President" in result[0].rendered
        assert "Quietland" in result[0].rendered


class TestOrdering:
    def test_sorted_by_tier(self):
        """Results are sorted by tier (Tier 1 first, Tier 3 last)."""
        leaders = [
            _make_leader("Quiet Leader"),
            _make_leader("Watch Leader"),
            _make_leader("Leader X"),
        ]
        call_a = {
            "Quiet Leader": SAMPLE_CALL_A_FEW_THREADS,
            "Watch Leader": SAMPLE_CALL_A_FEW_THREADS,
            "Leader X": SAMPLE_CALL_A,
        }
        call_b = {
            "Quiet Leader": SAMPLE_CALL_B_QUIET,
            "Watch Leader": SAMPLE_CALL_B_WATCH_ONLY,
            "Leader X": SAMPLE_CALL_B,
        }
        result = run_prefilter(leaders, call_a, call_b)
        tiers = [r.tier for r in result]
        assert tiers == sorted(tiers)

    def test_all_tiers_present(self):
        """When leaders span all tiers, all three are represented."""
        leaders = [
            _make_leader("Quiet Leader"),
            _make_leader("Watch Leader"),
            _make_leader("Leader X"),
        ]
        call_a = {
            "Quiet Leader": SAMPLE_CALL_A_FEW_THREADS,
            "Watch Leader": SAMPLE_CALL_A_FEW_THREADS,
            "Leader X": SAMPLE_CALL_A,
        }
        call_b = {
            "Quiet Leader": SAMPLE_CALL_B_QUIET,
            "Watch Leader": SAMPLE_CALL_B_WATCH_ONLY,
            "Leader X": SAMPLE_CALL_B,
        }
        result = run_prefilter(leaders, call_a, call_b)
        tier_set = {r.tier for r in result}
        assert tier_set == {Tier.TIER_1, Tier.TIER_2, Tier.TIER_3}


class TestEdgeCases:
    def test_missing_call_a(self):
        """Leader with missing Call A output still gets tiered."""
        leaders = [_make_leader("X")]
        result = run_prefilter(leaders, {}, {"X": SAMPLE_CALL_B})
        assert len(result) == 1

    def test_missing_call_b(self):
        """Leader with missing Call B output defaults to Tier 3."""
        leaders = [_make_leader("X")]
        result = run_prefilter(leaders, {"X": SAMPLE_CALL_A_FEW_THREADS}, {})
        assert result[0].tier == Tier.TIER_3

    def test_empty_inputs(self):
        """No leaders produces empty result."""
        assert run_prefilter([], {}, {}) == []

    def test_no_event_analysis_section(self):
        """Call B with no EVENT ANALYSIS section yields empty classifications."""
        call_b = "**ATTENTION FLAGS**\n- ALERT: Something urgent.\n"
        leaders = [_make_leader("X")]
        result = run_prefilter(leaders, {"X": ""}, {"X": call_b})
        # ALERT flag alone should still give Tier 1
        assert result[0].tier == Tier.TIER_1
