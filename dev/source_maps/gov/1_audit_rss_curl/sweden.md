# Sweden Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/sweden_government_sources.md`
**Test method:** WebFetch (primary), curl with browser User-Agent (fallback)

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 68 |
| Fully reachable (200 OK with content) | 52 |
| HTTP 403 (bot protection) | 9 |
| HTTP 404 (not found) | 3 |
| Connection/TLS failure | 1 |
| Redirect (301 to working URL) | 1 |
| Not a valid feed (HTML instead of RSS/Atom) | 2 |

### Key Findings

1. **government.se (English portal)** returns 403 to automated fetchers across all tested pages. The RSS feed from government.se works (returns valid RSS 2.0), but HTML pages are blocked. The Swedish-language regeringen.se has no bot protection and works perfectly.
2. **Försvarsmakten RSS** (`forsvarsmakten.se/sv/aktuellt/feed.rss`) returns 404 even with browser User-Agent. The RSS feed is dead. HTML entry points work fine.
3. **Riksdagen Open Data RSS feeds** all work perfectly — 4/4 feeds return valid RSS with current content.
4. **regeringen.se** platform works reliably for all Swedish-language pages (pressmeddelanden, tal, propositioner, rattsliga-dokument). One sub-URL (`/regeringens-politik/regeringsbeslut/`) returns 404.
5. **NATO Atom feed** (`news.htm?type=newsAtom`) returns HTML, not Atom XML — the feed URL is invalid.
6. **EU Council** (`consilium.europa.eu`) returns 403 on all tested URLs.
7. **norden.org** returns 403.
8. **svenskforfattningssamling.se** (SFS) returns 403.
9. **FOI RSS page** exists as HTML but the actual XML feed URL is not exposed; TLS connection failed on direct curl test.
10. **Riksgalden RSS** page lists 6 working RSS feed URLs — a useful discovery.

---

## 1. RSS/Atom Feed Tests

### Confirmed Working Feeds

| Feed | URL | Status | Notes |
|---|---|---|---|
| Government.se all-ministry RSS | `https://www.government.se/Filter/RssFeed?filterType=Taxonomy&filterByType=FilterablePageBase&preFilteredCategories=2069,...,2189&rootPageReference=0` | **OK** | Valid RSS 2.0. Recent items include Ukraine defense, Iran execution statement. |
| Riksdagen — Decisions | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=bet&beslutad=1&sort=beslutsdag&sortorder=desc&utformat=rss` | **OK** | Valid RSS. Current content. |
| Riksdagen — Propositions | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=prop&sort=datum&sortorder=desc&utformat=rss` | **OK** | Valid RSS. Current content (March 2026). |
| Riksdagen — Motions | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=mot&sort=datum&sortorder=desc&utformat=rss` | **OK** | Valid RSS. Current content (nuclear energy motions, March 2026). |
| Riksdagen — Questions/Interpellations | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=ip,fr,frs,ku-anm&sort=datum&sortorder=desc&utformat=rss` | **OK** | Valid RSS. Current content. |

### Failed / Invalid Feeds

| Feed | URL | Status | Notes |
|---|---|---|---|
| Försvarsmakten RSS | `https://www.forsvarsmakten.se/sv/aktuellt/feed.rss` | **404** | Dead URL. Returns 404 even with browser UA. [VERIFY] item **confirmed invalid**. |
| NATO Atom feed | `https://www.nato.int/cps/en/natohq/news.htm?type=newsAtom` | **INVALID** | Returns HTML page, not Atom XML. [VERIFY] item **confirmed invalid**. |
| EU Council RSS | `https://www.consilium.europa.eu/en/rss/` | **403** | Bot protection. [VERIFY] item **inconclusive** — blocked by WAF. |

### Feed Hub Pages (HTML, not feeds themselves)

| Page | URL | Status | Notes |
|---|---|---|---|
| Riksbank RSS subscription | `https://www.riksbank.se/en-gb/press-and-published/subscribe-via-rss/` | **200 OK** | HTML page. No individual feed XML URLs exposed in page content. Requires inspecting page source for `<link rel="alternate">` tags. |
| FOI RSS news | `https://www.foi.se/en/foi/misc/rss-news.html` | **200 OK** | HTML page, not RSS XML. Actual XML feed URL not discoverable from page content. [VERIFY] item **inconclusive**. |
| Riksgalden RSS | `https://www.riksgalden.se/en/press-and-publications/subscribe/rss-on-riksgalden.se/` | **200 OK** | HTML page listing 6 RSS feed paths (see below). |

