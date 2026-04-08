#!/usr/bin/env python3
"""
Test domains that scored 2/3 or less in the Claude WebFetch test
using trafilatura for article extraction via HTTP fetch.
"""

import json
import re
import glob
import os
import time
import traceback
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import trafilatura

BASE = Path(__file__).resolve().parent.parent
WEBFETCH_REPORT = BASE / "2_claude_fetch_results" / "WEBFETCH_REPORT.md"
BRAVE_DIR = BASE / "0_brave_search_results"
OUTPUT_DIR = Path(__file__).resolve().parent
RESULTS_FILE = OUTPUT_DIR / "results.json"
REPORT_FILE = OUTPUT_DIR / "REPORT.md"


def parse_low_score_domains(report_path: str) -> dict[str, str]:
    """Extract domains scoring 2/3 or less from the WebFetch report."""
    domains = {}
    with open(report_path) as f:
        for line in f:
            m = re.match(
                r'\|\s*\d+\s*\|\s*`([^`]+)`\s*\|.*\|\s*(\d+/\d+)\s*\|', line
            )
            if m:
                domain = m.group(1)
                score = m.group(2)
                num, denom = map(int, score.split("/"))
                if num < denom or (num <= 2 and denom == 3):
                    domains[domain.lower()] = score
    return domains


def collect_urls_from_brave(brave_dir: str, target_domains: set[str]) -> dict[str, list[str]]:
    """Collect up to 3 URLs per domain from brave search JSON results."""
    domain_urls: dict[str, list[str]] = {d: [] for d in target_domains}

    for jf in sorted(glob.glob(os.path.join(brave_dir, "*.json"))):
        with open(jf) as f:
            data = json.load(f)

        for source_name, source_data in data.get("sources", {}).items():
            for result in source_data.get("results", []):
                url = result.get("url", "")
                if not url:
                    continue
                parsed = urlparse(url)
                hostname = parsed.hostname or ""
                # Match against target domains (domain could be suffix)
                for td in target_domains:
                    if hostname == td or hostname.endswith("." + td):
                        if url not in domain_urls[td] and len(domain_urls[td]) < 3:
                            domain_urls[td].append(url)

    return {d: urls for d, urls in domain_urls.items() if urls}


def test_url_trafilatura(url: str, timeout: int = 30) -> dict:
    """Fetch a URL with trafilatura and check if article content is extracted."""
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            return {"url": url, "status": "FAILED", "reason": "fetch returned None", "content_length": 0}

        text = trafilatura.extract(downloaded)
        if text and len(text.strip()) > 100:
            return {
                "url": url,
                "status": "OK",
                "reason": "article content extracted",
                "content_length": len(text),
                "excerpt": text[:200].replace("\n", " "),
            }
        elif text:
            return {
                "url": url,
                "status": "FAILED",
                "reason": f"extracted text too short ({len(text.strip())} chars)",
                "content_length": len(text.strip()),
            }
        else:
            return {
                "url": url,
                "status": "FAILED",
                "reason": "trafilatura returned no text",
                "content_length": 0,
            }
    except Exception as e:
        return {
            "url": url,
            "status": "FAILED",
            "reason": str(e)[:200],
            "content_length": 0,
        }


def test_domain(domain: str, urls: list[str]) -> dict:
    """Test all URLs for a single domain."""
    results = []
    for url in urls:
        r = test_url_trafilatura(url)
        results.append(r)
        time.sleep(0.5)  # be polite
    ok_count = sum(1 for r in results if r["status"] == "OK")
    return {
        "domain": domain,
        "urls_tested": len(urls),
        "ok_count": ok_count,
        "score": f"{ok_count}/{len(urls)}",
        "results": results,
    }


