"""
Newsletter assembly: deterministic Markdown rendering from structured JSON.

No LLM calls — mechanical formatting only. Converts structured outputs from
the executive agent, regional reports, and country analyses into the publication template.
"""

from datetime import date, timedelta
from typing import Optional

from ..agents.regional import RegionalReport, REGION_COUNTRIES
from ..config import Depth, Movement, Region, SignalCategory
from ..models import (
    CountryLedger,
    ExecutiveBriefingItem,
    GlobalLedger,
    WatchlistItem,
    WeeklyEntry,
)


# =============================================================================
# Constants
# =============================================================================

REGION_DISPLAY_NAMES: dict[Region, str] = {
    Region.FRONTLINE_EASTERN_EUROPE: "Frontline & Eastern Europe",
    Region.WESTERN_EUROPE: "Western Europe",
    Region.ASIA_PACIFIC: "Asia-Pacific",
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: "Middle East, Turkey & South Asia",
    Region.AMERICAS: "The Americas",
}

# Fixed editorial order per spec: highest-stakes first
REGION_ORDER = [
    Region.FRONTLINE_EASTERN_EUROPE,
    Region.WESTERN_EUROPE,
    Region.ASIA_PACIFIC,
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA,
    Region.AMERICAS,
]

SIGNAL_CATEGORY_DISPLAY: dict[SignalCategory, str] = {
    SignalCategory.ALIGNMENT_DIPLOMATIC: "Diplomatic",
    SignalCategory.SECURITY_DEFENSE: "Security",
    SignalCategory.ECONOMIC_TECH: "Economic",
    SignalCategory.INSTITUTIONAL: "Institutional",
    SignalCategory.DOMESTIC_REGIME: "Domestic",
}

CONFIDENCE_LABELS: dict[int, str] = {
    5: "High confidence",
    4: "Moderate-high confidence",
    3: "Moderate confidence",
    2: "Low confidence",
    1: "Very low confidence",
}

# Activity level sort order (highest activity first)
_ACTIVITY_SORT = {"high": 0, "moderate": 1, "low": 2}


# =============================================================================
# Rendering helpers
# =============================================================================

def _format_date_range(end_date: date) -> str:
    start = end_date - timedelta(days=6)
    return f"{start.strftime('%B %d')} to {end_date.strftime('%B %d, %Y')}"


def _render_header(
    end_date: date,
    deep_dive_count: int,
    maintenance_count: int,
) -> str:
    date_range = _format_date_range(end_date)
    lines = [
        "# The Middle Powers Monitor",
        f"## Week of {date_range}",
        "",
        f"*Covering 28 countries across five regions. "
        f"{deep_dive_count} countries received full analytical treatment this week; "
        f"{maintenance_count} were held at maintenance.*",
    ]
    return "\n".join(lines)


def _render_executive_brief(
    briefing_items: list[ExecutiveBriefingItem],
) -> str:
    """Render the executive brief section from structured briefing items."""
    if not briefing_items:
        return (
            "*No system-level dynamics met the threshold for executive-level analysis "
            "this week. See regional sections for country-level developments.*"
        )

    # Sort by confidence descending
    sorted_items = sorted(briefing_items, key=lambda x: x.confidence, reverse=True)

    paragraphs = []
    for item in sorted_items:
        conf_label = CONFIDENCE_LABELS.get(item.confidence, "Moderate confidence")
        lines = [f"### {item.title}", ""]
        lines.append(item.what)
        lines.append("")
        lines.append(item.why_it_matters)
        lines.append("")
        conf_note = f"*{conf_label}. {item.confidence_note}*" if item.confidence_note else f"*{conf_label}.*"
        lines.append(conf_note)
        lines.append("")
        if item.what_to_watch:
            lines.append(f"*What to watch: {item.what_to_watch}*")
        paragraphs.append("\n".join(lines))

    return "\n\n".join(paragraphs)


