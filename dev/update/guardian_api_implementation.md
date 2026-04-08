# Guardian Open Platform — Implementation Spec

## Overview

The Guardian Content API provides full article text via API, eliminating the need for scraping or extraction for Guardian content. This makes it the most reliable source in the pipeline — structured data, guaranteed full text, rich metadata, and no bot detection issues.

**Base URL:** `https://content.guardianapis.com`
**Rate limit:** Developer key allows 12 calls/second, 500 calls/day (free tier). Elevated limits available on request.
**Authentication:** API key passed as `api-key` parameter.

---

## Relevant Coverage for MPM

The Guardian has strong original reporting for a subset of the 28 countries:

| Country | Coverage Quality | Tags / Sections | Notes |
|---------|-----------------|-----------------|-------|
| gb | **Tier 1** | `politics/politics`, `uk/uk` | Home market. Deepest coverage. |
| au | **Tier 1** | `australia-news/australia-news`, `world/australia` | Full Australian bureau. Use `production-office=aus` for bureau-specific content. |
| in | **Tier 2** | `world/india` | Dedicated India coverage, strong on politics and economics. |
| fr | **Tier 2** | `world/france` | Good coverage of French politics and EU dynamics. |
| de | **Tier 2** | `world/germany` | Coverage of German politics, EU economics. |
| ua | **Tier 2** | `world/ukraine` | Strong war coverage, diplomatic developments. |
| jp | **Tier 3** | `world/japan` | Intermittent, event-driven coverage. |
| br | **Tier 3** | `world/brazil` | Intermittent, focused on environmental and political crises. |
| tr | **Tier 3** | `world/turkey` | Event-driven, focused on democratic backsliding and regional security. |
| sa | **Tier 3** | `world/saudiarabia` | Event-driven, focused on human rights and energy. |
| kr | **Tier 3** | `world/south-korea` | Intermittent. |
| tw | **Tier 3** | `world/taiwan` | Intermittent, focused on cross-strait tensions. |
| id | **Tier 3** | `world/indonesia` | Sparse. |

Countries not listed have minimal or no dedicated Guardian coverage. The API is not worth querying for Estonia, Latvia, Lithuania, Czech Republic, Romania, Chile, Norway, Sweden, or Finland — Brave + Goggles handles those.

**Practical implication:** The Guardian API adds value for ~13 countries, primarily as a Tier 2-3 English-language analytical source that complements domestic-language Tier 1 sources. It's most valuable for UK, Australia, and India where Guardian has bureau-level coverage.

---

## Query Strategy for MPM

### Per-Country Weekly Query

One API call per relevant country per week:

```
GET /search
  ?q={actor_query}
  &tag={country_tag}
  &from-date={week_start}
  &to-date={week_end}
  &show-fields=body,headline,byline,wordcount,standfirst,shortUrl
  &show-tags=keyword,contributor
  &page-size=50
  &order-by=newest
  &api-key={key}
```

**`q` parameter:** Constructed from the country's actor/institution search terms, joined with OR. The Guardian indexes English content, so use English name variants:

```python
# Mexico example
q = 'Sheinbaum OR "de la Fuente" OR SEDENA OR "Mexican foreign ministry"'

# France example  
q = 'Macron OR Barrot OR "Quai d\'Orsay" OR "French defence" OR "Banque de France"'

# India example
q = 'Modi OR Jaishankar OR "Indian foreign ministry" OR "Reserve Bank of India" OR BJP'
```

**`tag` parameter:** Country-specific tag for precision:
- `world/mexico`, `world/france`, `world/india`, etc.
- For UK: `politics/politics` (broader political coverage) or combine with section
- For Australia: `australia-news/australia-news` or use `production-office=aus`

**`from-date` / `to-date`:** The pipeline's weekly analysis window.

**`show-fields=body`:** This is the critical parameter. Returns the full article text as HTML. Without it, you only get titles and metadata.

**`page-size=50`:** Maximum allowed. For most countries in a given week, 50 is more than sufficient. If `total` exceeds 50, paginate — but this will be rare for individual country queries.

