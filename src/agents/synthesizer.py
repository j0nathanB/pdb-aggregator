"""
Synthesizer Agent - Generates final brief narrative sections.

Produces:
- Executive summary (3-4 paragraphs)
- Regional context (Europe, Americas, Asia-Pacific)
- Source quality notes
"""

import logging
from typing import Optional

from ..config import (
    LeaderDossier,
    CrossCuttingThread,
    GlobalPulse,
    REGION_DISPLAY_NAMES,
    REGION_ORDER,
    get_leaders_by_region,
)
from .base import complete, with_retry

logger = logging.getLogger(__name__)


EXECUTIVE_SUMMARY_SYSTEM = """You are a senior intelligence analyst writing an executive summary 
for a weekly brief on world leaders.

Your executive summary should:
- Lead with the most significant development of the week
- Highlight 2-3 key cross-cutting themes
- Note any concerning trajectories or opportunities
- Be 3-4 paragraphs, written in clear analytical prose
- Avoid bullet points or lists
- Use specific names and details, not vague generalities

Write for a busy executive who needs to understand the key takeaways quickly.
"""


REGIONAL_CONTEXT_SYSTEM = """You are a regional analyst providing context for leader activities.

Your regional summary should:
- Explain the regional dynamics affecting the leaders
- Note key bilateral relationships and tensions
- Identify regional trends or patterns
- Be 2-3 paragraphs of analytical prose
- Reference specific events and developments
"""


