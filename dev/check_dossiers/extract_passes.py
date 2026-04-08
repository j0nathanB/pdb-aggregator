#!/usr/bin/env python3
"""Extract dossier sections into pass folders.

Pass 1: Sections 0-7
Pass 2: Sections 8-12
Pass 3: Sections 13-20
"""

from __future__ import annotations
import re
import os
from pathlib import Path

DOSSIERS_DIR = Path("/Users/zen/dev/src/pdb/assets/country_dossiers")
CHECK_DIR = Path("/Users/zen/dev/src/pdb/dev/check_dossiers")

# Section ranges per pass
PASS_RANGES = {
    "pass_1": range(0, 8),    # 0-7
    "pass_2": range(8, 13),   # 8-12
    "pass_3": range(13, 21),  # 13-20
}


def get_country_name(filename: str) -> str:
    """Extract country name from dossier filename."""
    # e.g., germany_dossier_2026-03-25.md -> germany
    match = re.match(r"(.+?)_dossier_", filename)
    if match:
        return match.group(1)
    return None


def find_section_boundaries(lines: list[str], country: str = "") -> list[tuple[int, int | str, int]]:
    """Find section boundaries in a dossier.

    Returns list of (line_index, section_number_or_range, heading_level).
    Section number can be an int or a string like "17-20" for merged sections.
    """
    boundaries = []

    # Standard pattern: "## SECTION 0:", "## Section 1:", "## Sections 17–20:", etc.
    section_pattern = re.compile(
        r'^(#{1,3})\s+'
        r'(?:SECTION|Section|SECTIONS|Sections)\s*'
        r'(\d+)(?:\s*[–\-—]\s*(\d+))?'
        r'[:\s]',
        re.IGNORECASE
    )

    # Latvia-specific: Roman numerals for sections 0-7
    roman_pattern = re.compile(
        r'^(#{1,3})\s+(I{1,3}|IV|V|VI{0,3}|VIII?)\.\s',
    )
    roman_to_int = {
        'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4,
        'VI': 5, 'VII': 6, 'VIII': 7,
    }

    # Latvia-specific: DOMAIN N for sections 8-12
    domain_pattern = re.compile(
        r'^(#{1,3})\s+DOMAIN\s+(\d+)[:\s]',
        re.IGNORECASE
    )

    # Latvia-specific: "## 13. Civil society..." plain numbered
    plain_num_pattern = re.compile(
        r'^(#{1,3})\s+(\d+)\.\s',
    )

    for i, line in enumerate(lines):
        m = section_pattern.match(line)
        if m:
            heading_level = len(m.group(1))
            start_num = int(m.group(2))
            end_num = int(m.group(3)) if m.group(3) else None

            if end_num:
                boundaries.append((i, f"{start_num}-{end_num}", heading_level))
            else:
                boundaries.append((i, start_num, heading_level))
            continue

        # Latvia Roman numeral sections (only if no standard sections found yet for pass 1)
        if country == "latvia":
            m = roman_pattern.match(line)
            if m:
                heading_level = len(m.group(1))
                roman = m.group(2)
                if roman in roman_to_int:
                    boundaries.append((i, roman_to_int[roman], heading_level))
                continue

            m = domain_pattern.match(line)
            if m:
                heading_level = len(m.group(1))
                domain_num = int(m.group(2))
                # Domain 1-5 maps to sections 8-12
                section_num = domain_num + 7
                boundaries.append((i, section_num, heading_level))
                continue

            m = plain_num_pattern.match(line)
            if m:
                heading_level = len(m.group(1))
                num = int(m.group(2))
                if 13 <= num <= 20:
                    boundaries.append((i, num, heading_level))
                continue

    return boundaries


def extract_section_content(lines: list[str], boundaries: list, target_sections: range) -> str:
    """Extract content for sections in the target range."""
    content_parts = []

    for idx, (line_idx, section_id, _) in enumerate(boundaries):
        # Determine which sections this boundary covers
        if isinstance(section_id, str):
            # Merged sections like "17-20"
            parts = section_id.split("-")
            covered = range(int(parts[0]), int(parts[1]) + 1)
        else:
            covered = range(section_id, section_id + 1)

        # Check if any of the covered sections are in our target range
        if any(s in target_sections for s in covered):
            # Find end of this section (start of next section or end of file)
            if idx + 1 < len(boundaries):
                end_idx = boundaries[idx + 1][0]
            else:
                end_idx = len(lines)

            content_parts.append("".join(lines[line_idx:end_idx]))

    return "\n".join(content_parts)


def extract_preamble(lines: list[str], boundaries: list) -> str:
    """Extract content before the first section (title, metadata, structural claim #0)."""
    if not boundaries:
        return ""
    first_section_line = boundaries[0][0]
    return "".join(lines[:first_section_line])


def process_dossier(filepath: Path):
    """Process a single dossier file, extracting into pass folders."""
    country = get_country_name(filepath.name)
    if not country:
        print(f"  Skipping {filepath.name} - can't determine country name")
        return

    with open(filepath, "r") as f:
        lines = f.readlines()

    boundaries = find_section_boundaries(lines, country)

    if not boundaries:
        print(f"  WARNING: No section boundaries found in {filepath.name}")
        return

    # Report what sections were found
    section_ids = [b[1] for b in boundaries]
    print(f"  {country}: found sections {section_ids}")

    preamble = extract_preamble(lines, boundaries)

    for pass_name, section_range in PASS_RANGES.items():
        content = extract_section_content(lines, boundaries, section_range)

        if not content.strip():
            print(f"    WARNING: No content for {pass_name} in {country}")
            continue

        # Include preamble for pass_1
        if pass_name == "pass_1":
            full_content = preamble + content
        else:
            full_content = content

        output_dir = CHECK_DIR / pass_name
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{country}.md"

        with open(output_path, "w") as f:
            f.write(full_content)

        # Count sections found for this pass
        found_sections = []
        for _, section_id, _ in boundaries:
            if isinstance(section_id, str):
                parts = section_id.split("-")
                covered = range(int(parts[0]), int(parts[1]) + 1)
            else:
                covered = range(section_id, section_id + 1)
            for s in covered:
                if s in section_range:
                    found_sections.append(s)

        print(f"    {pass_name}: sections {sorted(set(found_sections))}")


def main():
    # Get all dossier files
    dossier_files = sorted(DOSSIERS_DIR.glob("*_dossier_*.md"))
    print(f"Found {len(dossier_files)} dossier files\n")

    for filepath in dossier_files:
        process_dossier(filepath)
        print()


if __name__ == "__main__":
    main()
