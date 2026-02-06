"""
LLM-based cluster deduplication.

After HDBSCAN clustering, this module asks an LLM to identify clusters
that represent the same event and should be merged.
"""

import logging
from typing import Optional
import numpy as np

from .clusterer import EventCluster
from ..agents.base import complete, extract_json_from_response, with_retry

logger = logging.getLogger(__name__)


DEDUP_SYSTEM = """You are a news editor identifying duplicate story clusters.

Given a list of news story clusters (each with a title and snippet), identify
which clusters are about THE SAME EVENT and should be merged.

Two clusters are the same event if they describe the same specific occurrence:
- Same person doing the same thing at the same time/place
- Different sources covering the same announcement, speech, or incident

Two clusters are NOT the same event if:
- They're about the same general topic but different specific occurrences
- They're about the same person but different events on different days
- One is a reaction/follow-up to the other (those are related but distinct)

Return your answer as JSON."""


@with_retry(max_attempts=2)
async def deduplicate_clusters(
    clusters: list[EventCluster],
    leader_name: str,
) -> list[EventCluster]:
    """
    Use LLM to identify and merge duplicate clusters.

    Args:
        clusters: List of EventClusters from HDBSCAN
        leader_name: Name of the leader (for context)

    Returns:
        Deduplicated list of EventClusters
    """
    if len(clusters) < 2:
        return clusters

    # Build cluster summary for LLM
    cluster_summaries = []
    for i, cluster in enumerate(clusters):
        # Get representative title and first snippet
        title = cluster.representative_title
        snippet = cluster.snippets[0].snippet if cluster.snippets else ""
        sources = ", ".join(list(cluster.sources)[:3])

        cluster_summaries.append(
            f"{i}. [{sources}] {title}\n   {snippet[:150]}..."
        )

    summaries_text = "\n\n".join(cluster_summaries)

    prompt = f"""Review these {len(clusters)} news clusters about {leader_name}.

CLUSTERS:
{summaries_text}

Which clusters are about THE SAME EVENT and should be merged?

Return JSON:
{{
    "merge_groups": [
        [0, 3, 5],  // cluster indices that are the same event
        [1, 7]      // another group of duplicates
    ],
    "reasoning": "Brief explanation of why these are duplicates"
}}

If no clusters should be merged, return: {{"merge_groups": [], "reasoning": "All clusters are distinct events"}}
"""

    response = await complete(
        prompt=prompt,
        system=DEDUP_SYSTEM,
        temperature=0.1,  # Low temp for consistent judgment
        max_tokens=500,
    )

    data = extract_json_from_response(response)

    if not data or "merge_groups" not in data:
        logger.warning("Failed to parse dedup response, returning original clusters")
        return clusters

    merge_groups = data.get("merge_groups", [])
    reasoning = data.get("reasoning", "")

    if not merge_groups:
        logger.info(f"No duplicates found for {leader_name}: {reasoning}")
        return clusters

    logger.info(
        f"Found {len(merge_groups)} duplicate groups for {leader_name}: {reasoning}"
    )

    # Merge clusters
    return _merge_cluster_groups(clusters, merge_groups)


def _merge_cluster_groups(
    clusters: list[EventCluster],
    merge_groups: list[list[int]],
) -> list[EventCluster]:
    """
    Merge clusters according to the groups specified.

    Args:
        clusters: Original cluster list
        merge_groups: List of index groups to merge, e.g. [[0, 3, 5], [1, 7]]

    Returns:
        New list with merged clusters
    """
    # Track which clusters have been merged
    merged_indices: set[int] = set()
    result: list[EventCluster] = []

    for group in merge_groups:
        # Validate indices
        valid_indices = [i for i in group if 0 <= i < len(clusters)]
        if len(valid_indices) < 2:
            continue

        # Merge this group
        merged = _merge_clusters([clusters[i] for i in valid_indices])
        result.append(merged)
        merged_indices.update(valid_indices)

        logger.debug(
            f"Merged clusters {valid_indices} -> '{merged.representative_title[:60]}'"
        )

    # Add unmerged clusters
    for i, cluster in enumerate(clusters):
        if i not in merged_indices:
            result.append(cluster)

    return result


