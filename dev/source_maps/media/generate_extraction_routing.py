#!/usr/bin/env python3
"""
Generate extraction routing table from test results.

Reads:
- 2_claude_fetch_results/WEBFETCH_REPORT.md — Claude scores for 377 domains
- 6_all_results_analysis/REPORT.md — Cross-method comparison for 182 fallback domains

Outputs:
- assets/country_configs/extraction_routing.yaml — per-domain routing config

Usage:
    python generate_extraction_routing.py
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent
CLAUDE_REPORT = BASE_DIR / "2_claude_fetch_results" / "WEBFETCH_REPORT.md"
COMPARISON_REPORT = BASE_DIR / "6_all_results_analysis" / "REPORT.md"
OUTPUT_PATH = BASE_DIR.parent.parent.parent / "assets" / "country_configs" / "extraction_routing.yaml"

# Publisher API mappings
PUBLISHER_APIS = {
    "theguardian.com": "guardian",
    "ft.com": "ft",
}


def parse_score(score_str: str) -> tuple[int, int]:
    """Parse '2/3' into (ok, total)."""
    m = re.match(r"(\d+)/(\d+)", score_str.strip())
    if m:
        return int(m.group(1)), int(m.group(2))
    return 0, 0


def score_to_confidence(ok: int, total: int) -> str | None:
    """Convert score to confidence level."""
    if total == 0:
        return None
    ratio = ok / total
    if ratio >= 1.0:
        return "high"
    elif ratio >= 0.66:
        return "medium"
    elif ratio > 0:
        return "low"
    return None


def parse_claude_report(text: str) -> dict[str, tuple[int, int]]:
    """Parse WEBFETCH_REPORT.md → {domain: (ok, total)}."""
    scores = {}
    for line in text.split("\n"):
        m = re.match(
            r"\|\s*\d+\s*\|\s*`(.+?)`\s*\|.*\|\s*(\d+/\d+)\s*\|",
            line,
        )
        if m:
            domain = m.group(1).strip().lower()
            scores[domain] = parse_score(m.group(2))
    return scores


def parse_comparison_report(text: str) -> dict[str, dict]:
    """Parse cross-method REPORT.md → {domain: {claude, diffbot, curl, playwright, best}}."""
    results = {}
    for line in text.split("\n"):
        m = re.match(
            r"\|\s*\d+\s*\|\s*`(.+?)`\s*\|\s*(\d+/\d+)\s*\|\s*(\d+/\d+)\s*\|\s*(\d+/\d+)\s*\|\s*(\d+/\d+)\s*\|\s*(\w+)\s*\|",
            line,
        )
        if m:
            domain = m.group(1).strip().lower()
            results[domain] = {
                "claude": parse_score(m.group(2)),
                "diffbot": parse_score(m.group(3)),
                "curl": parse_score(m.group(4)),
                "playwright": parse_score(m.group(5)),
                "best": m.group(6).strip().lower(),
            }
    return results


def build_fallbacks(comp: dict, primary: str) -> list[str]:
    """Build fallback chain from comparison data, excluding the primary method.

    Order: curl → playwright → browserbase → diffbot.
    Diffbot is always last-resort due to its 5 calls/min rate limit.
    Browserbase is preferred over diffbot for bot-protected sites.
    """
    methods = []
    for method in ["curl", "playwright", "browserbase", "diffbot"]:
        if method == primary:
            continue
        ok, total = comp.get(method, (0, 0))
        if ok > 0:
            methods.append(method)
    return methods


def main():
    claude_text = CLAUDE_REPORT.read_text()
    comparison_text = COMPARISON_REPORT.read_text()

    claude_scores = parse_claude_report(claude_text)
    comparison_data = parse_comparison_report(comparison_text)

    routes = {}

    for domain, (ok, total) in sorted(claude_scores.items()):
        # Check for Publisher API
        publisher = PUBLISHER_APIS.get(domain)

        if publisher:
            # Publisher API domains
            route = {
                "primary": "publisher_api",
                "confidence": "high",
                "fallbacks": ["curl", "playwright", "browserbase", "diffbot"],
                "publisher_api": publisher,
            }
        elif ok == total and total > 0:
            # Claude 3/3 (or 2/2, 1/1) — Claude is primary
            route = {
                "primary": "claude",
                "confidence": "high",
                "fallbacks": ["curl", "playwright", "browserbase", "diffbot"],
            }
        elif domain in comparison_data:
            # Fallback domain — use comparison data
            comp = comparison_data[domain]
            best = comp["best"]

            if best == "none":
                route = {
                    "primary": "snippet_only",
                    "confidence": None,
                    "fallbacks": [],
                }
            else:
                best_ok, best_total = comp[best]
                confidence = score_to_confidence(best_ok, best_total)
                fallbacks = build_fallbacks(comp, best)

                route = {
                    "primary": best,
                    "confidence": confidence,
                    "fallbacks": fallbacks,
                }
        else:
            # Domain not in comparison table but Claude < 3/3
            # This shouldn't happen (all non-3/3 domains were tested)
            # Default to curl fallback chain
            route = {
                "primary": "curl",
                "confidence": None,
                "fallbacks": ["playwright", "browserbase", "diffbot"],
            }

        routes[domain] = route

    # Build output
    config = {
        "_generated_from": [
            "dev/source_maps/media/2_claude_fetch_results/WEBFETCH_REPORT.md",
            "dev/source_maps/media/6_all_results_analysis/REPORT.md",
        ],
        "_note": "Do not edit manually. Regenerate with: python dev/source_maps/media/generate_extraction_routing.py",
        "test_methodology": "3 URLs per domain, 4 methods tested",
        "domains_total": len(routes),
        "default_fallback_chain": ["curl", "playwright", "browserbase", "diffbot", "snippet_only"],
        "concurrency": {
            "curl": 20,
            "diffbot": 5,
            "playwright": 3,
            "browserbase": 10,
            "publisher_api": 5,
        },
        "rate_limits": {
            "per_domain_delay_seconds": 1.0,
            "max_urls_per_domain": 5,
        },
        "routes": routes,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)

    # Stats
    primaries = {}
    for r in routes.values():
        p = r["primary"]
        primaries[p] = primaries.get(p, 0) + 1

    print(f"Generated {OUTPUT_PATH}")
    print(f"  {len(routes)} domains routed")
    print(f"  Primary method distribution:")
    for method, count in sorted(primaries.items(), key=lambda x: -x[1]):
        print(f"    {method}: {count} ({100*count//len(routes)}%)")


if __name__ == "__main__":
    main()
