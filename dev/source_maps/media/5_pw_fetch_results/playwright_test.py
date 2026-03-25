#!/usr/bin/env python3
"""
Tier 4: Playwright + trafilatura extraction test.
Tests domains that scored 2/3 or less in the Claude WebFetch test.
Uses headless Chromium to render JS-heavy pages, then trafilatura to extract article content.
"""

from __future__ import annotations

import asyncio
import json
import re
import glob
import os
import logging
import time
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
from typing import Optional

import trafilatura
from trafilatura.metadata import extract_metadata
from playwright.async_api import async_playwright

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE = Path(__file__).resolve().parent.parent
WEBFETCH_REPORT = BASE / "2_claude_fetch_results" / "WEBFETCH_REPORT.md"
BRAVE_DIR = BASE / "0_brave_search_results"
OUTPUT_DIR = Path(__file__).resolve().parent
RESULTS_FILE = OUTPUT_DIR / "results.json"
REPORT_FILE = OUTPUT_DIR / "REPORT.md"

CONSENT_SELECTORS = [
    "button[id*='accept']",
    "button[id*='consent']",
    "button[class*='accept']",
    "button[class*='consent']",
    "button:has-text('Accept')",
    "button:has-text('Accept all')",
    "button:has-text('Accepter')",
    "button:has-text('Akzeptieren')",
    "button:has-text('Accetta')",
    "button:has-text('Aceptar')",
    "button:has-text('Godkänn')",
    "button:has-text('Hyväksy')",
    "[data-testid='cookie-accept']",
    "#onetrust-accept-btn-handler",
    ".cookie-banner button:first-of-type",
]

CHALLENGE_INDICATORS = [
    "cf-browser-verification",
    "challenge-running",
    "captcha",
    "recaptcha",
    "hcaptcha",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


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
                for td in target_domains:
                    if hostname == td or hostname.endswith("." + td):
                        if url not in domain_urls[td] and len(domain_urls[td]) < 3:
                            domain_urls[td].append(url)

    return {d: urls for d, urls in domain_urls.items() if urls}


class PlaywrightExtractor:
    """Manages browser lifecycle across multiple extractions."""

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._contexts = {}  # domain -> context

    async def start(self):
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(headless=True)

    async def stop(self):
        for ctx in self._contexts.values():
            await ctx.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def _get_context(self, domain: str, language: str = "en"):
        if domain not in self._contexts:
            ctx = await self._browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent=USER_AGENT,
                locale=language,
                java_script_enabled=True,
            )
            await ctx.route(
                "**/*.{png,jpg,jpeg,gif,svg,webp,mp4,webm,woff,woff2,ttf,eot}",
                lambda route: route.abort()
            )
            self._contexts[domain] = ctx
        return self._contexts[domain]

    async def extract(self, url: str, language: str = "en") -> dict | None:
        domain = urlparse(url).netloc
        context = await self._get_context(domain, language)
        page = await context.new_page()

        try:
            # Navigate
            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                logger.warning(f"Navigation failed for {url}: {e}")
                await page.close()
                return None

            # Check for challenge pages
            page_text = await page.text_content("body") or ""
            if any(ind in page_text.lower() for ind in CHALLENGE_INDICATORS):
                logger.warning(f"Challenge page detected for {url}, skipping")
                await page.close()
                return None

            # Dismiss cookie consent
            for selector in CONSENT_SELECTORS:
                try:
                    button = page.locator(selector).first
                    if await button.is_visible(timeout=500):
                        await button.click()
                        await page.wait_for_timeout(500)
                        break
                except Exception:
                    continue

            # Scroll to trigger lazy content
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Get rendered HTML
            html = await page.content()

        except Exception as e:
            logger.error(f"Unexpected error for {url}: {e}", exc_info=True)
            await page.close()
            return None

        await page.close()

        # Extract with trafilatura
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
            favor_recall=True,
        )

        if not extracted or len(extracted) < 200:
            logger.warning(
                f"Extraction failed for {url}: content too short "
                f"({len(extracted) if extracted else 0} chars)"
            )
            return None

        # Extract metadata
        metadata = extract_metadata(html)
        title = metadata.title if metadata else None
        date = metadata.date if metadata else None

        return {
            "title": title,
            "text": extracted,
            "url": url,
            "date": date,
            "extraction_method": "playwright_trafilatura",
        }


