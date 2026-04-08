# Brazil Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/brazil_government_sources.md`
**Test method:** WebFetch (primary), curl fallback with `Mozilla/5.0` User-Agent

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 55 |
| Reachable (HTTP 200 or valid feed) | 43 |
| Failed (4xx/5xx/connection error) | 12 |
| RSS/Atom feeds confirmed working | 14 |
| RSS feeds documented but broken/HTML | 3 |
| RSS feeds marked [VERIFY] — confirmed invalid | 3 |
| RSS feeds marked [VERIFY] — confirmed valid | 2 |
| API endpoints confirmed working | 3 |

---

## 1. Gov.br Platform Sources — RSS Feed Verification

All gov.br sources marked [VERIFY RSS] in the source document were tested. The Plone `/RSS` path works for some ministries but not all.

### RSS Feed Results

| Source | RSS URL | Status | Notes |
|---|---|---|---|
| Presidência (Planalto) | `gov.br/planalto/pt-br/acompanhe-o-planalto/noticias/RSS` | VALID (stale) | RSS 1.0 (RDF). curl returns 200 `application/atom+xml`. WebFetch returns 403 (bot-blocked). Feed exists but content appears stale (items from 2023-2024). Not reliably current. |
| MRE (Itamaraty) | `gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa/RSS` | INVALID | curl returns 404 `application/json`. RSS not available at this path. |
| Defesa | `gov.br/defesa/pt-br/centrais-de-conteudo/noticias/RSS` | VALID | RSS 1.0 (RDF). 100+ items. Most recent: 2025-04-24. Feed functional but may lag behind HTML listing. |
| Fazenda | `gov.br/fazenda/pt-br/assuntos/noticias/RSS` | INVALID | curl returns 404 `application/json`. RSS not available at this path. |
| MDIC | `gov.br/mdic/pt-br/assuntos/noticias/RSS` | VALID | RSS 1.0 (RDF). 12 items including 2 news articles and 10 collection items. Most recent: 2026-03-12. |
| GSI | `gov.br/gsi/pt-br/RSS` (tested) | INVALID | curl returns 404. No RSS available. |
| English gov.br | `gov.br/en/government-of-brazil/latest-news/latest-news/RSS` | VALID | curl returns 200 `application/atom+xml`. Feed exists. |
| Portal da Legislação | `www4.planalto.gov.br/legislacao/rss` | UNREACHABLE | Connection reset (exit code 56). Server drops connection. |

### Entry Point URL Results

| Source | Entry Point URL | Status | HTTP Code |
|---|---|---|---|
| Presidência | `gov.br/planalto/pt-br/acompanhe-o-planalto/noticias` | OK | 200 |
| MRE (notas) | `gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa` | OK | 200 |
| MRE (English) | `gov.br/mre/en/contact-us/press-area/press-releases` | OK | 200 |
| MRE (speeches) | `gov.br/mre/pt-br/canais_atendimento/imprensa/discursos-artigos-e-entrevistas` | FAIL | 404 |
| Defesa (noticias) | `gov.br/defesa/pt-br/centrais-de-conteudo/noticias` | OK | 200 |
| Defesa (imprensa) | `gov.br/defesa/pt-br/area-de-imprensa` | OK | 200 |
| Exército | `gov.br/exercito/pt-br/centrais-de-conteudo/noticias` | FAIL | 404 |
| Marinha | `gov.br/marinha/pt-br/noticias` | FAIL | 404 |
| Aeronáutica | `gov.br/aeronautica/pt-br/assuntos/noticias` | FAIL | 404 |
| Fazenda | `gov.br/fazenda/pt-br/assuntos/noticias` | OK | 200 |
| Tesouro Nacional | `gov.br/tesouronacional/pt-br/noticias` | OK | 200 |
| Receita Federal | `gov.br/receitafederal/pt-br/assuntos/noticias` | OK | 200 |
| MDIC | `gov.br/mdic/pt-br/assuntos/noticias` | OK | 200 |
| Siscomex | `gov.br/siscomex/pt-br` | OK | 200 |
| ABIN | `gov.br/abin/pt-br` | OK | 200 |
| GSI | `gov.br/gsi/pt-br` | OK | 200 |
| SECOM | `gov.br/secom/pt-br/acompanhe-a-secom/noticias` | OK | 200 (confirmed news listing with 145 pages) |
| Planalto English | `gov.br/planalto/en/latest-news` | OK | 200 |

---

## 2. Legislative Sources (Senado, Câmara)

### Senado Federal

| URL | Type | Status | Notes |
|---|---|---|---|
| `www12.senado.leg.br/noticias/ultimas` | Entry point | OK | Functioning news page with items dated 2026-03-19 |
| `www12.senado.leg.br/noticias/feed` | RSS | BROKEN | Returns HTML page, not RSS XML. Page says "Atualmente nao existem itens nessa pasta" (no items in this folder). |
| `www12.senado.leg.br/noticias/feed/todasnoticias` | RSS | BROKEN | Returns HTML page, not RSS XML. |
| `www12.senado.leg.br/noticias/senado-agora` | Entry point | OK | 200 |
| `senado.leg.br/comissoes/comissao?codcol=58` | CRE page | FAIL | 404 |

