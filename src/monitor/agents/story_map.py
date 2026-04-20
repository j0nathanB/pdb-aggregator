"""
Story Map Agent: clusters raw search results into distinct stories.

Sits between search expansion and extraction. Takes ~220-320 raw Brave
search results and organizes them into 15-30 story clusters with source
counts, summaries, and representative URLs for selective extraction.

No analytical judgment — maps the media landscape so the country agent
can see what was covered this week at a glance.
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import date

import anthropic
from json_repair import repair_json

from ..rate_limit import anthropic_limiter
from ..collection.brave import BraveNewsResult
from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CountryConfig,
    load_prompt,
)
from .expansion import ExpansionResult
from ..sanitize import extract_json

logger = logging.getLogger(__name__)


# =============================================================================
# Output schema
# =============================================================================

@dataclass
class ArticleRef:
    """A single article reference within a story cluster."""

    title: str
    source: str
    url: str
    date: str = ""


@dataclass
class StoryCluster:
    """A single story identified from search results."""

    story_id: int
    headline: str
    summary: str
    actors_involved: list[str] = field(default_factory=list)
    signal_category_hint: str = "unclear"
    source_count: int = 0
    sources: list[str] = field(default_factory=list)
    date_range: str = ""
    articles: list[ArticleRef] = field(default_factory=list)
    representative_urls: list[str] = field(default_factory=list)


@dataclass
class SingleSourceItem:
    """A story covered by only one outlet."""

    headline: str
    source: str
    url: str
    signal_category_hint: str = "unclear"


@dataclass
class UnassignedItem:
    """A search result the story map agent couldn't place in any bucket."""

    url: str
    description: str = ""
    extra_snippets: list[str] = field(default_factory=list)


@dataclass
class StoryMapOutput:
    """Complete story map for a single country."""

    country: str
    code: str
    analysis_date: str
    search_results_total: int
    stories_identified: int
    off_topic_filtered: int
    stories: list[StoryCluster] = field(default_factory=list)
    single_source_items: list[SingleSourceItem] = field(default_factory=list)
    unassigned: list[UnassignedItem] = field(default_factory=list)
    noise_summary: str = ""
    prompt_dedup: dict = field(default_factory=dict)

    @property
    def all_representative_urls(self) -> list[str]:
        """All URLs selected for extraction, deduplicated."""
        urls: list[str] = []
        seen: set[str] = set()
        for story in self.stories:
            for url in story.representative_urls:
                if url not in seen:
                    seen.add(url)
                    urls.append(url)
        for item in self.single_source_items:
            if item.url and item.url not in seen:
                seen.add(item.url)
                urls.append(item.url)
        return urls

    @property
    def extraction_url_count(self) -> int:
        return len(self.all_representative_urls)


# =============================================================================
# Prompt building
# =============================================================================

# Cap on the formatted search results text.
#
# Sized from real failure data: Poland's failed run was 449K chars → 180K
# input tokens (~2.49 chars/token). With Claude's 200K context limit, a
# ~12K-char system prompt (~5K tokens), and a 24K max_tokens output budget,
# the safe input ceiling is ~165K tokens ≈ ~410K chars. We cap at 350K to
# leave ~30K tokens of headroom.
#
# Distribution from the 2026-03-22 run (29 countries):
#   - At 150K cap: 29/29 truncated (way too tight)
#   - At 350K cap: 12/29 truncated
#   - Median raw size: 306K chars
#
# When exceeded, we drop results from the END of the assembled list. The
# formatter adds in priority order (wire → domestic → actor → vocab) and
# Brave returns each query by relevance, so dropping from the tail first
# discards low-priority vocab matches, then low-relevance actor matches.
MAX_SEARCH_TEXT_CHARS = 350_000

# Per-domain cap on how many results from a single outlet can enter the
# story_map prompt. Applied globally across all source_labels (shared counter).
#
# Rationale (from 2026-04-12 run analysis): individual outlets were producing
# 80-90 near-duplicate URLs per country (aftonbladet.se 93, yle.fi 92). Most
# are off-topic noise the LLM drops anyway. Cap=10 drops <1% of output stories
# best-case while preventing single-domain bloat. Brave returns by relevance,
# so the first N results are the most-relevant N for the query.
PER_DOMAIN_CAP = 10


