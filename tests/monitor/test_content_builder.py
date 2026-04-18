"""Tests for the content builder (structured data gathering)."""

from datetime import date

import pytest
from src.monitor.config import (
    CategoryStatus,
    Depth,
    Movement,
    Region,
    SignalCategory,
)
from src.monitor.agents.regional import CrossCuttingDynamic, RegionalReport, Gap
from src.monitor.models import (
    ActorRef,
    CategoryMovement,
    CountryLedger,
    Development,
    ExecutiveBriefingItem,
    GlobalLedger,
    GlobalPostureSummary,
    GlobalWeeklyEntry,
    PostureSummary,
    RejectedItem,
    SignalCategoryAssessment,
    SignalEnvironment,
    StoryClusterSummary,
    UnexpectedDevelopment,
    AbsenceCheck,
    DevilsAdvocate,
    WatchlistItem,
    WeeklyEntry,
)
from src.monitor.newsletter.content_builder import (
    build_all_pages,
    _collect_developments,
    _collect_other_stories,
)
from src.monitor.newsletter.content_models import (
    CountryContent,
    DevelopmentContent,
)


# ---- Helpers ----

def _all_category_status(status=CategoryStatus.QUIET):
    return {c: status for c in SignalCategory}

def _all_category_assessments():
    return {
        c: SignalCategoryAssessment(
            current_assessment=f"Assessment for {c.value}",
            confidence=3,
            last_updated=date(2026, 3, 14),
        )
        for c in SignalCategory
    }

def _test_ledger(code="mx", country="Mexico") -> CountryLedger:
    return CountryLedger(
        country=country, code=code, tier="periphery",
        actors=[ActorRef(name="Leader", role="President", primary=True)],
        last_updated=date(2026, 3, 14), created=date(2026, 3, 1),
        posture_summary=PostureSummary(
            as_of=date(2026, 3, 14),
            text=f"{country} navigates complex pressures.",
            category_status=_all_category_status(),
        ),
        signal_categories=_all_category_assessments(),
    )

def _deep_dive_entry() -> WeeklyEntry:
    movements = {c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory}
    movements[SignalCategory.ALIGNMENT_DIPLOMATIC] = CategoryMovement(
        movement=Movement.SIGNIFICANT,
        developments=[
            Development(
                headline="Leader meets US envoy",
                date=date(2026, 3, 12),
                source="Reuters", source_tier=2,
                summary="Discussed bilateral trade.",
            ),
        ],
    )
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.DEEP_DIVE,
        activity_level={"rating": "moderate", "rationale": "test"},
        category_movements=movements,
        story_clusters=[
            StoryClusterSummary(
                headline="Infrastructure deal", summary="Major deal signed",
                source_url="https://reuters.com/infra", source_name="Reuters",
            ),
        ],
    )

def _test_global_ledger() -> GlobalLedger:
    return GlobalLedger(
        last_updated=date(2026, 3, 14), created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 14), text="Global test.", signal_environment=SignalEnvironment(),
        ),
        weekly_entries=[GlobalWeeklyEntry(
            week=date(2026, 3, 14),
            executive_briefing_items=[ExecutiveBriefingItem(
                title="Americas pushback",
                regions_involved=["americas"],
                what="Mexico resists.", why_it_matters="Tests leverage.",
                what_to_watch="G20 prep.", confidence=3,
            )],
            items_considered_rejected=[RejectedItem(candidate="X", reason_rejected="Y")],
        )],
        watchlist=[WatchlistItem(
            item="BRICS summit", signal_category=SignalCategory.ALIGNMENT_DIPLOMATIC,
            countries=["br", "in"], why_it_matters="Tests bloc cohesion.",
            trigger="Membership announcements.", added_week=date(2026, 3, 7),
        )],
    )

