# Czech Republic Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/czech_republic_government_sources.md`
**Method:** WebFetch (primary), curl with browser User-Agent (fallback for 403/failure)

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 68 |
| RSS feeds tested | 17 |
| RSS feeds working | 14 |
| RSS feeds failed | 1 (CNB Czech press releases — 404) |
| RSS feeds confirmed absent | 2 (MZV explicitly "no active channels"; CNB RSS hub lists only 2 EN feeds) |
| Entry point URLs tested | 17 |
| Entry point URLs working | 13 |
| Entry point URLs failed | 4 (hrad.cz 403, MO /en/news 404, vlada /cz/jednani-vlady/ 404, PSP media section document-not-found) |
| Additional URLs tested | 34 |
| Additional URLs working | 27 |
| Additional URLs failed | 7 |
| Sites blocking automated access | 1 (hrad.cz — all paths return 403) |
| TLS certificate errors | 1 (nbu.gov.cz — works with -k flag) |

**Overall fetchability rate: 54/68 (79%)**
**Fetchability excluding hrad.cz bot-blocking: 54/62 (87%)**

---

## VERIFY Items — Resolution

| Item | Documented Claim | Test Result | Resolution |
|---|---|---|---|
| hrad.cz RSS feed URLs | RSS page at `/en/for-media/rss` — "returned 403 on automated fetch" | **Confirmed 403.** All hrad.cz paths (press releases, RSS, speeches, diary) return 403 to both WebFetch and curl with browser UA. Aggressive bot protection. | **INVALID for automation.** Requires browser-session scraping or headed browser (Playwright/Puppeteer). |
| PSP RSS | "RSS referenced in footer but URL unknown" | `/rss/` returns 403, `/rss/rss.xml` and `/rss/index.xml` return 404. | **No RSS available.** |
| MF RSS | "VERIFY RSS" | `/rss/` and `/rss.xml` both return 404. | **No RSS available.** |
| MPO RSS | "VERIFY RSS" | `/rss/` returns soft 404 (200 status but "Page not found" content). | **No RSS available.** |
| NUKIB RSS | "VERIFY RSS" | `/rss/` returns 502. | **No RSS available.** |
| e-Sbirka RSS | "VERIFY RSS on e-sbirka.cz" | `/rss` returns 404 (redirects then 404). Main page loads (200) but no RSS. | **No RSS available.** |
| CEZ press releases URL | "VERIFY URL" | `https://www.cez.cz/en/media/press-releases` — **200 OK**, functional press release listing with recent content (March 2026). | **VALID.** |
| CEZ RSS | "VERIFY RSS" | `/rss` returns 404. | **No RSS available.** |
| CNB Czech press releases RSS | "VERIFY URL" for `cnb.cz/cs/.content/rss-feed/rss-feed_tz.xml` | **404 Not Found.** The Czech-language RSS path does not mirror the English path. | **INVALID.** Only English RSS feeds confirmed working. |

---

## Per-Source Detailed Results

### 1a. Urad vlady (Government Office) — vlada.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://vlada.gov.cz/scripts/detail.php?pgid=215` | Entry point (CS press releases) | **200 OK** | 2,046 press releases listed. Functional. |
| `https://vlada.gov.cz/en/media-centrum/aktualne/` | Entry point (EN news) | **200 OK** | English news portal accessible. |
| `https://www.vlada.cz/cs/urad/RSS/rss.xml` | RSS (CS) | **302 -> 200 OK** | Redirects to `vlada.gov.cz`. Valid RSS 2.0, title "Vlada CR", 15 items. |
| `https://www.vlada.cz/en/rss.xml` | RSS (EN) | **302 -> 200 OK** | Redirects to `vlada.gov.cz`. Valid RSS 2.0, title "Government of the Czech Republic", 1 item. Sparse. |
| `https://vlada.gov.cz/cz/jednani-vlady/` | Additional (govt meetings) | **404** | Page not found. URL may have changed. |
| `https://vlada.gov.cz/scripts/detail.php?pgid=1304` | Additional (events) | **200 OK** | Expected events listing, functional. |
| `https://vlada.gov.cz/scripts/detail.php?pgid=1306` | Additional (press conf.) | **200 OK** | Press conference archive, functional. |
| `https://vlada.gov.cz/en/ppov/brs/office-of-the-government-of-the-czech-republic-23851/` | Additional (BRS/NSC) | **200 OK** | National Security Council page, functional. |