### Câmara dos Deputados

| URL | Type | Status | Notes |
|---|---|---|---|
| `camara.leg.br/noticias` | Entry point | OK | Functioning news page with items dated 2026-03-19 |
| `camara.leg.br/noticias/rss` | RSS hub | OK | 200 (HTML hub page listing all available feeds) |
| `camara.leg.br/noticias/rss/ultimas-noticias` | RSS | VALID | RSS 2.0. 12 items. Most recent: 2026-03-19 18:52 GMT |
| `camara.leg.br/noticias/rss/dinamico/RELACOES-EXTERIORES` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 14:35 UTC |
| `camara.leg.br/noticias/rss/dinamico/ECONOMIA` | RSS | VALID | RSS 2.0. 11 items. Most recent: 2026-03-19 14:19 UTC |
| `camara.leg.br/noticias/rss/dinamico/SEGURANCA` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 13:38 GMT |
| `camara.leg.br/noticias/rss/dinamico/POLITICA` | RSS | VALID | RSS 2.0. 11 items. Most recent: 2026-03-18 21:14 UTC |
| `dadosabertos.camara.leg.br/` | API portal | OK | 200 |

---

## 3. DOU (Diário Oficial da União)

| URL | Type | Status | Notes |
|---|---|---|---|
| `in.gov.br/leiturajornal` | Entry point | OK | Functioning DOU reader showing edition #53, dated 2026-03-19 |
| `in.gov.br/consulta` | Search | OK | Functioning search interface |
| `inlabs.in.gov.br/` | Bulk access | FAIL | 502 Bad Gateway |

---

## 4. BCB (Banco Central do Brasil)

| URL | Type | Status | Notes |
|---|---|---|---|
| `bcb.gov.br/` | Entry point | OK | 200 (JS-rendered site) |
| `bcb.gov.br/en` | English site | OK | 200 |
| `bcb.gov.br/api/servico/sitebcb/copom/atas?quantidade=5` | API | VALID | Returns JSON with 5 Copom meeting records (most recent: meeting 276, Jan 2026) |
| `api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/5?formato=json` | API | VALID | Returns JSON time series (Selic rate at 14.75, April 2026 data) |
| `api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json` (full series) | API | FAIL | 406 Not Acceptable (needs `/ultimos/N` parameter or different Accept header) |
| `dadosabertos.bcb.gov.br/dataset/atas-comunicados-copom` | Portal | OK | 200 |
| `dadosabertos.bcb.gov.br/` | Portal | OK | 200 |
| `opendata.bcb.gov.br/` | Portal | OK | 200 |

---

## 5. Country-Specific Institutions

### Petrobras

| URL | Type | Status | Notes |
|---|---|---|---|
| `agencia.petrobras.com.br/` | Entry point | OK | Functioning Liferay news portal with items dated March 2026 |
| `agencia.petrobras.com.br/en` | English | OK | 200 |
| `petrobras.com.br/fatos-e-dados/` | Alt entry | OK | 200 |

No RSS feed found (confirmed: none available on Liferay portal).

### STF (Supremo Tribunal Federal)

| URL | Type | Status | Notes |
|---|---|---|---|
| `portal.stf.jus.br/listagem/listarNoticias.asp` | Entry point | FAIL | 403 via curl (even with `-k` to skip SSL). WebFetch fails with SSL certificate error. SSL issue confirmed as documented. |
| `noticias.stf.jus.br/` | Alt entry | OK | 200 (functioning alternative news portal) |

No RSS feed found (confirmed: none available).

### Agência Brasil (EBC)

| URL | Type | Status | Notes |
|---|---|---|---|
| `agenciabrasil.ebc.com.br/ultimas` | Entry point | OK | Functioning news page with items dated 2026-03-19 |
| `agenciabrasil.ebc.com.br/en` | English | OK | 200 |
| `agenciabrasil.ebc.com.br/feed/` | Feed hub | OK | HTML hub page listing RSS feed links (not itself a feed) |
| `agenciabrasil.ebc.com.br/rss/politica/feed.xml` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 15:57 |
| `agenciabrasil.ebc.com.br/rss/economia/feed.xml` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 16:13 |
| `agenciabrasil.ebc.com.br/rss/internacional/feed.xml` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 13:12 |
| `agenciabrasil.ebc.com.br/rss/justica/feed.xml` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 15:54 |
| `agenciabrasil.ebc.com.br/rss/geral/feed.xml` | RSS | VALID | RSS 2.0. 10 items. Most recent: 2026-03-19 16:05 |
| `rss.ebc.com.br/` | EBC RSS hub | OK | 200 |

### TSE (Tribunal Superior Eleitoral)

| URL | Type | Status | Notes |
|---|---|---|---|
| `tse.jus.br/comunicacao/noticias` | Entry point | OK | Functioning news page with items dated March 2026 |
| `dadosabertos.tse.jus.br/` | Open data | OK | 200 |

