# Official Government Sources Supplement: ROMANIA

**Primary language of political discourse: Romanian**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Romania (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Romania. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Romania's government web infrastructure is decentralized. Unlike Mexico's unified `gob.mx` portal, Romanian ministries and institutions maintain independent websites across a mix of domains (`.gov.ro`, `.ro`, and ministry-specific subdomains). The Government of Romania portal (`gov.ro`) aggregates Prime Ministerial communications and cross-cutting government decisions but does not serve as a publishing platform for individual ministries. The Presidency (`presidency.ro`) operates entirely separate infrastructure. This decentralization means there is no single extraction pattern — each institution requires a dedicated scraper configuration — but it also reduces single-point-of-failure risk. A notable strength is the National Bank of Romania (BNR), which provides well-structured RSS feeds and XML data endpoints, making it the most machine-friendly government source in Romania. Most other institutions lack RSS and require HTML scraping or periodic polling.

---

## 1. OFFICIAL GOVERNMENT SOURCES: ROMANIA

### 1.1 Head of Government

Romania has a semi-presidential system where the President holds constitutional authority over defense and foreign policy and chairs the Supreme Council of National Defense (CSAT), while the Prime Minister leads the government and directs domestic and economic policy. Both must be monitored as P1 sources.

#### 1.1a Președinția României (Presidential Administration)

| Field | Detail |
|---|---|
| **Institution** | Președinția României (Presidential Administration) |
| **Domain** | `presidency.ro` |
| **Entry Point URL** | `https://www.presidency.ro/ro/media/comunicate-de-presa` (Romanian) / `https://www.presidency.ro/en/media/press-releases` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — check for `/feed/` or `/rss` endpoint] |
| **Language** | Romanian (primary); English (parallel translations of major statements) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Presidential statements, CSAT meeting communiqués, summit readouts, messages on national occasions. |
| **Content Format** | HTML. Press releases are full-text articles. Photos and video embeds accompany major events. |
| **Extraction Method** | HTML scraping of the press releases listing page. Pagination via URL parameters. Separate Romanian and English listing pages. |
| **Editorial Orientation** | Official presidential position. Under President Nicusor Dan (since May 2025), communications emphasize rule of law, Euro-Atlantic alignment, support for Ukraine, and institutional reform. Dan ran as an independent with USR support — positioning is pro-EU, pro-NATO, technocratic-reformist. |
| **Why This Source** | The Romanian president holds constitutional authority over defense and foreign policy and chairs CSAT. Presidential communiques on CSAT decisions, foreign summit participation, and bilateral meetings with heads of state are primary signals of strategic posture. CSAT decisions on defense procurement, intelligence assessments, and national security strategy are published exclusively through the presidential press office. |
| **Access Notes** | Open access. English translations cover major statements with slight delay. The site has returned 503 errors intermittently — implement retry logic. No bot protection observed under normal conditions. |

**Additional entry points:**
- CSAT decisions: published as presidential press releases tagged with CSAT reference, at the same press release URL
- Presidential messages: `https://www.presidency.ro/en/media/messages`
- Speeches: `https://www.presidency.ro/en/media/speeches`
- CSAT secretariat page: `https://www.presidency.ro/en/presidential-administration/departments/department-of-national-security/the-supreme-council-of-national-defence-secretariat`

---

#### 1.1b Guvernul României (Government of Romania / Prime Minister)

| Field | Detail |
|---|---|
| **Institution** | Guvernul României (Government of Romania) |
| **Domain** | `gov.ro` |
| **Entry Point URL** | `https://gov.ro/ro/media/comunicate` (Romanian) / `https://gov.ro/en/media/press-releases` (English) |
| **RSS/Atom Feed** | **Yes.** `https://gov.ro/en/rss` (English) / `https://gov.ro/ro/rss` (Romanian). Confirmed functional — delivers recent press releases and news items. |
| **Language** | Romanian (primary); English (major items translated) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Daily. Press releases cover Cabinet meetings (typically weekly), Prime Ministerial bilateral meetings, government ordinances, and policy announcements. |
| **Content Format** | HTML. Press releases with embedded images. Filterable by month/year. |
| **Extraction Method** | **RSS feed preferred** for new item detection. HTML scraping of listing page as fallback. Items paginated with month/year filters. |
| **Editorial Orientation** | Official government position. Under PM Ilie Bolojan (PNL, since June 2025), communications emphasize fiscal discipline, administrative reform, EU funds absorption, and Euro-Atlantic commitment. Coalition dynamics (PNL-PSD-USR-UDMR) introduce occasional framing tensions. |
| **Why This Source** | The authoritative source for government decisions (hotarari de guvern), emergency ordinances (ordonante de urgenta), Prime Ministerial statements, and Cabinet meeting outcomes. Government ordinances — particularly emergency ordinances — are the primary legislative vehicle for policy implementation in Romania and often precede parliamentary debate. |
| **Access Notes** | Open access. RSS feed functional. English section covers major items. The `gov.ro` portal also links to all ministry websites via `https://www.gov.ro/en/government/organization/ministries`. |

**Additional entry points:**
- News section (broader than press releases): `https://gov.ro/en/news`
- Prime Minister page: `https://gov.ro/en/prime-minister/`
- Government decisions: published simultaneously in Monitorul Oficial (see section 1.5)

---

### 1.2 Foreign Ministry — Ministerul Afacerilor Externe (MAE)

| Field | Detail |
|---|---|
| **Institution** | Ministerul Afacerilor Externe (MAE) |
| **Domain** | `mae.ro` |
| **Entry Point URL** | `https://www.mae.ro/en/taxonomy/term/952` (English press releases) / `https://www.mae.ro/taxonomy/term/148` (Romanian) |
| **RSS/Atom Feed** | Available via the Press Room section. [VERIFY RSS — the MAE Press Room page references RSS but the specific feed URL needs confirmation; check `https://www.mae.ro/rss` or `https://www.mae.ro/rss.xml`] |
| **Language** | Romanian (primary); English (parallel section for major diplomatic activity) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Comunicats issued for bilateral meetings, multilateral positioning (EU Council, NATO summits, OSCE, UN), consular affairs, and diaspora policy. |
| **Content Format** | HTML. Press releases are structured text with occasional PDF attachments for treaties or formal diplomatic notes. |
| **Extraction Method** | HTML scraping of taxonomy listing page. Items appear as titled links with date stamps. The MAE site runs on Drupal — taxonomy term pages are paginated. |
| **Editorial Orientation** | Official foreign ministry position. Under Minister Oana Toiu (USR, since June 2025), communications reflect strong Euro-Atlantic alignment, support for Ukraine and Moldova, OECD accession advocacy, and emphasis on Romania's NATO Eastern Flank role. |
| **Why This Source** | The only primary source for Romania's formal diplomatic positions, bilateral meeting readouts, treaty actions, ambassador credentials, and multilateral engagement. Critical for tracking Romania's posture toward Moldova/Ukraine, Black Sea cooperation, Schengen full accession, OECD membership process, and EU Council positioning. |
| **Access Notes** | Open access. The MAE site has returned 503 errors during high-traffic periods. The English section covers major diplomatic activity but with variable completeness. Drupal-based CMS — URL patterns follow `/en/node/{id}` structure. |

