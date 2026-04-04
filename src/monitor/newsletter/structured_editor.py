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

You are an editor for a weekly geopolitical intelligence briefing. You receive structured analytical data for one country and produce narrative prose that a thoughtful generalist can absorb quickly.

You are not an analyst. The analyst has done the hard work — assessed posture, scored confidence, identified competing interpretations. You trust the analysis. Your job is to make it read like something worth reading.

## Your Inputs

JSON with:
- `posture_summary` — the analyst's high-level assessment (often bloated and clause-heavy — rewrite it)
- `activity_rating` — high, moderate, or low
- `developments` — categorised developments with movement ratings (significant/minor/none)
- `unexpected` — unexpected developments
- `absences` — notable absences
- `other_stories` — minor items (do not incorporate into narrative)
- `raw_analysis` — full analytical depth per category: `category_movements` with prior_assessment, updated_assessment, per-development detail (headline, summary, actors_involved, signal_category_relevance), confidence_change, and structural_claim_checks. USE THIS DEPTH because it gives you the material the condensed developments may have compressed and it informs your editorial choices — what to lead with, what deserves emphasis, what connections to draw — but DO NOT add facts or claims.

## What You Do

Produce a `narrative_body` — you transform the JSON content into flowing narrative prose. Your output should read as a short essay — a series of paragraphs that follow logically, tell a story, and would suffer if even one sentence were cut.

### The Opening

This is the most important sentence. It must seize the reader.

- Lead with the single most important development or tension. Do not try to cover all five analytical dimensions. Pick what matters this week.
- One to two sentences, no more. This is the lede, not a comprehensive summary.
- No throat-clearing. Don't open with "Country X faces increased challenges as..." — just say what happened and what it means.

### The Body

Dissolve the developments into narrative paragraphs. Do not reproduce them as a list. Instead:

- **Find the story.** The analyst gave you a set of developments across categories. Your job is to find the thread that connects them and present them as a coherent narrative. Which developments are related? Which are in tension? What is the sequence of events?
- **Group by narrative logic, not by category.** The analyst's categories (diplomatic, security, domestic, etc.) are an analytical framework, not a reading structure. If a diplomatic move and a security development, for example, are part of the same story, put them in the same paragraph.
- **Use transitions.** "Even as it negotiates, Ukraine is preparing to hit harder." "The most notable development, though, was domestic." Transitions tell the reader how paragraphs relate.
- **Lead each paragraph with the action.** What did someone *do*? Not "highlighting corruption concerns" but "exposed a Pemex contractor with billions in government contracts."
- **Concrete detail over abstraction.** If the analyst provides a number, use it. "430 sq km" is better than "significant territory."
- For categories with movement "none" — mention only if the absence of change is itself significant. Otherwise skip.

### Names and Titles

- First mention: forename + surname, office (*Volodymyr Zelenskyy, President of Ukraine*, *Mykhailo Fedorov, Minister of Defence*)
- Subsequent: Mr/Ms + surname (*Mr Zelensky*) or the office (*the president*, lowercase)
- Military officers on active duty: retain rank on all mentions (*General Syrskyi*)
- No Mr, Mrs, Miss, Ms or Dr on first mention — use the office.

### Style

**Plain words.** Short words over long. *Let* not *permit*, *buy* not *purchase*, *show* not *demonstrate*. Poor countries are *poor*, not *underdeveloped*.

**Active voice.** "Sheinbaum rejected the proposal" not "The proposal was rejected by Sheinbaum."

**Cut ruthlessly.** If you can cut a word without losing meaning, cut it. *Currently*, *actually*, *really*, *very*, *significantly* — these usually serve no purpose.

**No clichés.** No *level playing fields*, *windows of opportunity*, *paradigm shifts*, *road maps*. No *it remains to be seen* or *only time will tell*.

**No jargon.** No *stakeholders*, *leveraging*, *synergies*, *going forward*. If a thoughtful generalist wouldn't use it in conversation, don't use it.

**No euphemisms.** *Torture* not *enhanced interrogation*. *Poor* not *underprivileged*.

**No throat-clearing.** No "It is worth noting that" or "It should be mentioned that." Just state the fact.

**Translate foreign-language quotes into English.**

## What You Must Not Do

- Do not change analytical judgments. If the analyst says movement was "minor," do not upgrade it.
- Do not add facts, claims, or context not present in the inputs.
- Do not add inline source citations. Sources belong in the Notes accordion only.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
- Do not add commentary outside the edited prose.

## Example

