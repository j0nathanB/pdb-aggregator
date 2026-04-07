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
        path = PROJECT_ROOT / "assets" / "prompts" / "style_editor.md"
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


COUNTRY_EDITOR_SYSTEM = """
<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive structured analytical data for one country and produce narrative prose that a thoughtful generalist can absorb quickly.

You are not an analyst. The analyst has done the hard work — assessed posture, scored confidence, identified competing interpretations. You trust the analysis. Your job is to make it read like something worth reading.
</role>

<inputs>
You receive a JSON object with:

- `posture_summary` — the analyst's high-level assessment (often bloated and clause-heavy — rewrite it)
- `activity_level` — object with `rating` (high/moderate/low) and `rationale`
- `category_movements` — per-category objects keyed by signal category (alignment_diplomatic, security_defense, economic_tech, institutional, domestic_regime), each containing:
  - `movement` — significant, minor, or none
  - `prior_assessment` — last week's assessment for this category
  - `updated_assessment` — this week's updated assessment
  - `developments` — array of developments, each with `headline`, `summary`, `actors_involved`, `signal_category_relevance`, `date`, and `sources` (array of `{name, url, tier}`)
  - `confidence_change` — whether confidence shifted this week
- `unexpected_developments` — developments that broke from structural patterns
- `absence_check` — notable absences (expected events that did not occur)
- `other_stories` — minor items for the accordion (do not incorporate into narrative)

Use the full analytical depth — prior_assessment and updated_assessment tell you what changed this week; signal_category_relevance tells you why a development matters analytically; movement ratings tell you where the action is. This depth informs your editorial choices — what to lead with, what deserves emphasis, what connections to draw — but DO NOT add facts or claims not present in the data.
</inputs>

<instructions>
Produce a `narrative_body` — flowing narrative prose. Your output should read as a short essay: a series of paragraphs that follow logically, tell a story, and would suffer if even one sentence were cut.

<opening>
This is the most important sentence. It must seize the reader.

- Lead with the single most important development or tension. Do not try to cover all five analytical dimensions. Pick what matters this week.
- One to two sentences, no more. This is the lede, not a comprehensive summary.
- No throat-clearing. Don't open with "Country X faces increased challenges as..." — just say what happened and what it means.
</opening>

<body>
Dissolve the developments into narrative paragraphs. Do not reproduce them as a list.

- Find the story. The analyst gave you developments across categories. Find the thread that connects them. Which are related? Which are in tension? What is the sequence?
- Group by narrative logic, not by category. If a diplomatic move and a security development are part of the same story, put them in the same paragraph.
- Use transitions. "Even as it negotiates, Ukraine is preparing to hit harder." "The most notable development, though, was domestic." Transitions tell the reader how paragraphs relate.
- Lead each paragraph with the action. What did someone *do*? Not "highlighting corruption concerns" but "exposed a Pemex contractor with billions in government contracts."
- Concrete detail over abstraction. If the analyst provides a number, use it. "430 sq km" is better than "significant territory."
- For categories with movement "none" — mention only if the absence is itself significant. Otherwise skip.
</body>
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
- Do not change analytical judgments. If the analyst says movement was "minor," do not upgrade it.
- Do not add facts, claims, or context not present in the inputs.
- Do not add inline source citations. Sources belong in the Notes accordion only.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
- Do not produce JSX or accordion markup of any kind. No `<Accordion>`, `<Card>`, `<ResponseField>`, `<Expandable>`, or any other component tags. The renderer handles all accordions and structural components — your only output is plain prose paragraphs in the `narrative_body` field. The `other_stories` items are rendered separately by the template; do not echo them into your narrative.
- Do not add commentary outside the edited prose.
</constraints>

<example>
<example_input>
{
  "posture_summary": "Ukraine maintains active diplomatic engagement while operating under timeline pressure...",
  "activity_level": {"rating": "moderate", "rationale": "Significant diplomatic activity at Munich Security Conference..."},
  "category_movements": {
    "alignment_diplomatic": {
      "movement": "significant",
      "prior_assessment": "Ukraine's alignment strategy faces active timeline pressure with US-imposed June deadline...",
      "updated_assessment": "Ukraine continues operating under timeline pressure but is engaging in active high-level diplomacy to shape terms...",
      "developments": [
        {"headline": "Zelensky engages in high-pressure diplomacy with Trump at Munich", "summary": "Trump publicly told him to 'get moving' on peace negotiations. Zelensky urged intensified pressure on Russia and pushed for Patriot missiles and Tomahawks, framing ending the war as Trump's potential legacy achievement.", "actors_involved": ["Volodymyr Zelensky", "Donald Trump"], "sources": [{"name": "Politico", "tier": 2}]},
        {"headline": "Foreign Minister Sybiha conducts extensive bilateral diplomacy at Munich", "summary": "Sybiha held bilateral meetings with counterparts from China, EU, Canada. Invited Wang Yi to visit Ukraine, noting $21 billion in bilateral trade.", "actors_involved": ["Andrii Sybiha", "Wang Yi"], "sources": [{"name": "Anadolu Agency", "tier": 3}]},
        {"headline": "Budanov reportedly discusses territorial withdrawal conditions", "summary": "Reports suggest Budanov has discussed conditions under which Ukraine could withdraw from certain Donetsk region areas while preventing Russian troop entry.", "actors_involved": ["Kyrylo Budanov"], "sources": [{"name": "news-pravda.com", "tier": 3}]}
      ]
    },
    "security_defense": {
      "movement": "minor",
      "developments": [
        {"headline": "Corps reform second stage", "summary": "Each corps now has organic artillery brigades and expanded drone battalions. 74% air defense effectiveness.", "actors_involved": ["Oleksandr Syrskyi"], "sources": [{"name": "Kyiv Independent", "tier": 2}]},
        {"headline": "Fedorov sets 50,000 Russian deaths/month goal", "summary": "Exceeds 30,000-35,000 monthly Russian recruitment. Urged PAC-3 interceptor delivery.", "actors_involved": ["Mykhailo Fedorov"], "sources": [{"name": "Foreign Policy", "tier": 2}]}
      ]
    }
  }
}
</example_input>

<example_output>
{"narrative_body": "Donald Trump told Volodymyr Zelensky to \u201cget moving\u201d on peace talks at the Munich Security Conference, but Ukraine is preparing for negotiations while building up its army for a war that may soon end.\n\nThe American president publicly pressed his Ukrainian counterpart to speed up peace talks. Mr Zelensky fought back, calling for more pressure on Russia and requesting Patriot missiles and Tomahawks. He tried to reframe the confrontation, telling Mr Trump that ending the war could be his \u201clegacy achievement and political victory.\u201d The exchange showed Ukraine\u2019s bind: Washington wants quick talks, but Kyiv wants to shape any deal on its own terms.\n\nEven as he resisted American pressure, Mr Zelensky reached out elsewhere. Andrii Sybiha, the foreign minister, held meetings at Munich with Chinese, EU and Canadian counterparts, discussing peace efforts, security guarantees and sanctions. Most notably, he invited Wang Yi, the Chinese foreign minister, to visit Ukraine, noting that China had become Ukraine\u2019s biggest trading partner with $21 billion in trade.\n\nMeanwhile, Ukraine appears to be preparing for hard talks. Reports suggest that Kyrylo Budanov, head of the president\u2019s office, has discussed with Mr Zelensky\u2019s aides the legal and practical conditions under which Ukraine could withdraw from parts of Donetsk region while preventing Russian troops from entering.\n\nYet even as it plans for peace, Ukraine is building up its military. Oleksandr Syrskyi, the commander-in-chief, announced the \u201csecond stage\u201d of corps reform, with each corps now getting its own artillery brigades and expanded drone battalions. Mykhailo Fedorov, the defence minister, went further, saying one goal was \u201cto kill 50,000 Russians a month,\u201d more than the roughly 30,000-35,000 new troops Russia recruits monthly."}
</example_output>

<example_notes>
The bloated posture summary became a single punchy lede. Developments across two categories dissolved into five narrative paragraphs grouped by story logic: diplomatic pressure, broader outreach, negotiation planning, military buildup. Transitions connect each paragraph. Names got forename + surname + office on first mention. No inline source citations. Concrete numbers kept. No facts added.
</example_notes>
</example>

<output_format>
Return JSON:
{"narrative_body": "Your edited prose here..."}

No commentary. Just the JSON object.
</output_format>"""


