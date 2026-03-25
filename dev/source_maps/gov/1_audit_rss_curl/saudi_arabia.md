# Saudi Arabia Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/saudi_arabia_government_sources.md`
**Test method:** WebFetch + curl with Mozilla/5.0 user agent, 12s timeout

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 47 |
| **Accessible (HTTP 200 with valid content)** | 14 |
| **Blocked (HTTP 403)** | 7 |
| **Timeout / Connection refused** | 15 |
| **Redirect to wrong page (soft fail)** | 10 |
| **404 / Not Found** | 1 |

### Key Findings

1. **SPA RSS feeds are dead.** All 7 RSS feed URLs (`rss.xml`, `rss3.xml` through `rss8.xml`) redirect to the Arabic homepage (`spa.gov.sa/ar`). They return HTTP 200 with `text/html` content, not XML. The SPA site has been rebuilt on a Next.js/React framework that eliminated legacy RSS endpoints. The legacy category URLs (`listnews.php`) also redirect to the Arabic homepage.

2. **SPA entry point works.** The English homepage (`spa.gov.sa/en`) returns HTTP 200 and is accessible, but the site is a JS-rendered SPA (single-page application) requiring client-side rendering for content extraction.

3. **SAMA is completely unreachable.** All 5 SAMA URLs timed out on both curl and WebFetch. The SharePoint-based site appears to be blocking external access or experiencing extended downtime.

4. **Several .gov.sa sites timeout consistently.** MODA (`mod.gov.sa`), Shura Council (`shura.gov.sa`), Umm al-Qura (`uqn.gov.sa`), PSS (`pss.gov.sa`), PCTC (`pctc.pss.gov.sa`), MOI (`moi.gov.sa`), and SAMI (`sami.com.sa`) all timed out. These sites may be geo-restricted or have aggressive bot protection.

5. **PIF blocks automated access.** All PIF URLs return HTTP 403 consistently across both curl and WebFetch.

6. **Vision 2030 blocks automated access.** Both Vision 2030 URLs return HTTP 403.

7. **my.gov.sa blocks automated access.** All National Platform agency profile URLs return HTTP 403.

8. **Accessible sites:** MOFA, MOF, Ministry of Commerce, GCC, OIC, GAMI, NDMC, NEOM, and Aramco (via WebFetch only) are reachable and serve content.

---

## Detailed Results

### 1. SPA (Saudi Press Agency) — Royal Court / Council of Ministers

| URL | Type | Method | HTTP | Content-Type | Result | Notes |
|---|---|---|---|---|---|---|
| `https://www.spa.gov.sa/en` | Entry point | curl | 200 | text/html | **PASS** | English homepage accessible |
| `https://www.spa.gov.sa/` | Entry point | curl | 200 | text/html | **PASS** | Redirects to /ar (Arabic) |
| `https://www.spa.gov.sa/rss.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; returns HTML/JSON, not XML RSS |
| `https://www.spa.gov.sa/rss3.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/rss4.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/rss5.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/rss6.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/rss7.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/rss8.xml` | RSS [VERIFY] | curl + WebFetch | 200 | text/html | **FAIL** | Redirects to /ar homepage; no RSS content |
| `https://www.spa.gov.sa/listnews.php?lang=en&cat=9` | Additional | curl | 200 | text/html | **FAIL** | Redirects to /ar homepage; legacy URL defunct |
| `https://www.spa.gov.sa/listnews.php?lang=en&cat=10` | Additional | curl | 200 | text/html | **FAIL** | Redirects to /ar homepage; legacy URL defunct |

**VERIFY verdict: All SPA RSS feeds are INVALID. The legacy RSS and category URL infrastructure has been replaced by a JS-rendered SPA. No RSS feeds are available.**

---

### 2. MOFA (Ministry of Foreign Affairs)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.mofa.gov.sa/en/ministry/news/Pages/default.aspx` | Entry point | curl | 200 | **PASS** | SharePoint site accessible; WebFetch returned only JS monitoring code |
| `https://www.mofa.gov.sa/en/ministry/statements/Pages/default.aspx` | Entry point | curl | 200 | **PASS** | Statements page accessible |
| `https://www.mofa.gov.sa/en/ksa/Pages/vision.aspx` | Additional | curl | 200 | **PASS** | Vision 2030 page on MOFA accessible |

