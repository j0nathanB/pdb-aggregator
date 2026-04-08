# Official Government Sources Supplement: SPAIN

**Primary language of political discourse: Spanish**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Spain (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Spain. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Spain's government web infrastructure is decentralized compared to countries like Mexico that use a unified portal. Each ministry and constitutional body operates its own domain and content management system — most built on SharePoint or custom CMS platforms under the `gob.es` top-level domain. La Moncloa (the seat of government) serves as the primary communications hub for executive-level announcements, including a centralized press release archive filterable by ministry. The Boletín Oficial del Estado (BOE) stands out as the most technically mature government source, offering a full REST API, multiple RSS feeds, and structured open data — making it the most pipeline-friendly government endpoint in Spain. Autonomous constitutional bodies (Banco de España, Congreso, Senado, Casa Real) maintain fully independent web infrastructure with varying levels of machine-readability.

---

## 1. OFFICIAL GOVERNMENT SOURCES: SPAIN

### 1.1 Head of Government — La Moncloa (Presidencia del Gobierno)

| Field | Detail |
|---|---|
| **Institution** | Presidencia del Gobierno / La Moncloa |
| **Domain** | `lamoncloa.gob.es` |
| **Entry Point URL** | `https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/Paginas/index.aspx` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Featured news: `/paginas/rss.aspx?tipo=1`. Current news: `/paginas/rss.aspx?tipo=2`. President highlights: `/paginas/rss.aspx?tipo=20`. President speeches: `/paginas/rss.aspx?tipo=23`. Council of Ministers summaries: `/paginas/rss.aspx?tipo=15`. Council of Ministers references: `/paginas/rss.aspx?tipo=16`. Post-Council press conference transcripts: `/paginas/rss.aspx?tipo=17`. |
| **Language** | Spanish (primary); English section available at `/lang/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Council of Ministers meets weekly (typically Tuesdays). Presidential statements, bilateral meeting readouts, and EU summit communiqués published same-day. |
| **Content Format** | HTML (SharePoint-based). Press releases organized by ministry. Some PDF attachments for formal agreements and Council of Ministers references. |
| **Extraction Method** | RSS feeds for structured polling (7 feeds covering distinct content types). HTML scraping of the press release archive with ministry-level filtering via query parameters. |
| **Editorial Orientation** | Official government position. All content produced by the Secretaría de Estado de Comunicación. Framing reflects PSOE-Sumar coalition policy priorities. |
| **Why This Source** | The single authoritative source for presidential statements, Council of Ministers decisions, and government-level policy announcements. The press archive aggregates releases from all ministries, making it a central hub. Council of Ministers post-session references provide the most comprehensive record of executive decisions. |
| **Access Notes** | No paywall, no authentication required. SharePoint-based infrastructure. The press release archive supports filtering by ministry, month, and year — date range extends back to 2006. Newsletter subscription available at `/serviciosdeprensa/newsletter/`. |

**Additional entry points:**
- Council of Ministers references: `https://www.lamoncloa.gob.es/consejodeministros/referencias/Paginas/index.aspx`
- President's agenda: `https://www.lamoncloa.gob.es/presidente/agenda/Paginas/index.aspx`
- Multimedia archive: `https://www.lamoncloa.gob.es/multimedia/Paginas/index.aspx`
- Government agenda: `https://www.lamoncloa.gob.es/gobierno/agenda/paginas/agenda.aspx`

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| Featured news | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=1` |
| Current news | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=2` |
| President highlights | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=20` |
| President agenda | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=22` |
| President speeches | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=23` |
| Council of Ministers summaries | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=15` |
| Council of Ministers references | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=16` |
| Council press conference transcripts | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=17` |
| Government agenda | `https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=32` |

---

### 1.2 Foreign Ministry — Ministerio de Asuntos Exteriores, Unión Europea y Cooperación

| Field | Detail |
|---|---|
| **Institution** | Ministerio de Asuntos Exteriores, Unión Europea y Cooperación (MAEC) |
| **Domain** | `exteriores.gob.es` |
| **Entry Point URL** | `https://www.exteriores.gob.es/es/Comunicacion/NotasPrensa/Paginas/index.aspx` |
| **RSS/Atom Feed** | None identified on the current site. [VERIFY RSS — SharePoint-based site may have hidden feed endpoints] |
| **Language** | Spanish (primary); English and French sections available for select content |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Notas de prensa issued for diplomatic meetings, treaty actions, consular emergencies, multilateral votes, bilateral visits, and ambassador appointments. Comunicados issued separately for formal diplomatic statements. |
| **Content Format** | HTML on SharePoint. Individual press releases follow the pattern `/es/Comunicacion/NotasPrensa/Paginas/2026_NOTAS_P/{slug}.aspx`. Comunicados at `/es/Comunicacion/Comunicados/Paginas/2026_COMUNICADOS/{slug}.aspx`. |
| **Extraction Method** | HTML scraping of the press release listing page. Pagination via `?p=N` query parameter. Two separate sections must be monitored: NotasPrensa and Comunicados. |
| **Editorial Orientation** | Official foreign ministry position. Under Minister José Manuel Albares, communications emphasize European integration, multilateralism, Ibero-American solidarity, and the strategic partnership with Morocco. |
| **Why This Source** | The only primary source for Spain's formal diplomatic positions, treaty ratifications, ambassador appointments, and bilateral/multilateral meeting readouts. Media coverage of MAEC activity — including by EFE and El País — is invariably derived from these communications. The separation of NotasPrensa (operational announcements) from Comunicados (formal diplomatic statements) provides a useful signal intensity indicator. |
| **Access Notes** | No paywall. SharePoint-based infrastructure separate from La Moncloa. The site also hosts country/territory fact sheets (`FichasPais`) with detailed bilateral relationship summaries. Embassy-level communications are published on per-country subdomains. |

**Additional entry points:**
- Comunicados (formal statements): `https://www.exteriores.gob.es/es/Comunicacion/Comunicados/Paginas/index.aspx`
- Country fact sheets: `https://www.exteriores.gob.es/es/Comunicacion/FichasPais/Paginas/index.aspx`
- Social media directory: `https://www.exteriores.gob.es/es/Comunicacion/AtlasRedesSociales/Paginas/index.aspx`
- EU Permanent Representation: `https://www.exteriores.gob.es/RepresentacionesPermanentes/EspanaUE/es/Paginas/inicio.aspx`

---

### 1.3 Defense Ministry — Ministerio de Defensa

| Field | Detail |
|---|---|
| **Institution** | Ministerio de Defensa |
| **Domain** | `defensa.gob.es` |
| **Entry Point URL** | `https://www.defensa.gob.es/gabinete/notasPrensa/` |
| **RSS/Atom Feed** | **Yes.** Press releases RSS: `https://www.defensa.gob.es/comun/rssChannel/rssNotasPrensa.xml` |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | 3-7 per week. Notas de prensa issued for military exercises, NATO/EU defense cooperation (PESCO, FCAS, EU Battlegroups), overseas deployments, defense procurement, ministerial visits, and institutional events. |
| **Content Format** | HTML. Individual releases organized by year and month under `/gabinete/notasPrensa/YYYY/MM/{release-code}.html`. Multimedia section with photos/video. |
| **Extraction Method** | RSS feed for automated polling (preferred). HTML scraping of the listing page as fallback. Year/month directory structure enables targeted historical scraping. |
| **Editorial Orientation** | Official defense communications. Under Minister Margarita Robles, messaging emphasizes NATO solidarity, European defense cooperation (FCAS, Eurofighter, PESCO projects), and Spain's commitment to the 2% GDP defense spending target. More transparent than many peer defense ministries — procurement announcements and exercise descriptions are reasonably detailed. |
| **Why This Source** | Primary source for Spain's defense posture: troop deployments, NATO commitments, FCAS progress, naval procurement (F-110 frigates, S-80 submarines), and bilateral defense agreements. The Revista Española de Defensa (published under the same domain) provides longer-form analysis. Infodefensa (Layer 1 media map) supplements but does not replace official ministerial communications. |
| **Access Notes** | No paywall. The RSS feed is functional and well-maintained. The site also hosts the Revista Española de Defensa (official defense magazine) and archives of the Estado Mayor de la Defensa (EMAD). Social media accounts on X, Facebook, YouTube, Flickr, and Instagram. |

**Additional entry points:**
- Revista Española de Defensa: `https://www.defensa.gob.es/gabinete/red/`
- EMAD (Joint Chiefs): `https://emad.defensa.gob.es/`
- Multimedia: `https://www.defensa.gob.es/gabinete/multimedia/`
- RSS channel page: `https://www.defensa.gob.es/comun/canalRss.html`

---

### 1.4 Parliament / Legislature

#### 1.4a Congreso de los Diputados (Congress of Deputies)

| Field | Detail |
|---|---|
| **Institution** | Congreso de los Diputados |
| **Domain** | `congreso.es` |
| **Entry Point URL** | `https://www.congreso.es/es/ultimas-publicaciones-oficiales` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — the site does not expose obvious feed endpoints] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily during session periods (September-December, February-June). Boletín Oficial de las Cortes Generales and Diarios de Sesiones published on sitting days. |
| **Content Format** | HTML index pages linking to PDF documents. Boletines Oficiales and Diarios de Sesiones are published as PDFs. Historical series searchable at `app.congreso.es`. |
| **Extraction Method** | HTML scraping of the latest publications page. PDF download and text extraction for Boletines and Diarios de Sesiones. The publications search (`congreso.es/es/busqueda-de-publicaciones`) supports filtering by type and date. |
| **Editorial Orientation** | Official legislative record. Nonpartisan — verbatim transcripts of plenary and committee sessions, full text of legislative initiatives, and voting records. |
| **Why This Source** | Parliamentary records document committee debates on defense budgets, treaty ratifications, troop deployments, and foreign affairs. The Comisión de Asuntos Exteriores and Comisión de Defensa proceedings are primary sources for detecting partisan constraints on executive action. Investiture debates and motions of no confidence are published here in full. The Boletín Oficial contains the text of all legislative initiatives. |
| **Access Notes** | No paywall. Fully searchable archive. The site can be slow and occasionally returns 403 errors. Historical Diarios de Sesiones at `app.congreso.es/est_sesiones/`. Publications index at `congreso.es/es/indice-de-publicaciones`. |

