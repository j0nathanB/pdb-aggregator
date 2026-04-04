"""
Content builder: maps ledgers/reports → structured content models.

Deterministic, no LLM calls. Replaces the data-gathering logic in assembly.py.
Output is structured dataclasses, not markdown strings.
"""

import logging
import re
from datetime import date, timedelta
from typing import Optional

from ..agents.regional import RegionalReport, REGION_COUNTRIES
from ..config import Depth, Movement, Region, SignalCategory
from ..models import (
    CountryLedger,
    GlobalLedger,
    WeeklyEntry,
)
from .assembly import (
    CONFIDENCE_LABELS,
    REGION_DISPLAY_NAMES,
    REGION_ICONS,
    REGION_ORDER,
    REGION_SLUGS,
    SIGNAL_CATEGORY_DISPLAY,
)
from .content_models import (
    AbsenceContent,
    BriefingItemInput,
    CountryContent,
    DevelopmentContent,
    ExecutiveBriefContent,
    OverviewPageContent,
    RegionCardContent,
    RegionPageContent,
    SourceRef,
    StoryClusterContent,
    UnexpectedContent,
    WatchlistItemContent,
    WatchlistPageContent,
)

logger = logging.getLogger(__name__)

# Activity level sort order
_ACTIVITY_SORT = {"high": 0, "moderate": 1, "low": 2}


# =============================================================================
# Development collection (enhanced — always populates all categories)
# =============================================================================

def _collect_developments(
    entry: WeeklyEntry,
    ledger: CountryLedger,
) -> list[DevelopmentContent]:
    """Collect developments from all signal categories.

    Unlike assembly.py's version which skips Movement.NONE, this always
    includes at least one item per category. For NONE, it uses the
    category's current assessment from the ledger.
    """
    developments = []

    if not entry.category_movements:
        return developments

    for cat in SignalCategory:
        mov = entry.category_movements.get(cat)
        cat_display = SIGNAL_CATEGORY_DISPLAY.get(cat, cat.value)

        if mov and mov.movement in (Movement.SIGNIFICANT, Movement.MINOR) and mov.developments:
            # Active movement — include developments
            for dev in mov.developments:
                sources = [
                    SourceRef(name=s.name, url=s.url, tier=s.tier)
                    for s in (dev.sources or [])
                ]
                developments.append(DevelopmentContent(
                    category=cat,
                    category_display=cat_display,
                    movement=mov.movement,
                    text=dev.summary or dev.headline,
                    sources=sources,
                ))
        else:
            # No movement or NONE — include current assessment
            assessment = ""
            if mov and mov.updated_assessment:
                assessment = mov.updated_assessment
            elif cat in ledger.signal_categories:
                assessment = ledger.signal_categories[cat].current_assessment
            if assessment:
                developments.append(DevelopmentContent(
                    category=cat,
                    category_display=cat_display,
                    movement=Movement.NONE,
                    text=assessment,
                ))

    # Sort: significant first, then minor, then none — by confidence descending
    movement_order = {Movement.SIGNIFICANT: 0, Movement.MINOR: 1, Movement.NONE: 2}
    developments.sort(key=lambda d: movement_order.get(d.movement, 3))

    return developments


def _collect_other_stories(
    entry: WeeklyEntry,
) -> list[StoryClusterContent]:
    """Collect story clusters not already shown in key developments."""
    if not entry.story_clusters:
        return []

    # URLs used in key developments
    dev_urls = set()
    if entry.category_movements:
        for mov in entry.category_movements.values():
            for dev in mov.developments:
                if dev.source_url:
                    dev_urls.add(dev.source_url)

    stories = []
    for cluster in entry.story_clusters:
        if cluster.source_url and cluster.source_url in dev_urls:
            continue
        stories.append(StoryClusterContent(
            headline=cluster.headline,
            summary=cluster.summary,
            source_name=cluster.source_name or "",
            source_url=cluster.source_url or "",
        ))

    return stories


# =============================================================================
# Country content building
# =============================================================================

def _build_country_content(
    code: str,
    ledger: CountryLedger,
    entry: Optional[WeeklyEntry],
    story_map_data: Optional[dict] = None,
) -> CountryContent:
    """Build structured content for a single country."""
    activity_rating = None
    if entry and entry.activity_level:
        activity_rating = entry.activity_level.get("rating")

    content = CountryContent(
        code=code,
        country=ledger.country,
        activity_rating=activity_rating,
        posture_summary=ledger.posture_summary.text,
        story_map_data=story_map_data,
    )

    if entry and entry.depth == Depth.DEEP_DIVE:
        content.developments = _collect_developments(entry, ledger)
        content.other_stories = _collect_other_stories(entry)

        # Unexpected developments
        for ud in (entry.unexpected_developments or []):
            if ud.headline and ud.headline.lower() not in ("unknown", ""):
                content.unexpected.append(UnexpectedContent(
                    headline=ud.headline,
                    assessment=ud.assessment or "",
                ))

        # Absence checks
        for absence in (entry.absence_check or []):
            if absence.significance and not absence.occurred:
                content.absences.append(AbsenceContent(
                    expected=absence.expected,
                    significance=absence.significance,
                ))

        # Raw analysis for editor context
        if entry.category_movements:
            content.raw_analysis = {
                cat.value: {
                    "movement": mov.movement.value,
                    "updated_assessment": mov.updated_assessment,
                    "prior_assessment": mov.prior_assessment,
                }
                for cat, mov in entry.category_movements.items()
            }

    return content


