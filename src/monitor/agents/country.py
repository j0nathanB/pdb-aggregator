"""
Country agent (deep dive): analyze across five signal categories.

Input: Story map + extracted articles + country dossier + country ledger.
       Falls back to web_search if no story map is provided.
Output: WeeklyEntry (without devils_advocate) + updated signal categories + posture summary.
"""

import logging
import os
from datetime import date, timedelta
from typing import TYPE_CHECKING, Optional

import anthropic

from ..rate_limit import anthropic_limiter
from ..config import (
    ANTHROPIC_API_KEY,
    MODEL,
    THINKING_BUDGET_TOKENS,
    CategoryStatus,
    ClaimStatus,
    CountryConfig,
    Depth,
    Movement,
    SignalCategory,
    load_prompt,
)
from ..models import (
    AbsenceCheck,
    CategoryMovement,
    ConfidenceChange,
    CountryLedger,
    Development,
    PostureSummary,
    SelfCorrection,
    SignalCategoryAssessment,
    StructuralClaimCheck,
    UnexpectedDevelopment,
    WeeklyEntry,
)
from ..sanitize import extract_json, safe_date, safe_enum, safe_int
from ..schema_helpers import pydantic_to_tool_schema

if TYPE_CHECKING:
    from ..collection.extract import ExtractionResult
    from .story_map import StoryMapOutput

logger = logging.getLogger(__name__)


# =============================================================================
# Output structure
# =============================================================================

class CountryAgentOutput:
    """Parsed output from the country agent."""

    def __init__(
        self,
        weekly_entry: WeeklyEntry,
        signal_categories: dict[SignalCategory, SignalCategoryAssessment],
        posture_summary: PostureSummary,
    ):
        self.weekly_entry = weekly_entry
        self.signal_categories = signal_categories
        self.posture_summary = posture_summary


# =============================================================================
# Tool-use schema (MPM_USE_TOOL_SCHEMA=1)
# =============================================================================
#
# Structured output via an Anthropic tool_use call. The tool's input_schema
# is validated server-side before the response is returned to us, so shape
# drift ("unchanged" instead of a ClaimStatus enum value, missing signal
# category, "high" instead of integer confidence) is caught at the API
# boundary rather than surfacing as a parse failure that loses the country.
#
# Feature-flagged behind MPM_USE_TOOL_SCHEMA so we can A/B on real runs
# without a code revert. See dev/country_agent_tool_use_plan.md.

USE_TOOL_SCHEMA = os.getenv("MPM_USE_TOOL_SCHEMA", "0") == "1"
RECORD_TOOL_NAME = "record_country_analysis"


def _build_record_country_schema() -> dict:
    """Compose the top-level tool input_schema from the three output models.

    Hard-codes the five signal-category keys as required properties rather
    than relying on `additionalProperties` — forces the model to address
    every category (a value we want structurally guaranteed).
    """
    return {
        "type": "object",
        "required": [
            "weekly_entry",
            "updated_signal_categories",
            "updated_posture_summary",
        ],
        "properties": {
            "weekly_entry": pydantic_to_tool_schema(WeeklyEntry),
            "updated_signal_categories": {
                "type": "object",
                "required": [c.value for c in SignalCategory],
                "properties": {
                    c.value: pydantic_to_tool_schema(SignalCategoryAssessment)
                    for c in SignalCategory
                },
            },
            "updated_posture_summary": pydantic_to_tool_schema(PostureSummary),
        },
    }


RECORD_COUNTRY_ANALYSIS_TOOL = {
    "name": RECORD_TOOL_NAME,
    "description": (
        "Record the complete weekly deep-dive analysis for this country. "
        "Call exactly once when your analysis is finished. Provide every "
        "field — the schema enforces the structure, so omissions will be "
        "rejected by the API."
    ),
    "input_schema": _build_record_country_schema(),
}


