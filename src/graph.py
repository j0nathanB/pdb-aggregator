"""
Graph module - exports the PDB workflow.

This module provides a cleaner import path for the workflow:
    from src.graph import PDBWorkflow

Supports two execution modes:
- Simple pipeline (default): Sequential async/await, easier debugging
- LangGraph pipeline: Full StateGraph with parallel routing
"""

from typing import Optional
from datetime import datetime, timedelta
import logging

from .config import (
    LeaderConfig,
    LeaderDossier,
    WeeklyBrief,
    GlobalPulse,
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
        logger.info(f"Mode: {'LangGraph' if self.use_langgraph else 'Simple'}")

        # Choose pipeline based on mode
        if self.use_langgraph:
            return await self._run_langgraph_pipeline(
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                leaders=leaders,
            )
        else:
            return await self._run_simple_pipeline(
                date_range_start=date_range_start,
                date_range_end=date_range_end,
                leaders=leaders,
            )

    async def _run_langgraph_pipeline(
        self,
        date_range_start: str,
        date_range_end: str,
        leaders: list[LeaderConfig],
    ) -> WeeklyBrief:
        """
        Run the pipeline using LangGraph orchestration.

        Full StateGraph with parallel leader processing and proper routing.
        """
        from .graph_langgraph import run_pdb_langgraph

        result = await run_pdb_langgraph(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            leaders=leaders,
        )

        brief = result.get("brief")

        if brief:
            return brief
        else:
            raise RuntimeError("LangGraph pipeline did not produce a brief")
    
    async def _run_simple_pipeline(
        self,
        date_range_start: str,
        date_range_end: str,
        leaders: list[LeaderConfig],
    ) -> WeeklyBrief:
        """
        Run the pipeline without LangGraph orchestration.

        Uses bottom-up architecture (no GlobalPulse).
        Useful for debugging and understanding the flow.
        """
        from .agents.source_fetcher import SourceFetcherAgent
        from .agents.translator import TranslatorAgent
        from .agents.classifier import ClassifierAgent
        from .agents.dossier_builder import DossierBuilderAgent
        from .agents.thread_detector import ThreadDetectorAgent
        from .agents.synthesizer import SynthesizerAgent
        from .persistence import save_brief
        from .config import RELEVANCE_THRESHOLD
        from .debug import (
            is_debug_enabled,
            save_fetch_results,
            save_translate_results,
            save_dedupe_results,
            save_classify_results,
            save_dossier_results,
            save_thread_detection_results,
            save_synthesis_results,
            save_final_brief,
            create_pipeline_summary,
        )

        # Bottom-up architecture: no global pulse step
        # Narrative emerges from leader actions

        # 1. Process each leader
        logger.info("Step 1: Processing leaders (bottom-up)")
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

                # Debug: save fetch results
                if is_debug_enabled():
                    source_breakdown = {}
                    for a in articles:
                        src = a.source_name
                        source_breakdown[src] = source_breakdown.get(src, 0) + 1
                    save_fetch_results(leader.name, articles, source_breakdown)

                # Translate
                translated_articles = await translator.translate_batch(articles)
                translated_count = sum(
                    1 for a in translated_articles
                    if a.translated_content and a.original_language != "en"
                )

                # Debug: save translate results
                if is_debug_enabled():
                    save_translate_results(leader.name, translated_articles, translated_count)

                # Dedupe (new step)
                original_count = len(translated_articles)
                deduped_articles = await classifier.summarize_and_dedupe(translated_articles, leader)

                # Debug: save dedupe results
                if is_debug_enabled():
                    save_dedupe_results(leader.name, original_count, deduped_articles)

                # Classify
                classified_articles = await classifier.classify_batch(deduped_articles, leader)

                # Filter
                relevant = [
                    a for a in classified_articles
                    if a.classification and a.classification.priority_score >= RELEVANCE_THRESHOLD
                ]

                # Debug: save classify results
                if is_debug_enabled():
                    save_classify_results(leader.name, classified_articles, len(relevant), RELEVANCE_THRESHOLD)

                # Build dossier (no global_context - bottom-up)
                dossier = await builder.build(
                    leader=leader,
                    articles=relevant,
                    global_context=None,  # Bottom-up: no top-down context
                )

                # Debug: save dossier results
                if is_debug_enabled():
                    save_dossier_results(leader.name, dossier)

                dossiers[leader.name] = dossier
                logger.info(f"    {len(relevant)} relevant articles")

            except Exception as e:
                logger.error(f"  Error processing {leader.name}: {e}")

        await fetcher.close()

        # 2. Detect cross-cutting threads (two-phase: multi-leader + singletons)
        logger.info("Step 2: Detecting threads (two-phase)")
        thread_detector = ThreadDetectorAgent()
        threads = await thread_detector.detect(dossiers, global_context=None)
        logger.info(f"  Found {len(threads)} threads")

        # Debug: save thread detection results
        if is_debug_enabled():
            multi_leader = [t for t in threads if not t.is_singleton]
            singletons = [t for t in threads if t.is_singleton]

            save_thread_detection_results(
                phase="multi_leader",
                threads=multi_leader,
                input_data={
                    "dossier_count": len(dossiers),
                    "leaders": list(dossiers.keys()),
                },
            )
            save_thread_detection_results(
                phase="singletons",
                threads=singletons,
                input_data={
                    "candidates_found": len(singletons),
                },
            )

        # 3. Generate synthesis
        logger.info("Step 3: Generating synthesis")
        synthesizer = SynthesizerAgent()

        executive_summary = await synthesizer.generate_executive_summary(
            threads=threads,
            dossiers=dossiers,
            global_pulse=None,  # Bottom-up: no top-down context
            date_range=f"{date_range_start} to {date_range_end}",
        )

        # Debug: save executive summary
        if is_debug_enabled():
            save_synthesis_results("executive_summary", {
                "summary": executive_summary,
                "thread_count": len(threads),
                "dossier_count": len(dossiers),
            })

        regional_contexts = await synthesizer.generate_regional_contexts(
            dossiers=dossiers,
            threads=threads,
        )

        # Debug: save regional contexts
        if is_debug_enabled():
            save_synthesis_results("regional_contexts", regional_contexts)

        source_quality = await synthesizer.generate_source_quality_assessment(dossiers)

        # Debug: save source quality
        if is_debug_enabled():
            save_synthesis_results("source_quality", source_quality)

        # 4. Compile brief
        logger.info("Step 4: Compiling brief")
        brief = WeeklyBrief(
            date_range=f"{date_range_start} to {date_range_end}",
            generated_at=datetime.now(),
            global_pulse=None,  # Bottom-up: no GlobalPulse
            executive_summary=executive_summary,
            cross_cutting_threads=threads,
            leader_dossiers=list(dossiers.values()),
            regional_context=regional_contexts,
            methodology_notes=self._generate_methodology_notes(dossiers),
            source_quality_notes=source_quality,
        )

        # 5. Save
        brief_path = save_brief(brief)
        logger.info(f"Brief saved to {brief_path}")

        # Debug: save final brief and pipeline summary
        if is_debug_enabled():
            save_final_brief(brief)

            # Create pipeline summary
            leader_stats = {
                "total": len(dossiers),
                "by_region": {},
            }
            for name, dossier in dossiers.items():
                region = dossier.leader.region
                if region not in leader_stats["by_region"]:
                    leader_stats["by_region"][region] = []
                leader_stats["by_region"][region].append({
                    "name": name,
                    "article_count": len(dossier.articles),
                    "action_count": len(dossier.key_actions),
                    "event_count": len(dossier.underlying_events),
                })

            thread_stats = {
                "total": len(threads),
                "multi_leader": sum(1 for t in threads if not t.is_singleton),
                "singletons": sum(1 for t in threads if t.is_singleton),
            }

            create_pipeline_summary(leader_stats, thread_stats)

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
3. Deduplicated articles covering the same underlying events
4. Classified articles using the Paragon taxonomy
5. Filtered to priority score >= 0.4
6. Built per-leader dossiers using bottom-up synthesis
7. Detected cross-cutting threads (multi-leader + singletons)
8. Synthesized findings into narrative sections

**Architecture**: Bottom-up approach where narrative emerges from leader
actions rather than top-down global context framing.

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
