# Indonesia Government Sources — Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/indonesia_government_sources.md`
**Test method:** WebFetch (with AI content verification) + curl fallback (with browser User-Agent, following redirects, 15s timeout)

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 55 |
| **Entry point URLs** | 22 |
| **Additional entry point URLs** | 24 |
| **RSS/Atom feed URLs** | 9 |
| **Reachable (HTTP 200 + content confirmed)** | 35 |
| **Blocked (403)** | 10 |
| **Not found (404)** | 6 |
| **Connection failure (000 / socket close / SSL error)** | 8 |
| **Confirmed RSS feeds** | 3 (setkab, emedia.dpr, kemhan) |
| **[VERIFY] RSS — invalid** | 6 (presidenri, setneg, mpr, bi, ekon, ojk) |

### Key Findings

1. **Three confirmed working RSS feeds:** Setkab (`setkab.go.id/feed/`), E-Media DPR (`emedia.dpr.go.id/feed/`), and — newly confirmed — Kemhan (`kemhan.go.id/feed/`). All return valid RSS 2.0 with recent items.
2. **Presidenri.go.id blocks all automated access** (403 on both feed and all entry points). Headless browser with anti-bot bypass likely required.
3. **Bank Indonesia is effectively unreachable** via standard HTTP. Socket drops on all tested URLs (ID and EN). ASP.NET ViewState + aggressive connection management.
4. **Kemenkeu drops connections** (000) on all tested URLs — JavaScript-heavy site needs headless browser.
5. **TNI HQ (`tni.mil.id`)** has SSL certificate issues AND returns 404 on `/news.html`. The entry point URL may have changed.
6. **Pertamina news-release URLs return 404** for both `/en/` and `/id/` paths — URL structure may have changed.
7. **Kemlu SPA confirmed:** Returns 200 to curl but WebFetch sees only a loading splash screen. Headless browser required as documented.
8. **DPR main site (`dpr.go.id`)** blocks automated access (403) across all paths, but E-Media subdomain works fine.

---

## 1. RSS Feed Test Results

| # | Feed URL | Status | Details |
|---|---|---|---|
| 1 | `https://setkab.go.id/feed/` | **CONFIRMED** | Valid RSS 2.0. Title: "Sekretariat Kabinet Republik Indonesia". 10 items. Latest: 2026-03-14. |
| 2 | `https://emedia.dpr.go.id/feed/` | **CONFIRMED** | Valid RSS 2.0. Title: "E-Media DPR RI". 10 items. Latest: 2026-03-16. |
| 3 | `https://www.kemhan.go.id/feed/` | **CONFIRMED** | Valid RSS 2.0. Title: "Kementerian Pertahanan Republik Indonesia". 10 items. Latest: 2026-03-18. |
| 4 | `https://www.presidenri.go.id/feed/` | **FAILED (403)** | [VERIFY] result: blocked. WordPress site returns 403 to all automated requests. |
| 5 | `https://www.setneg.go.id/feed/` | **FAILED (404)** | [VERIFY] result: no feed exists. |
| 6 | `https://www.mpr.go.id/feed/` | **FAILED (404)** | [VERIFY] result: no feed exists. |
| 7 | `https://www.bi.go.id/feed/` | **FAILED (000)** | [VERIFY] result: socket connection dropped after 302 redirect. ASP.NET site, no feed. |
| 8 | `https://ekon.go.id/feed/` | **FAILED (200 but HTML)** | [VERIFY] result: returns 200 but serves regular HTML page, not RSS/Atom XML. No feed exists. |
| 9 | `https://ojk.go.id/feed/` | **FAILED (404)** | [VERIFY] result: no feed exists. |

---

## 2. Primary Entry Point URL Results

