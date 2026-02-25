"""
Clustering quality regression tests.

Makes real API calls, replays cluster fixtures through dedup and story arc detection.
Run with: pytest tests/test_clustering_quality.py -v --timeout=300

These tests validate that the analytical model tier (Sonnet + 4K thinking)
produces valid results for structural LLM tasks:
- Dedup returns valid merge groups with fewer or equal clusters
- Story arc detection returns valid index groups
- Story arc title merge produces a non-empty title
"""

import pytest

from src.clustering.dedup import deduplicate_clusters
from src.clustering.story_grouper import detect_story_arcs
from src.clustering.cluster_reasoning import reason_about_clusters  # Direct import to avoid circular


@pytest.mark.timeout(300)
class TestDeduplication:
    """Verify dedup with Sonnet produces valid results."""

    @pytest.mark.asyncio
    async def test_dedup_returns_valid_clusters(self, carney_clusters):
        """Dedup returns a list of clusters, no more than the input count."""
        clusters, leader_name = carney_clusters
        original_count = len(clusters)

        result = await deduplicate_clusters(clusters, leader_name)

        assert isinstance(result, list), "Dedup should return a list"
        assert len(result) > 0, "Dedup should return at least one cluster"
        assert len(result) <= original_count, (
            f"Dedup should not create new clusters: {len(result)} > {original_count}"
        )

        # Every cluster in the result should have snippets
        for cluster in result:
            assert len(cluster.snippets) > 0, (
                f"Cluster '{cluster.representative_title[:40]}' has no snippets"
            )

    @pytest.mark.asyncio
    async def test_dedup_preserves_all_snippets(self, carney_clusters):
        """Merging clusters should not lose snippets."""
        clusters, leader_name = carney_clusters
        original_snippet_count = sum(len(c.snippets) for c in clusters)

        result = await deduplicate_clusters(clusters, leader_name)

        result_snippet_count = sum(len(c.snippets) for c in result)
        assert result_snippet_count == original_snippet_count, (
            f"Dedup lost snippets: {original_snippet_count} -> {result_snippet_count}"
        )

    @pytest.mark.asyncio
    async def test_dedup_multilingual_clusters(self, sheinbaum_clusters):
        """Dedup handles Spanish-titled clusters without errors."""
        clusters, leader_name = sheinbaum_clusters
        result = await deduplicate_clusters(clusters, leader_name)

        assert isinstance(result, list)
        assert len(result) > 0


@pytest.mark.timeout(300)
class TestStoryArcDetection:
    """Verify story arc detection with Sonnet."""

    @pytest.mark.asyncio
    async def test_story_arcs_returns_valid_groups(self, carney_clusters):
        """Story arc detection returns valid index groups."""
        clusters, leader_name = carney_clusters
        titles = [c.representative_title for c in clusters]

        arcs = await detect_story_arcs(titles, leader_name)

        assert isinstance(arcs, list), "Should return a list of index groups"
        for arc in arcs:
            assert isinstance(arc, list), f"Each arc should be a list, got {type(arc)}"
            assert len(arc) >= 2, f"Each arc should have >= 2 indices, got {len(arc)}"
            for idx in arc:
                assert 0 <= idx < len(titles), (
                    f"Arc index {idx} out of range [0, {len(titles)})"
                )

    @pytest.mark.asyncio
    async def test_story_arcs_no_overlapping_indices(self, carney_clusters):
        """No event should appear in multiple arcs."""
        clusters, leader_name = carney_clusters
        titles = [c.representative_title for c in clusters]

        arcs = await detect_story_arcs(titles, leader_name)

        seen = set()
        for arc in arcs:
            for idx in arc:
                assert idx not in seen, (
                    f"Index {idx} ('{titles[idx][:40]}...') appears in multiple arcs"
                )
                seen.add(idx)


@pytest.mark.timeout(120)
class TestStoryArcTitleMerge:
    """Verify title merging with Sonnet."""

    @pytest.mark.asyncio
    async def test_cluster_reasoning_produces_valid_output(self, carney_clusters):
        """Combined cluster reasoning (dedup + arcs) returns valid clusters."""
        clusters, leader_name = carney_clusters

        result = await reason_about_clusters(clusters, leader_name)

        assert isinstance(result, list), f"Should return a list, got {type(result)}"
        assert len(result) > 0, "Should return at least one cluster"
        assert len(result) <= len(clusters), (
            f"Should not produce more clusters than input ({len(result)} > {len(clusters)})"
        )
        for c in result:
            assert len(c.representative_title) > 0, "Each cluster should have a title"
