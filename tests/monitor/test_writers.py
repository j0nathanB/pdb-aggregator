"""Tests for the regional and global writer agents + scoped editing."""

import json
from datetime import date
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitor.config import Region
from src.monitor.newsletter.content_models import (
    CountryContent,
    ExecutiveBriefContent,
    BriefingItemInput,
    OverviewPageContent,
    RegionPageContent,
    WatchlistPageContent,
)


# ---- Helpers ----

def _make_country(code: str, country: str, narrative: str) -> CountryContent:
    c = CountryContent(code=code, country=country)
    c.narrative_body = narrative
    return c


def _make_region_page(region: Region, display_name: str, countries: list) -> RegionPageContent:
    return RegionPageContent(
        region=region,
        display_name=display_name,
        week_start=date(2026, 4, 3),
        week_end=date(2026, 4, 9),
        countries=countries,
    )


def _make_overview(essay: str | None = None) -> OverviewPageContent:
    brief = ExecutiveBriefContent(
        items=[BriefingItemInput(
            title="Test", regions_involved=["Americas"],
            what="Test what", why_it_matters="Test why",
            what_to_watch="Test watch", confidence=4,
        )],
    )
    if essay:
        brief.edited_essay = essay
    return OverviewPageContent(
        week_start=date(2026, 4, 3),
        week_end=date(2026, 4, 9),
        country_count=5,
        executive_brief=brief,
    )


def _mock_response(response_json: dict):
    """Create a mock anthropic Message with the given JSON response."""
    response_text = json.dumps(response_json)
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(type="text", text=response_text)]
    mock_msg.usage = MagicMock(input_tokens=100, output_tokens=200)
    return mock_msg


def _patch_writer(module_path: str, response_json: dict):
    """Patch a writer module's LLM call stack to return canned JSON."""
    mock_msg = _mock_response(response_json)

    # Mock the stream context manager
    mock_stream_ctx = AsyncMock()
    mock_stream_ctx.__aenter__.return_value = mock_stream_ctx
    mock_stream_ctx.__aexit__.return_value = False
    mock_stream_ctx.get_final_message.return_value = mock_msg

    mock_client = MagicMock()
    mock_client.messages.stream.return_value = mock_stream_ctx

    # anthropic_limiter is a callable that returns an async context manager
    mock_limiter_ctx = AsyncMock()
    mock_limiter_ctx.__aenter__.return_value = None
    mock_limiter_ctx.__aexit__.return_value = False

    async def mock_heartbeat(coro, label):
        return mock_msg

    return (
        patch(f"{module_path}.anthropic.AsyncAnthropic", return_value=mock_client),
        patch(f"{module_path}.ANTHROPIC_API_KEY", "test-key"),
        patch("src.monitor.newsletter._streaming.anthropic_limiter", return_value=mock_limiter_ctx),
        patch("src.monitor.newsletter._streaming.with_heartbeat", side_effect=mock_heartbeat),
    )


# =============================================================================
# Regional writer tests
# =============================================================================


class TestRegionalWriter:

    @pytest.mark.asyncio
    async def test_write_regional_essay(self):
        from src.monitor.newsletter.regional_writer import write_regional_essay

        page = _make_region_page(
            Region.AMERICAS, "The Americas",
            [
                _make_country("mx", "Mexico", "Mexico's president signed a trade deal."),
                _make_country("br", "Brazil", "Brazil expanded its naval presence."),
            ],
        )

        expected = {
            "headline": "Latin America hedges its bets",
            "regional_lead": "Mexico and Brazil moved in different directions this week.",
        }

        patches = _patch_writer("src.monitor.newsletter.regional_writer", expected)
        with patches[0], patches[1], patches[2], patches[3]:
            result = await write_regional_essay(page)

        assert result.regional_lead == "Mexico and Brazil moved in different directions this week."
        assert result.card_summary == "Latin America hedges its bets"

    @pytest.mark.asyncio
    async def test_skips_region_without_prose(self):
        from src.monitor.newsletter.regional_writer import write_regional_essay

        page = _make_region_page(
            Region.AMERICAS, "The Americas",
            [_make_country("mx", "Mexico", "")],
        )
        page.countries[0].narrative_body = None

        with patch("src.monitor.newsletter.regional_writer.ANTHROPIC_API_KEY", "test-key"):
            result = await write_regional_essay(page)

        assert result.regional_lead == ""

    @pytest.mark.asyncio
    async def test_write_all_regional_essays(self):
        from src.monitor.newsletter.regional_writer import write_all_regional_essays

        pages = {
            Region.AMERICAS: _make_region_page(
                Region.AMERICAS, "The Americas",
                [_make_country("mx", "Mexico", "Mexico summary.")],
            ),
        }

        expected = {
            "headline": "Test headline",
            "regional_lead": "Test essay.",
        }

        patches = _patch_writer("src.monitor.newsletter.regional_writer", expected)
        with patches[0], patches[1], patches[2], patches[3]:
            result = await write_all_regional_essays(pages)

        assert result[Region.AMERICAS].regional_lead == "Test essay."


