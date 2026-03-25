#!/usr/bin/env python3
"""
Compile cross-method comparison report from all extraction experiments.

Reads results from methods 1-4 and produces:
- Per-source best-method recommendation
- Per-country summary
- Overall statistics
- Markdown report
"""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent
CURL = BASE / "3_curl_results" / "curl_results.json"
WEBFETCH = BASE / "4_webfetch_results" / "webfetch_results.json"
DIFFBOT = BASE / "5_diffbot_results" / "diffbot_results.json"
PLAYWRIGHT = BASE / "6_playwright_results" / "playwright_results.json"
OUTPUT_JSON = Path(__file__).parent / "comparison.json"
OUTPUT_MD = Path(__file__).parent / "REPORT.md"


def load_safe(path):
    try:
        return json.load(open(path))
    except FileNotFoundError:
        return {}


def url_status(results_data, source_key, url):
    """Check if a specific URL succeeded in a given method's results."""
    if source_key not in results_data:
        return None  # not tested
    for r in results_data[source_key]["results"]:
        if r["url"] == url:
            return r["status"]
    return None  # not tested


def main():
    curl = load_safe(CURL)
    webfetch = load_safe(WEBFETCH)
    diffbot = load_safe(DIFFBOT)
    playwright = load_safe(PLAYWRIGHT)

    methods = {
        "curl": curl,
        "webfetch": webfetch,
        "diffbot": diffbot,
        "playwright": playwright,
    }

    # Collect all source keys and URLs from curl (the baseline)
    all_sources = sorted(curl.keys())

    comparison = {}
    country_stats = {}

    for source_key in all_sources:
        source = curl[source_key]
        domain = source["domain"]
        country = source["country"]

        if country not in country_stats:
            country_stats[country] = {m: {"ok": 0, "tested": 0} for m in methods}
            country_stats[country]["total_urls"] = 0

        url_results = []
        for r in source["results"]:
            url = r["url"]
            country_stats[country]["total_urls"] += 1

            statuses = {}
            for method_name, method_data in methods.items():
                s = url_status(method_data, source_key, url)
                if s is not None:
                    statuses[method_name] = s
                    country_stats[country][method_name]["tested"] += 1
                    if s == "OK":
                        country_stats[country][method_name]["ok"] += 1

            # Determine best method
            best = None
            for m in ["curl", "webfetch", "diffbot", "playwright"]:
                if statuses.get(m) == "OK":
                    best = m
                    break

            url_results.append({
                "url": url,
                "statuses": statuses,
                "best_method": best,
            })

        # Source-level best method: prefer the simplest method that gets all URLs
        source_method_scores = {}
        for m in methods:
            ok = sum(1 for u in url_results if u["statuses"].get(m) == "OK")
            tested = sum(1 for u in url_results if m in u["statuses"])
            source_method_scores[m] = (ok, tested)

        # Pick the simplest method that achieves max success
        max_ok = max(s[0] for s in source_method_scores.values())
        source_best = "NONE"
        for m in ["curl", "webfetch", "diffbot", "playwright"]:
            if source_method_scores[m][0] == max_ok and max_ok > 0:
                source_best = m
                break

        any_ok = any(u["best_method"] is not None for u in url_results)

        comparison[source_key] = {
            "domain": domain,
            "country": country,
            "recommended_method": source_best,
            "reachable": any_ok,
            "method_scores": {
                m: f"{s[0]}/{s[1]}" if s[1] > 0 else "--"
                for m, s in source_method_scores.items()
            },
            "urls": url_results,
        }

    # Save JSON
    with open(OUTPUT_JSON, "w") as f:
        json.dump(comparison, f, indent=2, ensure_ascii=False)

    # Generate markdown report
    lines = [
        "# Government Source Retrieval — Cross-Method Comparison",
        "",
        f"**Date:** 2026-03-21",
        f"**Sources tested:** {len(all_sources)}",
        f"**Total URLs:** {sum(s['total_urls'] for s in country_stats.values())}",
        "",
        "## Method Summary",
        "",
    ]

    # Overall stats
    for method_name in ["curl", "webfetch", "diffbot", "playwright"]:
        total_ok = sum(cs[method_name]["ok"] for cs in country_stats.values())
        total_tested = sum(cs[method_name]["tested"] for cs in country_stats.values())
        if total_tested > 0:
            lines.append(f"- **{method_name}**: {total_ok}/{total_tested} ({100*total_ok/total_tested:.0f}%)")
        else:
            lines.append(f"- **{method_name}**: not run")

    # Recommended method distribution
    method_counts = {}
    unreachable = 0
    for s in comparison.values():
        m = s["recommended_method"]
        if m == "NONE":
            unreachable += 1
        else:
            method_counts[m] = method_counts.get(m, 0) + 1

    lines.extend([
        "",
        "## Recommended Method Distribution",
        "",
    ])
    for m in ["curl", "webfetch", "diffbot", "playwright"]:
        if m in method_counts:
            lines.append(f"- **{m}**: {method_counts[m]} sources")
    if unreachable:
        lines.append(f"- **unreachable**: {unreachable} sources (all methods failed)")

    # Per-country table
    lines.extend([
        "",
        "## Per-Country Results",
        "",
        "| Country | URLs | curl | WebFetch | Diffbot | Playwright |",
        "|---|---|---|---|---|---|",
    ])

    for country in sorted(country_stats):
        cs = country_stats[country]
        total = cs["total_urls"]
        cols = [f"{country}", f"{total}"]
        for m in ["curl", "webfetch", "diffbot", "playwright"]:
            ok = cs[m]["ok"]
            tested = cs[m]["tested"]
            if tested > 0:
                cols.append(f"{ok}/{tested} ({100*ok/tested:.0f}%)")
            else:
                cols.append("--")
        lines.append("| " + " | ".join(cols) + " |")

    # Per-source table
    lines.extend([
        "",
        "## Per-Source Detail",
        "",
        "| Source | Domain | curl | WebFetch | Diffbot | Playwright | Best |",
        "|---|---|---|---|---|---|---|",
    ])

    for sk in all_sources:
        c = comparison[sk]
        cols = [
            f"`{sk}`",
            f"`{c['domain']}`",
        ]
        for m in ["curl", "webfetch", "diffbot", "playwright"]:
            cols.append(c["method_scores"].get(m, "--"))
        cols.append(f"**{c['recommended_method']}**")
        lines.append("| " + " | ".join(cols) + " |")

    # Unreachable sources
    unreachable_sources = [
        (sk, comparison[sk]["domain"], comparison[sk]["country"])
        for sk in all_sources if not comparison[sk]["reachable"]
    ]
    if unreachable_sources:
        lines.extend([
            "",
            "## Unreachable Sources (all methods failed)",
            "",
        ])
        for sk, domain, country in unreachable_sources:
            lines.append(f"- `{sk}` ({domain}) — {country}")

    with open(OUTPUT_MD, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Saved comparison → {OUTPUT_JSON}")
    print(f"Saved report     → {OUTPUT_MD}")


if __name__ == "__main__":
    main()
