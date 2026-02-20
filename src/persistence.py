"""
Persistence layer for saving and loading briefs.

Briefs are stored in a structured directory format:
    briefs/
        YYYYMMDD/
            brief.md          # Human-readable Markdown
            dossiers.json     # Structured leader data
            meta.json         # Brief metadata
            output.json       # Full serialized output
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import asdict, is_dataclass
import logging

from .config import (
    WeeklyBrief,
    LeaderDossier,
    Story,
    StoryScope,
    COUNTRY_EMOJI,
    # Deprecated but needed for backward compat
    CrossCuttingThread,
    GlobalPulse,
)

logger = logging.getLogger(__name__)


# Default briefs directory
BRIEFS_DIR = Path("briefs")

# Display name overrides (canonical name -> full display name)
DISPLAY_NAMES = {
    "Lula da Silva": "Luiz In\u00e1cio Lula da Silva",
}


def _display_name(name: str) -> str:
    """Return the display name for a leader, falling back to the canonical name."""
    return DISPLAY_NAMES.get(name, name)


def _serialize(obj):
    """Custom JSON serializer for dataclasses and datetime."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "value"):  # Enum
        return obj.value
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _format_date_range(date_range: str) -> str:
    """
    Format date range for display.

    Converts "2026-02-02 to 2026-02-09" to "_Week of February 2, 2026_"
    """
    import re

    # Try to parse "YYYY-MM-DD to YYYY-MM-DD" format
    match = re.match(r"(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})", date_range)
    if match:
        try:
            start = datetime.strptime(match.group(1), "%Y-%m-%d")
            start_str = start.strftime("%B %-d, %Y")
            return f"_Week of {start_str}_"
        except ValueError:
            pass

    # Fallback: return as-is with italics
    return f"_{date_range}_"


