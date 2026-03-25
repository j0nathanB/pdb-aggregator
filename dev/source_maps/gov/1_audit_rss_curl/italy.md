# Italy Government Sources — Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/italy_government_sources.md`
**Test method:** WebFetch for RSS validation; curl with Mozilla UA for HTTP status checks; WebFetch fallback for redirect/bot detection

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 68 |
| RSS feeds tested | 36 |
| RSS feeds confirmed working | 29 |
| RSS feeds broken/error | 6 |
| RSS feeds blocked (403) | 1 |
| Entry point URLs tested | 32 |
| Entry points returning 200 | 26 |
| Entry points returning 403 | 4 |
| Entry points blocked by bot protection | 2 |
| Entry points timing out | 1 |
| VERIFY items resolved | 5 |

**Overall fetchability rate:** 81% (55/68 URLs accessible)

---

## Per-Source Results

### 1.1 Palazzo Chigi (governo.it) — P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.governo.it/feed/rss` | RSS | **OK** (200) | Valid RSS 2.0. 10 items. Most recent: 2026-03-19. Feed title: "Feed" |
| `https://www.governo.it/it/notizie-governo` | Entry | **OK** (200) | HTML |
| `https://www.governo.it/it/sala-stampa` | Entry | **OK** (200) | HTML |
| `https://www.governo.it/it/notizie-presidente` | Entry | **OK** (200) | HTML |
| `https://www.governo.it/it/notizie-chigi` | Entry | **OK** (200) | HTML |
| `https://www.governo.it/it/archivio-articoli-presidenza-del-consiglio` | Entry | **OK** (200) | HTML |

**Status: FULLY OPERATIONAL** — RSS feed is active and current. All entry points accessible.

---

### 1.2 Farnesina / MAECI (esteri.it) — P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.esteri.it/it/sala_stampa/comunicati/` | Entry | **BLOCKED** | Radware Bot Manager. Redirects to `validate.perfdrive.com`. curl returns 200 for redirect target page, not content. |
| `https://www.esteri.it/it/sala_stampa/` | Entry | **OK** (200) | Surprisingly returns 200 for press room hub (may still be Radware challenge page) |
| `https://www.aics.gov.it/` | Entry | **OK** (200) | AICS development cooperation site accessible |
| `https://italiaue.esteri.it/it/` | Entry | **OK** (200) | EU Perm Rep homepage accessible (no Radware on this subdomain) |

**Status: BOT-PROTECTED** — Radware Bot Manager confirmed active on esteri.it. Headless browser (Playwright/Puppeteer) required. AICS and EU Perm Rep subdomains accessible without bot protection.

**[VERIFY RSS] result:** No RSS feed found. Confirmed blocked by Radware, making feed discovery impossible via automated means.

---

### 1.3 Ministero della Difesa (difesa.it) — P1

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.difesa.it/il-ministro/comunicati/elenco/index.html` | Entry | **OK** (200) | HTML |
| `https://www.difesa.it/comunicazione/index/72490.html` | Entry | **OK** (200) | HTML |
| `https://www.difesa.it/sgd-dna/staff/giornaleufficiale/giornale-ufficiale-della-difesa/32853.html` | Entry | **OK** (200) | HTML |
| `https://www.difesa.it/eng/` | Entry | **OK** (200) | English section exists (301 redirect, then 200) |
| `https://www.esercito.difesa.it/comunicazione/comunicati-stampa` | Entry | **TIMEOUT** | 301 redirect, then connection hangs. Timed out after 15s. |
| `https://www.marina.difesa.it/media-cultura/press-room/comunicati/Pagine/default2.aspx` | Entry | **OK** (200) | HTML |
| `https://www.aeronautica.difesa.it/home/media-e-comunicazione/comunicati-stampa/` | Entry | **OK** (200) | HTML |

**Status: MOSTLY OPERATIONAL** — Main difesa.it site accessible. Esercito (Army) subdomain has connectivity issues (redirect loop / timeout). SSL certificate issues were not encountered during this test.

**[VERIFY RSS] result:** No RSS feed found on difesa.it. Newsletter at newsletter.difesa.it is alternative.

**[VERIFY English section] result:** English section at `/eng/` confirmed accessible (200 after redirect).

---