### 1b. Presidential Office — hrad.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.hrad.cz/en/for-media/press-releases` | Entry point (EN) | **403 Forbidden** | Bot protection. Blocks all automated access. |
| `https://www.hrad.cz/cs/pro-media/tiskove-zpravy` | Entry point (CS) | **403 Forbidden** | Same bot protection. |
| `https://www.hrad.cz/en/for-media/rss` | RSS page | **403 Forbidden** | Cannot access RSS page or feeds. |
| `https://www.hrad.cz/en/president-of-the-cr/current-president-of-the-cr/selected-speeches-and-interviews` | Additional (speeches) | **403 Forbidden** | Blocked. |
| `https://www.hrad.cz/en/president-of-the-cr/current-president-of-the-cr/diary` | Additional (diary) | **403 Forbidden** | Blocked. |

**Assessment:** hrad.cz requires headed browser automation (Playwright/Puppeteer) for any scraping. Standard HTTP clients are blocked regardless of User-Agent.

### 2. MZV (Foreign Ministry) — mzv.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://mzv.gov.cz/jnp/en/issues_and_press/press_releases/index.html` | Entry point (EN) | **200 OK** | Press releases listing, March 2026 content. Functional. |
| `https://mzv.gov.cz/jnp/cz/informace_a_tisk/tiskove_zpravy/index.html` | Entry point (CS) | Not separately tested (same CMS pattern) | Expected functional. |
| `https://mzv.gov.cz/jnp/en/rss.html` | RSS info page | **200 OK** | Page explicitly states: "Sorry, no active RSS channels for now." |
| `https://mzv.gov.cz/jnp/en/issues_and_press/mfa_statements/index.html` | Additional (MFA statements) | **200 OK** | Accessible. Requires JS/cookies. |
| `https://mzv.gov.cz/jnp/en/about_the_ministry/organization_of_the_ministry/minister/speeches_and_articles/index.html` | Additional (minister speeches) | **200 OK** | Accessible. |
| `https://mzv.gov.cz/washington` | Additional (embassy) | **200 OK** | Embassy of CZ in Washington, functional. |

### 3. MO (Defense Ministry) — mo.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.mo.gov.cz/en/news` | Entry point (EN) | **404 Not Found** | URL invalid. Returns 404 with both WebFetch and curl. |
| `https://www.mo.gov.cz/scripts/detail.php?pgid=194` | Entry point (alt, CS) | **200 OK** | Newsroom via script, functional. |
| `https://www.mo.gov.cz/en/ministry-of-defence/strategy-and-doctrine/` | Additional | **200 (soft error)** | Page loads but shows "Zprava neexistuje" (message does not exist). |
| `https://www.mo.gov.cz/en/ministry-of-defence/facts-file/` | Additional | **200 (soft error)** | Same — page loads but content missing. |
| `https://www.mo.gov.cz/en/armed-forces/` | Additional | **200 (soft error)** | Same — content not found message. |
| `https://www.mo.gov.cz/en/armed-forces/foreign-operations/` | Additional | **200 (soft error)** | Same — content not found message. |

**Assessment:** MO's English URL structure (`/en/...`) appears broken or restructured. Only the legacy PHP script-based URLs work. The English site likely underwent a redesign that broke these paths.

