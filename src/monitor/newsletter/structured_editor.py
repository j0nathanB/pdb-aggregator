"""
Structured editor: receives content models, returns edited prose as JSON.

Replaces the regex-split markdown editor. The LLM receives structured
analytical data and returns JSON with prose fields. No markdown I/O.
"""

import asyncio
import json
import logging
import os
import re
from datetime import date
from pathlib import Path

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    load_prompt,
)
from ..sanitize import _record_fallback, extract_json
from ..timing import TrackedSemaphore
from ._streaming import stream_with_retry
from .content_models import (
    CountryContent,
    ExecutiveBriefContent,
    OverviewPageContent,
    RegionPageContent,
)

logger = logging.getLogger(__name__)

EDITOR_MODEL = MODEL

# Feature flag: when set, use Anthropic tool_use with typed input_schema
# for prose outputs rather than free-form JSON + json_repair fallback.
# Same flag that gates the country agent and story_map migrations.
USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"

# =============================================================================
# Tool definitions for country-scope prose editing
# =============================================================================
#
# edit_country and copyedit_country both emit {"narrative_body": str,
# "other_stories": [{"headline": str, "summary": str}]}. Style-editor for
# country emits just {"narrative_body": str}. The schemas are small enough
# to hand-write; pydantic isn't worth the ceremony for this.

COUNTRY_EDIT_TOOL_NAME = "record_country_narrative"
COUNTRY_EDIT_TOOL = {
    "name": COUNTRY_EDIT_TOOL_NAME,
    "description": (
        "Record the edited country narrative. Call exactly once when your "
        "editing is complete. The 'narrative_body' field holds your polished "
        "prose (use \\n\\n for paragraph breaks). 'other_stories' is "
        "optional; include it only if the input had other_stories to polish."
    ),
    "input_schema": {
        "type": "object",
        "required": ["narrative_body"],
        "properties": {
            "narrative_body": {"type": "string"},
            "other_stories": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["headline", "summary"],
                    "properties": {
                        "headline": {"type": "string"},
                        "summary": {"type": "string"},
                    },
                },
            },
        },
    },
}

COUNTRY_STYLE_TOOL_NAME = "record_styled_narrative"
COUNTRY_STYLE_TOOL = {
    "name": COUNTRY_STYLE_TOOL_NAME,
    "description": (
        "Record the style-edited country narrative. Call exactly once. "
        "'narrative_body' is the only required field."
    ),
    "input_schema": {
        "type": "object",
        "required": ["narrative_body"],
        "properties": {
            "narrative_body": {"type": "string"},
        },
    },
}


def _extract_tool_input(response, tool_name: str) -> dict | None:
    """Return the tool_use block's input for `tool_name`, or None."""
    for block in response.content:
        if (
            getattr(block, "type", None) == "tool_use"
            and getattr(block, "name", None) == tool_name
        ):
            return getattr(block, "input", None)
    return None

# Style guide loaded once per process
_style_guide: str | None = None

# =============================================================================
# Narrative body sanitizer
# =============================================================================
#
# Editor LLMs sometimes inject artifacts into narrative_body that should not
# be there: leading `### Country` headings (the template renders the flag
# heading separately), `**Activity Level:** ...` markers (analytical metadata
# not for the reader), and `<Accordion>...</Accordion>` blocks (rendered
# separately from the structured `other_stories` field). Editor system prompts
# explicitly prohibit these, but LLMs occasionally regress.
#
# This sanitizer runs after every editorial pass on narrative_body and strips
# the known artifact patterns. Logs a WARNING when it strips anything so we
# can track regression rates. Patterns are extensible — add new ones here as
# we discover them.

# Match opening accordion tag, anything (non-greedy), closing tag
_ACCORDION_RE = re.compile(
    r"<Accordion[^>]*>.*?</Accordion>\s*",
    re.DOTALL | re.IGNORECASE,
)

# Match any `### ...` or `#### ...` heading line, anywhere in the text.
# Editor prompts prohibit markdown headings; any heading line is an artifact.
_HEADING_RE = re.compile(r"^\s*#{3,4}\s+[^\n]*\n+", re.MULTILINE)

# Match `**Activity Level:** ...` and the variant `**Activity Level: ...**`
# (LLM sometimes wraps the value inside the bold markers).
_ACTIVITY_LEVEL_RE = re.compile(
    r"^\s*\*\*Activity\s*Level[:\s]?[^\n*]*\*\*[^\n]*\n+",
    re.MULTILINE | re.IGNORECASE,
)


