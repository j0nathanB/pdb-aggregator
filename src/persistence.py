"""
Persistence layer for saving and loading briefs.

Briefs are stored in a structured directory format:
    briefs/
        YYYYMMDD/
            brief.md          # Human-readable Markdown
            dossiers.json     # Structured leader data
            threads.json      # Cross-cutting threads
            meta.json         # Brief metadata
            output.json       # Full serialized output
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import asdict, is_dataclass
import logging

from .config import (
    WeeklyBrief,
    LeaderDossier,
    CrossCuttingThread,
    GlobalPulse,
)

logger = logging.getLogger(__name__)


# Default briefs directory
BRIEFS_DIR = Path("briefs")


def _serialize(obj):
    """Custom JSON serializer for dataclasses and datetime."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "value"):  # Enum
        return obj.value
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def save_brief(
    brief: WeeklyBrief,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Save a weekly brief to disk.
    
    Args:
        brief: The WeeklyBrief to save
        output_dir: Custom output directory (default: briefs/YYYYMMDD)
        
    Returns:
        Path to the saved brief directory
    """
    # Determine output directory
    if output_dir is None:
        date_str = datetime.now().strftime("%Y%m%d")
        output_dir = BRIEFS_DIR / date_str
    
    # Create directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving brief to {output_dir}")
    
    # 1. Save full output as JSON
    output_path = output_dir / "output.json"
    with open(output_path, "w") as f:
        json.dump(brief, f, default=_serialize, indent=2)
    
    # 2. Save dossiers separately
    dossiers_path = output_dir / "dossiers.json"
    dossiers_data = [asdict(d) for d in brief.leader_dossiers]
    with open(dossiers_path, "w") as f:
        json.dump(dossiers_data, f, default=_serialize, indent=2)
    
    # 3. Save threads separately
    threads_path = output_dir / "threads.json"
    threads_data = [asdict(t) for t in brief.cross_cutting_threads]
    with open(threads_path, "w") as f:
        json.dump(threads_data, f, default=_serialize, indent=2)
    
    # 4. Save metadata
    meta_path = output_dir / "meta.json"
    meta = {
        "date_range": brief.date_range,
        "generated_at": brief.generated_at.isoformat() if brief.generated_at else None,
        "leader_count": len(brief.leader_dossiers),
        "thread_count": len(brief.cross_cutting_threads),
        "methodology_notes": brief.methodology_notes,
        "source_quality_notes": brief.source_quality_notes,
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    
    # 5. Generate and save Markdown brief
    markdown_path = output_dir / "brief.md"
    markdown_content = _generate_markdown(brief)
    with open(markdown_path, "w") as f:
        f.write(markdown_content)
    
    logger.info(f"Brief saved: {output_dir}")
    
    return output_dir


def _generate_markdown(brief: WeeklyBrief) -> str:
    """Generate a human-readable Markdown brief."""
    sections = []
    
    # Header
    sections.append(f"# Weekly Intelligence Brief")
    sections.append(f"**Period:** {brief.date_range}")
    sections.append(f"**Generated:** {brief.generated_at.strftime('%Y-%m-%d %H:%M') if brief.generated_at else 'Unknown'}")
    sections.append("")
    
    # Executive Summary
    sections.append("## Executive Summary")
    sections.append("")
    sections.append(brief.executive_summary)
    sections.append("")
    
    # Cross-Cutting Threads
    if brief.cross_cutting_threads:
        sections.append("## Cross-Cutting Threads")
        sections.append("")
        
        for thread in brief.cross_cutting_threads:
            sections.append(f"### {thread.title}")
            sections.append("")
            sections.append(thread.description)
            sections.append("")
            
            if thread.leader_postures:
                sections.append("**Leader Positions:**")
                for leader, posture in thread.leader_postures.items():
                    sections.append(f"- **{leader}:** {posture}")
                sections.append("")
            
            if thread.trajectory:
                sections.append(f"**Trajectory:** {thread.trajectory}")
                sections.append("")
    
    # Leader Briefs
    sections.append("## Leader Briefs")
    sections.append("")
    
    for dossier in brief.leader_dossiers:
        sections.append(f"### {dossier.leader.name}")
        sections.append(f"*{dossier.leader.title}, {dossier.leader.country}*")
        sections.append("")
        
        if dossier.key_actions:
            sections.append("**Key Actions:**")
            for action in dossier.key_actions:
                sections.append(f"- {action.description}")
                if action.significance:
                    sections.append(f"  - *{action.significance}*")
            sections.append("")
        
        if dossier.domestic_context:
            sections.append("**Domestic Context:**")
            sections.append(dossier.domestic_context)
            sections.append("")
        
        if dossier.international_posture:
            sections.append("**International Posture:**")
            sections.append(dossier.international_posture)
            sections.append("")
        
        if dossier.assessment:
            sections.append("**Assessment:**")
            sections.append(dossier.assessment)
            sections.append("")
    
    # Regional Context
    if brief.regional_context:
        sections.append("## Regional Context")
        sections.append("")
        
        region_names = {
            "europe": "Europe",
            "americas": "Americas",
            "asia_pacific": "Asia-Pacific",
        }
        
        for region, context in brief.regional_context.items():
            sections.append(f"### {region_names.get(region, region)}")
            sections.append("")
            sections.append(context)
            sections.append("")
    
    # Source Quality Notes
    sections.append("## Source Quality Notes")
    sections.append("")
    sections.append(brief.source_quality_notes)
    sections.append("")
    
    # Methodology
    sections.append("## Methodology")
    sections.append("")
    sections.append(brief.methodology_notes)
    sections.append("")
    
    # Appendix: Sources
    sections.append("## Appendix: Sources Consulted")
    sections.append("")
    
    all_sources = set()
    for dossier in brief.leader_dossiers:
        for article in dossier.articles:
            all_sources.add(article.source_name)
    
    for source in sorted(all_sources):
        sections.append(f"- {source}")
    
    return "\n".join(sections)


def load_brief(brief_dir: Path) -> Optional[WeeklyBrief]:
    """
    Load a brief from disk.
    
    Args:
        brief_dir: Path to brief directory
        
    Returns:
        WeeklyBrief or None if not found
    """
    output_path = brief_dir / "output.json"
    
    if not output_path.exists():
        logger.warning(f"Brief not found: {output_path}")
        return None
    
    with open(output_path) as f:
        data = json.load(f)
    
    # Reconstruct WeeklyBrief
    # Note: This is simplified - full reconstruction would need proper deserialization
    return _deserialize_brief(data)


def _deserialize_brief(data: dict) -> WeeklyBrief:
    """Deserialize a brief from JSON data."""
    from .config import (
        LeaderConfig,
        SourceConfig,
        Article,
        ArticleClassification,
        LeaderAction,
        UnderlyingEvent,
        EventType,
        LeaderRole,
        ImpactLevel,
    )
    
    # Helper to parse datetime
    def parse_datetime(val):
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        return datetime.fromisoformat(val)
    
    # Deserialize leader dossiers
    dossiers = []
    for d in data.get("leader_dossiers", []):
        leader_data = d.get("leader", {})
        
        # Reconstruct domestic sources
        domestic_sources = [
            SourceConfig(
                name=s.get("name", ""),
                url=s.get("url", ""),
                language=s.get("language", "en"),
                source_type=s.get("source_type", "domestic"),
                rss_url=s.get("rss_url"),
            )
            for s in leader_data.get("domestic_sources", [])
        ]
        
        leader = LeaderConfig(
            name=leader_data.get("name", ""),
            title=leader_data.get("title", ""),
            country=leader_data.get("country", ""),
            region=leader_data.get("region", ""),
            domestic_sources=domestic_sources,
        )
        
        # Reconstruct key actions
        key_actions = [
            LeaderAction(
                description=a.get("description", ""),
                event_type=EventType(a.get("event_type", "other")),
                date=parse_datetime(a.get("date")),
                source_articles=a.get("source_articles", []),
                significance=a.get("significance", ""),
            )
            for a in d.get("key_actions", [])
        ]
        
        dossier = LeaderDossier(
            leader=leader,
            reporting_period=d.get("reporting_period", ""),
            key_actions=key_actions,
            domestic_context=d.get("domestic_context", ""),
            international_posture=d.get("international_posture", ""),
            assessment=d.get("assessment", ""),
            articles=[],  # Simplified - not fully reconstructing articles
            underlying_events=[],
            source_quality_notes=d.get("source_quality_notes", ""),
            generated_at=parse_datetime(d.get("generated_at")),
        )
        dossiers.append(dossier)
    
    # Deserialize threads
    threads = [
        CrossCuttingThread(
            id=t.get("id", ""),
            title=t.get("title", ""),
            description=t.get("description", ""),
            leader_postures=t.get("leader_postures", {}),
            leader_count=t.get("leader_count", 0),
            event_ids=t.get("event_ids", []),
            tension_points=t.get("tension_points", []),
            convergence_points=t.get("convergence_points", []),
            trajectory=t.get("trajectory", ""),
        )
        for t in data.get("cross_cutting_threads", [])
    ]
    
    # Deserialize global pulse
    gp_data = data.get("global_pulse", {})
    global_pulse = GlobalPulse(
        top_stories=gp_data.get("top_stories", []),
        key_themes=gp_data.get("key_themes", []),
        date_range=gp_data.get("date_range", ""),
    )
    
    return WeeklyBrief(
        date_range=data.get("date_range", ""),
        generated_at=parse_datetime(data.get("generated_at")),
        global_pulse=global_pulse,
        executive_summary=data.get("executive_summary", ""),
        cross_cutting_threads=threads,
        leader_dossiers=dossiers,
        regional_context=data.get("regional_context", {}),
        methodology_notes=data.get("methodology_notes", ""),
        source_quality_notes=data.get("source_quality_notes", ""),
    )


def load_latest_brief() -> Optional[WeeklyBrief]:
    """Load the most recent brief."""
    if not BRIEFS_DIR.exists():
        return None
    
    # Find most recent directory
    dirs = sorted(BRIEFS_DIR.iterdir(), reverse=True)
    
    for d in dirs:
        if d.is_dir() and (d / "output.json").exists():
            return load_brief(d)
    
    return None


def list_briefs() -> list[dict]:
    """List all available briefs with metadata."""
    if not BRIEFS_DIR.exists():
        return []
    
    briefs = []
    
    for d in sorted(BRIEFS_DIR.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        
        meta_path = d / "meta.json"
        if meta_path.exists():
            with open(meta_path) as f:
                meta = json.load(f)
            meta["path"] = str(d)
            briefs.append(meta)
    
    return briefs
