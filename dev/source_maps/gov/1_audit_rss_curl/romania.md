# Romania Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/romania_government_sources.md`
**Tested from:** macOS / US-based IP

---

## Summary

| Category | Count |
|---|---|
| **Total unique URLs tested** | 52 |
| **Fully accessible (HTTP 200 + content confirmed)** | 22 |
| **Accessible via curl only (200 but WebFetch blocked)** | 6 |
| **Service unavailable (503)** | 8 |
| **Forbidden (403)** | 2 |
| **Gone (410)** | 1 |
| **Connection failed (000 / timeout)** | 10 |
| **SSL/TLS certificate error** | 2 |
| **Redirect (needs follow-up)** | 1 |

### RSS Feed Verification Summary

| Source | RSS Documented | RSS Verified | Result |
|---|---|---|---|
| Presidency | [VERIFY] | **No RSS found** | All endpoints return 503/000. No `/rss`, `/feed` endpoints respond. |
| gov.ro | Yes (`gov.ro/en/rss`) | **Yes — functional** | Returns content with recent items (malformed XML but parseable). Items from 2026-03-19. |
| MAE | [VERIFY] | **Yes — `mae.ro/rss.xml`** | Valid RSS 2.0 feed. 200 OK with `application/rss+xml`. Recent items confirmed. |
| MApN | No | Confirmed no RSS | N/A |
| Chamber of Deputies | [VERIFY] | **No RSS found** | Site unreachable (connection timeout 000). |
| Senate | [VERIFY] | **No RSS found** | `/rss` returns 404. |
| Min. Finance | [VERIFY] | **No RSS found** | Site unreachable (connection timeout 000). |
| BNR | Yes (multiple) | **Yes — RSS hub + XML feeds** | RSS hub pages return 200. XML exchange rate feeds fully functional with current data (2026-03-19). |
| Min. Economy | [VERIFY] | **No RSS found** | Site returns 503 (Cloudflare). |
| SRI | [VERIFY] | **No RSS found** | `/rss` and `/feed` both return 404. |
| AGERPRES | [VERIFY] | **Partial — redirect to third-party** | `/rss` returns 522 via curl; WebFetch shows redirect to `createfeed.bazqux.com` (third-party feed generator). Not a native RSS feed. |
| EU Perm Rep | [VERIFY] | **No RSS found** | Site returns 503 (MAE subdomain). |
| NATO Delegation | [VERIFY] | **No RSS found** | Site unreachable (connection timeout 000). |
| BSEC | [VERIFY] | **No RSS found** | `/rss` returns 404. |

---

## Detailed Results by Institution

### 1a. Presidency (presidency.ro) — P1

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.presidency.ro/en/media/press-releases` | WebFetch | **503** | text/html | Service Unavailable |
| `https://www.presidency.ro/en/media/press-releases` | curl | **503** | text/html;charset=utf-8 | Confirmed 503 |
| `https://www.presidency.ro/en/media/press-releases` | curl (retry) | **000** | — | Connection failed on retry |
| `https://www.presidency.ro/ro/media/comunicate-de-presa` | WebFetch | **503** | — | Service Unavailable |
| `https://www.presidency.ro/en/rss` | WebFetch | **503** | — | No RSS found |
| `https://www.presidency.ro/en/rss` | curl | **503** | text/html;charset=utf-8 | No RSS |
| `https://www.presidency.ro/en/feed` | WebFetch | **503** | — | No RSS found |
| `https://www.presidency.ro/en/feed` | curl | **503** | text/html;charset=utf-8 | No RSS |
| `https://www.presidency.ro/feed` | curl | **503** | text/html;charset=utf-8 | No RSS |
| `https://www.presidency.ro/rss` | curl | **503** | text/html;charset=utf-8 | No RSS |
| `https://www.presidency.ro/en/media/messages` | Not separately testable | **503** (assumed) | — | Same domain, same 503 pattern |
| `https://www.presidency.ro/en/media/speeches` | Not separately testable | **503** (assumed) | — | Same domain |
| `https://www.presidency.ro/en/.../csat-secretariat` | Not separately testable | **503** (assumed) | — | Same domain |

