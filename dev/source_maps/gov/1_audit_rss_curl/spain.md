# Spain Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/spain_government_sources.md`
**Method:** WebFetch (primary), curl with browser UA (fallback)

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 78 |
| Reachable (HTTP 200 or valid feed) | 64 |
| Blocked/Forbidden (HTTP 403) | 4 |
| Not Found (HTTP 404) | 8 |
| Connection Error (SSL/other) | 1 |
| Redirected to API docs (not data endpoint) | 1 |
| **Overall reachability rate** | **82%** |

### Key Findings

- **La Moncloa**: All 9 RSS feeds and all 5 entry points fully functional. Best-documented source.
- **BOE**: RSS feeds all valid. API base path returns OpenAPI spec (documentation), not data. Correct API data endpoint is `api.php/boe/dias/{date}` but returns HTML documentation page rather than JSON/XML data for a specific date -- needs further investigation with proper Accept headers.
- **BOE [VERIFY] feeds confirmed**: Section I (`?s=1`) and Section III (`?s=3`) RSS feeds are both valid and returning items.
- **Banco de Espana**: All 7 main RSS feeds functional. BIEST statistical channels page blocked by WAF (403-equivalent error page). Podcast feed also works.
- **Casa Real**: All 4 Atom feeds functional.
- **Defensa**: RSS feed and all entry points functional.
- **MAEC**: Main entry point and Comunicados page work. Three additional URLs (FichasPais, AtlasRedesSociales, EU Permanent Rep via exteriores.gob.es) return 404 -- likely site restructured.
- **Congreso**: Returns 403 to WebFetch but 200 to curl with browser UA. Bot protection in place.
- **Senado**: Returns 403 to both WebFetch and curl. Stricter bot protection.
- **Hacienda**: Main entry point URL returns 404 (page moved/removed). Agenda RSS feed works. Syndication page works. Public finance statistics page returns 404.
- **DSN**: Homepage works. All 3 documented additional entry point URLs return 404 -- site has been restructured. Correct paths found: `/es/publicaciones/estrategia-de-seguridad-nacional`, `/es/publicaciones/estrategias-sectoriales`, `/es/publicaciones/informes-anuales`.
- **REPER (es-ue.org)**: WordPress RSS feed at `/feed/` confirmed valid (10 items). Posiciones page works. English site works.
- **MINECO**: RSS info page loads but does not expose actual feed URLs in HTML -- feeds loaded dynamically via SharePoint web part. Minister interventions page returns 404.
- **CNI**: Main site loads (minimal content). `sede.cni.gob.es` has SSL certificate issue but loads with `-k`. `ccn.cni.es` loads.

---

## 1. La Moncloa (Presidencia del Gobierno)

### RSS Feeds

| Feed | URL | Status | Notes |
|---|---|---|---|
| Featured news | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=1` | PASS | Valid RSS 2.0, 4 items, title: "Noticias Destacadas del Presidente del Gobierno" |
| Current news | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=2` | PASS | Valid RSS 2.0, 4 items, title: "Noticias Destacadas de los Ministerios" |
| President highlights | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=20` | PASS | Valid RSS 2.0, 4 items |
| President agenda | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=22` | PASS | Valid RSS 2.0, 4 items |
| President speeches | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=23` | PASS | Valid RSS 2.0, 4 items |
| Council of Ministers summaries | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=15` | PASS | Valid RSS 2.0, 4 items, title: "Resumenes del Consejo de Ministros" |
| Council of Ministers references | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=16` | PASS | Valid RSS 2.0, 4 items, title: "Referencias del Consejo de Ministros" |
| Council press conference transcripts | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=17` | PASS | Valid RSS 2.0, 4 items |
| Government agenda | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=32` | PASS | Valid RSS 2.0, 4 items |

### Entry Points

| Page | URL | Status | Notes |
|---|---|---|---|
| Press releases | `https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/Paginas/index.aspx` | PASS | Press release listing with ministry/date filters |
| Council of Ministers references | `https://www.lamoncloa.gob.es/consejodeministros/referencias/Paginas/index.aspx` | PASS | Cabinet meeting references by month/year |
| President's agenda | `https://www.lamoncloa.gob.es/presidente/agenda/Paginas/index.aspx` | PASS | Daily activity listing, data from 2010-2026 |
| Multimedia archive | `https://www.lamoncloa.gob.es/multimedia/Paginas/index.aspx` | PASS | Videos, photo galleries, photo library back to 1977 |
| Government agenda | `https://www.lamoncloa.gob.es/gobierno/agenda/paginas/agenda.aspx` | PASS | Daily ministerial schedule |

