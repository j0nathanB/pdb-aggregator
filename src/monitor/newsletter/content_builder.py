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
    AtAGlanceCountry,
    AtAGlancePageContent,
    AtAGlanceRegion,
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

        # Raw analysis for editor context — full detail matching old editor input
        if entry.category_movements:
            raw = {}
            for cat, mov in entry.category_movements.items():
                cat_key = cat.value
                raw[cat_key] = {
                    "movement": mov.movement.value,
                    "prior_assessment": mov.prior_assessment,
                    "updated_assessment": mov.updated_assessment,
                    "developments": [
                        {
                            "headline": d.headline,
                            "summary": d.summary,
                            "signal_category_relevance": d.signal_category_relevance,
                            "actors_involved": d.actors_involved,
                        }
                        for d in mov.developments
                    ],
                    "confidence_change": (
                        {
                            "from": mov.confidence_change.from_,
                            "to": mov.confidence_change.to,
                            "reason": mov.confidence_change.reason,
                        }
                        if mov.confidence_change
                        else None
                    ),
                }
            content.raw_analysis = {
                "activity_level": entry.activity_level,
                "category_movements": raw,
            }
            if entry.structural_claim_checks:
                content.raw_analysis["structural_claim_checks"] = [
                    {
                        "claim_ref": s.claim_ref,
                        "status": s.status.value if hasattr(s.status, "value") else str(s.status),
                        "evidence": s.evidence,
                    }
                    for s in entry.structural_claim_checks
                ]

    return content


# =============================================================================
# Regional content building
# =============================================================================

def _extract_regional_lead(report: Optional[RegionalReport]) -> tuple[str, list[str]]:
    """Extract gap paragraphs from a regional report.

    Returns (lead_prose, gap_paragraphs). Lead is empty — the regional
    writer produces it later from edited country summaries.
    """
    if not report:
        return "", []

    # Seed the lead with the regional synthesis overview — the editor
    # rewrites it into narrative prose using cross_cutting_dynamics.
    lead = report.regional_overview or ""

    # Extract gaps as separate paragraphs
    gaps = []
    if report and report.gaps:
        for gap in report.gaps:
            gaps.append(
                f"Notably absent this week: {gap.expected_dynamic}. {gap.assessment}"
            )

    return lead, gaps


def _extract_card_summary(report: Optional[RegionalReport]) -> str:
    """Placeholder — the regional writer produces the card summary later."""
    return ""


# =============================================================================
# At-a-glance builder
# =============================================================================

def _top_story(story_map: dict) -> tuple[str, int]:
    """Return (headline, source_count) for the top story in a story map."""
    stories = story_map.get("stories", [])
    if not stories:
        return "", 0
    best = max(stories, key=lambda s: s.get("source_count", 0))
    return best.get("headline", ""), best.get("source_count", 0)


def _build_at_a_glance(
    story_maps: dict[str, dict],
    country_ledgers: dict[str, "CountryLedger"],
    week_start: date,
    week_end: date,
) -> AtAGlancePageContent:
    """Build the at-a-glance page from story maps.

    Deterministic. Picks the top story (by source_count) for each country,
    groups by region in editorial order.
    """
    regions: list[AtAGlanceRegion] = []

    for region in REGION_ORDER:
        region_codes = REGION_COUNTRIES.get(region, [])
        countries: list[AtAGlanceCountry] = []

        for code in region_codes:
            sm = story_maps.get(code)
            if not sm:
                continue
            headline, source_count = _top_story(sm)
            if not headline:
                continue

            # Get country name from ledger, fall back to story map metadata
            ledger = country_ledgers.get(code)
            name = ledger.country if ledger else sm.get("country", code.upper())

            countries.append(AtAGlanceCountry(
                code=code,
                name=name,
                headline=headline,
                source_count=source_count,
            ))

        # Sort by source_count descending within region
        countries.sort(key=lambda c: -c.source_count)

        regions.append(AtAGlanceRegion(
            region=region,
            display_name=REGION_DISPLAY_NAMES.get(region, region.value),
            slug=REGION_SLUGS.get(region, region.value),
            countries=countries,
        ))

    return AtAGlancePageContent(
        week_start=week_start,
        week_end=week_end,
        regions=regions,
    )


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
) -> tuple[OverviewPageContent, dict[Region, RegionPageContent], WatchlistPageContent, AtAGlancePageContent]:
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

        # Build raw dynamics for editor context
        raw_dynamics = None
        if report and report.cross_cutting_dynamics:
            raw_dynamics = []
            for d in report.cross_cutting_dynamics:
                raw_dynamics.append({
                    "title": d.title,
                    "countries_involved": d.countries_involved,
                    "signal_categories": d.signal_categories,
                    "assessment": d.assessment,
                    "significance": d.significance,
                    "trend": d.trend,
                    "confidence": d.confidence,
                    "weakest_link": d.weakest_link,
                    "evidence_against_linkage": d.evidence_against_linkage,
                    "competing_interpretation": d.competing_interpretation,
                })

        page = RegionPageContent(
            region=region,
            display_name=display_name,
            week_start=week_start,
            week_end=end_date,
            regional_lead=lead,
            gap_paragraphs=gaps,
            card_summary=card_summary,
            raw_dynamics=raw_dynamics,
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

    # --- At-a-glance page ---
    at_a_glance = _build_at_a_glance(
        story_maps, country_ledgers, week_start, end_date,
    )

    return overview, region_pages, watchlist, at_a_glance