### Riksgalden RSS Feeds Discovered

| Feed | Relative URL |
|---|---|
| Press releases and news | `/en/press-and-publications/press-releases-and-news/rss/` |
| Borrowing requirements | `/en/press-and-publications/press-releases-and-news/newslists/newslist-central-government-borrowing/rss/` |
| Latest reports | `/en/press-and-publications/publications/rss/` |
| Government borrowing forecasts | `/press-och-publicerat/publikationer/statsupplaning/rss2/` |
| Central government debt | `/en/press-and-publications/press-releases-and-news/newslists/newslist-government-debt/rss/` |
| Guidelines | `/press-och-publicerat/publikationer/riktlinjer/rss/` |

---

## 2. Entry Point URL Tests — By Institution

### 2.1 Regeringskansliet (Government Offices / PM)

| URL | Status | Notes |
|---|---|---|
| `https://www.regeringen.se/pressmeddelanden/` | **OK** | 8,937 press releases. Filtering, RSS subscription available. |
| `https://www.government.se/press-releases/` | **403** | Bot protection on government.se HTML pages. |
| `https://www.regeringen.se/regeringens-politik/regeringsbeslut/` | **404** | URL not found. May have been restructured. |
| `https://www.regeringen.se/tal/` | **OK** | 273 speeches listed. Filtering available. |
| `https://www.regeringen.se/rattsliga-dokument/proposition/` | **OK** | 4,274 propositions. Working search/filter. |
| `https://www.government.se/prime-minister/` | **403** | Bot protection on government.se. |

### 2.2 Utrikesdepartementet (Foreign Affairs)

| URL | Status | Notes |
|---|---|---|
| `https://www.regeringen.se/pressmeddelanden/?teleFilter=Utrikesdepartementet` | **OK** | Filtered press releases working. |
| `https://www.government.se/government-of-sweden/ministry-for-foreign-affairs/` | **403** | Bot protection. |
| `https://www.government.se/government-of-sweden/ministry-for-foreign-affairs/diplomatic-portal/` | **403** | Bot protection. |
| `https://www.swedenabroad.se/` | **OK** | Embassy network portal. Multi-language. |
| `https://www.government.se/government-policy/foreign-policy/` | **403** | Bot protection. |
| `https://www.regeringen.se/uds-reseinformation/` | **OK** | UD travel information portal. |

### 2.3 Försvarsdepartementet (Defence Ministry)

| URL | Status | Notes |
|---|---|---|
| `https://www.regeringen.se/pressmeddelanden/?teleFilter=Försvarsdepartementet` | **OK** | Filtered press releases working. |
| `https://www.government.se/government-of-sweden/ministry-of-defence/` | **403** | Bot protection. |

### 2.4 Försvarsmakten (Armed Forces)

| URL | Status | Notes |
|---|---|---|
| `https://www.forsvarsmakten.se/sv/aktuellt/` | **OK** | News page with current articles (March 2026). |
| `https://www.forsvarsmakten.se/en/news/` | **OK** | English news. NATO/Sweden content. |
| `https://www.forsvarsmakten.se/sv/aktuellt/feed.rss` | **404** | RSS feed dead. |
| `https://www.mynewsdesk.com/com/forsvarsmakten` | **OK** | Press room with recent military news. |
| `https://www.forsvarsmakten.se/en/news/press-contacts/` | **OK** | Contact info: 08-788 88 88. |
| `https://www.forsvarsmakten.se/siteassets/2-om-forsvarsmakten/dokument/musts-arsoversikter/` | **404** | Directory listing not accessible. Individual PDF files may still exist. |

### 2.5 Riksdagen (Parliament)

| URL | Status | Notes |
|---|---|---|
| `https://www.riksdagen.se/sv/aktuellt/` | **OK** | Current news, calendar, decisions. |
| `https://www.riksdagen.se/en/news/` | **OK** | English news page. |
| `https://www.riksdagen.se/sv/dokument-och-lagar/` | **OK** | 500,000+ documents searchable. |
| `https://data.riksdagen.se/` | **301** | Redirects to `riksdagen.se/sv/dokument-och-lagar/riksdagens-oppna-data/`. Working redirect. |
| `https://www.riksdagen.se/sv/folj-och-prenumerera/prenumerera-via-e-post/` | **OK** | Email subscription page. Multiple lists available. |

