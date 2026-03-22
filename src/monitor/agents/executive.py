"""
Executive agent: global-level synthesis from regional reports.

Input: 5 regional reports + global ledger (prior state).
Output: Updated global ledger (dynamics, watchlist, briefing items, triage implications).
"""

import json
import logging
import re
from datetime import date
from typing import Optional

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    DynamicStatus,
    LinkageType,
    Region,
    SignalCategory,
)
from ..agents.regional import RegionalReport
from ..models import (
    ActiveDynamic,
    EvidenceStrength,
    ExecutiveBriefingItem,
    GlobalLedger,
    GlobalPostureSummary,
    GlobalSelfCorrection,
    GlobalWeeklyEntry,
    RejectedItem,
    SignalEnvironment,
    TriageImplication,
    WatchlistItem,
)

logger = logging.getLogger(__name__)


# =============================================================================
# System prompt
# =============================================================================

EXECUTIVE_SYSTEM_PROMPT = """\
## Role

You are the executive analyst for the Middle Powers Monitor, a weekly geopolitical \
intelligence publication. You sit at the top of a three-layer analytical system: 28 \
country desks feed into 5 regional syntheses, which feed into you. Your job is to \
identify the 3-5 developments, patterns, or structural shifts that are visible only at \
the global level — things that no single region reveals on its own.

You also maintain the global analytical ledger — the system's institutional memory at \
the highest level. You track cross-country dynamics over time, maintain a watchlist of \
items worth monitoring, and generate triage implications that steer where the pipeline \
directs its attention next week.

Your output has two audiences. The executive briefing items become the lead section of \
the newsletter — the part sophisticated readers subscribe for. The global ledger update \
is infrastructure that the pipeline's triage agent reads next week. Both must be excellent.

---

## Your Inputs

**REGIONAL REPORTS** — Five regional syntheses, each containing: cross-cutting dynamics \
with confidence scores and linkage assessments, rejected dynamics, gaps, and \
low-confidence quarantine items. These are your primary analytical material.

**GLOBAL LEDGER (prior state)** — Your own running analytical record from last week. It \
contains:
- `global_posture_summary`: your prior assessment of the global signal environment
- `active_dynamics`: cross-country patterns you've been tracking, with status, evidence \
strength, and triage implications
- `watchlist`: items worth monitoring that haven't risen to dynamic status
- Recent weekly entries: what you wrote in prior weeks, including self-corrections
- `archived_dynamics`: resolved patterns preserved for reference

Read the ledger carefully. Your job is to assess what changed this week relative to what \
you already believe, not to start fresh. New dynamics emerge. Existing dynamics strengthen, \
weaken, or resolve. Your prior self-corrections tell you where your analytical instincts \
have been wrong.

---

## Your Process

### Phase 1: Identify Candidates

Read all five regional reports. Identify 5-8 candidate strategic themes based on:

- **Cross-regional patterns:** The same dynamic appearing in two or more regions. If \
sovereignty signaling appears in the Americas report and the Western Europe report, that's \
a candidate for a global dynamic that neither region can see on its own.
- **Interaction effects across regions:** A development in one region creating consequences \
in another. European defense procurement decisions affecting Asia-Pacific deterrence \
calculus. Middle East instability creating diplomatic opportunities for Pivot states.
- **Structural shifts:** Changes that alter the operating environment for multiple countries \
simultaneously. A US policy change, a commodity price shock, an institutional development \
(UN vote, WTO ruling) that reshapes constraints across regions.
- **Significant absences:** Something the global posture summary predicted or the active \
dynamics anticipated that didn't materialize in any regional report.

Also check your active dynamics from last week. For each one, look for evidence in this \
week's regional reports that the dynamic is strengthening, weakening, stable, or resolved.

### Phase 2: Evaluate Against Prior State

For each candidate theme, check it against the global ledger:

- **Is this a continuation of an existing dynamic?** If so, update the dynamic's status \
and assessment rather than creating a new one. Has the evidence strengthened or weakened? \
Has the pattern expanded to new countries or contracted?
- **Is this genuinely new?** A dynamic that doesn't map to any existing entry in the \
ledger. Create it with status `emerging`.
- **Does this contradict a prior assessment?** If so, log a self-correction. What did you \
get wrong and why?
- **Does a prior dynamic need to be archived?** If the evidence no longer supports it, or \
if it has resolved (the event it was tracking concluded), move it to archived status with a \
closing assessment.

### Phase 3: Synthesize

Select the 3-5 themes that meet the bar for the executive briefing. The bar is:

- Visible only at the global or system level — not a regional dynamic repackaged
- Represents a structural change in the international order, or an emergent pattern with \
structural implications
- Would change how an informed observer understands what is happening in the world

For each theme, write:
- **What**: What is happening. 2-3 sentences of analytical description, not news summary.
- **Why it matters**: Strategic significance. 2-3 sentences explaining what this means for \
the international order, for middle-power positioning, or for the publication's core thesis \
about rhetorical vs. structural alignment with the liberal international order.
- **What to watch**: Leading indicators for next week. What would confirm, weaken, or \
resolve this theme?
- **Confidence**: Score with provenance. Which regional dynamics support it? What are their \
confidence scores? What's the weakest underlying country-level confidence? If the theme \
rests on low-confidence data, say so.
- **Competing narrative**: The strongest alternative strategic interpretation. Not a \
strawman — a genuine alternative that explains the same evidence differently.

### Phase 4: Update the Global Ledger

**Active dynamics:** Create, update, or archive dynamics based on this week's analysis.

For each active dynamic, update:
- `current_assessment` — what you now believe
- `status` — emerging, developing, established, monitoring, weakening, resolved
- `evidence_strength` — updated confidence, supporting country confidences, weakest link
- `triage_implications` — which countries should the triage agent flag next week, and why

For new dynamics, provide all fields including `competing_interpretation` and `what_to_watch`.

For dynamics unchanged this week, increment `consecutive_unchanged_weeks`. If this reaches \
3, you should either update the assessment with new reasoning, downgrade to monitoring, or \
archive it. Dynamics should not sit unchanged indefinitely.

**Watchlist:** Add items worth tracking that don't yet warrant a full dynamic entry. Remove \
items that have either been promoted to active dynamics or have become irrelevant.

**Global posture summary:** Rewrite the summary to reflect this week's analysis. Update \
the signal environment (most active categories, hotspots, quiet zones).

### Phase 5: Rejection Log

Record themes you considered for the executive briefing but rejected. For each, explain \
specifically why it didn't rise to executive-level significance. This is mandatory — an \
empty rejection log signals insufficient critical evaluation.

Common valid reasons for rejection:
- The pattern is regional, not global (belongs in the regional report, not the executive \
brief)
- The evidence is too thin (low-confidence country data propagating upward)
- The pattern is a continuation of a known dynamic without meaningful change this week \
(worth tracking, not worth featuring)
- On closer examination, the apparent cross-regional pattern is driven by coincidence \
rather than connection

---

## Tone and Voice

The executive briefing items will be rendered as the lead section of a weekly newsletter. \
Write them with the confidence and voice of a senior analytical publication — authoritative \
but engaging, structurally informed but readable.

- State uncertainty where it exists without apologizing for it. "The evidence is suggestive \
but incomplete" is stronger than "We're not sure."
- Avoid hedging language that drains analytical content. "This may or may not indicate a \
shift" says nothing. "The evidence points toward a shift but rests on single-source \
reporting from two of three countries" says something useful.
- The reader is a sophisticated generalist — someone who reads Foreign Affairs and The \
Economist, follows geopolitics seriously, but doesn't track 28 countries daily. Write for \
that person.

---

## Your Output

Return valid JSON with a single top-level object `global_ledger_update`:

```json
{
  "global_ledger_update": {
    "global_posture_summary": {
      "as_of": "{{ANALYSIS_DATE}}",
      "text": "3-5 sentence summary of the global analytical environment...",
      "signal_environment": {
        "most_active_categories": ["...", "..."],
        "quietest_categories": ["..."],
        "geographic_hotspots": ["..."],
        "geographic_quiet_zones": ["..."]
      }
    },

    "active_dynamics": [
      {
        "dynamic_id": 1,
        "title": "...",
        "created_week": "...",
        "last_updated": "{{ANALYSIS_DATE}}",
        "status": "emerging | developing | established | monitoring | weakening | resolved",
        "current_assessment": "...",
        "countries_involved": ["...", "..."],
        "signal_categories_touched": ["...", "..."],
        "evidence_strength": {
          "confidence": 3,
          "supporting_country_confidences": {"mx": 4, "in": 2},
          "weakest_link": "...",
          "linkage_type": "parallel_behavior | interaction_effect | institutional | absence",
          "linkage_assessment": "..."
        },
        "competing_interpretation": "...",
        "what_to_watch": "...",
        "triage_implications": {
          "countries_to_flag": ["...", "..."],
          "reason": "..."
        },
        "weeks_active": 2,
        "consecutive_unchanged_weeks": 0
      }
    ],

    "watchlist": [
      {
        "item": "...",
        "signal_category": "...",
        "countries": ["...", "..."],
        "why_it_matters": "...",
        "trigger": "...",
        "added_week": "{{ANALYSIS_DATE}}"
      }
    ],

    "weekly_entry": {
      "week": "{{ANALYSIS_DATE}}",
      "executive_briefing_items": [
        {
          "title": "Theme title",
          "regions_involved": ["...", "..."],
          "what": "What is happening (2-3 sentences)...",
          "why_it_matters": "Strategic significance (2-3 sentences)...",
          "what_to_watch": "Leading indicators for next week...",
          "confidence": 3,
          "confidence_note": "Provenance: which regional dynamics, what scores, weakest link..."
        }
      ],
      "dynamics_created": [],
      "dynamics_updated": [],
      "dynamics_archived": [],
      "items_considered_rejected": [
        {
          "candidate": "...",
          "reason_rejected": "..."
        }
      ],
      "self_corrections": []
    }
  }
}
```

### Notes on Dynamic Management

- When creating a new dynamic, assign the next available `dynamic_id` (one higher than \
the current maximum).
- When archiving a dynamic, move it from `active_dynamics` to a separate list and set \
status to `resolved`. Include a `closing_assessment` explaining why it was archived.
- Dynamics with `triage_implications` directly influence next week's triage decisions. Be \
deliberate about which countries you flag and why. Overflagging dilutes the signal. \
Underflagging means the pipeline misses what you've identified as important.
- The `competing_interpretation` on each dynamic is not decorative. It should be the \
interpretation that, if true, would most change the strategic picture. If you find yourself \
writing weak competing interpretations, the dynamic itself may be underdetermined.

---

## What You Must Not Do

- Do not summarize regional reports. The reader can read the regional sections. Your job is \
to find what no single region reveals on its own.
- Do not create dynamics without cross-regional evidence. A dynamic involving only countries \
from one region belongs in that region's report, not in the global ledger.
- Do not carry forward dynamics unchanged for more than 3 consecutive weeks. If nothing has \
changed, either the dynamic has stalled (downgrade or archive) or you're not looking hard \
enough (update the assessment with a reassessment of why it's static).
- Do not generate more than 8 triage implications across all active dynamics combined. If \
you're flagging more than 8 countries through triage implications, you're micromanaging \
the desks.
- Do not fabricate confidence provenance. If you don't know the underlying country \
confidence for a claim, say so — don't invent numbers.
- Do not let the executive briefing items and the global ledger dynamics diverge. Every \
briefing item should connect to an active dynamic. Every significant active dynamic should \
either be reflected in a briefing item or have an explanation for why it wasn't featured \
this week.

No commentary outside the JSON."""