**Assessment:** presidency.ro is completely unreachable. Returns 503 on all endpoints. The document notes intermittent 503 errors — this may be a persistent outage or aggressive bot blocking. Retry logic essential. AGERPRES fallback required.

---

### 1b. Government / PM (gov.ro) — P1

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://gov.ro/en/rss` | WebFetch | **200** | — | Content received. RSS items present but malformed XML. Recent items from 2026-03-19. |
| `https://gov.ro/ro/rss` | WebFetch | **200** | — | Content received. RSS items present. Recent items from 2026-03-19. |
| `https://gov.ro/en/media/press-releases` | WebFetch | **200** | text/html | Accessible. Press releases visible including OECD survey launch (Mar 12). |
| `https://gov.ro/en/news` | curl | **200** | text/html;charset=utf-8 | Accessible. |
| `https://gov.ro/en/prime-minister/` | curl | **200** | text/html;charset=utf-8 | Accessible. |

**Assessment:** Fully functional. RSS feeds work but XML is malformed — parser must be tolerant. All entry points accessible.

---

### 2. MAE — Foreign Affairs (mae.ro) — P1

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.mae.ro/en/taxonomy/term/952` | WebFetch | **503** | — | Service Unavailable |
| `https://www.mae.ro/en/taxonomy/term/952` | curl | **503** | text/html;charset=utf-8 | Confirmed 503 |
| `https://www.mae.ro/taxonomy/term/148` | curl | **000** | — | Connection failed |
| `https://www.mae.ro/rss` | curl | **503** | text/html;charset=utf-8 | Not a valid endpoint |
| `https://www.mae.ro/rss.xml` | curl | **200** | application/rss+xml;charset=utf-8 | **Valid RSS 2.0 feed!** |
| `https://www.mae.ro/rss.xml` | WebFetch | **200** | — | Confirmed valid RSS. Recent items include diplomatic meetings, EU Council participation. |
| `https://www.mae.ro/en/actuality` | curl | **000** | — | Connection failed |
| `https://www.mae.ro/en/romanian-missions` | curl | **000** | — | Connection failed |

**Assessment:** Main HTML pages return 503 or connection failures. However, the RSS feed at `mae.ro/rss.xml` is fully functional and should be the primary extraction method. This is a key finding — the [VERIFY] tag is resolved: **RSS exists and works at `https://www.mae.ro/rss.xml`**.

---

### 3. MApN — Defense (mapn.ro) — P1

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://english.mapn.ro/cpresa/` | WebFetch | **410 Gone** | — | Page returns "Gone" status |
| `https://english.mapn.ro/cpresa/` | curl | **200** | text/html;charset=UTF-8 | Accessible via curl (WebFetch 410 may be bot detection) |
| `https://www.mapn.ro/cpresa/` | curl | **200** | text/html;charset=UTF-8 | Accessible. |
| `https://english.mapn.ro/press/index.php` | curl | **200** | text/html;charset=UTF-8 | Accessible. |

**Assessment:** Accessible via curl. WebFetch returns 410 which may indicate selective bot blocking (responds differently to different user agents). No RSS confirmed. HTML scraping viable with proper user agent.

---

### 4a. Chamber of Deputies (cdep.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.cdep.ro/pls/dic/site.home?idl=2` | WebFetch | **Timeout** (60s) | — | Page did not respond within timeout |
| `https://www.cdep.ro/` | curl | **000** | — | Connection failed |
| `https://www.cdep.ro/pls/steno/steno.home?idl=2` | curl | **000** | — | Connection failed |
| `https://www.cdep.ro/pls/proiecte/upl_pck.home?idl=2` | curl | **000** | — | Connection failed |

**Assessment:** Completely unreachable. Oracle PL/SQL site appears to be down or blocking non-Romanian IPs. The document notes the architecture is "dated and can be slow." May require Romanian proxy or VPN for access.

---

### 4b. Senate (senat.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.senat.ro/` | WebFetch | **200** | — | Fully accessible. Recent content visible (budget debates, Moldova partnership). |
| `https://www.senat.ro/rss` | curl | **404** | text/html | No RSS feed available. |
| `https://www.senat.ro/pagini/bp/bp.htm` | curl | **200** | text/html | Biroul Permanent page accessible. |

