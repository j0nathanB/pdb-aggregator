"""Tests for the Brave News Search API client and source configuration."""

from __future__ import annotations

import asyncio
import json
import os
import re
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
    _is_allowlisted,
    _is_discarded,
    _is_off_topic_url,
    _load_off_topic_filters,
    _parse_global_allowlist,
    _parse_global_discards,
    _parse_goggle_boosts,
    _parse_goggle_discards,
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
    async def test_discard_filter_drops_matching_results(self, mock_client):
        """Results from $discard domains should be filtered out post-fetch."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Keep this", "url": "https://lemonde.fr/a",
                    "meta_url": {"netloc": "lemonde.fr", "hostname": "www.lemonde.fr"},
                },
                {
                    "title": "Drop this", "url": "https://cnews.fr/a",
                    "meta_url": {"netloc": "cnews.fr", "hostname": "www.cnews.fr"},
                },
                {
                    "title": "Drop subdomain", "url": "https://francais.rt.com/a",
                    "meta_url": {"netloc": "francais.rt.com", "hostname": "francais.rt.com"},
                },
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        mock_client._country_configs = {
            "fr": CountrySearchConfig(
                code="fr",
                use_local_params=False,
                local_params=None,
                sources=[],
                discard_domains=frozenset({"cnews.fr", "rt.com"}),
            )
        }

        response = await mock_client.search_news("Macron", country_code="fr")

        assert response.total_count == 1
        assert response.results[0].source_domain == "lemonde.fr"

        await mock_client.close()

    @pytest.mark.asyncio
    async def test_discard_filter_skipped_without_country_code(self, mock_client):
        """Without country_code, no discard filter is applied."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "x", "url": "https://cnews.fr/a",
                    "meta_url": {"netloc": "cnews.fr", "hostname": "www.cnews.fr"},
                },
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_client._client.get = AsyncMock(return_value=mock_response)

        mock_client._country_configs = {
            "fr": CountrySearchConfig(
                code="fr", use_local_params=False, local_params=None, sources=[],
                discard_domains=frozenset({"cnews.fr"}),
            )
        }

        response = await mock_client.search_news("Macron")  # no country_code

        assert response.total_count == 1
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


# =============================================================================
# Discard enforcement tests
# =============================================================================