# =============================================================================
# Prompt construction
# =============================================================================

def _format_regional_report(report: RegionalReport) -> str:
    """Format a regional report for executive synthesis input."""
    lines = [f"### {report.region.value}\n"]

    if report.cross_cutting_dynamics:
        for d in report.cross_cutting_dynamics:
            lines.append(f"**{d.title}**")
            lines.append(f"  Countries: {', '.join(d.countries_involved)}")
            lines.append(f"  Categories: {', '.join(d.signal_categories)}")
            lines.append(f"  Pattern: {d.pattern_type} ({d.linkage_strength})")
            lines.append(f"  Assessment: {d.assessment}")
            lines.append(f"  Significance: {d.significance}")
            lines.append(f"  Trend: {d.trend}")
            lines.append(f"  Confidence: {d.confidence} (inherited: {d.confidence_inherited_from})")
            lines.append(f"  Weakest link: {d.weakest_link}")
            lines.append(f"  Evidence against linkage: {d.evidence_against_linkage}")
            lines.append(f"  Competing interpretation: {d.competing_interpretation}")
            lines.append("")
    else:
        lines.append("No cross-cutting dynamics identified.")
        lines.append("")

    if report.dynamics_considered_and_rejected:
        lines.append("Rejected dynamics:")
        for r in report.dynamics_considered_and_rejected:
            lines.append(f"  - {r.candidate_dynamic}: {r.reason_rejected}")
        lines.append("")

    if report.gaps:
        lines.append("Gaps:")
        for g in report.gaps:
            lines.append(f"  - {g.expected_dynamic}: {g.assessment}")
        lines.append("")

    if report.low_confidence_items:
        lines.append("Low-confidence items:")
        for lc in report.low_confidence_items:
            lines.append(f"  - {lc.origin}: {lc.item} (confidence {lc.confidence})")
        lines.append("")

    return "\n".join(lines)