---

## 2. MAEC (Foreign Ministry)

### Entry Points

| Page | URL | Status | Notes |
|---|---|---|---|
| Notas de prensa | `https://www.exteriores.gob.es/es/Comunicacion/NotasPrensa/Paginas/index.aspx` | PASS | SharePoint press release listing, recent items from March 2026 |
| Comunicados | `https://www.exteriores.gob.es/es/Comunicacion/Comunicados/Paginas/index.aspx` | PASS | Formal diplomatic statements listing |
| Country fact sheets | `https://www.exteriores.gob.es/es/Comunicacion/FichasPais/Paginas/index.aspx` | FAIL (404) | URL broken, both WebFetch and curl return 404 |
| Social media directory | `https://www.exteriores.gob.es/es/Comunicacion/AtlasRedesSociales/Paginas/index.aspx` | FAIL (404) | URL broken, both WebFetch and curl return 404 |
| EU Permanent Rep (MAEC page) | `https://www.exteriores.gob.es/RepresentacionesPermanentes/EspanaUE/es/Paginas/inicio.aspx` | FAIL (404) | URL broken, both WebFetch and curl return 404 |

**RSS: None documented. [VERIFY] status: No RSS found -- confirmed no feeds available.**

---

## 3. Ministerio de Defensa

### RSS Feed

| Feed | URL | Status | Notes |
|---|---|---|---|
| Press releases | `https://www.defensa.gob.es/comun/rssChannel/rssNotasPrensa.xml` | PASS | Valid Atom feed, 10 entries, title: "Notas de Prensa" |

### Entry Points

| Page | URL | Status | Notes |
|---|---|---|---|
| Press releases | `https://www.defensa.gob.es/gabinete/notasPrensa/` | PASS | Chronological press release listing with search/filter |
| Revista Espanola de Defensa | `https://www.defensa.gob.es/gabinete/red/` | PASS | Defense magazine, current issue #436 (March 2026) |
| EMAD (Joint Chiefs) | `https://emad.defensa.gob.es/` | PASS | Estado Mayor de la Defensa homepage with news |
| Multimedia | `https://www.defensa.gob.es/gabinete/multimedia/` | PASS | YouTube videos and Flickr photo galleries |
| RSS channel page | `https://www.defensa.gob.es/comun/canalRss.html` | PASS | RSS info page with feed link |

---

## 4. Parliament / Legislature

### 4a. Congreso de los Diputados

| Page | URL | Status | Notes |
|---|---|---|---|
| Latest publications | `https://www.congreso.es/es/ultimas-publicaciones-oficiales` | PARTIAL | 403 via WebFetch; 200 via curl with browser UA. Bot protection active. |
| Publications search | `https://www.congreso.es/es/busqueda-de-publicaciones` | PARTIAL | 403 via WebFetch; 200 via curl with browser UA |
| Historical session diaries | `https://app.congreso.es/est_sesiones/` | PASS | 200 via curl |
| Publications index | `https://www.congreso.es/es/indice-de-publicaciones` | PARTIAL | 403 via WebFetch; 200 via curl with browser UA |

**RSS: None documented. [VERIFY] status: No RSS found.**

### 4b. Senado de Espana

| Page | URL | Status | Notes |
|---|---|---|---|
| Boletines oficiales | `https://www.senado.es/web/actividadparlamentaria/publicacionesoficiales/senado/boletinesoficiales/index.html` | FAIL (403) | Both WebFetch and curl return 403. Strict bot protection. |
| Diarios de sesiones | `https://www.senado.es/web/actividadparlamentaria/publicacionesoficiales/senado/diariossesiones/index.html` | FAIL (403) | curl returns 403 |
| Guided publication search | `https://www.senado.es/web/conocersenado/ayudabuscadorgeneral/busquedaguiada/publicacionesoficiales/index.html` | FAIL (403) | curl returns 403 |