def save_brief(
    brief: WeeklyBrief,
    output_dir: Optional[Path] = None,
) -> Path:
    """
    Save a weekly brief to disk.

    Args:
        brief: The WeeklyBrief to save
        output_dir: Custom output directory (default: briefs/YYYYMMDD)

    Returns:
        Path to the saved brief directory
    """
    # Determine output directory
    if output_dir is None:
        date_str = datetime.now().strftime("%Y%m%d")
        output_dir = BRIEFS_DIR / date_str

    # Create directory
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Saving brief to {output_dir}")

    # 1. Save full output as JSON
    output_path = output_dir / "output.json"
    with open(output_path, "w") as f:
        json.dump(brief, f, default=_serialize, indent=2)

    # 2. Save dossiers separately
    dossiers_path = output_dir / "dossiers.json"
    dossiers_data = [asdict(d) for d in brief.leader_dossiers]
    with open(dossiers_path, "w") as f:
        json.dump(dossiers_data, f, default=_serialize, indent=2)

    # 3. Save metadata
    meta_path = output_dir / "meta.json"
    meta = {
        "date_range": brief.date_range,
        "generated_at": brief.generated_at.isoformat() if brief.generated_at else None,
        "leader_count": len(brief.leader_dossiers),
        "main_story_count": len(brief.main_stories),
        "methodology_notes": brief.methodology_notes,
        "source_quality_notes": brief.source_quality_notes,
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    # 4. Generate and save brief page
    markdown_path = output_dir / "brief.md"
    markdown_content = _generate_markdown(brief)
    with open(markdown_path, "w") as f:
        f.write(markdown_content)

    # 5. Save individual leader dossier markdown files
    for dossier in brief.leader_dossiers:
        save_dossier_markdown(dossier, output_dir)

    logger.info(f"Brief saved: {output_dir}")

    return output_dir


def _generate_dossier_markdown(dossier: LeaderDossier, brief_date: str = "") -> str:
    """Generate standalone markdown for an individual leader dossier."""
    import re as _re

    sections = []

    # Derive date from reporting_period end date
    date_match = _re.search(r"(\d{4}-\d{2}-\d{2})$", dossier.reporting_period)
    dossier_date = date_match.group(1) if date_match else (
        dossier.generated_at.strftime("%Y-%m-%d") if dossier.generated_at else brief_date or "1970-01-01"
    )

    # Escape YAML special characters in strings
    leader_name = _display_name(dossier.leader.name).replace('"', '\\"')
    country = dossier.leader.country.replace('"', '\\"')
    title_text = f"{dossier.leader.country} — {_display_name(dossier.leader.name)}, {dossier.leader.title}"
    title_escaped = title_text.replace('"', '\\"')

    # Build nav_tree for dossier sidebar
    nav_tree = []
    story_sections = [
        ("Top Stories", dossier.main_stories),
        ("International", dossier.international_stories),
        ("Domestic", dossier.domestic_stories),
    ]
    for section_title, stories in story_sections:
        if not stories:
            continue
        children = []
        for story in stories:
            children.append({
                "label": story.title,
                "anchor": _slugify(story.title),
            })
        nav_tree.append({
            "label": section_title,
            "anchor": _slugify(section_title),
            "children": children,
        })
    if dossier.between_the_lines:
        nav_tree.append({
            "label": "Between the Lines",
            "anchor": "between-the-lines",
        })

    # YAML frontmatter for Jekyll
    sections.append("---")
    sections.append("layout: dossier")
    sections.append("doc_type: dossier")
    sections.append(f"title: \"{title_escaped}\"")
    sections.append(f"leader_name: \"{leader_name}\"")
    sections.append(f"country: \"{country}\"")
    sections.append(f"date: {dossier_date}")
    sections.append(f"brief_url: \"../../brief/\"")
    sections.append(_format_nav_tree(nav_tree))
    sections.append("---")
    sections.append("")

    # Header
    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "🌍")
    sections.append(f"# {emoji} {dossier.leader.country}")
    sections.append(f"## {_display_name(dossier.leader.name)}, {dossier.leader.title}")
    sections.append(_format_date_range(dossier.reporting_period))
    sections.append("")

    # Executive Summary
    if dossier.executive_summary:
        sections.append(f"> {dossier.executive_summary}")
        sections.append("")

    _render_story_list("Top Stories", dossier.main_stories, sections)
    _render_story_list("International", dossier.international_stories, sections)
    _render_story_list("Domestic", dossier.domestic_stories, sections)

    if dossier.between_the_lines:
        sections.append("## Between the Lines")
        sections.append("")
        for bullet in dossier.between_the_lines:
            sections.append(f"- {bullet}")
        sections.append("")

    # Generated timestamp at the bottom (consistent with main brief)
    sections.append("---")
    sections.append("")
    if dossier.generated_at:
        sections.append(f"*Generated: {dossier.generated_at.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(sections)


def save_dossier_markdown(dossier: LeaderDossier, output_dir: Path) -> Path:
    """
    Save an individual leader dossier as a standalone markdown file.

    Args:
        dossier: The LeaderDossier to save
        output_dir: Brief output directory (typically briefs/YYYYMMDD)

    Returns:
        Path to the saved markdown file
    """
    dossier_dir = output_dir / "dossiers"
    dossier_dir.mkdir(parents=True, exist_ok=True)

    safe_name = dossier.leader.name.lower().replace(" ", "_")
    md_path = dossier_dir / f"{safe_name}.md"

    markdown = _generate_dossier_markdown(dossier)
    with open(md_path, "w") as f:
        f.write(markdown)

    logger.info(f"Saved dossier markdown for {dossier.leader.name} to {md_path}")
    return md_path


def _format_story_refs(story: Story) -> str:
    """Format source references for a story."""
    refs_parts = []
    for src_name, urls in story.source_refs.items():
        links = ",".join(f"[{i+1}]({u})" for i, u in enumerate(urls))
        refs_parts.append(f"{src_name} {links}")
    return f" ({'; '.join(refs_parts)})" if refs_parts else ""


def _dossier_url(filename: str, anchor: str = "") -> str:
    """Convert a dossier filename to a Jekyll-compatible relative URL.

    Converts 'name.md' to '../dossiers/name' (drops .md extension, adds ../ prefix).
    Optionally appends an anchor fragment.
    """
    base = filename.removesuffix(".md")
    url = f"../dossiers/{base}"
    if anchor:
        url = f"{url}#{anchor}"
    return url


def _slugify(text: str) -> str:
    """Convert text to a URL slug matching Jekyll's default slugify filter."""
    import re
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')


def _yaml_escape(s: str) -> str:
    """Escape a string for use in a YAML double-quoted value."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')


def _format_nav_tree(nav_tree: list[dict]) -> str:
    """Format nav_tree as YAML for Jekyll frontmatter."""
    lines = ["nav_tree:"]
    for item in nav_tree:
        lines.append(f'  - label: "{_yaml_escape(item["label"])}"')
        lines.append(f'    anchor: "{item["anchor"]}"')
        if item.get("children"):
            lines.append("    children:")
            for child in item["children"]:
                lines.append(f'      - label: "{_yaml_escape(child["label"])}"')
                lines.append(f'        anchor: "{child["anchor"]}"')
                if child.get("children"):
                    lines.append("        children:")
                    for gc in child["children"]:
                        lines.append(f'          - label: "{_yaml_escape(gc["label"])}"')
                        lines.append(f'            anchor: "{gc["anchor"]}"')
    return "\n".join(lines)


def _build_nav_tree(brief: WeeklyBrief) -> list[dict]:
    """Build the sidebar navigation tree structure for the brief layout."""
    from .config import COUNTRY_SUBREGION, REGION_DISPLAY_NAMES, REGION_ORDER

    nav_tree = []

    # Top Stories
    top_stories = {
        "label": "Top Stories",
        "anchor": "top-stories",
        "children": [
            {"label": story.title, "anchor": _slugify(story.title)}
            for story in brief.main_stories
        ],
    }
    nav_tree.append(top_stories)

    # Regional Briefs
    region_dossiers: dict[str, list] = {}
    for dossier in brief.leader_dossiers:
        country = dossier.leader.country
        region = COUNTRY_SUBREGION.get(country, dossier.leader.region)
        if region not in region_dossiers:
            region_dossiers[region] = []
        region_dossiers[region].append(dossier)

    regional = {
        "label": "Regional Briefs",
        "anchor": "regional-briefs",
        "children": [],
    }

    for region in REGION_ORDER:
        if region not in region_dossiers:
            continue
        region_name = REGION_DISPLAY_NAMES.get(region, region.replace("_", " ").title())
        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)
        region_nav = {
            "label": region_name,
            "anchor": _slugify(region_name),
            "children": [
                {
                    "label": f"{COUNTRY_EMOJI.get(d.leader.country, '🌍')} {d.leader.country} / {_display_name(d.leader.name)}",
                    "anchor": _slugify(f"{d.leader.country} {d.leader.name}"),
                }
                for d in dossiers
            ],
        }
        regional["children"].append(region_nav)

    for region in sorted(region_dossiers.keys()):
        if region in REGION_ORDER:
            continue
        region_name = REGION_DISPLAY_NAMES.get(region, region.replace("_", " ").title())
        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)
        region_nav = {
            "label": region_name,
            "anchor": _slugify(region_name),
            "children": [
                {
                    "label": f"{COUNTRY_EMOJI.get(d.leader.country, '🌍')} {d.leader.country} / {_display_name(d.leader.name)}",
                    "anchor": _slugify(f"{d.leader.country} {d.leader.name}"),
                }
                for d in dossiers
            ],
        }
        regional["children"].append(region_nav)

    nav_tree.append(regional)

    return nav_tree


def _get_first_sentence(text: str) -> str:
    """Extract the first sentence from narrative text."""
    import re

    # Skip dateline (e.g., "CITY, Country — ")
    text = text.strip()
    if " — " in text:
        text = text.split(" — ", 1)[1]

    # Common abbreviations that shouldn't end a sentence
    # Replace periods in abbreviations with a placeholder
    abbrevs = [
        r'U\.S\.', r'U\.K\.', r'U\.N\.', r'E\.U\.', r'Dr\.', r'Mr\.', r'Mrs\.', r'Ms\.',
        r'Jr\.', r'Sr\.', r'Inc\.', r'Ltd\.', r'Corp\.', r'vs\.', r'etc\.', r'i\.e\.',
        r'e\.g\.', r'Gen\.', r'Gov\.', r'Sen\.', r'Rep\.', r'Pres\.', r'Prof\.',
        r'St\.', r'Ave\.', r'Blvd\.', r'Dept\.', r'No\.', r'Vol\.', r'Jan\.',
        r'Feb\.', r'Mar\.', r'Apr\.', r'Aug\.', r'Sept\.', r'Oct\.', r'Nov\.', r'Dec\.',
    ]

    protected = text
    for abbrev in abbrevs:
        protected = re.sub(abbrev, abbrev.replace(r'\.', '\x00'), protected, flags=re.IGNORECASE)

    # Find first real sentence ending (period followed by space and capital letter, or end of string)
    match = re.search(r'\.\s+[A-Z]', protected)
    if match:
        # Restore periods and return first sentence
        first = text[:match.start() + 1]
        return first

    # Try period at end
    if protected.endswith('.'):
        return text

    # Fallback: truncate
    if len(text) > 200:
        return text[:197] + "..."
    return text


def _render_story(story: Story, sections: list[str]):
    """Render a single story into markdown sections."""
    leaders_tag = ""
    if story.contributing_leaders and len(story.contributing_leaders) > 1:
        leaders_tag = f" *({', '.join(story.contributing_leaders)})*"

    refs = _format_story_refs(story)
    sections.append(f"### {story.title}{leaders_tag}")
    sections.append("")
    sections.append(story.narrative)
    if refs:
        sections.append(f"\n*Sources:{refs}*")
    sections.append("")


def _render_story_list(title: str, stories: list[Story], sections: list[str]):
    """Render a titled list of stories."""
    if not stories:
        return
    sections.append(f"## {title}")
    sections.append("")
    for story in stories:
        _render_story(story, sections)


def _brief_title(brief: WeeklyBrief) -> str:
    """Generate the brief's page title."""
    import re as _re
    match = _re.match(r"(\d{4}-\d{2}-\d{2})", brief.date_range)
    if match:
        try:
            start = datetime.strptime(match.group(1), "%Y-%m-%d")
            return f"Week of {start.strftime('%B %-d, %Y')}"
        except ValueError:
            pass
    return f"Week of {brief.date_range}"


def _brief_date(brief: WeeklyBrief) -> str:
    """Extract end date from brief for frontmatter."""
    import re as _re
    date_match = _re.search(r"(\d{4}-\d{2}-\d{2})$", brief.date_range)
    return date_match.group(1) if date_match else (
        brief.generated_at.strftime("%Y-%m-%d") if brief.generated_at else "1970-01-01"
    )


def _generate_markdown(brief: WeeklyBrief) -> str:
    """Generate the full brief page with custom sidebar navigation."""
    from .config import COUNTRY_SUBREGION, REGION_DISPLAY_NAMES, REGION_ORDER

    sections = []

    title = _brief_title(brief)
    date = _brief_date(brief)

    # Build nav_tree for sidebar
    nav_tree = _build_nav_tree(brief)
    nav_tree_yaml = _format_nav_tree(nav_tree)

    # YAML frontmatter
    sections.append("---")
    sections.append("layout: brief")
    sections.append("doc_type: brief")
    sections.append(f"title: \"{title}\"")
    sections.append(f"date: {date}")
    sections.append(f"date_range: \"{brief.date_range}\"")
    sections.append(f"leader_count: {len(brief.leader_dossiers)}")
    sections.append(f"story_count: {len(brief.main_stories)}")
    sections.append("nav_exclude: true")
    sections.append(nav_tree_yaml)
    sections.append("---")
    sections.append("")

    # Header
    sections.append(f"# {title}")
    sections.append("")

    # Executive Summary
    if brief.executive_summary:
        sections.append(f"> {brief.executive_summary}")
        sections.append("")

    # Top Stories
    if brief.main_stories:
        sections.append("## Top Stories")
        sections.append("")
        for story in brief.main_stories:
            _render_story(story, sections)

    # Regional Briefs
    _render_regional_briefs(
        brief, sections,
        COUNTRY_SUBREGION, REGION_DISPLAY_NAMES, REGION_ORDER,
    )

    # Footer with generation timestamp
    sections.append("---")
    sections.append("")
    sections.append(
        f"*Generated: "
        f"{brief.generated_at.strftime('%Y-%m-%d %H:%M') if brief.generated_at else 'Unknown'}*"
    )

    return "\n".join(sections)



def _render_briefs_section(brief: WeeklyBrief, sections: list[str]):
    """
    Render the Briefs section: headlines grouped by country with emoji flags.

    Each headline links to the full story in the dossier with a one-sentence summary.
    Country headers link to the primary leader's dossier for that country.
    Stories come from per-leader dossiers (not aggregate), ensuring links work.
    """
    # Build country -> leader -> stories mapping from dossiers
    # Also track primary dossier file per country (first leader encountered)
    country_stories: dict[str, list[tuple[str, str, Story]]] = {}  # country -> [(leader_name, dossier_file, story)]
    country_primary_dossier: dict[str, str] = {}  # country -> primary dossier file

    for dossier in brief.leader_dossiers:
        country = dossier.leader.country
        leader_name = dossier.leader.name
        safe_name = leader_name.lower().replace(" ", "_")
        dossier_file = f"{safe_name}.md"

        # Set primary dossier for country (first leader encountered)
        if country not in country_primary_dossier:
            country_primary_dossier[country] = dossier_file

        # Collect stories from this dossier that appear in international/domestic
        dossier_stories = dossier.international_stories + dossier.domestic_stories

        for story in dossier_stories:
            if country not in country_stories:
                country_stories[country] = []
            country_stories[country].append((leader_name, dossier_file, story))

    if not country_stories:
        return

    sections.append("## Briefs")
    sections.append("")

    # Sort countries by number of stories (descending), then alphabetically
    sorted_countries = sorted(
        country_stories.keys(),
        key=lambda c: (-len(country_stories[c]), c)
    )

    for country in sorted_countries:
        emoji = COUNTRY_EMOJI.get(country, "🌍")
        primary_dossier = country_primary_dossier.get(country, "")
        # Country header links to the primary leader's dossier
        sections.append(f"### [{emoji} {country}]({_dossier_url(primary_dossier)})")
        sections.append("")

        # Sort stories by score
        stories = sorted(country_stories[country], key=lambda x: x[2].score, reverse=True)

        for leader_name, dossier_file, story in stories:
            anchor = _slugify(story.title)
            summary = _get_first_sentence(story.narrative)
            # Format: - [Headline](dossier_link#anchor) — Summary
            sections.append(
                f"- [{story.title}]({_dossier_url(dossier_file, anchor)}) — {summary}"
            )

        sections.append("")


def _render_regional_briefs(
    brief: WeeklyBrief,
    sections: list[str],
    country_subregion: dict[str, str],
    region_display_names: dict[str, str],
    region_order: list[str],
):
    """
    Render per-leader briefs grouped by region.

    For each leader:
    - Executive summary (condensed)
    - Top stories + first international/domestic
    - Between the Lines (summarized)
    """
    # Group dossiers by region
    region_dossiers: dict[str, list[LeaderDossier]] = {}
    for dossier in brief.leader_dossiers:
        country = dossier.leader.country
        region = country_subregion.get(country, dossier.leader.region)
        if region not in region_dossiers:
            region_dossiers[region] = []
        region_dossiers[region].append(dossier)

    if not region_dossiers:
        return

    sections.append("## Regional Briefs")
    sections.append("")

    # Render regions in order
    first_region = True
    for region in region_order:
        if region not in region_dossiers:
            continue

        if not first_region:
            sections.append("---")
            sections.append("")
        first_region = False

        region_name = region_display_names.get(region, region.replace("_", " ").title())
        sections.append(f"### {region_name}")
        sections.append("")

        # Sort dossiers by country name
        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)

        for i, dossier in enumerate(dossiers):
            if i > 0:
                sections.append("* * *")
                sections.append("")
            _render_leader_brief(dossier, sections)

    # Render any regions not in the order list
    for region in sorted(region_dossiers.keys()):
        if region in region_order:
            continue

        if not first_region:
            sections.append("---")
            sections.append("")
        first_region = False

        region_name = region_display_names.get(region, region.replace("_", " ").title())
        sections.append(f"### {region_name}")
        sections.append("")
        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)
        for i, dossier in enumerate(dossiers):
            if i > 0:
                sections.append("* * *")
                sections.append("")
            _render_leader_brief(dossier, sections)


