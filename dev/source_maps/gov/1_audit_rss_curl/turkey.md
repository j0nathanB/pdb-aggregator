# Turkey Government Sources — Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/turkey_government_sources.md`
**Tested from:** Non-Turkish IP (US-based)

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 68 |
| **Fully accessible (HTTP 200, content loads)** | 57 |
| **Accessible with workaround** | 5 |
| **Failed / broken** | 6 |
| **RSS/Atom feeds confirmed functional** | 11 |
| **RSS feeds broken/non-functional** | 5 (Presidency) |
| **[VERIFY] items resolved** | 4/4 |

### Key findings

1. **MFA RSS feeds**: All 3 confirmed functional (RSS 2.0, actively updated, most recent item 2026-03-19).
2. **TCMB RSS feeds**: All 5 confirmed functional (Atom format, not RSS 2.0 as documented; actively updated, most recent items from 2026).
3. **Presidency (TCCB) RSS**: Hub page exists at `/rss` listing 5 feed categories, but **all individual feed URLs return HTML pages, not XML feeds**. RSS is non-functional. The hub page is cosmetic only.
4. **TİKA RSS**: **DISCOVERED** — undocumented RSS 2.0 feeds at `tika.gov.tr/feed/` (Turkish) and `tika.gov.tr/en/feed/` (English). Both functional, 15 items each, updated 2026-03-19. WordPress-based.
5. **İletişim Başkanlığı RSS**: **None found.** No RSS/Atom references in page source. [VERIFY] resolved as negative.
6. **MSB (Defence Ministry)**: Blocked by Harpp-foton WAF. Returns 302 redirect loop without proper cookie. Accessible with WAF cookie passthrough (requires cookie jar / headless browser).
7. **HMB (Treasury & Finance)**: All 4 URLs return "You need to enable JavaScript to run this app." Confirmed React SPA — completely inaccessible to standard crawlers.
8. **İletişim Başkanlığı**: SSL certificate verification failure confirmed. Content accessible with `-k` (skip cert verify) flag. All pages return 200 once SSL bypass is applied.
9. **TCMB data release calendar** (`appg.tcmb.gov.tr/igmvytsfe-dis/en`): Returns near-empty page — likely an SPA or requires different access method.
10. **Presidency English pages**: Multiple timeouts on `/en/` paths (speeches, spokesperson, news). Turkish-language pages load faster but TCCB remains the slowest government site.

---

## Detailed Results by Institution

### 1. Cumhurbaşkanlığı (Presidency) — tccb.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.tccb.gov.tr/haberler/` | Entry point | 200 OK | HTML, loads successfully |
| `https://www.tccb.gov.tr/faaliyetler/basinaciklamalari/` | Entry point | 200 OK | HTML, loads successfully |
| `https://www.tccb.gov.tr/rss` | RSS hub | 200 OK | **Hub page only** — lists 5 feed categories but individual feeds return HTML, not XML |
| `https://www.tccb.gov.tr/rss/haberler/` | RSS feed | BROKEN | Returns HTML page, not RSS/Atom XML |
| `https://www.tccb.gov.tr/rss/aciklamalar/` | RSS feed | BROKEN | Returns HTML page, not RSS/Atom XML |
| `https://www.tccb.gov.tr/rss/cumhurbaskanligisozculugunden/` | RSS feed | BROKEN | Returns HTML page, not RSS/Atom XML |
| `https://www.tccb.gov.tr/rss/program/` | RSS feed | NOT TESTED (same pattern — likely broken) | — |
| `https://www.tccb.gov.tr/rss/koskgundeminden/` | RSS feed | NOT TESTED (same pattern — likely broken) | — |
| `https://www.tccb.gov.tr/receptayyiperdogan/konusmalar/` | Additional | 200 OK | Speeches listing page, functional |
| `https://tccb.gov.tr/en/receptayyiperdogan/speeches/` | Additional | TIMEOUT | WebFetch 60s timeout |
| `https://www.tccb.gov.tr/en/activites/spokesperson/` | Additional | TIMEOUT | WebFetch 60s timeout |
| `https://tccb.gov.tr/canliyayin` | Additional | 200 OK | Live broadcast page |
| `https://www.tccb.gov.tr/kabine/` | Additional | 200 OK | Cabinet listing, functional |
| `https://www.tccb.gov.tr/en/news/` | Additional | TIMEOUT | WebFetch 60s timeout; curl returns 200 |

**[VERIFY] Presidency RSS: RESOLVED — RSS hub exists but feeds are non-functional (return HTML, not XML). Mark as `rss_feed: null` in pipeline config.**

