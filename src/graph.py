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

        Story-centric architecture:
        1. Per-leader clustering + dossier build (story-centric output)
        2. Aggregate briefing (replaces thread detection + synthesis)
        3. Source quality assessment
        4. Compile WeeklyBrief
        5. Save
        """
        from .agents.event_clustering import EventClusteringAgent
        from .agents.dossier_builder import DossierBuilderAgent
        from .agents.aggregate_builder import AggregateBriefingBuilder
        from .agents.synthesizer import SynthesizerAgent
        from .persistence import save_brief, generate_email
        from .debug import (
            is_debug_enabled,
            save_dossier_results,
            save_synthesis_results,
            save_final_brief,
            create_pipeline_summary,
        )

        # Step 1: Process each leader via event clustering pipeline
        logger.info("Step 1: Processing leaders (event clustering + story-centric dossier)")
        dossiers: dict[str, LeaderDossier] = {}

        clustering_agent = EventClusteringAgent()
        builder = DossierBuilderAgent()

        for leader in leaders:
            logger.info(f"  Processing: {leader.name}")

            try:
                top_events, rest_events, opinions = await clustering_agent.process_leader(
                    leader=leader,
                    date_start=date_range_start,
                    date_end=date_range_end,
                )

                articles_processed = sum(
                    len(e.articles) for e in top_events + rest_events
                )
                logger.info(
                    f"    {len(top_events)} top events, "
                    f"{len(rest_events)} remaining, "
                    f"{len(opinions)} opinions, "
                    f"{articles_processed} articles fetched"
                )

                dossier = await builder.build_from_events(
                    leader=leader,
                    top_events=top_events,
                    remaining_events=rest_events,
                    opinions=opinions,
                    date_start=date_range_start,
                    date_end=date_range_end,
                )

                if is_debug_enabled():
                    save_dossier_results(leader.name, dossier)

                dossiers[leader.name] = dossier

            except Exception as e:
                logger.error(f"  Error processing {leader.name}: {e}")

        # Step 2: Aggregate briefing (replaces thread detection + synthesis)
        logger.info("Step 2: Building aggregate briefing")
        aggregate_builder = AggregateBriefingBuilder()
        main_stories, intl_stories, dom_stories, btl, executive_summary = await aggregate_builder.build(
            dossiers
        )
        logger.info(
            f"  Aggregate: {len(main_stories)} main, "
            f"{len(intl_stories)} intl, {len(dom_stories)} dom, "
            f"{len(btl)} BTL"
        )

        if is_debug_enabled():
            save_synthesis_results("aggregate_briefing", {
                "main_stories": len(main_stories),
                "international_stories": len(intl_stories),
                "domestic_stories": len(dom_stories),
                "between_the_lines": btl,
                "executive_summary": executive_summary[:100] + "..." if len(executive_summary) > 100 else executive_summary,
            })

        # Step 3: Source quality assessment
        logger.info("Step 3: Source quality assessment")
        synthesizer = SynthesizerAgent()
        source_quality = await synthesizer.generate_source_quality_assessment(dossiers)

        if is_debug_enabled():
            save_synthesis_results("source_quality", source_quality)

        # Step 4: Compile brief
        logger.info("Step 4: Compiling brief")
        brief = WeeklyBrief(
            date_range=f"{date_range_start} to {date_range_end}",
            generated_at=datetime.now(),
            main_stories=main_stories,
            international_stories=intl_stories,
            domestic_stories=dom_stories,
            between_the_lines=btl,
            executive_summary=executive_summary,
            leader_dossiers=list(dossiers.values()),
            methodology_notes=self._generate_methodology_notes(dossiers),
            source_quality_notes=source_quality,
        )

        # Step 5: Save
        brief_path = save_brief(brief)
        logger.info(f"Brief saved to {brief_path}")

        # Step 6: Generate email digest
        try:
            email_path = await generate_email(brief, brief_path)
            logger.info(f"Email digest saved to {email_path}")
        except Exception as e:
            logger.error(f"Email digest generation failed (non-fatal): {e}")

        if is_debug_enabled():
            save_final_brief(brief)

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
                    "story_count": len(dossier.main_stories)
                        + len(dossier.international_stories)
                        + len(dossier.domestic_stories),
                })

            aggregate_stats = {
                "main_stories": len(main_stories),
                "international_stories": len(intl_stories),
                "domestic_stories": len(dom_stories),
                "between_the_lines": len(btl),
            }

            create_pipeline_summary(leader_stats, aggregate_stats)

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
1. Fetched snippets from {len(sources)} sources via SearchAPI
2. Embedded snippets using sentence-transformers (English or multilingual model per leader)
3. Clustered snippets into events using HDBSCAN
4. Scored events by source diversity and wire coverage
5. Fetched {total_articles} full articles for top events via Diffbot
6. Extracted entities and summaries via Diffbot NLP
7. Built per-leader story-centric dossiers from processed events
8. Matched overlapping stories across leaders via entity overlap
9. Synthesized aggregate briefing with shared multi-leader stories

**Architecture**: Story-centric pipeline where events are synthesized into
stories, then matched across leaders for aggregate briefing.

**Limitations**: Embedding-based clustering may miss nuance in short
snippets. Non-English content processed after extraction. Entity-based
story matching may miss thematic connections without shared entities.
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
