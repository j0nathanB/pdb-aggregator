# Official Government Sources Supplement: CANADA

**Primary languages of political discourse: English, French**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Canada (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Canada. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Canada's federal government operates a bilingual (English/French) web infrastructure, with most departments publishing through the centralized `canada.ca` portal maintained by Service Canada and Shared Services Canada. Since 2020, the Government of Canada has migrated most departmental communications to the unified `canada.ca` domain, replacing legacy `.gc.ca` departmental sites. News releases across departments are served through a standardized Atom feed API at `api.io.canada.ca`, which provides a consistent extraction pattern across agencies. A small number of institutions — the Prime Minister's Office (`pm.gc.ca`), Parliament (`ourcommons.ca`, `sencanada.ca`, `parl.ca`), the Bank of Canada (`bankofcanada.ca`), and the Canada Gazette (`gazette.gc.ca`) — maintain fully independent web infrastructure. All official government content is published simultaneously in English and French, as required by the Official Languages Act.

---

## 1. OFFICIAL GOVERNMENT SOURCES: CANADA

### 1.1 Head of Government — Prime Minister's Office (PMO)

| Field | Detail |
|---|---|
| **Institution** | Office of the Prime Minister / Cabinet du premier ministre |
| **Domain** | `pm.gc.ca` |
| **Entry Point URL** | `https://www.pm.gc.ca/en/news/releases` (EN) / `https://www.pm.gc.ca/fr/nouvelles/communiques` (FR) |
| **RSS/Atom Feed** | **Yes.** `https://pm.gc.ca/en/news.rss` (all news, English); `https://pm.gc.ca/fr/nouvelles.rss` (all news, French); `https://pm.gc.ca/en/media.rss` (photos/media, English) |
| **Language** | English and French (bilingual, parallel publication) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defence autonomy, Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Daily. News releases, statements, readouts of calls/meetings, and itineraries are published same-day. Volume increases around summits, parliamentary sessions, and diplomatic travel. |
| **Content Format** | HTML. Structured pages with consistent templates for releases, statements, speeches, and media advisories. |
| **Extraction Method** | RSS feed polling (`pm.gc.ca/en/news.rss`). Feed contains headline, summary, and link to full-text article. |
| **Editorial Orientation** | Official government position. All content is produced by the PMO communications team. Framing reflects the governing Liberal Party's policy priorities under PM Mark Carney. |
| **Why This Source** | The single authoritative source for the Prime Minister's official statements, bilateral meeting readouts, summit positions, and policy announcements. PM statements on trade, defence spending, Arctic sovereignty, and U.S. relations are market-moving and alliance-shaping. Under Carney, PMO communications have taken on an unusually direct economic-statecraft tone, particularly on tariff countermeasures and industrial strategy. |
| **Access Notes** | No paywall, no authentication required. No bot protection observed. Bilingual content with language toggle — EN and FR pages have parallel URL structures (`/en/` vs `/fr/`). |

**Additional entry points:**
- News releases: `https://www.pm.gc.ca/en/news/releases`
- Statements: `https://www.pm.gc.ca/en/news/statements`
- Speeches: `https://www.pm.gc.ca/en/news/speeches`
- Media advisories: `https://www.pm.gc.ca/en/news/media-advisories`
- Readouts: `https://www.pm.gc.ca/en/news/readouts`

---

### 1.2 Foreign Ministry — Global Affairs Canada (GAC)

| Field | Detail |
|---|---|
| **Institution** | Global Affairs Canada / Affaires mondiales Canada (GAC/AMC) |
| **Domain** | `international.canada.ca` / `canada.ca/en/global-affairs` |
| **Entry Point URL** | `https://international.canada.ca/en/global-affairs/news` (EN) / `https://international.canada.ca/fr/affaires-mondiales/nouvelles` (FR) |
| **RSS/Atom Feed** | **Yes — multiple Atom feeds available.** All news: `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate>=2015-01-01&pick=1000&format=atom&atomtitle=Global Affairs Canada news`. Type-specific feeds also available (see below). |
| **Language** | English and French (bilingual). Some diplomatic communications issued in third languages for multilateral contexts. |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily or near-daily. News releases, statements, readouts, and media advisories for bilateral meetings, multilateral summits (NATO, G7, UN, La Francophonie, Commonwealth), sanctions designations, and consular matters. |
| **Content Format** | HTML on canada.ca. Atom feeds provide structured metadata (title, date, summary, link). |
| **Extraction Method** | Atom feed polling via `api.io.canada.ca`. The API supports filtering by content type (`newsreleases`, `statements`, `readouts`, `mediaadvisories`, `speeches`). |
| **Editorial Orientation** | Official foreign-policy position. Under Foreign Minister Mélanie Joly, communications emphasize multilateral engagement, Indo-Pacific Strategy implementation, sanctions on Russia/Iran, and the evolving Canada-U.S. relationship. |
| **Why This Source** | The only primary source for Canada's formal diplomatic positions, sanctions designations, treaty actions, ambassador credentials, and bilateral/multilateral meeting readouts. GAC communications are the raw material from which CBC, Globe and Mail, and wire services construct foreign-policy coverage. Readouts of Minister Joly's calls and meetings frequently contain signals not captured in media reporting. |
| **Access Notes** | No paywall, no authentication required. The `api.io.canada.ca` Atom feeds are well-structured and reliable. The legacy `international.gc.ca` domain redirects to `international.canada.ca`. Travel advisories at `travel.gc.ca` have a separate RSS feed. |

**Key Atom feed URLs:**

| Feed | URL |
|---|---|
| All news | `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate>=2015-01-01&pick=1000&format=atom&atomtitle=Global Affairs Canada news` |
| News releases | Same URL with `&type=newsreleases` appended |
| Statements | Same URL with `&type=statements` appended |
| Readouts | Same URL with `&type=readouts` appended |
| Media advisories | Same URL with `&type=mediaadvisories` appended |
| Speeches | Same URL with `&type=speeches` appended |
| Travel advisories (separate) | `https://travel.gc.ca/feeds/rss/eng/travel-updates-24.aspx` |

---

### 1.3 Defence Ministry — Department of National Defence (DND) / Canadian Armed Forces (CAF)

| Field | Detail |
|---|---|
| **Institution** | Department of National Defence / Ministère de la Défense nationale (DND/MDN) and the Canadian Armed Forces / Forces armées canadiennes (CAF/FAC) |
| **Domain** | `canada.ca/en/department-national-defence` |
| **Entry Point URL** | `https://www.canada.ca/en/department-national-defence/corporate/news.html` |
| **RSS/Atom Feed** | **Yes.** `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentnationaldefense&sort=publishedDate&orderBy=desc&publishedDate>=2021-07-23&pick=50&format=atom&atomtitle=National+Defence+and+the+Canadian+Armed+Forces` |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defence autonomy, Diplomatic alignment (NATO/NORAD) |
| **Publication Frequency** | Daily or near-daily. News releases cover procurement announcements, CAF deployments, NORAD modernization updates, NATO contributions, defence policy statements, and operational updates (Op REASSURANCE, Op UNIFIER, Op IMPACT, etc.). The Maple Leaf / La Feuille d'érable internal newsletter publishes Defence Team News weekly. |
| **Content Format** | HTML on canada.ca. Atom feed via api.io.canada.ca. |
| **Extraction Method** | Atom feed polling. Same api.io.canada.ca pattern as GAC — department ID is `departmentnationaldefense`. |
| **Editorial Orientation** | Official defence communications. Under the current defence posture (post-"Our North, Strong and Free" defence policy update, 2024), communications emphasize NORAD modernization, Arctic sovereignty, NATO interoperability, and defence-industrial strategy. |
| **Why This Source** | Primary source for CAF deployment announcements, defence procurement decisions, NORAD modernization progress, and NATO contribution updates. DND news releases are the canonical record for defence spending commitments — a politically charged topic given Canada's longstanding failure to meet the NATO 2% GDP target. The Defence Team News (Maple Leaf) provides internal perspective not available in media. |
| **Access Notes** | No paywall. The legacy `forces.gc.ca` domain previously hosted RSS feeds but now returns 404 — use the `api.io.canada.ca` Atom feed instead. Email subscription available through canada.ca. |

**Additional entry points:**
- Defence policy documents: `https://www.canada.ca/en/department-national-defence/corporate/policies-standards.html`
- Operations: `https://www.canada.ca/en/department-national-defence/services/operations.html`
- Maple Leaf (Defence Team News): `https://www.canada.ca/en/department-national-defence/maple-leaf.html`

---

### 1.4 Parliament / Legislature

#### 1.4a House of Commons — Chambre des communes

| Field | Detail |
|---|---|
| **Institution** | House of Commons of Canada / Chambre des communes du Canada |
| **Domain** | `ourcommons.ca` |
| **Entry Point URL** | `https://www.ourcommons.ca/en/newsroom` |
| **RSS/Atom Feed** | No general RSS identified. Committee-specific email alerts available via `https://subscription.ourcommons.ca/Committees/en/NewsletterRegister`. Open Data feeds (XML) for Hansard and votes at `https://www.ourcommons.ca/en/open-data`. [VERIFY RSS at ourcommons.ca] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Security & defence autonomy, Domestic constraints |
| **Publication Frequency** | Daily during sitting periods. House sits approximately 135 days/year. Hansard (debates) published daily. Committee proceedings published within days of meeting. |
| **Content Format** | HTML. Hansard available in HTML and XML. Committee evidence (transcripts) in HTML. Open Data provides structured XML datasets. |
| **Extraction Method** | HTML scraping of newsroom page. Open Data XML feeds for votes and Hansard. Committee newsletter subscription for targeted monitoring. |
| **Editorial Orientation** | Institutional — non-partisan publication of parliamentary proceedings. Newsroom releases reflect Speaker's communications. |
| **Why This Source** | Standing Committee on Foreign Affairs and International Development (FAAE) and Standing Committee on National Defence (NDDN) are the primary venues for ministerial testimony and expert witness evidence on defence/foreign policy. Question Period transcripts capture opposition pressure on government policy. Votes and bill status via LEGISinfo at `parl.ca/legisinfo` provide the definitive record of legislative action. |
| **Access Notes** | No paywall. Open Data XML datasets available. ParlVU (`parlvu.parl.gc.ca`) streams live and archived committee/chamber proceedings. The subscription service allows email alerts for specific committee updates. |

**Additional entry points:**
- Hansard (latest): `https://www.ourcommons.ca/documentviewer/en/house/latest/hansard`
- LEGISinfo (bill tracking): `https://www.parl.ca/legisinfo/`
- Committee news releases: `https://www.parl.ca/Committees/en/PDAM/NewsReleases`
- ParlVU (video): `https://parlvu.parl.gc.ca/Harmony/`

#### 1.4b Senate of Canada — Sénat du Canada

| Field | Detail |
|---|---|
| **Institution** | Senate of Canada / Sénat du Canada |
| **Domain** | `sencanada.ca` |
| **Entry Point URL** | `https://sencanada.ca/en/newsroom/` |
| **RSS/Atom Feed** | None identified. Email newsletter (eNewsletter) available. [VERIFY RSS at sencanada.ca/en/newsroom/feed or similar] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Several times weekly during sitting periods. Senate Committee on Foreign Affairs and International Trade (AEFA) and Committee on National Security, Defence and Veterans Affairs (SECD) publish reports and meeting notices. |
| **Content Format** | HTML. Senate debates available in HTML. Committee reports in HTML/PDF. |
| **Extraction Method** | HTML scraping of newsroom page. |
| **Editorial Orientation** | Institutional. The Senate's independent, non-partisan reform (post-2015) means communications increasingly reflect individual senators' perspectives rather than party-line framing. |
| **Why This Source** | Senate committees on foreign affairs and defence conduct in-depth studies that produce reports with policy recommendations. These committee reports often receive less media coverage than House committee work but contain more substantive analysis. Senate debates on treaty implementation legislation provide an additional window into policy positions. |
| **Access Notes** | No paywall. SenCAplus (`sencanada.ca/en/sencaplus/`) is the Senate's online magazine with interviews and features. Live X (formerly Twitter) updates during sittings via @SenateCA. |

**Additional entry points:**
- SenCAplus (online magazine): `https://sencanada.ca/en/sencaplus/`
- Media centre: `https://sencanada.ca/en/media-centre/`
- Committee news: `https://sencanada.ca/en/committees/news/`

---

### 1.5 Official Gazette — Canada Gazette

| Field | Detail |
|---|---|
| **Institution** | Canada Gazette / Gazette du Canada |
| **Domain** | `gazette.gc.ca` |
| **Entry Point URL** | `https://gazette.gc.ca/accueil-home-eng.html` |
| **RSS/Atom Feed** | **Yes — three RSS feeds available.** Part I (Notices and proposed regulations): `https://www.gazette.gc.ca/rss/p1-eng.xml`; Part II (Official regulations, SORs): `https://www.gazette.gc.ca/rss/p2-eng.xml`; Part III (Acts of Parliament): `https://www.gazette.gc.ca/rss/en-ls-eng.xml`. French equivalents: `p1-fra.xml`, `p2-fra.xml`, `fr-ls-fra.xml`. |
| **Language** | English and French (bilingual, parallel publication) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Canada Gazette is the constitutional publication vehicle for all federal regulations, orders-in-council, and acts of Parliament |
| **Publication Frequency** | Part I: weekly (Saturdays). Part II: biweekly (Wednesdays, with extra editions as needed). Part III: after Royal Assent of each Act. |
| **Content Format** | HTML. Published editions are structured HTML with full regulatory text. PDF versions also available. |
| **Extraction Method** | RSS feed polling for new editions. Part I is most relevant for proposed regulations (e.g., sanctions regulations, trade measures, defence procurement). Part II for enacted regulations. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law and regulation. |
| **Why This Source** | Constitutional requirement: no federal regulation or order-in-council takes effect until published in the Canada Gazette. Sanctions designations (Special Economic Measures Act regulations), trade countermeasures (tariff surtaxes), and defence procurement approvals all appear here before or simultaneously with press release announcements. Part I proposed regulations include the Regulatory Impact Analysis Statement (RIAS) which explains the government's policy rationale. |
| **Access Notes** | No paywall, no authentication required. RSS feeds are free and well-maintained. Contact: info.gazette@tpsgc-pwgsc.gc.ca. The domain `canadagazette.gc.ca` also resolves to the same site. |

**Key RSS feed URLs:**

| Feed | URL (English) | URL (French) |
|---|---|---|
| Part I (Notices/proposed regs) | `https://www.gazette.gc.ca/rss/p1-eng.xml` | `https://www.gazette.gc.ca/rss/p1-fra.xml` |
| Part II (Official regulations) | `https://www.gazette.gc.ca/rss/p2-eng.xml` | `https://www.gazette.gc.ca/rss/p2-fra.xml` |
| Part III (Acts of Parliament) | `https://www.gazette.gc.ca/rss/en-ls-eng.xml` | `https://www.gazette.gc.ca/rss/fr-ls-fra.xml` |

---

### 1.6 Finance Ministry — Department of Finance Canada

| Field | Detail |
|---|---|
| **Institution** | Department of Finance Canada / Ministère des Finances Canada |
| **Domain** | `canada.ca/en/department-finance` |
| **Entry Point URL** | `https://www.canada.ca/en/department-finance/news.html` |
| **RSS/Atom Feed** | **Yes — multiple Atom feeds.** News releases: `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentfinance&type=newsreleases&sort=publishedDate&orderBy=desc&publishedDate%3E=2020-08-09&pick=100&format=atom&atomtitle=Canada%20News%20Centre%20-%20Department%20of%20Finance%20Canada%20-%20News%20Releases`. Also available: statements, speeches, backgrounders, media advisories (substitute `type=` parameter). Publications Atom: `https://www.canada.ca/content/dam/fin/documents/publications/pub-rep/publications-en.atom` |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. News releases for budget announcements, fiscal updates, tax policy changes, sanctions regulations, and bilateral/multilateral finance meetings (G7 Finance, IMF, World Bank). Volume surges around Budget Day and Fall Economic Statement. |
| **Content Format** | HTML on canada.ca. Budget documents and fiscal updates in HTML and PDF. Atom feeds via api.io.canada.ca. |
| **Extraction Method** | Atom feed polling via api.io.canada.ca (same pattern as GAC/DND). Department ID is `departmentfinance`. Publications Atom feed for budget documents and fiscal reports. |
| **Editorial Orientation** | Official fiscal/economic policy position. Under Minister of Finance François-Philippe Champagne, communications emphasize trade countermeasures, industrial strategy, and fiscal resilience. |
| **Why This Source** | Primary source for federal budget, Fall Economic Statement, tariff countermeasure announcements, and fiscal policy. Finance Canada news releases on sanctions regulations and trade surtaxes are often the first public signal of economic statecraft moves. Budget documents contain the definitive forward spending plan for defence, foreign aid, and trade facilitation. |
| **Access Notes** | No paywall. Budget documents typically released as a dedicated microsite within canada.ca. The `fin.gc.ca` legacy domain redirects to canada.ca. Stay-connected page at `https://www.canada.ca/en/department-finance/news/stay-connected.html` lists all available feeds. |

**Key Atom feed URLs:**

| Feed | Type parameter |
|---|---|
| News releases | `type=newsreleases` |
| Statements | `type=statements` |
| Speeches | `type=speeches` |
| Backgrounders | `type=backgrounders` |
| Media advisories | `type=mediaadvisories` |
| Publications (separate feed) | `https://www.canada.ca/content/dam/fin/documents/publications/pub-rep/publications-en.atom` |

---

### 1.7 Central Bank — Bank of Canada / Banque du Canada

| Field | Detail |
|---|---|
| **Institution** | Bank of Canada / Banque du Canada |
| **Domain** | `bankofcanada.ca` / `banqueducanada.ca` |
| **Entry Point URL** | `https://www.bankofcanada.ca/press/` (EN) / `https://www.banqueducanada.ca/presse/` (FR) |
| **RSS/Atom Feed** | **Yes — extensive RSS feeds available.** Hub page: `https://www.bankofcanada.ca/rss-feeds/`. Press releases: `https://www.bankofcanada.ca/content_type/press-releases/feed/`. Speeches: `https://www.bankofcanada.ca/content_type/speeches/feed/`. Exchange rates: `https://www.bankofcanada.ca/valet/fx_rss/`. See full list below. |
| **Language** | English and French (bilingual, parallel publication on both domains) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Interest rate decisions: 8 per year (scheduled Wednesdays at 9:45 AM ET). Monetary Policy Report: quarterly. Speeches: approximately monthly. Press releases and market notices: variable, several per week. Exchange rate RSS: daily updates. |
| **Content Format** | HTML for press releases and speeches. PDF for Monetary Policy Report, Financial Stability Report, and minutes. RSS feeds deliver structured data for exchange rates. |
| **Extraction Method** | RSS feed polling for press releases, speeches, announcements, and exchange rates. PDF download for quarterly reports. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Tiff Macklem, communications have emphasized inflation-targeting credibility and financial system resilience. The March 18, 2026 decision held the overnight rate at 2.25%. |
| **Why This Source** | The Bank of Canada is the only source for authoritative monetary policy decisions, inflation expectations, official exchange rates, and financial stability assessments. Interest rate announcements move the CAD and bond markets. Governor Macklem's speeches frequently contain forward guidance that markets parse closely. The Valet API and RSS feeds are among the most machine-friendly government data sources in Canada. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained and reliable. The Valet API (`https://www.bankofcanada.ca/valet/`) provides RESTful access to all Bank statistics. French-language mirror at `banqueducanada.ca`. |

**Key RSS feed URLs:**

| Feed | URL |
|---|---|
| Press releases | `https://www.bankofcanada.ca/content_type/press-releases/feed/` |
| Announcements | `https://www.bankofcanada.ca/content_type/announcements/feed/` |
| Speeches | `https://www.bankofcanada.ca/content_type/speeches/feed/` |
| Market notices | `https://www.bankofcanada.ca/content_type/notices/feed/` |
| Media advisories | `https://www.bankofcanada.ca/content_type/media-advisories/feed/` |
| News | `https://www.bankofcanada.ca/utility/news/feed/` |
| Monetary Policy Report | `https://www.bankofcanada.ca/content_type/mpr/feed/` |
| Financial Stability Report | `https://www.bankofcanada.ca/content_type/fsr/feed/` |
| Business Outlook Survey | `https://www.bankofcanada.ca/content_type/bos/feed/` |
| All publications | `https://www.bankofcanada.ca/content_type/publications/feed/` |
| Exchange rates (all) | `https://www.bankofcanada.ca/valet/fx_rss/` |
| USD/CAD rate | `https://www.bankofcanada.ca/valet/fx_rss/FXUSDCAD` |

---

### 1.8 Trade / Commerce — Innovation, Science and Economic Development Canada (ISED) / Trade Commissioner Service

| Field | Detail |
|---|---|
| **Institution** | Innovation, Science and Economic Development Canada (ISED) / Innovation, Sciences et Développement économique Canada (ISDE). Also: Trade Commissioner Service (TCS) under Global Affairs Canada. |
| **Domain** | `ised-isde.canada.ca` / `canada.ca/en/department-of-industry` |
| **Entry Point URL** | `https://ised-isde.canada.ca/site/media-room/en` (ISED media room) |
| **RSS/Atom Feed** | **Yes.** `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofindustry&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=100&format=atom&atomtitle=Innovation+Science+and+Economic+Development+Canada` |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Communications cover trade policy (tariff countermeasures, CUSMA/USMCA review), investment screening (Investment Canada Act decisions), critical minerals strategy, technology/AI policy, and industrial strategy. |
| **Content Format** | HTML on canada.ca. Atom feed via api.io.canada.ca. |
| **Extraction Method** | Atom feed polling. Department ID is `departmentofindustry` (ISED's legal name is still "Department of Industry" in the enabling statute). |
| **Editorial Orientation** | Official trade and industrial policy position. Under Minister Champagne (who also holds Finance), ISED communications emphasize supply chain resilience, critical minerals, semiconductor strategy, and Buy Canadian procurement. |
| **Why This Source** | Primary source for Investment Canada Act enforcement decisions (foreign investment screening — especially Chinese investments in critical minerals), trade countermeasures, and industrial strategy announcements. ISED/TCS releases are the raw data for BNN Bloomberg and Financial Post trade coverage. The Trade Commissioner Service, while organizationally under GAC, often co-publishes trade facilitation announcements through ISED. |
| **Access Notes** | No paywall. Email subscription at `ised-isde.canada.ca/site/ised/en/email-subscriptions`. Media contact: media@ised-isde.gc.ca. |

**Additional entry points:**
- Export Development Canada (EDC) newsroom: `https://www.edc.ca/en/about-us/newsroom.html`
- Trade Commissioner Service: `https://www.tradecommissioner.gc.ca/`

---

### 1.9 Intelligence / National Security — CSIS, PCO (NSIA), NSICOP

#### 1.9a Canadian Security Intelligence Service (CSIS)

| Field | Detail |
|---|---|
| **Institution** | Canadian Security Intelligence Service / Service canadien du renseignement de sécurité (CSIS/SCRS) |
| **Domain** | `canada.ca/en/security-intelligence-service` |
| **Entry Point URL** | `https://www.canada.ca/en/security-intelligence-service/corporate/publications.html` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS via api.io.canada.ca with dept parameter] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Domestic constraints |
| **Publication Frequency** | Low. The annual Public Report on the Threat Environment is the primary regular publication (typically released annually, though timing varies). Occasional public statements, threat assessments, and testimony transcripts. |
| **Content Format** | PDF for annual public report. HTML for public statements. |
| **Extraction Method** | Periodic check of publications page. PDF download for annual report. |
| **Editorial Orientation** | Intelligence agency — deliberately restrained public communications. The annual public report is the only systematic disclosure. Under CSIS Director David Vigneault's tenure, the agency increased public communications on foreign interference (Chinese, Indian, Iranian threats) in response to the Hogue Commission on Foreign Interference. |
| **Why This Source** | CSIS's annual public report is the single most important unclassified assessment of threats to Canadian national security. It covers espionage, foreign interference, terrorism, and cyber threats. CSIS's 2025-2026 public communications on foreign interference from China, India, and Iran have been unusually forthcoming compared to historical practice, driven by the Hogue Commission findings and political pressure. However, the bulk of intelligence signal emerges through leaks to Globe and Mail, Global News, and CBC rather than official channels. |
| **Access Notes** | `canada.ca/en/security-intelligence-service` is a minimal page. CSIS does not maintain a press release feed. Publications are archived at `publications.gc.ca`. |

#### 1.9b Privy Council Office — National Security and Intelligence Advisor (NSIA)

| Field | Detail |
|---|---|
| **Institution** | Privy Council Office (PCO) — National Security and Intelligence Advisor (NSIA) to the Prime Minister |
| **Domain** | `canada.ca/en/privy-council` |
| **Entry Point URL** | `https://www.canada.ca/en/privy-council/services/security/national-security-intelligence-advisor-branch-reports-publications.html` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Diplomatic alignment |
| **Publication Frequency** | Infrequent. Reports and publications from the NSIA branch are published periodically — notably threat assessments related to elections and national security reviews. Statements from the NSIA appear around G7 NSA meetings and major security events. |
| **Content Format** | HTML and PDF. |
| **Extraction Method** | Periodic check of the NSIA publications page. |
| **Editorial Orientation** | Official national security coordination position. The NSIA (currently Nathalie Drouin) serves as the Prime Minister's principal advisor on national security matters and coordinates the security and intelligence community. |
| **Why This Source** | The PCO/NSIA branch publishes threat assessments to Canadian elections, convenes G7 NSA meetings, and coordinates national security policy. The NSIA's mandate letter (published November 2024) and periodic statements provide signals about national security priorities. The PCO's coordination role means its communications often preview or frame interagency positions. |
| **Access Notes** | Minimal public-facing communications. Most PCO/NSIA activity is not published. |

#### 1.9c National Security and Intelligence Committee of Parliamentarians (NSICOP)

| Field | Detail |
|---|---|
| **Institution** | National Security and Intelligence Committee of Parliamentarians (NSICOP) / Comité des parlementaires sur la sécurité nationale et le renseignement (CPSNR) |
| **Domain** | `nsicop-cpsnr.ca` |
| **Entry Point URL** | `https://nsicop-cpsnr.ca/reports-rapports-en.html` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Domestic constraints |
| **Publication Frequency** | Low. Annual report plus occasional special reports. The 2024 Annual Report was tabled in Parliament on September 15, 2025. Special reports issued on specific reviews (e.g., counterterrorist financing review launched November 2025). |
| **Content Format** | PDF for annual and special reports. HTML for website content. |
| **Extraction Method** | Periodic check of reports page. PDF download. |
| **Editorial Orientation** | Parliamentary oversight — non-partisan. NSICOP has access to classified information and produces redacted public reports. The committee's reports on foreign interference have been politically significant. |
| **Why This Source** | NSICOP is Canada's closest equivalent to the U.S. Congressional intelligence committees in terms of oversight access. Its annual reports contain redacted summaries of reviews across CSIS, CSE (Communications Security Establishment), DND intelligence, and RCMP national security. The 2024 report on foreign interference by parliamentarians generated front-page coverage for weeks. Report publication dates are themselves signals. |
| **Access Notes** | Standalone website, independent of canada.ca. Reports are published in full as PDFs after tabling in Parliament. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Public Safety Canada / Sécurité publique Canada

| Field | Detail |
|---|---|
| **Institution** | Public Safety Canada / Sécurité publique Canada |
| **Domain** | `canada.ca/en/public-safety-canada` / `publicsafety.gc.ca` |
| **Entry Point URL** | `https://www.publicsafety.gc.ca/cnt/nws/nws-rlss/index-en.aspx` |
| **RSS/Atom Feed** | **Yes.** `https://api.io.canada.ca/io-server/gc/news/en/v2?dept=publicsafetycanada&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=100&format=atom&atomtitle=Public+Safety+Canada` |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Domestic constraints |
| **Publication Frequency** | 3-5 per week. News releases cover border security, firearms policy, organized crime, cybersecurity, emergency management, and national security legislation. |
| **Content Format** | HTML on canada.ca/publicsafety.gc.ca. Atom feed via api.io.canada.ca. |
| **Extraction Method** | Atom feed polling. Department ID is `publicsafetycanada`. |
| **Editorial Orientation** | Official public safety policy. Communications emphasize law enforcement tools, border integrity, and community safety. Under the current government, increased emphasis on foreign interference countermeasures and firearms regulation. |
| **Why This Source** | Public Safety Canada is the umbrella department for CSIS, RCMP, CBSA (Canada Border Services Agency), and CSC. Its communications often aggregate policy announcements that span multiple agencies. National security legislation (e.g., Criminal Code amendments for terrorism, foreign interference registry) originates from Public Safety. The department's news releases on extortion, border security, and organized crime capture the domestic security dimension that DND communications do not cover. |
| **Access Notes** | The legacy `publicsafety.gc.ca` domain coexists with the canada.ca page. Both are active. National security-specific news releases at `https://www.publicsafety.gc.ca/cnt/ntnl-scrt/nws-rlss-en.aspx`. |

#### 1.10b Hogue Commission / Public Inquiry into Foreign Interference

| Field | Detail |
|---|---|
| **Institution** | Public Inquiry into Foreign Interference in Federal Electoral Processes and Democratic Institutions (Hogue Commission) |
| **Domain** | `foreigninterferencecommission.ca` |
| **Entry Point URL** | `https://foreigninterferencecommission.ca/en/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Security & defence autonomy |
| **Publication Frequency** | Periodic. Reports, rulings, and hearing schedules published as proceedings advance. The final report was delivered in early 2025. Commission may still publish supplementary materials and follow-up communications. |
| **Content Format** | HTML and PDF. Reports are substantial PDF documents. Hearing transcripts available. |
| **Extraction Method** | Periodic check of commission website. PDF download for reports. |
| **Editorial Orientation** | Independent judicial inquiry. Commissioner Marie-Josée Hogue's findings on Chinese, Indian, and other foreign interference in Canadian elections are non-partisan but politically consequential. |
| **Why This Source** | The Hogue Commission is the single most important source for understanding the scope of foreign interference in Canadian democracy — a blind spot identified in the Source Intelligence Map. Commission findings directly shape CSIS authorities, election security measures, and bilateral relations with China and India. Even after the final report, follow-up materials and government responses to recommendations generate signal. |
| **Access Notes** | Standalone website. May eventually be archived at Library and Archives Canada. |

#### 1.10c Governor General of Canada

| Field | Detail |
|---|---|
| **Institution** | Office of the Governor General of Canada / Bureau du gouverneur général du Canada |
| **Domain** | `gg.ca` |
| **Entry Point URL** | `https://www.gg.ca/en/media` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at gg.ca] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Several times weekly. Media releases cover state visits, diplomatic credential ceremonies (ambassador accreditations), Royal Assent of legislation, and speech from the throne. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of media centre. |
| **Editorial Orientation** | Vice-regal — constitutionally non-partisan. The Governor General (currently Mary Simon) represents the Crown and performs ceremonial functions with diplomatic significance. |
| **Why This Source** | The Governor General's credential ceremonies for incoming ambassadors are the formal record of diplomatic representation changes. State visit announcements signal bilateral relationship priorities. The Speech from the Throne sets the legislative agenda. Governor General Simon's role as Canada's first Indigenous head of state adds diplomatic significance to her international engagements. |
| **Access Notes** | No paywall. Media centre includes news releases, photos, and videos. |

#### 1.10d Natural Resources Canada / Ressources naturelles Canada

| Field | Detail |
|---|---|
| **Institution** | Natural Resources Canada / Ressources naturelles Canada (NRCan/RNCan) |
| **Domain** | `canada.ca/en/natural-resources-canada` / `natural-resources.canada.ca` |
| **Entry Point URL** | `https://natural-resources.canada.ca/news/news-releases` |
| **RSS/Atom Feed** | RSS feeds available at `https://natural-resources.canada.ca/corporate/rss-feeds`. [VERIFY specific feed URLs] |
| **Language** | English and French (bilingual) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 2-4 per week. Communications cover critical minerals strategy, energy transition, pipeline decisions, LNG export permits, Arctic resource development, and Canada-U.S. energy trade. |
| **Content Format** | HTML on canada.ca. |
| **Extraction Method** | RSS feed polling or Atom feed via api.io.canada.ca. |
| **Editorial Orientation** | Official natural resource and energy policy. Under current government, communications emphasize critical minerals as strategic assets, energy transition, and supply chain security. |
| **Why This Source** | Canada's critical minerals strategy is a core element of its economic statecraft — positioning Canada as a secure, allied-nation supplier of minerals essential for semiconductors, batteries, and defence systems. NRCan communications on critical mineral extraction, LNG terminal approvals, and energy export policy directly affect Canada's trade leverage with the U.S. and strategic positioning vis-à-vis China. Energy is Canada's largest export sector and the foundation of the Canada-U.S. economic relationship. |
| **Access Notes** | No paywall. RSS feeds page at natural-resources.canada.ca. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS/Atom Available | Priority | Content Format | Frequency | canada.ca API |
|---|---|---|---|---|---|---|---|
| 1 | PMO | `pm.gc.ca/en/news/releases` | **Yes** (RSS) | P1 | HTML | Daily | No (own RSS) |
| 2 | GAC (Foreign Affairs) | `international.canada.ca/en/global-affairs/news` | **Yes** (Atom) | P1 | HTML | Daily | Yes |
| 3 | DND/CAF | `canada.ca/en/department-national-defence/corporate/news.html` | **Yes** (Atom) | P1 | HTML | Daily | Yes |
| 4a | House of Commons | `ourcommons.ca/en/newsroom` | [VERIFY] | P2 | HTML/XML | Daily (session) | No |
| 4b | Senate | `sencanada.ca/en/newsroom/` | [VERIFY] | P2 | HTML | Weekly (session) | No |
| 5 | Canada Gazette | `gazette.gc.ca` | **Yes** (RSS x3) | P2 | HTML/PDF | Weekly/biweekly | No (own RSS) |
| 6 | Finance Canada | `canada.ca/en/department-finance/news.html` | **Yes** (Atom) | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | Bank of Canada | `bankofcanada.ca/press/` | **Yes** (RSS x12+) | P2 | HTML/PDF/RSS | Variable | No (own RSS) |
| 8 | ISED | `ised-isde.canada.ca/site/media-room/en` | **Yes** (Atom) | P2 | HTML | 2-5/week | Yes |
| 9a | CSIS | `canada.ca/en/security-intelligence-service/corporate/publications.html` | No | P2 | PDF/HTML | Annual + occasional | No |
| 9b | PCO/NSIA | `canada.ca/en/privy-council/services/security/...` | No | P2 | HTML/PDF | Infrequent | No |
| 9c | NSICOP | `nsicop-cpsnr.ca/reports-rapports-en.html` | No | P2 | PDF | Annual + special | No |
| 10a | Public Safety | `publicsafety.gc.ca/cnt/nws/nws-rlss/index-en.aspx` | **Yes** (Atom) | P2 | HTML | 3-5/week | Yes |
| 10b | Hogue Commission | `foreigninterferencecommission.ca` | [VERIFY] | P2 | HTML/PDF | Periodic | No |
| 10c | Governor General | `gg.ca/en/media` | [VERIFY] | P2 | HTML | Weekly | No |
| 10d | NRCan | `natural-resources.canada.ca/news/news-releases` | **Yes** (RSS) | P2 | HTML | 2-4/week | Partial |

---

## 3. MONITORING CONFIGURATION

```yaml
# Canada Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/ca.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: ca_pmo
    name: Prime Minister's Office
    name_fr: Cabinet du premier ministre
    domain: pm.gc.ca
    entry_url: "https://www.pm.gc.ca/en/news/releases"
    rss_feed:
      en: "https://pm.gc.ca/en/news.rss"
      fr: "https://pm.gc.ca/fr/nouvelles.rss"
      media: "https://pm.gc.ca/en/media.rss"
    language: [en, fr]
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "RSS feed covers all news types (releases, statements, speeches, readouts). No bot protection observed."

  - id: ca_gac
    name: Global Affairs Canada
    name_fr: Affaires mondiales Canada
    domain: international.canada.ca
    entry_url: "https://international.canada.ca/en/global-affairs/news"
    rss_feed:
      all_news_en: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate>=2015-01-01&pick=1000&format=atom&atomtitle=Global Affairs Canada news"
      all_news_fr: "https://api.io.canada.ca/io-server/gc/news/fr/v2?dept=departmentofforeignaffairstradeanddevelopment&sort=publishedDate&orderBy=desc&publishedDate>=2015-01-01&pick=1000&format=atom&atomtitle=Affaires mondiales Canada nouvelles"
      travel_advisories: "https://travel.gc.ca/feeds/rss/eng/travel-updates-24.aspx"
    language: [en, fr]
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html
    extraction_method: atom_poll
    poll_interval_hours: 2
    notes: "Atom feeds via api.io.canada.ca. Supports type filtering (newsreleases, statements, readouts, speeches, mediaadvisories). Travel advisories on separate RSS."

  - id: ca_dnd
    name: Department of National Defence / Canadian Armed Forces
    name_fr: Ministère de la Défense nationale / Forces armées canadiennes
    domain: canada.ca
    entry_url: "https://www.canada.ca/en/department-national-defence/corporate/news.html"
    rss_feed:
      en: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentnationaldefense&sort=publishedDate&orderBy=desc&publishedDate>=2021-07-23&pick=50&format=atom&atomtitle=National+Defence+and+the+Canadian+Armed+Forces"
    language: [en, fr]
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html
    extraction_method: atom_poll
    poll_interval_hours: 2
    notes: "Same api.io.canada.ca pattern. Legacy forces.gc.ca RSS feeds return 404 — use api.io.canada.ca. Maple Leaf newsletter at canada.ca/en/department-national-defence/maple-leaf.html."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: ca_house_commons
    name: House of Commons
    name_fr: Chambre des communes
    domain: ourcommons.ca
    entry_url: "https://www.ourcommons.ca/en/newsroom"
    rss_feed: null  # [VERIFY]
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html_xml
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Open Data XML at ourcommons.ca/en/open-data. Committee newsletter via subscription.ourcommons.ca. LEGISinfo at parl.ca/legisinfo for bill tracking."

  - id: ca_senate
    name: Senate of Canada
    name_fr: Sénat du Canada
    domain: sencanada.ca
    entry_url: "https://sencanada.ca/en/newsroom/"
    rss_feed: null  # [VERIFY]
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "weekly_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "eNewsletter subscription available. Committee reports on foreign affairs (AEFA) and defence (SECD) are high-value."

  - id: ca_gazette
    name: Canada Gazette
    name_fr: Gazette du Canada
    domain: gazette.gc.ca
    entry_url: "https://gazette.gc.ca/accueil-home-eng.html"
    rss_feed:
      part_i_en: "https://www.gazette.gc.ca/rss/p1-eng.xml"
      part_i_fr: "https://www.gazette.gc.ca/rss/p1-fra.xml"
      part_ii_en: "https://www.gazette.gc.ca/rss/p2-eng.xml"
      part_ii_fr: "https://www.gazette.gc.ca/rss/p2-fra.xml"
      part_iii_en: "https://www.gazette.gc.ca/rss/en-ls-eng.xml"
      part_iii_fr: "https://www.gazette.gc.ca/rss/fr-ls-fra.xml"
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "weekly_biweekly"
    content_format: html_pdf
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Part I (Saturdays): proposed regulations. Part II (biweekly Wednesdays): enacted regulations/SORs. Part III: Acts after Royal Assent. Sanctions regulations appear in Part II."

  - id: ca_finance
    name: Department of Finance Canada
    name_fr: Ministère des Finances Canada
    domain: canada.ca
    entry_url: "https://www.canada.ca/en/department-finance/news.html"
    rss_feed:
      news_releases: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentfinance&type=newsreleases&sort=publishedDate&orderBy=desc&publishedDate%3E=2020-08-09&pick=100&format=atom&atomtitle=Department+of+Finance+Canada+News+Releases"
      statements: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentfinance&type=statements&sort=publishedDate&orderBy=desc&publishedDate%3E=2020-08-09&pick=100&format=atom&atomtitle=Department+of+Finance+Canada+Statements"
      publications: "https://www.canada.ca/content/dam/fin/documents/publications/pub-rep/publications-en.atom"
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: atom_poll
    poll_interval_hours: 6
    notes: "Budget documents and Fall Economic Statement as dedicated microsites. Supports type filtering (newsreleases, statements, speeches, backgrounders, mediaadvisories)."

  - id: ca_bank_of_canada
    name: Bank of Canada
    name_fr: Banque du Canada
    domain: bankofcanada.ca
    entry_url: "https://www.bankofcanada.ca/press/"
    rss_feed:
      press_releases: "https://www.bankofcanada.ca/content_type/press-releases/feed/"
      announcements: "https://www.bankofcanada.ca/content_type/announcements/feed/"
      speeches: "https://www.bankofcanada.ca/content_type/speeches/feed/"
      market_notices: "https://www.bankofcanada.ca/content_type/notices/feed/"
      mpr: "https://www.bankofcanada.ca/content_type/mpr/feed/"
      fsr: "https://www.bankofcanada.ca/content_type/fsr/feed/"
      fx_rates_all: "https://www.bankofcanada.ca/valet/fx_rss/"
      fx_usdcad: "https://www.bankofcanada.ca/valet/fx_rss/FXUSDCAD"
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best machine-readable government source in Canada. Valet API at bankofcanada.ca/valet/ for RESTful data access. Interest rate decisions 8x/year (Wednesdays 9:45 AM ET). French mirror at banqueducanada.ca."

  - id: ca_ised
    name: Innovation, Science and Economic Development Canada
    name_fr: Innovation, Sciences et Développement économique Canada
    domain: ised-isde.canada.ca
    entry_url: "https://ised-isde.canada.ca/site/media-room/en"
    rss_feed:
      en: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=departmentofindustry&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=100&format=atom&atomtitle=Innovation+Science+and+Economic+Development+Canada"
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: atom_poll
    poll_interval_hours: 12
    notes: "Department ID is 'departmentofindustry' (statutory name). Investment Canada Act decisions, critical minerals, trade countermeasures."

  - id: ca_csis
    name: Canadian Security Intelligence Service
    name_fr: Service canadien du renseignement de sécurité
    domain: canada.ca
    entry_url: "https://www.canada.ca/en/security-intelligence-service/corporate/publications.html"
    rss_feed: null
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: annual_plus_occasional
    content_format: pdf_html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Annual public report is primary output. Flag any new publication as high-priority anomaly. Real intelligence signal comes via leaks to Globe and Mail, Global News, CBC."

  - id: ca_nsicop
    name: National Security and Intelligence Committee of Parliamentarians
    name_fr: Comité des parlementaires sur la sécurité nationale et le renseignement
    domain: nsicop-cpsnr.ca
    entry_url: "https://nsicop-cpsnr.ca/reports-rapports-en.html"
    rss_feed: null
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "annual_plus_special"
    content_format: pdf
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Redacted classified material. Annual report + special reports. 2024 foreign interference report was politically significant."

  - id: ca_public_safety
    name: Public Safety Canada
    name_fr: Sécurité publique Canada
    domain: publicsafety.gc.ca
    entry_url: "https://www.publicsafety.gc.ca/cnt/nws/nws-rlss/index-en.aspx"
    rss_feed:
      en: "https://api.io.canada.ca/io-server/gc/news/en/v2?dept=publicsafetycanada&sort=publishedDate&orderBy=desc&publishedDate>=2021-10-25&pick=100&format=atom&atomtitle=Public+Safety+Canada"
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: atom_poll
    poll_interval_hours: 6
    notes: "Umbrella for CSIS, RCMP, CBSA. National security news at publicsafety.gc.ca/cnt/ntnl-scrt/nws-rlss-en.aspx."

  - id: ca_nrcan
    name: Natural Resources Canada
    name_fr: Ressources naturelles Canada
    domain: natural-resources.canada.ca
    entry_url: "https://natural-resources.canada.ca/news/news-releases"
    rss_feed: "https://natural-resources.canada.ca/corporate/rss-feeds"  # [VERIFY specific feed URLs]
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 12
    notes: "Critical minerals strategy, energy exports, LNG permits, Arctic resources."

  - id: ca_governor_general
    name: Governor General of Canada
    name_fr: Gouverneur général du Canada
    domain: gg.ca
    entry_url: "https://www.gg.ca/en/media"
    rss_feed: null  # [VERIFY]
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "several_weekly"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Ambassador credential ceremonies, state visits, Royal Assent."

  - id: ca_hogue_commission
    name: Public Inquiry into Foreign Interference
    name_fr: Commission d'enquête sur l'ingérence étrangère
    domain: foreigninterferencecommission.ca
    entry_url: "https://foreigninterferencecommission.ca/en/"
    rss_feed: null  # [VERIFY]
    language: [en, fr]
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - security_defense_autonomy
    publication_frequency: periodic
    content_format: html_pdf
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Final report delivered 2025. Monitor for supplementary materials and government response to recommendations."

# Shared API pattern for canada.ca departments
canada_ca_api_config:
  base_url_pattern: "https://api.io.canada.ca/io-server/gc/news/{lang}/v2?dept={dept_id}&sort=publishedDate&orderBy=desc&publishedDate>={date}&pick={count}&format=atom&atomtitle={title}"
  departments_on_api:
    - dept_id: departmentofforeignaffairstradeanddevelopment
      name: Global Affairs Canada
    - dept_id: departmentnationaldefense
      name: National Defence
    - dept_id: departmentfinance
      name: Department of Finance
    - dept_id: departmentofindustry
      name: ISED
    - dept_id: publicsafetycanada
      name: Public Safety Canada
  type_filters:
    - newsreleases
    - statements
    - readouts
    - mediaadvisories
    - speeches
    - backgrounders
  languages: [en, fr]
  rate_limit: "no known rate limit, but recommend max 1 request per 5 seconds"
  bot_protection: none_observed
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Canadian government communications are professionally produced, factually reliable in what they state, but strategically selective in what they choose to highlight or omit. The bilingual requirement means all official content is published simultaneously in English and French, but the framing emphasis can subtly differ between language versions — the French version occasionally includes formulations more attuned to Quebec sensitivities. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage.

- **PMO**: Cross-reference PM statements against same-day reporting in CBC News and Globe and Mail. Discrepancies between the official readout and media characterization of the same event (e.g., a bilateral call with the U.S. President) frequently reveal the analytical gulf between government framing and independent assessment. Under Carney, the PMO has adopted an unusually direct economic messaging style — cross-reference economic claims against BNN Bloomberg and Financial Post analysis.
- **GAC (Global Affairs)**: Diplomatic communications should be triangulated with CBC (independent broadcast perspective), Globe and Mail (elite foreign-policy commentary from Campbell Clark, Steven Chase), and La Presse / Radio-Canada (francophone framing of Canada's international positioning). When GAC statements on bilateral meetings omit specific outcomes, cross-reference with the counterpart government's readout — the delta between the two reveals the actual state of negotiations.
- **DND/CAF**: Defence communications report deployments, procurement decisions, and NORAD modernization milestones but systematically understate capability gaps, procurement delays, and the magnitude of the NATO spending shortfall. Cross-reference with Canadian Defence Review (trade-press detail), Macdonald-Laurier Institute (hawkish analytical perspective), and Ottawa Citizen/David Pugliese (the most persistent independent defence reporter). The Hill Times covers parliamentary committee testimony from DND officials that frequently contains admissions not present in press releases.
- **Bank of Canada**: Monetary policy communications are technically rigorous and less subject to political distortion than any other government source. Cross-reference with BNN Bloomberg for market interpretation and Financial Post for independent economic analysis. The Monetary Policy Report's economic projections should be compared against private-sector forecasts aggregated by Finance Canada.
- **Finance Canada**: Budget documents and fiscal updates are the definitive source for spending plans, but presentation framing (especially revenue projections and deficit trajectories) should be cross-referenced with Parliamentary Budget Officer (PBO) analyses at `pbo-dpb.ca`, which provide independent fiscal forecasting.
- **CSIS / NSICOP**: Intelligence agency communications are rare and deliberately calibrated. The annual CSIS public report understates threats in some areas (e.g., espionage by allied nations) and highlights others (e.g., Chinese/Iranian interference) according to political priorities. Cross-reference with Globe and Mail (Robert Fife, Steven Chase on national security leaks), Global News (Mercedes Stephenson), and NSICOP reports for the classified-but-redacted perspective.

**4.2 The canada.ca centralization and api.io.canada.ca Atom feed advantage**

Five of Canada's government source categories publish through the centralized `canada.ca` portal and offer standardized Atom feeds via `api.io.canada.ca`. This is a significant operational advantage over many other countries' government web infrastructure:
- A single extraction module with department-ID parameterization can service all five departments (GAC, DND, Finance, ISED, Public Safety)
- Atom feeds provide structured metadata (title, date, summary, URL) without requiring HTML scraping
- The API supports filtering by content type (`newsreleases`, `statements`, `readouts`, `speeches`, `mediaadvisories`, `backgrounders`)
- No bot protection or rate limiting has been observed on the API

Sources outside the `api.io.canada.ca` ecosystem — PMO (`pm.gc.ca`), Bank of Canada (`bankofcanada.ca`), Canada Gazette (`gazette.gc.ca`), Parliament (`ourcommons.ca`, `sencanada.ca`), NSICOP (`nsicop-cpsnr.ca`), and the Governor General (`gg.ca`) — require independent extraction configurations.

**4.3 The bilingual dimension**

Canada's Official Languages Act requires all federal government communications to be published simultaneously in English and French. This creates a natural deduplication challenge: every government announcement generates two parallel items (one EN, one FR). The pipeline should:
- Default to the English version as the canonical record (matching the `metadata: en` setting in `ca.yaml`)
- Monitor the French version selectively for Quebec-specific framing differences, particularly in GAC and PMO communications on La Francophonie, Quebec-France relations, and cultural policy
- Note that Radio-Canada (French CBC) and La Presse often amplify different aspects of the same government announcement than their English-language counterparts

**4.4 The CSIS/intelligence transparency gap**

Canada's intelligence agencies (CSIS, CSE, DND Intelligence) produce minimal public communications — a structural gap identified in the Source Intelligence Map's coverage gap assessment. The signal pathway for intelligence-relevant information is:
- CSIS annual public report (the only systematic unclassified assessment)
- NSICOP annual and special reports (redacted classified material)
- Hogue Commission findings (foreign interference specifically)
- Public Safety Canada news releases (legislative/policy context)
- Leaks to investigative media: Globe and Mail (Fife/Chase), Global News (Stephenson), CBC (Murray Brewster)
- Parliamentary committee testimony (FAAE, NDDN, SECU) — available via ParlVU and Hansard

The pipeline should not allocate significant resources to polling CSIS's page but should flag any new CSIS or NSICOP publication as a high-priority anomaly requiring immediate triage.

**4.5 The Parliamentary Budget Officer as independent check**

The Parliamentary Budget Officer (PBO) at `pbo-dpb.ca` provides independent fiscal and economic analysis that frequently contradicts Finance Canada and DND communications. PBO reports on defence spending, fiscal sustainability, and costing of government programs are essential for validating or challenging official claims. While not included in the 10 core categories above, PBO publications should be monitored as a cross-reference source for economic statecraft and defence spending signals.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for api.io.canada.ca

The `api.io.canada.ca` Atom feed API services 5 of 17 monitored government endpoints. A single scraper module with department-ID parameterization can service all five:

- **URL pattern**: `https://api.io.canada.ca/io-server/gc/news/{lang}/v2?dept={dept_id}&sort=publishedDate&orderBy=desc&publishedDate>={start_date}&pick={count}&format=atom&atomtitle={title}`
- **Department IDs**: `departmentofforeignaffairstradeanddevelopment` (GAC), `departmentnationaldefense` (DND), `departmentfinance` (Finance), `departmentofindustry` (ISED), `publicsafetycanada` (Public Safety)
- **Type filters** (append `&type={type}`): `newsreleases`, `statements`, `readouts`, `mediaadvisories`, `speeches`, `backgrounders`
- **Language**: Replace `{lang}` with `en` or `fr`
- **Rate limit**: No known rate limit; recommend maximum 1 request per 5 seconds as a courtesy
- **Bot protection**: None observed on the API endpoint

### 5.2 RSS/Atom-Enabled Sources (Priority for Automation)

Canada offers unusually strong RSS/Atom coverage across government sources — 9 of 17 endpoints provide feeds:

1. **api.io.canada.ca** (Atom): GAC, DND, Finance, ISED, Public Safety — standardized, structured, filterable
2. **PMO** (RSS): `pm.gc.ca/en/news.rss` — all news types, EN and FR
3. **Bank of Canada** (RSS): 12+ individual feeds covering press releases, speeches, publications, exchange rates, and economic indicators. The Valet API provides additional RESTful data access
4. **Canada Gazette** (RSS): Three feeds for Parts I, II, and III, in both EN and FR
5. **Natural Resources Canada** (RSS): Available but specific URLs require verification

This is a significantly better RSS coverage ratio than most countries. Prioritize feed-based polling over HTML scraping wherever feeds are available.

### 5.3 PDF Extraction Requirements

Three sources publish substantially in PDF:
- **Canada Gazette**: While the main editions are HTML, some regulatory annexes and schedules are PDF
- **Bank of Canada**: Monetary Policy Report, Financial Stability Report, and meeting minutes are multi-page PDF. Text-based, well-structured
- **CSIS**: Annual public report is a substantial PDF (50-100 pages). NSICOP reports are also PDF
- **Finance Canada**: Budget documents contain extensive PDF annexes with fiscal tables

### 5.4 Language and Encoding

All government sources publish bilingually in English and French. All canada.ca content is UTF-8 encoded. The `api.io.canada.ca` feeds return UTF-8 Atom XML. PMO RSS feeds are UTF-8. Bank of Canada feeds are UTF-8. The pipeline should:
- Ingest the English version by default (`metadata: en` per ca.yaml)
- Flag French-language versions of GAC and PMO communications for selective francophone-framing analysis
- Normalize all text to UTF-8 on ingestion (no legacy encoding issues observed across Canadian government sites)

### 5.5 Deduplication Across Sources

Government announcements in Canada frequently appear on multiple channels simultaneously:
- A trade countermeasure announcement appears in PMO releases, Finance Canada news, ISED news, and the Canada Gazette Part II (as a regulation)
- A defence deployment announcement appears in PMO releases, DND news, and GAC statements
- A sanctions designation appears in GAC statements, Finance Canada news, and the Canada Gazette Part II (as a Special Economic Measures Act regulation)
- Every announcement appears in both English and French (doubling the raw count)

Implement content-hash deduplication. Use the English version as canonical. For legal/regulatory text, use the Canada Gazette version as canonical. For policy announcements, use the originating department (GAC for diplomatic, DND for defence, Finance for fiscal) as canonical.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | PMO, GAC, DND | Every 2 hours | Daily publication, policy-critical, alliance-shaping |
| P2-Active | Finance, Public Safety, Bank of Canada, ISED, Canada Gazette | Every 6 hours | Regular publishing schedule, market-relevant |
| P2-Scheduled | House of Commons, Senate, Governor General, NRCan | Every 12 hours | Session-dependent or periodic |
| P2-Minimal | CSIS, NSICOP, PCO/NSIA, Hogue Commission | Weekly | Infrequent but high-impact; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| api.io.canada.ca outage | GAC, DND, Finance, ISED, Public Safety | Fall back to HTML scraping of each department's news page on canada.ca. Monitor @CanadaFP (GAC), @NationalDefence, @finaboriquebec on X. |
| pm.gc.ca downtime | PMO | Monitor @CanadianPM and @PMCanadien on X for real-time statements. Canadian Press wire will carry PMO releases within minutes. |
| bankofcanada.ca outage | Bank of Canada | Monetary policy decisions are simultaneously released to wire services (Reuters, Bloomberg, CP). Interest rate decisions also posted to LSEG/Bloomberg terminals. |
| gazette.gc.ca outage | Canada Gazette | The Open Government Portal at `open.canada.ca` archives gazette data. `canadagazette.gc.ca` may resolve to a different mirror. |
| Parliamentary site downtime | House of Commons, Senate | ParlVU (`parlvu.parl.gc.ca`) for live proceedings. LEGISinfo (`parl.ca/legisinfo`) for bill status. The Canadian Press covers major parliamentary proceedings in real-time. |
| NSICOP/CSIS sites down | NSICOP, CSIS | Reports tabled in Parliament are available via ourcommons.ca and sencanada.ca. Publications also archived at `publications.gc.ca`. |

---

*This supplement should be reviewed quarterly, upon any change in government (following a federal election), upon significant restructuring of the canada.ca platform or the api.io.canada.ca feed system, or following machinery-of-government changes that create, dissolve, or reorganize federal departments.*
