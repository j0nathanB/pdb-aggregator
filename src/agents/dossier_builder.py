"""
Dossier Builder Agent - Builds story-centric dossiers for each leader.

Takes processed events and synthesizes them into:
- Top Stories (top 5 by score, 2+ sources required)
- International (remaining, international scope)
- Domestic (remaining, domestic scope)
- Between the Lines (thematic bullets)
"""

import logging
from datetime import datetime
from typing import Optional
import json
import hashlib

from ..config import (
    Article,
    ArticleClassification,
    EventType,
    LeaderRole,
    ImpactLevel,
    LeaderConfig,
    LeaderDossier,
    Story,
    StoryScope,
    UnderlyingEvent,
)
from .base import complete, with_retry, extract_json_from_response
from .event_clustering import ProcessedEvent

logger = logging.getLogger(__name__)


DOSSIER_SYSTEM = """You are a Senior Editor for the Associated Press. Your writing is objective,
detached, and authoritative. You prioritize factual accuracy, source attribution,
and clarity. You follow AP style guidelines.

Your output must:
- Use INVERTED PYRAMID structure: most critical facts (Who, What, Where, When, Why) first
- Use NEUTRAL VERBS: "said" not "declared", "stated" not "proclaimed", "struck" not "bombarded"
- ATTRIBUTE every significant claim to a named source
- Start each story with a DATELINE: "CITY, Country —"
- Prioritize NEW DEVELOPMENTS over historical context
- Never editorialize, speculate about motivations, or use phrases like "appears to", "reveals", "demonstrates"
"""