def _render_leader_brief(dossier: LeaderDossier, sections: list[str]):
    """Render a single leader's brief within a regional section."""
    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "🌍")
    safe_name = dossier.leader.name.lower().replace(" ", "_")
    dossier_file = f"{safe_name}.md"

    # Leader header with link to full dossier
    sections.append(
        f"#### [{emoji} {dossier.leader.country} / {_display_name(dossier.leader.name)}]({_dossier_url(dossier_file)})"
    )
    sections.append("")

    # Executive summary (if available)
    if dossier.executive_summary:
        sections.append(f"> {dossier.executive_summary}")
        sections.append("")

    # Collect stories: main + first few international/domestic
    all_stories = list(dossier.main_stories)
    if dossier.international_stories:
        all_stories.extend(dossier.international_stories[:2])
    if dossier.domestic_stories:
        all_stories.extend(dossier.domestic_stories[:2])

    # Deduplicate by story ID (in case same story appears in multiple lists)
    seen_ids: set[str] = set()
    unique_stories = []
    for story in all_stories:
        if story.id not in seen_ids:
            seen_ids.add(story.id)
            unique_stories.append(story)

    # Filter out very short stories (less than 3 sentences)
    MIN_NARRATIVE_LENGTH = 100  # characters
    filtered_stories = [s for s in unique_stories if len(s.narrative) >= MIN_NARRATIVE_LENGTH]

    # Render stories as bullet points
    for story in filtered_stories[:5]:  # Limit to 5 stories per leader
        anchor = _slugify(story.title)
        summary = _get_first_sentence(story.narrative)
        sections.append(
            f"- [{story.title}]({_dossier_url(dossier_file, anchor)}) — {summary}"
        )

    if filtered_stories:
        sections.append("")

    # Between the Lines (first 2 bullets)
    if dossier.between_the_lines:
        sections.append("**Between the Lines:**")
        for bullet in dossier.between_the_lines[:2]:
            sections.append(f"- {bullet}")
        sections.append("")