**Additional entry points:**
- MAE Actuality (broader news): `https://www.mae.ro/en/actuality`
- Romanian diplomatic missions portal: `https://www.mae.ro/en/romanian-missions`
- EU Permanent Representation: `https://ue.mae.ro/en` (see section 1.10a)
- NATO Permanent Delegation: `https://nato.mae.ro/en` (see section 1.10b)

---

### 1.3 Defense Ministry — Ministerul Apararii Nationale (MApN)

| Field | Detail |
|---|---|
| **Institution** | Ministerul Apararii Nationale (MApN) |
| **Domain** | `mapn.ro` / `english.mapn.ro` |
| **Entry Point URL** | `https://english.mapn.ro/cpresa/` (English press releases archive) / `https://www.mapn.ro/cpresa/` (Romanian) |
| **RSS/Atom Feed** | None available. No RSS feed identified on either the Romanian or English-language sites. |
| **Language** | Romanian (primary); English (parallel press release archive with generally complete coverage) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Press releases cover NATO exercises, bilateral military cooperation, defense procurement contracts, airspace incident reports (radar detections of cross-border aerial objects from the Ukraine conflict zone), ministerial meetings, and military ceremonies. |
| **Content Format** | HTML. Structured press release archive with individual article pages. Some releases include photos. |
| **Extraction Method** | HTML scraping of the `/cpresa/` listing page. Individual press releases follow the URL pattern `https://english.mapn.ro/cpresa/{id}_{slug}`. No pagination controls identified — archive appears chronological with scroll-loading or single-page listing. |
| **Editorial Orientation** | Official military communication. Publications are factual but selective — operational details are carefully controlled. Under Minister Radu Miruta (PNL, since December 2025), communications emphasize NATO interoperability, defense modernization, and Romania's Eastern Flank responsibilities. |
| **Why This Source** | Direct source for defense procurement decisions, NATO exercise participation (Steadfast Defender, Sea Shield, etc.), bilateral military cooperation agreements, and — critically — airspace incident communiques related to the Ukraine conflict (radar detections of aerial objects near Tulcea County/Danube Delta). These radar-detection releases are unique to MApN and are not published elsewhere first. |
| **Access Notes** | Open access. No bot protection observed. The English-language site (`english.mapn.ro`) maintains a parallel press archive with generally complete translations. The Press Office can be reached at presamapn@mapn.ro. Separate from the main `mapn.ro` domain, the English site appears to be a static site rather than a CMS — updates may lag behind the Romanian version. |

**Additional entry points:**
- Press Office information page: `https://english.mapn.ro/press/index.php`
- Romanian Armed Forces General Staff: communications published through MApN press office, not separately
- Air Force radar detection communiques: published as standard press releases in the `/cpresa/` archive

---

### 1.4 Parliament — Parlamentul Romaniei

Romania has a bicameral parliament: the Camera Deputatilor (Chamber of Deputies) and the Senatul Romaniei (Senate). Both chambers maintain independent websites.

#### 1.4a Camera Deputatilor (Chamber of Deputies)

| Field | Detail |
|---|---|
| **Institution** | Camera Deputatilor (Chamber of Deputies) |
| **Domain** | `cdep.ro` |
| **Entry Point URL** | `https://www.cdep.ro/pls/dic/site.home?idl=2` (English home) / `https://www.cdep.ro/` (Romanian) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — Oracle PL/SQL-based site unlikely to have native RSS] |
| **Language** | Romanian (primary); English (structural/institutional pages, limited current content) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Economic & technological statecraft, Institutional engagement |
| **Publication Frequency** | Daily during session periods (February-June, September-December). Reduced during recess. |
| **Content Format** | HTML. The site runs on Oracle PL/SQL — URLs follow `cdep.ro/pls/{schema}/{procedure}` patterns. Stenographic records (stenograme), legislative proposals (proiecte de lege), and voting records are all accessible but through different entry points. |
| **Extraction Method** | HTML scraping. Complex site architecture with multiple PL/SQL-generated pages. Stenographic records and committee proceedings require navigating through date-based indices. |
| **Editorial Orientation** | Institutional. Publications reflect parliamentary proceedings without editorial framing. Majority coalition (PNL-PSD-USR-UDMR) controls agenda. |
| **Why This Source** | Budget approval (including defense budget), ratification of international agreements, enabling legislation for government policy, and committee hearings on foreign/security matters originate here. The Foreign Affairs Committee and Defense Committee proceedings contain testimony from MAE and MApN officials that is not available through any other channel. Stenographic records provide unfiltered records of parliamentary debate. |
| **Access Notes** | No paywall. The Oracle PL/SQL-based architecture is dated and can be slow. Press office contact: presa@cdep.ro. The English section is limited to institutional/structural information — current proceedings are Romanian-only. |

**Additional entry points:**
- Stenographic records: `https://www.cdep.ro/pls/steno/steno.home?idl=2`
- Legislative proposals: `https://www.cdep.ro/pls/proiecte/upl_pck.home?idl=2`
- Committee pages: `https://www.cdep.ro/pls/parlam/structura.co?idl=2`
- Voting records: `https://www.cdep.ro/pls/steno/eVot1.Home?idl=2`

#### 1.4b Senatul Romaniei (Senate)

| Field | Detail |
|---|---|
| **Institution** | Senatul Romaniei (Senate) |
| **Domain** | `senat.ro` |
| **Entry Point URL** | `https://www.senat.ro/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Romanian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods. Senate press releases cover Biroul Permanent (Permanent Bureau) decisions, plenary session agendas, and committee proceedings. |
| **Content Format** | HTML. ASP.NET-based site with structured committee and session pages. |
| **Extraction Method** | HTML scraping. Different infrastructure from Chamber of Deputies (ASP.NET vs. Oracle PL/SQL). |
| **Editorial Orientation** | Institutional. Senate President currently holds significant political weight as coalition dynamics shape legislative agenda. |
| **Why This Source** | The Senate has co-equal legislative authority with the Chamber of Deputies. Treaty ratifications, constitutional amendments, and organic laws on defense/intelligence require Senate approval. Senate committee hearings on national security (Comisia pentru aparare, ordine publica si siguranta nationala) provide oversight of SRI and SIE. |
| **Access Notes** | No paywall. Site is ASP.NET-based and can be slow. Press office: presa@senat.ro. No English-language section — Romanian only. The Biroul Permanent (Permanent Bureau) page at `https://www.senat.ro/pagini/bp/bp.htm` provides leadership and agenda information. |

**Additional entry points:**
- Biroul Permanent: `https://www.senat.ro/pagini/bp/bp.htm`
- Senate committees: accessible through the main senat.ro navigation
- Legislative proposals: integrated into session/agenda pages

---

### 1.5 Official Gazette — Monitorul Oficial al Romaniei