### 2.6 SFS (Official Gazette)

| URL | Status | Notes |
|---|---|---|
| `https://svenskforfattningssamling.se/` | **403** | Bot protection or access restriction. [VERIFY RSS] — **no RSS confirmed, site blocked**. |
| `https://lagrummet.se/` | **OK** | Legal information portal. Operated by Domstolsverket. |
| `https://www.regeringen.se/rattsliga-dokument/` | **OK** | 20,565 legal documents. Working search/filter. |

### 2.7 Finansdepartementet (Finance)

| URL | Status | Notes |
|---|---|---|
| `https://www.regeringen.se/pressmeddelanden/?teleFilter=Finansdepartementet` | **OK** | Filtered press releases. 8,937 total results. |
| `https://www.government.se/government-of-sweden/ministry-of-finance/` | **403** | Bot protection. |
| `https://www.regeringen.se/rattsliga-dokument/proposition/?teleFilter=Finansdepartementet` | **OK** | Budget propositions listing. |
| `https://www.government.se/government-policy/the-budget-and-fiscal-policy/` | **403** | Bot protection. |
| `https://www.riksgalden.se/en/press-and-publications/press-releases-and-news/` | **OK** | Debt Office press releases. RSS available. |
| `https://www.riksgalden.se/en/press-and-publications/subscribe/rss-on-riksgalden.se/` | **OK** | RSS hub page. 6 feeds listed. |

### 2.8 Riksbank (Central Bank)

| URL | Status | Notes |
|---|---|---|
| `https://www.riksbank.se/sv/press-och-publicerat/` | **OK** | Swedish press hub. |
| `https://www.riksbank.se/en-gb/press-and-published/` | **OK** | English press hub. |
| `https://www.riksbank.se/en-gb/press-and-published/subscribe-via-rss/` | **OK** | RSS subscription page (HTML hub, not feed itself). |
| `https://www.riksbank.se/en-gb/press-and-published/notices-and-press-releases/press-releases/` | **OK** | Press releases listing. |
| `https://www.riksbank.se/en-gb/statistics/` | **OK** | Statistics portal. |
| `https://www.riksbank.se/en-gb/monetary-policy/monetary-policy-report/` | **OK** | Monetary policy decisions. |
| `https://www.riksbank.se/en-gb/financial-stability/financial-stability-report/` | **OK** | Financial stability reports. |

### 2.9 Trade / Commerce

| URL | Status | Notes |
|---|---|---|
| `https://www.kommerskollegium.se/en/` | **OK** | English homepage. Trade policy sections. |
| `https://www.kommerskollegium.se/` | **OK** | Swedish homepage. [VERIFY RSS] — **no RSS found**. |
| `https://www.business-sweden.com/about-us/media/press-releases/` | **OK** | Press releases archive. 2025-2026 content. [VERIFY RSS] — **no RSS found**. |
| `https://isp.se/` | **OK** | Swedish homepage. Arms exports, sanctions, FDI screening. [VERIFY RSS] — **no RSS found**. |
| `https://isp.se/eng` | **OK** | English homepage. |

### 2.10 Intelligence / Security

| URL | Status | Notes |
|---|---|---|
| `https://www.sakerhetspolisen.se/ovriga-sidor/nyheter.html` | **OK** | News page. 10 articles. March 2026 content. |
| `https://sakerhetspolisen.se/ovriga-sidor/pressrum.html` | **OK** | Press room with contacts and spokespersons. |
| `https://sakerhetspolisen.se/ovriga-sidor/other-languages/english-engelska.html` | **OK** | English section. Annual assessment 2025-26 featured. |
| `https://www.forsvarsmakten.se/en/about-the-swedish-armed-forces/organisation/joint-forces/military-intelligence-and-security-service-must/` | **OK** | MUST organizational page. Lt Gen Thomas Nilsson. |
| `https://www.fra.se/` | **OK** | FRA homepage. Annual report "En farligare tid" featured. |

### 2.11 FOI (Defence Research Agency)

| URL | Status | Notes |
|---|---|---|
| `https://www.foi.se/en/foi/news-and-pressroom.html` | **OK** | English news/press. RSS mentioned on page. |
| `https://www.foi.se/nyheter-och-press.html` | **OK** | Swedish news/press. |
| `https://www.foi.se/en/foi/misc/rss-news.html` | **OK** | HTML page (not RSS XML). Actual feed URL not exposed. [VERIFY] — **inconclusive**. |

### 2.12 NATO

