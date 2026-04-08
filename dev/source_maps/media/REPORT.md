# Source Intelligence Maps: Comprehensive Report

**Generated:** 2026-03-16
**Pipeline scope:** 28 democratic middle powers across 5 geopolitical signal domains

---

## Executive Summary

This report documents a curated OSINT source collection for monitoring how 28 democratic middle powers position themselves internationally. The collection spans **493 sources** across **28 countries**, organized into five analytical domains: diplomatic alignment, security and defence autonomy, economic and technological statecraft, institutional engagement, and domestic constraints on external action.

Each source was selected based on its influence on the domestic policy-making class, editorial independence, and coverage of the five signal domains. Every source was then tested for automated accessibility using `curl`-based HTTP extraction — a conservative baseline that underestimates real-world performance (many modern sites require JavaScript rendering via headless browsers).

**Key findings:**
- **86.8%** of sources have reachable homepages via simple HTTP
- **50.9%** of sources are accessible via either direct HTML scraping or RSS full text — the effective floor for automated ingestion
- **33.3%** yield full article text from direct curl extraction alone
- **42.6%** offer RSS feeds; of those, **78.6%** provide full text in the feed
- The best-performing countries (Canada 89%, Australia 59%, Brazil 56%) have English-language or open-access media ecosystems; the hardest (Turkey 11%, Lithuania 12%, Japan 17%) rely heavily on JS-rendered sites or restrict bot access

---

## 1. Coverage by Region

| Region | Countries | Sources | Avg Sources/Country |
|---|---|---|---|
| Western Europe | 8 | 136 | 17.0 |
| Eastern Europe & Baltics | 7 | 121 | 17.3 |
| Asia-Pacific | 6 | 107 | 17.8 |
| Americas | 4 | 72 | 18.0 |
| Middle East | 3 | 53 | 17.7 |
| **Total** | **28** | **493** | **17.6** |

### Countries by Region

**Western Europe:** United Kingdom, France, Germany, Italy, Spain, Norway, Sweden, Finland
**Eastern Europe & Baltics:** Poland, Czech Republic, Romania, Ukraine, Estonia, Latvia, Lithuania
**Asia-Pacific:** Japan, South Korea, Taiwan, Australia, India, Indonesia
**Americas:** Canada, Mexico, Brazil, Chile
**Middle East:** Turkey, Saudi Arabia, UAE

---

## 2. Accessibility Test Results

### 2.1 Aggregate Performance

| Metric | Count | Rate |
|---|---|---|
| Homepage reachable | 428 / 493 | **86.8%** |
| Article page fetchable | 223 / 493 | **45.2%** |
| Full text extractable (HTML) | 164 / 493 | **33.3%** |
| RSS feed available | 210 / 493 | **42.6%** |
| RSS provides full text | 165 / 493 | **33.5%** |
| **Accessible via either channel** | **251 / 493** | **50.9%** |

> **Methodology note:** Tests used `curl` with a standard User-Agent, 15-second timeout, following redirects. This is a conservative baseline — sites returning 403/401 or requiring JavaScript will perform better with Playwright/Puppeteer and proper session handling.

### 2.2 Per-Country Accessibility Rankings

Ranked by full-text extraction rate (direct HTML scraping):

| Rank | Country | Sources | Homepage | Article | Full Text | RSS | Tier |
|---|---|---|---|---|---|---|---|
| 1 | Canada | 18 | 100% | 94% | **89%** | 83% | Excellent |
| 2 | Australia | 17 | 82% | 65% | **59%** | 47% | Good |
| 3 | Brazil | 18 | 100% | 61% | **56%** | 67% | Good |
| 4 | Latvia | 17 | 88% | 59% | **53%** | 65% | Good |
| 5 | Estonia | 16 | 100% | 69% | **50%** | 62% | Good |
| 6 | Romania | 17 | 76% | 47% | **41%** | 76% | Moderate |
| 7 | Saudi Arabia | 17 | 82% | 47% | **41%** | 24% | Moderate |
| 8 | Italy | 18 | 89% | 61% | **39%** | 50% | Moderate |
| 9 | Sweden | 17 | 88% | 47% | **35%** | 65% | Moderate |
| 10 | Chile | 18 | 83% | 61% | **33%** | 28% | Moderate |
| 11 | Mexico | 18 | 100% | 44% | **33%** | 39% | Moderate |
| 12 | South Korea | 18 | 78% | 39% | **33%** | 39% | Moderate |
| 13 | Taiwan | 18 | 94% | 39% | **33%** | 22% | Moderate |
| 14 | India | 19 | 95% | 42% | **32%** | 26% | Moderate |
| 15 | Finland | 17 | 100% | 53% | **29%** | 47% | Limited |
| 16 | Indonesia | 17 | 88% | 53% | **29%** | 41% | Limited |
| 17 | Norway | 18 | 100% | 50% | **28%** | 39% | Limited |
| 18 | Spain | 18 | 89% | 39% | **28%** | 33% | Limited |
| 19 | Czech Republic | 19 | 89% | 42% | **26%** | 68% | Limited |
| 20 | France | 17 | 71% | 29% | **24%** | 29% | Limited |
| 21 | Germany | 17 | 94% | 24% | **24%** | 24% | Limited |
| 22 | Ukraine | 18 | 83% | 44% | **22%** | 44% | Difficult |
| 23 | United Kingdom | 18 | 67% | 39% | **22%** | 28% | Difficult |
| 24 | Poland | 17 | 94% | 41% | **18%** | 41% | Difficult |
| 25 | UAE | 17 | 88% | 35% | **18%** | 29% | Difficult |
| 26 | Japan | 18 | 72% | 22% | **17%** | 11% | Difficult |
| 27 | Lithuania | 17 | 71% | 12% | **12%** | 35% | Difficult |
| 28 | Turkey | 19 | 68% | 11% | **11%** | 32% | Difficult |

