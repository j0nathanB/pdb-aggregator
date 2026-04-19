"""
Structured copyeditor: polishes prose fields on content models via JSON I/O.

Replaces the regex-split markdown copyeditor. The LLM receives prose fields
and returns polished versions. No markdown splitting or reassembly.
"""

import asyncio
import json
import logging
from datetime import date
from pathlib import Path

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    PROJECT_ROOT,
    THINKING_BUDGET_TOKENS,
    load_country_config,
    load_prompt,
)
from ..rate_limit import anthropic_limiter
from ..sanitize import extract_json
from ..timing import TrackedSemaphore, with_heartbeat
from .content_models import (
    AtAGlancePageContent,
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
        path = PROJECT_ROOT / "assets" / "prompts" / "editors" / "style_editor.md"
        if path.exists():
            _style_guide = path.read_text()
        else:
            _style_guide = ""
    return _style_guide


COPYEDITOR_SYSTEM = load_prompt("editors/structured_copyeditor")


def _build_leader_reference(codes: list[str]) -> str:
    """Build a <leader_reference> block from country config actors."""
    lines = []
    for code in codes:
        try:
            cfg = load_country_config(code)
        except FileNotFoundError:
            continue
        actors = [f"{a.name} ({a.role})" for a in cfg.actors if a.role]
        if actors:
            lines.append(f"  {code.upper()} ({cfg.country}): {', '.join(actors)}")
    if not lines:
        return ""
    return (
        "\n\n<leader_reference>\n"
        "Current leaders and key political figures. Use these roles/titles when "
        "referring to these individuals — do not use outdated titles.\n"
        + "\n".join(lines)
        + "\n</leader_reference>"
    )


async def _copyedit_prose(
    prose_fields: dict,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
    country_codes: list[str] | None = None,
    system_prompt_text: str | None = None,
    trace_root: Path | None = None,
) -> dict:
    """Send prose fields to the copyeditor and return polished versions.

    If system_prompt_text is provided, it is used verbatim as the copyeditor
    system prompt (after the style_guide block is appended by
    _build_system_prompt). This lets evaluation harnesses swap in alternative
    copyeditor prompts without fighting the load_prompt cache.

    If trace_root is provided, trace files are written under that directory
    instead of briefs/, so harness runs don't clobber production traces.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    from .structured_editor import _build_system_prompt
    base_prompt = system_prompt_text if system_prompt_text is not None else COPYEDITOR_SYSTEM
    system_prompt = _build_system_prompt(base_prompt)

    if country_codes:
        system_prompt += _build_leader_reference(country_codes)

    user_message = json.dumps(prose_fields, indent=2, ensure_ascii=False)

    logger.info("Copyeditor [%s]: starting", label)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
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
        trace_root=trace_root,
    )

    try:
        data = extract_json(response_text, context=f"copyeditor_{label}")
        from .structured_editor import _unwrap_double_json
        data = _unwrap_double_json(data)
        update_trace_parsed("copyeditor", label, run_date, parsed_output=data, trace_root=trace_root)
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
            update_trace_parsed("copyeditor", label, run_date, parsed_output=result, trace_root=trace_root)
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

    result = await _copyedit_prose(fields, country.code, analysis_date, country_codes=[country.code])

    from .structured_editor import sanitize_narrative_body
    country.narrative_body = sanitize_narrative_body(
        result.get("narrative_body", country.narrative_body),
        label=f"copyeditor_{country.code}",
    )
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
        "headline": page.headline,
        "regional_lead": page.regional_lead,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary": page.card_summary,
    }

    region_codes = [c.code for c in page.countries]
    result = await _copyedit_prose(fields, f"regional_{page.region.value}", analysis_date, country_codes=region_codes)

    if "headline" in result:
        page.headline = result["headline"]
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
    if brief.headline:
        fields["headline"] = brief.headline
    all_codes = [cfg.stem for cfg in sorted((PROJECT_ROOT / "assets" / "country_configs" / "countries").glob("*.yaml"))]
    result = await _copyedit_prose(fields, "executive", analysis_date, country_codes=all_codes)
    brief.edited_essay = result.get("edited_essay", brief.edited_essay)
    if "headline" in result:
        brief.headline = result["headline"]
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


AT_A_GLANCE_SYSTEM = load_prompt("editors/at_a_glance_copyeditor")


async def copyedit_at_a_glance(
    at_a_glance: AtAGlancePageContent,
    analysis_date: date | None = None,
) -> AtAGlancePageContent:
    """Copyedit at-a-glance headlines — single LLM call for all countries."""
    headlines = []
    for region in at_a_glance.regions:
        for c in region.countries:
            headlines.append({
                "country_code": c.code,
                "country_name": c.name,
                "headline": c.headline,
            })

    if not headlines:
        return at_a_glance

    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    from .structured_editor import _build_system_prompt
    system_prompt = _build_system_prompt(AT_A_GLANCE_SYSTEM)

    codes = [h["country_code"] for h in headlines]
    system_prompt += _build_leader_reference(codes)

    user_message = json.dumps(headlines, indent=2, ensure_ascii=False)

    logger.info("Copyeditor [at_a_glance]: starting (%d headlines)", len(headlines))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)

    async with anthropic_limiter():
        async with client.messages.stream(
            model=COPYEDITOR_MODEL,
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
                "Copyeditor at_a_glance: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Copyeditor [at_a_glance]: done — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "copyeditor", "at_a_glance", run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context="copyeditor_at_a_glance")
        update_trace_parsed("copyeditor", "at_a_glance", run_date, parsed_output=data)
    except (ValueError, KeyError):
        logger.warning("Copyeditor [at_a_glance]: failed to parse response, keeping originals")
        return at_a_glance

    # Apply polished headlines back
    if isinstance(data, list):
        lookup = {item["country_code"]: item["headline"] for item in data if "country_code" in item and "headline" in item}
        for region in at_a_glance.regions:
            for c in region.countries:
                if c.code in lookup:
                    c.headline = lookup[c.code]

    return at_a_glance


# =============================================================================
# Orchestration
# =============================================================================

async def copyedit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    watchlist: WatchlistPageContent,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
    scope: str = "all",
    at_a_glance: AtAGlancePageContent | None = None,
) -> tuple[OverviewPageContent, dict, WatchlistPageContent, AtAGlancePageContent | None]:
    """Copyedit content models. scope: 'all' | 'countries' | 'regional' | 'executive'."""

    semaphore = TrackedSemaphore(max_concurrent, "structured_copyeditor")

    async def _ce_country(country: CountryContent) -> CountryContent:
        async with semaphore.acquire(country.code):
            return await copyedit_country(country, analysis_date)

    async def _ce_regional(page: RegionPageContent) -> RegionPageContent:
        async with semaphore.acquire(f"regional_{page.region.value}"):
            return await copyedit_regional(page, analysis_date)

    tasks = []

    # Executive brief
    if scope in ("all", "executive") and overview.executive_brief.edited_essay:
        async def _ce_exec():
            async with semaphore.acquire("executive"):
                overview.executive_brief = await copyedit_executive(
                    overview.executive_brief, analysis_date,
                )
        tasks.append(_ce_exec())

    # Watchlist
    if scope in ("all", "countries") and watchlist.items:
        async def _ce_wl():
            async with semaphore.acquire("watchlist"):
                nonlocal watchlist
                watchlist = await copyedit_watchlist(watchlist, analysis_date)
        tasks.append(_ce_wl())

    # At-a-glance headlines
    if scope in ("all", "countries") and at_a_glance and at_a_glance.regions:
        async def _ce_glance():
            async with semaphore.acquire("at_a_glance"):
                nonlocal at_a_glance
                at_a_glance = await copyedit_at_a_glance(at_a_glance, analysis_date)
        tasks.append(_ce_glance())

    # Regional leads
    if scope in ("all", "regional"):
        for region, page in region_pages.items():
            if page.regional_lead:
                tasks.append(_ce_regional(page))

    # Country sections
    if scope in ("all", "countries"):
        for region, page in region_pages.items():
            for country in page.countries:
                if country.narrative_body:
                    tasks.append(_ce_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    return overview, region_pages, watchlist, at_a_glance
