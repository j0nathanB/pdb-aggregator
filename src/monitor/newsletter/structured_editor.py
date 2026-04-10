"""
Structured editor: receives content models, returns edited prose as JSON.

Replaces the regex-split markdown editor. The LLM receives structured
analytical data and returns JSON with prose fields. No markdown I/O.
"""

import asyncio
import json
import logging
import re
from datetime import date

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    load_prompt,
)
from ..rate_limit import anthropic_limiter
from ..sanitize import _record_fallback, extract_json
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
You receive a JSON object with these top-level fields:

- `country` — the country's display name (use this naturally; never echo it as a heading)
- `code` — the 2-letter country code (do not include in output)
- `posture_summary` — the analyst's high-level assessment (often bloated and clause-heavy — rewrite it as your lede if useful)
- `activity_rating` — a single string: "high", "moderate", or "low". Use it to gauge how much to write — do NOT include the literal phrase "Activity Level" anywhere in your prose.
- `developments` — flat list of this week's key developments. Each has `category` (signal-category label), `movement` (significant/minor/none), `text` (the development summary), and `sources` (list of `{name, url}`). This is your primary narrative material.
- `unexpected` — list of `{headline, assessment}` for developments that broke from structural patterns. Weave them in if analytically significant.
- `absences` — list of `{expected, significance}` for notable non-events. Mention only if structurally telling.
- `other_stories` — minor items rendered separately by the template. DO NOT incorporate these into your narrative.
- `raw_analysis` — full per-category analytical context (NESTED). Contains:
  - `activity_level` — `{rating, rationale}` explaining why activity rating was set
  - `category_movements` — per-category objects keyed by `alignment_diplomatic`, `security_defense`, `economic_tech`, `institutional`, `domestic_regime`. Each has `movement`, `prior_assessment`, `updated_assessment`, `developments` (with `headline`, `summary`, `signal_category_relevance`, `actors_involved`), and `confidence_change`.
  - `structural_claim_checks` — pattern verifications

Use the full analytical depth in `raw_analysis.category_movements` — `prior_assessment` vs `updated_assessment` tells you what changed this week; `signal_category_relevance` tells you why a development matters analytically; `movement` ratings tell you where the action is. This depth informs your editorial choices — what to lead with, what deserves emphasis, what connections to draw — but DO NOT add facts or claims not present in the data.
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
- Do not produce markdown formatting — no headings (`### Economic`, `## Section`, `#### Diplomatic`, etc.), no bullet lists, no bold section labels (`**Activity Level:**`, `**Posture:**`). Just plain prose paragraphs separated by blank lines. Group developments by narrative logic, not by signal category. If you need to mark a transition, use a transition sentence ("Even as it fights at home, the government turned outward this week."), not a heading.
- Do not produce JSX or accordion markup of any kind. No `<Accordion>`, `<Card>`, `<ResponseField>`, `<Expandable>`, or any other component tags. The renderer handles all accordions and structural components — your only output is plain prose paragraphs in the `narrative_body` field. The `other_stories` items are rendered separately by the template; do not echo them into your narrative.
- Your output MUST be valid JSON in the form `{"narrative_body": "..."}`. Do NOT echo the input JSON back. Do NOT return the input dict. The `narrative_body` field is required and must contain your edited prose as a single string with `\\n\\n` between paragraphs.
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
You are an editor for a weekly geopolitical intelligence briefing. You receive a regional essay that has already been written by a dedicated writer. Your job is to tighten, sharpen, and polish the prose — not to rewrite it from scratch.

You are not an analyst and not a writer. The writer has already produced a coherent essay with an analytical through-line. You trust the analysis and the structure. Your job is to make every sentence earn its place.
</role>

<inputs>
You receive a JSON object with:

- `regional_lead` — a pre-written essay (4-5 paragraphs) synthesizing the region's week
- `gap_paragraphs` — notable absences to polish
- `card_summary_seed` — starting point for the navigation card summary
</inputs>

<instructions>
Produce three outputs:

<regional_lead_task>
Polish the regional essay. Do NOT restructure or rewrite from scratch. Instead:

- Tighten every sentence. Cut words that add nothing. If you can say it in fewer words, do.
- Sharpen vague language into concrete detail. "Several countries acted" → name them.
- Strengthen transitions between paragraphs.
- Ensure each paragraph leads with action or judgment, not abstraction.
- Kill throat-clearing, hedging, and filler.
- The essay should be 3-5 substantial paragraphs when you are done.
</regional_lead_task>

<gap_task>
Produce ONE polished paragraph in `gap_paragraphs` (always a single-element array, even if the input has multiple gap items — weave them into one coherent paragraph).

- If the input has multiple gap items, find the analytical thread that connects them and merge into one paragraph that names each absence in turn.
- Do NOT begin with "Notably absent this week:", "Missing this week:", or any similar boilerplate prefix. State the absence directly.
- Keep it tight: 2-4 sentences maximum.
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
    "regional_lead": "3-5 substantial paragraphs of polished prose...",
    "gap_paragraphs": ["EU coordination on economic crisis response did not appear this week. ..."],
    "card_summary": "One sentence for the navigation card."
}

The `gap_paragraphs` array MUST contain exactly one element. Do not start the paragraph with "Notably absent" or "Missing this week".

No commentary. Just the JSON object.
</output_format>"""


EXECUTIVE_EDITOR_SYSTEM = """
<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive a global analytical essay that has already been written by a dedicated writer. Your job is to tighten, sharpen, and polish the prose — not to rewrite it from scratch.

You are not an analyst and not a writer. The writer has already produced a coherent essay with an analytical through-line. You trust the analysis and the structure. Your job is to make every sentence earn its place.
</role>