### 2.3 Accessibility Tiers

| Tier | Criteria | Countries | Recommendation |
|---|---|---|---|
| **Excellent** (>50%) | Majority of sources yield full text via curl | Canada | Curl-based pipeline viable as primary |
| **Good** (40-59%) | Strong subset accessible | Australia, Brazil, Latvia, Estonia | Curl primary + RSS supplement |
| **Moderate** (30-39%) | Mixed results | Romania, Saudi Arabia, Italy, Sweden, Chile, Mexico, South Korea, Taiwan, India | RSS primary + curl fallback; consider headless for key sources |
| **Limited** (20-29%) | Most sources resist simple extraction | Finland, Indonesia, Norway, Spain, Czech Republic, France, Germany | Headless browser required for most sources |
| **Difficult** (<20%) | Hostile to automated extraction | Ukraine, UK, Poland, UAE, Japan, Lithuania, Turkey | Headless browser + RSS + API access essential |

---

## 3. Homepage Failures (65 sources)

Sources whose homepage returned non-200 status codes or timed out. These require investigation — some may be temporary, others structural (bot blocking, geo-restriction, or misconfigured servers).

### By Failure Type

| Status | Count | Meaning |
|---|---|---|
| 403 Forbidden | 39 | Bot/scraper blocking (most common) |
| 0 / timeout | 7 | Connection failed or DNS issue |
| ? / unknown | 12 | Test inconclusive |
| 401 Unauthorized | 3 | Authentication required (Reuters) |
| 402 Payment Required | 1 | Paywall enforcement at HTTP level (Telegraph) |
| 404 Not Found | 1 | Bad URL (Japan Kantei) |

### Highest-Impact Failures

These are globally significant or high-value sources that block simple HTTP access:

| Source | Domain | Country | Status | Impact |
|---|---|---|---|---|
| Financial Times | ft.com | UK | 403 | Tier-1 global financial coverage |
| The Economist | economist.com | UK | 403 | Tier-1 global policy analysis |
| Reuters | reuters.com | UK/Chile/Japan | 401 | Primary wire service |
| The Telegraph | telegraph.co.uk | UK | 402 | UK defence/conservative lens |
| Les Echos | lesechos.fr | France | 403 | French business press |
| Liberation | liberation.fr | France | 403 | French centre-left |
| Arab News | arabnews.com | Saudi Arabia | 403 | English-language Saudi |
| Al Arabiya | alarabiya.net | Saudi/UAE | 403 | Pan-Arab broadcast |
| Anadolu Agency | anadolu.com.tr | Turkey | 403 | Turkish state wire |
| Hansard | hansard.parliament.uk | UK | 403 | UK parliamentary record |

---

## 4. RSS Feed Analysis

Of 493 sources tested:
- **210 (42.6%)** have discoverable RSS feeds
- **165 (33.5%)** provide full article text in their RSS feed
- RSS full-text rate among feeds that exist: **78.6%**

RSS is frequently the most reliable extraction channel — feeds that exist tend to provide complete content, bypassing paywall and JS-rendering issues entirely.

### RSS Champions (by country)

| Country | RSS Available | RSS Full Text | Notes |
|---|---|---|---|
| Canada | 83% | — | Excellent RSS ecosystem |
| Romania | 76% | — | Eastern European sites often maintain RSS |
| Czech Republic | 68% | — | Strong RSS despite low HTML scraping |
| Brazil | 67% | — | Many Brazilian outlets maintain feeds |
| Latvia | 65% | — | Baltic RSS tradition |
| Sweden | 65% | — | Nordic RSS support |
| Estonia | 62% | — | Baltic RSS tradition |

