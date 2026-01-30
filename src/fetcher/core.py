"""
Core news fetching functionality using SearchAPI + Diffbot.

SearchAPI provides Google News search results.
Diffbot extracts clean article text from URLs.
"""

import asyncio
import hashlib
import logging
import os
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

# =============================================================================
# API CONFIGURATION
# =============================================================================

SEARCHAPI_KEY = os.environ.get("SEARCHAPI_KEY")
DIFFBOT_TOKEN = os.environ.get("DIFFBOT_TOKEN")
DIFFBOT_DELAY_SECONDS = 12  # Rate limit: 5 calls/minute

# HTTP settings
TIMEOUT = httpx.Timeout(30.0, connect=10.0)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PDB-Aggregator/1.0)",
    "Accept": "application/json",
}


# =============================================================================
# OPINION FILTERING
# =============================================================================

# URL patterns that indicate opinion/editorial content
OPINION_URL_PATTERNS = [
    r"/opinion/",
    r"/editorial/",
    r"/op-ed/",
    r"/oped/",
    r"/commentary/",
    r"/views/",
    r"/perspective/",
    r"/viewpoint/",
    r"/analysis/",  # Often opinion-adjacent
    r"/blog/",
    r"/column/",
    r"/columnist/",
]

# Content patterns that indicate opinion (case-insensitive)
OPINION_CONTENT_PATTERNS = [
    r"\bI think\b",
    r"\bI believe\b",
    r"\bwe should\b",
    r"\bwe must\b",
    r"\bin my opinion\b",
    r"\bin my view\b",
    r"\bopinion:\b",
    r"\beditorial:\b",
    r"\bmy take\b",
    r"\bhere's why\b",
]

# Compiled regex patterns
_opinion_url_regex = re.compile("|".join(OPINION_URL_PATTERNS), re.IGNORECASE)
_opinion_content_regex = re.compile("|".join(OPINION_CONTENT_PATTERNS), re.IGNORECASE)


def is_opinion_article(url: str, title: str = "", content: str = "") -> bool:
    """
    Determine if an article is opinion/editorial content.

    Args:
        url: Article URL
        title: Article title (optional)
        content: Article content (optional)

    Returns:
        True if article appears to be opinion content
    """
    # Check URL patterns
    if _opinion_url_regex.search(url):
        return True

    # Check title for opinion indicators
    title_lower = title.lower()
    if any(word in title_lower for word in ["opinion:", "editorial:", "op-ed:", "commentary:"]):
        return True

    # Check content for opinion patterns (only first 1000 chars for efficiency)
    if content and _opinion_content_regex.search(content[:1000]):
        return True

    return False


# =============================================================================
# SEARCHAPI FUNCTIONS
# =============================================================================

