"""
Structured editor: receives content models, returns edited prose as JSON.

Replaces the regex-split markdown editor. The LLM receives structured
analytical data and returns JSON with prose fields. No markdown I/O.
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
from .content_models import (
    CountryContent,
    ExecutiveBriefContent,
    OverviewPageContent,
    RegionPageContent,
    WatchlistPageContent,
)

logger = logging.getLogger(__name__)

EDITOR_MODEL = MODEL

# Style guide loaded once per process
_style_guide: str | None = None


def _load_style_guide() -> str:
    global _style_guide
    if _style_guide is None:
        from ..config import PROJECT_ROOT
        path = PROJECT_ROOT / "assets" / "prompts" / "style_editor.md"
        if path.exists():
            _style_guide = path.read_text()
        else:
            _style_guide = ""
    return _style_guide


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


COUNTRY_EDITOR_SYSTEM = """# Country Section Editor

## Role

You are an editor for a weekly geopolitical intelligence briefing. You receive structured analytical data for one country and produce narrative prose. You trust the analysis — your job is to make it read like something worth reading.

## Your Input

JSON with:
- `posture_summary` — the analyst's high-level assessment
- `developments` — categorised developments with movement ratings (significant/minor/none)
- `unexpected` — unexpected developments
- `absences` — notable absences
- `raw_analysis` — full category assessments for depth

## What You Do

Produce a `narrative_body` — a short essay of 2-5 paragraphs that a thoughtful generalist can absorb quickly.

### The Opening
Lead with the single most important development or tension. One to two sentences. No throat-clearing.

### The Body
Dissolve the developments into narrative paragraphs. Group by story logic, not by category. Use transitions. Lead each paragraph with action. Concrete detail over abstraction.

For categories with movement "none" — mention them only if the absence of change is itself significant (e.g., "the security sector remained quiet despite regional escalation"). Otherwise skip them.

### Names and Titles
- First mention: Office + forename + surname (*President Volodymyr Zelensky*)
- Subsequent: Mr/Ms + surname (*Mr Zelensky*) or the office (*the president*)
- Military: retain rank on all mentions (*General Syrskyi*)

### Style
Plain words. Active voice. Cut ruthlessly. No clichés, jargon, euphemisms, or throat-clearing. No inline source citations.

## What You Must Not Do
- Do not change analytical judgments
- Do not add facts not in the input
- Do not add inline source citations
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs

## Example

Input (condensed):
```json
{
  "country": "Ukraine",
  "posture_summary": "Ukraine's alignment posture shifted significantly...",
  "developments": [
    {"category": "Diplomatic", "movement": "significant", "text": "Zelensky called Europe fragmented and lost at Davos..."},
    {"category": "Diplomatic", "movement": "significant", "text": "Three-way talks between Ukrainian, Russian, and American delegations began in Abu Dhabi..."},
    {"category": "Security", "movement": "significant", "text": "General Syrskyi said Ukraine would go on the offensive in 2026..."},
    {"category": "Security", "movement": "significant", "text": "Defence Minister Fedorov set a goal of 50,000 Russian battlefield deaths a month..."},
    {"category": "Domestic", "movement": "significant", "text": "Budanov was made chief of the President's Office, replacing Yermak..."}
  ]
}
```

Output:
```json
{"narrative_body": "Ukraine is a wartime state recalibrating its Western strategy while shifting to a more aggressive military posture and, possibly, preparing for a change of leadership.\n\nAt Davos in January, President Volodymyr Zelensky delivered an unusually blunt speech calling Europe \"fragmented\" and \"lost,\" likening the situation to \"Groundhog Day.\" Europe, he said, looked \"lost trying to convince the US president to change,\" and President Donald Trump \"will not listen to this kind of Europe.\" The frustration had a purpose. After meeting Mr Trump separately, Mr Zelensky said the two had agreed on post-war American security guarantees, though territorial questions remain open. Days later, three-way talks between Ukrainian, Russian, and American delegations began in Abu Dhabi, with Ukraine sending a senior team including Kyrylo Budanov and Rustem Umerov. Mr Trump's envoy Steve Witkoff and his son-in-law Jared Kushner held three hours of talks with President Vladimir Putin. The Kremlin confirmed the format but said Russia would keep fighting until a deal was reached.\n\nEven as it negotiates, Ukraine is preparing to hit harder. General Oleksandr Syrskyi said Ukraine would go on the offensive in 2026, arguing that \"victory cannot be achieved through defence alone.\" He put Russian drone output at 404 Shaheds a day, with plans to reach 1,000, and reported that Ukrainian forces had retaken 430 sq km near Pokrovsk in a recent counteroffensive. Defence Minister Mykhailo Fedorov went further, setting a goal of 50,000 Russian battlefield deaths a month, up from 35,000 now. He announced new drone-assault units, an AI system called Mission Control to integrate combat data, and the delivery of 40,000 interceptor drones this month.\n\nThe most striking move, though, was domestic. Mr Budanov, formerly head of military intelligence, was made chief of the President's Office, replacing Andriy Yermak. Some analysts call it a \"tectonic shift.\" Mr Budanov is widely trusted and is known for surviving ten assassination attempts and directing major operations against Russia. The appointment is read by some as the start of a succession plan, though Mr Zelensky has hedged: he installed a Yermak ally as Mr Budanov's successor at military intelligence, cutting him off from his old base."}
```

