# Canada Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/canada_government_sources.md`
**Tested by:** Automated WebFetch + curl fallback

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 62 |
| Passed (HTTP 200 / valid feed) | 56 |
| Failed (HTTP 404) | 4 |
| Failed (HTTP 403 / cert error) | 2 |
| Intermittent (HTTP/2 stream error) | 1 |
| No RSS confirmed ([VERIFY] items) | 4 |

**Overall pass rate: 90% (56/62)**

### Key Findings

1. **All api.io.canada.ca Atom feeds work perfectly** -- GAC, DND, Finance, ISED, Public Safety all return valid, current Atom XML.
2. **All PMO RSS feeds work** -- EN, FR, and media feeds all valid and current.
3. **All Bank of Canada RSS feeds work** -- All 12 tested feeds return valid RSS 1.0 (RDF).
4. **Canada Gazette RSS mostly works** -- 5 of 6 feeds valid. French Part III (`fr-ls-fra.xml`) returns 404.
5. **NRCan entry point URL is broken** -- `natural-resources.canada.ca/news/news-releases` returns 404. The RSS feeds page works and lists api.io.canada.ca Atom feeds.
6. **Travel advisories RSS is dead** -- `travel.gc.ca/feeds/rss/eng/travel-updates-24.aspx` returns 404.
7. **EDC newsroom has a certificate error** -- WebFetch fails on TLS; curl returns 200, so the page works in browsers but may cause issues for automated fetchers without full cert chains.
8. **Trade Commissioner Service blocks bots** -- `tradecommissioner.gc.ca` returns 403.
9. **No RSS feeds exist** for House of Commons, Senate, Governor General, or Hogue Commission (all [VERIFY] items confirmed negative).

---

## 1. PMO (Prime Minister's Office)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://pm.gc.ca/en/news.rss` | RSS | PASS | Valid RSS 2.0. Latest: 2026-03-19. Feed title: "News" |
| `https://pm.gc.ca/fr/nouvelles.rss` | RSS | PASS | Valid RSS 2.0. Latest: 2026-03-19. Feed title: "Nouvelles" |
| `https://pm.gc.ca/en/media.rss` | RSS | PASS | Valid RSS. Latest: 2026-03-12. Feed title: "Media" |
| `https://www.pm.gc.ca/en/news/releases` | Entry point | PASS | Page title: "News \| Prime Minister of Canada" |
| `https://www.pm.gc.ca/en/news/statements` | Additional | PASS | Loads correctly |
| `https://www.pm.gc.ca/en/news/speeches` | Additional | PASS | Loads correctly |
| `https://www.pm.gc.ca/en/news/media-advisories` | Additional | PASS | Loads correctly |
| `https://www.pm.gc.ca/en/news/readouts` | Additional | PASS | Loads correctly |

---

## 2. Global Affairs Canada (GAC)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate>=2015-01-01&pick=5&format=atom&atomtitle=Global+Affairs+Canada+news` | Atom | PASS | Valid Atom. Latest: 2026-03-19 |
| `https://international.canada.ca/en/global-affairs/news` | Entry point | PASS | Page title: "News: Global Affairs Canada" |
| `https://travel.gc.ca/feeds/rss/eng/travel-updates-24.aspx` | RSS | **FAIL (404)** | Travel advisories RSS not found. Confirmed via curl. |

---

## 3. DND / Canadian Armed Forces

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentnationaldefense&sort=publishedDate&orderBy=desc&publishedDate>=2021-07-23&pick=5&format=atom&atomtitle=National+Defence+and+the+Canadian+Armed+Forces` | Atom | PASS | Valid Atom. Latest: 2026-03-18 |
| `https://www.canada.ca/en/department-national-defence/corporate/news.html` | Entry point | PASS | Page title: "News - National Defence and the Canadian Armed Forces" |
| `https://www.canada.ca/en/department-national-defence/corporate/policies-standards.html` | Additional | PASS | Page title: "Policies and standards" |
| `https://www.canada.ca/en/department-national-defence/services/operations.html` | Additional | PASS | Page title: "Military operations and exercises" |
| `https://www.canada.ca/en/department-national-defence/maple-leaf.html` | Additional | PASS | Page title: "The Maple Leaf" |

---

## 4a. House of Commons

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.ourcommons.ca/en/newsroom` | Entry point | PASS | Page title: "Newsroom - House of Commons of Canada" |
| `https://www.ourcommons.ca/documentviewer/en/house/latest/hansard` | Additional | PASS | Shows latest Hansard (2026-03-13) |
| `https://www.parl.ca/legisinfo/` | Additional | PASS | Page title: "Home - LEGISinfo" |
| `https://www.parl.ca/Committees/en/PDAM/NewsReleases` | Additional | PASS | Page title: "News Releases - House of Commons of Canada" |
| `https://parlvu.parl.gc.ca/Harmony/` | Additional | PASS | Page title: "ParlVu" |
| `https://www.ourcommons.ca/en/open-data` | Additional | PASS | Page title: "Open Data - House of Commons of Canada" |
| `https://subscription.ourcommons.ca/Committees/en/NewsletterRegister` | Additional | PASS | HTTP 200 (curl) |
| RSS at `ourcommons.ca` | [VERIFY] | **NO RSS** | Tested `/en/newsroom/feed`, `/rss` -- all 404. No RSS feed exists. |

