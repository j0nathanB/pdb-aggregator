"""
Event scoring based on source diversity and coverage.

Scoring uses dynamic signals derived from the data:
- Velocity: articles per hour, normalized by time available (fixes "Friday news dump" bias)
- Semantic density: penalizes near-duplicate syndication without penalizing consensus
- Source diversity and wire coverage bonuses
"""
import logging
import math
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import numpy as np

from .clusterer import EventCluster, AUTHORITATIVE_SOURCE_TYPES

logger = logging.getLogger(__name__)

# High-signal keywords that indicate potentially important singletons
# These are rare, high-impact events that may not have trended yet
# Organized by category for maintainability
CRISIS_KEYWORDS = {
    "coup", "assassination", "assassinated", "martial law", "state of emergency",
    "declared war", "invasion", "nuclear", "missile strike", "terrorist attack",
    "mass shooting", "hostage", "kidnapped", "abducted",
}
POLITICAL_KEYWORDS = {
    "impeachment", "impeached", "indicted", "arrested", "resigned", "resigns",
    "steps down", "ousted", "removed from office", "corruption scandal",
    "bribery", "fraud charges", "criminal charges",
}
DIPLOMATIC_KEYWORDS = {
    "breaks ties", "severed relations", "recalled ambassador", "expelled diplomats",
    "sanctions imposed", "trade war", "blockade", "embargo",
}

# Combined set for fast lookup
HIGH_PRIORITY_KEYWORDS = CRISIS_KEYWORDS | POLITICAL_KEYWORDS | DIPLOMATIC_KEYWORDS