class DossierBuilderAgent:
    """
    Builds story-centric dossiers for each tracked leader.

    Synthesizes processed events into Top Stories, International,
    Domestic, and Between the Lines.
    """

    @with_retry(max_attempts=2)
    async def build_from_events(
        self,
        leader: LeaderConfig,
        top_events: list[ProcessedEvent],
        remaining_events: list[ProcessedEvent],
        opinions: list[dict] | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
    ) -> LeaderDossier:
        """
        Build dossier from processed events using story-centric structure.

        Args:
            leader: Leader configuration
            top_events: High-importance events
            remaining_events: Lower-importance events
            opinions: Separated opinion/commentary snippets (ignored in v2)
            date_start: Start date (YYYY-MM-DD) for reporting period
            date_end: End date (YYYY-MM-DD) for reporting period

        Returns:
            Completed LeaderDossier with story-centric sections
        """
        logger.info(
            f"Building dossier for {leader.name} from "
            f"{len(top_events)} top + {len(remaining_events)} remaining events"
        )

        all_events = top_events + remaining_events
        if not all_events:
            return self._empty_dossier(leader)

        # 1. Synthesize each event into a Story
        all_stories: list[Story] = []
        for event in all_events:
            story = await self._event_to_story(event, leader)
            if story:
                all_stories.append(story)

        if not all_stories:
            return self._empty_dossier(leader)

        # 2. Sort by score, take top 5 as main_stories
        # Only stories with 2+ sources are eligible for main_stories
        all_stories.sort(key=lambda s: s.score, reverse=True)
        main_candidates = [s for s in all_stories if s.source_count >= 2]
        singletons = [s for s in all_stories if s.source_count < 2]

        main_stories = main_candidates[:5]
        overflow = main_candidates[5:] + singletons

        # 3. Split overflow by scope
        international_stories = [s for s in overflow if s.scope == StoryScope.INTERNATIONAL]
        domestic_stories = [s for s in overflow if s.scope == StoryScope.DOMESTIC]

        logger.info(
            f"Dossier for {leader.name}: {len(main_stories)} main (2+ sources), "
            f"{len(singletons)} singletons moved to overflow"
        )

        # 4. Generate Between the Lines
        between_the_lines = await self._generate_between_the_lines(leader, all_stories)

        # Build underlying events for aggregate matching
        underlying_events = self._extract_events_from_processed(leader, top_events)

        # Convert events to Article objects for metadata
        articles = self._events_to_articles(all_events)

        if date_start and date_end:
            reporting_period = f"{date_start} to {date_end}"
        else:
            reporting_period = self._get_reporting_period(articles)

        dossier = LeaderDossier(
            leader=leader,
            reporting_period=reporting_period,
            main_stories=main_stories,
            international_stories=international_stories,
            domestic_stories=domestic_stories,
            between_the_lines=between_the_lines,
            articles=articles,
            underlying_events=underlying_events,
            source_quality_notes=self._assess_source_quality(articles, leader),
        )

        return dossier

    async def _synthesize_event(
        self,
        event: ProcessedEvent,
        leader: LeaderConfig,
    ) -> Optional[dict]:
        """
        Synthesize a single event from all its articles and NLP entities.

        Returns a dict with summary, key_facts, leader_role, positions, scope.
        """
        if not event.articles:
            return None

        # Build article text block
        article_blocks = []
        for i, a in enumerate(event.articles):
            content = a.get("content", "")
            lang = a.get("language", "en")
            source = a.get("source_name", "Unknown")
            lang_note = f" [language: {lang}]" if lang != "en" else ""
            article_blocks.append(
                f"--- Article {i+1}: {a.get('title', '')} ({source}){lang_note} ---\n"
                f"{content}"
            )

        articles_text = "\n\n".join(article_blocks)

        # Entity context from NLP
        entity_context = ", ".join(
            f"{e.get('name', '')} ({e.get('type', '')})"
            for e in event.entities[:10]
        ) if event.entities else "No entities extracted"

        prompt = f"""Synthesize this event about {leader.name} ({leader.title} of {leader.country}).

EVENT TITLE: {event.title}
SOURCES: {event.source_count} sources, {'wire coverage' if event.has_wire else 'no wire coverage'}

ARTICLES:
{articles_text}

EXTRACTED ENTITIES: {entity_context}

FIRST: Determine if this event is genuinely about {leader.name} and their political activities.
SKIP if the content is:
- Lottery results, sports scores, weather, entertainment gossip
- Generic news that only tangentially mentions the leader (e.g., in a sidebar)
- Not actually about the leader's actions, statements, or policies

If you should skip, return: {{"skip": true, "reason": "brief explanation"}}

OTHERWISE, write an AP-style news report:

IMPORTANT: Articles may be in Spanish, Portuguese, French, or other languages.
You MUST analyze all content and respond ONLY in English.
All titles and narratives must be in English — never output Spanish, Portuguese, or other languages.

Write an AP-style news report following inverted pyramid structure:
- Lead paragraph answers Who/What/Where/When
- Every claim attributed to a named source
- Dateline format: "CITY, Country —" (e.g., "KYIV, Ukraine —")
- Neutral verbs throughout ("said", "stated", not "declared", "proclaimed")
- Weave the leader's actions and any explicit positions into the narrative naturally
- New developments first, context later

CRITICAL - Factual accuracy:
- Names, species, places, numbers, and organizations must be copied EXACTLY from source text
- Do NOT substitute similar-sounding words (e.g., "pirarucu" is NOT "piranha")
- Before finalizing, verify that every specific noun in the headline appears verbatim in the narrative

Return JSON:
{{
    "title": "AP-style headline in present tense, max 10 words. Every noun must appear in the narrative.",
    "narrative": "Concise AP-style summary, 3-4 sentences MAX. Start with dateline (CITY, Country —). Lead with who/what/when. Attribute key claims. Focus on the essential facts only.",
    "scope": "international or domestic — 'international' if the event involves other countries, foreign leaders, or cross-border issues; 'domestic' if it is internal to {leader.country}"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.2,
                max_tokens=800,
            )
            data = extract_json_from_response(response)
            if data and "narrative" in data:
                return data
        except Exception as e:
            logger.warning(f"Event synthesis failed for '{event.title}': {e}")

        return None

    async def _event_to_story(
        self,
        event: ProcessedEvent,
        leader: LeaderConfig,
    ) -> Optional[Story]:
        """Convert a ProcessedEvent into a Story."""
        if not event.articles:
            return None

        synthesis = await self._synthesize_event(event, leader)

        # Check if LLM determined this event should be skipped (not about leader)
        if synthesis and synthesis.get("skip"):
            reason = synthesis.get("reason", "not relevant")
            logger.info(f"Skipping irrelevant event '{event.title[:50]}...': {reason}")
            return None

        if synthesis and synthesis.get("narrative"):
            title = synthesis.get("title", event.title)
            narrative = synthesis.get("narrative", event.title)
            scope_str = synthesis.get("scope", "domestic").lower()
        else:
            # Fallback: minimal story from event metadata
            title = event.title
            narrative = event.title
            scope_str = "domestic"

        # Ensure English output - detect and translate if needed
        if self._looks_non_english(title) or self._looks_non_english(narrative):
            logger.warning(f"Non-English content detected for '{title[:50]}...', translating")
            title, narrative = await self._ensure_english(title, narrative, leader)

        try:
            scope = StoryScope(scope_str)
        except ValueError:
            scope = StoryScope.DOMESTIC

        # Build source_refs: source_name -> [urls]
        source_refs: dict[str, list[str]] = {}
        for a in event.articles:
            name = a.get("source_name", "Unknown")
            url = a.get("url", "")
            if url:
                source_refs.setdefault(name, []).append(url)

        story_id = hashlib.md5(
            f"{leader.name}:{event.id}".encode()
        ).hexdigest()[:12]

        story = Story(
            id=story_id,
            title=title,
            narrative=narrative,
            scope=scope,
            source_count=event.source_count,
            has_wire=event.has_wire,
            score=event.score,
            source_refs=source_refs,
            entities=event.entities,
            cluster_id=event.id,
        )

        # Classify story for sorting overflow (Paragon taxonomy)
        story.classification = await self._classify_story(story, leader)

        return story

    async def _classify_story(
        self,
        story: Story,
        leader: LeaderConfig,
    ) -> ArticleClassification:
        """
        Classify a story using the Paragon taxonomy for sorting overflow stories.

        Classifies by event type, leader role, and impact level to calculate
        a priority score used when main stories are sorted by signal strength
        but overflow stories need tie-breaking.
        """
        prompt = f"""Classify this news story about {leader.name} ({leader.title} of {leader.country}).