def _format_global_ledger_state(gl: GlobalLedger) -> str:
    """Format the current global ledger state for the executive agent."""
    lines = ["## CURRENT GLOBAL LEDGER STATE\n"]
    lines.append(f"Last updated: {gl.last_updated.isoformat()}")
    lines.append(f"Posture: {gl.global_posture_summary.text}")
    lines.append("")

    if gl.active_dynamics:
        lines.append(f"### Active Dynamics ({len(gl.active_dynamics)})\n")
        for d in gl.active_dynamics:
            lines.append(f"**Dynamic #{d.dynamic_id}: {d.title}**")
            lines.append(f"  Status: {d.status.value}, weeks active: {d.weeks_active}, "
                          f"unchanged weeks: {d.consecutive_unchanged_weeks}")
            lines.append(f"  Countries: {', '.join(d.countries_involved)}")
            lines.append(f"  Assessment: {d.current_assessment}")
            lines.append(f"  Confidence: {d.evidence_strength.confidence}")
            if d.competing_interpretation:
                lines.append(f"  Competing interpretation: {d.competing_interpretation}")
            if d.what_to_watch:
                lines.append(f"  What to watch: {d.what_to_watch}")
            if d.triage_implications and d.triage_implications.countries_to_flag:
                lines.append(f"  Triage flags: {', '.join(d.triage_implications.countries_to_flag)}")
            if d.consecutive_unchanged_weeks >= 3:
                lines.append(f"  ⚠ STALE: unchanged for {d.consecutive_unchanged_weeks} weeks — "
                              "must update, downgrade, or archive.")
            lines.append("")
    else:
        lines.append("No active dynamics.\n")

    if gl.watchlist:
        lines.append(f"### Watchlist ({len(gl.watchlist)})\n")
        for i, w in enumerate(gl.watchlist):
            lines.append(f"  [{i}] {w.item} (countries: {', '.join(w.countries)}, "
                          f"trigger: {w.trigger})")
        lines.append("")

    # Recent weekly entries (for self-correction context)
    if gl.weekly_entries:
        recent = gl.weekly_entries[-3:]  # last 3 weeks
        lines.append(f"### Recent Weekly Entries ({len(recent)} shown)\n")
        for we in recent:
            lines.append(f"Week {we.week.isoformat()}:")
            lines.append(f"  Briefing items: {len(we.executive_briefing_items)}")
            lines.append(f"  Dynamics created: {we.dynamics_created}")
            lines.append(f"  Dynamics updated: {we.dynamics_updated}")
            lines.append(f"  Dynamics archived: {we.dynamics_archived}")
            if we.self_corrections:
                lines.append(f"  Self-corrections: {len(we.self_corrections)}")
                for sc in we.self_corrections:
                    lines.append(f"    - Dynamic #{sc.dynamic_id}: {sc.correction}")
            lines.append("")

    return "\n".join(lines)


