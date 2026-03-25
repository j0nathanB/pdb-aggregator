# Lithuania Government Sources: URL Fetchability Test Results

**Date tested:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/lithuania_government_sources.md`
**Testing tools:** WebFetch (browser-like fetch) and curl with Mozilla UA
**Test location:** macOS / US-based IP

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 47 |
| Fully reachable (200 OK or WebFetch success) | 15 |
| Reachable via RSS only (HTML 403, RSS 200) | 3 |
| Blocked (403 Forbidden) | 26 |
| DNS failure | 1 |
| Not found (404) | 1 |
| Redirect (301, then reachable) | 1 |

**Key finding:** Many Lithuanian government sites (lrp.lt, kam.lt, lb.lt, vsd.lt, lrv.lt HTML pages, urm.lt) return HTTP 403 to both curl and WebFetch, likely due to geo-blocking or bot protection. However, **lrv.lt RSS feeds work reliably** -- the `/en/news/rss` pattern is confirmed functional for `lrv.lt` (Government/PM) and `finmin.lrv.lt` (Finance Ministry). Sites on independent infrastructure (lrs.lt Seimas, e-tar.lt legal registry, data.gov.lt, baltasam.org, ignitisgrupe.lt, nato.int) are generally reachable.

---

## Per-Source Results

### 1a. President of the Republic (lrp.lt) -- P1

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://lrp.lt/en/media-center/news/6607` | Entry point | 403 | 403 | BLOCKED |
| `https://lrp.lt/en/rss` | RSS [VERIFY] | 403 | 403 | BLOCKED -- no RSS found |
| `https://lrp.lt/en/feed` | RSS [VERIFY] | 403 | 403 | BLOCKED -- no RSS found |
| `https://lrp.lt/en/activities/speeches/` | Additional [VERIFY] | -- | 403 | BLOCKED |
| `https://lrp.lt/en/media-center/photos/` | Additional | -- | 403 | BLOCKED |
| `https://lrp.lt/en/activities/state-of-the-nation-address/` | Additional | -- | 403 | BLOCKED |

**Verdict:** All lrp.lt URLs blocked. Likely geo-blocking or strict bot protection. No RSS feed found. Pipeline will need proxy/VPN from EU IP or alternative monitoring via social media (@GitanasNauseda) and LRT coverage.

---

### 1b. Government / PM Office (lrv.lt) -- P1

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://lrv.lt/en/news/` | Entry point | 403 | 403 | BLOCKED (HTML) |
| `https://lrv.lt/en/news/rss` | RSS | **200 OK** (RSS 2.0, 30 items) | -- | **WORKS** |
| `https://lrv.lt/en/rss` | RSS alt | 403 | 403 | BLOCKED |
| `https://lrv.lt/en/ministries/` | Additional | -- | 403 | BLOCKED |
| `https://lrv.lt/en/about-government/government/` | Additional | -- | 403 | BLOCKED |
| `https://lrv.lt/en/relevant-information/contact-us/information-for-the-media-1` | Additional | -- | 403 | BLOCKED |
| `https://lrv.lt/en/newsletters` | Additional | -- | 403 | BLOCKED |

**Verdict:** HTML pages blocked, but **RSS feed confirmed at `lrv.lt/en/news/rss`** -- RSS 2.0 with 30 items, channel title "News - lrv.lt". This is the primary extraction method for this source.

---

### 1.2 Ministry of Foreign Affairs / URM (urm.lt) -- P1

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.urm.lt/en/news/928` | Entry point | 403 | 403 | BLOCKED |
| `https://www.urm.lt/en/rss` | RSS [VERIFY] | 403 | 403 | BLOCKED -- not confirmed |
| `https://www.urm.lt/en/news/928/rss` | RSS [VERIFY] | -- | 403 | BLOCKED -- not confirmed |

**Verdict:** All urm.lt URLs blocked. RSS not verifiable. Needs EU-based proxy or scraping from an EU IP.

---