# =============================================================================
# Global writer tests
# =============================================================================


class TestGlobalWriter:

    @pytest.mark.asyncio
    async def test_write_global_essay(self):
        from src.monitor.newsletter.global_writer import write_global_essay

        overview = _make_overview()
        pages = {
            Region.AMERICAS: _make_region_page(
                Region.AMERICAS, "The Americas", [],
            ),
        }
        pages[Region.AMERICAS].regional_lead = "The Americas essay."

        expected = {
            "headline": "Global hedging accelerates",
            "edited_essay": "This week the world hedged.",
        }

        patches = _patch_writer("src.monitor.newsletter.global_writer", expected)
        with patches[0], patches[1], patches[2], patches[3]:
            result = await write_global_essay(overview, pages)

        assert result.executive_brief.edited_essay == "This week the world hedged."

    @pytest.mark.asyncio
    async def test_skips_without_regional_essays(self):
        from src.monitor.newsletter.global_writer import write_global_essay

        overview = _make_overview()
        pages = {
            Region.AMERICAS: _make_region_page(
                Region.AMERICAS, "The Americas", [],
            ),
        }

        with patch("src.monitor.newsletter.global_writer.ANTHROPIC_API_KEY", "test-key"):
            result = await write_global_essay(overview, pages)

        assert result.executive_brief.edited_essay is None


# =============================================================================
# Scoped editing tests
# =============================================================================


class TestScopedEditing:
    """Test that scope parameter correctly limits what gets processed."""

    def _make_fixtures(self):
        overview = _make_overview(essay="Pre-written executive essay.")
        country = _make_country("mx", "Mexico", "Mexico narrative.")
        page = _make_region_page(Region.AMERICAS, "The Americas", [country])
        page.regional_lead = "Regional essay here."
        page.card_summary = "Card summary."
        pages = {Region.AMERICAS: page}
        watchlist = WatchlistPageContent(
            week_start=date(2026, 4, 3), week_end=date(2026, 4, 9),
        )
        return overview, pages, watchlist

    @pytest.mark.asyncio
    async def test_scope_countries_skips_regional_and_executive(self):
        """scope='countries' should not edit regional leads or executive brief."""
        from src.monitor.newsletter.structured_editor import edit_all

        overview, pages, watchlist = self._make_fixtures()
        original_lead = pages[Region.AMERICAS].regional_lead
        original_essay = overview.executive_brief.edited_essay

        async def passthrough_country(c, **kw):
            return c

        with patch("src.monitor.newsletter.structured_editor.edit_country", side_effect=passthrough_country):
            result_ov, result_pages, _ = await edit_all(
                overview, pages, watchlist, scope="countries",
            )

        # Regional and executive should be untouched
        assert result_pages[Region.AMERICAS].regional_lead == original_lead
        assert result_ov.executive_brief.edited_essay == original_essay

    @pytest.mark.asyncio
    async def test_scope_regional_skips_countries_and_executive(self):
        """scope='regional' should not edit countries or executive brief."""
        from src.monitor.newsletter.structured_editor import edit_all

        overview, pages, watchlist = self._make_fixtures()
        original_body = pages[Region.AMERICAS].countries[0].narrative_body
        original_essay = overview.executive_brief.edited_essay

        async def passthrough_regional(p, **kw):
            return p

        with patch("src.monitor.newsletter.structured_editor.edit_regional", side_effect=passthrough_regional):
            result_ov, result_pages, _ = await edit_all(
                overview, pages, watchlist, scope="regional",
            )

        # Country and executive should be untouched
        assert result_pages[Region.AMERICAS].countries[0].narrative_body == original_body
        assert result_ov.executive_brief.edited_essay == original_essay

    @pytest.mark.asyncio
    async def test_scope_executive_skips_countries_and_regional(self):
        """scope='executive' should not edit countries or regional leads."""
        from src.monitor.newsletter.structured_editor import edit_all

        overview, pages, watchlist = self._make_fixtures()
        original_body = pages[Region.AMERICAS].countries[0].narrative_body
        original_lead = pages[Region.AMERICAS].regional_lead

        async def passthrough_exec(b, **kw):
            return b

        with patch("src.monitor.newsletter.structured_editor.edit_executive", side_effect=passthrough_exec):
            result_ov, result_pages, _ = await edit_all(
                overview, pages, watchlist, scope="executive",
            )

        # Country and regional should be untouched
        assert result_pages[Region.AMERICAS].countries[0].narrative_body == original_body
        assert result_pages[Region.AMERICAS].regional_lead == original_lead