def load_brief(brief_dir: Path) -> Optional[WeeklyBrief]:
    """
    Load a brief from disk.

    Args:
        brief_dir: Path to brief directory

    Returns:
        WeeklyBrief or None if not found
    """
    output_path = brief_dir / "output.json"

    if not output_path.exists():
        logger.warning(f"Brief not found: {output_path}")
        return None

    with open(output_path) as f:
        data = json.load(f)

    # Reconstruct WeeklyBrief
    return _deserialize_brief(data)


def _deserialize_story(data: dict) -> Story:
    """Deserialize a Story from JSON data."""
    scope_str = data.get("scope", "domestic")
    try:
        scope = StoryScope(scope_str)
    except ValueError:
        scope = StoryScope.DOMESTIC

    return Story(
        id=data.get("id", ""),
        title=data.get("title", ""),
        narrative=data.get("narrative", ""),
        scope=scope,
        source_count=data.get("source_count", 0),
        has_wire=data.get("has_wire", False),
        score=data.get("score", 0.0),
        source_refs=data.get("source_refs", {}),
        entities=data.get("entities", []),
        cluster_id=data.get("cluster_id", ""),
        contributing_leaders=data.get("contributing_leaders", []),
    )


def _deserialize_brief(data: dict) -> WeeklyBrief:
    """Deserialize a brief from JSON data, supporting both old and new formats."""
    from .config import (
        LeaderConfig,
        SourceConfig,
        LeaderAction,
        EventType,
    )

    # Helper to parse datetime
    def parse_datetime(val):
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        return datetime.fromisoformat(val)

    # Detect format: old format has "cross_cutting_threads" (unique to old format)
    is_old_format = "cross_cutting_threads" in data

    # Deserialize leader dossiers
    dossiers = []
    for d in data.get("leader_dossiers", []):
        leader_data = d.get("leader", {})

        # Reconstruct domestic sources
        domestic_sources = [
            SourceConfig(
                name=s.get("name", ""),
                url=s.get("url", ""),
                language=s.get("language", "en"),
                source_type=s.get("source_type", "domestic"),
                rss_url=s.get("rss_url"),
            )
            for s in leader_data.get("domestic_sources", [])
        ]

        leader = LeaderConfig(
            name=leader_data.get("name", ""),
            title=leader_data.get("title", ""),
            country=leader_data.get("country", ""),
            region=leader_data.get("region", ""),
            domestic_sources=domestic_sources,
        )

        # Check if this dossier is old format
        dossier_is_old = "key_actions" in d

        if dossier_is_old:
            # Old format -> convert to new
            dossier = _deserialize_old_dossier(d, leader)
        else:
            # New format
            dossier = LeaderDossier(
                leader=leader,
                reporting_period=d.get("reporting_period", ""),
                executive_summary=d.get("executive_summary", ""),
                main_stories=[_deserialize_story(s) for s in d.get("main_stories", [])],
                international_stories=[_deserialize_story(s) for s in d.get("international_stories", [])],
                domestic_stories=[_deserialize_story(s) for s in d.get("domestic_stories", [])],
                between_the_lines=d.get("between_the_lines", []),
                articles=[],
                underlying_events=[],
                source_quality_notes=d.get("source_quality_notes", ""),
                generated_at=parse_datetime(d.get("generated_at")),
            )

        dossiers.append(dossier)

    if is_old_format:
        # Old format -> map to new WeeklyBrief structure
        return WeeklyBrief(
            date_range=data.get("date_range", ""),
            generated_at=parse_datetime(data.get("generated_at")),
            main_stories=[],  # Old format had no story lists at aggregate level
            international_stories=[],
            domestic_stories=[],
            between_the_lines=[],
            executive_summary="",
            leader_dossiers=dossiers,
            methodology_notes=data.get("methodology_notes", ""),
            source_quality_notes=data.get("source_quality_notes", ""),
        )

    # New format
    return WeeklyBrief(
        date_range=data.get("date_range", ""),
        generated_at=parse_datetime(data.get("generated_at")),
        main_stories=[_deserialize_story(s) for s in data.get("main_stories", [])],
        international_stories=[_deserialize_story(s) for s in data.get("international_stories", [])],
        domestic_stories=[_deserialize_story(s) for s in data.get("domestic_stories", [])],
        between_the_lines=data.get("between_the_lines", []),
        executive_summary=data.get("executive_summary", ""),
        leader_dossiers=dossiers,
        methodology_notes=data.get("methodology_notes", ""),
        source_quality_notes=data.get("source_quality_notes", ""),
    )


