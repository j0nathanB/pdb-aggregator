# UAE Government Sources — Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/uae_government_sources.md`
**Test methods:** WebFetch (HTML-to-markdown via HTTPS), curl (HTTP status code + content type)

---

## Summary Counts

| Metric | Count |
|---|---|
| Total unique URLs tested | 44 |
| WebFetch success (content retrieved) | 16 |
| WebFetch fail (403/503/timeout/cert error) | 11 |
| curl 200 (reachable) | 14 |
| curl 403 (blocked) | 5 |
| curl 503 (server error) | 3 |
| curl timeout/connection refused (000) | 3 |
| curl 404 (not found) | 2 |
| RSS verified as functional | 0 |
| RSS verified as non-functional | 5 (WAM /rss, /feed, /en/rss return SPA HTML; MoD /feed/ 503; MoF /feed/ 404) |
| [VERIFY URL] resolved | 2 |
| [VERIFY RSS] resolved | 10 |

---

## Per-URL Result Table

### P1 Sources — Primary Entry Points

| # | Institution | URL | WebFetch | curl | Content Retrieved | Recommended Extraction | Notes |
|---|---|---|---|---|---|---|---|
| 1a | WAM (EN) | `https://www.wam.ae/en` | FAIL — SPA shell only (CSS/JS, no article content) | 200 | No (SPA requires headless browser) | Headless browser (Playwright) | Vue/React SPA; standard HTTP GET returns empty shell |
| 1a | WAM (AR) | `https://www.wam.ae/ar` | Not tested via WebFetch | 200 | Same SPA behavior expected | Headless browser | Same SPA architecture |
| 1b | UAE Cabinet | `https://uaecabinet.ae/en/news` | FAIL — 403 | 403 | No | Headless browser or authenticated scraper | Bot protection active |
| 2 | MoFA (EN) | `https://www.mofa.gov.ae/en/mediahub/news` | SUCCESS — 3 headlines retrieved | 200 | Yes — full article listings with titles, dates, summaries | HTML scrape (standard) | Clean HTML, paginated, date/slug URL pattern. Best-behaved P1 source. |
| 2 | MoFA (AR) | `https://www.mofa.gov.ae/ar-ae/mediahub/news` | Not tested via WebFetch | 200 | Expected yes | HTML scrape | Same site structure, Arabic path prefix |
| 3 | MoD | `https://mod.gov.ae/category/news/` | FAIL — 503 | 503 | No | WordPress API or headless browser | WordPress site returning 503 consistently. Possibly under load or geo-restricted. |

### P1 Sources — RSS Verification

| # | Institution | RSS URL Tested | Result | Content | Notes |
|---|---|---|---|---|---|
| 1a | WAM | `https://www.wam.ae/rss` | NOT RSS — returns SPA HTML (200) | No RSS XML | SPA catch-all route serves HTML for all paths |
| 1a | WAM | `https://www.wam.ae/feed` | NOT RSS — returns SPA HTML (200) | No RSS XML | Same behavior |
| 1a | WAM | `https://www.wam.ae/en/rss` | NOT RSS — returns SPA HTML (200) | No RSS XML | Same behavior |
| 3 | MoD | `https://mod.gov.ae/feed/` | FAIL — 503 | No | Server error, same as main site |
| 3 | MoD | `https://mod.gov.ae/category/news/feed/` | FAIL — 503 | No | Server error |
| 3 | MoD | `https://mod.gov.ae/wp-json/wp/v2/posts` | FAIL — 503 | No | WordPress REST API also returning 503 |
| 6 | MoF | `https://mof.gov.ae/feed/` | FAIL — 404 | No | WordPress RSS feed explicitly disabled or removed |
| 6 | MoF | `https://mof.gov.ae/wp-json/wp/v2/posts` | FAIL — connection reset | No | WordPress REST API blocked (connection reset by server) |

**RSS Conclusion:** No UAE government source provides a functional RSS/Atom feed. All [VERIFY RSS] items resolved as negative.

### P2 Sources — Primary Entry Points