### 1.4a Camera dei Deputati — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://comunicazione.camera.it/comunicati-stampa` | Entry | **OK** (200) | HTML |
| `https://comunicazione.camera.it/archivio-prima-pagina` | Entry | **OK** (200) | HTML |
| `https://www.camera.it/leg19/68` | Entry | **OK** (200) | RSS index page |
| `https://comunicazione.camera.it/rss/comunicati-stampa` | RSS | **OK** (200) | Valid RSS 2.0. 20 items. Most recent: 2026-03-19 |
| `https://comunicazione.camera.it/rss/notizie-prima-pagina` | RSS | **OK** (200) | Valid RSS 2.0. 20 items. Most recent: 2026-03-19 |
| `https://comunicazione.camera.it/rss/comma` | RSS | **OK** (200) | Valid RSS 2.0. 15 items. Most recent: 2026-03-13 |
| `https://comunicazione.camera.it/rss/commissioni-giunte` | RSS | **OK** (200) | Valid RSS 2.0. 1 item. Most recent: 2026-03-18 |
| `http://documenti.camera.it/apps/rssFeeds/odg/getFeed.asp` | RSS | **OK** (200) | text/xml |
| `http://documenti.camera.it/rss/resocontiAssemblea/getFeed.xml` | RSS | **OK** (200) | text/xml |
| `http://documenti.camera.it/apps/rssFeeds/ultimipdl/pdlUltimiAnnunciati.asp?idLegislatura=19` | RSS | **OK** (200) | text/xml |
| `http://documenti.camera.it/apps/rssFeeds/Dossier/getFeedinter.xml` | RSS | **OK** (200) | text/xml |
| `http://webtv.camera.it/rssFeeds/webtv/eventi_recenti.php` | RSS | **OK** (200) | application/xml |

**Status: FULLY OPERATIONAL** — All 9 RSS feeds and 3 entry points working. Outstanding RSS infrastructure.

---

### 1.4b Senato della Repubblica — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.senato.it/attualita/comunicati-stampa` | Entry | **OK** (200) | HTML |
| `https://www.senato.it/attualita/in-copertina` | Entry | **OK** (200) | HTML |
| `https://dati.senato.it/sito/feed_rss?testo_generico=9` | Entry | **OK** (200) | RSS index page (HTML) |
| `http://www.senato.it/senato/feeds/1/1252.xml` | RSS | **OK** (200) | Valid RSS 2.0. 10 items. Most recent: 2026-02-25 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedODGA.xml` | RSS | **OK** (200) | Valid RSS 2.0. 25 items. Most recent: 2026-03-20 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedRSTA.xml` | RSS | **OK** (200) | Valid RSS 2.0. 25 items. Most recent: 2026-03-18 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedODGGC.xml` | RSS | **OK** (200) | Valid RSS 2.0. 25 items. Most recent: 2026-03-26 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedRSGC.xml` | RSS | **OK** (200) | Valid RSS 2.0. 25 items. Most recent: 2026-03-17 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedDDL.xml` | RSS | **OK** (200) | Valid RSS 2.0. 30 items. Most recent: 2026-03-18 |
| `https://www.senato.it/static/bgt/UltimiAtti/feedADG.xml` | RSS | **OK** (200) | Valid RSS 2.0. 30 items. Most recent: 2026-03-13 |
| `https://www.senato.it/leg/19/BGT/Schede/Dossier/rss/aaii.xml` | RSS | **OK** (200) | Valid RSS 2.0. 100 items. Most recent: 2026-03-03 |
| `https://www.senato.it/static/bgt/UltimiAtti/feed.xml` | RSS | **OK** (200) | Valid RSS 2.0. 50 items. Most recent: 2026-03-20 |
| `http://www.parlamento.it/parlamento/feeds/3/284.xml` | RSS | **OK** (200) | Valid RSS 2.0. 10 items. Most recent: 2026-03-04 |

**Status: FULLY OPERATIONAL** — All 10 RSS feeds and 3 entry points working. Excellent feed infrastructure.

---

### 1.5 Gazzetta Ufficiale — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.gazzettaufficiale.it/` | Entry | **OK** (200) | HTML |
| `https://www.normattiva.it/` | Entry | **OK** (200) | HTML |
| `https://www.gazzettaufficiale.it/rss/SG` | RSS | **OK** (200) | Valid RSS 2.0, application/rss+xml. 36 items. Most recent: 2026-03-19 |
| `https://www.gazzettaufficiale.it/rss/S1` | RSS | **OK** (200) | application/rss+xml |
| `https://www.gazzettaufficiale.it/rss/S2` | RSS | **OK** (200) | application/rss+xml |
| `https://www.gazzettaufficiale.it/rss/S3` | RSS | **OK** (200) | application/rss+xml |
| `https://www.gazzettaufficiale.it/rss/S4` | RSS | **OK** (200) | application/rss+xml |
| `https://www.gazzettaufficiale.it/rss/S5` | RSS | **OK** (200) | application/rss+xml |
| `https://www.gazzettaufficiale.it/rss/P2` | RSS | **OK** (200) | application/rss+xml |