def sanitize_narrative_body(text: str, label: str = "") -> str:
    """Strip known artifact patterns from narrative_body prose.

    Removes accordion blocks, leading `### Heading` lines, and `**Activity
    Level:**` markers that editor LLMs sometimes inject. Logs a warning and
    increments the `narrative_sanitized` fallback counter when anything is
    stripped, so regression is observable.
    """
    if not text:
        return text

    original_len = len(text)
    stripped: list[str] = []

    new_text, n = _ACCORDION_RE.subn("", text)
    if n > 0:
        stripped.append(f"{n} accordion block(s)")
        text = new_text

    new_text, n = _HEADING_RE.subn("", text)
    if n > 0:
        stripped.append(f"{n} heading(s)")
        text = new_text

    new_text, n = _ACTIVITY_LEVEL_RE.subn("", text)
    if n > 0:
        stripped.append(f"{n} activity-level marker(s)")
        text = new_text

    text = text.strip()

    if stripped:
        ctx = f" [{label}]" if label else ""
        logger.warning(
            "Sanitized narrative_body%s: stripped %s (%d → %d chars)",
            ctx, ", ".join(stripped), original_len, len(text),
        )
        _record_fallback("narrative_sanitized")

    return text


NAMES_AND_TITLES_SECTION = """#### names and titles — briefing conventions ####

- First mention: forename + surname, with office as appositive or context (*Andrii Sybiha, the foreign minister*; *Oleksandr Syrskyi, the commander-in-chief*)
- For universally recognised figures (Trump, Zelensky, Putin), forename + surname alone is sufficient on first mention.
- Subsequent mentions: Mr/Ms + surname (*Mr Sybiha*) or the office in lowercase (*the foreign minister*, *the president*)
- Military officers on active duty: retain rank on all mentions (*General Syrskyi*)
- No Mr, Mrs, Miss, Ms or Dr on first mention.
"""


def _load_style_guide() -> str:
    global _style_guide
    if _style_guide is None:
        from ..config import PROJECT_ROOT
        path = PROJECT_ROOT / "assets" / "prompts" / "editors" / "style_editor.md"
        if path.exists():
            _style_guide = path.read_text()
        else:
            _style_guide = ""
    return _style_guide


def _unwrap_double_json(data: dict) -> dict:
    """Fix LLM double-encoding: if a value is a JSON string containing the same keys, unwrap it."""
    result = {}
    for key, value in data.items():
        if isinstance(value, str) and value.strip().startswith("{"):
            try:
                inner = json.loads(value)
                if isinstance(inner, dict) and key in inner:
                    # Double-wrapped: {"regional_lead": "{\"regional_lead\": \"...\"}"}
                    result[key] = inner[key]
                    continue
            except (json.JSONDecodeError, KeyError):
                pass
        result[key] = value
    return result


def _build_system_prompt(base_prompt: str) -> str:
    """Append the style guide wrapped in XML tags to a base system prompt."""
    style_guide = _load_style_guide()
    if style_guide:
        return f"{base_prompt}\n\n<style_guide>\n{NAMES_AND_TITLES_SECTION}\n{style_guide}\n</style_guide>"
    return base_prompt


def _build_country_input(country: CountryContent) -> str:
    """Build the structured input JSON for the country editor.

    Mirrors the old editor's input: posture summary, activity level,
    full category movements (with prior/updated assessments, per-development
    detail, confidence changes), unexpected developments, absence checks,
    structural claim checks, and other stories.
    """
    devs = []
    for d in country.developments:
        devs.append({
            "category": d.category_display,
            "movement": d.movement.value,
            "text": d.text,
            "sources": [{"name": s.name, "url": s.url} for s in d.sources] if d.sources else [],
        })

    data = {
        "country": country.country,
        "code": country.code,
        "posture_summary": country.posture_summary,
        "activity_rating": country.activity_rating,
        "developments": devs,
        "unexpected": [
            {"headline": u.headline, "assessment": u.assessment}
            for u in country.unexpected
        ],
        "absences": [
            {"expected": a.expected, "significance": a.significance}
            for a in country.absences
        ],
        "other_stories": [
            {"headline": s.headline, "summary": s.summary}
            for s in country.other_stories
        ],
    }
    # Include the full raw analysis context — this is what gives the editor
    # depth to work with (prior/updated assessments, confidence changes,
    # structural claim checks, actors involved)
    if country.raw_analysis:
        data["raw_analysis"] = country.raw_analysis

    return json.dumps(data, indent=2, ensure_ascii=False)


