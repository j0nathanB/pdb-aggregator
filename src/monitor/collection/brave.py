"""
Brave News Search API client for Layer 1 news discovery.

Handles per-country search param selection (EN vs local), rate limiting,
and source configuration loading from brave_sources.yaml.

API reference: https://api-dashboard.search.brave.com/api-reference/news/news_search/get
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"
BRAVE_SOURCES_PATH = PROJECT_ROOT / "assets" / "country_configs" / "brave_sources.yaml"
GOGGLES_DIR = PROJECT_ROOT / "assets" / "country_goggles"

# Goggle files must be served via URL for the Brave API.
# Default: GitHub raw content URL for this repo.
GOGGLES_BASE_URL = os.environ.get(
    "MPM_GOGGLES_BASE_URL",
    "https://raw.githubusercontent.com/j0nathanB/pdb-aggregator/main/assets/country_goggles",
)


# =============================================================================
# Data classes
# =============================================================================


@dataclass
class BraveNewsResult:
    """A single news result from Brave Search."""

    title: str
    url: str
    description: str
    age: str | None = None
    page_age: str | None = None
    source_domain: str | None = None
    extra_snippets: list[str] = field(default_factory=list)

    @classmethod
    def from_api(cls, item: dict) -> BraveNewsResult:
        meta = item.get("meta_url", {})
        return cls(
            title=item.get("title", ""),
            url=item.get("url", ""),
            description=item.get("description", ""),
            age=item.get("age"),
            page_age=item.get("page_age"),
            source_domain=meta.get("netloc") or meta.get("hostname"),
            extra_snippets=item.get("extra_snippets", []),
        )


@dataclass
class BraveSearchResponse:
    """Response from a Brave News Search query."""

    query: str
    results: list[BraveNewsResult]
    total_count: int


@dataclass
class IndexedSource:
    """A news source confirmed indexed by Brave."""

    name: str
    domain: str
    rss_full_text: bool = False


@dataclass
class CountrySearchConfig:
    """Per-country Brave search configuration."""

    code: str
    use_local_params: bool
    local_params: dict[str, str] | None
    sources: list[IndexedSource]

    @property
    def search_params(self) -> dict[str, str]:
        """Return the search params to use for this country."""
        if self.use_local_params and self.local_params:
            return dict(self.local_params)
        return {}

    def goggle_path(self) -> Path | None:
        """Return path to this country's goggle file, if it exists."""
        path = GOGGLES_DIR / f"{self.code}.goggle"
        return path if path.exists() else None

    def goggle_url(self) -> str | None:
        """Return the URL to this country's goggle file, if it exists locally."""
        if self.goggle_path() is None:
            return None
        return f"{GOGGLES_BASE_URL}/{self.code}.goggle"


# =============================================================================
# Source config loader
# =============================================================================


def load_brave_sources() -> dict[str, CountrySearchConfig]:
    """Load per-country Brave source config from brave_sources.yaml."""
    if not BRAVE_SOURCES_PATH.exists():
        raise FileNotFoundError(
            f"Brave sources config not found: {BRAVE_SOURCES_PATH}\n"
            "Generate it with: python dev/source_maps/media/generate_brave_config.py"
        )

    with open(BRAVE_SOURCES_PATH) as f:
        data = yaml.safe_load(f)

    configs = {}
    for code, entry in data.get("countries", {}).items():
        sources = [
            IndexedSource(
                name=s["name"],
                domain=s["domain"],
                rss_full_text=s.get("rss_full_text", False),
            )
            for s in entry.get("sources", [])
        ]
        configs[code] = CountrySearchConfig(
            code=code,
            use_local_params=entry.get("use_local_params", False),
            local_params=entry.get("local_params"),
            sources=sources,
        )

    return configs


# =============================================================================
# Brave News API client
# =============================================================================