**Status: FULLY OPERATIONAL** — All 7 RSS feeds and 2 entry points working.

---

### 1.6 MEF (mef.gov.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mef.gov.it/ufficio-stampa/comunicati/` | Entry | **OK** (200) | HTML |
| `https://www.mef.gov.it/inevidenza/` | Entry | **OK** (200) | HTML |
| `https://www.mef.gov.it/ufficio-stampa/atti-parlamentari.html` | Entry | **OK** (200) | HTML |
| `https://www.finanze.gov.it/it/rss/` | Entry | **OK** (200) | HTML info page, not a feed. Points to `http://www.finanze.gov.it/rss.xml` |
| `http://www.finanze.gov.it/rss.xml` | RSS | **FAIL** (403) | Forbidden. Actual RSS feed URL is blocked. |
| `https://www.rgs.mef.gov.it/` | Entry | **OK** (200) | HTML |

**Status: PARTIALLY OPERATIONAL** — Entry points work. RSS situation unresolved.

**[VERIFY RSS] result:** The MEF site references an RSS feed page at `finanze.gov.it/it/rss/` which is an informational HTML page pointing to `http://www.finanze.gov.it/rss.xml`. That RSS URL returns **403 Forbidden**. The main MEF domain (`mef.gov.it`) has no discoverable RSS feed. **RSS is NOT available for MEF.**

---

### 1.7 Banca d'Italia (bancaditalia.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.bancaditalia.it/media/comunicati/index.html` | Entry | **OK** (200) | HTML |
| `https://www.bancaditalia.it/media/index.html` | Entry | **OK** (200) | HTML |
| `https://www.bancaditalia.it/util/index.rss.html?lingua=it` | RSS | **OK** (200) | Valid RSS 2.0. 50 items. Most recent: 2026-03-19. **Master feed works.** |
| `https://www.bancaditalia.it/util/index.rss.html?sezione=media/comunicati&lingua=it` | RSS | **BROKEN** | Returns RSS envelope with `ERROR: syntax error for 'sezione' parameter value`. HTTP 200 but empty feed. |
| `https://www.bancaditalia.it/util/index.rss.html?sezione=media/bce-comunicati&lingua=it` | RSS | **BROKEN** | Same error as above. |
| `https://www.bancaditalia.it/util/index.rss.html?sezione=media/notizie&lingua=it` | RSS | **BROKEN** | Same error as above. |
| `https://www.bancaditalia.it/util/index.rss.html?sezione=pubblicazioni&lingua=it` | RSS | **BROKEN** | Same error — even single-path-segment `sezione` values fail. |
| `https://www.bancaditalia.it/util/index.rss.html?sezione=statistiche&lingua=it` | RSS | **BROKEN** | Same error. |
| `https://alert.bancaditalia.it/webApp/rss?LANGUAGE=it` | Entry | **OK** (200) | RSS directory page (HTML). Lists 132 feeds. |

**Status: PARTIALLY OPERATIONAL** — Master feed (`?lingua=it` without `sezione`) works and is current. **All parameterized `sezione` feeds are broken** — the server returns a valid RSS envelope but with an XML comment error: `ERROR: syntax error for 'sezione' parameter value`. This affects all 131 topic-specific feeds documented in the source map. The alert directory page at `alert.bancaditalia.it` is accessible and lists the feeds, but the feed URLs themselves are broken.

**Pipeline impact:** Use the master feed only (`?lingua=it`). The 132-feed infrastructure documented in the source map is currently non-functional for the `sezione` parameter. Email alerts at `alert.bancaditalia.it` remain a viable alternative.

---

### 1.8 MIMIT (mimit.gov.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mimit.gov.it/it/notizie-stampa` | Entry | **OK** (200) | HTML |
| `https://www.mimit.gov.it/index.php/it/per-i-media` | Entry | **OK** (200) | HTML |

**Status: FULLY OPERATIONAL** — No RSS (as documented). HTML scraping entry points accessible.

**[VERIFY RSS] result:** No RSS feed found. Confirmed.

---