**Additional entry points:**
- Publications search: `https://www.congreso.es/es/busqueda-de-publicaciones`
- Historical session diaries: `https://app.congreso.es/est_sesiones/`
- Publications index: `https://www.congreso.es/es/indice-de-publicaciones`

#### 1.4b Senado de España (Senate)

| Field | Detail |
|---|---|
| **Institution** | Senado de España |
| **Domain** | `senado.es` |
| **Entry Point URL** | `https://www.senado.es/web/actividadparlamentaria/publicacionesoficiales/senado/boletinesoficiales/index.html` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily during session periods. Boletín Oficial del Senado and Diarios de Sesiones published on sitting days. |
| **Content Format** | HTML index pages linking to PDF documents. Boletines and Diarios in PDF format. |
| **Extraction Method** | HTML scraping of publications pages. PDF download and extraction. |
| **Editorial Orientation** | Official legislative record. Nonpartisan. The Senate serves as the chamber of territorial representation — debates on autonomous community issues (particularly Catalonia, Basque Country) are politically significant. |
| **Why This Source** | Treaty ratifications require Senate approval. The Senate's territorial focus means debates on autonomy, territorial financing, and EU structural fund distribution appear here with depth not found in Congreso records. Committee testimony from MAEC and Defense Ministry officials appears in Senate Diarios de Sesiones. |
| **Access Notes** | No paywall. The site occasionally returns 403 errors. Guided search available at `senado.es/web/conocersenado/ayudabuscadorgeneral/busquedaguiada/publicacionesoficiales/index.html`. |

**Additional entry points:**
- Diarios de Sesiones: `https://www.senado.es/web/actividadparlamentaria/publicacionesoficiales/senado/diariossesiones/index.html`
- Guided publication search: `https://www.senado.es/web/conocersenado/ayudabuscadorgeneral/busquedaguiada/publicacionesoficiales/index.html`

---

### 1.5 Official Gazette — Boletín Oficial del Estado (BOE)

| Field | Detail |
|---|---|
| **Institution** | Agencia Estatal Boletín Oficial del Estado |
| **Domain** | `boe.es` |
| **Entry Point URL** | `https://www.boe.es/diario_boe/` (daily edition) / `https://www.boe.es/buscar/` (search) |
| **RSS/Atom Feed** | **Yes — extensive feed system.** Complete daily summary: `/rss/boe.php`. Section-specific feeds for Sections I-V. Thematic feeds for legislation by subject (~35 topic feeds including international relations, defense, taxation). Special feeds for public procurement by CPV code. |
| **API** | **Yes — full REST API.** `https://www.boe.es/datosabiertos/api/api.php`. Supports XML and JSON responses. Endpoints for daily summaries (by date, format `yyyymmdd`), consolidated legislation (by norm identifier), and auxiliary reference data. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the BOE is the constitutional publication vehicle for all state laws, royal decrees, international agreements, and executive orders |
| **Publication Frequency** | Daily (Monday-Saturday). Published early morning. Supplementary editions for urgent matters. |
| **Content Format** | HTML index pages linking to individual items in HTML and PDF. The API returns structured XML/JSON. Each item has a unique BOE identifier (e.g., `BOE-A-2026-XXXXX`). |
| **Extraction Method** | **API preferred** — the open data API provides structured access to daily summaries and individual items. RSS feeds for topic-based monitoring. HTML/PDF for full-text retrieval. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no state law, royal decree, international agreement, or government order is legally effective until published in the BOE. This is the only source that provides definitive, timestamped legal text. All media reporting on legislation is downstream of BOE publication. The BORME (Boletín Oficial del Registro Mercantil) for commercial registry data is published through the same platform. |
| **Access Notes** | No paywall. The API requires acceptance of reuse conditions but no authentication. "Mi BOE" personalized alert service available for registered users. The digital legal library provides free access to consolidated legal codes. Historical archive (Gazeta collection) spans 1661-1959. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| Complete daily BOE summary | `https://www.boe.es/rss/boe.php` |
| Section I (General provisions) | `https://www.boe.es/rss/boe.php?s=1` [VERIFY URL] |
| Section III (Other provisions) | `https://www.boe.es/rss/boe.php?s=3` [VERIFY URL] |
| BORME (Commercial Registry) | `https://www.boe.es/rss/borme.php` |
| International relations legislation | Available via thematic channel [VERIFY exact URL at `/rss/` directory] |
| Constitutional Court rulings | Available via thematic channel [VERIFY exact URL at `/rss/` directory] |

