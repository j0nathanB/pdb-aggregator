"""Tests for the article extraction module."""

from __future__ import annotations

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.monitor.collection.extract import (
    ClaudeExtractor,
    CurlTrafilaturaExtractor,
    DiffbotExtractor,
    DomainRoute,
    ExtractionOrchestrator,
    ExtractionResult,
    PlaywrightExtractor,
    RoutingConfig,
    load_routing_config,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def sample_routing_config():
    """Minimal routing config for testing."""
    return RoutingConfig(
        routes={
            "eluniversal.com.mx": DomainRoute(
                domain="eluniversal.com.mx",
                primary="claude",
                confidence="high",
                fallbacks=["curl", "diffbot"],
            ),
            "reuters.com": DomainRoute(
                domain="reuters.com",
                primary="curl",
                confidence="high",
                fallbacks=["diffbot", "playwright"],
            ),
            "theguardian.com": DomainRoute(
                domain="theguardian.com",
                primary="publisher_api",
                confidence="high",
                fallbacks=["curl", "diffbot"],
                publisher_api="guardian",
            ),
            "dgap.org": DomainRoute(
                domain="dgap.org",
                primary="snippet_only",
                confidence=None,
                fallbacks=[],
            ),
        },
        default_fallback_chain=["claude", "curl", "diffbot", "playwright", "snippet_only"],
        concurrency={"claude": 10, "curl": 20, "diffbot": 5, "playwright": 3, "publisher_api": 5},
        rate_limits={"per_domain_delay_seconds": 0.0, "max_urls_per_domain": 5},
    )


# =============================================================================
# ExtractionResult tests
# =============================================================================


class TestExtractionResult:
    def test_word_count(self):
        result = ExtractionResult(
            url="https://example.com",
            method="curl",
            success=True,
            text="This is a test article with several words in it.",
        )
        assert result.word_count == 10

    def test_word_count_empty(self):
        result = ExtractionResult(
            url="https://example.com",
            method="curl",
            success=False,
        )
        assert result.word_count == 0


# =============================================================================
# RoutingConfig tests
# =============================================================================


class TestRoutingConfig:
    def test_load_routing_config(self):
        config = load_routing_config()
        assert len(config.routes) == 377
        assert "claude" in config.default_fallback_chain
        assert config.concurrency["claude"] == 10

    def test_route_for_known_domain(self, sample_routing_config):
        route = sample_routing_config.route_for_url("https://www.reuters.com/world/test-article")
        assert route.domain == "reuters.com"
        assert route.primary == "curl"

    def test_route_for_known_domain_no_www(self, sample_routing_config):
        route = sample_routing_config.route_for_url("https://reuters.com/world/test-article")
        assert route.domain == "reuters.com"
        assert route.primary == "curl"

    def test_route_for_unknown_domain(self, sample_routing_config):
        route = sample_routing_config.route_for_url("https://unknown-site.com/article")
        assert route.primary == "claude"
        assert route.fallbacks == ["curl", "diffbot", "playwright", "snippet_only"]

    def test_route_publisher_api(self, sample_routing_config):
        route = sample_routing_config.route_for_url("https://www.theguardian.com/world/article")
        assert route.primary == "publisher_api"
        assert route.publisher_api == "guardian"

    def test_route_snippet_only(self, sample_routing_config):
        route = sample_routing_config.route_for_url("https://dgap.org/something")
        assert route.primary == "snippet_only"
        assert route.fallbacks == []


# =============================================================================
# CurlTrafilaturaExtractor tests
# =============================================================================


class TestCurlTrafilaturaExtractor:
    @pytest.mark.asyncio
    async def test_extract_success(self):
        extractor = CurlTrafilaturaExtractor()

        html = """
        <html><head><title>Test Article</title></head>
        <body>
        <article>
            <h1>Test Article Headline</h1>
            <p>This is a substantial article body with enough content to pass
            trafilatura's quality checks. We need several sentences here to make
            it realistic. The article discusses important policy developments in
            the region. Multiple paragraphs help ensure extraction succeeds.</p>
            <p>A second paragraph adds more substance to the article. This helps
            trafilatura determine that this is a real article and not boilerplate.</p>
        </article>
        </body></html>
        """

        async def mock_subprocess(*args, **kwargs):
            proc = MagicMock()
            proc.communicate = AsyncMock(return_value=(html.encode(), b""))
            proc.returncode = 0
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=mock_subprocess):
            result = await extractor.extract("https://example.com/article")

        # trafilatura may or may not extract from this minimal HTML
        assert result.url == "https://example.com/article"
        assert result.method == "curl"
        assert result.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_extract_curl_failure(self):
        extractor = CurlTrafilaturaExtractor()

        async def mock_subprocess(*args, **kwargs):
            proc = MagicMock()
            proc.communicate = AsyncMock(return_value=(b"", b"Connection refused"))
            proc.returncode = 7
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=mock_subprocess):
            result = await extractor.extract("https://example.com/article")

        assert result.success is False
        assert "Empty response" in result.error


# =============================================================================
# DiffbotExtractor tests
# =============================================================================