def hydrate_country_output(
    tool_input: dict,
    week_date: date,
    date_range: str,
    ledger: CountryLedger,
) -> CountryAgentOutput:
    """Build CountryAgentOutput from a schema-validated tool_use.input dict.

    The API has already validated the shape against input_schema, so this
    is a thin constructor. We still parse ISO dates and coerce enums to
    Python values, and we retain `.get()` on optional fields as belt-and-
    suspenders against any Anthropic schema-enforcement gap.
    """
    we = tool_input["weekly_entry"]

    # Category movements — all five required by the schema
    category_movements: dict[SignalCategory, CategoryMovement] = {}
    for cat in SignalCategory:
        cm = we["category_movements"].get(cat.value, {})
        developments = [
            Development(**{
                **d,
                "date": safe_date(d.get("date"), week_date, context="dev.date"),
            })
            for d in cm.get("developments", [])
        ]
        conf_change = cm.get("confidence_change")
        if conf_change:
            conf_change = ConfidenceChange(**conf_change)
        category_movements[cat] = CategoryMovement(
            movement=Movement(cm["movement"]),
            developments=developments,
            prior_assessment=cm.get("prior_assessment", ""),
            updated_assessment=cm.get("updated_assessment", ""),
            confidence_change=conf_change,
        )

    unexpected = [
        UnexpectedDevelopment(**{
            **u,
            "date": safe_date(u.get("date"), week_date, context="unexpected.date"),
            "signal_category": SignalCategory(u["signal_category"]),
        })
        for u in we.get("unexpected_developments", [])
    ]
    absence_checks = [
        AbsenceCheck(**{
            **a,
            "signal_category": SignalCategory(a["signal_category"]),
        })
        for a in we.get("absence_check", [])
    ]
    self_corrections = [
        SelfCorrection(**{
            **s,
            "category": SignalCategory(s["category"]),
            "prior_week": safe_date(s.get("prior_week"), week_date, context="sc.prior_week"),
        })
        for s in we.get("self_corrections", [])
    ]
    claim_checks = [
        StructuralClaimCheck(**{
            **c,
            "status": ClaimStatus(c["status"]),
        })
        for c in we.get("structural_claim_checks", [])
    ]

    weekly_entry = WeeklyEntry(
        week=week_date,
        date_range=date_range,
        depth=Depth.DEEP_DIVE,
        activity_level=we.get("activity_level", {"rating": "unknown", "rationale": ""}),
        category_movements=category_movements,
        unexpected_developments=unexpected,
        absence_check=absence_checks,
        self_corrections=self_corrections,
        structural_claim_checks=claim_checks,
        devils_advocate=None,
    )

    # Signal category assessments — all five required by the schema
    updated_assessments: dict[SignalCategory, SignalCategoryAssessment] = {}
    for cat in SignalCategory:
        ua = tool_input["updated_signal_categories"][cat.value]
        updated_assessments[cat] = SignalCategoryAssessment(
            current_assessment=ua["current_assessment"],
            confidence=ua.get("confidence", 3),
            confidence_rationale=ua.get("confidence_rationale", ""),
            key_actors=ua.get("key_actors", []),
            dossier_sections_referenced=ua.get("dossier_sections_referenced", []),
            last_updated=safe_date(ua.get("last_updated"), week_date, context="assessment.last_updated"),
        )

    up = tool_input["updated_posture_summary"]
    posture_summary = PostureSummary(
        as_of=safe_date(up.get("as_of"), week_date, context="posture.as_of"),
        text=up["text"],
        category_status={
            SignalCategory(k): CategoryStatus(v)
            for k, v in up.get("category_status", {}).items()
            if k in {c.value for c in SignalCategory}
        },
        last_deep_dive=safe_date(up.get("last_deep_dive"), week_date, context="posture.last_deep_dive"),
        consecutive_maintenance_weeks=up.get("consecutive_maintenance_weeks", 0),
    )

    return CountryAgentOutput(
        weekly_entry=weekly_entry,
        signal_categories=updated_assessments,
        posture_summary=posture_summary,
    )


# =============================================================================
# System prompt template
# =============================================================================

COUNTRY_AGENT_SYSTEM_PROMPT_TEMPLATE = load_prompt("agents/country_agent")


def _build_system_prompt(config: CountryConfig) -> str:
    """Fill template variables in the system prompt."""
    primary_lang = config.languages.primary

    # Map language codes to readable names for the prompt
    lang_names = {
        "es": "Spanish", "pt": "Portuguese", "fr": "French", "de": "German",
        "ja": "Japanese", "ko": "Korean", "zh": "Chinese", "ar": "Arabic",
        "tr": "Turkish", "uk": "Ukrainian", "pl": "Polish", "cs": "Czech",
        "ro": "Romanian", "et": "Estonian", "lv": "Latvian", "lt": "Lithuanian",
        "fi": "Finnish", "sv": "Swedish", "no": "Norwegian", "it": "Italian",
        "hi": "Hindi", "id": "Indonesian", "en": "English",
    }
    source_language = lang_names.get(primary_lang, primary_lang)

    return load_prompt(
        "agents/country_agent",
        COUNTRY=config.country,
        SOURCE_LANGUAGE=source_language,
    )


# =============================================================================
# Prompt construction
# =============================================================================