def _format_search_results(expansion: ExpansionResult) -> tuple[str, dict]:
    """Format raw Brave results into a text block for the LLM.

    Returns (formatted_text, dedup_record) where dedup_record tracks
    per-source-label counts and any URLs deduplicated at this stage.

    If the assembled text exceeds MAX_SEARCH_TEXT_CHARS, results are
    dropped from the tail (lowest-priority sources first) until the text
    fits. The dedup_record reports how many were truncated.
    """
    lines = []
    seen_urls: set[str] = set()
    domain_counts: dict[str, int] = {}
    label_counts: dict[str, dict[str, int]] = {}

    def _add_results(results: list[BraveNewsResult], source_label: str) -> None:
        included = 0
        skipped_urls: list[str] = []
        skipped_by_cap = 0
        for r in results:
            if r.url in seen_urls:
                skipped_urls.append(r.url)
                continue
            # Per-domain cap (shared across labels)
            domain_key = (r.source_domain or "").lower()
            if domain_key.startswith("www."):
                domain_key = domain_key[4:]
            if domain_key and domain_counts.get(domain_key, 0) >= PER_DOMAIN_CAP:
                skipped_by_cap += 1
                continue
            seen_urls.add(r.url)
            if domain_key:
                domain_counts[domain_key] = domain_counts.get(domain_key, 0) + 1
            included += 1
            line = f"- [{source_label}] {r.title}"
            if r.source_domain:
                line += f" | {r.source_domain}"
            if r.age:
                line += f" | {r.age}"
            line += f"\n  URL: {r.url}"
            if r.description:
                line += f"\n  Snippet: {r.description[:300]}"
            if r.extra_snippets:
                for snippet in r.extra_snippets[:3]:
                    line += f"\n  Extra: {snippet[:200]}"
            lines.append(line)
        label_counts[source_label] = {
            "input": len(results),
            "included": included,
            "deduped_at_format": len(skipped_urls),
            "skipped_by_domain_cap": skipped_by_cap,
        }

    _add_results(expansion.triage_wire, "wire")
    _add_results(expansion.triage_domestic, "domestic")
    _add_results(expansion.actor_results, "actor")
    _add_results(expansion.vocab_results, "vocab")

    total_input = sum(lc["input"] for lc in label_counts.values())
    total_deduped = sum(lc["deduped_at_format"] for lc in label_counts.values())
    total_capped = sum(lc["skipped_by_domain_cap"] for lc in label_counts.values())
    if total_capped:
        over_cap_domains = [d for d, n in domain_counts.items() if n >= PER_DOMAIN_CAP]
        logger.info(
            "Story map: per-domain cap (%d) dropped %d results across %d domain(s): %s",
            PER_DOMAIN_CAP, total_capped, len(over_cap_domains),
            ", ".join(sorted(over_cap_domains)[:10]),
        )
    pre_cap_count = len(lines)

    # Apply context-budget cap by dropping from the tail
    truncated = 0
    text = f"Total unique results: {len(lines)}\n\n" + "\n\n".join(lines)
    if len(text) > MAX_SEARCH_TEXT_CHARS:
        while len(text) > MAX_SEARCH_TEXT_CHARS and lines:
            lines.pop()
            truncated += 1
            text = (
                f"Total unique results: {len(lines)} "
                f"(truncated {truncated} from {pre_cap_count} to fit context budget)\n\n"
                + "\n\n".join(lines)
            )
        logger.warning(
            "Story map: truncated %d of %d formatted results to fit context budget "
            "(%d chars > %d cap)",
            truncated, pre_cap_count, len(text) + truncated * 1000, MAX_SEARCH_TEXT_CHARS,
        )
        from ..sanitize import _record_fallback
        _record_fallback("story_map_truncated")

    dedup_record = {
        "raw_input": total_input,
        "unique_in_prompt": len(lines),
        "deduped_at_format": total_deduped,
        "capped_per_domain": total_capped,
        "truncated_for_context": truncated,
        "per_source": label_counts,
    }

    return text, dedup_record


def _format_actor_list(config: CountryConfig) -> str:
    """Format the actor list for the LLM."""
    lines = []
    for actor in config.actors:
        primary = " (PRIMARY)" if actor.primary else ""
        terms = ", ".join(actor.search_terms) if actor.search_terms else ""
        lines.append(f"- {actor.name}: {actor.role}{primary}")
        if terms:
            lines.append(f"  Search terms: {terms}")
    return "\n".join(lines)


