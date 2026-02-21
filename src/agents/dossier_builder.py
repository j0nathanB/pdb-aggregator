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
    MODEL_SYNTHESIS,
    THINKING_SYNTHESIS,
    Story,
    StoryScope,
    UnderlyingEvent,
)
from .base import complete, with_retry, extract_json_from_response, batch_complete, BatchRequest
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

## AP Style Reference

DATELINES: Use the city name alone for major cities (LONDON, PARIS, TOKYO, BEIJING, MOSCOW,
WASHINGTON, JERUSALEM, CAIRO). For other cities use "CITY, Country" format: "KYIV, Ukraine",
"OTTAWA, Canada", "BRASILIA, Brazil". Use an em dash (—) after the dateline, not a hyphen.

ATTRIBUTION VERBS: Use "said" as the default. Acceptable alternatives: "stated", "told",
"announced", "reported", "noted", "added", "acknowledged", "confirmed", "denied". Never use:
"declared", "proclaimed", "revealed", "admitted", "confessed", "opined", "asserted", "claimed"
(implies doubt). Use "according to" for documents or unnamed sources.

NUMBERS: Spell out one through nine; use figures for 10 and above. Exceptions: ages, dates,
percentages, monetary amounts, and votes always use figures. Use "percent" not "%". Spell out
"million", "billion", "trillion" — write "$3.2 billion" not "$3,200,000,000".

TITLES: Capitalize formal titles before names: "President Macron", "Prime Minister Starmer".
Lowercase after names or standing alone: "Emmanuel Macron, the French president". Use first and
last name on first reference, last name only on subsequent references.

TIME REFERENCES: Use "Monday" not "last Monday" for days within the past week. Use specific
dates for older references: "Feb. 5" not "last Wednesday". Use "a.m." and "p.m." with periods.

## Paragon Taxonomy Reference

EVENT TYPES with definitions:
- POLICY_ANNOUNCEMENT: New policy, law, regulation, executive order, or formal government directive
- INTERNATIONAL_VISIT: Foreign travel by leader, hosting foreign leaders, state visits, summits
- MAJOR_SPEECH: Significant public address, keynote, parliamentary address, or UN speech
- CABINET_CHANGE: Government personnel changes, ministerial appointments, reshuffles, firings
- LEGAL_DEVELOPMENT: Court rulings, criminal investigations, indictments, judicial review
- BILATERAL_AGREEMENT: Treaties, trade deals, MOUs, defense pacts, formal accords
- CRISIS_RESPONSE: Emergency actions, disaster response, military mobilization, humanitarian aid
- ECONOMIC_ACTION: Tariffs, sanctions, fiscal policy, budget announcements, monetary decisions
- OTHER: Events not fitting above categories

LEADER ROLES:
- INITIATOR: Leader is the primary driver — announcing, proposing, directing the action
- PARTICIPANT: Leader is involved but not the primary driver — attending, responding, contributing
- SUBJECT: Leader is reported on passively — being investigated, criticized, assessed by others

IMPACT LEVELS:
- INTERNATIONAL: Affects multiple countries, cross-border implications, global significance
- NATIONAL: Affects the leader's country broadly, nationwide scope
- REGIONAL: Sub-national region, province, or state level impact
- LOCAL: Limited local impact, single city or municipality

## Output Format Specification

All responses must be valid JSON. String values must use proper escaping for quotes and
special characters. Enum values must match exactly (case-insensitive matching is applied).
Narrative text must not exceed 500 words. Headlines must not exceed 15 words.
"""


class DossierBuilderAgent:
    """
    Builds story-centric dossiers for each tracked leader.

    Synthesizes processed events into Top Stories, International,
    Domestic, and Between the Lines.
    """

    def _build_synthesize_prompt(
        self,
        event: "ProcessedEvent",
        leader: LeaderConfig,
    ) -> Optional[str]:
        """Build the synthesis prompt for a single event. Returns None if no articles."""
        if not event.articles:
            return None

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

        entity_context = ", ".join(
            f"{e.get('name', '')} ({e.get('type', '')})"
            for e in event.entities[:10]
        ) if event.entities else "No entities extracted"

        return f"""Synthesize this event about {leader.name} ({leader.title} of {leader.country}).

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
    "scope": "international or domestic — 'international' if the event involves other countries, foreign leaders, or cross-border issues; 'domestic' if it is internal to {leader.country}",
    "event_type": "One of: POLICY_ANNOUNCEMENT (new policy/law/regulation), INTERNATIONAL_VISIT (foreign travel/hosting foreign leaders), MAJOR_SPEECH (significant public address), CABINET_CHANGE (government personnel changes), LEGAL_DEVELOPMENT (court rulings/investigations), BILATERAL_AGREEMENT (treaties/deals/MOUs), CRISIS_RESPONSE (emergency actions), ECONOMIC_ACTION (tariffs/sanctions/fiscal policy), OTHER",
    "leader_role": "One of: INITIATOR (leader drives the action), PARTICIPANT (involved but not primary driver), SUBJECT (reported on passively)",
    "impact_level": "One of: INTERNATIONAL (affects multiple countries), NATIONAL (country-wide), REGIONAL (sub-national), LOCAL (limited local impact)"
}}
"""

    def _build_classify_prompt(
        self,
        story_title: str,
        story_narrative: str,
        leader: LeaderConfig,
    ) -> str:
        """Build the classification prompt for a synthesized story."""
        return f"""Classify this news story about {leader.name} ({leader.title} of {leader.country}).

