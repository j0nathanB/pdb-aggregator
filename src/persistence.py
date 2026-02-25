"""
Persistence layer for saving and loading briefs.

Briefs are stored in a structured directory format:
    briefs/
        YYYYMMDD/
            overview.mdx      # Human-readable Mintlify page
            dossiers.json     # Structured leader data
            meta.json         # Brief metadata
            output.json       # Full serialized output
            dossiers/
                leader_name.mdx  # Individual leader dossier pages
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

    # 4. Generate and save Mintlify overview page
    overview_path = output_dir / "overview.mdx"
    overview_content = _generate_markdown(brief)
    with open(overview_path, "w") as f:
        f.write(overview_content)

    # 5. Save individual leader dossier Mintlify pages
    for dossier in brief.leader_dossiers:
        save_dossier_markdown(dossier, output_dir)

    logger.info(f"Brief saved: {output_dir}")

    return output_dir


def update_mint_json(brief: WeeklyBrief, brief_dir_name: str, mint_json_path: Path) -> None:
    """
    Update mint.json navigation when a new brief is published.

    Adds the new brief as the "Latest Brief" and moves the previous latest
    to the Archives section.

    Args:
        brief: The new WeeklyBrief
        brief_dir_name: Directory name for this brief (e.g., "20260215" or "2026-02-15")
        mint_json_path: Path to mint.json
    """
    if not mint_json_path.exists():
        logger.warning(f"mint.json not found at {mint_json_path}, skipping nav update")
        return

    with open(mint_json_path) as f:
        config = json.load(f)

    title = _brief_title(brief)

    # Determine the brief date path segment (YYYY-MM-DD format)
    if len(brief_dir_name) == 8 and brief_dir_name.isdigit():
        date_path = f"{brief_dir_name[:4]}-{brief_dir_name[4:6]}-{brief_dir_name[6:]}"
    else:
        date_path = brief_dir_name

    overview_path = f"briefs/{date_path}/overview"

    # Build dossier page paths
    dossier_pages = []
    for dossier in brief.leader_dossiers:
        safe_name = dossier.leader.name.lower().replace(" ", "_")
        dossier_pages.append(f"briefs/{date_path}/dossiers/{safe_name}")

    # Find current "Latest Brief" and "Dossiers" groups to archive them
    nav = config.get("navigation", [])
    old_latest_pages = []
    old_dossier_pages = []
    old_latest_title = None

    remaining_nav = []
    for group in nav:
        group_name = group.get("group", "")
        if group_name == "Latest Brief":
            old_latest_pages = group.get("pages", [])
            # Try to find the title from the path (e.g., briefs/2026-02-08/overview)
            if old_latest_pages:
                # Extract date from path to build archive title
                import re
                m = re.search(r"briefs/(\d{4}-\d{2}-\d{2})/", old_latest_pages[0])
                if m:
                    try:
                        dt = datetime.strptime(m.group(1), "%Y-%m-%d")
                        old_latest_title = f"Week of {dt.strftime('%B %-d, %Y')}"
                    except ValueError:
                        old_latest_title = f"Week of {m.group(1)}"
        elif group_name == "Dossiers":
            old_dossier_pages = group.get("pages", [])
        else:
            remaining_nav.append(group)

    # Build new navigation
    new_nav = []

    # Latest Brief group
    new_nav.append({
        "group": "Latest Brief",
        "pages": [overview_path],
    })

    # Dossiers group
    new_nav.append({
        "group": "Dossiers",
        "pages": dossier_pages,
    })

    # Re-add Archives and existing archive groups
    for group in remaining_nav:
        new_nav.append(group)

    # If there was a previous latest brief, add it as an archive group
    if old_latest_pages and old_latest_title and old_latest_pages[0] != overview_path:
        archive_group = {
            "group": old_latest_title,
            "pages": old_latest_pages + old_dossier_pages,
        }
        new_nav.append(archive_group)

    config["navigation"] = new_nav

    # Update root redirect to point to new latest brief
    config["redirects"] = [
        {"source": "/", "destination": f"/{overview_path}"},
    ]

    with open(mint_json_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    logger.info(f"Updated mint.json navigation with brief: {title}")


def update_docs_json(brief: WeeklyBrief, brief_dir_name: str, docs_json_path: Path) -> None:
    """
    Update docs.json navigation when a new brief is published.

    Navigates the tab-based structure: tabs[0] ("Middle Powers") contains
    groups for Latest Brief, Dossiers, Archives, and archived week groups.

    Args:
        brief: The new WeeklyBrief
        brief_dir_name: Directory name for this brief (e.g., "2026-02-15")
        docs_json_path: Path to docs.json
    """
    if not docs_json_path.exists():
        logger.warning(f"docs.json not found at {docs_json_path}, skipping nav update")
        return

    with open(docs_json_path) as f:
        config = json.load(f)

    title = _brief_title(brief)

    # Determine the brief date path segment (YYYY-MM-DD format)
    if len(brief_dir_name) == 8 and brief_dir_name.isdigit():
        date_path = f"{brief_dir_name[:4]}-{brief_dir_name[4:6]}-{brief_dir_name[6:]}"
    else:
        date_path = brief_dir_name

    overview_path = f"briefs/{date_path}/overview"

    # Build dossier page paths
    dossier_pages = []
    for dossier in brief.leader_dossiers:
        safe_name = dossier.leader.name.lower().replace(" ", "_")
        dossier_pages.append(f"briefs/{date_path}/dossiers/{safe_name}")

    # Find the Middle Powers tab
    tabs = config.get("navigation", {}).get("tabs", [])
    mp_tab = None
    for tab in tabs:
        if tab.get("tab") == "Middle Powers":
            mp_tab = tab
            break

    if mp_tab is None:
        logger.warning("Middle Powers tab not found in docs.json, skipping nav update")
        return

    groups = mp_tab.get("groups", [])

    # Extract current Latest Brief and Dossiers groups to archive them
    old_latest_pages = []
    old_dossier_pages = []
    old_latest_title = None
    remaining_groups = []

    for group in groups:
        group_name = group.get("group", "")
        if group_name == "Latest Brief":
            old_latest_pages = group.get("pages", [])
            if old_latest_pages:
                import re
                m = re.search(r"briefs/(\d{4}-\d{2}-\d{2})/", old_latest_pages[0])
                if m:
                    try:
                        dt = datetime.strptime(m.group(1), "%Y-%m-%d")
                        old_latest_title = f"Week of {dt.strftime('%B %-d, %Y')}"
                    except ValueError:
                        old_latest_title = f"Week of {m.group(1)}"
        elif group_name == "Dossiers":
            old_dossier_pages = group.get("pages", [])
        else:
            remaining_groups.append(group)

    # Build new groups list
    new_groups = []

    # Latest Brief
    new_groups.append({
        "group": "Latest Brief",
        "pages": [overview_path],
    })

    # Dossiers
    if dossier_pages:
        new_groups.append({
            "group": "Dossiers",
            "pages": dossier_pages,
        })

    # Re-add Archives and existing archive groups
    for group in remaining_groups:
        new_groups.append(group)

    # If there was a previous latest brief, insert it as an archive group
    # (right after Archives, before older archive groups)
    if old_latest_pages and old_latest_title and old_latest_pages[0] != overview_path:
        archive_group = {
            "group": old_latest_title,
            "pages": old_latest_pages + old_dossier_pages,
        }
        # Find Archives group index and insert after it
        archives_idx = None
        for i, g in enumerate(new_groups):
            if g.get("group") == "Archives":
                archives_idx = i
                break
        if archives_idx is not None:
            new_groups.insert(archives_idx + 1, archive_group)
        else:
            new_groups.append(archive_group)

    mp_tab["groups"] = new_groups

    # Update root redirect to point to new latest brief
    config["redirects"] = [
        {"source": "/", "destination": f"/{overview_path}"},
    ]

    with open(docs_json_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    logger.info(f"Updated docs.json navigation with brief: {title}")


def update_archives_page(docs_json_path: Path) -> None:
    """
    Regenerate archives/index.mdx from the docs.json navigation groups.

    Reads the Middle Powers tab groups and builds a list of all briefs
    (latest + archived weeks).

    Args:
        docs_json_path: Path to docs.json (archives dir is resolved relative to it)
    """
    if not docs_json_path.exists():
        logger.warning(f"docs.json not found at {docs_json_path}, skipping archives update")
        return

    with open(docs_json_path) as f:
        config = json.load(f)

    # Find the Middle Powers tab
    tabs = config.get("navigation", {}).get("tabs", [])
    mp_tab = None
    for tab in tabs:
        if tab.get("tab") == "Middle Powers":
            mp_tab = tab
            break

    if mp_tab is None:
        return

    groups = mp_tab.get("groups", [])

    # Collect all brief entries (Latest Brief + archive week groups)
    brief_entries = []
    for group in groups:
        group_name = group.get("group", "")
        pages = group.get("pages", [])
        if not pages:
            continue

        if group_name == "Latest Brief":
            # Extract title from the overview path date
            overview = pages[0]
            import re
            m = re.search(r"briefs/(\d{4}-\d{2}-\d{2})/", overview)
            if m:
                try:
                    dt = datetime.strptime(m.group(1), "%Y-%m-%d")
                    entry_title = f"Week of {dt.strftime('%B %-d, %Y')}"
                except ValueError:
                    entry_title = f"Week of {m.group(1)}"
                brief_entries.append((m.group(1), entry_title, overview))
        elif group_name.startswith("Week of"):
            overview = pages[0]
            import re
            m = re.search(r"briefs/(\d{4}-\d{2}-\d{2})/", overview)
            date_key = m.group(1) if m else "0000-00-00"
            brief_entries.append((date_key, group_name, overview))

    # Sort by date descending
    brief_entries.sort(key=lambda e: e[0], reverse=True)

    # Build the archives page
    sections = []
    sections.append("---")
    sections.append('title: "Archives"')
    sections.append('description: "Past weekly intelligence briefs"')
    sections.append("---")
    sections.append("")
    sections.append("# Archives")
    sections.append("")
    sections.append("Past editions of The Middle Powers Monitor.")
    sections.append("")

    for _, entry_title, overview_path in brief_entries:
        sections.append(f"- [{entry_title}](/{overview_path})")

    sections.append("")

    # Write archives page
    archives_dir = docs_json_path.parent / "archives"
    archives_dir.mkdir(parents=True, exist_ok=True)
    index_path = archives_dir / "index.mdx"
    with open(index_path, "w") as f:
        f.write("\n".join(sections))

    logger.info(f"Updated archives page with {len(brief_entries)} briefs")


def _generate_dossier_markdown(dossier: LeaderDossier, brief_date: str = "") -> str:
    """Generate standalone Mintlify .mdx for an individual leader dossier."""
    sections = []

    # Escape YAML special characters in strings
    leader_name = _display_name(dossier.leader.name).replace('"', '\\"')
    title_text = f"{dossier.leader.country} — {_display_name(dossier.leader.name)}, {dossier.leader.title}"
    title_escaped = title_text.replace('"', '\\"')

    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "🌍")

    # Mintlify frontmatter
    sections.append("---")
    sections.append(f"title: \"{title_escaped}\"")
    sections.append(f"sidebarTitle: \"{emoji} {dossier.leader.country} — {leader_name}\"")
    sections.append("---")
    sections.append("")

    # Header
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

    # Generated timestamp at the bottom
    sections.append("---")
    sections.append("")
    if dossier.generated_at:
        sections.append(f"*Generated: {dossier.generated_at.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(sections)


def save_dossier_markdown(dossier: LeaderDossier, output_dir: Path) -> Path:
    """
    Save an individual leader dossier as a Mintlify .mdx page.

    Args:
        dossier: The LeaderDossier to save
        output_dir: Brief output directory (typically briefs/YYYYMMDD)

    Returns:
        Path to the saved .mdx file
    """
    dossier_dir = output_dir / "dossiers"
    dossier_dir.mkdir(parents=True, exist_ok=True)

    safe_name = dossier.leader.name.lower().replace(" ", "_")
    mdx_path = dossier_dir / f"{safe_name}.mdx"

    markdown = _generate_dossier_markdown(dossier)
    with open(mdx_path, "w") as f:
        f.write(markdown)

    logger.info(f"Saved dossier markdown for {dossier.leader.name} to {mdx_path}")
    return mdx_path


def _format_story_refs(story: Story) -> str:
    """Format source references for a story."""
    refs_parts = []
    for src_name, urls in story.source_refs.items():
        links = ",".join(f"[{i+1}]({u})" for i, u in enumerate(urls))
        refs_parts.append(f"{src_name} {links}")
    return f" ({'; '.join(refs_parts)})" if refs_parts else ""


def _dossier_url(filename: str, anchor: str = "") -> str:
    """Convert a dossier filename to a Mintlify-compatible relative URL.

    Converts 'name.mdx' to 'dossiers/name' (drops extension, relative from overview).
    Optionally appends an anchor fragment.
    """
    base = filename.removesuffix(".mdx").removesuffix(".md")
    url = f"dossiers/{base}"
    if anchor:
        url = f"{url}#{anchor}"
    return url


def _slugify(text: str) -> str:
    """Convert text to a URL slug matching Jekyll's default slugify filter."""
    import re
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')




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
    refs = _format_story_refs(story)
    sections.append(f"### {story.title}")
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
    """Generate the full brief overview page as Mintlify .mdx."""
    from .config import COUNTRY_SUBREGION, REGION_DISPLAY_NAMES, REGION_ORDER

    sections = []

    title = _brief_title(brief)

    # Mintlify frontmatter
    sections.append("---")
    sections.append(f"title: \"{title}\"")
    sections.append(f"description: \"Weekly intelligence brief covering Middle Power leadership\"")
    sections.append(f"sidebarTitle: \"Overview\"")
    sections.append("---")
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
                sections.append("---")
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
                sections.append("---")
                sections.append("")
            _render_leader_brief(dossier, sections)


def _render_leader_brief(dossier: LeaderDossier, sections: list[str]):
    """Render a single leader's brief within a regional section."""
    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "🌍")
    safe_name = dossier.leader.name.lower().replace(" ", "_")
    dossier_file = f"{safe_name}.mdx"

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

    # Build the canonical brief URL (Mintlify routes)
    date = _brief_date(brief)  # e.g., "2026-02-08"
    brief_url = f"https://idealbrief.org/briefs/{date}/overview"

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
