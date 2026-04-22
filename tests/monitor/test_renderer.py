"""Tests for the template renderer (content models → MDX)."""

from datetime import date

import pytest
from src.monitor.config import Movement, Region, SignalCategory
from src.monitor.newsletter.content_models import (
    BriefingItemInput,
    CountryContent,
    DevelopmentContent,
    ExecutiveBriefContent,
    OverviewPageContent,
    RegionPageContent,
    StoryClusterContent,
)
from src.monitor.newsletter.renderer import render_pages


def _test_overview() -> OverviewPageContent:
    return OverviewPageContent(
        week_start=date(2026, 3, 8),
        week_end=date(2026, 3, 14),
        country_count=28,
        executive_brief=ExecutiveBriefContent(
            items=[BriefingItemInput(
                title="Test item",
                regions_involved=["americas"],
                what="Something happened.",
                why_it_matters="It matters.",
                what_to_watch="Watch this.",
                confidence=3,
            )],
        ),
    )


def _test_region_page() -> RegionPageContent:
    return RegionPageContent(
        region=Region.AMERICAS,
        display_name="The Americas",
        week_start=date(2026, 3, 8),
        week_end=date(2026, 3, 14),
        regional_lead="The Americas region saw shifts.",
        gap_paragraphs=["Notably absent: Chile activity."],
        card_summary="Americas summary.",
        countries=[
            CountryContent(
                code="mx",
                country="Mexico",
                activity_rating="moderate",
                posture_summary="Mexico navigates complex pressures.",
                developments=[
                    DevelopmentContent(
                        category=SignalCategory.ALIGNMENT_DIPLOMATIC,
                        category_display="Diplomatic",
                        movement=Movement.SIGNIFICANT,
                        text="Discussed bilateral trade.",
                    ),
                ],
                other_stories=[
                    StoryClusterContent(
                        headline="Infrastructure deal",
                        summary="Major deal signed.",
                        source_name="Reuters",
                        source_url="https://reuters.com/infra",
                    ),
                ],
            ),
        ],
    )


class TestRenderPages:
    def test_produces_all_slugs(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        assert "overview" in pages
        assert "the-americas" in pages
        # watchlist.mdx is no longer rendered as of 015a040 (2026-04-13)
        assert "watchlist" not in pages

    def test_overview_has_frontmatter(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        assert '---' in pages["overview"]
        assert 'title: "The Middle Powers Monitor"' in pages["overview"]

    def test_overview_has_executive_brief(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        assert "Something happened." in pages["overview"]
        assert "It matters." in pages["overview"]

    def test_region_page_has_country(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        region = pages["the-americas"]
        assert "Mexico" in region
        assert "flagcdn.com/mx.svg" in region
        assert "bilateral trade" in region

    def test_region_page_has_regional_lead(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        assert "saw shifts" in pages["the-americas"]

    def test_region_page_has_other_stories(self):
        pages = render_pages(
            _test_overview(),
            {Region.AMERICAS: _test_region_page()},
        )
        region = pages["the-americas"]
        assert "<Accordion" in region
        assert "Infrastructure deal" in region

    # test_watchlist_page removed — watchlist.mdx rendering dropped in 015a040.

    def test_dollar_sign_escaped(self):
        overview = _test_overview()
        overview.executive_brief = ExecutiveBriefContent(
            items=[BriefingItemInput(
                title="Trade",
                regions_involved=["americas"],
                what="$500 billion deal.",
                why_it_matters="Matters.",
                what_to_watch="Watch.",
                confidence=3,
            )],
        )
        pages = render_pages(
            overview,
            {Region.AMERICAS: _test_region_page()},
        )
        assert "\\$500" in pages["overview"]

    def test_edited_essay_used_when_available(self):
        overview = _test_overview()
        overview.executive_brief.edited_essay = "This is the editor's polished essay."
        pages = render_pages(
            overview,
            {Region.AMERICAS: _test_region_page()},
        )
        assert "polished essay" in pages["overview"]
        # Should NOT show the raw item structure
        assert "What to watch" not in pages["overview"]