def _deserialize_old_dossier(data: dict, leader) -> LeaderDossier:
    """Convert an old-format dossier (key_actions) to new format (stories)."""
    from .config import LeaderAction, EventType

    # Convert key_actions to main_stories
    main_stories = []
    for action_data in data.get("key_actions", []):
        try:
            event_type_str = action_data.get("event_type", "other")
            scope = StoryScope.INTERNATIONAL if event_type_str in (
                "international_visit", "bilateral_agreement"
            ) else StoryScope.DOMESTIC
        except Exception:
            scope = StoryScope.DOMESTIC

        main_stories.append(Story(
            id=f"legacy-{len(main_stories)}",
            title=action_data.get("description", "")[:80],
            narrative=action_data.get("description", ""),
            scope=scope,
            source_count=len(action_data.get("source_articles", [])),
            has_wire=False,
            score=0.5,
            source_refs=action_data.get("source_refs", {}),
        ))

    # Map old context fields to between_the_lines
    btl = []
    if data.get("assessment"):
        btl.append(data["assessment"])

    return LeaderDossier(
        leader=leader,
        reporting_period=data.get("reporting_period", ""),
        main_stories=main_stories,
        international_stories=[],
        domestic_stories=[],
        between_the_lines=btl,
        articles=[],
        underlying_events=[],
        source_quality_notes=data.get("source_quality_notes", ""),
    )


