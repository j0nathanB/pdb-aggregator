# Official Government Sources Supplement: BRAZIL

**Primary language of political discourse: Portuguese**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Brazil (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Brazil. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Brazil's government web infrastructure is built on the unified `gov.br` platform — a Plone-based federal portal administered by the Secretaria de Governo Digital. Most federal ministries and agencies publish news and press releases through `gov.br/{agency}/pt-br/assuntos/noticias` or `gov.br/{agency}/pt-br/centrais-de-conteudo/noticias`, though URL patterns vary by ministry (unlike Mexico's strictly uniform `gob.mx/{agency}/archivo/prensa`). The gov.br platform supports RSS syndication via Plone's built-in `RSS` path suffix on listing pages, enabling feed access for most ministry news sections. Autonomous bodies (BCB, STF, TSE) and the legislature (Senado, Camara) maintain fully independent web infrastructure with their own RSS feeds and, in the case of the BCB, structured open-data APIs. State enterprises (Petrobras) operate independent press portals.

---

## 1. OFFICIAL GOVERNMENT SOURCES: BRAZIL

### 1.1 Head of Government — Presidência da República (Planalto)

| Field | Detail |
|---|---|
| **Institution** | Presidência da República |
| **Domain** | `gov.br/planalto` |
| **Entry Point URL** | `https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias` |
| **RSS/Atom Feed** | **Yes.** Gov.br Plone platform exposes RSS on listing pages. Feed URL: `https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias/RSS` [VERIFY RSS] |
| **Language** | Portuguese (English section at `gov.br/planalto/en/latest-news`) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Presidential speeches, decrees (decretos), vetoes (vetos), bilateral/multilateral meeting readouts, and official travel announcements are published same-day. |
| **Content Format** | HTML on gov.br. Some attached PDFs for formal decrees. Video embeds from TV Brasil/Canal Gov for speeches. |
| **Extraction Method** | RSS polling (if feed confirmed) or HTML scraping of the noticias listing page. Pagination via `?b_start:int=N` (Plone-style, 30 items per page). |
| **Editorial Orientation** | Official government position. All content produced by the Secretaria de Comunicação Social (SECOM). Framing reflects Lula/PT administration priorities — South-South cooperation, multilateral engagement, social policy. |
| **Why This Source** | The single authoritative source for presidential statements, decree signings, bilateral meeting readouts, and foreign-policy directives. Unlike Mexico's daily "mananera," Brazil does not have a fixed daily press conference — presidential communications are event-driven, making monitoring cadence less predictable. |
| **Access Notes** | No paywall. Gov.br occasionally returns 403 responses to automated requests; rotate User-Agent headers. English news available at `gov.br/planalto/en/latest-news` with its own RSS endpoint at `gov.br/en/government-of-brazil/latest-news/latest-news/RSS`. |

**Additional entry points:**
- SECOM (Secretaria de Comunicação Social): `https://www.gov.br/secom/pt-br/acompanhe-a-secom/noticias` — cross-government communications hub
- Agência Gov (government wire): `https://agenciagov.ebc.com.br/noticias` — EBC-operated wire service that redistributes all ministry communications
- Portal da Legislação (legislation RSS): `https://www4.planalto.gov.br/legislacao/rss` — RSS feed for new legislation signed by the President

---

### 1.2 Foreign Ministry — Ministério das Relações Exteriores (MRE / Itamaraty)

| Field | Detail |
|---|---|
| **Institution** | Ministério das Relações Exteriores (MRE) — commonly called Itamaraty |
| **Domain** | `gov.br/mre` |
| **Entry Point URL** | `https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa` |
| **RSS/Atom Feed** | Gov.br Plone RSS likely available at: `https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa/RSS` [VERIFY RSS]. Email distribution list available at `https://imprensamaillist.itamaraty.gov.br/`. |
| **Language** | Portuguese (primary); English press releases at `gov.br/mre/en/contact-us/press-area/press-releases` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. "Notas à imprensa" (press notes) issued for diplomatic meetings, treaty actions, multilateral votes, consular emergencies, and bilateral readouts. Separate "comunicados conjuntos" (joint communiqués) for summit-level events. |
| **Content Format** | HTML on gov.br. Formal diplomatic notes sometimes in PDF. |
| **Extraction Method** | RSS polling (if feed confirmed) or HTML scraping of the notas-a-imprensa listing page. Email subscription via Itamaraty mailing list as fallback. |
| **Editorial Orientation** | Official foreign ministry position. Reflects Itamaraty's institutional commitment to multilateralism, South-South cooperation, and "active non-alignment" (não-alinhamento ativo). Under Foreign Minister Mauro Vieira, emphasis on BRICS expansion, UN Security Council reform, and Mercosur-EU agreement finalization. |
| **Why This Source** | The only primary source for Brazil's formal diplomatic positions, bilateral/multilateral communiqués, ambassador appointments, and treaty ratifications. "Notas à imprensa" are the canonical signal of Itamaraty's declared posture. Media coverage (Folha, O Globo) is invariably derived from these notes. |
| **Access Notes** | Gov.br platform. The English press releases section provides parallel translations of major diplomatic communications. The Itamaraty mailing list (`imprensamaillist.itamaraty.gov.br`) is a reliable push-based alternative to polling. |

**Additional entry points:**
- English press releases: `https://www.gov.br/mre/en/contact-us/press-area/press-releases`
- Discursos (speeches): `https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/discursos-artigos-e-entrevistas`
- Social media: `@ItamaratyGovBr` on X (active, often publishes notas before web)

---

### 1.3 Defense Ministry — Ministério da Defesa

| Field | Detail |
|---|---|
| **Institution** | Ministério da Defesa |
| **Domain** | `gov.br/defesa` |
| **Entry Point URL** | `https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias` |
| **RSS/Atom Feed** | Gov.br Plone RSS likely available at: `https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias/RSS` [VERIFY RSS] |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Communications cover military exercises, defense cooperation agreements, procurement milestones, ministerial meetings, and force deployment announcements. Frequency increases during international exercises (e.g., UNITAS, Formosa) and crises (Amazon operations). |
| **Content Format** | HTML on gov.br. Pagination via `?b_start:int=30`. Some attached PDF documents for institutional reports. |
| **Extraction Method** | RSS polling or HTML scraping. Same gov.br Plone template as other ministries. |
| **Editorial Orientation** | Official defense ministry communication. Under Minister José Múcio Monteiro, communications emphasize civilian control, institutional modernization, and defense cooperation. Post-January 8 (2023), messaging carefully distinguishes institutional armed forces from political actors. |
| **Why This Source** | The only direct window into the Defense Ministry's strategic priorities, cooperation agreements, and procurement decisions. Brazil's unified defense ministry coordinates Army (Exército), Navy (Marinha), and Air Force (Aeronáutica) — all of which also publish independently but route strategic communications through the ministry. |
| **Access Notes** | Gov.br platform. The three service branches maintain separate gov.br presences (`gov.br/exercito`, `gov.br/marinha`, `gov.br/aeronautica`) with their own noticias sections, but strategic-level announcements originate at the ministry level. Agência Gov (`agenciagov.ebc.com.br/noticias/defesa`) syndicates defense ministry news. |

