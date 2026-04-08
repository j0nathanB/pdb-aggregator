"""Tests for the Brave News Search API client and source configuration."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.monitor.collection.brave import (
    BRAVE_NEWS_URL,
    BraveNewsClient,
    BraveNewsResult,
    BraveSearchResponse,
    CountrySearchConfig,
    IndexedSource,
    load_brave_sources,
)


# =============================================================================
# Fixtures
# =============================================================================

SAMPLE_API_RESPONSE = {
    "results": [
        {
            "title": "Sheinbaum anuncia reforma energética",
            "url": "https://www.eluniversal.com.mx/nacion/sheinbaum-reforma-energetica",
            "description": "La presidenta Claudia Sheinbaum presentó hoy...",
            "age": "hace 2 días",
            "page_age": "2026-03-18T14:30:00",
            "meta_url": {
                "scheme": "https",
                "netloc": "eluniversal.com.mx",
                "hostname": "www.eluniversal.com.mx",
            },
            "extra_snippets": [
                "El plan incluye inversión de 50 mil millones...",
                "PEMEX y CFE tendrán roles centrales...",
            ],
        },
        {
            "title": "Mexico energy reform draws mixed reactions",
            "url": "https://www.reuters.com/business/energy/mexico-energy-reform-2026-03-18",
            "description": "Reuters reports on the new Mexican energy policy...",
            "age": "1 day ago",
            "page_age": "2026-03-19T09:00:00",
            "meta_url": {
                "scheme": "https",
                "netloc": "reuters.com",
                "hostname": "www.reuters.com",
            },
            "extra_snippets": [],
        },
    ]
}


@pytest.fixture
def sample_country_config():
    return CountrySearchConfig(
        code="mx",
        use_local_params=True,
        local_params={
            "search_lang": "es",
            "ui_lang": "es-MX",
            "country": "MX",
        },
        sources=[
            IndexedSource(name="El Universal", domain="eluniversal.com.mx", rss_full_text=False),
            IndexedSource(name="Reforma", domain="reforma.com", rss_full_text=False),
            IndexedSource(name="El Financiero", domain="elfinanciero.com.mx", rss_full_text=True),
        ],
    )


@pytest.fixture
def sample_en_country_config():
    return CountrySearchConfig(
        code="au",
        use_local_params=False,
        local_params=None,
        sources=[
            IndexedSource(name="ABC News", domain="abc.net.au", rss_full_text=False),
        ],
    )


# =============================================================================
# BraveNewsResult tests
# =============================================================================


class TestBraveNewsResult:
    def test_from_api_full(self):
        item = SAMPLE_API_RESPONSE["results"][0]
        result = BraveNewsResult.from_api(item)

        assert result.title == "Sheinbaum anuncia reforma energética"
        assert result.url == "https://www.eluniversal.com.mx/nacion/sheinbaum-reforma-energetica"
        assert result.description.startswith("La presidenta")
        assert result.age == "hace 2 días"
        assert result.page_age == "2026-03-18T14:30:00"
        assert result.source_domain == "eluniversal.com.mx"
        assert len(result.extra_snippets) == 2

    def test_from_api_minimal(self):
        item = {"title": "Test", "url": "https://example.com"}
        result = BraveNewsResult.from_api(item)

        assert result.title == "Test"
        assert result.url == "https://example.com"
        assert result.description == ""
        assert result.age is None
        assert result.source_domain is None
        assert result.extra_snippets == []

    def test_from_api_no_meta_url(self):
        item = {
            "title": "Test",
            "url": "https://example.com",
            "description": "Desc",
        }
        result = BraveNewsResult.from_api(item)
        assert result.source_domain is None


# =============================================================================
# CountrySearchConfig tests
# =============================================================================


class TestCountrySearchConfig:
    def test_local_params_country(self, sample_country_config):
        params = sample_country_config.search_params
        assert params == {
            "search_lang": "es",
            "ui_lang": "es-MX",
            "country": "MX",
        }

    def test_en_default_country(self, sample_en_country_config):
        params = sample_en_country_config.search_params
        assert params == {}

    def test_goggle_path_exists_for_mx(self, sample_country_config):
        """mx.goggle exists in assets/country_goggles/."""
        assert sample_country_config.goggle_path() is not None

    def test_goggle_url_exists_for_mx(self, sample_country_config):
        """goggle_url returns a URL for mx since the file exists."""
        url = sample_country_config.goggle_url()
        assert url is not None
        assert url.endswith("/mx.goggle")

    def test_goggle_path_not_exists(self):
        """goggle_path returns None for a country with no goggle file."""
        cc = CountrySearchConfig(code="zz", use_local_params=False, local_params=None, sources=[])
        assert cc.goggle_path() is None

    def test_goggle_url_not_exists(self):
        """goggle_url returns None for a country with no goggle file."""
        cc = CountrySearchConfig(code="zz", use_local_params=False, local_params=None, sources=[])
        assert cc.goggle_url() is None

    def test_goggle_path_exists(self, sample_country_config, tmp_path):
        """goggle_path returns path when file exists."""
        import src.monitor.collection.brave as brave_mod
        original = brave_mod.GOGGLES_DIR
        brave_mod.GOGGLES_DIR = tmp_path
        try:
            (tmp_path / f"{sample_country_config.code}.goggle").write_text("! test")
            assert sample_country_config.goggle_path() is not None
        finally:
            brave_mod.GOGGLES_DIR = original

    def test_goggle_url_exists(self, sample_country_config, tmp_path):
        """goggle_url returns GitHub raw URL when file exists locally."""
        import src.monitor.collection.brave as brave_mod
        original = brave_mod.GOGGLES_DIR
        brave_mod.GOGGLES_DIR = tmp_path
        try:
            (tmp_path / f"{sample_country_config.code}.goggle").write_text("! test")
            url = sample_country_config.goggle_url()
            assert url is not None
            assert url.endswith(f"/{sample_country_config.code}.goggle")
            assert "raw.githubusercontent.com" in url
        finally:
            brave_mod.GOGGLES_DIR = original


# =============================================================================
# load_brave_sources tests
# =============================================================================


class TestLoadBraveSources:
    def test_loads_all_countries(self):
        configs = load_brave_sources()
        assert len(configs) == 28

    def test_mexico_uses_local(self):
        configs = load_brave_sources()
        mx = configs["mx"]
        assert mx.use_local_params is True
        assert mx.local_params["search_lang"] == "es"
        assert mx.local_params["country"] == "MX"

    def test_australia_uses_en(self):
        configs = load_brave_sources()
        au = configs["au"]
        assert au.use_local_params is False

    def test_local_countries(self):
        """Countries with local non-EN premium > 0 should use local params."""
        configs = load_brave_sources()
        expected_local = {"fr", "de", "pl", "fi", "mx", "br", "jp", "tw", "it", "es", "tr", "ca"}
        actual_local = {code for code, c in configs.items() if c.use_local_params}
        assert actual_local == expected_local

    def test_no_empty_source_lists(self):
        configs = load_brave_sources()
        for code, cfg in configs.items():
            assert len(cfg.sources) > 0, f"{code} has no indexed sources"

    def test_source_domains_are_valid(self):
        configs = load_brave_sources()
        for code, cfg in configs.items():
            for src in cfg.sources:
                assert "." in src.domain, f"Invalid domain for {src.name}: {src.domain}"


# =============================================================================
# BraveNewsClient tests
# =============================================================================


class TestBraveNewsClient:
    @pytest.fixture
    def mock_client(self):
        """Create a BraveNewsClient with mocked HTTP client."""
        client = BraveNewsClient(api_key="test-key", rate_limit_delay=0)
        return client

    @pytest.mark.asyncio
    async def test_search_news_basic(self, mock_client):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_response.raise_for_status = MagicMock()

        mock_client._client.get = AsyncMock(return_value=mock_response)

        response = await mock_client.search_news("Sheinbaum SEDENA")

        assert response.query == "Sheinbaum SEDENA"
        assert response.total_count == 2
        assert response.results[0].title == "Sheinbaum anuncia reforma energética"
        assert response.results[1].source_domain == "reuters.com"

        # Verify API call params
        call_args = mock_client._client.get.call_args
        assert call_args[0][0] == BRAVE_NEWS_URL
        params = call_args[1]["params"]
        assert params["q"] == "Sheinbaum SEDENA"
        assert params["count"] == 50
        assert params["freshness"] == "pw"
        assert params["extra_snippets"] is True

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_with_country_code_local(self, mock_client):
        """Country with local params should include them in the request."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        # Inject a local-params country config
        mock_client._country_configs = {
            "mx": CountrySearchConfig(
                code="mx",
                use_local_params=True,
                local_params={"search_lang": "es", "ui_lang": "es-MX", "country": "MX"},
                sources=[],
            )
        }

        await mock_client.search_news("Sheinbaum", country_code="mx")

        params = mock_client._client.get.call_args[1]["params"]
        assert params["search_lang"] == "es"
        assert params["ui_lang"] == "es-MX"
        assert params["country"] == "MX"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_with_country_code_en(self, mock_client):
        """Country without local params should not add lang params."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        mock_client._country_configs = {
            "au": CountrySearchConfig(
                code="au",
                use_local_params=False,
                local_params=None,
                sources=[],
            )
        }

        await mock_client.search_news("Albanese", country_code="au")

        params = mock_client._client.get.call_args[1]["params"]
        assert "search_lang" not in params
        assert "ui_lang" not in params
        assert "country" not in params

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_explicit_overrides_beat_country_config(self, mock_client):
        """Explicit params should override country config."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        mock_client._country_configs = {
            "mx": CountrySearchConfig(
                code="mx",
                use_local_params=True,
                local_params={"search_lang": "es", "ui_lang": "es-MX", "country": "MX"},
                sources=[],
            )
        }

        await mock_client.search_news(
            "Sheinbaum",
            country_code="mx",
            search_lang="en",
            country="US",
        )

        params = mock_client._client.get.call_args[1]["params"]
        assert params["search_lang"] == "en"
        assert params["country"] == "US"
        # ui_lang still comes from country config since not explicitly overridden
        assert params["ui_lang"] == "es-MX"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_custom_freshness_date_range(self, mock_client):
        """Support YYYY-MM-DDtoYYYY-MM-DD freshness for backfilling."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        await mock_client.search_news(
            "test query",
            freshness="2026-03-01to2026-03-14",
        )

        params = mock_client._client.get.call_args[1]["params"]
        assert params["freshness"] == "2026-03-01to2026-03-14"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_goggles_param(self, mock_client):
        """Goggles URL should be passed through."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        goggle_url = "https://raw.githubusercontent.com/user/repo/main/mx.goggle"
        await mock_client.search_news("test", goggles=goggle_url)

        params = mock_client._client.get.call_args[1]["params"]
        assert params["goggles"] == goggle_url

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_country_sources(self, mock_client):
        """search_country_sources should run one query per term."""
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_API_RESPONSE
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        mock_client._country_configs = {
            "mx": CountrySearchConfig(
                code="mx",
                use_local_params=True,
                local_params={"search_lang": "es", "country": "MX"},
                sources=[],
            )
        }

        responses = await mock_client.search_country_sources(
            "mx",
            ["Sheinbaum SEDENA", "nearshoring inversión"],
        )

        assert len(responses) == 2
        assert mock_client._client.get.call_count == 2

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_country_sources_auto_goggle(self, mock_client, tmp_path):
        """search_country_sources auto-resolves goggle URL when file exists."""
        import src.monitor.collection.brave as brave_mod
        original = brave_mod.GOGGLES_DIR
        brave_mod.GOGGLES_DIR = tmp_path
        try:
            (tmp_path / "mx.goggle").write_text("! test goggle")

            mock_response = MagicMock()
            mock_response.json.return_value = SAMPLE_API_RESPONSE
            mock_response.raise_for_status = MagicMock()
            mock_client._client.get = AsyncMock(return_value=mock_response)

            mock_client._country_configs = {
                "mx": CountrySearchConfig(
                    code="mx",
                    use_local_params=True,
                    local_params={"search_lang": "es", "country": "MX"},
                    sources=[],
                )
            }

            await mock_client.search_country_sources("mx", ["test query"])

            params = mock_client._client.get.call_args[1]["params"]
            assert "goggles" in params
            assert params["goggles"].endswith("/mx.goggle")
        finally:
            brave_mod.GOGGLES_DIR = original

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_search_unknown_country(self, mock_client):
        """Unknown country code should return empty list."""
        mock_client._country_configs = {}
        responses = await mock_client.search_country_sources("zz", ["test"])
        assert responses == []

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_get_indexed_sources(self, mock_client):
        mock_client._country_configs = {
            "mx": CountrySearchConfig(
                code="mx",
                use_local_params=True,
                local_params={},
                sources=[
                    IndexedSource(name="El Universal", domain="eluniversal.com.mx"),
                    IndexedSource(name="Reforma", domain="reforma.com"),
                ],
            )
        }

        sources = mock_client.get_indexed_sources("mx")
        assert len(sources) == 2
        assert sources[0].name == "El Universal"

        assert mock_client.get_indexed_sources("zz") == []

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_rate_limiting(self, mock_client):
        """Verify rate limiting introduces delay between requests."""
        mock_client._rate_limit_delay = 0.1  # short delay for testing

        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        import time

        start = time.monotonic()
        await mock_client.search_news("query1")
        await mock_client.search_news("query2")
        elapsed = time.monotonic() - start

        # Should take at least the rate limit delay
        assert elapsed >= 0.1

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_http_error_propagates(self, mock_client):
        """HTTP errors should raise."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "429 Too Many Requests",
            request=MagicMock(),
            response=MagicMock(status_code=429),
        )
        mock_client._client.get = AsyncMock(return_value=mock_response)

        with pytest.raises(httpx.HTTPStatusError):
            await mock_client.search_news("test")

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager protocol."""
        async with BraveNewsClient(api_key="test-key", rate_limit_delay=0) as client:
            assert client.api_key == "test-key"

    def test_missing_api_key_raises(self):
        with patch.dict(os.environ, {}, clear=True):
            # Remove BRAVE_API_KEY from env
            env = dict(os.environ)
            env.pop("BRAVE_API_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(ValueError, match="BRAVE_API_KEY"):
                    BraveNewsClient(api_key=None)


# =============================================================================
# Integration-style tests (load real config, mock HTTP)
# =============================================================================


class TestIntegration:
    def test_all_local_countries_have_params(self):
        """Every country with use_local_params=True must have local_params."""
        configs = load_brave_sources()
        for code, cfg in configs.items():
            if cfg.use_local_params:
                assert cfg.local_params is not None, f"{code} uses local but has no params"
                assert "search_lang" in cfg.local_params, f"{code} missing search_lang"
                assert "country" in cfg.local_params, f"{code} missing country"

    def test_source_count_matches_report(self):
        """Total indexed sources should match generation report."""
        configs = load_brave_sources()
        total = sum(len(c.sources) for c in configs.values())
        # 390 sources as reported by generate_brave_config.py
        assert total == 390