def load_latest_brief() -> Optional[WeeklyBrief]:
    """Load the most recent brief."""
    if not BRIEFS_DIR.exists():
        return None

    # Find most recent directory
    dirs = sorted(BRIEFS_DIR.iterdir(), reverse=True)

    for d in dirs:
        if d.is_dir() and (d / "output.json").exists():
            return load_brief(d)

    return None


def list_briefs() -> list[dict]:
    """List all available briefs with metadata."""
    if not BRIEFS_DIR.exists():
        return []

    briefs = []

    for d in sorted(BRIEFS_DIR.iterdir(), reverse=True):
        if not d.is_dir():
            continue

        meta_path = d / "meta.json"
        if meta_path.exists():
            with open(meta_path) as f:
                meta = json.load(f)
            meta["path"] = str(d)
            briefs.append(meta)

    return briefs


# =============================================================================
# INDIVIDUAL DOSSIER PERSISTENCE (for resume capability)
# =============================================================================

def save_dossier(dossier: LeaderDossier, output_dir: Path) -> Path:
    """
    Save an individual leader dossier for resume capability.

    Args:
        dossier: The LeaderDossier to save
        output_dir: Directory to save in (typically briefs/YYYYMMDD)

    Returns:
        Path to the saved dossier file
    """
    dossier_dir = output_dir / "dossiers"
    dossier_dir.mkdir(parents=True, exist_ok=True)

    # Create safe filename from leader name
    safe_name = dossier.leader.name.lower().replace(" ", "_")
    dossier_path = dossier_dir / f"{safe_name}.json"

    # Serialize dossier
    dossier_data = asdict(dossier)

    with open(dossier_path, "w") as f:
        json.dump(dossier_data, f, default=_serialize, indent=2)

    logger.info(f"Saved dossier for {dossier.leader.name} to {dossier_path}")

    return dossier_path