COUNTRY_EDITOR_SYSTEM = load_prompt("editors/country_editor")


REGIONAL_EDITOR_SYSTEM = load_prompt("editors/regional_editor")


EXECUTIVE_EDITOR_SYSTEM = load_prompt("editors/executive_editor")


# =============================================================================
# Editor functions
# =============================================================================

async def _call_editor_once(
    client: anthropic.AsyncAnthropic,
    system_prompt: str,
    user_message: str,
    label: str,
    model: str,
    tools: list[dict] | None = None,
) -> tuple[str, anthropic.types.Message]:
    """Single API call for the country editor. Returns (response_text, response).

    If `tools` is provided, registers them (e.g., for tool_use structured output).
    """
    kwargs: dict = dict(
        model=model,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
    )
    if tools:
        kwargs["tools"] = tools
    response = await stream_with_retry(
        client,
        f"Editor {label}: streaming API call",
        f"editor_{label}",
        **kwargs,
    )
    text_parts = [b.text for b in response.content if b.type == "text"]
    return "\n".join(text_parts), response


# Stricter retry message used when the editor returns the wrong shape
# (e.g., echoed input JSON, prose without the narrative_body wrapper).
_RETRY_INSTRUCTION = """The previous attempt did not return the expected format. Try again. Your output must be EXACTLY one JSON object with a single key `narrative_body` containing a multi-paragraph prose string. No other top-level keys. No markdown headings. No JSON shape that mirrors the input. Example shape:

{"narrative_body": "First paragraph of flowing prose.\\n\\nSecond paragraph.\\n\\nThird paragraph."}

Now produce that for the country whose input you received above."""


