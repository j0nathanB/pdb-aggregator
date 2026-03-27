"""
Newsletter assembly: deterministic Markdown rendering from structured JSON.

No LLM calls — mechanical formatting only. Converts structured outputs from
the executive agent, regional reports, and country analyses into the publication template.
"""

import logging
from datetime import date, timedelta
from typing import Optional

from ..agents.regional import RegionalReport, REGION_COUNTRIES

logger = logging.getLogger(__name__)
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
    Region.FRONTLINE_EASTERN_EUROPE: "Frontline and Eastern Europe",
    Region.WESTERN_EUROPE: "Western Europe",
    Region.ASIA_PACIFIC: "Asia-Pacific",
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: "Near East and South Asia",
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

# URL-safe slugs for region page filenames
REGION_SLUGS: dict[Region, str] = {
    Region.FRONTLINE_EASTERN_EUROPE: "frontline-eastern-europe",
    Region.WESTERN_EUROPE: "western-europe",
    Region.ASIA_PACIFIC: "asia-pacific",
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: "middle-east-turkey-south-asia",
    Region.AMERICAS: "the-americas",
}

# Activity level sort order (highest activity first)
_ACTIVITY_SORT = {"high": 0, "moderate": 1, "low": 2}


# =============================================================================
# Rendering helpers
# =============================================================================

def _country_heading(code: str, country: str) -> str:
    """Render a country heading with an inline flag image."""
    return (
        f'### <img src="https://flagcdn.com/h24/{code}.png" alt="{country}" '
        f"style={{{{display: 'inline', verticalAlign: 'middle', marginRight: '8px'}}}} />"
        f"{country}"
    )


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

    if not report:
        return (
            f"No significant cross-country dynamics emerged in {display_name} this week. "
            "Country-level developments are covered below."
        )

    # Use regional overview if available (always produced by the regional agent)
    if not report.cross_cutting_dynamics:
        if report.regional_overview:
            return report.regional_overview
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


def _collect_developments(entry: WeeklyEntry) -> list[dict]:
    """Collect and sort developments from a weekly entry's category movements."""
    developments = []
    if entry.category_movements:
        for cat, mov in entry.category_movements.items():
            if mov.movement in (Movement.SIGNIFICANT, Movement.MINOR) and mov.developments:
                cat_display = SIGNAL_CATEGORY_DISPLAY.get(cat, cat.value)
                for dev in mov.developments:
                    conf = None
                    if mov.confidence_change:
                        conf = mov.confidence_change.to
                    preliminary = conf is not None and conf <= 2

                    # Build source attribution from up to 3 sources
                    if dev.sources:
                        source_parts = []
                        for s in dev.sources[:3]:
                            if s.url:
                                source_parts.append(f"[{s.name}]({s.url})")
                            else:
                                source_parts.append(s.name)
                        source_attr = "; ".join(source_parts)
                    else:
                        source_attr = "unknown"
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

    movement_order = {Movement.SIGNIFICANT: 0, Movement.MINOR: 1}
    developments.sort(key=lambda d: (movement_order.get(d["movement"], 2), -d["confidence"]))
    return developments[:5]


def _render_deep_dive_entry(
    code: str,
    ledger: CountryLedger,
    entry: WeeklyEntry,
    summary_only: bool = False,
) -> str:
    """Render a deep-dive country entry.

    If summary_only=True, renders just the posture summary (for the overview page).
    If summary_only=False, renders full details with key developments and caveats.
    """
    lines = [_country_heading(ledger.code, ledger.country), ""]

    # Posture summary
    lines.append(ledger.posture_summary.text)
    lines.append("")

    if summary_only:
        return "\n".join(lines)

    # Full rendering: developments, unexpected, absences, caveat lector
    developments = _collect_developments(entry)

    if developments:
        lines.append("**Key developments:**")
        lines.append("")
        for d in developments:
            lines.append(d["text"])
    else:
        lines.append("Full analysis conducted; no significant posture changes identified despite initial indicators.")

    # Unexpected developments (skip placeholder/empty entries)
    if entry.unexpected_developments:
        for ud in entry.unexpected_developments:
            if not ud.headline or ud.headline.lower() in ("unknown", ""):
                continue
            assessment = f" {ud.assessment}" if ud.assessment else ""
            lines.append(f"- **Unexpected:** {ud.headline}.{assessment}")

    # Absence checks
    for absence in entry.absence_check:
        if absence.significance and not absence.occurred:
            lines.append(f"- **Notable absence:** {absence.expected} — {absence.significance}")

    lines.append("")

    # Other Stories accordion — story map clusters not in key developments
    if entry.story_clusters:
        # Collect source URLs already shown in key developments
        dev_urls = set()
        if entry.category_movements:
            for mov in entry.category_movements.values():
                for dev in mov.developments:
                    if dev.source_url:
                        dev_urls.add(dev.source_url)

        other_stories = []
        for cluster in entry.story_clusters:
            # Skip if this cluster's representative URL was used in key developments
            if cluster.source_url and cluster.source_url in dev_urls:
                continue
            other_stories.append(cluster)

        if other_stories:
            lines.append("<Accordion title=\"Other Stories\">")
            for cluster in other_stories:
                source_link = (
                    f"[{cluster.source_name}]({cluster.source_url})"
                    if cluster.source_url and cluster.source_name
                    else cluster.source_name or ""
                )
                lines.append(
                    f"- **{cluster.headline}** — {cluster.summary}"
                    + (f" *({source_link})*" if source_link else "")
                )
            lines.append("</Accordion>")
            lines.append("")

    return "\n".join(lines)