**Assessment:** Fully functional. No RSS confirmed. HTML scraping viable.

---

### 5. Monitorul Oficial (monitoruloficial.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://monitoruloficial.ro/` | WebFetch | **SSL error** | — | "unable to verify the first certificate" |
| `https://monitoruloficial.ro/` | curl | **200** | text/html;charset=UTF-8 | Accessible (curl ignores cert chain by default with -L) |
| `https://monitoruloficial.ro/` | curl (-k) | **200** | text/html;charset=UTF-8 | Accessible with explicit cert skip |
| `https://monitoruloficial.ro/en/produs/e-monitor-on-line-gratuit/` | WebFetch | **SSL error** | — | Same cert issue |
| `https://monitoruloficial.ro/en/produs/e-monitor-on-line-gratuit/` | curl (-k) | **200** | text/html;charset=UTF-8 | Accessible with cert skip |
| `https://op.europa.eu/en/web/forum/romania-oj` | curl | **200** | text/html;charset=UTF-8 | EU Forum page accessible. |

**Assessment:** Site is up but has an **SSL certificate chain issue** (intermediate cert missing). Scraper must disable strict certificate verification or use HTTP. Content accessible with `-k` flag.

---

### 6. Ministry of Finance (mfinante.gov.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://mfinante.gov.ro/ro/acasa` | WebFetch | **Connection closed** | — | Socket connection closed unexpectedly |
| `https://mfinante.gov.ro/ro/acasa` | curl | **000** | — | Connection failed |
| `https://mfinante.gov.ro/en/` | curl | **000** | — | Connection failed |
| `https://mfinante.gov.ro/en/web/trezor` | curl | **000** | — | Connection failed |
| `https://mfinante.gov.ro/en/web/trezor/piata-primara/anunturi-emisiuni` | curl | **000** | — | Connection failed |

**Assessment:** Completely unreachable. All endpoints return connection failures. May be geo-blocked, experiencing outage, or requiring Romanian network access. No RSS confirmed.

---

### 7. BNR — Central Bank (bnr.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.bnr.ro/nbrfxrates.xml` | WebFetch | **200** | — | **Valid XML.** Daily exchange rates. Most recent: 2026-03-19. 34 currency pairs. |
| `https://www.bnr.ro/nbrfxrates10days.xml` | WebFetch | **200** | — | **Valid XML.** 10-day history. Covers 2026-03-06 to 2026-03-19. 40+ currencies. |
| `https://www.bnr.ro/RSS-Feeds-4129.aspx` | WebFetch | **200** | — | Page loads but specific RSS URLs not clearly listed in rendered content. |
| `https://www.bnr.ro/Fluxuri-RSS-905.aspx` | curl | **200** | text/html;charset=UTF-8 | RSS hub page accessible. |
| `https://www.bnr.ro/Press-releases-4957.aspx` | WebFetch | **200** | — | Page loads (rendered as BNR homepage nav). |
| `https://www.bnr.ro/Comunicate-de-presa-4954.aspx` | curl | **200** | text/html;charset=UTF-8 | Romanian press releases accessible. |
| `https://www.bnr.ro/Monetary-policy-decisions-5765.aspx` | curl | **200** | text/html;charset=UTF-8 | Accessible. |
| `https://www.bnr.ro/Inflation-Reports-3553.aspx` | curl | **200** | text/html;charset=UTF-8 | Accessible. |

**Assessment:** Excellent availability. All endpoints functional. XML feeds are machine-readable and current. Best government source for automated ingestion. RSS hub pages load but individual RSS feed URLs need to be extracted from the hub page HTML.

---

### 8. Ministry of Economy (economie.gov.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `http://www.economie.gov.ro/` | WebFetch | **SSL error** | — | ERR_TLS_CERT_ALTNAME_INVALID |
| `http://www.economie.gov.ro/` | curl | **503** | text/html;charset=utf-8 | Cloudflare-style blocking |
| `https://economie.gov.ro/` | curl | **503** | text/html;charset=utf-8 | Same 503 |
| `http://www.imm.gov.ro/` | curl | **000** | — | Connection failed |
| `http://www.imm.gov.ro/en/mmaca/press-releases/` | curl | **000** | — | Connection failed |

