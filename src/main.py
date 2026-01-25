"""
CLI entry point for the PDB Aggregator.

Usage:
    python -m src.main                          # Full run with all leaders
    python -m src.main --leader "Mark Carney"   # Single leader
    python -m src.main --simple                 # Simple pipeline (no LangGraph)
    python -m src.main --list-briefs            # List stored briefs
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timedelta

from .config import get_leader_configs
from .graph import PDBWorkflow
from .persistence import list_briefs, load_brief
from pathlib import Path


def setup_logging(level: str = "INFO"):
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Reduce noise from httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Presidential Daily Brief style intelligence reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                              # Full run, last 7 days
  python -m src.main --leader "Mark Carney"       # Single leader
  python -m src.main --start 2026-01-13 --end 2026-01-21
  python -m src.main --simple --leader "Claudia Sheinbaum"
  python -m src.main --list-briefs
  python -m src.main --list-leaders
        """
    )
    
    parser.add_argument(
        "--leader",
        type=str,
        help="Process only this leader (by name)",
    )
    
    parser.add_argument(
        "--start",
        type=str,
        help="Start date (YYYY-MM-DD), defaults to 7 days ago",
    )
    
    parser.add_argument(
        "--end",
        type=str,
        help="End date (YYYY-MM-DD), defaults to today",
    )
    
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Use simple pipeline without LangGraph (easier debugging)",
    )
    
    parser.add_argument(
        "--list-briefs",
        action="store_true",
        help="List all stored briefs",
    )
    
    parser.add_argument(
        "--list-leaders",
        action="store_true",
        help="List all tracked leaders",
    )
    
    parser.add_argument(
        "--view-brief",
        type=str,
        metavar="PATH",
        help="View a specific brief by path",
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    
    return parser.parse_args()


def cmd_list_briefs():
    """List all stored briefs."""
    briefs = list_briefs()
    
    if not briefs:
        print("No briefs found.")
        return
    
    print(f"Found {len(briefs)} briefs:\n")
    
    for brief in briefs:
        print(f"  {brief.get('path', 'Unknown')}")
        print(f"    Period: {brief.get('date_range', 'Unknown')}")
        print(f"    Generated: {brief.get('generated_at', 'Unknown')}")
        print(f"    Leaders: {brief.get('leader_count', 0)}")
        print(f"    Threads: {brief.get('thread_count', 0)}")
        print()


def cmd_list_leaders():
    """List all tracked leaders."""
    leaders = get_leader_configs()
    
    print(f"Tracking {len(leaders)} leaders:\n")
    
    # Group by region
    by_region = {}
    for leader in leaders:
        if leader.region not in by_region:
            by_region[leader.region] = []
        by_region[leader.region].append(leader)
    
    region_names = {
        "europe": "Europe",
        "americas": "Americas",
        "asia_pacific": "Asia-Pacific",
    }
    
    for region in ["europe", "americas", "asia_pacific"]:
        if region not in by_region:
            continue
        
        print(f"{region_names.get(region, region)}:")
        for leader in by_region[region]:
            sources = ", ".join(s.name for s in leader.domestic_sources[:3])
            print(f"  • {leader.name} ({leader.title}, {leader.country})")
            print(f"    Sources: {sources}")
        print()


def cmd_view_brief(path: str):
    """View a specific brief."""
    brief_path = Path(path)
    
    if not brief_path.exists():
        print(f"Brief not found: {path}")
        return
    
    # Try to read the markdown file
    markdown_path = brief_path / "brief.md"
    
    if markdown_path.exists():
        with open(markdown_path) as f:
            print(f.read())
    else:
        # Fall back to loading and printing
        brief = load_brief(brief_path)
        if brief:
            print(f"Brief: {brief.date_range}")
            print(f"Generated: {brief.generated_at}")
            print()
            print(brief.executive_summary)
        else:
            print(f"Could not load brief from {path}")


async def cmd_run(args):
    """Run the workflow."""
    workflow = PDBWorkflow(use_langgraph=not args.simple)
    
    # Determine leaders to process
    leaders = None
    if args.leader:
        all_leaders = get_leader_configs()
        matching = [l for l in all_leaders if l.name.lower() == args.leader.lower()]
        
        if not matching:
            # Try partial match
            matching = [l for l in all_leaders if args.leader.lower() in l.name.lower()]
        
        if not matching:
            print(f"Leader not found: {args.leader}")
            print("Use --list-leaders to see available leaders")
            return
        
        leaders = matching
        print(f"Processing leader(s): {', '.join(l.name for l in leaders)}")
    
    # Determine date range
    date_end = args.end or datetime.now().strftime("%Y-%m-%d")
    date_start = args.start
    
    if not date_start:
        start = datetime.now() - timedelta(days=7)
        date_start = start.strftime("%Y-%m-%d")
    
    print(f"Date range: {date_start} to {date_end}")
    print()
    
    # Run workflow
    try:
        brief = await workflow.run(
            date_range_start=date_start,
            date_range_end=date_end,
            leaders=leaders,
        )
        
        print()
        print("=" * 60)
        print("BRIEF GENERATED SUCCESSFULLY")
        print("=" * 60)
        print()
        print(f"Period: {brief.date_range}")
        print(f"Leaders: {len(brief.leader_dossiers)}")
        print(f"Threads: {len(brief.cross_cutting_threads)}")
        print()
        print("Executive Summary (preview):")
        print("-" * 40)
        print(brief.executive_summary[:500] + "..." if len(brief.executive_summary) > 500 else brief.executive_summary)
        print()
        
        if brief.cross_cutting_threads:
            print("Cross-Cutting Threads:")
            for thread in brief.cross_cutting_threads:
                print(f"  • {thread.title} ({thread.leader_count} leaders)")
        
        print()
        print("Full brief saved to: briefs/")
        
    except Exception as e:
        print(f"Error running workflow: {e}")
        logging.exception("Workflow failed")
        sys.exit(1)


def main():
    """Main entry point."""
    args = parse_args()
    setup_logging(args.log_level)
    
    if args.list_briefs:
        cmd_list_briefs()
        return
    
    if args.list_leaders:
        cmd_list_leaders()
        return
    
    if args.view_brief:
        cmd_view_brief(args.view_brief)
        return
    
    # Run the workflow
    asyncio.run(cmd_run(args))


if __name__ == "__main__":
    main()