def _render_maintenance_entry(
    code: str,
    ledger: CountryLedger,
    entry: Optional[WeeklyEntry],
) -> str:
    """Render a maintenance country entry."""
    lines = [_country_heading(ledger.code, ledger.country), ""]
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
    logger.info(
        "Newsletter assembly: %d deep dives, %d maintenance, %d regional reports, end_date=%s",
        deep_dive_count, maintenance_count, len(regional_reports), end_date.isoformat(),
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


# =============================================================================
# Multi-page assembly (Mintlify site output)
# =============================================================================

def _mdx_frontmatter(title: str, description: str, sidebar_title: str, **extra: str) -> str:
    """Generate YAML frontmatter for an MDX page."""
    lines = [
        "---",
        f'title: "{title}"',
        f'description: "{description}"',
        f'sidebarTitle: "{sidebar_title}"',
    ]
    for key, value in extra.items():
        lines.append(f'{key}: "{value}"')
    lines.append("---")
    return "\n".join(lines) + "\n"


REGION_ICONS: dict[Region, str] = {
    Region.FRONTLINE_EASTERN_EUROPE: "shield",
    Region.WESTERN_EUROPE: "landmark",
    Region.ASIA_PACIFIC: "ship",
    Region.MIDDLE_EAST_TURKEY_SOUTH_ASIA: "compass",
    Region.AMERICAS: "scroll-text",
}


def _render_overview_page(
    global_ledger: GlobalLedger,
    regional_reports: dict[Region, RegionalReport],
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, Optional[WeeklyEntry]],
    end_date: date,
    brief_path: str,
) -> str:
    """Render the overview page: header, executive brief, region Cards."""
    deep_dive_count = sum(
        1 for e in country_entries.values()
        if e is not None and e.depth == Depth.DEEP_DIVE
    )
    maintenance_count = sum(
        1 for e in country_entries.values()
        if e is not None and e.depth == Depth.MAINTENANCE
    )

    week_start = end_date - timedelta(days=6)
    title = f"Week of {week_start.strftime('%B %d')}, {end_date.year}"

    sections = [
        _mdx_frontmatter(
            "The Middle Powers Monitor",
            "Weekly intelligence brief covering 28 middle powers across five regions",
            "Overview",
            mode="wide",
        ),
        "",
        f"## {title}",
        "",
    ]

    # Executive Brief
    latest = global_ledger.latest_entry()
    briefing_items = latest.executive_briefing_items if latest else []
    sections.append("")
    sections.append(_render_executive_brief(briefing_items))

    # Region Cards
    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append("## Regions")
    sections.append("")
    sections.append('<Columns cols={2}>')

    for region in REGION_ORDER:
        display_name = REGION_DISPLAY_NAMES[region]
        slug = REGION_SLUGS[region]
        icon = REGION_ICONS[region]

        # Build a one-line summary from the regional overview or deep-dive countries
        report = regional_reports.get(region)
        if report and report.regional_overview:
            summary = report.regional_overview
            # Truncate to ~120 chars for card body
            if len(summary) > 120:
                summary = summary[:117].rsplit(" ", 1)[0] + "..."
        elif report and report.cross_cutting_dynamics:
            summary = report.cross_cutting_dynamics[0].assessment
            if len(summary) > 120:
                summary = summary[:117].rsplit(" ", 1)[0] + "..."
        else:
            # Summarize from deep-dive country names if available
            region_codes = REGION_COUNTRIES.get(region, [])
            deep_dive_names = []
            for code in region_codes:
                entry = country_entries.get(code)
                if entry is not None and entry.depth == Depth.DEEP_DIVE and code in country_ledgers:
                    deep_dive_names.append(country_ledgers[code].country)
            if deep_dive_names:
                summary = f"{', '.join(deep_dive_names)} received full analytical treatment this week."
            else:
                summary = "Country-level developments are covered in the regional page."

        sections.append(f'  <Card title="{display_name}" icon="{icon}" href="{brief_path}/{slug}">')
        sections.append(f"    {summary}")
        sections.append("  </Card>")

    # Watchlist card
    watchlist = global_ledger.watchlist
    watchlist_count = len(watchlist)
    if watchlist_count:
        watchlist_summary = f"{watchlist_count} item{'s' if watchlist_count != 1 else ''}: {watchlist[0].item[:80]}."
    else:
        watchlist_summary = "No items this week."
    sections.append(f'  <Card title="Watchlist" icon="binoculars" href="{brief_path}/watchlist">')
    sections.append(f"    {watchlist_summary}")
    sections.append("  </Card>")

    sections.append("</Columns>")
    sections.append("")
    return "\n".join(sections)