**API endpoints:**
| Endpoint | Description |
|---|---|
| Daily summary | `GET /datosabiertos/api/boe/dias/{yyyymmdd}` |
| Consolidated legislation | `GET /datosabiertos/api/boe/legislacion/{norm_id}` |
| Search | `GET /datosabiertos/api/boe/buscar?q={query}&fpu={date_from}&fpf={date_to}` |
| Auxiliary data (subjects) | `GET /datosabiertos/api/boe/auxiliar/materias` |

---

### 1.6 Finance Ministry — Ministerio de Hacienda

| Field | Detail |
|---|---|
| **Institution** | Ministerio de Hacienda |
| **Domain** | `hacienda.gob.es` |
| **Entry Point URL** | `https://www.hacienda.gob.es/es-ES/Prensa/Noticias/Paginas/NotasPrensaHome.aspx` |
| **RSS/Atom Feed** | **Limited.** Ministry agenda RSS: `https://www.hacienda.gob.es/_layouts/15/rsseventos.aspx?hiloid=11`. No RSS for press releases identified — the syndication page (`/es-es/paginas/sindicacion.aspx`) lists feeds primarily for employment, auctions, and administrative data rather than press communications. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | 3-5 per week. Notas de prensa issued for fiscal policy announcements, budget execution reports, autonomous community financing decisions, tax policy changes, and public debt operations. Higher frequency during budget season (September-December). |
| **Content Format** | HTML on SharePoint. Individual press releases follow the pattern `/es-ES/Prensa/Noticias/Paginas/YYYY/{date-code}-{slug}.aspx`. Some comunicados link to attached PDF statistical tables. |
| **Extraction Method** | HTML scraping of the press release listing page. No usable press release RSS — must poll the HTML archive. PDF extraction for statistical annexes. |
| **Editorial Orientation** | Official fiscal policy position. Under First Deputy PM and Minister María Jesús Montero, communications emphasize fiscal consolidation compatible with social spending, autonomous community financing, and EU fiscal rule compliance. Data-heavy. |
| **Why This Source** | Primary source for Spain's federal budget execution, public debt management, autonomous community fiscal transfers, and tax revenue data. Essential for the Economic & Technological Statecraft domain — Hacienda communications are the raw data that Expansión, Cinco Días, and El Economista interpret. The Consejo de Política Fiscal y Financiera (CPFF) meeting outcomes, which determine fiscal transfers to autonomous communities, are published here. |
| **Access Notes** | No paywall. SharePoint-based infrastructure. The site supports multiple language variants (`es-ES`, `eu-ES`, `gl-ES`, `ca-ES`) for Basque, Galician, and Catalan. Social media: @Haciendagob on X, YouTube channel. |

**Additional entry points:**
- Syndication/RSS page: `https://www.hacienda.gob.es/es-es/paginas/sindicacion.aspx`
- Public finance statistics: `https://www.hacienda.gob.es/es-ES/CDI/Paginas/EstabilidadPresupuestaria/Informacion/home.aspx`
- Tax agency (AEAT): `https://sede.agenciatributaria.gob.es/`

---

### 1.7 Central Bank — Banco de España

| Field | Detail |
|---|---|
| **Institution** | Banco de España |
| **Domain** | `bde.es` |
| **Entry Point URL** | `https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/` (press releases) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS hub: `https://www.bde.es/wbe/es/inicio/rss/`. Key feeds: News & events (`/wbe/es/inicio/rss/rss-noticias/`), Publications (`/wbe/es/inicio/rss/rss-estudios-publicaciones/`), Statistics (`/wbe/es/inicio/rss/rss-estadisticas/`), Blog (`/wbe/es/inicio/rss/rss-blog/`), Regulations (`/wbe/es/inicio/rss/rss-normativa/`), Transparency (`/wbe/es/inicio/rss/rss-transparencia/`). BIEST statistical data RSS: `https://app.bde.es/bie_www/faces/bie_wwwias/jsp/op/CanalesRss/BIEST_Canales_RSS.jsp` |
| **Language** | Spanish (primary); English versions available for major publications at `/wbe/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy: follows ECB calendar (ECB Governing Council meets ~every 6 weeks; Banco de España contributes as Eurosystem member). Press releases: 2-5 per week. Financial stability reports: semi-annual. Statistical bulletins: monthly/quarterly. Blog posts: 2-4 per month. |
| **Content Format** | HTML for press releases and blog posts. PDF for formal publications (Annual Report, Financial Stability Report, economic bulletins). Statistical data via BIEST system (structured data). |
| **Extraction Method** | RSS feeds for automated monitoring across all content categories (news, publications, statistics, regulations). BIEST RSS for statistical indicators. PDF download for formal publications. |
| **Editorial Orientation** | Technically independent central bank within the Eurosystem. Communications are data-driven and institutionally neutral. Under Governor José Luis Escrivá (appointed 2024), increased emphasis on financial stability analysis and macroprudential supervision. The Banco de España does not set monetary policy independently — it participates in ECB Governing Council decisions — but its country-level analysis and financial stability assessments are authoritative. |
| **Why This Source** | Authoritative source for Spanish macroeconomic analysis, financial stability assessment, banking supervision data, and balance of payments statistics. The Annual Report and Financial Stability Report contain the most rigorous independent assessment of Spain's economic position. The BIEST statistical system provides structured time-series data on interest rates, exchange rates, national accounts, and financial sector indicators. Unlike in countries with independent monetary policy, the primary signal here is analytical rather than policy-setting. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds well-maintained. Newsletter subscription available at `/wbe/es/inicio/newsletters/`. English-language site provides parallel content for major publications. The BIEST system provides structured data download in multiple formats. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| News & events | `https://www.bde.es/wbe/es/inicio/rss/rss-noticias/` |
| Publications | `https://www.bde.es/wbe/es/inicio/rss/rss-estudios-publicaciones/` |
| Statistics | `https://www.bde.es/wbe/es/inicio/rss/rss-estadisticas/` |
| Blog | `https://www.bde.es/wbe/es/inicio/rss/rss-blog/` |
| Regulations | `https://www.bde.es/wbe/es/inicio/rss/rss-normativa/` |
| Transparency | `https://www.bde.es/wbe/es/inicio/rss/rss-transparencia/` |
| BIEST statistical channels | `https://app.bde.es/bie_www/faces/bie_wwwias/jsp/op/CanalesRss/BIEST_Canales_RSS.jsp` |
| Podcast | `https://www.bde.es/wbe/es/inicio/rss/rss-podcast/` |

