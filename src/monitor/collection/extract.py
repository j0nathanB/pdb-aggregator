"""
Article extraction with domain-based routing and fallback chains.

Dispatches URLs to the optimal extraction method based on empirical testing
(extraction_routing.yaml). Supports parallel pool dispatch with per-method
concurrency limits and automatic fallback on primary failure.

Extraction tiers:
    Tier 0: Claude web_fetch (195 domains, ~51%)
    Tier 1: curl + trafilatura (145 domains, ~38%)
    Tier 2: Diffbot Article API (12 domains, ~3%)
    Tier 3: Playwright (18 domains, ~4%)
    Tier 4: Publisher APIs (Guardian, etc.)
    Fallback: snippet_only (6 unretrievable domains)
"""

from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx
import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

ROUTING_PATH = PROJECT_ROOT / "assets" / "country_configs" / "extraction_routing.yaml"


# =============================================================================
# Data classes
# =============================================================================


@dataclass
class ExtractionResult:
    """Result of extracting an article's full text."""

    url: str
    method: str  # claude, curl, diffbot, playwright, publisher_api, snippet_only
    success: bool
    title: str = ""
    text: str = ""
    author: str = ""
    published_date: str = ""
    error: str = ""
    latency_ms: int = 0

    @property
    def word_count(self) -> int:
        return len(self.text.split()) if self.text else 0


@dataclass
class DomainRoute:
    """Routing config for a single domain."""

    domain: str
    primary: str
    confidence: str | None
    fallbacks: list[str]
    publisher_api: str | None = None


@dataclass
class RoutingConfig:
    """Full extraction routing configuration."""

    routes: dict[str, DomainRoute]
    default_fallback_chain: list[str]
    concurrency: dict[str, int]
    rate_limits: dict[str, float | int]

    def route_for_url(self, url: str) -> DomainRoute:
        """Look up routing for a URL by its domain."""
        domain = urlparse(url).netloc.lower()
        # Strip www. prefix for lookup
        if domain.startswith("www."):
            domain = domain[4:]

        if domain in self.routes:
            return self.routes[domain]

        # Unknown domain — use default fallback chain
        return DomainRoute(
            domain=domain,
            primary=self.default_fallback_chain[0],
            confidence=None,
            fallbacks=self.default_fallback_chain[1:],
        )


def load_routing_config() -> RoutingConfig:
    """Load extraction routing from YAML."""
    if not ROUTING_PATH.exists():
        raise FileNotFoundError(
            f"Extraction routing config not found: {ROUTING_PATH}\n"
            "Generate it with: python dev/source_maps/media/generate_extraction_routing.py"
        )

    with open(ROUTING_PATH) as f:
        data = yaml.safe_load(f)

    routes = {}
    for domain, route_data in data.get("routes", {}).items():
        routes[domain] = DomainRoute(
            domain=domain,
            primary=route_data["primary"],
            confidence=route_data.get("confidence"),
            fallbacks=route_data.get("fallbacks", []),
            publisher_api=route_data.get("publisher_api"),
        )

    return RoutingConfig(
        routes=routes,
        default_fallback_chain=data.get("default_fallback_chain", []),
        concurrency=data.get("concurrency", {}),
        rate_limits=data.get("rate_limits", {}),
    )


# =============================================================================
# Base extractor
# =============================================================================


class Extractor(ABC):
    """Base class for article extractors."""

    method_name: str = "base"

    @abstractmethod
    async def extract(self, url: str) -> ExtractionResult:
        """Extract article text from a URL."""
        ...


# =============================================================================
# Tier 1: curl + trafilatura
# =============================================================================