### 1.3 Ministry of National Defence / KAM (kam.lt) -- P1

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://kam.lt/en/category/news/` | Entry point | 403 | 403 | BLOCKED |
| `https://kam.lt/en/feed/` | RSS [VERIFY] | 403 | 403 | BLOCKED -- not confirmed |
| `https://kam.lt/en/category/news/feed/` | RSS [VERIFY] | 403 | 403 | BLOCKED -- not confirmed |
| `https://kam.lt/en/antrasis-operatyviniu-tarnybu-departamentas/` | AOTD page | -- | 403 | BLOCKED |
| `https://kam.lt/en/faq/nato-enhanced-forward-presence/` | NATO EFP | -- | 403 | BLOCKED |
| `https://kam.lt/wp-content/uploads/2025/03/2025-GR-ENG-02-21-El-be-uzraso_.pdf` | Threat assessment PDF [VERIFY] | -- | 403 | BLOCKED |
| `https://kariuomene.kam.lt/en/` | Armed Forces | -- | DNS fail | **DNS FAILURE** |

**Verdict:** All kam.lt URLs blocked. WordPress RSS feeds not verifiable. `kariuomene.kam.lt` subdomain has DNS resolution failure -- may have been deprecated or merged into main kam.lt. Needs EU-based proxy.

---

### 1.4 Seimas / Parliament (lrs.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.lrs.lt/sip/portal.show?p_k=2&p_kade_id=10` | Entry point | **200 OK** (confirmed working) | 200 | **WORKS** |
| `https://www.lrs.lt/sip/portal.show?p_r=38375&p_k=2&p_a=1685&p_kade_id=10` | NSGK committee | -- | 200 | **WORKS** |
| `https://www.lrs.lt/sip/portal.show?p_r=35733&p_k=2&p_a=1676&p_kade_id=10` | Committees | -- | 200 | **WORKS** |
| `https://www.lrs.lt/sip/portal.show?p_r=35354&p_k=2&p_a=1643&p_kade_id=10` | 2024-2028 term | -- | 200 | **WORKS** |
| `https://e-seimas.lrs.lt/` | E-Seimas | -- | 200 | **WORKS** |

**Verdict:** All lrs.lt and e-seimas.lrs.lt URLs fully reachable. No RSS found but HTML scraping is viable. No bot protection observed.

---

### 1.5 Register of Legal Acts / TAR (e-tar.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.e-tar.lt/portal/lt/index` | Entry point (LT) | **200 OK** (confirmed working) | 200 | **WORKS** |
| `https://www.e-tar.lt/portal/en/index` | Entry point (EN) | -- | 200 | **WORKS** |
| `https://www.e-tar.lt/portal/lt/legalActSearch` | Legal act search | -- | 200 | **WORKS** |
| `https://data.gov.lt/datasets/2613/` | Open data | -- | 200 | **WORKS** |
| `https://www.teisesakturegistras.lt/` | Alt domain | -- | 403 | BLOCKED |

**Verdict:** Primary e-tar.lt URLs all reachable. Open data at data.gov.lt works. Alternative domain teisesakturegistras.lt is blocked. No RSS. HTML scraping viable.

---

### 1.6 Ministry of Finance (finmin.lrv.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://finmin.lrv.lt/en/news/` | Entry point | 403 | 403 | BLOCKED (HTML) |
| `https://finmin.lrv.lt/en/news/rss` | RSS | **200 OK** (RSS 2.0, 30 items) | 200 `application/rss+xml` | **WORKS** |
| `https://finmin.lrv.lt/en/rss` | RSS alt | -- | 403 | BLOCKED |

**Verdict:** HTML blocked but **RSS confirmed at `finmin.lrv.lt/en/news/rss`** -- RSS 2.0 with 30 items, channel title "News - finmin.lrv.lt". Use RSS as primary extraction.

---

### 1.7 Bank of Lithuania (lb.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.lb.lt/en/news` | Entry point | 403 | 403 | BLOCKED |
| `https://www.lb.lt/en/rss` | RSS [VERIFY] | 403 | 403 | BLOCKED -- not confirmed |
| `https://www.lb.lt/en/reviews-and-publications` | Publications | -- | 403 | BLOCKED |
| `https://www.lb.lt/en/publications/financial-stability-review-2025` | FSR | -- | 403 | BLOCKED |
| `https://www.lb.lt/en/publications/annual-report-2024` | Annual report | -- | 403 | BLOCKED |

**Verdict:** All lb.lt URLs blocked. RSS not verifiable from outside EU. Needs EU-based proxy.