def _merge_clusters(clusters: list[EventCluster]) -> EventCluster:
    """
    Merge multiple clusters into one.

    - Combines all snippets
    - Recomputes centroid
    - Uses ID from largest cluster
    """
    # Sort by size to pick ID from largest
    clusters_sorted = sorted(clusters, key=lambda c: len(c.snippets), reverse=True)
    base = clusters_sorted[0]

    # Combine all snippets
    all_snippets = []
    for cluster in clusters:
        all_snippets.extend(cluster.snippets)

    # Recompute centroid
    embeddings = np.vstack([s.embedding for s in all_snippets])
    centroid = embeddings.mean(axis=0)
    centroid = centroid / np.linalg.norm(centroid)

    merged = EventCluster(
        id=f"merged_{base.id}",
        snippets=all_snippets,
        centroid=centroid,
    )

    logger.info(
        f"Merged {len(clusters)} clusters ({sum(len(c.snippets) for c in clusters)} snippets) "
        f"-> '{merged.representative_title[:60]}'"
    )

    return merged


# =============================================================================
# OPTIONAL: Hybrid approach - algorithmic pre-filter + LLM
# =============================================================================

async def deduplicate_clusters_hybrid(
    clusters: list[EventCluster],
    leader_name: str,
    similarity_threshold: float = 0.75,
) -> list[EventCluster]:
    """
    Hybrid dedup: algorithmic centroid check + LLM for edge cases.

    1. Compute pairwise centroid similarities
    2. Auto-merge pairs with similarity > 0.85 (confident)
    3. Send pairs with similarity 0.6-0.85 to LLM for judgment
    4. Return merged clusters

    This minimizes LLM calls while catching semantic duplicates.
    """
    if len(clusters) < 2:
        return clusters

    # Compute pairwise similarities
    centroids = np.vstack([c.centroid for c in clusters])
    similarities = centroids @ centroids.T

    # Find candidate pairs
    confident_merges: list[tuple[int, int]] = []
    uncertain_pairs: list[tuple[int, int, float]] = []

    n = len(clusters)
    for i in range(n):
        for j in range(i + 1, n):
            sim = similarities[i, j]
            if sim >= 0.85:
                confident_merges.append((i, j))
            elif sim >= 0.6:
                uncertain_pairs.append((i, j, sim))

    logger.info(
        f"Hybrid dedup: {len(confident_merges)} confident merges, "
        f"{len(uncertain_pairs)} uncertain pairs to review"
    )

    # Build merge groups from confident pairs using union-find
    merge_groups = _pairs_to_groups(confident_merges, n)

    # If uncertain pairs exist, ask LLM
    if uncertain_pairs:
        llm_merges = await _check_uncertain_pairs(clusters, uncertain_pairs, leader_name)
        # Add LLM-confirmed merges to groups
        additional_groups = _pairs_to_groups(llm_merges, n)
        merge_groups.extend(additional_groups)

    if not merge_groups:
        return clusters

    return _merge_cluster_groups(clusters, merge_groups)


def _pairs_to_groups(pairs: list[tuple[int, int]], n: int) -> list[list[int]]:
    """Convert pairwise merges to groups using union-find."""
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for i, j in pairs:
        union(i, j)

    # Group by root
    groups: dict[int, list[int]] = {}
    for i in range(n):
        root = find(i)
        if root not in groups:
            groups[root] = []
        groups[root].append(i)

    # Only return groups with 2+ members
    return [g for g in groups.values() if len(g) >= 2]


@with_retry(max_attempts=2)
async def _check_uncertain_pairs(
    clusters: list[EventCluster],
    pairs: list[tuple[int, int, float]],
    leader_name: str,
) -> list[tuple[int, int]]:
    """Ask LLM to judge uncertain pairs."""

    pair_descriptions = []
    for i, j, sim in pairs:
        pair_descriptions.append(
            f"Pair ({i}, {j}) similarity={sim:.2f}:\n"
            f"  A: {clusters[i].representative_title}\n"
            f"  B: {clusters[j].representative_title}"
        )

    pairs_text = "\n\n".join(pair_descriptions)

    prompt = f"""These cluster pairs about {leader_name} have moderate similarity and might be duplicates.

{pairs_text}

For each pair, are A and B about THE SAME EVENT (should merge) or different events (keep separate)?

Return JSON:
{{
    "same_event": [[0, 3], [1, 7]],  // pairs that ARE the same event
    "different": [[2, 5]]            // pairs that are different events
}}
"""

    response = await complete(
        prompt=prompt,
        system=DEDUP_SYSTEM,
        temperature=0.1,
        max_tokens=300,
    )

    data = extract_json_from_response(response)

    if not data or "same_event" not in data:
        return []

    return [tuple(p) for p in data.get("same_event", [])]
