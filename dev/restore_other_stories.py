"""
One-off: restore Other Stories accordions for PL, RO, NO, DE on the
2026-04-19 brief without re-running the country/editor stages.

What it does:
  1. Re-runs triage scan + expansion + story_map for the four countries
     in parallel. The story_map tool_use completeness gate from 82d2afd
     now triggers the text fallback if streaming truncates mid-arrays.
  2. Persists the story_map sidecars (ledgers/story_maps/{code}_{date}.json)
     and updates each country's weekly entry with populated story_clusters
     (persisted to ledgers/countries/{code}.json).
  3. For each country, builds the Other Stories list via
     _collect_other_stories, pipes it through copyedit_country to polish
     the headline/summary text.
  4. Renders an <Accordion title="Other Stories"> block per country and
     injects it into the corresponding region MDX at the end of that
     country's section.

Does NOT touch narrative_body (the polished prose from commit 90986cf
stays verbatim). Does NOT republish at-a-glance or overview.

Run with:
  MPM_USE_TOOL_SCHEMA=1 .venv/bin/python dev/restore_other_stories.py
"""

import asyncio
import logging
import os
import re
from datetime import date
from pathlib import Path

from src.monitor.agents.expansion import expand_country
from src.monitor.agents.story_map import run_story_map_agent
from src.monitor.agents.triage import scan_country
from src.monitor.collection.brave import BraveNewsClient
from src.monitor.config import load_all_country_configs
from src.monitor.ledger.storage import (
    load_country_ledger,
    save_country_ledger,
    save_story_map,
)
from src.monitor.models import StoryClusterSummary
from src.monitor.newsletter.content_builder import _collect_other_stories
from src.monitor.newsletter.content_models import CountryContent
from src.monitor.newsletter.structured_copyeditor import copyedit_country
from src.monitor.cli import _extract_country_narratives_from_mdx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("restore_other_stories")

END_DATE = date(2026, 4, 19)
CODES = ["pl", "ro", "no", "de"]
REGION_SLUG_BY_CODE = {
    "pl": "central-eastern-europe",
    "ro": "central-eastern-europe",
    "no": "nordic-baltic",
    "de": "western-europe",
}
COUNTRY_NAME_BY_CODE = {
    "pl": "Poland",
    "ro": "Romania",
    "no": "Norway",
    "de": "Germany",
}


async def _run_story_map_for(code: str, configs: dict, brave: BraveNewsClient):
    config = configs[code]
    logger.info("[%s] triage scan", code)
    scan = await scan_country(config, brave, END_DATE)
    logger.info("[%s] expansion", code)
    expansion = await expand_country(
        config, brave, triage_scan=scan, end_date=END_DATE
    )
    logger.info("[%s] story_map", code)
    story_map = await run_story_map_agent(config, expansion, END_DATE)
    return code, story_map


def _render_accordion(stories) -> str:
    lines = ["", "<Accordion title=\"Other Stories\">"]
    for s in stories:
        source_suffix = ""
        if s.source_url and s.source_name:
            source_suffix = f" *([{s.source_name}]({s.source_url}))*"
        lines.append(f"- **{s.headline}** — {s.summary}{source_suffix}")
        lines.append("")
    lines.append("</Accordion>")
    return "\n".join(lines)


BLOCK_SPLIT = re.compile(r"\n---\n\n(?=### )", re.MULTILINE)
FLAG_CODE = re.compile(r"flagcdn\.com/([a-z]{2})\.svg")


def _inject_accordions(mdx_path: Path, accordion_by_code: dict[str, str]) -> None:
    text = mdx_path.read_text()
    parts = BLOCK_SPLIT.split(text)
    head = parts[0]
    new_blocks = []
    for block in parts[1:]:
        m = FLAG_CODE.search(block)
        code = m.group(1) if m else None
        if code in accordion_by_code:
            # Target country: strip any existing trailing whitespace, then
            # append Accordion. Keep a trailing newline so the reassembled
            # file stays well-formed.
            block_stripped = block.rstrip() + "\n"
            block_with_accordion = block_stripped + accordion_by_code[code] + "\n"
            new_blocks.append(block_with_accordion)
        else:
            new_blocks.append(block)
    new_text = head + "\n---\n\n" + "\n---\n\n".join(new_blocks)
    mdx_path.write_text(new_text)


async def main():
    os.environ.setdefault("MPM_USE_TOOL_SCHEMA", "1")

    configs = load_all_country_configs()
    brave = BraveNewsClient()

    # Step 1: parallel story_map re-runs
    logger.info("Re-running story_map for %s", CODES)
    results = await asyncio.gather(
        *[_run_story_map_for(c, configs, brave) for c in CODES]
    )

    # Step 2: persist sidecars, update ledger story_clusters
    fresh_entries: dict[str, object] = {}
    for code, sm in results:
        if not sm or not sm.stories:
            logger.warning("%s: story_map empty — skipping", code)
            continue
        save_story_map(code, END_DATE, sm)
        ledger = load_country_ledger(code)
        for entry in ledger.weekly_entries:
            if entry.week == END_DATE:
                entry.story_clusters = [
                    StoryClusterSummary(
                        headline=sc.headline,
                        summary=sc.summary,
                        source_url=(
                            sc.representative_urls[0]
                            if sc.representative_urls
                            else ""
                        ),
                        source_name=sc.sources[0] if sc.sources else "",
                    )
                    for sc in sm.stories
                ]
                fresh_entries[code] = entry
                break
        save_country_ledger(ledger)
        logger.info(
            "%s: persisted %d clusters to sidecar + ledger",
            code, len(sm.stories),
        )

    # Step 3: build CountryContent + copyedit Other Stories
    # copyedit_country's tool requires narrative_body; we feed the existing
    # prose in and discard the copyeditor's narrative output, keeping only
    # the polished other_stories list.
    accordion_by_code: dict[str, str] = {}
    for code, entry in fresh_entries.items():
        other = _collect_other_stories(entry)
        if not other:
            logger.info("%s: no other_stories after dedupe — skipping", code)
            continue
        mdx_path = Path(
            f"site/briefs/{END_DATE.isoformat()}/"
            f"{REGION_SLUG_BY_CODE[code]}.mdx"
        )
        narratives = _extract_country_narratives_from_mdx(mdx_path)
        existing_narrative = narratives.get(code, "")
        if not existing_narrative:
            logger.warning(
                "%s: no existing narrative in MDX; using placeholder",
                code,
            )
            existing_narrative = "(narrative unchanged)"
        ledger = load_country_ledger(code)
        content = CountryContent(
            code=code,
            country=ledger.country,
            posture_summary=ledger.posture_summary.text,
            narrative_body=existing_narrative,
            other_stories=other,
        )
        logger.info("%s: copyediting %d other_stories", code, len(other))
        await copyedit_country(content, analysis_date=END_DATE)
        accordion_by_code[code] = _render_accordion(content.other_stories)
        logger.info(
            "%s: polished accordion built (%d chars)",
            code, len(accordion_by_code[code]),
        )

    # Step 4: inject into region MDXs
    grouped: dict[str, dict[str, str]] = {}
    for code, accordion in accordion_by_code.items():
        grouped.setdefault(REGION_SLUG_BY_CODE[code], {})[code] = accordion
    for slug, by_code in grouped.items():
        mdx_path = Path(f"site/briefs/{END_DATE.isoformat()}/{slug}.mdx")
        _inject_accordions(mdx_path, by_code)
        logger.info(
            "%s: injected accordions for %s", slug, sorted(by_code),
        )


if __name__ == "__main__":
    asyncio.run(main())
