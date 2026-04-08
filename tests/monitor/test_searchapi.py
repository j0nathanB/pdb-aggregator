"""Tests for the SearchAPI client (Layer 2 government source discovery)."""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitor.collection.searchapi import (
    SEARCHAPI_URL,
    SearchAPIClient,
    SearchAPIResponse,
    SearchResult,
)


# =============================================================================
# Fixtures
# =============================================================================


SAMPLE_API_RESPONSE = {
    "search_information": {
        "total_results": 15,
    },
    "organic_results": [
        {
            "position": 1,
            "title": "Comunicado No. 089 - SRE",
            "link": "https://sre.gob.mx/comunicados/089-2026",
            "snippet": "La Secretaría de Relaciones Exteriores informa sobre la firma del acuerdo bilateral...",
            "domain": "sre.gob.mx",
            "date": "2026-03-12",
        },
        {
            "position": 2,
            "title": "Acuerdo de cooperación México-Canadá",
            "link": "https://sre.gob.mx/tratados/cooperacion-canada",
            "snippet": "Texto del acuerdo de cooperación en seguridad hemisférica...",
            "domain": "sre.gob.mx",
        },
    ],
}


@pytest.fixture
def mock_client():
    client = SearchAPIClient(api_key="test-key", rate_limit_delay=0)
    return client


# =============================================================================
# SearchResult tests
# =============================================================================


class TestSearchResult:
    def test_creation(self):
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="A test result",
            domain="example.com",
            position=1,
        )
        assert result.title == "Test"
        assert result.domain == "example.com"

    def test_optional_date(self):
        result = SearchResult(
            title="Test",
            url="https://example.com",
            snippet="",
            domain="example.com",
        )
        assert result.date is None


# =============================================================================
# SearchAPIClient tests
# =============================================================================


class TestSearchAPIClient:
    @pytest.mark.asyncio
    async def test_search_basic(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_client._client.get = AsyncMock(return_value=mock_response)

        response = await mock_client.search("site:sre.gob.mx comunicado")

        assert response.query == "site:sre.gob.mx comunicado"
        assert response.total_results == 15
        assert len(response.results) == 2
        assert response.results[0].title == "Comunicado No. 089 - SRE"
        assert response.results[0].domain == "sre.gob.mx"
        assert response.results[0].date == "2026-03-12"

        # Verify API call
        call_args = mock_client._client.get.call_args
        assert call_args[0][0] == SEARCHAPI_URL
        params = call_args[1]["params"]
        assert params["q"] == "site:sre.gob.mx comunicado"
        assert params["engine"] == "google"
        assert "time_period" not in params  # no longer uses time_period

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_with_date_range(self, mock_client):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"organic_results": []}
        mock_client._client.get = AsyncMock(return_value=mock_response)

        await mock_client.search(
            "test query",
            time_period_min="03/15/2026",
            time_period_max="03/22/2026",
        )

        params = mock_client._client.get.call_args[1]["params"]
        assert params["time_period_min"] == "03/15/2026"
        assert params["time_period_max"] == "03/22/2026"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_no_date_range(self, mock_client):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"organic_results": []}
        mock_client._client.get = AsyncMock(return_value=mock_response)

        await mock_client.search("test query")

        params = mock_client._client.get.call_args[1]["params"]
        assert "time_period_min" not in params
        assert "time_period_max" not in params

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_government(self, mock_client):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_client._client.get = AsyncMock(return_value=mock_response)

        response = await mock_client.search_government(
            domain="sre.gob.mx",
            query="comunicado",
        )

        params = mock_client._client.get.call_args[1]["params"]
        assert params["q"] == "site:sre.gob.mx comunicado"
        assert len(response.results) == 2

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_government_no_query(self, mock_client):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"organic_results": []}
        mock_client._client.get = AsyncMock(return_value=mock_response)

        await mock_client.search_government(domain="gob.mx")

        params = mock_client._client.get.call_args[1]["params"]
        assert params["q"] == "site:gob.mx"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_country_government(self, mock_client):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_client._client.get = AsyncMock(return_value=mock_response)

        domains = [
            {"domain": "sre.gob.mx", "queries": ["comunicado", "tratado"]},
            {"domain": "gob.mx/sedena", "queries": ["adquisición"]},
        ]

        responses = await mock_client.search_country_government(domains)

        assert len(responses) == 3  # 2 queries + 1 query
        assert mock_client._client.get.call_count == 3

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_country_government_no_queries(self, mock_client):
        """Domain with no queries should do one search with site: only."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"organic_results": []}
        mock_client._client.get = AsyncMock(return_value=mock_response)

        domains = [{"domain": "gob.mx"}]
        responses = await mock_client.search_country_government(domains)

        assert len(responses) == 1
        params = mock_client._client.get.call_args[1]["params"]
        assert params["q"] == "site:gob.mx"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_domain_extraction_fallback(self, mock_client):
        """If domain field is missing, extract from URL."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "organic_results": [
                {
                    "title": "Test",
                    "link": "https://www.gob.mx/sedena/acciones/123",
                    "snippet": "Test snippet",
                    "position": 1,
                },
            ],
        }
        mock_client._client.get = AsyncMock(return_value=mock_response)

        response = await mock_client.search("test")
        assert response.results[0].domain == "www.gob.mx"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_http_error_propagates(self, mock_client):
        import httpx
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "429",
            request=MagicMock(),
            response=MagicMock(status_code=429),
        )
        mock_client._client.get = AsyncMock(return_value=mock_response)

        with pytest.raises(httpx.HTTPStatusError):
            await mock_client.search("test")

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with SearchAPIClient(api_key="test-key", rate_limit_delay=0) as client:
            assert client.api_key == "test-key"

    def test_missing_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            env = dict(os.environ)
            env.pop("SEARCHAPI_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(ValueError, match="SEARCHAPI_KEY"):
                    SearchAPIClient(api_key=None)

    @pytest.mark.asyncio
    async def test_rate_limiting(self, mock_client):
        mock_client._rate_limit_delay = 0.1

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"organic_results": []}
        mock_client._client.get = AsyncMock(return_value=mock_response)

        import time
        start = time.monotonic()
        await mock_client.search("q1")
        await mock_client.search("q2")
        elapsed = time.monotonic() - start

        assert elapsed >= 0.1
        await mock_client.close()