def _build_executive_prompt(
    regional_reports: dict[Region, RegionalReport],
    global_ledger: GlobalLedger,
) -> str:
    # Regional reports
    regional_sections = []
    for region in Region:
        if region in regional_reports:
            regional_sections.append(_format_regional_report(regional_reports[region]))
        else:
            regional_sections.append(f"### {region.value}\n\nNo report available.\n")

    # Global ledger state
    gl_state = _format_global_ledger_state(global_ledger)

    return f"""\
## REGIONAL REPORTS

{chr(10).join(regional_sections)}

{gl_state}

Synthesize the regional reports, update the global ledger, and produce the executive \
briefing items as specified in your instructions."""


# =============================================================================
# Response parsing & ledger update
# =============================================================================

def parse_executive_response(response_text: str) -> dict:
    """Parse the executive agent's JSON response.

    Handles both the new wrapped format (global_ledger_update) and the old flat format.
    """
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)

    data = json.loads(text)

    # Unwrap if using the new spec format
    if "global_ledger_update" in data:
        data = data["global_ledger_update"]

    return data


def _parse_active_dynamic(d: dict, week: date) -> ActiveDynamic:
    """Parse a single active dynamic from JSON."""
    es = d.get("evidence_strength", {})
    ti = d.get("triage_implications", {})

    created_week = week
    if "created_week" in d:
        try:
            created_week = date.fromisoformat(str(d["created_week"]))
        except (ValueError, TypeError):
            created_week = week

    last_updated = week
    if "last_updated" in d:
        try:
            last_updated = date.fromisoformat(str(d["last_updated"]))
        except (ValueError, TypeError):
            last_updated = week

    return ActiveDynamic(
        dynamic_id=d["dynamic_id"],
        title=d["title"],
        created_week=created_week,
        last_updated=last_updated,
        status=DynamicStatus(d.get("status", "emerging")),
        current_assessment=d["current_assessment"],
        countries_involved=d.get("countries_involved", []),
        signal_categories_touched=[
            SignalCategory(c) for c in d.get("signal_categories_touched", [])
        ],
        evidence_strength=EvidenceStrength(
            confidence=es.get("confidence", 3),
            supporting_country_confidences=es.get("supporting_country_confidences", {}),
            weakest_link=es.get("weakest_link", ""),
            linkage_type=LinkageType(es.get("linkage_type", "parallel_behavior")),
            linkage_assessment=es.get("linkage_assessment", ""),
        ),
        competing_interpretation=d.get("competing_interpretation", ""),
        what_to_watch=d.get("what_to_watch", ""),
        triage_implications=TriageImplication(
            countries_to_flag=ti.get("countries_to_flag", []),
            reason=ti.get("reason", ""),
        ),
        weeks_active=d.get("weeks_active", 1),
        consecutive_unchanged_weeks=d.get("consecutive_unchanged_weeks", 0),
    )