def build_story_map_prompt(
    config: CountryConfig,
    expansion: ExpansionResult,
    analysis_date: date,
) -> tuple[str, dict]:
    """Build the user message for the story map agent.

    Returns (prompt_text, dedup_record) where dedup_record tracks
    deduplication stats from formatting search results.
    """
    search_text, dedup_record = _format_search_results(expansion)
    parts = [
        f"## Country: {config.country} ({config.code.upper()})",
        f"## Analysis Date: {analysis_date.isoformat()}",
        "",
        "## ACTOR LIST",
        _format_actor_list(config),
        "",
        "## SEARCH RESULTS",
        search_text,
    ]
    return "\n".join(parts), dedup_record


# =============================================================================
# Tool-use schema (MPM_USE_TOOL_SCHEMA=1)
# =============================================================================
#
# Structured output via an Anthropic tool_use call. The tool's input_schema
# is validated server-side so malformed-JSON failures (~38% of the time
# historically — missing commas, unterminated strings, prose preamble)
# can't reach parse_story_map_response. Feature-flagged behind the same
# MPM_USE_TOOL_SCHEMA env var as the country agent.

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"
RECORD_STORY_MAP_TOOL_NAME = "record_story_map"

_SIGNAL_CATEGORY_HINT_ENUM = [
    "alignment_diplomatic", "security_defense", "economic_tech",
    "institutional", "domestic_regime", "unclear",
]

_ARTICLE_SCHEMA = {
    "type": "object",
    "required": ["title", "source", "url", "date"],
    "properties": {
        "title": {"type": "string"},
        "source": {"type": "string"},
        "url": {"type": "string"},
        "date": {"type": "string", "description": "YYYY-MM-DD or empty string"},
    },
}

_STORY_CLUSTER_SCHEMA = {
    "type": "object",
    "required": [
        "story_id", "headline", "summary", "actors_involved",
        "signal_category_hint", "source_count", "sources",
        "date_range", "articles", "representative_urls",
    ],
    "properties": {
        "story_id": {"type": "integer"},
        "headline": {"type": "string"},
        "summary": {"type": "string"},
        "actors_involved": {"type": "array", "items": {"type": "string"}},
        "signal_category_hint": {
            "type": "string",
            "enum": _SIGNAL_CATEGORY_HINT_ENUM,
        },
        "source_count": {"type": "integer"},
        "sources": {"type": "array", "items": {"type": "string"}},
        "date_range": {"type": "string"},
        "articles": {"type": "array", "items": _ARTICLE_SCHEMA},
        "representative_urls": {"type": "array", "items": {"type": "string"}},
    },
}

_SINGLE_SOURCE_SCHEMA = {
    "type": "object",
    "required": ["headline", "source", "url", "signal_category_hint"],
    "properties": {
        "headline": {"type": "string"},
        "source": {"type": "string"},
        "url": {"type": "string"},
        "signal_category_hint": {
            "type": "string",
            "enum": _SIGNAL_CATEGORY_HINT_ENUM,
        },
    },
}

_UNASSIGNED_SCHEMA = {
    "type": "object",
    "required": ["url", "description", "extra_snippets"],
    "properties": {
        "url": {"type": "string"},
        "description": {"type": "string"},
        "extra_snippets": {"type": "array", "items": {"type": "string"}},
    },
}

RECORD_STORY_MAP_TOOL = {
    "name": RECORD_STORY_MAP_TOOL_NAME,
    "description": (
        "Record the complete clustered story map for this country's week "
        "of news coverage. Call exactly once when clustering is complete. "
        "Provide every field — the schema enforces the structure."
    ),
    "input_schema": {
        "type": "object",
        "required": [
            "country", "analysis_date", "search_results_total",
            "stories_identified", "off_topic_filtered",
            "stories", "single_source_items", "unassigned", "noise_summary",
        ],
        "properties": {
            "country": {"type": "string"},
            "analysis_date": {"type": "string", "description": "YYYY-MM-DD"},
            "search_results_total": {"type": "integer"},
            "stories_identified": {"type": "integer"},
            "off_topic_filtered": {"type": "integer"},
            "stories": {"type": "array", "items": _STORY_CLUSTER_SCHEMA},
            "single_source_items": {"type": "array", "items": _SINGLE_SOURCE_SCHEMA},
            "unassigned": {"type": "array", "items": _UNASSIGNED_SCHEMA},
            "noise_summary": {"type": "string"},
        },
    },
}


