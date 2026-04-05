"""
Structured copyeditor: polishes prose fields on content models via JSON I/O.

Replaces the regex-split markdown copyeditor. The LLM receives prose fields
and returns polished versions. No markdown splitting or reassembly.
"""

import asyncio
import json
import logging
from datetime import date

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    PROJECT_ROOT,
    THINKING_BUDGET_TOKENS,
    load_prompt,
)
from ..rate_limit import anthropic_limiter
from ..sanitize import extract_json
from ..timing import TrackedSemaphore, with_heartbeat
from .content_models import (
    CountryContent,
    ExecutiveBriefContent,
    OverviewPageContent,
    RegionPageContent,
    WatchlistPageContent,
)

logger = logging.getLogger(__name__)

COPYEDITOR_MODEL = MODEL

# Style guide loaded once per process
_style_guide: str | None = None


def _load_style_guide() -> str:
    global _style_guide
    if _style_guide is None:
        path = PROJECT_ROOT / "assets" / "prompts" / "style_editor.md"
        if path.exists():
            _style_guide = path.read_text()
        else:
            _style_guide = ""
    return _style_guide


COPYEDITOR_SYSTEM = """
<role>
You are a copyeditor for a weekly geopolitical intelligence briefing. You receive prose fields as JSON and return polished versions. You do not change substance, structure, or analytical judgments — only mechanical polish.

Your model is The Economist's style: plain, direct prose that respects the reader's intelligence.
</role>

<inputs>
You receive a JSON object with one or more prose fields. Each field contains edited prose that needs mechanical polish. The field names vary by content type (e.g. `narrative_body`, `regional_lead`, `edited_essay`, `other_stories`).
</inputs>

<instructions>
For each prose field, apply these checks in priority order:

<abbreviations>
Write words in full on first appearance with abbreviation in parentheses: *Trades Union Congress (TUC)*, *Troubled Asset Relief Programme (TARP)*. After first mention, prefer the generic — *the agency* rather than *the IAEA*.

Do not give the abbreviation if the term is not used again.

Familiar abbreviations need not be spelled out: AIDS, BBC, CIA, EU, FBI, GDP, NATO, OECD, UNESCO.

All country-specific abbreviations and party names must be expanded:
- *the Labour Party (PT)* not bare *PT*
- *the Green Ecologist Party of Mexico (PVEM)* not bare *PVEM*
- *the Naval Secretariat (SEMAR)* not bare *SEMAR*

Pronounceable abbreviations in upper and lower case: Unicef, Mercosur, Pemex.

Foreign party/institution names translated to English with local abbreviation: *the Social Democratic Party (SPD)*, *the National Action Party (PAN)*.

Catch bare acronyms from upstream. Scan for any uppercase sequence (2-5 letters) not formally introduced. This is one of your most important jobs.
</abbreviations>

<prose_polish>
Tighten prose mechanically. Do not restructure or reorder — the editor already handled that.

Foreign-language quotes must be translated into English.
</prose_polish>
</instructions>

<style>
Plain words. Short words over long. *Let* not *permit*, *buy* not *purchase*, *show* not *demonstrate*. Poor countries are *poor*, not *underdeveloped*.

Active voice. "Sheinbaum rejected the proposal" not "The proposal was rejected by Sheinbaum."

Cut ruthlessly. If you can cut a word without losing meaning, cut it. *Currently*, *actually*, *really*, *very*, *significantly* — these usually serve no purpose.

No clichés. No *level playing fields*, *windows of opportunity*, *paradigm shifts*, *road maps*. No *it remains to be seen* or *only time will tell*.

No jargon. No *stakeholders*, *leveraging*, *synergies*, *going forward*.

No euphemisms. *Torture* not *enhanced interrogation*. *Poor* not *underprivileged*.

No throat-clearing. No "It is worth noting that" or "It should be mentioned that."

Translate foreign-language quotes into English.
</style>

<constraints>
- Do not change analytical judgments or factual claims.
- Do not restructure or reorder paragraphs.
- Do not add facts not in the input.
- If the prose is already clean, return it unchanged. Do not edit for the sake of editing.
</constraints>

<output_format>
Return the same JSON structure you received, with prose fields polished. Only modify string values — do not add or remove fields.
</output_format>"""