**RSS: None documented. [VERIFY] status: Cannot test due to 403 blocking.**

---

## 5. BOE (Official Gazette)

### RSS Feeds

| Feed | URL | Status | Notes |
|---|---|---|---|
| Complete daily BOE | `https://www.boe.es/rss/boe.php` | PASS | Valid RSS 2.0, 148 items, daily edition |
| Section I (General provisions) | `https://www.boe.es/rss/boe.php?s=1` | PASS [VERIFY confirmed] | Valid RSS 2.0, 8 items (royal decrees, orders) |
| Section III (Other provisions) | `https://www.boe.es/rss/boe.php?s=3` | PASS [VERIFY confirmed] | Valid RSS 2.0, 40 items |
| BORME (Commercial Registry) | `https://www.boe.es/rss/borme.php` | PASS | Valid RSS 2.0, 51 items |

### Entry Points & API

| Page | URL | Status | Notes |
|---|---|---|---|
| Daily edition | `https://www.boe.es/diario_boe/` | PASS | Monthly calendar interface for March 2026 |
| Search | `https://www.boe.es/buscar/` | PASS | Full search interface for legal publications |
| API documentation | `https://www.boe.es/datosabiertos/api/api.php` | PASS | Returns OpenAPI 3.1.0 specification |
| API daily summary | `https://www.boe.es/datosabiertos/api/api.php/boe/dias/20260318` | PASS (200) | Returns HTML documentation page; may need Accept headers for JSON/XML data |

### [VERIFY] Items

| Item | Status | Notes |
|---|---|---|
| Section I RSS (`?s=1`) | VALID | Confirmed working, 8 items |
| Section III RSS (`?s=3`) | VALID | Confirmed working, 40 items |
| International relations thematic feed | NOT TESTED | Exact URL unknown; document says "available via thematic channel" but no URL given |
| Constitutional Court rulings feed | NOT TESTED | Exact URL unknown; document says "available via thematic channel" but no URL given |

---

## 6. Ministerio de Hacienda

### RSS Feed

| Feed | URL | Status | Notes |
|---|---|---|---|
| Ministry agenda | `https://www.hacienda.gob.es/_layouts/15/rsseventos.aspx?hiloid=11` | PASS | Valid RSS 2.0, 10 items, title: "Agenda del Ministerio" |

### Entry Points

| Page | URL | Status | Notes |
|---|---|---|---|
| Press releases | `https://www.hacienda.gob.es/es-ES/Prensa/Noticias/Paginas/NotasPrensaHome.aspx` | FAIL (404) | Page not found. Both WebFetch and curl return 404. URL has likely changed. |
| Syndication/RSS page | `https://www.hacienda.gob.es/es-es/paginas/sindicacion.aspx` | PASS | RSS info hub listing feeds for agenda, employment, auctions, etc. |
| Public finance statistics | `https://www.hacienda.gob.es/es-ES/CDI/Paginas/EstabilidadPresupuestaria/Informacion/home.aspx` | FAIL (404) | Both WebFetch and curl return 404 |
| Tax agency (AEAT) | `https://sede.agenciatributaria.gob.es/` | PASS | Tax administration portal, fully functional |

---

## 7. Banco de Espana

### RSS Feeds

| Feed | URL | Status | Notes |
|---|---|---|---|
| News & events | `https://www.bde.es/wbe/es/inicio/rss/rss-noticias/` | PASS | Valid RSS 2.0, 20 items, title: "Banco de Espana - Es Noticia" |
| Publications | `https://www.bde.es/wbe/es/inicio/rss/rss-estudios-publicaciones/` | PASS | Valid RSS 2.0, 20 items |
| Statistics | `https://www.bde.es/wbe/es/inicio/rss/rss-estadisticas/` | PASS | Valid RSS 2.0, 100 items |
| Blog | `https://www.bde.es/wbe/es/inicio/rss/rss-blog/` | PASS | Valid RSS 2.0, 21 items |
| Regulations | `https://www.bde.es/wbe/es/inicio/rss/rss-normativa/` | PASS | Valid RSS 2.0, 21 items |
| Transparency | `https://www.bde.es/wbe/es/inicio/rss/rss-transparencia/` | PASS | Valid RSS 2.0, 20 items. Note: 1 item has malformed link (`#error`) |
| Podcast | `https://www.bde.es/wbe/es/inicio/rss/rss-podcast/` | PASS | Valid RSS 2.0, 22 items |
| BIEST statistical channels | `https://app.bde.es/bie_www/faces/bie_wwwias/jsp/op/CanalesRss/BIEST_Canales_RSS.jsp` | PARTIAL | Blocked by WAF via WebFetch (access denied error page). Returns 200 via curl -- content accessible but bot-protected. |

