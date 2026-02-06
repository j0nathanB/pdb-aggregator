"""
Initialization node - handles resume capability and workflow setup.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ..config import LeaderConfig, LeaderDossier, Story, StoryScope
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
    """Load a dossier from a JSON file, supporting both old and new formats."""
    try:
        with open(path) as f:
            data = json.load(f)

        # Detect old format
        if "key_actions" in data:
            return _load_old_format_dossier(data, leader)

        # New format: story-centric
        return LeaderDossier(
            leader=leader,
            reporting_period=data.get("reporting_period", ""),
            main_stories=[_deserialize_story(s) for s in data.get("main_stories", [])],
            international_stories=[_deserialize_story(s) for s in data.get("international_stories", [])],
            domestic_stories=[_deserialize_story(s) for s in data.get("domestic_stories", [])],
            between_the_lines=data.get("between_the_lines", []),
            articles=[],  # Don't reload articles for resume
            underlying_events=[],
            source_quality_notes=data.get("source_quality_notes", ""),
        )

    except Exception as e:
        logger.warning(f"Failed to load dossier from {path}: {e}")
        return None


def _deserialize_story(data: dict) -> Story:
    """Deserialize a Story from JSON data."""
    scope_str = data.get("scope", "domestic")
    try:
        scope = StoryScope(scope_str)
    except ValueError:
        scope = StoryScope.DOMESTIC

    return Story(
        id=data.get("id", ""),
        title=data.get("title", ""),
        narrative=data.get("narrative", ""),
        scope=scope,
        source_count=data.get("source_count", 0),
        has_wire=data.get("has_wire", False),
        score=data.get("score", 0.0),
        source_refs=data.get("source_refs", {}),
        entities=data.get("entities", []),
        cluster_id=data.get("cluster_id", ""),
        contributing_leaders=data.get("contributing_leaders", []),
    )


def _load_old_format_dossier(data: dict, leader: LeaderConfig) -> LeaderDossier:
    """Convert old-format dossier (key_actions) to new story-centric format."""
    # Convert key_actions to main_stories
    main_stories = []
    for action_data in data.get("key_actions", []):
        event_type_str = action_data.get("event_type", "other")
        scope = StoryScope.INTERNATIONAL if event_type_str in (
            "international_visit", "bilateral_agreement"
        ) else StoryScope.DOMESTIC

        main_stories.append(Story(
            id=f"legacy-{len(main_stories)}",
            title=action_data.get("description", "")[:80],
            narrative=action_data.get("description", ""),
            scope=scope,
            source_count=len(action_data.get("source_articles", [])),
            has_wire=False,
            score=0.5,
            source_refs=action_data.get("source_refs", {}),
        ))

    btl = []
    if data.get("assessment"):
        btl.append(data["assessment"])

    return LeaderDossier(
        leader=leader,
        reporting_period=data.get("reporting_period", ""),
        main_stories=main_stories,
        international_stories=[],
        domestic_stories=[],
        between_the_lines=btl,
        articles=[],
        underlying_events=[],
        source_quality_notes=data.get("source_quality_notes", ""),
    )


def should_process_leader(state: PDBState, leader_name: str) -> bool:
    """Check if a leader should be processed or skipped."""
    return leader_name in state.get("leaders_to_process", [])
