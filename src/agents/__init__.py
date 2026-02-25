"""
Agent modules for the PDB Aggregator pipeline.

Pipeline order:
1. EventClusteringAgent - Fetch snippets, cluster, score, fetch selected articles
2. DossierBuilderAgent - Build per-leader story-centric dossiers from processed events
3. AggregateBriefingBuilder - Match stories across leaders, build aggregate briefing
4. SynthesizerAgent - Source quality assessment

"""

from .dossier_builder import DossierBuilderAgent
from .event_clustering import EventClusteringAgent
from .synthesizer import SynthesizerAgent
from .aggregate_builder import AggregateBriefingBuilder
from .email_digest import EmailDigestAgent

__all__ = [
    "DossierBuilderAgent",
    "EventClusteringAgent",
    "SynthesizerAgent",
    "AggregateBriefingBuilder",
    "EmailDigestAgent",
]
