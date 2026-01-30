"""
Node implementations for the PDB LangGraph workflow.

Each module contains node functions that operate on PDBState.
"""

from .init import initialize_workflow
from .fetch import fetch_articles_for_leader
from .translate import translate_articles
from .dedupe import summarize_and_dedupe
from .classify import classify_articles
from .dossier import build_dossier
from .threads import (
    detect_multi_leader_threads,
    detect_singletons,
    merge_threads,
)
from .synthesis import (
    generate_executive_summary,
    generate_regional_contexts,
    assess_source_quality,
)
from .compile import compile_brief

__all__ = [
    "initialize_workflow",
    "fetch_articles_for_leader",
    "translate_articles",
    "summarize_and_dedupe",
    "classify_articles",
    "build_dossier",
    "detect_multi_leader_threads",
    "detect_singletons",
    "merge_threads",
    "generate_executive_summary",
    "generate_regional_contexts",
    "assess_source_quality",
    "compile_brief",
]