def _build_ledger_context(ledger: CountryLedger, max_entries: int = 4) -> str:
    """Build a compact representation of the ledger for prompt injection."""
    lines = []

    # Posture summary
    ps = ledger.posture_summary
    lines.append("## CURRENT POSTURE SUMMARY")
    lines.append(f"As of: {ps.as_of.isoformat()}")
    lines.append(ps.text)
    lines.append("Category status: " + ", ".join(
        f"{c.value}={s.value}" for c, s in ps.category_status.items()
    ))
    if ps.last_deep_dive:
        lines.append(f"Last deep dive: {ps.last_deep_dive.isoformat()}")
    lines.append("")

    # Signal category assessments
    lines.append("## CURRENT SIGNAL CATEGORY ASSESSMENTS")
    for cat, assessment in ledger.signal_categories.items():
        lines.append(f"\n### {cat.value}")
        lines.append(f"Assessment: {assessment.current_assessment}")
        lines.append(f"Confidence: {assessment.confidence}")
        if assessment.confidence_rationale:
            lines.append(f"Rationale: {assessment.confidence_rationale}")
        if assessment.key_actors:
            lines.append(f"Key actors: {', '.join(assessment.key_actors)}")
    lines.append("")

    # Recent weekly entries (most recent first, capped)
    recent = ledger.weekly_entries[-max_entries:] if ledger.weekly_entries else []
    if recent:
        lines.append(f"## RECENT WEEKLY ENTRIES (last {len(recent)})")
        for entry in reversed(recent):
            lines.append(f"\n### Week of {entry.week.isoformat()} ({entry.depth.value})")
            if entry.activity_level:
                lines.append(f"Activity: {entry.activity_level.get('rating', 'unknown')}")
            if entry.category_movements:
                for cat, mov in entry.category_movements.items():
                    if mov.movement != Movement.NONE:
                        lines.append(f"  {cat.value}: {mov.movement.value}")
                        if mov.updated_assessment:
                            lines.append(f"    → {mov.updated_assessment[:200]}")
            # Include devil's advocate challenges from prior deep dives
            if entry.devils_advocate and entry.devils_advocate.challenges:
                lines.append("  Devil's advocate challenges:")
                for challenge in entry.devils_advocate.challenges:
                    lines.append(f"    - {challenge[:200]}")
    elif ledger.consolidated_history:
        lines.append("## CONSOLIDATED HISTORY")
        lines.append(ledger.consolidated_history[:2000])

    # Corrections log
    if ledger.corrections_log:
        lines.append(f"\n## CORRECTIONS LOG ({len(ledger.corrections_log)} entries)")
        for cl_entry in ledger.corrections_log[-5:]:
            lines.append(
                f"- {cl_entry.correction_date}: {cl_entry.category_affected.value} — "
                f"{cl_entry.corrected_to[:150]} (root cause: {cl_entry.root_cause[:100]})"
            )

    # Structural claims to check
    active_claims = [
        c for c in ledger.structural_claim_status
        if c.status != ClaimStatus.FALSIFIED
    ]
    if active_claims:
        lines.append(f"\n## ACTIVE STRUCTURAL CLAIMS ({len(active_claims)} total)")
        # Show claims under pressure first, then sample of confirmed
        priority_claims = [c for c in active_claims if c.status != ClaimStatus.CONFIRMED]
        sample_confirmed = [c for c in active_claims if c.status == ClaimStatus.CONFIRMED][:5]
        for c in priority_claims + sample_confirmed:
            lines.append(f"- [{c.claim_ref}] (§{c.dossier_section}, {c.status.value}): {c.claim_text[:150]}")

    return "\n".join(lines)


def _build_country_prompt(
    config: CountryConfig,
    ledger: CountryLedger,
    dossier_text: str,
    end_date: date,
    allowed_domains: list[str] | None = None,
) -> str:
    start_date = end_date - timedelta(days=6)

    actor_lines = []
    for a in config.actors:
        terms = ", ".join(f'"{t}"' for t in a.search_terms)
        marker = " (PRIMARY)" if a.primary else ""
        actor_lines.append(f"- {a.name} ({a.role}){marker}: search terms: {terms}")
    actors_block = "\n".join(actor_lines)

    # Build source display from allowed_domains list
    domains = allowed_domains or []
    sources_block = "\n".join(f"- {d}" for d in domains) if domains else "- No sources configured"

    blind_spots_block = ""
    if config.blind_spots:
        blind_spots_block = "\nKnown blind spots:\n" + "\n".join(
            f"- {b.domain}: {b.reason} (signal lives in: {b.where_signal_lives})"
            for b in config.blind_spots
        )

    # Build per-category search vocabulary
    qv = config.news_discovery.query_vocabulary
    vocab_sections = {
        "Diplomatic alignment": qv.diplomatic_alignment,
        "Security & defense": qv.security_defense,
        "Economic & tech": qv.economic_tech,
        "Institutional": qv.institutional,
        "Domestic constraints": qv.domestic_constraints,
    }
    vocab_lines = []
    for label, terms in vocab_sections.items():
        if terms:
            vocab_lines.append(f"- **{label}**: {', '.join(terms)}")
    query_vocab_block = "\n".join(vocab_lines) if vocab_lines else ""

    ledger_context = _build_ledger_context(ledger)

    language_note = ""
    lang = config.languages.primary
    if lang and lang != "en":
        language_note = (
            f"\nIMPORTANT: This country's primary language is {lang}. "
            f"Search domestic sources in {lang} for better coverage. "
            f"Translate findings to English in your output."
        )

    return f"""\
Deep-dive analysis for {config.country} ({config.code.upper()}).

Tier: {config.tier.value}
Region: {config.region.value}
Date range: {start_date.isoformat()} to {end_date.isoformat()}

## KEY ACTORS AND INSTITUTIONS
{actors_block}

## WHITELISTED SOURCES

{sources_block}
{blind_spots_block}
{language_note}

## SEARCH VOCABULARY BY CATEGORY

Use these terms to ensure systematic coverage across all five signal categories. \
Run at least one search per category — do not rely on a single topic dominating your results.

{query_vocab_block}

## CURRENT LEDGER STATE

{ledger_context}

--- BEGIN COUNTRY DOSSIER ---

{dossier_text}

--- END COUNTRY DOSSIER ---

Search for developments during {start_date.isoformat()} to {end_date.isoformat()}. \
Use the search vocabulary above to ensure you cover ALL five signal categories systematically — \
do not stop after finding results for one or two categories. Analyze across all five signal \
categories and produce the JSON output as specified in your instructions."""