def hydrate_story_map(data: dict) -> StoryMapOutput:
    """Build StoryMapOutput from a schema-validated tool_use.input dict.

    The API has already validated the shape, so this is a thin constructor.
    Retains .get() on optional fields as belt-and-suspenders.
    """
    stories = []
    for s in data.get("stories", []):
        articles = [
            ArticleRef(
                title=a.get("title", ""),
                source=a.get("source", ""),
                url=a.get("url", ""),
                date=a.get("date", ""),
            )
            for a in s.get("articles", [])
        ]
        stories.append(StoryCluster(
            story_id=s.get("story_id", 0),
            headline=s.get("headline", ""),
            summary=s.get("summary", ""),
            actors_involved=s.get("actors_involved", []),
            signal_category_hint=s.get("signal_category_hint", "unclear"),
            source_count=s.get("source_count", 0),
            sources=s.get("sources", []),
            date_range=s.get("date_range", ""),
            articles=articles,
            representative_urls=s.get("representative_urls", []),
        ))

    single_source = [
        SingleSourceItem(
            headline=item.get("headline", ""),
            source=item.get("source", ""),
            url=item.get("url", ""),
            signal_category_hint=item.get("signal_category_hint", "unclear"),
        )
        for item in data.get("single_source_items", [])
    ]
    unassigned = [
        UnassignedItem(
            url=item.get("url", ""),
            description=item.get("description", ""),
            extra_snippets=item.get("extra_snippets", []),
        )
        for item in data.get("unassigned", [])
    ]

    return StoryMapOutput(
        country=data.get("country", ""),
        code=data.get("country", ""),  # prompt uses country name in this field
        analysis_date=data.get("analysis_date", ""),
        search_results_total=data.get("search_results_total", 0),
        stories_identified=data.get("stories_identified", 0),
        off_topic_filtered=data.get("off_topic_filtered", 0),
        stories=stories,
        single_source_items=single_source,
        unassigned=unassigned,
        noise_summary=data.get("noise_summary", ""),
    )


# =============================================================================
# Response parsing
# =============================================================================

def parse_story_map_response(response_text: str) -> StoryMapOutput:
    """Parse the story map LLM response into StoryMapOutput.

    Raises json.JSONDecodeError or KeyError on invalid responses.
    """
    try:
        data = extract_json(response_text, context="story_map")
    except ValueError:
        logger.warning("Story map extract_json failed, attempting json_repair")
        data = repair_json(response_text.strip(), return_objects=True)
        if not isinstance(data, dict):
            raise

    stories = []
    for s in data.get("stories", []):
        articles = [
            ArticleRef(
                title=a.get("title", ""),
                source=a.get("source", ""),
                url=a.get("url", ""),
                date=a.get("date", ""),
            )
            for a in s.get("articles", [])
        ]
        stories.append(StoryCluster(
            story_id=s.get("story_id", 0),
            headline=s.get("headline", ""),
            summary=s.get("summary", ""),
            actors_involved=s.get("actors_involved", []),
            signal_category_hint=s.get("signal_category_hint", "unclear"),
            source_count=s.get("source_count", 0),
            sources=s.get("sources", []),
            date_range=s.get("date_range", ""),
            articles=articles,
            representative_urls=s.get("representative_urls", []),
        ))

    single_source = []
    for item in data.get("single_source_items", []):
        single_source.append(SingleSourceItem(
            headline=item.get("headline", ""),
            source=item.get("source", ""),
            url=item.get("url", ""),
            signal_category_hint=item.get("signal_category_hint", "unclear"),
        ))

    unassigned = []
    for item in data.get("unassigned", []):
        unassigned.append(UnassignedItem(
            url=item.get("url", ""),
            description=item.get("description", ""),
            extra_snippets=item.get("extra_snippets", []),
        ))

    return StoryMapOutput(
        country=data.get("country", ""),
        code=data.get("country", ""),  # prompt uses country name in this field
        analysis_date=data.get("analysis_date", ""),
        search_results_total=data.get("search_results_total", 0),
        stories_identified=data.get("stories_identified", 0),
        off_topic_filtered=data.get("off_topic_filtered", 0),
        stories=stories,
        single_source_items=single_source,
        unassigned=unassigned,
        noise_summary=data.get("noise_summary", ""),
    )


