"""
Event scoring based on source diversity and coverage.
"""
import logging
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from dateutil import parser as date_parser

from .clusterer import EventCluster, AUTHORITATIVE_SOURCE_TYPES

logger = logging.getLogger(__name__)


@dataclass
class ScoredEvent:
    """An event cluster with importance score."""
    cluster: EventCluster
    score: float
    rank: int = 0


class EventScorer:
    """
    Scores event clusters for importance.

    Scoring factors:
    - Source diversity (more unique sources = more important)
    - Wire coverage (wire service coverage = more important)
    - Cluster size (more articles = more important, but diminishing returns)
    - Authoritative singleton boost (wire/official singletons get 2.5x with recency decay)
    """

    def __init__(
        self,
        wire_bonus: float = 1.5,
        diversity_weight: float = 1.0,
        size_weight: float = 0.5,
        # Authoritative singleton boost parameters
        # 2.1x makes wire singletons competitive with (but not beat) 2-source clusters
        authoritative_singleton_boost: float = 2.1,
        recency_full_boost_hours: float = 4.0,  # Full boost for first N hours
        recency_decay_hours: float = 24.0,  # Decay to 1.0x over this period
    ):
        self.wire_bonus = wire_bonus
        self.diversity_weight = diversity_weight
        self.size_weight = size_weight
        self.authoritative_singleton_boost = authoritative_singleton_boost
        self.recency_full_boost_hours = recency_full_boost_hours
        self.recency_decay_hours = recency_decay_hours

    def score_events(
        self,
        clusters: list[EventCluster],
        now: datetime | None = None,
    ) -> list[ScoredEvent]:
        """
        Score and rank event clusters.

        Args:
            clusters: List of event clusters
            now: Reference time for recency calculations (defaults to now)

        Returns:
            List of ScoredEvents, sorted by score descending
        """
        if now is None:
            now = datetime.now()

        scored = []

        for cluster in clusters:
            score = self._compute_score(cluster, now)
            scored.append(ScoredEvent(cluster=cluster, score=score))

        # Sort by score descending
        scored.sort(key=lambda x: x.score, reverse=True)

        # Assign ranks
        for i, event in enumerate(scored):
            event.rank = i + 1

        return scored

    def _compute_score(self, cluster: EventCluster, now: datetime | None = None) -> float:
        """Compute importance score for a cluster."""
        if now is None:
            now = datetime.now()

        # Base: unique source count
        diversity_score = cluster.unique_source_count * self.diversity_weight

        # Wire coverage bonus
        if cluster.has_wire_coverage:
            diversity_score *= self.wire_bonus

        # Authoritative singleton boost: wire/official singletons get elevated
        # with recency decay so fresh breaking news competes with multi-source clusters
        if cluster.unique_source_count == 1:
            is_authoritative = bool(cluster.source_types & AUTHORITATIVE_SOURCE_TYPES)
            if is_authoritative:
                boost = self._compute_recency_boost(cluster, now)
                if boost > 1.0:
                    logger.debug(
                        f"Authoritative singleton boost {boost:.2f}x for: "
                        f"'{cluster.representative_title[:50]}'"
                    )
                diversity_score *= boost

        # Size bonus (log scale to avoid domination by syndicated stories)
        size_score = math.log1p(len(cluster.snippets)) * self.size_weight

        return diversity_score + size_score

    def _compute_recency_boost(self, cluster: EventCluster, now: datetime) -> float:
        """
        Compute recency-based boost for authoritative singletons.

        Returns boost multiplier:
        - Full boost (2.5x) for content < recency_full_boost_hours old
        - Linear decay to 1.0x over recency_decay_hours
        - 1.0x (no boost) for older content
        """
        # Get the most recent date from cluster snippets
        latest_date = None
        for snippet in cluster.snippets:
            if not snippet.date:
                continue
            try:
                parsed = date_parser.parse(snippet.date, fuzzy=True)
                if latest_date is None or parsed > latest_date:
                    latest_date = parsed
            except (ValueError, TypeError):
                continue

        if latest_date is None:
            # No parseable date, assume moderately fresh (12h old)
            age_hours = 12.0
        else:
            # Handle timezone-naive comparison
            if latest_date.tzinfo is not None:
                latest_date = latest_date.replace(tzinfo=None)
            age_hours = (now - latest_date).total_seconds() / 3600

        # Fresh content: full boost
        if age_hours <= self.recency_full_boost_hours:
            return self.authoritative_singleton_boost

        # Decay period: linear interpolation from full boost to 1.0
        if age_hours <= self.recency_decay_hours:
            decay_range = self.recency_decay_hours - self.recency_full_boost_hours
            elapsed = age_hours - self.recency_full_boost_hours
            decay_fraction = elapsed / decay_range
            boost_range = self.authoritative_singleton_boost - 1.0
            return self.authoritative_singleton_boost - (decay_fraction * boost_range)

        # Old content: no boost
        return 1.0

    def filter_top_events(
        self,
        scored_events: list[ScoredEvent],
        max_events: int = 5,
        min_score_ratio: float = 0.5,
    ) -> tuple[list[ScoredEvent], list[ScoredEvent]]:
        """
        Split events into top (for brief) and rest (for dossier).

        Args:
            scored_events: Scored and ranked events
            max_events: Maximum events for brief
            min_score_ratio: Include events with score >= top_score * ratio

        Returns:
            Tuple of (top_events, remaining_events)
        """
        if not scored_events:
            return [], []

        top_score = scored_events[0].score
        threshold = top_score * min_score_ratio

        top = []
        rest = []

        for event in scored_events:
            if len(top) < max_events and event.score >= threshold:
                top.append(event)
            else:
                rest.append(event)

        return top, rest