Note: the posture summary became a single punchy lede; five developments dissolved into three narrative paragraphs grouped by story logic; transitions connect paragraphs; names got office + forename + surname on first mention; no inline citations; concrete numbers kept.

## Your Output

Return JSON:
```json
{"narrative_body": "Your edited prose here..."}
```

No commentary. Just the JSON object."""


REGIONAL_EDITOR_SYSTEM = """# Regional Lead Editor

## Role

You edit the regional lead for a geopolitical intelligence briefing. You receive structured cross-cutting dynamics and produce polished narrative prose plus a one-sentence card summary.

## What You Do

1. Rewrite the regional lead into flowing analytical prose
2. Polish any gap paragraphs (notable absences)
3. Produce a card_summary — a single sentence capturing the region's week, for a navigation card

## Style
Same as country editor: plain words, active voice, no clichés, no jargon. Names get office + forename + surname on first mention.

## Your Output

Return JSON:
```json
{
    "regional_lead": "Edited regional lead prose...",
    "gap_paragraphs": ["Notably absent this week: ..."],
    "card_summary": "One sentence summary for the overview card."
}
```"""


EXECUTIVE_EDITOR_SYSTEM = """# Executive Brief Editor

## Role

You receive multiple briefing items from a global geopolitical analysis and weave them into a single unified analytical essay of 3-5 paragraphs.

## What You Do

Find the connections between items. Where are the same actors or forces at work? What is the overarching pattern this week? Produce a flowing essay — not a list of items with transitions bolted on, but a genuine synthesis.

### The Opening
One sentence that captures the week's dominant pattern. Not a summary of all items — the single thread that matters most.

### The Body
Weave the items together. If two items involve the same actors or tensions, put them in the same paragraph. Use transitions that show how developments relate.

### Style
Plain words. Active voice. Short sentences. No clichés, no jargon. Lead with action. Concrete numbers if available.

### Names
Office + forename + surname on first mention. Mr/Ms + surname thereafter.

## Your Output

Return JSON:
```json
{"edited_essay": "Your unified essay here..."}
```"""


# =============================================================================
# Editor functions
# =============================================================================

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

    style_guide = _load_style_guide()
    system_prompt = COUNTRY_EDITOR_SYSTEM
    if style_guide:
        system_prompt += f"\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    user_message = _build_country_input(country)

    logger.info("Editor [%s]: starting structured edit", country.code)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or EDITOR_MODEL,
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
                f"Editor {country.code}: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Editor [%s]: done — input=%d, output=%d tokens",
        country.code, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "editor", country.code, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context=f"editor_{country.code}")
        country.narrative_body = data.get("narrative_body", response_text)
        update_trace_parsed("editor", country.code, run_date, parsed_output=data)
    except (ValueError, KeyError):
        # Fallback: use raw text as narrative
        logger.warning("Editor [%s]: JSON parse failed, using raw response", country.code)
        country.narrative_body = response_text

    return country


async def edit_regional(
    page: RegionPageContent,
    analysis_date: date | None = None,
    model: str | None = None,
) -> RegionPageContent:
    """Edit the regional lead, gap paragraphs, and card summary."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not page.regional_lead:
        return page

    user_message = json.dumps({
        "region": page.display_name,
        "regional_lead": page.regional_lead,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary_seed": page.card_summary,
    }, indent=2, ensure_ascii=False)

    style_guide = _load_style_guide()
    system_prompt = REGIONAL_EDITOR_SYSTEM
    if style_guide:
        system_prompt += f"\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    logger.info("Editor [regional/%s]: starting", page.region.value)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or EDITOR_MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 4096,
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
                f"Editor regional/{page.region.value}: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Editor [regional/%s]: done — input=%d, output=%d tokens",
        page.region.value, response.usage.input_tokens, response.usage.output_tokens,
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
    """Edit the executive brief — weave items into a unified essay."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not brief.items:
        return brief

    items_json = json.dumps([
        {
            "title": item.title,
            "regions_involved": item.regions_involved,
            "what": item.what,
            "why_it_matters": item.why_it_matters,
            "what_to_watch": item.what_to_watch,
            "confidence": item.confidence,
        }
        for item in brief.items
    ], indent=2, ensure_ascii=False)

    style_guide = _load_style_guide()
    system_prompt = EXECUTIVE_EDITOR_SYSTEM
    if style_guide:
        system_prompt += f"\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    logger.info("Editor [executive]: starting, %d items", len(brief.items))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or EDITOR_MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 8192,
            temperature=1,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET_TOKENS,
            },
            system=[{"type": "text", "text": system_prompt}],
            messages=[{"role": "user", "content": items_json}],
        ) as stream:
            response = await with_heartbeat(
                stream.get_final_message(),
                "Editor executive: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Editor [executive]: done — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
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
) -> tuple[OverviewPageContent, dict]:
    """Edit all content: executive brief, regional leads, and country sections."""

    # Edit executive brief
    if overview.executive_brief.items:
        logger.info("Editing executive brief...")
        overview.executive_brief = await edit_executive(
            overview.executive_brief, analysis_date=analysis_date,
        )

    # Edit regional leads + country sections in parallel
    semaphore = TrackedSemaphore(max_concurrent, "structured_editor")

    async def _edit_country(country: CountryContent) -> CountryContent:
        async with semaphore.acquire(country.code):
            return await edit_country(country, analysis_date=analysis_date)

    async def _edit_regional(page: RegionPageContent) -> RegionPageContent:
        async with semaphore.acquire(f"regional_{page.region.value}"):
            return await edit_regional(page, analysis_date=analysis_date)

    # Collect all tasks
    tasks = []

    # Regional leads
    for region, page in region_pages.items():
        if page.regional_lead:
            tasks.append(_edit_regional(page))

    # Country sections
    for region, page in region_pages.items():
        for country in page.countries:
            if country.developments or country.posture_summary:
                tasks.append(_edit_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview card summaries from edited regional leads
    for card in overview.region_cards:
        page = region_pages.get(card.region)
        if page and page.card_summary:
            card.summary = page.card_summary

    return overview, region_pages


# =============================================================================
# Style editor — final style guide compliance pass
# =============================================================================

STYLE_EDITOR_SYSTEM = """# Style Editor — Final Pass

