#!/usr/bin/env python3
"""
Build input_urls.json from SearchAPI results.

Selects up to 3 URLs per domain, preferring pages with news/media/release
in the URL path (higher signal) over structural/procedural pages.
"""

import json
import os
import re
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "2_search-api_results"
OUTPUT = Path(__file__).parent / "input_urls.json"

# Prefer URLs containing these patterns (news/release pages)
GOOD_PATTERNS = re.compile(
    r"(media-release|news|press|statement|speech|transcript|communique|"
    r"release|bulletin|rapport|comunicado|mitteilung|dichiarazione|"
    r"noticias|actualites|actualite|discours|besluit|"
    r"media|communicato|actualidad|meddelande)",
    re.IGNORECASE,
)

# Skip URLs matching these (structural, search pages, PDFs, career pages)
BAD_PATTERNS = re.compile(
    r"(\?q=|/search|/career|/job|/about|/contact|/faq|/rss|"
    r"\.pdf$|/tag/|/taxonomy/|/subscribe|/feed|/sitemap|"
    r"/chart-pack|/org-chart|/blueprint\.|/configuration/)",
    re.IGNORECASE,
)


def score_url(url: str) -> int:
    """Higher = better candidate for content extraction."""
    if BAD_PATTERNS.search(url):
        return -1
    s = 0
    if GOOD_PATTERNS.search(url):
        s += 10
    # Prefer dated URLs (contain year pattern like /2026/)
    if re.search(r"/202[4-6]", url):
        s += 5
    return s


def main():
    input_urls = {}

    for f in sorted(os.listdir(RESULTS_DIR)):
        if not f.endswith(".json"):
            continue

        with open(RESULTS_DIR / f) as fh:
            country_data = json.load(fh)

        country = country_data["country"]

        for source in country_data["sources"]:
            if not source["results"]:
                continue

            domain = source["domain"]
            source_id = source["id"]
            key = f"{country}/{source_id}"

            # Score and sort URLs
            candidates = []
            seen = set()
            for r in source["results"]:
                url = r["url"]
                if url in seen:
                    continue
                seen.add(url)
                s = score_url(url)
                if s >= 0:
                    candidates.append((s, url, r.get("title", ""), r.get("date", "")))

            candidates.sort(key=lambda x: x[0], reverse=True)

            # Take top 3
            selected = candidates[:3]
            if selected:
                input_urls[key] = {
                    "domain": domain,
                    "country": country,
                    "urls": [
                        {"url": u, "title": t, "date": d}
                        for _, u, t, d in selected
                    ],
                }

    with open(OUTPUT, "w") as f:
        json.dump(input_urls, f, indent=2, ensure_ascii=False)

    # Stats
    total_domains = len(input_urls)
    total_urls = sum(len(v["urls"]) for v in input_urls.values())
    countries = len(set(v["country"] for v in input_urls.values()))
    print(f"Built {OUTPUT}")
    print(f"  {countries} countries, {total_domains} sources, {total_urls} URLs")


if __name__ == "__main__":
    main()