---

### 1.8 Trade / Commerce — Ministerio de Economía, Comercio y Empresa

| Field | Detail |
|---|---|
| **Institution** | Ministerio de Economía, Comercio y Empresa (MINECO) |
| **Domain** | `portal.mineco.gob.es` / `comercio.gob.es` |
| **Entry Point URL** | `https://portal.mineco.gob.es/es-es/comunicacion/Paginas/default.aspx` (ministry news) / `https://comercio.gob.es/es-es/NotasPrensa/Paginas/index.aspx` (trade-specific press) |
| **RSS/Atom Feed** | RSS indicated at `https://portal.mineco.gob.es/es-es/ministerio/Paginas/Info_RSS.aspx` [VERIFY RSS — exact feed URLs not confirmed] |
| **Language** | Spanish (primary); English section available on comercio.gob.es |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Communications cover trade negotiations (EU FTAs, Mercosur), FDI data, industrial policy, digital economy regulation, and minister interventions. Separate trade-specific press releases from the Secretaría de Estado de Comercio. |
| **Content Format** | HTML on SharePoint. News items and press releases on both portal.mineco.gob.es and comercio.gob.es. Minister interventions and speeches in a dedicated subsection. |
| **Extraction Method** | HTML scraping of both domains' news pages. RSS if verified. The two domains serve different content: portal.mineco.gob.es for ministry-level communications, comercio.gob.es for trade policy specifics. |
| **Editorial Orientation** | Official economic/trade policy position. Under Minister Carlos Cuerpo, communications emphasize Spain's positioning as an FDI destination, Next Generation EU fund execution, digital transformation, and EU trade policy (particularly the Mercosur agreement and China tariff discussions). |
| **Why This Source** | Primary source for Spain's trade policy positions, FDI statistics, economic reform announcements, and EU internal market positioning. The Secretaría de Estado de Comercio manages Spain's bilateral trade promotion and WTO/EU trade negotiation participation. ICEX (Spain Trade and Investment, at `icex.es`) provides complementary trade promotion data. |
| **Access Notes** | No paywall. Two separate domains must be monitored. The legacy `mincotur.gob.es` domain (former Ministry of Industry, Trade and Tourism) still hosts historical press content. SharePoint-based infrastructure on both sites. |

**Additional entry points:**
- Trade-specific news: `https://portal.mineco.gob.es/es-es/comercio/Paginas/noticias.aspx`
- Economy and enterprise news: `https://portal.mineco.gob.es/es-es/economiayempresa/noticias/Paginas/default.aspx`
- ICEX (trade promotion): `https://www.icex.es/`
- Minister interventions: `https://portal.mineco.gob.es/es-es/ministerio/ministro/intervenciones/`

---

### 1.9 Intelligence / National Security — CNI and DSN

#### 1.9a Centro Nacional de Inteligencia (CNI)

| Field | Detail |
|---|---|
| **Institution** | Centro Nacional de Inteligencia (CNI) |
| **Domain** | `cni.es` |
| **Entry Point URL** | `https://www.cni.es/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. The CNI website is presentation-focused — it describes the organization's mission, structure, and values but publishes virtually no operational or policy communications. |
| **Content Format** | HTML. Modern single-page design with minimal textual content. The CCN (Centro Criptológico Nacional) subsidiary at `ccn.cni.es` publishes cybersecurity advisories and threat reports more actively. |
| **Extraction Method** | Periodic check of cni.es for any structural changes or new publications. Monitor CCN (`ccn.cni.es`) for cybersecurity-specific communications. |
| **Editorial Orientation** | N/A — effectively silent on policy matters. The site presents institutional identity (principles of "Service, Truth, and Future") without operational content. |
| **Why This Source** | Included for completeness. Like most national intelligence agencies, CNI's public communications are almost nonexistent. The real intelligence signal comes through: (a) leaks to investigative media (El Confidencial, elDiario.es); (b) parliamentary oversight committee proceedings; (c) DSN publications (see 1.9b); (d) judicial proceedings (the Pegasus/Catalangate affair generated signal through courts and media, not CNI communications). |
| **Access Notes** | The electronic headquarters (`sede.cni.gob.es`) hosts transparency compliance documents. CIF S2830132C, registered at Avenida Padre Huidobro 14, 28023 Madrid. |

#### 1.9b Departamento de Seguridad Nacional (DSN)

| Field | Detail |
|---|---|
| **Institution** | Departamento de Seguridad Nacional (DSN) — technical secretariat of the Consejo de Seguridad Nacional |
| **Domain** | `dsn.gob.es` |
| **Entry Point URL** | `https://www.dsn.gob.es/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish (primary); content available in Catalan, Basque, Galician, Valencian, and English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Notas de prensa, situation reports, and thematic analyses published regularly. Higher frequency during crises (terrorism, cyberattacks, natural disasters). |
| **Content Format** | HTML. Press releases, infographics, multimedia content. Strategic publications (National Security Strategy, sectoral strategies) in PDF. |
| **Extraction Method** | HTML scraping of the news/press section. Monitor the publications section for strategy documents. |
| **Editorial Orientation** | Official national security communications. The DSN serves as the advisory body to the Prime Minister on national security and coordinates across specialized councils (cybersecurity, aerospace, maritime, counterterrorism, energy security, organized crime). Communications frame security issues in an inter-agency, whole-of-government context. |
| **Why This Source** | The DSN is substantially more communicative than the CNI and publishes the closest thing Spain has to a public national security assessment. The National Security Strategy documents, annual reports, and sector-specific analyses (cybersecurity, maritime security, counterterrorism) provide the strategic framing that the CNI does not. National Security Council meeting announcements and outcomes appear here. Contact: comunicacion@dsn.presidencia.gob.es. |
| **Access Notes** | No paywall. Active social media presence on X, Instagram, YouTube, and LinkedIn. The DSN is organizationally part of the Presidencia del Gobierno (attached to La Moncloa). |

**Additional entry points:**
- National Security Strategy: `https://www.dsn.gob.es/es/estrategias-publicaciones/estrategias/estrategia-seguridad-nacional`
- Sectoral strategies: `https://www.dsn.gob.es/es/estrategias-publicaciones/estrategias`
- Annual reports: `https://www.dsn.gob.es/es/estrategias-publicaciones/informes-anuales`
- Situation Committee: referenced in press releases during crisis events