async def edit_country(
    country: CountryContent,
    analysis_date: date | None = None,
    model: str | None = None,
) -> CountryContent:
    """Edit a single country section. Sets narrative_body on the content model."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not country.developments and not country.posture_summary:
        return country

    system_prompt = _build_system_prompt(COUNTRY_EDITOR_SYSTEM)
    user_message = _build_country_input(country)
    use_model = model or EDITOR_MODEL

    logger.info("Editor [%s]: starting structured edit%s",
                country.code, " [tool_use]" if USE_TOOL_SCHEMA else "")

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    tools = [COUNTRY_EDIT_TOOL] if USE_TOOL_SCHEMA else None
    response_text, response = await _call_editor_once(
        client, system_prompt, user_message, country.code, use_model, tools=tools,
    )

    from ..trace import format_usage_short
    logger.info(
        "Editor [%s]: done — %s%s",
        country.code, format_usage_short(response),
        " [tool_use]" if USE_TOOL_SCHEMA else "",
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()

    def _has_narrative(data) -> bool:
        return isinstance(data, dict) and "narrative_body" in data and isinstance(data["narrative_body"], str) and data["narrative_body"].strip()

    parsed = None

    # Prefer tool_use block when present — schema-validated, no quote-escape bugs.
    if USE_TOOL_SCHEMA:
        tool_input = _extract_tool_input(response, COUNTRY_EDIT_TOOL_NAME)
        if _has_narrative(tool_input):
            parsed = tool_input
            response_text = json.dumps(tool_input, indent=2, ensure_ascii=False)
        else:
            logger.warning(
                "Editor [%s]: tool_use enabled but no valid tool_use block; "
                "falling back to free-form JSON path",
                country.code,
            )
            _record_fallback("editor_tool_use_fallback")

    save_raw_response(
        "editor", country.code, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    # Free-form JSON path (and fallback when tool_use didn't deliver)
    if not _has_narrative(parsed):
        try:
            parsed = extract_json(response_text, context=f"editor_{country.code}")
        except (ValueError, KeyError):
            pass

    # Retry once if the first response is missing narrative_body
    if not _has_narrative(parsed):
        logger.warning(
            "Editor [%s]: first attempt missing narrative_body (parsed keys: %s); retrying with stricter instruction",
            country.code,
            list(parsed.keys())[:5] if isinstance(parsed, dict) else type(parsed).__name__,
        )
        retry_message = (
            f"{user_message}\n\n---\n\n{_RETRY_INSTRUCTION}"
        )
        try:
            # Retry WITHOUT the tool — free-form as a last resort
            response_text, response = await _call_editor_once(
                client, system_prompt, retry_message, f"{country.code}-retry", use_model,
                tools=None,
            )
            from ..trace import format_usage_short
            logger.info(
                "Editor [%s] retry: %s",
                country.code, format_usage_short(response),
            )
            try:
                parsed = extract_json(response_text, context=f"editor_{country.code}_retry")
            except (ValueError, KeyError):
                parsed = None
        except Exception as e:
            logger.error("Editor [%s] retry failed: %s", country.code, e)

    if _has_narrative(parsed):
        country.narrative_body = parsed["narrative_body"]
        update_trace_parsed("editor", country.code, run_date, parsed_output=parsed)
    elif parsed is not None and isinstance(parsed, dict):
        # Parsed but still no narrative_body after retry — JSON-echo bug.
        # Fall back to posture_summary so the brief renders something coherent.
        logger.error(
            "Editor [%s]: retry also missing narrative_body — falling back to posture_summary",
            country.code,
        )
        _record_fallback("editor_json_echo")
        country.narrative_body = country.posture_summary or ""
        update_trace_parsed("editor", country.code, run_date, parsed_output=parsed)
    else:
        # JSON parse failed entirely — use raw text as narrative (LLM returned prose, not JSON)
        logger.warning("Editor [%s]: JSON parse failed, using raw response", country.code)
        country.narrative_body = response_text

    country.narrative_body = sanitize_narrative_body(
        country.narrative_body, label=f"editor_{country.code}",
    )
    return country


async def edit_regional(
    page: RegionPageContent,
    analysis_date: date | None = None,
    model: str | None = None,
) -> RegionPageContent:
    """Edit the regional lead, gap paragraphs, and card summary."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not page.regional_lead and not page.raw_dynamics and not page.countries:
        return page

    # Country summaries give the editor material even when dynamics are sparse
    country_summaries = [
        {"country": c.country, "summary": c.narrative_body}
        for c in page.countries if c.narrative_body
    ]

    input_data = {
        "region": page.display_name,
        "regional_lead": page.regional_lead or "",
        "regional_analyst_output": page.raw_dynamics or [],
        "country_summaries": country_summaries,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary_seed": page.card_summary,
    }
    user_message = json.dumps(input_data, indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt(REGIONAL_EDITOR_SYSTEM)

    logger.info("Editor [regional/%s]: starting", page.region.value)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    response = await stream_with_retry(
        client,
        f"Editor regional/{page.region.value}: streaming API call",
        f"editor_regional_{page.region.value}",
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    from ..trace import format_usage_short
    logger.info(
        "Editor [regional/%s]: done — %s",
        page.region.value, format_usage_short(response),
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "editor", f"regional_{page.region.value}", run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context=f"editor_regional_{page.region.value}")
        page.regional_lead = data.get("regional_lead", page.regional_lead)
        if "headline" in data:
            page.headline = data["headline"]
        if "gap_paragraphs" in data:
            page.gap_paragraphs = data["gap_paragraphs"]
        if "card_summary" in data:
            page.card_summary = data["card_summary"]
        update_trace_parsed("editor", f"regional_{page.region.value}", run_date, parsed_output=data)
    except (ValueError, KeyError):
        logger.warning("Editor [regional/%s]: JSON parse failed, keeping original", page.region.value)

    return page


async def edit_executive(
    brief: ExecutiveBriefContent,
    analysis_date: date | None = None,
    model: str | None = None,
) -> ExecutiveBriefContent:
    """Edit the executive brief — polish the writer's essay against briefing items."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not brief.edited_essay and not brief.items:
        return brief

    # Send writer's essay as primary, briefing items as constraint
    input_data = {
        "edited_essay": brief.edited_essay or "",
        "briefing_items": [
            {
                "title": item.title,
                "regions_involved": item.regions_involved,
                "what": item.what,
                "why_it_matters": item.why_it_matters,
                "what_to_watch": item.what_to_watch,
                "confidence": item.confidence,
            }
            for item in brief.items
        ],
    }
    items_json = json.dumps(input_data, indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt(EXECUTIVE_EDITOR_SYSTEM)

    logger.info("Editor [executive]: starting, %d items", len(brief.items))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    response = await stream_with_retry(
        client,
        "Editor executive: streaming API call",
        "editor_executive",
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": items_json}],
    )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    from ..trace import format_usage_short
    logger.info(
        "Editor [executive]: done — %s",
        format_usage_short(response),
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "editor", "executive", run_date,
        system_prompt=system_prompt,
        user_message=items_json,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context="editor_executive")
        brief.edited_essay = data.get("edited_essay", response_text)
        if "headline" in data:
            brief.headline = data["headline"]
        update_trace_parsed("editor", "executive", run_date, parsed_output=data)
    except (ValueError, KeyError):
        logger.warning("Editor [executive]: JSON parse failed, using raw response")
        brief.edited_essay = response_text

    return brief


# =============================================================================
# Orchestration — edit all content in parallel
# =============================================================================

async def edit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
    scope: str = "all",
    target_country: str | None = None,
    target_regions: list | None = None,
) -> tuple[OverviewPageContent, dict]:
    """Edit content. scope: 'all' | 'countries' | 'regional' | 'executive'.

    Optional filters for targeted-recovery flows:
        target_country: only edit this country code (within its region).
        target_regions: only edit regional leads for these regions.
    """

    semaphore = TrackedSemaphore(max_concurrent, "structured_editor")

    # Edit executive brief
    run_executive = False
    if scope == "all" and overview.executive_brief.items:
        run_executive = True
    elif scope == "executive" and overview.executive_brief.edited_essay:
        run_executive = True
    if run_executive:
        logger.info("Editing executive brief...")
        overview.executive_brief = await edit_executive(
            overview.executive_brief, analysis_date=analysis_date,
        )

    async def _edit_country(country: CountryContent) -> CountryContent:
        async with semaphore.acquire(country.code):
            return await edit_country(country, analysis_date=analysis_date)

    async def _edit_regional(page: RegionPageContent) -> RegionPageContent:
        async with semaphore.acquire(f"regional_{page.region.value}"):
            return await edit_regional(page, analysis_date=analysis_date)

    target_region_set = set(target_regions) if target_regions is not None else None

    # Collect all tasks
    tasks = []

    # Regional leads
    if scope in ("all", "regional"):
        for region, page in region_pages.items():
            if target_region_set is not None and region not in target_region_set:
                continue
            if page.regional_lead:
                tasks.append(_edit_regional(page))

    # Country sections
    if scope in ("all", "countries"):
        for region, page in region_pages.items():
            for country in page.countries:
                if target_country is not None and country.code != target_country:
                    continue
                if country.developments or country.posture_summary:
                    tasks.append(_edit_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    return overview, region_pages


# =============================================================================
# Style editor — final style guide compliance pass
# =============================================================================

STYLE_EDITOR_SYSTEM = load_prompt("editors/style_editor_system")


async def style_edit_prose(
    prose_fields: dict,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
    trace_root: Path | None = None,
) -> dict:
    """Run style editor on prose fields. Returns polished JSON.

    If trace_root is provided, trace files are written under that directory
    instead of briefs/, so harness runs don't clobber production traces.

    Country-scope tool_use: when USE_TOOL_SCHEMA is on and prose_fields is
    exactly `{"narrative_body": ...}`, register the typed tool so the API
    validates the output. Regional / executive / other shapes still use the
    free-form JSON path (migration for those in later phases).
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    system_prompt = _build_system_prompt(STYLE_EDITOR_SYSTEM)

    user_message = json.dumps(prose_fields, indent=2, ensure_ascii=False)

    # Only use tool_use when the caller's prose_fields matches the
    # country-scope schema (single narrative_body key).
    use_country_tool = (
        USE_TOOL_SCHEMA
        and set(prose_fields.keys()) == {"narrative_body"}
    )

    logger.info("Style editor [%s]: starting%s", label,
                " [tool_use]" if use_country_tool else "")

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    stream_kwargs: dict = dict(
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_message}],
    )
    if use_country_tool:
        stream_kwargs["tools"] = [COUNTRY_STYLE_TOOL]

    response = await stream_with_retry(
        client,
        f"Style editor {label}: streaming API call",
        f"style_editor_{label}",
        **stream_kwargs,
    )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    from ..trace import format_usage_short
    logger.info(
        "Style editor [%s]: done — %s%s",
        label, format_usage_short(response),
        " [tool_use]" if use_country_tool else "",
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()

    # Prefer tool_use block when present
    if use_country_tool:
        tool_input = _extract_tool_input(response, COUNTRY_STYLE_TOOL_NAME)
        if isinstance(tool_input, dict) and isinstance(tool_input.get("narrative_body"), str):
            save_raw_response(
                "style_editor", label, run_date,
                system_prompt=system_prompt,
                user_message=user_message,
                response_text=json.dumps(tool_input, indent=2, ensure_ascii=False),
                thinking_text=extract_thinking(response),
                usage=extract_usage(response),
                trace_root=trace_root,
            )
            update_trace_parsed("style_editor", label, run_date,
                                parsed_output=tool_input, trace_root=trace_root)
            return tool_input
        logger.warning(
            "Style editor [%s]: tool_use enabled but no valid block; falling back",
            label,
        )
        _record_fallback("style_editor_tool_use_fallback")

    save_raw_response(
        "style_editor", label, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
        trace_root=trace_root,
    )

    try:
        data = extract_json(response_text, context=f"style_editor_{label}")
        data = _unwrap_double_json(data)
        update_trace_parsed("style_editor", label, run_date, parsed_output=data, trace_root=trace_root)
        return data
    except (ValueError, KeyError):
        # LLM returned prose instead of JSON — use it as the polished version
        # of the first prose field in the input
        if response_text.strip():
            logger.info("Style editor [%s]: raw prose response, using as polished output", label)
            keys = list(prose_fields.keys())
            if len(keys) == 1:
                # Single field — map response directly
                result = {keys[0]: response_text.strip()}
            else:
                # Multiple fields — use response for the main prose field
                result = dict(prose_fields)
                main_key = next((k for k in keys if k in ("narrative_body", "regional_lead", "edited_essay")), keys[0])
                result[main_key] = response_text.strip()
            update_trace_parsed("style_editor", label, run_date, parsed_output=result, trace_root=trace_root)
            return result
        logger.warning("Style editor [%s]: empty response, keeping original", label)
        return prose_fields


async def style_edit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
    scope: str = "all",
    target_country: str | None = None,
    target_regions: list | None = None,
) -> tuple[OverviewPageContent, dict]:
    """Run style editor on prose content. scope: 'all' | 'countries' | 'regional' | 'executive'.

    See edit_all for target_country / target_regions semantics.
    """

    semaphore = TrackedSemaphore(max_concurrent, "style_editor")

    async def _se_country(country: CountryContent):
        if not country.narrative_body:
            return
        async with semaphore.acquire(country.code):
            result = await style_edit_prose(
                {"narrative_body": country.narrative_body},
                country.code, analysis_date,
            )
            country.narrative_body = sanitize_narrative_body(
                result.get("narrative_body", country.narrative_body),
                label=f"style_editor_{country.code}",
            )

    async def _se_regional(page: RegionPageContent):
        if not page.regional_lead:
            return
        async with semaphore.acquire(f"regional_{page.region.value}"):
            fields = {"regional_lead": page.regional_lead, "card_summary": page.card_summary}
            if page.headline:
                fields["headline"] = page.headline
            result = await style_edit_prose(
                fields, f"regional_{page.region.value}", analysis_date,
            )
            page.regional_lead = result.get("regional_lead", page.regional_lead)
            if "headline" in result:
                page.headline = result["headline"]
            if "card_summary" in result:
                page.card_summary = result["card_summary"]

    tasks = []

    # Executive brief
    if scope in ("all", "executive") and overview.executive_brief.edited_essay:
        async def _se_exec():
            async with semaphore.acquire("executive"):
                fields = {"edited_essay": overview.executive_brief.edited_essay}
                if overview.executive_brief.headline:
                    fields["headline"] = overview.executive_brief.headline
                result = await style_edit_prose(
                    fields, "executive", analysis_date,
                )
                overview.executive_brief.edited_essay = result.get(
                    "edited_essay", overview.executive_brief.edited_essay,
                )
                if "headline" in result:
                    overview.executive_brief.headline = result["headline"]
        tasks.append(_se_exec())

    target_region_set = set(target_regions) if target_regions is not None else None

    # Regional leads
    if scope in ("all", "regional"):
        for region, page in region_pages.items():
            if target_region_set is not None and region not in target_region_set:
                continue
            tasks.append(_se_regional(page))

    # Country sections
    if scope in ("all", "countries"):
        for region, page in region_pages.items():
            for country in page.countries:
                if target_country is not None and country.code != target_country:
                    continue
                tasks.append(_se_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    return overview, region_pages