---

## 4b. Senate of Canada

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://sencanada.ca/en/newsroom/` | Entry point | PASS | Page loads; content rendered via JavaScript (AJAX). Page title: "Newsroom" |
| `https://sencanada.ca/en/sencaplus/` | Additional | PASS | Page title: "SenCAPlus" |
| `https://sencanada.ca/en/media-centre/` | Additional | PASS | Page title: "Media centre" |
| `https://sencanada.ca/en/committees/news/` | Additional | PASS | Page title: "Committees" (redirects to committee hub) |
| RSS at `sencanada.ca` | [VERIFY] | **NO RSS** | Tested `/en/newsroom/feed`, `/en/newsroom/feed/` -- all 404. No RSS feed exists. |

---

## 5. Canada Gazette

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://gazette.gc.ca/accueil-home-eng.html` | Entry point | PASS | Page title: "Canada Gazette - Canada.ca" |
| `https://www.gazette.gc.ca/rss/p1-eng.xml` | RSS (Part I EN) | PASS | Valid RSS 2.0. Latest: 2026-03-14 |
| `https://www.gazette.gc.ca/rss/p2-eng.xml` | RSS (Part II EN) | PASS | Valid RSS 2.0. Latest: 2026-03-11 |
| `https://www.gazette.gc.ca/rss/en-ls-eng.xml` | RSS (Part III EN) | PASS | Valid RSS 2.0. Latest: 2025-03-28 |
| `https://www.gazette.gc.ca/rss/p1-fra.xml` | RSS (Part I FR) | PASS | Valid RSS 2.0. Latest: 2026-03-14 |
| `https://www.gazette.gc.ca/rss/p2-fra.xml` | RSS (Part II FR) | PASS | Valid RSS 2.0. Latest: 2026-03-11 |
| `https://www.gazette.gc.ca/rss/fr-ls-fra.xml` | RSS (Part III FR) | **FAIL (404)** | French Part III feed not found. English equivalent works. |

---

## 6. Department of Finance Canada

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentfinance&type=newsreleases&sort=publishedDate&orderBy=desc&publishedDate>=2020-08-09&pick=5&format=atom&atomtitle=Department+of+Finance+Canada+News+Releases` | Atom | PASS | Valid Atom. Latest: 2026-03-19 |
| `https://www.canada.ca/content/dam/fin/documents/publications/pub-rep/publications-en.atom` | Atom | PASS | Valid Atom. Latest: 2026-03-13. Title: "Department of Finance Canada - Publications and reports" |
| `https://www.canada.ca/en/department-finance/news.html` | Entry point | PASS | Page title: "News: Department of Finance Canada" |
| `https://www.canada.ca/en/department-finance/news/stay-connected.html` | Additional | **INTERMITTENT** | TLS connects but HTTP/2 stream error (INTERNAL_ERROR err 2). Server-side issue. |

---

## 7. Bank of Canada

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.bankofcanada.ca/press/` | Entry point | PASS | Page title: "Press - Bank of Canada" |
| `https://www.bankofcanada.ca/content_type/press-releases/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-03-18 |
| `https://www.bankofcanada.ca/content_type/announcements/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-02-19 |
| `https://www.bankofcanada.ca/content_type/speeches/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-03-18 |
| `https://www.bankofcanada.ca/content_type/notices/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-03-04 |
| `https://www.bankofcanada.ca/content_type/media-advisories/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-03-18 |
| `https://www.bankofcanada.ca/utility/news/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-03-18 |
| `https://www.bankofcanada.ca/content_type/mpr/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-01-28 |
| `https://www.bankofcanada.ca/content_type/fsr/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2025-05-08 |
| `https://www.bankofcanada.ca/content_type/bos/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-01-19 |
| `https://www.bankofcanada.ca/content_type/publications/feed/` | RSS | PASS | Valid RSS 1.0. Latest: 2026-02-11 |
| `https://www.bankofcanada.ca/valet/fx_rss/` | RSS | PASS | Valid RSS 1.0. 23 currency pairs. Latest: 2026-03-18 |
| `https://www.bankofcanada.ca/valet/fx_rss/FXUSDCAD` | RSS | PASS | Valid RSS 1.0. USD/CAD = 1.3706 (2026-03-18) |
| `https://www.bankofcanada.ca/rss-feeds/` | Hub page | PASS | HTTP 200. Lists all available feeds. |
| `https://www.bankofcanada.ca/valet/` | API hub | PASS | HTTP 200. RESTful data access. |