def _build_story_map_country_prompt(
    config: CountryConfig,
    ledger: CountryLedger,
    dossier_text: str,
    end_date: date,
    story_map: "StoryMapOutput",
    extracted_articles: list["ExtractionResult"],
    gov_findings: str = "",
) -> str:
    """Build country agent prompt with pre-built story map + extracted articles.

    This replaces the web_search-based prompt. The country agent reads the
    story map first (breadth), then extracted articles (depth), then produces
    its analysis.
    """
    start_date = end_date - timedelta(days=6)

    actor_lines = []
    for a in config.actors:
        terms = ", ".join(f'"{t}"' for t in a.search_terms)
        marker = " (PRIMARY)" if a.primary else ""
        actor_lines.append(f"- {a.name} ({a.role}){marker}: search terms: {terms}")
    actors_block = "\n".join(actor_lines)

    blind_spots_block = ""
    if config.blind_spots:
        blind_spots_block = "\nKnown blind spots:\n" + "\n".join(
            f"- {b.domain}: {b.reason} (signal lives in: {b.where_signal_lives})"
            for b in config.blind_spots
        )

    ledger_context = _build_ledger_context(ledger)

    language_note = ""
    lang = config.languages.primary
    if lang and lang != "en":
        language_note = (
            f"\nNote: This country's primary language is {lang}. "
            f"Sources may be in {lang}; translate findings to English in your output."
        )

    # Format story map
    story_map_block = _format_story_map(story_map)

    # Format extracted articles
    articles_block = _format_extracted_articles(extracted_articles)

    # Government findings
    gov_block = ""
    if gov_findings:
        gov_block = f"\n## GOVERNMENT SOURCE FINDINGS (Layer 2)\n\n{gov_findings}\n"

    return f"""\
Deep-dive analysis for {config.country} ({config.code.upper()}).

Tier: {config.tier.value}
Region: {config.region.value}
Date range: {start_date.isoformat()} to {end_date.isoformat()}

## KEY ACTORS AND INSTITUTIONS
{actors_block}
{blind_spots_block}
{language_note}

## CURRENT LEDGER STATE

{ledger_context}

## THIS WEEK'S MEDIA LANDSCAPE (Story Map)

The following story map was produced by clustering {story_map.search_results_total} search \
results from this week's news coverage. It shows {story_map.stories_identified} distinct \
stories ordered by media prominence (source count). {story_map.off_topic_filtered} off-topic \
results were filtered.

Read the story map first to understand the shape of the week, then consult the extracted \
articles below for depth on specific stories.

{story_map_block}

## EXTRACTED ARTICLES

Full text for representative articles from each story cluster. Use these for depth — the \
story map above gives you breadth.

{articles_block}
{gov_block}
--- BEGIN COUNTRY DOSSIER ---

{dossier_text}

--- END COUNTRY DOSSIER ---

Analyze all five signal categories using the story map and extracted articles above. \
The story map is your primary organizing structure — work through the stories and assess \
which signal categories they touch. After completing your assessment, review the story map \
for high-prominence stories (5+ sources) that you did not flag as significant. If the media \
is heavily covering something you assessed as not posture-relevant, note this in your \
activity level rationale — coverage distribution itself can be a domestic_regime signal.

Produce the JSON output as specified in your instructions."""


def _format_story_map(story_map: "StoryMapOutput") -> str:
    """Format story map for inclusion in the country agent prompt."""
    lines = []
    for s in story_map.stories:
        actors = ", ".join(s.actors_involved) if s.actors_involved else "none listed"
        sources = ", ".join(s.sources) if s.sources else "unknown"
        # Include article URLs so the country agent can cite them
        article_lines = ""
        if s.articles:
            refs = [f"  - {a.source}: {a.url}" for a in s.articles if a.url]
            if refs:
                article_lines = "\n**Article URLs:**\n" + "\n".join(refs)
        lines.append(
            f"### Story #{s.story_id}: {s.headline}\n"
            f"**Summary:** {s.summary}\n"
            f"**Actors:** {actors}\n"
            f"**Signal category hint:** {s.signal_category_hint}\n"
            f"**Sources ({s.source_count}):** {sources}"
            f"{article_lines}\n"
            f"**Date range:** {s.date_range}"
        )

    if story_map.single_source_items:
        lines.append("\n### Single-Source Items")
        for item in story_map.single_source_items:
            url_suffix = f" — {item.url}" if item.url else ""
            lines.append(
                f"- {item.headline} ({item.source}{url_suffix}) — {item.signal_category_hint}"
            )

    if story_map.noise_summary:
        lines.append(f"\n**Noise summary:** {story_map.noise_summary}")

    return "\n\n".join(lines)


