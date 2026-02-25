"""
Unified cluster reasoning - combines dedup and story arc detection in a single LLM call.

Replaces the two-step flow of deduplicate_clusters() + detect_story_arcs() with a single
reason_about_clusters() call that uses CoT bridging via remaining_distinct_events.

All indices reference the *original* cluster list. Dedup merges are applied first into a
consumed set, then arc merges on remaining indices.
"""

import logging
import numpy as np

from .clusterer import EventCluster
from ..agents.base import complete, extract_json_from_response, with_retry
from ..config import MODEL_ANALYTICAL, THINKING_ANALYTICAL

logger = logging.getLogger(__name__)


REASONING_SYSTEM = """You are a senior news editor and fact-checker. You have two tasks:

TASK 1 — DEDUPLICATION:
Identify clusters that describe the EXACT SAME physical occurrence or announcement.

DO MERGE (dedup):
- The exact same event reported in different languages
- The exact same announcement covered by different publishers on the same day

DO NOT MERGE (dedup):
- Follow-up reactions or consequences of an earlier event
- Subsequent days of a multi-day event (those are story arcs — Task 2)
- Similar policies or actions happening at different times

TASK 2 — STORY ARC DETECTION:
Among the REMAINING distinct events (after dedup), identify developing story arcs.

A Story Arc requires a causal or direct narrative link:
- "Event A happens" → "Actor reacts to Event A" → "Consequences of Event A"
- A multi-day state visit: arrival → meetings → departure
- An ongoing negotiation: proposal → counter-proposal → deal

DO NOT group events just because they share a broad theme.

Return your answer as JSON."""


@with_retry(max_attempts=2)
async def reason_about_clusters(
    clusters: list[EventCluster],
    leader_name: str,
    model: str = MODEL_ANALYTICAL,
    thinking_budget: int = THINKING_ANALYTICAL,
) -> list[EventCluster]:
    """
    Combined dedup + story arc detection in a single LLM call.

    Uses a CoT bridge: the LLM first outputs dedup merges, then explicitly lists
    remaining indices (forcing reasoning about post-dedup state), then identifies
    story arcs among those remaining events.

    Args:
        clusters: List of EventClusters from HDBSCAN
        leader_name: Name of the leader (for context)
        model: Model to use
        thinking_budget: Thinking budget tokens

    Returns:
        Merged list of EventClusters with both dedup and arc merges applied
    """
    if len(clusters) < 2:
        return clusters

    # Build cluster summaries
    cluster_lines = []
    for i, cluster in enumerate(clusters):
        title = cluster.representative_title
        snippet = cluster.snippets[0].snippet if cluster.snippets else ""
        date = cluster.snippets[0].date if cluster.snippets else ""
        sources = ", ".join(list(cluster.sources)[:3])
        date_tag = f" [{date}]" if date else ""

        cluster_lines.append(
            f"{i}.{date_tag} [{sources}] {title}\n   {snippet[:200]}"
        )

    summaries_text = "\n\n".join(cluster_lines)
    all_indices = list(range(len(clusters)))

    prompt = f"""Review these {len(clusters)} news clusters about {leader_name}.

CLUSTERS:
{summaries_text}

Work through these steps IN ORDER:

STEP 1 — DEDUPLICATION:
For every potential merge, compare the Primary Actor, Specific Action, and Timing \
to confirm they describe the EXACT SAME occurrence. List groups of indices to merge.

STEP 2 — REMAINING EVENTS:
After removing duplicates, explicitly list all remaining distinct event indices \
from the original list ({all_indices}). This forces you to reason about the post-dedup state.

STEP 3 — STORY ARCS:
Among the remaining distinct events only, identify any developing story arcs \
with causal or direct narrative links. For each arc, provide a merged headline.

Return JSON:
{{
    "dedup_reasoning": "Brief explanation of dedup decisions",
    "dedup_merges": [[0, 3]],
    "remaining_distinct_events": [0, 1, 2, 4, 5],
    "arc_reasoning": "Brief explanation of arc decisions",
    "story_arcs": [
        {{"indices": [1, 4], "merged_title": "Single headline covering the arc, max 12 words"}}
    ]
}}

If no dedup merges needed: "dedup_merges": []
If no story arcs found: "story_arcs": []
"""

    response = await complete(
        prompt=prompt,
        system=REASONING_SYSTEM,
        temperature=0.1,
        model=model,
        thinking_budget=thinking_budget,
    )

    data = extract_json_from_response(response)

    if not data:
        logger.warning("Failed to parse cluster reasoning response, returning original clusters")
        return clusters

    dedup_merges = data.get("dedup_merges", [])
    story_arcs = data.get("story_arcs", [])
    dedup_reasoning = data.get("dedup_reasoning", "")
    arc_reasoning = data.get("arc_reasoning", "")

    if dedup_merges:
        logger.info(f"Cluster reasoning for {leader_name} — dedup: {dedup_reasoning}")
    if story_arcs:
        logger.info(f"Cluster reasoning for {leader_name} — arcs: {arc_reasoning}")

    if not dedup_merges and not story_arcs:
        logger.info(f"No merges found for {leader_name}")
        return clusters

    return _apply_all_merges(clusters, dedup_merges, story_arcs, leader_name)


