"""
Guardian Open Platform client for MPM pipeline.

Provides full article text, tags, section, byline, publication date.
Rate limit: 12 calls/second, 500 calls/day (free developer key).
Languages: English only.

API reference: https://open-platform.theguardian.com/documentation/
"""

from __future__ import annotations

import asyncio
import html
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Countries where Guardian API adds value, with their tag and production office
GUARDIAN_COUNTRIES: dict[str, dict] = {
    "gb": {"tag": "politics/politics", "production_office": None},
    "au": {"tag": "australia-news/australia-news", "production_office": "aus"},
    "in": {"tag": "world/india", "production_office": None},
    "fr": {"tag": "world/france", "production_office": None},
    "de": {"tag": "world/germany", "production_office": None},
    "ua": {"tag": "world/ukraine", "production_office": None},
    "jp": {"tag": "world/japan", "production_office": None},
    "br": {"tag": "world/brazil", "production_office": None},
    "tr": {"tag": "world/turkey", "production_office": None},
    "sa": {"tag": "world/saudiarabia", "production_office": None},
    "kr": {"tag": "world/south-korea", "production_office": None},
    "tw": {"tag": "world/taiwan", "production_office": None},
    "id": {"tag": "world/indonesia", "production_office": None},
    "hu": {"tag": "world/hungary", "production_office": None},
}


# =============================================================================
# Data classes
# =============================================================================


@dataclass
class GuardianArticle:
    """Parsed Guardian API article, ready for pipeline consumption."""

    url: str
    guardian_id: str
    title: str
    text: str  # Full article text (HTML stripped)
    snippet: str  # Standfirst / summary
    byline: str | None
    wordcount: int
    publication_date: str  # ISO datetime
    section: str
    tags: list[str]  # Tag IDs
    short_url: str | None

    def to_extraction_format(self) -> dict:
        """Convert to the pipeline's standard extraction output format."""
        return {
            "url": self.url,
            "domain": "theguardian.com",
            "title": self.title,
            "text": self.text,
            "snippet": self.snippet,
            "extraction_method": "publisher_api_guardian",
            "extraction_failed": False,
            "source_layer": "layer1",
            "metadata": {
                "guardian_id": self.guardian_id,
                "byline": self.byline,
                "wordcount": self.wordcount,
                "publication_date": self.publication_date,
                "section": self.section,
                "tags": self.tags,
                "short_url": self.short_url,
            },
        }


# =============================================================================
# HTML stripping
# =============================================================================


def strip_html(html_content: str) -> str:
    """Convert HTML body to plain text, preserving paragraph breaks.

    The Guardian's body field returns HTML like:
    <p>First paragraph.</p><p>Second paragraph.</p>

    Convert to:
    First paragraph.

    Second paragraph.
    """
    # Replace paragraph/block tags with double newlines
    text = re.sub(r"</(p|div|h[1-6]|blockquote|li)>", "\n\n", html_content)
    text = re.sub(r"<br\s*/?>", "\n", text)
    # Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# =============================================================================
# Guardian API client
# =============================================================================