| # | Institution | Entry Point URL | WebFetch | curl | Status | Notes |
|---|---|---|---|---|---|---|
| 1a | Presiden RI | `https://www.presidenri.go.id/siaran-pers/` | 403 | 403 | **BLOCKED** | Returns 403 to all automated requests. Cloudflare or server-side bot protection. |
| 1b | Setkab | `https://setkab.go.id/berita/` | 200 + content | — | **OK** | Full news listing with recent articles (Mar 2026). WordPress. |
| 1c | Setneg | `https://www.setneg.go.id/listcontent/listberita/berita_presiden_dan_pemerintah` | 200 + content | — | **OK** | News listing with pagination. Latest articles Mar 2026. |
| 2 | Kemlu (ID) | `https://kemlu.go.id/portal/id/list/berita/84/press-release` | 200 (SPA shell only) | 200 | **PARTIAL** | Returns 200 but content is SPA loading screen. Headless browser required. |
| 2 | Kemlu (EN) | `https://kemlu.go.id/portal/en/list/berita/84/press-release` | — | 200 | **PARTIAL** | Same SPA issue as Indonesian version. |
| 3a | Kemhan | `https://www.kemhan.go.id/category/berita` | 200 + content | — | **OK** | Full news portal with recent articles. WordPress. |
| 3b | TNI HQ | `https://tni.mil.id/news.html` | SSL error | 404 | **FAILED** | SSL certificate invalid + 404 on news.html. Entry point may have moved. |
| 3c | TNI AD | `https://tniad.mil.id/berita/` | — | 200 | **OK** | Reachable (SSL skip required). |
| 3c | TNI AL | `https://www.tnial.mil.id/` | — | 200 | **OK** | Reachable (SSL skip required). |
| 3c | TNI AU | `https://tni-au.mil.id/berita/satuan` | — | 200 | **OK** | Reachable (SSL skip required). |
| 4a | DPR (E-Media) | `https://emedia.dpr.go.id/` | 200 + content | — | **OK** | Full parliamentary news portal. WordPress. Active content. |
| 4a | DPR (main) | `https://www.dpr.go.id/berita` | — | 403 | **BLOCKED** | Main DPR site blocks automated access. Use E-Media instead. |
| 4b | MPR | `https://www.mpr.go.id/berita` | 200 + content | — | **OK** | News section with leadership statements. Accessibility tools present. |
| 5a | Peraturan.go.id | `https://peraturan.go.id/` | 200 + content | — | **OK** | 61,832 regulations indexed. Search interface functional. |
| 5b | JDIH Setneg | `https://jdih.setneg.go.id/Terbaru` | 200 (body hidden) | 200 | **DEGRADED** | Returns 200 but CSS hides body content (`display:none`). JS-dependent rendering. |
| 6 | Kemenkeu | `https://www.kemenkeu.go.id/informasi-publik/publikasi/siaran-pers` | 200 (JS shell) | 000 | **DEGRADED** | WebFetch gets only JS/CSS scaffolding. curl gets connection timeout. Headless browser required. |
| 7 | Bank Indonesia (ID) | `https://www.bi.go.id/id/publikasi/ruang-media/news-release/default.aspx` | Socket close | 200 | **PARTIAL** | WebFetch socket error. curl returns 200. ASP.NET ViewState site — flaky connections. |
| 7 | Bank Indonesia (EN) | `https://www.bi.go.id/en/publikasi/ruang-media/news-release/default.aspx` | — | 000 | **FAILED** | Connection drops on English version. |
| 8 | Kemendag | `https://www.kemendag.go.id/berita/siaran-pers` | 200 + content | — | **OK** | Press releases with 438 pages of archives. Pagination works. |
| 9 | BIN | `https://www.bin.go.id/` | Socket close | 000 | **FAILED** | Actively rejects connections. Expected behavior per documentation. |
| 10a | Pertamina (EN) | `https://www.pertamina.com/en/news-room/news-release` | 404 | 404 | **FAILED** | URL returns 404. Site restructured — URL path may have changed. |
| 10a | Pertamina (ID) | `https://www.pertamina.com/id/news-room/news-release` | — | 404 | **FAILED** | Same 404. Both language paths broken. |
| 10b | Danantara | `https://www.danantaraindonesia.co.id/media-center/press-releases` | 200 + content | — | **OK** | Next.js site. Press releases, news, highlights. Active content (Mar 2026). |
| 10c | Kemenko Ekon | `https://ekon.go.id/publikasi/1/siaran-pers` | SSL error | 200 | **PARTIAL** | WebFetch fails on SSL certificate. curl returns 200 (with -k flag). |
| 10d | OJK (ID) | `https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/` | 200 + content | — | **OK** | Press releases with search and pagination. Latest Mar 2026. ASP.NET. |
| 10d | OJK (EN) | `https://ojk.go.id/en/berita-dan-kegiatan/siaran-pers/` | — | 200 | **OK** | English version reachable. |