class TestDiscardEnforcement:
    def test_parse_goggle_discards(self, tmp_path):
        goggle = tmp_path / "test.goggle"
        goggle.write_text(
            "! header comment\n"
            "$boost=10,site=lemonde.fr\n"
            "$discard,site=cnews.fr\n"
            "$discard, site=valeursactuelles.com\n"  # space after comma
            "$discard,site=francais.rt.com\n"
            "$boost=5,site=mediapart.fr\n"
        )
        discards = _parse_goggle_discards(goggle)
        assert discards == frozenset({"cnews.fr", "valeursactuelles.com", "francais.rt.com"})

    def test_parse_goggle_discards_missing_file(self, tmp_path):
        assert _parse_goggle_discards(tmp_path / "does_not_exist.goggle") == frozenset()

    def test_is_discarded_exact_match(self):
        assert _is_discarded("cnews.fr", frozenset({"cnews.fr"})) is True

    def test_is_discarded_strips_www(self):
        assert _is_discarded("www.cnews.fr", frozenset({"cnews.fr"})) is True

    def test_is_discarded_subdomain(self):
        assert _is_discarded("francais.rt.com", frozenset({"rt.com"})) is True
        assert _is_discarded("de.rt.com", frozenset({"rt.com"})) is True

    def test_is_discarded_case_insensitive(self):
        assert _is_discarded("CNews.FR", frozenset({"cnews.fr"})) is True

    def test_is_discarded_miss(self):
        assert _is_discarded("lemonde.fr", frozenset({"cnews.fr"})) is False

    def test_is_discarded_partial_name_not_subdomain(self):
        """rt.com should NOT match fake-rt.com (not a true subdomain)."""
        assert _is_discarded("fake-rt.com", frozenset({"rt.com"})) is False

    def test_is_discarded_none_safe(self):
        assert _is_discarded(None, frozenset({"cnews.fr"})) is False

    def test_is_discarded_empty_discards(self):
        assert _is_discarded("cnews.fr", frozenset()) is False

    def test_load_brave_sources_populates_discards_from_goggle(self):
        """Real loaded configs carry discard_domains from their goggle files."""
        configs = load_brave_sources()
        fr = configs.get("fr")
        assert fr is not None
        # fr.goggle has these $discard entries today
        assert "cnews.fr" in fr.discard_domains
        assert "valeursactuelles.com" in fr.discard_domains

    def test_parse_global_discards(self, tmp_path):
        path = tmp_path / "_global_discards.txt"
        path.write_text(
            "# Comment at top\n"
            "\n"  # blank line
            "news-pravda.com\n"
            "# inline comment line\n"
            "battinews.com\n"
            "$discard,site=marketbeat.com\n"  # goggle syntax also accepted
            "not_a_domain_no_dot\n"  # rejected — no dot
            "has space.com\n"  # rejected — has space
            "onaquietday.org\n"
        )
        discards = _parse_global_discards(path)
        assert discards == frozenset({
            "news-pravda.com", "battinews.com", "marketbeat.com", "onaquietday.org",
        })

    def test_parse_global_discards_missing_file(self, tmp_path):
        assert _parse_global_discards(tmp_path / "missing.txt") == frozenset()

    def test_load_brave_sources_unions_global_discards(self):
        """Global discard list should merge into every country's discard_domains."""
        configs = load_brave_sources()
        # Global file adds news-pravda.com (parent match) and several spam domains
        for code, cfg in configs.items():
            assert "news-pravda.com" in cfg.discard_domains, (
                f"{code} missing global discard news-pravda.com"
            )
            assert "battinews.com" in cfg.discard_domains, (
                f"{code} missing global discard battinews.com"
            )

    def test_global_discard_matches_all_pravda_subdomains(self):
        """Because _is_discarded matches subdomains, listing `news-pravda.com`
        in the global file blocks every `*.news-pravda.com` variant."""
        discards = frozenset({"news-pravda.com"})
        for subdomain in [
            "deutsch.news-pravda.com",
            "estonia.news-pravda.com",
            "nato.news-pravda.com",
            "ua.news-pravda.com",
            "italy.news-pravda.com",
        ]:
            assert _is_discarded(subdomain, discards) is True, subdomain


# =============================================================================
# Off-topic URL filter tests
# =============================================================================


