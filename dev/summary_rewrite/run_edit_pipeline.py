#!/usr/bin/env python3
"""
Run regional summary essays through the editor → copyeditor → style editor pipeline.

Reads each regional_summary_*.md, sends through three editing passes,
and writes the result to an 'edited/' subfolder.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# Add project root to path
sys.path.insert(0, str(PROJECT_ROOT))

import anthropic

from src.monitor.config import ANTHROPIC_API_KEY, MODEL, THINKING_BUDGET_TOKENS, load_prompt
from src.monitor.rate_limit import anthropic_limiter
from src.monitor.sanitize import extract_json

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Load style guide once
STYLE_GUIDE_PATH = PROJECT_ROOT / "assets" / "prompts" / "style_editor.md"
STYLE_GUIDE = STYLE_GUIDE_PATH.read_text() if STYLE_GUIDE_PATH.exists() else ""

NAMES_SECTION = """#### names and titles — briefing conventions ####

- First mention: forename + surname, with office as appositive or context (*Andrii Sybiha, the foreign minister*; *Oleksandr Syrskyi, the commander-in-chief*)
- For universally recognised figures (Trump, Zelensky, Putin), forename + surname alone is sufficient on first mention.
- Subsequent mentions: Mr/Ms + surname (*Mr Sybiha*) or the office in lowercase (*the foreign minister*, *the president*)
- Military officers on active duty: retain rank on all mentions (*General Syrskyi*)
- No Mr, Mrs, Miss, Ms or Dr on first mention.
"""

# ---- Editor system prompt (polish mode) ----

EDITOR_SYSTEM = f"""<role>
You are an editor for a weekly geopolitical intelligence briefing. You receive a regional essay that has already been written. Your job is to tighten, sharpen, and polish the prose — not to rewrite it from scratch.
</role>

<instructions>
Polish the essay. Do NOT restructure or rewrite from scratch. Instead:

- Tighten every sentence. Cut words that add nothing.
- Sharpen vague language into concrete detail.
- Strengthen transitions between paragraphs.
- Ensure each paragraph leads with action or judgment, not abstraction.
- Kill throat-clearing, hedging, and filler.
</instructions>

<style>
Plain words. Short words over long. Active voice. Cut ruthlessly.
No clichés. No jargon. No euphemisms. No throat-clearing.
Translate foreign-language quotes into English.
</style>

<constraints>
- Do not change analytical judgments.
- Do not add facts not present in the input.
- Do not produce markdown formatting (headings, bullets, bold) — just plain prose paragraphs.
</constraints>

<output_format>
Return JSON:
{{"regional_lead": "Your polished essay here..."}}
No commentary. Just the JSON object.
</output_format>

<style_guide>
{NAMES_SECTION}
{STYLE_GUIDE}
</style_guide>"""

# ---- Copyeditor system prompt ----

COPYEDITOR_SYSTEM = f"""<role>
You are a copyeditor for a weekly geopolitical intelligence briefing. You receive prose that has already been edited. Your job is mechanical polish only — no substance changes, no restructuring.
</role>

<instructions>
- Names: First mention = forename + surname (with office). Subsequent = Mr/Ms + surname.
- Abbreviations: spell out on first mention with abbreviation in parentheses. Expand all country-specific acronyms.
- Tighten prose: cut clutter, prefer active voice, no jargon.
- Translate foreign-language quotes to English.
- Do not change analytical content or structure.
</instructions>

<output_format>
Return JSON:
{{"regional_lead": "Your copyedited text here..."}}
No commentary. Just the JSON object.
</output_format>

<style_guide>
{NAMES_SECTION}
{STYLE_GUIDE}
</style_guide>"""

# ---- Style editor system prompt ----

STYLE_EDITOR_SYSTEM = f"""<role>
You are a style editor for a weekly geopolitical intelligence briefing. You receive prose that has already been edited and copyedited. Your ONLY job is style guide compliance. Do not change facts, structure, or analytical judgments.
</role>

<instructions>
Apply the style guide strictly:
- Plain words (let not permit, buy not purchase, show not demonstrate)
- Active voice
- Cut unnecessary words (currently, actually, really, very)
- No clichés, no jargon, no euphemisms
- Figures: never start a sentence with a digit
- Foreign names: translate party/institution names
</instructions>