# Pre-compiled regex patterns with word boundaries to avoid substring traps
# e.g., "recouped" should NOT match "coup", "anti-nuclear" should NOT match "nuclear"
HIGH_PRIORITY_PATTERNS: dict[str, re.Pattern] = {
    keyword: re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    for keyword in HIGH_PRIORITY_KEYWORDS
}


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
    - Authoritative singleton boost (wire/official singletons get boost with recency decay)
    - Velocity (articles/hour normalized by time available - fixes "Friday news dump" bias)
    - Semantic density (penalizes syndication without penalizing consensus)
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
        # Velocity parameters (time-normalized arrival rate)
        velocity_min_span_hours: float = 0.5,  # Floor to prevent div-by-zero on simultaneous articles
        velocity_max_multiplier: float = 5.0,  # Cap to prevent extreme boosts
        # Semantic density parameters (penalize duplication, not consensus)
        duplication_threshold: float = 0.90,  # Similarity above this = near-duplicate
        duplication_max_penalty: float = 0.5,  # Max penalty when 100% are duplicates
        # High-priority keyword singleton boost (content-based rescue)
        # Singletons containing crisis/scandal keywords get boosted even without wire coverage
        keyword_singleton_boost: float = 2.0,  # Boost for keyword-containing singletons
    ):
        self.wire_bonus = wire_bonus
        self.diversity_weight = diversity_weight
        self.size_weight = size_weight
        self.authoritative_singleton_boost = authoritative_singleton_boost
        self.recency_full_boost_hours = recency_full_boost_hours
        self.recency_decay_hours = recency_decay_hours
        self.velocity_min_span_hours = velocity_min_span_hours
        self.velocity_max_multiplier = velocity_max_multiplier
        self.duplication_threshold = duplication_threshold
        self.duplication_max_penalty = duplication_max_penalty
        self.keyword_singleton_boost = keyword_singleton_boost

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

        # Singleton rescue: boost singletons that might be important signals
        # Two paths: (1) authoritative source, (2) high-priority keywords
        if cluster.unique_source_count == 1:
            is_authoritative = bool(cluster.source_types & AUTHORITATIVE_SOURCE_TYPES)
            has_priority_keywords = self._has_priority_keywords(cluster)

            # Path 1: Authoritative singleton boost (wire/official sources)
            if is_authoritative:
                boost = self._compute_recency_boost(cluster, now)
                if boost > 1.0:
                    logger.debug(
                        f"Authoritative singleton boost {boost:.2f}x for: "
                        f"'{cluster.representative_title[:50]}'"
                    )
                diversity_score *= boost

            # Path 2: Content-based priority boost (high-signal keywords)
            # This rescues singletons from non-wire sources breaking important news
            elif has_priority_keywords:
                boost = self._compute_recency_boost(cluster, now)
                # Use keyword boost instead of authoritative boost
                keyword_boost = 1.0 + (self.keyword_singleton_boost - 1.0) * (boost / self.authoritative_singleton_boost)
                keyword_boost = max(keyword_boost, 1.0)
                if keyword_boost > 1.0:
                    logger.info(
                        f"[Singleton Rescue] High-priority keywords detected, "
                        f"boost {keyword_boost:.2f}x for: '{cluster.representative_title[:50]}'"
                    )
                diversity_score *= keyword_boost

        # Size bonus (log scale to avoid domination by syndicated stories)
        size_score = math.log1p(len(cluster.snippets)) * self.size_weight

        base_score = diversity_score + size_score

        # Dynamic multipliers derived from cluster data
        velocity = self._compute_velocity(cluster, now)
        density = self._compute_semantic_density(cluster)

        final_score = base_score * velocity * density

        if velocity != 1.0 or density != 1.0:
            logger.debug(
                f"Score adjustments for '{cluster.representative_title[:40]}': "
                f"base={base_score:.2f}, velocity={velocity:.2f}x, density={density:.2f}x, "
                f"final={final_score:.2f}"
            )

        return final_score

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

    def _compute_velocity(self, cluster: EventCluster, pipeline_run_time: datetime) -> float:
        """
        Compute time-normalized velocity (articles per hour).

        Fixes "Friday news dump" bias: a story breaking Friday afternoon with 5 articles
        in 4 hours should score higher than a Monday story with 50 articles over 6 days.

        Returns multiplier >= 1.0 (velocity always boosts, never penalizes).
        """
        dates = self._parse_cluster_dates(cluster)
        if len(dates) < 2:
            return 1.0  # Singleton, no velocity signal

        first, last = min(dates), max(dates)

        # Floor: prevent div-by-zero for simultaneous articles (e.g., coordinated press release)
        span_hours = max((last - first).total_seconds() / 3600, self.velocity_min_span_hours)

        raw_velocity = len(cluster.snippets) / span_hours

        # Time boost: how much time did this story have to accumulate?
        # Friday story with 4 hours available gets boosted vs Monday story with 144 hours
        hours_available = max((pipeline_run_time - first).total_seconds() / 3600, 1.0)
        week_hours = 168.0

        # Logarithmic decay: rewards recentness without explosions
        # Monday (144h available): log(168/144) + 1 = 1.15x
        # Friday (4h available): log(168/4) + 1 = 4.7x
        time_boost = np.log(week_hours / hours_available) + 1.0

        # Cap final multiplier to prevent extreme boosts
        velocity_multiplier = min(raw_velocity * time_boost, self.velocity_max_multiplier)

        # Velocity should only boost, never penalize (floor at 1.0)
        return max(velocity_multiplier, 1.0)

    def _compute_semantic_density(self, cluster: EventCluster) -> float:
        """
        Compute semantic density penalty for near-duplicate syndication.

        Key insight: penalize DUPLICATION (exact copies), not CONSENSUS (agreement on facts).
        - High similarity (>0.90) = Redundant syndicated copies (bad)
        - Medium similarity (0.6-0.9) = Corroborated facts (good)
        - Low similarity (<0.6) = Noisy/unrelated (handled by clustering)

        Returns multiplier in [1.0 - max_penalty, 1.0].
        """
        if len(cluster.snippets) < 2:
            return 1.0  # Singleton, assume novel

        embeddings = np.vstack([s.embedding for s in cluster.snippets])
        sim_matrix = embeddings @ embeddings.T

        # Get upper triangle excluding diagonal (self-similarity)
        triu_indices = np.triu_indices(len(cluster.snippets), k=1)
        similarities = sim_matrix[triu_indices]

        # What fraction of pairs are near-duplicates?
        redundancy_ratio = float(np.mean(similarities > self.duplication_threshold))

        # If 100% of articles are duplicates, apply max penalty
        # If 0% are duplicates, no penalty (1.0x)
        density_multiplier = 1.0 - (redundancy_ratio * self.duplication_max_penalty)

        return density_multiplier

    def _parse_cluster_dates(self, cluster: EventCluster) -> list[datetime]:
        """Parse all valid dates from cluster snippets."""
        dates = []
        for snippet in cluster.snippets:
            if not snippet.date:
                continue
            try:
                parsed = date_parser.parse(snippet.date, fuzzy=True)
                # Handle timezone-naive comparison
                if parsed.tzinfo is not None:
                    parsed = parsed.replace(tzinfo=None)
                dates.append(parsed)
            except (ValueError, TypeError):
                continue
        return dates

    def _has_priority_keywords(self, cluster: EventCluster) -> bool:
        """
        Check if cluster content contains high-priority keywords.

        These are rare, high-impact terms (coup, assassination, impeachment, etc.)
        that indicate a potentially important signal even from a single source.
        This enables "singleton rescue" for breaking news that hasn't trended yet.

        Uses word-boundary regex to avoid substring traps:
        - "recouped" does NOT match "coup"
        - "anti-nuclear" does NOT match "nuclear"
        """
        # Combine all text from cluster snippets
        text_parts = []
        for snippet in cluster.snippets:
            text_parts.append(snippet.title)
            text_parts.append(snippet.snippet)

        combined_text = " ".join(text_parts)

        # Check for any high-priority keyword using word-boundary regex
        for keyword, pattern in HIGH_PRIORITY_PATTERNS.items():
            if pattern.search(combined_text):
                logger.debug(
                    f"Priority keyword '{keyword}' found in: "
                    f"'{cluster.representative_title[:50]}'"
                )
                return True

        return False

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
