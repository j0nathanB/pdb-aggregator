# How to Run a Multi-Method Article Retrieval Experiment

**Context:** We test 4 extraction methods against a list of source domains/URLs to determine which method works best for each domain. Results feed into the pipeline's extraction hierarchy.

**Prior art:** See `0_brave_search_results/` through `7_claude_v_curl/` for examples of completed experiments.

---

## Prerequisites

### Tools & dependencies

```bash
# Python packages (trafilatura for curl test, playwright for browser test, browserbase for cloud browser)
pip install trafilatura playwright browserbase
playwright install chromium

# Diffbot API token — stored in /Users/zen/dev/src/pdb/.env as DIFFBOT_TOKEN
# Rate limit: 5 calls/minute (1 call per 12 seconds)

# Browserbase — requires BROWSERBASE_API_KEY and BROWSERBASE_PROJECT_ID in .env
# Cloud browser that bypasses Cloudflare JS challenges and bot protection
```

### Input format

Prepare a JSON file with your test URLs. Each domain should have **3 URLs** for statistical consistency:

```json
{
  "example.gov": {
    "urls": [
      "https://example.gov/press-release-1",
      "https://example.gov/statement-2",
      "https://example.gov/news-3"
    ]
  },
  "another.gov.br": {
    "urls": [
      "https://another.gov.br/article-1",
      "https://another.gov.br/article-2",
      "https://another.gov.br/article-3"
    ]
  }
}
```

Save this as `input_urls.json` in your experiment directory.

---

## Method 1: curl + trafilatura (run first — fastest, free, and typically best)

This is a simple Python HTTP fetch + content extraction. No browser, no API key needed.

```python
"""curl_test.py — Run trafilatura extraction on all domains."""
import json
import trafilatura

input_data = json.load(open("input_urls.json"))
results = {}

for domain in sorted(input_data.keys()):
    urls = input_data[domain]["urls"]
    domain_results = []
    for url in urls:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                if text and len(text.strip()) > 100:
                    domain_results.append({"url": url, "status": "OK", "snippet": text[:200]})
                else:
                    domain_results.append({"url": url, "status": "FAILED", "reason": "extraction returned insufficient text"})
            else:
                domain_results.append({"url": url, "status": "FAILED", "reason": "fetch returned None"})
        except Exception as e:
            domain_results.append({"url": url, "status": "FAILED", "reason": str(e)[:100]})

    ok = sum(1 for r in domain_results if r["status"] == "OK")
    results[domain] = {
        "ok": ok, "total": len(domain_results),
        "score": f"{ok}/{len(domain_results)}", "results": domain_results
    }
    print(f"{domain}: {ok}/{len(domain_results)}")

with open("curl_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

Run: `python3 curl_test.py`
Expected time: ~1-2 minutes for 50 domains.

---

## Method 2: Diffbot API (rate-limited — run last or in background)

**Rate limit: 5 calls per minute.** A failed `/v3/article` call followed by a `/v3/analyze` fallback = 2 calls, so worst case is ~2.5 domains/minute.

```python
"""diffbot_test.py — Run Diffbot extraction with rate limiting."""
import json, urllib.request, urllib.parse, urllib.error, time, os

TOKEN = os.environ.get("DIFFBOT_TOKEN") or "YOUR_TOKEN_HERE"
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
            time.sleep(wait)
        call_times = [t for t in call_times if time.time() - t < 60]
    call_times.append(time.time())
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode())

input_data = json.load(open("input_urls.json"))
results = {}