### Triage-Level Query (Optional)

For the triage wire scan, the Guardian can supplement AP/France24 for countries where it has strong coverage. A lighter query without `show-fields=body`:

```
GET /search
  ?tag={country_tag}
  &from-date={week_start}
  &to-date={week_end}
  &page-size=10
  &order-by=newest
  &api-key={key}
```

Returns headlines only — fast, cheap, no full text. Useful for UK, Australia, India triage enrichment.

---

## Response Parsing

### Content Search Response

```json
{
  "response": {
    "status": "ok",
    "total": 7,
    "startIndex": 1,
    "pageSize": 50,
    "currentPage": 1,
    "pages": 1,
    "orderBy": "newest",
    "results": [
      {
        "id": "world/2026/mar/18/india-jaishankar-defence-cooperation-australia",
        "type": "article",
        "sectionId": "world",
        "sectionName": "World news",
        "webPublicationDate": "2026-03-18T14:06:14Z",
        "webTitle": "India and Australia deepen defence ties...",
        "webUrl": "https://www.theguardian.com/world/2026/mar/18/...",
        "apiUrl": "https://content.guardianapis.com/world/2026/mar/18/...",
        "fields": {
          "headline": "India and Australia deepen defence ties...",
          "standfirst": "Jaishankar and Penny Wong...",
          "body": "<p>Full article HTML text...</p>",
          "byline": "Helen Davidson in Sydney",
          "wordcount": "1247",
          "shortUrl": "https://www.theguardian.com/p/..."
        },
        "tags": [
          {
            "id": "world/india",
            "type": "keyword",
            "webTitle": "India"
          },
          {
            "id": "world/australia",
            "type": "keyword",
            "webTitle": "Australia"
          },
          {
            "id": "world/asia-pacific",
            "type": "keyword",
            "webTitle": "Asia Pacific"
          }
        ]
      }
    ]
  }
}
```

### Mapping to Pipeline Extraction Format

Each Guardian API result maps to the extraction output format:

```python
{
    "url": result["webUrl"],
    "domain": "theguardian.com",
    "title": result["fields"]["headline"],
    "text": strip_html(result["fields"]["body"]),  # Strip HTML tags from body
    "snippet": result["fields"].get("standfirst", ""),
    "extraction_method": "publisher_api_guardian",
    "extraction_failed": False,
    "source_layer": "layer1",
    "metadata": {
        "guardian_id": result["id"],
        "byline": result["fields"].get("byline"),
        "wordcount": int(result["fields"].get("wordcount", 0)),
        "publication_date": result["webPublicationDate"],
        "section": result["sectionId"],
        "tags": [t["id"] for t in result.get("tags", [])],
        "short_url": result["fields"].get("shortUrl"),
    }
}
```

**HTML stripping:** The `body` field returns HTML. Use a simple HTML-to-text conversion (Python `html2text` or BeautifulSoup `.get_text()`) to produce clean text for the country agent. Preserve paragraph breaks.

---

## Integration with Extraction Architecture

### Routing Table Entry

```yaml
# In extraction/routing.yaml
theguardian.com:
  primary: publisher_api
  confidence: high
  publisher_api: guardian
  fallbacks: [curl]  # curl works at 3/3 as backup
  notes: "Full text via API. No extraction needed. Fallback to curl only if API is down."
```

### When Guardian API Results Arrive

Guardian API calls run as part of Layer 1 collection, in parallel with Brave discovery. The orchestrator:

1. Runs Brave queries for the country (discovers articles from all Goggle-ranked sources)
2. Runs Guardian API query for the country (discovers articles from Guardian specifically)
3. Deduplicates by URL — if Brave also discovered a Guardian article, the API result takes precedence (it has guaranteed full text)
4. Merges results into the country's Layer 1 input for the country agent

Guardian results bypass the extraction chain entirely — they arrive with full text already extracted. They go straight into the country agent's Layer 1 input.

### Query Budget