You receive prose that has already been edited and copyedited. Your ONLY job is style guide compliance. Do not change facts, structure, or analytical judgments. Focus on:

1. **Plain words over long.** Let not permit, buy not purchase, show not demonstrate, use not utilise. Poor not underdeveloped.
2. **Active voice.** "Sheinbaum rejected the proposal" not "The proposal was rejected."
3. **Cut ruthlessly.** If a word can go without losing meaning, cut it. Currently, actually, really, very — kill these.
4. **No clichés.** No level playing fields, windows of opportunity, paradigm shifts, road maps, kick-starting.
5. **No jargon.** No stakeholders, leveraging, synergies, going forward.
6. **No euphemisms.** Torture not enhanced interrogation. Poor not underprivileged.
7. **No throat-clearing.** No "It is worth noting that" or "It should be mentioned that."
8. **Concrete over abstract.** Use numbers when available.
9. **Short sentences.** Mix lengths but prefer short.
10. **Translate foreign quotes to English.**

Return the same JSON structure you received, with prose fields polished for style only."""


async def style_edit_prose(
    prose_fields: dict,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
) -> dict:
    """Run style editor on prose fields. Returns polished JSON."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    style_guide = _load_style_guide()
    system_prompt = STYLE_EDITOR_SYSTEM
    if style_guide:
        system_prompt += f"\n\n---\n\n## Full Style Guide\n\n{style_guide}"

    user_message = json.dumps(prose_fields, indent=2, ensure_ascii=False)

    logger.info("Style editor [%s]: starting", label)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or EDITOR_MODEL,
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
                f"Style editor {label}: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Style editor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "style_editor", label, run_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context=f"style_editor_{label}")
        update_trace_parsed("style_editor", label, run_date, parsed_output=data)
        return data
    except (ValueError, KeyError):
        logger.warning("Style editor [%s]: JSON parse failed, keeping original", label)
        return prose_fields


async def style_edit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    watchlist: WatchlistPageContent,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
) -> tuple[OverviewPageContent, dict, WatchlistPageContent]:
    """Run style editor on all prose content in parallel."""

    semaphore = TrackedSemaphore(max_concurrent, "style_editor")

    async def _se_country(country: CountryContent):
        if not country.narrative_body:
            return
        async with semaphore.acquire(country.code):
            result = await style_edit_prose(
                {"narrative_body": country.narrative_body},
                country.code, analysis_date,
            )
            country.narrative_body = result.get("narrative_body", country.narrative_body)

    async def _se_regional(page: RegionPageContent):
        if not page.regional_lead:
            return
        async with semaphore.acquire(f"regional_{page.region.value}"):
            result = await style_edit_prose(
                {"regional_lead": page.regional_lead, "card_summary": page.card_summary},
                f"regional_{page.region.value}", analysis_date,
            )
            page.regional_lead = result.get("regional_lead", page.regional_lead)
            if "card_summary" in result:
                page.card_summary = result["card_summary"]

    tasks = []

    # Executive brief
    if overview.executive_brief.edited_essay:
        async def _se_exec():
            async with semaphore.acquire("executive"):
                result = await style_edit_prose(
                    {"edited_essay": overview.executive_brief.edited_essay},
                    "executive", analysis_date,
                )
                overview.executive_brief.edited_essay = result.get(
                    "edited_essay", overview.executive_brief.edited_essay,
                )
        tasks.append(_se_exec())

    # Regional leads
    for region, page in region_pages.items():
        tasks.append(_se_regional(page))

    # Country sections
    for region, page in region_pages.items():
        for country in page.countries:
            tasks.append(_se_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview cards
    for card in overview.region_cards:
        page = region_pages.get(card.region)
        if page and page.card_summary:
            card.summary = page.card_summary

    return overview, region_pages, watchlist