for domain in sorted(input_data.keys()):
    urls = input_data[domain]["urls"]
    domain_results = []
    for url in urls:
        encoded = urllib.parse.quote(url, safe='')
        status, api_used, snippet = "FAILED", None, None

        # Try /v3/article first
        try:
            data = rate_limited_fetch(f"{ARTICLE_URL}&url={encoded}")
            objects = data.get("objects", [])
            if objects and objects[0].get("text", "").strip():
                status, api_used = "OK", "article"
                snippet = objects[0]["text"][:200]
        except Exception:
            pass

        # Fallback to /v3/analyze
        if status != "OK":
            try:
                data = rate_limited_fetch(f"{ANALYZE_URL}&url={encoded}")
                objects = data.get("objects", [])
                if objects and objects[0].get("text", "").strip():
                    status, api_used = "OK", "analyze"
                    snippet = objects[0]["text"][:200]
            except Exception:
                pass

        domain_results.append({"url": url, "status": status, "api_used": api_used, "snippet": snippet})

    ok = sum(1 for r in domain_results if r["status"] == "OK")
    results[domain] = {
        "ok": ok, "total": len(domain_results),
        "score": f"{ok}/{len(domain_results)}", "results": domain_results
    }
    print(f"{domain}: {ok}/{len(domain_results)}")

