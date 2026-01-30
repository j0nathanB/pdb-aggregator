"""
Thread detection nodes - two-phase detection of cross-cutting themes.

Phase 1: Multi-leader threads (events involving 2+ leaders)
Phase 2: High-impact singletons (single-leader events meeting threshold criteria)
"""

import hashlib
import logging
from typing import Any

from ..config import (
    CrossCuttingThread,
    LeaderDossier,
    EventType,
    LeaderRole,
    ImpactLevel,
    HIGH_WEIGHT_EVENT_TYPES,
    SINGLETON_THRESHOLD,
)
from ..state import PDBState
from ..agents.thread_detector import ThreadDetectorAgent
from ..debug import save_thread_detection_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def detect_multi_leader_threads(state: PDBState) -> dict[str, Any]:
    """
    Phase 1: Detect threads involving multiple leaders.

    Args:
        state: PDB state with dossiers

    Returns:
        Updated state with multi_leader_threads field populated
    """
    dossiers = state.get("dossiers", {})

    if len(dossiers) < 2:
        logger.info("Not enough dossiers for multi-leader thread detection")
        return {"multi_leader_threads": []}

    logger.info(f"Detecting multi-leader threads from {len(dossiers)} dossiers")

    try:
        detector = ThreadDetectorAgent()

        # Detect threads with min_leaders=2 (multi-leader only)
        threads = await detector.detect_multi_leader_threads(
            dossiers=dossiers,
            min_leaders=2,
        )

        logger.info(f"Found {len(threads)} multi-leader threads")

        # Save debug output
        if is_debug_enabled():
            input_data = {
                "dossier_count": len(dossiers),
                "leaders": list(dossiers.keys()),
                "total_events": sum(
                    len(d.underlying_events) for d in dossiers.values()
                ),
            }
            save_thread_detection_results(
                phase="multi_leader",
                threads=threads,
                input_data=input_data,
            )

        return {"multi_leader_threads": threads}

    except Exception as e:
        logger.error(f"Multi-leader thread detection failed: {e}")
        return {"multi_leader_threads": []}


async def detect_singletons(state: PDBState) -> dict[str, Any]:
    """
    Phase 2: Identify high-impact single-leader events.

    Singleton criteria:
    - Priority score >= SINGLETON_THRESHOLD
    - Event type in HIGH_WEIGHT_EVENT_TYPES
    - Leader role is INITIATOR
    - Impact level is INTERNATIONAL or NATIONAL
    - Not already in a multi-leader thread

    Args:
        state: PDB state with dossiers and multi-leader threads

    Returns:
        Updated state with singleton_threads field populated
    """
    dossiers = state.get("dossiers", {})
    multi_leader_threads = state.get("multi_leader_threads", [])

    # Get events already in multi-leader threads
    clustered_events: set[str] = set()
    for thread in multi_leader_threads:
        clustered_events.update(thread.event_ids)

    singletons: list[CrossCuttingThread] = []

    for leader_name, dossier in dossiers.items():
        for article in dossier.articles:
            if not article.classification:
                continue

            c = article.classification

            # Check singleton criteria
            if not _meets_singleton_criteria(c, article.id, clustered_events):
                continue

            # Create singleton thread
            singleton = _create_singleton_thread(
                article=article,
                leader_name=leader_name,
                dossier=dossier,
            )
            singletons.append(singleton)

    # Sort by significance score and take top 3
    singletons.sort(key=lambda t: t.significance_score, reverse=True)
    top_singletons = singletons[:3]

    logger.info(f"Found {len(top_singletons)} singleton threads")

    # Save debug output
    if is_debug_enabled():
        input_data = {
            "dossier_count": len(dossiers),
            "multi_leader_thread_count": len(multi_leader_threads),
            "clustered_event_count": len(clustered_events),
            "candidates_found": len(singletons),
            "kept": len(top_singletons),
        }
        save_thread_detection_results(
            phase="singletons",
            threads=top_singletons,
            input_data=input_data,
        )

    return {"singleton_threads": top_singletons}


def _meets_singleton_criteria(
    classification,
    article_id: str,
    clustered_events: set[str],
) -> bool:
    """Check if an article meets singleton thread criteria."""
    # Must meet threshold
    if classification.priority_score < SINGLETON_THRESHOLD:
        return False

    # Must be high-weight event type
    if classification.event_type not in HIGH_WEIGHT_EVENT_TYPES:
        return False

    # Leader must be initiator
    if classification.leader_role != LeaderRole.INITIATOR:
        return False

    # Must have international or national impact
    if classification.impact_level not in [ImpactLevel.INTERNATIONAL, ImpactLevel.NATIONAL]:
        return False

    # Must not be in an existing thread
    if article_id in clustered_events:
        return False

    return True


def _create_singleton_thread(
    article,
    leader_name: str,
    dossier: LeaderDossier,
) -> CrossCuttingThread:
    """Create a singleton thread from a high-impact article."""
    c = article.classification

    # Generate thread ID
    thread_id = hashlib.md5(f"singleton:{leader_name}:{article.id}".encode()).hexdigest()[:8]

    # Create thread
    return CrossCuttingThread(
        id=thread_id,
        title=article.title[:100],  # Use article title as thread title
        description=article.summary or article.content[:200] + "...",
        leader_postures={leader_name: f"{c.event_type.value}: {c.reasoning[:100]}"},
        leader_count=1,
        event_ids=[article.id],
        tension_points=[],
        convergence_points=[],
        trajectory=f"Watch for international response to {leader_name}'s {c.event_type.value}",
        is_singleton=True,
        significance_score=c.priority_score,
        event_type=c.event_type.value,
    )


async def merge_threads(state: PDBState) -> dict[str, Any]:
    """
    Merge multi-leader threads and singletons into final thread list.

    Args:
        state: PDB state with multi_leader_threads and singleton_threads

    Returns:
        Updated state with all_threads field populated
    """
    multi_leader = state.get("multi_leader_threads", [])
    singletons = state.get("singleton_threads", [])

    # Combine and sort: multi-leader first (by leader count), then singletons (by score)
    all_threads = []

    # Add multi-leader threads first
    multi_sorted = sorted(multi_leader, key=lambda t: t.leader_count, reverse=True)
    all_threads.extend(multi_sorted)

    # Add singletons
    all_threads.extend(singletons)

    logger.info(
        f"Merged threads: {len(multi_leader)} multi-leader + "
        f"{len(singletons)} singletons = {len(all_threads)} total"
    )

    return {"all_threads": all_threads}