def _test_regional_report() -> RegionalReport:
    return RegionalReport(
        region=Region.AMERICAS, week=date(2026, 3, 14),
        regional_overview="The Americas region saw diplomatic shifts.",
        cross_cutting_dynamics=[CrossCuttingDynamic(
            title="Hemispheric realignment",
            countries_involved=["mx", "br"],
            signal_categories=["alignment_diplomatic"],
            pattern_type="parallel",
            assessment="Mexico and Brazil coordinating response.",
            significance="Tests hemispheric leverage.",
            trend="emerging",
            confidence=3, confidence_inherited_from={"mx": 3, "br": 3},
            weakest_link="", evidence_against_linkage="",
            linkage_strength="moderate", linkage_justification="",
            competing_interpretation="",
        )],
    )


# ---- Tests ----

class TestCollectDevelopments:
    def test_includes_significant_movements(self):
        entry = _deep_dive_entry()
        ledger = _test_ledger()
        devs = _collect_developments(entry, ledger)
        sig = [d for d in devs if d.movement == Movement.SIGNIFICANT]
        assert len(sig) >= 1
        assert "bilateral trade" in sig[0].text

    def test_includes_none_movements_with_assessment(self):
        """Movement.NONE categories should be included with current assessment."""
        entry = _deep_dive_entry()
        ledger = _test_ledger()
        devs = _collect_developments(entry, ledger)
        none_devs = [d for d in devs if d.movement == Movement.NONE]
        assert len(none_devs) >= 1  # at least some NONE categories included

    def test_all_categories_represented(self):
        """Every signal category should have at least one development."""
        entry = _deep_dive_entry()
        ledger = _test_ledger()
        devs = _collect_developments(entry, ledger)
        categories = {d.category for d in devs}
        assert categories == set(SignalCategory)

    def test_sorted_significant_first(self):
        entry = _deep_dive_entry()
        ledger = _test_ledger()
        devs = _collect_developments(entry, ledger)
        movements = [d.movement for d in devs]
        sig_idx = next(i for i, m in enumerate(movements) if m == Movement.SIGNIFICANT)
        none_idxs = [i for i, m in enumerate(movements) if m == Movement.NONE]
        for ni in none_idxs:
            assert ni > sig_idx


class TestCollectOtherStories:
    def test_collects_story_clusters(self):
        entry = _deep_dive_entry()
        stories = _collect_other_stories(entry)
        assert len(stories) == 1
        assert stories[0].headline == "Infrastructure deal"

    def test_empty_when_no_clusters(self):
        entry = _deep_dive_entry()
        entry.story_clusters = []
        assert _collect_other_stories(entry) == []


class TestBuildAllPages:
    def test_produces_all_page_types(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}

        overview, region_pages, watchlist, _ = build_all_pages(
            gl, reports, ledgers, entries, date(2026, 3, 14),
        )

        assert overview.country_count == 1
        assert len(overview.executive_brief.items) == 1
        assert Region.AMERICAS in region_pages
        assert len(watchlist.items) == 1

    def test_country_in_correct_region(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}

        _, region_pages, _, _ = build_all_pages(
            gl, reports, ledgers, entries, date(2026, 3, 14),
        )

        americas = region_pages[Region.AMERICAS]
        codes = [c.code for c in americas.countries]
        assert "mx" in codes

    def test_regional_lead_seeded_from_overview(self):
        """Regional lead is seeded from the synthesis overview for the editor."""
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}

        _, region_pages, _, _ = build_all_pages(
            gl, reports, ledgers, entries, date(2026, 3, 14),
        )

        americas = region_pages[Region.AMERICAS]
        assert americas.regional_lead == "The Americas region saw diplomatic shifts."

    def test_card_summary_placeholder(self):
        """Card summary is empty after build — the regional writer fills it later."""
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}

        _, region_pages, _, _ = build_all_pages(
            gl, reports, ledgers, entries, date(2026, 3, 14),
        )

        assert region_pages[Region.AMERICAS].card_summary == ""  # writer fills this later

    def test_country_content_has_developments(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}

        _, region_pages, _, _ = build_all_pages(
            gl, reports, ledgers, entries, date(2026, 3, 14),
        )

        mx = region_pages[Region.AMERICAS].countries[0]
        assert mx.code == "mx"
        assert len(mx.developments) >= 1
        assert mx.posture_summary == "Mexico navigates complex pressures."
