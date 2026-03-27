"""
Editor agent: rewrites assembled sections into style-guide prose.

Sits between assembly (deterministic rendering) and copyediting (mechanical
polish). Receives both the assembled Markdown and the raw analytical JSON
so it can make informed narrative choices. Handles country sections (one per
call, parallelisable) and regional leads.
"""

import asyncio
import json
import logging
import re
from datetime import date

import anthropic

from ..config import ANTHROPIC_API_KEY, MODEL, PROJECT_ROOT, THINKING_BUDGET_TOKENS, load_prompt
from ..models import CountryLedger, WeeklyEntry

# Editor uses the configured model (ideally Opus for narrative quality)
EDITOR_MODEL = MODEL

logger = logging.getLogger(__name__)


async def _stream_message(client: anthropic.AsyncAnthropic, **kwargs) -> anthropic.types.Message:
    """Send a message using streaming to avoid timeout on long requests."""
    async with client.messages.stream(**kwargs) as stream:
        response = await stream.get_final_message()
    return response


# Style guide loaded once per process
_style_guide: str | None = None


def _sanitize_mdx(text: str) -> str:
    """Fix common MDX-breaking patterns in editor output."""
    # Ensure </Accordion> is always followed by two newlines
    text = re.sub(r'</Accordion>\s*(?!\n\n)', '</Accordion>\n\n', text)
    # Ensure ### headings always have a blank line before them
    text = re.sub(r'(?<!\n\n)(### )', r'\n\n\1', text)
    # Avoid triple+ newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Escape dollar signs to prevent LaTeX rendering in MDX
    # Skip already-escaped \$ and $-in-URLs
    text = re.sub(r'(?<!\\)\$(?!\$)', r'\\$', text)
    return text


def _load_style_guide() -> str:
    global _style_guide
    if _style_guide is None:
        _style_guide = (PROJECT_ROOT / "docs" / "style_guide.md").read_text()
    return _style_guide


def _build_raw_analysis_block(
    ledger: CountryLedger,
    entry: WeeklyEntry,
) -> str:
    """Serialize the raw analytical output for the editor's context."""
    raw = {
        "country": ledger.country,
        "code": ledger.code,
        "posture_summary": ledger.posture_summary.text,
        "activity_level": entry.activity_level,
        "category_movements": {},
    }

    if entry.category_movements:
        for cat, mov in entry.category_movements.items():
            cat_key = cat.value if hasattr(cat, "value") else str(cat)
            raw["category_movements"][cat_key] = {
                "movement": mov.movement.value if hasattr(mov.movement, "value") else str(mov.movement),
                "prior_assessment": mov.prior_assessment,
                "updated_assessment": mov.updated_assessment,
                "developments": [
                    {
                        "headline": d.headline,
                        "summary": d.summary,
                        "signal_category_relevance": d.signal_category_relevance,
                        "actors_involved": d.actors_involved,
                    }
                    for d in mov.developments
                ],
                "confidence_change": (
                    {
                        "from": mov.confidence_change.from_,
                        "to": mov.confidence_change.to,
                        "reason": mov.confidence_change.reason,
                    }
                    if mov.confidence_change
                    else None
                ),
            }

    if entry.unexpected_developments:
        raw["unexpected_developments"] = [
            {"headline": ud.headline, "assessment": ud.assessment}
            for ud in entry.unexpected_developments
            if ud.headline and ud.headline.lower() not in ("unknown", "")
        ]

    if entry.absence_check:
        raw["absence_check"] = [
            {"expected": a.expected, "significance": a.significance, "occurred": a.occurred}
            for a in entry.absence_check
            if a.significance
        ]

    if entry.structural_claim_checks:
        raw["structural_claim_checks"] = [
            {"claim_ref": s.claim_ref, "status": s.status.value if hasattr(s.status, "value") else str(s.status), "evidence": s.evidence}
            for s in entry.structural_claim_checks
        ]

    return json.dumps(raw, indent=2, default=str)


async def run_editor(
    assembled_section: str,
    ledger: CountryLedger,
    entry: WeeklyEntry,
    model: str | None = None,
) -> str:
    """Run the editor agent on a single country section.

    Args:
        assembled_section: The mechanically rendered Markdown section.
        ledger: The country ledger (for posture summary and metadata).
        entry: The weekly entry (raw analytical output).
        model: Override the default model.

    Returns:
        The edited Markdown section.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not assembled_section.strip():
        return assembled_section

    task_prompt = load_prompt("editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    raw_analysis = _build_raw_analysis_block(ledger, entry)
    user_message = (
        "## ASSEMBLED SECTION\n\n"
        f"{assembled_section}\n\n"
        "---\n\n"
        "## RAW ANALYSIS\n\n"
        f"```json\n{raw_analysis}\n```"
    )

    label = f"{ledger.country} ({ledger.code})"
    logger.info("Editor [%s]: starting, input=%d chars", label, len(assembled_section))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    response = await _stream_message(
        client,
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    result = "\n".join(text_parts)

    logger.info(
        "Editor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "editor", ledger.code.lower(), date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return _sanitize_mdx(result)


def _build_regional_analysis_block(report: "RegionalReport") -> str:
    """Serialize the regional report for the editor's context."""
    from dataclasses import asdict
    raw = asdict(report)
    # Convert enums to strings
    raw["region"] = report.region.value
    raw["week"] = report.week.isoformat()
    return json.dumps(raw, indent=2, default=str)


