# How to Run a Multi-Method Article Retrieval Experiment

**Context:** We test 4 extraction methods against a list of source domains/URLs to determine which method works best for each domain. Results feed into the pipeline's extraction hierarchy.

**Prior art:** See `0_brave_search_results/` through `7_claude_v_curl/` for examples of completed experiments.

---

## Prerequisites

### Tools & dependencies

```bash
# Python packages (trafilatura for curl test, playwright for browser test)
pip install trafilatura playwright
playwright install chromium

# Diffbot API token — stored in /Users/zen/dev/src/pdb/.env as DIFFBOT_TOKEN
# Rate limit: 5 calls/minute (1 call per 12 seconds)

# Claude WebFetch — available natively via Claude Code's WebFetch tool
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

## Method 2: Claude WebFetch (native)

Use Claude Code's built-in WebFetch tool. For each URL, call:

```
WebFetch(url=<url>, prompt="Extract the article title and first 2 sentences of the article body text. If this is a paywall, cookie wall, or error page, say BLOCKED.")
```

**Scoring:**
- **OK** — article content was returned
- **BLOCKED** — paywall, cookie wall, or captcha detected
- **FAILED** — error, timeout, redirect loop, or "unable to fetch"

Save results in the same JSON format as curl. Note: this must be run interactively through Claude Code or via subagents. For large batches (>30 domains), split into parallel agents of ~30-40 domains each to avoid timeouts. Each agent should read `input_urls.json` and process its assigned chunk.

---

## Method 3: Diffbot API (rate-limited — run last or in background)

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

## Method 4: Playwright + trafilatura (headless browser)

Uses a real Chromium browser to render JS, dismiss cookie banners, and extract content. Slowest but handles JS-rendered sites that curl can't.

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

## Compiling the Cross-Method Report

After all 4 methods have run, compile results:

```python
"""compile_report.py — Compare all methods."""
import json

curl = json.load(open("curl_results.json"))
claude = json.load(open("claude_results.json"))
diffbot = json.load(open("diffbot_results.json"))
pw = json.load(open("playwright_results.json"))

all_domains = sorted(set(curl) | set(claude) | set(diffbot) | set(pw))

lines = []
lines.append("| # | Domain | Claude | curl+traf | Diffbot | Playwright | Best |")
lines.append("|---|--------|--------|-----------|---------|------------|------|")

for i, d in enumerate(all_domains, 1):
    scores = {}
    for name, data in [("Claude", claude), ("curl", curl), ("Diffbot", diffbot), ("PW", pw)]:
        if d in data:
            scores[name] = data[d]["ok"] / max(data[d]["total"], 1)

    best = max(scores, key=scores.get) if scores else "NONE"

    def fmt(data, d):
        return data[d]["score"] if d in data else "--"

    lines.append(f"| {i} | `{d}` | {fmt(claude,d)} | {fmt(curl,d)} | {fmt(diffbot,d)} | {fmt(pw,d)} | {best} |")

print("\n".join(lines))
```

---

## Expected Outcomes (based on prior experiments)

From our tests on 377 news/policy domains:

| Method | URL success rate | Best for |
|--------|-----------------|----------|
| **curl + trafilatura** | **81%** | Most sites. Fast, free, no rate limits. First choice. |
| **Diffbot API** | 65% | Sites that block Python user-agents but serve Diffbot's crawler (reuters.com, nationalpost.com, defence.gov.au). Rate-limited. |
| **Claude WebFetch** | 51% on hard domains, 100% on easy | Sites that block trafilatura but allow Claude's infra (e.g., cbc.ca). |
| **Playwright** | 48% | JS-rendered sites where content isn't in initial HTML (intelligenceonline.com, president.gov.ua, lalettre.fr, irozhlas.cz). |

**Government sites specifically** were the hardest category in prior tests. defence.gov.au, mod.go.jp, mnd.gov.tw all failed across multiple methods. Expect lower success rates than news/policy sources.

## Recommended execution order

1. **curl + trafilatura first** — fast, free, best overall performer
2. **For domains where curl scored <3/3**, run Claude WebFetch and Diffbot in parallel
3. **For domains still <3/3**, run Playwright as last resort
4. Compile cross-method report to determine the optimal method per domain