class TestOffTopicFilter:
    def test_load_off_topic_filters(self, tmp_path):
        path = tmp_path / "off_topic_filters.csv"
        path.write_text(
            "# leading comment\n"
            "# another comment\n"
            "domain,filter_type,filter_pattern,country\n"
            "bbc.com,path,/sport/,Multiple\n"
            "express.co.uk,path,/showbiz/,United Kingdom\n"
            "# inline comment mid-file\n"
            r"example.com,regex,/\d{4}/sports/,Multiple" "\n"
            "blogs.example.com,subdomain,blogs.example.com,Multiple\n"
        )
        rules = _load_off_topic_filters(path)
        assert len(rules) == 4
        assert rules[0]["domain"] == "bbc.com"
        assert rules[0]["type"] == "path"
        assert rules[0]["pattern"] == "/sport/"
        # Regex precompiled
        assert "_compiled" in rules[2]

    def test_load_off_topic_filters_missing_file(self, tmp_path):
        assert _load_off_topic_filters(tmp_path / "missing.csv") == []

    def test_is_off_topic_path_match(self):
        rules = [{"domain": "bbc.com", "type": "path", "pattern": "/sport/"}]
        assert _is_off_topic_url("https://www.bbc.com/sport/football/123", rules) is True

    def test_is_off_topic_path_no_match(self):
        rules = [{"domain": "bbc.com", "type": "path", "pattern": "/sport/"}]
        assert _is_off_topic_url("https://www.bbc.com/news/politics/123", rules) is False

    def test_is_off_topic_domain_scoped(self):
        """A /sport/ rule for bbc.com should not affect guardian.com."""
        rules = [{"domain": "bbc.com", "type": "path", "pattern": "/sport/"}]
        assert _is_off_topic_url("https://www.theguardian.com/sport/x", rules) is False

    def test_is_off_topic_subdomain_match(self):
        rules = [{"domain": "example.com", "type": "subdomain", "pattern": "blogs.example.com"}]
        assert _is_off_topic_url("https://blogs.example.com/foo", rules) is True
        assert _is_off_topic_url("https://example.com/foo", rules) is False

    def test_is_off_topic_regex_match(self):
        compiled = re.compile(r"/\d{4}/sports/")
        rules = [{"domain": "example.com", "type": "regex",
                  "pattern": r"/\d{4}/sports/", "_compiled": compiled}]
        assert _is_off_topic_url("https://example.com/2026/sports/x", rules) is True
        assert _is_off_topic_url("https://example.com/sports/x", rules) is False

    def test_is_off_topic_empty_rules(self):
        assert _is_off_topic_url("https://www.bbc.com/sport/x", []) is False

    def test_real_file_loads_and_covers_known_cases(self):
        """Integration check: the real off_topic_filters.csv loads and
        matches at least the core seed cases from the audit."""
        rules = _load_off_topic_filters()
        assert len(rules) > 0
        assert _is_off_topic_url("https://www.bbc.com/sport/football/123", rules) is True
        assert _is_off_topic_url("https://www.express.co.uk/showbiz/foo", rules) is True
        assert _is_off_topic_url("https://www.dailymail.co.uk/tvshowbiz/foo", rules) is True
        # Legitimate news paths should pass
        assert _is_off_topic_url("https://www.bbc.com/news/politics/x", rules) is False

    @pytest.mark.asyncio
    async def test_search_news_drops_off_topic_urls(self, tmp_path):
        """End-to-end: off-topic filter runs post-fetch in search_news."""
        import src.monitor.collection.brave as brave_mod

        client = BraveNewsClient(api_key="test-key", rate_limit_delay=0)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Sport story", "url": "https://www.bbc.com/sport/football/123",
                    "meta_url": {"netloc": "bbc.com", "hostname": "www.bbc.com"},
                },
                {
                    "title": "Political story", "url": "https://www.bbc.com/news/politics/456",
                    "meta_url": {"netloc": "bbc.com", "hostname": "www.bbc.com"},
                },
            ]
        }
        mock_response.raise_for_status = MagicMock()
        client._client.get = AsyncMock(return_value=mock_response)

        # Inject a minimal rule set so behavior is deterministic regardless
        # of what's in the real off_topic_filters.csv
        original_rules = brave_mod._OFF_TOPIC_RULES
        brave_mod._OFF_TOPIC_RULES = [
            {"domain": "bbc.com", "type": "path", "pattern": "/sport/"},
        ]
        try:
            response = await client.search_news("test")
        finally:
            brave_mod._OFF_TOPIC_RULES = original_rules

        assert response.total_count == 1
        assert response.results[0].url.endswith("/news/politics/456")
        await client.close()


# =============================================================================
# Inverted-allowlist tests
# =============================================================================