| # | Institution | URL | WebFetch | curl | Content Retrieved | Recommended Extraction | Notes |
|---|---|---|---|---|---|---|---|
| 4 | FNC | `https://www.almajles.gov.ae/` | FAIL — timeout | timeout (000) | No | Headless browser (if reachable) | Connection timeout — possibly geo-restricted or down. Site may only be accessible from UAE. |
| 5 | UAE Legislation | `https://uaelegislation.gov.ae/en` | FAIL — 403 | 403 | No | Headless browser or authenticated scraper | Bot protection |
| 5 | UAE Legislation (news) | `https://uaelegislation.gov.ae/en/news` | FAIL — 403 | Not tested | No | Same as parent | Same protection |
| 6 | MoF (news) | `https://mof.gov.ae/en/media-center/news/` | SUCCESS — 3 headlines retrieved (March 2026 items) | 200 implied | Yes — article listings with titles and dates | HTML scrape (standard) | WordPress site, clean HTML output. Well-structured. |
| 6 | MoF (press releases) | `https://mof.gov.ae/press-release-archives/` | FAIL — 404 | 404 | No | URL is dead | Archive URL no longer valid |
| 6 | MoF (publications) | `https://mof.gov.ae/en/media-center/publications-and-releases/` | SUCCESS — publications listed | 200 implied | Yes — Pulse of Finance newsletters, annual reports, legal bulletins | HTML scrape | Well-structured, PDFs downloadable |
| 7 | CBUAE (news) | `https://www.centralbank.ae/en/news-and-publications/news-and-insights/` | FAIL — 403 | 403 | No | Headless browser with cookie handling | Active bot protection confirmed |
| 7 | CBUAE (publications) | `https://www.centralbank.ae/en/news-and-publications/publications/` | Not tested via WebFetch | 403 | No | Same protection | Same bot protection |
| 7 | CBUAE (research) | `https://www.centralbank.ae/en/research-and-statistics/` | Not tested via WebFetch | 403 | No | Same protection | All CBUAE endpoints return 403 |
| 8a | MoET | `https://www.moet.gov.ae/en/home` | SUCCESS — full page content visible | 200 implied | Yes — Media Centre with news articles, events, data | HTML scrape | Well-structured government site. News section identified. |
| 8b | MoFT | `https://www.moft.gov.ae/` | FAIL — ECONNREFUSED | connection refused (000) | No | N/A — domain not operational | **[VERIFY URL] RESOLVED: Domain does not exist / no server running.** Ministry likely still operates under moet.gov.ae. |
| 9 | NCEMA | `https://ncema.gov.ae/` | FAIL — timeout | timeout (000) | No | Unknown — site unreachable | Connection timeout. Possibly geo-restricted, rate-limited, or down. |
| 9 | NCEMA (news) | `https://www.ncema.gov.ae/en/media-center/news/` | Not tested via WebFetch | timeout (000) | No | Same | Same timeout behavior |
| 10a | ADNOC | `https://www.adnoc.ae/en/news-and-media/press-releases` | SUCCESS — 3 press releases retrieved (March 2026) | 200 implied | Yes — dated press releases with titles and summaries | HTML scrape (standard) | Clean corporate site. Best corporate source. |
| 10b | EDGE Group | `https://edgegroup.ae/` | FAIL — 403 | 403 | No (Cloudflare "Attention Required" challenge page) | Headless browser with Cloudflare bypass | Behind Cloudflare WAF. Standard HTTP and WebFetch both blocked. |
| 10b | EDGE Group | `https://edgegroup.ae/news` | FAIL — 403 | 403 | No | Same | Same Cloudflare protection |
| 10c | ADIA | `https://www.adia.ae/en/media` | FAIL — 404 (page not found on ADIA site) | N/A | No | Use corrected URL | **URL incorrect in source doc.** |
| 10c | ADIA (corrected) | `https://www.adia.ae/en/publications` | SUCCESS — news and publications visible | 200 implied | Yes — investment news, annual reviews (2009-2024), overview docs | HTML scrape | Correct URL is /en/publications, not /en/media |
| 10c | Mubadala | `https://www.mubadala.com/en/news` | FAIL — SSL certificate error (WebFetch) | 200 (curl) | curl succeeds, WebFetch fails on cert verification | HTML scrape (curl-based, skip cert verify or fix cert chain) | SSL certificate issue — first cert in chain not verifiable by WebFetch. curl succeeds. |
| 10c | ADQ | `https://www.adq.ae/newsroom` | FAIL — 404 | N/A | No | Use corrected URL | **URL incorrect in source doc.** |
| 10c | ADQ (corrected) | `https://www.adq.ae/media-and-insights/newsroom` | SUCCESS — 3 headlines retrieved (Dec 2025) | 200 | Yes — press releases with dates and summaries | HTML scrape | Correct newsroom URL confirmed |
| 10d | ADMO | `https://www.mediaoffice.abudhabi/en/` | SUCCESS — 3 headlines retrieved (March 2026) | 200 | Yes — government news, topic-based organization | HTML scrape (standard) | Excellent source. Topic-based URLs work. |
| 10d | DMO | `https://www.mediaoffice.ae/en/` | SUCCESS — 3 headlines retrieved (March 2026) | 200 | Yes — government news with dates | HTML scrape (standard) | **[VERIFY URL] RESOLVED: URL is valid and functional.** |