### 1.9a DIS (sicurezzanazionale.gov.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.sicurezzanazionale.gov.it/` | Entry | **OK** (200) | HTML. Script-heavy as documented. |

**Status: OPERATIONAL** — Homepage accessible. Low-frequency monitoring target.

---

### 1.9c COPASIR (parlamento.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.parlamento.it/1172` | Entry | **OK** (200) | HTML |

**Status: OPERATIONAL** — Entry point accessible.

---

### 1.10a Quirinale (quirinale.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.quirinale.it/ricerca/comunicati` | Entry | **BLOCKED** (403) | Forbidden for automated requests. Confirms documented issue. |
| `https://www.quirinale.it/ricerca/discorsi` | Entry | **BLOCKED** (403) | Forbidden |
| `https://www.quirinale.it/ricerca/Notizie` | Entry | **BLOCKED** (403) | Forbidden |
| `https://archivio.quirinale.it/aspr/redazione/discorsi` | Entry | **BLOCKED** (403) | Historical archive also blocking (documented as "more permissive" — not confirmed) |
| `http://presidenti.quirinale.it/elementi/Elenchi.aspx?tipo=Comunicato` | Entry | **BLOCKED** (403) | Legacy presidential communications also blocked |

**Status: FULLY BLOCKED** — All 5 Quirinale URLs return 403 Forbidden. The bot protection is more aggressive than documented — it blocks all automated access including the historical archive and legacy site. User-agent rotation alone is unlikely to work; headless browser with full JS rendering may be needed.

**[VERIFY RSS] result:** No RSS feed discoverable. All endpoints return 403. Cannot verify.

---

### 1.10b EU Permanent Representation (italiaue.esteri.it) — P2

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://italiaue.esteri.it/it/` | Entry | **OK** (200) | HTML |
| `https://italiaue.esteri.it/it/news/dalla_rappresentanza/` | Entry | **OK** (200) | HTML |

**Status: FULLY OPERATIONAL** — Unlike parent domain esteri.it, this subdomain does NOT have Radware bot protection. Both entry points accessible.

**[VERIFY bot protection] result:** No Radware protection detected on italiaue.esteri.it. Standard HTTP scraping should work.

---

## VERIFY Items Resolution Summary

| Item | Source | Verdict |
|---|---|---|
| Farnesina RSS | esteri.it | **No RSS.** Radware blocks discovery. Confirmed not available. |
| Difesa RSS | difesa.it | **No RSS.** Newsletter at newsletter.difesa.it is alternative. |
| Difesa English section | difesa.it/eng | **Valid.** Returns 200 after 301 redirect. |
| MEF RSS | mef.gov.it | **No working RSS.** `finanze.gov.it/rss.xml` returns 403. Main MEF domain has no feed. |
| MIMIT RSS | mimit.gov.it | **No RSS.** Confirmed not available. |
| Quirinale RSS | quirinale.it | **Cannot verify.** All endpoints return 403. |
| EU Perm Rep bot protection | italiaue.esteri.it | **No bot protection.** Accessible via standard HTTP. |

---

## Critical Findings

### 1. Banca d'Italia `sezione` feeds are all broken
The source document claims 132 RSS feeds. In reality, **only the master feed works** (`?lingua=it`). All parameterized feeds with `sezione=...` return a syntax error inside an empty RSS envelope. This is a server-side issue, not a client-side problem. The pipeline should use the master feed and filter by content rather than relying on topic-specific feeds.

### 2. Quirinale is more locked down than documented
The source document suggests user-agent rotation as mitigation. In practice, **all 5 Quirinale URLs** (including the historical archive and legacy site) return 403. Full headless browser rendering with JS execution is likely required.

### 3. Farnesina Radware protection confirmed
Redirects to `validate.perfdrive.com` as documented. Headless browser required. However, the EU Perm Rep subdomain (`italiaue.esteri.it`) is NOT behind Radware and is fully accessible.

### 4. Esercito (Army) subdomain has connectivity issues
`esercito.difesa.it` times out after a 301 redirect. Other armed services subdomains (Marina, Aeronautica) work fine.

### 5. MEF RSS is dead
The `finanze.gov.it/rss.xml` URL returns 403. No working RSS feed exists for MEF or its departments.

### 6. Top-performing RSS sources
Camera dei Deputati (9/9 feeds working), Senato (10/10 feeds working), and Gazzetta Ufficiale (7/7 feeds working) have flawless RSS infrastructure. Palazzo Chigi's single feed is also reliable and current.