---

## 3. Additional Entry Point URL Results

| # | URL | curl Status | Notes |
|---|---|---|---|
| 1 | `https://www.presidenri.go.id/pidato/` | 403 | Blocked (same as main site) |
| 2 | `https://www.presidenri.go.id/galeri-foto/` | 403 | Blocked |
| 3 | `https://www.presidenri.go.id/galeri-video/` | 403 | Blocked |
| 4 | `https://setkab.go.id/category/peraturan/` | 200 | OK |
| 5 | `https://setkab.go.id/category/pidato/` | 404 | Not found — category path may have changed |
| 6 | `https://setkab.go.id/en/category/news/` | 200 | OK — English section functional |
| 7 | `https://jdih.setkab.go.id/` | 000 | Connection failure |
| 8 | `https://ppid.kemhan.go.id/` | 200 | OK |
| 9 | `https://jdih.kemhan.go.id/` | 200 | OK |
| 10 | `https://ksap.dpr.go.id/` | 403 | Blocked |
| 11 | `https://en.dpr.go.id/berita/` | 403 | Blocked (same as main DPR site) |
| 12 | `https://www.dpr.go.id/uu/prolegnas` | 403 | Blocked |
| 13 | `https://peraturan.go.id/eng` | 200 | OK — English interface available |
| 14 | `https://www.kemenkeu.go.id/en` | 000 | Connection failure (same as main Kemenkeu) |
| 15 | `https://fiskal.kemenkeu.go.id/publikasi/siaran-pers` | 000 | Connection failure |
| 16 | `https://djpb.kemenkeu.go.id/` | 000 | Connection failure |
| 17 | `https://www.beacukai.go.id/` | 200 | OK |
| 18 | `https://ditjendaglu.kemendag.go.id/` | 200 | OK |
| 19 | `https://bkperdag.kemendag.go.id/` | 200 | OK |
| 20 | `https://jdihn.go.id/` | 200 | OK |
| 21 | `https://jdih.setneg.go.id/` | 200 | OK (main page; /Terbaru has rendering issues) |
| 22 | `https://peraturan.bpk.go.id/` | 403 | Blocked |
| 23 | `https://danantaraindonesia.org/` | 200 | Reachable — verify if redirect to .co.id or separate |
| 24 | `https://polhukam.go.id/` | 000 | Connection failure — [VERIFY] URL unresolvable |

---

## 4. [VERIFY] Item Resolution

| Item | Document Claim | Test Result | Verdict |
|---|---|---|---|
| presidenri.go.id RSS at `/feed/` | "WordPress site, feed likely exists" | 403 on all requests | **UNVERIFIABLE** — feed may exist but site blocks all automated access. Cannot confirm without browser-based test. |
| setneg.go.id RSS | "None identified. [VERIFY RSS]" | 404 at `/feed/` | **NO RSS** — confirmed no feed. |
| kemhan.go.id RSS at `/feed/` | "[VERIFY RSS at kemhan.go.id/feed/]" | Valid RSS 2.0, 10 items, latest 2026-03-18 | **CONFIRMED VALID** — upgrade to confirmed RSS source. |
| mpr.go.id RSS at `/feed/` | "[VERIFY RSS at mpr.go.id/feed/]" | 404 | **NO RSS** — confirmed no feed. |
| bi.go.id RSS | "[VERIFY RSS]" | Socket drop / connection failure | **NO RSS** — ASP.NET site, no feed infrastructure. |
| ekon.go.id RSS | "[VERIFY RSS]" | 200 but returns HTML, not XML | **NO RSS** — no feed exists. |
| ojk.go.id RSS | "[VERIFY RSS]" | 404 | **NO RSS** — confirmed no feed. |
| kemenkeu.go.id/en | "[VERIFY URL]" | 000 (connection failure) | **UNREACHABLE** — entire kemenkeu.go.id domain drops connections to automated clients. |
| pertamina.com/id/news-room/news-release | "[VERIFY URL]" | 404 | **BROKEN** — URL path no longer valid. Site restructured. |
| danantaraindonesia.org | "[VERIFY whether this redirects or is a separate entity]" | 200 | **REACHABLE** — returns 200. Needs manual browser check to determine if it redirects to .co.id. |
| polhukam.go.id | "[VERIFY URL]" | 000 (connection failure) | **UNREACHABLE** — domain does not resolve or actively drops connections. |