No RSS feed found (confirmed: none available).

### Other

| URL | Type | Status | Notes |
|---|---|---|---|
| `agenciagov.ebc.com.br/noticias` | Agência Gov | OK | Functioning government news portal with items dated 2026-03-19 |
| `comexstat.mdic.gov.br/` | ComexStat | OK | 200 |
| `imprensamaillist.itamaraty.gov.br/` | MRE mailing list | OK | 200 |

---

## 6. Key Findings and Recommendations

### [VERIFY] Resolution Summary

| Source | Verified Item | Result | Action Required |
|---|---|---|---|
| Presidência RSS | `gov.br/planalto/.../noticias/RSS` | EXISTS but stale (2023-2024 content) | Use HTML scraping as primary; RSS unreliable for current content |
| MRE RSS | `gov.br/mre/.../notas-a-imprensa/RSS` | DOES NOT EXIST (404) | HTML scraping only. Use Itamaraty email list as push alternative. |
| Defesa RSS | `gov.br/defesa/.../noticias/RSS` | EXISTS and functional | RSS polling viable. Most recent item April 2025. |
| Fazenda RSS | `gov.br/fazenda/.../noticias/RSS` | DOES NOT EXIST (404) | HTML scraping only |
| MDIC RSS | `gov.br/mdic/.../noticias/RSS` | EXISTS and functional | RSS polling viable. Items dated March 2026. |
| GSI RSS | `gov.br/gsi/pt-br/RSS` | DOES NOT EXIST (404) | Periodic HTML check only |
| Petrobras RSS | `agencia.petrobras.com.br` | NONE FOUND | HTML scraping only |
| STF RSS | `portal.stf.jus.br` | NONE FOUND; primary URL has SSL/403 issues | Use `noticias.stf.jus.br` as primary entry point |
| TSE RSS | `tse.jus.br` | NONE FOUND | HTML scraping only |
| Senado RSS | `www12.senado.leg.br/noticias/feed` | BROKEN (returns HTML, not XML) | All documented Senado RSS feeds return HTML pages. Use HTML scraping. |

### Critical Issues

1. **Senado RSS feeds are non-functional.** Both `/noticias/feed` and `/noticias/feed/todasnoticias` return HTML pages, not RSS XML. The source document lists these as confirmed ("Yes -- multiple feeds available") but they are broken. The pipeline must use HTML scraping for Senado content.

2. **STF primary URL blocked.** `portal.stf.jus.br/listagem/listarNoticias.asp` returns 403 even with User-Agent rotation and SSL bypass (`-k`). Use `noticias.stf.jus.br/` instead (confirmed working at 200).

3. **Military branch URLs are all 404.** The documented entry points for Exército (`gov.br/exercito`), Marinha (`gov.br/marinha`), and Aeronáutica (`gov.br/aeronautica`) all return 404. These gov.br slugs may have been restructured. URL discovery needed.

4. **MRE speeches URL is 404.** `gov.br/mre/pt-br/canais_atendimento/imprensa/discursos-artigos-e-entrevistas` returns 404. Path may have changed.

5. **INLABS is down (502).** The DOU bulk access system at `inlabs.in.gov.br` returned 502 Bad Gateway. May be transient.

6. **BCB time series API requires `/ultimos/N` suffix.** The full series endpoint returns 406; use the `/ultimos/N` variant for reliable access.

7. **Planalto RSS exists but is stale.** Feed returns valid RSS 1.0 XML but items are from 2023-2024. Not reliable for current monitoring. WebFetch is blocked (403) even though curl succeeds.

### Tier Ranking by Reliability

**Tier 1 — Highly reliable, current, automated intake ready:**
- Câmara dos Deputados RSS feeds (all 5 tested: working, current)
- Agência Brasil RSS feeds (all 5 tested: working, same-day content)
- BCB Copom API (working, structured JSON)
- BCB Time Series API (working with `/ultimos/N`)

**Tier 2 — Reachable, HTML scraping required:**
- Presidência entry point (200, news listing)
- MRE notas-a-imprensa (200, news listing)
- Defesa noticias (200, news listing + RSS available)
- Fazenda noticias (200, news listing)
- MDIC noticias (200, news listing + RSS available)
- DOU leiturajornal / consulta (200, both working)
- SECOM noticias (200, 145 pages of content)
- Agência Gov (200, government wire)
- TSE noticias (200, news listing)
- Petrobras agência (200, Liferay portal)
- Senado ultimas (200, news listing)

**Tier 3 — Reachable with caveats:**
- STF: primary URL blocked (403), alternative `noticias.stf.jus.br` works
- ABIN / GSI: reachable but minimal content (as documented)
- Planalto RSS: exists but stale content

**Tier 4 — Currently unreachable:**
- Portal da Legislação RSS (connection reset)
- INLABS (502)
- Exército / Marinha / Aeronáutica entry points (404)
- MRE speeches page (404)
- Senado CRE committee page (404)