def _parse_watchlist_item(w: dict, week: date) -> WatchlistItem:
    """Parse a single watchlist item from JSON."""
    added_week = week
    if "added_week" in w:
        try:
            added_week = date.fromisoformat(str(w["added_week"]))
        except (ValueError, TypeError):
            added_week = week

    return WatchlistItem(
        item=w["item"],
        signal_category=SignalCategory(w["signal_category"]),
        countries=w.get("countries", []),
        why_it_matters=w.get("why_it_matters", ""),
        trigger=w.get("trigger", ""),
        added_week=added_week,
    )


def apply_executive_output(
    global_ledger: GlobalLedger,
    data: dict,
    week: date,
) -> GlobalLedger:
    """Apply the executive agent's output to the global ledger.

    Supports both the new full-state format (active_dynamics + weekly_entry)
    and the old delta format (dynamics_to_create/update/archive).
    """

    # Update global posture summary
    gps = data["global_posture_summary"]
    as_of = week
    if "as_of" in gps:
        try:
            as_of = date.fromisoformat(str(gps["as_of"]))
        except (ValueError, TypeError):
            as_of = week

    global_ledger.global_posture_summary = GlobalPostureSummary(
        as_of=as_of,
        text=gps["text"],
        signal_environment=SignalEnvironment(
            most_active_categories=[
                SignalCategory(c) for c in gps.get("signal_environment", {}).get("most_active_categories", [])
            ],
            quietest_categories=[
                SignalCategory(c) for c in gps.get("signal_environment", {}).get("quietest_categories", [])
            ],
            geographic_hotspots=gps.get("signal_environment", {}).get("geographic_hotspots", []),
            geographic_quiet_zones=gps.get("signal_environment", {}).get("geographic_quiet_zones", []),
        ),
    )

    # Detect format: new full-state vs old delta
    if "active_dynamics" in data:
        return _apply_full_state(global_ledger, data, week)
    else:
        return _apply_delta(global_ledger, data, week)


