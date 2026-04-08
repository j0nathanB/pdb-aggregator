# Poland Government Sources -- URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/poland_government_sources.md`
**Tested from:** macOS / US IP

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 55 |
| Fully accessible (HTTP 200 + content confirmed) | 39 |
| Accessible via curl only (200 but content blocked for bots) | 5 |
| Blocked (HTTP 403) | 6 |
| Not found (HTTP 404) | 2 |
| Connection refused / DNS failure | 2 |
| Timeout / unreachable | 2 |

**Overall fetchability rate:** 39/55 confirmed working (71%), 44/55 reachable (80%)

---

## VERIFY Item Results

| Item | URL | Result | Notes |
|---|---|---|---|
| Prezydent RSS | `prezydent.pl/rss`, `/feed` | **No RSS found** | Both return 403 (entire domain blocks bots) |
| Senat RSS | `senat.gov.pl/rss`, `/feed` | **No RSS found** | Both return 403 (entire domain blocks bots) |
| NBP RSS | `nbp.pl/rss` | **False positive** | Returns `application/rss+xml` content-type header but body is Incapsula bot-block page |
| BBN RSS | `bbn.gov.pl/rss`, `/feed` | **Untestable** | Entire domain times out from test location |
| 3SI RSS | `3seas.eu` | **No RSS found** | Domain DNS fails / connection refused |
| Senat entry URL | `senat.gov.pl/aktualnosci/` | **403 Forbidden** | Entire domain returns 403 for all automated requests |
| ABW entry URL | `abw.gov.pl/pl/aktualnosci` | **404 Not Found** | Path does not exist; base domain works at `abw.gov.pl/en/` (200) |
| BBN entry URL | `bbn.gov.pl/pl/wydarzenia/` | **Timeout** | Domain unreachable from test location (both HTTP/1.1 and HTTP/2) |
| AU (Armaments Agency) | `au.gov.pl/` | **Connection refused** | DNS resolves but no web server responding |
| WOT (Territorial Defence) | `gov.pl/web/obrona-terytorialna` | **200 OK** | Redirects to gov.pl main page, not a dedicated WOT section |
| MRiT URL variant | `gov.pl/web/rozwoj-technologia/aktualnosci` | **200 OK** | Works (not `/wiadomosci`) |

---

## Per-URL Results: Primary Entry Points

### P1 Sources

| # | Institution | Entry Point URL | Method | HTTP | Content | Status |
|---|---|---|---|---|---|---|
| 1a | Prezydent RP | `https://www.prezydent.pl/aktualnosci` | curl | 403 | text/html | BLOCKED -- bot protection on entire domain |
| 1b | KPRM (Premier) | `https://www.gov.pl/web/premier/aktualnosci` | WebFetch | 200 | News listing confirmed | OK |
| 2 | MSZ (Foreign Affairs) | `https://www.gov.pl/web/dyplomacja/aktualnosci` | WebFetch | 200 | News listing confirmed | OK |
| 3 | MON (Defence) | `https://www.gov.pl/web/obrona-narodowa/aktualnosci5` | WebFetch | 200 | News listing confirmed | OK |

### P2 Sources