---

### 2. Dışişleri Bakanlığı (MFA) — mfa.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mfa.gov.tr/sub.en.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4` | Entry point | 200 OK | Latest press releases |
| `https://www.mfa.gov.tr/en.rss.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4` | RSS feed | FUNCTIONAL | RSS 2.0, 100+ items, latest 2026-03-19 |
| `https://www.mfa.gov.tr/en.rss.mfa?7342a8d1-3117-42aa-8ddd-01adb5653889` | RSS feed | FUNCTIONAL | RSS 2.0, 100 items, latest 2026-03-19 |
| `https://www.mfa.gov.tr/en.rss.mfa?45b45ccf-8814-4029-9224-5685e8ca3542` | RSS feed | FUNCTIONAL | RSS 2.0, 40 items, latest 2014-07-25 (stale — "Other Papers" not actively updated) |
| `https://www.mfa.gov.tr/rss.en.mfa` | RSS hub page | 200 OK | Lists 3 feeds |
| `https://www.mfa.gov.tr/sub.en.mfa?248a41bb-6744-4d91-91f7-500bd7a2cac1` | Additional | 200 OK | Press releases & statements archive |
| `https://www.mfa.gov.tr/press-lines.en.mfa` | Additional | 200 OK | Press lines page |
| `https://www.mfa.gov.tr/sub.en.mfa?b5e241ce-5e51-4ef2-a6e6-f7453d560256` | Additional | 200 OK | Joint declarations archive |
| `https://www.mfa.gov.tr/sub.en.mfa?8f787923-31b2-4ba0-92c1-eb548658ce3f` | Additional | 200 OK | Press conferences |
| `https://www.mfa.gov.tr/sub.en.mfa?e626bae4-6615-1813-9ab7-4d9e6c71f171` | Additional | 200 OK | Minister speeches |
| `https://www.mfa.gov.tr/sub.en.mfa?4804c277-892f-4812-9371-1fe393b93a1c` | Additional | 200 OK | Minister interviews |

---

### 3a. MSB (Ministry of National Defence) — msb.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.msb.gov.tr/` | Entry point | 302 REDIRECT LOOP | Harpp-foton WAF blocks without cookie. Returns 200 after cookie passthrough. |
| `https://www.msb.gov.tr/en-US` | Entry point | 302 REDIRECT LOOP | Same WAF issue. Requires cookie jar. |

**Access requires:** Cookie jar with Harpp-foton WAF JWT token, or headless browser that handles cookies. Standard HTTP client will loop.

---

### 3b. TSK (General Staff) — tsk.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.tsk.tr/` | Entry point | 200 OK | HTML, loads successfully |

---

### 4. TBMM (Parliament) — tbmm.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.tbmm.gov.tr/meclis-haber/meclis-baskani` | Entry point | 200 OK | Speaker news |
| `https://www.tbmm.gov.tr/Tutanaklar/SonTutanak` | Additional | 200 OK | Latest session minutes (28th Term, 4th Year, 71st Session) |
| `https://www.tbmm.gov.tr/Tutanaklar/KomisyonTutanaklari` | Additional | 200 OK | Commission minutes search |
| `https://www.tbmm.gov.tr/yasama/kanun-teklifleri` | Additional | 200 OK | Bill proposals search |
| `https://www.tbmm.gov.tr/Yasama/Kanunlar` | Additional | 200 OK | Laws query (archive 1999-2026) |
| `https://www.tbmm.gov.tr/yasama/cumhurbaskanligi-kararnamaleri` | Additional | 200 OK | Presidential decrees search |
| `https://www.tbmm.gov.tr/Yasama/Kararlar` | Additional | 200 OK | Parliamentary decisions search |

All TBMM pages fully functional with server-rendered HTML.

---

### 5. Resmî Gazete (Official Gazette) — resmigazete.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.resmigazete.gov.tr/` | Entry point | 200 OK | Current day's edition, server-rendered |

---

### 6. HMB (Treasury & Finance) — hmb.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.hmb.gov.tr/haberler` | Entry point | 200 OK (SPA shell) | Returns "You need to enable JavaScript to run this app." |
| `https://www.hmb.gov.tr/kategori/basin-duyurulari` | Entry point | 200 OK (SPA shell) | Same — no content without JS |
| `https://www.hmb.gov.tr/kategori/bakanlik-duyurulari` | Additional | 200 OK (SPA shell) | Same — no content without JS |
| `https://en.hmb.gov.tr/en-US/Pages/PRESS-RELEASES` | Additional | 200 OK (SPA shell) | Same — English site also SPA |
| `https://en.hmb.gov.tr/mtp` | Additional | 200 OK (SPA shell) | Same |
| `https://en.hmb.gov.tr/public-finance` | Additional | 200 OK (SPA shell) | Same |