---

### 1.10 Country-Specific Institutions

#### 1.10a Casa Real (Royal Household)

| Field | Detail |
|---|---|
| **Institution** | Casa de Su Majestad el Rey |
| **Domain** | `casareal.es` |
| **Entry Point URL** | `https://www.casareal.es/ES/AreaPrensa/Paginas/area_prensa_comunicados.aspx` |
| **RSS/Atom Feed** | **Yes — four feeds available.** Activities: `/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=00ad4efe-38db-408d-b95c-43e0c724a414`. Official trips: `/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=2e3aaa49-c3bd-47a7-85a5-c43ab889d81f`. Speeches: `/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=a1f180ed-b45a-40c5-a13b-61d27cb664bc`. Comunicados: `/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=239d2332-7145-4633-b7c5-64c79640ab02`. |
| **Language** | Spanish (primary); English section at `/EN/`; also available in Catalan and Valencian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Irregular — 2-5 per month. Comunicados issued for state visits, official audiences, diplomatic receptions, and institutional statements. Activities published more frequently (multiple per week). |
| **Content Format** | HTML (SharePoint-based). Individual comunicados at `area_prensa_comunicados_interior.aspx?data={number}`. Photo galleries. |
| **Extraction Method** | RSS feeds for automated monitoring (4 feeds: activities, trips, speeches, comunicados). HTML scraping as fallback. Paginated listing page (5/10/20/30/40/50 items per page). |
| **Editorial Orientation** | Official Royal Household communication. King Felipe VI's public role is constitutionally limited to head of state and symbol of national unity. Communications are carefully apolitical but diplomatic engagements — state visits, ambassador credential ceremonies, international summits — reveal Spain's diplomatic priority hierarchy. |
| **Why This Source** | The King's diplomatic agenda is a leading indicator of bilateral relationship priority. State visits, credential ceremonies, and bilateral audiences with foreign leaders signal which relationships Madrid is cultivating. Royal speeches (particularly the annual Christmas message and UN General Assembly addresses) frame Spain's strategic narrative. King Felipe VI's role in the handover of EU Council presidency and NATO summits provides insight into Spain's institutional positioning. |
| **Access Notes** | No paywall. SharePoint-based site with custom feed infrastructure. RSS page at `/ES/Paginas/rss.aspx`. Social media: @CasaReal on X, Facebook. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| Activities | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=00ad4efe-38db-408d-b95c-43e0c724a414` |
| Official trips | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=2e3aaa49-c3bd-47a7-85a5-c43ab889d81f` |
| Speeches | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=a1f180ed-b45a-40c5-a13b-61d27cb664bc` |
| Comunicados | `https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=239d2332-7145-4633-b7c5-64c79640ab02` |

#### 1.10b Representación Permanente de España ante la UE (EU Permanent Representation)

| Field | Detail |
|---|---|
| **Institution** | Representación Permanente de España ante la Unión Europea (REPER) |
| **Domain** | `es-ue.org` / `exteriores.gob.es/RepresentacionesPermanentes/EspanaUE` |
| **Entry Point URL** | `https://es-ue.org/` (main communications site) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish (primary); English at `en.es-ue.org` |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week, concentrated around EU Council meetings, Eurogroup sessions, and COREPER activity. Frequency spikes during Council presidency periods or major EU negotiations. |
| **Content Format** | HTML. News articles produced by the Oficina de Comunicación. Social media content on LinkedIn, X (@EspanaenUE), Bluesky, Instagram. |
| **Extraction Method** | HTML scraping of es-ue.org news section. The site appears WordPress-based — RSS may be available at `es-ue.org/feed/` [VERIFY RSS]. |
| **Editorial Orientation** | Official government EU engagement framing. Content emphasizes Spain's active participation in EU institutions. Ambassador Marcos Alonso Alonso leads the team of ministerial advisors who participate in 150+ EU working groups. |
| **Why This Source** | The REPER is Spain's day-to-day interface with EU institutions. Its communications reveal which EU dossiers Spain is prioritizing, how Madrid positions itself on Council votes, and Spain's negotiating stance on major EU legislation. The REPER's thematic coverage (trade, migration, defense, energy, digital) spans multiple analytical domains. The separate `es-ue.org` domain, distinct from the MAEC institutional page, suggests an active communications strategy. |
| **Access Notes** | No paywall. Two web presences: `es-ue.org` (active communications) and the MAEC institutional page (static). Staff directory available at `en.es-ue.org/directorio/`. |

**Additional entry points:**
- MAEC institutional page: `https://www.exteriores.gob.es/RepresentacionesPermanentes/EspanaUE/es/Paginas/inicio.aspx`
- English site: `https://en.es-ue.org/`
- Policy positions: `https://es-ue.org/posiciones/` [VERIFY URL]

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Infrastructure |
|---|---|---|---|---|---|---|---|
| 1 | La Moncloa (Presidencia) | `lamoncloa.gob.es/serviciosdeprensa/notasprensa/` | **Yes** (9 feeds) | P1 | HTML | Daily | SharePoint |
| 2 | MAEC (Foreign Ministry) | `exteriores.gob.es/es/Comunicacion/NotasPrensa/` | No | P1 | HTML | Daily | SharePoint |
| 3 | Defensa (Defense Ministry) | `defensa.gob.es/gabinete/notasPrensa/` | **Yes** (1 feed) | P1 | HTML | 3-7/week | Custom CMS |
| 4a | Congreso de los Diputados | `congreso.es/es/ultimas-publicaciones-oficiales` | No | P2 | HTML/PDF | Daily (session) | Custom |
| 4b | Senado | `senado.es/web/.../boletinesoficiales/` | No | P2 | HTML/PDF | Daily (session) | Custom |
| 5 | BOE (Official Gazette) | `boe.es/diario_boe/` | **Yes** (35+ feeds) | P2 | HTML/PDF/API | Daily | Custom + API |
| 6 | Hacienda (Finance) | `hacienda.gob.es/es-ES/Prensa/Noticias/` | Limited (agenda only) | P2 | HTML/PDF | 3-5/week | SharePoint |
| 7 | Banco de España | `bde.es/wbe/es/.../notas-banco-espana/` | **Yes** (8+ feeds) | P2 | HTML/PDF | Variable | Custom |
| 8 | MINECO (Economy/Trade) | `portal.mineco.gob.es/es-es/comunicacion/` | [VERIFY] | P2 | HTML | 2-5/week | SharePoint |
| 9a | CNI (Intelligence) | `cni.es` | No | P2 | Minimal | Negligible | Custom |
| 9b | DSN (National Security) | `dsn.gob.es` | [VERIFY] | P2 | HTML/PDF | 2-5/week | Custom |
| 10a | Casa Real | `casareal.es/ES/AreaPrensa/` | **Yes** (4 feeds) | P2 | HTML | 2-5/month | SharePoint |
| 10b | REPER (EU Rep) | `es-ue.org` | [VERIFY] | P2 | HTML | 3-7/week | WordPress? |