| Field | Detail |
|---|---|
| **Institution** | Monitorul Oficial al Romaniei (Official Gazette of Romania) |
| **Domain** | `monitoruloficial.ro` |
| **Entry Point URL** | `https://monitoruloficial.ro/` (main portal) |
| **RSS/Atom Feed** | None available. |
| **Language** | Romanian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Monitorul Oficial is the constitutional publication vehicle for all laws, government ordinances, presidential decrees, and normative acts |
| **Publication Frequency** | Daily (Part I — laws, ordinances, decrees, decisions). Part I is the strategically relevant section. Parts II-VII cover other categories (international treaties in Part II). |
| **Content Format** | PDF. Individual acts are published as pages within daily gazette editions. The e-Monitor provides electronic access. |
| **Extraction Method** | The e-Monitor online application (`https://monitoruloficial.ro/en/produs/e-monitor-on-line-gratuit/`) provides free access to current editions. PDF download and text extraction required. Historical archive access may require subscription. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, government ordinance, presidential decree, or international treaty ratification is legally binding until published in the Monitorul Oficial Part I. This is the definitive, timestamped legal record. Defense procurement authorizations, intelligence service organizational changes, international agreement ratifications, and fiscal legislation all appear here. Media reports on legislation are always downstream of Monitorul Oficial publication. |
| **Access Notes** | The e-Monitor free online version provides access to current editions on the day of publication. Full archive access and advanced search require subscription. The publishing house (Regia Autonoma Monitorul Oficial) operates at Str. Parcului 65, Sector 1, Bucharest. No bot protection observed on the main portal. |

**Additional entry points:**
- Free e-Monitor: `https://monitoruloficial.ro/en/produs/e-monitor-on-line-gratuit/`
- EU Forum of Official Gazettes (Romania entry): `https://op.europa.eu/en/web/forum/romania-oj`
- Expert Monitor (commercial legal database): `http://www.expert-monitor.ro/`

---

### 1.6 Finance Ministry — Ministerul Finantelor (MF)

| Field | Detail |
|---|---|
| **Institution** | Ministerul Finantelor (Ministry of Finance) |
| **Domain** | `mfinante.gov.ro` |
| **Entry Point URL** | `https://mfinante.gov.ro/ro/acasa` (Romanian home — press releases accessible through news/communication sections) / `https://mfinante.gov.ro/en/` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Romanian (primary); English (select major publications, investor presentations) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Communications cover budget execution reports, fiscal policy announcements, government securities issuance, emergency ordinances on fiscal matters, EU funds absorption data, and tax legislation changes. |
| **Content Format** | HTML for press releases. PDF for budget execution reports, investor presentations, and statistical data. The Trezor (Treasury) subsection at `mfinante.gov.ro/web/trezor` provides structured bond issuance data. |
| **Extraction Method** | HTML scraping of news/communication pages. PDF download for statistical reports. The site uses Liferay CMS — URL patterns follow Liferay conventions. |
| **Editorial Orientation** | Official fiscal policy position. Under Minister Marcel Bolos (PNL), communications emphasize fiscal consolidation, EU funds absorption, and compliance with EU fiscal rules (Excessive Deficit Procedure). Romania's fiscal deficit (~7.65% of GDP in 2025) makes MF communications particularly significant for tracking compliance commitments. |
| **Why This Source** | Primary source for budget execution data, fiscal policy announcements, government borrowing (domestic and international bond issuances), tax legislation, and EU funds absorption reporting. Romania's ongoing Excessive Deficit Procedure with the EU makes MF fiscal data a structural constraint on defense spending and strategic investment capacity. |
| **Access Notes** | Open access for most content. Liferay-based CMS. The English section provides investor presentations and select macro-fiscal publications. Government securities data at `https://mfinante.gov.ro/en/web/trezor`. The National Agency for Fiscal Administration (ANAF) operates separately at `anaf.ro`. |

**Additional entry points:**
- Treasury / government securities: `https://mfinante.gov.ro/en/web/trezor`
- Primary market issuance announcements: `https://mfinante.gov.ro/en/web/trezor/piata-primara/anunturi-emisiuni`
- Budget execution data: published as PDF reports accessible through the main site

---

### 1.7 Central Bank — Banca Nationala a Romaniei (BNR)