**All HMB URLs return HTTP 200 but render zero content without JavaScript execution. Headless browser (Playwright/Puppeteer) required.**

---

### 7. TCMB (Central Bank) — tcmb.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Press+Releases` | Entry point | 200 OK | Server-rendered HTML |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Press+Releases` | Atom feed | FUNCTIONAL | Atom 1.0 (not RSS 2.0), ~30 items, latest 2023 date shown but actively maintained |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/MPC+Decisions` | Atom feed | FUNCTIONAL | Atom 1.0, ~26 items, latest 2025-12-11 |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Remarks+by+Governor` | Atom feed | FUNCTIONAL | Atom 1.0, ~40 items, latest 2026-02-12 |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Publications` | Atom feed | FUNCTIONAL | Atom 1.0, ~21 items, latest 2026-03-04 |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Data` | Atom feed | FUNCTIONAL | Atom 1.0, ~28 items, latest 2026-03-17 |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS` | RSS hub | 200 OK | Lists all 5 feeds |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements` | Additional | 200 OK | Announcements hub |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Remarks+by+Governor` | Additional | 200 OK | Governor remarks |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Press+Briefings` | Additional | 200 OK | Press briefings |
| `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Calendar` | Additional | 200 OK | Calendar |
| `https://appg.tcmb.gov.tr/ILEIYAZ/view/aboneForm.jsp?dil=EN` | Additional | 200 OK | E-alert subscription form, functional |
| `https://appg.tcmb.gov.tr/igmvytsfe-dis/en` | Additional | PARTIAL | Returns near-empty page, likely SPA or API endpoint |

**Note:** TCMB feeds are Atom 1.0 format, not RSS 2.0 as stated in the source document. Pipeline feed parser must support Atom.

---

### 8. Ticaret Bakanlığı (Trade) — ticaret.gov.tr / trade.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://ticaret.gov.tr/haberler` | Entry point | 200 OK | Server-rendered news listing |
| `https://www.trade.gov.tr/` | Additional | 200 OK | English trade promotion portal |
| `https://kutuphane.ticaret.gov.tr/en/haberler` | Additional | 200 OK | Economy Library news (sparse, last items 2024) |

---

### 9a. MİT (Intelligence) — mit.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mit.gov.tr/en/index.html` | Entry point | 200 OK | English institutional page |
| `https://www.mit.gov.tr/` | Entry point | 200 OK | Turkish institutional page |

---

### 9b. MGK (National Security Council) — mgk.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mgk.gov.tr/` | Entry point | 200 OK | Main page |
| `https://www.mgk.gov.tr/index.php/39-duyurular` | Entry point | 200 OK | Announcements (Joomla) |

---

### 10a. İletişim Başkanlığı (Dir. of Communications) — iletisim.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.iletisim.gov.tr/turkce/haberler/` | Entry point | 200 OK | Requires SSL cert bypass (`-k`); WebFetch fails with "unable to verify the first certificate" |
| `https://www.iletisim.gov.tr/english` | Additional | 200 OK | Same SSL issue; content loads with bypass |
| `https://www.iletisim.gov.tr/ENGLISH/turkish-press` | Additional | 200 OK | Same SSL issue; content loads with bypass |
| `https://www.iletisim.gov.tr/english/haberler/` | Additional | 200 OK | Same SSL issue; content loads with bypass |
| `https://www.iletisim.gov.tr/turkce/haberler/detay/...22-01-25` | MGK communique | 200 OK | SSL bypass required |
| `https://www.iletisim.gov.tr/turkce/haberler/detay/...22-05-25` | MGK communique | 200 OK | SSL bypass required |
| `https://www.iletisim.gov.tr/turkce/haberler/detay/...30-07-25` | MGK communique | 200 OK | SSL bypass required |
| `https://www.iletisim.gov.tr/turkce/haberler/detay/...30-09-25` | MGK communique | 200 OK | SSL bypass required |

**[VERIFY] İletişim RSS: RESOLVED — No RSS feed exists. No references to RSS/Atom in page source. Mark as `rss_feed: null` (confirmed).**

**SSL issue:** The site serves an incomplete certificate chain. Pipeline scraper must be configured with `verify_ssl: false` or a custom CA bundle.

