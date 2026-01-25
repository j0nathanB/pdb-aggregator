"""
PDB Aggregator - Presidential Daily Brief style news aggregation.

A multi-agent system for generating weekly intelligence briefs
tracking world leaders using LangGraph orchestration.
"""

from .config import (
    LeaderConfig,
    LeaderDossier,
    Article,
    WeeklyBrief,
    CrossCuttingThread,
    GlobalPulse,
    get_leader_configs,
    RELEVANCE_THRESHOLD,
)

__all__ = [
    "LeaderConfig",
    "LeaderDossier", 
    "Article",
    "WeeklyBrief",
    "CrossCuttingThread",
    "GlobalPulse",
    "get_leader_configs",
    "RELEVANCE_THRESHOLD",
]

__version__ = "0.1.0"