async def search_news_searchapi(
    query: str,
    num_results: int = 10,
    date_range: Optional[tuple[str, str]] = None,
    site: Optional[str] = None,
    page: int = 1,
    time_period: Optional[str] = None,
) -> list[dict]:
    """
    Search Google News via SearchAPI.

    Args:
        query: Search query
        num_results: Number of results to return
        date_range: Optional (start_date, end_date) tuple in YYYY-MM-DD format
        site: Optional site filter (e.g., "reuters.com")
        page: Page number (1-indexed)
        time_period: Optional time period filter (e.g., "last_hour", "last_day", "last_week", "last_month", "last_year")

    Returns:
        List of search result dicts with title, link, snippet, etc.
    """
    if not SEARCHAPI_KEY:
        logger.warning("SEARCHAPI_KEY not set, cannot search")
        return []

    # Build query with site filter if provided
    search_query = query
    if site:
        search_query = f"site:{site} {query}"

    params = {
        "engine": "google_news",
        "q": search_query,
        "api_key": SEARCHAPI_KEY,
        "num": num_results,
        "page": page,
    }

    # Add time period if specified
    if time_period:
        params["time_period"] = time_period

    # Add date range if specified
    if date_range:
        start_date, end_date = date_range
        # SearchAPI uses tbs parameter for date filtering
        params["tbs"] = f"cdr:1,cd_min:{start_date},cd_max:{end_date}"

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
        try:
            response = await client.get(
                "https://www.searchapi.io/api/v1/search",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("news_results", []) or data.get("organic_results", []):
                # Handle source as either string or dict
                source = item.get("source", "")
                if isinstance(source, dict):
                    source = source.get("name", "")

                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("link", ""),
                    "snippet": item.get("snippet", ""),
                    "source": source,
                    "date": item.get("date", ""),
                })

            return results

        except httpx.HTTPError as e:
            logger.error(f"SearchAPI request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"SearchAPI error: {e}")
            return []


# =============================================================================
# DIFFBOT FUNCTIONS
# =============================================================================

async def extract_article_diffbot(url: str) -> Optional[dict]:
    """
    Extract article content using Diffbot Article API.

    Args:
        url: URL of the article to extract

    Returns:
        Dict with title, text, author, date, etc. or None on failure
    """
    if not DIFFBOT_TOKEN:
        logger.warning("DIFFBOT_TOKEN not set, cannot extract")
        return None

    params = {
        "token": DIFFBOT_TOKEN,
        "url": url,
    }

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
        try:
            response = await client.get(
                "https://api.diffbot.com/v3/article",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

            if "objects" not in data or not data["objects"]:
                logger.warning(f"No content extracted from {url}")
                return None

            article = data["objects"][0]

            return {
                "title": article.get("title", ""),
                "text": article.get("text", ""),
                "author": article.get("author", ""),
                "date": article.get("date", ""),
                "siteName": article.get("siteName", ""),
                "language": article.get("humanLanguage", "en"),
            }

        except httpx.HTTPError as e:
            logger.error(f"Diffbot request failed for {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Diffbot error for {url}: {e}")
            return None


# =============================================================================
# MAIN FETCH FUNCTION
# =============================================================================

async def fetch_articles_for_leader(
    leader_name: str,
    sources: list[dict],
    date_start: str,
    date_end: str,
    max_articles_per_source: int = 5,
    skip_opinion: bool = True,
) -> list[dict]:
    """
    Fetch news articles for a leader using SearchAPI + Diffbot.

    1. Search via SearchAPI Google News engine with domain filter
    2. Filter out opinion pieces (URL + content analysis)
    3. Extract full text via Diffbot

    Args:
        leader_name: Name of the leader to search for
        sources: List of source configs with 'name' and 'url' keys
        date_start: Start date (YYYY-MM-DD)
        date_end: End date (YYYY-MM-DD)
        max_articles_per_source: Max articles to fetch per source
        skip_opinion: Whether to filter out opinion articles

    Returns:
        List of article dicts with full text extracted
    """
    from ..debug import save_search_results, is_debug_enabled

    if not SEARCHAPI_KEY:
        logger.warning("SEARCHAPI_KEY not set, returning empty results")
        return []

    all_articles = []
    date_range = (date_start, date_end)

    for source in sources:
        source_name = source.get("name", "Unknown")
        source_url = source.get("url", "")

        # Extract domain from URL
        domain = urlparse(source_url).netloc if source_url else None

        logger.info(f"Searching {source_name} for {leader_name}")

        # Search for articles
        results = await search_news_searchapi(
            query=leader_name,
            num_results=max_articles_per_source * 2,  # Fetch extra to account for filtering
            date_range=date_range,
            site=domain,
        )

        # Save search results for debugging
        if is_debug_enabled():
            save_search_results(
                leader_name=leader_name,
                source_name=source_name,
                query=f"{leader_name} site:{domain}" if domain else leader_name,
                results=results,
            )

        # Process each result
        articles_from_source = []
        for result in results:
            url = result.get("link", "")
            title = result.get("title", "")

            if not url:
                continue

            # Skip opinion articles based on URL
            if skip_opinion and is_opinion_article(url, title):
                logger.debug(f"Skipping opinion article: {title[:50]}")
                continue

            # Extract full content via Diffbot
            if DIFFBOT_TOKEN:
                # Rate limit Diffbot calls
                await asyncio.sleep(DIFFBOT_DELAY_SECONDS)

                extracted = await extract_article_diffbot(url)

                if extracted:
                    content = extracted.get("text", "")

                    # Skip opinion based on content
                    if skip_opinion and is_opinion_article(url, title, content):
                        logger.debug(f"Skipping opinion article (content): {title[:50]}")
                        continue

                    article = {
                        "id": hashlib.md5(f"{source_name}:{url}".encode()).hexdigest()[:12],
                        "title": extracted.get("title") or title,
                        "url": url,
                        "content": content,
                        "source_name": source_name,
                        "source_type": source.get("source_type", "domestic"),
                        "language": extracted.get("language", source.get("language", "en")),
                        "published_at": extracted.get("date"),
                        "snippet": result.get("snippet", ""),
                    }
                    articles_from_source.append(article)
            else:
                # Without Diffbot, use snippet only
                article = {
                    "id": hashlib.md5(f"{source_name}:{url}".encode()).hexdigest()[:12],
                    "title": title,
                    "url": url,
                    "content": result.get("snippet", ""),
                    "source_name": source_name,
                    "source_type": source.get("source_type", "domestic"),
                    "language": source.get("language", "en"),
                    "published_at": result.get("date"),
                    "snippet": result.get("snippet", ""),
                }
                articles_from_source.append(article)

            # Stop if we have enough
            if len(articles_from_source) >= max_articles_per_source:
                break

        logger.info(f"  Found {len(articles_from_source)} articles from {source_name}")
        all_articles.extend(articles_from_source)

    return all_articles


async def fetch_articles_without_api(
    leader_name: str,
    sources: list[dict],
    date_start: str,
    date_end: str,
) -> list[dict]:
    """
    Fallback fetch function when API keys are not available.

    Returns empty list - caller should fall back to RSS or other methods.
    """
    logger.info(f"API keys not available, returning empty results for {leader_name}")
    return []