**Additional entry points:**
- Exército Brasileiro: `https://www.gov.br/exercito/pt-br/centrais-de-conteudo/noticias`
- Marinha do Brasil: `https://www.gov.br/marinha/pt-br/noticias`
- Força Aérea Brasileira: `https://www.gov.br/aeronautica/pt-br/assuntos/noticias`
- Área de imprensa: `https://www.gov.br/defesa/pt-br/area-de-imprensa`
- Social media: `@DefesaGovBr` on X

---

### 1.4 Parliament / Legislature

#### 1.4a Senado Federal (Federal Senate)

| Field | Detail |
|---|---|
| **Institution** | Senado Federal |
| **Domain** | `senado.leg.br` |
| **Entry Point URL** | `https://www12.senado.leg.br/noticias/ultimas` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Main feed: `https://www12.senado.leg.br/noticias/feed`. All news: `https://www12.senado.leg.br/noticias/feed/todasnoticias`. Topic-specific feeds available for: Agência Senado, Comissões, Congresso Nacional, CPIs, Cultura, Entrevista, Especial, Institucional, Investigações, Mercosul, Orçamento, Plenário, Presidência, Projetos. |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods (February-July, August-December). Reduced during recess. Agência Senado produces 10-30 items per day during active sessions. |
| **Content Format** | HTML. Plone-based site with structured article pages. |
| **Extraction Method** | RSS polling (well-maintained feeds). Multiple topic-specific feeds allow targeted monitoring. |
| **Editorial Orientation** | Institutional — Agência Senado covers proceedings from all parties. Not editorially aligned with the government majority, unlike executive branch sources. |
| **Why This Source** | Treaty ratifications (including Mercosur-EU), ambassador confirmations, CRE (Comissão de Relações Exteriores e Defesa Nacional) hearings, defense budget votes, and constitutional amendment deliberations all originate here. The CRE's hearings with Itamaraty and Defense Ministry officials produce testimony not available through executive sources. |
| **Access Notes** | Independent infrastructure from gov.br. RSS feeds are well-maintained and reliable. No paywall. No bot protection observed. |

**Additional entry points:**
- Senado Agora (real-time plenary): `https://www12.senado.leg.br/noticias/senado-agora`
- Comissão de Relações Exteriores (CRE): `https://www.senado.leg.br/comissoes/comissao?codcol=58`

#### 1.4b Câmara dos Deputados (Chamber of Deputies)

| Field | Detail |
|---|---|
| **Institution** | Câmara dos Deputados |
| **Domain** | `camara.leg.br` |
| **Entry Point URL** | `https://www.camara.leg.br/noticias` |
| **RSS/Atom Feed** | **Yes — extensive topic-based feeds.** Hub page: `https://www.camara.leg.br/noticias/rss`. Key feeds: Latest news (`/noticias/rss/ultimas-noticias`), Relações Exteriores (`/noticias/rss/dinamico/RELACOES-EXTERIORES`), Economia (`/noticias/rss/dinamico/ECONOMIA`), Segurança (`/noticias/rss/dinamico/SEGURANCA`), Política (`/noticias/rss/dinamico/POLITICA`). 23 topic-specific feeds available. |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods. Agência Câmara produces high-volume coverage — 20-40 items per day during active sessions. |
| **Content Format** | HTML. Well-structured article pages with topic tagging. |
| **Extraction Method** | RSS polling — the most feed-rich government source in Brazil with 23 topic-specific feeds. The Relações Exteriores and Segurança feeds are directly relevant for pipeline monitoring. |
| **Editorial Orientation** | Institutional. Agência Câmara covers all party activities. |
| **Why This Source** | Budget approval (Lei Orçamentária Anual), constitutional amendment votes (PECs), enabling legislation for trade agreements, defense appropriations, and bancada dynamics (ruralista, evangélica) that constrain foreign-policy action all originate here. |
| **Access Notes** | Independent infrastructure from gov.br. RSS feeds well-maintained. Legacy URLs at `www2.camara.leg.br/agencia/assinarRSS.html` may still function. No paywall. |

**Additional entry points:**
- RSS hub: `https://www.camara.leg.br/noticias/rss`
- Dados Abertos (open data API): `https://dadosabertos.camara.leg.br/` — structured legislative data including voting records and propositions
- Comissão de Relações Exteriores e Defesa Nacional (CREDN): tracked via the Segurança and Relações Exteriores RSS feeds

---

### 1.5 Official Gazette — Diário Oficial da União (DOU)

| Field | Detail |
|---|---|
| **Institution** | Diário Oficial da União (DOU) — published by the Imprensa Nacional |
| **Domain** | `in.gov.br` |
| **Entry Point URL** | `https://www.in.gov.br/leiturajornal` (daily edition reader) / `https://www.in.gov.br/consulta` (search system) |
| **RSS/Atom Feed** | None available. |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the DOU is the constitutional publication vehicle for all federal laws, regulations, executive orders, and international agreements |
| **Publication Frequency** | Daily (Monday-Friday). Three sections: Seção 1 (normative acts, laws, decrees), Seção 2 (personnel acts), Seção 3 (contracts, bids, notices). Extra editions (edições extras) for urgent matters. |
| **Content Format** | HTML index pages. Individual acts viewable as HTML or downloadable as PDF. INLABS system provides full editions in PDF and XML formats. |
| **Extraction Method** | (a) HTML scraping of daily edition index via `in.gov.br/leiturajornal?secao=dou1&data=DD-MM-YYYY`. (b) Full-text search via `in.gov.br/consulta`. (c) INLABS bulk access (`inlabs.in.gov.br`) for complete editions in PDF/XML — free since January 2020. (d) Open data base at `in.gov.br/acesso-a-informacao/dados-abertos/base-de-dados`. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no federal law, regulation, international agreement, or executive decree is legally binding until published in the DOU. Treaty ratifications, defense procurement contracts, regulatory changes, and ministerial appointments are all published here before anywhere else. |
| **Access Notes** | Free access since 2020. INLABS system (`inlabs.in.gov.br`) provides programmatic access to complete editions in XML — the most machine-friendly access method. Registration required for INLABS bulk downloads. Scripts for automated download available at `github.com/Imprensa-Nacional/inlabs`. |