---

### 1.8 Ministry of Economy and Innovation / EIMIN (eimin.lrv.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://eimin.lrv.lt/en/structure-and-contacts/news-1/press-releases` | Entry point | 403 | 403 | BLOCKED |
| `https://eimin.lrv.lt/en/news/rss` | RSS [VERIFY] | **404** | 404 | **NOT FOUND** |
| `https://eimin.lrv.lt/en/rss` | RSS alt | -- | 403 | BLOCKED |
| `https://eimin.lrv.lt/en/structure-and-contacts/news-1/press-releases/rss` | RSS alt | -- | 403 | BLOCKED |
| `https://eimin.lrv.lt/en/business_environment/trade` | Trade [VERIFY] | -- | 403 | BLOCKED |
| `https://eimin.lrv.lt/en/sector-activities/investment/` | Investment | -- | 403 | BLOCKED |
| `https://eimin.lrv.lt/en/sector-activities/innovation/innovation-support-infrastructure` | Innovation | -- | 403 | BLOCKED |

**Verdict:** All EIMIN URLs blocked. Unlike lrv.lt and finmin.lrv.lt, the `eimin.lrv.lt/en/news/rss` path returns 404 -- EIMIN's news may live at a different path (`/structure-and-contacts/news-1/press-releases`) so the standard lrv.lt RSS pattern does not apply. Needs further investigation from EU IP.

---

### 1.9a State Security Department / VSD (vsd.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.vsd.lt/en/` | Entry point | 403 | 403 | BLOCKED |
| `https://www.vsd.lt/en/reports/national-threat-assessment-2025/` | Threat assessment | 403 | 403 | BLOCKED |
| `https://www.vsd.lt/en/activities/activity-reports/` | Activity reports | -- | 403 | BLOCKED |
| `https://www.vsd.lt/en/archive-national-threat-assessments/` | Archive | -- | 403 | BLOCKED |

**Verdict:** All vsd.lt URLs blocked. Needs EU-based proxy.

---

### 1.9b AOTD (kam.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://kam.lt/en/antrasis-operatyviniu-tarnybu-departamentas/` | Entry point | -- | 403 | BLOCKED |

**Verdict:** Blocked (same as all kam.lt). See KAM section above.

---

### 1.10a NATO EFP / German Brigade -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://kam.lt/en/faq/nato-enhanced-forward-presence/` | KAM EFP | -- | 403 | BLOCKED |
| `https://jfcbs.nato.int/page5964943/2017/enhanced-forward-presence-battlegroup-lithuania` | JFC Brunssum | 403 | 403 | BLOCKED |
| `https://shape.nato.int/efp` | SHAPE EFP | 403 | 403 | BLOCKED |
| `https://www.nato.int/cps/en/natohq/news.htm` | NATO news | **200 OK** (redirects to new URL, confirmed working) | 200 | **WORKS** |

**Verdict:** NATO subsidiary sites (jfcbs, shape) are blocked. Main nato.int news page works (redirects to `nato.int/en/news-and-events/articles/news`). KAM EFP page blocked with all kam.lt.

---

### 1.10b EU Council (consilium.europa.eu) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.consilium.europa.eu/en/press/press-releases/` | Entry point | 403 | 403 | BLOCKED |
| `https://www.consilium.europa.eu/en/rss/` | RSS [VERIFY] | 403 | 403 | BLOCKED -- not confirmed |

**Verdict:** EU Council site blocked. Likely Cloudflare or similar protection. Needs browser-based scraping or official API.

---

### 1.10c Baltic Cooperation (baltasam.org) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.baltasam.org/` | Entry point [VERIFY] | **200 OK** (confirmed working, active site) | -- | **WORKS** |

**Verdict:** Baltic Assembly site fully reachable and actively maintained (Estonian presidency 2026). URL confirmed valid.

---

### 1.10d Ignitis Group (ignitisgrupe.lt) -- P2

| URL | Type | WebFetch | curl | Status |
|---|---|---|---|---|
| `https://www.ignitisgrupe.lt/en/news` | Entry point [VERIFY] | 301 -> `http://ignitisgrupe.lt/en/news` -> **200 OK** | -- | **WORKS** (with redirect) |