### RSS-as-Lifeline Countries

Countries where RSS significantly outperforms direct scraping:

| Country | Full Text (HTML) | RSS Available | Delta |
|---|---|---|---|
| Czech Republic | 26% | 68% | **+42pp** |
| Sweden | 35% | 65% | **+30pp** |
| Poland | 18% | 41% | **+23pp** |
| Ukraine | 22% | 44% | **+22pp** |
| Lithuania | 12% | 35% | **+23pp** |
| Turkey | 11% | 32% | **+21pp** |

For these countries, RSS should be the **primary ingestion channel**, with HTML scraping as fallback.

---

## 5. Source Type Distribution

The standardized source types across all maps:

| Type | Count | Description |
|---|---|---|
| Paper of record | ~70 | National broadsheets and public broadcasters |
| Political specialist | ~45 | Policy magazines, political newsletters, niche outlets |
| Security & defence | ~35 | Defence journals, military analysis, strategic studies |
| Government/official | ~35 | Government press offices, legislative records, wire services |
| Business & financial | ~30 | Financial dailies, economic coverage |
| Think tank / research | ~40 | Policy institutes, academic analysis platforms |
| Opposition-aligned | ~25 | Outlets reflecting opposition or alternative perspectives |
| Investigative | ~25 | Independent investigative journalism outlets |
| Regional | ~15 | Regional or devolved-nation perspectives |

> Note: Type labels vary across source maps due to per-country formatting differences. Counts are approximate groupings.

---

## 6. Language Distribution

| Language(s) | Countries |
|---|---|
| English only | United Kingdom, Australia, India* |
| English + local | Canada (FR), South Korea (KR), Japan (JA), Taiwan (ZH), Indonesia (ID), UAE (AR), Saudi Arabia (AR) |
| Local only | France (FR), Germany (DE), Spain (ES), Italy (IT), Norway (NO), Sweden (SV), Finland (FI), Poland (PL), Czech Republic (CS), Romania (RO), Estonia (ET), Latvia (LV), Lithuania (LT), Ukraine (UK), Turkey (TR), Brazil (PT), Chile (ES), Mexico (ES) |

*India sources include both English and Hindi-language outlets.

**Implication for pipeline:** Google News API queries need to be issued in both the country's primary language(s) and English (where English-language outlets exist) to achieve complete coverage.

---

## 7. Coverage Gap Analysis

Recurring themes across all 28 country source maps:

### 7.1 Intelligence & Security Services

Nearly every country map flags a gap in coverage of intelligence community activity. This is structural — intelligence operations are by definition resistant to open-source monitoring. Partial mitigation via:
- Think tanks with government adjacency (RUSI, CSIS, IISS)
- FOI-based investigative outlets (Declassified UK, Netzpolitik.org)
- Parliamentary oversight committee publications

### 7.2 Defence Procurement & Industrial Base

Several countries lack dedicated defence-industry trade press:
- **Chile, Mexico, Brazil:** No domestic defence beat; reliance on Spanish-language Infodefensa or DefesaNet
- **Indonesia:** Self-censorship around military institutional dynamics
- **Czech Republic, Romania:** Defence-export coverage thin despite growing industries

### 7.3 Sub-National / Regional Perspectives

Federal or devolved systems have under-monitored regional dynamics:
- **UK:** Scottish independence → Trident basing, NATO posture
- **Spain:** Basque/Galician regional foreign policy perspectives
- **India:** Regional-language press in southern/northeastern states
- **Canada:** Arctic sovereignty, Indigenous perspectives on Northern affairs
- **Indonesia:** Outer-island perspectives on South China Sea

### 7.4 Non-Elite / Social Media Discourse

Several maps note that policy-elite sources miss populist or grassroots signals:
- **Poland:** Conservative Telegram/social media channels
- **Turkey:** Encrypted messaging and social media circumventing press restrictions
- **Brazil:** WhatsApp-driven political discourse
- **India:** Hindi-belt vernacular media

---

## 8. Recommendations for Pipeline Implementation

### 8.1 Ingestion Strategy (by tier)

