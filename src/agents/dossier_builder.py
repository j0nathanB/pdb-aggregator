"""
Dossier Builder Agent - Builds structured dossiers for each leader.

Takes classified articles and synthesizes them into:
- Key actions (3-5 most significant)
- Domestic context
- International posture
- Analyst assessment
"""

import logging
from datetime import datetime
from typing import Optional
import json

from ..config import (
    Article,
    LeaderConfig,
    LeaderDossier,
    LeaderAction,
    GlobalPulse,
    UnderlyingEvent,
    EventType,
)
from .base import complete, with_retry, extract_json_from_response

logger = logging.getLogger(__name__)


DOSSIER_SYSTEM = """You are a senior intelligence analyst writing a dossier on a world leader.

Your dossier should be:
- FACTUAL: Based only on the provided source articles
- ANALYTICAL: Go beyond summarizing to assess significance
- BALANCED: Present multiple perspectives where they exist
- CONCISE: Prioritize clarity over comprehensiveness

Structure your analysis around:
1. What concrete actions did this leader take?
2. What domestic pressures or context explain their behavior?
3. How are they positioning themselves internationally?
4. What is your assessment of their trajectory?
"""


class DossierBuilderAgent:
    """
    Builds comprehensive dossiers for each tracked leader.
    
    Synthesizes classified articles into structured analysis
    with key actions, context, and assessment.
    """
    
    @with_retry(max_attempts=2)
    async def build(
        self,
        leader: LeaderConfig,
        articles: list[Article],
        global_context: Optional[GlobalPulse] = None,
    ) -> LeaderDossier:
        """
        Build a dossier for a leader from their articles.

        Uses BOTTOM-UP approach - global_context is deprecated and ignored.
        The narrative emerges from leader actions, not top-down framing.

        Args:
            leader: Leader configuration
            articles: Classified and filtered articles
            global_context: DEPRECATED - ignored in bottom-up architecture

        Returns:
            Completed LeaderDossier
        """
        # Note: global_context is ignored in bottom-up architecture
        if global_context is not None:
            logger.debug("global_context provided but ignored (bottom-up architecture)")

        logger.info(f"Building dossier for {leader.name} from {len(articles)} articles")
        
        if not articles:
            return self._empty_dossier(leader)
        
        # Sort articles by priority
        sorted_articles = sorted(
            articles,
            key=lambda a: a.classification.priority_score if a.classification else 0,
            reverse=True,
        )
        
        # Extract key actions
        key_actions = await self._extract_key_actions(leader, sorted_articles)
        
        # Generate narrative sections
        domestic_context = await self._generate_domestic_context(leader, sorted_articles)
        international_posture = await self._generate_international_posture(leader, sorted_articles)
        assessment = await self._generate_assessment(leader, sorted_articles, global_context)
        
        # Extract underlying events for thread detection
        underlying_events = await self._extract_events(leader, sorted_articles[:10])
        
        # Compile dossier
        dossier = LeaderDossier(
            leader=leader,
            reporting_period=self._get_reporting_period(articles),
            key_actions=key_actions,
            domestic_context=domestic_context,
            international_posture=international_posture,
            assessment=assessment,
            articles=articles,
            underlying_events=underlying_events,
            source_quality_notes=self._assess_source_quality(articles, leader),
        )
        
        return dossier
    
    async def _extract_key_actions(
        self,
        leader: LeaderConfig,
        articles: list[Article],
    ) -> list[LeaderAction]:
        """Extract 3-5 most significant actions from articles."""
        
        # Build article summaries for context
        article_summaries = self._format_articles_for_prompt(articles[:15])
        
        prompt = f"""Based on these news articles about {leader.name} ({leader.title} of {leader.country}), 
identify the 3-5 MOST SIGNIFICANT actions or decisions they made.

ARTICLES:
{article_summaries}

For each action, provide JSON:
{{
    "actions": [
        {{
            "description": "What the leader did",
            "event_type": "POLICY_ANNOUNCEMENT|INTERNATIONAL_VISIT|MAJOR_SPEECH|CABINET_CHANGE|LEGAL_DEVELOPMENT|BILATERAL_AGREEMENT|CRISIS_RESPONSE|ECONOMIC_ACTION|OTHER",
            "significance": "Why this matters",
            "article_indices": [0, 2]  // Which articles support this
        }}
    ]
}}

Focus on actions where the leader was an INITIATOR, not just mentioned.
"""
        
        response = await complete(
            prompt=prompt,
            system=DOSSIER_SYSTEM,
            temperature=0.2,
        )
        
        return self._parse_actions(response, articles)
    
    def _parse_actions(
        self,
        response: str,
        articles: list[Article],
    ) -> list[LeaderAction]:
        """Parse action extraction response."""
        data = extract_json_from_response(response)
        
        if not data or "actions" not in data:
            logger.warning("Failed to parse actions response")
            return []
        
        actions = []
        for item in data["actions"][:5]:  # Cap at 5
            try:
                # Map article indices to IDs
                indices = item.get("article_indices", [])
                source_articles = [
                    articles[i].id 
                    for i in indices 
                    if i < len(articles)
                ]
                
                # Parse event type
                event_type_str = item.get("event_type", "OTHER").upper()
                try:
                    event_type = EventType(event_type_str.lower())
                except ValueError:
                    event_type = EventType.OTHER
                
                actions.append(LeaderAction(
                    description=item.get("description", ""),
                    event_type=event_type,
                    source_articles=source_articles,
                    significance=item.get("significance", ""),
                ))
            except Exception as e:
                logger.warning(f"Failed to parse action: {e}")
                continue
        
        return actions
    
    async def _generate_domestic_context(
        self,
        leader: LeaderConfig,
        articles: list[Article],
    ) -> str:
        """Generate domestic context paragraph."""
        
        # Filter to domestic sources
        domestic_articles = [
            a for a in articles 
            if a.source_type == "domestic"
        ]
        
        if not domestic_articles:
            domestic_articles = articles[:5]
        
        article_summaries = self._format_articles_for_prompt(domestic_articles[:10])
        
        prompt = f"""Based on these articles, write 2-3 sentences about the DOMESTIC CONTEXT 
for {leader.name}'s recent actions.

Focus on:
- Internal political pressures
- Public opinion or polling (if mentioned)
- Coalition dynamics or party politics
- Economic conditions affecting decisions

ARTICLES:
{article_summaries}

Write in analytical prose, not bullet points.
"""
        
        response = await complete(
            prompt=prompt,
            system=DOSSIER_SYSTEM,
            temperature=0.3,
            max_tokens=500,
        )
        
        return response.strip()
    
    async def _generate_international_posture(
        self,
        leader: LeaderConfig,
        articles: list[Article],
    ) -> str:
        """Generate international posture paragraph."""
        
        # Filter to international-impact articles
        intl_articles = [
            a for a in articles
            if a.classification and a.classification.impact_level.value == "international"
        ]
        
        if not intl_articles:
            intl_articles = articles[:5]
        
        article_summaries = self._format_articles_for_prompt(intl_articles[:10])
        
        prompt = f"""Based on these articles, write 2-3 sentences about {leader.name}'s 
INTERNATIONAL POSTURE during this period.

Focus on:
- Key bilateral relationships
- Stance on major international issues
- Diplomatic initiatives or tensions
- Alliances and alignments

ARTICLES:
{article_summaries}

Write in analytical prose, not bullet points.
"""
        
        response = await complete(
            prompt=prompt,
            system=DOSSIER_SYSTEM,
            temperature=0.3,
            max_tokens=500,
        )
        
        return response.strip()
    
    async def _generate_assessment(
        self,
        leader: LeaderConfig,
        articles: list[Article],
        global_context: Optional[GlobalPulse],
    ) -> str:
        """Generate analyst assessment paragraph."""

        article_summaries = self._format_articles_for_prompt(articles[:10])

        # Bottom-up: assessment is based on articles, not top-down global context
        # global_context parameter kept for API compatibility but ignored

        prompt = f"""Based on these articles, write a 2-3 sentence
ANALYST ASSESSMENT of {leader.name}'s trajectory.

ARTICLES:
{article_summaries}

Your assessment should:
- Identify the most important trend or development
- Note any significant changes from recent patterns
- Flag potential risks or opportunities ahead
- Consider international implications of their actions

Write as a senior analyst giving a bottom-line assessment.
Focus on what the LEADER's actions reveal about their strategy and priorities.
"""

        response = await complete(
            prompt=prompt,
            system=DOSSIER_SYSTEM,
            temperature=0.4,
            max_tokens=400,
        )

        return response.strip()
    
    async def _extract_events(
        self,
        leader: LeaderConfig,
        articles: list[Article],
    ) -> list[UnderlyingEvent]:
        """Extract underlying events for thread detection."""
        
        from .classifier import ClassifierAgent
        classifier = ClassifierAgent()
        
        events = []
        for i, article in enumerate(articles):
            try:
                event_desc = await classifier.extract_underlying_event(article, leader)
                if event_desc:
                    events.append(UnderlyingEvent(
                        id=f"{leader.name}:{article.id}",
                        description=event_desc,
                        leaders_involved=[leader.name],
                        article_ids=[article.id],
                    ))
            except Exception as e:
                logger.warning(f"Event extraction failed for article {i}: {e}")
        
        return events
    
    def _format_articles_for_prompt(self, articles: list[Article]) -> str:
        """Format articles for inclusion in prompt."""
        formatted = []
        for i, article in enumerate(articles):
            content = article.display_content
            if len(content) > 500:
                content = content[:500] + "..."
            
            priority = ""
            if article.classification:
                priority = f" [Priority: {article.classification.priority_score:.2f}]"
            
            formatted.append(
                f"[{i}] {article.title}{priority}\n"
                f"    Source: {article.source_name}\n"
                f"    {content}"
            )
        
        return "\n\n".join(formatted)
    
    def _get_reporting_period(self, articles: list[Article]) -> str:
        """Determine reporting period from article dates."""
        dates = [a.published_at for a in articles if a.published_at]
        
        if not dates:
            return "Unknown period"
        
        min_date = min(dates)
        max_date = max(dates)
        
        return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"
    
    def _assess_source_quality(
        self,
        articles: list[Article],
        leader: LeaderConfig,
    ) -> str:
        """Assess quality and coverage of sources."""
        notes = []
        
        # Check for domestic source coverage
        domestic_sources = {s.name for s in leader.domestic_sources}
        fetched_sources = {a.source_name for a in articles}
        
        missing = domestic_sources - fetched_sources
        if missing:
            notes.append(f"Missing domestic sources: {', '.join(missing)}")
        
        # Check for state media
        state_media = [a for a in articles if a.source_type == "state_media"]
        if state_media:
            notes.append(
                f"Includes {len(state_media)} state media articles "
                "(messaging may not reflect reality)"
            )
        
        # Check article count
        if len(articles) < 3:
            notes.append("Limited article coverage for this period")
        
        return "; ".join(notes) if notes else "Good source coverage"
    
    def _empty_dossier(self, leader: LeaderConfig) -> LeaderDossier:
        """Create an empty dossier when no articles are available."""
        return LeaderDossier(
            leader=leader,
            reporting_period="No coverage",
            key_actions=[],
            domestic_context="No articles available for this period.",
            international_posture="No articles available for this period.",
            assessment="Unable to assess due to lack of source coverage.",
            articles=[],
            underlying_events=[],
            source_quality_notes="No articles fetched for this leader.",
        )
