"""
Aggregate Briefing Builder - Synthesizes per-leader dossiers into aggregate briefing.

Replaces ThreadDetectorAgent. Identifies overlapping stories across leaders
via entity URI overlap and builds aggregate Top Stories, International,
Domestic, and Between the Lines.
"""

import logging
import hashlib
from collections import defaultdict
from typing import Optional

from ..config import (
    LeaderDossier,
    Story,
    StoryScope,
)
from ..clustering import validate_cross_leader_match
from .base import complete, with_retry, extract_json_from_response

logger = logging.getLogger(__name__)


AGGREGATE_SYSTEM = """You are a Senior Editor for the Associated Press. Your writing is objective,
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


class AggregateBriefingBuilder:
    """
    Builds the aggregate briefing from per-leader dossiers.

    Steps:
    1. Collect all stories from all dossiers
    2. Match overlapping stories across leaders via entity URI overlap
    3. Synthesize shared stories into combined narratives
    4. Select aggregate Top Stories (up to 5, 2+ sources required, sorted by score)
    5. Sort overflow by classification priority (Paragon taxonomy), limit to 7
    6. Distribute overflow to International/Domestic by scope
    7. Generate Between the Lines (thematic + per-leader)
    """

    async def build(
        self,
        dossiers: dict[str, LeaderDossier],
    ) -> tuple[list[Story], list[Story], list[Story], list[str], str]:
        """
        Build aggregate briefing from leader dossiers.

        Args:
            dossiers: Map of leader name to LeaderDossier

        Returns:
            Tuple of (main_stories, intl_stories, dom_stories, between_the_lines, executive_summary)
        """
        logger.info(f"Building aggregate briefing from {len(dossiers)} dossiers")

        # 1. Collect all stories from all dossiers
        all_stories = self._collect_all_stories(dossiers)
        if not all_stories:
            return [], [], [], [], ""

        # 2. Find overlapping stories across leaders (entity-based matching)
        shared_groups, standalone = self._find_shared_stories(all_stories)
        logger.info(
            f"Found {len(shared_groups)} candidate shared groups, "
            f"{len(standalone)} standalone stories"
        )

        # 2.5 Validate shared groups are thematically related (LLM gate)
        validated_groups, rejected_stories = await self._validate_shared_groups(
            shared_groups
        )
        standalone.extend(rejected_stories)
        logger.info(
            f"After thematic validation: {len(validated_groups)} valid groups, "
            f"{len(rejected_stories)} rejected (moved to standalone)"
        )

        # 3. Synthesize validated shared stories
        merged_stories: list[Story] = []
        for group in validated_groups:
            merged = await self._synthesize_shared_story(group)
            if merged:
                merged_stories.append(merged)

        # 4. Combine merged + standalone, select Main Stories
        all_candidates = merged_stories + standalone

        # Score bonus for multi-leader stories
        for story in all_candidates:
            if len(story.contributing_leaders) > 1:
                story.score *= (1.0 + 0.2 * len(story.contributing_leaders))

        all_candidates.sort(key=lambda s: s.score, reverse=True)

        # Only stories with 2+ sources are eligible for main_stories
        main_candidates = [s for s in all_candidates if s.source_count >= 2]
        singletons = [s for s in all_candidates if s.source_count < 2]

        main_stories = main_candidates[:5]
        overflow = main_candidates[5:] + singletons

        logger.info(
            f"Aggregate main: {len(main_stories)} stories (2+ sources), "
            f"{len(singletons)} singletons moved to overflow"
        )

        # 5. Sort overflow by classification priority (Paragon taxonomy) and limit to 7
        # Classification breaks ties when signal strength (score) is similar
        def classification_priority(story: Story) -> float:
            if story.classification:
                return story.classification.priority_score
            return 0.0

        overflow.sort(key=lambda s: (classification_priority(s), s.score), reverse=True)
        overflow = overflow[:7]  # Limit briefs section to 7 stories

        # 6. Distribute remaining by scope
        intl_stories = [s for s in overflow if s.scope == StoryScope.INTERNATIONAL]
        dom_stories = [s for s in overflow if s.scope == StoryScope.DOMESTIC]

        # 7. Generate Between the Lines
        between_the_lines = await self._generate_between_the_lines(
            all_candidates, dossiers
        )

        # 8. Generate Executive Summary
        executive_summary = await self._generate_executive_summary(
            main_stories, dossiers
        )

        logger.info(
            f"Aggregate: {len(main_stories)} main, "
            f"{len(intl_stories)} intl, {len(dom_stories)} dom, "
            f"{len(between_the_lines)} BTL bullets"
        )

        return main_stories, intl_stories, dom_stories, between_the_lines, executive_summary

    def _collect_all_stories(
        self,
        dossiers: dict[str, LeaderDossier],
    ) -> list[tuple[str, Story]]:
        """Collect all stories from all dossiers, tagged with leader name."""
        all_stories = []
        for leader_name, dossier in dossiers.items():
            for story in (
                dossier.main_stories
                + dossier.international_stories
                + dossier.domestic_stories
            ):
                # Tag story with its leader
                if not story.contributing_leaders:
                    story.contributing_leaders = [leader_name]
                all_stories.append((leader_name, story))
        return all_stories

    def _find_shared_stories(
        self,
        tagged_stories: list[tuple[str, Story]],
        min_entity_overlap: int = 3,
        max_group_size: int = 4,
    ) -> tuple[list[list[tuple[str, Story]]], list[Story]]:
        """
        Find stories that overlap across leaders using entity URI overlap.

        Two stories are candidates for merging if they share min_entity_overlap+
        high-salience entity URIs and come from different leaders.

        Groups are limited to max_group_size to prevent mega-clusters from
        transitive chaining.

        Returns:
            (shared_groups, standalone_stories)
        """
        # Build entity URI index
        story_entities: dict[int, set[str]] = {}
        for idx, (leader, story) in enumerate(tagged_stories):
            uris = set()
            for entity in story.entities:
                uri = entity.get("uri", entity.get("name", ""))
                if uri:
                    uris.add(uri)
            story_entities[idx] = uris

        # Find pairs with sufficient shared entities from different leaders
        n = len(tagged_stories)
        merged_into: dict[int, int] = {}  # idx -> group_id

        groups: dict[int, list[int]] = {}
        next_group = 0

        for i in range(n):
            for j in range(i + 1, n):
                leader_i = tagged_stories[i][0]
                leader_j = tagged_stories[j][0]

                # Must be different leaders
                if leader_i == leader_j:
                    continue

                # Check entity overlap (raised threshold to prevent weak matches)
                overlap = story_entities[i] & story_entities[j]
                if len(overlap) < min_entity_overlap:
                    continue

                # Found a match - merge groups (with size limit)
                group_i = merged_into.get(i)
                group_j = merged_into.get(j)

                if group_i is not None and group_j is not None:
                    # No transitivity: don't merge existing groups together
                    # This prevents A-B + B-C from chaining into A-B-C
                    pass
                elif group_i is not None:
                    if len(groups[group_i]) < max_group_size:
                        groups[group_i].append(j)
                        merged_into[j] = group_i
                elif group_j is not None:
                    if len(groups[group_j]) < max_group_size:
                        groups[group_j].append(i)
                        merged_into[i] = group_j
                else:
                    groups[next_group] = [i, j]
                    merged_into[i] = next_group
                    merged_into[j] = next_group
                    next_group += 1

        # Build output
        shared_groups = []
        for group_id, indices in groups.items():
            group = [tagged_stories[idx] for idx in set(indices)]
            shared_groups.append(group)

        standalone_indices = set(range(n)) - set(merged_into.keys())
        standalone = [tagged_stories[idx][1] for idx in standalone_indices]

        logger.info(
            f"Entity matching: {len(shared_groups)} groups (max {max_group_size}), "
            f"{len(standalone)} standalone (threshold: {min_entity_overlap}+ entities)"
        )

        return shared_groups, standalone

    async def _validate_shared_groups(
        self,
        shared_groups: list[list[tuple[str, Story]]],
    ) -> tuple[list[list[tuple[str, Story]]], list[Story]]:
        """
        Validate that entity-matched story groups are thematically related.

        Uses LLM to confirm stories are about the same topic before merging.
        Stories that fail validation are returned as rejected (standalone).

        Returns:
            (validated_groups, rejected_stories)
        """
        validated: list[list[tuple[str, Story]]] = []
        rejected: list[Story] = []

        for group in shared_groups:
            if len(group) < 2:
                # Single story, no validation needed
                validated.append(group)
                continue

            # Build summaries for validation
            summaries = [
                (leader, story.title, story.narrative)
                for leader, story in group
            ]

            # Validate thematic relationship
            is_related = await validate_cross_leader_match(summaries)

            if is_related:
                validated.append(group)
            else:
                # Move all stories in this group to standalone
                for leader, story in group:
                    rejected.append(story)
                leaders = [leader for leader, _ in group]
                logger.info(
                    f"Rejected cross-leader group (not thematically related): "
                    f"{leaders}"
                )

        return validated, rejected

    @with_retry(max_attempts=2)
    async def _synthesize_shared_story(
        self,
        group: list[tuple[str, Story]],
    ) -> Optional[Story]:
        """
        Synthesize a shared story from multiple leaders' versions.

        Merges narratives into a combined Story with contributing_leaders set.
        """
        if not group:
            return None

        leaders = list(set(leader for leader, _ in group))
        stories = [story for _, story in group]

        # Use the highest-scoring story as the base
        stories.sort(key=lambda s: s.score, reverse=True)
        base = stories[0]

        # Build context for synthesis
        leader_perspectives = []
        for leader, story in group:
            leader_perspectives.append(f"{leader}: {story.narrative}")

        perspectives_text = "\n\n".join(leader_perspectives)

        prompt = f"""Synthesize these perspectives on the same story from different leaders into a single combined summary.