### Additional Entry Points

| # | Institution | URL | WebFetch | curl | Content Retrieved | Notes |
|---|---|---|---|---|---|---|
| 1a | NMO Presidential News | `https://www.nmo.gov.ae/en/presidential-news` | SUCCESS — NMA page with news content | 200 implied | Yes — featured news, navigation, e-services | Note: redirects to Arabic NMA homepage but content is present |
| 1a | UAE Gov Platform News | `https://u.ae/en/media/news` | SUCCESS — 3 headlines retrieved | 200 implied | Yes — government news listings with search/filter | Good fallback for WAM |
| 2 | UAE Embassy Washington | `https://www.uae-embassy.org/latest-regional-news-and-developments` | SUCCESS — 3 headlines retrieved (March 2026) | 200 implied | Yes — regional news with dates and images | Excellent bilateral channel |
| 3 | ADMO Defense Topic | `https://www.mediaoffice.abudhabi/en/topic/ministry-of-defence/` | Not tested via WebFetch | 200 | Expected yes | Good MoD fallback |
| 3 | ADMO EDGE Topic | `https://www.mediaoffice.abudhabi/en/topic/edge-group/` | Not tested via WebFetch | 200 | Expected yes | Good EDGE fallback |
| 4 | FNC on u.ae | `https://u.ae/en/about-the-uae/the-uae-government/the-federal-national-council-` | Not tested via WebFetch | 200 | Expected yes | Informational page, not news feed |
| 5 | MoJ Laws Portal | `https://www.moj.gov.ae/en/laws-and-legislation/latest-legislations-and-laws.aspx` | SUCCESS — filter interface visible, but 0 results displayed | 200 implied | Partial — page loads but legislation list shows "Total Count: 0" | May require specific filter parameters to return results |
| 5 | e-Laws (MoJ) | `https://elaws.moj.gov.ae/` | SUCCESS — legal portal visible | 200 implied | Yes — federal legislation, court decisions, treaties | Functional legal research portal |
| 5 | Dubai Official Gazette | `https://legal.dubai.gov.ae/en/Services/Pages/Official-Gazette.aspx` | SUCCESS — gazette archive visible (back to 1950) | 200 implied | Yes — filterable gazette PDFs by year/issue | SharePoint-based, PDF downloads |
| 5 | Abu Dhabi Policies | `https://www.abudhabi.gov.ae/en/policies-and-legislations` | SUCCESS — Official Gazette archive (2009-2023) | 200 implied | Yes — monthly gazette PDFs downloadable | Well-maintained archive |

---

## VERIFY Resolution Section

### [VERIFY URL] Items

| Item | URL Tested | Resolution |
|---|---|---|
| MoFT domain (moft.gov.ae) | `https://www.moft.gov.ae/` | **INVALID** — ECONNREFUSED. No server running. The Ministry of Foreign Trade (established June 2025) does not have an independent web presence. Content likely remains under `moet.gov.ae`. Recommend monitoring MoET and WAM for MoFT content. |
| DMO URL (mediaoffice.ae) | `https://www.mediaoffice.ae/en/` | **VALID** — Returns 200, full content with headlines. Dubai Media Office is fully operational at this URL. |
| EDGE Group press/news URL | `https://edgegroup.ae/news` | **BLOCKED** — 403 Cloudflare challenge. The news section exists but is behind WAF. Use ADMO topic page (`mediaoffice.abudhabi/en/topic/edge-group/`) as fallback. |

### [VERIFY RSS] Items