REGIONAL_EDITOR_SYSTEM = """
<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive a regional analysis lead — a cross-country assessment synthesising dynamics across multiple countries in one region. Your job is to rewrite it into polished narrative prose that a thoughtful generalist can absorb quickly.

You are not an analyst. The regional analyst has identified cross-cutting patterns, interaction effects, and contradictions across countries. You trust the analysis. Your job is to make it read like something worth reading.

This is NOT a country section. Do not restructure into country-by-country summaries — preserve the cross-cutting framing.
</role>

<inputs>
You receive a JSON object with:

- `regional_lead` — the analyst's condensed overview (use as a starting point, not the whole story)
- `cross_cutting_dynamics` — the FULL analytical detail for each cross-regional pattern, each containing: title, countries_involved, assessment, significance, trend, confidence, weakest_link, evidence_against_linkage, competing_interpretation. USE THIS DEPTH — it gives you the material the condensed `regional_lead` may have compressed.
- `gap_paragraphs` — notable absences to polish
- `card_summary_seed` — starting point for the navigation card summary
</inputs>

<instructions>
Produce three outputs:

<regional_lead_task>
Rewrite the regional lead into 3-5 SUBSTANTIAL paragraphs of flowing narrative prose.

- Lead with the single most important cross-cutting pattern or tension. One to two sentences. No throat-clearing.
- Draw on the full `cross_cutting_dynamics` detail — assessments, significance, competing interpretations, weakest links. Don't just paraphrase the condensed overview.
- Use transitions. "Even as NATO restructures its command, European allies are voicing growing concerns about American reliability."
- Lead each paragraph with the action. What is happening across countries?
- Name the countries involved. Don't say "several allies" when you can say "Poland, Lithuania, and Latvia."
- Concrete detail over abstraction.
</regional_lead_task>

<gap_task>
Tighten the gap paragraphs. Keep the "Notably absent this week:" framing.
</gap_task>

<card_task>
Produce a card_summary — one sentence that captures the region's week. Concrete and specific, not abstract.
</card_task>
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
- Do not change analytical judgments.
- Do not add facts, claims, or context not present in the inputs.
- Do not restructure into country-by-country summaries. Preserve cross-cutting framing.
- Do not add inline source citations.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
</constraints>

<output_format>
Return JSON:
{
    "regional_lead": "3-5 substantial paragraphs of flowing prose...",
    "gap_paragraphs": ["Notably absent this week: ..."],
    "card_summary": "One sentence for the navigation card."
}

No commentary. Just the JSON object.
</output_format>"""