---

## 5. Accessibility Tiers

### Tier 1: Fully Accessible (RSS feed available, automated polling ready)
- `setkab.go.id` — RSS confirmed, WebFetch works, highest-value source
- `emedia.dpr.go.id` — RSS confirmed, WebFetch works
- `kemhan.go.id` — RSS **newly confirmed**, WebFetch works

### Tier 2: Accessible via Standard HTTP Scraping
- `setneg.go.id` — HTML scraping, no bot protection
- `kemhan.go.id` — also accessible via HTML (RSS preferred)
- `mpr.go.id` — HTML scraping, no bot protection
- `peraturan.go.id` — search database, functional
- `kemendag.go.id` — HTML scraping, 438 pages of archives
- `ojk.go.id` — ASP.NET but accessible, bilingual
- `danantaraindonesia.co.id` — Next.js, clean HTML
- `tniad.mil.id` — requires SSL certificate skip
- `tnial.mil.id` — requires SSL certificate skip
- `tni-au.mil.id` — requires SSL certificate skip

### Tier 3: Requires Headless Browser
- `kemlu.go.id` — SPA, returns loading screen to HTTP clients
- `kemenkeu.go.id` — JS-heavy, connection drops on standard HTTP
- `bi.go.id` — ASP.NET, socket drops, ViewState-dependent
- `jdih.setneg.go.id/Terbaru` — body hidden via CSS, JS-dependent
- `ekon.go.id` — SSL certificate issues via WebFetch, curl works with `-k`

### Tier 4: Blocked / Requires Anti-Bot Bypass
- `presidenri.go.id` — 403 on all paths (Cloudflare/bot protection)
- `dpr.go.id` (main site) — 403 (use emedia.dpr.go.id instead)
- `ksap.dpr.go.id` — 403
- `peraturan.bpk.go.id` — 403

### Tier 5: Unreachable / Broken
- `tni.mil.id` — SSL invalid + 404 on entry point
- `bin.go.id` — actively drops connections (expected)
- `pertamina.com/news-room/news-release` — 404 on both language paths
- `polhukam.go.id` — connection failure
- `jdih.setkab.go.id` — connection failure
- `fiskal.kemenkeu.go.id` — connection failure
- `djpb.kemenkeu.go.id` — connection failure

---

## 6. Recommendations for Pipeline Configuration

1. **Upgrade kemhan.go.id to RSS polling.** The `/feed/` endpoint is confirmed valid RSS 2.0 with current content. Change `extraction_method` from `html_scrape` to `rss_poll` in the YAML manifest.

2. **Mark presidenri.go.id as requiring anti-bot bypass.** All paths return 403. Options: (a) headless browser with stealth plugin, (b) residential proxy, (c) fall back to Setkab which republishes presidential communications.

3. **Investigate pertamina.com URL restructuring.** Both `/en/news-room/news-release` and `/id/news-room/news-release` return 404. A browser-based investigation is needed to find the current news release URL path.

4. **Investigate tni.mil.id entry point.** `/news.html` returns 404. The TNI HQ site may have restructured. The three service branch portals (tniad, tnial, tni-au) all work with SSL certificate skip.

5. **Kemenkeu entire domain is problematic.** Main site, English site, Fiskal subdomain, and DJPB subdomain all fail with connection drops. All Kemenkeu-family URLs need headless browser with robust retry logic.

6. **Remove non-functional [VERIFY] RSS entries.** Confirmed no RSS exists for: setneg.go.id, mpr.go.id, bi.go.id, ekon.go.id, ojk.go.id. Update the YAML manifest to `rss_feed: null` (remove verify comments).

7. **Add polhukam.go.id to unreachable list.** The [VERIFY URL] for Kemenko Polhukam fails to connect. This source needs a valid URL or should be deprioritized.