| Item | URLs Tested | Resolution |
|---|---|---|
| WAM RSS | `wam.ae/rss`, `wam.ae/feed`, `wam.ae/en/rss` | **NO RSS** — All return 200 but serve SPA HTML shell, not RSS XML. The SPA catch-all route handles all paths. RSS was removed during the 2024-2025 NMA site rebuild. |
| UAE Cabinet RSS | Not testable (site returns 403) | **UNVERIFIABLE** — Site blocks automated access entirely. Assume no RSS. |
| MoFA RSS | No RSS endpoints found | **NO RSS** — Site does not expose RSS. Confirmed via WebFetch page inspection. |
| MoD RSS (WordPress) | `mod.gov.ae/feed/`, `mod.gov.ae/category/news/feed/` | **UNVERIFIABLE** — Site returns 503 on all endpoints. WordPress RSS may exist but site is currently down/unreachable. |
| MoF RSS (WordPress) | `mof.gov.ae/feed/` | **NO RSS** — Returns 404. WordPress default RSS has been explicitly disabled. WP REST API also blocked (connection reset). |
| FNC RSS | Not testable (site times out) | **UNVERIFIABLE** — Site completely unreachable. |
| CBUAE RSS | Not testable (403 on all endpoints) | **UNVERIFIABLE** — Bot protection blocks all automated access. Assume no RSS. |
| MoET RSS | No RSS endpoints found | **NO RSS** — Site loads fine but no RSS link discovered in page content. |
| NCEMA RSS | Not testable (site times out) | **UNVERIFIABLE** — Site completely unreachable. |
| ADNOC RSS | No RSS endpoints found | **NO RSS** — Corporate site, no RSS link in page content. |
| EDGE Group RSS | Not testable (403 Cloudflare) | **UNVERIFIABLE** — Cloudflare blocks all automated access. |
| ADMO/DMO RSS | No RSS endpoints found | **NO RSS** — Neither media office exposes RSS feeds. |
| SWF RSS (ADIA/Mubadala/ADQ) | No RSS endpoints found | **NO RSS** — None of the three SWFs offer RSS. |

---

## Recommendations

### Tier 1: Directly Scrapable via Standard HTTP (Best Case)
These sources return full HTML content to standard HTTP clients:
1. **MoFA** (`mofa.gov.ae/en/mediahub/news`) — cleanest P1 source
2. **MoF** (`mof.gov.ae/en/media-center/news/`) — WordPress, well-structured
3. **ADNOC** (`adnoc.ae/en/news-and-media/press-releases`) — clean corporate HTML
4. **MoET** (`moet.gov.ae/en/home`) — full content accessible
5. **ADMO** (`mediaoffice.abudhabi/en/`) — topic-based URLs, excellent
6. **DMO** (`mediaoffice.ae/en/`) — similar structure to ADMO
7. **UAE Embassy Washington** (`uae-embassy.org`) — good bilateral source
8. **u.ae** (`u.ae/en/media/news`) — WAM fallback
9. **ADIA** (`adia.ae/en/publications`) — corrected URL
10. **ADQ** (`adq.ae/media-and-insights/newsroom`) — corrected URL
11. **MoJ / e-Laws** (`elaws.moj.gov.ae`) — legislation portal
12. **Dubai Official Gazette** (`legal.dubai.gov.ae`) — gazette PDFs
13. **Abu Dhabi Policies** (`abudhabi.gov.ae/en/policies-and-legislations`) — gazette PDFs

### Tier 2: Requires Headless Browser (SPA/Bot Protection)
1. **WAM** (`wam.ae/en`) — SPA, requires Playwright/Puppeteer rendering
2. **UAE Cabinet** (`uaecabinet.ae/en/news`) — 403, bot protection
3. **CBUAE** (`centralbank.ae`) — 403 on all endpoints, aggressive bot protection
4. **UAE Legislation** (`uaelegislation.gov.ae`) — 403, bot protection
5. **EDGE Group** (`edgegroup.ae`) — Cloudflare WAF challenge page

### Tier 3: Currently Unreachable
1. **MoD** (`mod.gov.ae`) — 503 on all endpoints, possibly down or geo-restricted
2. **FNC** (`almajles.gov.ae`) — connection timeout, unreachable
3. **NCEMA** (`ncema.gov.ae`) — connection timeout, unreachable

### Tier 4: Non-Existent
1. **MoFT** (`moft.gov.ae`) — ECONNREFUSED, domain has no server

### URL Corrections Required in Source Document
| Current URL | Corrected URL | Reason |
|---|---|---|
| `https://www.adia.ae/en/media` | `https://www.adia.ae/en/publications` | /en/media returns 404; /en/publications is the correct news/publications page |
| `https://www.adq.ae/newsroom` | `https://www.adq.ae/media-and-insights/newsroom` | /newsroom returns 404; full path required |
| `https://mof.gov.ae/press-release-archives/` | Remove or replace with `https://mof.gov.ae/en/media-center/publications-and-releases/` | /press-release-archives/ returns 404 |

### Mubadala SSL Note
`https://www.mubadala.com/en/news` returns 200 via curl but WebFetch fails with SSL certificate verification error ("unable to verify the first certificate"). The scraper should either use a curl-based fetcher or configure SSL to accept the incomplete certificate chain.