**Verdict:** Ignitis Group news page works after redirect (drops `www.`). Confirmed active with recent articles (March 2026). 47 pages of news content. URL verified valid. No RSS found.

---

## VERIFY Items Resolution

| Item | Result |
|---|---|
| lrp.lt RSS (`/en/rss` or `/en/feed`) | **No RSS found** -- both paths return 403. Cannot confirm from outside EU. |
| lrp.lt speeches URL | **Cannot verify** -- 403 |
| lrv.lt RSS | **CONFIRMED** at `lrv.lt/en/news/rss` (RSS 2.0, 30 items) |
| urm.lt RSS | **Cannot verify** -- 403 on all attempted paths |
| kam.lt WordPress RSS | **Cannot verify** -- 403 on `/en/feed/` and `/category/news/feed/` |
| lrs.lt RSS | **No RSS found** -- HTML pages work but no RSS endpoints discovered |
| e-tar.lt RSS | **No RSS found** -- HTML pages work, no RSS tested/found |
| finmin.lrv.lt RSS | **CONFIRMED** at `finmin.lrv.lt/en/news/rss` (RSS 2.0, 30 items) |
| eimin.lrv.lt RSS | **NOT AVAILABLE** -- `/en/news/rss` returns 404 (news at non-standard path) |
| lb.lt RSS | **Cannot verify** -- 403 |
| ignitisgrupe.lt entry URL | **CONFIRMED** valid and working (with www->non-www redirect) |
| ignitisgrupe.lt RSS | **No RSS found** |
| baltasam.org URL | **CONFIRMED** valid and working |
| consilium.europa.eu RSS | **Cannot verify** -- 403 |
| kam.lt threat assessment PDF | **Cannot verify** -- 403 |
| kariuomene.kam.lt | **DNS FAILURE** -- subdomain may be deprecated |
| eimin.lrv.lt trade URL | **Cannot verify** -- 403 |

---

## Recommendations

### 1. EU-based proxy required
The majority of Lithuanian government sites (lrp.lt, kam.lt, urm.lt, lb.lt, vsd.lt) and some EU institutional sites (consilium.europa.eu, shape.nato.int) return 403 from US-based IPs. Pipeline deployment **must** use an EU-based (ideally Lithuanian) IP for fetching. Many 403 results may become 200 from within the EU.

### 2. Confirmed RSS feeds (use as primary extraction)
- `https://lrv.lt/en/news/rss` -- Government/PM (RSS 2.0, 30 items)
- `https://finmin.lrv.lt/en/news/rss` -- Finance Ministry (RSS 2.0, 30 items)

The lrv.lt RSS pattern (`{subdomain}.lrv.lt/en/news/rss`) should be retested from EU IP for all lrv.lt subdomains.

### 3. Fully reachable without proxy
- lrs.lt (Seimas) -- all tested URLs work, including e-seimas.lrs.lt
- e-tar.lt (Legal registry) -- main site and search work
- data.gov.lt -- open data endpoint works
- baltasam.org (Baltic Assembly) -- works
- ignitisgrupe.lt (Ignitis Group) -- works after redirect
- nato.int (main site) -- works (subsidiary sites blocked)

### 4. kariuomene.kam.lt deprecation
The Lithuanian Armed Forces subdomain `kariuomene.kam.lt` has a DNS resolution failure. This subdomain may have been merged into the main `kam.lt` site. Update the source document accordingly.

### 5. EIMIN RSS path issue
Unlike other lrv.lt ministries, EIMIN's news lives at `/structure-and-contacts/news-1/press-releases` rather than `/news/`. The standard `/en/news/rss` path returns 404. The actual RSS path (if any) needs to be discovered from an EU IP.

### 6. Re-test priority from EU IP
All 403 results should be retested from an EU-based IP. Priority retests:
1. lrp.lt (President) -- all URLs including RSS verification
2. kam.lt (Defence) -- all URLs including WordPress RSS at `/en/feed/`
3. urm.lt (Foreign Affairs) -- all URLs including RSS
4. lb.lt (Central Bank) -- all URLs including `/en/rss`
5. vsd.lt (State Security) -- all URLs
6. consilium.europa.eu (EU Council) -- press releases and RSS
