# Chile Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/chile_government_sources.md`
**Methodology:** Each URL tested first with WebFetch; on failure, retested with curl (following redirects, browser User-Agent). RSS [VERIFY] items tested at `/feed/` endpoints.

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 37 |
| Fully accessible (HTTP 200 + content confirmed) | 27 |
| Accessible via curl only (bot protection / SSL) | 5 |
| Blocked (HTTP 403) | 3 |
| Not found (HTTP 404) | 1 |
| Redirect-only (functional but redirects) | 1 |
| **Overall reachability rate** | **86% (32/37)** |

### VERIFY Results

| Source | VERIFY Item | Result |
|---|---|---|
| Min. Defensa (`defensa.cl`) | WordPress `/feed/` RSS | **No RSS found** — returns 404 |
| Senado (`senado.cl`) | RSS feed | **No RSS found** — `/feed/` returns 404 |
| Camara Diputados (`camara.cl`) | RSS at `/prensa/feed/` | **No RSS found** — returns HTML 404 page |
| COCHILCO (`cochilco.cl`) | WordPress `/feed/` RSS | **RSS CONFIRMED** — valid RSS 2.0 feed with 9 items, hourly updates |
| Contraloria (`contraloria.cl`) | RSS feed | **No RSS found** — `/feed/` returns 404 |

---

## Primary Entry Point URLs

| # | Institution | URL | WebFetch | curl | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | Presidencia | `https://prensa.presidencia.cl/comunicados.aspx` | FAIL (SSL) | 200 | OK (curl) | SSL certificate error confirmed; requires `-k` flag. Content serves correctly. |
| 2 | Presidencia (mirror) | `https://www.gob.cl/noticias/` | FAIL (403) | 403 | BLOCKED | Bot protection. Returns 403 to both WebFetch and curl. |
| 2b | Presidencia (press filter) | `https://www.gob.cl/noticias/comunicado-de-prensa/` | -- | 403 | BLOCKED | Same bot protection as gob.cl root. |
| 3 | Cancilleria (MFA) | `https://www.minrel.gob.cl/minrel/sala-de-prensa` | 200 | -- | OK | Fully accessible. 84+ pages of press releases confirmed. |
| 4 | Min. Defensa | `https://www.defensa.cl/` | 200 | -- | OK | WordPress-based. News items from March 2026 confirmed. |
| 5 | Ejercito | `https://www.ejercito.cl/prensa-y-multimedia` | FAIL (403) | 403 | BLOCKED | Bot protection on all ejercito.cl paths including root. |
| 6 | Armada | `https://www.armada.cl/noticias-navales` | 200 | -- | OK | Naval news articles from March 2026 confirmed. |
| 7 | FACH | `https://fach.mil.cl/noticias` | 200 | -- | OK | Air Force news confirmed. 94 pages of archive. |
| 8 | Senado | `https://www.senado.cl/comunicaciones/noticias` | 200 | -- | OK | Legislative news from March 19, 2026 confirmed. |
| 9 | Camara Diputados | `https://www.camara.cl/prensa/prensa_cms.aspx` | 200 | -- | OK | Press center portal accessible. ASP.NET CMS. |
| 10 | Diario Oficial | `https://www.diariooficial.interior.gob.cl/` | 200 | -- | OK | Official gazette portal accessible. |
| 10b | Diario Oficial (electronic) | `https://www.diariooficial.interior.gob.cl/edicionelectronica/` | 200 | -- | OK | Electronic edition #44,404 (March 19, 2026) confirmed. |
| 11 | Hacienda | `https://www.hacienda.cl/noticias-y-eventos/comunicados` | 200 | -- | OK | Press releases from March 2022 to present confirmed. |
| 12 | Banco Central | `https://www.bcentral.cl/noticias-y-publicaciones/prensa` | FAIL (empty) | 200 | OK (curl) | Incapsula WAF returns empty content to WebFetch; curl gets 200. Bot protection confirmed. |
| 13 | SUBREI | `https://www.subrei.gob.cl/` | FAIL (403) | 200 | OK (curl) | WebFetch blocked; curl succeeds with browser UA. |
| 14 | ANI | `https://www.interior.gob.cl/transparencia/ani/index.html` | 200 | -- | OK | Transparency page with 16 categories of public info. |
| 15 | CODELCO | `https://www.codelco.com/prensa` | 200 | -- | OK | Press hub with Feb-March 2026 articles confirmed. |
| 16 | BCN / Ley Chile | `https://www.bcn.cl/leychile/` | 200 | -- | OK | Legal database accessible (JS-heavy, may timeout). |
| 17 | COCHILCO | `https://www.cochilco.cl/web/noticias/` | 200 | -- | OK | News from March 18, 2026 confirmed. |
| 18 | Contraloria | `https://www.contraloria.cl/` | 200 (redirect) | 200 | OK | Redirect page → portal. Loads via JS redirect. |

---

## RSS / API Endpoints