**Key URL patterns:**
| Section | URL Pattern |
|---|---|
| Seção 1 (normative acts) | `https://www.in.gov.br/leiturajornal?secao=dou1&data=DD-MM-YYYY` |
| Seção 2 (personnel) | `https://www.in.gov.br/leiturajornal?secao=dou2&data=DD-MM-YYYY` |
| Seção 3 (contracts) | `https://www.in.gov.br/leiturajornal?secao=dou3&data=DD-MM-YYYY` |
| Extra editions | `https://www.in.gov.br/leiturajornal?secao=do1e&data=DD-MM-YYYY` |
| Search | `https://www.in.gov.br/consulta/-/buscar/dou` |

---

### 1.6 Finance Ministry — Ministério da Fazenda

| Field | Detail |
|---|---|
| **Institution** | Ministério da Fazenda |
| **Domain** | `gov.br/fazenda` |
| **Entry Point URL** | `https://www.gov.br/fazenda/pt-br/assuntos/noticias` |
| **RSS/Atom Feed** | Gov.br Plone RSS likely available at: `https://www.gov.br/fazenda/pt-br/assuntos/noticias/RSS` [VERIFY RSS] |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Daily. 3-7 items per day covering fiscal policy, tax reform implementation, international economic cooperation, public debt, and budget execution. Organized by year (`/noticias/2026/`, `/noticias/2025/`). |
| **Content Format** | HTML on gov.br. Statistical reports and technical notes frequently attached as PDFs. |
| **Extraction Method** | RSS polling (if feed confirmed) or HTML scraping. Same Plone pagination as other gov.br sites (`?b_start:int=N`). |
| **Editorial Orientation** | Official fiscal policy position. Under Minister Fernando Haddad (PT), communications emphasize fiscal responsibility within a social-democratic framework — the "arcabouço fiscal" (fiscal framework), tax reform (reforma tributária), and "neoindustrialização." |
| **Why This Source** | Primary source for fiscal policy announcements, public debt operations, tax revenue data, international economic negotiations, and Brazil's positions in G20/BRICS financial discussions. Haddad's communications frequently signal diplomatic-economic linkages (Mercosur-EU trade implications, BRICS NDB participation). |
| **Access Notes** | Gov.br platform. The Secretaria do Tesouro Nacional (STN) publishes debt and fiscal data at `gov.br/tesouronacional`. The Receita Federal (tax authority) at `gov.br/receitafederal` provides tax-related communications. |

**Additional entry points:**
- Tesouro Nacional: `https://www.gov.br/tesouronacional/pt-br/noticias`
- Receita Federal: `https://www.gov.br/receitafederal/pt-br/assuntos/noticias`
- Conselho Monetário Nacional (CMN) resolutions: published in the DOU

---

### 1.7 Central Bank — Banco Central do Brasil (BCB)

| Field | Detail |
|---|---|
| **Institution** | Banco Central do Brasil (BCB) |
| **Domain** | `bcb.gov.br` |
| **Entry Point URL** | `https://www.bcb.gov.br/detalhenoticia/702/noticia` (news listing — JavaScript-rendered) |
| **RSS/Atom Feed** | No RSS feeds available for press releases. However, the BCB provides **structured open-data APIs** for Copom documents and economic indicators (see below). |
| **Language** | Portuguese (primary); English site at `bcb.gov.br/en` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Copom monetary policy decisions: 8 per year (typically Tuesday-Wednesday meetings; comunicado released Wednesday at 6:00 PM; ata released following Tuesday at 8:00 AM). Quarterly inflation reports. Miscellaneous communications: weekly. |
| **Content Format** | Copom comunicados and atas available in HTML and PDF. The website is JavaScript-rendered (Angular/React), making HTML scraping difficult. Open-data APIs return JSON. |
| **Extraction Method** | **Primary: Open Data API.** Copom documents API: `https://www.bcb.gov.br/api/servico/sitebcb/copom/atas?quantidade=N` (atas); comunicados via `dadosabertos.bcb.gov.br/dataset/atas-comunicados-copom`. Time series API for economic indicators: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados?formato=json`. The website's news section requires headless browser rendering due to JavaScript dependency. |
| **Editorial Orientation** | Technically independent central bank (autonomy law enacted 2021). Communications are data-driven and institutionally neutral. Under Governor Gabriel Galípolo (appointed 2024), perceived as more communicative than predecessor Roberto Campos Neto, but maintaining inflation-targeting orthodoxy in public statements. |
| **Why This Source** | BCB is the sole authoritative source for Selic rate decisions, inflation expectations, foreign reserve levels, exchange rate policy signals, and macroeconomic assessments. Copom comunicados move markets and are the single most-watched government publication in Brazil. |
| **Access Notes** | No paywall. JavaScript-rendered main site — headless browser required for scraping. Open Data APIs are well-documented and reliable — preferred for automated access. English site provides parallel content for major publications. Full API documentation at `bcb.gov.br/conteudo/dadosabertos/BCBDeinf/elements_copom.html`. |

**Key API endpoints:**
| Endpoint | URL |
|---|---|
| Copom atas (list) | `https://www.bcb.gov.br/api/servico/sitebcb/copom/atas?quantidade=5` |
| Copom ata (detail) | `https://www.bcb.gov.br/api/servico/sitebcb/copom/atas_detalhes?nro_reuniao={N}` |
| Open data portal (Copom) | `https://dadosabertos.bcb.gov.br/dataset/atas-comunicados-copom` |
| Time series (Selic, IPCA, etc.) | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados?formato=json` |
| Open data portal (general) | `https://dadosabertos.bcb.gov.br/` / `https://opendata.bcb.gov.br/` |

---

### 1.8 Trade / Commerce — Ministério do Desenvolvimento, Indústria, Comércio e Serviços (MDIC)

| Field | Detail |
|---|---|
| **Institution** | Ministério do Desenvolvimento, Indústria, Comércio e Serviços (MDIC) |
| **Domain** | `gov.br/mdic` |
| **Entry Point URL** | `https://www.gov.br/mdic/pt-br/assuntos/noticias` |
| **RSS/Atom Feed** | Gov.br Plone RSS likely available at: `https://www.gov.br/mdic/pt-br/assuntos/noticias/RSS` [VERIFY RSS] |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | Daily. 2-5 items per day covering trade negotiations, export data, FDI policy, industrial policy (Nova Indústria Brasil), and bilateral trade agreements. News organized by year/month (`/noticias/2026/marco/`). |
| **Content Format** | HTML on gov.br. Trade statistics in PDF/Excel attachments. |
| **Extraction Method** | RSS polling (if feed confirmed) or HTML scraping. |
| **Editorial Orientation** | Official trade/industrial policy position. Under Vice-President and Minister Geraldo Alckmin, communications emphasize "neoindustrialização," export diversification, FDI attraction ("Janela Unica de Investimentos"), and trade negotiations (Mercosur-EU, bilateral agreements). |
| **Why This Source** | Primary source for trade policy announcements, export/import data, FDI statistics, industrial policy programs (Nova Indústria Brasil), and Brazil's positions in trade negotiations. MDIC comunicados are the first source for tariff changes, trade agreement progress, and bilateral commercial cooperation. |
| **Access Notes** | Gov.br platform. Trade statistics portal: ComexStat at `comexstat.mdic.gov.br`. MDIC's API for trade data provides structured programmatic access. |

