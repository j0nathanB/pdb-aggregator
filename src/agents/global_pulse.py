"""
Global Pulse Agent - Fetches top world stories to establish context.

This helps anchor the brief by identifying what major events leaders
might be responding to during the reporting period.
"""

import logging
from datetime import datetime
from typing import Optional

from ..config import GlobalPulse
from .base import complete, with_retry

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a senior intelligence analyst identifying the top global news stories.

Your task is to identify the 5 most significant world events/stories from the given time period 
that would be relevant context for understanding world leader activities.

Focus on:
- Geopolitical developments (conflicts, treaties, summits)
- Economic events (markets, trade, sanctions)
- Security issues (terrorism, military movements)
- Major policy shifts by significant powers
- International institutional actions (UN, NATO, EU, etc.)

Exclude:
- Celebrity news
- Sports (unless geopolitically significant)
- Local crime stories
- Entertainment industry news

Output format:
TOP STORIES:
1. [Concise headline-style description]
2. [Concise headline-style description]
3. [Concise headline-style description]
4. [Concise headline-style description]
5. [Concise headline-style description]

KEY THEMES:
- [Theme 1]
- [Theme 2]
- [Theme 3]
"""


class GlobalPulseAgent:
    """
    Fetches top world stories to provide context for the brief.
    
    In a production system, this would search news APIs.
    Currently uses LLM knowledge as a proxy (with appropriate caveats).
    """
    
    @with_retry(max_attempts=3)
    async def fetch(
        self,
        date_start: str,
        date_end: str,
    ) -> GlobalPulse:
        """
        Fetch global pulse for the given date range.
        
        Args:
            date_start: Start date (ISO format)
            date_end: End date (ISO format)
            
        Returns:
            GlobalPulse with top stories and themes
        """
        logger.info(f"Fetching global pulse: {date_start} to {date_end}")
        
        prompt = f"""Identify the top 5 global news stories and key themes for the period:
{date_start} to {date_end}

Note: If you don't have reliable information about this specific time period, 
indicate that and provide what context you can about ongoing situations that 
would likely be relevant.
"""
        
        response = await complete(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            temperature=0.2,
        )
        
        # Parse response
        pulse = self._parse_response(response, f"{date_start} to {date_end}")
        
        logger.info(f"Global pulse: {len(pulse.top_stories)} stories, {len(pulse.key_themes)} themes")
        
        return pulse
    
    def _parse_response(self, response: str, date_range: str) -> GlobalPulse:
        """Parse LLM response into GlobalPulse structure."""
        top_stories = []
        key_themes = []
        
        lines = response.strip().split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if "TOP STORIES" in line.upper():
                current_section = "stories"
                continue
            elif "KEY THEMES" in line.upper():
                current_section = "themes"
                continue
            
            if not line or line.startswith("#"):
                continue
            
            # Extract numbered items or bullet points
            if current_section == "stories":
                # Remove numbering like "1." or "1)"
                cleaned = line.lstrip("0123456789.-) ")
                if cleaned:
                    top_stories.append(cleaned)
            elif current_section == "themes":
                cleaned = line.lstrip("-* ")
                if cleaned:
                    key_themes.append(cleaned)
        
        return GlobalPulse(
            top_stories=top_stories[:5],  # Cap at 5
            key_themes=key_themes[:5],
            date_range=date_range,
        )
    
    async def fetch_with_search(
        self,
        date_start: str,
        date_end: str,
        search_fn: callable,
    ) -> GlobalPulse:
        """
        Fetch global pulse using actual web search.
        
        Args:
            date_start: Start date
            date_end: End date
            search_fn: Async function that takes a query and returns search results
            
        Returns:
            GlobalPulse based on actual search results
        """
        # Search for top news
        queries = [
            f"world news {date_start} {date_end}",
            f"international news headlines {date_start}",
            "geopolitics major events this week",
        ]
        
        all_results = []
        for query in queries:
            try:
                results = await search_fn(query)
                all_results.extend(results)
            except Exception as e:
                logger.warning(f"Search failed for '{query}': {e}")
        
        if not all_results:
            # Fall back to LLM knowledge
            logger.warning("No search results, falling back to LLM knowledge")
            return await self.fetch(date_start, date_end)
        
        # Use LLM to synthesize search results into pulse
        results_text = "\n".join([
            f"- {r.get('title', 'Untitled')}: {r.get('snippet', '')}"
            for r in all_results[:20]
        ])
        
        prompt = f"""Based on these search results for {date_start} to {date_end}, 
identify the top 5 global stories and key themes:

{results_text}
"""
        
        response = await complete(
            prompt=prompt,
            system=SYSTEM_PROMPT,
            temperature=0.2,
        )
        
        return self._parse_response(response, f"{date_start} to {date_end}")
