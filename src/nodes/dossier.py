"""
Dossier node - builds leader dossier from classified articles.

Note: The LangGraph subgraph still uses article-based processing
(fetch -> translate -> dedupe -> classify -> build_dossier).
This node wraps the articles into a minimal ProcessedEvent format
for compatibility with the story-centric DossierBuilderAgent.
"""

import logging
import hashlib
from typing import Any

from ..state import LeaderProcessingState
from ..agents.dossier_builder import DossierBuilderAgent
from ..agents.event_clustering import ProcessedEvent
from ..debug import save_dossier_results, is_debug_enabled

logger = logging.getLogger(__name__)


async def build_dossier(state: LeaderProcessingState) -> dict[str, Any]:
    """
    Build a dossier for the leader from classified articles.

    Wraps classified articles into ProcessedEvent format for
    the story-centric DossierBuilderAgent.

    Args:
        state: Leader processing state with classified articles

    Returns:
        Updated state with dossier field populated
    """
    articles = state.get("classified_articles", [])
    leader = state["leader"]

    logger.info(f"Building dossier for {leader.name} from {len(articles)} articles")

    try:
        builder = DossierBuilderAgent()

        # Wrap articles into ProcessedEvents (one event per article)
        events = []
        for i, article in enumerate(articles):
            event_id = hashlib.md5(
                f"{leader.name}:{article.id}".encode()
            ).hexdigest()[:8]

            events.append(ProcessedEvent(
                id=event_id,
                title=article.title,
                articles=[{
                    "id": article.id,
                    "title": article.title,
                    "url": article.url,
                    "source_name": article.source_name,
                    "source_type": article.source_type,
                    "content": article.display_content,
                    "language": article.original_language,
                }],
                entities=[],
                summary=article.summary or "",
                score=article.classification.priority_score if article.classification else 0.5,
                rank=i + 1,
                source_count=1,
                has_wire=article.source_type == "wire",
            ))

        # Split top 5 / remaining
        top_events = events[:5]
        remaining_events = events[5:]

        dossier = await builder.build_from_events(
            leader=leader,
            top_events=top_events,
            remaining_events=remaining_events,
            date_start=state.get("date_range_start"),
            date_end=state.get("date_range_end"),
        )

        story_count = (
            len(dossier.main_stories)
            + len(dossier.international_stories)
            + len(dossier.domestic_stories)
        )
        logger.info(
            f"Built dossier for {leader.name}: "
            f"{story_count} stories, "
            f"{len(dossier.underlying_events)} events"
        )

        # Save debug output
        if is_debug_enabled():
            save_dossier_results(
                leader_name=leader.name,
                dossier=dossier,
            )

        return {"dossier": dossier}

    except Exception as e:
        logger.error(f"Dossier building failed for {leader.name}: {e}")
        return {
            "dossier": None,
            "error": f"Dossier building failed: {e}",
        }