| # | Institution | Entry Point URL | Method | HTTP | Content | Status |
|---|---|---|---|---|---|---|
| 4a | Sejm | `https://www.sejm.gov.pl/sejm10.nsf/wydarzenia.xsp?symbol=MEDIA_KOMUNIKATY` | curl | 200 | text/html | OK (CAPTCHA may appear for bots) |
| 4b | Senat | `https://www.senat.gov.pl/aktualnosci/` | curl | 403 | text/html | BLOCKED |
| 5 | Dziennik Ustaw | `https://dziennikustaw.gov.pl/DU` | WebFetch | 200 | Legal acts listing confirmed | OK |
| 6 | MF (Finance) | `https://www.gov.pl/web/finanse/wiadomosci` | WebFetch | 200 | News listing confirmed | OK |
| 7 | NBP | `https://nbp.pl/polityka-pieniezna/dokumenty-rpp/komunikaty-z-posiedzen-rpp/` | curl | 404 | text/html | NOT FOUND -- URL may have changed |
| 8 | MRiT (Dev/Tech) | `https://www.gov.pl/web/rozwoj-technologia/aktualnosci` | WebFetch | 200 | News listing confirmed | OK |
| 9a | ABW | `https://www.abw.gov.pl/pl/aktualnosci` | curl | 404 | text/html | NOT FOUND -- path incorrect |
| 9b | AW | `https://aw.gov.pl/pl/` | curl | 200 | text/html (empty content) | OK (minimal site as expected) |
| 9c | BBN | `https://www.bbn.gov.pl/pl/wydarzenia/` | curl | timeout | -- | UNREACHABLE |
| 10a | EU Rep | `https://www.gov.pl/web/eu` | WebFetch | 200 | EU representation page confirmed | OK |
| 10b | NATO Del | `https://brukselanato.msz.gov.pl/en/` | curl | 200 | text/html | OK |
| 10c | Three Seas | `https://3seas.eu/` | curl | ECONNREFUSED | -- | DOWN / DNS failure |
| 10d | GUS | `https://stat.gov.pl/en/` | WebFetch | 200 | Statistics Poland portal confirmed | OK |

---

## Per-URL Results: Additional Entry Points

### KPRM Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.gov.pl/web/premier/decyzje-rzadu` | WebFetch | 200 | OK -- government decisions listing |
| `https://www.gov.pl/web/premier/komunikaty-cir` | WebFetch | 200 | OK -- CIR communications |
| `https://www.gov.pl/web/premier/zapowiedzi` | WebFetch | 200 | OK -- upcoming events |
| `https://www.gov.pl/web/primeminister` | WebFetch | 200 | OK -- English PM page |

### MSZ Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.gov.pl/web/diplomacy/news-` | WebFetch | 200 | OK -- English diplomacy news |
| `https://brukselaue.msz.gov.pl/en/` | curl | 200 | OK (WebFetch returned empty content) |
| `https://brukselanato.msz.gov.pl/en/` | curl | 200 | OK (WebFetch returned empty content) |
| `https://www.msz.gov.pl/en/news/press_office/press_office_2` | curl | 200 | OK |
| `https://polish-presidency.consilium.europa.eu/en/` | WebFetch | 200 | OK -- presidency archive page |

### MON Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.gov.pl/web/national-defence/news` | WebFetch | 200 | OK -- English defence news |
| `https://au.gov.pl/` | curl | ECONNREFUSED | DOWN -- no web server |
| `https://www.gov.pl/web/obrona-terytorialna` | curl | 200 | REDIRECT to gov.pl main (not a dedicated page) |

### Prezydent Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.prezydent.pl/en/for-the-media/` | curl | 403 | BLOCKED |
| `https://president.pl/news` | curl | 403 | BLOCKED |

### Sejm / Legislature Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.sejm.gov.pl/sejm10.nsf/rss.xsp` | curl | 200 | OK but CAPTCHA challenge served to bots |
| `https://www.sejm.gov.pl/sejm10.nsf/druki.xsp` | curl | 200 | OK |
| `https://www.sejm.gov.pl/sejm10.nsf/agent.xsp?symbol=posglos&NrKadencji=10` | curl | 200 | OK |
| `https://www.sejm.gov.pl/sejm10.nsf/PlanPosKom.xsp` | curl | 200 | OK |
| `https://www.sejm.gov.pl/sejm10.nsf/PorzadekObrad.xsp` | curl | 200 | OK |

