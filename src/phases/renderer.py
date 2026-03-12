"""
Phase 2: Publication Renderer — renders tiered analytical inputs into
the Middle Powers Monitor weekly brief.

Single LLM call that takes pre-filtered leader assessments (tiered),
thematic clusters, key evidence, and renders them into publication format.
This module does NOT generate new analysis — it selects, organizes, and
translates existing Phase 1 analytical work.
"""

import logging
import re
from dataclasses import dataclass
from typing import Optional

from ..agents.base import complete
from ..config import MODEL_EDITORIAL, THINKING_EDITORIAL
from .prefilter import Tier, TieredLeader

logger = logging.getLogger(__name__)


# =============================================================================
# Data types
# =============================================================================

@dataclass
class Phase2Result:
    brief_text: str  # The rendered publication
    signal_count: int  # Number of signal stories detected
    leaders_with_assessment: list[str]  # Leaders who got AI Assessment
    also_tracking: list[str]  # Leaders in Also Tracking


# =============================================================================
# System prompt
# =============================================================================

SYSTEM_PROMPT = """\
You are the production editor for the Middle Powers Monitor, a
weekly intelligence publication tracking democratic leaders
defending liberal international order.

You have received analytical inputs organized by significance:
- TIER 1: Full analytical assessments for leaders with
  significant developments
- TIER 2: Condensed summaries for leaders with moderate
  developments
- TIER 3: Minimal stubs for leaders with routine weeks

You also have a Thematic Clusters Brief identifying cross-leader
patterns detected across all leaders' events.

Your job is to render these into the publication's established
format. You are NOT generating new analysis. You are selecting,
organizing, and translating existing analytical work.

CRITICAL RULE: Every claim in every AI Assessment must be
traceable to a specific statement in the corresponding Phase 1
output. Do not introduce claims, connections, or interpretations
not present in the analyst's work. If analysis is thin, the AI
Assessment should be proportionally brief."""


# =============================================================================
# Helpers
# =============================================================================

def _extract_key_evidence(call_b_text: str) -> str:
    """
    Extract the KEY EVIDENCE FOR PHASE 2 section from a Call B output.

    Returns the section body text, or empty string if not found.
    """
    pattern = re.compile(
        r"\*\*KEY EVIDENCE FOR PHASE 2\*\*\s*\n(.*?)(?=\n\*\*[A-Z]|\Z)",
        re.DOTALL,
    )
    match = pattern.search(call_b_text)
    return match.group(1).strip() if match else ""


def _build_key_evidence_appendix(tiered_leaders: list[TieredLeader]) -> str:
    """
    Aggregate KEY EVIDENCE FOR PHASE 2 sections from Tier 1 and Tier 2 outputs.

    Returns a formatted appendix string with evidence grouped by leader.
    """
    parts: list[str] = []
    for tl in tiered_leaders:
        if tl.tier not in (Tier.TIER_1, Tier.TIER_2):
            continue
        evidence = _extract_key_evidence(tl.call_b_output)
        if evidence:
            parts.append(
                f"### {tl.leader.name} ({tl.leader.title}, {tl.leader.country})\n"
                f"{evidence}"
            )
    return "\n\n".join(parts)


