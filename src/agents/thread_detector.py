"""
Thread Detector Agent - Detects cross-cutting themes across leaders.

Uses semantic clustering of underlying events to find:
- Shared themes connecting multiple leaders
- Divergent postures on common issues
- Tension and convergence points
"""

import logging
from typing import Optional
from collections import defaultdict
import hashlib

from ..config import (
    LeaderDossier,
    CrossCuttingThread,
    GlobalPulse,
    UnderlyingEvent,
)
from .base import complete, with_retry, extract_json_from_response, process_batch

logger = logging.getLogger(__name__)


THREAD_SYSTEM = """You are an intelligence analyst identifying cross-cutting themes in world leader activities.

Your task is to find CONNECTIONS between different leaders' actions - themes, events, or issues 
that multiple leaders are responding to or involved in.

Good cross-cutting threads:
- A specific international event multiple leaders addressed (e.g., "NATO summit commitments")
- A shared policy challenge (e.g., "Energy security responses to price spikes")
- Bilateral/multilateral interactions (e.g., "US-EU trade negotiation postures")

Poor threads (avoid):
- Generic categories ("Economic policy") - too vague
- Single-leader activities - must involve 2+ leaders
- Unconnected coincidences - need actual thematic link
"""


class ThreadDetectorAgent:
    """
    Detects cross-cutting threads that connect multiple leaders.
    
    Pipeline:
    1. Collect underlying events from all dossiers
    2. Cluster semantically similar events
    3. For multi-leader clusters, synthesize into threads
    4. Analyze leader postures within each thread
    """
    
    async def detect(
        self,
        dossiers: dict[str, LeaderDossier],
        global_context: Optional[GlobalPulse] = None,
        min_leaders: int = 2,
    ) -> list[CrossCuttingThread]:
        """
        Detect cross-cutting threads from leader dossiers.
        
        Args:
            dossiers: Map of leader name to dossier
            global_context: Global pulse for context
            min_leaders: Minimum leaders required for a thread
            
        Returns:
            List of detected cross-cutting threads
        """
        logger.info(f"Detecting threads from {len(dossiers)} dossiers")
        
        # 1. Collect all underlying events
        all_events: list[tuple[str, UnderlyingEvent]] = []
        for leader_name, dossier in dossiers.items():
            for event in dossier.underlying_events:
                all_events.append((leader_name, event))
        
        if len(all_events) < min_leaders:
            logger.info("Not enough events for thread detection")
            return []
        
        logger.info(f"Analyzing {len(all_events)} underlying events")
        
        # 2. Use LLM to identify clusters (simpler than embedding-based clustering)
        clusters = await self._identify_clusters(all_events, global_context)
        
        # 3. Filter to multi-leader clusters
        multi_leader_clusters = [
            c for c in clusters 
            if len(set(c["leaders"])) >= min_leaders
        ]
        
        logger.info(f"Found {len(multi_leader_clusters)} multi-leader clusters")
        
        # 4. Synthesize each cluster into a thread
        threads = []
        for cluster in multi_leader_clusters:
            thread = await self._synthesize_thread(cluster, dossiers)
            if thread:
                threads.append(thread)
        
        # Sort by number of leaders involved
        threads.sort(key=lambda t: t.leader_count, reverse=True)
        
        return threads
    
    async def _identify_clusters(
        self,
        events: list[tuple[str, UnderlyingEvent]],
        global_context: Optional[GlobalPulse],
    ) -> list[dict]:
        """
        Use LLM to identify thematic clusters of events.
        
        Returns list of clusters, each with:
        - theme: Cluster theme
        - event_indices: Which events belong
        - leaders: Which leaders are involved
        """
        
        # Format events for prompt
        event_list = []
        for i, (leader, event) in enumerate(events):
            event_list.append(f"[{i}] {leader}: {event.description}")
        
        events_text = "\n".join(event_list)
        
        global_context_str = ""
        if global_context and global_context.top_stories:
            global_context_str = f"""
TOP GLOBAL STORIES (for context):
{chr(10).join(f'- {s}' for s in global_context.top_stories)}
"""
        
        prompt = f"""Analyze these underlying events from different world leaders and identify 
THEMATIC CLUSTERS - events that are connected by a common theme, issue, or international event.

{global_context_str}

EVENTS:
{events_text}

For each cluster you identify, provide JSON:
{{
    "clusters": [
        {{
            "theme": "Descriptive theme name (e.g., 'NATO defense spending commitments')",
            "event_indices": [0, 3, 7],
            "connection": "How these events are connected"
        }}
    ]
}}

Rules:
- Each cluster must include events from 2+ DIFFERENT leaders
- Events can only appear in one cluster
- Only create clusters with genuine thematic connections
- Aim for 2-5 clusters maximum
"""
        
        response = await complete(
            prompt=prompt,
            system=THREAD_SYSTEM,
            temperature=0.3,
        )
        
        data = extract_json_from_response(response)
        
        if not data or "clusters" not in data:
            logger.warning("Failed to parse cluster response")
            return []
        
        # Enrich clusters with leader info
        enriched_clusters = []
        for cluster in data["clusters"]:
            indices = cluster.get("event_indices", [])
            leaders = []
            event_ids = []
            
            for idx in indices:
                if idx < len(events):
                    leader_name, event = events[idx]
                    leaders.append(leader_name)
                    event_ids.append(event.id)
            
            enriched_clusters.append({
                "theme": cluster.get("theme", "Unknown theme"),
                "event_indices": indices,
                "leaders": leaders,
                "event_ids": event_ids,
                "connection": cluster.get("connection", ""),
            })
        
        return enriched_clusters
    
    @with_retry(max_attempts=2)
    async def _synthesize_thread(
        self,
        cluster: dict,
        dossiers: dict[str, LeaderDossier],
    ) -> Optional[CrossCuttingThread]:
        """
        Synthesize a cluster into a full CrossCuttingThread.
        
        Analyzes each leader's posture on the theme.
        """
        theme = cluster["theme"]
        leaders = list(set(cluster["leaders"]))
        
        # Gather relevant content for each leader
        leader_content = {}
        for leader_name in leaders:
            if leader_name in dossiers:
                dossier = dossiers[leader_name]
                # Get relevant actions
                actions = [
                    a.description for a in dossier.key_actions
                ][:3]
                leader_content[leader_name] = {
                    "actions": actions,
                    "assessment": dossier.assessment,
                }
        
        # Generate thread synthesis
        prompt = f"""Synthesize this cross-cutting thread involving multiple world leaders.

THEME: {theme}
CONNECTION: {cluster.get('connection', '')}

LEADERS INVOLVED:
{self._format_leader_content(leader_content)}

Generate a thread analysis as JSON:
{{
    "title": "Concise thread title",
    "description": "2-3 sentence description of the thread",
    "leader_postures": {{
        "Leader Name": "Their position/approach on this issue"
    }},
    "tension_points": ["Point of disagreement or competition"],
    "convergence_points": ["Point of agreement or alignment"],
    "trajectory": "Where this thread is heading"
}}
"""
        
        response = await complete(
            prompt=prompt,
            system=THREAD_SYSTEM,
            temperature=0.3,
        )
        
        data = extract_json_from_response(response)
        
        if not data:
            logger.warning(f"Failed to synthesize thread: {theme}")
            return None
        
        # Generate stable ID
        thread_id = hashlib.md5(theme.encode()).hexdigest()[:8]
        
        return CrossCuttingThread(
            id=thread_id,
            title=data.get("title", theme),
            description=data.get("description", ""),
            leader_postures=data.get("leader_postures", {}),
            leader_count=len(leaders),
            event_ids=cluster.get("event_ids", []),
            tension_points=data.get("tension_points", []),
            convergence_points=data.get("convergence_points", []),
            trajectory=data.get("trajectory", ""),
        )
    
    def _format_leader_content(self, leader_content: dict) -> str:
        """Format leader content for prompt."""
        sections = []
        for leader_name, content in leader_content.items():
            actions_str = "\n".join(f"  - {a}" for a in content.get("actions", []))
            sections.append(
                f"{leader_name}:\n"
                f"  Actions:\n{actions_str}\n"
                f"  Assessment: {content.get('assessment', 'N/A')}"
            )
        return "\n\n".join(sections)
    
    async def detect_with_embeddings(
        self,
        dossiers: dict[str, LeaderDossier],
        min_leaders: int = 2,
        eps: float = 0.3,
        min_samples: int = 2,
    ) -> list[CrossCuttingThread]:
        """
        Alternative thread detection using embeddings and DBSCAN clustering.
        
        Requires sentence-transformers or similar for embeddings.
        This is a more sophisticated approach for production use.
        
        Args:
            dossiers: Map of leader name to dossier
            min_leaders: Minimum leaders for a thread
            eps: DBSCAN epsilon parameter
            min_samples: DBSCAN min_samples parameter
            
        Returns:
            List of detected threads
        """
        # This would use actual embeddings - placeholder for now
        logger.warning("Embedding-based clustering not implemented, falling back to LLM")
        return await self.detect(dossiers, min_leaders=min_leaders)