class CurlTrafilaturaExtractor(Extractor):
    """Extract articles using curl fetch + trafilatura HTML parsing.

    Fast and reliable for most standard news sites. Runs curl as a subprocess
    to handle redirects/cookies, then uses trafilatura for content extraction.
    """

    method_name = "curl"

    def __init__(self, timeout: int = 30):
        self._timeout = timeout

    async def extract(self, url: str) -> ExtractionResult:
        start = time.monotonic()
        try:
            html = await self._fetch_html(url)
            if not html:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="Empty response from curl",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            import trafilatura

            result = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=False,
                favor_precision=True,
                output_format="txt",
            )

            if not result:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="trafilatura returned no content",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            metadata = trafilatura.extract(
                html,
                include_comments=False,
                output_format="xmltei",
            )
            title = ""
            author = ""
            date = ""
            if metadata:
                import re
                title_m = re.search(r"<title[^>]*>(.*?)</title>", metadata, re.DOTALL)
                if title_m:
                    title = title_m.group(1).strip()
                author_m = re.search(r'<author[^>]*>(.*?)</author>', metadata, re.DOTALL)
                if author_m:
                    author = author_m.group(1).strip()
                date_m = re.search(r'<date[^>]*>(.*?)</date>', metadata, re.DOTALL)
                if date_m:
                    date = date_m.group(1).strip()

            return ExtractionResult(
                url=url, method=self.method_name, success=True,
                title=title, text=result, author=author,
                published_date=date,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except Exception as e:
            return ExtractionResult(
                url=url, method=self.method_name, success=False,
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    async def _fetch_html(self, url: str) -> str:
        """Fetch HTML using curl subprocess."""
        proc = await asyncio.create_subprocess_exec(
            "curl", "-sL", "-m", str(self._timeout),
            "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "--compressed",
            url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            logger.debug("curl failed for %s: %s", url, stderr.decode()[:200])
            return ""
        return stdout.decode("utf-8", errors="replace")


# =============================================================================
# Tier 2: Diffbot Article API
# =============================================================================


class DiffbotExtractor(Extractor):
    """Extract articles using the Diffbot Article API.

    Best for JavaScript-heavy sites and paywalled content that Diffbot
    has cached. Requires DIFFBOT_API_KEY in environment.
    """

    method_name = "diffbot"
    API_URL = "https://api.diffbot.com/v3/article"

    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self._api_key = api_key or os.getenv("DIFFBOT_API_KEY")
        if not self._api_key:
            raise ValueError("DIFFBOT_API_KEY not found in environment or constructor")
        self._client = httpx.AsyncClient(timeout=timeout)

    async def extract(self, url: str) -> ExtractionResult:
        start = time.monotonic()
        try:
            response = await self._client.get(
                self.API_URL,
                params={"token": self._api_key, "url": url},
            )
            response.raise_for_status()
            data = response.json()

            objects = data.get("objects", [])
            if not objects:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="Diffbot returned no objects",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            article = objects[0]
            return ExtractionResult(
                url=url, method=self.method_name, success=True,
                title=article.get("title", ""),
                text=article.get("text", ""),
                author=article.get("author", ""),
                published_date=article.get("date", ""),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except Exception as e:
            return ExtractionResult(
                url=url, method=self.method_name, success=False,
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    async def close(self) -> None:
        await self._client.aclose()


# =============================================================================
# Tier 3: Playwright
# =============================================================================


class PlaywrightExtractor(Extractor):
    """Extract articles using Playwright headless browser + trafilatura.

    For sites that require JavaScript rendering. Slower but handles
    SPAs, lazy-loaded content, and complex paywalls.
    """

    method_name = "playwright"

    def __init__(self, timeout: int = 30000):
        self._timeout = timeout  # Playwright uses milliseconds

    async def extract(self, url: str) -> ExtractionResult:
        start = time.monotonic()
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=self._timeout, wait_until="domcontentloaded")

                # Wait a bit for JS rendering
                await page.wait_for_timeout(2000)
                html = await page.content()
                await browser.close()

            if not html:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="Playwright returned empty page",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            import trafilatura

            text = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=False,
                favor_precision=True,
                output_format="txt",
            )

            if not text:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="trafilatura returned no content from rendered page",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            return ExtractionResult(
                url=url, method=self.method_name, success=True,
                text=text,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except Exception as e:
            return ExtractionResult(
                url=url, method=self.method_name, success=False,
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )


# =============================================================================
# Tier 0: Claude web_fetch
# =============================================================================


class ClaudeExtractor(Extractor):
    """Extract articles using Claude's web_fetch tool.

    Primary method for 51% of domains. Uses the Anthropic API with
    the web_fetch tool to retrieve and parse article content.
    """

    method_name = "claude"

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
    ):
        self._api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self._api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment or constructor")
        self._model = model
        self._client = httpx.AsyncClient(timeout=60.0)

    async def extract(self, url: str) -> ExtractionResult:
        start = time.monotonic()
        try:
            response = await self._client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                    "anthropic-beta": "web-fetch-2025-04-15",
                },
                json={
                    "model": self._model,
                    "max_tokens": 4096,
                    "tools": [{"type": "web_fetch", "name": "web_fetch"}],
                    "messages": [
                        {
                            "role": "user",
                            "content": (
                                f"Fetch this URL and extract the article: {url}\n\n"
                                "Return ONLY a JSON object with these fields:\n"
                                '- "title": article headline\n'
                                '- "author": author name(s) or ""\n'
                                '- "published_date": publication date or ""\n'
                                '- "text": full article body text\n\n'
                                "Do not summarize. Return the complete article text."
                            ),
                        }
                    ],
                },
            )
            response.raise_for_status()
            data = response.json()

            # Extract text from Claude's response
            content_blocks = data.get("content", [])
            text_parts = []
            for block in content_blocks:
                if block.get("type") == "text":
                    text_parts.append(block["text"])

            full_text = "\n".join(text_parts)

            # Try to parse as JSON
            import json
            try:
                parsed = json.loads(full_text)
                return ExtractionResult(
                    url=url, method=self.method_name, success=True,
                    title=parsed.get("title", ""),
                    text=parsed.get("text", ""),
                    author=parsed.get("author", ""),
                    published_date=parsed.get("published_date", ""),
                    latency_ms=int((time.monotonic() - start) * 1000),
                )
            except json.JSONDecodeError:
                # Claude returned plain text — use as-is
                if len(full_text) > 100:
                    return ExtractionResult(
                        url=url, method=self.method_name, success=True,
                        text=full_text,
                        latency_ms=int((time.monotonic() - start) * 1000),
                    )
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error=f"Claude returned insufficient content: {full_text[:200]}",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

        except Exception as e:
            return ExtractionResult(
                url=url, method=self.method_name, success=False,
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    async def close(self) -> None:
        await self._client.aclose()


# =============================================================================
# Tier 4: Publisher APIs
# =============================================================================


class PublisherAPIExtractor(ABC):
    """Base class for publisher-specific API extractors.

    Wraps a Publisher API client to conform to the extraction pipeline's
    interface (url in → ExtractionResult out). The full Publisher API
    clients live in their own modules (e.g., guardian.py) and provide
    richer interfaces for search, triage, etc.
    """

    method_name = "publisher_api"
    publisher_name: str = "base"

    @abstractmethod
    async def extract(self, url: str) -> ExtractionResult:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...


class GuardianExtractor(PublisherAPIExtractor):
    """Extraction adapter for the Guardian Open Platform API.

    Uses the full GuardianAPI client from guardian.py to fetch articles
    by URL. For search/triage, use GuardianAPI directly.
    """

    publisher_name = "guardian"

    def __init__(self, api_key: str | None = None):
        from src.monitor.collection.guardian import GuardianAPI as _GuardianAPI

        self._api = _GuardianAPI(api_key=api_key)

    async def extract(self, url: str) -> ExtractionResult:
        start = time.monotonic()
        try:
            article = await self._api.get_article(url)

            if not article or not article.text:
                return ExtractionResult(
                    url=url, method=self.method_name, success=False,
                    error="Guardian API returned no content",
                    latency_ms=int((time.monotonic() - start) * 1000),
                )

            return ExtractionResult(
                url=url, method=self.method_name, success=True,
                title=article.title,
                text=article.text,
                author=article.byline or "",
                published_date=article.publication_date,
                latency_ms=int((time.monotonic() - start) * 1000),
            )

        except Exception as e:
            return ExtractionResult(
                url=url, method=self.method_name, success=False,
                error=str(e),
                latency_ms=int((time.monotonic() - start) * 1000),
            )

    async def close(self) -> None:
        await self._api.close()


# Publisher API extractor registry
PUBLISHER_APIS: dict[str, type[PublisherAPIExtractor]] = {
    "guardian": GuardianExtractor,
}


# =============================================================================
# Extraction orchestrator
# =============================================================================


class ExtractionOrchestrator:
    """Orchestrates parallel article extraction with routing and fallbacks.

    Dispatches URLs to extraction methods based on domain routing table,
    manages per-method concurrency limits, and handles fallback chains
    when primary extraction fails.

    Usage:
        async with ExtractionOrchestrator() as orchestrator:
            results = await orchestrator.extract_batch(urls)
    """

    def __init__(
        self,
        routing_config: RoutingConfig | None = None,
        claude_extractor: ClaudeExtractor | None = None,
        diffbot_extractor: DiffbotExtractor | None = None,
    ):
        self._config = routing_config or load_routing_config()
        self._extractors: dict[str, Extractor] = {}
        self._publisher_apis: dict[str, PublisherAPIExtractor] = {}
        self._semaphores: dict[str, asyncio.Semaphore] = {}
        self._domain_locks: dict[str, asyncio.Lock] = {}
        self._domain_last_request: dict[str, float] = {}
        self._owned_resources: list = []

        # Per-domain rate limit from config
        self._per_domain_delay = self._config.rate_limits.get("per_domain_delay_seconds", 1.0)
        self._max_urls_per_domain = int(self._config.rate_limits.get("max_urls_per_domain", 5))

        # Initialize extractors
        self._extractors["curl"] = CurlTrafilaturaExtractor()
        self._extractors["playwright"] = PlaywrightExtractor()

        # Claude web_fetch extractor disabled — curl/trafilatura covers all domains
        # and has higher success rates (81% vs 51%).
        if claude_extractor:
            self._extractors["claude"] = claude_extractor

        if diffbot_extractor:
            self._extractors["diffbot"] = diffbot_extractor
        else:
            try:
                ext = DiffbotExtractor()
                self._extractors["diffbot"] = ext
                self._owned_resources.append(ext)
            except ValueError:
                logger.warning("DIFFBOT_API_KEY not set — Diffbot extractor unavailable")

        # Initialize semaphores from concurrency config
        for method, limit in self._config.concurrency.items():
            self._semaphores[method] = asyncio.Semaphore(limit)

    async def close(self) -> None:
        for resource in self._owned_resources:
            if hasattr(resource, "close"):
                await resource.close()
        for api in self._publisher_apis.values():
            if hasattr(api, "close"):
                await api.close()

    async def __aenter__(self) -> ExtractionOrchestrator:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    def _get_publisher_api(self, api_name: str) -> PublisherAPIExtractor | None:
        """Get or create a publisher API extractor instance."""
        if api_name in self._publisher_apis:
            return self._publisher_apis[api_name]

        api_class = PUBLISHER_APIS.get(api_name)
        if not api_class:
            logger.warning("Unknown publisher API: %s", api_name)
            return None

        try:
            api = api_class()
            self._publisher_apis[api_name] = api
            return api
        except ValueError as e:
            logger.warning("Could not initialize %s API: %s", api_name, e)
            return None

    async def _rate_limit_domain(self, domain: str) -> None:
        """Enforce per-domain rate limiting."""
        if domain not in self._domain_locks:
            self._domain_locks[domain] = asyncio.Lock()

        async with self._domain_locks[domain]:
            last = self._domain_last_request.get(domain, 0)
            now = time.monotonic()
            elapsed = now - last
            if elapsed < self._per_domain_delay:
                await asyncio.sleep(self._per_domain_delay - elapsed)
            self._domain_last_request[domain] = time.monotonic()

    async def _extract_with_method(self, url: str, method: str, route: DomainRoute) -> ExtractionResult:
        """Extract using a specific method with concurrency control."""
        # Handle publisher APIs
        if method == "publisher_api" and route.publisher_api:
            api = self._get_publisher_api(route.publisher_api)
            if api:
                sem = self._semaphores.get("publisher_api", asyncio.Semaphore(5))
                async with sem:
                    await self._rate_limit_domain(route.domain)
                    result = await api.extract(url)
                    result.url = url
                    return result
            return ExtractionResult(
                url=url, method=method, success=False,
                error=f"Publisher API '{route.publisher_api}' not available",
            )

        # Handle snippet_only
        if method == "snippet_only":
            return ExtractionResult(
                url=url, method=method, success=True,
                text="",  # No text — signal to use search snippet
            )

        # Regular extractor
        extractor = self._extractors.get(method)
        if not extractor:
            return ExtractionResult(
                url=url, method=method, success=False,
                error=f"Extractor '{method}' not available",
            )

        sem = self._semaphores.get(method, asyncio.Semaphore(10))
        async with sem:
            await self._rate_limit_domain(route.domain)
            result = await extractor.extract(url)
            result.url = url  # Ensure URL is always set
            return result

    async def _extract_primary(self, url: str) -> ExtractionResult:
        """Extract a single URL using only its primary method (no fallbacks)."""
        route = self._config.route_for_url(url)
        return await self._extract_with_method(url, route.primary, route)

    async def extract_url(self, url: str) -> ExtractionResult:
        """Extract a single URL using its routed method with fallbacks.

        For single-URL extraction outside of batch context. Uses sequential
        fallback (not two-phase). For batch extraction, use extract_batch().
        """
        route = self._config.route_for_url(url)

        # Try primary method
        result = await self._extract_with_method(url, route.primary, route)
        if result.success:
            return result

        logger.debug(
            "Primary extraction failed for %s (%s): %s",
            url, route.primary, result.error,
        )

        # Try fallbacks
        for fallback_method in route.fallbacks:
            result = await self._extract_with_method(url, fallback_method, route)
            if result.success:
                logger.debug(
                    "Fallback %s succeeded for %s", fallback_method, url,
                )
                return result
            logger.debug(
                "Fallback %s failed for %s: %s",
                fallback_method, url, result.error,
            )

        # All methods failed — return snippet_only
        return ExtractionResult(
            url=url, method="snippet_only", success=True,
            text="",
        )

    async def extract_batch(
        self,
        urls: list[str],
        max_per_domain: int | None = None,
    ) -> list[ExtractionResult]:
        """Extract a batch of URLs with two-phase parallel dispatch.

        Phase 1: Dispatch all URLs to primary extraction pools in parallel.
                 All pools (Claude, curl, Diffbot, Playwright, Publisher API)
                 run simultaneously, with per-method concurrency limits.

        Phase 2: Collect primary failures, dispatch to fallback methods
                 as a single batch pass. Fallback chain per the routing table.

        Any remaining failures after Phase 2 → snippet_only with confidence
        cap at 2.

        Args:
            urls: List of article URLs to extract.
            max_per_domain: Max URLs per domain (overrides config default).

        Returns:
            List of ExtractionResult in the same order as input URLs.
        """
        limit = max_per_domain or self._max_urls_per_domain

        # Deduplicate and apply per-domain limits
        domain_counts: dict[str, int] = {}
        filtered_urls: list[str] = []
        skipped_indices: set[int] = set()

        for i, url in enumerate(urls):
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            count = domain_counts.get(domain, 0)
            if count >= limit:
                skipped_indices.add(i)
                continue
            domain_counts[domain] = count + 1
            filtered_urls.append(url)

        # ── Phase 1: Primary dispatch ──────────────────────────────────
        # All URLs dispatched to their primary method concurrently.
        # Semaphores enforce per-method concurrency limits.
        primary_tasks = [self._extract_primary(url) for url in filtered_urls]
        primary_results = await asyncio.gather(*primary_tasks, return_exceptions=True)

        result_map: dict[str, ExtractionResult] = {}
        failed_urls: list[str] = []

        for url, result in zip(filtered_urls, primary_results):
            if isinstance(result, Exception):
                result_map[url] = ExtractionResult(
                    url=url, method="error", success=False,
                    error=str(result),
                )
                failed_urls.append(url)
            elif result.success:
                result_map[url] = result
            else:
                result_map[url] = result
                failed_urls.append(url)
                logger.debug(
                    "Primary extraction failed for %s (%s): %s",
                    url, result.method, result.error,
                )

        # ── Phase 2: Fallback batch ────────────────────────────────────
        # Collect all primary failures. For each, try fallback methods
        # from its routing table in order. All fallback attempts for all
        # URLs run as a single concurrent pass per fallback level.
        if failed_urls:
            # Group by fallback level — process first fallback for all URLs,
            # then second fallback for remaining failures, etc.
            remaining = list(failed_urls)
            max_fallback_depth = max(
                (len(self._config.route_for_url(url).fallbacks) for url in remaining),
                default=0,
            )

            for depth in range(max_fallback_depth):
                if not remaining:
                    break

                # Build tasks for this fallback level
                fallback_tasks = []
                fallback_urls = []
                for url in remaining:
                    route = self._config.route_for_url(url)
                    if depth < len(route.fallbacks):
                        method = route.fallbacks[depth]
                        fallback_tasks.append(
                            self._extract_with_method(url, method, route)
                        )
                        fallback_urls.append(url)

                if not fallback_tasks:
                    break

                fallback_results = await asyncio.gather(
                    *fallback_tasks, return_exceptions=True
                )

                still_failing = []
                for url, result in zip(fallback_urls, fallback_results):
                    if isinstance(result, Exception):
                        logger.debug("Fallback exception for %s: %s", url, result)
                        still_failing.append(url)
                    elif result.success:
                        result_map[url] = result
                        logger.debug(
                            "Fallback %s succeeded for %s", result.method, url,
                        )
                    else:
                        logger.debug(
                            "Fallback %s failed for %s: %s",
                            result.method, url, result.error,
                        )
                        still_failing.append(url)

                # URLs not attempted at this depth stay in remaining
                not_attempted = [u for u in remaining if u not in fallback_urls]
                remaining = still_failing + not_attempted

            # Any still-remaining failures → snippet_only
            for url in remaining:
                if not result_map.get(url, ExtractionResult(url="", method="", success=False)).success:
                    result_map[url] = ExtractionResult(
                        url=url, method="snippet_only", success=True,
                        text="",
                    )

        # ── Build ordered result list ──────────────────────────────────
        ordered = []
        for i, url in enumerate(urls):
            if i in skipped_indices:
                ordered.append(ExtractionResult(
                    url=url, method="skipped", success=False,
                    error=f"Per-domain limit ({limit}) exceeded",
                ))
            elif url in result_map:
                ordered.append(result_map[url])
            else:
                ordered.append(ExtractionResult(
                    url=url, method="error", success=False,
                    error="URL not found in results",
                ))

        return ordered