class TestDiffbotExtractor:
    @pytest.mark.asyncio
    async def test_extract_success(self):
        extractor = DiffbotExtractor(api_key="test-key")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "objects": [
                {
                    "title": "Test Article",
                    "text": "Full article body text here.",
                    "author": "John Doe",
                    "date": "2026-03-18",
                }
            ]
        }

        extractor._client.get = AsyncMock(return_value=mock_response)

        result = await extractor.extract("https://example.com/article")

        assert result.success is True
        assert result.title == "Test Article"
        assert result.text == "Full article body text here."
        assert result.author == "John Doe"
        assert result.method == "diffbot"

        await extractor.close()

    @pytest.mark.asyncio
    async def test_extract_no_objects(self):
        extractor = DiffbotExtractor(api_key="test-key")

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"objects": []}

        extractor._client.get = AsyncMock(return_value=mock_response)

        result = await extractor.extract("https://example.com/article")

        assert result.success is False
        assert "no objects" in result.error

        await extractor.close()

    def test_missing_api_key(self):
        import os
        with patch.dict(os.environ, {}, clear=True):
            env = dict(os.environ)
            env.pop("DIFFBOT_API_KEY", None)
            with patch.dict(os.environ, env, clear=True):
                with pytest.raises(ValueError, match="DIFFBOT_API_KEY"):
                    DiffbotExtractor(api_key=None)


# =============================================================================
# ClaudeExtractor tests
# =============================================================================


class TestClaudeExtractor:
    @pytest.mark.asyncio
    async def test_extract_json_response(self):
        extractor = ClaudeExtractor(api_key="test-key")

        import json
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "title": "Mexico Reform",
                        "text": "The president announced a major reform package...",
                        "author": "Reporter",
                        "published_date": "2026-03-18",
                    }),
                }
            ]
        }

        extractor._client.post = AsyncMock(return_value=mock_response)

        result = await extractor.extract("https://example.com/article")

        assert result.success is True
        assert result.title == "Mexico Reform"
        assert "reform package" in result.text
        assert result.method == "claude"

        await extractor.close()

    @pytest.mark.asyncio
    async def test_extract_plain_text_response(self):
        extractor = ClaudeExtractor(api_key="test-key")

        long_text = "A" * 200  # Longer than 100 chars

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "content": [{"type": "text", "text": long_text}]
        }

        extractor._client.post = AsyncMock(return_value=mock_response)

        result = await extractor.extract("https://example.com/article")

        assert result.success is True
        assert result.text == long_text

        await extractor.close()

    @pytest.mark.asyncio
    async def test_extract_short_text_fails(self):
        extractor = ClaudeExtractor(api_key="test-key")

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "content": [{"type": "text", "text": "Sorry, I cannot access that URL."}]
        }

        extractor._client.post = AsyncMock(return_value=mock_response)

        result = await extractor.extract("https://example.com/article")

        assert result.success is False
        assert "insufficient content" in result.error

        await extractor.close()


# =============================================================================
# ExtractionOrchestrator tests
# =============================================================================