HEADLINE: {story.title}

NARRATIVE: {story.narrative}

Classify by:

1. EVENT_TYPE - What kind of event?
   - POLICY_ANNOUNCEMENT: New policy, law, regulation, executive order
   - INTERNATIONAL_VISIT: Foreign travel, hosting foreign leaders
   - MAJOR_SPEECH: Significant public address, keynote
   - CABINET_CHANGE: Government personnel changes, appointments
   - LEGAL_DEVELOPMENT: Court rulings, investigations
   - BILATERAL_AGREEMENT: Treaties, deals, MOUs
   - CRISIS_RESPONSE: Emergency actions, disaster response
   - ECONOMIC_ACTION: Tariffs, sanctions, fiscal policy
   - OTHER: Doesn't fit above

2. LEADER_ROLE - Leader's role in this event?
   - INITIATOR: Leader is driving/announcing the action
   - PARTICIPANT: Leader involved but not primary driver
   - SUBJECT: Leader reported on passively

3. IMPACT_LEVEL - Geographic scope?
   - INTERNATIONAL: Affects multiple countries
   - NATIONAL: Affects leader's country broadly
   - REGIONAL: Sub-national region
   - LOCAL: Limited local impact

Return JSON:
{{
    "event_type": "EVENT_TYPE",
    "leader_role": "LEADER_ROLE",
    "impact_level": "IMPACT_LEVEL"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.1,
                max_tokens=200,
            )
            data = extract_json_from_response(response)

            if data:
                event_type = self._parse_event_type(data.get("event_type", "OTHER"))
                leader_role = self._parse_leader_role(data.get("leader_role", "SUBJECT"))
                impact_level = self._parse_impact_level(data.get("impact_level", "NATIONAL"))

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
                    reasoning="",
                )
        except Exception as e:
            logger.warning(f"Story classification failed for '{story.title[:50]}': {e}")

        # Default: low priority
        return ArticleClassification(
            event_type=EventType.OTHER,
            leader_role=LeaderRole.SUBJECT,
            impact_level=ImpactLevel.LOCAL,
            priority_score=0.0,
            reasoning="Default (classification failed)",
        )

    def _parse_event_type(self, value: str) -> EventType:
        """Parse event type string to enum."""
        value = value.upper().replace(" ", "_")
        try:
            return EventType(value.lower())
        except ValueError:
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

    async def _generate_between_the_lines(
        self,
        leader: LeaderConfig,
        stories: list[Story],
    ) -> list[str]:
        """
        Generate Between the Lines bullets from all stories.

        Identifies themes not immediately evident from individual stories,
        things to watch as events develop.
        """
        if not stories:
            return []

        story_summaries = "\n".join(
            f"- {s.title}: {s.narrative[:200]}"
            for s in stories[:10]
        )

        prompt = f"""Based on this week's stories about {leader.name} ({leader.title} of {leader.country}), identify 2-4 "Between the Lines" observations.

STORIES:
{story_summaries}

"Between the Lines" observations should be:
- Themes or patterns that may not be immediately evident from individual stories
- Things to watch as events develop
- Grounded in the week's content, not general trajectory speculation
- Each observation should be 1-2 sentences

Return JSON:
{{
    "observations": ["observation 1", "observation 2", "observation 3"]
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.4,
                max_tokens=600,
            )
            data = extract_json_from_response(response)
            if data and "observations" in data:
                return data["observations"][:4]
        except Exception as e:
            logger.warning(f"Between the lines generation failed for {leader.name}: {e}")

        return []

    def _events_to_articles(self, events: list[ProcessedEvent]) -> list[Article]:
        """Convert ProcessedEvents to Article objects for compatibility."""
        articles = []
        for event in events:
            for article_dict in event.articles:
                articles.append(Article(
                    id=article_dict.get("id", ""),
                    title=article_dict.get("title", ""),
                    url=article_dict.get("url", ""),
                    source_name=article_dict.get("source_name", ""),
                    source_type=article_dict.get("source_type", "domestic"),
                    content=article_dict.get("content", ""),
                    original_language=article_dict.get("language", "en"),
                ))
        return articles

    def _extract_events_from_processed(
        self,
        leader: LeaderConfig,
        events: list[ProcessedEvent],
    ) -> list[UnderlyingEvent]:
        """Convert ProcessedEvents to UnderlyingEvents for aggregate matching."""
        underlying = []
        for event in events:
            article_ids = [a.get("id", "") for a in event.articles]
            underlying.append(UnderlyingEvent(
                id=f"{leader.name}:{event.id}",
                description=event.title,
                leaders_involved=[leader.name],
                article_ids=article_ids,
            ))
        return underlying

    def _format_articles_for_prompt(self, articles: list[Article]) -> str:
        """Format articles for inclusion in prompt."""
        formatted = []
        for i, article in enumerate(articles):
            content = article.display_content
            if len(content) > 2000:
                content = content[:2000] + "..."

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
        """Create an empty dossier when no events are available."""
        return LeaderDossier(
            leader=leader,
            reporting_period="No coverage",
            main_stories=[],
            international_stories=[],
            domestic_stories=[],
            between_the_lines=[],
            articles=[],
            underlying_events=[],
            source_quality_notes="No articles fetched for this leader.",
        )

    def _looks_non_english(self, text: str) -> bool:
        """
        Quick heuristic check if text appears to be non-English.

        Checks for common Spanish/Portuguese/French patterns.
        """
        if not text:
            return False

        text_lower = text.lower()

        # Common non-English words that rarely appear in English news
        non_english_markers = [
            # Spanish
            " y ", " el ", " la ", " de ", " en ", " que ", " con ", " una ",
            " los ", " las ", " del ", " para ", " por ", " como ", " más ",
            " política ", " gobierno ", " presidente ",
            # Portuguese
            " o ", " e ", " da ", " do ", " em ", " um ", " uma ", " para ",
            " com ", " não ", " são ", " foi ", " sobre ",
            # French
            " le ", " les ", " et ", " une ", " des ", " dans ", " pour ",
            " sur ", " avec ", " est ", " sont ", " qui ",
        ]

        # Check for non-English patterns
        marker_count = sum(1 for marker in non_english_markers if marker in text_lower)
        if marker_count >= 2:
            return True

        # Check for accented characters common in Spanish/Portuguese/French
        accented_chars = sum(1 for c in text if c in "áéíóúñüàèìòùâêîôûçãõ")
        if accented_chars >= 3:
            return True

        return False

    async def _ensure_english(
        self,
        title: str,
        narrative: str,
        leader: LeaderConfig,
    ) -> tuple[str, str]:
        """Translate title and narrative to English if needed."""
        prompt = f"""Translate the following news content to English.

TITLE: {title}

NARRATIVE: {narrative}

Return JSON:
{{
    "title": "English headline, AP style, max 10 words",
    "narrative": "English narrative, same facts, AP style"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.1,
                max_tokens=500,
            )
            data = extract_json_from_response(response)
            if data and "title" in data and "narrative" in data:
                return data["title"], data["narrative"]
        except Exception as e:
            logger.warning(f"English translation failed: {e}")

        # Fallback: return originals with warning
        return f"[Translation needed] {title}", narrative