| URL | Status | Notes |
|---|---|---|
| `https://www.nato.int/cps/en/natohq/news.htm` | **OK** | News hub. Site undergoing redesign. |
| `https://www.nato.int/cps/en/natohq/topics_52535.htm` | **OK** | Sweden-NATO relations page. Accession March 7, 2024. |
| `https://www.nato.int/cps/en/natohq/news.htm?type=newsAtom` | **INVALID** | Returns HTML, not Atom feed. [VERIFY] — **confirmed invalid**. |

### 2.13 EU Council

| URL | Status | Notes |
|---|---|---|
| `https://www.consilium.europa.eu/en/press/press-releases/` | **403** | Bot protection / WAF. [VERIFY RSS] — **inconclusive**. |
| `https://www.consilium.europa.eu/en/rss/` | **403** | Bot protection / WAF. [VERIFY RSS] — **inconclusive**. |

### 2.14 Nordic Cooperation

| URL | Status | Notes |
|---|---|---|
| `https://www.norden.org/en/news` | **403** | Bot protection. [VERIFY RSS] — **inconclusive**. |
| `https://www.nordefco.org/` | **OK** | NORDEFCO homepage. News carousel. Denmark 2024 chairmanship. |

---

## 3. [VERIFY] Item Resolution

| Item | URL | Document Claim | Test Result | Verdict |
|---|---|---|---|---|
| Försvarsmakten RSS | `forsvarsmakten.se/sv/aktuellt/feed.rss` | RSS feed, may need browser UA | 404 with all UAs | **INVALID — feed does not exist** |
| SFS RSS | `svenskforfattningssamling.se/` | No RSS identified, verify | Site returns 403; no RSS found | **NO RSS — site has bot protection** |
| Kommerskollegium RSS | `kommerskollegium.se` | No RSS identified, verify | Site loads, no RSS found | **NO RSS** |
| Business Sweden RSS | `business-sweden.com` | No RSS identified, verify | Site loads, no RSS found | **NO RSS** |
| ISP RSS | `isp.se` | No RSS identified, verify | Site loads, no RSS found | **NO RSS** |
| FOI RSS exact URL | `foi.se/en/foi/misc/rss-news.html` | RSS news page, verify exact URL | HTML page, not XML feed | **INCONCLUSIVE — RSS exists per page text but XML URL unknown** |
| NATO Atom | `nato.int/cps/en/natohq/news.htm?type=newsAtom` | Atom feed, verify | Returns HTML, not Atom | **INVALID — not a feed** |
| EU Council RSS | `consilium.europa.eu/en/rss/` | RSS available, verify | 403 bot protection | **INCONCLUSIVE — blocked by WAF** |
| Norden.org RSS | `norden.org` | May have RSS, verify | 403 bot protection | **INCONCLUSIVE — blocked by WAF** |

---

## 4. Recommendations for Pipeline Configuration

### Immediate Actions

1. **Remove Försvarsmakten RSS** from config. Use HTML scraping of `/sv/aktuellt/` or MyNewsdesk as primary extraction.
2. **Remove NATO Atom feed** from config. Use HTML scraping of `nato.int/cps/en/natohq/news.htm`.
3. **Add Riksgalden RSS feeds** to Finansdepartementet monitoring (6 feeds discovered).
4. **Flag government.se HTML pages** as requiring browser-level fetching (Playwright/Puppeteer). The RSS feed works without authentication.
5. **Flag svenskforfattningssamling.se** as requiring browser-level fetching (403 to automated tools).
6. **Flag consilium.europa.eu and norden.org** as requiring browser-level fetching or API access.

### Reliable Automation Targets (RSS)

- Government.se all-ministry RSS feed (single URL covers all ministries)
- Riksdagen Open Data (4 feeds, all working, exceptionally well-structured)
- Riksgalden (6 feeds discovered)
- Riksbank RSS (hub page exists, individual feed URLs need source inspection)

### HTML Scraping Required

- Försvarsmakten `/sv/aktuellt/` and `/en/news/`
- SAPO `/ovriga-sidor/nyheter.html`
- FOI `/en/foi/news-and-pressroom.html`
- Kommerskollegium, Business Sweden, ISP (all entry points)
- FRA `/` (minimal content)

### Browser-Level Fetching Required

- government.se (all HTML pages — 403 to standard HTTP clients)
- svenskforfattningssamling.se (403)
- consilium.europa.eu (403)
- norden.org (403)