def _render_regional_lead(
    region: Region,
    report: Optional[RegionalReport],
) -> str:
    """Render the regional lead paragraph from cross-cutting dynamics."""
    display_name = REGION_DISPLAY_NAMES.get(region, region.value)

    if not report or not report.cross_cutting_dynamics:
        return (
            f"No significant cross-country dynamics emerged in {display_name} this week. "
            "Country-level developments are covered below."
        )

    paragraphs = []
    for dynamic in report.cross_cutting_dynamics:
        parts = [f"{dynamic.assessment}"]
        if dynamic.significance:
            parts.append(dynamic.significance)

        # Only show confidence/linkage parenthetically if confidence <= 3 or weak/speculative
        show_meta = (
            dynamic.confidence <= 3
            or dynamic.linkage_strength in ("weak", "speculative")
        )
        if show_meta:
            parts.append(
                f"({CONFIDENCE_LABELS.get(dynamic.confidence, 'Moderate confidence').lower()}; "
                f"linkage: {dynamic.linkage_strength})"
            )

        paragraphs.append(" ".join(parts))

    # Append gaps as "Notably absent" paragraphs
    if report.gaps:
        for gap in report.gaps:
            paragraphs.append(
                f"Notably absent this week: {gap.expected_dynamic}. {gap.assessment}"
            )

    return "\n\n".join(paragraphs)


def _render_deep_dive_entry(
    code: str,
    ledger: CountryLedger,
    entry: WeeklyEntry,
) -> str:
    """Render a deep-dive country entry."""
    lines = [f"### {ledger.country}", ""]

    # Posture summary
    lines.append(ledger.posture_summary.text)
    lines.append("")

    # Collect developments from category movements
    developments = []
    if entry.category_movements:
        for cat, mov in entry.category_movements.items():
            if mov.movement in (Movement.SIGNIFICANT, Movement.MINOR) and mov.developments:
                cat_display = SIGNAL_CATEGORY_DISPLAY.get(cat, cat.value)
                for dev in mov.developments:
                    # Determine confidence for preliminary tag
                    conf = None
                    if mov.confidence_change:
                        conf = mov.confidence_change.to
                    preliminary = conf is not None and conf <= 2

                    source_attr = f"{dev.source}"
                    if dev.date:
                        source_attr += f", {dev.date.isoformat()}"
                    if preliminary:
                        source_attr += " *(preliminary)*"

                    summary = dev.summary or dev.headline
                    developments.append({
                        "movement": mov.movement,
                        "confidence": conf or 3,
                        "text": f"- **{cat_display}:** {summary} *({source_attr})*",
                    })

    # Sort: significant first, then minor; within same level by confidence desc
    movement_order = {Movement.SIGNIFICANT: 0, Movement.MINOR: 1}
    developments.sort(key=lambda d: (movement_order.get(d["movement"], 2), -d["confidence"]))

    # Cap at 5 developments
    developments = developments[:5]

    if developments:
        lines.append("**Key developments:**")
        lines.append("")
        for d in developments:
            lines.append(d["text"])
    else:
        lines.append("Full analysis conducted; no significant posture changes identified despite initial indicators.")

    # Unexpected developments
    if entry.unexpected_developments:
        for ud in entry.unexpected_developments:
            assessment = f" {ud.assessment}" if ud.assessment else ""
            lines.append(f"- **Unexpected:** {ud.headline}.{assessment}")

    # Absence checks
    for absence in entry.absence_check:
        if absence.significance and not absence.occurred:
            lines.append(f"- **Notable absence:** {absence.expected} — {absence.significance}")

    lines.append("")

    # Between the Lines (blockquote)
    if entry.devils_advocate and entry.devils_advocate.challenges:
        top_challenge = entry.devils_advocate.challenges[0]
        lines.append(f"> **Between the Lines:** {top_challenge}")
        lines.append("")

    return "\n".join(lines)


def _render_maintenance_entry(
    code: str,
    ledger: CountryLedger,
    entry: Optional[WeeklyEntry],
) -> str:
    """Render a maintenance country entry."""
    lines = [f"### {ledger.country}", ""]
    lines.append(f"{ledger.posture_summary.text} No significant developments this week.")
    lines.append("")
    return "\n".join(lines)


