#!/usr/bin/env python3
"""
Method 4: Playwright headless browser extraction on URLs that failed
both curl+trafilatura and Diffbot.

Reads previous results to find remaining failures, renders pages in
Chromium, extracts text via trafilatura.
"""

import json
from pathlib import Path

import trafilatura
from playwright.sync_api import sync_playwright

CURL_RESULTS = Path(__file__).parent.parent / "3_curl_results" / "curl_results.json"
DIFFBOT_RESULTS = Path(__file__).parent.parent / "5_diffbot_results" / "diffbot_results.json"
INPUT_URLS = Path(__file__).parent.parent / "3_curl_results" / "input_urls.json"
OUTPUT = Path(__file__).parent / "playwright_results.json"

MIN_TEXT_LENGTH = 100

COOKIE_SELECTORS = [
    "button:has-text('Accept')",
    "button:has-text('Agree')",
    "button:has-text('OK')",
    "button:has-text('Accepter')",
    "button:has-text('Akzeptieren')",
    "button:has-text('Aceptar')",
    "[id*='cookie'] button",
    "[class*='consent'] button",
    "[class*='cookie'] button",
]


def collect_still_failed():
    """Find URLs that failed both curl and diffbot."""
    curl = json.load(open(CURL_RESULTS))

    # All curl failures
    curl_failures = {}
    for source_key, source_data in curl.items():
        failed = [r["url"] for r in source_data["results"] if r["status"] != "OK"]
        if failed:
            curl_failures[source_key] = {
                "domain": source_data["domain"],
                "country": source_data["country"],
                "urls": set(failed),
            }

    # Remove diffbot successes
    try:
        diffbot = json.load(open(DIFFBOT_RESULTS))
        for source_key, source_data in diffbot.items():
            if source_key in curl_failures:
                for r in source_data["results"]:
                    if r["status"] == "OK":
                        curl_failures[source_key]["urls"].discard(r["url"])
                if not curl_failures[source_key]["urls"]:
                    del curl_failures[source_key]
    except FileNotFoundError:
        pass  # Diffbot hasn't run yet — test all curl failures

    # Convert sets back to lists
    for k in curl_failures:
        curl_failures[k]["urls"] = list(curl_failures[k]["urls"])

    return curl_failures


def main():
    failed_sources = collect_still_failed()
    total_urls = sum(len(v["urls"]) for v in failed_sources.values())
    print(f"Testing {total_urls} still-failed URLs across {len(failed_sources)} sources\n")

    results = {}
    processed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        for source_key in sorted(failed_sources.keys()):
            entry = failed_sources[source_key]
            source_results = []

            for url in entry["urls"]:
                processed += 1
                page = None
                try:
                    page = context.new_page()
                    page.goto(url, timeout=30000, wait_until="networkidle")

                    # Try to dismiss cookie banners
                    for selector in COOKIE_SELECTORS:
                        try:
                            page.click(selector, timeout=2000)
                        except Exception:
                            pass

                    page.wait_for_timeout(2000)
                    html = page.content()
                    page.close()
                    page = None

                    text = trafilatura.extract(html)
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
                            "reason": "insufficient text after extraction",
                            "chars": len(text) if text else 0,
                        })
                except Exception as e:
                    source_results.append({
                        "url": url,
                        "status": "FAILED",
                        "reason": str(e)[:200],
                    })
                finally:
                    if page:
                        try:
                            page.close()
                        except Exception:
                            pass

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

        browser.close()

    with open(OUTPUT, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    total_ok = sum(r["ok"] for r in results.values())
    total = sum(r["total"] for r in results.values())
    pct = 100 * total_ok / total if total else 0
    print(f"\n{'='*50}")
    print(f"  Playwright: {total_ok}/{total} previously-failed URLs now OK ({pct:.0f}%)")
    print(f"  Saved → {OUTPUT}")


if __name__ == "__main__":
    main()