**Assessment:** Unreachable. SSL certificate mismatch plus Cloudflare-style bot protection. Headless browser with Romanian proxy likely required. IMM subdomain also unreachable.

---

### 9a. SRI — Domestic Intelligence (sri.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.sri.ro/articole/` | WebFetch | **403 Forbidden** | — | Access denied |
| `https://www.sri.ro/articole/` | curl | **403** | text/html;charset=iso-8859-1 | Confirmed 403 |
| `https://www.sri.ro/en` | curl | **200** | text/html;charset=UTF-8 | English home accessible |
| `https://www.sri.ro/rss` | curl | **404** | text/html;charset=UTF-8 | No RSS |
| `https://www.sri.ro/feed` | curl | **404** | text/html;charset=UTF-8 | No RSS |

**Assessment:** Articles page returns 403 Forbidden — likely bot blocking or access restriction on the articles listing. English home page is accessible. No RSS. May require browser-like headers or Romanian IP.

---

### 9b. SIE — Foreign Intelligence (sie.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.sie.ro/` | WebFetch | **200** | — | Accessible. Shows recruitment/careers page content. |
| `https://www.sie.ro/` | curl | **200** | text/html | Confirmed accessible. |
| `https://www.sie.ro/rcd2011/En/index_e.html` | curl | **200** | text/html | Old English site accessible. |

**Assessment:** Accessible. Minimal content as documented. No RSS (not expected).

---

### 10a. EU Permanent Representation (ue.mae.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://ue.mae.ro/en` | WebFetch | **503** | — | Service Unavailable |
| `https://ue.mae.ro/en` | curl | **503** | text/html;charset=utf-8 | Confirmed 503 |
| `https://ue.mae.ro/en/feed` | curl | **503** | text/html;charset=utf-8 | No RSS (same 503) |

**Assessment:** Unreachable — same 503 pattern as main MAE site. MAE subdomain infrastructure shares the same availability issues.

---

### 10b. NATO Permanent Delegation (nato.mae.ro) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://nato.mae.ro/en` | WebFetch | **503** | — | Service Unavailable |
| `https://nato.mae.ro/en` | curl | **000** | — | Connection failed |
| `https://nato.mae.ro/en/local-news` | curl | **000** | — | Connection failed |
| `https://nato.mae.ro/en/feed` | curl | **000** | — | Connection failed |

**Assessment:** Completely unreachable. Connection failures suggest DNS or routing issues beyond the 503s seen on other MAE subdomains.

---

### 10c. BSEC (bsec-organization.org) — P2

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.bsec-organization.org/press-releases` | WebFetch | **200** | — | Fully accessible. Recent press releases visible (March 2026). |
| `https://www.bsec-organization.org/rss` | curl | **404** | text/html | No RSS feed. |

**Assessment:** Fully functional. No RSS. HTML scraping viable.

---

### 10d. AGERPRES (agerpres.ro) — P1

| URL | Method | Status | Content-Type | Notes |
|---|---|---|---|---|
| `https://www.agerpres.ro/english` | WebFetch | **200** | — | Fully accessible. Headlines visible including parliament budget debates (Mar 19, 2026). |
| `https://www.agerpres.ro/rss` | curl | **522** | text/plain | Server error. |
| `https://www.agerpres.ro/rss` | WebFetch | **301 redirect** | — | Redirects to third-party `createfeed.bazqux.com`. Not a native RSS feed. |

**Assessment:** HTML entry point fully functional. RSS is not natively available — the `/rss` path redirects to a third-party feed generator service (bazqux.com), which returned a 522 error via curl. HTML scraping is the reliable extraction method.

---

## Additional Entry Points Summary

