# Article Extraction Architecture

## Overview

Brave Search discovers articles (headlines, URLs, metadata). A separate extraction layer retrieves full article text. Extraction uses a static routing table that assigns each domain to its optimal extraction method, based on empirical testing across 377 domains.

---

## Extraction Methods

### Tier 0: Claude web_fetch
- **What it is:** Claude's native HTTP fetch capability
- **Strengths:** Free (API call cost only), fast, no infrastructure
- **Weaknesses:** Blocked by many news sites' anti-bot protections, fails on JavaScript-rendered pages
- **Coverage:** 195/377 domains (51%) at 3/3 success rate
- **Use as primary for:** Domains where Claude fetch tested at 3/3

### Tier 1: curl + trafilatura
- **What it is:** Simple HTTP request (Python `httpx` or `requests`) followed by content extraction via trafilatura library
- **Strengths:** Highest overall success rate (81% URL-level), penetrates many paywalls and bot detections that block Claude and Playwright, lightweight infrastructure
- **Weaknesses:** Cannot handle JavaScript-rendered pages, some sites detect and block automated requests
- **Coverage:** 146/182 fallback domains resolved (80%)
- **Use as primary for:** The dominant fallback method. Most European, Latin American, Indian, Japanese, and Scandinavian outlets

### Tier 2: Diffbot Article API
- **What it is:** Diffbot's `/v3/article` endpoint with `/v3/analyze` fallback
- **Strengths:** Proprietary rendering handles complex layouts, metered paywalls, CMS-embedded content. Uniquely effective for some government and institutional sites
- **Weaknesses:** Per-call cost (~$0.001-0.01/call depending on plan), 29% domain-level success rate as primary method
- **Coverage:** 12 domains where Diffbot is the only method that works
- **Use as primary for:** Domains that resist both Claude and curl — typically institutional sites, some Arabic-language outlets, and a few major outlets (reuters.com at 1/3)
- **Budget consideration:** ~10,000 credits/month. Reserve for domains where it's genuinely needed, not as general fallback

### Tier 3: Playwright + trafilatura
- **What it is:** Headless Chromium browser rendering + trafilatura content extraction
- **Strengths:** Handles JavaScript-rendered content that curl cannot reach. Only method for some JS-heavy sites
- **Weaknesses:** Slowest method, heaviest infrastructure, many sites detect and block headless browsers (50 domains where curl works but Playwright fails)
- **Coverage:** 18 domains where Playwright is the only fallback that works
- **Use as primary for:** JS-rendered sites that block simple HTTP — several government sites, intelligence/defense outlets, some paywalled publications

### Tier 4: Publisher APIs
- **What it is:** Structured API access provided by publishers themselves. Returns clean, reliable article text with metadata
- **Strengths:** Most reliable extraction — no scraping, no bot detection issues, structured data, full text guaranteed
- **Weaknesses:** Limited availability (few publishers offer APIs), may require API keys, rate limits, terms of service constraints
- **Use as primary for:** Any domain where a Publisher API is available — it should always be preferred over scraping

**Currently identified Publisher APIs:**

| Publisher | API | Status | Notes |
|-----------|-----|--------|-------|
| The Guardian | Guardian Open Platform | Scaffolded — needs API key and integration | Free tier available. Covers UK, Australia, India, EU, US foreign policy. Search by tag/section/date. Full structured article text. |
| Financial Times | FT Content API | Scaffolded — needs commercial access evaluation | Likely requires paid access. Covers global economics, finance, geopolitics. High-value Tier 1 source for economic_tech signal category. |

**Potential future Publisher APIs (not yet evaluated):**

| Publisher | Likelihood | Notes |
|-----------|-----------|-------|
| AP News | Unknown | AP has syndication APIs but unclear if available for this use case |
| Deutsche Welle | Possible | DW has developer resources; coverage overlaps with existing German sources |
| NHK World | Possible | NHK has API documentation for some services |

Publisher APIs should be evaluated opportunistically. When a high-value source is difficult to extract via other methods, check whether it offers API access before building custom scraping infrastructure.

---

## Domain Routing Table

### Schema