class TestAllowlistFilter:
    def test_parse_goggle_boosts(self, tmp_path):
        goggle = tmp_path / "test.goggle"
        goggle.write_text(
            "! header comment\n"
            "$boost=10,site=lemonde.fr\n"
            "$boost=5,site=mediapart.fr\n"
            "$boost=3,site=publicsenat.fr\n"
            "$discard,site=cnews.fr\n"  # discards must NOT be captured here
        )
        boosts = _parse_goggle_boosts(goggle)
        assert boosts == frozenset({"lemonde.fr", "mediapart.fr", "publicsenat.fr"})

    def test_parse_global_allowlist(self, tmp_path):
        path = tmp_path / "_global_allowlist.txt"
        path.write_text(
            "# header comment\n"
            "reuters.com\n"
            "bbc.com\n"
            "$boost=5,site=bloomberg.com\n"  # goggle boost syntax accepted
            "\n"  # blank line
            "# inline comment\n"
            "ft.com\n"
        )
        allowlist = _parse_global_allowlist(path)
        assert allowlist == frozenset({"reuters.com", "bbc.com", "bloomberg.com", "ft.com"})

    def test_is_allowlisted_exact(self):
        assert _is_allowlisted("reuters.com", frozenset({"reuters.com"})) is True

    def test_is_allowlisted_subdomain(self):
        allowlist = frozenset({"bbc.com"})
        assert _is_allowlisted("news.bbc.com", allowlist) is True
        assert _is_allowlisted("www.bbc.com", allowlist) is True

    def test_is_allowlisted_miss(self):
        assert _is_allowlisted("rijnmond.nl", frozenset({"reuters.com"})) is False

    def test_is_allowlisted_none_safe(self):
        assert _is_allowlisted(None, frozenset({"reuters.com"})) is False

    def test_is_allowlisted_empty_set(self):
        assert _is_allowlisted("reuters.com", frozenset()) is False

    def test_load_brave_sources_populates_allowed_domains(self):
        """Real goggle boosts + global allowlist merge into each country's allowed_domains."""
        configs = load_brave_sources()
        fr = configs.get("fr")
        assert fr is not None
        # fr.goggle has lemonde.fr at tier 10
        assert "lemonde.fr" in fr.allowed_domains
        # global allowlist always present
        assert "reuters.com" in fr.allowed_domains
        assert "bbc.com" in fr.allowed_domains

    @pytest.mark.asyncio
    async def test_search_news_drops_off_allowlist_when_flag_on(self, monkeypatch):
        """With MPM_DOMAIN_ALLOWLIST=1, only allowlisted results pass through."""
        import src.monitor.collection.brave as brave_mod
        monkeypatch.setattr(brave_mod, "USE_DOMAIN_ALLOWLIST", True)

        client = BraveNewsClient(api_key="test-key", rate_limit_delay=0)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "Keep — allowlisted", "url": "https://reuters.com/a",
                    "meta_url": {"netloc": "reuters.com", "hostname": "www.reuters.com"},
                },
                {
                    "title": "Drop — keyword collision", "url": "https://rijnmond.nl/foo",
                    "meta_url": {"netloc": "rijnmond.nl", "hostname": "rijnmond.nl"},
                },
                {
                    "title": "Drop — another collision", "url": "https://telegrafi.com/x",
                    "meta_url": {"netloc": "telegrafi.com", "hostname": "telegrafi.com"},
                },
            ]
        }
        mock_response.raise_for_status = MagicMock()
        client._client.get = AsyncMock(return_value=mock_response)

        client._country_configs = {
            "jp": CountrySearchConfig(
                code="jp", use_local_params=False, local_params=None, sources=[],
                allowed_domains=frozenset({"reuters.com", "japantimes.co.jp"}),
            )
        }
        response = await client.search_news("Takaichi", country_code="jp")
        assert response.total_count == 1
        assert response.results[0].url == "https://reuters.com/a"
        await client.close()

    @pytest.mark.asyncio
    async def test_search_news_skips_allowlist_when_flag_off(self, monkeypatch):
        """Default behavior (flag off): allowlist filter doesn't apply."""
        import src.monitor.collection.brave as brave_mod
        monkeypatch.setattr(brave_mod, "USE_DOMAIN_ALLOWLIST", False)

        client = BraveNewsClient(api_key="test-key", rate_limit_delay=0)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "title": "x", "url": "https://rijnmond.nl/foo",
                    "meta_url": {"netloc": "rijnmond.nl", "hostname": "rijnmond.nl"},
                },
            ]
        }
        mock_response.raise_for_status = MagicMock()
        client._client.get = AsyncMock(return_value=mock_response)

        client._country_configs = {
            "jp": CountrySearchConfig(
                code="jp", use_local_params=False, local_params=None, sources=[],
                allowed_domains=frozenset({"reuters.com"}),
            )
        }
        response = await client.search_news("Takaichi", country_code="jp")
        assert response.total_count == 1  # not filtered
        await client.close()
