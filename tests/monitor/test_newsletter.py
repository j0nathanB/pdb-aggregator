"""Tests for newsletter assembly: deterministic Markdown rendering."""

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
    AbsenceCheck,
    ActorRef,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    DevilsAdvocate,
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
    WatchlistItem,
    WeeklyEntry,
)
from src.monitor.newsletter.assembly import (
    CONFIDENCE_LABELS,
    REGION_DISPLAY_NAMES,
    REGION_ORDER,
    SIGNAL_CATEGORY_DISPLAY,
    _format_date_range,
    _render_deep_dive_entry,
    _render_executive_brief,
    _render_footer,
    _render_header,
    _render_maintenance_entry,
    _render_regional_lead,
    _render_watchlist,
    assemble_newsletter,
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
        country=country,
        code=code,
        tier="periphery",
        actors=[ActorRef(name="Leader", role="President", primary=True)],
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
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
                source="Reuters",
                source_tier=2,
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
        devils_advocate=DevilsAdvocate(
            challenges=["The meeting may be routine rather than a policy shift."],
        ),
    )


def _maintenance_entry() -> WeeklyEntry:
    return WeeklyEntry(
        week=date(2026, 3, 14),
        date_range="2026-03-07 to 2026-03-14",
        depth=Depth.MAINTENANCE,
    )


def _test_global_ledger() -> GlobalLedger:
    return GlobalLedger(
        last_updated=date(2026, 3, 14),
        created=date(2026, 3, 1),
        global_posture_summary=GlobalPostureSummary(
            as_of=date(2026, 3, 14),
            text="Global test posture.",
            signal_environment=SignalEnvironment(),
        ),
        weekly_entries=[
            GlobalWeeklyEntry(
                week=date(2026, 3, 14),
                executive_briefing_items=[
                    ExecutiveBriefingItem(
                        title="Americas pushback crystallizes",
                        regions_involved=["americas"],
                        what="Mexico and Brazil resist US pressure.",
                        why_it_matters="Tests hemispheric leverage.",
                        what_to_watch="G20 preparations.",
                        confidence=3,
                    ),
                ],
                items_considered_rejected=[
                    RejectedItem(candidate="X", reason_rejected="Y"),
                ],
            )
        ],
        watchlist=[
            WatchlistItem(
                item="BRICS expansion summit",
                signal_category=SignalCategory.INSTITUTIONAL,
                countries=["br", "in"],
                why_it_matters="Could reshape institutional order.",
                trigger="Formal invitations.",
                added_week=date(2026, 3, 14),
            ),
        ],
    )


def _test_regional_report() -> RegionalReport:
    return RegionalReport(
        region=Region.AMERICAS,
        week=date(2026, 3, 14),
        cross_cutting_dynamics=[
            CrossCuttingDynamic(
                title="Coordinated pushback",
                countries_involved=["mx", "br"],
                signal_categories=["alignment_diplomatic"],
                pattern_type="parallel",
                assessment="Both escalating sovereignty rhetoric.",
                significance="Indicates potential Americas-wide realignment.",
                trend="developing",
                confidence=3,
                confidence_inherited_from={"mx": 4, "br": 3},
                weakest_link="Brazil single-source BRICS report.",
                evidence_against_linkage="Countries may be responding independently.",
                linkage_strength="moderate",
                linkage_justification="Shared US pressure and temporal proximity.",
                competing_interpretation="Independent domestic pressures.",
            ),
        ],
    )


# ---- Header ----

class TestRenderHeader:
    def test_includes_title(self):
        result = _render_header(date(2026, 3, 14), 10, 18)
        assert "# The Middle Powers Monitor" in result

    def test_includes_date_range(self):
        result = _render_header(date(2026, 3, 14), 10, 18)
        assert "March 8, 2026" in result

    def test_coverage_stats_not_in_header(self):
        """Coverage stats were removed from header — verify they stay out."""
        result = _render_header(date(2026, 3, 14), 10, 18)
        assert "countries received" not in result