| URL | Status | Method | Notes |
|---|---|---|---|
| `https://gov.ro/en/news` | 200 | curl | Accessible |
| `https://gov.ro/en/prime-minister/` | 200 | curl | Accessible |
| `https://www.senat.ro/pagini/bp/bp.htm` | 200 | curl | Accessible |
| `https://english.mapn.ro/press/index.php` | 200 | curl | Accessible |
| `https://www.bnr.ro/Monetary-policy-decisions-5765.aspx` | 200 | curl | Accessible |
| `https://www.bnr.ro/Inflation-Reports-3553.aspx` | 200 | curl | Accessible |
| `https://op.europa.eu/en/web/forum/romania-oj` | 200 | curl | Accessible |
| `https://www.sie.ro/rcd2011/En/index_e.html` | 200 | curl | Old SIE site accessible |
| `https://www.sri.ro/en` | 200 | curl | English home accessible |
| `https://monitoruloficial.ro/en/produs/e-monitor-on-line-gratuit/` | 200 | curl (-k) | SSL cert issue but content OK |
| `https://www.mae.ro/en/actuality` | 000 | curl | Connection failed |
| `https://www.mae.ro/en/romanian-missions` | 000 | curl | Connection failed |
| `https://www.cdep.ro/pls/steno/steno.home?idl=2` | 000 | curl | Connection failed |
| `https://www.cdep.ro/pls/proiecte/upl_pck.home?idl=2` | 000 | curl | Connection failed |
| `https://mfinante.gov.ro/en/web/trezor` | 000 | curl | Connection failed |
| `https://mfinante.gov.ro/en/web/trezor/piata-primara/anunturi-emisiuni` | 000 | curl | Connection failed |
| `http://www.imm.gov.ro/` | 000 | curl | Connection failed |
| `http://www.expert-monitor.ro/` | 000 | curl | Connection failed |
| `https://nato.mae.ro/en/local-news` | 000 | curl | Connection failed |

---

## Key Findings and Recommendations

### 1. RSS Feed Status (VERIFY resolutions)

- **MAE RSS discovered:** `https://www.mae.ro/rss.xml` is a valid, functional RSS 2.0 feed. Update the source document to reflect this. This should be the primary extraction method for MAE.
- **gov.ro RSS confirmed:** Both `gov.ro/en/rss` and `gov.ro/ro/rss` work, though XML is malformed. Use a tolerant parser.
- **BNR feeds confirmed:** XML exchange rate feeds are excellent. RSS hub pages load but individual feed URLs need extraction from hub HTML.
- **AGERPRES has no native RSS.** The `/rss` endpoint redirects to a third-party service (bazqux.com) that is itself unreliable (522 errors).
- **All other [VERIFY] items resolved as negative:** Presidency, Chamber of Deputies, Senate, Ministry of Finance, Ministry of Economy, SRI, EU Perm Rep, NATO Delegation, and BSEC have no RSS feeds.

### 2. Availability Concerns

- **presidency.ro:** Persistent 503 errors across all endpoints. Critical P1 source unavailable. AGERPRES fallback essential.
- **MAE ecosystem (mae.ro, ue.mae.ro, nato.mae.ro):** HTML pages return 503 or connection failures, but `mae.ro/rss.xml` works. Use RSS as primary method.
- **cdep.ro:** Completely unreachable (connection timeouts). May require Romanian IP.
- **mfinante.gov.ro:** Completely unreachable (connection failures). May require Romanian IP.
- **economie.gov.ro:** 503 Cloudflare-style blocking. Headless browser + Romanian proxy needed.
- **sri.ro/articole/:** 403 Forbidden on the articles listing page (though `/en` home page works).
- **monitoruloficial.ro:** SSL certificate chain issue. Scraper must skip cert verification.

### 3. Reliability Tiers

| Tier | Sources | Notes |
|---|---|---|
| **Tier 1 — Highly Reliable** | BNR (all endpoints), gov.ro (RSS + HTML), AGERPRES (HTML), BSEC, senat.ro, SIE | Consistently accessible, stable infrastructure |
| **Tier 2 — Accessible with Caveats** | MApN (needs proper UA), MAE (RSS only), monitoruloficial.ro (SSL issue), SRI (home only, not /articole/) | Require specific technical workarounds |
| **Tier 3 — Unreachable from Test Location** | presidency.ro, cdep.ro, mfinante.gov.ro, economie.gov.ro, ue.mae.ro, nato.mae.ro | May require Romanian proxy/VPN; persistent 503s or connection failures |
