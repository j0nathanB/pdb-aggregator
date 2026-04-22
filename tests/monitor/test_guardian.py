"""Tests for the Guardian Open Platform API client."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitor.collection.guardian import (
    GUARDIAN_COUNTRIES,
    GuardianAPI,
    GuardianArticle,
    guardian_extract_for_country,
    guardian_triage_for_country,
    strip_html,
)


# =============================================================================
# Fixtures
# =============================================================================


SAMPLE_API_RESPONSE = {
    "response": {
        "status": "ok",
        "total": 2,
        "startIndex": 1,
        "pageSize": 50,
        "currentPage": 1,
        "pages": 1,
        "orderBy": "newest",
        "results": [
            {
                "id": "world/2026/mar/18/india-jaishankar-defence-cooperation-australia",
                "type": "article",
                "sectionId": "world",
                "sectionName": "World news",
                "webPublicationDate": "2026-03-18T14:06:14Z",
                "webTitle": "India and Australia deepen defence ties amid Indo-Pacific tensions",
                "webUrl": "https://www.theguardian.com/world/2026/mar/18/india-jaishankar-defence-cooperation-australia",
                "apiUrl": "https://content.guardianapis.com/world/2026/mar/18/india-jaishankar-defence-cooperation-australia",
                "fields": {
                    "headline": "India and Australia deepen defence ties amid Indo-Pacific tensions",
                    "standfirst": "<p>Jaishankar and Penny Wong sign new security pact</p>",
                    "body": "<p>India's foreign minister S Jaishankar met with Australian counterpart Penny Wong on Tuesday to sign a landmark defence cooperation agreement.</p><p>The pact includes joint naval exercises in the Indian Ocean and intelligence sharing on maritime threats.</p>",
                    "byline": "Helen Davidson in Sydney",
                    "wordcount": "1247",
                    "shortUrl": "https://www.theguardian.com/p/abc123",
                },
                "tags": [
                    {"id": "world/india", "type": "keyword", "webTitle": "India"},
                    {"id": "world/australia", "type": "keyword", "webTitle": "Australia"},
                    {"id": "world/asia-pacific", "type": "keyword", "webTitle": "Asia Pacific"},
                ],
            },
            {
                "id": "world/2026/mar/17/modi-semiconductor-investment",
                "type": "article",
                "sectionId": "world",
                "sectionName": "World news",
                "webPublicationDate": "2026-03-17T09:00:00Z",
                "webTitle": "Modi announces semiconductor manufacturing push",
                "webUrl": "https://www.theguardian.com/world/2026/mar/17/modi-semiconductor-investment",
                "fields": {
                    "headline": "Modi announces semiconductor manufacturing push",
                    "body": "<p>Prime Minister Narendra Modi unveiled a $10bn semiconductor manufacturing initiative.</p>",
                    "byline": "Michael Safi in Delhi",
                    "wordcount": "890",
                },
                "tags": [
                    {"id": "world/india", "type": "keyword", "webTitle": "India"},
                ],
            },
        ],
    }
}

SAMPLE_SINGLE_ARTICLE = {
    "response": {
        "status": "ok",
        "content": SAMPLE_API_RESPONSE["response"]["results"][0],
    }
}


@pytest.fixture
def mock_api():
    api = GuardianAPI(api_key="test-key")
    return api


# =============================================================================
# strip_html tests
# =============================================================================


class TestStripHtml:
    def test_paragraphs(self):
        html = "<p>First paragraph.</p><p>Second paragraph.</p>"
        result = strip_html(html)
        assert "First paragraph." in result
        assert "Second paragraph." in result
        assert "\n\n" in result

    def test_headings(self):
        html = "<h2>Section Title</h2><p>Content here.</p>"
        result = strip_html(html)
        assert "Section Title" in result
        assert "Content here." in result

    def test_br_tags(self):
        html = "Line one.<br/>Line two.<br>Line three."
        result = strip_html(html)
        assert "Line one.\nLine two.\nLine three." == result

    def test_html_entities(self):
        html = "<p>He said &ldquo;hello&rdquo; &amp; goodbye.</p>"
        result = strip_html(html)
        assert "\u201chello\u201d" in result
        assert "& goodbye" in result

    def test_empty_input(self):
        assert strip_html("") == ""

    def test_plain_text_passthrough(self):
        assert strip_html("No tags here.") == "No tags here."

    def test_nested_tags(self):
        html = "<p>Text with <strong>bold</strong> and <em>italic</em>.</p>"
        result = strip_html(html)
        assert "Text with bold and italic." in result


# =============================================================================
# GuardianArticle tests
# =============================================================================


class TestGuardianArticle:
    def test_to_extraction_format(self):
        article = GuardianArticle(
            url="https://www.theguardian.com/world/2026/mar/18/test",
            guardian_id="world/2026/mar/18/test",
            title="Test Article",
            text="Full article text here.",
            snippet="Summary of the article.",
            byline="Reporter Name",
            wordcount=500,
            publication_date="2026-03-18T14:00:00Z",
            section="world",
            tags=["world/india"],
            short_url="https://www.theguardian.com/p/abc",
        )

        fmt = article.to_extraction_format()

        assert fmt["url"] == article.url
        assert fmt["domain"] == "theguardian.com"
        assert fmt["title"] == "Test Article"
        assert fmt["text"] == "Full article text here."
        assert fmt["extraction_method"] == "publisher_api_guardian"
        assert fmt["extraction_failed"] is False
        assert fmt["source_layer"] == "layer1"
        assert fmt["metadata"]["guardian_id"] == "world/2026/mar/18/test"
        assert fmt["metadata"]["byline"] == "Reporter Name"
        assert fmt["metadata"]["wordcount"] == 500
        assert fmt["metadata"]["tags"] == ["world/india"]


# =============================================================================
# GuardianAPI tests
# =============================================================================


class TestGuardianAPI:
    @pytest.mark.asyncio
    async def test_search_country_success(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_api._client.get = AsyncMock(return_value=mock_response)

        articles = await mock_api.search_country(
            country_code="in",
            actor_query='Modi OR Jaishankar',
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        assert len(articles) == 2
        assert articles[0].title == "India and Australia deepen defence ties amid Indo-Pacific tensions"
        assert articles[0].byline == "Helen Davidson in Sydney"
        assert articles[0].wordcount == 1247
        assert "world/india" in articles[0].tags
        assert "world/australia" in articles[0].tags
        assert "Jaishankar" in articles[0].text
        assert "defence cooperation" in articles[0].text

        # Verify API call params
        call_args = mock_api._client.get.call_args
        params = call_args[1]["params"]
        assert params["q"] == "Modi OR Jaishankar"
        assert params["tag"] == "world/india"
        assert params["from-date"] == "2026-03-14"
        assert params["show-fields"] == GuardianAPI.FULL_FIELDS
        assert params["show-tags"] == "keyword"

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_search_country_unsupported(self, mock_api):
        articles = await mock_api.search_country(
            country_code="ee",  # Estonia — not in GUARDIAN_COUNTRIES
            actor_query="test",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )
        assert articles == []
        await mock_api.close()

    @pytest.mark.asyncio
    async def test_search_country_australia_production_office(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": {"results": [], "pages": 1}}
        mock_api._client.get = AsyncMock(return_value=mock_response)

        await mock_api.search_country(
            country_code="au",
            actor_query="Albanese",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        params = mock_api._client.get.call_args[1]["params"]
        assert params["production-office"] == "aus"
        assert params["tag"] == "australia-news/australia-news"

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_search_country_triage_mode(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_api._client.get = AsyncMock(return_value=mock_response)

        articles = await mock_api.search_country(
            country_code="in",
            actor_query="Modi",
            from_date="2026-03-14",
            to_date="2026-03-21",
            full_text=False,
            max_results=10,
        )

        params = mock_api._client.get.call_args[1]["params"]
        assert params["show-fields"] == GuardianAPI.TRIAGE_FIELDS
        assert params["page-size"] == 10

        # In triage mode, text should be empty (no body field)
        # (but our mock returns body, so _parse_result won't strip it)
        assert len(articles) == 2

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_search_query(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_api._client.get = AsyncMock(return_value=mock_response)

        articles = await mock_api.search_query(
            query="NATO AND defence spending",
            from_date="2026-03-14",
            to_date="2026-03-21",
            section="world",
        )

        assert len(articles) == 2
        params = mock_api._client.get.call_args[1]["params"]
        assert params["q"] == "NATO AND defence spending"
        assert params["section"] == "world"

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_get_article(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_SINGLE_ARTICLE
        mock_api._client.get = AsyncMock(return_value=mock_response)

        article = await mock_api.get_article(
            "https://www.theguardian.com/world/2026/mar/18/india-jaishankar-defence-cooperation-australia"
        )

        assert article is not None
        assert article.title == "India and Australia deepen defence ties amid Indo-Pacific tensions"
        assert article.guardian_id == "world/2026/mar/18/india-jaishankar-defence-cooperation-australia"

        # Verify URL construction
        call_args = mock_api._client.get.call_args
        url = call_args[0][0]
        assert url == "https://content.guardianapis.com/world/2026/mar/18/india-jaishankar-defence-cooperation-australia"

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_get_article_not_found(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_api._client.get = AsyncMock(return_value=mock_response)

        article = await mock_api.get_article(
            "https://www.theguardian.com/world/2026/mar/18/nonexistent"
        )

        assert article is None
        await mock_api.close()

    @pytest.mark.asyncio
    async def test_pagination(self, mock_api):
        page1 = {
            "response": {
                "status": "ok",
                "total": 60,
                "currentPage": 1,
                "pages": 2,
                "results": SAMPLE_API_RESPONSE["response"]["results"],
            }
        }
        page2 = {
            "response": {
                "status": "ok",
                "total": 60,
                "currentPage": 2,
                "pages": 2,
                "results": [SAMPLE_API_RESPONSE["response"]["results"][0]],
            }
        }

        mock_api._client.get = AsyncMock(
            side_effect=[
                MagicMock(status_code=200, json=MagicMock(return_value=page1)),
                MagicMock(status_code=200, json=MagicMock(return_value=page2)),
            ]
        )

        articles = await mock_api.search_country(
            country_code="in",
            actor_query="Modi",
            from_date="2026-03-14",
            to_date="2026-03-21",
            max_results=60,
        )

        assert len(articles) == 3
        assert mock_api._client.get.call_count == 2

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_empty_actor_query(self, mock_api):
        """Empty actor_query should omit q parameter (for triage)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": {"results": [], "pages": 1}}
        mock_api._client.get = AsyncMock(return_value=mock_response)

        await mock_api.search_country(
            country_code="gb",
            actor_query="",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        params = mock_api._client.get.call_args[1]["params"]
        assert "q" not in params

        await mock_api.close()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with GuardianAPI(api_key="test-key") as api:
            assert api.api_key == "test-key"

    def test_missing_api_key(self):
        import os
        with patch.dict(os.environ, {}, clear=True):
            env = dict(os.environ)
            env.pop("GUARDIAN_API_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(ValueError, match="GUARDIAN_API_KEY"):
                    GuardianAPI(api_key=None)

    @pytest.mark.asyncio
    async def test_snippet_parsing(self, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_api._client.get = AsyncMock(return_value=mock_response)

        articles = await mock_api.search_country(
            country_code="in",
            actor_query="Jaishankar",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        # standfirst HTML should be stripped
        assert articles[0].snippet == "Jaishankar and Penny Wong sign new security pact"
        # Second article has no standfirst
        assert articles[1].snippet == ""

        await mock_api.close()


# =============================================================================
# GUARDIAN_COUNTRIES tests
# =============================================================================


class TestGuardianCountries:
    def test_expected_countries(self):
        expected = {"gb", "au", "in", "fr", "de", "ua", "jp", "br", "tr", "sa", "kr", "tw", "id", "hu"}
        assert set(GUARDIAN_COUNTRIES.keys()) == expected

    def test_count(self):
        assert len(GUARDIAN_COUNTRIES) == 14

    def test_australia_has_production_office(self):
        assert GUARDIAN_COUNTRIES["au"]["production_office"] == "aus"

    def test_others_no_production_office(self):
        for code, config in GUARDIAN_COUNTRIES.items():
            if code != "au":
                assert config["production_office"] is None, f"{code} should not have production_office"

    def test_all_have_tags(self):
        for code, config in GUARDIAN_COUNTRIES.items():
            assert "tag" in config, f"{code} missing tag"
            assert "/" in config["tag"], f"{code} tag should be in section/tag format"


# =============================================================================
# Integration helper tests
# =============================================================================


class TestIntegrationHelpers:
    @pytest.mark.asyncio
    async def test_guardian_extract_for_country(self):
        api = GuardianAPI(api_key="test-key")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        api._client.get = AsyncMock(return_value=mock_response)

        results = await guardian_extract_for_country(
            api=api,
            country_code="in",
            actor_query="Modi",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        assert len(results) == 2
        assert results[0]["extraction_method"] == "publisher_api_guardian"
        assert results[0]["extraction_failed"] is False
        assert results[0]["domain"] == "theguardian.com"
        assert results[0]["text"]  # Should have full text

        await api.close()

    @pytest.mark.asyncio
    async def test_guardian_triage_unsupported_country(self):
        api = GuardianAPI(api_key="test-key")
        results = await guardian_triage_for_country(
            api=api,
            country_code="ee",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )
        assert results == []
        await api.close()

    @pytest.mark.asyncio
    async def test_guardian_triage_for_country(self):
        api = GuardianAPI(api_key="test-key")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        api._client.get = AsyncMock(return_value=mock_response)

        results = await guardian_triage_for_country(
            api=api,
            country_code="gb",
            from_date="2026-03-14",
            to_date="2026-03-21",
        )

        assert len(results) == 2

        # Verify triage mode params
        params = api._client.get.call_args[1]["params"]
        assert params["show-fields"] == GuardianAPI.TRIAGE_FIELDS
        assert params["page-size"] == 10

        await api.close()
