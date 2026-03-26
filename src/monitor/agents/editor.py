"""
Editor agent: rewrites assembled country sections into style-guide prose.

Sits between assembly (deterministic rendering) and copyediting (mechanical
polish). Receives both the assembled Markdown and the raw analytical JSON
so it can make informed narrative choices. One country section per call,
parallelisable across countries.
"""

import asyncio
import json
import logging
import re
from datetime import date

import anthropic

from ..config import ANTHROPIC_API_KEY, PROJECT_ROOT, THINKING_BUDGET_TOKENS, load_prompt
from ..models import CountryLedger, WeeklyEntry

# Editor uses Opus for narrative quality
EDITOR_MODEL = "claude-opus-4-6-20250826"

logger = logging.getLogger(__name__)

# Style guide loaded once per process
_style_guide: str | None = None


def _load_style_guide() -> str:
    global _style_guide
    if _style_guide is None:
        _style_guide = (PROJECT_ROOT / "docs" / "style_guide.md").read_text()
    return _style_guide


def _build_raw_analysis_block(
    ledger: CountryLedger,
    entry: WeeklyEntry,
) -> str:
    """Serialize the raw analytical output for the editor's context."""
    raw = {
        "country": ledger.country,
        "code": ledger.code,
        "posture_summary": ledger.posture_summary.text,
        "activity_level": entry.activity_level,
        "category_movements": {},
    }

    if entry.category_movements:
        for cat, mov in entry.category_movements.items():
            cat_key = cat.value if hasattr(cat, "value") else str(cat)
            raw["category_movements"][cat_key] = {
                "movement": mov.movement.value if hasattr(mov.movement, "value") else str(mov.movement),
                "prior_assessment": mov.prior_assessment,
                "updated_assessment": mov.updated_assessment,
                "developments": [
                    {
                        "headline": d.headline,
                        "summary": d.summary,
                        "signal_category_relevance": d.signal_category_relevance,
                        "actors_involved": d.actors_involved,
                    }
                    for d in mov.developments
                ],
                "confidence_change": (
                    {
                        "from": mov.confidence_change.from_,
                        "to": mov.confidence_change.to,
                        "reason": mov.confidence_change.reason,
                    }
                    if mov.confidence_change
                    else None
                ),
            }

    if entry.unexpected_developments:
        raw["unexpected_developments"] = [
            {"headline": ud.headline, "assessment": ud.assessment}
            for ud in entry.unexpected_developments
            if ud.headline and ud.headline.lower() not in ("unknown", "")
        ]

    if entry.absence_check:
        raw["absence_check"] = [
            {"expected": a.expected, "significance": a.significance, "occurred": a.occurred}
            for a in entry.absence_check
            if a.significance
        ]

    if entry.structural_claim_checks:
        raw["structural_claim_checks"] = [
            {"claim_ref": s.claim_ref, "status": s.status.value if hasattr(s.status, "value") else str(s.status), "evidence": s.evidence}
            for s in entry.structural_claim_checks
        ]

    return json.dumps(raw, indent=2, default=str)


async def run_editor(
    assembled_section: str,
    ledger: CountryLedger,
    entry: WeeklyEntry,
    model: str | None = None,
) -> str:
    """Run the editor agent on a single country section.

    Args:
        assembled_section: The mechanically rendered Markdown section.
        ledger: The country ledger (for posture summary and metadata).
        entry: The weekly entry (raw analytical output).
        model: Override the default model.

    Returns:
        The edited Markdown section.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not assembled_section.strip():
        return assembled_section

    task_prompt = load_prompt("editor")
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"

    raw_analysis = _build_raw_analysis_block(ledger, entry)
    user_message = (
        "## ASSEMBLED SECTION\n\n"
        f"{assembled_section}\n\n"
        "---\n\n"
        "## RAW ANALYSIS\n\n"
        f"```json\n{raw_analysis}\n```"
    )

    label = f"{ledger.country} ({ledger.code})"
    logger.info("Editor [%s]: starting, input=%d chars", label, len(assembled_section))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    response = await client.messages.create(
        model=model or EDITOR_MODEL,
        max_tokens=THINKING_BUDGET_TOKENS + 8192,
        thinking={
            "type": "enabled",
            "budget_tokens": THINKING_BUDGET_TOKENS,
        },
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts = [
        block.text for block in response.content
        if block.type == "text"
    ]
    result = "\n".join(text_parts)

    logger.info(
        "Editor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    from ..trace import save_trace, extract_thinking, extract_usage
    save_trace(
        "editor", ledger.code.lower(), date.today(),
        system_prompt=system_prompt,
        user_message=user_message,
        response_text=result,
        thinking_text=extract_thinking(response),
        usage=extract_usage(response),
    )

    return result


async def edit_newsletter(
    newsletter: str,
    country_ledgers: dict[str, CountryLedger],
    country_entries: dict[str, WeeklyEntry],
    max_concurrent: int = 5,
) -> str:
    """Edit all country sections in a newsletter in parallel.

    Identifies country sections by ### headings, matches them to ledger/entry
    data, runs the editor on each, and reassembles.
    """
    # Split into segments: (text, country_code_or_none)
    segments = _split_country_sections(newsletter)

    editable = [
        (i, code) for i, (_, code) in enumerate(segments) if code is not None
    ]

    if not editable:
        logger.info("Editor: no country sections found, skipping")
        return newsletter

    logger.info("Editor: %d country sections to edit", len(editable))

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _edit(idx: int, code: str) -> tuple[int, str]:
        async with semaphore:
            section_text = segments[idx][0]
            ledger = country_ledgers.get(code)
            entry = country_entries.get(code)
            if not ledger or not entry:
                logger.warning("Editor [%s]: no ledger/entry data, skipping", code)
                return (idx, section_text)
            try:
                edited = await run_editor(section_text, ledger, entry)
                return (idx, edited)
            except Exception as e:
                logger.warning("Editor [%s] failed, using original: %s", code, e)
                return (idx, section_text)

    tasks = [_edit(idx, code) for idx, code in editable]
    results = await asyncio.gather(*tasks)

    assembled = [text for text, _ in segments]
    for idx, edited_text in results:
        assembled[idx] = edited_text

    return "".join(assembled)


# Country code extraction from flag image URLs
_FLAG_PATTERN = re.compile(r'flagcdn\.com/h24/(\w{2})\.png')


def _split_country_sections(newsletter: str) -> list[tuple[str, str | None]]:
    """Split a newsletter into segments, identifying country sections.

    Returns list of (text, country_code_or_none). Country sections start
    with ### and contain a flag image from which we extract the code.
    """
    # Split by ### country headings (keeping the delimiter)
    parts = re.split(r'(?=\n\n### )', newsletter)

    result: list[tuple[str, str | None]] = []

    for part in parts:
        if not part:
            continue

        # Check if this is a country section
        if part.lstrip().startswith("### ") or part.startswith("\n\n### "):
            flag_match = _FLAG_PATTERN.search(part)
            if flag_match:
                code = flag_match.group(1)
                result.append((part, code))
                continue

        result.append((part, None))

    return result