def _apply_all_merges(
    clusters: list[EventCluster],
    dedup_merges: list[list[int]],
    story_arcs: list[dict],
    leader_name: str,
) -> list[EventCluster]:
    """
    Apply dedup merges first, then arc merges on remaining indices.

    All indices reference the original cluster list. Dedup takes priority
    if indices overlap with arc groups.
    """
    n = len(clusters)
    consumed: set[int] = set()
    result: list[EventCluster] = []

    # Phase 1: Dedup merges (higher priority)
    for group in dedup_merges:
        valid = [i for i in group if 0 <= i < n and i not in consumed]
        if len(valid) < 2:
            continue
        merged = _merge_clusters([clusters[i] for i in valid], suffix="dedup")
        result.append(merged)
        consumed.update(valid)
        logger.info(
            f"Dedup merged clusters {valid} for {leader_name} "
            f"-> '{merged.representative_title[:60]}'"
        )

    # Phase 2: Arc merges (on remaining indices only)
    for arc in story_arcs:
        indices = arc.get("indices", [])
        merged_title = arc.get("merged_title", "")
        valid = [i for i in indices if 0 <= i < n and i not in consumed]
        if len(valid) < 2:
            continue
        merged = _merge_clusters(
            [clusters[i] for i in valid], suffix="arc", title_override=merged_title
        )
        result.append(merged)
        consumed.update(valid)
        logger.info(
            f"Arc merged clusters {valid} for {leader_name} "
            f"-> '{merged.representative_title[:60]}'"
        )

    # Add unconsumed clusters
    for i, cluster in enumerate(clusters):
        if i not in consumed:
            result.append(cluster)

    logger.info(
        f"Cluster reasoning: {n} -> {len(result)} clusters for {leader_name} "
        f"({len(consumed)} indices consumed)"
    )

    return result


def _merge_clusters(
    clusters: list[EventCluster],
    suffix: str = "merged",
    title_override: str = "",
) -> EventCluster:
    """
    Merge multiple clusters into one.

    Combines all snippets, recomputes centroid, and optionally overrides the title.
    """
    # Sort by size to pick ID from largest
    clusters_sorted = sorted(clusters, key=lambda c: len(c.snippets), reverse=True)
    base = clusters_sorted[0]

    all_snippets = []
    for cluster in clusters:
        all_snippets.extend(cluster.snippets)

    embeddings = np.vstack([s.embedding for s in all_snippets])
    centroid = embeddings.mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm > 0:
        centroid = centroid / norm

    merged = EventCluster(
        id=f"{base.id}_{suffix}",
        snippets=all_snippets,
        centroid=centroid,
    )

    # Override title if provided (from arc detection)
    if title_override:
        merged._title_override = title_override

    return merged