```
Tier 1: RSS Full Text (where available)
  → Lowest latency, highest reliability, bypasses paywalls
  → Primary channel for 210 sources (42.6%)

Tier 2: Direct HTML Extraction (curl/requests)
  → Works for ~164 sources (33.3%)
  → Use newspaper3k, trafilatura, or readability for text extraction

Tier 3: Headless Browser (Playwright/Puppeteer)
  → Required for JS-rendered SPAs (common in Japan, Turkey, Lithuania)
  → Estimate ~80-100 additional sources recoverable

Tier 4: Google News API Snippet
  → Fallback for hard-paywalled sources (FT, Economist, Janes)
  → Headline + snippet only; flag as incomplete

Tier 5: Manual / API Access
  → Premium subscriptions (Janes, Politico Pro, Bloomberg Terminal)
  → Government APIs where available
```

### 8.2 Priority Headless Browser Targets

Countries where headless browser investment yields the highest marginal return:

| Country | Current Full Text | Est. with Headless | Key Sources Recovered |
|---|---|---|---|
| Turkey | 11% | ~45% | Anadolu, Sozcu, T24, Bianet |
| Japan | 17% | ~50% | NHK, Mainichi, Yomiuri, Kantei |
| Lithuania | 12% | ~40% | Delfi, LRT, 15min |
| United Kingdom | 22% | ~55% | FT, Economist, Telegraph, Hansard |
| France | 24% | ~50% | Les Echos, Liberation, Le Monde |
| Germany | 24% | ~50% | FAZ, Handelsblatt, Zeit |

### 8.3 Source Whitelist JSON Schema

Recommended structure for the pipeline's source whitelist:

```json
{
  "country": "united_kingdom",
  "google_news_codes": ["GB:en"],
  "sources": [
    {
      "name": "BBC News",
      "domain": "bbc.co.uk",
      "alt_domains": ["bbc.com"],
      "type": "paper_of_record",
      "language": "en",
      "domains_covered": ["diplomatic_alignment", "security_defence", "institutional_engagement", "domestic_constraints"],
      "editorial_orientation": "centrist",
      "ingestion": {
        "primary_channel": "rss",
        "rss_url": "https://feeds.bbci.co.uk/news/rss.xml",
        "rss_full_text": true,
        "fallback_channel": "html",
        "requires_headless": false,
        "paywall": "none"
      },
      "reliability_flags": {
        "is_government_source": false,
        "is_state_affiliated": false,
        "ownership_note": "BBC, publicly funded via licence fee"
      }
    }
  ]
}
```

### 8.4 Monitoring & Maintenance

- **Quarterly re-test:** Re-run accessibility tests every 90 days; sites change bot-blocking policies
- **RSS feed health:** Monitor for feeds going stale (>7 days no update) — may indicate feed deprecation
- **Source map refresh:** Review source selections annually or when major media ownership changes occur (e.g., Postmedia acquisition)
- **Coverage gap tracking:** Maintain a watchlist of excluded outlets (see Notable Exclusions in each country map) for promotion if coverage gaps widen

---

## 9. File Inventory

### Source Intelligence Maps (28 files)

```
/Users/zen/dev/src/pdb/docs/source_intelligence_maps/
├── australia.md          ├── japan.md
├── brazil.md             ├── latvia.md
├── canada.md             ├── lithuania.md
├── chile.md              ├── mexico.md
├── czech_republic.md     ├── norway.md
├── estonia.md            ├── poland.md
├── finland.md            ├── romania.md
├── france.md             ├── saudi_arabia.md
├── germany.md            ├── south_korea.md
├── india.md              ├── spain.md
├── indonesia.md          ├── sweden.md
├── italy.md              ├── taiwan.md
├── turkey.md             ├── uae.md
├── ukraine.md            └── united_kingdom.md
```

### Accessibility Test Results (28 files)

```
/Users/zen/dev/src/pdb/docs/source_intelligence_maps/tests/
├── {country}_accessibility.json  (×28)
```

Each JSON file contains an array of source objects with fields:
`source_name`, `domain`, `can_fetch_homepage`, `homepage_status_code`, `can_fetch_article`, `can_get_full_text`, `first_paragraph`, `last_paragraph`, `test_article_url`, `publication_date`, `has_rss`, `rss_url`, `rss_has_full_text`, `notes`

---

## 10. Summary Statistics

| Metric | Value |
|---|---|
| Countries covered | 28 |
| Total sources curated | 493 |
| Average sources per country | 17.6 |
| Languages represented | 22+ |
| Sources with reachable homepage | 428 (86.8%) |
| Sources with extractable full text (HTML) | 164 (33.3%) |
| Sources with RSS feeds | 210 (42.6%) |
| Sources accessible via any automated channel | 251 (50.9%) |
| Estimated accessible with headless browser | ~350 (71%) |
| Sources requiring subscription/API | ~50 (10%) |
| Completely inaccessible to automation | ~90 (18%) |
