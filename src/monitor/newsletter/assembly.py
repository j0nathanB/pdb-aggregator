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
        f'### <img src="https://flagcdn.com/{code}.svg" width="32" alt="{country}" '
        f"style={{{{display: 'inline', verticalAlign: 'middle', position: 'relative', "
        f"top: '-2px', marginRight: '8px', border: '1px solid #d1d5db', borderRadius: '2px'}}}} />"
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


def _extract_card_summary(report: Optional["RegionalReport"]) -> str:
    """Extract the first 1-2 sentences of the regional lead for a Card summary.

    Uses the rendered regional lead text (same prose that appears on the page).
    If the first paragraph is one sentence, returns that sentence.
    Otherwise returns the first two sentences.
    """
    if not report:
        return ""

    # Get the rendered lead text (first dynamic's assessment + significance)
    if report.regional_overview:
        text = report.regional_overview
    elif report.cross_cutting_dynamics:
        d = report.cross_cutting_dynamics[0]
        parts = [d.assessment]
        if d.significance:
            parts.append(d.significance)
        text = " ".join(parts)
    else:
        return ""

    # Get the first paragraph
    first_para = text.split("\n\n")[0].strip()

    # Split into sentences (handle Mr./Mrs./Dr./etc. abbreviations)
    import re
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', first_para)

    if len(sentences) <= 1:
        return first_para
    return " ".join(sentences[:2])


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

                    summary = dev.summary or dev.headline
                    developments.append({
                        "movement": mov.movement,
                        "confidence": conf or 3,
                        "text": f"- **{cat_display}:** {summary}",
                    })

    movement_order = {Movement.SIGNIFICANT: 0, Movement.MINOR: 1}
    developments.sort(key=lambda d: (movement_order.get(d["movement"], 2), -d["confidence"]))
    return developments[:5]


def _format_date_range_display(dates: list[str]) -> str:
    """Format a list of ISO date strings into a readable range.

    e.g. ["2026-01-18", "2026-01-20", "2026-01-18"] -> "January 18-20, 2026"
    """
    parsed = []
    for d in dates:
        if d:
            try:
                parsed.append(date.fromisoformat(d))
            except ValueError:
                continue
    if not parsed:
        return ""
    parsed.sort()
    earliest = min(parsed)
    latest = max(parsed)
    if earliest == latest:
        return earliest.strftime("%B %d, %Y")
    if earliest.month == latest.month and earliest.year == latest.year:
        return f"{earliest.strftime('%B %d')}-{latest.day}, {latest.year}"
    if earliest.year == latest.year:
        return f"{earliest.strftime('%B %d')} - {latest.strftime('%B %d')}, {latest.year}"
    return f"{earliest.strftime('%B %d, %Y')} - {latest.strftime('%B %d, %Y')}"


def _render_sources_section(story_map_data: dict) -> str:
    """Render a Notes section with ResponseField headers and Expandable source lists."""
    lines = ['<Accordion title="Notes">']

    for story in story_map_data.get("stories", []):
        articles = story.get("articles", [])
        if not articles:
            continue

        headline = story.get("headline", "Untitled")
        date_range = _format_date_range_display([a.get("date", "") for a in articles])

        lines.append(f'<ResponseField name="{headline}" type="{date_range}">')
        lines.append(f'<Expandable title="Sources ({len(articles)})">')
        for a in articles:
            title = a.get("title", "Untitled")
            source = a.get("source", "")
            url = a.get("url", "")
            if url:
                lines.append(f"- [{title} — {source}]({url})")
            else:
                lines.append(f"- {title} — {source}")
        lines.append("</Expandable>")
        lines.append("</ResponseField>")
        lines.append("")

    # Single-source items
    singles = story_map_data.get("single_source_items", [])
    if singles:
        lines.append('<ResponseField name="Other" type="">')
        lines.append(f'<Expandable title="Sources ({len(singles)})">')
        for item in singles:
            title = item.get("headline", "Untitled")
            source = item.get("source", "")
            url = item.get("url", "")
            if url:
                lines.append(f"- [{title} — {source}]({url})")
            else:
                lines.append(f"- {title} — {source}")
        lines.append("</Expandable>")
        lines.append("</ResponseField>")
        lines.append("")

    lines.append("</Accordion>")
    return "\n".join(lines)


def _render_deep_dive_entry(
    code: str,
    ledger: CountryLedger,
    entry: WeeklyEntry,
    summary_only: bool = False,
    story_map_data: dict | None = None,
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

    # Sources accordion — full article references from story map sidecar
    if story_map_data and story_map_data.get("stories"):
        lines.append(_render_sources_section(story_map_data))
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

        # Build card summary from the regional lead text (first 1-2 sentences
        # of the first paragraph, matching what appears on the region page).
        report = regional_reports.get(region)
        summary = _extract_card_summary(report)
        if not summary:
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
    story_maps: dict[str, dict] | None = None,
) -> str:
    """Render a single region page with full country details."""
    display_name = REGION_DISPLAY_NAMES[region]
    date_range = _format_date_range(end_date)

    sections = [
        _mdx_frontmatter(display_name, f"Week of {date_range}", display_name),
        "## Regional Summary",
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
        sm_data = story_maps.get(code) if story_maps else None
        sections.append("")
        sections.append("---")
        sections.append("")
        sections.append(_render_deep_dive_entry(code, country_ledgers[code], entry, story_map_data=sm_data))

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
    story_maps: dict[str, dict] | None = None,
) -> dict[str, str]:
    """
    Assemble multi-page newsletter output for Mintlify.

    Returns a dict mapping filename (without extension) to MDX content:
        "overview" -> overview page
        "frontline-eastern-europe" -> region page
        "western-europe" -> region page
        ...
        "watchlist" -> watchlist page

    Args:
        story_maps: Optional dict mapping country code to story map sidecar
            data (from ledgers/story_maps/). When provided, a Sources accordion
            is rendered below each country's Other Stories section.
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
            story_maps=story_maps,
        )

    # Watchlist
    pages["watchlist"] = _render_watchlist_page(global_ledger, end_date)

    logger.info(
        "Newsletter multi-page assembly: %d pages, end_date=%s",
        len(pages), end_date.isoformat(),
    )

    return pages
