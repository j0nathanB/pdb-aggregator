"""
Publish assembled newsletter pages to the Mintlify site directory.

Writes MDX files and updates docs.json navigation (Latest Brief + Archives).
"""

import json
import logging
import re
from datetime import date, timedelta
from pathlib import Path

from ...monitor.config import PROJECT_ROOT

logger = logging.getLogger(__name__)

SITE_DIR = PROJECT_ROOT / "site"
DOCS_JSON = SITE_DIR / "docs.json"

# Stable page order for navigation
PAGE_ORDER = [
    "overview",
    "frontline-eastern-europe",
    "western-europe",
    "asia-pacific",
    "near-east-south-asia",
    "the-americas",
    "watchlist",
]


def _escape_mdx(content: str) -> str:
    """Escape characters that have special meaning in MDX.

    Escapes $ signs (LaTeX math trigger) in body text while preserving
    frontmatter and JSX expressions.
    """
    # Split frontmatter from body
    parts = content.split("---", 2)
    if len(parts) >= 3:
        # parts[0] is before first ---, parts[1] is frontmatter, parts[2] is body
        body = parts[2]
        # Escape bare $ (not already escaped) outside JSX expressions
        body = re.sub(r'(?<!\\)\$', r'\\$', body)
        return f"{parts[0]}---{parts[1]}---{body}"

    # No frontmatter — escape the whole thing
    return re.sub(r'(?<!\\)\$', r'\\$', content)


def publish_brief(pages: dict[str, str], end_date: date) -> Path:
    """
    Write MDX pages to site/briefs/{date}/ and update docs.json.

    Args:
        pages: dict of slug -> MDX content from assemble_newsletter_pages()
        end_date: the brief's end date (used for directory name and nav)

    Returns:
        Path to the brief directory.
    """
    date_str = end_date.isoformat()
    brief_dir = SITE_DIR / "briefs" / date_str
    brief_dir.mkdir(parents=True, exist_ok=True)

    # Write MDX files
    for slug, content in pages.items():
        page_path = brief_dir / f"{slug}.mdx"
        page_path.write_text(_escape_mdx(content))
        logger.debug("Wrote %s", page_path)

    logger.info("Published %d pages to %s", len(pages), brief_dir)

    # Update docs.json navigation
    _update_docs_json(date_str, end_date)

    return brief_dir


def _stamp_archived(brief_date_str: str) -> None:
    """Rewrite description frontmatter in archived brief pages to say 'Archived brief'."""
    brief_dir = SITE_DIR / "briefs" / brief_date_str
    if not brief_dir.exists():
        return

    # Parse the date for a readable label
    try:
        d = date.fromisoformat(brief_date_str)
        start = d - timedelta(days=6)
        week_label = f"Week of {start.strftime('%B')} {start.day}, {d.year}"
    except ValueError:
        week_label = brief_date_str

    desc_pattern = re.compile(r'^(description:\s*")(.+?)(")$', re.MULTILINE)
    sidebar_pattern = re.compile(r'^(sidebarTitle:\s*")(.+?)(")$', re.MULTILINE)

    for mdx in brief_dir.glob("*.mdx"):
        text = mdx.read_text()
        is_overview = mdx.stem == "overview"

        # Description (renders below the title): keep original content
        new_desc = (
            "A weekly survey of 29 middle powers across five regions"
            if is_overview else week_label
        )
        text = desc_pattern.sub(rf'\g<1>{new_desc}\3', text)

        # Ensure overview pages keep "Overview" as sidebarTitle
        if is_overview:
            text = sidebar_pattern.sub(r'\g<1>Overview\3', text)

        mdx.write_text(text)

    logger.debug("Stamped archived description on %s", brief_dir)