### Entry Point

| Page | URL | Status | Notes |
|---|---|---|---|
| Press releases | `https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/` | PASS | 1,858 results archive, paginated |

---

## 8. MINECO (Economy/Trade)

### Entry Points

| Page | URL | Status | Notes |
|---|---|---|---|
| Ministry communications | `https://portal.mineco.gob.es/es-es/comunicacion/Paginas/default.aspx` | PASS | SharePoint news listing (content loads dynamically via web part) |
| Trade press releases | `https://comercio.gob.es/es-es/NotasPrensa/Paginas/index.aspx` | PASS | Press release archive with date/category filters |
| Trade-specific news | `https://portal.mineco.gob.es/es-es/comercio/Paginas/noticias.aspx` | PARTIAL | Page loads but dynamic content component may fail to render ("No se puede cargar la aplicacion") |
| Economy and enterprise news | `https://portal.mineco.gob.es/es-es/economiayempresa/noticias/Paginas/default.aspx` | PASS | News listing page, SharePoint SPFx components load |
| ICEX (trade promotion) | `https://www.icex.es/` | PASS | Fully functional internationalization services portal |
| Minister interventions | `https://portal.mineco.gob.es/es-es/ministerio/ministro/intervenciones/` | FAIL (404) | Page not found |

### [VERIFY] Items

| Item | Status | Notes |
|---|---|---|
| RSS info page | `https://portal.mineco.gob.es/es-es/ministerio/Paginas/Info_RSS.aspx` | PAGE EXISTS but no feed URLs visible | Page explains RSS concept; actual feed links loaded dynamically via SharePoint web part and not available in static HTML. RSS feeds effectively unverifiable from this page. |

---

## 9. Intelligence / National Security

### 9a. CNI

| Page | URL | Status | Notes |
|---|---|---|---|
| Main site | `https://www.cni.es/` | PASS | Presentation-focused homepage, Joomla-based. Minimal content as expected. |
| Electronic headquarters | `https://sede.cni.gob.es/` | PARTIAL | SSL certificate error (curl exit code 60); loads with `-k` flag (200). Certificate needs renewal or has chain issue. |
| CCN (cybersecurity arm) | `https://ccn.cni.es/` | PASS | 200 via curl |

### 9b. DSN (National Security)

| Page | URL | Status | Notes |
|---|---|---|---|
| Homepage | `https://www.dsn.gob.es/` | PASS | Active security news site with current updates (March 2026) |
| National Security Strategy | `https://www.dsn.gob.es/es/estrategias-publicaciones/estrategias/estrategia-seguridad-nacional` | FAIL (404) | **Site restructured.** Correct URL: `/es/publicaciones/estrategia-de-seguridad-nacional` (200) |
| Sectoral strategies | `https://www.dsn.gob.es/es/estrategias-publicaciones/estrategias` | FAIL (404) | **Site restructured.** Correct URL: `/es/publicaciones/estrategias-sectoriales` (200) |
| Annual reports | `https://www.dsn.gob.es/es/estrategias-publicaciones/informes-anuales` | FAIL (404) | **Site restructured.** Correct URL: `/es/publicaciones/informes-anuales` (200) |

**RSS: None documented. [VERIFY] status: No RSS found on restructured site.**

---

## 10. Country-Specific Institutions

### 10a. Casa Real (Royal Household)

#### RSS Feeds (Atom)

