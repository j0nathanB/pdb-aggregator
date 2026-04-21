"""
Resume Step 3 (copyedit) + Step 4 (inject) from dev/restore_other_stories.py.

The prior run (2026-04-21 morning) completed story_map for all 4 and copyedit
for PL, RO, NO before DE's streaming call stalled during a 5-hour laptop
sleep and died with Connection errors on retry. Re-running the whole
script would redo the expensive story_map stage. This resume script:

  1. Reads polished other_stories for PL/RO/NO from
     briefs/20260419/traces/copyeditor_{code}.json (the trace's
     response_text holds the full copyeditor JSON output).
  2. Runs copyedit for DE only (~1 LLM call).
  3. Renders <Accordion title="Other Stories"> blocks for all 4 and
     injects them into the region MDXs.

Idempotent on re-run.
"""

import asyncio
import json
import logging
import os
import re
from datetime import date
from pathlib import Path

from src.monitor.ledger.storage import load_country_ledger
from src.monitor.newsletter.content_builder import _collect_other_stories
from src.monitor.newsletter.content_models import CountryContent, StoryClusterContent
from src.monitor.newsletter.structured_copyeditor import copyedit_country
from src.monitor.cli import _extract_country_narratives_from_mdx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("restore_resume")

END_DATE = date(2026, 4, 19)
REGION_SLUG_BY_CODE = {
    "pl": "central-eastern-europe",
    "ro": "central-eastern-europe",
    "no": "nordic-baltic",
    "de": "western-europe",
}


def _load_polished_from_trace(code: str) -> list[StoryClusterContent] | None:
    """Read polished other_stories from a copyeditor trace response_text.

    Returns None if the trace doesn't contain an `other_stories` array
    (e.g., hasn't been run yet, or the run produced narrative_body only).
    """
    trace_path = Path(f"briefs/20260419/traces/copyeditor_{code}.json")
    if not trace_path.exists():
        return None
    trace = json.loads(trace_path.read_text())
    rt = trace.get("output", {}).get("response_text", "")
    if not rt:
        return None
    try:
        data = json.loads(rt)
    except json.JSONDecodeError:
        return None
    items = data.get("other_stories")
    if not items:
        return None
    # Map polished headline/summary back onto the ORIGINAL source_url/source_name
    # from the ledger's story_clusters (copyeditor tool doesn't round-trip those).
    ledger = load_country_ledger(code)
    entry = next(e for e in ledger.weekly_entries if e.week == END_DATE)
    src_by_headline = {
        sc.headline: (sc.source_url, sc.source_name)
        for sc in entry.story_clusters
    }
    result = []
    for it in items:
        headline = it.get("headline", "")
        summary = it.get("summary", "")
        # The copyeditor rewrites the headline, so direct match won't work.
        # Fall back to index-order alignment against _collect_other_stories.
        result.append(StoryClusterContent(
            headline=headline,
            summary=summary,
            source_name="",
            source_url="",
        ))
    # Align by index with the ledger's collected other_stories (which
    # preserves source fields). The copyeditor keeps list order stable.
    originals = _collect_other_stories(entry)
    for i, orig in enumerate(originals):
        if i < len(result):
            result[i].source_url = orig.source_url
            result[i].source_name = orig.source_name
    return result


async def _copyedit_de() -> list[StoryClusterContent]:
    """Run copyedit for DE with narrative_body from MDX + fresh ledger clusters."""
    ledger = load_country_ledger("de")
    entry = next(e for e in ledger.weekly_entries if e.week == END_DATE)
    other = _collect_other_stories(entry)
    if not other:
        logger.warning("de: no other_stories to copyedit")
        return []
    mdx_path = Path(f"site/briefs/{END_DATE.isoformat()}/western-europe.mdx")
    narratives = _extract_country_narratives_from_mdx(mdx_path)
    content = CountryContent(
        code="de",
        country=ledger.country,
        posture_summary=ledger.posture_summary.text,
        narrative_body=narratives.get("de", "(narrative unchanged)"),
        other_stories=other,
    )
    logger.info("de: copyediting %d other_stories", len(other))
    await copyedit_country(content, analysis_date=END_DATE)
    return content.other_stories


def _render_accordion(stories: list[StoryClusterContent]) -> str:
    lines = ["", '<Accordion title="Other Stories">']
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
            # Strip existing Accordion if present (makes this step idempotent)
            body = re.sub(
                r'\n*<Accordion title="Other Stories">.*?</Accordion>\n*',
                "\n",
                block,
                count=1,
                flags=re.DOTALL,
            )
            body = body.rstrip() + "\n"
            new_blocks.append(body + accordion_by_code[code] + "\n")
        else:
            new_blocks.append(block)
    new_text = head + "\n---\n\n" + "\n---\n\n".join(new_blocks)
    mdx_path.write_text(new_text)


async def main():
    os.environ.setdefault("MPM_USE_TOOL_SCHEMA", "1")

    stories_by_code: dict[str, list[StoryClusterContent]] = {}
    for code in ("pl", "ro", "no"):
        polished = _load_polished_from_trace(code)
        if polished:
            stories_by_code[code] = polished
            logger.info("%s: loaded %d polished stories from trace", code, len(polished))
        else:
            logger.warning("%s: no polished trace found; skipping", code)

    de_polished = await _copyedit_de()
    if de_polished:
        stories_by_code["de"] = de_polished
        logger.info("de: polished %d stories live", len(de_polished))

    accordions = {code: _render_accordion(s) for code, s in stories_by_code.items()}

    # Group by region slug and inject
    grouped: dict[str, dict[str, str]] = {}
    for code, acc in accordions.items():
        grouped.setdefault(REGION_SLUG_BY_CODE[code], {})[code] = acc

    for slug, by_code in grouped.items():
        path = Path(f"site/briefs/{END_DATE.isoformat()}/{slug}.mdx")
        _inject_accordions(path, by_code)
        logger.info("%s: injected %d accordion(s): %s",
                    slug, len(by_code), sorted(by_code))


if __name__ == "__main__":
    asyncio.run(main())
