"""
Copyeditor agent: polishes rendered newsletter sections for style and naming.

Runs after newsletter assembly. Takes each editable section (executive brief,
regional analysis, country section) and returns a copy-edited version with
consistent title/name conventions and Economist-style prose. No analytical
changes — style and clarity only.
"""

import asyncio
import logging
import re
from dataclasses import dataclass

import anthropic

from ..config import ANTHROPIC_API_KEY, PROJECT_ROOT, THINKING_BUDGET_TOKENS, load_prompt

# Style guide loaded once per process
_style_guide: str | None = None


def _load_style_guide() -> str:
    """Load the style guide from docs/style_guide.md."""
    global _style_guide
    if _style_guide is None:
        _style_guide = (PROJECT_ROOT / "docs" / "style_guide.md").read_text()
    return _style_guide

# Copyeditor always uses Opus for highest editorial quality
COPYEDITOR_MODEL = "claude-opus-4-6-20250826"

logger = logging.getLogger(__name__)


# =============================================================================
# Section types
# =============================================================================

@dataclass
class EditableSection:
    """A section of the newsletter that should be copyedited."""

    text: str
    label: str  # For logging: "Mexico", "Executive Brief", "The Americas"
    section_type: str  # "country", "executive", "regional"


# =============================================================================
# Prompt building
# =============================================================================

def build_copyeditor_prompt(section: str, section_type: str) -> str:
    """Build the user message for the copyeditor agent."""
    if section_type == "executive":
        return (
            "Below is the executive brief section of a geopolitical newsletter. "
            "It contains several analytical items separated by ### headings. "
            "Rewrite them into a single cohesive briefing — flowing prose paragraphs "
            "that a senior reader can absorb in one sitting. Weave the items together: "
            "find the connections, eliminate redundancy across items, and add transitions. "
            "Drop the ### item headings entirely. You may restructure freely. "
            "The output should read as one unified analytical essay, not a list of "
            "separate observations. Return only the edited Markdown.\n\n"
            "---\n\n"
            f"{section}"
        )

    type_hint = {
        "country": "This is a country section.",
        "regional": "This is a regional analysis.",
    }.get(section_type, "")

    return (
        f"Edit the following section for style and naming conventions. "
        f"{type_hint} Return only the edited Markdown.\n\n"
        "---\n\n"
        f"{section}"
    )


# =============================================================================
# Single section edit
# =============================================================================

async def run_copyeditor(
    section_text: str,
    label: str,
    section_type: str = "country",
    model: str | None = None,
) -> str:
    """Run the copyeditor agent on a single section.

    Args:
        section_text: The rendered Markdown for the section.
        label: Human-readable label for logging.
        section_type: One of "country", "executive", "regional".
        model: Override the default model.

    Returns:
        The edited Markdown section.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    if not section_text.strip():
        return section_text

    task_prompt = load_prompt("copyeditor", COUNTRY=label)
    style_guide = _load_style_guide()
    system_prompt = f"{task_prompt}\n\n---\n\n## Reference Style Guide\n\n{style_guide}"
    user_message = build_copyeditor_prompt(section_text, section_type)

    logger.info("Copyeditor [%s]: starting, input=%d chars", label, len(section_text))

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    response = await client.messages.create(
        model=model or COPYEDITOR_MODEL,
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
        "Copyeditor [%s]: done — input=%d, output=%d tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    return result


# =============================================================================
# Newsletter splitting
# =============================================================================

# Boilerplate patterns that don't need copyediting
_BOILERPLATE_PATTERNS = [
    r"^\*?No system-level dynamics",
    r"^No significant cross-country dynamics",
    r"^No significant developments",
]


def _is_boilerplate(text: str) -> bool:
    """Check if a section is boilerplate that doesn't need editing."""
    stripped = text.strip()
    if not stripped or len(stripped) < 50:
        return True
    for pattern in _BOILERPLATE_PATTERNS:
        if re.search(pattern, stripped, re.MULTILINE):
            return True
    return False