```yaml
# extraction/routing.yaml

# Metadata
generated: 2026-03-20
domains_total: 377
test_methodology: "3 URLs per domain, 4 methods tested"

routes:
  # Each domain maps to its primary extraction method and fallback chain
  apnews.com:
    primary: claude
    confidence: high       # 3/3 in testing
    fallbacks: [curl, diffbot]
    
  lemonde.fr:
    primary: curl
    confidence: high       # 3/3
    fallbacks: [diffbot, playwright]
    
  reuters.com:
    primary: diffbot
    confidence: low        # 1/3
    fallbacks: [playwright]
    notes: "Extremely difficult to extract. Consider Publisher API if available."
    
  intelligenceonline.com:
    primary: playwright
    confidence: high       # 3/3
    fallbacks: [diffbot]
    
  theguardian.com:
    primary: publisher_api  # Guardian Open Platform
    confidence: high
    fallbacks: [curl, diffbot]
    publisher_api: guardian
    
  ft.com:
    primary: curl           # 3/3 in testing
    confidence: high
    fallbacks: [publisher_api, diffbot]
    publisher_api: ft       # when available
    notes: "curl works but Publisher API preferred for reliability"

  # Unretrievable — headline + snippet only
  dgap.org:
    primary: snippet_only
    confidence: null
    fallbacks: []
    notes: "0/3 across all methods"
    
  liberation.fr:
    primary: snippet_only
    confidence: null
    fallbacks: []
    notes: "0/3 across all methods. Hard paywall."
```

### Confidence Levels

- **high**: 3/3 URLs successful in testing. Expect reliable extraction.
- **medium**: 2/3 URLs successful. Generally works but occasional failures expected.
- **low**: 1/3 URLs successful. Unreliable — extraction may fail more often than it succeeds. Fallback should be tried proactively.

### Routing for Unknown Domains