def generate_report(all_results: list[dict], low_score_domains: dict[str, str]) -> str:
    """Generate a markdown report in the style of the Brave REPORT."""
    total_domains = len(all_results)
    total_urls = sum(r["urls_tested"] for r in all_results)
    total_ok = sum(r["ok_count"] for r in all_results)
    total_failed = total_urls - total_ok
    fully_accessible = sum(1 for r in all_results if r["ok_count"] == r["urls_tested"])
    partially = sum(1 for r in all_results if 0 < r["ok_count"] < r["urls_tested"])
    fully_inaccessible = sum(1 for r in all_results if r["ok_count"] == 0)

    # Compare with WebFetch scores
    improved = []
    same = []
    worse = []
    for r in all_results:
        wf_score = low_score_domains.get(r["domain"], "?/?")
        wf_num, wf_denom = map(int, wf_score.split("/"))
        traf_num = r["ok_count"]
        traf_denom = r["urls_tested"]
        wf_ratio = wf_num / wf_denom if wf_denom > 0 else 0
        traf_ratio = traf_num / traf_denom if traf_denom > 0 else 0
        if traf_ratio > wf_ratio:
            improved.append(r)
        elif traf_ratio < wf_ratio:
            worse.append(r)
        else:
            same.append(r)

    lines = [
        "# Trafilatura Article Extraction Test Report",
        "",
        f"**Generated:** 2026-03-20",
        "",
        "**Method:** For each source domain that scored 2/3 or less in the Claude WebFetch test, "
        "fetched up to 3 article URLs (from Brave search results) using `trafilatura.fetch_url()` + "
        "`trafilatura.extract()`. A successful result means article content (>100 chars) was extracted.",
        "",
        "---",
        "",
        f"**Total domains tested:** {total_domains}",
        f"**Total URL fetch attempts:** {total_urls}",
        f"**Successful article extractions (OK):** {total_ok} ({total_ok*100//total_urls}%)" if total_urls else "",
        f"**Failed extractions (FAILED):** {total_failed} ({total_failed*100//total_urls}%)" if total_urls else "",
        "",
        f"**Fully accessible domains (all URLs OK):** {fully_accessible} ({fully_accessible*100//total_domains}%)" if total_domains else "",
        f"**Partially accessible domains:** {partially} ({partially*100//total_domains}%)" if total_domains else "",
        f"**Fully inaccessible domains (0 OK):** {fully_inaccessible} ({fully_inaccessible*100//total_domains}%)" if total_domains else "",
        "",
        "## Comparison with Claude WebFetch",
        "",
        f"**Improved over WebFetch:** {len(improved)} domains",
        f"**Same as WebFetch:** {len(same)} domains",
        f"**Worse than WebFetch:** {len(worse)} domains",
        "",
        "## Full Results",
        "",
        "| # | Domain | WebFetch Score | URL 1 | URL 2 | URL 3 | Trafilatura Score |",
        "|---|--------|---------------|-------|-------|-------|-------------------|",
    ]

    for i, r in enumerate(sorted(all_results, key=lambda x: x["domain"]), 1):
        wf_score = low_score_domains.get(r["domain"], "?/?")
        url_cols = []
        for j in range(3):
            if j < len(r["results"]):
                url_cols.append(r["results"][j]["status"])
            else:
                url_cols.append("--")
        lines.append(
            f"| {i} | `{r['domain']}` | {wf_score} | {url_cols[0]} | {url_cols[1]} | {url_cols[2]} | {r['score']} |"
        )

    # Improved domains section
    if improved:
        lines.extend(["", "## Improved Domains (trafilatura > WebFetch)", ""])
        for r in sorted(improved, key=lambda x: x["domain"]):
            wf_score = low_score_domains.get(r["domain"], "?/?")
            lines.append(f"- `{r['domain']}`: {wf_score} → {r['score']}")

    # Still inaccessible
    if fully_inaccessible > 0:
        lines.extend(["", "## Still Inaccessible (0 OK with both methods)", ""])
        for r in sorted(all_results, key=lambda x: x["domain"]):
            if r["ok_count"] == 0:
                wf_score = low_score_domains.get(r["domain"], "?/?")
                if wf_score.startswith("0/"):
                    lines.append(f"- `{r['domain']}`")

    lines.append("")
    return "\n".join(lines)


def main():
    print("Parsing WebFetch report for low-score domains...")
    low_score_domains = parse_low_score_domains(str(WEBFETCH_REPORT))
    print(f"Found {len(low_score_domains)} domains scoring 2/3 or less")

    print("Collecting URLs from Brave search results...")
    domain_urls = collect_urls_from_brave(str(BRAVE_DIR), set(low_score_domains.keys()))
    print(f"Found URLs for {len(domain_urls)} domains")

    domains_without_urls = set(low_score_domains.keys()) - set(domain_urls.keys())
    if domains_without_urls:
        print(f"No URLs found for {len(domains_without_urls)} domains: {sorted(domains_without_urls)[:10]}...")

    print("\nTesting domains with trafilatura...")
    all_results = []
    total = len(domain_urls)

    for i, (domain, urls) in enumerate(sorted(domain_urls.items()), 1):
        print(f"  [{i}/{total}] {domain} ({len(urls)} URLs)...", end=" ", flush=True)
        result = test_domain(domain, urls)
        all_results.append(result)
        print(f"{result['score']}")

    # Save raw results
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results saved to {RESULTS_FILE}")

    # Generate and save report
    report = generate_report(all_results, low_score_domains)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