def load_dossier(path: Path, leader) -> Optional[LeaderDossier]:
    """
    Load an individual leader dossier from file.

    Args:
        path: Path to dossier JSON file
        leader: LeaderConfig for this leader

    Returns:
        LeaderDossier or None if not found/invalid
    """
    if not path.exists():
        return None

    try:
        with open(path) as f:
            data = json.load(f)

        return _deserialize_dossier(data, leader)

    except Exception as e:
        logger.warning(f"Failed to load dossier from {path}: {e}")
        return None


def _deserialize_dossier(data: dict, leader) -> LeaderDossier:
    """Deserialize a dossier from JSON data, supporting both formats."""

    # Helper to parse datetime
    def parse_datetime(val):
        if val is None:
            return None
        if isinstance(val, datetime):
            return val
        return datetime.fromisoformat(val)

    # Detect old format
    if "key_actions" in data:
        return _deserialize_old_dossier(data, leader)

    # New format
    return LeaderDossier(
        leader=leader,
        reporting_period=data.get("reporting_period", ""),
        executive_summary=data.get("executive_summary", ""),
        main_stories=[_deserialize_story(s) for s in data.get("main_stories", [])],
        international_stories=[_deserialize_story(s) for s in data.get("international_stories", [])],
        domestic_stories=[_deserialize_story(s) for s in data.get("domestic_stories", [])],
        between_the_lines=data.get("between_the_lines", []),
        articles=[],  # Don't reload articles for resume
        underlying_events=[],
        source_quality_notes=data.get("source_quality_notes", ""),
        generated_at=parse_datetime(data.get("generated_at")),
    )