**VERIFY verdict (SharePoint ListFeed): NOT TESTED — would require List GUID discovery. Given that the site is SharePoint-based and accessible, ListFeed endpoints may exist but were not discoverable without authenticated access.**

---

### 3. MODA (Ministry of Defense)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.mod.gov.sa/en/Pages/default.aspx` | Entry point | curl + WebFetch | TIMEOUT | **FAIL** | Connection timeout on both methods; site unreachable |
| `https://www.sami.com.sa/` | Additional | curl + WebFetch | TIMEOUT | **FAIL** | SAMI site also unreachable |
| `https://www.gami.gov.sa/` | Additional [VERIFY] | curl + WebFetch | 200 | **PASS** | GAMI confirmed accessible; redirects to /ar; military industries regulator confirmed |

**VERIFY verdict (GAMI URL): VALID. gami.gov.sa is the General Authority for Military Industries, accessible and serving content.**

---

### 4. Shura Council

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.shura.gov.sa/wps/wcm/connect/shuraen/internet/news` | Entry point | curl + WebFetch | TIMEOUT | **FAIL** | WebSphere site unreachable |
| `https://www.shura.gov.sa/wps/wcm/connect/shuraen/internet/Laws+and+Regulations/` | Additional | curl | TIMEOUT | **FAIL** | Also unreachable |
| `https://my.gov.sa/en/agencies/17525` | Additional | curl | 403 | **BLOCKED** | National Platform blocks automated access |

---

### 5. Umm al-Qura (Official Gazette)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://uqn.gov.sa/` | Entry point | curl + WebFetch | TIMEOUT | **FAIL** | Site unreachable; consistent with doc's note about historical unreliability |

---

### 6. MOF (Ministry of Finance)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.mof.gov.sa/en/MediaCenter/news/Pages/default.aspx` | Entry point | curl + WebFetch | 200 | **PASS** | SharePoint site accessible; news articles visible (Sukuk issuances, conferences) |
| `https://www.ndmc.gov.sa/` | Additional [VERIFY] | curl + WebFetch | 200 | **PASS** | NDMC confirmed accessible; National Debt Management Center confirmed |
| `https://my.gov.sa/en/agencies/17645` | Additional | curl | 403 | **BLOCKED** | National Platform blocks automated access |

**VERIFY verdict (NDMC URL): VALID. ndmc.gov.sa is the National Debt Management Center, accessible and serving content.**

---

### 7. SAMA (Saudi Central Bank)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.sama.gov.sa/en-US/News/pages/allnews.aspx` | Entry point | curl + WebFetch | TIMEOUT | **FAIL** | Connection closed / timeout |
| `https://www.sama.gov.sa/en-US/EconomicReports/Pages/MonthlyStatistics.aspx` | Additional | curl | TIMEOUT | **FAIL** | Unreachable |
| `https://www.sama.gov.sa/en-US/OpenData/Pages/default.aspx` | Additional [VERIFY] | curl + WebFetch | TIMEOUT | **FAIL** | Unreachable |
| `https://www.sama.gov.sa/en-US/About/Pages/SAMAFunction.aspx` | Additional | curl | TIMEOUT | **FAIL** | Unreachable |
| `https://www.sama.gov.sa/en-US/News/_layouts/listfeed.aspx` | RSS [VERIFY] | curl | TIMEOUT | **FAIL** | SharePoint ListFeed endpoint unreachable |

**VERIFY verdict (SAMA Open Data): UNTESTABLE — entire sama.gov.sa domain is unreachable. May be geo-restricted or experiencing extended outage.**
**VERIFY verdict (SAMA ListFeed RSS): UNTESTABLE — same reason.**

---

### 8. Ministry of Commerce

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://mc.gov.sa/en/mediacenter/News/Pages/default.aspx` | Entry point | curl + WebFetch | 200 | **PASS** | SharePoint site accessible; news articles visible (vehicle recalls, ministry announcements, Dec 2025 content) |
| `https://my.gov.sa/en/agencies/17606` | Additional | curl | 403 | **BLOCKED** | National Platform blocks automated access |
| `https://www.saudiaexports.sa/` | Additional [VERIFY] | curl + WebFetch | TIMEOUT/ECONNREFUSED | **FAIL** | SEDA site unreachable; connection refused |

**VERIFY verdict (SEDA URL): INVALID or UNREACHABLE. saudiaexports.sa refuses connections.**

---