| Field | Detail |
|---|---|
| **Institution** | Banca Nationala a Romaniei (BNR) |
| **Domain** | `bnr.ro` |
| **Entry Point URL** | `https://www.bnr.ro/Press-releases-4957.aspx` (English press releases) / `https://www.bnr.ro/Comunicate-de-presa-4954.aspx` (Romanian) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS hub: `https://www.bnr.ro/RSS-Feeds-4129.aspx` (English) / `https://www.bnr.ro/Fluxuri-RSS-905.aspx` (Romanian). Available feeds include: Publications, Research News, Mass Media News, Public News, BNR News, and Press Releases (Comunicate de presa). Exchange rate XML feed: `https://www.bnr.ro/nbrfxrates.xml` (daily) / `https://www.bnr.ro/nbrfxrates10days.xml` (10-day history). |
| **Language** | Romanian (primary); English (comprehensive parallel site for major publications and press releases) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (Board meetings on published schedule). Press releases: several per week covering monetary policy, financial stability, reserves, banking supervision, payment systems. Exchange rate data: daily. |
| **Content Format** | HTML for press releases. **PDF** for monetary policy decisions, minutes, inflation reports, financial stability reports, and annual reports. **XML** for exchange rate data feeds. |
| **Extraction Method** | **RSS feeds for press release monitoring** (best approach). XML endpoint for exchange rate data (structured, machine-readable). PDF download and extraction for major publications. The BNR website is well-structured ASP.NET — stable URL patterns. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and institutionally conservative. BNR has maintained a hawkish stance relative to regional peers — the policy rate was held at 6.5% through early 2026. Governor Mugur Isarescu (in post since 1990, the world's longest-serving central bank governor) provides institutional continuity. |
| **Why This Source** | BNR is the authoritative source for monetary policy decisions, inflation expectations, official economic indicators, exchange rate data, international reserves, financial stability assessments, and banking sector supervision. Its RSS feeds and XML endpoints make it the most machine-friendly government source in Romania. Monetary policy decisions and inflation reports directly shape fiscal space for defense spending and economic statecraft. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained. The English-language site at `bnr.ro/en` provides comprehensive parallel coverage. Exchange rate XML feeds are freely accessible and stable. Email subscription also available. The BNR Direct mobile app mirrors website content. |

**Key data endpoints:**
| Feed | URL |
|---|---|
| Daily exchange rates (XML) | `https://www.bnr.ro/nbrfxrates.xml` |
| 10-day exchange rate history (XML) | `https://www.bnr.ro/nbrfxrates10days.xml` |
| RSS feeds hub (English) | `https://www.bnr.ro/RSS-Feeds-4129.aspx` |
| RSS feeds hub (Romanian) | `https://www.bnr.ro/Fluxuri-RSS-905.aspx` |
| Press releases (English) | `https://www.bnr.ro/Press-releases-4957.aspx` |
| Monetary policy decisions | `https://www.bnr.ro/Monetary-policy-decisions-5765.aspx` |
| Inflation reports | `https://www.bnr.ro/Inflation-Reports-3553.aspx` |

---

### 1.8 Trade / Economy — Ministerul Economiei, Antreprenoriatului si Turismului

| Field | Detail |
|---|---|
| **Institution** | Ministerul Economiei, Antreprenoriatului si Turismului (Ministry of Economy, Entrepreneurship and Tourism) |
| **Domain** | `economie.gov.ro` |
| **Entry Point URL** | `http://www.economie.gov.ro/` [VERIFY URL — site has shown Cloudflare-style "Verifying your browser" challenges] |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Romanian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-4 per week. Communications cover industrial policy, trade agreements, foreign direct investment, tourism policy, state aid schemes, and SME support programs. |
| **Content Format** | HTML. Press releases (comunicat de presa) section. Some attached PDFs for normative acts and strategy documents. |
| **Extraction Method** | HTML scraping. The site has shown browser verification challenges (Cloudflare or similar) — headless browser rendering may be required. |
| **Editorial Orientation** | Official economic policy position. Communications reflect government industrial strategy, EU single market positioning, and trade policy. |
| **Why This Source** | Primary source for trade policy, industrial strategy, FDI attraction, state enterprise oversight, and economic dimensions of EU institutional engagement. Romania's growing role in European supply chain diversification (semiconductors, critical minerals, defense industry) makes Ministry of Economy communications increasingly relevant to economic statecraft analysis. |
| **Access Notes** | The `economie.gov.ro` site has intermittently returned browser verification pages, suggesting bot protection. No English-language section identified. A related portal at `imm.gov.ro` covers SME policy with a press releases section at `http://www.imm.gov.ro/en/mmaca/press-releases/`. |

**Additional entry points:**
- SME policy portal: `http://www.imm.gov.ro/`
- State aid and competition: accessible through the main Ministry of Economy site
- Trade data: Romania's trade statistics are primarily published by the National Institute of Statistics (INS) at `insse.ro`

---

### 1.9 Intelligence / National Security — SRI, SIE, CSAT

Romania's intelligence and national security architecture comprises three key bodies: the Romanian Intelligence Service (SRI — domestic), the Foreign Intelligence Service (SIE — external), and the Supreme Council of National Defense (CSAT — strategic coordination, chaired by the President). Unlike Mexico's CNI, Romania's intelligence services maintain moderately active public communication profiles — SRI in particular has adopted a transparency posture in recent years, publishing annual activity reports and issuing press releases on hybrid/cyber threats.

#### 1.9a Serviciul Roman de Informatii (SRI — Romanian Intelligence Service)

| Field | Detail |
|---|---|
| **Institution** | Serviciul Roman de Informatii (SRI) |
| **Domain** | `sri.ro` |
| **Entry Point URL** | `https://www.sri.ro/articole/` (press releases/articles) / `https://www.sri.ro/en` (English home) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Romanian (primary); English (select pages, institutional overview) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Irregular — 2-6 per month. Press releases issued for annual activity reports presented to Parliament, statements on disinformation campaigns, cyber threat advisories, and institutional events. Frequency increases during periods of heightened security concern (e.g., drone intrusions, election interference). |
| **Content Format** | HTML. Annual activity reports in PDF. |
| **Extraction Method** | HTML scraping of articles page. Low-volume source — periodic polling sufficient. |
| **Editorial Orientation** | Institutional security communication. SRI has adopted a proactive transparency posture under recent leadership, particularly on hybrid threats, disinformation, and cyber security. Communications are calibrated to support public awareness without revealing operational details. |
| **Why This Source** | SRI is Romania's primary domestic intelligence service and the lead agency for counterintelligence, counter-terrorism, and countering hybrid threats. Its public communications on Russian information operations targeting Romania and Moldova, cyber threats to critical infrastructure, and election security are unique signals unavailable from any other source. Annual reports presented to Parliament provide the most comprehensive unclassified assessment of Romania's threat environment. |
| **Access Notes** | Open access. Low publication volume. The English section is limited to institutional overview pages. Annual activity reports (rapoarte de activitate) are the highest-value publications — typically released in Q1 for the previous year. |

#### 1.9b Serviciul de Informatii Externe (SIE — Foreign Intelligence Service)

| Field | Detail |
|---|---|
| **Institution** | Serviciul de Informatii Externe (SIE) |
| **Domain** | `sie.ro` |
| **Entry Point URL** | `https://www.sie.ro/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Romanian (primary); English (institutional pages) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Minimal — 1-3 per month at most. SIE issues press releases only for specific denials, clarifications (e.g., the May 2025 denial regarding alleged French intelligence visits), leadership appointments, and annual activity reports. |
| **Content Format** | HTML. Minimal web presence. |
| **Extraction Method** | Periodic check of the SIE website. Low-volume — weekly polling sufficient. |
| **Editorial Orientation** | Institutional. SIE is considerably more opaque than SRI. Public communications are rare and typically reactive (denying media reports or countering disinformation about SIE activities). |
| **Why This Source** | Included for completeness and anomaly detection. SIE's near-silence makes any publication a notable signal. Annual activity reports to Parliament provide the only unclassified window into Romania's foreign intelligence priorities and threat assessments. Press releases correcting or denying media reporting (as with the May 2025 French intelligence denial) can reveal information about sensitive diplomatic/intelligence relationships. |
| **Access Notes** | The `sie.ro` domain hosts a minimal website. An older version is accessible at `https://www.sie.ro/rcd2011/En/index_e.html`. No bot protection. The real intelligence signal from SIE comes through parliamentary oversight committee proceedings and leaks to investigative media (RISE Project, G4Media) rather than official channels. |

#### 1.9c Consiliul Suprem de Aparare a Tarii (CSAT — Supreme Council of National Defense)

| Field | Detail |
|---|---|
| **Institution** | Consiliul Suprem de Aparare a Tarii (CSAT) |
| **Domain** | Published through `presidency.ro` |
| **Entry Point URL** | CSAT decisions and meeting communiques are published as presidential press releases at `https://www.presidency.ro/en/media/press-releases` |
| **RSS/Atom Feed** | None separate — follows presidency.ro feed (if available). |
| **Language** | Romanian (primary); English (major decisions translated) |
| **Type** | `legislative_official` |
| **Priority** | **P1** (CSAT decisions are among the highest-priority government signals for defense and security posture) |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Irregular — CSAT meets as convened by the President. Typically 6-12 meetings per year, with additional emergency sessions. Each meeting produces a communique published through the Presidency. |
| **Content Format** | HTML press releases on presidency.ro. |
| **Extraction Method** | Captured through presidency.ro monitoring (see section 1.1a). Filter for CSAT-related press releases by keyword matching ("CSAT", "Consiliul Suprem de Aparare", "Supreme Council of National Defence"). |
| **Editorial Orientation** | Official national security position. CSAT decisions are consensus documents — the Council includes the President, PM, defense/interior/foreign ministers, intelligence chiefs, and military leadership. |
| **Why This Source** | CSAT is the constitutional body responsible for organizing and coordinating defense and national security. Its decisions cover: defense procurement authorizations, national security strategy approval, threat assessments, intelligence budget allocation, and responses to security crises (e.g., drone intrusions, election interference). CSAT approved the November 2025 national security threat assessment for 2026 and the Strategic Defense Analysis. These decisions are the single most authoritative signals of Romania's strategic posture. |
| **Access Notes** | Not a separate website — CSAT secretariat operates within the Presidential Administration. Communiques are published as presidential press releases. The CSAT secretariat page at `https://www.presidency.ro/en/presidential-administration/departments/department-of-national-security/the-supreme-council-of-national-defence-secretariat` provides institutional background. Parliament reviews CSAT activity annually. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Reprezentanta Permanenta a Romaniei pe langa Uniunea Europeana (EU Permanent Representation)

| Field | Detail |
|---|---|
| **Institution** | Reprezentanta Permanenta a Romaniei pe langa UE |
| **Domain** | `ue.mae.ro` |
| **Entry Point URL** | `https://ue.mae.ro/en` (English home) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — Drupal-based site may have `/feed`] |
| **Language** | Romanian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | 2-5 per week. Press releases cover ministerial participation in EU Council meetings, COREPER deliberations, bilateral meetings in Brussels, and Romania's EU policy positions. |
| **Content Format** | HTML. Drupal-based (MAE subdomain). |
| **Extraction Method** | HTML scraping. Same Drupal infrastructure as main MAE site. |
| **Editorial Orientation** | Official EU engagement position. Reflects Romania's priorities in EU Council negotiations. |
| **Why This Source** | Romania's EU Permanent Representation is the front line for tracking Romania's positioning in EU Council votes, Common Foreign and Security Policy decisions, Schengen implementation, EU enlargement (Moldova), and EU fiscal governance. The Permanent Representative (Ambassador Iulia Matei) participates in COREPER II — communications from this office reveal Romania's negotiating positions before they appear in media. |
| **Access Notes** | Open access. Subdomain of MAE (ue.mae.ro). Press Room section contains press releases and transparency reporting on meetings with interest representatives. English content generally available. |

