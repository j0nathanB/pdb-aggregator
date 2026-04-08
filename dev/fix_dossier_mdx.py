#!/usr/bin/env python3
"""Fix MDX parsing errors in dossier files.

Escapes `<`, `>`, `{`, `}` characters in prose that MDX interprets as JSX.
Preserves YAML frontmatter unchanged. Skips index.mdx (has real MDX components).
"""

import re
from pathlib import Path

DOSSIERS_DIR = Path(__file__).resolve().parent.parent / "site" / "dossiers"


def fix_mdx_body(body: str) -> str:
    """Escape problematic characters in MDX body content."""
    # Replace { and } with escaped versions
    body = body.replace("{", "\\{")
    body = body.replace("}", "\\}")
    # Replace < and > with HTML entities
    body = body.replace("<", "&lt;")
    body = body.replace(">", "&gt;")
    return body


def process_file(path: Path) -> bool:
    """Process a single .mdx file. Returns True if changes were made."""
    content = path.read_text(encoding="utf-8")

    # Split frontmatter from body
    # Frontmatter is between the first two '---' lines
    match = re.match(r"^(---\n.*?\n---\n)(.*)", content, re.DOTALL)
    if not match:
        print(f"  SKIP (no frontmatter): {path.name}")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    fixed_body = fix_mdx_body(body)

    if fixed_body == body:
        print(f"  No changes needed: {path.name}")
        return False

    path.write_text(frontmatter + fixed_body, encoding="utf-8")
    print(f"  FIXED: {path.name}")
    return True


def main():
    mdx_files = sorted(DOSSIERS_DIR.glob("*.mdx"))
    print(f"Found {len(mdx_files)} .mdx files in {DOSSIERS_DIR}\n")

    fixed_count = 0
    for f in mdx_files:
        if f.name == "index.mdx":
            print(f"  SKIP (index): {f.name}")
            continue
        if process_file(f):
            fixed_count += 1

    print(f"\nDone. Fixed {fixed_count} files.")


if __name__ == "__main__":
    main()
