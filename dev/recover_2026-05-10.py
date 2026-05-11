"""
One-off recovery for the 2026-05-10 brief.

The Sun 5/10 Fargate run completed all country desks (30) and regional
syntheses (6), then crashed at executive synthesis with `KeyError: 'what'`
on a briefing item that the LLM truncated mid-output (hit max_tokens).

Country + regional traces and ledgers are on disk from commit 51453f0
("Brief: 2026-05-10 (FAILED — partial traces + ledgers)"). This script
re-runs executive + newsletter + publishing only, with the executive
defensive guard and bumped max_tokens already in place.

Run from repo root: .venv/bin/python dev/recover_2026-05-10.py
"""

from __future__ import annotations

import asyncio
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitor.agents.executive import run_executive_agent
from src.monitor.cli import _load_pipeline_state
from src.monitor.ledger.storage import save_global_ledger, load_global_ledger, load_story_map
from src.monitor.newsletter.content_builder import build_all_pages
from src.monitor.newsletter.global_writer import write_global_essay
from src.monitor.newsletter.publish import publish_brief
from src.monitor.newsletter.regional_writer import write_all_regional_essays
from src.monitor.newsletter.renderer import render_pages
from src.monitor.newsletter.structured_copyeditor import copyedit_all
from src.monitor.newsletter.structured_editor import edit_all, style_edit_all

END_DATE = date(2026, 5, 10)
CONCURRENCY = 5


async def main() -> None:
    print(f"Recovery start: end_date={END_DATE}")
    country_ledgers, country_entries, regional_reports, _ = _load_pipeline_state(END_DATE)
    global_ledger = load_global_ledger()
    print(
        f"  Loaded: {len(country_ledgers)} country ledgers, "
        f"{len(regional_reports)} regional reports"
    )

    print("Running executive synthesis...")
    global_ledger = await run_executive_agent(regional_reports, global_ledger, END_DATE)
    save_global_ledger(global_ledger)
    latest = global_ledger.latest_entry()
    if latest:
        print(f"  Briefing items: {len(latest.executive_briefing_items)}")

    print("Building structured content...")
    story_maps_data: dict[str, dict] = {}
    for code in country_ledgers:
        try:
            story_maps_data[code] = load_story_map(code, END_DATE)
        except FileNotFoundError:
            pass

    overview_content, region_page_contents, at_a_glance_content = build_all_pages(
        global_ledger, regional_reports, country_ledgers, country_entries, END_DATE,
        story_maps=story_maps_data or None,
    )

    print("Round 1: Editing country summaries...")
    overview_content, region_page_contents = await edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="countries",
    )
    overview_content, region_page_contents, at_a_glance_content = await copyedit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="countries",
        at_a_glance=at_a_glance_content,
    )
    overview_content, region_page_contents = await style_edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="countries",
    )

    print("Writing regional essays...")
    region_page_contents = await write_all_regional_essays(
        region_page_contents, max_concurrent=CONCURRENCY,
    )

    print("Round 2: Editing regional essays...")
    overview_content, region_page_contents = await edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="regional",
    )
    overview_content, region_page_contents, _ = await copyedit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="regional",
    )
    overview_content, region_page_contents = await style_edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="regional",
    )

    print("Writing global essay...")
    overview_content = await write_global_essay(overview_content, region_page_contents)

    print("Round 3: Editing global essay...")
    overview_content, region_page_contents = await edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="executive",
    )
    overview_content, region_page_contents, _ = await copyedit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="executive",
    )
    overview_content, region_page_contents = await style_edit_all(
        overview_content, region_page_contents,
        analysis_date=END_DATE, max_concurrent=CONCURRENCY, scope="executive",
    )

    print("Rendering and publishing...")
    pages = render_pages(overview_content, region_page_contents, at_a_glance_content)
    brief_dir = publish_brief(pages, END_DATE)
    print(f"Recovery complete: published to {brief_dir}")


if __name__ == "__main__":
    asyncio.run(main())
