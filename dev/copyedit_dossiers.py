#!/usr/bin/env python3
"""Phase 2: LLM-based copyediting of country dossier MDX files.

Sends each dossier section to Claude for prose copyediting using the
Economist style guide. Also generates titles and executive summaries
for dossiers that lack them.

Usage:
    python dev/copyedit_dossiers.py --dry-run          # preview what would be sent
    python dev/copyedit_dossiers.py latvia              # single file
    python dev/copyedit_dossiers.py                     # all dossiers
    python dev/copyedit_dossiers.py --title-only        # only generate titles/summaries
    python dev/copyedit_dossiers.py --skip-titles       # only copyedit sections
"""

import asyncio
import os
import re
import sys
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOSSIERS_DIR = PROJECT_ROOT / "site" / "dossiers"
PROMPTS_DIR = PROJECT_ROOT / "assets" / "prompts"

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-20250514"
MAX_CONCURRENT = 3


def _load_system_prompt() -> str:
    return (PROMPTS_DIR / "editors" / "dossier_copyeditor.md").read_text()


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------

def _split_dossier(content: str) -> dict:
    """Split a dossier into frontmatter, preamble, and sections.

    Returns {
        "frontmatter": str,   # --- yaml ---
        "preamble": str,      # # Title + summary + --- before section I
        "sections": [(heading, body), ...],  # each ## section
    }
    """
    # Split off frontmatter
    fm_match = re.match(r"^(---\n.*?\n---\n)(.*)", content, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = fm_match.group(2)
    else:
        frontmatter = ""
        body = content

    # Split by ## headings
    parts = re.split(r"(?=^## )", body, flags=re.MULTILINE)

    preamble = parts[0] if parts else ""
    sections = []
    for part in parts[1:]:
        m = re.match(r"^(## .+?)(?:\n|$)", part)
        heading = m.group(1) if m else ""
        sections.append((heading, part))

    return {
        "frontmatter": frontmatter,
        "preamble": preamble,
        "sections": sections,
    }


def _needs_title(preamble: str, country_name: str) -> bool:
    """Check if the preamble has only a placeholder country-name title."""
    m = re.search(r"^#\s+(.+)$", preamble, re.MULTILINE)
    if not m:
        return True
    title = m.group(1).strip()
    # If title is just the country name, it needs a real one
    return title.lower() == country_name.lower()


def _has_summary(preamble: str) -> bool:
    """Check if the preamble has a paragraph between title and ---."""
    # Strip the # title line and any blank lines
    lines = preamble.strip().split("\n")
    # Find content between # title and ---
    after_title = False
    for line in lines:
        if line.startswith("# "):
            after_title = True
            continue
        if after_title:
            stripped = line.strip()
            if stripped == "---":
                return False
            if stripped and not stripped.startswith("#"):
                return True
    return False


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

async def _call_claude(
    client: anthropic.AsyncAnthropic,
    system: str,
    user_msg: str,
    semaphore: asyncio.Semaphore,
) -> str:
    async with semaphore:
        response = await client.messages.create(
            model=MODEL,
            max_tokens=16384,
            temperature=0,
            system=[{"type": "text", "text": system}],
            messages=[{"role": "user", "content": user_msg}],
        )
        parts = [b.text for b in response.content if b.type == "text"]
        tokens_in = response.usage.input_tokens
        tokens_out = response.usage.output_tokens
        print(f"    ({tokens_in} in / {tokens_out} out)")
        return "\n".join(parts)


async def _generate_title_and_summary(
    client: anthropic.AsyncAnthropic,
    system: str,
    country_name: str,
    first_section: str,
    semaphore: asyncio.Semaphore,
) -> tuple[str, str]:
    """Generate a title and executive summary for a dossier."""
    user_msg = (
        f"Task: TITLE_AND_SUMMARY\n\n"
        f"Country: {country_name}\n\n"
        f"First section of the dossier:\n\n"
        f"---\n\n{first_section}"
    )
    print(f"  Generating title and summary for {country_name}...")
    result = await _call_claude(client, system, user_msg, semaphore)

    # Parse TITLE: and SUMMARY: from response
    title = ""
    summary = ""
    title_match = re.search(r"TITLE:\s*(.+?)(?:\n|$)", result)
    if title_match:
        title = title_match.group(1).strip()

    summary_match = re.search(r"SUMMARY:\s*\n(.+)", result, re.DOTALL)
    if summary_match:
        summary = summary_match.group(1).strip()

    return title, summary


async def _edit_section(
    client: anthropic.AsyncAnthropic,
    system: str,
    heading: str,
    section_text: str,
    label: str,
    semaphore: asyncio.Semaphore,
) -> str:
    user_msg = (
        f"Task: SECTION_EDIT\n\n"
        f"Edit the following dossier section for style. "
        f"Return only the edited section.\n\n"
        f"---\n\n{section_text}"
    )
    print(f"  Editing: {label}...")
    return await _call_claude(client, system, user_msg, semaphore)


# ---------------------------------------------------------------------------
# Per-dossier processing
# ---------------------------------------------------------------------------

async def process_dossier(
    filepath: Path,
    client: anthropic.AsyncAnthropic,
    system: str,
    semaphore: asyncio.Semaphore,
    dry_run: bool = False,
    title_only: bool = False,
    skip_titles: bool = False,
) -> dict:
    country_name = filepath.stem.replace("_", " ").title()
    _overrides = {"Uae": "UAE"}
    country_name = _overrides.get(country_name, country_name)

    content = filepath.read_text(encoding="utf-8")
    parsed = _split_dossier(content)

    stats = {
        "file": filepath.name,
        "title_generated": False,
        "sections_edited": 0,
        "skipped": False,
    }

    needs_new_title = _needs_title(parsed["preamble"], country_name)
    needs_summary = not _has_summary(parsed["preamble"])

    if dry_run:
        print(f"  {filepath.name}: {len(parsed['sections'])} sections"
              f"{', needs title' if needs_new_title else ''}"
              f"{', needs summary' if needs_summary else ''}")
        stats["skipped"] = True
        return stats

    # Step 1: Generate title and summary if needed
    new_title = ""
    new_summary = ""
    if not skip_titles and (needs_new_title or needs_summary):
        first_section = parsed["sections"][0][1] if parsed["sections"] else ""
        new_title, new_summary = await _generate_title_and_summary(
            client, system, country_name, first_section, semaphore,
        )
        stats["title_generated"] = True

    # Step 2: Rebuild preamble with new title/summary
    preamble = parsed["preamble"]
    if new_title:
        # Replace the # title line
        preamble = re.sub(r"^#\s+.+$", f"# {new_title}", preamble, count=1, flags=re.MULTILINE)
    if new_summary and needs_summary:
        # Insert summary between title and ---
        lines = preamble.split("\n")
        new_lines = []
        title_found = False
        for line in lines:
            new_lines.append(line)
            if line.startswith("# ") and not title_found:
                title_found = True
                new_lines.append("")
                new_lines.append(new_summary)
        preamble = "\n".join(new_lines)

    if title_only:
        # Only update preamble, don't edit sections
        result = parsed["frontmatter"] + preamble + "".join(
            text for _, text in parsed["sections"]
        )
        filepath.write_text(result, encoding="utf-8")
        return stats

    # Step 3: Copyedit each section in parallel
    async def _do_edit(idx, heading, text):
        label = heading[:60] if heading else f"section {idx}"
        # Check if original ends with a --- separator
        had_trailing_sep = text.rstrip().endswith("---")
        edited = await _edit_section(
            client, system, heading, text, label, semaphore,
        )
        # Restore --- separator if the LLM stripped it
        if had_trailing_sep and not edited.rstrip().endswith("---"):
            edited = edited.rstrip() + "\n\n---\n\n"
        return idx, edited

    tasks = [
        _do_edit(i, h, t)
        for i, (h, t) in enumerate(parsed["sections"])
    ]
    results = await asyncio.gather(*tasks)

    edited_sections = list(parsed["sections"])
    for idx, edited_text in results:
        edited_sections[idx] = (edited_sections[idx][0], edited_text)
        stats["sections_edited"] += 1

    # Step 4: Reassemble
    result = parsed["frontmatter"] + preamble + "".join(
        text for _, text in edited_sections
    )
    filepath.write_text(result, encoding="utf-8")

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def main_async() -> None:
    dry_run = "--dry-run" in sys.argv

    if not API_KEY and not dry_run:
        print("ANTHROPIC_API_KEY not set")
        sys.exit(1)
    title_only = "--title-only" in sys.argv
    skip_titles = "--skip-titles" in sys.argv
    single = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            single = arg

    files = sorted(DOSSIERS_DIR.glob("*.mdx"))
    files = [f for f in files if f.name != "index.mdx"]

    if single:
        files = [f for f in files if f.stem == single]
        if not files:
            print(f"No dossier found for '{single}'")
            sys.exit(1)

    system = _load_system_prompt()
    client = anthropic.AsyncAnthropic(api_key=API_KEY)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    mode_parts = []
    if dry_run:
        mode_parts.append("DRY RUN")
    if title_only:
        mode_parts.append("TITLES ONLY")
    if skip_titles:
        mode_parts.append("SKIP TITLES")
    mode = " | ".join(mode_parts) if mode_parts else "FULL EDIT"

    print(f"Copyediting {len(files)} dossiers ({mode})\n")

    all_stats = []
    for f in files:
        print(f"\n{'='*60}")
        print(f"Processing {f.name}")
        print(f"{'='*60}")
        stats = await process_dossier(
            f, client, system, semaphore,
            dry_run=dry_run,
            title_only=title_only,
            skip_titles=skip_titles,
        )
        all_stats.append(stats)

    print(f"\n{'='*60}")
    print("Summary:")
    titles = sum(1 for s in all_stats if s["title_generated"])
    sections = sum(s["sections_edited"] for s in all_stats)
    print(f"  Titles generated: {titles}")
    print(f"  Sections edited: {sections}")


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