<inputs>
You receive a JSON object with:

- `edited_essay` — a pre-written essay (up to 5 paragraphs) synthesizing the week's global developments
</inputs>

<instructions>
Polish the essay. Do NOT restructure or rewrite from scratch. Instead:

- Tighten every sentence. Cut words that add nothing.
- Sharpen vague language into concrete detail. "Countries acted" → name them and say what they did.
- Strengthen transitions between paragraphs so the essay reads as one argument, not a list.
- Ensure the opening captures the week's dominant pattern in one or two sentences.
- Ensure each paragraph leads with action or judgment, not abstraction, and develops the idea with concrete detail.
- Kill throat-clearing, hedging, and filler.
- The essay should be 3-5 substantial paragraphs when you are done.
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
- Do not add facts, claims, or context not present in the inputs. You may add editorial framing — interpretive turns, rhetorical structure, transitions — that make the analysis land, provided they don't alter the analytical judgment.
- Do not add inline source citations.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
</constraints>

<output_format>
Return JSON:
{"edited_essay": "Your polished essay here..."}

No commentary. Just the JSON object.
</output_format>"""


# =============================================================================
# Editor functions
# =============================================================================

async def _call_editor_once(
    client: anthropic.AsyncAnthropic,
    system_prompt: str,
    user_message: str,
    label: str,
    model: str,
) -> tuple[str, anthropic.types.Message]:
    """Single API call for the country editor. Returns (response_text, response)."""
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model,
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
                f"Editor {label}: streaming API call",
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

    logger.info("Editor [%s]: starting structured edit", country.code)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    response_text, response = await _call_editor_once(
        client, system_prompt, user_message, country.code, use_model,
    )

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

    def _has_narrative(data) -> bool:
        return isinstance(data, dict) and "narrative_body" in data and isinstance(data["narrative_body"], str) and data["narrative_body"].strip()

    parsed = None
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
            response_text, response = await _call_editor_once(
                client, system_prompt, retry_message, f"{country.code}-retry", use_model,
            )
            logger.info(
                "Editor [%s] retry: input=%d, output=%d tokens",
                country.code, response.usage.input_tokens, response.usage.output_tokens,
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

    if not page.regional_lead:
        return page

    input_data = {
        "region": page.display_name,
        "regional_lead": page.regional_lead,
        "gap_paragraphs": page.gap_paragraphs,
        "card_summary_seed": page.card_summary,
    }
    user_message = json.dumps(input_data, indent=2, ensure_ascii=False)

    system_prompt = _build_system_prompt(REGIONAL_EDITOR_SYSTEM)

    logger.info("Editor [regional/%s]: starting", page.region.value)

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
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
    """Edit the executive brief — polish a pre-written essay or weave items into one."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    # If the writer has already produced an essay, send it for polishing
    if brief.edited_essay:
        items_json = json.dumps(
            {"edited_essay": brief.edited_essay},
            indent=2, ensure_ascii=False,
        )
    elif brief.items:
        # Legacy path: weave structured items into an essay
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
    else:
        return brief

    system_prompt = _build_system_prompt(EXECUTIVE_EDITOR_SYSTEM)

    logger.info("Editor [executive]: starting, %d items", len(brief.items))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
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
- Do not add facts, claims, or context not present in the inputs. You may add editorial framing — interpretive turns, rhetorical structure, transitions — that make the analysis land, provided they don't alter the analytical judgment.
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

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
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
    scope: str = "all",
) -> tuple[OverviewPageContent, dict, "WatchlistPageContent | None"]:
    """Edit content. scope: 'all' | 'countries' | 'regional' | 'executive'."""

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

    # Collect all tasks
    tasks = []

    # Regional leads
    if scope in ("all", "regional"):
        for region, page in region_pages.items():
            if page.regional_lead:
                tasks.append(_edit_regional(page))

    # Country sections
    if scope in ("all", "countries"):
        for region, page in region_pages.items():
            for country in page.countries:
                if country.developments or country.posture_summary:
                    tasks.append(_edit_country(country))

    # Watchlist
    if scope in ("all", "countries") and watchlist and watchlist.items:
        async def _edit_watchlist():
            async with semaphore.acquire("watchlist"):
                return await edit_watchlist(watchlist, analysis_date=analysis_date)
        tasks.append(_edit_watchlist())

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview card summaries from edited regional leads
    if scope in ("all", "regional"):
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

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
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
    scope: str = "all",
) -> tuple[OverviewPageContent, dict, WatchlistPageContent]:
    """Run style editor on prose content. scope: 'all' | 'countries' | 'regional' | 'executive'."""

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
            result = await style_edit_prose(
                {"regional_lead": page.regional_lead, "card_summary": page.card_summary},
                f"regional_{page.region.value}", analysis_date,
            )
            page.regional_lead = result.get("regional_lead", page.regional_lead)
            if "card_summary" in result:
                page.card_summary = result["card_summary"]

    tasks = []

    # Executive brief
    if scope in ("all", "executive") and overview.executive_brief.edited_essay:
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
    if scope in ("all", "regional"):
        for region, page in region_pages.items():
            tasks.append(_se_regional(page))

    # Country sections
    if scope in ("all", "countries"):
        for region, page in region_pages.items():
            for country in page.countries:
                tasks.append(_se_country(country))

    if tasks:
        await asyncio.gather(*tasks)

    # Update overview cards
    if scope in ("all", "regional"):
        for card in overview.region_cards:
            page = region_pages.get(card.region)
            if page and page.card_summary:
                card.summary = page.card_summary

    return overview, region_pages, watchlist
