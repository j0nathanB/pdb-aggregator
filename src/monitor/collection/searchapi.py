"""
SearchAPI client for Layer 2 government source discovery.

Performs Google searches scoped to government domains via site: operators.
Used exclusively for government monitoring — news discovery uses Brave (Layer 1).

API reference: https://www.searchapi.io/docs/google
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

SEARCHAPI_URL = "https://www.searchapi.io/api/v1/search"


@dataclass
class SearchResult:
    """A single result from a SearchAPI query."""

    title: str
    url: str
    snippet: str
    domain: str
    position: int = 0
    date: str | None = None


@dataclass
class SearchAPIResponse:
    """Response from a SearchAPI query."""

    query: str
    results: list[SearchResult]
    total_results: int = 0


class SearchAPIClient:
    """Async client for SearchAPI (Google results).

    Used for Layer 2 government source discovery. Queries are scoped
    to government domains using site: operators.

    Usage:
        async with SearchAPIClient() as client:
            response = await client.search_government(
                domain="sre.gob.mx",
                query="comunicado",
                time_period_min="03/15/2026",
                time_period_max="03/22/2026",
            )
    """

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit_delay: float = 1.0,
    ):
        self.api_key = api_key or os.getenv("SEARCHAPI_KEY")
        if not self.api_key:
            raise ValueError("SEARCHAPI_KEY not found in environment or constructor")
        self._rate_limit_delay = rate_limit_delay
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> SearchAPIClient:
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

    async def search(
        self,
        query: str,
        *,
        num: int = 10,
        time_period_min: str | None = None,
        time_period_max: str | None = None,
    ) -> SearchAPIResponse:
        """Execute a search query via SearchAPI.

        Args:
            query: Search query (may include site: operators).
            num: Number of results (1-100, default 10).
            time_period_min: Start date in MM/DD/YYYY format.
            time_period_max: End date in MM/DD/YYYY format.

        Returns:
            SearchAPIResponse with parsed results.
        """
        await self._rate_limit()

        params: dict[str, str | int] = {
            "engine": "google",
            "api_key": self.api_key,
            "q": query,
            "num": num,
        }

        if time_period_min:
            params["time_period_min"] = time_period_min
        if time_period_max:
            params["time_period_max"] = time_period_max

        logger.debug("SearchAPI request: q=%r, num=%s, range=%s to %s", query, num, time_period_min, time_period_max)

        response = await self._client.get(SEARCHAPI_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("organic_results", []):
            domain = item.get("domain", "")
            if not domain:
                # Extract domain from link
                from urllib.parse import urlparse
                parsed = urlparse(item.get("link", ""))
                domain = parsed.netloc

            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                domain=domain,
                position=item.get("position", 0),
                date=item.get("date"),
            ))

        resp = SearchAPIResponse(
            query=query,
            results=results,
            total_results=data.get("search_information", {}).get("total_results", len(results)),
        )
        logger.debug("SearchAPI results: q=%r → %d results", query, len(results))
        return resp

    async def search_government(
        self,
        domain: str,
        query: str = "",
        *,
        time_period_min: str | None = None,
        time_period_max: str | None = None,
        num: int = 10,
    ) -> SearchAPIResponse:
        """Search a government domain using site: scoping.

        Args:
            domain: Government domain to scope search (e.g., "sre.gob.mx").
            query: Additional search terms (e.g., "comunicado").
            time_period_min: Start date in MM/DD/YYYY format.
            time_period_max: End date in MM/DD/YYYY format.
            num: Number of results.

        Returns:
            SearchAPIResponse with results from the specified domain.
        """
        full_query = f"site:{domain}"
        if query:
            full_query = f"site:{domain} {query}"

        return await self.search(
            full_query,
            num=num,
            time_period_min=time_period_min,
            time_period_max=time_period_max,
        )

    async def search_country_government(
        self,
        domains: list[dict],
        *,
        time_period_min: str | None = None,
        time_period_max: str | None = None,
    ) -> list[SearchAPIResponse]:
        """Search multiple government domains for a country.

        Args:
            domains: List of dicts with "domain" and optional "queries" keys.
                Each dict represents a government institution to monitor.
                Example: [
                    {"domain": "sre.gob.mx", "queries": ["comunicado", "tratado"]},
                    {"domain": "gob.mx/sedena", "queries": ["adquisición"]},
                ]
            time_period_min: Start date in MM/DD/YYYY format.
            time_period_max: End date in MM/DD/YYYY format.

        Returns:
            List of SearchAPIResponse, one per domain+query combination.
        """
        logger.info("SearchAPI: searching %d government domains", len(domains))
        responses = []
        for domain_config in domains:
            domain = domain_config["domain"]
            queries = domain_config.get("queries", [""])

            for query in queries:
                resp = await self.search_government(
                    domain=domain,
                    query=query,
                    time_period_min=time_period_min,
                    time_period_max=time_period_max,
                )
                responses.append(resp)
                logger.debug(
                    "SearchAPI gov: domain=%s query=%r → %d results",
                    domain, query, len(resp.results),
                )

        total = sum(len(r.results) for r in responses)
        logger.info("SearchAPI: %d domains → %d total results", len(domains), total)
        return responses
