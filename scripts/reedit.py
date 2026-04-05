"""
Targeted re-edit pipeline: re-run editorial passes on specific countries/regions.

Usage:
    # Re-edit three countries from the editor stage
    python scripts/reedit.py --date 2026-02-22 --country pl cz no --from editor

    # Re-edit two regions from the copyeditor stage
    python scripts/reedit.py --date 2026-02-22 --region frontline_eastern_europe western_europe --from copyeditor

    # Re-edit the executive brief from the editor stage
    python scripts/reedit.py --date 2026-02-22 --executive --from editor

Stages: editor, copyeditor, style_editor

Outputs markdown files to briefs/{date}/reedits/ and patches the corresponding
MDX pages in site/briefs/{date}/.
"""

import argparse
import asyncio
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitor.config import Region, load_all_country_configs
from src.monitor.ledger.storage import (
    load_country_ledger,
    load_global_ledger,
    load_story_map,
    list_country_ledgers,
    load_all_regional_reports,
)
from src.monitor.newsletter.content_builder import build_all_pages
from src.monitor.newsletter.content_models import CountryContent, RegionPageContent
from src.monitor.newsletter.renderer import render_pages, _render_notes_section, _format_date_range
from src.monitor.newsletter.assembly import REGION_SLUGS, REGION_DISPLAY_NAMES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("reedit")

STAGES = ["editor", "copyeditor", "style_editor"]


# =============================================================================
# Editorial passes
# =============================================================================

async def run_editor(country: CountryContent, end_date: date) -> CountryContent:
    from src.monitor.newsletter.structured_editor import edit_country
    return await edit_country(country, analysis_date=end_date)


async def run_copyeditor(country: CountryContent, end_date: date) -> CountryContent:
    from src.monitor.newsletter.structured_copyeditor import copyedit_country
    return await copyedit_country(country, analysis_date=end_date)


async def run_style_editor_country(country: CountryContent, end_date: date) -> CountryContent:
    from src.monitor.newsletter.structured_editor import style_edit_prose
    if not country.narrative_body:
        return country
    result = await style_edit_prose(
        {"narrative_body": country.narrative_body},
        country.code, analysis_date=end_date,
    )
    country.narrative_body = result.get("narrative_body", country.narrative_body)
    return country


async def run_regional_editor(page: RegionPageContent, end_date: date) -> RegionPageContent:
    from src.monitor.newsletter.structured_editor import edit_regional
    return await edit_regional(page, analysis_date=end_date)


async def run_regional_copyeditor(page: RegionPageContent, end_date: date) -> RegionPageContent:
    from src.monitor.newsletter.structured_copyeditor import copyedit_regional
    return await copyedit_regional(page, analysis_date=end_date)


async def run_regional_style_editor(page: RegionPageContent, end_date: date) -> RegionPageContent:
    from src.monitor.newsletter.structured_editor import style_edit_prose
    if not page.regional_lead:
        return page
    result = await style_edit_prose(
        {"regional_lead": page.regional_lead, "card_summary": page.card_summary},
        f"regional_{page.region.value}", analysis_date=end_date,
    )
    page.regional_lead = result.get("regional_lead", page.regional_lead)
    if "card_summary" in result:
        page.card_summary = result["card_summary"]
    return page


async def run_executive_editor(overview, end_date: date):
    from src.monitor.newsletter.structured_editor import edit_executive
    overview.executive_brief = await edit_executive(
        overview.executive_brief, analysis_date=end_date,
    )
    return overview


async def run_executive_copyeditor(overview, end_date: date):
    from src.monitor.newsletter.structured_copyeditor import copyedit_executive
    overview.executive_brief = await copyedit_executive(
        overview.executive_brief, analysis_date=end_date,
    )
    return overview


async def run_executive_style_editor(overview, end_date: date):
    from src.monitor.newsletter.structured_editor import style_edit_prose
    if not overview.executive_brief.edited_essay:
        return overview
    result = await style_edit_prose(
        {"edited_essay": overview.executive_brief.edited_essay},
        "executive", analysis_date=end_date,
    )
    overview.executive_brief.edited_essay = result.get(
        "edited_essay", overview.executive_brief.edited_essay,
    )
    return overview


# =============================================================================
# Country rendering + MDX patching
# =============================================================================

def render_country_markdown(country: CountryContent) -> str:
    """Render a single country's content to markdown (no MDX components)."""
    parts = []
    if country.narrative_body:
        parts.append(country.narrative_body)
    else:
        parts.append(country.posture_summary)
    return "\n\n".join(parts)