with open("diffbot_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

Run: `python3 diffbot_test.py`
Expected time: ~12 seconds per URL minimum. 50 domains × 3 URLs = ~30 min best case, ~60 min worst case.

**Important:** The script saves progress inline — if interrupted, you can modify it to skip completed domains by checking the output file.

---

## Method 3: Playwright + trafilatura (local headless browser)

Uses a local Chromium browser to render JS, dismiss cookie banners, and extract content. Handles JS-rendered sites that curl can't.

```python
"""playwright_test.py — Headless browser extraction."""
import json
from playwright.sync_api import sync_playwright
import trafilatura

input_data = json.load(open("input_urls.json"))
results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    for domain in sorted(input_data.keys()):
        urls = input_data[domain]["urls"]
        domain_results = []
        for url in urls:
            try:
                page = context.new_page()
                page.goto(url, timeout=30000, wait_until="networkidle")
                # Try to dismiss cookie banners
                for selector in ["button:has-text('Accept')", "button:has-text('Agree')", "button:has-text('OK')", "[id*='cookie'] button", "[class*='consent'] button"]:
                    try:
                        page.click(selector, timeout=2000)
                    except Exception:
                        pass
                page.wait_for_timeout(2000)
                html = page.content()
                page.close()

                text = trafilatura.extract(html)
                if text and len(text.strip()) > 200:
                    domain_results.append({"url": url, "status": "OK", "snippet": text[:200]})
                else:
                    domain_results.append({"url": url, "status": "FAILED", "reason": "insufficient text after extraction"})
            except Exception as e:
                domain_results.append({"url": url, "status": "FAILED", "reason": str(e)[:100]})
                try: page.close()
                except: pass

        ok = sum(1 for r in domain_results if r["status"] == "OK")
        results[domain] = {
            "ok": ok, "total": len(domain_results),
            "score": f"{ok}/{len(domain_results)}", "results": domain_results
        }
        print(f"{domain}: {ok}/{len(domain_results)}")

    browser.close()

with open("playwright_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

Run: `python3 playwright_test.py`
Expected time: ~5-10 seconds per URL. 50 domains × 3 URLs = ~12-25 minutes.

---

## Method 4: Browserbase (cloud browser — bypasses bot protection)

Uses Browserbase's managed cloud browser infrastructure via CDP. Handles Cloudflare JS challenges, aggressive bot detection, and geo-restricted content that local Playwright can't bypass. Requires `BROWSERBASE_API_KEY` and `BROWSERBASE_PROJECT_ID` in `.env`.

```python
"""browserbase_test.py — Cloud browser extraction via Browserbase."""
import json, os, time
from browserbase import Browserbase
from playwright.sync_api import sync_playwright
import trafilatura

API_KEY = os.environ["BROWSERBASE_API_KEY"]
PROJECT_ID = os.environ["BROWSERBASE_PROJECT_ID"]

input_data = json.load(open("input_urls.json"))
results = {}

bb = Browserbase(api_key=API_KEY)

for domain in sorted(input_data.keys()):
    urls = input_data[domain]["urls"]
    domain_results = []
    for url in urls:
        try:
            session = bb.sessions.create(project_id=PROJECT_ID)
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(session.connect_url)
                context = browser.contexts[0]
                page = context.pages[0]
                page.goto(url, timeout=30000, wait_until="domcontentloaded")
                # Wait for Cloudflare JS challenge to resolve
                page.wait_for_timeout(8000)
                html = page.content()
                browser.close()

            text = trafilatura.extract(html)
            if text and len(text.strip()) > 200:
                domain_results.append({"url": url, "status": "OK", "snippet": text[:200]})
            else:
                domain_results.append({"url": url, "status": "FAILED", "reason": "insufficient text after extraction"})
        except Exception as e:
            domain_results.append({"url": url, "status": "FAILED", "reason": str(e)[:100]})

    ok = sum(1 for r in domain_results if r["status"] == "OK")
    results[domain] = {
        "ok": ok, "total": len(domain_results),
        "score": f"{ok}/{len(domain_results)}", "results": domain_results
    }
    print(f"{domain}: {ok}/{len(domain_results)}")

with open("browserbase_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

Run: `python3 browserbase_test.py`
Expected time: ~10-15 seconds per URL (includes challenge wait). 50 domains × 3 URLs = ~25-40 minutes.

**When to use over local Playwright:** Sites protected by Cloudflare JS challenges, aggressive bot detection, or IP-based blocking. Browserbase sessions run from cloud IPs with residential fingerprints, bypassing protections that block local Playwright.

---

## Compiling the Cross-Method Report

After all 4 methods have run, compile results:

```python
"""compile_report.py — Compare all methods."""
import json

curl = json.load(open("curl_results.json"))
diffbot = json.load(open("diffbot_results.json"))
pw = json.load(open("playwright_results.json"))
bb = json.load(open("browserbase_results.json"))

all_domains = sorted(set(curl) | set(diffbot) | set(pw) | set(bb))

lines = []
lines.append("| # | Domain | curl+traf | Diffbot | Playwright | Browserbase | Best |")
lines.append("|---|--------|-----------|---------|------------|-------------|------|")

for i, d in enumerate(all_domains, 1):
    scores = {}
    for name, data in [("curl", curl), ("Diffbot", diffbot), ("PW", pw), ("BB", bb)]:
        if d in data:
            scores[name] = data[d]["ok"] / max(data[d]["total"], 1)

    best = max(scores, key=scores.get) if scores else "NONE"

    def fmt(data, d):
        return data[d]["score"] if d in data else "--"

    lines.append(f"| {i} | `{d}` | {fmt(curl,d)} | {fmt(diffbot,d)} | {fmt(pw,d)} | {fmt(bb,d)} | {best} |")

print("\n".join(lines))
```

---

## Expected Outcomes (based on prior experiments)

From our tests on 377 news/policy domains:

| Method | URL success rate | Best for |
|--------|-----------------|----------|
| **curl + trafilatura** | **81%** | Most sites. Fast, free, no rate limits. First choice. |
| **Diffbot API** | 65% | Sites that block Python user-agents but serve Diffbot's crawler (reuters.com, nationalpost.com, defence.gov.au). Rate-limited. |
| **Playwright** | 48% | JS-rendered sites where content isn't in initial HTML (intelligenceonline.com, president.gov.ua, lalettre.fr, irozhlas.cz). |
| **Browserbase** | Use for Cloudflare-protected sites | Sites behind Cloudflare JS challenges and aggressive bot detection that block both curl and local Playwright. Cloud IPs with residential fingerprints. |

**Government sites specifically** were the hardest category in prior tests. defence.gov.au, mod.go.jp, mnd.gov.tw all failed across multiple methods. Expect lower success rates than news/policy sources.

## Recommended execution order

1. **curl + trafilatura first** — fast, free, best overall performer
2. **For domains where curl scored <3/3**, run Diffbot in parallel
3. **For domains still <3/3**, run Playwright (local) for JS-rendered sites
4. **For domains still failing** (especially Cloudflare-protected), run Browserbase
5. Compile cross-method report to determine the optimal method per domain