def _build_renderer_user_prompt(
    tiered_leaders: list[TieredLeader],
    clusters_brief: str,
    date_start: str,
    date_end: str,
    prior_brief: Optional[str] = None,
) -> str:
    """
    Assemble the full user prompt for the Phase 2 renderer LLM call.

    Combines tiered leader assessments, thematic clusters, key evidence,
    optional prior brief, and detailed formatting instructions.
    """
    # Group leaders by tier
    tier_1 = [tl for tl in tiered_leaders if tl.tier == Tier.TIER_1]
    tier_2 = [tl for tl in tiered_leaders if tl.tier == Tier.TIER_2]
    tier_3 = [tl for tl in tiered_leaders if tl.tier == Tier.TIER_3]

    # Build tier sections
    tier_1_text = "\n\n".join(tl.rendered for tl in tier_1) if tier_1 else "(No Tier 1 leaders this week.)"
    tier_2_text = "\n\n".join(tl.rendered for tl in tier_2) if tier_2 else "(No Tier 2 leaders this week.)"
    tier_3_text = "\n\n".join(tl.rendered for tl in tier_3) if tier_3 else "(No Tier 3 leaders this week.)"

    # Build key evidence appendix
    key_evidence = _build_key_evidence_appendix(tiered_leaders)
    if not key_evidence:
        key_evidence = "(No key evidence extracts available.)"

    # Prior brief section (conditional)
    prior_brief_section = ""
    if prior_brief:
        prior_brief_section = (
            f"\n---\n\n"
            f"## PRIOR WEEK'S BRIEF (for continuity)\n\n"
            f"{prior_brief}\n"
        )

    return f"""\
## ANALYTICAL INPUTS

[NOTE: Leaders are organized by analytical significance.
Randomized within tiers. Tier assignment reflects this week's
significance, not overall importance.]

### TIER 1: Full Assessments
[These leaders had significant developments. Complete analytical
assessment available.]

{tier_1_text}

### TIER 2: Condensed Summaries
[Moderate developments. Activity summary, cross-leader
connections, between the lines, falsification, and key evidence
available.]

{tier_2_text}

### TIER 3: Quiet Weeks
[Routine weeks. Activity level and active thread titles only.]

{tier_3_text}

---

## THEMATIC CLUSTERS BRIEF

{clusters_brief}

---

## KEY EVIDENCE APPENDIX (Tier 1 + Tier 2)

{key_evidence}
{prior_brief_section}
---

## INSTRUCTIONS

Produce the Middle Powers Monitor weekly brief for the week of
{date_start} to {date_end}.

### Step 1: Selection

**SIGNAL STORIES (1-3):**
Draw exclusively from Tier 1 leaders. Select based on:
- STRUCTURAL or ALERT attention flags
- SIGNIFICANT SHIFT or POTENTIAL STRUCTURAL CHANGE classifications
- NOTABLE clusters in the Thematic Clusters Brief
- Impact on middle power coordination / liberal order defense

If no events meet the SIGNIFICANT SHIFT threshold, select the
most consequential TACTICAL ADJUSTMENT developments. Do not force
drama — a consolidation week should read as such.

**AI ASSESSMENT SELECTION (Regional Briefs):**
- Tier 1 leaders: always include AI Assessment
- Tier 2 leaders: include when Between the Lines or falsification
  criteria contain non-obvious analytical substance
- Tier 3 leaders: no AI Assessment

**ALSO TRACKING:**
- Low-priority Key Actions from Tier 1 and Tier 2
- Tier 3 leaders with active threads worth noting
- Domestic events with minimal foreign policy implications
- If a Tier 3 leader is named in the Thematic Clusters Brief,
  include them in Also Tracking with a note about the connection

### Step 2: Write the Brief

Use this exact structure:

---

# The Middle Powers Monitor

## Week of {date_start} to {date_end}

[Opening paragraph: 2-3 sentences identifying the week's most
significant developments across all leaders. Direct, concrete,
no throat-clearing.]

---

## This Week's Signal

[For each Signal story (1-3):]

### [FLAG EMOJI] [Headline]

**BLUF:** [1-2 sentences. What happened, stated plainly.]

- [Bullet points: key facts from structured summary and key
  evidence appendix. No analysis in bullets.]

**AI Assessment:** [3-5 sentences. Draw EXCLUSIVELY from Phase 1
analytical assessment. Translate analyst jargon into accessible
prose. Drop claim references. Preserve analytical substance:
structural grounding, running picture trajectory, deviation
classification, falsification criteria as "watch for" language.]

---

## Regional Briefs

[Group leaders by region:]
- North America
- South America
- Europe
- Baltic States

[For each leader:]

#### [FLAG EMOJI] [Country] / [Leader Name]

- [3-6 bullets for active weeks, 1-2 for quiet weeks]

[If AI Assessment selected:]

**AI Assessment:** [2-4 sentences. Focus on single most important
analytical point.]

---

## Also Tracking

- **[Country]:** [1 sentence items]

---

*[Methodology line: leaders monitored, sources processed, date
range, notable gaps.]*

### Writing Guidelines

TONE: Informed, direct, occasionally dry. Wire service clarity
with analyst depth.

BULLETS: Factual, concrete. No analysis — that's the AI
Assessment's job.

AI ASSESSMENTS: Answer "so what?" Use "watch for" language.
Never bluff depth. If the analyst's assessment is thin, keep
the AI Assessment short.

TIER RULES:
- Signal stories from Tier 1 only
- AI Assessments from Tier 1 (always) and Tier 2 (selective)
- Tier 3 in Also Tracking only (or omitted if no active threads)
- If Thematic Clusters Brief identifies a pattern involving a
  Tier 2 or Tier 3 leader, ensure that pattern is surfaced
  somewhere in the brief

DO NOT:
- Introduce analysis not present in Phase 1 outputs
- Produce AI Assessments for every leader
- Repeat analytical observations from prior week without new
  evidence
- Editorialize about whether actions are good or bad"""


# =============================================================================
# Output parsing
# =============================================================================

