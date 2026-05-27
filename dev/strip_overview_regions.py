"""Strip the trailing '## Regions' section (and preceding '---') from overview.mdx files."""
import re
from pathlib import Path

BRIEFS_ROOT = Path(__file__).resolve().parents[1] / "site" / "briefs"

# Match: optional blank lines, ---, blank, ## Regions, then everything to EOF
PATTERN = re.compile(r'\n+(?:---\n\n)?## Regions\n.*\Z', re.DOTALL)


def main() -> None:
    for brief_dir in sorted(BRIEFS_ROOT.iterdir()):
        if not brief_dir.is_dir() or brief_dir.name.startswith(("_", ".")):
            continue
        overview = brief_dir / "overview.mdx"
        if not overview.exists():
            continue
        text = overview.read_text()
        new_text, n = PATTERN.subn("\n", text)
        if n:
            overview.write_text(new_text)
            print(f"{brief_dir.name}: stripped Regions section")
        else:
            print(f"{brief_dir.name}: no Regions section found")


if __name__ == "__main__":
    main()