class TestFormatDateRange:
    def test_formats_correctly(self):
        result = _format_date_range(date(2026, 3, 14))
        assert "March" in result
        assert "2026" in result


# ---- Executive Brief ----

class TestRenderExecutiveBrief:
    def test_renders_items_with_h3(self):
        items = [ExecutiveBriefingItem(
            title="Test Title",
            what="What happened.",
            why_it_matters="Why it matters.",
            what_to_watch="What to watch.",
            confidence=3,
        )]
        result = _render_executive_brief(items)
        assert "### Test Title" in result
        assert "What happened." in result
        assert "Why it matters." in result
        assert "What to watch" in result

    def test_confidence_not_rendered(self):
        """Confidence labels are no longer rendered in the executive brief."""
        items = [ExecutiveBriefingItem(
            title="T", what="W", why_it_matters="M", confidence=4,
        )]
        result = _render_executive_brief(items)
        assert "confidence" not in result.lower()

    def test_items_ordered_by_confidence(self):
        items = [
            ExecutiveBriefingItem(title="Low", what=".", why_it_matters=".", confidence=2),
            ExecutiveBriefingItem(title="High", what=".", why_it_matters=".", confidence=5),
        ]
        result = _render_executive_brief(items)
        high_pos = result.find("High")
        low_pos = result.find("Low")
        assert high_pos < low_pos

    def test_confidence_note_not_rendered(self):
        """Confidence notes are no longer rendered in the executive brief."""
        items = [ExecutiveBriefingItem(
            title="T", what="W", why_it_matters="M",
            confidence=3, confidence_note="Rests on single-source data.",
        )]
        result = _render_executive_brief(items)
        assert "Rests on single-source data" not in result

    def test_empty_items_fallback(self):
        result = _render_executive_brief([])
        assert "No system-level dynamics" in result


# ---- Regional Lead ----

class TestRenderRegionalLead:
    def test_renders_dynamics(self):
        result = _render_regional_lead(Region.AMERICAS, _test_regional_report())
        assert "sovereignty rhetoric" in result

    def test_none_report_fallback(self):
        result = _render_regional_lead(Region.AMERICAS, None)
        assert "No significant cross-country dynamics" in result
        assert "The Americas" in result

    def test_no_dynamics_fallback(self):
        empty_report = RegionalReport(region=Region.AMERICAS, week=date(2026, 3, 14))
        result = _render_regional_lead(Region.AMERICAS, empty_report)
        assert "No significant cross-country dynamics" in result

    def test_no_confidence_parenthetical(self):
        """Confidence parentheticals are no longer rendered in regional leads."""
        report = _test_regional_report()
        result = _render_regional_lead(Region.AMERICAS, report)
        assert "confidence" not in result.lower()

    def test_hides_confidence_when_high(self):
        report = RegionalReport(
            region=Region.AMERICAS,
            week=date(2026, 3, 14),
            cross_cutting_dynamics=[
                CrossCuttingDynamic(
                    title="T", countries_involved=["mx"], signal_categories=["alignment_diplomatic"],
                    pattern_type="parallel", assessment="Test.", significance="Sig.",
                    trend="developing", confidence=4,
                    confidence_inherited_from={"mx": 4},
                    weakest_link="", evidence_against_linkage="",
                    linkage_strength="strong", linkage_justification="",
                    competing_interpretation="",
                ),
            ],
        )
        result = _render_regional_lead(Region.AMERICAS, report)
        assert "confidence" not in result.lower()

    def test_includes_gaps(self):
        report = RegionalReport(
            region=Region.AMERICAS,
            week=date(2026, 3, 14),
            cross_cutting_dynamics=[
                CrossCuttingDynamic(
                    title="T", countries_involved=["mx"], signal_categories=["alignment_diplomatic"],
                    pattern_type="parallel", assessment="Test.", significance="",
                    trend="developing", confidence=4,
                    confidence_inherited_from={"mx": 4},
                    weakest_link="", evidence_against_linkage="",
                    linkage_strength="strong", linkage_justification="",
                    competing_interpretation="",
                ),
            ],
            gaps=[
                Gap(expected_dynamic="Pacific Alliance coordination", observed="None", assessment="Alliance appears dormant."),
            ],
        )
        result = _render_regional_lead(Region.AMERICAS, report)
        assert "Notably absent" in result
        assert "Pacific Alliance" in result

    def test_omits_competing_interpretation(self):
        """Spec says competing interpretations are not rendered in newsletter."""
        result = _render_regional_lead(Region.AMERICAS, _test_regional_report())
        assert "Independent domestic pressures" not in result

    def test_omits_evidence_against_linkage(self):
        result = _render_regional_lead(Region.AMERICAS, _test_regional_report())
        assert "responding independently" not in result


