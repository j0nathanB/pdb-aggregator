"""
Agent modules for the PDB Aggregator pipeline.

Bottom-up architecture pipeline order:
1. SourceFetcherAgent - Fetch articles from wire + domestic sources
2. TranslatorAgent - Translate non-English content
3. ClassifierAgent - Apply Paragon taxonomy classification + dedupe
4. DossierBuilderAgent - Build per-leader dossiers
5. ThreadDetectorAgent - Detect cross-cutting themes (multi-leader + singletons)
6. SynthesizerAgent - Generate executive summary and regional context

Note: GlobalPulseAgent has been removed in favor of bottom-up architecture
where narrative emerges from leader actions.
"""

from .source_fetcher import SourceFetcherAgent
from .translator import TranslatorAgent
from .classifier import ClassifierAgent
from .dossier_builder import DossierBuilderAgent
from .thread_detector import ThreadDetectorAgent
from .synthesizer import SynthesizerAgent

__all__ = [
    "SourceFetcherAgent",
    "TranslatorAgent",
    "ClassifierAgent",
    "DossierBuilderAgent",
    "ThreadDetectorAgent",
    "SynthesizerAgent",
]