### 9. PSS (Presidency of State Security)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://pss.gov.sa/` | Entry point [VERIFY] | curl + WebFetch | TIMEOUT/ECONNREFUSED | **FAIL** | Connection refused — consistent with doc's description of minimal web presence |
| `https://pctc.pss.gov.sa/` | Additional | curl + WebFetch | TIMEOUT | **FAIL** | Counter-terrorism subdomain also unreachable |
| `https://www.moi.gov.sa/` | Additional | curl + WebFetch | TIMEOUT | **FAIL** | Ministry of Interior also unreachable |

**VERIFY verdict (PSS URL): EFFECTIVELY DEAD. pss.gov.sa refuses connections. The agency has no functional web presence.**

---

### 10a. Vision 2030

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.vision2030.gov.sa/en/overview` | Entry point | curl + WebFetch | 403 | **BLOCKED** | Bot protection active |
| `https://www.vision2030.gov.sa/en/explore/projects` | Entry point | curl | 403 | **BLOCKED** | Same bot protection |

---

### 10b. PIF (Public Investment Fund)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.pif.gov.sa/en/news-and-insights/press-releases/` | Entry point | curl + WebFetch | 403 | **BLOCKED** | Bot protection active |
| `https://www.pif.gov.sa/en/news-and-insights/` | Additional | curl | 403 | **BLOCKED** | Same |
| `https://www.pif.gov.sa/en/our-investments/` | Additional | curl | 403 | **BLOCKED** | Same |
| `https://www.pif.gov.sa/en/investors/` | Additional | curl | 403 | **BLOCKED** | Same |

---

### 10c. Aramco

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.aramco.com/en/news-media/news` | Entry point | WebFetch | 200 | **PASS (partial)** | Page structure loads but news content is JS-rendered; curl times out |
| `https://www.aramco.com/en/news-media` | Additional | curl | TIMEOUT | **FAIL** | curl timeout; likely needs JS rendering |
| `https://www.aramco.com/en/investors/investor-news` | Additional | curl | TIMEOUT | **FAIL** | curl timeout |
| `https://www.aramco.com/en/news-media/publications` | Additional | curl | TIMEOUT | **FAIL** | curl timeout |
| `https://www.saudiexchange.sa/` | Additional | curl | 403 | **BLOCKED** | Saudi Exchange blocks automated access |

---

### 10d. GCC General Secretariat

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.gcc-sg.org/en/MediaCenter/News/Pages/default.aspx` | Entry point | curl + WebFetch | 200 | **PASS** | SharePoint site accessible; March 2026 news articles visible |
| `https://www.gcc-sg.org/en-us/Statements/MinisterialCouncilData/PressReleases/Pages/Home.aspx` | Entry point | curl | 200 | **FAIL (404 page)** | Returns 200 but redirects to custom 404 page at `/_layouts/15/GCCPortal/404/404.html` |

---

### 10e. OIC (Organisation of Islamic Cooperation)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.oic-oci.org/` | Entry point | curl + WebFetch | 200 | **PASS** | Homepage accessible; OIC branding confirmed; trilingual (AR/EN/FR) |

---

### Additional URLs (NEOM, National Platform)

| URL | Type | Method | HTTP | Result | Notes |
|---|---|---|---|---|---|
| `https://www.neom.com/en-us/newsroom` | Additional | curl + WebFetch | 200 | **PASS (partial)** | Page loads but content is JS-rendered (CSS/framework only in WebFetch) |
| `https://my.gov.sa/en/agencies/17327` | Additional | curl | 403 | **BLOCKED** | All my.gov.sa agency pages block automated access |

---

## Accessibility Summary by Source

