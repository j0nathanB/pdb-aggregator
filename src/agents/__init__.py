"""
Agent modules for the PDB Aggregator pipeline.

Event clustering architecture pipeline order:
1. EventClusteringAgent - Fetch snippets, cluster, score, fetch selected articles
2. DossierBuilderAgent - Build per-leader story-centric dossiers from processed events
3. AggregateBriefingBuilder - Match stories across leaders, build aggregate briefing
4. SynthesizerAgent - Source quality assessment

Legacy agents (still available for fallback):
- SourceFetcherAgent - Direct article fetching
- TranslatorAgent - Non-English content translation
- ClassifierAgent - Paragon taxonomy classification
- ThreadDetectorAgent - Cross-cutting thread detection (replaced by AggregateBriefingBuilder)
"""

from .source_fetcher import SourceFetcherAgent
from .translator import TranslatorAgent
from .classifier import ClassifierAgent
from .dossier_builder import DossierBuilderAgent
from .event_clustering import EventClusteringAgent
from .thread_detector import ThreadDetectorAgent
from .synthesizer import SynthesizerAgent
from .aggregate_builder import AggregateBriefingBuilder
from .email_digest import EmailDigestAgent

__all__ = [
    "SourceFetcherAgent",
    "TranslatorAgent",
    "ClassifierAgent",
    "DossierBuilderAgent",
    "EventClusteringAgent",
    "ThreadDetectorAgent",
    "SynthesizerAgent",
    "AggregateBriefingBuilder",
    "EmailDigestAgent",
]
