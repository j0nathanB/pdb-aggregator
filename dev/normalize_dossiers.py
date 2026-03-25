#!/usr/bin/env python3
"""Phase 1: Mechanical normalization of country dossier MDX files.

Transforms all 28 dossiers to match Latvia's format (sections I–VIII style):
- Convert ## headings to Roman numeral format: ## I. Descriptive title
- Convert ### sub-headings to **bold text** paragraphs (fixes Mintlify sidebar)
- Remove METADATA sections
- Remove STRUCTURAL CLAIMS blocks
- Normalize ALL CAPS titles to sentence case
- Convert #### headings to bold text
- Escape $ signs to prevent MDX LaTeX rendering
- Remove bold-text METADATA tables
- Clean up # title lines: strip template prefixes, pass markers, country name

Usage:
    python dev/normalize_dossiers.py --dry-run          # preview changes
    python dev/normalize_dossiers.py                     # apply to all dossiers
    python dev/normalize_dossiers.py latvia --dry-run    # single file
"""

import re
import sys
from pathlib import Path

DOSSIERS_DIR = Path(__file__).resolve().parent.parent / "site" / "dossiers"


def to_roman(n: int) -> str:
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    result = ""
    for val, numeral in vals:
        while n >= val:
            result += numeral
            n -= val
    return result


# Words/acronyms that must stay uppercase during case normalization
_KEEP_UPPER = {
    "NATO", "IMF", "OPEC", "EU", "UN", "GDP", "US", "USA", "UK", "USSR",
    "AUKUS", "PCC", "BJP", "RSS", "KGB", "CIA", "FBI", "ICJ", "EEZ",
    "AKP", "SPD", "KRS", "ROC", "PRC", "ASEAN", "GIUK", "MBZ", "COP30",
    "SD", "AAA", "FrP", "ABLV", "AML", "SPOLU", "PiS", "DNB", "A2/AD",
    "PT/PVEM", "ECR", "EPP", "FCMC", "NBS", "KNAB", "SAB", "ZZS",
    "DNA", "ANZAC", "OSCE", "WTO", "AIIB", "TPP", "CPTPP",
}


def _to_sentence_case(title: str) -> str:
    """Convert ALL CAPS or mixed-caps heading to sentence case.

    Preserves known acronyms/proper nouns and leaves already-lowercase
    titles unchanged.
    """
    alpha = [c for c in title if c.isalpha()]
    if not alpha:
        return title
    upper_ratio = sum(1 for c in alpha if c.isupper()) / len(alpha)
    if upper_ratio < 0.55:
        return title  # already in reasonable case

    words = title.split()
    result = []
    for i, word in enumerate(words):
        clean = word.strip(",:;—–-()'/")
        if clean in _KEEP_UPPER or clean.upper() in _KEEP_UPPER:
            result.append(word)
        elif i == 0:
            result.append(word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper())
        else:
            result.append(word.lower())
    return " ".join(result)


# ---------------------------------------------------------------------------
# Heading parsing
# ---------------------------------------------------------------------------

_RE_ROMAN = re.compile(r"^([IVXLC]+)\.\s+(.+)$")
_RE_SECTION_N = re.compile(r"^[Ss][Ee][Cc][Tt][Ii][Oo][Nn]\s+(\d+):\s*(.+)$")
_RE_DOMAIN_N = re.compile(r"^[Dd][Oo][Mm][Aa][Ii][Nn]\s+(\d+):\s*(.+)$")
_RE_PART_N = re.compile(r"^[Pp]art\s+(\d+):\s*(.+)$")
_RE_NUM_DOT = re.compile(r"^(\d+)\.\s+(.+)$")


def _parse_heading(text: str) -> tuple[bool, str]:
    """Return (already_roman, title_text).

    If already_roman is True the heading is in the target format and the
    caller should increment the counter but not reformat.
    """
    text = text.strip()

    if _RE_ROMAN.match(text):
        return True, text

    for pat in (_RE_SECTION_N, _RE_DOMAIN_N, _RE_PART_N, _RE_NUM_DOT):
        m = pat.match(text)
        if m:
            return False, m.group(2).strip()

    # Descriptive heading without prefix
    return False, text


def _is_structural_claims(line: str) -> bool:
    stripped = line.strip().lstrip("> ")
    # Handle &gt; HTML entities used in some MDX files
    stripped = stripped.replace("&gt;", "").strip()
    return bool(re.match(r"\*?\*?STRUCTURAL CLAIMS", stripped, re.IGNORECASE))


def _is_metadata_heading(line: str) -> bool:
    stripped = line.strip()
    # Heading form: ## METADATA, #### METADATA
    if re.match(r"^#{2,4}\s+METADATA\s*$", stripped, re.IGNORECASE):
        return True
    # Bold text form: **METADATA**
    if re.match(r"^\*\*METADATA\*\*\s*$", stripped, re.IGNORECASE):
        return True
    return False


# ---------------------------------------------------------------------------
# Title cleanup
# ---------------------------------------------------------------------------