def _render_region_page(
    region: Region,
    regional_reports: dict[Region, RegionalReport],
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, Optional[WeeklyEntry]],
    end_date: date,
) -> str:
    """Render a single region page with full country details."""
    display_name = REGION_DISPLAY_NAMES[region]
    date_range = _format_date_range(end_date)

    sections = [
        _mdx_frontmatter(display_name, f"Week of {date_range}", display_name),
        "",
    ]

    # Regional lead
    report = regional_reports.get(region)
    sections.append(_render_regional_lead(region, report))

    # Full country entries
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

    deep_dives.sort(key=lambda c: _activity_sort_key(country_entries.get(c)))
    maintenances.sort(key=lambda c: country_ledgers[c].country)

    for code in deep_dives:
        entry = country_entries[code]
        sections.append("")
        sections.append("---")
        sections.append("")
        sections.append(_render_deep_dive_entry(code, country_ledgers[code], entry))

    for code in maintenances:
        entry = country_entries.get(code)
        sections.append("")
        sections.append("---")
        sections.append("")
        sections.append(_render_maintenance_entry(code, country_ledgers[code], entry))

    return "\n".join(sections)


def _render_watchlist_page(
    global_ledger: GlobalLedger,
    end_date: date,
) -> str:
    """Render the watchlist as its own page."""
    date_range = _format_date_range(end_date)

    sections = [
        _mdx_frontmatter("Watchlist", f"Week of {date_range}", "Watchlist"),
        "",
        "*Items worth monitoring that didn't make the executive briefing.*",
        "",
    ]

    watchlist = global_ledger.watchlist
    if watchlist:
        sorted_items = sorted(watchlist, key=lambda w: w.added_week, reverse=True)[:10]
        for item in sorted_items:
            countries = ", ".join(c.upper() for c in item.countries) if item.countries else ""
            country_part = f" ({countries})" if countries else ""
            trigger_part = f" *Trigger: {item.trigger}.*" if item.trigger else ""
            sections.append(
                f"- **{item.item}**{country_part}: "
                f"{item.why_it_matters}{trigger_part}"
            )
    else:
        sections.append("*No items on the watchlist this week.*")

    sections.append("")
    sections.append("---")
    sections.append("")
    sections.append(
        "*The Middle Powers Monitor tracks 28 countries across five regions, "
        "analyzing state positioning through five analytical dimensions: "
        "diplomatic alignment, security posture, economic statecraft, "
        "institutional engagement, and domestic constraints. Published weekly.*"
    )
    sections.append("")
    sections.append(f"*This edition: {end_date.isoformat()}*")

    return "\n".join(sections)


def assemble_newsletter_pages(
    global_ledger: GlobalLedger,
    regional_reports: dict[Region, RegionalReport],
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, Optional[WeeklyEntry]],
    end_date: date,
) -> dict[str, str]:
    """
    Assemble multi-page newsletter output for Mintlify.

    Returns a dict mapping filename (without extension) to MDX content:
        "overview" -> overview page
        "frontline-eastern-europe" -> region page
        "western-europe" -> region page
        ...
        "watchlist" -> watchlist page
    """
    brief_path = f"/briefs/{end_date.isoformat()}"

    pages = {}

    # Overview
    pages["overview"] = _render_overview_page(
        global_ledger, regional_reports, country_ledgers,
        country_entries, end_date, brief_path,
    )

    # Region pages
    for region in REGION_ORDER:
        slug = REGION_SLUGS[region]
        pages[slug] = _render_region_page(
            region, regional_reports, country_ledgers,
            country_entries, end_date,
        )

    # Watchlist
    pages["watchlist"] = _render_watchlist_page(global_ledger, end_date)

    logger.info(
        "Newsletter multi-page assembly: %d pages, end_date=%s",
        len(pages), end_date.isoformat(),
    )

    return pages