def _split_newsletter_sections(
    newsletter: str,
) -> list[tuple[str, EditableSection | None]]:
    """Split a newsletter into segments, identifying editable sections.

    Returns a list of (raw_text, editable_section_or_none) tuples.
    Segments without an EditableSection are passed through unchanged.

    Strategy: split by region boundaries (``---\\n\\n## ``), then within
    each region split by ``### `` country headers.
    """
    # Split by --- ## Region boundaries (keeping the delimiter)
    top_parts = re.split(r"(?=---\n\n## )", newsletter)

    result: list[tuple[str, EditableSection | None]] = []

    for part in top_parts:
        if not part:
            continue

        # Check if this is a region section (starts with ---)
        region_match = re.match(r"^---\n\n## (.+?)(?:\n|$)", part)

        if not region_match:
            # This is the preamble (header + executive brief)
            # Send the entire executive brief as one unit so the copyeditor
            # can weave items into a cohesive narrative
            exec_parts = re.split(r"(?=\n\n### )", part)
            header = exec_parts[0]
            exec_body = "".join(exec_parts[1:])
            result.append((header, None))  # Header/metadata
            if exec_body.strip():
                result.append((
                    exec_body,
                    EditableSection(text=exec_body, label="Executive Brief", section_type="executive"),
                ))
            continue

        region_name = region_match.group(1).strip()

        # Watchlist and footer pass through
        if region_name == "Watchlist":
            result.append((part, None))
            continue

        # Split this region into: regional lead + country sections
        inner_parts = re.split(r"(?=\n\n### )", part)
        regional_lead = inner_parts[0]

        # Check if regional lead has substantive content (not boilerplate)
        # The lead is everything after the "---\n\n## Region\n\n" header
        lead_lines = regional_lead.split("\n", 4)
        lead_body = lead_lines[-1] if len(lead_lines) > 3 else ""
        if not _is_boilerplate(lead_body):
            result.append((
                regional_lead,
                EditableSection(text=regional_lead, label=region_name, section_type="regional"),
            ))
        else:
            result.append((regional_lead, None))

        # Process ### country sections
        for cp in inner_parts[1:]:
            name_match = re.match(r"\n\n### (.+?)(?:\n|$)", cp)
            if name_match:
                country_name = name_match.group(1).strip()
                result.append((
                    cp,
                    EditableSection(text=cp, label=country_name, section_type="country"),
                ))
            else:
                result.append((cp, None))

    return result


# =============================================================================
# Full newsletter copyedit
# =============================================================================

async def copyedit_newsletter(
    newsletter: str,
    max_concurrent: int = 5,
) -> str:
    """Copyedit all editable sections in a newsletter in parallel.

    Identifies executive brief items, regional analyses, and country
    sections. Runs the copyeditor on each in parallel and reassembles.
    """
    segments = _split_newsletter_sections(newsletter)

    # Collect editable sections with their indices
    editable = [
        (i, section)
        for i, (_, section) in enumerate(segments)
        if section is not None
    ]

    if not editable:
        logger.info("Copyeditor: no editable sections found, skipping")
        return newsletter

    section_types = {}
    for _, section in editable:
        section_types[section.section_type] = section_types.get(section.section_type, 0) + 1
    logger.info(
        "Copyeditor: %d sections to edit (%s)",
        len(editable),
        ", ".join(f"{count} {stype}" for stype, count in section_types.items()),
    )

    semaphore = asyncio.Semaphore(max_concurrent)

    async def _edit(idx: int, section: EditableSection) -> tuple[int, str]:
        async with semaphore:
            try:
                edited = await run_copyeditor(
                    section.text, section.label, section.section_type,
                )
                return (idx, edited)
            except Exception as e:
                logger.warning("Copyeditor [%s] failed, using original: %s", section.label, e)
                return (idx, section.text)

    tasks = [_edit(idx, section) for idx, section in editable]
    results = await asyncio.gather(*tasks)

    # Reassemble: replace editable sections with edited versions
    assembled = [text for text, _ in segments]
    for idx, edited_text in results:
        assembled[idx] = edited_text

    return "".join(assembled)
