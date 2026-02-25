#!/usr/bin/env python3
"""
One-time migration script: convert existing briefs from Jekyll to Mintlify format.

Reads briefs from briefs/YYYYMMDD/output.json (raw pipeline output),
converts them to Mintlify-compatible .mdx pages, and writes to
briefs/YYYY-MM-DD/overview.mdx + briefs/YYYY-MM-DD/dossiers/*.mdx.

Also rebuilds mint.json navigation from all migrated briefs.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path so we can import src modules
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.persistence import (
    _deserialize_brief,
    _brief_title,
    _brief_date,
    _slugify,
    _display_name,
    _format_date_range,
    _format_story_refs,
    _get_first_sentence,
    DISPLAY_NAMES,
)
from src.config import COUNTRY_EMOJI, COUNTRY_SUBREGION, REGION_DISPLAY_NAMES, REGION_ORDER


def strip_kramdown(text: str) -> str:
    """Remove kramdown-specific attribute markers like {: #anchor} and {: .class}."""
    return re.sub(r'\n\{:\s*[#.][^}]*\}\s*', '\n', text)


def generate_mintlify_overview(brief, brief_date_str: str) -> str:
    """Generate the main brief overview page as Mintlify .mdx."""
    sections = []

    title = _brief_title(brief)

    # Mintlify frontmatter (no layout, no nav_tree, no doc_type)
    sections.append("---")
    sections.append(f'title: "{title}"')
    sections.append(f'description: "Weekly intelligence brief covering Middle Power leadership"')
    sections.append(f'sidebarTitle: "Overview"')
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
    _render_regional_briefs(brief, sections, brief_date_str)

    # Footer
    sections.append("---")
    sections.append("")
    if brief.generated_at:
        sections.append(f"*Generated: {brief.generated_at.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(sections)


def generate_mintlify_dossier(dossier, brief_date_str: str) -> str:
    """Generate a single dossier page as Mintlify .mdx."""
    sections = []

    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "\U0001f30d")
    leader_name = _display_name(dossier.leader.name)
    title_text = f"{dossier.leader.country} \u2014 {leader_name}, {dossier.leader.title}"

    # Mintlify frontmatter
    sections.append("---")
    sections.append(f'title: "{title_text}"')
    sections.append(f'sidebarTitle: "{emoji} {dossier.leader.country} \u2014 {leader_name}"')
    sections.append("---")
    sections.append("")

    # Header
    sections.append(f"# {emoji} {dossier.leader.country}")
    sections.append(f"## {leader_name}, {dossier.leader.title}")
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

    # Footer
    sections.append("---")
    sections.append("")
    if dossier.generated_at:
        sections.append(f"*Generated: {dossier.generated_at.strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(sections)


def _render_story(story, sections: list[str]):
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


def _render_story_list(title: str, stories, sections: list[str]):
    """Render a titled list of stories."""
    if not stories:
        return
    sections.append(f"## {title}")
    sections.append("")
    for story in stories:
        _render_story(story, sections)


def _dossier_url(filename: str, anchor: str = "") -> str:
    """Build relative URL to a dossier from the overview page."""
    base = filename.removesuffix(".mdx").removesuffix(".md")
    url = f"dossiers/{base}"
    if anchor:
        url = f"{url}#{anchor}"
    return url


def _render_regional_briefs(brief, sections: list[str], brief_date_str: str):
    """Render per-leader briefs grouped by region."""
    region_dossiers: dict[str, list] = {}
    for dossier in brief.leader_dossiers:
        country = dossier.leader.country
        region = COUNTRY_SUBREGION.get(country, dossier.leader.region)
        if region not in region_dossiers:
            region_dossiers[region] = []
        region_dossiers[region].append(dossier)

    if not region_dossiers:
        return

    sections.append("## Regional Briefs")
    sections.append("")

    first_region = True
    for region in REGION_ORDER:
        if region not in region_dossiers:
            continue

        if not first_region:
            sections.append("---")
            sections.append("")
        first_region = False

        region_name = REGION_DISPLAY_NAMES.get(region, region.replace("_", " ").title())
        sections.append(f"### {region_name}")
        sections.append("")

        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)
        for i, dossier in enumerate(dossiers):
            if i > 0:
                sections.append("---")
                sections.append("")
            _render_leader_brief(dossier, sections)

    # Regions not in the canonical order
    for region in sorted(region_dossiers.keys()):
        if region in REGION_ORDER:
            continue
        if not first_region:
            sections.append("---")
            sections.append("")
        first_region = False
        region_name = REGION_DISPLAY_NAMES.get(region, region.replace("_", " ").title())
        sections.append(f"### {region_name}")
        sections.append("")
        dossiers = sorted(region_dossiers[region], key=lambda d: d.leader.country)
        for i, dossier in enumerate(dossiers):
            if i > 0:
                sections.append("---")
                sections.append("")
            _render_leader_brief(dossier, sections)


def _render_leader_brief(dossier, sections: list[str]):
    """Render a single leader's brief within a regional section."""
    emoji = COUNTRY_EMOJI.get(dossier.leader.country, "\U0001f30d")
    safe_name = dossier.leader.name.lower().replace(" ", "_")
    dossier_file = f"{safe_name}.mdx"

    sections.append(
        f"#### [{emoji} {dossier.leader.country} / {_display_name(dossier.leader.name)}]({_dossier_url(dossier_file)})"
    )
    sections.append("")

    if dossier.executive_summary:
        sections.append(f"> {dossier.executive_summary}")
        sections.append("")

    # Collect stories
    all_stories = list(dossier.main_stories)
    if dossier.international_stories:
        all_stories.extend(dossier.international_stories[:2])
    if dossier.domestic_stories:
        all_stories.extend(dossier.domestic_stories[:2])

    seen_ids: set[str] = set()
    unique_stories = []
    for story in all_stories:
        if story.id not in seen_ids:
            seen_ids.add(story.id)
            unique_stories.append(story)

    MIN_NARRATIVE_LENGTH = 100
    filtered_stories = [s for s in unique_stories if len(s.narrative) >= MIN_NARRATIVE_LENGTH]

    for story in filtered_stories[:5]:
        anchor = _slugify(story.title)
        summary = _get_first_sentence(story.narrative)
        sections.append(
            f"- [{story.title}]({_dossier_url(dossier_file, anchor)}) \u2014 {summary}"
        )

    if filtered_stories:
        sections.append("")

    if dossier.between_the_lines:
        sections.append("**Between the Lines:**")
        for bullet in dossier.between_the_lines[:2]:
            sections.append(f"- {bullet}")
        sections.append("")


def yyyymmdd_to_iso(dirname: str) -> str:
    """Convert '20260208' to '2026-02-08'."""
    return f"{dirname[:4]}-{dirname[4:6]}-{dirname[6:]}"


def migrate_brief(source_dir: Path, output_base: Path) -> Optional[dict]:
    """
    Migrate a single brief from briefs/YYYYMMDD/ to briefs/YYYY-MM-DD/.

    Returns nav metadata dict or None if no output.json found.
    """
    output_json = source_dir / "output.json"
    if not output_json.exists():
        print(f"  Skipping {source_dir.name}: no output.json")
        return None

    with open(output_json) as f:
        data = json.load(f)

    brief = _deserialize_brief(data)

    # Determine the ISO date for this brief
    brief_date_str = _brief_date(brief)
    title = _brief_title(brief)

    output_dir = output_base / brief_date_str
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate overview page
    overview_mdx = generate_mintlify_overview(brief, brief_date_str)
    overview_path = output_dir / "overview.mdx"
    with open(overview_path, "w") as f:
        f.write(overview_mdx)
    print(f"  Wrote {overview_path}")

    # Generate dossier pages
    dossier_dir = output_dir / "dossiers"
    dossier_dir.mkdir(parents=True, exist_ok=True)

    dossier_pages = []
    for dossier in brief.leader_dossiers:
        safe_name = dossier.leader.name.lower().replace(" ", "_")
        dossier_mdx = generate_mintlify_dossier(dossier, brief_date_str)
        dossier_path = dossier_dir / f"{safe_name}.mdx"
        with open(dossier_path, "w") as f:
            f.write(dossier_mdx)

        emoji = COUNTRY_EMOJI.get(dossier.leader.country, "\U0001f30d")
        dossier_pages.append({
            "path": f"briefs/{brief_date_str}/dossiers/{safe_name}",
            "label": f"{emoji} {dossier.leader.country} \u2014 {_display_name(dossier.leader.name)}",
        })

    print(f"  Wrote {len(dossier_pages)} dossier pages to {dossier_dir}")

    # Also copy JSON artifacts for the pipeline
    for json_file in ["meta.json", "dossiers.json", "output.json"]:
        src = source_dir / json_file
        if src.exists():
            import shutil
            shutil.copy2(str(src), str(output_dir / json_file))

    return {
        "date": brief_date_str,
        "title": title,
        "overview_path": f"briefs/{brief_date_str}/overview",
        "dossier_pages": dossier_pages,
    }


def build_mint_json(brief_metas: list[dict], mint_json_path: Path):
    """Build mint.json navigation from migrated brief metadata."""
    with open(mint_json_path) as f:
        config = json.load(f)

    # Sort briefs by date descending (latest first)
    brief_metas.sort(key=lambda m: m["date"], reverse=True)

    if not brief_metas:
        print("No briefs to add to navigation")
        return

    latest = brief_metas[0]
    archives = brief_metas[1:]

    # Build navigation groups
    nav = []

    # Latest Brief tab group
    latest_group = {
        "group": "Latest Brief",
        "pages": [latest["overview_path"]],
    }
    nav.append(latest_group)

    # Latest Brief dossiers group
    if latest["dossier_pages"]:
        dossier_group = {
            "group": "Dossiers",
            "pages": [dp["path"] for dp in latest["dossier_pages"]],
        }
        nav.append(dossier_group)

    # Archives tab group
    archive_group = {
        "group": "Archives",
        "pages": ["archives/index"],
    }
    nav.append(archive_group)

    # Archive brief groups (one per older brief)
    for meta in archives:
        group = {
            "group": meta["title"],
            "pages": [
                meta["overview_path"],
                *[dp["path"] for dp in meta["dossier_pages"]],
            ],
        }
        nav.append(group)

    config["navigation"] = nav

    # Set root redirect to latest brief
    config["redirects"] = [
        {"source": "/", "destination": f"/{latest['overview_path']}"},
    ]

    with open(mint_json_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Updated {mint_json_path} with {len(brief_metas)} briefs")


def create_archives_page(brief_metas: list[dict], output_base: Path):
    """Create the archives index page."""
    brief_metas.sort(key=lambda m: m["date"], reverse=True)

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

    for meta in brief_metas:
        sections.append(f"- [{meta['title']}](/{meta['overview_path']})")

    sections.append("")

    archives_dir = output_base.parent / "archives"
    archives_dir.mkdir(parents=True, exist_ok=True)
    index_path = archives_dir / "index.mdx"
    with open(index_path, "w") as f:
        f.write("\n".join(sections))

    print(f"Wrote {index_path}")


def build_docs_json(brief_metas: list[dict], docs_json_path: Path):
    """Build docs.json tab-based navigation from migrated brief metadata.

    Writes the Middle Powers tab with Latest Brief, Dossiers, Archives,
    and archived week groups. Preserves Trade/Climate placeholder tabs.
    """
    with open(docs_json_path) as f:
        config = json.load(f)

    brief_metas.sort(key=lambda m: m["date"], reverse=True)

    if not brief_metas:
        print("No briefs to add to navigation")
        return

    latest = brief_metas[0]
    archives = brief_metas[1:]

    # Build Middle Powers tab groups
    groups = []

    # Latest Brief
    groups.append({
        "group": "Latest Brief",
        "pages": [latest["overview_path"]],
    })

    # Dossiers for latest brief
    if latest["dossier_pages"]:
        groups.append({
            "group": "Dossiers",
            "pages": [dp["path"] for dp in latest["dossier_pages"]],
        })

    # Archives index
    groups.append({
        "group": "Archives",
        "pages": ["archives/index"],
    })

    # Archived week groups
    for meta in archives:
        groups.append({
            "group": meta["title"],
            "pages": [
                meta["overview_path"],
                *[dp["path"] for dp in meta["dossier_pages"]],
            ],
        })

    # Find or create Middle Powers tab
    tabs = config.get("navigation", {}).get("tabs", [])
    mp_tab = None
    for tab in tabs:
        if tab.get("tab") == "Middle Powers":
            mp_tab = tab
            break

    if mp_tab:
        mp_tab["groups"] = groups
    else:
        tabs.insert(0, {"tab": "Middle Powers", "groups": groups})

    if "navigation" not in config:
        config["navigation"] = {}
    config["navigation"]["tabs"] = tabs

    # Root redirect to latest brief
    config["redirects"] = [
        {"source": "/", "destination": f"/{latest['overview_path']}"},
    ]

    with open(docs_json_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Updated {docs_json_path} with {len(brief_metas)} briefs")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Migrate briefs to Mintlify format")
    parser.add_argument(
        "--docs-repo",
        type=Path,
        help="Path to the docs repo. Writes briefs and docs.json there instead of pdb.",
    )
    args = parser.parse_args()

    briefs_source = PROJECT_ROOT / "briefs"

    if args.docs_repo:
        briefs_output = args.docs_repo / "briefs"
        nav_json_path = args.docs_repo / "docs.json"
        archives_base = args.docs_repo
        use_docs_json = True
    else:
        briefs_output = PROJECT_ROOT / "briefs"
        nav_json_path = PROJECT_ROOT / "mint.json"
        archives_base = PROJECT_ROOT
        use_docs_json = False

    # Find all brief directories with output.json
    source_dirs = sorted(
        [d for d in briefs_source.iterdir()
         if d.is_dir() and d.name.isdigit() and len(d.name) == 8 and (d / "output.json").exists()],
        key=lambda d: d.name,
    )

    if not source_dirs:
        print("No briefs found to migrate")
        return

    print(f"Found {len(source_dirs)} briefs to migrate")

    brief_metas = []
    for source_dir in source_dirs:
        print(f"\nMigrating {source_dir.name}...")
        meta = migrate_brief(source_dir, briefs_output)
        if meta:
            brief_metas.append(meta)

    # Create archives page
    create_archives_page(brief_metas, archives_base / "briefs")

    # Update navigation config
    if use_docs_json:
        build_docs_json(brief_metas, nav_json_path)
    else:
        build_mint_json(brief_metas, nav_json_path)

    print(f"\nMigration complete: {len(brief_metas)} briefs converted")
    if args.docs_repo:
        print(f"Output written to: {args.docs_repo}")
        print("Next steps:")
        print(f"  1. cd {args.docs_repo} && npx mintlify dev   # Preview locally")
        print("  2. Verify navigation and links")
    else:
        print("Next steps:")
        print("  1. npx mintlify dev   # Preview locally")
        print("  2. Verify navigation and links")
        print("  3. Delete _briefs/, _layouts/, _sass/, _config.yml, Gemfile*")


if __name__ == "__main__":
    main()