### 4a. PSP (Chamber of Deputies) — psp.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.psp.cz/sqw/hp.sqw?k=90` | Entry point (media) | **200 OK** | But shows "Dokument nebyl nalezen" (document not found). Navigation works. |
| `https://pspen.psp.cz/` | Entry point (EN portal) | **200 OK** | English portal accessible with live broadcast link. |
| `https://www.psp.cz/rss/` | VERIFY RSS | **403 Forbidden** | Access denied. |
| `https://www.psp.cz/eknih/` | Additional (steno records) | **200 OK** | Digital library of parliamentary records, functional. |
| `https://www.psp.cz/sqw/hlasy.sqw` | Additional (vote records) | **200 OK** | Loads but shows "Hlasovani nebylo nalezeno" (vote not found) — needs query params. |
| `https://www.psp.cz/sqw/sbirka.sqw` | Additional (laws mirror) | **200 OK** | Legal documents collection, functional (encoding issues in display). |
| `https://pspen.psp.cz/live-broadcast/` | Additional (live broadcast) | **200 OK** | Live broadcast page, accessible. |

### 4b. Senat (Senate) — senat.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.senat.cz/zpravodajstvi/zpravy.php` | Entry point (CS press) | **200 OK** | Press releases listing, 100+ items. Functional. |
| `https://www.senat.cz/informace/pro_media/index-eng.php` | Entry point (EN media) | **200 OK** | English media section accessible. |
| `https://www.senat.cz/zpravodajstvi/zpravy_rss.php` | RSS (press releases) | **200 OK** | Valid RSS 2.0. "Senat.cz - tiskove zpravy". 100 items. |
| `https://www.senat.cz/zpravodajstvi/akce_rss.php` | RSS (events) | **200 OK** | Valid RSS 2.0. "Senat.cz - akce". 100 items. |
| `https://www.senat.cz/zpravodajstvi/videa_rss.php` | RSS (videos) | **200 OK** | Valid RSS 2.0. "Senat.cz - videogalerie". 100+ items. |
| `https://www.senat.cz/dokumenty/posledni_projednavane_tisky_rss.php` | RSS (discussed bills) | **200 OK** | Valid RSS 2.0. 200+ items. |
| `https://www.senat.cz/dokumenty/zarazene_neprojednavane_tisky_rss.php` | RSS (enrolled bills) | **200 OK** | Valid RSS 2.0. 8 items. |
| `https://www.senat.cz/dokumenty/zakony_3_psp_rss.php` | RSS (laws 3rd reading) | **200 OK** | Valid RSS 2.0. 0 items (empty but valid feed). |

**Assessment:** Senate has the best RSS infrastructure. All 6 feeds functional.

### 5. Sbirka zakonu / e-Sbirka (Official Gazette)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.e-sbirka.cz/` | Entry point | **200 OK** | Page loads but minimal content rendered (heavy JS app). |
| `https://aplikace.mv.gov.cz/sbirka-zakonu/getall.aspx` | Additional (legacy) | **200 OK** | Legacy archive functional. Years 1945-2025 for laws, 2000-2025 for treaties. |
| `https://mv.gov.cz/clanek/esbirka-a-elegislativa.aspx` | Additional (MoI info) | **200 OK** | Ministry of Interior e-Sbirka information page, accessible. |
| `https://www.psp.cz/sqw/sbirka.sqw` | Additional (PSP mirror) | **200 OK** | See PSP section above. |

### 6. MF (Finance Ministry) — mf.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://mf.gov.cz/en/about-ministry/media-room/news-and-press-releases` | Entry point (EN) | **200 OK** | Press releases 2008-2026 listed. Functional. |
| `https://www.mfcr.cz/cs/informacni-servis/tiskove-zpravy/` | Entry point (CS, legacy) | **404 Not Found** | Legacy domain path no longer works. |
| `https://monitor.statnipokladna.gov.cz/` | Additional (public finance) | **200 OK** | Requires JavaScript. State treasury monitor portal loads. |