async def generate_email(brief: WeeklyBrief, brief_dir: Path) -> Path:
    """
    Generate an HTML email digest from a brief and write it to brief_dir.

    Calls the EmailDigestAgent to condense the brief, then renders the
    result into an HTML email template.

    Args:
        brief: The WeeklyBrief to condense
        brief_dir: Directory to write email.html into

    Returns:
        Path to the saved email.html file
    """
    from .agents.email_digest import EmailDigestAgent
    from .email_template import render_email_html

    logger.info("Generating email digest")

    agent = EmailDigestAgent()
    digest = await agent.generate_digest(brief)

    brief_date = _brief_title(brief)  # e.g., "Week of February 8, 2026"

    # Build the canonical brief URL
    date = _brief_date(brief)  # e.g., "2026-02-08"
    brief_url = f"https://idealbrief.org/briefs/{date}/brief/"

    html = render_email_html(digest, brief_date, brief_url)

    email_path = brief_dir / "email.html"
    with open(email_path, "w") as f:
        f.write(html)

    size_kb = len(html.encode("utf-8")) / 1024
    logger.info(f"Email HTML saved to {email_path} ({size_kb:.1f} KB)")

    return email_path


def get_existing_dossiers(output_dir: Path, leaders: list) -> dict:
    """
    Check for existing dossiers in output directory.

    Used for resume capability - returns dossiers that are already complete.

    Args:
        output_dir: Directory to check (typically briefs/YYYYMMDD)
        leaders: List of LeaderConfig objects

    Returns:
        Dict mapping leader name to LeaderDossier for completed dossiers
    """
    dossier_dir = output_dir / "dossiers"

    if not dossier_dir.exists():
        return {}

    existing = {}

    for leader in leaders:
        safe_name = leader.name.lower().replace(" ", "_")
        dossier_path = dossier_dir / f"{safe_name}.json"

        if dossier_path.exists():
            dossier = load_dossier(dossier_path, leader)
            if dossier:
                existing[leader.name] = dossier
                logger.info(f"Found existing dossier for {leader.name}")

    return existing