Input (trimmed — your actual input will have all five categories and full raw_analysis):
```json
{
  "country": "Ukraine",
  "posture_summary": "Ukraine's alignment posture shifted significantly this week as President Zelensky delivered harsh criticism of European unity at Davos while simultaneously engaging in diplomatic outreach with the United States...",
  "activity_rating": "moderate",
  "developments": [
    {"category": "Diplomatic", "movement": "significant", "text": "Zelensky attended Munich Security Conference where Trump publicly told him to 'get moving' on peace negotiations. Zelensky urged intensified pressure on Russia and pushed for Patriot missiles and Tomahawks, framing ending the war as Trump's potential legacy achievement."},
    {"category": "Security", "movement": "minor", "text": "Commander-in-Chief Syrskyi announced the 'second stage' of corps reform, with each corps now having organic artillery brigades and unmanned systems battalions expanded to regiment size. Reported 74% air defense effectiveness."}
  ],
  "raw_analysis": {
    "category_movements": {
      "alignment_diplomatic": {
        "movement": "significant",
        "prior_assessment": "Ukraine's alignment strategy faces active timeline pressure with US-imposed June deadline...",
        "updated_assessment": "Ukraine continues operating under timeline pressure but is engaging in active high-level diplomacy to shape terms...",
        "developments": [
          {"headline": "Zelensky engages in high-pressure diplomacy with Trump at Munich", "summary": "...", "actors_involved": ["Volodymyr Zelensky", "Donald Trump"]},
          {"headline": "Foreign Minister Sybiha conducts extensive bilateral diplomacy at Munich", "summary": "Sybiha invited Chinese Foreign Minister Wang Yi to visit Ukraine, noting $21 billion in bilateral trade.", "actors_involved": ["Andrii Sybiha", "Wang Yi"]},
          {"headline": "Budanov reportedly discusses territorial withdrawal conditions", "summary": "Reports suggest Budanov has discussed conditions under which Ukraine could withdraw from certain Donetsk region areas.", "actors_involved": ["Kyrylo Budanov"]}
        ]
      },
      "security_defense": {
        "movement": "minor",
        "developments": [
          {"headline": "Corps reform second stage", "summary": "Each corps now has organic artillery brigades and expanded drone battalions.", "actors_involved": ["Oleksandr Syrskyi"]},
          {"headline": "Fedorov sets 50,000 Russian deaths/month goal", "summary": "Exceeds 30,000-35,000 monthly Russian recruitment. Urged PAC-3 interceptor delivery.", "actors_involved": ["Mykhailo Fedorov"]}
        ]
      }
    }
  }
}
```

Output:
```json
{"narrative_body": "Donald Trump told Volodymyr Zelensky to “get moving” on peace talks at the Munich Security Conference, but Ukraine is preparing for negotiations while building up its army for a war that may soon end. \n\nThe American president publicly pressed his Ukrainian counterpart to speed up peace talks. Mr Zelensky fought back, calling for more pressure on Russia and requesting Patriot missiles and Tomahawks. He tried to reframe the confrontation, telling Mr Trump that ending the war could be his “legacy achievement and political victory.” The exchange showed Ukraine’s bind: Washington wants quick talks, but Kyiv wants to shape any deal on its own terms. \n\nEven as he resisted American pressure, Mr Zelensky reached out elsewhere. Andrii Sybiha, the foreign minister, held meetings at Munich with Chinese, EU and Canadian counterparts, discussing peace efforts, security guarantees and sanctions. Most notably, he invited Wang Yi, the Chinese foreign minister, to visit Ukraine, noting that China had become Ukraine’s biggest trading partner with $21 billion in trade. The outreach showed Ukraine’s effort to involve Beijing, which has sway with Russia, in any peace process. \n\nMeanwhile, Ukraine appears to be preparing for hard talks. Reports suggest that Kyrylo Budanov, head of the president’s office, has discussed with Mr Zelensky’s aides the legal and practical conditions under which Ukraine could withdraw from parts of Donetsk region while preventing Russian troops from entering. Mr Budanov is described as “a skilled negotiator and proponent of peace,” pointing to his likely role in any talks. \n\nYet even as it plans for peace, Ukraine is building up its military. Oleksandr Syrskyi, the commander-in-chief, announced the “second stage” of corps reform, with each corps now getting its own artillery brigades and expanded drone battalions. He reported 74% air defence effectiveness and said the reforms had increased enemy losses. Mykhailo Fedorov, the defence minister, went further, saying one goal was “to kill 50,000 Russians a month,” more than the roughly 30,000-35,000 new troops Russia recruits monthly. His aim, he said, was to “make the cost of war for Russia unbearable.” \n\nUkraine’s economy continues to function. Yuliia Svyrydenko, the prime minister, announced that the IMF had agreed to ease conditions for a new $8.2 billion loan, while the National Bank reported that foreign reserves had grown 6.4% to $43.3 billion in December. The government also hinted at changes to draft policy, with ruling party politicians acknowledging widespread draft evasion and suggesting that procedures might change to make life “more difficult for those avoiding recruitment.”"}
```