def _format_extracted_articles(articles: list["ExtractionResult"]) -> str:
    """Format extracted articles for the country agent prompt."""
    if not articles:
        return "No articles were successfully extracted."

    successful = [a for a in articles if a.success and a.text]
    failed = [a for a in articles if not a.success or not a.text]

    lines = []
    for i, article in enumerate(successful, 1):
        title = article.title or "Untitled"
        # Cap article text to avoid overwhelming the context
        text = article.text[:4000]
        if len(article.text) > 4000:
            text += "\n[... truncated]"
        lines.append(
            f"### Article {i}: {title}\n"
            f"**URL:** {article.url}\n"
            f"**Method:** {article.method}\n\n"
            f"{text}"
        )

    if failed:
        lines.append(f"\n*{len(failed)} articles failed extraction (URLs logged).*")

    summary = f"**{len(successful)} articles extracted, {len(failed)} failed.**\n\n"
    return summary + "\n\n---\n\n".join(lines)


# =============================================================================
# Response parsing
# =============================================================================

def _parse_source_tier(val: object) -> int:
    """Coerce LLM source_tier to int. Handles 'tier_2', 'Tier 1', 2, etc."""
    if isinstance(val, int):
        return max(1, min(val, 4))
    s = str(val).lower().replace("tier_", "").replace("tier ", "").strip()
    try:
        return max(1, min(int(s), 4))
    except (ValueError, TypeError):
        return 2


_CONFIDENCE_WORD_MAP = {
    "very high": 5, "very_high": 5,
    "high": 5, "strong": 5,
    "medium-high": 4, "medium_high": 4, "moderately high": 4,
    "medium": 3, "moderate": 3, "mid": 3,
    "medium-low": 2, "medium_low": 2, "moderately low": 2,
    "low": 1, "weak": 1, "very low": 1, "very_low": 1,
}


def _coerce_confidence(val, default: int = 3) -> int:
    """Coerce LLM confidence to int 1-5. Handles 'high'/'medium'/'low', 3, '3'."""
    if isinstance(val, int):
        return max(1, min(val, 5))
    if isinstance(val, str):
        s = val.strip().lower()
        if s in _CONFIDENCE_WORD_MAP:
            return _CONFIDENCE_WORD_MAP[s]
        return safe_int(s, default, min_val=1, max_val=5, context="confidence")
    return default


