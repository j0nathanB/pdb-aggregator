# Official Government Sources Supplement: MEXICO

**Primary language of political discourse: Spanish**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Mexico (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Mexico. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Government sources in Mexico are structurally centralized through the `gob.mx` platform — a unified federal portal operated by the Coordinación de Estrategia Digital Nacional. Most federal secretariats (SEDENA, SEMAR, SRE, SSPC, SHCP, SE) publish press releases through `gob.mx/{agency}/archivo/prensa` rather than maintaining independent press rooms. This creates a single extraction pattern for most agencies but also means a single point of failure if `gob.mx` experiences downtime or restructuring. Autonomous bodies (Banxico, INE, SCJN) and productive state enterprises (PEMEX, CFE) maintain fully independent web infrastructure.

---

## 1. OFFICIAL GOVERNMENT SOURCES: MEXICO

### 1.1 Head of Government — Presidencia de la República

| Field | Detail |
|---|---|
| **Institution** | Presidencia de la República |
| **Domain** | `gob.mx/presidencia` |
| **Entry Point URL** | `https://www.gob.mx/presidencia/archivo/prensa?idiom=es` |
| **RSS/Atom Feed** | None available. The gob.mx platform does not expose RSS feeds for individual agency press archives. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. The "mananera" (morning press conference) generates a stenographic version every weekday. Official communications (comunicados) are published same-day. |
| **Content Format** | HTML (articles on gob.mx). Stenographic versions are long-form HTML. Some attached PDFs for formal decrees. |
| **Extraction Method** | HTML scraping of `gob.mx/presidencia/archivo/prensa` listing page. Each item links to a full-text article page. Pagination via query parameters. |
| **Editorial Orientation** | Official government position. All content is produced by the Coordinación de Comunicación Social de la Presidencia. Framing reflects Morena/4T policy priorities. |
| **Why This Source** | The single authoritative source for presidential statements, policy announcements, and the daily "mananera" transcript. The stenographic versions contain the full Q&A with press corps, which frequently surfaces positions not captured in the formal comunicado. |
| **Access Notes** | No paywall, no authentication required. Some pages intermittently return "Challenge Validation" responses suggesting Cloudflare or similar bot protection on gob.mx. Rate limiting may apply. |

**Additional entry points:**
- Mananera transcripts: filtered via category "Versión estenográfica" on the press archive page
- Official decrees/acuerdos: published simultaneously in the DOF (see section 1.5)

---

### 1.2 Foreign Ministry — Secretaría de Relaciones Exteriores (SRE)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de Relaciones Exteriores (SRE) |
| **Domain** | `gob.mx/sre` / `sre.gob.mx` |
| **Entry Point URL** | `https://www.gob.mx/sre/archivo/prensa` |
| **RSS/Atom Feed** | None available on gob.mx. |
| **Language** | Spanish (primary); some communications issued bilingually for major diplomatic events |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Comunicados issued for diplomatic meetings, treaty actions, consular emergencies, multilateral votes. |
| **Content Format** | HTML on gob.mx. Formal diplomatic notes sometimes in PDF. |
| **Extraction Method** | HTML scraping of `gob.mx/sre/archivo/prensa` listing page. Same gob.mx template as Presidencia. |
| **Editorial Orientation** | Official foreign ministry position. Reflects Mexico's doctrinal commitment to non-intervention, sovereign equality, and multilateralism. Under Foreign Minister Juan Ramón de la Fuente, increased emphasis on UN system engagement. |
| **Why This Source** | The only primary source for Mexico's formal diplomatic positions, treaty ratifications, ambassador appointments, and bilateral/multilateral meeting readouts. Media coverage of SRE activity is invariably derived from these comunicados. |
| **Access Notes** | Same gob.mx infrastructure as Presidencia. The legacy `sre.gob.mx` domain hosts some subsites (consular portals, `embamex.sre.gob.mx` for embassy-specific releases) but the primary press feed is on gob.mx. |

**Additional entry points:**
- Embassy-level communications (US): `https://embamex.sre.gob.mx/eua/index.php/es/comunicados`
- SRE portals hub: `https://portales.sre.gob.mx/`

---

### 1.3 Defense / Security — SEDENA, SEMAR, SSPC, Gabinete de Seguridad

#### 1.3a Secretaría de la Defensa Nacional (SEDENA)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de la Defensa Nacional (SEDENA) |
| **Domain** | `gob.mx/defensa` / `sedena.gob.mx` |
| **Entry Point URL** | `https://www.gob.mx/defensa/es/archivo/prensa` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-5 per week. Comunicados issued for operations, seizures, detentions, institutional ceremonies. Procurement and budget information is not published via press releases. |
| **Content Format** | HTML on gob.mx. Operational bulletins frequently include infographic images. |
| **Extraction Method** | HTML scraping of gob.mx listing page. Same template. |
| **Editorial Orientation** | Official military communication. Highly controlled — releases only operational outcomes (seizures, detentions), never casualties, setbacks, or procurement details. Framing emphasizes results and institutional prestige. |
| **Why This Source** | The only direct window into SEDENA's operational tempo and strategic priorities. Despite the controlled nature, frequency and content of bulletins reveal operational focus areas (which cartels, which regions, which types of contraband). |
| **Access Notes** | The legacy `sedena.gob.mx` site exists but most current press content routes through gob.mx/defensa. Bot protection via gob.mx applies. |

#### 1.3b Secretaría de Marina (SEMAR)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de Marina — Armada de México (SEMAR) |
| **Domain** | `gob.mx/semar` |
| **Entry Point URL** | `https://www.gob.mx/semar/archivo/prensa` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 1-3 per week. Less frequent than SEDENA. Focus on naval operations, maritime interdiction, port security. |
| **Content Format** | HTML on gob.mx. |
| **Extraction Method** | HTML scraping of gob.mx listing page. Same template as other agencies. |
| **Editorial Orientation** | Official naval communication. Same controlled pattern as SEDENA. |
| **Why This Source** | Covers maritime security dimensions — Pacific and Gulf coast interdiction, port security, and SEMAR's institutional role — that SEDENA bulletins do not address. |
| **Access Notes** | Same gob.mx infrastructure. |

#### 1.3c Secretaría de Seguridad y Protección Ciudadana (SSPC)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de Seguridad y Protección Ciudadana (SSPC) |
| **Domain** | `gob.mx/sspc` / `seguridad.sspc.gob.mx` |
| **Entry Point URL** | `https://www.gob.mx/sspc/archivo/prensa?idiom=es` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. SSPC produces the most frequent security-related communications because it coordinates the Gabinete de Seguridad. |
| **Content Format** | HTML on gob.mx. |
| **Extraction Method** | HTML scraping of gob.mx listing page. |
| **Editorial Orientation** | Official security policy position. Under Omar García Harfuch, communications emphasize operational results (decomiso statistics, detention counts) and the "Estrategia Nacional de Seguridad." |
| **Why This Source** | SSPC is the civilian umbrella for security policy. Its bulletins aggregate results from SEDENA, SEMAR, Guardia Nacional, and FGR into unified security narratives. The Gabinete de Seguridad daily briefings are the primary government security reporting mechanism. |
| **Access Notes** | Same gob.mx infrastructure. |

#### 1.3d Gabinete de Seguridad (Security Cabinet)

| Field | Detail |
|---|---|
| **Institution** | Gabinete de Seguridad |
| **Domain** | `gabinetedeseguridad.gob.mx` / `seguridad.sspc.gob.mx` |
| **Entry Point URL** | `https://gabinetedeseguridad.gob.mx/informes/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `government_aligned` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Daily security reports (informes diarios). |
| **Content Format** | HTML. Informe pages contain structured data on security operations. |
| **Extraction Method** | HTML scraping. Separate site from gob.mx — different template. |
| **Editorial Orientation** | Aggregated security data from SEDENA, SEMAR, FGR, Guardia Nacional, SSPC. Designed to project government control narrative. |
| **Why This Source** | The daily security informes provide structured operational data (detentions, seizures, operations by agency) that individual agency bulletins present selectively. This is the closest thing to a consolidated security data feed. |
| **Access Notes** | Standalone domain. No known bot protection issues. Also accessible via `seguridad.sspc.gob.mx/noticias/`. |

---

### 1.4 Parliament / Legislature

#### 1.4a Senado de la República

| Field | Detail |
|---|---|
| **Institution** | Senado de la República (Senate) |
| **Domain** | `senado.gob.mx` / `comunicacionsocial.senado.gob.mx` |
| **Entry Point URL** | `https://comunicacionsocial.senado.gob.mx/informacion/comunicados` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at comunicacionsocial.senado.gob.mx/feed or /rss] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods (Feb-Apr, Sep-Dec). Reduced during recess. |
| **Content Format** | HTML. Comunicados are text-based press releases. |
| **Extraction Method** | HTML scraping. Separate infrastructure from gob.mx. |
| **Editorial Orientation** | Institutional — reflects majority (Morena) framing but includes minority-party boletines. |
| **Why This Source** | Treaty ratifications, ambassador confirmations, and committee hearings on foreign/security policy originate here. Committee testimony from SRE, SEDENA, and Banxico officials appears in Senate records before (or instead of) media coverage. |
| **Access Notes** | No paywall. Site can be slow. |

**Additional entry points:**
- Gaceta del Senado (parliamentary gazette): `https://www.senado.gob.mx/66/gaceta_del_senado/`
- Legislative information system (SEGOB): `https://sil.gobernacion.gob.mx/`

#### 1.4b Cámara de Diputados

| Field | Detail |
|---|---|
| **Institution** | Cámara de Diputados (Chamber of Deputies) |
| **Domain** | `diputados.gob.mx` / `comunicacionsocial.diputados.gob.mx` |
| **Entry Point URL** | `https://comunicacionsocial.diputados.gob.mx/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods. |
| **Content Format** | HTML (boletines). The Gaceta Parlamentaria is published as indexed HTML with embedded PDFs. |
| **Extraction Method** | HTML scraping. Multiple subdomains with different templates. |
| **Editorial Orientation** | Institutional. Majority-party framing dominates. |
| **Why This Source** | Budget approval, constitutional reform votes, and enabling legislation for executive policy (energy reform, security policy, trade implementation) originate here. The Gaceta Parlamentaria contains the full text of initiatives and voting records. |
| **Access Notes** | Multiple legacy subdomains (www5.diputados.gob.mx, web.diputados.gob.mx). Some subsites are poorly maintained. |

**Additional entry points:**
- Gaceta Parlamentaria: `https://gaceta.diputados.gob.mx/`
- Boletines archive: `http://www5.diputados.gob.mx/index.php/esl/Comunicacion/Boletines`
- Parliamentary chronicle: `https://cronica.diputados.gob.mx/`

---

### 1.5 Official Gazette — Diario Oficial de la Federación (DOF)

| Field | Detail |
|---|---|
| **Institution** | Diario Oficial de la Federación (DOF) |
| **Domain** | `dof.gob.mx` / `sidof.segob.gob.mx` |
| **Entry Point URL** | `https://www.dof.gob.mx/` (daily edition) / `https://sidof.segob.gob.mx/` (search system) |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the DOF is the constitutional publication vehicle for all federal laws, regulations, and executive orders |
| **Publication Frequency** | Daily (Edición Matutina, Monday-Friday). Ediciones Vespertinas (afternoon) for urgent decrees. |
| **Content Format** | HTML index pages linking to **PDF** documents. Individual decrees and regulations are published as PDFs. |
| **Extraction Method** | Index page scraping to identify new publications, then PDF download and text extraction. The SIDOF system (`sidof.segob.gob.mx`) provides a search interface with date-range filtering. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no federal law, regulation, international agreement, or executive order is legally binding until published in the DOF. This is the only source that provides definitive, timestamped legal text. Media reports on legislation are always downstream of DOF publication. |
| **Access Notes** | SSL certificate issues have been observed on `dof.gob.mx` (unable to verify first certificate). The SIDOF system at `sidof.segob.gob.mx` may be more reliable for automated access. Open data section available. User registration system exists but is not required for reading. |

---

### 1.6 Finance Ministry — Secretaría de Hacienda y Crédito Público (SHCP)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de Hacienda y Crédito Público (SHCP) |
| **Domain** | `gob.mx/shcp` / `shcp.gob.mx` |
| **Entry Point URL** | `https://www.gob.mx/shcp/archivo/prensa?idiom=es` |
| **RSS/Atom Feed** | None available on gob.mx. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Comunicados issued for fiscal policy announcements, public debt operations, tax policy changes, budget execution reports. |
| **Content Format** | HTML on gob.mx. Many comunicados link to attached PDF documents (statistical tables, budget reports). |
| **Extraction Method** | HTML scraping of gob.mx listing page. PDF extraction for statistical annexes. |
| **Editorial Orientation** | Official fiscal policy position. Technical language, data-heavy. |
| **Why This Source** | Primary source for federal budget execution, public debt operations, tax revenue data, and fiscal policy announcements. Essential for Economic & Technological Statecraft domain — SHCP comunicados are the raw data that El Financiero and El Economista interpret. |
| **Access Notes** | Same gob.mx infrastructure. The legacy `shcp.gob.mx` redirects to a responsive portal but primary press content is on gob.mx. Public finance data also at `finanzaspublicas.hacienda.gob.mx`. |

---

### 1.7 Central Bank — Banco de México (Banxico)

| Field | Detail |
|---|---|
| **Institution** | Banco de México (Banxico) |
| **Domain** | `banxico.org.mx` |
| **Entry Point URL** | `https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html` (monetary policy decisions) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Indicators RSS hub: `https://www.banxico.org.mx/estadisticas/rss-indicadores-banco-mexico.html`. Key feeds include: exchange rate (FIX), TIIE, CETES rates, international reserves, UDIs, remittances. Feed URL pattern: `https://www.banxico.org.mx/rsscb/rss?BMXC_canal={channel}&BMXC_idioma=es` |
| **Language** | Spanish (primary); English versions available for major publications |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (scheduled Thursdays at 1:00 PM). Quarterly inflation reports. Miscellaneous communications: weekly. RSS indicator feeds: real-time/daily updates. |
| **Content Format** | **PDF** for formal monetary policy announcements and minutes. HTML for miscellaneous communications. RSS feeds deliver structured data (exchange rates, interest rates). |
| **Extraction Method** | RSS feeds for indicator data (structured, machine-readable). PDF download and extraction for monetary policy decisions and minutes. HTML scraping for miscellaneous communications. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Victoria Rodríguez Ceja, perceived as somewhat accommodating to executive preferences on rate cuts. |
| **Why This Source** | Banxico is the only source for authoritative monetary policy decisions, inflation expectations, and official economic indicators. Its RSS feeds are the most machine-friendly government data source in Mexico. Monetary policy announcements move markets and are cited by all financial media. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained and reliable. Email subscription service also available at `https://www.banxico.org.mx/viewers/JSP/subscriptions.jsp`. English-language site at `banxico.org.mx/indexen.html`. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| FIX exchange rate | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es` |
| Interbank interest rate (TIIE) | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=tiie&BMXC_idioma=es` |
| CETES rate | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=cetes&BMXC_idioma=es` |
| International reserves | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=reserv&BMXC_idioma=es` |
| Remittances | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=remesa&BMXC_idioma=es` |
| UDIs | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=udis&BMXC_idioma=es` |
| Overnight funding rate | `https://www.banxico.org.mx/rsscb/rss?BMXC_canal=fondeo&BMXC_idioma=es` |

---

### 1.8 Trade / Commerce — Secretaría de Economía (SE)

| Field | Detail |
|---|---|
| **Institution** | Secretaría de Economía (SE) |
| **Domain** | `gob.mx/se` |
| **Entry Point URL** | `https://www.gob.mx/se/archivo/prensa?idiom=es` |
| **RSS/Atom Feed** | None available on gob.mx. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-4 per week. Communications cover trade negotiations (T-MEC/USMCA review), FDI announcements, tariff actions, nearshoring policy, and industrial policy. |
| **Content Format** | HTML on gob.mx. Trade statistics and reports in PDF. |
| **Extraction Method** | HTML scraping of gob.mx listing page. Same template. |
| **Editorial Orientation** | Official trade policy position. Under Secretary Marcelo Ebrard, communications emphasize T-MEC permanence, tariff elimination, and Mexico's positioning as a nearshoring destination. |
| **Why This Source** | Primary source for trade policy announcements, T-MEC review positions, tariff actions, and FDI data. Ebrard's dual role (former Foreign Minister, now heading Economy) makes SE communications unusually relevant to diplomatic alignment domain. |
| **Access Notes** | Same gob.mx infrastructure. DataMéxico platform (`economia.gob.mx/datamexico/`) provides open data on trade and economic indicators. SNICE trade information system at `snice.gob.mx`. |

---

### 1.9 Intelligence / National Security — Centro Nacional de Inteligencia (CNI)

| Field | Detail |
|---|---|
| **Institution** | Centro Nacional de Inteligencia (CNI) — successor to CISEN |
| **Domain** | `gob.mx/cni` / `cni.gob.mx` |
| **Entry Point URL** | `https://www.gob.mx/cni` |
| **RSS/Atom Feed** | None available. |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. CNI publishes virtually no operational or policy communications. Transparency obligations are met through `cni.gob.mx/transparencia/`. |
| **Content Format** | Minimal HTML on gob.mx. Transparency documents in PDF. |
| **Extraction Method** | Periodic check of gob.mx/cni for any new publications. Transparency portal scraping for organizational/budget changes. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. CNI's public-facing communications are almost nonexistent — the agency operates through internal channels. Its transparency portal may surface organizational restructuring, budget changes, or leadership appointments that indicate strategic shifts. The real intelligence signal from CNI comes through leaks to investigative outlets (Proceso, Animal Politico) rather than official channels. |
| **Access Notes** | `gob.mx/cni` is a minimal page. `cni.gob.mx/transparencia/` hosts transparency compliance documents. The CNI is a deconcentrated body attached to the SSPC. |

---

### 1.10 Country-Specific Institutions

#### 1.10a PEMEX (Petróleos Mexicanos)

| Field | Detail |
|---|---|
| **Institution** | Petróleos Mexicanos (PEMEX) |
| **Domain** | `pemex.com` |
| **Entry Point URL** | `https://www.pemex.com/saladeprensa/boletines_nacionales/Paginas/default.aspx` |
| **RSS/Atom Feed** | **Yes.** RSS hub: `https://www.pemex.com/Paginas/rss.aspx`. National bulletins: `https://www.pemex.com/saladeprensa/boletines_nacionales/_layouts/listfeed.aspx?List={7626F8B4-FCAD-41B1-AEE3-2B66E60B61E0}`. Regional bulletins: `https://www.pemex.com/saladeprensa/boletines_regionales/_layouts/listfeed.aspx?List={2A313372-2769-48E1-A21D-124F4D3D013E}` |
| **Language** | Spanish |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 2-5 per week. Comunicados cover production data, financial results, refinery operations, exploration, and accidents/incidents. |
| **Content Format** | HTML (SharePoint-based). PDF attachments for financial reports and statistical data. |
| **Extraction Method** | RSS feeds for national and regional bulletins. SharePoint list feeds. |
| **Editorial Orientation** | State enterprise communication. Emphasizes production targets, investment, and energy sovereignty narrative. Financial difficulties and debt levels are acknowledged in mandatory disclosures but not highlighted in press communications. |
| **Why This Source** | PEMEX is Mexico's largest enterprise and a central pillar of the 4T energy sovereignty doctrine. Production data, refinery output, financial health, and strategic investments directly affect fiscal stability and trade relationships. PEMEX debt is a sovereign credit risk factor monitored by international markets. |
| **Access Notes** | SharePoint-based site. RSS feeds functional. No bot protection observed. Deer Park refinery (US) has a separate press section in English. |

#### 1.10b CFE (Comisión Federal de Electricidad)

| Field | Detail |
|---|---|
| **Institution** | Comisión Federal de Electricidad (CFE) |
| **Domain** | `cfe.mx` |
| **Entry Point URL** | `https://app.cfe.mx/Aplicaciones/OTROS/Boletines/Prensa?c=2` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 1-3 per week. Communications cover electricity generation, infrastructure projects, renewable energy, rate adjustments, and financial results. |
| **Content Format** | HTML. Boletines de prensa on a custom application portal. |
| **Extraction Method** | HTML scraping of the boletines application. Custom URL structure (`app.cfe.mx/Aplicaciones/...`). |
| **Editorial Orientation** | State enterprise communication. Emphasizes energy sovereignty, infrastructure investment, and public service mission. |
| **Why This Source** | CFE is the monopoly electricity transmitter/distributor and Mexico's second-largest state enterprise. Energy policy (renewable integration, fossil fuel dependence, private sector participation) is a structural issue for economic statecraft and climate diplomacy. |
| **Access Notes** | The boletines app runs on a separate subdomain (`app.cfe.mx`). Main `cfe.mx` is consumer-facing. No known bot protection on the press section. |

#### 1.10c INE (Instituto Nacional Electoral)

| Field | Detail |
|---|---|
| **Institution** | Instituto Nacional Electoral (INE) |
| **Domain** | `ine.mx` / `centralelectoral.ine.mx` |
| **Entry Point URL** | `https://centralelectoral.ine.mx/` |
| **RSS/Atom Feed** | Likely available at `https://centralelectoral.ine.mx/feed/` (WordPress site). [VERIFY RSS] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints |
| **Publication Frequency** | Daily or near-daily on Central Electoral. Higher frequency during electoral periods. |
| **Content Format** | HTML (WordPress). |
| **Extraction Method** | WordPress RSS feed (if confirmed). HTML scraping of Central Electoral. URL pattern: `centralelectoral.ine.mx/YYYY/MM/DD/slug/`. |
| **Editorial Orientation** | Autonomous electoral authority. Institutionally committed to nonpartisan framing. Under sustained political pressure from Morena — the 2025 institutional reform reduced INE's autonomy. |
| **Why This Source** | INE's communications reveal the state of democratic institutional integrity — a key Domestic Constraints indicator. Electoral calendar, party registration decisions, campaign finance rulings, and institutional defense statements all surface here. |
| **Access Notes** | WordPress-based Central Electoral site. Main `ine.mx` is institutional. No paywall. |

#### 1.10d SCJN (Suprema Corte de Justicia de la Nación)

| Field | Detail |
|---|---|
| **Institution** | Suprema Corte de Justicia de la Nación (SCJN) |
| **Domain** | `scjn.gob.mx` |
| **Entry Point URL** | `https://www.scjn.gob.mx/multimedia/comunicados` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | 2-5 per week. Comunicados issued for major rulings, plenary session decisions, constitutional controversies, and institutional statements. |
| **Content Format** | HTML. Stenographic versions of sessions available. Press multimedia section includes video, audio, and text. |
| **Extraction Method** | HTML scraping of comunicados page. Separate infrastructure from gob.mx. |
| **Editorial Orientation** | Judicial institution. Following the 2024 judicial reform (elected judges), the SCJN is in a period of profound institutional transformation. Communications reflect the tension between institutional continuity and political restructuring. |
| **Why This Source** | SCJN rulings on constitutional controversies — energy policy, electoral law, military jurisdiction, indigenous rights, trade agreements — directly constrain or enable executive action across all five analytical domains. The 2024 judicial reform makes SCJN institutional communications an active indicator of democratic institutional health. |
| **Access Notes** | Independent infrastructure (not on gob.mx). The judicial search system (Semanario Judicial de la Federación) at `sjf.scjn.gob.mx` provides the full text of rulings. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | gob.mx Platform |
|---|---|---|---|---|---|---|---|
| 1 | Presidencia | `gob.mx/presidencia/archivo/prensa` | No | P1 | HTML | Daily | Yes |
| 2 | SRE | `gob.mx/sre/archivo/prensa` | No | P1 | HTML/PDF | Daily | Yes |
| 3a | SEDENA | `gob.mx/defensa/es/archivo/prensa` | No | P1 | HTML | 2-5/week | Yes |
| 3b | SEMAR | `gob.mx/semar/archivo/prensa` | No | P1 | HTML | 1-3/week | Yes |
| 3c | SSPC | `gob.mx/sspc/archivo/prensa` | No | P1 | HTML | Daily | Yes |
| 3d | Gabinete de Seguridad | `gabinetedeseguridad.gob.mx/informes/` | No | P1 | HTML | Daily | No |
| 4a | Senado | `comunicacionsocial.senado.gob.mx/informacion/comunicados` | [VERIFY] | P2 | HTML | Daily (session) | No |
| 4b | Cámara de Diputados | `comunicacionsocial.diputados.gob.mx/` | [VERIFY] | P2 | HTML/PDF | Daily (session) | No |
| 5 | DOF | `dof.gob.mx` / `sidof.segob.gob.mx` | No | P2 | PDF | Daily | No |
| 6 | SHCP | `gob.mx/shcp/archivo/prensa` | No | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | Banxico | `banxico.org.mx/publicaciones-y-prensa/...` | **Yes** (multiple) | P2 | PDF/HTML/RSS | Variable | No |
| 8 | Sec. Economía | `gob.mx/se/archivo/prensa` | No | P2 | HTML | 2-4/week | Yes |
| 9 | CNI | `gob.mx/cni` | No | P2 | Minimal | Negligible | Yes |
| 10a | PEMEX | `pemex.com/saladeprensa/boletines_nacionales/...` | **Yes** | P2 | HTML/PDF | 2-5/week | No |
| 10b | CFE | `app.cfe.mx/Aplicaciones/OTROS/Boletines/Prensa` | [VERIFY] | P2 | HTML | 1-3/week | No |
| 10c | INE | `centralelectoral.ine.mx/` | [VERIFY] | P2 | HTML | Daily | No |
| 10d | SCJN | `scjn.gob.mx/multimedia/comunicados` | [VERIFY] | P2 | HTML | 2-5/week | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Mexico Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/mx.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: mx_presidencia
    name: Presidencia de la República
    domain: gob.mx
    entry_url: "https://www.gob.mx/presidencia/archivo/prensa?idiom=es"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Mananera transcripts published daily. Bot protection (Cloudflare) may require rotating headers."

  - id: mx_sre
    name: Secretaría de Relaciones Exteriores (SRE)
    domain: gob.mx
    entry_url: "https://www.gob.mx/sre/archivo/prensa"
    rss_feed: null
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
    notes: "Embassy-level releases at embamex.sre.gob.mx (per-country subdomains)."

  - id: mx_sedena
    name: Secretaría de la Defensa Nacional (SEDENA)
    domain: gob.mx
    entry_url: "https://www.gob.mx/defensa/es/archivo/prensa"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Controlled bulletins only. No procurement or casualty data."

  - id: mx_semar
    name: Secretaría de Marina (SEMAR)
    domain: gob.mx
    entry_url: "https://www.gob.mx/semar/archivo/prensa"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Maritime interdiction and naval operations focus."

  - id: mx_sspc
    name: Secretaría de Seguridad y Protección Ciudadana (SSPC)
    domain: gob.mx
    entry_url: "https://www.gob.mx/sspc/archivo/prensa?idiom=es"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Umbrella for Gabinete de Seguridad. García Harfuch operational reports."

  - id: mx_gabinete_seguridad
    name: Gabinete de Seguridad
    domain: gabinetedeseguridad.gob.mx
    entry_url: "https://gabinetedeseguridad.gob.mx/informes/"
    rss_feed: null
    language: es
    type: government_aligned
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Daily consolidated security reports. Separate infrastructure from gob.mx."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: mx_senado
    name: Senado de la República
    domain: senado.gob.mx
    entry_url: "https://comunicacionsocial.senado.gob.mx/informacion/comunicados"
    rss_feed: null  # [VERIFY]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Treaty ratifications, ambassador confirmations, committee testimony."

  - id: mx_diputados
    name: Cámara de Diputados
    domain: diputados.gob.mx
    entry_url: "https://comunicacionsocial.diputados.gob.mx/"
    rss_feed: null  # [VERIFY]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Budget votes, constitutional reforms. Gaceta Parlamentaria at gaceta.diputados.gob.mx."

  - id: mx_dof
    name: Diario Oficial de la Federación (DOF)
    domain: dof.gob.mx
    entry_url: "https://sidof.segob.gob.mx/"
    rss_feed: null
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
    content_format: pdf
    extraction_method: pdf_download_extract
    poll_interval_hours: 6
    notes: "SSL certificate issues on dof.gob.mx. Use sidof.segob.gob.mx as primary. All federal law is published here."

  - id: mx_shcp
    name: Secretaría de Hacienda y Crédito Público (SHCP)
    domain: gob.mx
    entry_url: "https://www.gob.mx/shcp/archivo/prensa?idiom=es"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Fiscal policy, public debt, budget execution. PDF annexes contain statistical tables."

  - id: mx_banxico
    name: Banco de México (Banxico)
    domain: banxico.org.mx
    entry_url: "https://www.banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/anuncios-politica-monetaria-t.html"
    rss_feed:
      indicators_hub: "https://www.banxico.org.mx/estadisticas/rss-indicadores-banco-mexico.html"
      fix_exchange_rate: "https://www.banxico.org.mx/rsscb/rss?BMXC_canal=fix&BMXC_idioma=es"
      tiie: "https://www.banxico.org.mx/rsscb/rss?BMXC_canal=tiie&BMXC_idioma=es"
      cetes: "https://www.banxico.org.mx/rsscb/rss?BMXC_canal=cetes&BMXC_idioma=es"
      reserves: "https://www.banxico.org.mx/rsscb/rss?BMXC_canal=reserv&BMXC_idioma=es"
      remittances: "https://www.banxico.org.mx/rsscb/rss?BMXC_canal=remesa&BMXC_idioma=es"
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best machine-readable government source in Mexico. RSS for indicators, PDF for policy decisions. Monetary policy Thursdays at 1pm. English site available."

  - id: mx_economia
    name: Secretaría de Economía (SE)
    domain: gob.mx
    entry_url: "https://www.gob.mx/se/archivo/prensa?idiom=es"
    rss_feed: null
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "T-MEC review, tariffs, nearshoring, FDI. DataMexico at economia.gob.mx/datamexico/."

  - id: mx_cni
    name: Centro Nacional de Inteligencia (CNI)
    domain: gob.mx
    entry_url: "https://www.gob.mx/cni"
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
    notes: "Effectively silent agency. Transparency portal at cni.gob.mx/transparencia/. Real signal comes via leaks to Proceso/Animal Político."

  - id: mx_pemex
    name: Petróleos Mexicanos (PEMEX)
    domain: pemex.com
    entry_url: "https://www.pemex.com/saladeprensa/boletines_nacionales/Paginas/default.aspx"
    rss_feed:
      national_bulletins: "https://www.pemex.com/saladeprensa/boletines_nacionales/_layouts/listfeed.aspx?List={7626F8B4-FCAD-41B1-AEE3-2B66E60B61E0}"
      regional_bulletins: "https://www.pemex.com/saladeprensa/boletines_regionales/_layouts/listfeed.aspx?List={2A313372-2769-48E1-A21D-124F4D3D013E}"
      speeches: "https://www.pemex.com/saladeprensa/discursos/_layouts/listfeed.aspx?List={BE973D09-094F-4A56-8677-062D1CC8DB44}"
    language: es
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "2-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "SharePoint-based. RSS feeds functional. Deer Park refinery press separate (English)."

  - id: mx_cfe
    name: Comisión Federal de Electricidad (CFE)
    domain: cfe.mx
    entry_url: "https://app.cfe.mx/Aplicaciones/OTROS/Boletines/Prensa?c=2"
    rss_feed: null  # [VERIFY]
    language: es
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Custom application portal on app.cfe.mx subdomain."

  - id: mx_ine
    name: Instituto Nacional Electoral (INE)
    domain: ine.mx
    entry_url: "https://centralelectoral.ine.mx/"
    rss_feed: "https://centralelectoral.ine.mx/feed/"  # [VERIFY - WordPress site likely has /feed/]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 12
    notes: "WordPress site (Astra/Elementor). RSS feed likely at /feed/. Electoral calendar drives frequency."

  - id: mx_scjn
    name: Suprema Corte de Justicia de la Nación (SCJN)
    domain: scjn.gob.mx
    entry_url: "https://www.scjn.gob.mx/multimedia/comunicados"
    rss_feed: null  # [VERIFY]
    language: es
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Post-judicial reform (elected judges). Full rulings at sjf.scjn.gob.mx."

# Extraction pattern for gob.mx agencies
gob_mx_shared_config:
  base_url_pattern: "https://www.gob.mx/{agency_slug}/archivo/prensa"
  agencies_on_platform:
    - presidencia
    - sre
    - defensa  # SEDENA uses "defensa" not "sedena"
    - semar
    - sspc
    - shcp
    - se  # Secretaría de Economía
    - cni
  pagination: query_parameter  # ?page=N
  bot_protection: cloudflare_challenge  # intermittent
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "es-MX,es;q=0.9"
  rate_limit: "max 1 request per 3 seconds per agency"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Mexican government communications are systematically optimistic and omission-heavy. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage.

- **Presidencia**: Cross-reference mananera statements against same-day reporting in El Universal and Reforma. Discrepancies between the stenographic version and media summaries frequently reveal editorial framing choices on both sides.
- **SRE**: Diplomatic comunidados should be triangulated with El Pais Mexico (external perspective) and La Jornada (government-aligned framing). When SRE and La Jornada framing diverges, it signals internal policy tension.
- **SEDENA/SEMAR**: Military bulletins report outcomes (seizures, detentions) but never casualties, operational failures, or procurement costs. Cross-reference with Proceso (military institutional coverage), InSight Crime (operational analysis), and Animal Politico (data-driven verification of official statistics).
- **SSPC/Gabinete de Seguridad**: Garcia Harfuch's daily security informes present aggregated statistics designed to show improvement. Cross-reference decomiso and detention figures against Semanario Zeta (border region), Pie de Pagina (community-level impact), and El Universal (national crime data).
- **Banxico**: Monetary policy decisions are technically rigorous and less subject to political distortion, but the selection of what to emphasize in comunicados reflects institutional positioning. Cross-reference with El Financiero and El Economista for market interpretation.
- **SHCP**: Fiscal data is generally reliable in headline numbers but presentation framing (base period selection, seasonal adjustment choices) can obscure trends. El Financiero provides the sharpest independent fiscal analysis.
- **PEMEX/CFE**: State enterprise communications systematically overstate production achievements and understate financial difficulties. Cross-reference with El Financiero (financial analysis), Reforma (investigative), and Bloomberg (international investor perspective).

**4.2 The gob.mx centralization effect**

Seven of Mexico's ten government source categories publish through the centralized gob.mx platform. This creates operational efficiency (single extraction pattern) but also means:
- Platform-wide outages affect all seven sources simultaneously
- Template changes propagate across all agencies
- The Coordinacion de Estrategia Digital Nacional can modify or remove content centrally
- Publication timing is subject to platform-level approval workflows

Sources outside gob.mx (Banxico, PEMEX, legislature, judiciary) operate on independent infrastructure and are not subject to these constraints.

**4.3 The CNI silence problem**

Mexico's intelligence agency (CNI) produces effectively zero public communications. This is a structural gap that cannot be filled by monitoring. Intelligence-relevant signals surface through:
- Leaks to investigative media (Proceso, Animal Politico, Aristegui Noticias)
- SSPC communications that reference "intelligence-led operations"
- Congressional committee testimony (when senators question CNI officials)
- DOF publications of organizational/budget changes

The pipeline should not allocate significant resources to polling CNI's gob.mx page but should flag any new publication as a high-priority anomaly.

**4.4 Legislative gap: committee proceedings**

The existing Source Intelligence Map identifies parliamentary transcripts as a blind spot. The Gaceta Parlamentaria (both Senate and Chamber of Deputies) contains committee-level proceedings, including testimony from SEDENA, SRE, and Banxico officials, that no media outlet fully covers. However, these are published in unstructured formats (long HTML documents, sometimes PDF) with no RSS feeds, making automated extraction difficult. Prioritize: (a) foreign affairs committee sessions, (b) defense/security committee sessions, (c) budget committee hearings during the annual Paquete Economico review (September-December).

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for gob.mx

The gob.mx platform hosts 7 of 17 monitored government endpoints. A single scraper module with agency-slug parameterization can service all seven:

- **URL pattern**: `https://www.gob.mx/{slug}/archivo/prensa?idiom=es&page={n}`
- **Agency slugs**: `presidencia`, `sre`, `defensa`, `semar`, `sspc`, `shcp`, `se`, `cni`
- **Article URL pattern**: `https://www.gob.mx/{slug}/prensa/{article-slug}` or `https://www.gob.mx/{slug}/articulos/{article-slug}`
- **Rate limit**: Enforce minimum 3-second intervals between requests. Rotate User-Agent headers.
- **Bot protection**: gob.mx intermittently serves Cloudflare "Challenge Validation" pages. Implement retry with exponential backoff. Consider headless browser fallback for persistent challenges.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Only two government sources provide functional RSS feeds:

1. **Banxico**: Multiple indicator-specific RSS feeds (exchange rates, interest rates, reserves). These are structured data suitable for direct parsing. The monetary policy announcements page does not have RSS — those are PDFs published on a fixed schedule (8 times/year, Thursdays at 1:00 PM).

2. **PEMEX**: SharePoint ListFeed-based RSS for national bulletins, regional bulletins, speeches, interviews, and presentations. SharePoint RSS feeds are functional but may return XML with SharePoint-specific namespaces requiring custom parsing.

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Three sources publish primarily or substantially in PDF:
- **DOF**: All legal texts are PDF. Require OCR-capable extraction for scanned historical documents; recent publications are text-based PDFs.
- **Banxico**: Monetary policy decisions and minutes are multi-page PDF. Text-based, well-structured.
- **SHCP**: Statistical annexes to comunicados are PDF with tables. May require table extraction (tabula/camelot).

### 5.4 Language and Encoding

All government sources publish in Spanish. Banxico provides parallel English versions for major publications. PEMEX Deer Park refinery has an English press section. All gob.mx content is UTF-8 encoded. Some legacy subsites (Chamber of Deputies, older SEDENA pages) may serve content with Latin-1 encoding — normalize to UTF-8 on ingestion.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A presidential decree appears in Presidencia comunicados, the DOF, and often SHCP or SE comunicados
- Security operations appear in SEDENA, SEMAR, SSPC, and Gabinete de Seguridad bulletins
- Treaty actions appear in SRE, Presidencia, and Senate communications

Implement content-hash deduplication. Use the DOF publication as the canonical version for legal texts. Use the originating agency (SRE for diplomatic, SEDENA for military) as canonical for operational communications.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Presidencia, SRE, SSPC | Every 2 hours | Daily publication, policy-critical |
| P1-Standard | SEDENA, SEMAR, Gabinete de Seguridad | Every 4 hours | Less frequent but high-priority when published |
| P2-Active | Senado, Diputados, SHCP, Banxico, SE, PEMEX | Every 6 hours | Regular publishing schedule |
| P2-Low | DOF, CFE, INE, SCJN | Every 12 hours | Important but slower publication cycle |
| P2-Minimal | CNI | Weekly | Effectively silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| gob.mx platform outage | Presidencia, SRE, SEDENA, SEMAR, SSPC, SHCP, SE, CNI | Monitor @PresidenciaMX, @SRE_mx, @SSPCMexico on X for real-time communications. Government social media often precedes web publication. |
| DOF SSL certificate failure | DOF | Use SIDOF mirror at `sidof.segob.gob.mx`. Content is identical. |
| Cloudflare bot challenge on gob.mx | All gob.mx agencies | Headless browser rendering (Playwright/Puppeteer). Alternatively, many gob.mx comunicados are syndicated to government-aligned media (La Jornada) within minutes. |
| PEMEX SharePoint downtime | PEMEX | Monitor @Abordo_Pemex on X. Financial disclosures also filed with BMV (Mexican Stock Exchange) and SEC (for international bonds). |
| Legislative site maintenance | Senado, Diputados | SIL (Sistema de Informacion Legislativa) at `sil.gobernacion.gob.mx` provides parallel legislative tracking maintained by SEGOB. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of the gob.mx platform, change in government administration, or creation/dissolution of federal agencies.*