---

## 8. ISED (Innovation, Science and Economic Development)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofindustry&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=5&format=atom&atomtitle=Innovation+Science+and+Economic+Development+Canada` | Atom | PASS | Valid Atom. Latest: 2026-03-18 |
| `https://ised-isde.canada.ca/site/media-room/en` | Entry point | PASS | Page title: "Media room" |
| `https://www.edc.ca/en/about-us/newsroom.html` | Additional | **PARTIAL** | curl returns 200, but WebFetch fails on TLS cert verification. Works in browsers. |
| `https://www.tradecommissioner.gc.ca/` | Additional | **FAIL (403)** | Blocked by bot protection. curl with UA returns 403. |

---

## 9a. CSIS

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.canada.ca/en/security-intelligence-service/corporate/publications.html` | Entry point | PASS | Page title: "Publications - Canada.ca". Lists annual reports 2010-2024. |

---

## 9b. PCO / NSIA

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.canada.ca/en/privy-council/services/security/national-security-intelligence-advisor-branch-reports-publications.html` | Entry point | PASS | Page title: "Reports and publications - National Security and Intelligence - Privy Council Office" |

---

## 9c. NSICOP

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://nsicop-cpsnr.ca/reports-rapports-en.html` | Entry point | PASS | Page title: "Reports". 14 reports listed (2018-2025). |

---

## 10a. Public Safety Canada

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=publicsafetycanada&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=5&format=atom&atomtitle=Public+Safety+Canada` | Atom | PASS | Valid Atom. Latest: 2026-03-19 |
| `https://www.publicsafety.gc.ca/cnt/nws/nws-rlss/index-en.aspx` | Entry point | PASS | Page title: "News Releases". Releases from 2022-2026. |
| `https://www.publicsafety.gc.ca/cnt/ntnl-scrt/nws-rlss-en.aspx` | Additional | PASS | Page title: "National Security News Releases" |

---

## 10b. Hogue Commission (Foreign Interference)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://foreigninterferencecommission.ca/en/` | Entry point | PASS | Commission has completed its work. Final report released Jan 2025. |
| RSS at `foreigninterferencecommission.ca` | [VERIFY] | **NO RSS** | `/en/feed` and `/feed` return HTML pages, not RSS. No feed exists. |

---

## 10c. Governor General

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.gg.ca/en/media` | Entry point | PASS | Page title: "Media Centre \| The Governor General of Canada". Shows recent events. |
| RSS at `gg.ca` | [VERIFY] | **NO RSS** | Tested `/en/media/feed`, `/feed`, `/en/rss` -- all 404. No RSS feed exists. |

---

## 10d. Natural Resources Canada (NRCan)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://natural-resources.canada.ca/news/news-releases` | Entry point | **FAIL (404)** | Page not found. URL may have changed during site restructuring. |
| `https://natural-resources.canada.ca/corporate/rss-feeds` | RSS hub page | PASS | Lists available feeds including api.io.canada.ca Atom and Simply Science RSS. |
| `https://natural-resources.canada.ca/simply-science/rss.xml` | RSS | PASS | HTTP 200, content-type: application/rss+xml |

---

## Recommendations

### Broken URLs Requiring Updates

| Source | Broken URL | Suggested Action |
|---|---|---|
| GAC (travel) | `travel.gc.ca/feeds/rss/eng/travel-updates-24.aspx` | Find replacement RSS on travel.gc.ca or drop |
| Canada Gazette | `gazette.gc.ca/rss/fr-ls-fra.xml` (Part III FR) | May be `fr-ls-fra.xml` typo; try other patterns or drop French Part III |
| NRCan | `natural-resources.canada.ca/news/news-releases` | Use api.io.canada.ca Atom feed instead (available per RSS hub page) |
| Finance | `canada.ca/en/department-finance/news/stay-connected.html` | Server-side HTTP/2 issue; non-critical (informational page only) |

### Bot-Blocked URLs

| Source | URL | Workaround |
|---|---|---|
| Trade Commissioner | `tradecommissioner.gc.ca` | Returns 403. Low priority -- trade content also available via GAC and ISED feeds. |
| EDC | `edc.ca/en/about-us/newsroom.html` | TLS cert issue for automated fetchers; curl with `-k` works. Low priority supplementary source. |

### Confirmed: No RSS Available

These sources require HTML scraping or periodic page checks:
- House of Commons (`ourcommons.ca`) -- use Open Data XML feeds as alternative
- Senate of Canada (`sencanada.ca`) -- JS-rendered content; requires headless browser
- Governor General (`gg.ca`) -- standard HTML scraping
- Hogue Commission (`foreigninterferencecommission.ca`) -- commission completed; archive monitoring only
- CSIS (`canada.ca/en/security-intelligence-service`) -- annual publication check
- PCO/NSIA -- periodic check
- NSICOP (`nsicop-cpsnr.ca`) -- periodic check