# =============================================================================
# Agent
# =============================================================================

async def run_story_map_agent(
    config: CountryConfig,
    expansion: ExpansionResult,
    analysis_date: date,
    model: str | None = None,
) -> StoryMapOutput:
    """Run the story map agent for a single country.

    Args:
        config: The country's configuration.
        expansion: Combined triage + expansion search results.
        analysis_date: The date of analysis (typically the pipeline end_date).
        model: Override the default model.

    Returns:
        StoryMapOutput with clustered stories and representative URLs.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    total_results = expansion.total_count
    if total_results == 0:
        logger.info("Story map %s: no search results — returning empty", config.code)
        return StoryMapOutput(
            country=config.country,
            code=config.code,
            analysis_date=analysis_date.isoformat(),
            search_results_total=0,
            stories_identified=0,
            off_topic_filtered=0,
        )

    system_prompt = load_prompt(
        "agents/story_map_agent",
        COUNTRY=config.country,
        COUNTRY_CODE=config.code.upper(),
        ANALYSIS_DATE=analysis_date.isoformat(),
    )

    user_message, prompt_dedup = build_story_map_prompt(config, expansion, analysis_date)

    logger.info(
        "Story map %s: %d total results (wire=%d, domestic=%d, actor=%d, vocab=%d), "
        "prompt length=%d chars, deduped_at_format=%d",
        config.code, total_results, *expansion.source_counts.values(),
        len(user_message), prompt_dedup["deduped_at_format"],
    )

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    # Use streaming to avoid SDK timeout for large requests
    text_content = ""
    input_tokens = 0
    output_tokens = 0

    stream_kwargs: dict = dict(
        model=model or MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        temperature=1,  # required for extended thinking
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )
    if USE_TOOL_SCHEMA:
        stream_kwargs["tools"] = [RECORD_STORY_MAP_TOOL]

    from ..timing import with_heartbeat
    async with anthropic_limiter():
        async with client.messages.stream(**stream_kwargs) as stream:
            response = await with_heartbeat(
                stream.get_final_message(),
                f"Story map {config.code}: streaming API call",
            )

    tool_input: dict | None = None
    for block in response.content:
        if block.type == "text" and not text_content:
            text_content = block.text
        elif (
            block.type == "tool_use"
            and getattr(block, "name", None) == RECORD_STORY_MAP_TOOL_NAME
        ):
            tool_input = getattr(block, "input", None)

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    logger.info(
        "Story map %s: API response — input=%d, output=%d tokens",
        config.code, input_tokens, output_tokens,
    )

    # Pick the source of truth for the trace: tool_input if present, else text
    if USE_TOOL_SCHEMA and tool_input is not None:
        trace_response_text = json.dumps(tool_input, indent=2, ensure_ascii=False)
    else:
        trace_response_text = text_content

    if not trace_response_text and tool_input is None:
        logger.error("Story map %s: no text or tool_use in LLM response", config.code)
        raise ValueError(f"Story map agent returned no output for {config.code}")

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    save_raw_response(
        "story_map", config.code, analysis_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=trace_response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    if USE_TOOL_SCHEMA and tool_input is not None:
        output = hydrate_story_map(tool_input)
    else:
        output = parse_story_map_response(text_content)

    output.prompt_dedup = prompt_dedup

    # Accounting check
    story_sources = sum(s.source_count for s in output.stories)
    accounted = story_sources + len(output.single_source_items) + output.off_topic_filtered
    unique_in_prompt = prompt_dedup.get("unique_in_prompt", output.search_results_total)
    gap = unique_in_prompt - accounted
    gap_pct = (gap / unique_in_prompt * 100) if unique_in_prompt else 0

    logger.info(
        "Story map %s: %d stories, %d single-source items, %d off-topic filtered, "
        "%d unassigned, %d URLs for extraction, accounting=%d/%d (gap=%d, %.0f%%)",
        config.code, output.stories_identified,
        len(output.single_source_items), output.off_topic_filtered,
        len(output.unassigned), output.extraction_url_count,
        accounted, unique_in_prompt, gap, gap_pct,
    )

    update_trace_parsed("story_map", config.code, analysis_date, parsed_output=output)

    return output