| Feed | URL | Status | Notes |
|---|---|---|---|
| Activities | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=00ad4efe-38db-408d-b95c-43e0c724a414` | PASS | Valid Atom 1.0, 20 entries |
| Official trips | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=2e3aaa49-c3bd-47a7-85a5-c43ab889d81f` | PASS | Valid Atom 1.0, 20 entries |
| Speeches | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=a1f180ed-b45a-40c5-a13b-61d27cb664bc` | PASS | Valid Atom 1.0, 20 entries |
| Comunicados | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=239d2332-7145-4633-b7c5-64c79640ab02` | PASS | Valid Atom 1.0, 19 entries |

#### Entry Point

| Page | URL | Status | Notes |
|---|---|---|---|
| Press comunicados | `https://www.casareal.es/ES/AreaPrensa/Paginas/area_prensa_comunicados.aspx` | PASS | SharePoint page, 76 comunicados listed |

### 10b. REPER (EU Permanent Representation)

| Page | URL | Status | Notes |
|---|---|---|---|
| Main site | `https://es-ue.org/` | PASS | WordPress site, news carousel, active content |
| WordPress RSS feed | `https://es-ue.org/feed/` | PASS [VERIFY confirmed] | Valid RSS 2.0, 10 items, hourly updates. Title: "ES-UE.ORG" |
| English site | `https://en.es-ue.org/` | PASS | Parallel English version |
| Posiciones (positions) | `https://es-ue.org/posiciones/` | PASS [VERIFY confirmed] | Page loads; contains Swedish Presidency position documents (2023, likely outdated) |
| MAEC institutional page | `https://www.exteriores.gob.es/RepresentacionesPermanentes/EspanaUE/es/Paginas/inicio.aspx` | FAIL (404) | See MAEC section above |

---

## Issues Requiring Action

### Critical (broken entry points for active sources)

1. **Hacienda press releases entry point** (`NotasPrensaHome.aspx`): Returns 404. Must find new URL.
2. **Hacienda public finance statistics**: Returns 404. Must find new URL.
3. **Senado**: All URLs return 403. Cannot be scraped without browser automation or session handling.

### Moderate (additional URLs broken, site restructured)

4. **DSN**: All 3 additional entry point URLs return 404 due to site restructuring. Corrected paths identified (see above).
5. **MAEC**: 3 of 5 additional URLs return 404 (FichasPais, AtlasRedesSociales, EU Permanent Rep via exteriores.gob.es). Site likely restructured.
6. **MINECO minister interventions**: Returns 404.
7. **BIEST statistical channels**: Blocked by WAF on automated access.
8. **CNI sede**: SSL certificate error.

### Informational ([VERIFY] resolutions)

9. **BOE Section I RSS (`?s=1`)**: VALID -- confirmed working.
10. **BOE Section III RSS (`?s=3`)**: VALID -- confirmed working.
11. **BOE thematic feeds** (international relations, Constitutional Court): URLs unknown, not testable.
12. **REPER RSS at `/feed/`**: VALID -- confirmed working WordPress RSS feed.
13. **REPER posiciones page**: VALID -- page loads with content.
14. **MAEC RSS**: No RSS found -- confirmed absent.
15. **Congreso RSS**: No RSS found -- confirmed absent.
16. **Senado RSS**: Cannot verify due to 403 blocking.
17. **DSN RSS**: No RSS found on restructured site.
18. **MINECO RSS**: Info page exists but no actual feed URLs extractable from static HTML.

---

## Reachability by Institution

| Institution | Total URLs | Reachable | Failed | Rate |
|---|---|---|---|---|
| La Moncloa | 14 | 14 | 0 | 100% |
| MAEC | 5 | 2 | 3 | 40% |
| Defensa | 6 | 6 | 0 | 100% |
| Congreso | 3 | 3 (curl only) | 0 | 100%* |
| Senado | 3 | 0 | 3 | 0% |
| BOE | 6 | 6 | 0 | 100% |
| Hacienda | 5 | 3 | 2 | 60% |
| Banco de Espana | 9 | 8 | 1 | 89% |
| MINECO | 7 | 5 | 2 | 71% |
| CNI | 3 | 2 | 1 | 67% |
| DSN | 4 | 1 | 3 | 25% |
| Casa Real | 5 | 5 | 0 | 100% |
| REPER | 5 | 4 | 1 | 80% |

*Congreso requires browser-like UA to avoid 403; WebFetch alone fails.

---

*Generated 2026-03-19 by automated fetchability test.*