Brave may return articles from domains not in the routing table (organic-ranked sources that aren't in any Goggle). For unknown domains, use the default fallback chain:

```
claude → curl → diffbot → playwright → snippet_only
```

This mirrors the overall success rate hierarchy. If an unknown domain appears frequently, add it to the routing table after testing.

---

## Execution Architecture

### Parallel Pool Dispatch

When the pipeline has a batch of URLs to extract (after Brave discovery), dispatch them to extraction pools in parallel based on the routing table:

```
URL batch from Brave discovery
        │
        ├─→ Pool A: Claude web_fetch (195 domains, ~51% of URLs)
        │
        ├─→ Pool B: curl + trafilatura (146 domains, ~39% of URLs)
        │
        ├─→ Pool C: Diffbot (12 domains, ~3% of URLs)
        │
        ├─→ Pool D: Playwright (18 domains, ~5% of URLs)
        │
        ├─→ Pool E: Publisher APIs (Guardian, FT when available)
        │
        └─→ Snippet-only (6 domains, ~2% of URLs)
        
All pools run simultaneously.
```

### Fallback Batch

After all primary pools complete, collect failures and dispatch to fallback methods:

```
Primary failures
        │
        ├─→ Claude failures → try curl
        │
        ├─→ curl failures → try diffbot, then playwright
        │
        ├─→ Diffbot failures → try curl, then playwright
        │
        └─→ Playwright failures → try curl, then diffbot

Fallback batch runs as a single pass.
Any remaining failures → snippet_only with confidence cap at 2.
```

### Concurrency Limits

| Pool | Concurrency | Rationale |
|------|------------|-----------|
| Claude web_fetch | 10 concurrent | API rate limits |
| curl + trafilatura | 20 concurrent | Lightweight; main bottleneck is target site rate limiting |
| Diffbot | 5 concurrent | API rate limits + credit conservation |
| Playwright | 3 concurrent | Heavy resource usage per browser instance |
| Publisher APIs | 5 concurrent | Per-API rate limits |

### Rate Limiting Per Domain

Regardless of extraction method, respect per-domain rate limits:
- Maximum 1 request per second per domain
- Maximum 5 URLs per domain per extraction cycle
- If more than 5 URLs from a single domain need extraction, prioritize by Brave ranking (Goggle Tier 1 articles first)

---

## Publisher API Scaffolding

### Guardian Open Platform

```python
# Placeholder — needs API key and integration

class GuardianAPI:
    """
    Guardian Open Platform client.
    Docs: https://open-platform.theguardian.com/documentation/
    
    Provides: Full article text, tags, section, byline, publication date
    Rate limit: 12 calls/second (developer key), 500 calls/day (free tier)
    Languages: English
    Coverage: UK, Australia, India, EU affairs, US foreign policy
    
    Countries where Guardian is relevant:
    - gb (Tier 1-2 source)
    - au (Tier 2 source)
    - in (Tier 2-3 source)
    - EU countries (Tier 3 for EU affairs coverage)
    """
    
    BASE_URL = "https://content.guardianapis.com"
    
    async def search(self, query: str, from_date: str, to_date: str,
                     section: str = None, page_size: int = 20) -> list:
        """Search for articles matching query within date range."""
        # TODO: Implement
        raise NotImplementedError
    
    async def get_article(self, url: str) -> dict:
        """Fetch full article content by URL or API ID."""
        # TODO: Implement
        raise NotImplementedError
    
    def url_to_api_id(self, url: str) -> str:
        """Convert a theguardian.com URL to an API content path."""
        # Guardian URLs map to API paths:
        # https://www.theguardian.com/world/2026/mar/20/article-slug
        # → world/2026/mar/20/article-slug
        # TODO: Implement
        raise NotImplementedError
```

### Financial Times Content API

```python
# Placeholder — needs commercial access evaluation

class FTAPI:
    """
    FT Content API client.
    
    Access: Likely requires commercial agreement.
    Provides: Full article text, metadata, topic tags
    Coverage: Global economics, finance, geopolitics
    
    Countries where FT is relevant:
    - gb (Tier 1 source for economic_tech)
    - All countries (Tier 2-3 for global economic coverage)
    
    NOTE: FT articles are already extractable via curl at 3/3.
    Publisher API would provide more reliable, structured access
    but is not urgently needed given curl success rate.
    """
    
    async def get_article(self, url: str) -> dict:
        """Fetch full article content."""
        # TODO: Evaluate access requirements
        raise NotImplementedError
```

### Generic Publisher API Interface

```python
from abc import ABC, abstractmethod

class PublisherAPI(ABC):
    """
    Base class for Publisher API integrations.
    
    New Publisher APIs should implement this interface.
    The extraction orchestrator dispatches to Publisher APIs
    based on domain-to-API mappings in the routing table.
    """
    
    @abstractmethod
    async def get_article(self, url: str) -> dict:
        """
        Fetch article by URL.
        
        Returns:
            {
                "title": str,
                "text": str,          # Full article text
                "author": str | None,
                "date": str,          # ISO format
                "section": str | None,
                "tags": list[str],
                "url": str,
                "source": str,        # API name for provenance
                "extraction_method": "publisher_api",
            }
        """
        pass
    
    @abstractmethod
    async def search(self, query: str, from_date: str, to_date: str,
                     **kwargs) -> list[dict]:
        """
        Search for articles. Optional — not all Publisher APIs
        support search. Those that do can supplement Brave discovery.
        """
        pass
```

---

## Routing Table Maintenance

### When to Update

- **Monthly:** Re-run the extraction test suite against a sample of URLs from each pool. Domains may change their anti-bot protections, paywall behavior, or site architecture.
- **On extraction failure spike:** If a domain's extraction success rate drops below its recorded confidence level over a week of pipeline runs, re-test and update routing.
- **On new source addition:** When a new domain appears in a country's Goggle (source curation update), test all extraction methods and add to routing table.
- **On Publisher API availability:** When a new Publisher API becomes available for a domain already in the routing table, add it as primary and demote the previous method to fallback.

### Logging

Every extraction attempt should log:
- Domain, URL, method attempted, success/failure, response time
- If failure: error type (timeout, 403, bot detection, paywall, empty content)
- If fallback used: which method succeeded after primary failed

Weekly aggregation of extraction logs produces a health report per domain, per method. This feeds routing table updates and source curation maintenance.

---

## Integration with Architecture

This extraction layer sits between Brave discovery (Step 2 in the pipeline flow) and the country agent (Step 3). The orchestrator:

1. Receives URLs from Brave discovery
2. Looks up each URL's domain in the routing table
3. Dispatches to parallel extraction pools
4. Runs fallback batch for failures
5. Packages results (full text where extracted, snippet where not, with extraction metadata)
6. Passes packaged results to the country agent as Layer 1 input

The country agent sees the final extracted content. It does not know or care which extraction method produced it. The only extraction-related information surfaced to the agent is a flag on articles where extraction failed and only snippet was available — these carry a confidence cap of 2.
