#!/usr/bin/env python3
"""
Brave News Search: Source Discovery per Country Leader

For each source in each country's source map, performs two Brave News searches
for that country's leader:
  1. English search (search_lang=en, country=US) -> saved as {country}_en.json
  2. Localized search (country-specific lang/country params) -> saved as {country}_local.json

Cross-references results with rss_full_text_sources.md and produces a summary report.
"""

from __future__ import annotations

import json
import os
import re
import time
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

import requests
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_MAPS_DIR = BASE_DIR / "source_maps"
RSS_FILE = BASE_DIR / "rss_full_text_sources.md"
OUTPUT_DIR = Path(__file__).parent
ENV_FILE = BASE_DIR.parent.parent.parent / ".env"

load_dotenv(ENV_FILE)
BRAVE_API_KEY = os.environ["BRAVE_API_KEY"]
BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"

# ---------- Country config ----------
# Each entry: leader name, localized search params (search_lang, ui_lang, country_code)
# Some countries have multiple local languages; we pick the dominant political discourse language.
COUNTRY_CONFIG = {
    "australia": {
        "leader": "Anthony Albanese",
        "local": {"search_lang": "en", "ui_lang": "en-AU", "country": "AU"},
    },
    "brazil": {
        "leader": "Lula",
        "local": {"search_lang": "pt-br", "ui_lang": "pt-BR", "country": "BR"},
    },
    "canada": {
        "leader": "Mark Carney",
        "local": {"search_lang": "fr", "ui_lang": "fr-CA", "country": "CA"},
    },
    "chile": {
        "leader": "Gabriel Boric",
        "local": {"search_lang": "es", "ui_lang": "es-CL", "country": "CL"},
    },
    "czech_republic": {
        "leader": "Petr Fiala",
        "local": {"search_lang": "cs", "ui_lang": "cs-CZ", "country": "ALL"},
    },
    "estonia": {
        "leader": "Kristen Michal",
        "local": {"search_lang": "et", "ui_lang": "et-EE", "country": "ALL"},
    },
    "finland": {
        "leader": "Petteri Orpo",
        "local": {"search_lang": "fi", "ui_lang": "fi-FI", "country": "FI"},
    },
    "france": {
        "leader": "Emmanuel Macron",
        "local": {"search_lang": "fr", "ui_lang": "fr-FR", "country": "FR"},
    },
    "germany": {
        "leader": "Friedrich Merz",
        "local": {"search_lang": "de", "ui_lang": "de-DE", "country": "DE"},
    },
    "india": {
        "leader": "Narendra Modi",
        "local": {"search_lang": "hi", "ui_lang": "hi-IN", "country": "IN"},
    },
    "indonesia": {
        "leader": "Prabowo Subianto",
        "local": {"search_lang": "ms", "ui_lang": "id-ID", "country": "ID"},
    },
    "italy": {
        "leader": "Giorgia Meloni",
        "local": {"search_lang": "it", "ui_lang": "it-IT", "country": "IT"},
    },
    "japan": {
        "leader": "Shigeru Ishiba",
        "local": {"search_lang": "jp", "ui_lang": "ja-JP", "country": "JP"},
    },
    "latvia": {
        "leader": "Evika Silina",
        "local": {"search_lang": "lv", "ui_lang": "lv-LV", "country": "ALL"},
    },
    "lithuania": {
        "leader": "Gintautas Paluckas",
        "local": {"search_lang": "lt", "ui_lang": "lt-LT", "country": "ALL"},
    },
    "mexico": {
        "leader": "Claudia Sheinbaum",
        "local": {"search_lang": "es", "ui_lang": "es-MX", "country": "MX"},
    },
    "norway": {
        "leader": "Jonas Gahr Store",
        "local": {"search_lang": "nb", "ui_lang": "nb-NO", "country": "NO"},
    },
    "poland": {
        "leader": "Donald Tusk",
        "local": {"search_lang": "pl", "ui_lang": "pl-PL", "country": "PL"},
    },
    "romania": {
        "leader": "Nicusor Dan",
        "local": {"search_lang": "ro", "ui_lang": "ro-RO", "country": "ALL"},
    },
    "saudi_arabia": {
        "leader": "Mohammed bin Salman",
        "local": {"search_lang": "ar", "ui_lang": "ar-SA", "country": "SA"},
    },
    "south_korea": {
        "leader": "Lee Jae-myung",
        "local": {"search_lang": "ko", "ui_lang": "ko-KR", "country": "KR"},
    },
    "spain": {
        "leader": "Pedro Sanchez",
        "local": {"search_lang": "es", "ui_lang": "es-ES", "country": "ES"},
    },
    "sweden": {
        "leader": "Ulf Kristersson",
        "local": {"search_lang": "sv", "ui_lang": "sv-SE", "country": "SE"},
    },
    "taiwan": {
        "leader": "Lai Ching-te",
        "local": {"search_lang": "zh-hant", "ui_lang": "zh-TW", "country": "TW"},
    },
    "turkey": {
        "leader": "Recep Tayyip Erdogan",
        "local": {"search_lang": "tr", "ui_lang": "tr-TR", "country": "TR"},
    },
    "uae": {
        "leader": "Mohammed bin Zayed",
        "local": {"search_lang": "ar", "ui_lang": "ar-AE", "country": "ALL"},
    },
    "ukraine": {
        "leader": "Volodymyr Zelenskyy",
        "local": {"search_lang": "uk", "ui_lang": "uk-UA", "country": "ALL"},
    },
    "united_kingdom": {
        "leader": "Keir Starmer",
        "local": {"search_lang": "en-gb", "ui_lang": "en-GB", "country": "GB"},
    },
}


