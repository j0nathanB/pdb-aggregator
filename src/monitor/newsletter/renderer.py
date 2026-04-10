"""
Template renderer: converts structured content models into MDX strings.

Uses Jinja2 templates. Markdown/MDX is produced exactly once, here.
Output is dict[str, str] (slug → MDX content), compatible with publish_brief().
"""

import logging
import re
from datetime import date, timedelta
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from ..config import Region
from .assembly import REGION_SLUGS, REGION_ORDER
from .content_models import (
    AtAGlancePageContent,
    OverviewPageContent,
    RegionPageContent,
    WatchlistPageContent,
)

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent / "templates"


def _format_date_range(end_date: date) -> str:
    """Format end_date into 'Month DD, YYYY' start date string."""
    start = end_date - timedelta(days=6)
    return f"{start.strftime('%B %d, %Y')}"


def _format_date_range_display(dates: list[str]) -> str:
    """Format ISO date strings into a readable range for notes section."""
    valid = sorted(set(d for d in dates if d and len(d) >= 10))
    if not valid:
        return ""
    if len(valid) == 1:
        try:
            d = date.fromisoformat(valid[0])
            return d.strftime("%B %d, %Y")
        except ValueError:
            return valid[0]
    try:
        d1 = date.fromisoformat(valid[0])
        d2 = date.fromisoformat(valid[-1])
        if d1.month == d2.month and d1.year == d2.year:
            return f"{d1.strftime('%B')} {d1.day}–{d2.day}, {d1.year}"
        return f"{d1.strftime('%B %d')} – {d2.strftime('%B %d, %Y')}"
    except ValueError:
        return f"{valid[0]} – {valid[-1]}"


def _render_notes_section(story_map_data: dict) -> str:
    """Render the Notes accordion with ResponseField + Expandable components."""
    lines = ['<Accordion title="Notes">']

    for story in story_map_data.get("stories", []):
        articles = story.get("articles", [])
        if not articles:
            continue

        headline = story.get("headline", "Untitled")
        # Sanitize headline for JSX attribute — quotes break name="..."
        headline = headline.replace('\\', '').replace('"', "'")
        date_range = _format_date_range_display([a.get("date", "") for a in articles])

        lines.append(f'<ResponseField name="{headline}" type="{date_range}">')
        lines.append(f'<Expandable title="Sources ({len(articles)})">')
        for a in articles:
            title = a.get("title", "Untitled")
            source = a.get("source", "")
            url = a.get("url", "")
            if url:
                lines.append(f"- [{title} — {source}]({url})")
            else:
                lines.append(f"- {title} — {source}")
        lines.append("</Expandable>")
        lines.append("</ResponseField>")
        lines.append("")

    singles = story_map_data.get("single_source_items", [])
    if singles:
        lines.append('<ResponseField name="Other" type="">')
        lines.append(f'<Expandable title="Sources ({len(singles)})">')
        for item in singles:
            title = item.get("headline", "Untitled")
            source = item.get("source", "")
            url = item.get("url", "")
            if url:
                lines.append(f"- [{title} — {source}]({url})")
            else:
                lines.append(f"- {title} — {source}")
        lines.append("</Expandable>")
        lines.append("</ResponseField>")
        lines.append("")

    lines.append("</Accordion>")
    return "\n".join(lines)


def _escape_mdx(text: str) -> str:
    """Escape special characters that break MDX rendering."""
    # Strip emoji (flag emoji and others break Mintlify's MDX parser)
    text = re.sub(r'[\U0001F000-\U0001FFFF]', '', text)
    # Escape unescaped dollar signs (prevent LaTeX)
    text = re.sub(r'(?<!\\)\$(?!\$)', r'\$', text)
    return text


# Boilerplate openers the regional editor sometimes prepends to gap paragraphs.
# We strip these so the gap reads as direct prose.
_GAP_BOILERPLATE_RE = re.compile(
    r"^\s*(?:notably absent|missing|not present|absent)\s*(?:this week)?\s*[:\-—–]?\s*",
    re.IGNORECASE,
)


def _sanitize_gap_paragraphs(gaps: list[str]) -> list[str]:
    """Strip boilerplate openers and merge multiple gaps into one paragraph.

    The regional editor's prompt asks for a single woven gap, but LLMs sometimes
    produce multiple separate items with "Notably absent this week:" prefixes.
    This deterministic post-process enforces both invariants.
    """
    cleaned: list[str] = []
    for g in gaps:
        if not g or not g.strip():
            continue
        stripped = _GAP_BOILERPLATE_RE.sub("", g.strip())
        # Capitalise first letter if the boilerplate stripped one off mid-sentence
        if stripped and stripped[0].islower():
            stripped = stripped[0].upper() + stripped[1:]
        cleaned.append(stripped)
    if len(cleaned) <= 1:
        return cleaned
    # Merge multiple paragraphs into one with sentence-level joins
    merged = " ".join(p.rstrip(".") + "." for p in cleaned)
    return [merged]


def _build_env() -> Environment:
    """Create Jinja2 environment with custom globals."""
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["render_notes_section"] = _render_notes_section
    return env


def render_pages(
    overview: OverviewPageContent,
    region_pages: dict[Region, RegionPageContent],
    watchlist: WatchlistPageContent,
    at_a_glance: AtAGlancePageContent | None = None,
) -> dict[str, str]:
    """Render all pages from structured content models.

    Returns dict[str, str] (slug → MDX content), compatible with publish_brief().
    """
    env = _build_env()
    pages: dict[str, str] = {}

    end_date = overview.week_end
    end_date_str = end_date.isoformat()
    date_range = _format_date_range(end_date)

    # Overview page
    overview_tmpl = env.get_template("overview.mdx.j2")
    pages["overview"] = _escape_mdx(overview_tmpl.render(
        date_range=date_range,
        end_date_str=end_date_str,
        country_count=overview.country_count,
        executive_brief=overview.executive_brief,
        region_cards=overview.region_cards,
        watchlist_card_summary=overview.watchlist_card_summary,
    ))

    # At-a-glance page
    if at_a_glance and at_a_glance.regions:
        glance_tmpl = env.get_template("at-a-glance.mdx.j2")
        pages["at-a-glance"] = _escape_mdx(glance_tmpl.render(
            date_range=date_range,
            end_date_str=end_date_str,
            regions=at_a_glance.regions,
        ))

    # Region pages
    region_tmpl = env.get_template("region.mdx.j2")
    for region in REGION_ORDER:
        page_content = region_pages.get(region)
        if not page_content:
            continue
        slug = REGION_SLUGS.get(region, region.value)
        pages[slug] = _escape_mdx(region_tmpl.render(
            display_name=page_content.display_name,
            date_range=date_range,
            regional_lead=page_content.regional_lead,
            gap_paragraphs=_sanitize_gap_paragraphs(page_content.gap_paragraphs),
            countries=page_content.countries,
        ))

    # Watchlist page
    watchlist_tmpl = env.get_template("watchlist.mdx.j2")
    pages["watchlist"] = _escape_mdx(watchlist_tmpl.render(
        date_range=date_range,
        items=watchlist.items,
        edited_narrative=watchlist.edited_narrative,
    ))

    return pages
