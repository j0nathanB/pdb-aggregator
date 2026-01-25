"""
Classifier Agent - Applies Paragon taxonomy to articles.

Classifies each article by:
- Event type (policy announcement, visit, speech, etc.)
- Leader role (initiator, participant, subject)
- Impact level (international, national, regional, local)

Then calculates a priority score for filtering.
"""

import json
import logging
from typing import Optional

from ..config import (
    Article,
    ArticleClassification,
    LeaderConfig,
    EventType,
    LeaderRole,
    ImpactLevel,
    EVENT_TYPE_WEIGHTS,
    LEADER_ROLE_WEIGHTS,
    IMPACT_LEVEL_WEIGHTS,
)
from .base import complete, with_retry, process_batch, extract_json_from_response

logger = logging.getLogger(__name__)


CLASSIFICATION_SYSTEM = """You are an intelligence analyst classifying news articles about world leaders.

For each article, determine:

1. EVENT_TYPE - What kind of event is being reported?
   - POLICY_ANNOUNCEMENT: New policy, law, regulation, executive order
   - INTERNATIONAL_VISIT: Foreign travel, hosting foreign leaders
   - MAJOR_SPEECH: Significant public address, keynote, address to nation
   - CABINET_CHANGE: Government personnel changes, appointments, dismissals
   - LEGAL_DEVELOPMENT: Court rulings, investigations, indictments
   - BILATERAL_AGREEMENT: Treaties, deals, MOUs, joint statements
   - CRISIS_RESPONSE: Emergency actions, disaster response, conflict management
   - ECONOMIC_ACTION: Tariffs, sanctions, fiscal policy, budget
   - OTHER: Doesn't fit above categories

2. LEADER_ROLE - What is the leader's role in this event?
   - INITIATOR: Leader is driving/announcing/deciding the action
   - PARTICIPANT: Leader is involved but not the primary driver
   - SUBJECT: Leader is being reported on passively (e.g., polling, criticism)

3. IMPACT_LEVEL - What is the geographic scope of impact?
   - INTERNATIONAL: Affects multiple countries
   - NATIONAL: Affects the leader's country broadly
   - REGIONAL: Affects a sub-national region
   - LOCAL: Limited local impact

Output your classification as JSON:
{
    "event_type": "EVENT_TYPE",
    "leader_role": "LEADER_ROLE", 
    "impact_level": "IMPACT_LEVEL",
    "reasoning": "Brief explanation of classification"
}
"""


class ClassifierAgent:
    """
    Classifies articles using the Paragon taxonomy.
    
    Each article is scored based on:
    - Event type significance
    - Leader's role (initiator vs subject)
    - Geographic impact scope
    """
    
    async def classify_batch(
        self,
        articles: list[Article],
        leader: LeaderConfig,
    ) -> list[Article]:
        """
        Classify a batch of articles for a specific leader.
        
        Args:
            articles: Articles to classify
            leader: The leader these articles are about
            
        Returns:
            Articles with classification populated
        """
        if not articles:
            return articles
        
        logger.info(f"Classifying {len(articles)} articles for {leader.name}")
        
        async def classify_one(article: Article) -> Article:
            return await self.classify_article(article, leader)
        
        classified = await process_batch(
            items=articles,
            processor=classify_one,
            max_concurrent=5,
            desc=f"Classifying {leader.name}",
        )
        
        # Filter out None results
        return [a for a in classified if a is not None]
    
    @with_retry(max_attempts=2)
    async def classify_article(
        self,
        article: Article,
        leader: LeaderConfig,
    ) -> Article:
        """
        Classify a single article.
        
        Args:
            article: Article to classify
            leader: The leader context
            
        Returns:
            Article with classification populated
        """
        content = article.display_content
        
        if not content:
            # No content to classify
            article.classification = self._default_classification()
            return article
        
        prompt = f"""Classify this news article about {leader.name} ({leader.title} of {leader.country}).

HEADLINE: {article.title}

CONTENT:
{content[:3000]}  # Truncate for token efficiency

Provide your classification as JSON.
"""
        
        response = await complete(
            prompt=prompt,
            system=CLASSIFICATION_SYSTEM,
            temperature=0.1,
        )
        
        # Parse classification
        classification = self._parse_classification(response)
        article.classification = classification
        
        return article
    
    def _parse_classification(self, response: str) -> ArticleClassification:
        """Parse LLM response into classification object."""
        
        # Try to extract JSON
        data = extract_json_from_response(response)
        
        if not data:
            logger.warning(f"Failed to parse classification JSON: {response[:200]}")
            return self._default_classification()
        
        try:
            # Parse enum values (handle case insensitivity)
            event_type = self._parse_event_type(data.get("event_type", "OTHER"))
            leader_role = self._parse_leader_role(data.get("leader_role", "SUBJECT"))
            impact_level = self._parse_impact_level(data.get("impact_level", "NATIONAL"))
            
            # Calculate priority score
            priority_score = ArticleClassification.calculate_priority(
                event_type=event_type,
                leader_role=leader_role,
                impact_level=impact_level,
            )
            
            return ArticleClassification(
                event_type=event_type,
                leader_role=leader_role,
                impact_level=impact_level,
                priority_score=priority_score,
                reasoning=data.get("reasoning", ""),
            )
            
        except Exception as e:
            logger.warning(f"Classification parsing error: {e}")
            return self._default_classification()
    
    def _parse_event_type(self, value: str) -> EventType:
        """Parse event type string to enum."""
        value = value.upper().replace(" ", "_")
        try:
            return EventType(value.lower())
        except ValueError:
            # Try matching by name
            for et in EventType:
                if et.name == value:
                    return et
            return EventType.OTHER
    
    def _parse_leader_role(self, value: str) -> LeaderRole:
        """Parse leader role string to enum."""
        value = value.upper()
        try:
            return LeaderRole(value.lower())
        except ValueError:
            for lr in LeaderRole:
                if lr.name == value:
                    return lr
            return LeaderRole.SUBJECT
    
    def _parse_impact_level(self, value: str) -> ImpactLevel:
        """Parse impact level string to enum."""
        value = value.upper()
        try:
            return ImpactLevel(value.lower())
        except ValueError:
            for il in ImpactLevel:
                if il.name == value:
                    return il
            return ImpactLevel.NATIONAL
    
    def _default_classification(self) -> ArticleClassification:
        """Return a default low-priority classification."""
        return ArticleClassification(
            event_type=EventType.OTHER,
            leader_role=LeaderRole.SUBJECT,
            impact_level=ImpactLevel.LOCAL,
            priority_score=0.0,
            reasoning="Default classification (parsing failed or no content)",
        )
    
    async def extract_underlying_event(
        self,
        article: Article,
        leader: LeaderConfig,
    ) -> Optional[str]:
        """
        Extract a normalized description of the underlying event.
        
        Used for cross-cutting thread detection - we want to identify
        when multiple articles are about the same real-world event.
        
        Args:
            article: Classified article
            leader: Leader context
            
        Returns:
            Normalized event description or None
        """
        content = article.display_content
        
        if not content:
            return None
        
        prompt = f"""What is the underlying real-world event in this article?

HEADLINE: {article.title}
CONTENT: {content[:2000]}

Describe the core event in 1-2 sentences, focusing on:
- What happened
- Where it happened
- When it happened (if stated)
- Who was primarily involved

Be specific and factual. If this is commentary/opinion without a clear event, respond with "NO_EVENT".
"""
        
        response = await complete(
            prompt=prompt,
            temperature=0.1,
            max_tokens=200,
        )
        
        response = response.strip()
        
        if "NO_EVENT" in response.upper():
            return None
        
        return response
