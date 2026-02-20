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
from ..config import MODEL_ANALYTICAL, THINKING_ANALYTICAL

logger = logging.getLogger(__name__)


DEDUP_SYSTEM = """You are a strict journalistic fact-checker. Your job is to identify \
if two or more news clusters refer to the EXACT SAME physical occurrence or announcement.

WARNING: These clusters have already been grouped by semantic similarity (HDBSCAN). \
They may share the same entities, topics, and keywords, but describe DIFFERENT events. \
Your job is to catch cross-lingual duplicates and prevent false merges.

DO MERGE:
- The exact same event reported in different languages (e.g., English and French)
- The exact same announcement covered by different publishers on the same day

DO NOT MERGE:
- Follow-up reactions or consequences of an earlier event
- Subsequent days of a multi-day event (those are story arcs, handled separately)
- Similar policies or actions happening at different times
- A news roundup that merely mentions an event vs. dedicated coverage of that event

Return your answer as JSON."""


@with_retry(max_attempts=2)
async def deduplicate_clusters(
    clusters: list[EventCluster],
    leader_name: str,
    model: str = MODEL_ANALYTICAL,
    thinking_budget: int = THINKING_ANALYTICAL,
) -> list[EventCluster]:
    """
    Use LLM to identify and merge duplicate clusters.

    Deprecated: Use cluster_reasoning.reason_about_clusters() instead, which combines
    dedup + arc detection in a single LLM call. Kept for fallback/standalone use.
    """
    if len(clusters) < 2:
        return clusters

    # Build cluster summary for LLM
    cluster_summaries = []
    for i, cluster in enumerate(clusters):
        title = cluster.representative_title
        snippet = cluster.snippets[0].snippet if cluster.snippets else ""
        date = cluster.snippets[0].date if cluster.snippets else ""
        sources = ", ".join(list(cluster.sources)[:3])
        date_tag = f" [{date}]" if date else ""

        cluster_summaries.append(
            f"{i}.{date_tag} [{sources}] {title}\n   {snippet[:200]}"
        )

    summaries_text = "\n\n".join(cluster_summaries)

    prompt = f"""Review these {len(clusters)} news clusters about {leader_name}.

CLUSTERS:
{summaries_text}

For every potential merge, compare the Primary Actor, Specific Action, and Timing \
to confirm they describe the EXACT SAME occurrence.

Return JSON:
{{
    "reasoning": "Cluster 0 and 5 describe the exact same EV rollback announced on Wednesday, in English and French respectively. Cluster 1 is about a new strategy launch, which is a different action.",
    "merge_groups": [
        [0, 5]
    ]
}}

If no clusters should be merged, return: {{"reasoning": "All clusters are distinct events.", "merge_groups": []}}
"""

    response = await complete(
        prompt=prompt,
        system=DEDUP_SYSTEM,
        temperature=0.1,  # Low temp for consistent judgment
        model=model,
        thinking_budget=thinking_budget,
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

