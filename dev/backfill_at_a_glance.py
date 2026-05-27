"""Backfill italic region card_summary lines into at-a-glance.mdx files.

Extracts each region's overview Card body from overview.mdx and inserts it
italicized below the matching region heading in at-a-glance.mdx.

Skips briefs already containing italic summaries.
"""
import re
import sys
from pathlib import Path

BRIEFS_ROOT = Path(__file__).resolve().parents[1] / "site" / "briefs"

OVERVIEW_CARD_RE = re.compile(
    r'<Card\s+title="([^"]+)"\s+icon="[^"]+"\s+href="/briefs/[^/]+/([a-z-]+)"\s*>\s*'
    r'(.+?)\s*</Card>',
    re.DOTALL,
)


def extract_region_summaries(overview_text: str) -> dict[str, str]:
    """Map region slug → card body text."""
    summaries = {}
    for match in OVERVIEW_CARD_RE.finditer(overview_text):
        title, slug, body = match.group(1), match.group(2), match.group(3)
        body = " ".join(body.split())
        summaries[slug] = body
    return summaries


def insert_italic_lines(glance_text: str, summaries: dict[str, str]) -> tuple[str, list[str]]:
    """Insert italicized summary line below each region header.

    Returns (new_text, list_of_slugs_inserted).
    """
    inserted = []
    for slug, body in summaries.items():
        header_pattern = re.compile(
            rf'(## \[[^\]]+\]\(/briefs/[^/]+/{re.escape(slug)}\)\n\n)(?!_)',
        )
        new_glance, n = header_pattern.subn(rf'\1_{body}_\n\n', glance_text)
        if n == 1:
            glance_text = new_glance
            inserted.append(slug)
        elif n > 1:
            print(f"  WARN: multiple headers matched slug {slug}", file=sys.stderr)
    return glance_text, inserted


def process_brief(brief_dir: Path) -> None:
    overview_path = brief_dir / "overview.mdx"
    glance_path = brief_dir / "at-a-glance.mdx"
    if not overview_path.exists() or not glance_path.exists():
        return

    overview_text = overview_path.read_text()
    glance_text = glance_path.read_text()

    summaries = extract_region_summaries(overview_text)
    if not summaries:
        print(f"{brief_dir.name}: no region cards found in overview")
        return

    new_text, inserted = insert_italic_lines(glance_text, summaries)
    if not inserted:
        print(f"{brief_dir.name}: nothing to insert (already done?)")
        return

    glance_path.write_text(new_text)
    print(f"{brief_dir.name}: inserted {len(inserted)} ({', '.join(inserted)})")


def main() -> None:
    for brief_dir in sorted(BRIEFS_ROOT.iterdir()):
        if not brief_dir.is_dir() or brief_dir.name.startswith(("_", ".")):
            continue
        if not (brief_dir / "at-a-glance.mdx").exists():
            continue
        process_brief(brief_dir)


if __name__ == "__main__":
    main()
