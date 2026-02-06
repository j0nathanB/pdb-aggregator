"""
Event scoring based on source diversity and coverage.
"""
import math
from dataclasses import dataclass
from .clusterer import EventCluster


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
    """

    def __init__(
        self,
        wire_bonus: float = 1.5,
        diversity_weight: float = 1.0,
        size_weight: float = 0.5,
    ):
        self.wire_bonus = wire_bonus
        self.diversity_weight = diversity_weight
        self.size_weight = size_weight

    def score_events(
        self,
        clusters: list[EventCluster],
    ) -> list[ScoredEvent]:
        """
        Score and rank event clusters.

        Args:
            clusters: List of event clusters

        Returns:
            List of ScoredEvents, sorted by score descending
        """
        scored = []

        for cluster in clusters:
            score = self._compute_score(cluster)
            scored.append(ScoredEvent(cluster=cluster, score=score))

        # Sort by score descending
        scored.sort(key=lambda x: x.score, reverse=True)

        # Assign ranks
        for i, event in enumerate(scored):
            event.rank = i + 1

        return scored

    def _compute_score(self, cluster: EventCluster) -> float:
        """Compute importance score for a cluster."""
        # Base: unique source count
        diversity_score = cluster.unique_source_count * self.diversity_weight

        # Wire coverage bonus
        if cluster.has_wire_coverage:
            diversity_score *= self.wire_bonus

        # Size bonus (log scale to avoid domination by syndicated stories)
        size_score = math.log1p(len(cluster.snippets)) * self.size_weight

        return diversity_score + size_score

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
