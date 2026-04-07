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

# Cap on the formatted search results text. ~150K chars ≈ 60K input tokens,
# leaving plenty of room for system prompt + thinking budget + output.
# When exceeded, we drop results from the END of the assembled list. The
# formatter adds in priority order (wire → domestic → actor → vocab) and
# Brave returns each query by relevance, so dropping from the end first
# discards low-priority vocab matches, then low-relevance actor matches.
MAX_SEARCH_TEXT_CHARS = 150_000


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
    label_counts: dict[str, dict[str, int]] = {}

    def _add_results(results: list[BraveNewsResult], source_label: str) -> None:
        included = 0
        skipped_urls: list[str] = []
        for r in results:
            if r.url in seen_urls:
                skipped_urls.append(r.url)
                continue
            seen_urls.add(r.url)
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
        }

    _add_results(expansion.triage_wire, "wire")
    _add_results(expansion.triage_domestic, "domestic")
    _add_results(expansion.actor_results, "actor")
    _add_results(expansion.vocab_results, "vocab")

    total_input = sum(lc["input"] for lc in label_counts.values())
    total_deduped = sum(lc["deduped_at_format"] for lc in label_counts.values())
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
        "story_map_agent",
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

    from ..timing import with_heartbeat
    async with anthropic_limiter():
        async with client.messages.stream(
            model=model or MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 8192,
            temperature=1,  # required for extended thinking
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET_TOKENS,
            },
            system=[{"type": "text", "text": system_prompt}],
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            response = await with_heartbeat(
                stream.get_final_message(),
                f"Story map {config.code}: streaming API call",
            )

    for block in response.content:
        if block.type == "text":
            text_content = block.text
            break

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    logger.info(
        "Story map %s: API response — input=%d, output=%d tokens",
        config.code, input_tokens, output_tokens,
    )

    if not text_content:
        logger.error("Story map %s: no text in LLM response", config.code)
        raise ValueError(f"Story map agent returned no text for {config.code}")

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    save_raw_response(
        "story_map", config.code, analysis_date,
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=text_content,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

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