#### 1.10b Delegatia Permanenta a Romaniei la NATO (NATO Permanent Delegation)

| Field | Detail |
|---|---|
| **Institution** | Delegatia Permanenta a Romaniei la NATO |
| **Domain** | `nato.mae.ro` |
| **Entry Point URL** | `https://nato.mae.ro/en` (English home) / `https://nato.mae.ro/en/local-news` (news/press releases) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Romanian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Low — 1-3 per month. Publications cover NATO summit participation, public diplomacy events, and bilateral meetings at NATO HQ. |
| **Content Format** | HTML. Drupal-based (MAE subdomain). |
| **Extraction Method** | HTML scraping. Low-volume source — weekly polling sufficient. |
| **Editorial Orientation** | Official NATO engagement position. Emphasizes Romania's contributions to Allied defense, Eastern Flank posture, and NATO-EU cooperation. |
| **Why This Source** | Provides direct insight into Romania's NATO positioning — burden-sharing commitments (Romania met the 2% GDP defense spending target), contributions to NATO force structure (MND SE HQ, NFIU, multinational brigade), and Romania's advocacy within NATO decision-making. Ambassador Sebastian Danul Neculaescu represents Romania at the North Atlantic Council. |
| **Access Notes** | Open access. Subdomain of MAE (nato.mae.ro). Low publication frequency but high signal value when content appears. |

#### 1.10c BSEC (Organization of the Black Sea Economic Cooperation)

| Field | Detail |
|---|---|
| **Institution** | Organization of the Black Sea Economic Cooperation (BSEC) |
| **Domain** | `bsec-organization.org` |
| **Entry Point URL** | `https://www.bsec-organization.org/press-releases` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Low — 2-4 per month. Press releases cover ministerial meetings, working group sessions, and institutional developments. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of press releases page. Low-volume source. |
| **Editorial Orientation** | Multilateral institutional communication. BSEC is headquartered in Istanbul and includes 12 member states (Albania, Armenia, Azerbaijan, Bulgaria, Georgia, Greece, Moldova, Romania, Russia, Serbia, Turkey, Ukraine). |
| **Why This Source** | BSEC is the primary multilateral format for Black Sea regional cooperation. Romania was a founding member (1992). Tracking BSEC communications reveals the state of regional cooperation mechanisms — particularly salient given the Ukraine conflict's impact on Black Sea security and the suspension of Russia's meaningful participation. The existing Source Intelligence Map identifies Black Sea regional security analysis as a structural coverage gap — BSEC provides one of the few institutional windows into this space. |
| **Access Notes** | Open access. English-language site. The Parliamentary Assembly of the BSEC (PABSEC) operates separately at `pabsec.org`. |

#### 1.10d AGERPRES (National News Agency)

| Field | Detail |
|---|---|
| **Institution** | AGERPRES — Agentia Nationala de Presa |
| **Domain** | `agerpres.ro` |
| **Entry Point URL** | `https://www.agerpres.ro/english` (English) / `https://www.agerpres.ro/` (Romanian) |
| **RSS/Atom Feed** | Available. [VERIFY specific RSS URLs — check `https://www.agerpres.ro/rss` or `/feed`] |
| **Language** | Romanian (primary); English (select major items with slight delay) |
| **Type** | `government_aligned` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains — AGERPRES is the first-mover on all official communiques |
| **Publication Frequency** | Continuous — dozens of items daily. AGERPRES operates as a wire service, publishing presidential statements, MFA readouts, defense ministry announcements, parliamentary proceedings, and economic data releases in near-real-time. |
| **Content Format** | HTML. Wire-service format articles with datelines. |
| **Extraction Method** | RSS feed preferred (if available). HTML scraping of the English-language section as fallback. High publication volume requires robust filtering/deduplication. |
| **Editorial Orientation** | Official/neutral wire service. Reflects government-released positions verbatim. AGERPRES is a public institution subordinated to the Romanian Parliament — not an independent news outlet. It functions as the primary distribution mechanism for all government communications. |
| **Why This Source** | AGERPRES is the single most important aggregation point for Romanian government communications. It publishes the full text of presidential statements, CSAT communiques, MFA readouts, MApN press releases, and government decisions — often before or simultaneously with publication on the originating institution's website. For pipeline purposes, monitoring AGERPRES provides a unified stream of government communications that would otherwise require polling 10+ separate websites. |
| **Access Notes** | Open access. English feed covers major items. The existing Source Intelligence Map (Layer 1) already includes AGERPRES as Source #1 — this entry in Layer 2 reflects its dual role as both a media outlet and a government communications aggregator. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Independent Infra |
|---|---|---|---|---|---|---|---|
| 1a | Presidency (Nicusor Dan) | `presidency.ro/en/media/press-releases` | [VERIFY] | P1 | HTML | Daily | Yes |
| 1b | Government / PM (Bolojan) | `gov.ro/en/media/press-releases` | **Yes** (`gov.ro/en/rss`) | P1 | HTML | Daily | Yes |
| 2 | MAE (Foreign Affairs) | `mae.ro/en/taxonomy/term/952` | [VERIFY] | P1 | HTML | Daily | Yes |
| 3 | MApN (Defense) | `english.mapn.ro/cpresa/` | No | P1 | HTML | 3-7/week | Yes |
| 4a | Camera Deputatilor | `cdep.ro` | [VERIFY] | P2 | HTML | Daily (session) | Yes |
| 4b | Senatul Romaniei | `senat.ro` | [VERIFY] | P2 | HTML | Daily (session) | Yes |
| 5 | Monitorul Oficial | `monitoruloficial.ro` | No | P2 | PDF | Daily | Yes |
| 6 | Min. Finance (MF) | `mfinante.gov.ro` | [VERIFY] | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | BNR (Central Bank) | `bnr.ro/Press-releases-4957.aspx` | **Yes** (multiple) | P2 | PDF/HTML/XML | Variable | Yes |
| 8 | Min. Economy | `economie.gov.ro` | [VERIFY] | P2 | HTML | 2-4/week | Yes |
| 9a | SRI (Domestic Intel) | `sri.ro/articole/` | [VERIFY] | P2 | HTML/PDF | Irregular | Yes |
| 9b | SIE (Foreign Intel) | `sie.ro` | No | P2 | HTML | Minimal | Yes |
| 9c | CSAT | Via `presidency.ro` | Via Presidency | P1 | HTML | Per meeting | Via Presidency |
| 10a | EU Perm Rep | `ue.mae.ro/en` | [VERIFY] | P2 | HTML | 2-5/week | MAE subdomain |
| 10b | NATO Delegation | `nato.mae.ro/en` | [VERIFY] | P2 | HTML | 1-3/month | MAE subdomain |
| 10c | BSEC | `bsec-organization.org/press-releases` | [VERIFY] | P2 | HTML | 2-4/month | Yes |
| 10d | AGERPRES | `agerpres.ro/english` | [VERIFY] | P1 | HTML | Continuous | Yes |

