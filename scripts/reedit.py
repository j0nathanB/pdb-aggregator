"""
Targeted re-edit pipeline: re-run editorial passes on specific countries/regions.

Usage:
    # Re-edit three countries from the editor stage
    python scripts/reedit.py --date 2026-02-22 --country pl cz no --from editor

    # Re-edit two regions from the copyeditor stage
    python scripts/reedit.py --date 2026-02-22 --region central_eastern_europe western_europe --from copyeditor

    # Re-edit the executive brief from the editor stage
    python scripts/reedit.py --date 2026-02-22 --executive --from editor

    # Recover a country whose agent failed: parse the trace, rebuild the
    # ledger entry + story map, then run editor → copyeditor → style → patch.
    # Use this when the country agent's JSON was malformed; manually patch the
    # response_text in briefs/{date}/traces/country_{code}.json first if needed.
    python scripts/reedit.py --date 2026-03-15 --country ae --from country

Stages: country, editor, copyeditor, style_editor

The 'country' stage is special — it runs before the editorial passes and
recovers a failed country from its trace files. It will:
  1. Parse the (manually-patched) response_text from country_{code}.json
  2. Build a WeeklyEntry and append/replace it in the country ledger
  3. Save the story_map_{code}.json sidecar from the trace if it exists
  4. Attach story_clusters from the story map to the new weekly entry
After recovery, the standard editor → copyeditor → style → patch flow runs.

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

STAGES = ["country", "writer", "editor", "copyeditor", "style_editor"]
EDITORIAL_STAGES = ["writer", "editor", "copyeditor", "style_editor"]


# =============================================================================
# Country recovery from trace
# =============================================================================

def recover_country_from_trace(code: str, end_date: date) -> bool:
    """Recover a failed country from its trace files.

    When a country agent's JSON parse fails, the orchestrator marks the country
    as failed and skips ledger update. This recovery:
      1. Reads briefs/{date}/traces/country_{code}.json
      2. Parses the response_text (assumes manually patched if originally broken)
      3. Builds a WeeklyEntry and appends/replaces it in the country ledger
      4. Reads briefs/{date}/traces/story_map_{code}.json if present
      5. Saves the story map sidecar to ledgers/story_maps/{code}_{date}.json
      6. Attaches story_clusters to the weekly entry from the story map

    Returns True on success.
    """
    from src.monitor.agents.country import parse_country_response
    from src.monitor.ledger.storage import (
        load_country_ledger,
        save_country_ledger,
    )
    from src.monitor.models import StoryClusterSummary
    from datetime import timedelta

    date_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "traces"
    country_trace_path = date_dir / f"country_{code}.json"
    story_map_trace_path = date_dir / f"story_map_{code}.json"

    if not country_trace_path.exists():
        logger.error("Country trace not found: %s", country_trace_path)
        return False

    # 1. Parse country trace
    trace = json.loads(country_trace_path.read_text())
    response_text = trace["output"]["response_text"]
    if not response_text:
        logger.error("Country trace has empty response_text: %s", country_trace_path)
        return False

    # 2. Load ledger and parse country output
    ledger = load_country_ledger(code)
    date_range = f"{(end_date - timedelta(days=6)).isoformat()} to {end_date.isoformat()}"
    try:
        result = parse_country_response(response_text, end_date, date_range, ledger)
    except Exception as e:
        logger.error(
            "Failed to parse country trace for %s: %s. "
            "If JSON was malformed, manually patch the response_text in %s and retry.",
            code, e, country_trace_path,
        )
        return False

    n_devs = sum(len(m.developments) for m in result.weekly_entry.category_movements.values())
    logger.info("Recovered %s: %d categories, %d developments", code, len(result.weekly_entry.category_movements), n_devs)

    # 3. Save story map sidecar from trace if available, then attach clusters
    if story_map_trace_path.exists():
        sm_trace = json.loads(story_map_trace_path.read_text())
        sm_parsed = sm_trace.get("output", {}).get("parsed")
        if sm_parsed and isinstance(sm_parsed, dict):
            sm_ledger_path = PROJECT_ROOT / "ledgers" / "story_maps" / f"{code}_{end_date.isoformat()}.json"
            sm_ledger_path.parent.mkdir(parents=True, exist_ok=True)
            sm_ledger_entry = {
                "country": ledger.country,
                "code": code,
                "week": end_date.isoformat(),
                "analysis_date": sm_parsed.get("analysis_date", end_date.isoformat()),
                "search_results_total": sm_parsed.get("search_results_total", 0),
                "stories_identified": sm_parsed.get("stories_identified", 0),
                "off_topic_filtered": sm_parsed.get("off_topic_filtered", 0),
                "noise_summary": sm_parsed.get("noise_summary", ""),
                "stories": sm_parsed.get("stories", []),
                "single_source_items": sm_parsed.get("single_source_items", []),
            }
            sm_ledger_path.write_text(json.dumps(sm_ledger_entry, indent=2))
            logger.info("  Story map sidecar saved: %s (%d stories, %d singles)",
                        sm_ledger_path, len(sm_ledger_entry["stories"]), len(sm_ledger_entry["single_source_items"]))

            # Attach story clusters to the weekly entry
            clusters = []
            for sc in sm_parsed.get("stories", []):
                rep_urls = sc.get("representative_urls") or []
                sources = sc.get("sources") or []
                clusters.append(StoryClusterSummary(
                    headline=sc.get("headline", "Untitled"),
                    summary=sc.get("summary", ""),
                    source_url=rep_urls[0] if rep_urls else "",
                    source_name=sources[0] if sources else "",
                ))
            result.weekly_entry.story_clusters = clusters
            logger.info("  Attached %d story clusters to weekly entry", len(clusters))
    else:
        logger.warning("  No story map trace at %s — Other Stories/Notes will be empty", story_map_trace_path)

    # 4. Append or replace the weekly entry in the ledger
    existing_idx = next(
        (i for i, e in enumerate(ledger.weekly_entries) if e.week == end_date),
        None,
    )
    if existing_idx is not None:
        ledger.weekly_entries[existing_idx] = result.weekly_entry
        logger.info("  Replaced existing entry at index %d", existing_idx)
    else:
        ledger.weekly_entries.append(result.weekly_entry)
        logger.info("  Appended new weekly entry")

    ledger.posture_summary = result.posture_summary
    ledger.signal_categories = result.signal_categories
    ledger.last_updated = end_date

    save_country_ledger(ledger)
    logger.info("  Saved ledger: %s now has %d weekly entries", code, len(ledger.weekly_entries))
    return True


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
    from src.monitor.newsletter.structured_editor import sanitize_narrative_body, style_edit_prose
    if not country.narrative_body:
        return country
    result = await style_edit_prose(
        {"narrative_body": country.narrative_body},
        country.code, analysis_date=end_date,
    )
    country.narrative_body = sanitize_narrative_body(
        result.get("narrative_body", country.narrative_body),
        label=f"reedit_style_{country.code}",
    )
    return country


async def run_regional_writer(page: RegionPageContent, end_date: date) -> RegionPageContent:
    from src.monitor.newsletter.regional_writer import write_regional_essay
    return await write_regional_essay(page)


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


async def run_global_writer(overview, region_pages, end_date: date):
    from src.monitor.newsletter.global_writer import write_global_essay
    return await write_global_essay(overview, region_pages)


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


def patch_mdx_regional(mdx_path: Path, new_lead: str, new_gaps: list[str],
                       headline: str = "") -> bool:
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
    parts = []
    if headline:
        parts.append(f"\n**{headline}**")
    parts.append(new_lead if headline else "\n" + new_lead)
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
    """Re-edit specific countries through the editorial chain.

    If from_stage is "country", country recovery already ran in main();
    here we just normalize to "editor" so all editorial passes execute.
    """
    output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "reedits"
    output_dir.mkdir(parents=True, exist_ok=True)

    # "country" stage normalizes to running all editorial passes
    effective_stage = "editor" if from_stage == "country" else from_stage
    stage_idx = EDITORIAL_STAGES.index(effective_stage)

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

    # "country" stage doesn't apply to regional reedits — normalize to "writer"
    effective_stage = "writer" if from_stage == "country" else from_stage
    stage_idx = EDITORIAL_STAGES.index(effective_stage)

    # Load existing country narratives from traces so the regional editor
    # has country_summaries to draw from.
    traces_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "traces"
    for _region, page in region_pages.items():
        for country in page.countries:
            if country.narrative_body:
                continue
            # Try style_editor trace first, then editor, then copyeditor
            for prefix in ("style_editor_", "copyeditor_", "editor_"):
                trace_path = traces_dir / f"{prefix}{country.code}.json"
                if trace_path.exists():
                    try:
                        with open(trace_path) as f:
                            trace = json.load(f)
                        parsed = trace.get("output", {}).get("parsed", {})
                        body = parsed.get("narrative_body", "")
                        if body:
                            country.narrative_body = body
                            break
                    except (json.JSONDecodeError, KeyError):
                        continue

    # Load regional writer output from traces so the editor gets the
    # writer's draft as regional_lead (matching production pipeline).
    for _region, page in region_pages.items():
        writer_trace = traces_dir / f"regional_writer_{_region.value}.json"
        if writer_trace.exists() and not page.regional_lead:
            try:
                with open(writer_trace) as f:
                    trace = json.load(f)
                parsed = trace.get("output", {}).get("parsed", {})
                lead = parsed.get("regional_lead", "")
                if lead:
                    page.regional_lead = lead
                    logger.info("Loaded writer draft for %s (%d chars)", page.display_name, len(lead))
            except (json.JSONDecodeError, KeyError):
                pass

    for region, page in region_pages.items():
        if region.value not in region_values:
            continue

        logger.info("Re-editing regional lead: %s from %s", page.display_name, from_stage)

        if stage_idx <= 0:  # writer
            page = await run_regional_writer(page, end_date)
        if stage_idx <= 1:  # editor
            page = await run_regional_editor(page, end_date)
        if stage_idx <= 2:  # copyeditor
            page = await run_regional_copyeditor(page, end_date)
        if stage_idx <= 3:  # style_editor
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
                if patch_mdx_regional(mdx_path, page.regional_lead, page.gap_paragraphs, page.headline):
                    logger.info("  Patched: %s", mdx_path)


async def reedit_executive(
    end_date: date,
    from_stage: str,
    overview, region_pages, watchlist,
):
    """Re-edit the executive brief through the editorial chain."""
    output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "reedits"
    output_dir.mkdir(parents=True, exist_ok=True)

    # "country" stage doesn't apply to executive reedits — normalize to "writer"
    effective_stage = "writer" if from_stage == "country" else from_stage
    stage_idx = EDITORIAL_STAGES.index(effective_stage)

    # Load global writer output from trace so the editor gets the
    # writer's draft (matching production pipeline).
    if stage_idx > 0 and not overview.executive_brief.edited_essay:
        traces_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "traces"
        writer_trace = traces_dir / "global_writer_executive.json"
        if writer_trace.exists():
            try:
                with open(writer_trace) as f:
                    trace = json.load(f)
                parsed = trace.get("output", {}).get("parsed", {})
                essay = parsed.get("edited_essay", "")
                if essay:
                    overview.executive_brief.edited_essay = essay
                    logger.info("Loaded global writer draft (%d chars)", len(essay))
            except (json.JSONDecodeError, KeyError):
                pass

    logger.info("Re-editing executive brief from %s", from_stage)

    if stage_idx <= 0:  # writer
        overview = await run_global_writer(overview, region_pages, end_date)
    if stage_idx <= 1:  # editor
        overview = await run_executive_editor(overview, end_date)
    if stage_idx <= 2:  # copyeditor
        overview = await run_executive_copyeditor(overview, end_date)
    if stage_idx <= 3:  # style_editor
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
            headline = overview.executive_brief.headline or ""
            headline_block = f"**{headline}**\n\n" if headline else ""
            new_content = (
                content[:week_match.end()] + "\n\n" + headline_block + essay + "\n\n"
                + content[regions_match.start():]
            )
            mdx_path.write_text(new_content)
            logger.info("  Patched: %s", mdx_path)


async def main():
    parser = argparse.ArgumentParser(description="Targeted re-edit pipeline")
    parser.add_argument("--date", required=True, help="Brief date (YYYY-MM-DD)")
    parser.add_argument("--country", nargs="+", help="Country codes to re-edit (e.g. pl cz no)")
    parser.add_argument("--region", nargs="+", help="Region values to re-edit (e.g. central_eastern_europe)")
    parser.add_argument("--executive", action="store_true", help="Re-edit executive brief")
    parser.add_argument("--from", dest="from_stage", default="editor",
                        choices=STAGES, help="Start from this stage (default: editor)")
    args = parser.parse_args()

    end_date = date.fromisoformat(args.date)

    if not args.country and not args.region and not args.executive:
        parser.error("Specify --country, --region, or --executive")

    # Country recovery from trace (must happen before building content)
    if args.from_stage == "country":
        if not args.country:
            parser.error("--from country requires --country to specify which country to recover")
        logger.info("Recovering %d country(ies) from trace files...", len(args.country))
        for code in args.country:
            ok = recover_country_from_trace(code, end_date)
            if not ok:
                logger.error("Recovery failed for %s — aborting", code)
                sys.exit(1)

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

    overview, region_pages, watchlist, at_a_glance = build_all_pages(
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
