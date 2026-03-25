#!/usr/bin/env python3
"""Convert country dossier .md files to Mintlify-compatible .mdx files."""

import glob
import os
import re

SOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "country_dossiers")
TARGET_DIR = os.path.join(os.path.dirname(__file__), "..", "site", "dossiers")

# Special case title overrides
TITLE_OVERRIDES = {
    "uae": "UAE",
}


def slug_from_filename(filename: str) -> str:
    """Extract country slug from filename like 'mexico_dossier_2026-03-08.md'."""
    match = re.match(r"^(.+?)_dossier_\d{4}-\d{2}-\d{2}\.md$", filename)
    if not match:
        raise ValueError(f"Unexpected filename pattern: {filename}")
    return match.group(1)


def title_from_slug(slug: str) -> str:
    """Convert slug to title case, with special-case handling."""
    if slug in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[slug]
    return slug.replace("_", " ").title()


def convert_dossier(source_path: str, target_path: str, title: str, slug: str) -> None:
    """Read a dossier .md and write a .mdx with Mintlify frontmatter."""
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter = (
        f"---\n"
        f'title: "{title}"\n'
        f'description: "Strategic country dossier for {title}"\n'
        f'sidebarTitle: "{title}"\n'
        f"---\n\n"
    )

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)


def main() -> None:
    os.makedirs(TARGET_DIR, exist_ok=True)

    pattern = os.path.join(SOURCE_DIR, "*_dossier_*.md")
    files = sorted(glob.glob(pattern))

    print(f"Found {len(files)} dossier files in {SOURCE_DIR}")

    for source_path in files:
        filename = os.path.basename(source_path)
        slug = slug_from_filename(filename)
        title = title_from_slug(slug)
        target_path = os.path.join(TARGET_DIR, f"{slug}.mdx")

        convert_dossier(source_path, target_path, title, slug)
        print(f"  {filename} -> {slug}.mdx  ({title})")

    print(f"\nWrote {len(files)} .mdx files to {TARGET_DIR}")


if __name__ == "__main__":
    main()