def _update_docs_json(date_str: str, end_date: date) -> None:
    """Update docs.json: set Latest Brief to this date, archive the previous latest."""
    if not DOCS_JSON.exists():
        logger.warning("docs.json not found at %s, skipping nav update", DOCS_JSON)
        return

    docs = json.loads(DOCS_JSON.read_text())
    tabs = docs.get("navigation", {}).get("tabs", [])

    brief_prefix = f"briefs/{date_str}"
    page_list = [f"{brief_prefix}/{slug}" for slug in PAGE_ORDER]

    week_start = end_date - timedelta(days=6)
    archive_label = f"Week of {week_start.strftime('%B')} {week_start.day}, {end_date.year}"

    # Find the Latest Brief and Archives tabs
    latest_tab = None
    archives_tab = None
    for tab in tabs:
        if tab.get("tab") == "Latest Brief":
            latest_tab = tab
        elif tab.get("tab") == "Archives":
            archives_tab = tab

    # Move current Latest Brief into Archives (if it exists and is different)
    if latest_tab and latest_tab.get("pages"):
        old_pages = latest_tab["pages"]
        # Extract date from the first page path: "briefs/YYYY-MM-DD/overview"
        old_date_str = None
        if old_pages:
            parts = old_pages[0].split("/")
            if len(parts) >= 2:
                old_date_str = parts[1]

        if old_date_str and old_date_str != date_str:
            # Stamp the old brief's MDX files as archived
            _stamp_archived(old_date_str)

            # Build archive group label: "Jan 19 — Jan 25" date range
            try:
                old_end = date.fromisoformat(old_date_str)
                old_start = old_end - timedelta(days=6)
                old_label = f"{old_start.strftime('%b')} {old_start.day} — {old_end.strftime('%b')} {old_end.day}"
            except ValueError:
                old_label = old_date_str

            old_group = {"group": old_label, "expanded": False, "pages": old_pages}

            if archives_tab is None:
                archives_tab = {"tab": "Archives", "groups": [{"group": "Past Briefs", "pages": []}]}
                tabs.append(archives_tab)

            # Ensure nested structure: groups[0] is "Past Briefs" parent
            parent_groups = archives_tab.get("groups", [])
            past_briefs = None
            for g in parent_groups:
                if g.get("group") == "Past Briefs":
                    past_briefs = g
                    break
            if past_briefs is None:
                # Migrate flat groups into nested structure
                existing_entries = []
                for g in parent_groups:
                    g["expanded"] = False
                    existing_entries.append(g)
                past_briefs = {"group": "Past Briefs", "pages": existing_entries}
                archives_tab["groups"] = [past_briefs]

            entries = past_briefs.get("pages", [])
            # Don't duplicate — check if this date is already archived
            if not any(old_date_str in str(e.get("pages", [])) for e in entries if isinstance(e, dict)):
                entries.insert(0, old_group)
            past_briefs["pages"] = entries

    # Set Latest Brief to new pages
    if latest_tab is None:
        latest_tab = {"tab": "Latest Brief", "pages": []}
        tabs.insert(0, latest_tab)
    latest_tab["pages"] = page_list

    # Update redirect
    docs.setdefault("redirects", [])
    for r in docs["redirects"]:
        if r.get("source") == "/":
            r["destination"] = f"/{brief_prefix}/overview"
            break
    else:
        docs["redirects"].append({
            "source": "/",
            "destination": f"/{brief_prefix}/overview",
        })

    # Remove the new brief from Archives if it ended up there
    if archives_tab and archives_tab.get("groups"):
        for parent in archives_tab["groups"]:
            if parent.get("group") == "Past Briefs":
                parent["pages"] = [
                    e for e in parent.get("pages", [])
                    if not isinstance(e, dict) or date_str not in str(e.get("pages", []))
                ]

    # Sort archive entries by date (newest first)
    if archives_tab and archives_tab.get("groups"):
        def _extract_date(entry: dict) -> str:
            pages = entry.get("pages", [])
            if pages and isinstance(pages[0], str):
                parts = pages[0].split("/")
                if len(parts) >= 2:
                    return parts[1]
            return ""
        for parent in archives_tab["groups"]:
            if parent.get("group") == "Past Briefs":
                parent["pages"].sort(key=_extract_date, reverse=True)

    docs["navigation"]["tabs"] = tabs

    DOCS_JSON.write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n")
    logger.info("Updated docs.json: Latest Brief → %s", date_str)