def parse_country_response(
    response_text: str,
    week_date: date,
    date_range: str,
    ledger: CountryLedger,
) -> CountryAgentOutput:
    """Parse the country agent's JSON response into structured output."""
    data = extract_json(response_text, context=f"country_response")

    # Support both wrapped and unwrapped formats
    entry_data = data.get("weekly_entry", data)

    # Parse category movements (resilient to LLM field name variations)
    raw_movements = entry_data.get("category_movements", {})
    category_movements = {}
    for cat in SignalCategory:
        cat_data = raw_movements.get(cat.value, {})
        if not cat_data:
            # Default to no movement if LLM omitted this category
            category_movements[cat] = CategoryMovement(
                movement=Movement.NONE, developments=[],
                prior_assessment="", updated_assessment="",
            )
            continue

        developments = []
        for d in cat_data.get("developments", []):
            try:
                headline = d.get("headline") or d.get("title") or d.get("summary", "Unknown")
                raw_date = d.get("date")
                parsed_date = date.fromisoformat(raw_date) if isinstance(raw_date, str) else (raw_date or week_date)
                # Build dev dict — model validator handles single→multi source migration
                dev_data = {
                    "headline": headline,
                    "date": parsed_date,
                    "summary": d.get("summary", ""),
                    "actors_involved": d.get("actors_involved", []),
                    "signal_category_relevance": d.get("signal_category_relevance", ""),
                }
                if "sources" in d:
                    dev_data["sources"] = d["sources"]
                else:
                    dev_data["source"] = d.get("source", "unknown")
                    dev_data["source_tier"] = _parse_source_tier(d.get("source_tier", 2))
                    dev_data["source_url"] = d.get("source_url", "")
                developments.append(Development(**dev_data))
            except Exception as e:
                logger.warning("Skipping malformed development in %s: %s", cat.value, e)

        conf_change = None
        if cat_data.get("confidence_change"):
            try:
                conf_change = ConfidenceChange(**cat_data["confidence_change"])
            except Exception:
                pass

        movement = safe_enum(Movement, cat_data.get("movement", "none"), Movement.NONE, context="category_movement")

        try:
            category_movements[cat] = CategoryMovement(
                movement=movement,
                developments=developments,
                prior_assessment=str(cat_data.get("prior_assessment", "") or ""),
                updated_assessment=str(cat_data.get("updated_assessment", "") or ""),
                confidence_change=conf_change,
            )
        except Exception as e:
            logger.warning(
                "Country agent %s: malformed CategoryMovement for %s, using empty: %s",
                ledger.code, cat.value, e,
            )
            category_movements[cat] = CategoryMovement(
                movement=Movement.NONE, developments=developments,
                prior_assessment="", updated_assessment="",
            )

    # Parse unexpected developments (resilient to LLM field name variations)
    unexpected = []
    for u in entry_data.get("unexpected_developments", []):
        try:
            headline = u.get("headline") or u.get("title") or u.get("summary", "Unknown")
            raw_date = u.get("date")
            parsed_date = date.fromisoformat(raw_date) if isinstance(raw_date, str) else (raw_date or week_date)
            sig_cat = safe_enum(SignalCategory, u.get("signal_category", "alignment_diplomatic"), SignalCategory.ALIGNMENT_DIPLOMATIC, context="unexpected_development")
            unexpected.append(UnexpectedDevelopment(
                headline=headline,
                date=parsed_date,
                source=u.get("source", "unknown"),
                source_tier=_parse_source_tier(u.get("source_tier", 2)),
                signal_category=sig_cat,
                assessment=u.get("assessment", ""),
                disposition=u.get("disposition", "logged"),
            ))
        except Exception as e:
            logger.warning("Skipping malformed unexpected development: %s", e)

    # Parse absence checks
    absence_checks = []
    for a in entry_data.get("absence_check", []):
        if isinstance(a, str):
            logger.warning("Skipping string absence_check entry: %s", a[:100])
            continue
        try:
            sig_cat = safe_enum(SignalCategory, a.get("signal_category", "alignment_diplomatic"), SignalCategory.ALIGNMENT_DIPLOMATIC, context="absence_check")
            absence_checks.append(AbsenceCheck(
                expected=a.get("expected", ""),
                signal_category=sig_cat,
                occurred=a.get("occurred", False),
                significance=a.get("significance", ""),
                confidence=a.get("confidence", 2),
            ))
        except Exception as e:
            logger.warning("Skipping malformed absence check: %s", e)

    # Parse self-corrections
    self_corrections = []
    for s in entry_data.get("self_corrections", []):
        try:
            cat = safe_enum(SignalCategory, s.get("category", "alignment_diplomatic"), SignalCategory.ALIGNMENT_DIPLOMATIC, context="self_correction")
            pw = safe_date(s.get("prior_week"), week_date, context="self_correction.prior_week")
            self_corrections.append(SelfCorrection(
                category=cat,
                prior_week=pw,
                original_claim=s.get("original_claim", ""),
                correction=s.get("correction", ""),
                root_cause=s.get("root_cause", ""),
            ))
        except Exception as e:
            logger.warning("Skipping malformed self_correction: %s", e)

    # Parse structural claim checks
    claim_checks = []
    for c in entry_data.get("structural_claim_checks", []):
        try:
            raw_conf = c.get("confidence_in_claim", c.get("confidence", 3))
            claim_checks.append(StructuralClaimCheck(
                claim_ref=c.get("claim_ref", c.get("ref", c.get("id", "unknown"))),
                claim_text=c.get("claim_text", c.get("claim", c.get("text", ""))),
                # LLM sometimes returns e.g. "unchanged"/"maintained" (semantically
                # reasonable but outside the enum) — map to CONFIRMED baseline.
                status=safe_enum(
                    ClaimStatus, c.get("status", "confirmed"),
                    ClaimStatus.CONFIRMED, context="claim_check.status",
                ),
                evidence=c.get("evidence", ""),
                # LLM sometimes returns "high"/"medium"/"low" instead of 1-5.
                confidence_in_claim=_coerce_confidence(raw_conf, default=3),
            ))
        except Exception as e:
            logger.warning("Skipping malformed claim check: %s", e)

    # Build weekly entry (without devils_advocate — added by separate agent)
    weekly_entry = WeeklyEntry(
        week=week_date,
        date_range=date_range,
        depth=Depth.DEEP_DIVE,
        activity_level=entry_data.get("activity_level", {"rating": "unknown", "rationale": "Not provided by agent."}),
        category_movements=category_movements,
        unexpected_developments=unexpected,
        absence_check=absence_checks,
        self_corrections=self_corrections,
        structural_claim_checks=claim_checks,
        devils_advocate=None,  # Populated by devil's advocate agent
    )

    # Parse updated signal category assessments
    # Support both key names
    assessments_data = data.get("updated_signal_categories", data.get("updated_assessments", {}))
    updated_assessments = {}
    for cat in SignalCategory:
        ua = assessments_data.get(cat.value)
        if ua is None:
            # LLM omitted this category — carry forward the prior assessment
            # from the ledger rather than killing the whole country's output.
            # CountryLedger.all_categories_present guarantees every category
            # is present in ledger.signal_categories.
            logger.warning(
                "Country agent %s: response missing signal category %r; "
                "carrying forward prior ledger assessment",
                ledger.code, cat.value,
            )
            updated_assessments[cat] = ledger.signal_categories[cat]
            continue
        try:
            updated_assessments[cat] = SignalCategoryAssessment(
                current_assessment=ua.get("current_assessment", "")
                    or ledger.signal_categories[cat].current_assessment,
                confidence=_coerce_confidence(ua.get("confidence"), default=3),
                confidence_rationale=ua.get("confidence_rationale", ""),
                key_actors=ua.get("key_actors", []),
                dossier_sections_referenced=ua.get("dossier_sections_referenced", []),
                last_updated=safe_date(ua.get("last_updated"), week_date, context="assessment.last_updated"),
            )
        except Exception as e:
            logger.warning(
                "Country agent %s: malformed assessment for %s, carrying forward ledger: %s",
                ledger.code, cat.value, e,
            )
            updated_assessments[cat] = ledger.signal_categories[cat]

    # Parse updated posture summary
    # Support both key names
    up = data.get("updated_posture_summary", data.get("updated_posture", {})) or {}
    category_status = {}
    valid_categories = {c.value for c in SignalCategory}
    for k, v in (up.get("category_status") or {}).items():
        if k not in valid_categories:
            logger.warning("Skipping invalid SignalCategory key %r in posture.category_status", k)
            continue
        category_status[SignalCategory(k)] = safe_enum(CategoryStatus, v, CategoryStatus.ROUTINE, context="posture.category_status")
    try:
        posture_summary = PostureSummary(
            as_of=safe_date(up.get("as_of"), week_date, context="posture.as_of"),
            text=up.get("text") or ledger.posture_summary.text,
            category_status=category_status or dict(ledger.posture_summary.category_status),
            last_deep_dive=safe_date(up.get("last_deep_dive"), week_date, context="posture.last_deep_dive"),
            consecutive_maintenance_weeks=up.get("consecutive_maintenance_weeks", 0),
        )
    except Exception as e:
        logger.warning(
            "Country agent %s: malformed posture_summary, carrying forward ledger: %s",
            ledger.code, e,
        )
        posture_summary = ledger.posture_summary.model_copy(
            update={"as_of": week_date, "last_deep_dive": week_date}
        )

    return CountryAgentOutput(
        weekly_entry=weekly_entry,
        signal_categories=updated_assessments,
        posture_summary=posture_summary,
    )


