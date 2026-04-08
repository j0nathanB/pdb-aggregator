"""
Executive agent: global-level synthesis from regional reports.

Input: 5 regional reports + global ledger (prior state).
Output: Updated global ledger (dynamics, watchlist, briefing items, triage implications).
"""

import logging
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
    load_prompt,
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
from ..sanitize import extract_json, safe_date, safe_enum, safe_enum_list

logger = logging.getLogger(__name__)


# =============================================================================
# System prompt
# =============================================================================

EXECUTIVE_SYSTEM_PROMPT = load_prompt("executive")


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
    data = extract_json(response_text, context="executive_response")

    # Unwrap if using the new spec format
    if "global_ledger_update" in data:
        data = data["global_ledger_update"]

    return data


def _safe_linkage_type(value: str) -> LinkageType:
    """Parse a LinkageType, falling back to PARALLEL_BEHAVIOR for invalid values."""
    return safe_enum(LinkageType, value, LinkageType.PARALLEL_BEHAVIOR, context="executive")


def _parse_active_dynamic(d: dict, week: date) -> ActiveDynamic:
    """Parse a single active dynamic from JSON."""
    es = d.get("evidence_strength", {})
    ti = d.get("triage_implications", {})

    created_week = safe_date(d.get("created_week"), week, context="dynamic.created_week")
    last_updated = safe_date(d.get("last_updated"), week, context="dynamic.last_updated")

    return ActiveDynamic(
        dynamic_id=d["dynamic_id"],
        title=d["title"],
        created_week=created_week,
        last_updated=last_updated,
        status=safe_enum(DynamicStatus, d.get("status", "emerging"), DynamicStatus.EMERGING, context="active_dynamic"),
        current_assessment=d["current_assessment"],
        countries_involved=d.get("countries_involved", []),
        signal_categories_touched=safe_enum_list(SignalCategory, d.get("signal_categories_touched", []), context="active_dynamic"),
        evidence_strength=EvidenceStrength(
            confidence=es.get("confidence", 3),
            supporting_country_confidences=es.get("supporting_country_confidences", {}),
            weakest_link=es.get("weakest_link", ""),
            linkage_type=_safe_linkage_type(es.get("linkage_type", "parallel_behavior")),
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
    added_week = safe_date(w.get("added_week"), week, context="watchlist_item.added_week")

    return WatchlistItem(
        item=w["item"],
        signal_category=safe_enum(SignalCategory, w.get("signal_category", "alignment_diplomatic"), SignalCategory.ALIGNMENT_DIPLOMATIC, context="watchlist_item"),
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
    as_of = safe_date(gps.get("as_of"), week, context="global_posture_summary.as_of")

    se = gps.get("signal_environment", {})
    global_ledger.global_posture_summary = GlobalPostureSummary(
        as_of=as_of,
        text=gps["text"],
        signal_environment=SignalEnvironment(
            most_active_categories=safe_enum_list(SignalCategory, se.get("most_active_categories", []), context="signal_environment"),
            quietest_categories=safe_enum_list(SignalCategory, se.get("quietest_categories", []), context="signal_environment"),
            geographic_hotspots=se.get("geographic_hotspots", []),
            geographic_quiet_zones=se.get("geographic_quiet_zones", []),
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
            status=safe_enum(DynamicStatus, d.get("status", "emerging"), DynamicStatus.EMERGING, context="delta_create"),
            current_assessment=d["current_assessment"],
            countries_involved=d.get("countries_involved", []),
            signal_categories_touched=safe_enum_list(SignalCategory, d.get("signal_categories_touched", []), context="delta_create"),
            evidence_strength=EvidenceStrength(
                confidence=es.get("confidence", 3),
                supporting_country_confidences=es.get("supporting_country_confidences", {}),
                weakest_link=es.get("weakest_link", ""),
                linkage_type=_safe_linkage_type(es.get("linkage_type", "parallel_behavior")),
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
                dynamic.status = safe_enum(DynamicStatus, u["status"], dynamic.status, context="delta_update")
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
                        linkage_type=_safe_linkage_type(es.get("linkage_type", dynamic.evidence_strength.linkage_type.value)),
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
            signal_category=safe_enum(SignalCategory, w.get("signal_category", "alignment_diplomatic"), SignalCategory.ALIGNMENT_DIPLOMATIC, context="watchlist_add"),
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

    rejected = []
    for r in we_data.get("items_considered_rejected",
                         [{"candidate": "None", "reason_rejected": "N/A"}]):
        rejected.append(RejectedItem(
            candidate=r.get("candidate", "Unknown"),
            reason_rejected=r.get("reason_rejected", r.get("reason", "N/A")),
        ))

    corrections = []
    for s in we_data.get("self_corrections", []):
        try:
            corrections.append(GlobalSelfCorrection(
                dynamic_id=s.get("dynamic_id", "unknown"),
                prior_assessment=s.get("prior_assessment", ""),
                correction=s.get("correction", ""),
                root_cause=s.get("root_cause", ""),
            ))
        except Exception as e:
            logger.warning("Skipping malformed self-correction: %s", e)

    weekly_entry = GlobalWeeklyEntry(
        week=week,
        executive_briefing_items=briefing_items,
        dynamics_created=we_data.get("dynamics_created", []),
        dynamics_updated=we_data.get("dynamics_updated", []),
        dynamics_archived=we_data.get("dynamics_archived", []),
        items_considered_rejected=rejected,
        self_corrections=corrections,
    )
    existing_idx = next(
        (i for i, e in enumerate(global_ledger.weekly_entries) if e.week == week),
        None,
    )
    if existing_idx is not None:
        logger.warning("Replacing existing global weekly entry for %s", week)
        global_ledger.weekly_entries[existing_idx] = weekly_entry
    else:
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

    logger.info(
        "Executive synthesis: %d regional reports, %d active dynamics in ledger",
        len(regional_reports), len(global_ledger.active_dynamics),
    )
    logger.debug("Executive: prompt=%d chars", len(prompt))

    from ..timing import with_heartbeat
    from ..rate_limit import anthropic_limiter
    async with anthropic_limiter():
        response = await with_heartbeat(
            client.messages.create(
                model=MODEL,
                max_tokens=THINKING_BUDGET_TOKENS + 12288,
                temperature=1,
                thinking={
                    "type": "enabled",
                    "budget_tokens": THINKING_BUDGET_TOKENS,
                },
                system=[{"type": "text", "text": load_prompt("executive")}],
                messages=[{"role": "user", "content": prompt}],
                timeout=600.0,
            ),
            "Executive synthesis: API call",
        )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    response_text = "\n".join(text_parts)

    logger.info(
        "Executive synthesis: API complete — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    save_raw_response(
        "executive", "global", week,
        system_prompt=load_prompt("executive"),
        user_message=prompt,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    data = parse_executive_response(response_text)
    logger.info(
        "Executive: %d briefing items, %d dynamics created, %d updated, %d archived",
        len(data.get("weekly_entry", {}).get("executive_briefing_items", [])),
        len(data.get("weekly_entry", {}).get("dynamics_created", [])),
        len(data.get("weekly_entry", {}).get("dynamics_updated", [])),
        len(data.get("weekly_entry", {}).get("dynamics_archived", [])),
    )
    update_trace_parsed("executive", "global", week, parsed_output=data)

    return apply_executive_output(global_ledger, data, week)
