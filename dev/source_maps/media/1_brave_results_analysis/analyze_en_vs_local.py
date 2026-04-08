#!/usr/bin/env python3
"""
Compare EN vs Local Brave News search results per country.

For each country, compares:
- Result counts (which approach yields more results)
- URL overlap (are the same articles returned?)
- Content freshness (which returns newer articles)
- Language distribution (are local searches returning local-language content?)

Outputs per-country markdown files and an aggregate report.
"""
from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "0_brave_search_results"
OUTPUT_DIR = Path(__file__).parent


def load_country_pair(country: str) -> tuple[dict, dict]:
    en_path = RESULTS_DIR / f"{country}_en.json"
    local_path = RESULTS_DIR / f"{country}_local.json"
    with open(en_path) as f:
        en_data = json.load(f)
    with open(local_path) as f:
        local_data = json.load(f)
    return en_data, local_data


def extract_urls(results: list[dict]) -> set[str]:
    return {r["url"] for r in results if r.get("url")}


def detect_language_from_url_and_title(result: dict) -> str:
    """Heuristic: check for common non-English URL patterns and title characters."""
    url = result.get("url", "")
    title = result.get("title", "")

    # Check for explicit language paths
    if "/en/" in url or "/english/" in url:
        return "en"
    if "/fr/" in url or "/francais/" in url:
        return "fr"
    if "/de/" in url or "/deutsch/" in url:
        return "de"
    if "/es/" in url or "/espanol/" in url:
        return "es"
    if "/pt/" in url or "/pt-br/" in url:
        return "pt"

    # Check for non-Latin scripts in title
    has_cjk = bool(re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]', title))
    has_korean = bool(re.search(r'[\uac00-\ud7af]', title))
    has_cyrillic = bool(re.search(r'[\u0400-\u04ff]', title))
    has_arabic = bool(re.search(r'[\u0600-\u06ff]', title))
    has_devanagari = bool(re.search(r'[\u0900-\u097f]', title))
    has_thai = bool(re.search(r'[\u0e00-\u0e7f]', title))

    if has_cjk:
        return "cjk"
    if has_korean:
        return "ko"
    if has_cyrillic:
        return "cyrillic"
    if has_arabic:
        return "ar"
    if has_devanagari:
        return "hi"
    if has_thai:
        return "th"

    # Check for accented characters common in European languages
    has_accented = bool(re.search(r'[àâäéèêëïîôùûüÿçœæ]', title.lower()))
    has_german = bool(re.search(r'[äöüß]', title.lower()))
    has_nordic = bool(re.search(r'[åæøöä]', title.lower()))
    has_polish = bool(re.search(r'[ąćęłńóśźż]', title.lower()))
    has_czech = bool(re.search(r'[čďěňřšťůž]', title.lower()))
    has_romanian = bool(re.search(r'[ăâîșț]', title.lower()))

    if has_german:
        return "de"
    if has_nordic:
        return "nordic"
    if has_polish:
        return "pl"
    if has_czech:
        return "cs"
    if has_romanian:
        return "ro"
    if has_accented:
        return "romance"  # French/Spanish/Portuguese/Italian

    return "en"  # default assumption