With the free tier (500 calls/day):
- 13 relevant countries × 1 deep-dive query each = 13 calls
- Plus optional triage queries for UK/AU/IN = 3 calls
- Total: ~16 calls per weekly cycle
- Well within the 500/day limit even with retries and pagination

---

## Implementation

```python
"""
Guardian Open Platform client for MPM pipeline.

Provides: Full article text, tags, section, byline, publication date.
Rate limit: 12 calls/second, 500 calls/day (free developer key).
Languages: English only.
"""

import asyncio
import html
from dataclasses import dataclass
from typing import Optional

import httpx


# Countries where Guardian API adds value
GUARDIAN_COUNTRIES = {
    "gb": {"tag": "politics/politics", "production_office": None},
    "au": {"tag": "australia-news/australia-news", "production_office": "aus"},
    "in": {"tag": "world/india", "production_office": None},
    "fr": {"tag": "world/france", "production_office": None},
    "de": {"tag": "world/germany", "production_office": None},
    "ua": {"tag": "world/ukraine", "production_office": None},
    "jp": {"tag": "world/japan", "production_office": None},
    "br": {"tag": "world/brazil", "production_office": None},
    "tr": {"tag": "world/turkey", "production_office": None},
    "sa": {"tag": "world/saudiarabia", "production_office": None},
    "kr": {"tag": "world/south-korea", "production_office": None},
    "tw": {"tag": "world/taiwan", "production_office": None},
    "id": {"tag": "world/indonesia", "production_office": None},
}


@dataclass
class GuardianArticle:
    """Parsed Guardian API article, ready for pipeline consumption."""
    url: str
    guardian_id: str
    title: str
    text: str                    # Full article text (HTML stripped)
    snippet: str                 # Standfirst / summary
    byline: Optional[str]
    wordcount: int
    publication_date: str        # ISO datetime
    section: str
    tags: list[str]              # Tag IDs
    short_url: Optional[str]

    def to_extraction_format(self) -> dict:
        """Convert to the pipeline's standard extraction output format."""
        return {
            "url": self.url,
            "domain": "theguardian.com",
            "title": self.title,
            "text": self.text,
            "snippet": self.snippet,
            "extraction_method": "publisher_api_guardian",
            "extraction_failed": False,
            "source_layer": "layer1",
            "metadata": {
                "guardian_id": self.guardian_id,
                "byline": self.byline,
                "wordcount": self.wordcount,
                "publication_date": self.publication_date,
                "section": self.section,
                "tags": self.tags,
                "short_url": self.short_url,
            },
        }


def strip_html(html_content: str) -> str:
    """
    Convert HTML body to plain text, preserving paragraph breaks.
    
    The Guardian's body field returns HTML like:
    <p>First paragraph.</p><p>Second paragraph.</p>
    
    Convert to:
    First paragraph.
    
    Second paragraph.
    """
    # Replace paragraph/block tags with double newlines
    import re
    text = re.sub(r'</(p|div|h[1-6]|blockquote|li)>', '\n\n', html_content)
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html.unescape(text)
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


class GuardianAPI:
    """
    Guardian Open Platform client for the MPM pipeline.
    
    Usage:
        api = GuardianAPI(api_key="your-key")
        articles = await api.search_country(
            country_code="in",
            actor_query='Modi OR Jaishankar OR "Reserve Bank of India"',
            from_date="2026-03-14",
            to_date="2026-03-21",
        )
    """

    BASE_URL = "https://content.guardianapis.com"
    
    # Fields to request for full article retrieval
    FULL_FIELDS = "body,headline,byline,wordcount,standfirst,shortUrl"
    
    # Fields for headline-only triage queries
    TRIAGE_FIELDS = "headline,standfirst,shortUrl"

    def __init__(self, api_key: str, rate_limit: float = 12.0):
        self.api_key = api_key
        self._semaphore = asyncio.Semaphore(int(rate_limit))
        self._client = httpx.AsyncClient(timeout=30.0)

    async def search_country(
        self,
        country_code: str,
        actor_query: str,
        from_date: str,
        to_date: str,
        full_text: bool = True,
        max_results: int = 50,
    ) -> list[GuardianArticle]:
        """
        Search for articles about a country's tracked actors within a date range.
        
        Args:
            country_code: ISO 2-letter country code (must be in GUARDIAN_COUNTRIES)
            actor_query: OR-joined actor/institution search terms in English
            from_date: Start of date range (YYYY-MM-DD)
            to_date: End of date range (YYYY-MM-DD)
            full_text: If True, retrieve full article body. If False, headlines only (for triage).
            max_results: Maximum articles to return (API max per page: 50)
            
        Returns:
            List of GuardianArticle objects
        """
        if country_code not in GUARDIAN_COUNTRIES:
            return []

        country_config = GUARDIAN_COUNTRIES[country_code]
        
        params = {
            "q": actor_query,
            "tag": country_config["tag"],
            "from-date": from_date,
            "to-date": to_date,
            "show-fields": self.FULL_FIELDS if full_text else self.TRIAGE_FIELDS,
            "show-tags": "keyword",
            "page-size": min(max_results, 50),
            "order-by": "newest",
            "api-key": self.api_key,
        }
        
        if country_config.get("production_office"):
            params["production-office"] = country_config["production_office"]

        results = await self._paginated_search(params, max_results)
        return [self._parse_result(r, full_text) for r in results]

    async def search_query(
        self,
        query: str,
        from_date: str,
        to_date: str,
        section: Optional[str] = None,
        tag: Optional[str] = None,
        full_text: bool = True,
        max_results: int = 50,
    ) -> list[GuardianArticle]:
        """
        Generic search — for queries that don't map to a single country.
        
        Useful for cross-country queries like:
        - "NATO AND (defence OR defense) AND spending"
        - "BRICS AND (summit OR expansion)"
        """
        params = {
            "q": query,
            "from-date": from_date,
            "to-date": to_date,
            "show-fields": self.FULL_FIELDS if full_text else self.TRIAGE_FIELDS,
            "show-tags": "keyword",
            "page-size": min(max_results, 50),
            "order-by": "newest",
            "api-key": self.api_key,
        }
        
        if section:
            params["section"] = section
        if tag:
            params["tag"] = tag

        results = await self._paginated_search(params, max_results)
        return [self._parse_result(r, full_text) for r in results]

    async def get_article(self, guardian_url: str) -> Optional[GuardianArticle]:
        """
        Fetch a specific article by its Guardian URL.
        
        Converts theguardian.com URL to API URL:
        https://www.theguardian.com/world/2026/mar/18/article-slug
        → https://content.guardianapis.com/world/2026/mar/18/article-slug
        """
        # Extract path from URL
        path = guardian_url.replace("https://www.theguardian.com/", "")
        path = path.replace("http://www.theguardian.com/", "")
        
        api_url = f"{self.BASE_URL}/{path}"
        params = {
            "show-fields": self.FULL_FIELDS,
            "show-tags": "keyword",
            "api-key": self.api_key,
        }

        async with self._semaphore:
            response = await self._client.get(api_url, params=params)

        if response.status_code != 200:
            return None

        data = response.json()
        content = data.get("response", {}).get("content")
        if not content:
            return None

        return self._parse_result(content, full_text=True)

    async def _paginated_search(
        self, params: dict, max_results: int
    ) -> list[dict]:
        """Fetch search results, paginating if necessary."""
        all_results = []
        page = 1

        while len(all_results) < max_results:
            params["page"] = page
            
            async with self._semaphore:
                response = await self._client.get(
                    f"{self.BASE_URL}/search", params=params
                )

            if response.status_code != 200:
                break

            data = response.json().get("response", {})
            results = data.get("results", [])
            
            if not results:
                break

            all_results.extend(results)
            
            # Check if there are more pages
            total_pages = data.get("pages", 1)
            if page >= total_pages:
                break
            
            page += 1

        return all_results[:max_results]

    def _parse_result(self, result: dict, full_text: bool) -> GuardianArticle:
        """Parse a single API result into a GuardianArticle."""
        fields = result.get("fields", {})
        tags = result.get("tags", [])

        body_html = fields.get("body", "")
        text = strip_html(body_html) if full_text and body_html else ""

        return GuardianArticle(
            url=result.get("webUrl", ""),
            guardian_id=result.get("id", ""),
            title=fields.get("headline", result.get("webTitle", "")),
            text=text,
            snippet=strip_html(fields.get("standfirst", "")),
            byline=fields.get("byline"),
            wordcount=int(fields.get("wordcount", 0)),
            publication_date=result.get("webPublicationDate", ""),
            section=result.get("sectionId", ""),
            tags=[t["id"] for t in tags],
            short_url=fields.get("shortUrl"),
        )

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()


# --- Integration helper for the extraction orchestrator ---

async def guardian_extract_for_country(
    api: GuardianAPI,
    country_code: str,
    actor_query: str,
    from_date: str,
    to_date: str,
) -> list[dict]:
    """
    Convenience function for the extraction orchestrator.
    
    Returns articles in the pipeline's standard extraction format,
    ready to merge with Brave + extraction chain results.
    """
    articles = await api.search_country(
        country_code=country_code,
        actor_query=actor_query,
        from_date=from_date,
        to_date=to_date,
        full_text=True,
    )
    return [a.to_extraction_format() for a in articles]


async def guardian_triage_for_country(
    api: GuardianAPI,
    country_code: str,
    from_date: str,
    to_date: str,
) -> list[dict]:
    """
    Lightweight triage query — headlines only, no actor filtering.
    
    Returns recent Guardian coverage of a country for triage enrichment.
    Only worth calling for countries where Guardian has Tier 1-2 coverage:
    gb, au, in, fr, de, ua.
    """
    if country_code not in GUARDIAN_COUNTRIES:
        return []
    
    articles = await api.search_country(
        country_code=country_code,
        actor_query="",  # No actor filter — get all coverage
        from_date=from_date,
        to_date=to_date,
        full_text=False,
        max_results=10,
    )
    return [a.to_extraction_format() for a in articles]
```