HEADLINE: {story_title}

NARRATIVE: {story_narrative}

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

        # 4-5. Generate BTL + Executive Summary (single collapsed call)
        between_the_lines, executive_summary = await self._generate_btl_and_summary(
            leader, all_stories, main_stories, international_stories, domestic_stories
        )

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
            executive_summary=executive_summary,
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
        prompt = self._build_synthesize_prompt(event, leader)
        if prompt is None:
            return None

        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.2,
            )
            data = extract_json_from_response(response)
            if data and "narrative" in data:
                return data
            else:
                # Debug: log why extraction failed
                if data is None:
                    logger.warning(
                        f"JSON extraction failed for '{event.title[:50]}...'. "
                        f"Response preview: {response[:200]}..."
                    )
                elif "narrative" not in data:
                    logger.warning(
                        f"No 'narrative' in response for '{event.title[:50]}...'. "
                        f"Got keys: {list(data.keys())}"
                    )
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
            # Synthesis failed - skip this event rather than using title=narrative fallback
            logger.warning(
                f"Skipping event '{event.title[:50]}...' - synthesis failed (no narrative)"
            )
            return None

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
            embedding=event.embedding,  # Carry centroid for cross-leader semantic matching
        )

        # Extract classification from merged synthesis response
        story.classification = self._extract_classification(synthesis)

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
        prompt = self._build_classify_prompt(story.title, story.narrative, leader)
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.1,
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

    def _extract_classification(self, data: dict) -> ArticleClassification:
        """Extract classification from a merged synthesis+classification response."""
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

    async def _batch_synthesize_events(
        self,
        events: list["ProcessedEvent"],
        leader: LeaderConfig,
    ) -> dict[int, dict]:
        """
        Batch-synthesize all events via the Message Batches API.

        Returns a dict mapping event index to synthesis output dict.
        """
        requests: list[BatchRequest] = []
        index_map: dict[str, int] = {}  # custom_id -> event index

        for idx, event in enumerate(events):
            prompt = self._build_synthesize_prompt(event, leader)
            if prompt is None:
                continue
            custom_id = f"synth-{idx}"
            index_map[custom_id] = idx
            requests.append(BatchRequest(
                custom_id=custom_id,
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                model=MODEL_SYNTHESIS,
                thinking_budget=THINKING_SYNTHESIS,
                temperature=0.2,
            ))

        if not requests:
            return {}

        logger.info(
            f"Batch synthesizing {len(requests)} events for {leader.name}"
        )
        results = await batch_complete(requests)

        syntheses: dict[int, dict] = {}
        for custom_id, result in results.items():
            idx = index_map[custom_id]
            if not result.success:
                logger.warning(
                    f"Batch synthesis failed for event {idx} ({leader.name}): {result.error}"
                )
                continue
            data = extract_json_from_response(result.text)
            if data and ("narrative" in data or "skip" in data):
                syntheses[idx] = data
            else:
                logger.warning(
                    f"Batch synthesis JSON parse failed for event {idx} ({leader.name})"
                )

        return syntheses

    async def _batch_classify_stories(
        self,
        stories_by_idx: dict[int, Story],
        leader: LeaderConfig,
    ) -> dict[int, ArticleClassification]:
        """
        Batch-classify all stories via the Message Batches API.

        Returns a dict mapping event index to ArticleClassification.
        """
        requests: list[BatchRequest] = []
        index_map: dict[str, int] = {}

        for idx, story in stories_by_idx.items():
            custom_id = f"class-{idx}"
            index_map[custom_id] = idx
            requests.append(BatchRequest(
                custom_id=custom_id,
                prompt=self._build_classify_prompt(story.title, story.narrative, leader),
                system=DOSSIER_SYSTEM,
            ))

        if not requests:
            return {}

        logger.info(
            f"Batch classifying {len(requests)} stories for {leader.name}"
        )
        results = await batch_complete(requests)

        classifications: dict[int, ArticleClassification] = {}
        for custom_id, result in results.items():
            idx = index_map[custom_id]
            if not result.success:
                logger.warning(
                    f"Batch classification failed for story {idx} ({leader.name}): {result.error}"
                )
                continue
            data = extract_json_from_response(result.text)
            if data:
                event_type = self._parse_event_type(data.get("event_type", "OTHER"))
                leader_role = self._parse_leader_role(data.get("leader_role", "SUBJECT"))
                impact_level = self._parse_impact_level(data.get("impact_level", "NATIONAL"))
                priority_score = ArticleClassification.calculate_priority(
                    event_type=event_type,
                    leader_role=leader_role,
                    impact_level=impact_level,
                )
                classifications[idx] = ArticleClassification(
                    event_type=event_type,
                    leader_role=leader_role,
                    impact_level=impact_level,
                    priority_score=priority_score,
                    reasoning="",
                )

        return classifications

    async def build_from_events_batched(
        self,
        leader: LeaderConfig,
        top_events: list["ProcessedEvent"],
        remaining_events: list["ProcessedEvent"],
        opinions: list[dict] | None = None,
        date_start: str | None = None,
        date_end: str | None = None,
    ) -> LeaderDossier:
        """
        Build dossier using the Message Batches API for synthesis.

        Classification is merged into the synthesis prompt, so only one batch
        is needed. Falls back to sequential build_from_events() if batch fails.
        """
        logger.info(
            f"Building batched dossier for {leader.name} from "
            f"{len(top_events)} top + {len(remaining_events)} remaining events"
        )

        all_events = top_events + remaining_events
        if not all_events:
            return self._empty_dossier(leader)

        # Phase 1: Batch synthesize all events
        try:
            syntheses = await self._batch_synthesize_events(all_events, leader)
        except Exception as e:
            logger.warning(
                f"Batch synthesis failed for {leader.name}, falling back to sequential: {e}"
            )
            return await self.build_from_events(
                leader=leader,
                top_events=top_events,
                remaining_events=remaining_events,
                opinions=opinions,
                date_start=date_start,
                date_end=date_end,
            )

        # Build preliminary Story objects from synthesis results
        stories_by_idx: dict[int, Story] = {}
        for idx, synthesis in syntheses.items():
            event = all_events[idx]

            # Skip if LLM determined event is not relevant
            if synthesis.get("skip"):
                reason = synthesis.get("reason", "not relevant")
                logger.info(f"Skipping irrelevant event '{event.title[:50]}...': {reason}")
                continue

            if not synthesis.get("narrative"):
                logger.warning(
                    f"Skipping event '{event.title[:50]}...' - synthesis has no narrative"
                )
                continue

            title = synthesis.get("title", event.title)
            narrative = synthesis.get("narrative", event.title)
            scope_str = synthesis.get("scope", "domestic").lower()

            try:
                scope = StoryScope(scope_str)
            except ValueError:
                scope = StoryScope.DOMESTIC

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
                embedding=event.embedding,
            )

            # Extract classification from merged synthesis response
            story.classification = self._extract_classification(synthesis)
            stories_by_idx[idx] = story

        if not stories_by_idx:
            return self._empty_dossier(leader)

        # Sort and split (same logic as build_from_events)
        all_stories = list(stories_by_idx.values())
        all_stories.sort(key=lambda s: s.score, reverse=True)
        main_candidates = [s for s in all_stories if s.source_count >= 2]
        singletons = [s for s in all_stories if s.source_count < 2]

        main_stories = main_candidates[:5]
        overflow = main_candidates[5:] + singletons

        international_stories = [s for s in overflow if s.scope == StoryScope.INTERNATIONAL]
        domestic_stories = [s for s in overflow if s.scope == StoryScope.DOMESTIC]

        logger.info(
            f"Batched dossier for {leader.name}: {len(main_stories)} main (2+ sources), "
            f"{len(singletons)} singletons moved to overflow"
        )

        # BTL + executive summary (single collapsed call)
        between_the_lines, executive_summary = await self._generate_btl_and_summary(
            leader, all_stories, main_stories, international_stories, domestic_stories
        )

        underlying_events = self._extract_events_from_processed(leader, top_events)
        articles = self._events_to_articles(all_events)

        if date_start and date_end:
            reporting_period = f"{date_start} to {date_end}"
        else:
            reporting_period = self._get_reporting_period(articles)

        return LeaderDossier(
            leader=leader,
            reporting_period=reporting_period,
            executive_summary=executive_summary,
            main_stories=main_stories,
            international_stories=international_stories,
            domestic_stories=domestic_stories,
            between_the_lines=between_the_lines,
            articles=articles,
            underlying_events=underlying_events,
            source_quality_notes=self._assess_source_quality(articles, leader),
        )

    async def _generate_btl_and_summary(
        self,
        leader: LeaderConfig,
        all_stories: list[Story],
        main_stories: list[Story],
        international_stories: list[Story],
        domestic_stories: list[Story],
    ) -> tuple[list[str], str]:
        """
        Generate BTL observations and executive summary in a single CoT call.

        The exec summary depends on BTL output, so this is a natural chain.
        Returns (observations, summary). Falls back to ([], "") on failure.
        """
        if not all_stories:
            return [], ""

        story_summaries = "\n".join(
            f"- {s.title}: {s.narrative[:200]}"
            for s in all_stories[:10]
        )

        all_section_stories = main_stories + international_stories + domestic_stories
        story_bullets = "\n".join(
            f"- {s.title}" for s in all_section_stories[:10]
        )

        prompt = f"""Analyze this week's stories about {leader.name} ({leader.title} of {leader.country}).

STORIES WITH CONTEXT:
{story_summaries}

STORY HEADLINES:
{story_bullets}

Complete TWO tasks in order:

TASK 1 — "Between the Lines" observations:
- Identify 2-4 themes or patterns not immediately evident from individual stories
- Things to watch as events develop
- Grounded in the week's content, not general trajectory speculation
- Each observation should be 1-2 sentences

TASK 2 — Executive Summary:
Using the observations above as context, write 2-3 sentences that:
- Lead with the most significant development
- Capture the overall narrative of the week
- Use neutral, factual language (AP style)
- Focus on actions taken, not speculation

Return JSON:
{{
    "observations": ["observation 1", "observation 2", "observation 3"],
    "summary": "2-3 sentence executive summary"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.4,
            )
            data = extract_json_from_response(response)
            if data:
                observations = data.get("observations", [])[:4]
                summary = data.get("summary", "")
                if observations or summary:
                    return observations, summary
        except Exception as e:
            logger.warning(f"BTL+summary generation failed for {leader.name}: {e}")

        return [], ""

    async def _generate_between_the_lines(
        self,
        leader: LeaderConfig,
        stories: list[Story],
    ) -> list[str]:
        """
        Generate Between the Lines bullets from all stories.

        Deprecated: Use _generate_btl_and_summary() instead. Kept for fallback.
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
            )
            data = extract_json_from_response(response)
            if data and "observations" in data:
                return data["observations"][:4]
        except Exception as e:
            logger.warning(f"Between the lines generation failed for {leader.name}: {e}")

        return []

    async def _generate_executive_summary(
        self,
        leader: LeaderConfig,
        main_stories: list[Story],
        international_stories: list[Story],
        domestic_stories: list[Story],
        between_the_lines: list[str],
    ) -> str:
        """
        Generate a 2-3 sentence executive summary of the leader's week.

        Deprecated: Use _generate_btl_and_summary() instead. Kept for fallback.
        """
        all_stories = main_stories + international_stories + domestic_stories
        if not all_stories:
            return ""

        # Build story context
        story_bullets = "\n".join(
            f"- {s.title}" for s in all_stories[:10]
        )

        btl_context = ""
        if between_the_lines:
            btl_context = "\n\nKEY THEMES:\n" + "\n".join(
                f"- {b}" for b in between_the_lines[:3]
            )

        prompt = f"""Write a brief executive summary for {leader.name} ({leader.title} of {leader.country}) this week.

TOP STORIES:
{story_bullets}
{btl_context}

Write 2-3 sentences that:
- Lead with the most significant development
- Capture the overall narrative of the week
- Use neutral, factual language (AP style)
- Focus on actions taken, not speculation

Return JSON:
{{
    "summary": "2-3 sentence executive summary"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=DOSSIER_SYSTEM,
                temperature=0.3,
            )
            data = extract_json_from_response(response)
            if data and "summary" in data:
                return data["summary"]
        except Exception as e:
            logger.warning(f"Executive summary generation failed for {leader.name}: {e}")

        return ""

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
            )
            data = extract_json_from_response(response)
            if data and "title" in data and "narrative" in data:
                return data["title"], data["narrative"]
        except Exception as e:
            logger.warning(f"English translation failed: {e}")

        # Fallback: return originals with warning
        return f"[Translation needed] {title}", narrative
