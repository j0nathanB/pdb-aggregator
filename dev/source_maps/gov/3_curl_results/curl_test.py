#!/usr/bin/env python3
"""
Method 1: curl + trafilatura extraction on government source URLs.

Reads input_urls.json, fetches each URL, extracts text via trafilatura,
and saves structured results to curl_results.json.
"""

import json
import sys
import time
from pathlib import Path

import trafilatura

INPUT = Path(__file__).parent / "input_urls.json"
OUTPUT = Path(__file__).parent / "curl_results.json"

MIN_TEXT_LENGTH = 100  # chars — below this we count as failed


def main():
    input_data = json.load(open(INPUT))
    results = {}
    total_ok = 0
    total_fail = 0
    total_urls = sum(len(v["urls"]) for v in input_data.values())

    processed = 0
    for source_key in sorted(input_data.keys()):
        entry = input_data[source_key]
        domain = entry["domain"]
        country = entry["country"]
        urls = entry["urls"]

        source_results = []
        for item in urls:
            url = item["url"]
            processed += 1
            try:
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    text = trafilatura.extract(downloaded)
                    if text and len(text.strip()) > MIN_TEXT_LENGTH:
                        source_results.append({
                            "url": url,
                            "status": "OK",
                            "chars": len(text),
                            "snippet": text[:300],
                        })
                    else:
                        source_results.append({
                            "url": url,
                            "status": "FAILED",
                            "reason": "extraction returned insufficient text",
                            "chars": len(text) if text else 0,
                        })
                else:
                    source_results.append({
                        "url": url,
                        "status": "FAILED",
                        "reason": "fetch returned None",
                    })
            except Exception as e:
                source_results.append({
                    "url": url,
                    "status": "FAILED",
                    "reason": str(e)[:200],
                })

            # Light rate limiting to be polite
            time.sleep(0.5)

        ok = sum(1 for r in source_results if r["status"] == "OK")
        total_ok += ok
        total_fail += len(source_results) - ok

        results[source_key] = {
            "domain": domain,
            "country": country,
            "ok": ok,
            "total": len(source_results),
            "score": f"{ok}/{len(source_results)}",
            "results": source_results,
        }

        status_char = "✓" if ok == len(source_results) else ("◐" if ok > 0 else "✗")
        print(f"  [{processed:3d}/{total_urls}] {status_char} {source_key}: {ok}/{len(source_results)}")

    # Save results
    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    total = total_ok + total_fail
    print(f"\n{'='*50}")
    print(f"  curl+trafilatura: {total_ok}/{total} URLs OK ({100*total_ok/total:.0f}%)")
    print(f"  Saved → {OUTPUT}")

    # Per-country summary
    country_stats = {}
    for key, r in results.items():
        c = r["country"]
        if c not in country_stats:
            country_stats[c] = {"ok": 0, "total": 0}
        country_stats[c]["ok"] += r["ok"]
        country_stats[c]["total"] += r["total"]

    print(f"\n  Per-country breakdown:")
    for c in sorted(country_stats):
        s = country_stats[c]
        pct = 100 * s["ok"] / s["total"] if s["total"] else 0
        print(f"    {c:25s} {s['ok']:3d}/{s['total']:<3d} ({pct:.0f}%)")


if __name__ == "__main__":
    main()