async def _copyedit_prose(
    prose_fields: dict,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
) -> dict:
    """Send prose fields to the copyeditor and return polished versions."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    from .structured_editor import _build_system_prompt
    system_prompt = _build_system_prompt(COPYEDITOR_SYSTEM)

    user_message = json.dumps(prose_fields, indent=2, ensure_ascii=False)

    logger.info("Copyeditor [%s]: starting", label)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or COPYEDITOR_MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 8192,
            temperature=1,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET_TOKENS,
            },
            system=[{"type": "text", "text": system_prompt}],
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            response = await with_heartbeat(
                stream.get_final_message(),
                f"Copyeditor {label}: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Copyeditor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "copyeditor", label, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context=f"copyeditor_{label}")
        from .structured_editor import _unwrap_double_json
        data = _unwrap_double_json(data)
        update_trace_parsed("copyeditor", label, run_date, parsed_output=data)
        return data
    except (ValueError, KeyError):
        # LLM returned prose instead of JSON — use as polished version
        if response_text.strip():
            logger.info("Copyeditor [%s]: raw prose response, using as polished output", label)
            keys = list(prose_fields.keys())
            if len(keys) == 1:
                result = {keys[0]: response_text.strip()}
            else:
                result = dict(prose_fields)
                main_key = next((k for k in keys if k in ("narrative_body", "regional_lead", "edited_essay")), keys[0])
                result[main_key] = response_text.strip()
            update_trace_parsed("copyeditor", label, run_date, parsed_output=result)
            return result
        logger.warning("Copyeditor [%s]: empty response, keeping original", label)
        return prose_fields


# =============================================================================
# Per-content-type copyediting
# =============================================================================

async def copyedit_country(
    country: CountryContent,
    analysis_date: date | None = None,
) -> CountryContent:
    """Copyedit a country section's prose fields."""
    if not country.narrative_body:
        return country

    fields = {"narrative_body": country.narrative_body}

    # Include other stories for polish
    if country.other_stories:
        fields["other_stories"] = [
            {"headline": s.headline, "summary": s.summary}
            for s in country.other_stories
        ]

    result = await _copyedit_prose(fields, country.code, analysis_date)

    country.narrative_body = result.get("narrative_body", country.narrative_body)
    if "other_stories" in result and country.other_stories:
        for i, story_data in enumerate(result["other_stories"]):
            if i < len(country.other_stories):
                country.other_stories[i].headline = story_data.get("headline", country.other_stories[i].headline)
                country.other_stories[i].summary = story_data.get("summary", country.other_stories[i].summary)

    return country


async def copyedit_regional(
    page: RegionPageContent,
    analysis_date: date | None = None,
) -> RegionPageContent:
    """Copyedit a regional page's prose fields."""
    if not page.regional_lead:
        return page

    fields = {
        "regional_lead": page.regional_lead,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary": page.card_summary,
    }

    result = await _copyedit_prose(fields, f"regional_{page.region.value}", analysis_date)

    page.regional_lead = result.get("regional_lead", page.regional_lead)
    if "gap_paragraphs" in result:
        page.gap_paragraphs = result["gap_paragraphs"]
    if "card_summary" in result:
        page.card_summary = result["card_summary"]

    return page


async def copyedit_executive(
    brief: ExecutiveBriefContent,
    analysis_date: date | None = None,
) -> ExecutiveBriefContent:
    """Copyedit the executive brief essay."""
    if not brief.edited_essay:
        return brief

    fields = {"edited_essay": brief.edited_essay}
    result = await _copyedit_prose(fields, "executive", analysis_date)
    brief.edited_essay = result.get("edited_essay", brief.edited_essay)
    return brief


async def copyedit_watchlist(
    watchlist: WatchlistPageContent,
    analysis_date: date | None = None,
) -> WatchlistPageContent:
    """Copyedit watchlist item prose."""
    if not watchlist.items:
        return watchlist

    fields = {
        "items": [
            {"item": w.item, "why_it_matters": w.why_it_matters, "trigger": w.trigger}
            for w in watchlist.items
        ],
    }

    result = await _copyedit_prose(fields, "watchlist", analysis_date)

    if "items" in result:
        for i, item_data in enumerate(result["items"]):
            if i < len(watchlist.items):
                watchlist.items[i].item = item_data.get("item", watchlist.items[i].item)
                watchlist.items[i].why_it_matters = item_data.get("why_it_matters", watchlist.items[i].why_it_matters)
                watchlist.items[i].trigger = item_data.get("trigger", watchlist.items[i].trigger)

    return watchlist


# =============================================================================
# Orchestration
# =============================================================================

async def copyedit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    watchlist: WatchlistPageContent,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
) -> tuple[OverviewPageContent, dict, WatchlistPageContent]:
    """Copyedit all content models in parallel."""

    semaphore = TrackedSemaphore(max_concurrent, "structured_copyeditor")

    async def _ce_country(country: CountryContent) -> CountryContent:
        async with semaphore.acquire(country.code):
            return await copyedit_country(country, analysis_date)

    async def _ce_regional(page: RegionPageContent) -> RegionPageContent:
        async with semaphore.acquire(f"regional_{page.region.value}"):
            return await copyedit_regional(page, analysis_date)

    tasks = []

    # Executive brief
    if overview.executive_brief.edited_essay:
        async def _ce_exec():
            async with semaphore.acquire("executive"):
                overview.executive_brief = await copyedit_executive(
                    overview.executive_brief, analysis_date,
                )
        tasks.append(_ce_exec())

    # Watchlist
    if watchlist.items:
        async def _ce_wl():
            async with semaphore.acquire("watchlist"):
                nonlocal watchlist
                watchlist = await copyedit_watchlist(watchlist, analysis_date)
        tasks.append(_ce_wl())

    # Regional leads
    for region, page in region_pages.items():
        if page.regional_lead:
            tasks.append(_ce_regional(page))

    # Country sections
    for region, page in region_pages.items():
        for country in page.countries:
            if country.narrative_body:
                tasks.append(_ce_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview cards from copyedited regional summaries
    for card in overview.region_cards:
        page = region_pages.get(card.region)
        if page and page.card_summary:
            card.summary = page.card_summary

    return overview, region_pages, watchlist