STORY: {base.title}

PERSPECTIVES:
{perspectives_text}

Write a concise combined summary covering all leaders' involvement.

Return JSON:
{{
    "title": "Combined story title, max 12 words",
    "narrative": "Concise AP-style summary, 3-4 sentences MAX. Start with dateline. Cover each leader's role briefly. Focus on essential facts only."
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=AGGREGATE_SYSTEM,
                temperature=0.3,
                max_tokens=600,
            )
            data = extract_json_from_response(response)
        except Exception as e:
            logger.warning(f"Shared story synthesis failed: {e}")
            data = None

        if not data:
            # Fallback: use the best single story
            base.contributing_leaders = leaders
            return base

        # Merge source_refs from all stories
        merged_refs: dict[str, list[str]] = {}
        merged_entities: list[dict] = []
        seen_uris: set[str] = set()

        for story in stories:
            for src_name, urls in story.source_refs.items():
                merged_refs.setdefault(src_name, []).extend(urls)
            for entity in story.entities:
                uri = entity.get("uri", entity.get("name", ""))
                if uri not in seen_uris:
                    seen_uris.add(uri)
                    merged_entities.append(entity)

        # Aggregate source count and score
        total_sources = sum(s.source_count for s in stories)
        max_score = max(s.score for s in stories)
        has_wire = any(s.has_wire for s in stories)

        story_id = hashlib.md5(
            f"shared:{'|'.join(sorted(leaders))}:{base.cluster_id}".encode()
        ).hexdigest()[:12]

        return Story(
            id=story_id,
            title=data.get("title", base.title),
            narrative=data.get("narrative", base.narrative),
            scope=base.scope,
            source_count=total_sources,
            has_wire=has_wire,
            score=max_score,
            source_refs=merged_refs,
            entities=merged_entities,
            cluster_id=base.cluster_id,
            contributing_leaders=leaders,
        )

    async def _generate_between_the_lines(
        self,
        all_stories: list[Story],
        dossiers: dict[str, LeaderDossier],
    ) -> list[str]:
        """
        Generate aggregate Between the Lines.

        Two parts:
        1. Thematic analysis across all stories
        2. Per-leader BTL bullets prefixed with leader name
        """
        btl_bullets: list[str] = []

        # Part 1: Thematic analysis via LLM
        if all_stories:
            thematic = await self._generate_thematic_btl(all_stories)
            btl_bullets.extend(thematic)

        # Part 2: Pull per-leader BTL bullets
        for leader_name, dossier in dossiers.items():
            for bullet in dossier.between_the_lines[:2]:  # max 2 per leader
                btl_bullets.append(f"{leader_name}: {bullet}")

        return btl_bullets

    async def _generate_thematic_btl(
        self,
        stories: list[Story],
    ) -> list[str]:
        """Generate thematic Between the Lines from aggregate stories."""
        story_summaries = "\n".join(
            f"- {s.title} (leaders: {', '.join(s.contributing_leaders) if s.contributing_leaders else 'N/A'}): "
            f"{s.narrative[:150]}"
            for s in stories[:15]
        )

        prompt = f"""Based on these stories from this week's briefing on world leaders, identify 2-3 cross-cutting themes or connections.

STORIES:
{story_summaries}

"Between the Lines" observations should be:
- Themes or connections across different leaders/regions
- Patterns not immediately obvious from individual stories
- Things to watch as events develop
- Each observation should be 1-2 sentences

Return JSON:
{{
    "observations": ["observation 1", "observation 2"]
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=AGGREGATE_SYSTEM,
                temperature=0.4,
                max_tokens=500,
            )
            data = extract_json_from_response(response)
            if data and "observations" in data:
                return data["observations"][:3]
        except Exception as e:
            logger.warning(f"Thematic BTL generation failed: {e}")

        return []

    async def _generate_executive_summary(
        self,
        main_stories: list[Story],
        dossiers: dict[str, LeaderDossier],
    ) -> str:
        """
        Generate a 2-4 sentence executive summary of the week's key developments.

        Distills the main stories and cross-cutting themes into a brief
        overview suitable for quick scanning at the top of the aggregate brief.
        """
        if not main_stories:
            return ""

        # Build story context from main stories
        story_bullets = "\n".join(
            f"- {s.title} ({', '.join(s.contributing_leaders) if s.contributing_leaders else 'N/A'})"
            for s in main_stories[:7]
        )

        # Get leader summaries if available
        leader_context = ""
        summaries = [
            f"- {name}: {d.executive_summary}"
            for name, d in dossiers.items()
            if d.executive_summary
        ]
        if summaries:
            leader_context = "\n\nLEADER SUMMARIES:\n" + "\n".join(summaries[:5])

        prompt = f"""Write a brief executive summary for this week's global leadership briefing.

TOP STORIES:
{story_bullets}
{leader_context}

Write 2-4 sentences that:
- Lead with the dominant theme or most significant development
- Capture key tensions, diplomatic moves, or policy shifts
- Reference specific leaders and their actions
- Use neutral, factual language (AP style)
- Connect developments across regions where relevant

Return JSON:
{{
    "summary": "2-4 sentence executive summary"
}}
"""
        try:
            response = await complete(
                prompt=prompt,
                system=AGGREGATE_SYSTEM,
                temperature=0.3,
                max_tokens=400,
            )
            data = extract_json_from_response(response)
            if data and "summary" in data:
                return data["summary"]
        except Exception as e:
            logger.warning(f"Aggregate executive summary generation failed: {e}")

        return ""
