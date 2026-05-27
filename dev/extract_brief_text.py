#!/usr/bin/env python3
"""Extract reader-facing prose from the latest published brief to markdown.

Pulls the global overview, each regional summary, every country's narrative,
and the "Other Stories" bullets. Skips at-a-glance, frontmatter, <Note>
blocks, the <Accordion title="Notes"> sources block, and flag <img> tags.

Writes markdown to briefs/{date}/brief_text.md.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_BRIEFS = REPO_ROOT / "site" / "briefs"
BRIEFS = REPO_ROOT / "briefs"

FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\s*', re.DOTALL)
NOTE_BLOCK_RE = re.compile(r'<Note>\s*.*?</Note>\s*', re.DOTALL)
NOTES_ACCORDION_RE = re.compile(
    r'<Accordion title="Notes">.*?</Accordion>\s*', re.DOTALL
)
OTHER_STORIES_RE = re.compile(
    r'<Accordion title="Other Stories">\s*\n?(.*?)\n?\s*</Accordion>',
    re.DOTALL,
)
FLAG_IMG_RE = re.compile(
    r'<img\s+src="https://flagcdn\.com/[^"]+"[^>]*/>\s*'
)
TITLE_RE = re.compile(r'^title:\s*"([^"]+)"', re.MULTILINE)


def clean(text: str) -> str:
    text = FRONTMATTER_RE.sub('', text)
    text = NOTE_BLOCK_RE.sub('', text)
    text = NOTES_ACCORDION_RE.sub('', text)
    text = OTHER_STORIES_RE.sub(
        lambda m: f"#### Other Stories\n\n{m.group(1).strip()}\n", text
    )
    text = FLAG_IMG_RE.sub('', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


def extract_title(text: str) -> str:
    m = TITLE_RE.search(text)
    return m.group(1) if m else ''


def latest_brief() -> Path:
    dirs = sorted(
        p for p in SITE_BRIEFS.iterdir()
        if p.is_dir() and re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.name)
    )
    if not dirs:
        sys.exit(f"No brief directories under {SITE_BRIEFS}")
    return dirs[-1]


def main() -> None:
    brief = latest_brief()
    parts: list[str] = [f"# Middle Powers Monitor — Week of {brief.name}\n"]

    overview = brief / "overview.mdx"
    if overview.exists():
        parts.append("## Global Overview\n")
        parts.append(clean(overview.read_text()))

    skip = {"overview.mdx", "at-a-glance.mdx"}
    for mdx in sorted(brief.glob("*.mdx")):
        if mdx.name in skip:
            continue
        text = mdx.read_text()
        title = extract_title(text)
        parts.append("---\n")
        if title:
            parts.append(f"# {title}\n")
        parts.append(clean(text))

    out_dir = BRIEFS / brief.name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "brief_text.md"
    out_path.write_text("\n".join(parts))
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