def render_country_mdx_section(country: CountryContent) -> str:
    """Render a country's full MDX section (narrative + Other Stories + Notes)."""
    parts = []

    # Narrative
    if country.narrative_body:
        parts.append(country.narrative_body)
    else:
        parts.append(country.posture_summary)

    # Other Stories accordion
    if country.other_stories:
        lines = ['', '<Accordion title="Other Stories">']
        for story in country.other_stories:
            source_link = ""
            if story.source_url and story.source_name:
                source_link = f" *([{story.source_name}]({story.source_url}))*"
            lines.append(f"- **{story.headline}** — {story.summary}{source_link}")
        lines.append("</Accordion>")
        parts.append("\n".join(lines))

    # Notes accordion
    if country.story_map_data and country.story_map_data.get("stories"):
        parts.append("")
        parts.append(_render_notes_section(country.story_map_data))

    return "\n\n".join(parts)


def patch_mdx_country(mdx_path: Path, code: str, country_name: str, new_section: str) -> bool:
    """Replace a country section in an MDX file."""
    content = mdx_path.read_text()

    # Find the country heading
    pattern = re.compile(
        rf'(### <img [^>]*/{code}\.svg[^>]*/>\s*{re.escape(country_name)})\n',
        re.IGNORECASE,
    )
    match = pattern.search(content)
    if not match:
        logger.error("Could not find heading for %s (%s) in %s", country_name, code, mdx_path)
        return False

    heading = match.group(1)
    section_start = match.end()

    # Find the next country heading or end-of-file marker
    next_heading = re.search(r'\n---\n\n### <img ', content[section_start:])
    if next_heading:
        section_end = section_start + next_heading.start()
    else:
        section_end = len(content)

    # Replace
    new_content = content[:section_start] + "\n" + new_section + "\n\n" + content[section_end:]
    mdx_path.write_text(new_content)
    return True


def patch_mdx_regional(mdx_path: Path, new_lead: str, new_gaps: list[str]) -> bool:
    """Replace the regional lead in an MDX file."""
    content = mdx_path.read_text()

    # Find between "## Regional Summary\n" and first "\n---\n"
    lead_start = content.find("## Regional Summary")
    if lead_start == -1:
        logger.error("Could not find '## Regional Summary' in %s", mdx_path)
        return False

    lead_start = content.index("\n", lead_start) + 1  # after the heading line

    first_separator = content.find("\n---\n", lead_start)
    if first_separator == -1:
        first_separator = len(content)

    # Build replacement
    parts = ["\n" + new_lead]
    for gap in new_gaps:
        parts.append(gap)
    replacement = "\n\n".join(parts) + "\n\n"

    new_content = content[:lead_start] + replacement + content[first_separator:]
    mdx_path.write_text(new_content)
    return True


# =============================================================================
# Main pipeline
# =============================================================================

async def reedit_countries(
    codes: list[str],
    end_date: date,
    from_stage: str,
    overview, region_pages, watchlist,
):
    """Re-edit specific countries through the editorial chain."""
    output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "reedits"
    output_dir.mkdir(parents=True, exist_ok=True)

    stage_idx = STAGES.index(from_stage)

    for region, page in region_pages.items():
        for country in page.countries:
            if country.code not in codes:
                continue

            logger.info("Re-editing %s (%s) from %s", country.country, country.code, from_stage)

            # Run editorial stages
            if stage_idx <= 0:
                country = await run_editor(country, end_date)
            if stage_idx <= 1:
                country = await run_copyeditor(country, end_date)
            if stage_idx <= 2:
                country = await run_style_editor_country(country, end_date)

            # Write markdown output
            md_path = output_dir / f"{country.code}.md"
            md_path.write_text(render_country_markdown(country))
            logger.info("  Markdown: %s (%d chars)", md_path, len(country.narrative_body or ""))

            # Patch MDX
            slug = REGION_SLUGS.get(region)
            if slug:
                mdx_path = PROJECT_ROOT / "site" / "briefs" / end_date.isoformat() / f"{slug}.mdx"
                if mdx_path.exists():
                    section = render_country_mdx_section(country)
                    if patch_mdx_country(mdx_path, country.code, country.country, section):
                        logger.info("  Patched: %s", mdx_path)
                    else:
                        logger.error("  Failed to patch: %s", mdx_path)


