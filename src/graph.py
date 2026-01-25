"""
Graph module - exports the PDB workflow.

This module provides a cleaner import path for the workflow:
    from src.graph import PDBWorkflow
"""

# Re-export from workflow module
# Note: In the actual project structure, workflow.py should be moved to src/
# For now, we define PDBWorkflow here directly

from typing import Optional
from datetime import datetime, timedelta
import logging

from .config import (
    LeaderConfig,
    LeaderDossier,
    WeeklyBrief,
    get_leader_configs,
)

logger = logging.getLogger(__name__)


class PDBWorkflow:
    """
    High-level interface for running the PDB generation workflow.
    
    This is a simplified version that runs the pipeline without LangGraph
    for easier debugging and testing. The full LangGraph version is in
    workflow.py (to be moved to this package).
    """
    
    def __init__(self, use_langgraph: bool = False):
        """
        Initialize the workflow.
        
        Args:
            use_langgraph: Whether to use full LangGraph orchestration
        """
        self.use_langgraph = use_langgraph
    
    async def run(
        self,
        date_range_start: Optional[str] = None,
        date_range_end: Optional[str] = None,
        leaders: Optional[list[LeaderConfig]] = None,
    ) -> WeeklyBrief:
        """
        Execute the full PDB generation workflow.
        
        Args:
            date_range_start: Start of date range (ISO format)
            date_range_end: End of date range (ISO format)
            leaders: Optional list of leaders to track (defaults to all)
            
        Returns:
            The generated WeeklyBrief
        """
        # Default to last 7 days
        if not date_range_end:
            date_range_end = datetime.now().strftime("%Y-%m-%d")
        if not date_range_start:
            start = datetime.now() - timedelta(days=7)
            date_range_start = start.strftime("%Y-%m-%d")
        
        # Default to all leaders
        if not leaders:
            leaders = get_leader_configs()
        
        logger.info(f"Starting PDB workflow: {date_range_start} to {date_range_end}")
        logger.info(f"Tracking {len(leaders)} leaders")
        
        # Run the simple pipeline
        return await self._run_simple_pipeline(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            leaders=leaders,
        )
    
    async def _run_simple_pipeline(
        self,
        date_range_start: str,
        date_range_end: str,
        leaders: list[LeaderConfig],
    ) -> WeeklyBrief:
        """
        Run the pipeline without LangGraph orchestration.
        
        Useful for debugging and understanding the flow.
        """
        from .agents.global_pulse import GlobalPulseAgent
        from .agents.source_fetcher import SourceFetcherAgent
        from .agents.translator import TranslatorAgent
        from .agents.classifier import ClassifierAgent
        from .agents.dossier_builder import DossierBuilderAgent
        from .agents.thread_detector import ThreadDetectorAgent
        from .agents.synthesizer import SynthesizerAgent
        from .persistence import save_brief
        from .config import GlobalPulse, RELEVANCE_THRESHOLD
        
        # 1. Fetch global pulse
        logger.info("Step 1: Fetching global pulse")
        pulse_agent = GlobalPulseAgent()
        global_pulse = await pulse_agent.fetch(date_range_start, date_range_end)
        
        # 2. Process each leader
        logger.info("Step 2: Processing leaders")
        dossiers: dict[str, LeaderDossier] = {}
        
        fetcher = SourceFetcherAgent()
        translator = TranslatorAgent()
        classifier = ClassifierAgent()
        builder = DossierBuilderAgent()
        
        for leader in leaders:
            logger.info(f"  Processing: {leader.name}")
            
            try:
                # Fetch articles
                articles = await fetcher.fetch_for_leader(
                    leader=leader,
                    date_start=date_range_start,
                    date_end=date_range_end,
                )
                
                # Translate
                articles = await translator.translate_batch(articles)
                
                # Classify
                articles = await classifier.classify_batch(articles, leader)
                
                # Filter
                relevant = [
                    a for a in articles
                    if a.classification and a.classification.priority_score >= RELEVANCE_THRESHOLD
                ]
                
                # Build dossier
                dossier = await builder.build(
                    leader=leader,
                    articles=relevant,
                    global_context=global_pulse,
                )
                
                dossiers[leader.name] = dossier
                logger.info(f"    {len(relevant)} relevant articles")
                
            except Exception as e:
                logger.error(f"  Error processing {leader.name}: {e}")
        
        await fetcher.close()
        
        # 3. Detect cross-cutting threads
        logger.info("Step 3: Detecting threads")
        thread_detector = ThreadDetectorAgent()
        threads = await thread_detector.detect(dossiers, global_pulse)
        logger.info(f"  Found {len(threads)} threads")
        
        # 4. Generate synthesis
        logger.info("Step 4: Generating synthesis")
        synthesizer = SynthesizerAgent()
        
        executive_summary = await synthesizer.generate_executive_summary(
            threads=threads,
            dossiers=dossiers,
            global_pulse=global_pulse,
            date_range=f"{date_range_start} to {date_range_end}",
        )
        
        regional_contexts = await synthesizer.generate_regional_contexts(
            dossiers=dossiers,
            threads=threads,
        )
        
        source_quality = await synthesizer.generate_source_quality_assessment(dossiers)
        
        # 5. Compile brief
        logger.info("Step 5: Compiling brief")
        brief = WeeklyBrief(
            date_range=f"{date_range_start} to {date_range_end}",
            generated_at=datetime.now(),
            global_pulse=global_pulse,
            executive_summary=executive_summary,
            cross_cutting_threads=threads,
            leader_dossiers=list(dossiers.values()),
            regional_context=regional_contexts,
            methodology_notes=self._generate_methodology_notes(dossiers),
            source_quality_notes=source_quality,
        )
        
        # 6. Save
        brief_path = save_brief(brief)
        logger.info(f"Brief saved to {brief_path}")
        
        return brief
    
    def _generate_methodology_notes(self, dossiers: dict[str, LeaderDossier]) -> str:
        """Generate methodology disclosure."""
        total_articles = sum(len(d.articles) for d in dossiers.values())
        sources = set()
        for d in dossiers.values():
            for a in d.articles:
                sources.add(a.source_name)
        
        return f"""
**Methodology**

This brief was generated using an automated multi-agent system that:
1. Fetched {total_articles} articles from {len(sources)} sources
2. Translated non-English content using LLM translation
3. Classified articles using the Paragon taxonomy
4. Filtered to priority score ≥ 0.4
5. Clustered underlying events to detect cross-cutting threads
6. Synthesized findings into narrative sections

**Limitations**: Automated classification may miss nuance. Non-English 
translation may lose political subtlety. Thread detection uses semantic
similarity and may over- or under-cluster.
"""
    
    async def run_single_leader(
        self,
        leader_name: str,
        date_range_start: Optional[str] = None,
        date_range_end: Optional[str] = None,
    ) -> LeaderDossier:
        """
        Run the pipeline for a single leader (useful for testing).
        """
        # Find leader config
        leaders = get_leader_configs()
        leader = next((l for l in leaders if l.name == leader_name), None)
        
        if not leader:
            raise ValueError(f"Unknown leader: {leader_name}")
        
        # Run with just this leader
        brief = await self.run(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            leaders=[leader],
        )
        
        # Return just the dossier
        if brief.leader_dossiers:
            return brief.leader_dossiers[0]
        
        raise RuntimeError(f"No dossier generated for {leader_name}")


# Export for convenience
__all__ = ["PDBWorkflow"]
