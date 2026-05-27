#!/usr/bin/env python3
"""
Generate regional and executive summaries using new prompts.

For each published brief:
1. Extract country sections from each region's MDX
2. Call Claude with regional_summary_prompt as system + countries as user
3. Compile all regional summaries → call Claude with executive_summary_prompt
"""

import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

import anthropic

MODEL = "claude-opus-4-6"
BRIEFS_DIR = Path(__file__).resolve().parents[2] / "site" / "briefs"
OUTPUT_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = Path(__file__).resolve().parents[1]  # dev/

REGIONAL_PROMPT = (PROMPTS_DIR / "regional_summary_prompt.md").read_text()
EXECUTIVE_PROMPT = (PROMPTS_DIR / "executive_summary_prompt.md").read_text()

REGIONS = [
    "asia-pacific",
    "frontline-eastern-europe",
    "near-east-south-asia",
    "the-americas",
    "western-europe",
]

SKIP_DIRS = {"_old", ".DS_Store"}

client = anthropic.Anthropic()


def extract_country_sections(mdx_path: Path) -> str:
    """Extract text between each ### <img src="https://flagcdn.com/
    and its corresponding <Accordion title="Other Stories"> line."""
    text = mdx_path.read_text()
    lines = text.split("\n")

    sections = []
    in_section = False
    current_section = []

    for line in lines:
        if '### <img src="https://flagcdn.com/' in line:
            # Start a new country section
            if current_section:
                sections.append("\n".join(current_section))
            current_section = [line]
            in_section = True
        elif in_section and '<Accordion title="Other Stories">' in line:
            # End of country section (don't include this line)
            sections.append("\n".join(current_section))
            current_section = []
            in_section = False
        elif in_section:
            current_section.append(line)

    # Handle edge case: section without Accordion closer
    if current_section:
        sections.append("\n".join(current_section))

    return "\n\n---\n\n".join(sections)


def call_claude(system_prompt: str, user_content: str) -> str:
    """Call Claude API and return the text response."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text


def process_brief(date_str: str) -> None:
    """Process one brief: extract countries, generate regional + executive summaries."""
    brief_dir = BRIEFS_DIR / date_str
    out_dir = OUTPUT_DIR / date_str
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Processing brief: {date_str}")
    print(f"{'='*60}")

    regional_summaries = {}

    for region in REGIONS:
        mdx_path = brief_dir / f"{region}.mdx"
        if not mdx_path.exists():
            print(f"  SKIP {region} — no MDX file")
            continue

        # Step 1: Extract country sections
        countries_content = extract_country_sections(mdx_path)
        if not countries_content.strip():
            print(f"  SKIP {region} — no country sections found")
            continue

        countries_file = out_dir / f"{region}_countries.md"
        countries_file.write_text(countries_content)
        print(f"  Extracted {region} countries ({len(countries_content)} chars)")

        # Step 2: Generate regional summary
        print(f"  Generating regional summary for {region}...")
        summary = call_claude(REGIONAL_PROMPT, countries_content)
        summary_file = out_dir / f"regional_summary_{region}.md"
        summary_file.write_text(summary)
        regional_summaries[region] = summary
        print(f"  Saved regional_summary_{region}.md ({len(summary)} chars)")

    # Step 3: Compile all regional summaries
    if not regional_summaries:
        print(f"  ERROR: No regional summaries generated for {date_str}")
        return

    compiled_parts = []
    for region in REGIONS:
        if region in regional_summaries:
            compiled_parts.append(f"## {region}\n\n{regional_summaries[region]}")

    all_summaries = "\n\n---\n\n".join(compiled_parts)
    all_file = out_dir / "all_region_summaries.md"
    all_file.write_text(all_summaries)
    print(f"  Compiled all_region_summaries.md ({len(all_summaries)} chars)")

    # Step 4: Generate executive summary
    print(f"  Generating executive summary...")
    exec_summary = call_claude(EXECUTIVE_PROMPT, all_summaries)
    exec_file = out_dir / "executive_summary.md"
    exec_file.write_text(exec_summary)
    print(f"  Saved executive_summary.md ({len(exec_summary)} chars)")


def main():
    # Get sorted brief dates, skip non-date dirs
    dates = sorted(
        d.name
        for d in BRIEFS_DIR.iterdir()
        if d.is_dir() and d.name not in SKIP_DIRS and re.match(r"\d{4}-\d{2}-\d{2}", d.name)
    )

    print(f"Found {len(dates)} briefs: {', '.join(dates)}")
    print(f"Regions: {', '.join(REGIONS)}")
    print(f"Model: {MODEL}")
    print(f"Output: {OUTPUT_DIR}")

    for date_str in dates:
        process_brief(date_str)

    print(f"\n{'='*60}")
    print("Done! All summaries generated.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