**Additional entry points:**
- ComexStat (trade data): `https://comexstat.mdic.gov.br/`
- Siscomex (trade operations): `https://www.gov.br/siscomex/pt-br`
- CAMEX (Câmara de Comércio Exterior) resolutions: published in the DOU

---

### 1.9 Intelligence / National Security — ABIN and GSI

#### 1.9a Agência Brasileira de Inteligência (ABIN)

| Field | Detail |
|---|---|
| **Institution** | Agência Brasileira de Inteligência (ABIN) |
| **Domain** | `gov.br/abin` |
| **Entry Point URL** | `https://www.gov.br/abin/pt-br` |
| **RSS/Atom Feed** | None available. |
| **Language** | Portuguese (English section at `gov.br/abin/en`) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Minimal. ABIN publishes virtually no operational or policy communications. Institutional pages updated infrequently. The Revista Brasileira de Inteligência (RBI) academic journal is published periodically at `rbi.abin.gov.br`. |
| **Content Format** | Minimal HTML on gov.br. Transparency documents in PDF. |
| **Extraction Method** | Periodic check of gov.br/abin for any new publications. Flag any new publication as a high-priority anomaly. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. ABIN's public communications are almost nonexistent. The agency is undergoing significant institutional restructuring following the 2023-2024 illegal surveillance scandal (during the Bolsonaro administration). Under new leadership, the agency is focused on rebuilding institutional credibility. Real intelligence signals surface through leaks to investigative media (Folha, O Globo, Intercept Brasil) and STF judicial proceedings rather than official channels. |
| **Access Notes** | Gov.br platform. Transparency portal accessible via gov.br/abin/pt-br/acesso-a-informacao. The Revista Brasileira de Inteligência at `rbi.abin.gov.br/RBI` publishes analytical articles that may signal institutional thinking. |

#### 1.9b Gabinete de Segurança Institucional (GSI)

| Field | Detail |
|---|---|
| **Institution** | Gabinete de Segurança Institucional da Presidência da República (GSI) |
| **Domain** | `gov.br/gsi` |
| **Entry Point URL** | `https://www.gov.br/gsi/pt-br` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Infrequent. The GSI publishes institutional communications related to nuclear policy (CNEN oversight), critical infrastructure protection, and national security council (CDN) support activities. |
| **Content Format** | Minimal HTML on gov.br. |
| **Extraction Method** | Periodic check. |
| **Editorial Orientation** | Institutional national security. Under Minister General Marcos Antonio Amaro dos Santos, the GSI has been less publicly visible than under previous administrations. |
| **Why This Source** | The GSI is the institutional home of national security coordination, including the Conselho de Defesa Nacional (CDN). Its public communications are sparse, but any publication signals high-level security policy attention. The GSI also oversees the Agência Nacional de Segurança Cibernética and nuclear policy coordination. |
| **Access Notes** | Gov.br platform. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Petrobras

| Field | Detail |
|---|---|
| **Institution** | Petróleo Brasileiro S.A. (Petrobras) |
| **Domain** | `petrobras.com.br` / `agencia.petrobras.com.br` |
| **Entry Point URL** | `https://agencia.petrobras.com.br/` (Petrobras News Agency) / `https://petrobras.com.br/fatos-e-dados/` (Fatos e Dados) |
| **RSS/Atom Feed** | None identified on current Liferay-based portal. [VERIFY RSS at agencia.petrobras.com.br] |
| **Language** | Portuguese (English: `agencia.petrobras.com.br/en`) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Daily. 3-8 items per day covering production data, financial results, exploration, pre-salt operations, refinery output, ESG initiatives, and energy transition investments. |
| **Content Format** | HTML (Liferay-based). Financial reports and statistical data in PDF. Investor presentations in PDF/PPT. |
| **Extraction Method** | HTML scraping of agencia.petrobras.com.br listing pages. Financial disclosures also filed with CVM (Brazilian SEC) and NYSE (for ADR holders). |
| **Editorial Orientation** | State-controlled enterprise communication. Under CEO Magda Chambriard (appointed 2024), communications emphasize production growth, pre-salt reserves, refinery investment, and alignment with government energy policy — while maintaining investor-relations commitments to financial transparency. |
| **Why This Source** | Petrobras is Latin America's largest company by revenue, Brazil's largest exporter, and a central pillar of the country's energy sovereignty strategy. Production data, dividend policy, pre-salt investment, and strategic partnerships (with national oil companies from BRICS nations) directly affect fiscal stability, trade balance, and Brazil's climate diplomacy positioning. Petrobras dividend payments are a major component of federal revenue. |
| **Access Notes** | Agência Petrobras is a Liferay DXP-based portal (launched 2024, replacing the older Fatos e Dados site). No known bot protection. English section provides parallel coverage. CVM filings at `sistemas.cvm.gov.br` and SEC filings provide structured financial data. |

#### 1.10b STF (Supremo Tribunal Federal)

