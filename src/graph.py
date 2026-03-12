"""
Graph module — PDB workflow orchestrator.

Provides both the legacy v1 pipeline (PDBWorkflow) and the new v3
analytical pipeline (AnalyticalPipeline).
"""

from typing import Optional
from datetime import datetime, timedelta
from pathlib import Path
import asyncio
import logging

from .config import (
    BATCH_ENABLED,
    LeaderConfig,
    LeaderDossier,
    WeeklyBrief,
    get_leader_configs,
)
from .running_picture.schema import leader_slug

logger = logging.getLogger(__name__)


# =============================================================================
# V3 ANALYTICAL PIPELINE
# =============================================================================


class AnalyticalPipeline:
    """
    V3 analytical pipeline orchestrator.

    Pipeline stages:
    1. Event clustering (upstream, unchanged)
    2. Cross-Correlation Pass → thematic clusters + Phase 0 trigger
    3. Phase 0 (conditional) → global context brief
    4. Phase 1 Call A per leader → running picture entries
    5. Phase 1 Call B per leader → analytical assessments
    6. Pre-filter (Python) → tier assignment
    7. Phase 2 Renderer → publication output
    8. Save + email
    """

    def __init__(self, baseline_dir: Optional[Path] = None):
        """
        Args:
            baseline_dir: Directory containing country dossiers and leader
                profiles. Expected files: {slug}_country.md, {slug}_profile.md
        """
        self.baseline_dir = baseline_dir or Path("baseline")

    async def run(
        self,
        date_range_start: Optional[str] = None,
        date_range_end: Optional[str] = None,
        leaders: Optional[list[LeaderConfig]] = None,
        running_picture_dir: Optional[Path] = None,
        prior_brief: Optional[str] = None,
    ) -> str:
        """
        Execute the full v3 analytical pipeline.

        Args:
            date_range_start: Start of date range (ISO format)
            date_range_end: End of date range (ISO format)
            leaders: Optional list of leaders (defaults to all)
            running_picture_dir: Override running picture base directory
            prior_brief: Previous week's brief for continuity

        Returns:
            The rendered publication brief text.
        """
        from .agents.event_clustering import EventClusteringAgent
        from .agents.analyst import AnalystAgent
        from .phases.cross_correlation import run_cross_correlation
        from .phases.phase0 import run_phase_0
        from .phases.prefilter import run_prefilter
        from .phases.renderer import run_renderer
        from .phases.consolidation import needs_consolidation, run_consolidation

        if not date_range_end:
            date_range_end = datetime.now().strftime("%Y-%m-%d")
        if not date_range_start:
            start = datetime.now() - timedelta(days=7)
            date_range_start = start.strftime("%Y-%m-%d")
        if not leaders:
            leaders = get_leader_configs()

        base_dir = str(running_picture_dir) if running_picture_dir else None

        logger.info(f"Starting v3 pipeline: {date_range_start} to {date_range_end}")
        logger.info(f"Tracking {len(leaders)} leaders")

        # ------------------------------------------------------------------
        # Step 1: Event clustering (upstream, unchanged)
        # ------------------------------------------------------------------
        logger.info("Step 1: Event clustering")
        clustering_agent = EventClusteringAgent()
        events_by_leader: dict[str, list] = {}

        for leader in leaders:
            try:
                top_events, rest_events, _opinions = await clustering_agent.process_leader(
                    leader=leader,
                    date_start=date_range_start,
                    date_end=date_range_end,
                )
                events_by_leader[leader.name] = top_events + rest_events
                logger.info(
                    f"  {leader.name}: {len(top_events)} top + "
                    f"{len(rest_events)} rest events"
                )
            except Exception as e:
                logger.error(f"  Error clustering {leader.name}: {e}")
                events_by_leader[leader.name] = []

        # ------------------------------------------------------------------
        # Step 2: Cross-Correlation Pass
        # ------------------------------------------------------------------
        logger.info("Step 2: Cross-Correlation Pass")
        cross_result = await run_cross_correlation(
            events_by_leader=events_by_leader,
            leaders=leaders,
            date_start=date_range_start,
            date_end=date_range_end,
        )
        logger.info(
            f"  Clusters identified. Phase 0 trigger: {cross_result.trigger_phase_0}"
        )

        # ------------------------------------------------------------------
        # Step 3: Phase 0 (conditional)
        # ------------------------------------------------------------------
        global_context: Optional[str] = None
        if cross_result.trigger_phase_0:
            logger.info("Step 3: Phase 0 — Global Context Brief")
            global_context = await run_phase_0(cross_result.triggered_clusters)
            logger.info(f"  Global context: {len(global_context)} chars")
        else:
            logger.info("Step 3: Phase 0 skipped (not triggered)")

        # ------------------------------------------------------------------
        # Step 4-5: Phase 1 Call A + Call B per leader
        # ------------------------------------------------------------------
        logger.info("Step 4-5: Phase 1 per-leader analysis")
        analyst = AnalystAgent()
        call_a_outputs: dict[str, str] = {}
        call_b_outputs: dict[str, str] = {}

        for leader in leaders:
            events = events_by_leader.get(leader.name, [])
            country_dossier = self._load_baseline(leader, "country")
            leader_profile = self._load_baseline(leader, "profile")

            try:
                # Call A: structured running picture entry
                entry_text, _parsed = await analyst.run_call_a_and_save(
                    leader=leader,
                    events=events,
                    date_start=date_range_start,
                    date_end=date_range_end,
                    country_dossier=country_dossier,
                    leader_profile=leader_profile,
                    global_context=global_context,
                    base_dir=base_dir,
                )
                call_a_outputs[leader.name] = entry_text
                logger.info(f"  {leader.name}: Call A complete")

                # Call B: analytical assessment
                assessment = await analyst.run_call_b(
                    leader=leader,
                    call_a_output=entry_text,
                    events=events,
                    date_start=date_range_start,
                    date_end=date_range_end,
                    country_dossier=country_dossier,
                    leader_profile=leader_profile,
                    global_context=global_context,
                    base_dir=base_dir,
                )
                call_b_outputs[leader.name] = assessment
                logger.info(f"  {leader.name}: Call B complete")

            except Exception as e:
                logger.error(f"  Error analyzing {leader.name}: {e}")
                call_a_outputs.setdefault(leader.name, "")
                call_b_outputs.setdefault(leader.name, "")

        # ------------------------------------------------------------------
        # Step 6: Pre-filter (pure Python, no LLM)
        # ------------------------------------------------------------------
        logger.info("Step 6: Pre-filtering")
        tiered_leaders = run_prefilter(leaders, call_a_outputs, call_b_outputs)

        tier_counts = {}
        for tl in tiered_leaders:
            tier_counts[tl.tier] = tier_counts.get(tl.tier, 0) + 1
        logger.info(f"  Tiers: {dict(tier_counts)}")

        # ------------------------------------------------------------------
        # Step 7: Phase 2 Renderer
        # ------------------------------------------------------------------
        logger.info("Step 7: Phase 2 rendering")
        phase2_result = await run_renderer(
            tiered_leaders=tiered_leaders,
            clusters_brief=cross_result.clusters_brief,
            date_start=date_range_start,
            date_end=date_range_end,
            prior_brief=prior_brief,
        )
        logger.info(
            f"  Brief rendered: {phase2_result.signal_count} signals, "
            f"{len(phase2_result.leaders_with_assessment)} assessments"
        )

        # ------------------------------------------------------------------
        # Step 8: Post-cycle — consolidation check
        # ------------------------------------------------------------------
        logger.info("Step 8: Consolidation check")
        for leader in leaders:
            if needs_consolidation(leader.name, base_dir=base_dir):
                try:
                    country_dossier = self._load_baseline(leader, "country")
                    leader_profile = self._load_baseline(leader, "profile")
                    await run_consolidation(
                        leader=leader,
                        country_dossier=country_dossier,
                        leader_profile=leader_profile,
                        base_dir=base_dir,
                    )
                    logger.info(f"  Consolidated: {leader.name}")
                except Exception as e:
                    logger.error(f"  Consolidation error for {leader.name}: {e}")

        logger.info("Pipeline complete")
        return phase2_result.brief_text

    def _load_baseline(self, leader: LeaderConfig, doc_type: str) -> str:
        """Load a baseline document (country dossier or leader profile)."""
        slug = leader_slug(leader.name)
        filename = f"{slug}_{doc_type}.md"
        path = self.baseline_dir / filename
        if path.exists():
            return path.read_text()
        logger.warning(f"Baseline document not found: {path}")
        return f"[{doc_type.title()} document not available for {leader.name}]"


