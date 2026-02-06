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
from datetime import datetime, timedelta
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


def _parse_result_date(date_str: str) -> Optional[datetime]:
    """
    Parse a date string from search results into a datetime.

    Handles common formats from SearchAPI / Google News:
    - "2 days ago", "3 hours ago", "1 week ago"
    - "Jan 28, 2026", "January 28, 2026"
    - "2026-01-28", "2026-01-28T..."
    - "01/28/2026"
    """
    if not date_str or not date_str.strip():
        return None

    date_str = date_str.strip()

    # Relative time: "X hours/days/weeks ago"
    relative_match = re.match(
        r"(\d+)\s+(second|minute|hour|day|week|month)s?\s+ago",
        date_str,
        re.IGNORECASE,
    )
    if relative_match:
        amount = int(relative_match.group(1))
        unit = relative_match.group(2).lower()
        now = datetime.now()
        if unit in ("second", "minute", "hour"):
            return now  # same day
        elif unit == "day":
            return now - timedelta(days=amount)
        elif unit == "week":
            return now - timedelta(weeks=amount)
        elif unit == "month":
            return now - timedelta(days=amount * 30)

    # ISO format: 2026-01-28 or 2026-01-28T...
    iso_match = re.match(r"(\d{4}-\d{2}-\d{2})", date_str)
    if iso_match:
        try:
            return datetime.strptime(iso_match.group(1), "%Y-%m-%d")
        except ValueError:
            pass

    # US format: 01/28/2026
    us_match = re.match(r"(\d{2}/\d{2}/\d{4})", date_str)
    if us_match:
        try:
            return datetime.strptime(us_match.group(1), "%m/%d/%Y")
        except ValueError:
            pass

    # Named month: "Jan 28, 2026" or "January 28, 2026"
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%d %b %Y", "%d %B %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def _is_within_date_range(
    date_str: str,
    date_start: str,
    date_end: str,
    margin_days: int = 2,
) -> bool:
    """
    Check if a result's date falls within the requested range (with margin).

    Args:
        date_str: Date string from search result
        date_start: Range start (YYYY-MM-DD)
        date_end: Range end (YYYY-MM-DD)
        margin_days: Extra days of margin outside range (default 2)

    Returns:
        True if within range, or if date cannot be parsed (fail-open)
    """
    parsed = _parse_result_date(date_str)
    if parsed is None:
        # Can't parse -> let it through (fail-open)
        return True

    try:
        range_start = datetime.strptime(date_start, "%Y-%m-%d") - timedelta(days=margin_days)
        range_end = datetime.strptime(date_end, "%Y-%m-%d") + timedelta(days=margin_days)
    except ValueError:
        return True

    return range_start <= parsed <= range_end


async def fetch_snippets_for_leader(
    leader_name: str,
    sources: list[dict],
    date_start: str,
    date_end: str,
    max_results_per_source: int = 10,
) -> list[dict]:
    """
    Fetch search result snippets WITHOUT full article extraction.

    This is the first phase - cheap SerpAPI calls only, no Diffbot.
    Results are validated against the requested date range; stale
    articles outside the range are discarded.

    Args:
        leader_name: Name of leader to search
        sources: List of source configs
        date_start: Start date (YYYY-MM-DD)
        date_end: End date (YYYY-MM-DD)
        max_results_per_source: Max snippets per source

    Returns:
        List of snippet dicts with source metadata
    """
    if not SEARCHAPI_KEY:
        logger.warning("SEARCHAPI_KEY not set")
        return []

    all_snippets = []
    stale_count = 0
    date_range = (date_start, date_end)

    for source in sources:
        source_name = source.get("name", "Unknown")
        source_url = source.get("url", "")
        source_type = source.get("source_type", "domestic")

        domain = urlparse(source_url).netloc if source_url else None

        results = await search_news_searchapi(
            query=leader_name,
            num_results=max_results_per_source,
            date_range=date_range,
            site=domain,
        )

        for result in results:
            date_val = result.get("date", "")

            # Filter out stale articles
            if not _is_within_date_range(date_val, date_start, date_end):
                logger.debug(
                    f"Filtering stale result: '{result.get('title', '')[:60]}' "
                    f"(date={date_val}) outside {date_start}..{date_end}"
                )
                stale_count += 1
                continue

            all_snippets.append({
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "url": result.get("link", ""),
                "source_name": source_name,
                "source_type": source_type,
                "date": date_val,
            })

    if stale_count > 0:
        logger.info(f"Filtered {stale_count} stale results outside date range {date_start}..{date_end}")

    return all_snippets


async def fetch_full_articles(
    urls: list[str],
    source_metadata: dict[str, dict],
) -> list[dict]:
    """
    Fetch full article content for specific URLs via Diffbot.

    This is the second phase - expensive Diffbot calls only for selected articles.

    Args:
        urls: List of article URLs to fetch
        source_metadata: Map of URL to source info (name, type, language)

    Returns:
        List of article dicts with full content
    """
    if not DIFFBOT_TOKEN:
        logger.warning("DIFFBOT_TOKEN not set")
        return []

    articles = []

    for url in urls:
        await asyncio.sleep(DIFFBOT_DELAY_SECONDS)

        extracted = await extract_article_diffbot(url)

        if extracted:
            meta = source_metadata.get(url, {})
            articles.append({
                "id": hashlib.md5(url.encode()).hexdigest()[:12],
                "title": extracted.get("title", ""),
                "url": url,
                "content": extracted.get("text", ""),
                "source_name": meta.get("source_name", "Unknown"),
                "source_type": meta.get("source_type", "domestic"),
                "language": extracted.get("language", "en"),
                "published_at": extracted.get("date"),
            })

    return articles


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