def _render_watchlist(watchlist: list[WatchlistItem]) -> str:
    """Render the watchlist section. Returns empty string if no items."""
    if not watchlist:
        return ""

    # Sort by added_week descending, cap at 10
    sorted_items = sorted(watchlist, key=lambda w: w.added_week, reverse=True)[:10]

    lines = [
        "---",
        "",
        "## Watchlist",
        "",
        "*Items worth monitoring that didn't make the executive briefing.*",
        "",
    ]

    for item in sorted_items:
        countries = ", ".join(c.upper() for c in item.countries) if item.countries else ""
        country_part = f" ({countries})" if countries else ""
        trigger_part = f" *Trigger: {item.trigger}.*" if item.trigger else ""
        lines.append(
            f"- **{item.item}**{country_part}: "
            f"{item.why_it_matters}{trigger_part}"
        )

    lines.append("")
    return "\n".join(lines)


def _render_footer(end_date: date) -> str:
    return (
        "---\n\n"
        "*The Middle Powers Monitor tracks 28 countries across five regions, "
        "analyzing state positioning through five analytical dimensions: "
        "diplomatic alignment, security posture, economic statecraft, "
        "institutional engagement, and domestic constraints. Published weekly.*\n\n"
        f"*This edition: {end_date.isoformat()}*"
    )


def _activity_sort_key(entry: Optional[WeeklyEntry]) -> int:
    """Sort key for country entries by activity level (high first)."""
    if entry is None or entry.activity_level is None:
        return 99
    rating = entry.activity_level.get("rating", "low")
    return _ACTIVITY_SORT.get(rating, 2)


# =============================================================================
# Main assembly
# =============================================================================

def assemble_newsletter(
    global_ledger: GlobalLedger,
    regional_reports: dict[Region, RegionalReport],
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, Optional[WeeklyEntry]],
    end_date: date,
) -> str:
    """
    Assemble the full newsletter from structured outputs.

    This is a purely deterministic operation — no LLM calls.

    Args:
        global_ledger: Updated global ledger (after executive agent).
        regional_reports: Regional synthesis reports keyed by Region.
        country_ledgers: Country ledgers keyed by code (after updates).
        country_entries: This week's entries keyed by code.
        end_date: End of the analysis week.
    """
    sections = []

    # Count deep-dive vs maintenance from entries
    deep_dive_count = sum(
        1 for e in country_entries.values()
        if e is not None and e.depth == Depth.DEEP_DIVE
    )
    maintenance_count = sum(
        1 for e in country_entries.values()
        if e is not None and e.depth == Depth.MAINTENANCE
    )

    # Header
    sections.append(_render_header(end_date, deep_dive_count, maintenance_count))

    # Executive Brief
    latest = global_ledger.latest_entry()
    briefing_items = latest.executive_briefing_items if latest else []
    sections.append(_render_executive_brief(briefing_items))

    # Regional sections
    for region in REGION_ORDER:
        display_name = REGION_DISPLAY_NAMES[region]
        sections.append(f"---\n\n## {display_name}")

        # Regional lead
        report = regional_reports.get(region)
        sections.append(_render_regional_lead(region, report))

        # Partition countries into deep-dive and maintenance
        region_codes = REGION_COUNTRIES.get(region, [])
        deep_dives = []
        maintenances = []
        for code in region_codes:
            if code not in country_ledgers:
                continue
            entry = country_entries.get(code)
            if entry is not None and entry.depth == Depth.DEEP_DIVE:
                deep_dives.append(code)
            else:
                maintenances.append(code)

        # Sort deep-dives by activity level (high → moderate → low)
        deep_dives.sort(key=lambda c: _activity_sort_key(country_entries.get(c)))
        # Maintenance entries in alphabetical order
        maintenances.sort(key=lambda c: country_ledgers[c].country)

        # Render deep-dive entries first
        for code in deep_dives:
            entry = country_entries[code]
            sections.append(_render_deep_dive_entry(code, country_ledgers[code], entry))

        # Then maintenance entries
        for code in maintenances:
            entry = country_entries.get(code)
            sections.append(_render_maintenance_entry(code, country_ledgers[code], entry))

    # Watchlist (omit if empty)
    watchlist_section = _render_watchlist(global_ledger.watchlist)
    if watchlist_section:
        sections.append(watchlist_section)

    # Footer
    sections.append(_render_footer(end_date))

    return "\n\n".join(sections)
