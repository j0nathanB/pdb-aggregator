"""
Initialization node - handles resume capability and workflow setup.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import LeaderConfig, LeaderDossier
from ..state import PDBState

logger = logging.getLogger(__name__)

# Default briefs directory
BRIEFS_DIR = Path("briefs")


async def initialize_workflow(state: PDBState) -> dict[str, Any]:
    """
    Check for existing dossiers and determine which leaders to process.

    This enables resume capability - if a run is interrupted, we can
    skip leaders that already have completed dossiers.

    Args:
        state: Current workflow state

    Returns:
        Updated state fields for resume logic
    """
    output_dir = BRIEFS_DIR / datetime.now().strftime("%Y%m%d")
    dossier_dir = output_dir / "dossiers"

    leaders_to_skip: list[str] = []
    leaders_to_process: list[str] = []
    existing_dossiers: dict[str, LeaderDossier] = {}

    for leader in state["leaders"]:
        safe_name = leader.name.lower().replace(" ", "_")
        dossier_path = dossier_dir / f"{safe_name}.json"

        if dossier_path.exists():
            dossier = _load_dossier_from_file(dossier_path, leader)
            if dossier:
                logger.info(f"Found existing dossier for {leader.name}, skipping")
                leaders_to_skip.append(leader.name)
                existing_dossiers[leader.name] = dossier
                continue

        leaders_to_process.append(leader.name)

    logger.info(f"Resume state: {len(leaders_to_skip)} to skip, {len(leaders_to_process)} to process")

    return {
        "output_dir": str(output_dir),
        "leaders_to_skip": leaders_to_skip,
        "leaders_to_process": leaders_to_process,
        "dossiers": existing_dossiers,
    }


def _load_dossier_from_file(path: Path, leader: LeaderConfig) -> LeaderDossier | None:
    """Load a dossier from a JSON file."""
    try:
        with open(path) as f:
            data = json.load(f)

        # Reconstruct dossier from JSON
        from ..config import LeaderAction, EventType, UnderlyingEvent

        key_actions = []
        for action_data in data.get("key_actions", []):
            try:
                event_type = EventType(action_data.get("event_type", "other"))
            except ValueError:
                event_type = EventType.OTHER

            key_actions.append(LeaderAction(
                description=action_data.get("description", ""),
                event_type=event_type,
                source_articles=action_data.get("source_articles", []),
                significance=action_data.get("significance", ""),
            ))

        underlying_events = []
        for event_data in data.get("underlying_events", []):
            underlying_events.append(UnderlyingEvent(
                id=event_data.get("id", ""),
                description=event_data.get("description", ""),
                leaders_involved=event_data.get("leaders_involved", []),
                article_ids=event_data.get("article_ids", []),
            ))

        return LeaderDossier(
            leader=leader,
            reporting_period=data.get("reporting_period", ""),
            key_actions=key_actions,
            domestic_context=data.get("domestic_context", ""),
            international_posture=data.get("international_posture", ""),
            assessment=data.get("assessment", ""),
            articles=[],  # Don't reload articles for resume
            underlying_events=underlying_events,
            source_quality_notes=data.get("source_quality_notes", ""),
        )

    except Exception as e:
        logger.warning(f"Failed to load dossier from {path}: {e}")
        return None


def should_process_leader(state: PDBState, leader_name: str) -> bool:
    """Check if a leader should be processed or skipped."""
    return leader_name in state.get("leaders_to_process", [])