---

## Orchestrator Integration

### Where Guardian Fits in the Pipeline Flow

```
Step 2: NEWS COLLECTION — Layer 1

  For deep-dive countries:
    ┌─────────────────────┐    ┌─────────────────────┐
    │   Brave News API    │    │   Guardian API       │
    │   + Goggle queries  │    │   (13 countries)     │
    │   (all countries)   │    │                      │
    └─────────┬───────────┘    └─────────┬───────────┘
              │                          │
              ▼                          │ (already extracted)
    ┌─────────────────────┐              │
    │  Extraction chain   │              │
    │  (curl/diffbot/     │              │
    │   playwright/etc)   │              │
    └─────────┬───────────┘              │
              │                          │
              ▼                          ▼
    ┌────────────────────────────────────────────┐
    │          Deduplicate + Merge               │
    │  (Guardian API results take precedence     │
    │   over Brave-extracted Guardian articles)  │
    └─────────────────┬──────────────────────────┘
                      │
                      ▼
              Country Agent Input
```

### Deduplication Logic

When both Brave and the Guardian API return the same article:
1. Match by URL (normalize: strip query params, trailing slashes)
2. If match found, keep the Guardian API version (guaranteed full text, structured metadata)
3. If Brave found a Guardian article that the API query missed (different search terms), extract it via curl (3/3 success rate for theguardian.com)

### Countries Without Guardian Coverage

For countries not in `GUARDIAN_COUNTRIES` (Estonia, Latvia, Lithuania, Czech Republic, Romania, Chile, Norway, Sweden, Finland, Mexico, Poland, Spain, Italy, UAE), the Guardian API is not queried. Layer 1 relies entirely on Brave + extraction chain.

---

## Cost

Guardian API is free at the developer tier. The only cost consideration is the 500 calls/day limit, which the pipeline is well within (~16 calls per weekly cycle, plus margin for retries and pagination).

If the pipeline later needs to run more frequently than weekly, or if the country list expands significantly, a commercial tier may be needed. Contact Guardian developer support.
