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


# =============================================================================
# Trace preload: verify build_all_pages reads prior editor outputs from
# briefs/{date}/traces/ so scoped recoveries don't wipe non-target content.
# Regression guard for the 2026-04-19 recovery regression documented in
# commits 5685d9a and 9c72ca4.
# =============================================================================


class TestBuildAllPagesTracePreload:
    """Prior editor outputs (narrative_body / regional_lead / edited_essay /
    other_stories / card_summary / headline) should be preloaded from the
    latest trace on disk so a recovery that doesn't re-run the editor for
    a given country / region / executive keeps its prior polished content.
    """

    @pytest.fixture
    def fake_project_root(self, tmp_path, monkeypatch):
        """Point _trace_reader at a tmp_path and yield the traces dir."""
        import src.monitor.newsletter._trace_reader as tr
        monkeypatch.setattr(tr, "PROJECT_ROOT", tmp_path)
        traces = tmp_path / "briefs" / "20260314" / "traces"
        traces.mkdir(parents=True)
        return traces

    def _write_trace(self, traces_dir, stem, payload):
        import json
        (traces_dir / f"{stem}.json").write_text(json.dumps({
            "agent": stem.split("_")[0],
            "label": stem,
            "run_date": "2026-03-14",
            "output": {"response_text": json.dumps(payload), "parsed": None, "thinking": ""},
            "usage": {},
        }))

    def _build(self):
        gl = _test_global_ledger()
        reports = {Region.AMERICAS: _test_regional_report()}
        ledgers = {"mx": _test_ledger()}
        entries = {"mx": _deep_dive_entry()}
        return build_all_pages(gl, reports, ledgers, entries, date(2026, 3, 14))

    def test_narrative_body_preloaded_from_style_editor(self, fake_project_root):
        self._write_trace(fake_project_root, "style_editor_mx",
                          {"narrative_body": "STYLE-POLISHED PROSE"})
        _, region_pages, _, _ = self._build()
        mx = region_pages[Region.AMERICAS].countries[0]
        assert mx.narrative_body == "STYLE-POLISHED PROSE"

    def test_narrative_falls_through_priority_order(self, fake_project_root):
        """style_editor > copyeditor > editor. Missing higher priorities fall through."""
        self._write_trace(fake_project_root, "copyeditor_mx",
                          {"narrative_body": "COPYEDITED PROSE"})
        self._write_trace(fake_project_root, "editor_mx",
                          {"narrative_body": "FIRST-PASS PROSE"})
        # No style_editor trace — should pick copyeditor.
        _, region_pages, _, _ = self._build()
        assert region_pages[Region.AMERICAS].countries[0].narrative_body == "COPYEDITED PROSE"

    def test_other_stories_preloaded_from_copyeditor(self, fake_project_root):
        """Style_editor's tool schema is narrative_body only; other_stories
        must come from copyeditor. The merge helper should find the polished
        headline/summary even when style_editor's trace also exists."""
        self._write_trace(fake_project_root, "style_editor_mx",
                          {"narrative_body": "STYLE PROSE"})
        self._write_trace(fake_project_root, "copyeditor_mx", {
            "narrative_body": "COPY PROSE",  # not used — style_editor wins
            "other_stories": [
                {"headline": "Polished headline", "summary": "Polished summary"},
            ],
        })
        _, region_pages, _, _ = self._build()
        mx = region_pages[Region.AMERICAS].countries[0]
        assert mx.narrative_body == "STYLE PROSE"
        assert len(mx.other_stories) == 1
        assert mx.other_stories[0].headline == "Polished headline"
        assert mx.other_stories[0].summary == "Polished summary"

    def test_other_stories_keeps_source_fields(self, fake_project_root):
        """Copyeditor polishes headline/summary but doesn't round-trip
        source_url/source_name. Those must survive from the ledger cluster."""
        self._write_trace(fake_project_root, "copyeditor_mx", {
            "narrative_body": "PROSE",
            "other_stories": [{"headline": "Polished", "summary": "Summary"}],
        })
        _, region_pages, _, _ = self._build()
        mx = region_pages[Region.AMERICAS].countries[0]
        # source_url / source_name come from _deep_dive_entry.story_clusters
        assert mx.other_stories[0].source_url == "https://reuters.com/infra"
        assert mx.other_stories[0].source_name == "Reuters"

    def test_regional_lead_preloaded(self, fake_project_root):
        """Without a trace, regional_lead seeds from synthesis overview.
        With a trace, prior polished essay wins."""
        self._write_trace(fake_project_root, "style_editor_regional_americas",
                          {"regional_lead": "POLISHED ESSAY", "headline": "Hook"})
        _, region_pages, _, _ = self._build()
        page = region_pages[Region.AMERICAS]
        assert page.regional_lead == "POLISHED ESSAY"
        assert page.headline == "Hook"
        # card_summary falls back to headline when editor didn't emit card_summary
        assert page.card_summary == "Hook"

    def test_regional_card_summary_uses_editor_field_when_present(self, fake_project_root):
        """When the regional editor emits a distinct card_summary, use it,
        don't collapse back to headline."""
        self._write_trace(fake_project_root, "editor_regional_americas", {
            "regional_lead": "ESSAY",
            "headline": "Hook",
            "card_summary": "Distinct card summary for at-a-glance",
        })
        _, region_pages, _, _ = self._build()
        page = region_pages[Region.AMERICAS]
        assert page.card_summary == "Distinct card summary for at-a-glance"

    def test_executive_essay_preloaded(self, fake_project_root):
        self._write_trace(fake_project_root, "style_editor_executive",
                          {"edited_essay": "EXEC ESSAY", "headline": "Exec Hook"})
        overview, _, _, _ = self._build()
        assert overview.executive_brief.edited_essay == "EXEC ESSAY"
        assert overview.executive_brief.headline == "Exec Hook"

    def test_no_traces_dir_means_empty_fields(self, tmp_path, monkeypatch):
        """First week for a date (no briefs/{date}/traces/ yet) → fields
        stay at their defaults, no exceptions."""
        import src.monitor.newsletter._trace_reader as tr
        monkeypatch.setattr(tr, "PROJECT_ROOT", tmp_path)
        # No traces dir created.
        overview, region_pages, _, _ = self._build()
        mx = region_pages[Region.AMERICAS].countries[0]
        assert mx.narrative_body is None
        assert overview.executive_brief.edited_essay is None

    def test_malformed_trace_does_not_crash(self, fake_project_root):
        """If response_text isn't parseable as JSON, skip the trace."""
        import json
        (fake_project_root / "editor_mx.json").write_text(json.dumps({
            "output": {"response_text": "not valid json {{", "parsed": None},
        }))
        # Should not raise
        _, region_pages, _, _ = self._build()
        mx = region_pages[Region.AMERICAS].countries[0]
        # Falls through to default since no valid trace exists
        assert mx.narrative_body is None

    def test_rendered_region_uses_prose_when_trace_exists(self, fake_project_root):
        """End-to-end regression guard for the 2026-04-19 recovery bug:
        when a prior editor trace exists for a country, the rendered region
        MDX must render polished prose — NOT fall through to the bulleted
        {% else %} branch in region.mdx.j2. This is the specific failure
        mode that silently regressed 12 non-target countries after a
        scoped recovery before commits 9c72ca4 and 7a35493.
        """
        from src.monitor.newsletter.renderer import render_pages
        self._write_trace(fake_project_root, "style_editor_mx",
                          {"narrative_body": "Mexico's week in polished prose."})
        overview, region_pages, _, _ = self._build()
        rendered = render_pages(overview, region_pages)
        americas_mdx = rendered["the-americas"]
        assert "Mexico's week in polished prose." in americas_mdx
        # The bulleted-fallback template branch emits "**Key developments:**"
        # when narrative_body is empty. Its absence proves preload worked.
        assert "**Key developments:**" not in americas_mdx

    def test_rendered_region_falls_back_when_no_trace(self, fake_project_root):
        """Mirror of the above: with NO trace and NO live editor pass,
        the template's bulleted {% else %} branch should fire (the known
        pre-preload behavior). This pins the template's escape hatch so
        we notice if it ever silently changes.
        """
        from src.monitor.newsletter.renderer import render_pages
        # No traces written for mx.
        overview, region_pages, _, _ = self._build()
        rendered = render_pages(overview, region_pages)
        americas_mdx = rendered["the-americas"]
        assert "**Key developments:**" in americas_mdx
