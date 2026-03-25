# Mexico — Government Source Fetch Accessibility Report
Generated: 2026-03-20

## Summary
- Total entry points tested: 40
- Directly fetchable (curl 200): 36
- Blocked/inaccessible: 1 (Senado comunicados 403)
- Bot protection on content: gob.mx serves Challenge Validation pages to automated clients (Cloudflare crypto challenge)
- RSS/Atom feeds verified working: 11 (7 Banxico + 3 PEMEX + 1 INE)
- [VERIFY] items resolved: 5

## Key Finding: gob.mx Bot Protection

All 8 gob.mx agency URLs return HTTP 200 via curl, but the actual HTML content is a **Cloudflare Challenge Validation page** (crypto challenge with JavaScript). Standard HTTP scraping will NOT retrieve real content from gob.mx. **Playwright/headless browser is required for all gob.mx sources.**

This affects: Presidencia, SRE, SEDENA, SEMAR, SSPC, SHCP, Secretaría de Economía, CNI.

## Results

### gob.mx Platform (8 agencies)

| URL | curl | Content | Extraction Method |
|---|---|---|---|
| `gob.mx/presidencia/archivo/prensa?idiom=es` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/sre/archivo/prensa` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/defensa/es/archivo/prensa` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/semar/archivo/prensa` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/sspc/archivo/prensa?idiom=es` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/shcp/archivo/prensa?idiom=es` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/se/archivo/prensa?idiom=es` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |
| `gob.mx/cni` | ✅ 200 | ❌ Challenge Validation page | **playwright_required** |

### Non-gob.mx Sources

| URL | curl | Content | Extraction Method |
|---|---|---|---|
| `gabinetedeseguridad.gob.mx/informes/` | ✅ 200 | ✅ HTML content | curl_scrape |
| `comunicacionsocial.senado.gob.mx/informacion/comunicados` | ❌ 403 | ❌ Blocked | **playwright_required** |
| `comunicacionsocial.diputados.gob.mx/` | ✅ 200 | ✅ HTML content | curl_scrape |
| `dof.gob.mx/` | ✅ 200 | ✅ HTML content (SSL OK despite documented concerns) | curl_scrape |
| `sidof.segob.gob.mx/` | ✅ 200 | ✅ HTML content | curl_scrape |
| `banxico.org.mx/publicaciones-y-prensa/...` | ✅ 200 | ✅ HTML content | curl_scrape |
| `pemex.com/saladeprensa/boletines_nacionales/...` | ✅ 200 | ✅ HTML content (SharePoint) | curl_scrape |
| `app.cfe.mx/Aplicaciones/OTROS/Boletines/Prensa?c=2` | ✅ 200 | ✅ HTML content | curl_scrape |
| `centralelectoral.ine.mx/` | ✅ 200 | ✅ HTML content (WordPress) | rss_parser (feed confirmed) |
| `scjn.gob.mx/multimedia/comunicados` | ✅ 200 | ✅ HTML content | curl_scrape |
| `embamex.sre.gob.mx/eua/index.php/es/comunicados` | ✅ 200 | ✅ HTML content | curl_scrape |
| `gaceta.diputados.gob.mx/` | ✅ 200 | ✅ HTML content | curl_scrape |
| `senado.gob.mx/66/gaceta_del_senado/` | ✅ 200 | ✅ HTML content | curl_scrape |
| `portales.sre.gob.mx/` | ✅ 200 | ✅ HTML content | curl_scrape |

### RSS/Atom Feeds

| Feed URL | Status | Content-Type | Valid |
|---|---|---|---|
| Banxico FIX exchange rate | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico TIIE | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico CETES | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico Reserves | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico Remittances | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico UDIs | ✅ 200 | `text/xml` | ✅ Valid RSS |
| Banxico Overnight Funding | ✅ 200 | `text/xml` | ✅ Valid RSS |
| PEMEX National Bulletins | ✅ 200 | `text/xml; charset=utf-8` | ✅ Valid RSS (SharePoint ListFeed) |
| PEMEX Regional Bulletins | ✅ 200 | `text/xml; charset=utf-8` | ✅ Valid RSS (SharePoint ListFeed) |
| PEMEX Speeches | ✅ 200 | `text/xml; charset=utf-8` | ✅ Valid RSS (SharePoint ListFeed) |

**All 10 documented RSS feeds are working and returning valid XML.**

## VERIFY Resolution

| Item | URL Tested | Result | Resolution |
|---|---|---|---|
| Senado RSS | `comunicacionsocial.senado.gob.mx/feed` | ❌ 403 | **No RSS available** — entire site blocks automated access |
| Senado RSS | `comunicacionsocial.senado.gob.mx/rss` | ❌ 403 | **No RSS available** |
| Diputados RSS | `comunicacionsocial.diputados.gob.mx/feed` | ❌ 404 | **No RSS available** |
| Diputados RSS | `comunicacionsocial.diputados.gob.mx/rss` | ❌ 404 | **No RSS available** |
| INE RSS | `centralelectoral.ine.mx/feed/` | ✅ 200 `application/rss+xml` | **✅ CONFIRMED — valid WordPress RSS 2.0 feed.** Add to pipeline config. |
| SCJN RSS | `scjn.gob.mx/feed` | ❌ 404 | **No RSS available** |
| SCJN RSS | `scjn.gob.mx/rss` | ❌ 404 | **No RSS available** |
| CFE RSS | `app.cfe.mx/Aplicaciones/OTROS/Boletines/feed` | ✅ 200 `text/html` | ❌ **Redirect to cfe.mx homepage** — not a feed |

## Accessibility Tiers

### Tier 1 — Direct automation (RSS feeds, no bot protection)
- **Banxico** (7 RSS feeds) — best source for automation
- **PEMEX** (3 RSS feeds) — SharePoint ListFeed
- **INE** (1 RSS feed) — WordPress, newly confirmed

### Tier 2 — curl/HTTP scraping (no bot protection, HTML content)
- **Gabinete de Seguridad** — clean HTML
- **Cámara de Diputados** (comunicación social + Gaceta) — clean HTML
- **DOF / SIDOF** — both working, SSL issue not observed
- **CFE** — custom app portal
- **SCJN** — clean HTML
- **Embamex/SRE portals** — clean HTML
- **Senado Gaceta** — working (separate from blocked comunicación social)

### Tier 3 — Headless browser required (bot protection / JavaScript)
- **All gob.mx agencies** (8 sources) — Cloudflare crypto challenge blocks all non-browser clients
- **Senado comunicación social** — 403 on automated access

## Pipeline Configuration Updates Needed

1. **Add INE RSS feed** to YAML manifest: `https://centralelectoral.ine.mx/feed/` (confirmed working)
2. **Mark all gob.mx sources as `extraction: playwright`** — curl scraping will not work
3. **Remove CFE RSS** from consideration — `/feed` redirects to homepage
4. **Remove Senado/Diputados/SCJN RSS** — confirmed nonexistent
5. **DOF SSL note may be outdated** — SSL worked fine during testing
6. **Senado comunicación social needs playwright** — 403 on standard HTTP