def parse_source_map(filepath: Path) -> list[dict]:
    """Extract source name and domain from a source map markdown file."""
    text = filepath.read_text()
    sources = []

    # Pattern 1: Table format (like Saudi Arabia) - look for rows with domain info
    # | # | Name | Domain | ...
    table_pattern = re.compile(
        r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*`?([a-zA-Z0-9._/-]+\.[a-zA-Z]{2,}(?:/[^\s|`]*)?)`?\s*\|"
    )
    for m in table_pattern.finditer(text):
        name = m.group(1).strip().strip("*")
        domain = m.group(2).strip().rstrip("/")
        # Clean domain: remove paths, keep just the domain
        domain_clean = domain.split("/")[0] if "/" in domain else domain
        sources.append({"name": name, "domain": domain_clean})

    if sources:
        return sources

    # Pattern 2: Section format (like France, Japan) - ### N. Source Name + **Domain** field
    section_pattern = re.compile(
        r"###\s+\d+\.\s+(.+?)(?:\n|\r)",
    )
    domain_pattern = re.compile(
        r"\*\*(?:Domain|Name)\*\*\s*\|\s*`?([a-zA-Z0-9._/-]+\.[a-zA-Z]{2,}[^\s|`]*)`?"
    )

    sections = list(section_pattern.finditer(text))
    for i, sec_match in enumerate(sections):
        name = sec_match.group(1).strip().strip("*")
        # Find domain in the section between this heading and the next
        start = sec_match.end()
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        section_text = text[start:end]

        domain_match = domain_pattern.search(section_text)
        if domain_match:
            raw = domain_match.group(1).strip().rstrip("/")
            # Some have multiple domains separated by " / " or " (English) / (Japanese)"
            # Take the first domain
            domain = raw.split()[0].split("/")[0] if " " in raw else raw
            # Handle cases like "english.kyodonews.net / japanwire.kyodonews.net"
            if " / " in raw:
                domain = raw.split(" / ")[0].strip()
            # Strip protocol or www prefix for cleaner site: queries
            domain = domain.replace("https://", "").replace("http://", "")
            if domain.startswith("www."):
                domain = domain[4:]
            # Some domains have paths; take just the host
            domain = domain.split("/")[0]
            sources.append({"name": name, "domain": domain})

    return sources


def load_rss_sources() -> set[str]:
    """Load set of domains that have RSS full text."""
    text = RSS_FILE.read_text()
    domains = set()
    # Match domain patterns in table cells: `domain.tld`
    for m in re.finditer(r"`([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})`", text):
        domains.add(m.group(1).lower())
    return domains


def brave_news_search(query: str, count: int = 10, **kwargs) -> dict:
    """Perform a Brave News Search API call."""
    params = {"q": query, "count": count}
    params.update(kwargs)
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY,
    }
    resp = requests.get(BRAVE_NEWS_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_source(domain: str, leader: str, search_type: str, local_params: dict | None = None) -> dict:
    """Search for a source's coverage of a leader.

    search_type: 'en' or 'local'
    """
    query = f"site:{domain} {leader}"

    if search_type == "en":
        params = {"search_lang": "en", "country": "US"}
    else:
        params = local_params or {}

    try:
        result = brave_news_search(query, count=10, **params)
        num_results = len(result.get("results", []))
        return {
            "query": query,
            "params": params,
            "num_results": num_results,
            "results": result.get("results", []),
            "raw_response": result,
            "error": None,
        }
    except requests.exceptions.HTTPError as e:
        return {
            "query": query,
            "params": params,
            "num_results": 0,
            "results": [],
            "raw_response": None,
            "error": f"HTTP {e.response.status_code}: {e.response.text[:200]}",
        }
    except Exception as e:
        return {
            "query": query,
            "params": params,
            "num_results": 0,
            "results": [],
            "raw_response": None,
            "error": str(e),
        }


def main():
    rss_domains = load_rss_sources()
    print(f"Loaded {len(rss_domains)} RSS full-text domains")

    report_lines = []
    report_lines.append("# Brave News Search: Source Discovery Report")
    report_lines.append(f"\n**Generated:** 2026-03-20")
    report_lines.append(f"\n**Method:** For each source, searched `site:<domain> <leader>` via Brave News API with count=10")
    report_lines.append("\n---\n")

    source_map_files = sorted(SOURCE_MAPS_DIR.glob("*.md"))
    print(f"Found {len(source_map_files)} source maps")

    total_searches = 0
    total_hits_en = 0
    total_hits_local = 0
    total_rss = 0

    for sm_file in source_map_files:
        country_key = sm_file.stem  # e.g., "france"
        if country_key not in COUNTRY_CONFIG:
            print(f"SKIP: No config for {country_key}")
            continue

        config = COUNTRY_CONFIG[country_key]
        leader = config["leader"]
        local_params = config["local"]
        sources = parse_source_map(sm_file)

        if not sources:
            print(f"WARNING: No sources parsed from {sm_file.name}")
            continue

        country_display = country_key.replace("_", " ").title()
        print(f"\n{'='*60}")
        print(f"  {country_display} — Leader: {leader} — {len(sources)} sources")
        print(f"{'='*60}")

        en_results = {}
        local_results = {}

        for src in sources:
            name = src["name"]
            domain = src["domain"]

            # English search
            print(f"  [{country_key}] EN search: site:{domain} {leader} ...", end=" ", flush=True)
            en_res = search_source(domain, leader, "en")
            en_results[name] = en_res
            print(f"-> {en_res['num_results']} results" + (f" (ERR: {en_res['error']})" if en_res['error'] else ""))
            time.sleep(1.1)  # rate limit: ~1 req/sec for free tier

            # Local search
            print(f"  [{country_key}] LOCAL search: site:{domain} {leader} ...", end=" ", flush=True)
            local_res = search_source(domain, leader, "local", local_params)
            local_results[name] = local_res
            print(f"-> {local_res['num_results']} results" + (f" (ERR: {local_res['error']})" if local_res['error'] else ""))
            time.sleep(1.1)

            total_searches += 2

        # Save JSON results
        en_json_path = OUTPUT_DIR / f"{country_key}_en.json"
        local_json_path = OUTPUT_DIR / f"{country_key}_local.json"

        # Build saveable JSON (strip raw_response to keep files smaller, but keep results)
        def slim(results_dict):
            out = {}
            for name, r in results_dict.items():
                out[name] = {
                    "query": r["query"],
                    "params": r["params"],
                    "num_results": r["num_results"],
                    "results": r["results"],
                    "error": r["error"],
                }
            return out

        with open(en_json_path, "w") as f:
            json.dump({"country": country_key, "leader": leader, "search_type": "en", "sources": slim(en_results)}, f, indent=2, ensure_ascii=False)

        with open(local_json_path, "w") as f:
            json.dump({"country": country_key, "leader": leader, "search_type": "local",
                        "local_params": local_params, "sources": slim(local_results)}, f, indent=2, ensure_ascii=False)

        # Build report section
        report_lines.append(f"## {country_display}")
        report_lines.append(f"\n**Leader:** {leader}")
        report_lines.append(f"**Local search params:** search_lang={local_params['search_lang']}, country={local_params['country']}")
        report_lines.append(f"**Sources:** {len(sources)}\n")
        report_lines.append("| # | Source | Domain | EN Results | Local Results | RSS Full Text |")
        report_lines.append("|---|--------|--------|-----------|--------------|---------------|")

        for i, src in enumerate(sources, 1):
            name = src["name"]
            domain = src["domain"]
            en_count = en_results[name]["num_results"]
            local_count = local_results[name]["num_results"]
            is_rss = domain.lower() in rss_domains or any(
                domain.lower() in rd for rd in rss_domains
            )

            en_status = f"{en_count}" if en_count > 0 else "0"
            local_status = f"{local_count}" if local_count > 0 else "0"
            rss_status = "RSS" if is_rss else "-"

            if en_count > 0:
                total_hits_en += 1
            if local_count > 0:
                total_hits_local += 1
            if is_rss:
                total_rss += 1

            report_lines.append(f"| {i} | {name} | `{domain}` | {en_status} | {local_status} | {rss_status} |")

        report_lines.append("")

    # Summary
    total_sources = total_searches // 2 if total_searches > 0 else 0
    report_lines.insert(4, f"**Total sources tested:** {total_sources}")
    report_lines.insert(5, f"**Sources with EN results:** {total_hits_en} ({100*total_hits_en//max(total_sources,1)}%)")
    report_lines.insert(6, f"**Sources with Local results:** {total_hits_local} ({100*total_hits_local//max(total_sources,1)}%)")
    report_lines.insert(7, f"**Sources with RSS full text:** {total_rss} ({100*total_rss//max(total_sources,1)}%)")
    report_lines.insert(8, "")

    report_path = OUTPUT_DIR / "REPORT.md"
    report_path.write_text("\n".join(report_lines))
    print(f"\n\nReport saved to {report_path}")
    print(f"Total API calls: {total_searches}")
    print(f"EN hits: {total_hits_en}/{total_sources}, Local hits: {total_hits_local}/{total_sources}, RSS: {total_rss}/{total_sources}")


if __name__ == "__main__":
    main()