| Field | Detail |
|---|---|
| **Institution** | Supremo Tribunal Federal (STF) |
| **Domain** | `portal.stf.jus.br` |
| **Entry Point URL** | `https://portal.stf.jus.br/listagem/listarNoticias.asp` / `https://noticias.stf.jus.br/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Portuguese (English section at `portal.stf.jus.br/internacional/`) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily when in session. 5-15 news items per day during active session periods. The Informativo STF weekly digest summarizes key rulings. |
| **Content Format** | HTML. Session transcripts available. Press releases (comunicados) via the Comunicação section. |
| **Extraction Method** | HTML scraping of noticias listing page. SSL certificate issues have been observed — implement certificate verification fallback. Email subscription available for Informativo STF digest. |
| **Editorial Orientation** | Judicial institution. The STF's communications emphasize institutional independence and constitutional interpretation. Under Chief Justice Luís Roberto Barroso, communications have been more publicly engaged than under previous courts. |
| **Why This Source** | STF rulings on constitutional controversies — January 8 prosecutions, social media regulation (X/Twitter ban precedent), indigenous land demarcation, environmental enforcement, executive power limits — directly constrain or enable executive action across all five analytical domains. The STF's institutional posture is a key domestic constraint variable. |
| **Access Notes** | Independent infrastructure (not on gov.br). SSL certificate issues observed — may require certificate verification bypass. Informativo STF weekly digest provides structured case summaries. Full rulings searchable at `jurisprudencia.stf.jus.br`. Contact: Coordenadoria de Imprensa at portal. |

#### 1.10c Agência Brasil (EBC)

| Field | Detail |
|---|---|
| **Institution** | Agência Brasil — Empresa Brasil de Comunicação (EBC) |
| **Domain** | `agenciabrasil.ebc.com.br` |
| **Entry Point URL** | `https://agenciabrasil.ebc.com.br/ultimas` |
| **RSS/Atom Feed** | **Yes — multiple category feeds.** Feed hub: `https://agenciabrasil.ebc.com.br/feed/`. Pattern: `https://agenciabrasil.ebc.com.br/rss/{category}/feed.xml`. Categories: ultimas-noticias, direitos-humanos, economia, educacao, esportes, geral, internacional, justica, politica, saude, parceiros. EBC-wide RSS hub: `https://rss.ebc.com.br/`. |
| **Language** | Portuguese (English section at `agenciabrasil.ebc.com.br/en`) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains (general government wire) |
| **Publication Frequency** | Continuous — 30-50 items per day. Wire-service cadence. |
| **Content Format** | HTML. Wire-style articles with structured tags. |
| **Extraction Method** | RSS polling — the most feed-rich government-adjacent source in Brazil. The `politica` and `internacional` feeds are most relevant for pipeline monitoring. |
| **Editorial Orientation** | Government-aligned public broadcaster. Wire-style factual reporting of government actions. Not editorially independent — publishes presidential and ministerial statements verbatim. Essential for capturing declared government positions, not for independent analysis. |
| **Why This Source** | Agência Brasil functions as the de facto Brazilian government wire service. It publishes presidential statements, ministerial announcements, and official positions on international affairs with wire-service speed and completeness. Its RSS feeds are the most reliable automated intake point for government communications. Already in the Layer 1 media map — included here for RSS feed documentation. |
| **Access Notes** | Fully free. RSS feeds well-maintained and reliable. English section provides translations of major stories. |

#### 1.10d TSE (Tribunal Superior Eleitoral)