async def reedit_regions(
    region_values: list[str],
    end_date: date,
    from_stage: str,
    overview, region_pages, watchlist,
):
    """Re-edit specific regional leads through the editorial chain."""
    output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "reedits"
    output_dir.mkdir(parents=True, exist_ok=True)

    stage_idx = STAGES.index(from_stage)

    for region, page in region_pages.items():
        if region.value not in region_values:
            continue

        logger.info("Re-editing regional lead: %s from %s", page.display_name, from_stage)

        if stage_idx <= 0:
            page = await run_regional_editor(page, end_date)
        if stage_idx <= 1:
            page = await run_regional_copyeditor(page, end_date)
        if stage_idx <= 2:
            page = await run_regional_style_editor(page, end_date)

        # Write markdown
        md_path = output_dir / f"regional_{region.value}.md"
        md_path.write_text(page.regional_lead + "\n\n" + "\n\n".join(page.gap_paragraphs))
        logger.info("  Markdown: %s (%d chars)", md_path, len(page.regional_lead))

        # Patch MDX
        slug = REGION_SLUGS.get(region)
        if slug:
            mdx_path = PROJECT_ROOT / "site" / "briefs" / end_date.isoformat() / f"{slug}.mdx"
            if mdx_path.exists():
                if patch_mdx_regional(mdx_path, page.regional_lead, page.gap_paragraphs):
                    logger.info("  Patched: %s", mdx_path)


async def reedit_executive(
    end_date: date,
    from_stage: str,
    overview, region_pages, watchlist,
):
    """Re-edit the executive brief through the editorial chain."""
    output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "reedits"
    output_dir.mkdir(parents=True, exist_ok=True)

    stage_idx = STAGES.index(from_stage)

    logger.info("Re-editing executive brief from %s", from_stage)

    if stage_idx <= 0:
        overview = await run_executive_editor(overview, end_date)
    if stage_idx <= 1:
        overview = await run_executive_copyeditor(overview, end_date)
    if stage_idx <= 2:
        overview = await run_executive_style_editor(overview, end_date)

    essay = overview.executive_brief.edited_essay or ""

    # Write markdown
    md_path = output_dir / "executive.md"
    md_path.write_text(essay)
    logger.info("  Markdown: %s (%d chars)", md_path, len(essay))

    # Patch overview MDX
    mdx_path = PROJECT_ROOT / "site" / "briefs" / end_date.isoformat() / "overview.mdx"
    if mdx_path.exists():
        content = mdx_path.read_text()
        # Find between "## Week of" heading and "---\n\n## Regions"
        week_match = re.search(r'(## Week of [^\n]+)\n', content)
        regions_match = re.search(r'\n---\n\n## Regions', content)
        if week_match and regions_match:
            new_content = (
                content[:week_match.end()] + "\n\n" + essay + "\n\n"
                + content[regions_match.start():]
            )
            mdx_path.write_text(new_content)
            logger.info("  Patched: %s", mdx_path)


async def main():
    parser = argparse.ArgumentParser(description="Targeted re-edit pipeline")
    parser.add_argument("--date", required=True, help="Brief date (YYYY-MM-DD)")
    parser.add_argument("--country", nargs="+", help="Country codes to re-edit (e.g. pl cz no)")
    parser.add_argument("--region", nargs="+", help="Region values to re-edit (e.g. frontline_eastern_europe)")
    parser.add_argument("--executive", action="store_true", help="Re-edit executive brief")
    parser.add_argument("--from", dest="from_stage", default="editor",
                        choices=STAGES, help="Start from this stage (default: editor)")
    args = parser.parse_args()

    end_date = date.fromisoformat(args.date)

    if not args.country and not args.region and not args.executive:
        parser.error("Specify --country, --region, or --executive")

    # Build structured content from disk
    logger.info("Building structured content for %s...", end_date)
    country_ledgers = {}
    country_entries = {}
    for code in list_country_ledgers():
        ledger = load_country_ledger(code)
        country_ledgers[code] = ledger
        entry = ledger.latest_entry()
        if entry:
            country_entries[code] = entry

    regional_reports = load_all_regional_reports()
    global_ledger = load_global_ledger()

    story_maps = {}
    for code in country_ledgers:
        try:
            story_maps[code] = load_story_map(code, end_date)
        except FileNotFoundError:
            pass

    overview, region_pages, watchlist = build_all_pages(
        global_ledger, regional_reports, country_ledgers, country_entries,
        end_date, story_maps=story_maps or None,
    )

    # Run re-edits
    if args.country:
        await reedit_countries(args.country, end_date, args.from_stage,
                               overview, region_pages, watchlist)

    if args.region:
        await reedit_regions(args.region, end_date, args.from_stage,
                              overview, region_pages, watchlist)

    if args.executive:
        await reedit_executive(end_date, args.from_stage,
                                overview, region_pages, watchlist)

    logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