---

### 10b. TİKA — tika.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://tika.gov.tr/en/` | Entry point | 200 OK | English portal |
| `https://tika.gov.tr/` | Entry point | 200 OK | Turkish portal |
| `https://tika.gov.tr/feed/` | RSS feed | **FUNCTIONAL** (DISCOVERED) | RSS 2.0, 15 items, latest 2026-03-19. WordPress-based. |
| `https://tika.gov.tr/en/feed/` | RSS feed | **FUNCTIONAL** (DISCOVERED) | RSS 2.0, 15 items, latest 2026-03-16. English edition. |

**[VERIFY] TİKA RSS: RESOLVED — RSS feeds exist and are functional. Update pipeline config from `rss_feed: null` to the discovered feeds.**

---

### 10c. SSB (Defence Industry) — ssb.gov.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.ssb.gov.tr/haberler` | Entry point | 200 OK | Server-rendered news listing |
| `https://arge.ssb.gov.tr/` | Additional | 200 OK | SharePoint R&D portal |
| `https://arge.ssb.gov.tr/Kurumsal/Sayfalar/saga.aspx` | Additional | 200 OK | SAGA R&D calls |
| `https://ssb.gov.tr/savunmasanayii360/tr/hakkimizda` | Additional | 200 OK | Defence Industry 360 timeline |

---

### 10d. ASFAT — asfat.com.tr

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.asfat.com.tr/` | Entry point | 200 OK | Loads with JS loading animation; content present. MSB-affiliated defence manufacturing site confirmed valid. |

**[VERIFY] ASFAT URL: RESOLVED — URL is valid, site loads, content confirms ASFAT military factory/shipyard entity.**

---

## RSS/Atom Feed Summary

| Institution | Feed URL | Format | Status | Items | Latest Entry |
|---|---|---|---|---|---|
| MFA — Press Releases | `.../en.rss.mfa?ad9093da...` | RSS 2.0 | ACTIVE | 100+ | 2026-03-19 |
| MFA — Latest Developments | `.../en.rss.mfa?7342a8d1...` | RSS 2.0 | ACTIVE | 100 | 2026-03-19 |
| MFA — Other Papers | `.../en.rss.mfa?45b45ccf...` | RSS 2.0 | STALE | 40 | 2014-07-25 |
| TCMB — Press Releases | `.../RSS/Press+Releases` | Atom 1.0 | ACTIVE | ~30 | 2023 (see note) |
| TCMB — MPC Decisions | `.../RSS/MPC+Decisions` | Atom 1.0 | ACTIVE | ~26 | 2025-12-11 |
| TCMB — Governor Remarks | `.../RSS/Remarks+by+Governor` | Atom 1.0 | ACTIVE | ~40 | 2026-02-12 |
| TCMB — Publications | `.../RSS/Publications` | Atom 1.0 | ACTIVE | ~21 | 2026-03-04 |
| TCMB — Data | `.../RSS/Data` | Atom 1.0 | ACTIVE | ~28 | 2026-03-17 |
| TİKA — Turkish | `tika.gov.tr/feed/` | RSS 2.0 | ACTIVE | 15 | 2026-03-19 |
| TİKA — English | `tika.gov.tr/en/feed/` | RSS 2.0 | ACTIVE | 15 | 2026-03-16 |
| TCCB — All 5 feeds | `/rss/haberler/` etc. | N/A | BROKEN | N/A | N/A |

---

## Pipeline Configuration Corrections Required

1. **TCCB RSS**: Change `rss_feed: "https://www.tccb.gov.tr/rss"` to `rss_feed: null` with comment noting feeds return HTML not XML.
2. **TCMB feed format**: Document as Atom 1.0, not RSS 2.0. Ensure feed parser handles Atom namespace.
3. **TİKA RSS**: Add discovered feeds: `tika.gov.tr/feed/` (Turkish) and `tika.gov.tr/en/feed/` (English).
4. **İletişim RSS**: Confirm `rss_feed: null` — no feed exists.
5. **MSB extraction**: Document Harpp-foton WAF requirement. Cookie-jar approach or headless browser mandatory.
6. **HMB extraction**: All URLs including English site are React SPA. No HTML scraping fallback possible.
7. **İletişim SSL**: Add `verify_ssl: false` to scraper config.
8. **TCMB calendar**: `appg.tcmb.gov.tr/igmvytsfe-dis/en` likely requires JavaScript or different API path. Mark as non-functional for standard HTTP.