# ---- Deep Dive Entry ----

class TestRenderDeepDiveEntry:
    def test_h3_header(self):
        result = _render_deep_dive_entry("mx", _test_ledger(), _deep_dive_entry())
        assert "###" in result and "Mexico" in result

    def test_includes_posture(self):
        result = _render_deep_dive_entry("mx", _test_ledger(), _deep_dive_entry())
        assert "navigates complex pressures" in result

    def test_includes_developments(self):
        result = _render_deep_dive_entry("mx", _test_ledger(), _deep_dive_entry())
        assert "Discussed bilateral trade" in result

    def test_uses_category_display_name(self):
        result = _render_deep_dive_entry("mx", _test_ledger(), _deep_dive_entry())
        assert "**Diplomatic:**" in result

    def test_no_caveat_lector_in_brief(self):
        result = _render_deep_dive_entry("mx", _test_ledger(), _deep_dive_entry())
        assert "Caveat Lector" not in result

    def test_other_stories_accordion(self):
        entry = _deep_dive_entry()
        entry.story_clusters = [
            StoryClusterSummary(
                headline="Leader meets US envoy",
                summary="Discussed bilateral trade.",
                source_url="https://reuters.com/1",
                source_name="reuters.com",
            ),
            StoryClusterSummary(
                headline="Central bank holds rate steady",
                summary="Rate held at 9.5%.",
                source_url="https://elfinanciero.com/1",
                source_name="elfinanciero.com",
            ),
            StoryClusterSummary(
                headline="Oil spill affects Gulf coast",
                summary="Massive spill hit 39 communities.",
                source_url="https://jornada.com.mx/1",
                source_name="jornada.com.mx",
            ),
        ]
        # The first cluster's source_url isn't in key developments (dev has no source_url),
        # so all three should appear
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "<Accordion title=\"Other Stories\">" in result
        assert "**Central bank holds rate steady**" in result
        assert "**Oil spill affects Gulf coast**" in result
        assert "elfinanciero.com" in result
        assert "</Accordion>" in result

    def test_other_stories_excludes_key_developments(self):
        entry = _deep_dive_entry()
        # Add source URL to the development so it matches a cluster
        entry.category_movements[SignalCategory.ALIGNMENT_DIPLOMATIC].developments[0].sources[0].url = "https://reuters.com/1"
        entry.story_clusters = [
            StoryClusterSummary(
                headline="Leader meets US envoy",
                summary="Discussed bilateral trade.",
                source_url="https://reuters.com/1",
                source_name="reuters.com",
            ),
            StoryClusterSummary(
                headline="Central bank holds rate steady",
                summary="Rate held at 9.5%.",
                source_url="https://elfinanciero.com/1",
                source_name="elfinanciero.com",
            ),
        ]
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "Leader meets US envoy" not in result.split("Other Stories")[1]
        assert "Central bank holds rate steady" in result

    def test_no_other_stories_when_empty(self):
        entry = _deep_dive_entry()
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "Other Stories" not in result

    def test_no_movements_shows_fallback(self):
        entry = WeeklyEntry(
            week=date(2026, 3, 14),
            date_range="2026-03-07 to 2026-03-14",
            depth=Depth.DEEP_DIVE,
            activity_level={"rating": "low", "rationale": "test"},
            category_movements={c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory},
        )
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "no significant posture changes" in result

    def test_unexpected_developments(self):
        entry = _deep_dive_entry()
        entry.unexpected_developments = [
            UnexpectedDevelopment(
                headline="CJNG successor named",
                date=date(2026, 3, 11),
                source="Proceso",
                source_tier=3,
                signal_category=SignalCategory.SECURITY_DEFENSE,
                assessment="Could reshape cartel dynamics.",
            ),
        ]
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "**Unexpected:**" in result
        assert "CJNG successor" in result

    def test_absence_checks(self):
        entry = _deep_dive_entry()
        entry.absence_check = [
            AbsenceCheck(
                expected="USMCA review statement",
                signal_category=SignalCategory.ECONOMIC_TECH,
                occurred=False,
                significance="Silence may indicate negotiations.",
            ),
        ]
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        assert "**Notable absence:**" in result
        assert "USMCA" in result

    def test_max_five_developments(self):
        """Only the top 5 developments should be rendered."""
        movements = {c: CategoryMovement(movement=Movement.NONE) for c in SignalCategory}
        devs = [
            Development(headline=f"Dev {i}", date=date(2026, 3, 12), source="R", source_tier=2, summary=f"S{i}")
            for i in range(7)
        ]
        movements[SignalCategory.ALIGNMENT_DIPLOMATIC] = CategoryMovement(
            movement=Movement.SIGNIFICANT, developments=devs[:4],
        )
        movements[SignalCategory.SECURITY_DEFENSE] = CategoryMovement(
            movement=Movement.MINOR, developments=devs[4:],
        )
        entry = WeeklyEntry(
            week=date(2026, 3, 14), date_range="d", depth=Depth.DEEP_DIVE,
            activity_level={"rating": "high", "rationale": "test"},
            category_movements=movements,
        )
        result = _render_deep_dive_entry("mx", _test_ledger(), entry)
        # Should have at most 5 bullet points
        assert result.count("- **") <= 5