# Generic dossier title phrases — if the cleaned title matches any of
# these (case-insensitive), it's template junk and should be emptied.
_GENERIC_TITLES = re.compile(
    r"^(?:"
    r"(?:structural\s+)?(?:country\s+)?(?:intelligence\s+)?dossier"
    r"|analytical\s+intelligence\s+dossier"
    r"|comprehensive\s+analytical\s+dossier"
    r"|an?\s+analytical\s+(?:intelligence\s+)?dossier"
    r"|middle\s+powers\s+monitor\s+(?:analytical|structural)\s+dossier"
    r"|structural\s+(?:country\s+)?dossier"
    r"|Federal\s+Republic\s+of\s+Germany"
    r")\s*$",
    re.IGNORECASE,
)

# Template prefixes to strip from # title lines
_TITLE_TEMPLATES = [
    r"^(?:STRUCTURAL\s+)?COUNTRY\s+DOSSIER:\s*",
    r"^Structural\s+[Cc]ountry\s+[Dd]ossier:\s*",
    r"^Structural\s+[Ii]ntelligence\s+[Dd]ossier:\s*",
    r"^Middle\s+Powers\s+Monitor[:\s|—–-]+",
    r"^Analytical\s+[Ii]ntelligence\s+[Dd]ossier:\s*",
]

# Suffixes to strip
_TITLE_SUFFIXES = [
    r"\s*[—–-]\s*(?:Pass\s+\d+(?:\s+of\s+\d+)?|Research\s+Compilation)(?:\s*\(Sections?\s+[\d–-]+\))?\s*$",
    r"\s*\(Pass\s+\d+(?:\s+of\s+\d+)?(?:,\s*Sections?\s+[\d–-]+)?\)\s*$",
]


_COUNTRY_EXPANSIONS = {
    "UAE": "United Arab Emirates",
    "Germany": "Federal Republic of Germany",
}


def _clean_title(title: str, country: str) -> str:
    """Clean a dossier # title line.

    Strips template prefixes ('Structural Country Dossier:'),
    pass markers ('— Pass 1 (Sections 0–7)'), and leading country
    name ('Latvia: ' → '').  Returns '' if nothing unique remains.
    """
    text = title.strip()

    # Strip template prefixes
    for pat in _TITLE_TEMPLATES:
        text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()

    # Strip suffixes (pass markers, section ranges)
    for pat in _TITLE_SUFFIXES:
        text = re.sub(pat, "", text, flags=re.IGNORECASE).strip()

    # Strip "Country: " or "Country — " prefix (try all name variants)
    names = {country, country.upper(), country.lower()}
    expansion = _COUNTRY_EXPANSIONS.get(country)
    if expansion:
        names.add(expansion)
    for name in names:
        escaped = re.escape(name)
        text = re.sub(rf"^{escaped}\s*[:—–-]\s*", "", text, flags=re.IGNORECASE).strip()
        if re.match(rf"^{escaped}\s*$", text, flags=re.IGNORECASE):
            text = ""

    # Check if what remains is still generic template text
    if text and _GENERIC_TITLES.match(text):
        text = ""

    # Too short to be meaningful
    if len(text) < 5:
        text = ""

    return text


def _strip_confidence_markers(line: str) -> str:
    """Remove inline confidence markers like [HIGH CONFIDENCE]."""
    return re.sub(r"\s*\[(?:HIGH|MODERATE|LOW|MEDIUM)\s+CONFIDENCE\]", "", line, flags=re.IGNORECASE)


def _escape_dollars(line: str) -> str:
    """Escape bare $ signs that MDX would interpret as LaTeX math delimiters.

    Replaces $NNN patterns (currency amounts) with escaped versions.
    Leaves already-escaped \\$ alone.
    """
    # Don't touch lines that are frontmatter, code blocks, or HTML
    if line.startswith("```") or line.startswith("    ") or line.startswith("<"):
        return line
    # Replace $ that isn't already escaped (not preceded by \)
    # but only when followed by a digit or word char (currency usage)
    return re.sub(r"(?<!\\)\$(?=[\d\w])", r"\\$", line)


# ---------------------------------------------------------------------------
# Core normalizer
# ---------------------------------------------------------------------------