async def test_url(extractor: PlaywrightExtractor, url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        try:
            result = await extractor.extract(url)
            if result and result["text"]:
                return {
                    "url": url,
                    "status": "OK",
                    "reason": "article content extracted",
                    "content_length": len(result["text"]),
                    "title": result.get("title"),
                    "date": result.get("date"),
                    "excerpt": result["text"][:200].replace("\n", " "),
                }
            else:
                return {
                    "url": url,
                    "status": "FAILED",
                    "reason": "extraction returned no usable content",
                    "content_length": 0,
                }
        except Exception as e:
            return {
                "url": url,
                "status": "FAILED",
                "reason": str(e)[:200],
                "content_length": 0,
            }


async def test_domain(extractor: PlaywrightExtractor, domain: str, urls: list[str], semaphore: asyncio.Semaphore) -> dict:
    results = []
    for url in urls:
        r = await test_url(extractor, url, semaphore)
        results.append(r)
        await asyncio.sleep(0.5)  # be polite between requests to same domain

    ok_count = sum(1 for r in results if r["status"] == "OK")
    return {
        "domain": domain,
        "urls_tested": len(urls),
        "ok_count": ok_count,
        "score": f"{ok_count}/{len(urls)}",
        "results": results,
    }


def generate_report(all_results: list[dict], low_score_domains: dict[str, str]) -> str:
    total_domains = len(all_results)
    total_urls = sum(r["urls_tested"] for r in all_results)
    total_ok = sum(r["ok_count"] for r in all_results)
    total_failed = total_urls - total_ok
    fully_accessible = sum(1 for r in all_results if r["ok_count"] == r["urls_tested"])
    partially = sum(1 for r in all_results if 0 < r["ok_count"] < r["urls_tested"])
    fully_inaccessible = sum(1 for r in all_results if r["ok_count"] == 0)

    improved = []
    same = []
    worse = []
    for r in all_results:
        wf_score = low_score_domains.get(r["domain"], "0/0")
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

    pct = lambda n, d: f"{n*100//d}%" if d > 0 else "N/A"

    lines = [
        "# Playwright + Trafilatura Article Extraction Test Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "**Method:** For each source domain that scored 2/3 or less in the Claude WebFetch test, "
        "launched a headless Chromium browser via Playwright to render the page (including JS execution, "
        "cookie consent dismissal, and lazy-load triggering), then extracted article content with "
        "`trafilatura.extract()`. A successful result means article content (>200 chars) was extracted "
        "from the rendered HTML.",
        "",
        "**Tier:** 4 of 4 in extraction chain (Claude web_fetch → Diffbot → curl+trafilatura → Playwright+trafilatura)",
        "",
        "---",
        "",
        f"**Total domains tested:** {total_domains}",
        f"**Total URL fetch attempts:** {total_urls}",
        f"**Successful article extractions (OK):** {total_ok} ({pct(total_ok, total_urls)})",
        f"**Failed extractions (FAILED):** {total_failed} ({pct(total_failed, total_urls)})",
        "",
        f"**Fully accessible domains (all URLs OK):** {fully_accessible} ({pct(fully_accessible, total_domains)})",
        f"**Partially accessible domains:** {partially} ({pct(partially, total_domains)})",
        f"**Fully inaccessible domains (0 OK):** {fully_inaccessible} ({pct(fully_inaccessible, total_domains)})",
        "",
        "## Comparison with Claude WebFetch",
        "",
        f"**Improved over WebFetch:** {len(improved)} domains",
        f"**Same as WebFetch:** {len(same)} domains",
        f"**Worse than WebFetch:** {len(worse)} domains",
        "",
        "## Full Results",
        "",
        "| # | Domain | WebFetch Score | URL 1 | URL 2 | URL 3 | Playwright Score |",
        "|---|--------|---------------|-------|-------|-------|-----------------|",
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

    if improved:
        lines.extend(["", "## Improved Domains (Playwright > WebFetch)", ""])
        for r in sorted(improved, key=lambda x: x["domain"]):
            wf_score = low_score_domains.get(r["domain"], "?/?")
            lines.append(f"- `{r['domain']}`: {wf_score} → {r['score']}")

    still_inaccessible = [
        r for r in all_results
        if r["ok_count"] == 0 and low_score_domains.get(r["domain"], "").startswith("0/")
    ]
    if still_inaccessible:
        lines.extend(["", "## Still Inaccessible (0 OK across WebFetch and Playwright)", ""])
        for r in sorted(still_inaccessible, key=lambda x: x["domain"]):
            lines.append(f"- `{r['domain']}`")

    # Domains where Playwright recovered content
    newly_accessible = [r for r in improved if low_score_domains.get(r["domain"], "").startswith("0/")]
    if newly_accessible:
        lines.extend(["", "## Newly Accessible via Playwright (was 0/N in WebFetch)", ""])
        for r in sorted(newly_accessible, key=lambda x: x["domain"]):
            wf_score = low_score_domains.get(r["domain"], "?/?")
            lines.append(f"- `{r['domain']}`: {wf_score} → {r['score']}")

    lines.append("")
    return "\n".join(lines)


async def main():
    print("Parsing WebFetch report for low-score domains...")
    low_score_domains = parse_low_score_domains(str(WEBFETCH_REPORT))
    print(f"Found {len(low_score_domains)} domains scoring 2/3 or less")

    print("Collecting URLs from Brave search results...")
    domain_urls = collect_urls_from_brave(str(BRAVE_DIR), set(low_score_domains.keys()))
    print(f"Found URLs for {len(domain_urls)} domains")

    domains_without_urls = set(low_score_domains.keys()) - set(domain_urls.keys())
    if domains_without_urls:
        print(f"No Brave URLs found for {len(domains_without_urls)} domains: {sorted(domains_without_urls)[:10]}...")

    print(f"\nTesting {len(domain_urls)} domains with Playwright + trafilatura...")

    extractor = PlaywrightExtractor()
    await extractor.start()
    semaphore = asyncio.Semaphore(3)

    all_results = []
    total = len(domain_urls)

    for i, (domain, urls) in enumerate(sorted(domain_urls.items()), 1):
        print(f"  [{i}/{total}] {domain} ({len(urls)} URLs)...", end=" ", flush=True)
        result = await test_domain(extractor, domain, urls, semaphore)
        all_results.append(result)
        print(f"{result['score']}")

    await extractor.stop()

    # Save raw results (strip full text to keep file manageable)
    save_results = []
    for r in all_results:
        sr = dict(r)
        sr["results"] = []
        for url_r in r["results"]:
            url_sr = dict(url_r)
            url_sr.pop("text", None)  # don't save full text
            sr["results"].append(url_sr)
        save_results.append(sr)

    with open(RESULTS_FILE, "w") as f:
        json.dump(save_results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results saved to {RESULTS_FILE}")

    report = generate_report(all_results, low_score_domains)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"Report saved to {REPORT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
