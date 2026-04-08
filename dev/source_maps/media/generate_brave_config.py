#!/usr/bin/env python3
"""
Generate Brave News API source configuration from REPORT.md.

Reads the source discovery report, cross-references with RANKING_ANALYSIS
local-language premium data, and outputs a YAML config with:
- Per-country search params (EN default vs local)
- Indexed sources (only those that returned results)

Usage:
    python generate_brave_config.py
    # Writes to assets/country_configs/brave_sources.yaml
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPORT_PATH = Path(__file__).parent / "0_brave_search_results" / "REPORT.md"
OUTPUT_PATH = Path(__file__).parent.parent.parent.parent / "assets" / "country_configs" / "brave_sources.yaml"

# Country name (as used in REPORT headings) -> ISO 2-letter code
NAME_TO_CODE = {
    "Australia": "au",
    "Brazil": "br",
    "Canada": "ca",
    "Chile": "cl",
    "Czech Republic": "cz",
    "Estonia": "ee",
    "Finland": "fi",
    "France": "fr",
    "Germany": "de",
    "India": "in",
    "Indonesia": "id",
    "Italy": "it",
    "Japan": "jp",
    "Latvia": "lv",
    "Lithuania": "lt",
    "Mexico": "mx",
    "Norway": "no",
    "Poland": "pl",
    "Romania": "ro",
    "Saudi Arabia": "sa",
    "South Korea": "kr",
    "Spain": "es",
    "Sweden": "se",
    "Taiwan": "tw",
    "Turkey": "tr",
    "Uae": "ae",
    "Ukraine": "ua",
    "United Kingdom": "gb",
}

# Local search params per country (from brave_source_search.py COUNTRY_CONFIG)
LOCAL_PARAMS = {
    "au": {"search_lang": "en", "ui_lang": "en-AU", "country": "AU"},
    "br": {"search_lang": "pt-br", "ui_lang": "pt-BR", "country": "BR"},
    "ca": {"search_lang": "fr", "ui_lang": "fr-CA", "country": "CA"},
    "cl": {"search_lang": "es", "ui_lang": "es-CL", "country": "CL"},
    "cz": {"search_lang": "cs", "ui_lang": "cs-CZ", "country": "ALL"},
    "ee": {"search_lang": "et", "ui_lang": "et-EE", "country": "ALL"},
    "fi": {"search_lang": "fi", "ui_lang": "fi-FI", "country": "FI"},
    "fr": {"search_lang": "fr", "ui_lang": "fr-FR", "country": "FR"},
    "de": {"search_lang": "de", "ui_lang": "de-DE", "country": "DE"},
    "in": {"search_lang": "hi", "ui_lang": "hi-IN", "country": "IN"},
    "id": {"search_lang": "ms", "ui_lang": "id-ID", "country": "ID"},
    "it": {"search_lang": "it", "ui_lang": "it-IT", "country": "IT"},
    "jp": {"search_lang": "jp", "ui_lang": "ja-JP", "country": "JP"},
    "lv": {"search_lang": "lv", "ui_lang": "lv-LV", "country": "ALL"},
    "lt": {"search_lang": "lt", "ui_lang": "lt-LT", "country": "ALL"},
    "mx": {"search_lang": "es", "ui_lang": "es-MX", "country": "MX"},
    "no": {"search_lang": "nb", "ui_lang": "nb-NO", "country": "NO"},
    "pl": {"search_lang": "pl", "ui_lang": "pl-PL", "country": "PL"},
    "ro": {"search_lang": "ro", "ui_lang": "ro-RO", "country": "ALL"},
    "sa": {"search_lang": "ar", "ui_lang": "ar-SA", "country": "SA"},
    "kr": {"search_lang": "ko", "ui_lang": "ko-KR", "country": "KR"},
    "es": {"search_lang": "es", "ui_lang": "es-ES", "country": "ES"},
    "se": {"search_lang": "sv", "ui_lang": "sv-SE", "country": "SE"},
    "tw": {"search_lang": "zh-hant", "ui_lang": "zh-TW", "country": "TW"},
    "tr": {"search_lang": "tr", "ui_lang": "tr-TR", "country": "TR"},
    "ae": {"search_lang": "ar", "ui_lang": "ar-AE", "country": "ALL"},
    "ua": {"search_lang": "uk", "ui_lang": "uk-UA", "country": "ALL"},
    "gb": {"search_lang": "en-gb", "ui_lang": "en-GB", "country": "GB"},
}

# Countries where local non-EN premium > 0 (from RANKING_ANALYSIS)
# These use local_params instead of EN defaults
USE_LOCAL = {"fr", "de", "pl", "fi", "mx", "br", "jp", "tw", "it", "es", "tr", "ca"}


def parse_report(text: str) -> dict:
    """Parse REPORT.md into structured country data."""
    countries = {}

    # Split by ## headings (country sections)
    sections = re.split(r"\n## ", text)

    for section in sections[1:]:  # skip preamble
        lines = section.strip().split("\n")
        country_name = lines[0].strip()
        code = NAME_TO_CODE.get(country_name)
        if not code:
            continue

        # Extract local search params line
        local_line = next(
            (l for l in lines if l.startswith("**Local search params:**")), ""
        )

        # Parse table rows: | # | Source | Domain | EN Results | Local Results | RSS Full Text |
        sources = []
        for line in lines:
            m = re.match(
                r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*`(.+?)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(RSS|-)\s*\|",
                line,
            )
            if m:
                name = m.group(1).strip()
                domain = m.group(2).strip()
                en_results = int(m.group(3))
                local_results = int(m.group(4))
                rss = m.group(5).strip() == "RSS"

                # Only include sources that returned results
                if en_results > 0 or local_results > 0:
                    sources.append(
                        {
                            "name": name,
                            "domain": domain,
                            "rss_full_text": rss,
                        }
                    )

        if sources:
            countries[code] = {
                "use_local_params": code in USE_LOCAL,
                "local_params": LOCAL_PARAMS.get(code, {}),
                "sources": sources,
            }

    return countries


def main():
    report_text = REPORT_PATH.read_text()
    countries = parse_report(report_text)

    config = {
        "_generated_from": "dev/source_maps/media/0_brave_search_results/REPORT.md",
        "_note": "Do not edit manually. Regenerate with: python dev/source_maps/media/generate_brave_config.py",
        "defaults": {
            "count": 50,
            "offset": 0,
            "freshness": "pw",
            "extra_snippets": True,
        },
        "countries": {},
    }

    for code in sorted(countries.keys()):
        entry = countries[code]
        country_data = {"use_local_params": entry["use_local_params"]}
        if entry["use_local_params"]:
            country_data["local_params"] = entry["local_params"]
        country_data["sources"] = entry["sources"]

        config["countries"][code] = country_data

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

    total_sources = sum(len(c["sources"]) for c in config["countries"].values())
    local_countries = sum(1 for c in config["countries"].values() if c["use_local_params"])
    print(f"Generated {OUTPUT_PATH}")
    print(f"  {len(config['countries'])} countries, {total_sources} indexed sources")
    print(f"  {local_countries} countries using local params, {len(config['countries']) - local_countries} using EN defaults")


if __name__ == "__main__":
    main()