---

## 3. MONITORING CONFIGURATION

```yaml
# Spain Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/es.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: es_moncloa
    name: La Moncloa (Presidencia del Gobierno)
    domain: lamoncloa.gob.es
    entry_url: "https://www.lamoncloa.gob.es/serviciosdeprensa/notasprensa/Paginas/index.aspx"
    rss_feed:
      featured_news: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=1"
      current_news: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=2"
      president_highlights: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=20"
      president_speeches: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=23"
      council_summaries: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=15"
      council_references: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=16"
      council_pressers: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=17"
      president_agenda: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=22"
      government_agenda: "https://www.lamoncloa.gob.es/paginas/rss.aspx?tipo=32"
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "9 RSS feeds covering distinct content types. Council of Ministers references (tipo=16) are the most policy-dense. SharePoint infrastructure."

  - id: es_maec
    name: Ministerio de Asuntos Exteriores (MAEC)
    domain: exteriores.gob.es
    entry_url: "https://www.exteriores.gob.es/es/Comunicacion/NotasPrensa/Paginas/index.aspx"
    rss_feed: null  # [VERIFY]
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Two sections to monitor: NotasPrensa and Comunicados. Pagination via ?p=N. SharePoint site."
    additional_urls:
      - "https://www.exteriores.gob.es/es/Comunicacion/Comunicados/Paginas/index.aspx"

  - id: es_defensa
    name: Ministerio de Defensa
    domain: defensa.gob.es
    entry_url: "https://www.defensa.gob.es/gabinete/notasPrensa/"
    rss_feed: "https://www.defensa.gob.es/comun/rssChannel/rssNotasPrensa.xml"
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 4
    notes: "RSS feed well-maintained. Year/month directory structure enables historical scraping. Revista Española de Defensa also on this domain."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: es_congreso
    name: Congreso de los Diputados
    domain: congreso.es
    entry_url: "https://www.congreso.es/es/ultimas-publicaciones-oficiales"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
      - security_defense_autonomy
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 6
    notes: "Boletines and Diarios de Sesiones in PDF. Site can be slow, occasionally 403. Focus on Comisión de Asuntos Exteriores and Comisión de Defensa."

  - id: es_senado
    name: Senado de España
    domain: senado.es
    entry_url: "https://www.senado.es/web/actividadparlamentaria/publicacionesoficiales/senado/boletinesoficiales/index.html"
    rss_feed: null  # [VERIFY]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 6
    notes: "Treaty ratifications, territorial debates. Occasionally returns 403."

  - id: es_boe
    name: Boletín Oficial del Estado (BOE)
    domain: boe.es
    entry_url: "https://www.boe.es/diario_boe/"
    rss_feed:
      complete_daily: "https://www.boe.es/rss/boe.php"
      borme: "https://www.boe.es/rss/borme.php"
    api:
      base_url: "https://www.boe.es/datosabiertos/api/api.php"
      daily_summary: "/boe/dias/{yyyymmdd}"
      search: "/boe/buscar?q={query}&fpu={date_from}&fpf={date_to}"
      formats: ["xml", "json"]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html_pdf_api
    extraction_method: api_preferred_rss_fallback
    poll_interval_hours: 6
    notes: "Most technically mature government source. REST API + 35+ RSS feeds. All laws/decrees/international agreements published here. Use API for structured queries, RSS for monitoring."

  - id: es_hacienda
    name: Ministerio de Hacienda
    domain: hacienda.gob.es
    entry_url: "https://www.hacienda.gob.es/es-ES/Prensa/Noticias/Paginas/NotasPrensaHome.aspx"
    rss_feed:
      agenda: "https://www.hacienda.gob.es/_layouts/15/rsseventos.aspx?hiloid=11"
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "No press release RSS — must scrape HTML archive. Agenda RSS available. PDF statistical annexes. SharePoint."

  - id: es_bde
    name: Banco de España
    domain: bde.es
    entry_url: "https://www.bde.es/wbe/es/noticias-eventos/actualidad-banco-espana/notas-banco-espana/"
    rss_feed:
      news: "https://www.bde.es/wbe/es/inicio/rss/rss-noticias/"
      publications: "https://www.bde.es/wbe/es/inicio/rss/rss-estudios-publicaciones/"
      statistics: "https://www.bde.es/wbe/es/inicio/rss/rss-estadisticas/"
      blog: "https://www.bde.es/wbe/es/inicio/rss/rss-blog/"
      regulations: "https://www.bde.es/wbe/es/inicio/rss/rss-normativa/"
      transparency: "https://www.bde.es/wbe/es/inicio/rss/rss-transparencia/"
      biest_statistics: "https://app.bde.es/bie_www/faces/bie_wwwias/jsp/op/CanalesRss/BIEST_Canales_RSS.jsp"
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best RSS coverage of any Spanish government source. 8+ feeds across all content types. BIEST for structured statistical data. English versions available. No bot protection."

  - id: es_mineco
    name: Ministerio de Economía, Comercio y Empresa (MINECO)
    domain: portal.mineco.gob.es
    entry_url: "https://portal.mineco.gob.es/es-es/comunicacion/Paginas/default.aspx"
    rss_feed: null  # RSS page exists but exact feed URLs unconfirmed [VERIFY at /es-es/ministerio/Paginas/Info_RSS.aspx]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Two domains: portal.mineco.gob.es (ministry) and comercio.gob.es (trade). SharePoint. Legacy mincotur.gob.es still active."
    additional_urls:
      - "https://comercio.gob.es/es-es/NotasPrensa/Paginas/index.aspx"

  - id: es_cni
    name: Centro Nacional de Inteligencia (CNI)
    domain: cni.es
    entry_url: "https://www.cni.es/"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent. Presentation-focused website. CCN (ccn.cni.es) publishes cybersecurity advisories more actively. Real signal via leaks to El Confidencial/elDiario.es."

  - id: es_dsn
    name: Departamento de Seguridad Nacional (DSN)
    domain: dsn.gob.es
    entry_url: "https://www.dsn.gob.es/"
    rss_feed: null  # [VERIFY]
    language: es
    type: government_aligned
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "National Security Council secretariat. Publishes strategy documents, annual reports, sector analyses. More communicative than CNI. Contact: comunicacion@dsn.presidencia.gob.es."

  - id: es_casareal
    name: Casa de Su Majestad el Rey (Royal Household)
    domain: casareal.es
    entry_url: "https://www.casareal.es/ES/AreaPrensa/Paginas/area_prensa_comunicados.aspx"
    rss_feed:
      activities: "https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=00ad4efe-38db-408d-b95c-43e0c724a414"
      official_trips: "https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=2e3aaa49-c3bd-47a7-85a5-c43ab889d81f"
      speeches: "https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=a1f180ed-b45a-40c5-a13b-61d27cb664bc"
      comunicados: "https://www.casareal.es/ES/_layouts/csmrfeeds/CustomListFeed.aspx?ID=239d2332-7145-4633-b7c5-64c79640ab02"
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "2-5_per_month"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 12
    notes: "4 RSS feeds via SharePoint custom feed infrastructure. King's diplomatic agenda is a leading indicator of bilateral priority. Low frequency but high signal."

  - id: es_reper
    name: Representación Permanente de España ante la UE
    domain: es-ue.org
    entry_url: "https://es-ue.org/"
    rss_feed: null  # [VERIFY — WordPress-based, may have /feed/ endpoint]
    language: es
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape  # or rss_poll if /feed/ confirmed
    poll_interval_hours: 12
    notes: "Active communications site. Separate from MAEC institutional page. Likely WordPress — check es-ue.org/feed/ for RSS. Also on X @EspanaenUE, LinkedIn, Bluesky."
    additional_urls:
      - "https://www.exteriores.gob.es/RepresentacionesPermanentes/EspanaUE/es/Paginas/inicio.aspx"

# No shared platform equivalent to Mexico's gob.mx
# Each Spanish ministry operates independent infrastructure
# SharePoint is the most common CMS (La Moncloa, MAEC, Hacienda, MINECO, Casa Real)
# but implementations vary significantly across sites

shared_config:
  sharepoint_sites:
    - lamoncloa.gob.es
    - exteriores.gob.es
    - hacienda.gob.es
    - portal.mineco.gob.es
    - casareal.es
  notes: "SharePoint sites share similar pagination patterns and HTML structure but each has custom templates. No unified extraction pattern possible — each requires site-specific selectors."
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "es-ES,es;q=0.9"
  rate_limit: "max 1 request per 3 seconds per domain"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Spanish government communications are more institutionally diverse than in countries with centralized government portals. Each ministry controls its own messaging, creating both redundancy (the same event announced by La Moncloa and the originating ministry) and occasionally revealing inter-ministerial tension (when framings diverge). The pipeline must treat government sources as confirming the government's chosen public position — not as confirming underlying facts.

- **La Moncloa**: Cross-reference Council of Ministers references against same-day reporting in El País (center-left perspective) and El Mundo (center-right counterpoint). The post-Council press conference transcripts (RSS tipo=17) contain Q&A that often reveals positions not in the formal reference. Discrepancies between La Moncloa framing and Agencia EFE dispatches — despite EFE being state-owned — can signal tension between the communications apparatus and the wire service's editorial independence.

- **MAEC**: Diplomatic comunicados should be triangulated with El País international desk (Spain's largest foreign correspondent network), Atalayar (for Mediterranean/North Africa dimension), and Real Instituto Elcano analysis (for strategic context). When MAEC and La Moncloa issue separate communications on the same diplomatic event with different emphasis, it signals either inter-institutional coordination or — more interestingly — divergent priorities between the presidency and the foreign ministry.

- **Defensa**: Military press releases are more detailed than in many peer countries (procurement milestones, exercise specifics, deployment rotations) but omit cost overruns, capability gaps, and industrial disputes. Cross-reference with Infodefensa (the only dedicated Spanish defense publication), Política Exterior (for strategic context), and ABC/El Mundo (for opposition framing of defense spending commitments, particularly the 2% GDP target).

- **BOE**: Legal text published in the BOE is authoritative and definitive — this is the one government source where the content is the fact, not a framing of the fact. However, the timing of publication (delays between Council approval and BOE publication) can itself be a signal. Cross-reference with Expansión and Cinco Días for market and business interpretation of regulatory changes.

- **Banco de España**: The most technically rigorous government source. Financial stability reports and macroeconomic projections are genuine analytical products, not political communications. Cross-reference with El Economista and Expansión for market interpretation. The BdE's periodic divergence from ECB projections (when Spain-specific conditions warrant) is a high-value signal for economic statecraft analysis.

- **Hacienda**: Fiscal data is reliable in headline numbers but presentation framing — base period selection, seasonal adjustment methodology, comparisons against forecast rather than prior year — can shape narrative. Autonomous community financing decisions (CPFF outcomes) are politically explosive and should be cross-referenced with La Vanguardia (Catalan perspective), El Correo (Basque perspective), and the financial press.

- **Casa Real**: Royal communications are sparse and carefully apolitical. The signal lies in the diplomatic agenda — which heads of state receive visits, which credential ceremonies are highlighted, which international events the King attends. Cross-reference with ABC (monarchist editorial line, most detailed Royal coverage) and El País (more critical perspective on the monarchy's institutional role).

**4.2 The decentralized infrastructure effect**

Unlike Mexico's centralized gob.mx platform, Spain's government web infrastructure is fully decentralized. Each ministry and constitutional body operates independent SharePoint instances or custom CMS platforms. This means:
- No single point of failure affects all sources simultaneously
- Template changes at one ministry do not propagate to others
- Each site requires site-specific extraction selectors
- RSS availability varies dramatically across sites (BOE has 35+ feeds; MAEC has none)
- Content removal or modification at one site does not affect others

The practical implication is higher development cost for extraction (no shared scraper module) but greater resilience against platform-wide outages.

**4.3 The CNI silence problem**

Spain's intelligence agency (CNI) produces effectively zero public communications — even less than its Mexican namesake. This is a structural gap that cannot be filled by monitoring. Intelligence-relevant signals surface through:
- Leaks to investigative media (El Confidencial for institutional leaks, elDiario.es for surveillance/privacy concerns)
- The DSN, which publishes the strategic analysis that the CNI does not
- The CCN (Centro Criptológico Nacional, the CNI's cybersecurity arm at `ccn.cni.es`), which actively publishes threat advisories and security guidelines
- Parliamentary oversight committee proceedings (Comisión de control de los créditos destinados a gastos reservados)
- Judicial proceedings (the Pegasus/Catalangate affair produced extensive signal through courts and media)

The pipeline should not allocate significant resources to polling cni.es but should flag any new publication as a high-priority anomaly. The DSN and CCN are the actionable public-facing outlets for national security analysis.

**4.4 The BOE as definitive legal source**

Spain's BOE is technically superior to most comparable official gazettes globally. Its REST API, extensive RSS system, and structured data formats make it the most pipeline-friendly government source in the Spanish ecosystem. For the pipeline:
- Use the API for targeted queries (international agreements, defense-related royal decrees, economic regulation)
- Use topic-specific RSS feeds for passive monitoring (international relations channel, defense legislation channel)
- Treat BOE publication as the canonical timestamp for all legal acts — media reports on legislation are always downstream of BOE publication
- The BORME (commercial registry) section captures corporate restructurings with geopolitical relevance (Telefónica shareholder changes, defense contractor mergers, state-owned enterprise actions)

**4.5 Legislative gap: committee proceedings**

The existing Source Intelligence Map identifies parliamentary transcripts as a coverage gap. Both Congreso and Senado publish Diarios de Sesiones containing committee-level proceedings — including testimony from MAEC, Defense, and BdE officials — that no media outlet fully covers. However, these are published as long-form PDFs with no RSS feeds or structured data, making automated extraction difficult. Prioritize: (a) Comisión de Asuntos Exteriores sessions, (b) Comisión de Defensa sessions, (c) budget committee hearings during Presupuestos Generales del Estado review (September-December), (d) the Senate's Comisión General de las Comunidades Autónomas for territorial dynamics.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 No Shared Extraction Architecture

Unlike Mexico's gob.mx platform (which provides a single scraping template for 7+ agencies), Spain's decentralized government infrastructure requires site-specific extraction modules. The 14 monitored endpoints fall into four infrastructure categories:

| Infrastructure Type | Sites | Extraction Approach |
|---|---|---|
| **SharePoint** | La Moncloa, MAEC, Hacienda, MINECO, Casa Real | SharePoint HTML parsing with site-specific selectors. Pagination via query parameters. Custom feed endpoints where available (La Moncloa `?tipo=N`, Casa Real `CustomListFeed.aspx`). |
| **Custom CMS** | Defensa, Congreso, Senado, DSN, CNI | Site-specific HTML scraping. Defensa has RSS. Others require polling. |
| **API/Structured** | BOE, Banco de España | REST API (BOE) and RSS feeds (BdE). Structured data extraction. Most automation-friendly. |
| **WordPress/Modern** | REPER (es-ue.org) | Standard WordPress extraction. Likely `/feed/` RSS endpoint. |

### 5.2 RSS-Enabled Sources (Priority for Automation)

Five government sources provide functional RSS feeds, in descending order of coverage:

1. **BOE**: 35+ topic-specific RSS feeds plus complete daily summary. REST API for structured queries. The most machine-friendly government source in Spain.

2. **Banco de España**: 8+ RSS feeds covering news, publications, statistics, blog, regulations, transparency, and podcast. BIEST statistical channels provide structured economic data.

3. **La Moncloa**: 9 RSS feeds covering featured/current news, presidential highlights/speeches/agenda, Council of Ministers summaries/references/press conferences, and government agenda. The Council of Ministers references feed (tipo=16) is the single most policy-dense government RSS feed in Spain.

4. **Casa Real**: 4 RSS feeds via custom SharePoint feed infrastructure — activities, official trips, speeches, and comunicados.

5. **Defensa**: 1 RSS feed for press releases (`rssNotasPrensa.xml`).

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Four sources publish primarily or substantially in PDF:
- **BOE**: All legal texts available in PDF alongside HTML. The API provides structured metadata but full text requires PDF or HTML retrieval.
- **Congreso/Senado**: Boletines Oficiales and Diarios de Sesiones are multi-page PDFs. Text-based (not scanned), but long-form and unstructured.
- **Banco de España**: Financial Stability Report, Annual Report, and economic bulletins are formal PDFs. Well-structured with table of contents. Statistical annexes contain tables requiring structured extraction.
- **Hacienda**: Statistical annexes to press releases in PDF with tables. May require table extraction (tabula/camelot).

### 5.4 Language and Encoding

All government sources publish primarily in Spanish. Notable multilingual capabilities:
- **La Moncloa**: English section at `/lang/en/` for major presidential communications.
- **MAEC**: Select content in English and French.
- **Banco de España**: Full parallel English site at `/wbe/en/` for major publications.
- **Casa Real**: English, Catalan, and Valencian sections available.
- **BOE**: Spanish only (legal text is constitutionally in Castilian Spanish).
- **Hacienda**: Interface available in Basque, Galician, and Catalan; content in Spanish.
- **DSN**: Interface in Spanish, Catalan, Basque, Galician, Valencian, and English.

All sites serve UTF-8 encoded content. No legacy encoding issues identified.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A Council of Ministers decision appears in La Moncloa references, the originating ministry's press section, and the BOE (for legal force)
- Defense cooperation agreements appear in Defensa, MAEC, and La Moncloa press releases
- EU-related announcements appear on La Moncloa, MAEC, REPER, and sometimes Hacienda or MINECO
- Royal diplomatic engagements appear on Casa Real and MAEC

Implement content-hash deduplication. Use the following canonical source hierarchy:
- **Legal texts**: BOE is always canonical
- **Foreign policy**: MAEC is canonical (La Moncloa may publish simultaneously but MAEC has the authoritative diplomatic framing)
- **Defense**: Defensa is canonical
- **Economic/fiscal**: Hacienda is canonical for fiscal, BdE for monetary/financial, MINECO for trade
- **Executive decisions**: La Moncloa Council of Ministers reference is canonical
- **Royal activities**: Casa Real is canonical

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | La Moncloa, MAEC | Every 2 hours | Daily publication, policy-critical. La Moncloa via RSS; MAEC via scraping. |
| P1-Standard | Defensa | Every 4 hours | Less frequent but high-priority when published. RSS available. |
| P2-Active | BOE, BdE, DSN, Hacienda, MINECO | Every 6 hours | Regular publishing schedule. BOE/BdE via API/RSS; others via scraping. |
| P2-Low | Congreso, Senado, Casa Real, REPER | Every 12 hours | Session-dependent (legislature) or low frequency (Casa Real). Casa Real via RSS. |
| P2-Minimal | CNI | Weekly | Effectively silent; flag any publication as anomaly. |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| SharePoint outage at specific ministry | La Moncloa, MAEC, Hacienda, MINECO, or Casa Real (individually) | Monitor corresponding X accounts (@desabordo, @MAabordo, @Haciendagob, @CasaReal). La Moncloa press releases are syndicated to Agencia EFE within minutes. Government social media frequently publishes before web. |
| Congreso/Senado site returns 403 | Legislature | Monitor Agencia EFE parliamentary desk. Legislative tracking also available through BOE (Boletín Oficial de las Cortes Generales section). |
| BOE API downtime | BOE | Fall back to RSS feeds (complete daily summary). If RSS also fails, HTML scraping of daily edition index page. |
| BdE website maintenance | Banco de España | Monitor @BancoDeEspana on X. Major publications (monetary policy, financial stability) are simultaneously sent to financial wire services (Reuters, Bloomberg). |
| REPER site outage | EU Permanent Representation | Monitor @EspanaenUE on X, LinkedIn, and Bluesky. MAEC institutional page for REPER is a backup. EU Council press releases provide a parallel channel for Spain-relevant EU decisions. |
| Multiple ministry outages | Broad impact | Agencia EFE (state wire service) is the primary fallback — EFE dispatches are derived from government communications and typically appear within 30-60 minutes of official publication. La Moncloa's centralized press archive also captures communications from all ministries. |

---

*This supplement should be reviewed quarterly or upon any major government restructuring (cabinet reshuffles change ministry names and domains), change in administration (new governments frequently reorganize ministerial portfolios), or significant website migration (SharePoint version upgrades can break existing selectors and feed URLs).*
