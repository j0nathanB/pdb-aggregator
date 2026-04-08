#!/usr/bin/env python3
"""Replace pass 3 sections in dossiers with updated versions.

For each country with a _pass3 file:
1. Back up the original dossier to _old/
2. Find where pass 3 starts in the original (first line matching section 13 or equivalent)
3. Keep everything before that line, append the new pass 3 content
"""

from __future__ import annotations
import re
import shutil
from pathlib import Path

DOSSIERS_DIR = Path("/Users/zen/dev/src/pdb/assets/country_dossiers")
PASS3_DIR = DOSSIERS_DIR / "_pass3"
OLD_DIR = DOSSIERS_DIR / "_old"

# Map country name from pass3 filename to dossier filename
def find_dossier(country: str) -> Path | None:
    matches = list(DOSSIERS_DIR.glob(f"{country}_dossier_*.md"))
    return matches[0] if matches else None


def find_pass3_start(lines: list[str], country: str) -> int | None:
    """Find the line number where pass 3 content begins.

    This is the first occurrence of Section 13 (or equivalent header).
    We also need to check for transition text between pass 2 and pass 3
    (e.g., "# Structural Intelligence Dossier: ... Sections 13-20").
    """
    # Patterns that indicate the start of pass 3 content
    # Look for section 13 header or a pass 3 title block
    patterns = [
        # Standard: ## Section 13 / ## SECTION 13
        re.compile(r'^#{1,3}\s+[Ss]ection\s+13[:\s]', re.IGNORECASE),
        # Plain numbered: ## 13.
        re.compile(r'^#{1,3}\s+13\.\s'),
        # Title block for pass 3: "# Structural ... Sections 13"
        re.compile(r'^#\s+.*[Ss]ections?\s+13', re.IGNORECASE),
        # Taiwan uses Roman numerals for pass 3: ## I. Civil society
        # but we need to distinguish from pass 1 Roman numerals
    ]

    # Special handling for Taiwan - pass 3 starts at "## I. Civil society"
    # which comes AFTER "## Conclusion" following Domain 5
    if country == "taiwan":
        found_domain5_end = False
        for i, line in enumerate(lines):
            if re.match(r'^## Conclusion', line) and found_domain5_end:
                # This is the conclusion after domains, pass 3 starts after
                # Actually, let's look for "Civil society" header
                pass
            if re.match(r'STRUCTURAL CLAIMS.*DOMAIN 5', line, re.IGNORECASE):
                found_domain5_end = True
            if found_domain5_end and re.match(r'^## I\.\s+Civil society', line, re.IGNORECASE):
                return i
        # Fallback: look for the pass 3 title block
        for i, line in enumerate(lines):
            if re.match(r'^#.*[Ss]ections?\s+13', line):
                return i

    # Special handling for Ukraine - uses "## SECTION 13"
    # but also has a title block "# Structural Intelligence Dossier: Ukraine (Sections 13-20)"
    if country == "ukraine":
        for i, line in enumerate(lines):
            if re.match(r'^#\s+Structural.*[Ss]ections?\s+13', line):
                return i

    for i, line in enumerate(lines):
        for pattern in patterns:
            if pattern.match(line):
                return i

    return None


def process_country(country: str):
    pass3_file = PASS3_DIR / f"{country}_pass3.md"
    dossier_file = find_dossier(country)

    if not dossier_file:
        print(f"  ERROR: No dossier file found for {country}")
        return False

    # Read both files
    with open(dossier_file) as f:
        original_lines = f.readlines()

    with open(pass3_file) as f:
        new_pass3 = f.read()

    # Find where pass 3 starts in the original
    cut_line = find_pass3_start(original_lines, country)

    if cut_line is None:
        print(f"  ERROR: Could not find pass 3 start in {dossier_file.name}")
        return False

    print(f"  Found pass 3 start at line {cut_line + 1}: {original_lines[cut_line].strip()[:80]}")

    # Back up original
    backup_path = OLD_DIR / dossier_file.name
    shutil.copy2(dossier_file, backup_path)
    print(f"  Backed up to _old/{dossier_file.name}")

    # Build new content: everything before cut_line + new pass 3
    preserved = "".join(original_lines[:cut_line])

    # Ensure there's a clean separator
    if not preserved.endswith("\n\n"):
        if preserved.endswith("\n"):
            preserved += "\n"
        else:
            preserved += "\n\n"

    new_content = preserved + new_pass3

    # Write back
    with open(dossier_file, "w") as f:
        f.write(new_content)

    old_lines = len(original_lines)
    new_lines = new_content.count("\n")
    print(f"  Replaced: {old_lines} lines -> {new_lines} lines")

    return True


def main():
    countries = [f.stem.replace("_pass3", "") for f in PASS3_DIR.glob("*_pass3.md")]
    print(f"Processing {len(countries)} countries: {sorted(countries)}\n")

    success = 0
    for country in sorted(countries):
        print(f"{country}:")
        if process_country(country):
            success += 1
        print()

    print(f"\nDone: {success}/{len(countries)} countries processed successfully")


if __name__ == "__main__":
    main()