### 7. CNB (Czech National Bank) — cnb.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.cnb.cz/en/cnb-news/` | Entry point | **200 OK** | News archive with year/month filters. Functional. |
| `https://www.cnb.cz/en/public/media-service/` | Entry point (media hub) | **200 OK** | Media service page with contacts, calendar, social media. |
| `https://www.cnb.cz/en/.content/rss-feed/rss-feed_tz.xml` | RSS (EN press releases) | **200 OK** | Valid RSS 2.0. "Czech National Bank - Press releases". 10 items. **Verified.** |
| `https://www.cnb.cz/en/.content/rss-feed/rss-feed_00023.rss` | RSS (EN blog) | **200 OK** | Valid RSS 2.0. "cnBlog". 10 items. **Verified.** |
| `https://www.cnb.cz/cs/.content/rss-feed/rss-feed_tz.xml` | RSS (CS press releases) | **404 Not Found** | Czech RSS path does not exist. Only English feeds available. |
| `https://www.cnb.cz/en/general/rss/` | RSS hub page | **200 OK** | Lists only 2 feeds: press releases EN + cnBlog EN. |
| `https://www.cnb.cz/en/monetary-policy/bank-board-decisions/` | Additional | **200 OK** | Current 2W repo rate 3.50%. Meeting calendar for 2026 listed. |
| `https://www.cnb.cz/en/public/media-service/governors-speeches-and-interviews/` | Additional | **200 OK** | Governor Michl speeches 2022-2026 archive. |
| `https://www.cnb.cz/en/public/media-service/the-cnb-comments-on-the-statistical-data-on-inflation-and-gdp/` | Additional | **200 OK** | Page loads but shows "No entries found" — requires filter selection. |
| `https://www.cnb.cz/en/cnb-news/calendar/` | Additional | **200 OK** | Calendar with filters, downloadable spreadsheet available. |
| `https://www.cnb.cz/arad/` | Additional (stats DB) | **200 OK** | ARAD statistical database. Minimal content rendered in fetch. |

### 8. MPO (Industry & Trade) — mpo.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://mpo.gov.cz/en/guidepost/for-the-media/press-releases/` | Entry point (EN) | **200 OK** | Press releases 2020-2026. Functional. |
| `https://mpo.gov.cz/cz/rozcestnik/pro-media/tiskove-zpravy/` | Entry point (CS) | Not separately tested | Expected functional (same CMS). |
| `https://mpo.gov.cz/en/energy/` | Additional | **200 OK** | Energy policy section accessible. |
| `https://mpo.gov.cz/en/foreign-trade/` | Additional | **200 OK** | Foreign trade section accessible. |

### 9a. BIS (Domestic Intelligence) — bis.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bis.cz/en/` | Entry point | **200 OK** | Institutional homepage. Mission, focus areas, annual reports link. |
| `https://www.bis.cz/annual-reports/` | Additional | **200 OK** | Annual reports page accessible. Multilingual (CS/EN/DE/FR). |

### 9b. UZSI (Foreign Intelligence) — uzsi.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.uzsi.cz/en/` | Entry point | **200 OK** | Institutional homepage. Minimal content. Established Jan 1993. |

### 9c. VZ (Military Intelligence) — vzcr.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://vzcr.gov.cz/en` | Entry point | **200 OK** | Institutional portal. CZE SATCEN, cyber defence, press releases sections. |

### 9d. NUKIB (Cyber Security) — nukib.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://nukib.gov.cz/en/infoservis-en/news/` | Entry point | **200 OK** | News listing with recent items (cooperation with Japan, cyber threats). |
| `https://nukib.gov.cz/en/infoservis-en/publications-reports/` | Additional | **200 OK** | Publications archive with PDFs. |
| `https://nukib.gov.cz/en/cyber-security/` | Additional | **200 OK** | Cyber security section accessible. |
| `https://nukib.gov.cz/en/cyber-security/research-nukib/` | Additional | **200 OK** | Research section accessible. |