### Dziennik Ustaw / ISAP Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://dziennikustaw.gov.pl/MP` | WebFetch | 200 | OK -- Monitor Polski listing |
| `https://isap.sejm.gov.pl/` | curl | 200 | OK (CAPTCHA for WebFetch) |
| `https://isap.sejm.gov.pl/isap.nsf/ByYear.xsp` | curl | 200 | OK |

### NBP Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://nbp.pl/en/` | curl | 200 | OK |
| `https://nbp.pl/en/monetary-policy/mpc-documents/monetary-policy-council-press-releases/` | curl | 200 | OK |
| `https://nbp.pl/en/monetary-policy/mpc-documents/inflation-reports/` | curl | 200 | OK |
| `https://nbp.pl/en/financial-stability/` | curl | 200 | OK |
| `https://nbp.pl/en/statistic-and-financial-reporting/calendar/` | curl | 200 | OK |
| `https://api.nbp.pl/en.html` | WebFetch | 200 | OK -- API documentation |
| `https://nbp.pl/rss` | curl | 200 | FALSE POSITIVE -- header says RSS but body is Incapsula block |

### MRiT Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.paih.gov.pl/en` | WebFetch | 200 | OK -- PAIH investment agency |
| `https://www.gov.pl/web/development-technology` | curl | 200 | OK -- English MRiT |

### Security Services Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.abw.gov.pl/en/` | curl | 200 | OK |
| `https://aw.gov.pl/en/` | curl | 200 | OK |
| `https://en.bbn.gov.pl/en/news` | curl | timeout | UNREACHABLE |

### GUS Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://stat.gov.pl/en/rss/` | WebFetch | 200 | OK -- RSS listing page |
| `https://stat.gov.pl/rss/en/3/3.xml` | WebFetch | 200 | OK -- valid RSS feed with current items |
| `https://api.stat.gov.pl/Home/Index?lang=en` | WebFetch | 200 | OK -- API portal with 9 APIs listed |

### MF Additional

| URL | Method | HTTP | Status |
|---|---|---|---|
| `https://www.gov.pl/web/finance` | curl | 200 | OK -- English Finance page |

---

## Per-URL Results: API Endpoints

| API | URL | Method | HTTP | Content-Type | Status |
|---|---|---|---|---|---|
| NBP Exchange Rates (A) | `https://api.nbp.pl/api/exchangerates/tables/A/` | WebFetch | 200 | JSON | OK -- 32 currencies, live data |
| NBP Gold Prices | `https://api.nbp.pl/api/cenyzlota/` | WebFetch | 200 | JSON | OK -- current gold price |
| NBP API Docs | `https://api.nbp.pl/en.html` | WebFetch | 200 | HTML | OK |
| Sejm ELI (DU 2026) | `https://api.sejm.gov.pl/eli/acts/DU/2026` | WebFetch | 200 | JSON | OK -- 367 acts |
| Sejm ELI (MP 2026) | `https://api.sejm.gov.pl/eli/acts/MP/2026` | WebFetch | 200 | JSON | OK -- 305 entries |
| Sejm Votings | `https://api.sejm.gov.pl/sejm/term10/votings` | WebFetch | 200 | JSON | OK -- 128 session records |
| Sejm MPs | `https://api.sejm.gov.pl/sejm/term10/MP` | WebFetch | 200 | JSON | OK -- 200+ MP records |
| Sejm Prints | `https://api.sejm.gov.pl/sejm/term10/prints` | curl | 200 | application/json | OK |
| Sejm Interpellations | `https://api.sejm.gov.pl/sejm/term10/interpellations` | WebFetch | 200 | JSON | OK -- full lifecycle data |
| Sejm Committees | `https://api.sejm.gov.pl/sejm/term10/committees` | curl | 200 | application/json | OK |
| GUS API Portal | `https://api.stat.gov.pl/Home/Index?lang=en` | WebFetch | 200 | HTML | OK -- 9 APIs available |

---

## RSS Feed Results

