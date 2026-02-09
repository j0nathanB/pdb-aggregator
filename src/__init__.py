"""
PDB Aggregator - Presidential Daily Brief style news aggregation.

A multi-agent system for generating weekly intelligence briefs
tracking world leaders using LangGraph orchestration.

Architecture: Bottom-up approach where narrative emerges from
leader actions rather than top-down global context framing.
"""

from pathlib import Path
from dotenv import load_dotenv

# Load .env before any other imports that read environment variables
load_dotenv(Path(__file__).parent.parent / ".env")

from .config import (
    LeaderConfig,
    LeaderDossier,
    Article,
    WeeklyBrief,
    CrossCuttingThread,
    GlobalPulse,  # Optional in bottom-up architecture
    get_leader_configs,
    RELEVANCE_THRESHOLD,
    HIGH_WEIGHT_EVENT_TYPES,
    SINGLETON_THRESHOLD,
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
    "HIGH_WEIGHT_EVENT_TYPES",
    "SINGLETON_THRESHOLD",
]

__version__ = "0.2.0"  # Major update: LangGraph migration + bottom-up architecture