class GuardianAPI:
    """Guardian Open Platform client for the MPM pipeline.

    Usage:
        async with GuardianAPI(api_key="your-key") as api:
            articles = await api.search_country(
                country_code="in",
                actor_query='Modi OR Jaishankar OR "Reserve Bank of India"',
                from_date="2026-03-14",
                to_date="2026-03-21",
            )
    """

    BASE_URL = "https://content.guardianapis.com"

    # Fields to request for full article retrieval
    FULL_FIELDS = "body,headline,byline,wordcount,standfirst,shortUrl"

    # Fields for headline-only triage queries
    TRIAGE_FIELDS = "headline,standfirst,shortUrl"

    def __init__(
        self,
        api_key: str | None = None,
        rate_limit: float = 12.0,
    ):
        self.api_key = api_key or os.getenv("GUARDIAN_API_KEY") or os.getenv("THE_GUARDIAN_API_KEY")
        if not self.api_key:
            raise ValueError("GUARDIAN_API_KEY not found in environment or constructor")
        self._semaphore = asyncio.Semaphore(int(rate_limit))
        self._client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> GuardianAPI:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def search_country(
        self,
        country_code: str,
        actor_query: str,
        from_date: str,
        to_date: str,
        full_text: bool = True,
        max_results: int = 50,
    ) -> list[GuardianArticle]:
        """Search for articles about a country's tracked actors within a date range.

        Args:
            country_code: ISO 2-letter country code (must be in GUARDIAN_COUNTRIES).
            actor_query: OR-joined actor/institution search terms in English.
            from_date: Start of date range (YYYY-MM-DD).
            to_date: End of date range (YYYY-MM-DD).
            full_text: If True, retrieve full article body. If False, headlines only.
            max_results: Maximum articles to return (API max per page: 50).

        Returns:
            List of GuardianArticle objects.
        """
        if country_code not in GUARDIAN_COUNTRIES:
            return []

        country_config = GUARDIAN_COUNTRIES[country_code]

        params: dict[str, str | int] = {
            "tag": country_config["tag"],
            "from-date": from_date,
            "to-date": to_date,
            "show-fields": self.FULL_FIELDS if full_text else self.TRIAGE_FIELDS,
            "show-tags": "keyword",
            "page-size": min(max_results, 50),
            "order-by": "newest",
            "api-key": self.api_key,
        }

        if actor_query:
            params["q"] = actor_query

        if country_config.get("production_office"):
            params["production-office"] = country_config["production_office"]

        results = await self._paginated_search(params, max_results)
        return [self._parse_result(r, full_text) for r in results]

    async def search_query(
        self,
        query: str,
        from_date: str,
        to_date: str,
        section: str | None = None,
        tag: str | None = None,
        full_text: bool = True,
        max_results: int = 50,
    ) -> list[GuardianArticle]:
        """Generic search — for queries that don't map to a single country.

        Useful for cross-country queries like:
        - "NATO AND (defence OR defense) AND spending"
        - "BRICS AND (summit OR expansion)"
        """
        params: dict[str, str | int] = {
            "q": query,
            "from-date": from_date,
            "to-date": to_date,
            "show-fields": self.FULL_FIELDS if full_text else self.TRIAGE_FIELDS,
            "show-tags": "keyword",
            "page-size": min(max_results, 50),
            "order-by": "newest",
            "api-key": self.api_key,
        }

        if section:
            params["section"] = section
        if tag:
            params["tag"] = tag

        results = await self._paginated_search(params, max_results)
        return [self._parse_result(r, full_text) for r in results]

    async def get_article(self, guardian_url: str) -> GuardianArticle | None:
        """Fetch a specific article by its Guardian URL.

        Converts theguardian.com URL to API URL:
        https://www.theguardian.com/world/2026/mar/18/article-slug
        → https://content.guardianapis.com/world/2026/mar/18/article-slug
        """
        path = guardian_url.replace("https://www.theguardian.com/", "")
        path = path.replace("http://www.theguardian.com/", "")
        path = path.rstrip("/")

        api_url = f"{self.BASE_URL}/{path}"
        params = {
            "show-fields": self.FULL_FIELDS,
            "show-tags": "keyword",
            "api-key": self.api_key,
        }

        async with self._semaphore:
            response = await self._client.get(api_url, params=params)

        if response.status_code != 200:
            logger.debug(
                "Guardian API returned %d for %s", response.status_code, guardian_url
            )
            return None

        data = response.json()
        content = data.get("response", {}).get("content")
        if not content:
            return None

        return self._parse_result(content, full_text=True)

    async def _paginated_search(
        self, params: dict, max_results: int
    ) -> list[dict]:
        """Fetch search results, paginating if necessary."""
        all_results: list[dict] = []
        page = 1

        while len(all_results) < max_results:
            params["page"] = page

            async with self._semaphore:
                response = await self._client.get(
                    f"{self.BASE_URL}/search", params=params
                )

            if response.status_code != 200:
                logger.warning(
                    "Guardian API search returned %d on page %d",
                    response.status_code, page,
                )
                break

            data = response.json().get("response", {})
            results = data.get("results", [])

            if not results:
                break

            all_results.extend(results)

            total_pages = data.get("pages", 1)
            if page >= total_pages:
                break

            page += 1

        return all_results[:max_results]

    def _parse_result(self, result: dict, full_text: bool) -> GuardianArticle:
        """Parse a single API result into a GuardianArticle."""
        fields = result.get("fields", {})
        tags = result.get("tags", [])

        body_html = fields.get("body", "")
        text = strip_html(body_html) if full_text and body_html else ""

        return GuardianArticle(
            url=result.get("webUrl", ""),
            guardian_id=result.get("id", ""),
            title=fields.get("headline", result.get("webTitle", "")),
            text=text,
            snippet=strip_html(fields.get("standfirst", "")) if fields.get("standfirst") else "",
            byline=fields.get("byline"),
            wordcount=int(fields.get("wordcount", 0)),
            publication_date=result.get("webPublicationDate", ""),
            section=result.get("sectionId", ""),
            tags=[t["id"] for t in tags],
            short_url=fields.get("shortUrl"),
        )


# =============================================================================
# Integration helpers for the extraction orchestrator
# =============================================================================


async def guardian_extract_for_country(
    api: GuardianAPI,
    country_code: str,
    actor_query: str,
    from_date: str,
    to_date: str,
) -> list[dict]:
    """Convenience function for the extraction orchestrator.

    Returns articles in the pipeline's standard extraction format,
    ready to merge with Brave + extraction chain results.
    """
    articles = await api.search_country(
        country_code=country_code,
        actor_query=actor_query,
        from_date=from_date,
        to_date=to_date,
        full_text=True,
    )
    return [a.to_extraction_format() for a in articles]


async def guardian_triage_for_country(
    api: GuardianAPI,
    country_code: str,
    from_date: str,
    to_date: str,
) -> list[dict]:
    """Lightweight triage query — headlines only, no actor filtering.

    Returns recent Guardian coverage of a country for triage enrichment.
    Only worth calling for countries where Guardian has Tier 1-2 coverage:
    gb, au, in, fr, de, ua.
    """
    if country_code not in GUARDIAN_COUNTRIES:
        return []

    articles = await api.search_country(
        country_code=country_code,
        actor_query="",
        from_date=from_date,
        to_date=to_date,
        full_text=False,
        max_results=10,
    )
    return [a.to_extraction_format() for a in articles]