def parse_age(page_age: str) -> datetime | None:
    """Parse page_age like '2026-03-20T10:20:45'."""
    if not page_age:
        return None
    try:
        return datetime.fromisoformat(page_age.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def analyze_country(country: str, en_data: dict, local_data: dict) -> dict:
    """Analyze EN vs Local results for a single country."""
    leader = en_data["leader"]
    local_params = local_data.get("local_params", {})

    source_analyses = []
    total_en_results = 0
    total_local_results = 0
    total_en_only_urls = 0
    total_local_only_urls = 0
    total_shared_urls = 0
    sources_en_wins = 0
    sources_local_wins = 0
    sources_tied = 0
    sources_both_zero = 0
    identical_count = 0
    local_error_count = 0

    en_sources = en_data["sources"]
    local_sources = local_data["sources"]

    for source_name in en_sources:
        en_src = en_sources[source_name]
        local_src = local_sources.get(source_name, {"num_results": 0, "results": [], "error": "missing"})

        en_count = en_src["num_results"]
        local_count = local_src["num_results"]
        local_error = local_src.get("error")

        total_en_results += en_count
        total_local_results += local_count

        en_urls = extract_urls(en_src["results"])
        local_urls = extract_urls(local_src["results"])

        shared = en_urls & local_urls
        en_only = en_urls - local_urls
        local_only = local_urls - en_urls

        total_shared_urls += len(shared)
        total_en_only_urls += len(en_only)
        total_local_only_urls += len(local_only)

        # Determine winner
        if local_error:
            local_error_count += 1
        if en_count == 0 and local_count == 0:
            sources_both_zero += 1
            winner = "neither"
        elif en_count > local_count:
            sources_en_wins += 1
            winner = "en"
        elif local_count > en_count:
            sources_local_wins += 1
            winner = "local"
        else:
            sources_tied += 1
            winner = "tied"

        # Check if results are identical (same URLs)
        is_identical = (en_urls == local_urls) and en_count > 0
        if is_identical:
            identical_count += 1

        # Language analysis of results
        en_langs = defaultdict(int)
        for r in en_src["results"]:
            lang = detect_language_from_url_and_title(r)
            en_langs[lang] += 1

        local_langs = defaultdict(int)
        for r in local_src["results"]:
            lang = detect_language_from_url_and_title(r)
            local_langs[lang] += 1

        # Freshness: average page_age
        en_dates = [parse_age(r.get("page_age", "")) for r in en_src["results"]]
        en_dates = [d for d in en_dates if d]
        local_dates = [parse_age(r.get("page_age", "")) for r in local_src["results"]]
        local_dates = [d for d in local_dates if d]

        en_newest = max(en_dates).isoformat() if en_dates else None
        local_newest = max(local_dates).isoformat() if local_dates else None

        source_analyses.append({
            "name": source_name,
            "en_count": en_count,
            "local_count": local_count,
            "shared_urls": len(shared),
            "en_only_urls": len(en_only),
            "local_only_urls": len(local_only),
            "is_identical": is_identical,
            "winner": winner,
            "local_error": local_error,
            "en_langs": dict(en_langs),
            "local_langs": dict(local_langs),
            "en_newest": en_newest,
            "local_newest": local_newest,
        })

    num_sources = len(en_sources)
    all_urls_total = total_shared_urls + total_en_only_urls + total_local_only_urls
    overlap_pct = (total_shared_urls / all_urls_total * 100) if all_urls_total > 0 else 0

    return {
        "country": country,
        "leader": leader,
        "local_params": local_params,
        "num_sources": num_sources,
        "total_en_results": total_en_results,
        "total_local_results": total_local_results,
        "total_shared_urls": total_shared_urls,
        "total_en_only_urls": total_en_only_urls,
        "total_local_only_urls": total_local_only_urls,
        "overlap_pct": overlap_pct,
        "sources_en_wins": sources_en_wins,
        "sources_local_wins": sources_local_wins,
        "sources_tied": sources_tied,
        "sources_both_zero": sources_both_zero,
        "identical_count": identical_count,
        "local_error_count": local_error_count,
        "source_analyses": source_analyses,
    }


def write_country_report(analysis: dict):
    country = analysis["country"]
    display = country.replace("_", " ").title()
    lines = []

    lines.append(f"# EN vs Local Search Analysis: {display}")
    lines.append(f"\n**Leader:** {analysis['leader']}")
    lp = analysis["local_params"]
    lines.append(f"**Local params:** search_lang={lp.get('search_lang','?')}, ui_lang={lp.get('ui_lang','?')}, country={lp.get('country','?')}")
    lines.append(f"**Sources analyzed:** {analysis['num_sources']}")

    # Determine if local had API errors
    if analysis["local_error_count"] > 0:
        lines.append(f"\n> **WARNING:** {analysis['local_error_count']}/{analysis['num_sources']} local searches returned API errors (invalid ui_lang). Local results are unreliable for this country.")

    lines.append("\n---\n")
    lines.append("## Summary\n")
    lines.append(f"| Metric | EN | Local |")
    lines.append(f"|--------|-----|-------|")
    lines.append(f"| Total results | {analysis['total_en_results']} | {analysis['total_local_results']} |")
    lines.append(f"| Sources with more results | {analysis['sources_en_wins']} | {analysis['sources_local_wins']} |")
    lines.append(f"| Sources tied | {analysis['sources_tied']} | |")
    lines.append(f"| Sources both zero | {analysis['sources_both_zero']} | |")
    lines.append(f"| Identical result sets | {analysis['identical_count']} | |")

    lines.append(f"\n**URL overlap:** {analysis['overlap_pct']:.1f}% of all unique URLs were returned by both searches")
    lines.append(f"- EN-only URLs: {analysis['total_en_only_urls']}")
    lines.append(f"- Local-only URLs: {analysis['total_local_only_urls']}")
    lines.append(f"- Shared URLs: {analysis['total_shared_urls']}")

    # Verdict
    lines.append("\n### Verdict\n")
    if analysis["local_error_count"] == analysis["num_sources"]:
        lines.append("**Local search failed entirely** due to unsupported `ui_lang`. EN search is the only viable option for this country.")
    elif analysis["overlap_pct"] > 85:
        lines.append(f"**Results are largely identical** ({analysis['overlap_pct']:.0f}% URL overlap). EN and local searches return effectively the same content. EN search is sufficient.")
    elif analysis["total_en_results"] > analysis["total_local_results"] * 1.3:
        diff_pct = (analysis["total_en_results"] - analysis["total_local_results"]) / max(analysis["total_en_results"], 1) * 100
        lines.append(f"**EN search yields better results** — {diff_pct:.0f}% more total results. The EN search finds more indexed content across sources.")
    elif analysis["total_local_results"] > analysis["total_en_results"] * 1.3:
        diff_pct = (analysis["total_local_results"] - analysis["total_en_results"]) / max(analysis["total_local_results"], 1) * 100
        lines.append(f"**Local search yields better results** — {diff_pct:.0f}% more total results. The localized search surfaces content the EN search misses.")
    else:
        lines.append(f"**Mixed results** — neither approach is clearly dominant. EN returned {analysis['total_en_results']} results vs local's {analysis['total_local_results']}. Consider running both for maximum coverage.")

    # Why section
    lines.append("\n### Why\n")
    if analysis["local_error_count"] > 0:
        lines.append(f"- Brave API rejected `ui_lang` parameter for {analysis['local_error_count']} searches — this locale is not in Brave's supported set")
    if analysis["overlap_pct"] > 85:
        lines.append("- High overlap indicates Brave's news index is not significantly language-filtered for this country")
        lines.append("- The `site:` operator constrains results to the same domain regardless of language settings")
    if analysis["total_en_only_urls"] > analysis["total_local_only_urls"] * 2:
        lines.append("- EN search surfaces more unique URLs, likely because Brave's English-language index is broader")
    if analysis["total_local_only_urls"] > analysis["total_en_only_urls"] * 2:
        lines.append("- Local search surfaces unique local-language URLs that the EN search misses — valuable for non-English sources")

    # Per-source detail table
    lines.append("\n---\n")
    lines.append("## Per-Source Detail\n")
    lines.append("| Source | EN | Local | Shared | EN-only | Local-only | Identical | Winner |")
    lines.append("|--------|-----|-------|--------|---------|------------|-----------|--------|")

    for sa in analysis["source_analyses"]:
        ident = "yes" if sa["is_identical"] else "-"
        error_note = " (err)" if sa["local_error"] else ""
        lines.append(
            f"| {sa['name']} | {sa['en_count']} | {sa['local_count']}{error_note} | "
            f"{sa['shared_urls']} | {sa['en_only_urls']} | {sa['local_only_urls']} | {ident} | {sa['winner']} |"
        )

    # Language distribution
    lines.append("\n---\n")
    lines.append("## Language Distribution in Results\n")
    lines.append("Heuristic detection based on URL paths and title character analysis.\n")

    en_agg_langs = defaultdict(int)
    local_agg_langs = defaultdict(int)
    for sa in analysis["source_analyses"]:
        for lang, cnt in sa["en_langs"].items():
            en_agg_langs[lang] += cnt
        for lang, cnt in sa["local_langs"].items():
            local_agg_langs[lang] += cnt

    lines.append("| Language | EN results | Local results |")
    lines.append("|----------|-----------|--------------|")
    all_langs = sorted(set(list(en_agg_langs.keys()) + list(local_agg_langs.keys())))
    for lang in all_langs:
        lines.append(f"| {lang} | {en_agg_langs.get(lang, 0)} | {local_agg_langs.get(lang, 0)} |")

    report_path = OUTPUT_DIR / f"{country}.md"
    report_path.write_text("\n".join(lines))
    return report_path


def write_aggregate_report(all_analyses: list[dict]):
    lines = []
    lines.append("# Aggregate Analysis: EN vs Local Brave News Search\n")
    lines.append(f"**Generated:** 2026-03-20")
    lines.append(f"**Countries analyzed:** {len(all_analyses)}")

    grand_en = sum(a["total_en_results"] for a in all_analyses)
    grand_local = sum(a["total_local_results"] for a in all_analyses)
    grand_shared = sum(a["total_shared_urls"] for a in all_analyses)
    grand_en_only = sum(a["total_en_only_urls"] for a in all_analyses)
    grand_local_only = sum(a["total_local_only_urls"] for a in all_analyses)
    grand_all = grand_shared + grand_en_only + grand_local_only
    grand_overlap = (grand_shared / grand_all * 100) if grand_all > 0 else 0

    lines.append("\n---\n")
    lines.append("## Global Summary\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total EN results | {grand_en} |")
    lines.append(f"| Total Local results | {grand_local} |")
    lines.append(f"| Overall URL overlap | {grand_overlap:.1f}% |")
    lines.append(f"| EN-only URLs | {grand_en_only} |")
    lines.append(f"| Local-only URLs | {grand_local_only} |")
    lines.append(f"| Shared URLs | {grand_shared} |")

    # Categorize countries
    identical_countries = []      # >85% overlap
    en_better_countries = []      # EN yields 30%+ more
    local_better_countries = []   # Local yields 30%+ more
    mixed_countries = []          # Neither clearly better
    broken_countries = []         # Local had all errors

    for a in all_analyses:
        if a["local_error_count"] == a["num_sources"]:
            broken_countries.append(a)
        elif a["overlap_pct"] > 85:
            identical_countries.append(a)
        elif a["total_en_results"] > a["total_local_results"] * 1.3:
            en_better_countries.append(a)
        elif a["total_local_results"] > a["total_en_results"] * 1.3:
            local_better_countries.append(a)
        else:
            mixed_countries.append(a)

    lines.append("\n---\n")
    lines.append("## Country Classification\n")

    lines.append(f"### Largely Identical ({len(identical_countries)} countries)\n")
    lines.append("EN and Local return >85% the same URLs. **EN search alone is sufficient.**\n")
    if identical_countries:
        lines.append("| Country | Overlap | EN results | Local results |")
        lines.append("|---------|---------|-----------|--------------|")
        for a in sorted(identical_countries, key=lambda x: -x["overlap_pct"]):
            lines.append(f"| {a['country'].replace('_',' ').title()} | {a['overlap_pct']:.0f}% | {a['total_en_results']} | {a['total_local_results']} |")
    else:
        lines.append("*(none)*")

    lines.append(f"\n### EN Yields Better Results ({len(en_better_countries)} countries)\n")
    lines.append("EN search returns 30%+ more results. **EN is the primary search; local adds marginal value.**\n")
    if en_better_countries:
        lines.append("| Country | EN results | Local results | Diff | Overlap |")
        lines.append("|---------|-----------|--------------|------|---------|")
        for a in sorted(en_better_countries, key=lambda x: -(x["total_en_results"] - x["total_local_results"])):
            diff = a["total_en_results"] - a["total_local_results"]
            lines.append(f"| {a['country'].replace('_',' ').title()} | {a['total_en_results']} | {a['total_local_results']} | +{diff} | {a['overlap_pct']:.0f}% |")
    else:
        lines.append("*(none)*")

    lines.append(f"\n### Local Yields Better Results ({len(local_better_countries)} countries)\n")
    lines.append("Local search returns 30%+ more results. **Both searches recommended for maximum coverage.**\n")
    if local_better_countries:
        lines.append("| Country | EN results | Local results | Diff | Overlap |")
        lines.append("|---------|-----------|--------------|------|---------|")
        for a in sorted(local_better_countries, key=lambda x: -(x["total_local_results"] - x["total_en_results"])):
            diff = a["total_local_results"] - a["total_en_results"]
            lines.append(f"| {a['country'].replace('_',' ').title()} | {a['total_en_results']} | {a['total_local_results']} | +{diff} | {a['overlap_pct']:.0f}% |")
    else:
        lines.append("*(none)*")

    lines.append(f"\n### Mixed / Close ({len(mixed_countries)} countries)\n")
    lines.append("Neither approach is clearly dominant (<30% difference). **Running both provides marginal additional coverage.**\n")
    if mixed_countries:
        lines.append("| Country | EN results | Local results | Overlap |")
        lines.append("|---------|-----------|--------------|---------|")
        for a in sorted(mixed_countries, key=lambda x: x["country"]):
            lines.append(f"| {a['country'].replace('_',' ').title()} | {a['total_en_results']} | {a['total_local_results']} | {a['overlap_pct']:.0f}% |")
    else:
        lines.append("*(none)*")

    lines.append(f"\n### Local Search Broken ({len(broken_countries)} countries)\n")
    lines.append("Brave API rejected `ui_lang` parameter — locale not supported. **EN search is the only option.**\n")
    if broken_countries:
        lines.append("| Country | Local params | EN results | Issue |")
        lines.append("|---------|-------------|-----------|-------|")
        for a in sorted(broken_countries, key=lambda x: x["country"]):
            lp = a["local_params"]
            lines.append(f"| {a['country'].replace('_',' ').title()} | ui_lang={lp.get('ui_lang','?')} | {a['total_en_results']} | `ui_lang` not in Brave's supported set |")
    else:
        lines.append("*(none)*")

    # Recommendations
    lines.append("\n---\n")
    lines.append("## Recommendations\n")
    lines.append("### Why EN and Local often return the same results\n")
    lines.append("- The `site:` operator in the query anchors results to a specific domain, which is the dominant filter")
    lines.append("- Brave's news index appears to return the same articles regardless of `search_lang` for most domains")
    lines.append("- The `search_lang` and `country` parameters primarily affect ranking and snippet language, not the underlying index")
    lines.append("- For English-language domains (e.g., `reuters.com`, `theguardian.com`), language settings have no effect\n")

    lines.append("### When local search adds value\n")
    lines.append("- Countries with primarily non-English media and where Brave has good local-language indexing")
    lines.append("- Sources that publish in multiple languages — local search may surface the native-language edition")
    lines.append("- Countries where the local search found unique URLs not in the EN results\n")

    lines.append("### Pipeline recommendation\n")
    lines.append("1. **Default to EN search** — it provides the broadest coverage and works for all countries")
    lines.append("2. **Add local search only for countries where it demonstrably adds unique content** (see 'Local Yields Better' category above)")
    lines.append("3. **Skip local search for countries with broken locale support** — use EN only")
    lines.append("4. **For countries with identical results** — running both is redundant; use EN only to halve API costs")

    # Per-country summary table
    lines.append("\n---\n")
    lines.append("## Full Country Comparison Table\n")
    lines.append("| Country | Leader | EN | Local | Overlap | EN-only | Local-only | Category |")
    lines.append("|---------|--------|-----|-------|---------|---------|------------|----------|")

    for a in sorted(all_analyses, key=lambda x: x["country"]):
        cat = "broken"
        if a in identical_countries:
            cat = "identical"
        elif a in en_better_countries:
            cat = "EN better"
        elif a in local_better_countries:
            cat = "local better"
        elif a in mixed_countries:
            cat = "mixed"

        lines.append(
            f"| {a['country'].replace('_',' ').title()} | {a['leader']} | "
            f"{a['total_en_results']} | {a['total_local_results']} | "
            f"{a['overlap_pct']:.0f}% | {a['total_en_only_urls']} | {a['total_local_only_urls']} | {cat} |"
        )

    report_path = OUTPUT_DIR / "AGGREGATE.md"
    report_path.write_text("\n".join(lines))
    return report_path


def main():
    countries = sorted(set(
        f.stem.replace("_en", "").replace("_local", "")
        for f in RESULTS_DIR.glob("*.json")
    ))

    print(f"Analyzing {len(countries)} countries...")

    all_analyses = []
    for country in countries:
        en_data, local_data = load_country_pair(country)
        analysis = analyze_country(country, en_data, local_data)
        all_analyses.append(analysis)

        report_path = write_country_report(analysis)
        overlap = analysis["overlap_pct"]
        print(f"  {country:20s}  EN={analysis['total_en_results']:3d}  Local={analysis['total_local_results']:3d}  "
              f"overlap={overlap:.0f}%  errors={analysis['local_error_count']}")

    agg_path = write_aggregate_report(all_analyses)
    print(f"\nAggregate report: {agg_path}")

    # Save raw analysis as JSON for further use
    json_path = OUTPUT_DIR / "analysis_data.json"
    # Strip source_analyses for the summary JSON to keep it manageable
    summary = []
    for a in all_analyses:
        s = {k: v for k, v in a.items() if k != "source_analyses"}
        summary.append(s)
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Raw data: {json_path}")


if __name__ == "__main__":
    main()