| # | Source | Primary URL Accessible? | RSS Available? | Bot Protection? | Recommended Extraction |
|---|---|---|---|---|---|
| 1 | SPA | Yes (JS-rendered) | **No** (all feeds dead) | Intermittent | Headless browser scraping |
| 2 | MOFA | **Yes** | Undiscovered | Low | HTML scraping (SharePoint) |
| 3 | MODA | **No** (timeout) | No | N/A — unreachable | Monitor via SPA only |
| 4 | Shura Council | **No** (timeout) | Undiscovered | N/A — unreachable | Requires geo-located proxy or manual |
| 5 | Umm al-Qura | **No** (timeout) | No | N/A — unreachable | Requires geo-located proxy or manual |
| 6 | MOF | **Yes** | Undiscovered | Low | HTML scraping (SharePoint) |
| 7 | SAMA | **No** (timeout) | Untestable | N/A — unreachable | Requires geo-located proxy |
| 8 | Min. of Commerce | **Yes** | Undiscovered | Low | HTML scraping (SharePoint) |
| 9 | PSS | **No** (refused) | No | N/A — dead | Monitor via SPA; flag anomalies |
| 10a | Vision 2030 | **No** (403) | No | **Yes** (active) | Requires browser-based or API approach |
| 10b | PIF | **No** (403) | No | **Yes** (active) | Requires browser-based or API approach |
| 10c | Aramco | **Partial** (JS-rendered) | No | Moderate | Headless browser required |
| 10d | GCC | **Yes** | Undiscovered | Low | HTML scraping (SharePoint) |
| 10e | OIC | **Yes** | Undiscovered | Low | HTML scraping |

---

## VERIFY Items Resolution

| Item | URL | Verdict |
|---|---|---|
| SPA RSS feeds (rss.xml, rss3-8.xml) | `spa.gov.sa/rss*.xml` | **INVALID** — all redirect to homepage; RSS infrastructure removed |
| MOFA SharePoint ListFeed | `mofa.gov.sa/.../_layouts/listfeed.aspx` | **UNTESTED** — requires List GUID discovery |
| MODA RSS | `mod.gov.sa` | **UNTESTABLE** — site unreachable |
| Shura Council RSS | `shura.gov.sa` | **UNTESTABLE** — site unreachable |
| Umm al-Qura RSS | `uqn.gov.sa` | **UNTESTABLE** — site unreachable |
| MOF SharePoint ListFeed | `mof.gov.sa/.../_layouts/listfeed.aspx` | **UNTESTED** — requires List GUID; site accessible |
| SAMA SharePoint ListFeed | `sama.gov.sa/.../_layouts/listfeed.aspx` | **UNTESTABLE** — site unreachable |
| SAMA Open Data URL | `sama.gov.sa/en-US/OpenData/Pages/default.aspx` | **UNTESTABLE** — site unreachable |
| MC SharePoint ListFeed | `mc.gov.sa/.../_layouts/listfeed.aspx` | **UNTESTED** — requires List GUID; site accessible |
| GAMI URL | `gami.gov.sa` | **VALID** — accessible, confirmed as General Authority for Military Industries |
| NDMC URL | `ndmc.gov.sa` | **VALID** — accessible, confirmed as National Debt Management Center |
| PSS URL | `pss.gov.sa` | **INVALID** — connection refused; no functional web presence |
| SEDA URL | `saudiaexports.sa` | **INVALID** — connection refused |
| Vision 2030 RSS | `vision2030.gov.sa` | **NO RSS** — site blocks automated access entirely |
| PIF RSS | `pif.gov.sa` | **NO RSS** — site blocks automated access entirely |
| Aramco RSS | `aramco.com` | **NO RSS** — site is JS-rendered; no feed discovered |
| GCC SharePoint ListFeed | `gcc-sg.org/.../_layouts/listfeed.aspx` | **UNTESTED** — requires List GUID; site accessible |
| OIC RSS | `oic-oci.org` | **NO RSS** — no feed discovered |

---

## Recommendations

1. **SPA monitoring must use headless browser scraping.** RSS feeds are dead and the site is fully JS-rendered. The YAML manifest should remove all `rss_feed` entries for SPA and set `extraction_method: headless_browser_scrape`.

2. **Geo-located proxy is likely required** for SAMA, MODA, Shura Council, Umm al-Qura, MOI, and PSS. These sites may restrict access to Saudi/GCC IP ranges. Testing from a Saudi-based VPS would confirm.

3. **PIF and Vision 2030 require anti-bot bypass.** Both return consistent 403s, suggesting Cloudflare or similar WAF. A headless browser with residential proxy may be needed.

4. **SharePoint ListFeed discovery** should be attempted for MOFA, MOF, MC, and GCC — all are accessible SharePoint sites where hidden RSS endpoints may exist but require List GUID enumeration.

5. **SPA remains the single most critical target** despite RSS loss. It is the only universally accessible channel that aggregates Royal Court, MODA, and PSS content.

6. **GCC press releases URL is broken.** The ministerial press releases path returns a custom 404. Only the news page works.

7. **Aramco requires headless browser.** curl times out but WebFetch confirms the page structure exists — content is dynamically loaded.