async def run_regional_editor(
    assembled_lead: str,
    report: "RegionalReport",
    model: str | None = None,
) -> str:
    """Run the editor agent on a regional lead section.

    Args:
        assembled_lead: The mechanically rendered regional lead text.
        report: The RegionalReport with cross-cutting dynamics and overview.
        model: Override the default model.

    Returns:
        The edited regional lead text.
    """
    from .regional import RegionalReport  # noqa: F811

    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not assembled_lead.strip():
        return assembled_lead

    task_prompt = load_prompt("editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    raw_analysis = _build_regional_analysis_block(report)
    user_message = (
        "## ASSEMBLED SECTION\n\n"
        "This is a **regional analysis lead** — not a country section. "
        "It synthesises cross-cutting dynamics across multiple countries in the region. "
        "Rewrite it into polished narrative prose following the style guide. "
        "Do not restructure into country-by-country summaries — preserve the cross-cutting framing.\n\n"
        f"{assembled_lead}\n\n"
        "---\n\n"
        "## RAW ANALYSIS\n\n"
        f"```json\n{raw_analysis}\n```"
    )

    label = report.region.value
    logger.info("Editor [regional/%s]: starting, input=%d chars", label, len(assembled_lead))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    response = await _stream_message(
        client,
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 4096,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    result = "\n".join(text_parts)

    logger.info(
        "Editor [regional/%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "editor", f"regional_{label}", date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return _sanitize_mdx(result)


async def edit_newsletter(
    newsletter: str,
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, WeeklyEntry],
    max_concurrent: int = 5,
) -> str:
    """Edit all country sections in a newsletter in parallel.

    Identifies country sections by ### headings, matches them to ledger/entry
    data, runs the editor on each, and reassembles.
    """
    # Split into segments: (text, country_code_or_none)
    segments = _split_country_sections(newsletter)

    editable = [
        (i, code) for i, (_, code) in enumerate(segments) if code is not None
    ]

    if not editable:
        logger.info("Editor: no country sections found, skipping")
        return newsletter

    logger.info("Editor: %d country sections to edit", len(editable))

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _edit(idx: int, code: str) -> tuple[int, str]:
        async with semaphore:
            section_text = segments[idx][0]
            ledger = country_ledgers.get(code)
            entry = country_entries.get(code)
            if not ledger or not entry:
                logger.warning("Editor [%s]: no ledger/entry data, skipping", code)
                return (idx, section_text)
            try:
                edited = await run_editor(section_text, ledger, entry)
                return (idx, edited)
            except Exception as e:
                logger.warning("Editor [%s] failed, using original: %s", code, e)
                return (idx, section_text)

    tasks = [_edit(idx, code) for idx, code in editable]
    results = await asyncio.gather(*tasks)

    assembled = [text for text, _ in segments]
    for idx, edited_text in results:
        assembled[idx] = edited_text

    return _sanitize_mdx("".join(assembled))


# Country code extraction from flag image URLs
_FLAG_PATTERN = re.compile(r'flagcdn\.com/h24/(\w{2})\.png')


def _split_country_sections(newsletter: str) -> list[tuple[str, str | None]]:
    """Split a newsletter into segments, identifying country sections.

    Returns list of (text, country_code_or_none). Country sections start
    with ### and contain a flag image from which we extract the code.
    """
    # Split by ### country headings (keeping the delimiter)
    parts = re.split(r'(?=\n\n### )', newsletter)

    result: list[tuple[str, str | None]] = []

    for part in parts:
        if not part:
            continue

        # Check if this is a country section
        if part.lstrip().startswith("### ") or part.startswith("\n\n### "):
            flag_match = _FLAG_PATTERN.search(part)
            if flag_match:
                code = flag_match.group(1)
                result.append((part, code))
                continue

        result.append((part, None))

    return result


# =========================================================================
# Region page editing (regional lead + country sections)
# =========================================================================

# Import display names for region detection
from ..agents.regional import REGION_DISPLAY_NAMES


async def edit_region_page(
    page: str,
    regional_reports: dict,
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, WeeklyEntry],
    max_concurrent: int = 5,
) -> str:
    """Edit a region page: regional lead + country sections.

    Splits the page into the regional lead (before first ### country heading)
    and country sections, edits both, and reassembles.
    """
    # Find the regional lead vs country sections
    first_country = re.search(r'\n\n### ', page)
    if first_country:
        lead_text = page[:first_country.start()]
        country_text = page[first_country.start():]
    else:
        lead_text = page
        country_text = ""

    # Identify which region this page is for
    region = None
    for r in REGION_DISPLAY_NAMES:
        display = REGION_DISPLAY_NAMES[r]
        if display in page:
            region = r
            break

    # Edit regional lead if we have a report
    if region and region in regional_reports:
        report = regional_reports[region]
        # Extract just the prose (skip MDX frontmatter)
        lead_lines = lead_text.split("\n")
        frontmatter_end = 0
        in_frontmatter = False
        for i, line in enumerate(lead_lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    frontmatter_end = i + 1
                    in_frontmatter = False

        if frontmatter_end > 0:
            frontmatter = "\n".join(lead_lines[:frontmatter_end])
            prose = "\n".join(lead_lines[frontmatter_end:])
        else:
            frontmatter = ""
            prose = lead_text

        if prose.strip():
            try:
                edited_prose = await run_regional_editor(prose, report)
                lead_text = frontmatter + "\n" + edited_prose if frontmatter else edited_prose
            except Exception as e:
                logger.warning("Editor [regional/%s] failed, using original: %s", region.value, e)

    # Edit country sections
    if country_text.strip():
        edited_countries = await edit_newsletter(
            country_text, country_ledgers, country_entries, max_concurrent
        )
    else:
        edited_countries = country_text

    return _sanitize_mdx(lead_text + edited_countries)


# =========================================================================
# Executive brief editing
# =========================================================================


async def run_executive_editor(
    assembled_brief: str,
    briefing_items: list,
    model: str | None = None,
) -> str:
    """Run the editor agent on the executive brief.

    Args:
        assembled_brief: The mechanically rendered executive brief Markdown.
        briefing_items: The structured ExecutiveBriefingItem list from the global ledger.
        model: Override the default model.

    Returns:
        The edited executive brief as a unified analytical essay.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not assembled_brief.strip():
        return assembled_brief

    task_prompt = load_prompt("editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    # Serialize briefing items as raw analysis
    raw_items = []
    for item in briefing_items:
        raw_items.append({
            "title": item.title,
            "regions_involved": item.regions_involved,
            "what": item.what,
            "why_it_matters": item.why_it_matters,
            "what_to_watch": item.what_to_watch,
            "confidence": item.confidence,
            "confidence_note": item.confidence_note,
        })
    raw_analysis = json.dumps(raw_items, indent=2, default=str)

    user_message = (
        "## ASSEMBLED SECTION\n\n"
        "This is the **executive brief** — the top-level analytical summary of the week. "
        "It was assembled mechanically as a series of separate items with ### headings. "
        "Your job is to weave these into a unified analytical essay:\n\n"
        "- Drop the ### item headings.\n"
        "- Merge items that make related points.\n"
        "- Reorder for narrative flow — lead with the most important development.\n"
        "- Add transitions so the brief reads as a coherent story, not disconnected observations.\n"
        "- Eliminate redundancy across items.\n"
        "- Keep confidence notes where they add value (low or contested confidence).\n"
        "- The result should be 3-5 paragraphs of flowing prose.\n\n"
        f"{assembled_brief}\n\n"
        "---\n\n"
        "## RAW ANALYSIS\n\n"
        f"```json\n{raw_analysis}\n```"
    )

    logger.info("Editor [executive]: starting, input=%d chars", len(assembled_brief))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    response = await _stream_message(
        client,
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 4096,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    result = "\n".join(text_parts)

    logger.info(
        "Editor [executive]: done — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "editor", "executive", date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return _sanitize_mdx(result)


async def edit_overview_page(
    page: str,
    briefing_items: list,
) -> str:
    """Edit the overview page: run the executive brief through the editor.

    Extracts the executive brief section (between the week heading and the
    --- before Regions), edits it, and reassembles.
    """
    # The executive brief sits between "## Week of..." and "---\n\n## Regions"
    regions_marker = re.search(r'\n---\n\n## Regions', page)
    if not regions_marker:
        logger.info("Editor [overview]: no Regions marker found, skipping")
        return page

    # Find the brief content — it's after the week heading, before the regions divider
    # The page structure is: frontmatter + week heading + executive brief + --- + ## Regions + cards
    preamble_end = re.search(r'\n## Week of .+\n', page)
    if not preamble_end:
        logger.info("Editor [overview]: no week heading found, skipping")
        return page

    brief_start = preamble_end.end()
    brief_end = regions_marker.start()
    brief_text = page[brief_start:brief_end].strip()

    if not brief_text or brief_text.startswith("*No system-level"):
        return page

    try:
        edited_brief = await run_executive_editor(brief_text, briefing_items)
        return page[:brief_start] + "\n\n" + edited_brief + "\n\n" + page[brief_end:]
    except Exception as e:
        logger.warning("Editor [executive] failed, using original: %s", e)
        return page