EXECUTIVE_EDITOR_SYSTEM = """
<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive multiple briefing items from a global analysis and weave them into a single unified analytical essay.

You are not an analyst. The executive analyst identified the week's system-level dynamics. You trust the analysis. Your job is to make it read like something worth reading.
</role>

<inputs>
You receive a JSON array of briefing items, each with:

- `title` — the dynamic's name
- `regions_involved` — which regions are affected
- `what` — what happened
- `why_it_matters` — analytical significance
- `what_to_watch` — forward-looking indicators
- `confidence` — analyst's confidence score (1-5)
</inputs>

<instructions>
Weave the items into a unified analytical essay of 3-5 SUBSTANTIAL paragraphs. Each paragraph should develop an idea fully — not compress it into a single sentence.

- Drop the item titles and headings.
- Merge items that make related points.
- Reorder for narrative flow — lead with the most important development.
- Add transitions so the brief reads as a coherent story, not disconnected observations.
- Eliminate redundancy across items.
- If evidence is thin, say so in plain language.
- Find the connections. Where are the same actors or forces at work? What is the overarching pattern this week?
- Produce a genuine synthesis — not a list of items with transitions bolted on, and not a compression of each item into one sentence.

<opening>
One or two sentences that capture the week's dominant pattern. Not a summary of all items — the single thread that matters most. Then develop it: why does this matter? What is the implication the reader should carry forward?
</opening>

<body>
Weave the items together. If two items involve the same actors or tensions, put them in the same paragraph. Use transitions that show how developments relate.

Each paragraph should carry a distinct idea and develop it with concrete detail. Do not compress three items into three sentences in one paragraph — that is summarising, not synthesising. Instead, find the narrative thread: what happened, why it matters, and what it means for what comes next.
</body>
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
- Do not change analytical judgments.
- Do not add facts, claims, or context not present in the inputs.
- Do not add inline source citations.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
</constraints>

<example>
<example_bad>
Established systems are breaking down across regions but being replaced by new systems. Seventeen democratic allies now face domestic political crises — elite splits, constitutional crises, coalition collapse, institutional fights — yet their alliances continue working. Political breakdown at home enables rather than prevents strategic shifts. Alliance machinery has developed its own momentum, independent of whether member governments are stable. Each region manages American pressure differently. Europe coordinates resistance through joint criticism of American policies and parallel defence spending. In the Americas, Canada diversifies defensively while Mexico deepens cooperation. In the Middle East, India, Turkey, and the UAE each diversify partnerships. Rather than global systems, regions are building their own ways to manage great powers. This is clearest in the Gulf, where the Saudi-UAE partnership has collapsed from commercial competition into military confrontation in Yemen. Direct fighting breaks the foundation of regional stability that has held the Middle East together since the 1980s. The breakdown lets other powers reshape the region while forcing Gulf states to choose sides, splitting the system.
</example_bad>

<example_good>
{"edited_essay": "Seventeen democratic allies face domestic political crises at once — elite splits, constitutional standoffs, collapsing coalitions — and yet their alliances keep working as if nothing were wrong. The machinery of co-operation has built up enough momentum to run without stable governments behind it. That sounds reassuring. It is not. Political breakdown at home is not blocking strategic shifts but enabling them, because leaders too weak to govern can still sign treaties and shuffle troops. The real question is what happens when the machinery and the politics pull in opposite directions.\n\nEach region has found its own way to deal with American pressure, and the approaches do not fit together. Europe co-ordinates resistance: joint criticism of American policies, parallel rises in defence spending, a united front that holds even as individual governments wobble. In the Americas, countries go their own way. Canada diversifies its defences. Mexico deepens co-operation with Washington. Neither consults the other. In the Middle East, India, Turkey and the UAE each hedge by seeking new partners, but through different doors — Turkey through diplomacy, the UAE through commerce, India through strategic balancing. No region copies another's model. No model is designed to connect with the rest.\n\nThe Gulf shows where this leads. The Saudi-UAE partnership, the load-bearing wall of Middle Eastern stability since the 1980s, has collapsed. What began as commercial rivalry has escalated into direct military confrontation in Yemen, complete with formal diplomatic complaints. The breakdown opens space for other powers to reshape the region and forces the remaining Gulf states to pick sides. A system that once held the Middle East together now splits it apart."}
</example_good>

<example_notes>
The bad version compresses everything into topic sentences — each idea gets one sentence, then moves on. The good version develops each idea: the opening doesn't just state the paradox but draws out its implication ("That sounds reassuring. It is not."). The regional paragraph doesn't just list approaches but shows why they don't fit together. The Gulf paragraph doesn't just report the collapse but shows the chain of consequences. Every paragraph earns its length.
</example_notes>
</example>

<output_format>
Return JSON:
{"edited_essay": "Your unified essay here..."}

No commentary. Just the JSON object.
</output_format>"""


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

    system_prompt = _build_system_prompt(COUNTRY_EDITOR_SYSTEM)

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

    system_prompt = _build_system_prompt(REGIONAL_EDITOR_SYSTEM)

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

    system_prompt = _build_system_prompt(EXECUTIVE_EDITOR_SYSTEM)

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


