"""
Source Fetcher Agent - Fetches articles from wire services and domestic sources.

Multi-tier aggregation strategy:
1. API-based fetching (SearchAPI + Diffbot) when keys available
2. Wire services (Reuters, AP, AFP) for baseline English coverage via RSS
3. Domestic sources for local perspective and depth
4. LLM-generated placeholders as fallback for testing
"""

import asyncio
import hashlib
import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

import httpx

from ..config import (
    Article,
    LeaderConfig,
    SourceConfig,
    WIRE_SERVICES,
    MAX_ARTICLES_PER_LEADER,
)
from ..fetcher import (
    fetch_articles_for_leader as fetch_via_api,
    SEARCHAPI_KEY,
    DIFFBOT_TOKEN,
)
from .base import complete, with_retry, process_batch

logger = logging.getLogger(__name__)


# HTTP client settings
TIMEOUT = httpx.Timeout(30.0, connect=10.0)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; PDB-Aggregator/1.0; +https://example.com/bot)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


class SourceFetcherAgent:
    """
    Fetches news articles about tracked leaders from multiple source types.
    
    Strategy:
    1. Try RSS feeds first (fastest, most structured)
    2. Fall back to web search for sources without RSS
    3. Deduplicate across sources
    """
    
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self.client is None:
            self.client = httpx.AsyncClient(
                timeout=TIMEOUT,
                headers=HEADERS,
                follow_redirects=True,
            )
        return self.client
    
    async def close(self):
        """Close HTTP client."""
        if self.client:
            await self.client.aclose()
            self.client = None
    
    async def fetch_for_leader(
        self,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """
        Fetch all articles mentioning a leader from all configured sources.

        Uses API-based fetching (SearchAPI + Diffbot) when keys are available,
        otherwise falls back to RSS and placeholder methods.

        Args:
            leader: Leader configuration
            date_start: Start date (ISO format)
            date_end: End date (ISO format)

        Returns:
            List of deduplicated articles
        """
        logger.info(f"Fetching articles for {leader.name}")

        # Check for API keys
        if SEARCHAPI_KEY and DIFFBOT_TOKEN:
            return await self._fetch_via_api(leader, date_start, date_end)
        else:
            return await self._fetch_via_rss(leader, date_start, date_end)

    async def _fetch_via_api(
        self,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """Fetch articles using SearchAPI + Diffbot."""
        logger.info(f"  Using API-based fetching for {leader.name}")

        # Combine wire services and domestic sources
        all_sources = []

        for source in WIRE_SERVICES:
            all_sources.append({
                "name": source.name,
                "url": source.url,
                "language": source.language,
                "source_type": source.source_type,
            })

        for source in leader.domestic_sources:
            all_sources.append({
                "name": source.name,
                "url": source.url,
                "language": source.language,
                "source_type": source.source_type,
            })

        # Fetch via API
        api_results = await fetch_via_api(
            leader_name=leader.name,
            sources=all_sources,
            date_start=date_start,
            date_end=date_end,
            max_articles_per_source=MAX_ARTICLES_PER_LEADER,
            skip_opinion=True,
        )

        # Convert to Article objects
        articles = []
        for result in api_results:
            article = Article(
                id=result.get("id", ""),
                title=result.get("title", ""),
                url=result.get("url", ""),
                source_name=result.get("source_name", ""),
                source_type=result.get("source_type", "domestic"),
                content=result.get("content", ""),
                summary=result.get("snippet", ""),
                original_language=result.get("language", "en"),
            )
            articles.append(article)

        logger.info(f"  API fetch: {len(articles)} articles")

        # Deduplicate
        unique_articles = self._deduplicate(articles)
        logger.info(f"  After dedup: {len(unique_articles)} articles")

        return unique_articles

    async def _fetch_via_rss(
        self,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """Fallback: Fetch articles using RSS and placeholder methods."""
        logger.info(f"  Using RSS-based fetching for {leader.name}")

        all_articles: list[Article] = []

        # 1. Fetch from wire services
        wire_articles = await self._fetch_from_sources(
            sources=WIRE_SERVICES,
            leader=leader,
            date_start=date_start,
            date_end=date_end,
        )
        all_articles.extend(wire_articles)
        logger.info(f"  Wire services: {len(wire_articles)} articles")

        # 2. Fetch from domestic sources
        domestic_articles = await self._fetch_from_sources(
            sources=leader.domestic_sources,
            leader=leader,
            date_start=date_start,
            date_end=date_end,
        )
        all_articles.extend(domestic_articles)
        logger.info(f"  Domestic sources: {len(domestic_articles)} articles")

        # 3. Deduplicate
        unique_articles = self._deduplicate(all_articles)
        logger.info(f"  After dedup: {len(unique_articles)} articles")

        return unique_articles
    
    async def _fetch_from_sources(
        self,
        sources: list[SourceConfig],
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """Fetch from a list of sources in parallel."""
        
        async def fetch_one(source: SourceConfig) -> list[Article]:
            try:
                if source.rss_url:
                    return await self._fetch_from_rss(source, leader, date_start, date_end)
                else:
                    return await self._fetch_via_search(source, leader, date_start, date_end)
            except Exception as e:
                logger.warning(f"Failed to fetch from {source.name}: {e}")
                return []
        
        results = await process_batch(
            items=sources,
            processor=fetch_one,
            max_concurrent=3,
            desc=f"Fetching for {leader.name}",
        )
        
        # Flatten results
        articles = []
        for result in results:
            if result:
                articles.extend(result)
        
        return articles
    
    async def _fetch_from_rss(
        self,
        source: SourceConfig,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """Fetch articles from an RSS feed."""
        client = await self._get_client()
        
        try:
            response = await client.get(source.rss_url)
            response.raise_for_status()
        except httpx.HTTPError as e:
            logger.warning(f"RSS fetch failed for {source.name}: {e}")
            return await self._fetch_via_search(source, leader, date_start, date_end)
        
        # Parse RSS
        try:
            root = ET.fromstring(response.text)
        except ET.ParseError as e:
            logger.warning(f"RSS parse failed for {source.name}: {e}")
            return []
        
        articles = []
        
        # Handle both RSS 2.0 and Atom formats
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        
        for item in items:
            article = self._parse_rss_item(item, source, leader)
            if article and self._matches_leader(article, leader):
                articles.append(article)
        
        return articles
    
    def _parse_rss_item(
        self,
        item: ET.Element,
        source: SourceConfig,
        leader: LeaderConfig,
    ) -> Optional[Article]:
        """Parse a single RSS item into an Article."""
        # RSS 2.0 format
        title = item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title")
        link = item.findtext("link") or item.find("{http://www.w3.org/2005/Atom}link")
        description = item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary")
        pub_date = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}published")
        
        # Handle Atom link element (has href attribute)
        if hasattr(link, "get"):
            link = link.get("href")
        
        if not title or not link:
            return None
        
        # Generate stable ID
        article_id = hashlib.md5(f"{source.name}:{link}".encode()).hexdigest()[:12]
        
        # Parse date
        published_at = None
        if pub_date:
            try:
                # Try common RSS date formats
                for fmt in [
                    "%a, %d %b %Y %H:%M:%S %z",
                    "%a, %d %b %Y %H:%M:%S GMT",
                    "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%dT%H:%M:%SZ",
                ]:
                    try:
                        published_at = datetime.strptime(pub_date.strip(), fmt)
                        break
                    except ValueError:
                        continue
            except Exception:
                pass
        
        return Article(
            id=article_id,
            title=title.strip(),
            url=link if isinstance(link, str) else str(link),
            source_name=source.name,
            source_type=source.source_type,
            published_at=published_at,
            content=description or "",
            summary=description or "",
            original_language=source.language,
        )
    
    async def _fetch_via_search(
        self,
        source: SourceConfig,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """
        Fetch articles via simulated search.
        
        In production, this would use a real search API (Google News, NewsAPI, etc.)
        For now, we use LLM to generate plausible article summaries based on
        known patterns. This is a placeholder for proper search integration.
        """
        # For now, return empty list - proper search would go here
        # This is where you'd integrate NewsAPI, Google News API, etc.
        logger.debug(f"Search fallback not implemented for {source.name}")
        
        # Placeholder: Use LLM to generate what articles MIGHT exist
        # This is NOT production-ready - just for testing the pipeline
        return await self._generate_placeholder_articles(source, leader, date_start, date_end)
    
    async def _generate_placeholder_articles(
        self,
        source: SourceConfig,
        leader: LeaderConfig,
        date_start: str,
        date_end: str,
    ) -> list[Article]:
        """
        Generate placeholder articles for testing.
        
        WARNING: This is for pipeline testing only. In production,
        replace with actual news API integration.
        """
        prompt = f"""Generate 2-3 realistic news article summaries that {source.name} 
might have published about {leader.name} ({leader.title} of {leader.country}) 
during {date_start} to {date_end}.

For each article, provide:
- A realistic headline
- A 2-3 sentence summary
- The type of event (policy, visit, speech, etc.)

Format each as:
HEADLINE: [headline]
SUMMARY: [summary]
---
"""
        
        try:
            response = await complete(
                prompt=prompt,
                temperature=0.7,
            )
            
            return self._parse_placeholder_response(response, source, leader)
        except Exception as e:
            logger.warning(f"Placeholder generation failed: {e}")
            return []
    
    def _parse_placeholder_response(
        self,
        response: str,
        source: SourceConfig,
        leader: LeaderConfig,
    ) -> list[Article]:
        """Parse placeholder article response."""
        articles = []
        
        # Split by separator
        blocks = response.split("---")
        
        for i, block in enumerate(blocks):
            lines = block.strip().split("\n")
            headline = ""
            summary = ""
            
            for line in lines:
                if line.startswith("HEADLINE:"):
                    headline = line.replace("HEADLINE:", "").strip()
                elif line.startswith("SUMMARY:"):
                    summary = line.replace("SUMMARY:", "").strip()
            
            if headline:
                article_id = hashlib.md5(
                    f"{source.name}:{leader.name}:{i}:{headline[:50]}".encode()
                ).hexdigest()[:12]
                
                articles.append(Article(
                    id=article_id,
                    title=headline,
                    url=f"{source.url}/article/{article_id}",  # Placeholder URL
                    source_name=source.name,
                    source_type=source.source_type,
                    content=summary,
                    summary=summary,
                    original_language=source.language,
                ))
        
        return articles
    
    def _matches_leader(self, article: Article, leader: LeaderConfig) -> bool:
        """Check if article mentions the leader."""
        text = f"{article.title} {article.content}".lower()
        
        for term in leader.search_terms:
            if term.lower() in text:
                return True
        
        return False
    
    def _deduplicate(self, articles: list[Article]) -> list[Article]:
        """
        Remove duplicate articles based on title similarity.
        
        Uses simple title normalization. Production version would
        use more sophisticated deduplication (embeddings, etc.)
        """
        seen_titles: dict[str, Article] = {}
        unique = []
        
        for article in articles:
            # Normalize title for comparison
            normalized = self._normalize_title(article.title)
            
            if normalized not in seen_titles:
                seen_titles[normalized] = article
                unique.append(article)
            else:
                # Keep the one with more content
                existing = seen_titles[normalized]
                if len(article.content) > len(existing.content):
                    unique.remove(existing)
                    unique.append(article)
                    seen_titles[normalized] = article
        
        return unique
    
    def _normalize_title(self, title: str) -> str:
        """Normalize title for deduplication comparison."""
        import re
        
        # Lowercase, remove punctuation, collapse whitespace
        normalized = title.lower()
        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        
        return normalized