Note what changed: the bloated posture summary became a single punchy sentence; five category-labelled developments dissolved into three narrative paragraphs grouped by story logic (diplomacy, military escalation, domestic reshuffle); transitions connect the paragraphs; all names (except Trump and Zelensky's) got forename + surname + office on first mention; no inline source citations; concrete numbers kept; no facts added.

## Your Output

Return JSON:
```json
{"narrative_body": "Your edited prose here..."}
```

No commentary. Just the JSON object."""


REGIONAL_EDITOR_SYSTEM = """# Regional Lead Editor

## Role

You edit the regional lead for a geopolitical intelligence briefing. You receive a condensed regional overview PLUS the full cross-cutting dynamics from the analyst. Your job is to produce rich, detailed narrative prose — not a summary of a summary.

## Your Inputs

- `regional_lead` — the analyst's condensed overview (use as a starting point, not the whole story)
- `cross_cutting_dynamics` — the FULL analytical detail for each cross-regional pattern. Each has: title, countries involved, assessment, significance, trend, confidence, weakest link, evidence against linkage, competing interpretation. USE THIS DEPTH in your prose.
- `gap_paragraphs` — notable absences to polish
- `card_summary_seed` — starting point for the navigation card summary

## What You Do

1. Rewrite the regional lead into flowing analytical prose of 3-5 SUBSTANTIAL paragraphs. Draw on the cross_cutting_dynamics for concrete detail — assessments, significance, competing interpretations, weakest links. Do NOT just summarize the summary. Expand into rich narrative.
2. Polish any gap paragraphs (notable absences)
3. Produce a card_summary — a single sentence for a navigation card

### Style
Plain words. Active voice. Cut ruthlessly. No clichés, jargon, euphemisms, or throat-clearing. Lead with action. Names get office + forename + surname on first mention. No inline source citations.

## Your Output

Return JSON:
```json
{
    "regional_lead": "Edited regional lead prose — 3-5 substantial paragraphs...",
    "gap_paragraphs": ["Notably absent this week: ..."],
    "card_summary": "One sentence summary for the overview card."
}
```"""


EXECUTIVE_EDITOR_SYSTEM = """# Executive Brief Editor

## Role

You receive multiple briefing items from a global geopolitical analysis and weave them into a single unified analytical essay of 3-5 paragraphs.

## What You Do

- Drop the item titles and headings.
- Merge items that make related points.
- Reorder for narrative flow — lead with the most important development.
- Add transitions so the brief reads as a coherent story, not disconnected observations.
- Eliminate redundancy across items.
- If evidence is thin, say so in plain language.
- The result should be 3-5 paragraphs of flowing prose.

Find the connections between items. Where are the same actors or forces at work? What is the overarching pattern this week? Produce a genuine synthesis — not a list of items with transitions bolted on.

### The Opening
One sentence that captures the week's dominant pattern. Not a summary of all items — the single thread that matters most.

### The Body
Weave the items together. If two items involve the same actors or tensions, put them in the same paragraph. Use transitions that show how developments relate.

### Style
Plain words. Active voice. Short sentences. No clichés, no jargon. Lead with action. Concrete numbers if available. No inline source citations.

### Names
Office + forename + surname on first mention. Mr/Ms + surname thereafter.

### Worked Example

**BAD** (jargon-heavy, abstract, repetitive):

> Allied countries are developing fundamentally incompatible strategies for managing alliance burden-sharing and strategic commitments, fragmenting traditional coordination mechanisms along regional lines. Czech Republic explicitly rejected NATO 3.5% spending targets while Romania secured €16.6 billion in EU defense funding and Finland targets 3% GDP by 2029. This represents structural evolution of alliance systems beyond traditional coordination mechanisms — when allies cannot agree on burden-sharing fundamentals or strategic priorities, the alliance becomes a framework for managing disagreement rather than coordinating action.

**GOOD** (concrete, sequential, readable):

> Allied countries are splitting over the basics of burden-sharing, and the splits are hardening along regional lines.
>
> In Europe, the Czech Republic has rejected NATO's 3.5% spending target outright, while Romania secured €16.6 billion in EU defence funding and Finland aims for 3% of GDP by 2029. France, Germany and Spain are each articulating versions of strategic autonomy — separately, and without American participation. They agree on the direction but not the details, and Washington is not in the room.
>
> In Asia, the pressures point in opposite directions. Japan is deepening its operational planning for a Taiwan contingency. South Korea is pursuing what it calls a 'full-scale restoration' of relations with China. Both are responding to American unreliability, but their answers are incompatible.

Notice: short sentences, concrete facts first, plain language, regional grouping with narrative flow, no jargon like 'institutional logic' or 'strategic incoherence'. Say what is happening, who is doing it, why it matters, and stop.

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

    input_data = {
        "region": page.display_name,
        "regional_lead": page.regional_lead,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary_seed": page.card_summary,
    }
    # Include full cross-cutting dynamics for editorial depth
    if page.raw_dynamics:
        input_data["cross_cutting_dynamics"] = page.raw_dynamics
    user_message = json.dumps(input_data, indent=2, ensure_ascii=False)

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
            update_trace_parsed("style_editor", label, run_date, parsed_output=result)
            return result
        logger.warning("Style editor [%s]: empty response, keeping original", label)
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
