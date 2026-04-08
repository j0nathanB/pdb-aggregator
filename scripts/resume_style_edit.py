"""
Resume 2026-02-15 pipeline: reconstruct pages from traces, style edit, publish.

Reconstructs post-editor pages from trace files (skipping copyeditor),
runs style editor on all region pages (executive already done), then publishes.
"""
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitor.newsletter.assembly import (
    REGION_ORDER, REGION_SLUGS, assemble_newsletter_pages,
)
from src.monitor.newsletter.publish import publish_brief
from src.monitor.agents.regional import REGION_COUNTRIES
from src.monitor.agents.editor import style_edit_page


TRACES_DIR = PROJECT_ROOT / "briefs" / "20260215" / "traces"
END_DATE = date(2026, 2, 15)


def load_trace_output(filename: str) -> str:
    path = TRACES_DIR / filename
    with open(path) as f:
        return json.load(f)["output"]["response_text"]


async def main():
    # 1. Load pipeline state and re-assemble pages (deterministic, no API)
    from src.monitor.cli import _load_pipeline_state
    from src.monitor.ledger.storage import load_story_map

    country_ledgers, country_entries, regional_reports, global_ledger = \
        _load_pipeline_state(END_DATE)

    story_maps_data = {}
    for code in country_ledgers:
        try:
            story_maps_data[code] = load_story_map(code, END_DATE)
        except FileNotFoundError:
            pass

    pages = assemble_newsletter_pages(
        global_ledger, regional_reports, country_ledgers, country_entries, END_DATE,
        story_maps=story_maps_data or None,
    )
    print(f"Assembled {len(pages)} pages")

    # 2. Splice editor output into region pages (regional leads + country sections)
    for region in REGION_ORDER:
        slug = REGION_SLUGS[region]
        page = pages[slug]
        codes = REGION_COUNTRIES.get(region, [])

        first_country = re.search(r'\n\n### ', page)
        if not first_country:
            continue

        lead_part = page[:first_country.start()]

        # Replace regional lead prose with editor output
        editor_trace = f"editor_regional_{region.value}.json"
        if (TRACES_DIR / editor_trace).exists():
            edited_lead = load_trace_output(editor_trace)

            # Preserve frontmatter
            lead_lines = lead_part.split("\n")
            fm_end = 0
            in_fm = False
            for i, line in enumerate(lead_lines):
                if line.strip() == "---":
                    in_fm = not in_fm
                    if not in_fm:
                        fm_end = i + 1
            frontmatter = "\n".join(lead_lines[:fm_end]) if fm_end > 0 else ""

            # Preserve ## Regional Summary heading
            heading_match = re.search(r'## Regional Summary\b.*', lead_part)
            heading = heading_match.group(0) if heading_match else "## Regional Summary"

            lead_part = frontmatter + "\n\n" + heading + "\n\n" + edited_lead

        # Splice in copyeditor country sections from traces
        country_sections = []
        for code in codes:
            trace = f"copyeditor_{code}.json"
            if (TRACES_DIR / trace).exists():
                country_sections.append(load_trace_output(trace))
            else:
                print(f"  WARNING: No copyeditor trace for {code}")

        pages[slug] = lead_part + "\n\n" + "\n\n".join(country_sections)
        print(f"  Reconstructed {slug}: {len(codes)} countries")

    # 3. Splice style-edited executive into overview (already done in prior run)
    if "overview" in pages:
        overview = pages["overview"]
        style_exec = load_trace_output("style_editor_executive.json")

        week_match = re.search(r'\n## Week of .+\n', overview)
        regions_match = re.search(r'\n---\n\n## Regions', overview)
        if week_match and regions_match:
            pages["overview"] = (
                overview[:week_match.end()]
                + "\n\n" + style_exec + "\n\n"
                + overview[regions_match.start():]
            )
        print("  Spliced style-edited executive into overview")

    # 4. Load watchlist from editor trace
    if (TRACES_DIR / "editor_watchlist.json").exists():
        pages["watchlist"] = load_trace_output("editor_watchlist.json")
        print("  Loaded watchlist from editor trace")

    # 5. Style edit all region pages (overview/watchlist skip)
    print("\nStyle editing region pages...")
    for slug in list(pages.keys()):
        if slug in ("overview", "watchlist"):
            continue
        print(f"  {slug}...")
        pages[slug] = await style_edit_page(pages[slug], analysis_date=END_DATE, max_concurrent=5)

    # 6. Publish
    print("\nPublishing...")
    brief_dir = publish_brief(pages, END_DATE)
    print(f"Published to {brief_dir}")


if __name__ == "__main__":
    asyncio.run(main())