<output_format>
Return JSON:
{{"regional_lead": "Your style-edited text here..."}}
No commentary. Just the JSON object.
</output_format>

<style_guide>
{NAMES_SECTION}
{STYLE_GUIDE}
</style_guide>"""


PROSE_KEY = "regional_lead"  # overridden via CLI for executive summaries


async def call_llm(system_prompt: str, user_message: str, label: str) -> str:
    """Single LLM call, returns the prose field from JSON response."""
    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    async with anthropic_limiter():
        response = await client.messages.create(
            model=MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 8192,
            temperature=1,
            thinking={
                "type": "enabled",
                "budget_tokens": THINKING_BUDGET_TOKENS,
            },
            system=[{"type": "text", "text": system_prompt}],
            messages=[{"role": "user", "content": user_message}],
        )

    text_parts = [b.text for b in response.content if b.type == "text"]
    response_text = "\n".join(text_parts)

    logger.info(
        "%s: %d input, %d output tokens",
        label, response.usage.input_tokens, response.usage.output_tokens,
    )

    try:
        data = extract_json(response_text, context=label)
        return data.get(PROSE_KEY, response_text)
    except (ValueError, KeyError):
        logger.warning("%s: JSON parse failed, using raw response", label)
        return response_text


async def edit_essay(essay: str, label: str) -> str:
    """Run one essay through editor → copyeditor → style editor."""
    user_msg = json.dumps({PROSE_KEY: essay}, ensure_ascii=False)

    # Step 1: Editor
    logger.info("%s: editing...", label)
    edited = await call_llm(EDITOR_SYSTEM, user_msg, f"{label}/editor")

    # Step 2: Copyeditor
    logger.info("%s: copyediting...", label)
    user_msg2 = json.dumps({PROSE_KEY: edited}, ensure_ascii=False)
    copyedited = await call_llm(COPYEDITOR_SYSTEM, user_msg2, f"{label}/copyeditor")

    # Step 3: Style editor
    logger.info("%s: style editing...", label)
    user_msg3 = json.dumps({PROSE_KEY: copyedited}, ensure_ascii=False)
    styled = await call_llm(STYLE_EDITOR_SYSTEM, user_msg3, f"{label}/style_editor")

    return styled


async def process_file(filepath: Path) -> None:
    """Process one regional summary file through the edit pipeline."""
    date_dir = filepath.parent
    edited_dir = date_dir / "edited"
    edited_dir.mkdir(exist_ok=True)

    output_path = edited_dir / filepath.name
    if output_path.exists():
        logger.info("SKIP %s (already exists)", output_path.relative_to(date_dir.parent))
        return

    essay = filepath.read_text().strip()
    label = f"{date_dir.name}/{filepath.stem}"

    result = await edit_essay(essay, label)

    output_path.write_text(result)
    logger.info("DONE %s → %s", filepath.name, output_path.relative_to(date_dir.parent))


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="Run essays through edit pipeline")
    parser.add_argument(
        "--pattern", default="*/regional_summary_*.md",
        help="Glob pattern relative to summary_rewrite/ (default: */regional_summary_*.md)",
    )
    parser.add_argument(
        "--key", default="regional_lead",
        help="JSON key for prose field (default: regional_lead)",
    )
    args = parser.parse_args()

    global PROSE_KEY
    PROSE_KEY = args.key

    # Update system prompts to use the right key
    global EDITOR_SYSTEM, COPYEDITOR_SYSTEM, STYLE_EDITOR_SYSTEM
    EDITOR_SYSTEM = EDITOR_SYSTEM.replace("regional_lead", PROSE_KEY)
    COPYEDITOR_SYSTEM = COPYEDITOR_SYSTEM.replace("regional_lead", PROSE_KEY)
    STYLE_EDITOR_SYSTEM = STYLE_EDITOR_SYSTEM.replace("regional_lead", PROSE_KEY)

    base_dir = Path(__file__).resolve().parent

    files = sorted(base_dir.glob(args.pattern))
    logger.info("Found %d files to edit (key=%s)", len(files), PROSE_KEY)

    # Process with concurrency limit
    sem = asyncio.Semaphore(3)

    async def _limited(f):
        async with sem:
            await process_file(f)

    await asyncio.gather(*[_limited(f) for f in files])

    logger.info("All done!")


if __name__ == "__main__":
    asyncio.run(main())
