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
    from ..rate_limit import anthropic_limiter
    async with anthropic_limiter():
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


_NOTES_ACCORDION_RE = re.compile(
    r'\n*<Accordion title="Notes">.*?</Accordion>\s*',
    re.DOTALL,
)


def _strip_sources_accordion(text: str) -> tuple[str, str]:
    """Remove Notes accordion from text, returning (text_without, notes_block).

    The Notes accordion contains mechanical reference data that should not
    be sent to the editor LLM (which tends to drop it). It is re-appended
    after editing.
    """
    match = _NOTES_ACCORDION_RE.search(text)
    if not match:
        return text, ""
    sources_block = match.group(0).strip()
    text_without = text[:match.start()] + text[match.end():]
    return text_without, sources_block


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
    analysis_date: date | None = None,
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

    # Strip Sources accordion — it's mechanical reference data, not prose.
    # Re-append after editing so the editor doesn't drop it.
    section_to_edit, sources_suffix = _strip_sources_accordion(assembled_section)

    task_prompt = load_prompt("editors/editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    raw_analysis = _build_raw_analysis_block(ledger, entry)
    user_message = (
        "## ASSEMBLED SECTION\n\n"
        f"{section_to_edit}\n\n"
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

    from ..trace import save_raw_response, extract_thinking, extract_usage
    save_raw_response(
        "editor", ledger.code.lower(), analysis_date or date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    edited = _sanitize_mdx(result)
    if sources_suffix:
        edited = edited.rstrip() + "\n\n" + sources_suffix + "\n"
    return edited


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
    analysis_date: date | None = None,
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

    task_prompt = load_prompt("editors/editor")
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

    from ..trace import save_raw_response, extract_thinking, extract_usage
    save_raw_response(
        "editor", f"regional_{label}", analysis_date or date.today(),
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
    analysis_date: date | None = None,
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

    from ..timing import TrackedSemaphore
    semaphore = TrackedSemaphore(max_concurrent, "editor")

    async def _edit(idx: int, code: str) -> tuple[int, str]:
        async with semaphore.acquire(code):
            section_text = segments[idx][0]
            ledger = country_ledgers.get(code)
            entry = country_entries.get(code)
            if not ledger or not entry:
                logger.warning("Editor [%s]: no ledger/entry data, skipping", code)
                return (idx, section_text)
            try:
                edited = await run_editor(section_text, ledger, entry, analysis_date=analysis_date)
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
_FLAG_PATTERN = re.compile(r'flagcdn\.com/(?:h24/)?(\w{2})\.(?:png|svg)')


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
    analysis_date: date | None = None,
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

        # Preserve ## Regional Summary heading — strip before editing, re-prepend after
        section_heading = ""
        prose_stripped = prose.lstrip("\n")
        if prose_stripped.startswith("## "):
            heading_end = prose_stripped.index("\n") if "\n" in prose_stripped else len(prose_stripped)
            section_heading = prose_stripped[:heading_end]
            prose = prose_stripped[heading_end:]

        if prose.strip():
            try:
                edited_prose = await run_regional_editor(prose, report, analysis_date=analysis_date)
                # Strip any ### region heading the editor may have inserted
                edited_prose = re.sub(r'^###\s+[^\n]+\n+', '', edited_prose.lstrip("\n"))
                if section_heading:
                    edited_prose = section_heading + "\n\n" + edited_prose.lstrip("\n")
                lead_text = frontmatter + "\n" + edited_prose if frontmatter else edited_prose
            except Exception as e:
                logger.warning("Editor [regional/%s] failed, using original: %s", region.value, e)

    # Edit country sections
    if country_text.strip():
        edited_countries = await edit_newsletter(
            country_text, country_ledgers, country_entries, max_concurrent,
            analysis_date=analysis_date,
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
    analysis_date: date | None = None,
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

    task_prompt = load_prompt("editors/editor")
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
        "- If evidence is thin, say so in plain language — do not include pipeline metadata like "
        "'(confidence: contested)' parentheticals.\n"
        "- The result should be 3-5 paragraphs of flowing prose.\n\n"
        "### Worked example\n\n"
        "**BAD** (jargon-heavy, abstract, repetitive):\n\n"
        "> Allied countries are developing fundamentally incompatible strategies for managing "
        "alliance burden-sharing and strategic commitments, fragmenting traditional coordination "
        "mechanisms along regional lines. Czech Republic explicitly rejected NATO 3.5% spending "
        "targets while Romania secured €16.6 billion in EU defense funding and Finland targets "
        "3% GDP by 2029. This represents structural evolution of alliance systems beyond "
        "traditional coordination mechanisms — when allies cannot agree on burden-sharing "
        "fundamentals or strategic priorities, the alliance becomes a framework for managing "
        "disagreement rather than coordinating action.\n\n"
        "**GOOD** (concrete, sequential, readable):\n\n"
        "> Allied countries are splitting over the basics of burden-sharing, and the splits are "
        "hardening along regional lines.\n>\n"
        "> In Europe, the Czech Republic has rejected NATO's 3.5% spending target outright, while "
        "Romania secured €16.6 billion in EU defence funding and Finland aims for 3% of GDP by "
        "2029. France, Germany and Spain are each articulating versions of strategic autonomy — "
        "separately, and without American participation. They agree on the direction but not the "
        "details, and Washington is not in the room.\n>\n"
        "> In Asia, the pressures point in opposite directions. Japan is deepening its operational "
        "planning for a Taiwan contingency. South Korea is pursuing what it calls a 'full-scale "
        "restoration' of relations with China. Both are responding to American unreliability, but "
        "their answers are incompatible.\n\n"
        "Notice: short sentences, concrete facts first, plain language, regional grouping with "
        "narrative flow, no jargon like 'institutional logic' or 'strategic incoherence'. "
        "Say what is happening, who is doing it, why it matters, and stop.\n\n"
        "---\n\n"
        "## YOUR INPUT\n\n"
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

    from ..trace import save_raw_response, extract_thinking, extract_usage
    save_raw_response(
        "editor", "executive", analysis_date or date.today(),
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
    analysis_date: date | None = None,
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
        edited_brief = await run_executive_editor(brief_text, briefing_items, analysis_date=analysis_date)
        return page[:brief_start] + "\n\n" + edited_brief + "\n\n" + page[brief_end:]
    except Exception as e:
        logger.warning("Editor [executive] failed, using original: %s", e)
        return page


async def edit_watchlist_page(
    page: str,
    analysis_date: date | None = None,
    model: str | None = None,
) -> str:
    """Run the watchlist editor on the watchlist page.

    Rewrites mechanical bullet-point watchlist items into natural prose
    paragraphs while preserving frontmatter and footer.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not page.strip() or "*No items on the watchlist" in page:
        return page

    task_prompt = load_prompt("editors/watchlist_editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    user_message = (
        "Rewrite this watchlist page into natural prose. "
        "Return the full page including frontmatter and footer.\n\n"
        f"{page}"
    )

    logger.info("Editor [watchlist]: starting, input=%d chars", len(page))

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
        "Editor [watchlist]: done — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, extract_thinking, extract_usage
    save_raw_response(
        "editor", "watchlist", analysis_date or date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return _sanitize_mdx(result)


async def summarize_card_summaries(
    page: str,
    analysis_date: date | None = None,
) -> str:
    """Condense region Card summaries on the overview page to one sentence each.

    Finds each <Card> body, sends the text to Haiku for a one-sentence
    summary, and replaces it in the page.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    # Find all Card bodies (text between <Card ...> and </Card>)
    card_pattern = re.compile(
        r'(<Card\s+title="[^"]*"\s+icon="[^"]*"\s+href="[^"]*">)\s*\n\s*(.*?)\s*\n\s*(</Card>)',
        re.DOTALL,
    )
    matches = [m for m in card_pattern.finditer(page) if "Watchlist" not in m.group(1)]
    if not matches:
        return page

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async def _summarize(text: str) -> str:
        if not text.strip() or len(text) < 20:
            return text
        from ..rate_limit import anthropic_limiter
        async with anthropic_limiter():
            response = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": (
                        "Condense this regional summary into ONE concise sentence for a navigation card. "
                        "No jargon, no hedging. State what happened this week. "
                        "Do not invent details not in the source text.\n\n"
                        f"{text}"
                    ),
                }],
            )
        return response.content[0].text.strip()

    # Summarize all cards in parallel
    card_texts = [m.group(2).strip() for m in matches]
    summaries = await asyncio.gather(*[_summarize(t) for t in card_texts])

    # Replace in reverse order to preserve positions
    result = page
    for match, summary in reversed(list(zip(matches, summaries))):
        opening = match.group(1)
        closing = match.group(3)
        result = result[:match.start()] + f"{opening}\n    {summary}\n  {closing}" + result[match.end():]

    logger.info("Card summaries: condensed %d cards via Haiku", len(matches))
    return result


# =========================================================================
# Style editor — final pass for style guide compliance
# =========================================================================

async def run_style_editor(
    section_text: str,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
) -> str:
    """Run the style editor on a single prose section.

    This is the final editorial pass. It rewrites prose to comply with the
    style guide without changing analytical content. Each section (executive,
    regional, country) is processed separately for optimal output.

    Args:
        section_text: The prose section to edit.
        label: Label for logging and trace file (e.g., "executive", "regional_americas", "ua").
        analysis_date: Pipeline end date for trace directory.
        model: Override the default model.

    Returns:
        The style-compliant prose section.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not section_text.strip():
        return section_text

    # Strip Notes accordion — re-append after editing
    section_to_edit, sources_suffix = _strip_sources_accordion(section_text)

    task_prompt = load_prompt("editors/style_editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    user_message = section_to_edit

    logger.info("Style editor [%s]: starting, input=%d chars", label, len(section_to_edit))

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
        "Style editor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, extract_thinking, extract_usage
    save_raw_response(
        "style_editor", label.lower().replace(" ", "_"),
        analysis_date or date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    edited = _sanitize_mdx(result)
    if sources_suffix:
        edited = edited.rstrip() + "\n\n" + sources_suffix + "\n"
    return edited


async def style_edit_page(
    page: str,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
) -> str:
    """Run the style editor on all prose sections of a page.

    Splits the page into individual sections (regional lead + each country),
    processes each through the style editor in parallel, and reassembles.
    """
    # Split into segments by ### country headings
    segments = _split_country_sections(page)

    from ..timing import TrackedSemaphore
    semaphore = TrackedSemaphore(max_concurrent, "style_editor")

    async def _edit(idx: int, text: str, code: str | None) -> tuple[int, str]:
        async with semaphore.acquire(code or f"segment_{idx}"):
            if code:
                label = code
            elif idx == 0:
                # First segment is the regional lead (or overview preamble)
                label = "regional_lead"
            else:
                label = f"section_{idx}"

            # Skip very short segments (separators, empty)
            if len(text.strip()) < 50:
                return (idx, text)

            try:
                edited = await run_style_editor(text, label, analysis_date=analysis_date)
                return (idx, edited)
            except Exception as e:
                logger.warning("Style editor [%s] failed, using original: %s", label, e)
                return (idx, text)

    tasks = [_edit(i, text, code) for i, (text, code) in enumerate(segments)]
    results = await asyncio.gather(*tasks)

    assembled = [text for text, _ in segments]
    for idx, edited_text in results:
        assembled[idx] = edited_text

    return _sanitize_mdx("".join(assembled))
