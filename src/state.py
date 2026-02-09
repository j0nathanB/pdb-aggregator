"""
LangGraph state schema for the PDB workflow.

Defines the state types used by the StateGraph nodes.
"""

from typing import TypedDict, Annotated, Optional, Any
import operator

from .config import (
    Article,
    LeaderConfig,
    LeaderDossier,
    Story,
    WeeklyBrief,
)


class LeaderProcessingResult(TypedDict):
    """Result from processing a single leader."""
    leader_name: str
    articles: list[Article]
    dossier: Optional[LeaderDossier]
    error: Optional[str]


class LeaderProcessingState(TypedDict):
    """State for the per-leader processing subgraph."""
    leader: LeaderConfig
    date_range_start: str
    date_range_end: str

    # Processing stages
    articles: list[Article]
    translated_articles: list[Article]
    deduped_articles: list[Article]
    classified_articles: list[Article]

    # Output
    dossier: Optional[LeaderDossier]
    error: Optional[str]


class PDBState(TypedDict):
    """Main state for the PDB LangGraph workflow."""
    # Config
    date_range_start: str
    date_range_end: str
    leaders: list[LeaderConfig]

    # Resume state
    leaders_to_skip: list[str]
    leaders_to_process: list[str]
    output_dir: str

    # Aggregated results (merge via operator.or_)
    leader_results: Annotated[dict[str, LeaderProcessingResult], operator.or_]
    dossiers: Annotated[dict[str, LeaderDossier], operator.or_]

    # Aggregate briefing (story-centric)
    aggregate_main_stories: list[Story]
    aggregate_intl_stories: list[Story]
    aggregate_dom_stories: list[Story]
    aggregate_btl: list[str]
    aggregate_executive_summary: str

    # Source quality
    source_quality_notes: str

    # Final output
    brief: Optional[WeeklyBrief]


def create_initial_state(
    date_range_start: str,
    date_range_end: str,
    leaders: list[LeaderConfig],
) -> PDBState:
    """Create initial state for the PDB workflow."""
    return {
        # Config
        "date_range_start": date_range_start,
        "date_range_end": date_range_end,
        "leaders": leaders,

        # Resume state (populated by init node)
        "leaders_to_skip": [],
        "leaders_to_process": [],
        "output_dir": "",

        # Results
        "leader_results": {},
        "dossiers": {},

        # Aggregate briefing
        "aggregate_main_stories": [],
        "aggregate_intl_stories": [],
        "aggregate_dom_stories": [],
        "aggregate_btl": [],
        "aggregate_executive_summary": "",

        # Source quality
        "source_quality_notes": "",

        # Output
        "brief": None,
    }


def create_leader_processing_state(
    leader: LeaderConfig,
    date_range_start: str,
    date_range_end: str,
) -> LeaderProcessingState:
    """Create initial state for per-leader processing."""
    return {
        "leader": leader,
        "date_range_start": date_range_start,
        "date_range_end": date_range_end,

        "articles": [],
        "translated_articles": [],
        "deduped_articles": [],
        "classified_articles": [],

        "dossier": None,
        "error": None,
    }
