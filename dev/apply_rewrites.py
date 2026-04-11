#!/usr/bin/env python3
"""Replace published brief summaries with edited rewrites from dev/summary_rewrite/."""

from pathlib import Path

REWRITE_DIR = Path("dev/summary_rewrite")
BRIEFS_DIR = Path("site/briefs")

REGION_MAP = {
    "regional_summary_asia-pacific.md": "asia-pacific.mdx",
    "regional_summary_frontline-eastern-europe.md": "frontline-eastern-europe.mdx",
    "regional_summary_near-east-south-asia.md": "near-east-south-asia.mdx",
    "regional_summary_the-americas.md": "the-americas.mdx",
    "regional_summary_western-europe.md": "western-europe.mdx",
}


def parse_edited(path: Path) -> tuple[str, str]:
    """Return (title, prose). Title is line 1 with **/# markdown stripped."""
    text = path.read_text().strip()
    lines = text.split("\n")
    raw_title = lines[0].strip()

    # Strip markdown formatting from title
    if raw_title.startswith("**") and raw_title.endswith("**"):
        title = raw_title[2:-2].strip()
    elif raw_title.startswith("# "):
        title = raw_title[2:].strip()
    else:
        title = raw_title

    # Prose begins after the first blank line following the title
    prose_start = 1
    while prose_start < len(lines) and lines[prose_start].strip() == "":
        prose_start += 1
    prose = "\n".join(lines[prose_start:]).strip()

    return title, prose


def replace_section(content: str, start_marker: str, end_marker: str,
                    title: str, prose: str, file_label: str) -> str | None:
    """Replace the lines between start_marker and end_marker with title + prose.
    Preserves any trailing `---` separator that was before end_marker."""
    lines = content.split("\n")

    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if start_idx is None and line.startswith(start_marker):
            start_idx = i
        elif start_idx is not None and line.startswith(end_marker):
            end_idx = i
            break

    if start_idx is None:
        print(f"  ERROR: {file_label}: could not find '{start_marker}'")
        return None
    if end_idx is None:
        print(f"  ERROR: {file_label}: could not find '{end_marker}'")
        return None

    # Check if original section had a `---` separator just before end_marker
    # Scan back from end_idx through blank lines to find the last non-blank line
    has_separator = False
    scan = end_idx - 1
    while scan > start_idx and lines[scan].strip() == "":
        scan -= 1
    if scan > start_idx and lines[scan].strip() == "---":
        has_separator = True

    # Build replacement: start_marker line, blank, title, blank, prose, blank,
    # (optional --- + blank), end_marker line
    new_section = [
        lines[start_idx],
        "",
        f"**{title}**",
        "",
        prose,
        "",
    ]
    if has_separator:
        new_section.extend(["---", ""])
    new_section.append(lines[end_idx])

    new_lines = lines[:start_idx] + new_section + lines[end_idx + 1:]
    return "\n".join(new_lines)


def apply_overview(date: str, title: str, prose: str) -> bool:
    overview = BRIEFS_DIR / date / "overview.mdx"
    if not overview.exists():
        print(f"  SKIP overview (not found)")
        return False

    content = overview.read_text()
    new_content = replace_section(
        content, "## Week of", "## Regions", title, prose,
        f"{date}/overview.mdx",
    )
    if new_content is None:
        return False
    overview.write_text(new_content)
    print(f"  overview.mdx: \"{title}\"")
    return True


def apply_regional(date: str, mdx_file: str, title: str, prose: str) -> bool:
    mdx_path = BRIEFS_DIR / date / mdx_file
    if not mdx_path.exists():
        print(f"  SKIP {mdx_file} (not found)")
        return False

    content = mdx_path.read_text()
    new_content = replace_section(
        content, "## Regional Summary", "## Country Summaries", title, prose,
        f"{date}/{mdx_file}",
    )
    if new_content is None:
        return False
    mdx_path.write_text(new_content)
    print(f"  {mdx_file}: \"{title}\"")
    return True


def main():
    dates = sorted(d.name for d in REWRITE_DIR.iterdir() if d.is_dir() and d.name.startswith("2026"))
    total = 0
    errors = 0

    for date in dates:
        edited_dir = REWRITE_DIR / date / "edited"
        if not edited_dir.exists():
            continue

        brief_dir = BRIEFS_DIR / date
        if not brief_dir.exists():
            print(f"SKIP {date}: no brief folder")
            continue

        print(f"\n{date}:")

        exec_path = edited_dir / "executive_summary.md"
        if exec_path.exists():
            title, prose = parse_edited(exec_path)
            if apply_overview(date, title, prose):
                total += 1
            else:
                errors += 1

        for region_file, mdx_file in REGION_MAP.items():
            region_path = edited_dir / region_file
            if region_path.exists():
                title, prose = parse_edited(region_path)
                if apply_regional(date, mdx_file, title, prose):
                    total += 1
                else:
                    errors += 1

    print(f"\nDone: {total} files updated, {errors} errors")


if __name__ == "__main__":
    main()