# =============================================================================
# Regional content building
# =============================================================================

def _extract_regional_lead(report: Optional[RegionalReport]) -> tuple[str, list[str]]:
    """Extract regional lead prose and gap paragraphs from a regional report.

    Returns (lead_prose, gap_paragraphs).
    """
    if not report:
        return "", []

    # Use regional overview if available
    if report.regional_overview:
        lead = report.regional_overview
    elif report.cross_cutting_dynamics:
        paragraphs = []
        for dynamic in report.cross_cutting_dynamics:
            parts = [dynamic.assessment]
            if dynamic.significance:
                parts.append(dynamic.significance)
            paragraphs.append(" ".join(parts))
        lead = "\n\n".join(paragraphs)
    else:
        lead = ""

    # Extract gaps as separate paragraphs
    gaps = []
    if report and report.gaps:
        for gap in report.gaps:
            gaps.append(
                f"Notably absent this week: {gap.expected_dynamic}. {gap.assessment}"
            )

    return lead, gaps


def _extract_card_summary(report: Optional[RegionalReport]) -> str:
    """Extract first 1-2 sentences for the region card on the overview page."""
    if not report:
        return ""

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

    first_para = text.split("\n\n")[0].strip()
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', first_para)
    if len(sentences) <= 1:
        return first_para
    return " ".join(sentences[:2])


# =============================================================================
# Main entry point
# =============================================================================

def build_all_pages(
    global_ledger: GlobalLedger,
    regional_reports: dict[Region, RegionalReport],
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, Optional[WeeklyEntry]],
    end_date: date,
    story_maps: Optional[dict[str, dict]] = None,
) -> tuple[OverviewPageContent, dict[Region, RegionPageContent], WatchlistPageContent]:
    """Build structured content for all pages.

    Deterministic, no LLM calls. This is the structured equivalent of
    assemble_newsletter_pages() — same inputs, structured output instead
    of markdown strings.
    """
    story_maps = story_maps or {}
    week_start = end_date - timedelta(days=6)

    # --- Overview page ---
    latest = global_ledger.latest_entry()
    briefing_items = []
    if latest:
        for item in sorted(latest.executive_briefing_items, key=lambda i: -i.confidence):
            briefing_items.append(BriefingItemInput(
                title=item.title,
                regions_involved=item.regions_involved,
                what=item.what,
                why_it_matters=item.why_it_matters,
                what_to_watch=item.what_to_watch,
                confidence=item.confidence,
                confidence_note=item.confidence_note,
            ))

    overview = OverviewPageContent(
        week_start=week_start,
        week_end=end_date,
        country_count=len(country_ledgers),
        executive_brief=ExecutiveBriefContent(items=briefing_items),
    )

    # --- Region pages ---
    region_pages: dict[Region, RegionPageContent] = {}

    for region in REGION_ORDER:
        report = regional_reports.get(region)
        lead, gaps = _extract_regional_lead(report)
        card_summary = _extract_card_summary(report)
        display_name = REGION_DISPLAY_NAMES.get(region, region.value)
        slug = REGION_SLUGS.get(region, region.value)
        icon = REGION_ICONS.get(region, "globe")

        # Build country content for this region
        region_codes = REGION_COUNTRIES.get(region, [])
        countries: list[CountryContent] = []

        for code in region_codes:
            ledger = country_ledgers.get(code)
            if not ledger:
                continue
            entry = country_entries.get(code)
            sm_data = story_maps.get(code)
            countries.append(_build_country_content(code, ledger, entry, sm_data))

        # Sort by activity level (high → moderate → low → none)
        countries.sort(key=lambda c: _ACTIVITY_SORT.get(c.activity_rating or "", 99))

        page = RegionPageContent(
            region=region,
            display_name=display_name,
            week_start=week_start,
            week_end=end_date,
            regional_lead=lead,
            gap_paragraphs=gaps,
            card_summary=card_summary,
            countries=countries,
        )
        region_pages[region] = page

        # Add card to overview
        overview.region_cards.append(RegionCardContent(
            region=region,
            display_name=display_name,
            slug=slug,
            icon=icon,
            summary=card_summary,
        ))

    # --- Watchlist page ---
    watchlist_items = []
    if global_ledger.watchlist:
        sorted_watchlist = sorted(global_ledger.watchlist, key=lambda w: w.added_week, reverse=True)
        for w in sorted_watchlist[:10]:
            watchlist_items.append(WatchlistItemContent(
                item=w.item,
                countries=w.countries,
                why_it_matters=w.why_it_matters,
                trigger=w.trigger,
                added_week=w.added_week,
            ))

    watchlist = WatchlistPageContent(
        week_start=week_start,
        week_end=end_date,
        items=watchlist_items,
    )

    overview.watchlist_count = len(watchlist_items)
    if watchlist_items:
        overview.watchlist_card_summary = (
            f"{len(watchlist_items)} items on watch — "
            f"{watchlist_items[0].item[:80]}..."
            if len(watchlist_items[0].item) > 80
            else f"{len(watchlist_items)} items on watch — {watchlist_items[0].item}"
        )

    return overview, region_pages, watchlist
