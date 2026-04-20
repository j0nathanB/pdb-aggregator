"""
Regional writer: produces Economist-style regional essays from edited country prose.

Runs after Round 1 editing (countries + watchlist). Each region's edited
country narrative_body texts are fed to the LLM, which writes a 4-5 paragraph
analytical essay with a thesis-driven through-line.
"""

import asyncio
import json
import logging
from datetime import date

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    load_prompt,
)
from ..rate_limit import anthropic_limiter
from ..sanitize import extract_json
from ..timing import TrackedSemaphore, with_heartbeat
from .content_models import RegionPageContent

logger = logging.getLogger(__name__)

WRITER_MODEL = MODEL

# System prompt built once per process
_system_prompt: str | None = None


def _build_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is not None:
        return _system_prompt

    task_instructions = load_prompt("writers/regional_writer")

    # Load style guide
    from ..config import PROJECT_ROOT
    style_path = PROJECT_ROOT / "assets" / "prompts" / "editors" / "style_editor.md"
    style_guide = style_path.read_text() if style_path.exists() else ""

    _system_prompt = f"""<role>
You are a writer for a weekly geopolitical intelligence briefing. You receive edited country summaries for a single region and write a unified analytical essay.

You are not an analyst. The analysts and editors have already done their work — the country summaries you receive are polished prose. Your job is to synthesize them into a single essay that makes an argument about what the week reveals in this region.
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
    "region": "Region name",
    "country_summaries": [
        {{"country": "Country Name", "summary": "Edited country narrative..."}},
        ...
    ]
}}
</input_format>

<output_format>
Return a JSON object:
{{
    "headline": "Short headline for the essay",
    "regional_lead": "Your 4-5 paragraph essay here..."
}}

No commentary. Just the JSON object.
</output_format>"""

    return _system_prompt


async def write_regional_essay(
    page: RegionPageContent,
    model: str | None = None,
) -> RegionPageContent:
    """Write a regional essay from edited country summaries."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    # Collect edited country prose
    summaries = []
    for country in page.countries:
        if country.narrative_body:
            summaries.append({
                "country": country.country,
                "summary": country.narrative_body,
            })

    if not summaries:
        logger.warning("Regional writer [%s]: no country summaries, skipping", page.region.value)
        return page

    input_data = {
        "region": page.display_name,
        "country_summaries": summaries,
    }
    user_message = json.dumps(input_data, indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt()
    use_model = model or WRITER_MODEL

    logger.info(
        "Regional writer [%s]: starting, %d country summaries",
        page.region.value, len(summaries),
    )

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=use_model,
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
                f"Regional writer {page.region.value}: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Regional writer [%s]: done — input=%d, output=%d tokens",
        page.region.value,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = page.week_end
    save_raw_response(
        "regional_writer", page.region.value, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    data = extract_json(response_text, context=f"regional_writer_{page.region.value}")
    if "regional_lead" in data:
        page.regional_lead = data["regional_lead"]
    if "headline" in data:
        page.card_summary = data["headline"]
    update_trace_parsed("regional_writer", page.region.value, run_date, parsed_output=data)

    return page


async def write_all_regional_essays(
    region_pages: dict,
    max_concurrent: int = 5,
    regions: list | None = None,
) -> dict:
    """Write regional essays for all regions in parallel.

    Args:
        regions: Optional filter — only write essays for these regions
            (list of Region enum members). Default None processes all.
    """

    semaphore = TrackedSemaphore(max_concurrent, "regional_writer")

    async def _write(page: RegionPageContent) -> RegionPageContent:
        async with semaphore.acquire(f"regional_writer_{page.region.value}"):
            return await write_regional_essay(page)

    target = set(regions) if regions is not None else None
    tasks = []
    for region, page in region_pages.items():
        if target is not None and region not in target:
            continue
        # Only write if there are countries with edited prose
        has_prose = any(c.narrative_body for c in page.countries)
        if has_prose:
            tasks.append(_write(page))

    if tasks:
        await asyncio.gather(*tasks)

    return region_pages