# ---- Maintenance Entry ----

class TestRenderMaintenanceEntry:
    def test_h3_header(self):
        result = _render_maintenance_entry("mx", _test_ledger(), _maintenance_entry())
        assert "###" in result and "Mexico" in result

    def test_posture_and_no_developments(self):
        result = _render_maintenance_entry("mx", _test_ledger(), _maintenance_entry())
        assert "navigates complex pressures" in result
        assert "No significant developments" in result

    def test_no_between_the_lines(self):
        result = _render_maintenance_entry("mx", _test_ledger(), _maintenance_entry())
        assert "Caveat Lector" not in result


# ---- Watchlist ----

class TestRenderWatchlist:
    def test_renders_items(self):
        items = [WatchlistItem(
            item="Test watch item",
            signal_category=SignalCategory.INSTITUTIONAL,
            countries=["br", "in"],
            why_it_matters="Important.",
            trigger="Some trigger.",
            added_week=date(2026, 3, 14),
        )]
        result = _render_watchlist(items)
        assert "## Watchlist" in result
        assert "Test watch item" in result
        assert "BR, IN" in result
        assert "Important." in result
        assert "Trigger: Some trigger." in result

    def test_empty_watchlist_returns_empty(self):
        result = _render_watchlist([])
        assert result == ""

    def test_max_ten_items(self):
        items = [
            WatchlistItem(
                item=f"Item {i}",
                signal_category=SignalCategory.INSTITUTIONAL,
                countries=["br"],
                added_week=date(2026, 3, i + 1),
            )
            for i in range(15)
        ]
        result = _render_watchlist(items)
        # Should only render 10 items
        assert result.count("- **Item") == 10

    def test_includes_subtitle(self):
        items = [WatchlistItem(
            item="X", signal_category=SignalCategory.INSTITUTIONAL,
            countries=[], added_week=date(2026, 3, 14),
        )]
        result = _render_watchlist(items)
        assert "Items worth monitoring" in result