# =============================================================================
# LEGACY V1 PIPELINE (preserved for backwards compatibility)
# =============================================================================


class PDBWorkflow:
    """Legacy v1 pipeline. Use AnalyticalPipeline for v3."""

    async def run(
        self,
        date_range_start: Optional[str] = None,
        date_range_end: Optional[str] = None,
        leaders: Optional[list[LeaderConfig]] = None,
    ) -> WeeklyBrief:
        """Execute the legacy PDB generation workflow."""
        if not date_range_end:
            date_range_end = datetime.now().strftime("%Y-%m-%d")
        if not date_range_start:
            start = datetime.now() - timedelta(days=7)
            date_range_start = start.strftime("%Y-%m-%d")
        if not leaders:
            leaders = get_leader_configs()

        logger.info(f"Starting PDB workflow: {date_range_start} to {date_range_end}")
        logger.info(f"Tracking {len(leaders)} leaders")

        return await self._run_pipeline(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            leaders=leaders,
        )

    async def _run_pipeline(
        self,
        date_range_start: str,
        date_range_end: str,
        leaders: list[LeaderConfig],
    ) -> WeeklyBrief:
        """Run the legacy pipeline."""
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

                if BATCH_ENABLED:
                    dossier = await builder.build_from_events_batched(
                        leader=leader,
                        top_events=top_events,
                        remaining_events=rest_events,
                        opinions=opinions,
                        date_start=date_range_start,
                        date_end=date_range_end,
                    )
                else:
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

        logger.info("Step 3: Source quality assessment")
        synthesizer = SynthesizerAgent()
        source_quality = await synthesizer.generate_source_quality_assessment(dossiers)

        if is_debug_enabled():
            save_synthesis_results("source_quality", source_quality)

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

        brief_path = save_brief(brief)
        logger.info(f"Brief saved to {brief_path}")

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
        """Run the legacy pipeline for a single leader."""
        leaders = get_leader_configs()
        leader = next((l for l in leaders if l.name == leader_name), None)

        if not leader:
            raise ValueError(f"Unknown leader: {leader_name}")

        brief = await self.run(
            date_range_start=date_range_start,
            date_range_end=date_range_end,
            leaders=[leader],
        )

        if brief.leader_dossiers:
            return brief.leader_dossiers[0]

        raise RuntimeError(f"No dossier generated for {leader_name}")


__all__ = ["PDBWorkflow", "AnalyticalPipeline"]