def _parse_brief_metadata(brief_text: str) -> Phase2Result:
    """
    Parse the rendered brief to extract metadata: signal story count,
    leaders with AI Assessments, and Also Tracking leaders.
    """
    # Count signal stories: look for ### headers under "This Week's Signal"
    signal_section_match = re.search(
        r"## This Week's Signal\s*\n(.*?)(?=\n## (?!This Week)|\Z)",
        brief_text,
        re.DOTALL,
    )
    signal_count = 0
    if signal_section_match:
        signal_body = signal_section_match.group(1)
        signal_count = len(re.findall(r"^###\s+.+", signal_body, re.MULTILINE))

    # Find leaders with AI Assessments: look for "#### ... / Leader Name"
    # followed later by "**AI Assessment:**"
    leaders_with_assessment: list[str] = []

    # Match leader headers in Regional Briefs and Signal stories
    leader_header_pattern = re.compile(
        r"(?:####|###)\s+.+?/\s*(.+?)$",
        re.MULTILINE,
    )

    # Split the brief into chunks around leader headers to check for AI Assessment
    parts = re.split(r"(?=(?:####|###)\s+)", brief_text)
    for part in parts:
        header_match = leader_header_pattern.match(part)
        if header_match:
            leader_name = header_match.group(1).strip()
            if re.search(r"\*\*AI Assessment:?\*\*", part):
                if leader_name not in leaders_with_assessment:
                    leaders_with_assessment.append(leader_name)

    # Also check signal stories for AI Assessments with leader names
    # Signal stories use format "### [FLAG] Headline" — leader names may
    # appear in BLUF or body, but we already caught #### headers above.

    # Parse Also Tracking section
    also_tracking: list[str] = []
    tracking_match = re.search(
        r"## Also Tracking\s*\n(.*?)(?=\n---|\n##|\n\*\[|\Z)",
        brief_text,
        re.DOTALL,
    )
    if tracking_match:
        tracking_body = tracking_match.group(1)
        # Match "- **Country:**" pattern
        for m in re.finditer(r"-\s+\*\*(.+?)\*\*", tracking_body):
            country = m.group(1).rstrip(":")
            if country not in also_tracking:
                also_tracking.append(country)

    return Phase2Result(
        brief_text=brief_text,
        signal_count=signal_count,
        leaders_with_assessment=leaders_with_assessment,
        also_tracking=also_tracking,
    )


# =============================================================================
# Main entry point
# =============================================================================

async def run_renderer(
    tiered_leaders: list[TieredLeader],
    clusters_brief: str,
    date_start: str,
    date_end: str,
    prior_brief: Optional[str] = None,
) -> Phase2Result:
    """
    Render the Middle Powers Monitor weekly brief from tiered analytical inputs.

    Makes a single LLM call using the editorial model (Opus) to produce
    the publication-format brief from pre-filtered Phase 1 outputs.

    Args:
        tiered_leaders: Pre-filtered and tiered leader assessments from prefilter.
        clusters_brief: Thematic clusters text from cross-correlation pass.
        date_start: Start date of the reporting period (e.g. "2026-03-01").
        date_end: End date of the reporting period (e.g. "2026-03-07").
        prior_brief: Optional prior week's brief for continuity reference.

    Returns:
        Phase2Result with the rendered brief and extracted metadata.
    """
    user_prompt = _build_renderer_user_prompt(
        tiered_leaders=tiered_leaders,
        clusters_brief=clusters_brief,
        date_start=date_start,
        date_end=date_end,
        prior_brief=prior_brief,
    )

    tier_counts = {t: 0 for t in Tier}
    for tl in tiered_leaders:
        tier_counts[tl.tier] += 1

    logger.info(
        "Phase 2 renderer: %d leaders (T1=%d, T2=%d, T3=%d), "
        "clusters_brief=%d chars, prior_brief=%s",
        len(tiered_leaders),
        tier_counts[Tier.TIER_1],
        tier_counts[Tier.TIER_2],
        tier_counts[Tier.TIER_3],
        len(clusters_brief),
        "yes" if prior_brief else "no",
    )

    brief_text = await complete(
        prompt=user_prompt,
        system=SYSTEM_PROMPT,
        model=MODEL_EDITORIAL,
        max_tokens=30000,
        thinking_budget=THINKING_EDITORIAL,
    )

    result = _parse_brief_metadata(brief_text)

    logger.info(
        "Phase 2 renderer complete: %d chars, %d signal stories, "
        "%d leaders with assessment, %d in also tracking",
        len(result.brief_text),
        result.signal_count,
        len(result.leaders_with_assessment),
        len(result.also_tracking),
    )

    return result