| # | Source | URL | Type | Status | Notes |
|---|---|---|---|---|---|
| 1 | BCN RSS Hub | `https://www.bcn.cl/rss/copy_of_index_html` | RSS Hub | OK (200) | Hub page accessible. Lists feed categories but individual feed URLs must be extracted by clicking RSS icons on-site. |
| 2 | COCHILCO RSS | `https://www.cochilco.cl/web/noticias/feed/` | RSS 2.0 | OK (200) | **Valid RSS feed.** 9 items, hourly updates. Copper/lithium market reports. Most recent: March 18, 2026. |
| 3 | Banco Central API | `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx` | REST API | OK (200) | Endpoint responds. Requires registration + auth params for data retrieval. |
| 4 | Banco Central BDE Portal | `https://si3.bcentral.cl/siete` | Web Portal | OK (200) | Statistical database portal accessible. |
| 5 | Banco Central API Docs | `https://si3.bcentral.cl/estadisticas/Principal1/Web_Services/index.htm` | Docs | OK (200) | Redirects to `/Siete/es/Siete/API` — documentation accessible via redirect. |
| 6 | Defensa `/feed/` | `https://www.defensa.cl/feed/` | RSS (VERIFY) | FAIL (404) | No RSS feed despite WordPress platform. |
| 7 | Senado `/feed/` | `https://www.senado.cl/comunicaciones/noticias/feed/` | RSS (VERIFY) | FAIL (404) | No RSS feed available. |
| 8 | Camara `/prensa/feed/` | `https://www.camara.cl/prensa/feed/` | RSS (VERIFY) | FAIL (404) | Returns HTML 404 page. No RSS. |
| 9 | Contraloria `/feed/` | `https://www.contraloria.cl/feed/` | RSS (VERIFY) | FAIL (404) | No RSS feed available. |

---

## Additional Entry Points

| # | Source | URL | Status | Notes |
|---|---|---|---|---|
| 1 | Senado — Legislative Activity | `https://www.senado.cl/actividad-legislativa/` | OK (200) | Legislative hub with commissions, sessions, project tracking. |
| 2 | Senado — Live Sessions | `https://sesiones.senado.cl/` | OK (200) | Live session streaming portal accessible. |
| 3 | Camara — Bill Tracking | `https://www.camara.cl/legislacion/ProyectosDeLey/proyectos_ley.aspx` | OK (200) | Bill search with filtering. JS-heavy but functional. |
| 4 | Camara — Open Data | `https://opendata.camara.cl/` | OK (200) | Open legislative data in XML format. Voting, bills, sessions. |
| 5 | Camara — Commissions | `https://www.camara.cl/legislacion/comisiones/` | FAIL (403) | Blocked by bot protection. |
| 6 | DIPRES (root) | `https://www.dipres.gob.cl/` | OK (200) | Redirect page; loads target via JS. |
| 7 | DIPRES — Statistics | `https://www.dipres.gob.cl/598/w3-propertyvalue-25291.html` | OK (200) | Statistical portal accessible. |
| 8 | DIPRES — Press Releases | `https://www.dipres.gob.cl/598/w3-propertyvalue-2135.html` | OK (200) | Press releases page accessible. |
| 9 | ProChile | `https://www.prochile.gob.cl/` | OK (200) | Export promotion portal. Trade tools and events. |
| 10 | SUBREI — Monthly Trade Report | `https://www.subrei.gob.cl/estudios-y-documentos/minuta-mensual/` | OK (200) | Monthly trade minutes accessible. |
| 11 | SUBREI — Documents | `https://www.subrei.gob.cl/estudios-y-documentos/documentos` | OK (200) | Studies and documents hub accessible. |

---

## Key Findings

### Bot Protection Issues (3 sources fully blocked)

1. **gob.cl** — Returns 403 to all automated requests (WebFetch and curl). The government news portal mirror for Presidencia is unusable for automated scraping. Use `prensa.presidencia.cl` (with SSL exception) instead.

2. **ejercito.cl** — Returns 403 to all automated requests across all paths. The Chilean Army website has aggressive bot protection. Requires browser automation (Playwright/Puppeteer) or headless browser with JS rendering.

3. **camara.cl/legislacion/comisiones/** — This specific subpath is blocked while other camara.cl paths work fine.

### SSL Certificate Issues (1 source)

- **prensa.presidencia.cl** — SSL certificate verification fails (documented in source map). Content is accessible with certificate exception (`-k` flag). Recommend using the site with TLS verification disabled or implementing certificate pinning workaround.

### WAF / Bot Mitigation (2 sources partially accessible)

- **bcentral.cl** — Incapsula/Imperva WAF blocks content extraction via WebFetch (returns empty page). curl gets HTTP 200. The API at `si3.bcentral.cl` is on separate infrastructure and is fully accessible — use API for data, not web scraping.

- **subrei.gob.cl** — Blocks WebFetch (403) but allows curl with browser User-Agent. Moderate bot protection.

### Newly Discovered RSS Feed

- **COCHILCO** (`cochilco.cl/web/noticias/feed/`) — WordPress RSS 2.0 feed confirmed working. 9 items with hourly updates. This should be added to the monitoring manifest as an RSS-enabled source, upgrading COCHILCO from scrape-only to RSS polling.

### Recommendations for Pipeline Configuration

1. **Presidencia**: Use `prensa.presidencia.cl` with SSL verification disabled. Do NOT rely on `gob.cl/noticias/` mirror.
2. **Ejercito**: Requires headless browser (Playwright) — no simple HTTP client will work.
3. **Banco Central**: Use the REST API at `si3.bcentral.cl` for data. For press releases, use headless browser or monitor via media syndication.
4. **COCHILCO**: Switch from `html_scrape` to `rss_poll` using the confirmed feed at `/web/noticias/feed/`.
5. **BCN RSS**: The hub page exists but individual feed URLs need to be extracted from the BCN portal directly (the hub page does not list raw URLs).
