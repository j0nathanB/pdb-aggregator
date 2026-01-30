"""
Fetcher module - News article fetching with SearchAPI + Diffbot.

Provides production-quality news fetching for the PDB pipeline.
"""

from .core import (
    fetch_articles_for_leader,
    SEARCHAPI_KEY,
    DIFFBOT_TOKEN,
    DIFFBOT_DELAY_SECONDS,
)

__all__ = [
    "fetch_articles_for_leader",
    "SEARCHAPI_KEY",
    "DIFFBOT_TOKEN",
    "DIFFBOT_DELAY_SECONDS",
]
