"""
A/B test: default curl user-agent vs Firefox user-agent.

Fetches the same URLs with both user agents and compares response
status codes, content lengths, and whether article content was received.
"""

import json
import subprocess
import random
import time
from pathlib import Path

# Config
SAMPLE_SIZE = 50  # URLs to test
TIMEOUT = 15  # seconds per request
FIREFOX_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:149.0) Gecko/20100101 Firefox/149.0"

OUTPUT_DIR = Path(__file__).parent
URLS_FILE = OUTPUT_DIR / "test_urls.json"


def curl_fetch(url: str, user_agent: str | None = None) -> dict:
    """Fetch a URL with curl, optionally with a custom user agent."""
    cmd = [
        "curl", "-sS", "-L",
        "--max-time", str(TIMEOUT),
        "-o", "/dev/null",
        "-w", json.dumps({
            "http_code": "%{http_code}",
            "size_download": "%{size_download}",
            "time_total": "%{time_total}",
            "url_effective": "%{url_effective}",
        }),
    ]
    if user_agent:
        cmd += ["-H", f"User-Agent: {user_agent}"]
    cmd.append(url)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT + 5)
        info = json.loads(result.stdout)
        return {
            "http_code": int(info["http_code"]),
            "size_download": int(info["size_download"]),
            "time_total": float(info["time_total"]),
            "error": None,
        }
    except Exception as e:
        return {
            "http_code": 0,
            "size_download": 0,
            "time_total": 0,
            "error": str(e),
        }


def main():
    with open(URLS_FILE) as f:
        all_urls = json.load(f)

    # Sample
    random.seed(42)
    urls = random.sample(all_urls, min(SAMPLE_SIZE, len(all_urls)))
    print(f"Testing {len(urls)} URLs with default UA vs Firefox UA\n")

    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url[:80]}...")

        # Default UA
        default = curl_fetch(url)
        time.sleep(0.3)

        # Firefox UA
        firefox = curl_fetch(url, FIREFOX_UA)
        time.sleep(0.3)

        result = {
            "url": url,
            "default": default,
            "firefox": firefox,
        }
        results.append(result)

        # Quick status
        d_code, f_code = default["http_code"], firefox["http_code"]
        d_size, f_size = default["size_download"], firefox["size_download"]
        diff = "SAME" if d_code == f_code and abs(d_size - f_size) < 500 else "DIFF"
        print(f"  default: {d_code} ({d_size:,}B) | firefox: {f_code} ({f_size:,}B) [{diff}]")

    # Save raw results
    with open(OUTPUT_DIR / "ab_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Analyze
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total = len(results)
    same_status = sum(1 for r in results if r["default"]["http_code"] == r["firefox"]["http_code"])
    default_ok = sum(1 for r in results if r["default"]["http_code"] == 200)
    firefox_ok = sum(1 for r in results if r["firefox"]["http_code"] == 200)
    firefox_only = sum(
        1 for r in results
        if r["firefox"]["http_code"] == 200 and r["default"]["http_code"] != 200
    )
    default_only = sum(
        1 for r in results
        if r["default"]["http_code"] == 200 and r["firefox"]["http_code"] != 200
    )

    # Size comparison (only where both got 200)
    both_ok = [r for r in results if r["default"]["http_code"] == 200 and r["firefox"]["http_code"] == 200]
    bigger_firefox = sum(1 for r in both_ok if r["firefox"]["size_download"] > r["default"]["size_download"] + 500)
    bigger_default = sum(1 for r in both_ok if r["default"]["size_download"] > r["firefox"]["size_download"] + 500)
    size_same = len(both_ok) - bigger_firefox - bigger_default

    # Blocked detection (403, 429, or very small response)
    default_blocked = sum(
        1 for r in results
        if r["default"]["http_code"] in (403, 429, 406, 451)
        or (r["default"]["http_code"] == 200 and r["default"]["size_download"] < 1000)
    )
    firefox_blocked = sum(
        1 for r in results
        if r["firefox"]["http_code"] in (403, 429, 406, 451)
        or (r["firefox"]["http_code"] == 200 and r["firefox"]["size_download"] < 1000)
    )

    print(f"Total URLs tested:       {total}")
    print(f"Same HTTP status:        {same_status}/{total}")
    print(f"")
    print(f"HTTP 200 (default UA):   {default_ok}/{total}")
    print(f"HTTP 200 (Firefox UA):   {firefox_ok}/{total}")
    print(f"Firefox-only success:    {firefox_only}")
    print(f"Default-only success:    {default_only}")
    print(f"")
    print(f"Likely blocked (default): {default_blocked}")
    print(f"Likely blocked (Firefox): {firefox_blocked}")
    print(f"")
    print(f"Where both got 200 ({len(both_ok)} URLs):")
    print(f"  Firefox returned more content: {bigger_firefox}")
    print(f"  Default returned more content: {bigger_default}")
    print(f"  Similar content size:          {size_same}")

    # Show the interesting diffs
    diffs = [r for r in results if r["default"]["http_code"] != r["firefox"]["http_code"]]
    if diffs:
        print(f"\n--- Status code differences ({len(diffs)}) ---")
        for r in diffs:
            print(f"  {r['url'][:70]}")
            print(f"    default={r['default']['http_code']} firefox={r['firefox']['http_code']}")

    # Save summary
    summary = {
        "total": total,
        "same_status": same_status,
        "default_200": default_ok,
        "firefox_200": firefox_ok,
        "firefox_only_success": firefox_only,
        "default_only_success": default_only,
        "default_blocked": default_blocked,
        "firefox_blocked": firefox_blocked,
        "both_ok_count": len(both_ok),
        "firefox_bigger": bigger_firefox,
        "default_bigger": bigger_default,
        "size_same": size_same,
        "status_diffs": [
            {
                "url": r["url"],
                "default_code": r["default"]["http_code"],
                "firefox_code": r["firefox"]["http_code"],
            }
            for r in diffs
        ],
    }
    with open(OUTPUT_DIR / "ab_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