---

## 3. MONITORING CONFIGURATION

```yaml
# Romania Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/ro.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: ro_presidency
    name: Președinția României (Presidential Administration)
    domain: presidency.ro
    entry_url: "https://www.presidency.ro/ro/media/comunicate-de-presa"
    entry_url_en: "https://www.presidency.ro/en/media/press-releases"
    rss_feed: null  # [VERIFY]
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: >
      CSAT decisions published here. President holds constitutional authority over
      defense and foreign policy. English translations available for major statements.
      Site has returned 503 errors intermittently — implement retry logic.

  - id: ro_government
    name: Guvernul României (Government / PM)
    domain: gov.ro
    entry_url: "https://gov.ro/ro/media/comunicate"
    entry_url_en: "https://gov.ro/en/media/press-releases"
    rss_feed:
      ro: "https://gov.ro/ro/rss"
      en: "https://gov.ro/en/rss"
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: >
      RSS feed confirmed functional. Government ordinances (OUG) published here
      before Monitorul Oficial. PM Bolojan (PNL) coalition with PSD-USR-UDMR.

  - id: ro_mae
    name: Ministerul Afacerilor Externe (MAE)
    domain: mae.ro
    entry_url: "https://www.mae.ro/taxonomy/term/148"
    entry_url_en: "https://www.mae.ro/en/taxonomy/term/952"
    rss_feed: null  # [VERIFY — check mae.ro/rss or Press Room section]
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: >
      Drupal-based CMS. 503 errors observed during high traffic. Minister Oana Toiu (USR).
      Embassy/mission-level communications via mae.ro subdomain system.

  - id: ro_mapn
    name: Ministerul Apararii Nationale (MApN)
    domain: mapn.ro
    entry_url: "https://www.mapn.ro/cpresa/"
    entry_url_en: "https://english.mapn.ro/cpresa/"
    rss_feed: null
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: >
      No RSS. English archive at english.mapn.ro generally complete. Radar detection
      communiques for cross-border aerial objects are high-priority items. Minister
      Radu Miruta (PNL, since Dec 2025).

  - id: ro_agerpres
    name: AGERPRES (National News Agency)
    domain: agerpres.ro
    entry_url: "https://www.agerpres.ro/"
    entry_url_en: "https://www.agerpres.ro/english"
    rss_feed: null  # [VERIFY — check agerpres.ro/rss]
    language: ro
    language_secondary: en
    type: government_aligned
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: continuous
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 2
    notes: >
      Unified government communications aggregator. High volume — requires keyword
      filtering. Subordinated to Parliament. First-mover on all official communiques.

  - id: ro_csat
    name: CSAT (Supreme Council of National Defense)
    domain: presidency.ro
    entry_url: "https://www.presidency.ro/en/media/press-releases"
    rss_feed: null
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "6-12_per_year"
    content_format: html
    extraction_method: keyword_filter_on_presidency
    poll_interval_hours: 2  # inherits from presidency polling
    notes: >
      Not a separate website — CSAT communiques published via presidency.ro.
      Filter by keywords: CSAT, Consiliul Suprem, Supreme Council. Every publication
      is high-priority. Defense procurement, threat assessments, national security
      strategy decisions.

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: ro_cdep
    name: Camera Deputatilor (Chamber of Deputies)
    domain: cdep.ro
    entry_url: "https://www.cdep.ro/pls/dic/site.home?idl=2"
    rss_feed: null  # [VERIFY]
    language: ro
    language_secondary: en  # limited
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - economic_technological_statecraft
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Oracle PL/SQL-based site. Complex URL structure. Stenographic records at
      cdep.ro/pls/steno/. Foreign Affairs and Defense committee proceedings
      contain unique intelligence. English section limited.

  - id: ro_senat
    name: Senatul Romaniei (Senate)
    domain: senat.ro
    entry_url: "https://www.senat.ro/"
    rss_feed: null  # [VERIFY]
    language: ro
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
    notes: >
      ASP.NET-based site. Romanian only. Treaty ratifications and intelligence
      oversight committee proceedings are high-value items.

  - id: ro_monitorul_oficial
    name: Monitorul Oficial al Romaniei
    domain: monitoruloficial.ro
    entry_url: "https://monitoruloficial.ro/"
    rss_feed: null
    language: ro
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
    notes: >
      Constitutional publication requirement — no law is binding until published here.
      Part I (laws, ordinances, decrees) is strategically relevant. Part II covers
      international treaties. Free e-Monitor for current editions; archive requires subscription.

  - id: ro_mfinante
    name: Ministerul Finantelor (Ministry of Finance)
    domain: mfinante.gov.ro
    entry_url: "https://mfinante.gov.ro/ro/acasa"
    entry_url_en: "https://mfinante.gov.ro/en/"
    rss_feed: null  # [VERIFY]
    language: ro
    language_secondary: en  # select publications
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Liferay CMS. Budget execution data, fiscal policy, bond issuances. Treasury
      data at mfinante.gov.ro/web/trezor. Romania's fiscal deficit (~7.65% GDP)
      under EU Excessive Deficit Procedure — MF data tracks compliance.

  - id: ro_bnr
    name: Banca Nationala a Romaniei (BNR)
    domain: bnr.ro
    entry_url: "https://www.bnr.ro/Press-releases-4957.aspx"
    entry_url_ro: "https://www.bnr.ro/Comunicate-de-presa-4954.aspx"
    rss_feed:
      hub_en: "https://www.bnr.ro/RSS-Feeds-4129.aspx"
      hub_ro: "https://www.bnr.ro/Fluxuri-RSS-905.aspx"
    xml_feeds:
      exchange_rates_daily: "https://www.bnr.ro/nbrfxrates.xml"
      exchange_rates_10day: "https://www.bnr.ro/nbrfxrates10days.xml"
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_html_xml_mixed
    extraction_method: rss_poll_and_xml_fetch
    poll_interval_hours: 6
    notes: >
      Best machine-readable government source in Romania. RSS for press releases,
      XML for exchange rates. Monetary policy decisions 8x/year. Governor Isarescu
      (since 1990). Policy rate at 6.5% (early 2026). Comprehensive English site.

  - id: ro_min_economy
    name: Ministerul Economiei (Ministry of Economy)
    domain: economie.gov.ro
    entry_url: "http://www.economie.gov.ro/"
    rss_feed: null  # [VERIFY]
    language: ro
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Browser verification challenges (Cloudflare-style) observed. Headless browser
      may be required. No English section. SME portal at imm.gov.ro. Trade statistics
      via National Institute of Statistics (insse.ro).

  - id: ro_sri
    name: Serviciul Roman de Informatii (SRI)
    domain: sri.ro
    entry_url: "https://www.sri.ro/articole/"
    rss_feed: null  # [VERIFY]
    language: ro
    language_secondary: en  # limited
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: irregular
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Low volume but high signal value. Annual activity reports (Q1) are the
      highest-value publications. Hybrid threat and disinformation advisories
      are unique to SRI. Flag any new publication for immediate review.

  - id: ro_sie
    name: Serviciul de Informatii Externe (SIE)
    domain: sie.ro
    entry_url: "https://www.sie.ro/"
    rss_feed: null
    language: ro
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: minimal
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: >
      Near-silent agency. Any publication is a high-priority anomaly. Annual reports
      to Parliament are the only regular output. Real signal comes through
      parliamentary committees and investigative media leaks.

  - id: ro_eu_perm_rep
    name: EU Permanent Representation
    domain: ue.mae.ro
    entry_url: "https://ue.mae.ro/en"
    rss_feed: null  # [VERIFY — Drupal site, check /feed]
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      MAE subdomain (Drupal). Ambassador Iulia Matei at COREPER II. Press Room
      includes transparency reporting on meetings with interest representatives.

  - id: ro_nato_delegation
    name: NATO Permanent Delegation
    domain: nato.mae.ro
    entry_url: "https://nato.mae.ro/en"
    rss_feed: null  # [VERIFY]
    language: ro
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "1-3_per_month"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: >
      MAE subdomain. Low frequency but high signal when published. Ambassador
      Neculaescu at North Atlantic Council. Romania hosts MND SE HQ, NFIU,
      multinational brigade.

  - id: ro_bsec
    name: BSEC (Black Sea Economic Cooperation)
    domain: bsec-organization.org
    entry_url: "https://www.bsec-organization.org/press-releases"
    rss_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "2-4_per_month"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: >
      Multilateral organization (12 member states). Romania founding member.
      HQ in Istanbul. Tracks Black Sea regional cooperation — a structural
      gap identified in the Layer 1 Source Intelligence Map.
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Romanian government communications are generally more structured and less propagandistic than in many peer countries, but they remain systematically optimistic and selective. The pipeline must treat government sources as confirming that an institution has chosen to make a statement — not as confirming the underlying facts. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage and coalition dynamics.

- **Presidency**: Cross-reference CSAT communiques and presidential statements against G4Media (independent political analysis) and Digi24 (mainstream reporting). When the Presidency issues a statement on defense or foreign policy that diverges from the PM's gov.ro communications, it signals a constitutional-institutional tension between the President and the government coalition — a critical posture indicator in Romania's semi-presidential system. Under Nicusor Dan (independent/USR-aligned President) and Ilie Bolojan (PNL PM leading a PNL-PSD-USR-UDMR coalition), such divergences may surface on issues where USR and PSD have opposing positions.

- **Government/PM (gov.ro)**: Triangulate with Digi24, HotNews (centre-liberal), and G4Media. Government ordinances (especially OUG — emergency ordinances) should be verified against their publication in Monitorul Oficial for the definitive text. Media coverage of government decisions frequently adds context on coalition negotiations that the official comunicat omits.

- **MAE**: Diplomatic comunicats should be triangulated with Romania Insider (English-language curation), AGERPRES (verbatim republication with additional context), and Euronews Romania (external perspective). When MAE readouts of bilateral meetings differ in emphasis from the counterpart foreign ministry's readout, it reveals negotiating positions.

- **MApN**: Defense press releases report exercises, procurement, and airspace incidents but typically omit cost details, operational difficulties, and interoperability challenges. Cross-reference with New Strategy Center (security think tank), Recorder (investigative — defense procurement), and RISE Project (defense-sector irregularities). Romania Insider provides English-language curation of MApN releases with additional context.

- **BNR**: Monetary policy communications are technically rigorous and among the most reliable government outputs. Cross-reference with Ziarul Financiar and Profit.ro for market interpretation. BNR's quarterly Inflation Reports provide the most granular analysis of Romania's macroeconomic conditions.

- **MF (Finance)**: Budget execution data is generally reliable in headline numbers but framing (GDP denominator selection, revenue projection methodology) can obscure trends. Romania's fiscal deficit is large enough (~7.65% of GDP in 2025) that MF framing choices have strategic implications for defense spending capacity. Cross-reference with Ziarul Financiar, the European Commission's country reports, and IMF Article IV consultations.

- **SRI/SIE**: Intelligence service communications are rare but high-signal. SRI annual reports to Parliament should be cross-referenced with G4Media and Recorder coverage of the parliamentary hearings. SRI disinformation advisories should be triangulated with EU East StratCom Task Force reporting and independent media verification (G4Media, RISE Project).

**4.2 The decentralization effect**

Unlike Mexico's centralized gob.mx platform, Romania's government sources are fully decentralized — each institution operates independent web infrastructure with different CMS platforms (Drupal for MAE and subdomains, Oracle PL/SQL for Chamber of Deputies, ASP.NET for Senate, Liferay for Ministry of Finance, custom/static for MApN, ASP.NET for BNR). This means:

- No single point of failure: one ministry's downtime does not affect others
- No unified extraction pattern: each source requires a dedicated scraper configuration
- No centralized content control: individual institutions have publication autonomy
- Variable technical quality: BNR (excellent, with RSS/XML) at one end, Ministry of Economy (intermittent access issues) at the other
- AGERPRES serves as a partial aggregation layer, republishing most government communications — but with wire-service condensation that may lose nuance from the original

**4.3 The CSAT signal premium**

CSAT decisions are the single highest-value government signal for Romania's defense and security posture. Unlike regular ministerial communications, CSAT decisions represent consensus among the President, PM, defense/interior/foreign ministers, intelligence chiefs, and Chief of General Staff. The pipeline should apply maximum priority to any presidential press release containing CSAT-related keywords. Key signal types:

- Defense procurement authorizations (e.g., the March 2025 light corvette decision)
- Annual threat assessments and strategic defense analyses (November 2025 session)
- Emergency security responses (e.g., September 2025 drone intrusion session)
- National security strategy approvals
- Intelligence budget and organizational decisions

**4.4 The semi-presidential dynamic**

Romania's constitutional architecture creates a dual-executive signal environment. The President controls defense and foreign policy (and chairs CSAT), while the PM controls the government and domestic/economic policy. When the President and PM are from the same political family, government communications are broadly aligned. In the current configuration (independent President Nicusor Dan + PNL PM Ilie Bolojan leading a broad coalition), the pipeline must track both presidency.ro and gov.ro independently and flag divergences — these reveal institutional or policy-level tensions that affect Romania's strategic posture.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Architecture — Per-Source Scraper Design

Romania's government sources require individual scraper configurations. There is no shared extraction pattern (unlike Mexico's gob.mx). Recommended approach:

- **Group 1 — Drupal-based (MAE ecosystem)**: `mae.ro`, `ue.mae.ro`, `nato.mae.ro`. Share Drupal CMS conventions — taxonomy term pages, `/en/node/{id}` URL patterns. A single Drupal scraper module with domain parameterization can service all three.
- **Group 2 — Standalone sites**: `presidency.ro`, `gov.ro`, `mapn.ro` / `english.mapn.ro`, `sri.ro`, `sie.ro`, `economie.gov.ro`. Each requires a dedicated scraper. Prioritize `gov.ro` (has RSS) and `presidency.ro` (highest signal value).
- **Group 3 — Legacy infrastructure**: `cdep.ro` (Oracle PL/SQL), `senat.ro` (ASP.NET). Complex, dated architectures requiring careful scraper design. Lower priority for automation — consider manual monitoring or AGERPRES-mediated coverage.
- **Group 4 — Machine-readable**: `bnr.ro`. RSS feeds + XML endpoints. Implement as structured data ingest rather than scraping.
- **Group 5 — PDF extraction**: `monitoruloficial.ro`, `mfinante.gov.ro` (statistical reports), `bnr.ro` (publications). Require PDF download and text extraction pipeline.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Three government sources provide functional RSS or structured data feeds:

1. **gov.ro**: RSS feeds at `gov.ro/ro/rss` (Romanian) and `gov.ro/en/rss` (English). Confirmed functional. Delivers press releases and news items. This should be the primary automated intake for government/PM communications.

2. **BNR**: Multiple feeds via the RSS hub pages. Exchange rate XML at `bnr.ro/nbrfxrates.xml` (daily, structured, machine-readable). This is the most machine-friendly government data source in Romania.

3. **AGERPRES**: RSS likely available but URL unverified. If confirmed, AGERPRES RSS would provide the single most efficient intake for all government communications — it aggregates across all institutions. [VERIFY: check `agerpres.ro/rss` or inspect page source for `<link rel="alternate" type="application/rss+xml">`]

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Three sources publish substantially in PDF:
- **Monitorul Oficial**: All legal texts are PDF. Current editions generally text-based. The e-Monitor provides daily access. Require PDF text extraction; consider filtering by Part I only for strategic relevance.
- **BNR**: Monetary policy decisions, minutes, inflation reports, and financial stability reports are multi-page PDF. Well-structured, text-based. Table extraction useful for statistical data.
- **MF (Finance)**: Budget execution reports, investor presentations, and statistical annexes are PDF. Some contain complex tables requiring tabular extraction (tabula/camelot).

### 5.4 Language and Encoding

All government sources publish primarily in Romanian. English availability varies:

| Source | English Availability |
|---|---|
| Presidency | Major statements translated |
| gov.ro | Major items translated; RSS in both languages |
| MAE | Comprehensive English section |
| MApN | Full parallel English press archive |
| BNR | Comprehensive English site |
| MF | Select investor publications |
| AGERPRES | Select items with slight delay |
| SRI | Limited institutional pages |
| EU Perm Rep / NATO Delegation | English available |
| Parliament, Monitorul Oficial, Min. Economy, SIE | Romanian only |

All sites serve content in UTF-8. No legacy encoding issues observed. Romanian-language content requires Romanian NLP capabilities for automated analysis — key vocabulary provided in the Layer 1 Source Intelligence Map's Localized Query Vocabulary section.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A CSAT decision appears in presidential press releases, AGERPRES, gov.ro (if the PM participated), and MApN (if defense-related)
- Diplomatic communications appear in MAE, AGERPRES, presidency.ro (if presidential-level), and sometimes gov.ro
- Laws and ordinances appear in gov.ro, Monitorul Oficial, and the originating ministry
- Defense procurement decisions appear in MApN, presidency.ro (via CSAT), and AGERPRES

Implement content-hash deduplication. Use the following canonical source hierarchy:
1. **Monitorul Oficial**: canonical for all legal texts (laws, ordinances, decrees)
2. **Presidency**: canonical for CSAT decisions and presidential-level diplomatic events
3. **Originating ministry** (MAE for diplomatic, MApN for defense, MF for fiscal): canonical for institutional communications
4. **gov.ro**: canonical for government/PM decisions
5. **AGERPRES**: use as fallback/validation source, not canonical

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Presidency, gov.ro, MAE, AGERPRES | Every 2 hours | Daily publication, policy-critical, CSAT decisions |
| P1-Standard | MApN | Every 4 hours | Regular publication, defense-critical (airspace incidents) |
| P2-Active | Chamber of Deputies, Senate, MF, BNR | Every 6 hours | Regular publishing schedule during session/active periods |
| P2-Standard | EU Perm Rep, Monitorul Oficial, Min. Economy, SRI | Every 12 hours | Moderate frequency |
| P2-Low | NATO Delegation, BSEC | Every 24 hours | Low frequency but high signal |
| P2-Minimal | SIE | Weekly | Near-silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| presidency.ro 503 errors | Presidency, CSAT | AGERPRES (`agerpres.ro/english`) republishes presidential communications within minutes. Monitor @Abordo_Pemex on X. Social media: @KlsIohannis (legacy) — new Nicusor Dan presidency social media accounts. |
| MAE Drupal site downtime | MAE, EU Perm Rep, NATO Delegation | AGERPRES for MAE communications. EU Perm Rep content occasionally mirrored on main MAE site. Monitor @MAERomania on X. |
| MApN site unresponsive | MApN | AGERPRES republishes MApN press releases. Romania Insider (`romania-insider.com`) curates defense news in English. |
| BNR site downtime | BNR | Exchange rate data mirrored by commercial services (floatrates.com, cursbanci.ro). Monetary policy decisions covered by Ziarul Financiar and Profit.ro within minutes. |
| Monitorul Oficial subscription required | Monitorul Oficial (archive) | Current-day editions are free via e-Monitor. For archive access, the EU Forum of Official Gazettes (`op.europa.eu/en/web/forum/romania-oj`) provides metadata. Commercial service Expert Monitor (`expert-monitor.ro`) provides paid access. |
| Parliament sites slow/unresponsive | cdep.ro, senat.ro | AGERPRES covers major parliamentary proceedings. G4Media and Digi24 provide detailed parliamentary reporting. |
| Ministry of Economy browser verification | economie.gov.ro | Headless browser rendering (Playwright/Puppeteer). Government press releases about economy ministry activities also appear on gov.ro. |

---

*This supplement should be reviewed quarterly or upon any major government reshuffle, change in the PNL-PSD PM rotation (scheduled for 2027), presidential administration changes, or restructuring of ministry web infrastructure. The [VERIFY] tags should be resolved through direct testing of RSS/feed endpoints during pipeline integration.*