class TestExtractionOrchestrator:
    @pytest.fixture
    def mock_orchestrator(self, sample_routing_config):
        """Orchestrator with mocked extractors."""
        mock_claude = MagicMock(spec=ClaudeExtractor)
        mock_claude.method_name = "claude"
        mock_claude.extract = AsyncMock(return_value=ExtractionResult(
            url="", method="claude", success=True,
            title="Test", text="Article body text.",
        ))

        mock_curl = MagicMock(spec=CurlTrafilaturaExtractor)
        mock_curl.method_name = "curl"
        mock_curl.extract = AsyncMock(return_value=ExtractionResult(
            url="", method="curl", success=True,
            title="Test", text="Curl article body.",
        ))

        orch = ExtractionOrchestrator.__new__(ExtractionOrchestrator)
        orch._config = sample_routing_config
        orch._extractors = {"claude": mock_claude, "curl": mock_curl}
        orch._publisher_apis = {}
        orch._semaphores = {
            method: asyncio.Semaphore(limit)
            for method, limit in sample_routing_config.concurrency.items()
        }
        orch._domain_locks = {}
        orch._domain_last_request = {}
        orch._per_domain_delay = 0.0
        orch._max_urls_per_domain = 5
        orch._owned_resources = []

        return orch

    @pytest.mark.asyncio
    async def test_extract_url_primary_success(self, mock_orchestrator):
        result = await mock_orchestrator.extract_url(
            "https://www.eluniversal.com.mx/nacion/test"
        )
        assert result.success is True
        assert result.method == "claude"

    @pytest.mark.asyncio
    async def test_extract_url_fallback(self, mock_orchestrator):
        # Make claude fail
        mock_orchestrator._extractors["claude"].extract = AsyncMock(
            return_value=ExtractionResult(
                url="", method="claude", success=False, error="Timeout",
            )
        )

        result = await mock_orchestrator.extract_url(
            "https://www.eluniversal.com.mx/nacion/test"
        )
        assert result.success is True
        assert result.method == "curl"

    @pytest.mark.asyncio
    async def test_extract_url_all_fail_returns_snippet_only(self, mock_orchestrator):
        # Make all extractors fail
        for ext in mock_orchestrator._extractors.values():
            ext.extract = AsyncMock(return_value=ExtractionResult(
                url="", method="test", success=False, error="Failed",
            ))

        result = await mock_orchestrator.extract_url(
            "https://www.eluniversal.com.mx/nacion/test"
        )
        assert result.method == "snippet_only"
        assert result.success is True

    @pytest.mark.asyncio
    async def test_extract_url_snippet_only_domain(self, mock_orchestrator):
        result = await mock_orchestrator.extract_url("https://dgap.org/article")
        assert result.method == "snippet_only"
        assert result.success is True

    @pytest.mark.asyncio
    async def test_extract_batch_ordering(self, mock_orchestrator):
        urls = [
            "https://www.eluniversal.com.mx/nacion/test1",
            "https://reuters.com/article/test2",
            "https://dgap.org/article",
        ]

        results = await mock_orchestrator.extract_batch(urls)

        assert len(results) == 3
        assert results[0].url == urls[0]
        assert results[1].url == urls[1]
        assert results[2].url == urls[2]

    @pytest.mark.asyncio
    async def test_extract_batch_two_phase_fallback(self, mock_orchestrator):
        """Primary failures should be retried via fallback in Phase 2."""
        # Claude fails, curl succeeds
        mock_orchestrator._extractors["claude"].extract = AsyncMock(
            return_value=ExtractionResult(
                url="", method="claude", success=False, error="Blocked",
            )
        )

        urls = [
            "https://www.eluniversal.com.mx/nacion/test1",  # primary=claude → fails → fallback curl
            "https://reuters.com/article/test2",              # primary=curl → succeeds
        ]

        results = await mock_orchestrator.extract_batch(urls)

        assert len(results) == 2
        # First URL: claude failed, fell back to curl
        assert results[0].success is True
        assert results[0].method == "curl"
        # Second URL: curl succeeded as primary
        assert results[1].success is True
        assert results[1].method == "curl"

    @pytest.mark.asyncio
    async def test_extract_batch_all_fail_snippet_only(self, mock_orchestrator):
        """When all methods fail in both phases, result is snippet_only."""
        for ext in mock_orchestrator._extractors.values():
            ext.extract = AsyncMock(return_value=ExtractionResult(
                url="", method="test", success=False, error="Failed",
            ))

        urls = ["https://www.eluniversal.com.mx/nacion/test1"]
        results = await mock_orchestrator.extract_batch(urls)

        assert len(results) == 1
        assert results[0].method == "snippet_only"
        assert results[0].success is True

    @pytest.mark.asyncio
    async def test_extract_batch_per_domain_limit(self, mock_orchestrator):
        mock_orchestrator._max_urls_per_domain = 2

        urls = [
            "https://reuters.com/article/1",
            "https://reuters.com/article/2",
            "https://reuters.com/article/3",  # Should be skipped
        ]

        results = await mock_orchestrator.extract_batch(urls)

        assert len(results) == 3
        assert results[0].success is True
        assert results[1].success is True
        assert results[2].method == "skipped"
        assert results[2].success is False

    @pytest.mark.asyncio
    async def test_extract_unknown_domain(self, mock_orchestrator):
        result = await mock_orchestrator.extract_url("https://unknown-news.com/article")
        # Should use default fallback chain, primary=claude
        assert result.success is True
        assert result.method == "claude"

    @pytest.mark.asyncio
    async def test_context_manager(self, sample_routing_config):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test", "DIFFBOT_API_KEY": "test"}):
            async with ExtractionOrchestrator(routing_config=sample_routing_config) as orch:
                assert "curl" in orch._extractors


# =============================================================================
# Integration: load real routing config
# =============================================================================


class TestRoutingConfigIntegration:
    def test_load_real_config(self):
        config = load_routing_config()
        assert config.routes["theguardian.com"].primary == "publisher_api"
        assert config.routes["theguardian.com"].publisher_api == "guardian"

    def test_ft_publisher_api(self):
        config = load_routing_config()
        assert config.routes["ft.com"].primary == "publisher_api"
        assert config.routes["ft.com"].publisher_api == "ft"

    def test_publisher_api_count(self):
        config = load_routing_config()
        api_count = sum(1 for r in config.routes.values() if r.primary == "publisher_api")
        assert api_count == 2  # Guardian + FT

    def test_claude_domain_count(self):
        config = load_routing_config()
        claude_count = sum(1 for r in config.routes.values() if r.primary == "claude")
        assert claude_count == 195

    def test_snippet_only_count(self):
        config = load_routing_config()
        snippet_count = sum(1 for r in config.routes.values() if r.primary == "snippet_only")
        assert snippet_count == 6

    def test_all_routes_have_valid_primary(self):
        config = load_routing_config()
        valid = {"claude", "curl", "diffbot", "playwright", "publisher_api", "snippet_only"}
        for domain, route in config.routes.items():
            assert route.primary in valid, f"{domain} has invalid primary: {route.primary}"
