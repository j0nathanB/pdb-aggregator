"""
Global writer: produces an Economist-style executive essay from edited regional prose.

Runs after Round 2 editing (regional essays). All five edited regional essays
are fed to the LLM, which writes a max 5-paragraph analytical essay with a
thesis-driven through-line about what the week reveals globally.
"""

import json
import logging
import os
from datetime import date

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    load_prompt,
)
from ..sanitize import _record_fallback, extract_json
from ._streaming import stream_with_retry
from .content_models import OverviewPageContent, RegionPageContent

logger = logging.getLogger(__name__)

WRITER_MODEL = MODEL

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"

GLOBAL_ESSAY_TOOL_NAME = "record_global_essay"
GLOBAL_ESSAY_TOOL = {
    "name": GLOBAL_ESSAY_TOOL_NAME,
    "description": (
        "Record the finished global executive essay. Call exactly once when "
        "the essay is complete. Both fields are required."
    ),
    "input_schema": {
        "type": "object",
        "required": ["headline", "edited_essay"],
        "properties": {
            "headline": {"type": "string"},
            "edited_essay": {"type": "string"},
        },
    },
}

# System prompt built once per process
_system_prompt: str | None = None


def _build_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is not None:
        return _system_prompt

    task_instructions = load_prompt("writers/global_writer")

    # Load style guide
    from ..config import PROJECT_ROOT
    style_path = PROJECT_ROOT / "assets" / "prompts" / "editors" / "style_editor.md"
    style_guide = style_path.read_text() if style_path.exists() else ""

    _system_prompt = f"""<role>
You are a writer for a weekly geopolitical intelligence briefing. You receive edited regional essays — one per region — and write a single unified analytical essay that captures what the week reveals globally.

You are not an analyst. The analysts and editors have already done their work — the regional essays you receive are polished prose. Your job is to synthesize them into a single essay that makes an argument about the global pattern.
</role>

<instructions>
{task_instructions}
</instructions>

<style_guide>
{style_guide}
</style_guide>

<input_format>
You receive a JSON object:
{{
    "regional_essays": [
        {{"region": "Region Name", "essay": "Edited regional essay..."}},
        ...
    ]
}}
</input_format>

<output_format>
Return a JSON object:
{{
    "headline": "Short headline for the essay",
    "edited_essay": "Your max 5-paragraph essay here..."
}}

No commentary. Just the JSON object.
</output_format>"""

    return _system_prompt


async def write_global_essay(
    overview: OverviewPageContent,
    region_pages: dict,
    model: str | None = None,
) -> OverviewPageContent:
    """Write the global executive essay from edited regional essays."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    # Collect edited regional prose
    essays = []
    for region, page in region_pages.items():
        if page.regional_lead:
            essays.append({
                "region": page.display_name,
                "essay": page.regional_lead,
            })

    if not essays:
        logger.warning("Global writer: no regional essays, skipping")
        return overview

    input_data = {"regional_essays": essays}
    user_message = json.dumps(input_data, indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt()
    use_model = model or WRITER_MODEL

    logger.info("Global writer: starting, %d regional essays%s",
                len(essays), " [tool_use]" if USE_TOOL_SCHEMA else "")

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    stream_kwargs: dict = dict(
        model=use_model,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )
    if USE_TOOL_SCHEMA:
        stream_kwargs["tools"] = [GLOBAL_ESSAY_TOOL]

    response = await stream_with_retry(
        client, "Global writer: streaming API call", "global_writer",
        **stream_kwargs,
    )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    # Prefer tool_use block when present
    tool_input: dict | None = None
    if USE_TOOL_SCHEMA:
        for block in response.content:
            if (getattr(block, "type", None) == "tool_use"
                    and getattr(block, "name", None) == GLOBAL_ESSAY_TOOL_NAME):
                tool_input = getattr(block, "input", None)
                break

    logger.info(
        "Global writer: done — input=%d, output=%d tokens%s",
        response.usage.input_tokens, response.usage.output_tokens,
        " [tool_use]" if tool_input else "",
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = overview.week_end

    if tool_input is not None:
        save_raw_response(
            "global_writer", "executive", run_date,
            system_prompt=system_prompt,
            user_message=user_message,
            response_text=json.dumps(tool_input, indent=2, ensure_ascii=False),
            thinking_text=extract_thinking(response),
            usage=extract_usage(response),
        )
        overview.executive_brief.edited_essay = tool_input.get("edited_essay", "")
        if "headline" in tool_input:
            overview.executive_brief.headline = tool_input["headline"]
        update_trace_parsed("global_writer", "executive", run_date, parsed_output=tool_input)
        return overview

    if USE_TOOL_SCHEMA:
        logger.warning("Global writer: tool_use enabled but no valid block; falling back")
        _record_fallback("global_writer_tool_use_fallback")

    save_raw_response(
        "global_writer", "executive", run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    data = extract_json(response_text, context="global_writer")
    if "edited_essay" in data:
        overview.executive_brief.edited_essay = data["edited_essay"]
    update_trace_parsed("global_writer", "executive", run_date, parsed_output=data)

    return overview
