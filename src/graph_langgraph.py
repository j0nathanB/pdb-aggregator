"""
LangGraph workflow definition for the PDB pipeline.

Defines the full StateGraph with nodes, edges, and parallel routing
for processing leaders and synthesizing the final brief.
"""

import logging
from typing import Literal, Sequence

from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send

from .config import LeaderConfig, LeaderDossier, RELEVANCE_THRESHOLD
from .state import (
    PDBState,
    LeaderProcessingState,
    create_initial_state,
    create_leader_processing_state,
)
from .nodes import (
    initialize_workflow,
    fetch_articles_for_leader,
    translate_articles,
    summarize_and_dedupe,
    classify_articles,
    build_dossier,
    build_aggregate_briefing,
    assess_source_quality,
    compile_brief,
)

logger = logging.getLogger(__name__)


# =============================================================================
# ROUTING FUNCTIONS
# =============================================================================

def route_to_leaders(state: PDBState) -> list[Send]:
    """
    Route to parallel leader processing for each leader that needs processing.

    Returns Send objects for each leader that should be processed.
    """
    leaders_to_process = state.get("leaders_to_process", [])
    date_start = state["date_range_start"]
    date_end = state["date_range_end"]

    sends = []
    for leader in state["leaders"]:
        if leader.name in leaders_to_process:
            # Create processing state for this leader
            leader_state = create_leader_processing_state(leader, date_start, date_end)
            sends.append(Send("process_leader", leader_state))

    logger.info(f"Routing to {len(sends)} leader processing nodes")

    return sends


def should_run_aggregate(state: PDBState) -> Literal["continue", "skip"]:
    """
    Determine if we should run aggregate briefing or skip (no dossiers).
    """
    dossiers = state.get("dossiers", {})

    if not dossiers:
        logger.warning("No dossiers generated, skipping aggregate briefing")
        return "skip"

    return "continue"


# =============================================================================
# AGGREGATION NODE
# =============================================================================

async def aggregate_leader_results(state: PDBState) -> dict:
    """
    Aggregate results from parallel leader processing.

    This node is called after all process_leader nodes complete.
    The state already has results merged via operator.or_.
    """
    dossiers = state.get("dossiers", {})
    logger.info(f"Aggregated {len(dossiers)} dossiers")

    # Nothing to do - state merging handles aggregation
    return {}


# =============================================================================
# LEADER SUBGRAPH
# =============================================================================

def create_leader_subgraph():
    """
    Create the per-leader processing subgraph.

    Pipeline: fetch -> translate -> dedupe -> classify -> build_dossier
    """
    graph = StateGraph(LeaderProcessingState)

    # Add nodes
    graph.add_node("fetch", fetch_articles_for_leader)
    graph.add_node("translate", translate_articles)
    graph.add_node("dedupe", summarize_and_dedupe)
    graph.add_node("classify", classify_articles)
    graph.add_node("build_dossier", build_dossier)

    # Add edges (sequential processing)
    graph.add_edge(START, "fetch")
    graph.add_edge("fetch", "translate")
    graph.add_edge("translate", "dedupe")
    graph.add_edge("dedupe", "classify")
    graph.add_edge("classify", "build_dossier")
    graph.add_edge("build_dossier", END)

    return graph.compile()


# =============================================================================
# LEADER PROCESSING WRAPPER
# =============================================================================

async def process_leader(state: LeaderProcessingState) -> dict:
    """
    Process a single leader through the full pipeline.

    This is a wrapper that runs the leader subgraph and returns
    results for aggregation into the main state.
    """
    leader = state["leader"]
    logger.info(f"Processing leader: {leader.name}")

    try:
        # Run the leader subgraph
        subgraph = create_leader_subgraph()
        result = await subgraph.ainvoke(state)

        dossier = result.get("dossier")

        if dossier:
            return {
                "dossiers": {leader.name: dossier},
                "leader_results": {
                    leader.name: {
                        "leader_name": leader.name,
                        "articles": result.get("classified_articles", []),
                        "dossier": dossier,
                        "error": None,
                    }
                },
            }
        else:
            return {
                "leader_results": {
                    leader.name: {
                        "leader_name": leader.name,
                        "articles": [],
                        "dossier": None,
                        "error": result.get("error", "Unknown error"),
                    }
                },
            }

    except Exception as e:
        logger.error(f"Failed to process {leader.name}: {e}")
        return {
            "leader_results": {
                leader.name: {
                    "leader_name": leader.name,
                    "articles": [],
                    "dossier": None,
                    "error": str(e),
                }
            },
        }


# =============================================================================
# MAIN GRAPH
# =============================================================================

def create_pdb_graph():
    """
    Create the main PDB LangGraph workflow.

    Structure:
    1. init -> check for existing dossiers (resume)
    2. route_to_leaders -> parallel leader processing
    3. aggregate -> combine results
    4. Parallel: aggregate_briefing, quality assessment
    5. compile -> final brief
    """
    graph = StateGraph(PDBState)

    # Add nodes
    graph.add_node("init", initialize_workflow)
    graph.add_node("process_leader", process_leader)
    graph.add_node("aggregate", aggregate_leader_results)
    graph.add_node("aggregate_briefing", build_aggregate_briefing)
    graph.add_node("quality", assess_source_quality)
    graph.add_node("compile", compile_brief)

    # Entry edge
    graph.add_edge(START, "init")

    # Route to parallel leader processing
    graph.add_conditional_edges(
        "init",
        route_to_leaders,
        ["process_leader"],
    )

    # Aggregate after all leader processing completes
    graph.add_edge("process_leader", "aggregate")

    # Conditional: continue to aggregate briefing or skip
    graph.add_conditional_edges(
        "aggregate",
        should_run_aggregate,
        {
            "continue": "aggregate_briefing",
            "skip": END,
        },
    )

    # Parallel: aggregate briefing + quality assessment
    graph.add_edge("aggregate_briefing", "compile")
    graph.add_edge("aggregate", "quality")
    graph.add_edge("quality", "compile")

    # Final output
    graph.add_edge("compile", END)

    return graph.compile()


# =============================================================================
# CONVENIENCE FUNCTION
# =============================================================================

async def run_pdb_langgraph(
    date_range_start: str,
    date_range_end: str,
    leaders: list[LeaderConfig],
) -> PDBState:
    """
    Run the full PDB workflow using LangGraph.

    Args:
        date_range_start: Start date (ISO format)
        date_range_end: End date (ISO format)
        leaders: Leaders to process

    Returns:
        Final PDBState with brief
    """
    logger.info(f"Starting LangGraph PDB workflow: {date_range_start} to {date_range_end}")
    logger.info(f"Processing {len(leaders)} leaders")

    # Create initial state
    initial_state = create_initial_state(date_range_start, date_range_end, leaders)

    # Create and run graph
    graph = create_pdb_graph()
    result = await graph.ainvoke(initial_state)

    return result