# ---- Footer ----

class TestRenderFooter:
    def test_includes_description(self):
        result = _render_footer(date(2026, 3, 14))
        assert "30 countries" in result
        assert "six regions" in result

    def test_includes_date(self):
        result = _render_footer(date(2026, 3, 14))
        assert "2026-03-14" in result


# ---- Region Order ----

class TestRegionOrder:
    def test_central_eastern_europe_first(self):
        assert REGION_ORDER[0] == Region.CENTRAL_EASTERN_EUROPE

    def test_americas_last(self):
        assert REGION_ORDER[-1] == Region.AMERICAS

    def test_all_regions_present(self):
        assert set(REGION_ORDER) == set(Region)


# ---- Full Assembly ----

class TestAssembleNewsletter:
    def test_produces_markdown(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger("mx", "Mexico")}
        entries = {"mx": _deep_dive_entry()}

        newsletter = assemble_newsletter(gl, reports, ledgers, entries, date(2026, 3, 14))
        assert "# The Middle Powers Monitor" in newsletter

    def test_includes_executive_brief(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        assert "Americas pushback crystallizes" in newsletter

    def test_includes_all_region_headers(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        for display_name in REGION_DISPLAY_NAMES.values():
            assert display_name in newsletter

    def test_includes_country_sections(self):
        gl = _test_global_ledger()
        ledgers = {"mx": _test_ledger("mx", "Mexico")}
        entries = {"mx": _deep_dive_entry()}
        newsletter = assemble_newsletter(gl, {}, ledgers, entries, date(2026, 3, 14))
        assert "Mexico" in newsletter
        assert "Discussed bilateral trade" in newsletter

    def test_includes_watchlist(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        assert "BRICS expansion summit" in newsletter

    def test_includes_regional_lead(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        newsletter = assemble_newsletter(gl, reports, {}, {}, date(2026, 3, 14))
        assert "sovereignty rhetoric" in newsletter

    def test_region_order_in_output(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        cee_pos = newsletter.find("Central-Eastern Europe")
        americas_pos = newsletter.find("The Americas")
        assert cee_pos < americas_pos

    def test_coverage_stats_not_in_newsletter(self):
        """Coverage stats were removed from the newsletter header."""
        gl = _test_global_ledger()
        entries = {"mx": _deep_dive_entry(), "br": _maintenance_entry()}
        newsletter = assemble_newsletter(gl, {}, {}, entries, date(2026, 3, 14))
        assert "countries received" not in newsletter

    def test_includes_footer(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        assert "30 countries across six regions" in newsletter
        assert "2026-03-14" in newsletter

    def test_empty_watchlist_omitted(self):
        gl = _test_global_ledger()
        gl.watchlist = []
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        assert "## Watchlist" not in newsletter

    def test_deep_dive_before_maintenance(self):
        gl = _test_global_ledger()
        ledgers = {
            "mx": _test_ledger("mx", "Mexico"),
            "br": _test_ledger("br", "Brazil"),
        }
        entries = {
            "mx": _deep_dive_entry(),
            "br": _maintenance_entry(),
        }
        newsletter = assemble_newsletter(gl, {}, ledgers, entries, date(2026, 3, 14))
        mx_pos = newsletter.find("Mexico")
        br_pos = newsletter.find("Brazil")
        if mx_pos != -1 and br_pos != -1:
            assert mx_pos < br_pos

    def test_h2_for_regions(self):
        gl = _test_global_ledger()
        newsletter = assemble_newsletter(gl, {}, {}, {}, date(2026, 3, 14))
        assert "## Central-Eastern Europe" in newsletter
        assert "## The Americas" in newsletter