class BraveNewsClient:
    """Async client for the Brave News Search API.

    Handles rate limiting, per-country param selection, and response parsing.

    Usage:
        async with BraveNewsClient() as client:
            response = await client.search_news("Sheinbaum SEDENA", country_code="mx")
    """

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit_delay: float = 1.1,
    ):
        self.api_key = api_key or os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not found in environment or constructor")
        self._rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self._client = httpx.AsyncClient(
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key,
            },
            timeout=30.0,
        )
        self._country_configs: dict[str, CountrySearchConfig] | None = None

    @property
    def country_configs(self) -> dict[str, CountrySearchConfig]:
        if self._country_configs is None:
            self._country_configs = load_brave_sources()
        return self._country_configs

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> BraveNewsClient:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def _rate_limit(self) -> None:
        """Enforce minimum delay between API requests."""
        async with self._lock:
            loop = asyncio.get_event_loop()
            now = loop.time()
            elapsed = now - self._last_request_time
            if elapsed < self._rate_limit_delay:
                await asyncio.sleep(self._rate_limit_delay - elapsed)
            self._last_request_time = loop.time()

    async def search_news(
        self,
        query: str,
        *,
        country_code: str | None = None,
        count: int = 50,
        offset: int = 0,
        freshness: str = "pw",
        extra_snippets: bool = True,
        goggles: str | None = None,
        search_lang: str | None = None,
        ui_lang: str | None = None,
        country: str | None = None,
    ) -> BraveSearchResponse:
        """Search the Brave News API.

        Args:
            query: Search query (max 400 chars, 50 words).
            country_code: ISO 2-letter code. If provided, applies that country's
                configured search params (EN or local) automatically.
            count: Results per request (1-50, default 50).
            offset: Pagination offset (0-9, default 0).
            freshness: Age filter. "pw" (past week), "pd" (past day),
                "pm" (past month), or "YYYY-MM-DDtoYYYY-MM-DD" for date range.
            extra_snippets: Request up to 5 additional excerpts per result.
            goggles: URL to a Goggle file for custom ranking.
            search_lang: Override search language (normally set via country_code).
            ui_lang: Override UI language (normally set via country_code).
            country: Override country param (normally set via country_code).

        Returns:
            BraveSearchResponse with parsed results.
        """
        await self._rate_limit()

        params: dict[str, str | int | bool] = {
            "q": query,
            "count": count,
            "offset": offset,
            "freshness": freshness,
            "extra_snippets": extra_snippets,
        }

        # Apply per-country params if country_code provided
        if country_code:
            cc = self.country_configs.get(country_code)
            if cc:
                params.update(cc.search_params)

        # Explicit overrides take precedence
        if search_lang is not None:
            params["search_lang"] = search_lang
        if ui_lang is not None:
            params["ui_lang"] = ui_lang
        if country is not None:
            params["country"] = country
        if goggles is not None:
            params["goggles"] = goggles

        logger.debug("Brave News API request: q=%r params=%s", query, params)

        response = await self._client.get(BRAVE_NEWS_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = [
            BraveNewsResult.from_api(item) for item in data.get("results", [])
        ]

        logger.debug("Brave News: q=%r → %d results", query, len(results))

        return BraveSearchResponse(
            query=query,
            results=results,
            total_count=len(results),
        )

    async def search_country_sources(
        self,
        country_code: str,
        query_terms: list[str],
        *,
        freshness: str = "pw",
        goggles: str | None = None,
    ) -> list[BraveSearchResponse]:
        """Run multiple queries for a country using its configured params.

        Combines each query term with the country's search params and goggle.
        Used during deep-dive collection (Step 2 in the pipeline).

        Args:
            country_code: ISO 2-letter code.
            query_terms: List of search queries (actor names, vocab terms, etc.).
            freshness: Age filter.
            goggles: URL to goggle file. If None, checks for local goggle.

        Returns:
            List of BraveSearchResponse, one per query term.
        """
        cc = self.country_configs.get(country_code)
        if not cc:
            logger.warning("No Brave config for country %s", country_code)
            return []

        # Use country goggle if available and no explicit goggle provided
        if goggles is None:
            goggles = cc.goggle_url()
            if goggles:
                logger.debug("Using goggle for %s: %s", country_code, goggles)

        logger.info("Brave: searching %s with %d query terms", country_code, len(query_terms))
        responses = []
        for term in query_terms:
            resp = await self.search_news(
                term,
                country_code=country_code,
                freshness=freshness,
                goggles=goggles,
            )
            responses.append(resp)

        total = sum(r.total_count for r in responses)
        logger.info("Brave: %s → %d queries, %d total results", country_code, len(responses), total)
        return responses

    def get_indexed_sources(self, country_code: str) -> list[IndexedSource]:
        """Return the list of Brave-indexed sources for a country."""
        cc = self.country_configs.get(country_code)
        return cc.sources if cc else []

    def get_country_config(self, country_code: str) -> CountrySearchConfig | None:
        """Return the search config for a country."""
        return self.country_configs.get(country_code)