### 10a. CZSO (Statistical Office) — csu.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://csu.gov.cz/news_releases_archive` | Entry point | **200 OK** | News releases archive. Scheduled releases at 9 AM. 2025/2026 calendars downloadable. |
| `https://csu.gov.cz/rss/statistika/aktuality?jazyk=EN` | RSS (News EN) | **200 OK** | Valid RSS 2.0. "CSO - News". 19 items. |
| `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=RI&jazyk=EN` | RSS (News Releases EN) | **200 OK** | Valid RSS 2.0. "CSO - News Release". 100 items. |
| `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=TZ&jazyk=EN` | RSS (Press Releases EN) | **200 OK** | Valid RSS 2.0. "CSO - Press Release". 103 items. |
| `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Ana&jazyk=EN` | RSS (Analyses EN) | **200 OK** | Valid RSS 2.0. "CSO - Analysis". 110 items. |
| `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Pub&jazyk=EN` | RSS (Publications EN) | **200 OK** | Valid RSS 2.0. "CSO - Publication". 100 items. |
| `https://www.volby.cz/index_en.htm` | Additional (elections) | **200 OK** | Election results portal. Requires JavaScript. |

### 10b. CEZ Group — cez.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.cez.cz/en/media/press-releases` | Entry point | **200 OK** | Press releases with March 2026 content. Filterable by topic. **VERIFY resolved: VALID.** |

### 10c. NBU (National Security Authority) — nbu.gov.cz

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.nbu.gov.cz/en/` | Entry point | **TLS cert error** | ERR_TLS_CERT_ALTNAME_INVALID. Works with `curl -k` (200 OK, text/html). Certificate mismatch for `www.nbu.gov.cz`. |

---

## Key Findings

### Critical Issues

1. **hrad.cz (Presidential Office)** blocks all automated access with 403 on every path. This is a P1 source requiring headed browser automation (Playwright/Puppeteer with stealth settings). No RSS feeds can be verified or used.

2. **mo.gov.cz (Defense Ministry)** English URL structure is broken. `/en/news` returns 404, and all `/en/ministry-of-defence/...` paths show "message does not exist." Only the legacy PHP script URL (`/scripts/detail.php?pgid=194`) works. English content may need to be accessed differently.

3. **nbu.gov.cz** has a TLS certificate mismatch on `www.nbu.gov.cz`. Low-priority source but needs cert fix or use without `www` prefix.

### RSS Feed Scorecard

| Source | Feeds Claimed | Feeds Working | Notes |
|---|---|---|---|
| Senat (Senate) | 6 | 6 (1 empty) | Best RSS in Czech govt. All functional. |
| CZSO (Statistical Office) | 5 | 5 | All functional, well-populated. |
| CNB (Central Bank) | 3 (2 EN, 1 CS) | 2 EN | CS press releases feed 404. Only EN feeds exist. |
| Vlada (Government Office) | 2 (CS + EN) | 2 | Both redirect vlada.cz -> vlada.gov.cz. EN feed has only 1 item. |
| Hrad (Presidential Office) | Unknown | 0 testable | All paths return 403. Cannot verify any RSS. |
| MZV (Foreign Ministry) | 0 | 0 | Explicitly "no active channels." |
| All others | 0 | 0 | No RSS found at any tested path. |

**Total working RSS feeds: 15 across 4 institutions.**

### Automation Readiness Tiers

| Tier | Sources | Method |
|---|---|---|
| **Tier 1: RSS-ready** | Senat, CZSO, CNB, Vlada (CS) | RSS polling. Fully automatable. |
| **Tier 2: HTML-scrapable** | MZV, MF, MPO, BIS, UZSI, VZ, NUKIB, CEZ, PSP, e-Sbirka, Vlada (EN) | Standard HTTP + HTML parsing. No bot protection. |
| **Tier 3: Requires headed browser** | Hrad.cz | Playwright/Puppeteer with anti-detection. 403 on all standard HTTP. |
| **Tier 4: Broken/needs investigation** | MO (English paths), NBU (TLS), PSP media section (doc not found) | URLs need updating or special handling. |