# =============================================================================
# Main entry point
# =============================================================================

async def run_country_agent(
    config: CountryConfig,
    ledger: CountryLedger,
    end_date: date | None = None,
    allowed_domains: list[str] | None = None,
    story_map: Optional["StoryMapOutput"] = None,
    extracted_articles: Optional[list["ExtractionResult"]] = None,
    gov_findings: str = "",
) -> CountryAgentOutput:
    """
    Run the country desk deep-dive analysis.

    When story_map and extracted_articles are provided, the agent works from
    pre-built content (no web_search). Otherwise falls back to web_search mode.

    Args:
        config: Country configuration.
        ledger: Current country ledger state.
        end_date: End of the analysis window.
        allowed_domains: Domains for web_search tool (fallback mode only).
        story_map: Pre-built story map from the story map agent.
        extracted_articles: Extracted full-text articles for representative URLs.
        gov_findings: Formatted government source findings (Layer 2).
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    end_date = end_date or date.today()
    start_date = end_date - timedelta(days=6)
    date_range = f"{start_date.isoformat()} to {end_date.isoformat()}"

    dossier_text = config.dossier_path.read_text()
    system_prompt = _build_system_prompt(config)

    use_story_map = story_map is not None and story_map.stories_identified > 0

    if use_story_map:
        prompt = _build_story_map_country_prompt(
            config, ledger, dossier_text, end_date,
            story_map=story_map,
            extracted_articles=extracted_articles or [],
            gov_findings=gov_findings,
        )
        logger.info(
            "Country agent %s: starting deep dive (story map mode), "
            "date_range=%s, %d stories, %d extracted articles",
            config.code, date_range,
            story_map.stories_identified,
            len(extracted_articles or []),
        )
    else:
        prompt = _build_country_prompt(
            config, ledger, dossier_text, end_date,
            allowed_domains=allowed_domains,
        )
        logger.info(
            "Country agent %s: starting deep dive (web_search fallback), date_range=%s",
            config.code, date_range,
        )

    logger.debug(
        "Country agent %s: dossier=%d chars, prompt=%d chars",
        config.code, len(dossier_text), len(prompt),
    )
    logger.debug(
        "Country agent %s: ledger has %d weekly entries, posture as_of=%s",
        config.code, len(ledger.weekly_entries),
        ledger.posture_summary.as_of.isoformat(),
    )

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    # Build API call — with or without web_search tool
    api_kwargs: dict = {
        "model": MODEL,
        # max_tokens is the COMBINED ceiling (thinking + visible output). With
        # 16k thinking budget, leave 16k for visible output so the JSON
        # response has room when the model thinks beyond its budget. Prior
        # value (+8192) left only 8k, which truncated cl on the 2026-05-03
        # run: 114k input pushed thinking past 16k, the model used the entire
        # 24k on thinking, emitted empty visible text, and
        # parse_country_response failed with "No JSON object found." Same
        # failure mode story_map already mitigated in `b0404af`.
        "max_tokens": THINKING_BUDGET_TOKENS + 16384,
        "temperature": 1,  # required for extended thinking
        "thinking": {
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        # cache_control here doesn't produce cross-country reuse — each
        # country's system_prompt has {{COUNTRY}} interpolated at the front,
        # so cache keys differ per country (verified 2026-05-03: 0% hit rate
        # on 29/30 country calls). It DOES help on retries: when a country
        # fails and is retried within the 5-min TTL, the second call hits
        # the cached prefix (verified: fi got 355k cache_read tokens across
        # retries on the same run). Phase 4.5 template restructure
        # (dev/backlog.md) is the structural fix for cross-country reuse.
        "system": [{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        "messages": [{"role": "user", "content": prompt}],
        "timeout": 600.0,
    }

    tools: list[dict] = []
    if not use_story_map:
        # Fallback: let the agent search the web itself
        tools.append({
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": config.search.deep_dive_queries_max,
        })
    if USE_TOOL_SCHEMA:
        # Structured-output tool — the API validates input against schema
        tools.append(RECORD_COUNTRY_ANALYSIS_TOOL)
    if tools:
        api_kwargs["tools"] = tools

    from ..timing import with_heartbeat
    async with anthropic_limiter():
        response = await with_heartbeat(
            client.messages.create(**api_kwargs),
            f"Country agent {config.code}: API call",
        )

    # Extract text blocks, tool-use block (if MPM_USE_TOOL_SCHEMA), and log web searches
    block_types = [block.type for block in response.content]
    text_parts = []
    record_tool_input: dict | None = None
    search_log: list[dict] = []
    current_query: str | None = None

    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "tool_use" and getattr(block, "name", None) == RECORD_TOOL_NAME:
            record_tool_input = getattr(block, "input", None)
        elif block.type == "server_tool_use":
            current_query = getattr(block, "input", {}).get("query", "?")
        elif block.type == "web_search_tool_result":
            result_urls = []
            content = getattr(block, "content", [])
            if not isinstance(content, list):
                # WebSearchToolResultError — no results
                search_log.append({
                    "query": current_query,
                    "results_count": 0,
                    "results": [],
                    "error": str(content),
                })
                current_query = None
                continue
            for item in content:
                if getattr(item, "type", None) == "web_search_result":
                    result_urls.append({
                        "title": getattr(item, "title", ""),
                        "url": getattr(item, "url", ""),
                    })
            search_log.append({
                "query": current_query,
                "results_count": len(result_urls),
                "results": result_urls,
            })
            current_query = None

    response_text = "\n".join(text_parts)

    via_tool_use = USE_TOOL_SCHEMA and record_tool_input is not None
    logger.info(
        "Country agent %s: API complete — input=%d, output=%d tokens, stop=%s%s",
        config.code, response.usage.input_tokens, response.usage.output_tokens,
        response.stop_reason,
        " [tool_use]" if via_tool_use else "",
    )
    logger.debug(
        "Country agent %s: block_types=%s, text_length=%d",
        config.code, block_types, len(response_text),
    )
    # Log each web search query and what it returned
    for i, sl in enumerate(search_log, 1):
        logger.info(
            "Country agent %s: search %d/%d — q=%r, %d results",
            config.code, i, len(search_log), sl["query"], sl["results_count"],
        )
        for r in sl["results"]:
            logger.debug(
                "Country agent %s: search %d result — %s (%s)",
                config.code, i, r["title"][:120], r["url"],
            )
    # "Response text very short" is only a warning signal in the free-form
    # JSON path. When tool_use delivered a structured response, empty text
    # is the expected shape — the model put its output in the tool_use
    # block, not the text block.
    if len(response_text) < 100 and not via_tool_use:
        logger.warning("Country agent %s: response text very short: %r", config.code, response_text[:500])

    from ..trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage

    # For trace continuity: if the response came via tool_use, dump its
    # input as pretty JSON so existing trace analyzers keep working.
    if USE_TOOL_SCHEMA and record_tool_input is not None:
        import json as _json
        trace_response_text = _json.dumps(record_tool_input, indent=2, default=str)
    else:
        trace_response_text = response_text

    save_raw_response(
        "country", config.code, end_date,
        system_prompt=system_prompt,
        user_message=prompt,
        response_text=trace_response_text,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
        extra={"search_log": search_log} if search_log else None,
    )

    if USE_TOOL_SCHEMA:
        if record_tool_input is None:
            raise ValueError(
                f"Country agent {config.code}: no {RECORD_TOOL_NAME} tool_use "
                f"block found in response (block types: {block_types})"
            )
        result = hydrate_country_output(record_tool_input, end_date, date_range, ledger)
    else:
        result = parse_country_response(response_text, end_date, date_range, ledger)
    active_cats = [
        c.value for c, m in result.weekly_entry.category_movements.items()
        if m.movement != Movement.NONE
    ]
    logger.info(
        "Country agent %s: parsed — activity=%s, active_categories=%s, %d developments, %d claim_checks",
        config.code,
        result.weekly_entry.activity_level.get("rating", "?") if result.weekly_entry.activity_level else "?",
        active_cats or "none",
        sum(len(m.developments) for m in result.weekly_entry.category_movements.values()),
        len(result.weekly_entry.structural_claim_checks),
    )
    update_trace_parsed("country", config.code, end_date, parsed_output=result)

    return result