class SynthesizerAgent:
    """
    Generates the final narrative sections of the weekly brief.
    
    Takes structured data (dossiers, threads) and synthesizes
    into readable analytical prose.
    """
    
    @with_retry(max_attempts=2)
    async def generate_executive_summary(
        self,
        threads: list[CrossCuttingThread],
        dossiers: dict[str, LeaderDossier],
        global_pulse: Optional[GlobalPulse],
        date_range: str,
    ) -> str:
        """
        Generate the executive summary section.
        
        Args:
            threads: Cross-cutting threads
            dossiers: Leader dossiers
            global_pulse: Global context
            date_range: Reporting period
            
        Returns:
            Executive summary text (3-4 paragraphs)
        """
        logger.info("Generating executive summary")
        
        # Format inputs for prompt
        threads_summary = self._format_threads(threads)
        dossiers_summary = self._format_dossiers(dossiers)
        global_context = self._format_global_pulse(global_pulse)
        
        prompt = f"""Write an executive summary for a weekly intelligence brief covering {date_range}.

{global_context}

CROSS-CUTTING THREADS:
{threads_summary}

LEADER HIGHLIGHTS:
{dossiers_summary}

Write 3-4 paragraphs that synthesize the most important developments, themes, and trajectories.
Lead with what matters most.
"""
        
        response = await complete(
            prompt=prompt,
            system=EXECUTIVE_SUMMARY_SYSTEM,
            temperature=0.4,
            max_tokens=1500,
        )
        
        return response.strip()
    
    @with_retry(max_attempts=2)
    async def generate_regional_contexts(
        self,
        dossiers: dict[str, LeaderDossier],
        threads: list[CrossCuttingThread],
    ) -> dict[str, str]:
        """
        Generate regional context sections.
        
        Args:
            dossiers: Leader dossiers
            threads: Cross-cutting threads
            
        Returns:
            Map of region -> context text
        """
        logger.info("Generating regional contexts")
        
        regional_contexts = {}
        
        # Group dossiers by region
        leaders_by_region = get_leaders_by_region()
        
        for region in REGION_ORDER:
            region_name = REGION_DISPLAY_NAMES.get(region, region)
            
            # Get dossiers for this region
            region_leaders = leaders_by_region.get(region, [])
            region_dossiers = {
                name: dossier
                for name, dossier in dossiers.items()
                if any(l.name == name for l in region_leaders)
            }
            
            if not region_dossiers:
                regional_contexts[region] = f"No coverage for {region_name} this period."
                continue
            
            # Get threads involving this region's leaders
            region_threads = [
                t for t in threads
                if any(name in t.leader_postures for name in region_dossiers.keys())
            ]
            
            context = await self._generate_single_regional_context(
                region_name=region_name,
                dossiers=region_dossiers,
                threads=region_threads,
            )
            
            regional_contexts[region] = context
        
        return regional_contexts
    
    async def _generate_single_regional_context(
        self,
        region_name: str,
        dossiers: dict[str, LeaderDossier],
        threads: list[CrossCuttingThread],
    ) -> str:
        """Generate context for a single region."""
        
        dossiers_summary = self._format_dossiers(dossiers)
        threads_summary = self._format_threads(threads) if threads else "No cross-cutting threads."
        
        prompt = f"""Write a regional context section for {region_name}.

LEADERS IN THIS REGION:
{dossiers_summary}

RELEVANT THREADS:
{threads_summary}

Write 2-3 paragraphs analyzing:
- Key regional dynamics affecting these leaders
- Bilateral relationships and tensions
- Regional trends or patterns emerging
"""
        
        response = await complete(
            prompt=prompt,
            system=REGIONAL_CONTEXT_SYSTEM,
            temperature=0.4,
            max_tokens=800,
        )
        
        return response.strip()
    
    def _format_threads(self, threads: list[CrossCuttingThread]) -> str:
        """Format threads for prompt inclusion."""
        if not threads:
            return "No cross-cutting threads identified."
        
        formatted = []
        for thread in threads[:5]:  # Top 5
            leaders = ", ".join(thread.leader_postures.keys())
            formatted.append(
                f"• {thread.title}\n"
                f"  Leaders: {leaders}\n"
                f"  {thread.description}\n"
                f"  Trajectory: {thread.trajectory}"
            )
        
        return "\n\n".join(formatted)
    
    def _format_dossiers(self, dossiers: dict[str, LeaderDossier]) -> str:
        """Format dossiers for prompt inclusion."""
        if not dossiers:
            return "No dossiers available."
        
        formatted = []
        for name, dossier in dossiers.items():
            # Get top actions
            actions = [a.description for a in dossier.key_actions[:2]]
            actions_str = "; ".join(actions) if actions else "No significant actions"
            
            formatted.append(
                f"• {name} ({dossier.leader.title}, {dossier.leader.country})\n"
                f"  Key actions: {actions_str}\n"
                f"  Assessment: {dossier.assessment[:200]}..."
            )
        
        return "\n\n".join(formatted)
    
    def _format_global_pulse(self, pulse: Optional[GlobalPulse]) -> str:
        """Format global pulse for prompt inclusion."""
        if not pulse or not pulse.top_stories:
            return ""
        
        stories = "\n".join(f"- {s}" for s in pulse.top_stories[:5])
        
        return f"""GLOBAL CONTEXT:
{stories}
"""
    
    async def generate_source_quality_assessment(
        self,
        dossiers: dict[str, LeaderDossier],
    ) -> str:
        """
        Generate a source quality assessment section.
        
        Notes any gaps, biases, or reliability concerns.
        """
        concerns = []
        
        for name, dossier in dossiers.items():
            # Check for state media
            state_media_count = sum(
                1 for a in dossier.articles 
                if a.source_type == "state_media"
            )
            if state_media_count > 0:
                concerns.append(
                    f"**{name}**: {state_media_count} state media articles included - "
                    "content may reflect official messaging rather than ground truth."
                )
            
            # Check for limited coverage
            if len(dossier.articles) < 3:
                concerns.append(
                    f"**{name}**: Limited source coverage ({len(dossier.articles)} articles) - "
                    "assessment confidence is lower."
                )
            
            # Include any dossier-specific notes
            if dossier.source_quality_notes and "Good source" not in dossier.source_quality_notes:
                concerns.append(f"**{name}**: {dossier.source_quality_notes}")
        
        if not concerns:
            return "Source coverage was adequate across all leaders with no significant gaps or reliability concerns."
        
        return "\n".join(concerns)