| Field | Detail |
|---|---|
| **Institution** | Tribunal Superior Eleitoral (TSE) |
| **Domain** | `tse.jus.br` |
| **Entry Point URL** | `https://www.tse.jus.br/comunicacao/noticias` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Portuguese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints |
| **Publication Frequency** | Daily. Increased frequency during electoral periods (2026 elections are a major cycle). |
| **Content Format** | HTML. Election data in structured formats via open data portal. |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | Autonomous electoral court. Institutionally committed to nonpartisan framing. |
| **Why This Source** | The TSE's communications reveal the state of democratic institutional integrity — a key Domestic Constraints indicator. With the 2026 presidential election cycle beginning, TSE rulings on Bolsonaro's ineligibility, party registration, campaign finance, and electoral technology (electronic voting) are directly relevant to political stability assessment. |
| **Access Notes** | Independent infrastructure. Open data portal at `dadosabertos.tse.jus.br` provides structured electoral data. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | gov.br Platform |
|---|---|---|---|---|---|---|---|
| 1 | Presidência | `gov.br/planalto/pt-br/acompanhe-o-planalto/noticias` | [VERIFY] (Plone) | P1 | HTML | Daily | Yes |
| 2 | MRE (Itamaraty) | `gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa` | [VERIFY] (Plone) + Email list | P1 | HTML/PDF | Daily | Yes |
| 3 | Defesa | `gov.br/defesa/pt-br/centrais-de-conteudo/noticias` | [VERIFY] (Plone) | P1 | HTML | 3-7/week | Yes |
| 4a | Senado | `www12.senado.leg.br/noticias/ultimas` | **Yes** (multiple) | P2 | HTML | Daily (session) | No |
| 4b | Câmara | `camara.leg.br/noticias` | **Yes** (23 feeds) | P2 | HTML | Daily (session) | No |
| 5 | DOU | `in.gov.br/leiturajornal` / `in.gov.br/consulta` | No (XML via INLABS) | P2 | HTML/PDF/XML | Daily | No |
| 6 | Fazenda | `gov.br/fazenda/pt-br/assuntos/noticias` | [VERIFY] (Plone) | P2 | HTML/PDF | Daily | Yes |
| 7 | BCB | `bcb.gov.br` (JS-rendered) | No (APIs available) | P2 | HTML/PDF/JSON | Variable | No |
| 8 | MDIC | `gov.br/mdic/pt-br/assuntos/noticias` | [VERIFY] (Plone) | P2 | HTML | Daily | Yes |
| 9a | ABIN | `gov.br/abin/pt-br` | No | P2 | Minimal | Negligible | Yes |
| 9b | GSI | `gov.br/gsi/pt-br` | No | P2 | Minimal | Infrequent | Yes |
| 10a | Petrobras | `agencia.petrobras.com.br` | [VERIFY] | P2 | HTML/PDF | Daily | No |
| 10b | STF | `portal.stf.jus.br/listagem/listarNoticias.asp` | [VERIFY] | P2 | HTML | Daily (session) | No |
| 10c | Agência Brasil | `agenciabrasil.ebc.com.br/ultimas` | **Yes** (multiple) | P2 | HTML | Continuous | No |
| 10d | TSE | `tse.jus.br/comunicacao/noticias` | [VERIFY] | P2 | HTML | Daily | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Brazil Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/br.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: br_presidencia
    name: Presidência da República (Planalto)
    domain: gov.br
    entry_url: "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias"
    rss_feed: "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/noticias/RSS"  # [VERIFY - Plone RSS path]
    language: pt
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 2
    notes: "Gov.br Plone platform. English news at gov.br/planalto/en/latest-news. 403 errors possible — rotate User-Agent."

  - id: br_mre
    name: Ministério das Relações Exteriores (Itamaraty)
    domain: gov.br
    entry_url: "https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa"
    rss_feed: "https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa/RSS"  # [VERIFY]
    email_list: "https://imprensamaillist.itamaraty.gov.br/"
    language: pt
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 2
    notes: "Email distribution list is reliable push alternative. English releases at gov.br/mre/en/. @ItamaratyGovBr on X often publishes notas before web."

  - id: br_defesa
    name: Ministério da Defesa
    domain: gov.br
    entry_url: "https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias"
    rss_feed: "https://www.gov.br/defesa/pt-br/centrais-de-conteudo/noticias/RSS"  # [VERIFY]
    language: pt
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 4
    notes: "Service branch sites (Exército, Marinha, Aeronáutica) also on gov.br. Agência Gov syndicates defense news."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: br_senado
    name: Senado Federal (Agência Senado)
    domain: senado.leg.br
    entry_url: "https://www12.senado.leg.br/noticias/ultimas"
    rss_feed:
      main: "https://www12.senado.leg.br/noticias/feed"
      all_news: "https://www12.senado.leg.br/noticias/feed/todasnoticias"
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Well-maintained RSS feeds. Topic-specific feeds available (Comissões, Mercosul, Plenário, Orçamento, etc.)."

  - id: br_camara
    name: Câmara dos Deputados (Agência Câmara)
    domain: camara.leg.br
    entry_url: "https://www.camara.leg.br/noticias"
    rss_feed:
      latest: "https://www.camara.leg.br/noticias/rss/ultimas-noticias"
      foreign_affairs: "https://www.camara.leg.br/noticias/rss/dinamico/RELACOES-EXTERIORES"
      economy: "https://www.camara.leg.br/noticias/rss/dinamico/ECONOMIA"
      security: "https://www.camara.leg.br/noticias/rss/dinamico/SEGURANCA"
      politics: "https://www.camara.leg.br/noticias/rss/dinamico/POLITICA"
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "23 topic-specific RSS feeds. RELACOES-EXTERIORES and SEGURANCA feeds most relevant. Open data API at dadosabertos.camara.leg.br."

  - id: br_dou
    name: Diário Oficial da União (DOU)
    domain: in.gov.br
    entry_url: "https://www.in.gov.br/leiturajornal"
    rss_feed: null
    inlabs_access: "https://inlabs.in.gov.br/"
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html_pdf_xml
    extraction_method: inlabs_xml_or_html_scrape
    poll_interval_hours: 6
    notes: "INLABS provides XML bulk access (free since 2020, registration required). GitHub scripts at github.com/Imprensa-Nacional/inlabs. Seção 1 (dou1) is most relevant for policy monitoring."

  - id: br_fazenda
    name: Ministério da Fazenda
    domain: gov.br
    entry_url: "https://www.gov.br/fazenda/pt-br/assuntos/noticias"
    rss_feed: "https://www.gov.br/fazenda/pt-br/assuntos/noticias/RSS"  # [VERIFY]
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 6
    notes: "Tesouro Nacional fiscal data at gov.br/tesouronacional. PDF annexes contain statistical tables."

  - id: br_bcb
    name: Banco Central do Brasil (BCB)
    domain: bcb.gov.br
    entry_url: "https://www.bcb.gov.br/"
    rss_feed: null
    api_endpoints:
      copom_atas: "https://www.bcb.gov.br/api/servico/sitebcb/copom/atas?quantidade=5"
      copom_ata_detail: "https://www.bcb.gov.br/api/servico/sitebcb/copom/atas_detalhes?nro_reuniao={N}"
      open_data_copom: "https://dadosabertos.bcb.gov.br/dataset/atas-comunicados-copom"
      time_series: "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados?formato=json"
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: json_pdf_mixed
    extraction_method: api_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best machine-readable government source in Brazil. APIs for Copom documents and time series. JS-rendered site requires headless browser for scraping. English site at bcb.gov.br/en."

  - id: br_mdic
    name: Ministério do Desenvolvimento, Indústria, Comércio e Serviços (MDIC)
    domain: gov.br
    entry_url: "https://www.gov.br/mdic/pt-br/assuntos/noticias"
    rss_feed: "https://www.gov.br/mdic/pt-br/assuntos/noticias/RSS"  # [VERIFY]
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 12
    notes: "Trade data at comexstat.mdic.gov.br. Under VP Alckmin — dual role gives MDIC cross-portfolio significance."

  - id: br_abin
    name: Agência Brasileira de Inteligência (ABIN)
    domain: gov.br
    entry_url: "https://www.gov.br/abin/pt-br"
    rss_feed: null
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent agency post-surveillance scandal. RBI journal at rbi.abin.gov.br. Real signal via leaks to Folha/O Globo/Intercept Brasil."

  - id: br_gsi
    name: Gabinete de Segurança Institucional (GSI)
    domain: gov.br
    entry_url: "https://www.gov.br/gsi/pt-br"
    rss_feed: null
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: infrequent
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "National security coordination body. Oversees CDN (Conselho de Defesa Nacional) and cybersecurity. Any publication is a high-priority anomaly."

  - id: br_petrobras
    name: Petrobras (Agência Petrobras)
    domain: petrobras.com.br
    entry_url: "https://agencia.petrobras.com.br/"
    rss_feed: null  # [VERIFY]
    language: pt
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Liferay DXP portal. English at agencia.petrobras.com.br/en. CVM/NYSE filings provide structured financial data."

  - id: br_stf
    name: Supremo Tribunal Federal (STF)
    domain: portal.stf.jus.br
    entry_url: "https://portal.stf.jus.br/listagem/listarNoticias.asp"
    rss_feed: null  # [VERIFY]
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "SSL cert issues observed. Informativo STF weekly digest available via email. Full rulings at jurisprudencia.stf.jus.br."

  - id: br_agencia_brasil
    name: Agência Brasil (EBC)
    domain: agenciabrasil.ebc.com.br
    entry_url: "https://agenciabrasil.ebc.com.br/ultimas"
    rss_feed:
      feed_hub: "https://agenciabrasil.ebc.com.br/feed/"
      politica: "https://agenciabrasil.ebc.com.br/rss/politica/feed.xml"
      economia: "https://agenciabrasil.ebc.com.br/rss/economia/feed.xml"
      internacional: "https://agenciabrasil.ebc.com.br/rss/internacional/feed.xml"
      justica: "https://agenciabrasil.ebc.com.br/rss/justica/feed.xml"
      geral: "https://agenciabrasil.ebc.com.br/rss/geral/feed.xml"
    language: pt
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
      - domestic_constraints
      - security_defense_autonomy
    publication_frequency: continuous
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 4
    notes: "Government wire service. Best RSS coverage of any Brazilian gov source. English at agenciabrasil.ebc.com.br/en. EBC-wide feeds at rss.ebc.com.br."

  - id: br_tse
    name: Tribunal Superior Eleitoral (TSE)
    domain: tse.jus.br
    entry_url: "https://www.tse.jus.br/comunicacao/noticias"
    rss_feed: null  # [VERIFY]
    language: pt
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Priority increases to P1 during electoral periods (2026 cycle). Open data at dadosabertos.tse.jus.br."