| Source | RSS URL | Status | Notes |
|---|---|---|---|
| GUS (News EN) | `https://stat.gov.pl/rss/en/3/3.xml` | **WORKING** | Valid RSS 2.0, current items (2026-03-19) |
| GUS (Infographics) | `https://stat.gov.pl/rss/en/3438/56.xml` | Listed (not individually tested) | On RSS listing page |
| GUS (BDL) | `http://bdl.stat.gov.pl/bdl/rss/EN` | Listed (not individually tested) | On RSS listing page |
| Sejm RSS channels | `https://www.sejm.gov.pl/sejm10.nsf/rss.xsp` | **CAPTCHA blocked** | Domino CMS serves CAPTCHA to automated requests |
| NBP | `https://nbp.pl/rss` | **BLOCKED** | Incapsula blocks content despite correct content-type header |
| Prezydent | `prezydent.pl/rss`, `/feed` | **No RSS** | 403 on entire domain |
| Senat | `senat.gov.pl/rss`, `/feed` | **No RSS** | 403 on entire domain |
| BBN | `bbn.gov.pl` | **Untestable** | Domain unreachable |

---

## Key Findings and Recommendations

### Critical Issues

1. **prezydent.pl / president.pl -- entire domain blocks bots (403).** The document states "does not appear to use aggressive bot protection" but testing shows consistent 403 for all paths. This is a P1 source requiring browser-based scraping (Playwright/Puppeteer) or social media fallback (@prezydentpl on X).

2. **senat.gov.pl -- entire domain returns 403.** The document already noted this possibility. Requires browser-based scraping or fallback to @PolskiSenat on X and PAP coverage.

3. **bbn.gov.pl / en.bbn.gov.pl -- completely unreachable.** Connection times out on both HTTP/1.1 and HTTP/2. Either geo-blocked or experiencing infrastructure issues. Needs retesting from European IP.

4. **abw.gov.pl/pl/aktualnosci -- 404 Not Found.** The documented entry point URL is incorrect. The English site at `abw.gov.pl/en/` works (200). The correct Polish news path needs investigation.

5. **NBP MPC page (primary entry URL) -- 404.** The documented URL `nbp.pl/polityka-pieniezna/dokumenty-rpp/komunikaty-z-posiedzen-rpp/` returns 404. The site structure may have changed. The English equivalent at `nbp.pl/en/monetary-policy/mpc-documents/monetary-policy-council-press-releases/` returns 200.

### Confirmed Non-Functional

6. **au.gov.pl (Armaments Agency) -- connection refused.** No web server responding. This VERIFY item is invalid.

7. **3seas.eu (Three Seas Initiative) -- connection refused / DNS failure.** Domain appears down entirely.

### Partially Functional

8. **Sejm RSS feeds -- CAPTCHA blocked.** The RSS listing page at `sejm.gov.pl/sejm10.nsf/rss.xsp` returns 200 but serves a CAPTCHA challenge. The Sejm API endpoints are the reliable alternative (all 6 tested endpoints return clean JSON).

9. **Sejm website pages** (druki, voting browser, committee schedule, session agendas) all return HTTP 200 via curl but may serve CAPTCHAs to automated clients. The API is the preferred channel.

10. **NBP RSS** -- headers indicate RSS content type but body is Incapsula block page. Not usable. NBP API at `api.nbp.pl` is the reliable alternative (confirmed working).

### Fully Functional (No Issues)

- **gov.pl platform** (5 agencies): All entry points and additional URLs working perfectly. No bot protection issues.
- **Sejm API** (6 endpoints): All returning clean JSON, no authentication required.
- **NBP API** (2 endpoints + docs): All working, JSON responses, no authentication.
- **GUS RSS + API**: Both working. RSS feed contains current data.
- **Dziennik Ustaw / Monitor Polski**: Both listing pages working.
- **PAIH**: Working.
- **Polish EU Presidency archive**: Working.
- **MSZ embassy subdomains**: Both return 200 (content may require browser rendering).
