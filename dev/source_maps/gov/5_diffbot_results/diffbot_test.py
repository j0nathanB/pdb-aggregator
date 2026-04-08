#!/usr/bin/env python3
"""
Method 3: Diffbot API extraction on URLs that failed curl+trafilatura.

Reads curl_results.json to find failures, runs Diffbot /v3/article
with /v3/analyze fallback, saves results.

Rate limit: 5 calls/minute.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CURL_RESULTS = Path(__file__).parent.parent / "3_curl_results" / "curl_results.json"
INPUT_URLS = Path(__file__).parent.parent / "3_curl_results" / "input_urls.json"
OUTPUT = Path(__file__).parent / "diffbot_results.json"

# Load token from .env
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[4] / ".env")

TOKEN = os.environ.get("DIFFBOT_TOKEN")
if not TOKEN:
    print("ERROR: DIFFBOT_TOKEN not found", file=sys.stderr)
    sys.exit(1)

ARTICLE_URL = f"https://api.diffbot.com/v3/article?token={TOKEN}"
ANALYZE_URL = f"https://api.diffbot.com/v3/analyze?token={TOKEN}"

call_times = []


def rate_limited_fetch(url):
    """Respect 5 calls/min limit."""
    global call_times
    now = time.time()
    call_times = [t for t in call_times if now - t < 60]
    if len(call_times) >= 5:
        wait = 60 - (now - call_times[0]) + 0.5
        if wait > 0:
            print(f"    (rate limit: waiting {wait:.0f}s)", flush=True)
            time.sleep(wait)
        call_times = [t for t in call_times if time.time() - t < 60]
    call_times.append(time.time())
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode())


def main():
    # Load curl results to find failures
    curl_results = json.load(open(CURL_RESULTS))
    input_data = json.load(open(INPUT_URLS))

    # Collect failed URLs grouped by source
    failed_sources = {}
    for source_key, source_data in curl_results.items():
        failed_urls = []
        for r in source_data["results"]:
            if r["status"] != "OK":
                failed_urls.append(r["url"])
        if failed_urls:
            failed_sources[source_key] = {
                "domain": source_data["domain"],
                "country": source_data["country"],
                "urls": failed_urls,
            }

    total_urls = sum(len(v["urls"]) for v in failed_sources.values())
    print(f"Testing {total_urls} URLs that failed curl+trafilatura across {len(failed_sources)} sources\n")

    results = {}
    processed = 0

    for source_key in sorted(failed_sources.keys()):
        entry = failed_sources[source_key]
        source_results = []

        for url in entry["urls"]:
            processed += 1
            encoded = urllib.parse.quote(url, safe="")
            status, api_used, snippet, chars = "FAILED", None, None, 0

            # Try /v3/article first
            try:
                data = rate_limited_fetch(f"{ARTICLE_URL}&url={encoded}")
                objects = data.get("objects", [])
                if objects and objects[0].get("text", "").strip():
                    text = objects[0]["text"]
                    if len(text) > 100:
                        status, api_used = "OK", "article"
                        snippet = text[:300]
                        chars = len(text)
            except Exception:
                pass

            # Fallback to /v3/analyze
            if status != "OK":
                try:
                    data = rate_limited_fetch(f"{ANALYZE_URL}&url={encoded}")
                    objects = data.get("objects", [])
                    if objects and objects[0].get("text", "").strip():
                        text = objects[0]["text"]
                        if len(text) > 100:
                            status, api_used = "OK", "analyze"
                            snippet = text[:300]
                            chars = len(text)
                except Exception:
                    pass

            source_results.append({
                "url": url,
                "status": status,
                "api_used": api_used,
                "chars": chars,
                "snippet": snippet,
            })

        ok = sum(1 for r in source_results if r["status"] == "OK")
        results[source_key] = {
            "domain": entry["domain"],
            "country": entry["country"],
            "ok": ok,
            "total": len(source_results),
            "score": f"{ok}/{len(source_results)}",
            "results": source_results,
        }

        status_char = "✓" if ok == len(source_results) else ("◐" if ok > 0 else "✗")
        print(f"  [{processed:3d}/{total_urls}] {status_char} {source_key}: {ok}/{len(source_results)}")

    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    total_ok = sum(r["ok"] for r in results.values())
    total = sum(r["total"] for r in results.values())
    print(f"\n{'='*50}")
    print(f"  Diffbot: {total_ok}/{total} previously-failed URLs now OK ({100*total_ok/total:.0f}%)")
    print(f"  Saved → {OUTPUT}")


if __name__ == "__main__":
    main()