# Gov.br shared extraction configuration
gov_br_shared_config:
  platform: plone
  base_url: "https://www.gov.br"
  agencies_on_platform:
    - slug: planalto
      news_path: "/pt-br/acompanhe-o-planalto/noticias"
    - slug: mre
      news_path: "/pt-br/canais_atendimento/imprensa/notas-a-imprensa"
    - slug: defesa
      news_path: "/pt-br/centrais-de-conteudo/noticias"
    - slug: fazenda
      news_path: "/pt-br/assuntos/noticias"
    - slug: mdic
      news_path: "/pt-br/assuntos/noticias"
    - slug: abin
      news_path: "/pt-br"  # minimal content
    - slug: gsi
      news_path: "/pt-br"  # minimal content
  pagination: "?b_start:int=N"  # Plone-style, increments of 30
  rss_pattern: "{news_listing_url}/RSS"  # Plone syndication — VERIFY per agency
  bot_protection: intermittent_403  # Not Cloudflare — likely rate limiting
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "pt-BR,pt;q=0.9"
  rate_limit: "max 1 request per 3 seconds per agency"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Brazilian government communications are systematically positive and omission-heavy, but less centrally controlled than Mexico's gob.mx ecosystem. The gov.br platform lacks the uniform template discipline of gob.mx — each ministry has a somewhat different URL structure, content organization, and publication cadence. The interpretive value of government sources lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing and language choices relative to media coverage.

- **Presidência (Planalto)**: Cross-reference presidential statements against same-day reporting in Folha de S.Paulo and O Globo. Unlike Mexico's daily mananera, presidential communications in Brazil are event-driven — silence itself can be a signal. When Planalto does not comment on a diplomatic development covered by Folha, it indicates either deliberate ambiguity or internal policy disagreement.
- **MRE (Itamaraty)**: Diplomatic "notas à imprensa" should be triangulated with Folha's "Mundo" section (critical, independent perspective), O Globo (establishment lens), and The Brazilian Report (English-language analytical context). When Itamaraty issues a nota in both Portuguese and English simultaneously, it signals the communication targets an international audience — the English version may contain subtle framing differences from the Portuguese original.
- **Defesa**: Defense Ministry communications report cooperation agreements, exercises, and institutional events but never operational failures, civil-military tensions, or procurement controversies. Cross-reference with DefesaNet (defense-specialist reporting), Metrópoles (Brasilia sourcing for civil-military friction), and Intercept Brasil (investigative coverage of military institutional issues).
- **BCB**: Copom comunicados and atas are technically rigorous and among the least politically distorted government sources — institutional autonomy (since 2021 law) provides some insulation. However, emphasis choices in the comunicado language signal institutional positioning vis-a-vis the executive. Cross-reference with Valor Econômico (market interpretation), Folha's "Mercado" section, and Bloomberg (international investor perspective).
- **Fazenda**: Fiscal data is generally reliable in headline numbers, but presentation framing (base period selection, inclusion/exclusion of extraordinary revenues) can obscure trends. Valor Econômico and Estadão provide the sharpest independent fiscal analysis.
- **Petrobras**: State enterprise communications systematically emphasize production milestones and strategic investments while downplaying financial risks, debt levels, and political interference in pricing. Cross-reference with Valor Econômico (financial analysis), Folha (investigative — Petrobras governance has deep historical investigative coverage), and Bloomberg/Reuters (international investor perspective).
- **Senado/Câmara (Agências)**: Congressional news agencies are institutionally nonpartisan and provide more balanced coverage than executive sources. The most analytically valuable content is buried in committee hearing coverage — particularly CRE (foreign relations) and defense committee testimony from ministers — that no media outlet fully covers.

**4.2 The gov.br platform: similarities and differences with Mexico's gob.mx**

Five of Brazil's ten government source categories publish through the gov.br platform (Plone-based). Unlike Mexico's uniform gob.mx template, Brazil's implementation is less standardized:
- URL patterns vary by ministry (some use `/assuntos/noticias`, others `/centrais-de-conteudo/noticias`, others `/canais_atendimento/imprensa/`)
- RSS availability depends on whether each ministry's Plone instance has syndication enabled — this must be verified per agency
- Pagination is consistent (Plone `?b_start:int=N`) but page sizes may vary
- Bot protection is less aggressive than gob.mx's Cloudflare — primarily rate-limiting with intermittent 403 errors

Sources outside gov.br (BCB, Senado, Câmara, STF, TSE, Petrobras, DOU) operate on fully independent infrastructure with varying technical maturity — from the BCB's well-structured APIs to the STF's aging ASP-based portal with SSL certificate issues.

**4.3 The ABIN silence and GSI opacity problem**

Brazil's intelligence agency (ABIN) and national security coordination body (GSI) produce effectively zero public communications of analytical value. This is structurally comparable to Mexico's CNI silence. Intelligence-relevant signals surface through:
- Leaks to investigative media (Folha, O Globo, Intercept Brasil, Metrópoles)
- STF proceedings (particularly the January 8 investigation and ABIN surveillance scandal cases)
- Congressional CPI (parliamentary inquiry) testimony
- DOU publications of organizational/budget changes
- Presidential decrees published in the DOU that reference national security matters

The pipeline should not allocate significant resources to polling ABIN or GSI pages but should flag any new publication as a high-priority anomaly. The ABIN scandal (illegal surveillance during the Bolsonaro administration) makes any ABIN institutional communication in 2025-2026 a significant signal of post-crisis institutional repositioning.

**4.4 Legislative gap: committee proceedings and open data**

The existing Source Intelligence Map identifies parliamentary transcripts as a monitoring resource. Brazil's legislature offers significantly better structured data access than Mexico's:
- The Câmara dos Deputados provides 23 topic-specific RSS feeds, including dedicated "Relações Exteriores" and "Segurança" feeds
- The Senado's multiple RSS channels include Comissões and Mercosul-specific feeds
- The Câmara's Dados Abertos API (`dadosabertos.camara.leg.br`) provides structured access to voting records, propositions, and legislative activity

Priority committee monitoring: (a) CRE (Comissão de Relações Exteriores e Defesa Nacional) — both chambers, (b) CAE (Comissão de Assuntos Econômicos) — Senate, (c) Comissão de Finanças e Tributação — Câmara, (d) any CPI with foreign-policy or security implications.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for gov.br

The gov.br platform hosts 5 of the 16 monitored government endpoints (Presidência, MRE, Defesa, Fazenda, MDIC — plus ABIN and GSI which have minimal content). Unlike Mexico's uniform gob.mx template, gov.br's Plone implementation varies by agency, requiring per-agency configuration:

- **URL base**: `https://www.gov.br/{slug}{news_path}`
- **Pagination**: Plone-style `?b_start:int=N` (typically increments of 30, but verify per agency)
- **RSS pattern**: `{news_listing_url}/RSS` — Plone's built-in syndication. Availability must be verified per agency as not all ministry instances have syndication enabled.
- **Article URL pattern**: varies — typically `https://www.gov.br/{slug}/pt-br/assuntos/noticias/{year}/{month}/{article-slug}`
- **Rate limit**: Enforce minimum 3-second intervals between requests. Rotate User-Agent headers.
- **Bot protection**: Less aggressive than Mexico's gob.mx Cloudflare — primarily intermittent 403 errors suggesting rate limiting. Standard User-Agent rotation usually sufficient.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Four government source categories provide functional RSS feeds:

1. **Agência Brasil (EBC)**: The most reliable and comprehensive RSS source. Multiple category-specific feeds (politica, economia, internacional, justica, geral). Wire-service cadence with continuous publication. Feed URL pattern: `agenciabrasil.ebc.com.br/rss/{category}/feed.xml`.

2. **Câmara dos Deputados**: 23 topic-specific RSS feeds. The `RELACOES-EXTERIORES`, `SEGURANCA`, `ECONOMIA`, and `POLITICA` feeds are directly relevant. Feed URL pattern: `camara.leg.br/noticias/rss/dinamico/{TOPIC}`.

3. **Senado Federal**: Multiple feeds including all-news and topic-specific channels. Feed URL pattern: `www12.senado.leg.br/noticias/feed/{channel}`.

4. **Gov.br agencies** (unverified): The Plone platform supports RSS via the `/RSS` path suffix on listing pages. This should work for Presidência, MRE, Defesa, Fazenda, and MDIC but must be verified per agency — some ministries may have disabled syndication.

Additionally, the **Portal da Legislação** provides RSS for new legislation at `www4.planalto.gov.br/legislacao/rss`.

### 5.3 API-Enabled Sources (Priority for Structured Data)

Two government sources provide structured APIs — a significant advantage over Mexico's infrastructure:

1. **BCB (Banco Central)**: RESTful APIs for Copom documents (atas and comunicados) and economic time series. JSON format. Well-documented at `dadosabertos.bcb.gov.br`. The time series API (`api.bcb.gov.br/dados/serie/`) covers Selic, IPCA, exchange rates, reserves, and hundreds of other indicators. This is the most machine-friendly government data source in Brazil.

2. **DOU (INLABS)**: XML bulk access to complete editions of the Diário Oficial da União. Free since 2020 (registration required). GitHub repository with download scripts at `github.com/Imprensa-Nacional/inlabs`. Monthly publication of previous month's editions in open XML format.

3. **Câmara dos Deputados Open Data**: RESTful API at `dadosabertos.camara.leg.br` for voting records, propositions, and legislative activity. JSON/XML formats.

### 5.4 PDF Extraction Requirements

Four sources publish primarily or substantially in PDF:
- **DOU**: Legal texts published as PDF (also available as XML via INLABS). Text-based PDFs for recent publications.
- **BCB**: Copom atas and monetary policy decisions are multi-page PDF. Text-based, well-structured. Also available via API in HTML-tagged text format.
- **Fazenda**: Statistical annexes to communications are PDF with tables. May require table extraction (tabula/camelot).
- **Petrobras**: Financial reports, investor presentations, and production data in PDF. CVM/NYSE filings provide alternative structured access.

### 5.5 Language and Encoding

All government sources publish primarily in Portuguese (pt-BR). English-language parallel content is available from:
- **Presidência**: `gov.br/planalto/en/latest-news` with RSS at `gov.br/en/government-of-brazil/latest-news/latest-news/RSS`
- **MRE (Itamaraty)**: `gov.br/mre/en/contact-us/press-area/press-releases`
- **BCB**: `bcb.gov.br/en` with English versions of major publications
- **Agência Brasil**: `agenciabrasil.ebc.com.br/en`
- **Petrobras**: `agencia.petrobras.com.br/en`

All gov.br content is UTF-8 encoded. The STF portal (`portal.stf.jus.br`) and DOU (`in.gov.br`) use UTF-8 but some legacy pages may have encoding issues — normalize on ingestion.

### 5.6 Deduplication Across Sources

Government announcements in Brazil frequently appear on multiple channels simultaneously — more extensively than in Mexico due to Agência Brasil's wire-service role:
- A presidential decree appears in Planalto noticias, the DOU, Agência Brasil, Agência Gov, and often the relevant ministry's news page
- Foreign policy statements appear in MRE notas, Planalto noticias, Agência Brasil, and Senado/Câmara news (if committee testimony is involved)
- Defense announcements appear in Defesa noticias, the relevant service branch's page, Agência Brasil, and Agência Gov
- Copom decisions appear on BCB, Agência Brasil, and (as CMN resolutions) in the DOU

Implement content-hash deduplication. Use the DOU publication as the canonical version for legal texts. Use the originating ministry (MRE for diplomatic, Defesa for military, BCB for monetary policy) as canonical for operational communications. Use Agência Brasil as a catch-all fallback — it syndicates everything but adds no original analytical content.

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| Gov.br platform outage | Presidência, MRE, Defesa, Fazenda, MDIC, ABIN, GSI | Monitor Agência Brasil RSS feeds (agenciabrasil.ebc.com.br/rss/) — EBC syndicates all government communications. Also monitor @plaborig, @ItamaratyGovBr, @DefesaGovBr on X. |
| Gov.br 403 rate limiting | All gov.br agencies | Reduce poll frequency, rotate User-Agent headers. Agência Gov (agenciagov.ebc.com.br) mirrors gov.br content on separate EBC infrastructure. |
| BCB JavaScript rendering failure | BCB | Use BCB Open Data APIs (dadosabertos.bcb.gov.br) for Copom documents. Time series API (api.bcb.gov.br) is independent of the website. Social media: @BancoCentralBR on X. |
| STF SSL certificate failure | STF | Use alternative news portal at noticias.stf.jus.br. Monitor @STF_oficial on X. Informativo STF weekly digest available via email subscription. |
| DOU/INLABS downtime | DOU | Use search system at in.gov.br/consulta as fallback. Third-party DOU monitoring services (JusBrasil at jusbrasil.com.br/diarios/DOU/) provide alternative access. |
| Petrobras portal migration | Petrobras | Monitor CVM filings (sistemas.cvm.gov.br) for mandatory financial disclosures. Bloomberg/Reuters terminals receive Petrobras releases via wire. @petaborig on X. |
| Senado/Câmara RSS failure | Legislature | Scrape HTML listing pages directly. Agência Brasil covers major legislative developments. SIL (Sistema de Informações Legislativas) at legis.senado.leg.br provides parallel legislative tracking. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of the gov.br platform, change in government administration (next presidential inauguration: January 2027), or creation/dissolution of federal ministries. The 2026 election cycle (October) will significantly increase the relevance of TSE, STF, and legislative sources — consider elevating TSE to P1 during the electoral period (July-October 2026).*