def _apply_full_state(
    global_ledger: GlobalLedger,
    data: dict,
    week: date,
) -> GlobalLedger:
    """Apply the new full-state format where LLM outputs complete active_dynamics list."""

    # Parse the full active dynamics list from output
    new_dynamics = [
        _parse_active_dynamic(d, week)
        for d in data.get("active_dynamics", [])
    ]

    # Determine archived dynamics from weekly_entry metadata
    we_data = data.get("weekly_entry", {})
    archived_ids = set(we_data.get("dynamics_archived", []))

    # Move archived dynamics from prior state
    if archived_ids:
        to_archive = [
            d for d in global_ledger.active_dynamics
            if d.dynamic_id in archived_ids
        ]
        for d in to_archive:
            d.status = DynamicStatus.RESOLVED
        global_ledger.archived_dynamics.extend(to_archive)

    # Replace active dynamics with new list
    global_ledger.active_dynamics = new_dynamics

    # Replace watchlist with new list
    global_ledger.watchlist = [
        _parse_watchlist_item(w, week)
        for w in data.get("watchlist", [])
    ]

    # Build weekly entry
    _build_and_append_weekly_entry(global_ledger, we_data, week)

    global_ledger.last_updated = week
    return global_ledger


def _apply_delta(
    global_ledger: GlobalLedger,
    data: dict,
    week: date,
) -> GlobalLedger:
    """Apply the old delta format (dynamics_to_create/update/archive)."""

    # Track IDs for weekly entry
    created_ids = []
    updated_ids = []
    archived_ids = list(data.get("dynamics_to_archive", []))

    # Create new dynamics
    for d in data.get("dynamics_to_create", []):
        new_id = global_ledger.next_dynamic_id()
        es = d.get("evidence_strength", {})
        ti = d.get("triage_implications", {})
        dynamic = ActiveDynamic(
            dynamic_id=new_id,
            title=d["title"],
            created_week=week,
            last_updated=week,
            status=DynamicStatus(d.get("status", "emerging")),
            current_assessment=d["current_assessment"],
            countries_involved=d.get("countries_involved", []),
            signal_categories_touched=[
                SignalCategory(c) for c in d.get("signal_categories_touched", [])
            ],
            evidence_strength=EvidenceStrength(
                confidence=es.get("confidence", 3),
                supporting_country_confidences=es.get("supporting_country_confidences", {}),
                weakest_link=es.get("weakest_link", ""),
                linkage_type=LinkageType(es.get("linkage_type", "parallel_behavior")),
                linkage_assessment=es.get("linkage_assessment", ""),
            ),
            competing_interpretation=d.get("competing_interpretation", ""),
            what_to_watch=d.get("what_to_watch", ""),
            triage_implications=TriageImplication(
                countries_to_flag=ti.get("countries_to_flag", []),
                reason=ti.get("reason", ""),
            ),
            weeks_active=1,
            consecutive_unchanged_weeks=0,
        )
        global_ledger.active_dynamics.append(dynamic)
        created_ids.append(new_id)

    # Update existing dynamics
    for u in data.get("dynamics_to_update", []):
        did = u["dynamic_id"]
        for dynamic in global_ledger.active_dynamics:
            if dynamic.dynamic_id == did:
                dynamic.last_updated = week
                dynamic.status = DynamicStatus(u["status"])
                dynamic.current_assessment = u["current_assessment"]
                dynamic.countries_involved = u.get("countries_involved", dynamic.countries_involved)
                if "evidence_strength" in u:
                    es = u["evidence_strength"]
                    dynamic.evidence_strength = EvidenceStrength(
                        confidence=es.get("confidence", dynamic.evidence_strength.confidence),
                        supporting_country_confidences=es.get(
                            "supporting_country_confidences",
                            dynamic.evidence_strength.supporting_country_confidences,
                        ),
                        weakest_link=es.get("weakest_link", dynamic.evidence_strength.weakest_link),
                        linkage_type=LinkageType(es.get("linkage_type", dynamic.evidence_strength.linkage_type.value)),
                        linkage_assessment=es.get("linkage_assessment", dynamic.evidence_strength.linkage_assessment),
                    )
                if "competing_interpretation" in u:
                    dynamic.competing_interpretation = u["competing_interpretation"]
                if "what_to_watch" in u:
                    dynamic.what_to_watch = u["what_to_watch"]
                if "triage_implications" in u:
                    ti = u["triage_implications"]
                    dynamic.triage_implications = TriageImplication(
                        countries_to_flag=ti.get("countries_to_flag", []),
                        reason=ti.get("reason", ""),
                    )
                dynamic.weeks_active += 1
                dynamic.consecutive_unchanged_weeks = 0
                updated_ids.append(did)
                break

    # Increment unchanged weeks for dynamics not updated or just created
    for dynamic in global_ledger.active_dynamics:
        if (dynamic.dynamic_id not in updated_ids
                and dynamic.dynamic_id not in archived_ids
                and dynamic.dynamic_id not in created_ids):
            dynamic.consecutive_unchanged_weeks += 1
            dynamic.weeks_active += 1

    # Archive dynamics
    if archived_ids:
        to_archive = [d for d in global_ledger.active_dynamics if d.dynamic_id in archived_ids]
        for d in to_archive:
            d.status = DynamicStatus.RESOLVED
        global_ledger.archived_dynamics.extend(to_archive)
        global_ledger.active_dynamics = [
            d for d in global_ledger.active_dynamics if d.dynamic_id not in archived_ids
        ]

    # Update watchlist
    remove_indices = set(data.get("watchlist_remove_indices", []))
    if remove_indices:
        global_ledger.watchlist = [
            w for i, w in enumerate(global_ledger.watchlist) if i not in remove_indices
        ]
    for w in data.get("watchlist_add", []):
        global_ledger.watchlist.append(WatchlistItem(
            item=w["item"],
            signal_category=SignalCategory(w["signal_category"]),
            countries=w.get("countries", []),
            why_it_matters=w.get("why_it_matters", ""),
            trigger=w.get("trigger", ""),
            added_week=week,
        ))

    # Build weekly entry
    we_data = {
        "executive_briefing_items": data.get("executive_briefing_items", []),
        "dynamics_created": created_ids,
        "dynamics_updated": updated_ids,
        "dynamics_archived": archived_ids,
        "items_considered_rejected": data.get("items_considered_rejected",
                                              [{"candidate": "None", "reason_rejected": "N/A"}]),
        "self_corrections": data.get("self_corrections", []),
    }
    _build_and_append_weekly_entry(global_ledger, we_data, week)

    global_ledger.last_updated = week
    return global_ledger