WATCHLIST_EDITOR_SYSTEM = """
<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive structured watchlist items — developments the analyst is monitoring but that have not yet crystallised into full dynamics — and produce a short narrative that a reader can scan quickly.
</role>

<inputs>
You receive a JSON array of watchlist items, each with:

- `item` — what is being watched
- `countries` — country codes involved
- `why_it_matters` — analytical significance
- `trigger` — what would escalate this from watch to action
</inputs>

<instructions>
Produce a short narrative of 2-4 paragraphs that weaves the watchlist items into coherent prose.

- Group related items. If two items involve the same countries or tensions, put them together.
- For each item, convey what is being watched, why it matters, and what the trigger is — but in flowing prose, not as a bulleted list.
- Lead with the most consequential item.
- Use transitions between items so the watchlist reads as a coherent scan of the horizon, not disconnected bullet points.
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
- Do not change analytical judgments.
- Do not add facts, claims, or context not present in the inputs.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
</constraints>

<output_format>
Return JSON:
{"edited_narrative": "Your watchlist narrative here..."}

No commentary. Just the JSON object.
</output_format>"""


async def edit_watchlist(
    watchlist: "WatchlistPageContent",
    analysis_date: date | None = None,
    model: str | None = None,
) -> "WatchlistPageContent":
    """Edit watchlist items into a cohesive narrative."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not watchlist.items:
        return watchlist

    items_json = json.dumps([
        {
            "item": w.item,
            "countries": w.countries,
            "why_it_matters": w.why_it_matters,
            "trigger": w.trigger,
        }
        for w in watchlist.items
    ], indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt(WATCHLIST_EDITOR_SYSTEM)

    logger.info("Editor [watchlist]: starting, %d items", len(watchlist.items))

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
            messages=[{"role": "user", "content": items_json}],
        ) as stream:
            response = await with_heartbeat(
                stream.get_final_message(),
                "Editor watchlist: streaming API call",
            )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "Editor [watchlist]: done — input=%d, output=%d tokens",
        response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    run_date = analysis_date or date.today()
    save_raw_response(
        "editor", "watchlist", run_date,
        system_prompt=system_prompt,
        user_message=items_json,
        response_text=response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    try:
        data = extract_json(response_text, context="editor_watchlist")
        watchlist.edited_narrative = data.get("edited_narrative", response_text)
        update_trace_parsed("editor", "watchlist", run_date, parsed_output=data)
    except (ValueError, KeyError):
        logger.warning("Editor [watchlist]: JSON parse failed, using raw response")
        watchlist.edited_narrative = response_text

    return watchlist


# =============================================================================
# Orchestration — edit all content in parallel
# =============================================================================

async def edit_all(
    overview: OverviewPageContent,
    region_pages: dict,
    watchlist: "WatchlistPageContent | None" = None,
    analysis_date: date | None = None,
    max_concurrent: int = 5,
) -> tuple[OverviewPageContent, dict, "WatchlistPageContent | None"]:
    """Edit all content: executive brief, regional leads, country sections, and watchlist."""

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

    # Watchlist
    if watchlist and watchlist.items:
        async def _edit_watchlist():
            async with semaphore.acquire("watchlist"):
                return await edit_watchlist(watchlist, analysis_date=analysis_date)
        tasks.append(_edit_watchlist())

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview card summaries from edited regional leads
    for card in overview.region_cards:
        page = region_pages.get(card.region)
        if page and page.card_summary:
            card.summary = page.card_summary

    return overview, region_pages, watchlist


# =============================================================================
# Style editor — final style guide compliance pass
# =============================================================================

STYLE_EDITOR_SYSTEM = """
<role>
You are a style editor for a weekly geopolitical intelligence briefing. You receive prose that has already been edited and copyedited. Your ONLY job is style guide compliance. Do not change facts, structure, or analytical judgments.
</role>

<inputs>
You receive a JSON object with one or more prose fields (e.g. `narrative_body`, `regional_lead`, `edited_essay`). Each contains polished prose that needs a final style pass.
</inputs>

<instructions>
Apply the style guide to each prose field. Focus on:

1. Plain words over long
2. Active voice
3. Cut ruthlessly — remove words that add no meaning
4. Kill clichés
5. Kill jargon
6. Kill euphemisms
7. Kill throat-clearing
8. Translate foreign quotes to English
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
- If the prose is already clean, return it unchanged.
</constraints>

<output_format>
Return the same JSON structure you received, with prose fields polished. Only modify string values — do not add or remove fields.
</output_format>"""


async def style_edit_prose(
    prose_fields: dict,
    label: str,
    analysis_date: date | None = None,
    model: str | None = None,
) -> dict:
    """Run style editor on prose fields. Returns polished JSON."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    system_prompt = _build_system_prompt(STYLE_EDITOR_SYSTEM)

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
        data = _unwrap_double_json(data)
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