def normalize_dossier(filepath: Path, dry_run: bool = False) -> dict:
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Derive country name from filename for title cleanup
    country_name = filepath.stem.replace("_", " ").title()
    _NAME_OVERRIDES = {"Uae": "UAE", "United Kingdom": "United Kingdom"}
    country_name = _NAME_OVERRIDES.get(country_name, country_name)

    stats = {
        "file": filepath.name,
        "headings_converted": 0,
        "subheadings_converted": 0,
        "metadata_removed": False,
        "confidence_markers_removed": 0,
        "dollars_escaped": 0,
        "title_cleaned": False,
    }

    out: list[str] = []
    section_counter = 0
    i = 0
    frontmatter_dashes = 0
    in_frontmatter = False
    in_metadata = False

    while i < len(lines):
        line = lines[i]

        # ---- frontmatter ----
        if line.strip() == "---" and frontmatter_dashes < 2:
            frontmatter_dashes += 1
            in_frontmatter = frontmatter_dashes == 1
            out.append(line)
            i += 1
            continue

        if in_frontmatter:
            out.append(line)
            i += 1
            continue

        # ---- # title cleanup ----
        m = re.match(r"^#\s+(.+)$", line)
        if m and not line.startswith("##"):
            cleaned = _clean_title(m.group(1), country_name)
            if cleaned:
                out.append(f"# {cleaned}")
            else:
                out.append(f"# {country_name}")
            stats["title_cleaned"] = True
            i += 1
            continue

        # ---- Remove boilerplate header lines ----
        if re.match(
            r"^\*\*MIDDLE\s+POWERS\s+MONITOR",
            line.strip(),
            re.IGNORECASE,
        ):
            i += 1
            continue

        # ---- METADATA removal ----
        if _is_metadata_heading(line):
            stats["metadata_removed"] = True
            in_metadata = True
            i += 1
            continue

        if in_metadata:
            # Eat lines until next ## heading or --- separator
            if line.startswith("## "):
                in_metadata = False
                # fall through to process this heading
            elif line.strip() == "---":
                in_metadata = False
                # Keep the separator, fall through
            else:
                i += 1
                continue

        # ---- STRUCTURAL CLAIMS: preserved for agent narrativization ----
        # (Previously removed here; now kept so agents can rewrite as prose)

        # ---- #### headings → bold ----
        m = re.match(r"^####\s+(.+)$", line)
        if m:
            out.append(f"**{m.group(1).strip()}**")
            stats["subheadings_converted"] += 1
            i += 1
            continue

        # ---- ### headings → bold ----
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            out.append(f"**{m.group(1).strip()}**")
            stats["subheadings_converted"] += 1
            i += 1
            continue

        # ---- ## headings → Roman numeral ----
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            heading_text = m.group(1).strip()

            # Skip non-content sections
            if heading_text.lower() in ("sources", "references"):
                # Remove sources section — eat until next ## or EOF
                i += 1
                while i < len(lines) and not lines[i].startswith("## "):
                    i += 1
                continue

            already_roman, title = _parse_heading(heading_text)
            section_counter += 1
            roman = to_roman(section_counter)

            if already_roman:
                # Re-stamp with correct sequential numeral
                _, bare_title = _RE_ROMAN.match(title).groups()
                out.append(f"## {roman}. {bare_title}")
            else:
                title = _to_sentence_case(title)
                out.append(f"## {roman}. {title}")

            stats["headings_converted"] += 1
            i += 1
            continue

        # ---- confidence markers ----
        cleaned = _strip_confidence_markers(line)
        if cleaned != line:
            stats["confidence_markers_removed"] += 1
            line = cleaned

        # ---- escape $ signs and pass through ----
        escaped = _escape_dollars(line)
        if escaped != line:
            stats["dollars_escaped"] += line.count("$") - line.count("\\$")
        out.append(escaped)
        i += 1

    result = "\n".join(out)

    if not dry_run:
        filepath.write_text(result, encoding="utf-8")

    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv
    single = None
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            single = arg

    files = sorted(DOSSIERS_DIR.glob("*.mdx"))
    files = [f for f in files if f.name != "index.mdx"]

    if single:
        files = [f for f in files if f.stem == single]
        if not files:
            print(f"No dossier found for '{single}'")
            sys.exit(1)

    mode = "DRY RUN" if dry_run else "WRITING"
    print(f"Normalizing {len(files)} dossiers ({mode})\n")

    all_stats = []
    for f in files:
        stats = normalize_dossier(f, dry_run=dry_run)
        all_stats.append(stats)
        flags = []
        if stats["headings_converted"]:
            flags.append(f"{stats['headings_converted']} headings")
        if stats["subheadings_converted"]:
            flags.append(f"{stats['subheadings_converted']} sub→bold")
        if stats["metadata_removed"]:
            flags.append("metadata removed")
        if stats["confidence_markers_removed"]:
            flags.append(f"{stats['confidence_markers_removed']} confidence markers")
        if stats["title_cleaned"]:
            flags.append("title cleaned")
        if stats["dollars_escaped"]:
            flags.append(f"{stats['dollars_escaped']} $ escaped")
        summary = " | ".join(flags) if flags else "no changes"
        print(f"  {stats['file']:30s} {summary}")

    total_h = sum(s["headings_converted"] for s in all_stats)
    total_s = sum(s["subheadings_converted"] for s in all_stats)
    total_m = sum(1 for s in all_stats if s["metadata_removed"])
    total_c = sum(s["confidence_markers_removed"] for s in all_stats)
    total_d = sum(s["dollars_escaped"] for s in all_stats)

    print(
        f"\nTotals: {total_h} headings, {total_s} sub→bold, "
        f"{total_m} metadata, {total_c} confidence markers, {total_d} $ escaped"
    )


if __name__ == "__main__":
    main()