def _build_and_append_weekly_entry(
    global_ledger: GlobalLedger,
    we_data: dict,
    week: date,
) -> None:
    """Build a GlobalWeeklyEntry from parsed data and append to the ledger."""
    briefing_items = [
        ExecutiveBriefingItem(
            title=b["title"],
            regions_involved=b.get("regions_involved", []),
            what=b["what"],
            why_it_matters=b["why_it_matters"],
            what_to_watch=b.get("what_to_watch", ""),
            confidence=b.get("confidence", 3),
            confidence_note=b.get("confidence_note", ""),
        )
        for b in we_data.get("executive_briefing_items", [])
    ]

    rejected = [
        RejectedItem(
            candidate=r["candidate"],
            reason_rejected=r["reason_rejected"],
        )
        for r in we_data.get("items_considered_rejected",
                             [{"candidate": "None", "reason_rejected": "N/A"}])
    ]

    corrections = [
        GlobalSelfCorrection(
            dynamic_id=s["dynamic_id"],
            prior_assessment=s["prior_assessment"],
            correction=s["correction"],
            root_cause=s["root_cause"],
        )
        for s in we_data.get("self_corrections", [])
    ]

    weekly_entry = GlobalWeeklyEntry(
        week=week,
        executive_briefing_items=briefing_items,
        dynamics_created=we_data.get("dynamics_created", []),
        dynamics_updated=we_data.get("dynamics_updated", []),
        dynamics_archived=we_data.get("dynamics_archived", []),
        items_considered_rejected=rejected,
        self_corrections=corrections,
    )
    global_ledger.weekly_entries.append(weekly_entry)


# =============================================================================
# Entry point
# =============================================================================

async def run_executive_agent(
    regional_reports: dict[Region, RegionalReport],
    global_ledger: GlobalLedger,
    week: date | None = None,
) -> GlobalLedger:
    """
    Run the executive synthesis agent.

    Updates the global ledger in place and returns it.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    week = week or date.today()
    prompt = _build_executive_prompt(regional_reports, global_ledger)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    logger.info("Running executive synthesis")

    response = await client.messages.create(
        model=MODEL,
        max_tokens=12288,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": EXECUTIVE_SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": prompt}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        f"Executive synthesis: input={response.usage.input_tokens}, "
        f"output={response.usage.output_tokens}"
    )

    data = parse_executive_response(response_text)
    return apply_executive_output(global_ledger, data, week)
