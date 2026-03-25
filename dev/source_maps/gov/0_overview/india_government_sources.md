# Official Government Sources Supplement: INDIA

**Primary languages of political discourse: English and Hindi**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — India (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for India. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

India's government web infrastructure is decentralized across the `*.gov.in` and `*.nic.in` domain families. Unlike Mexico's centralized `gob.mx` platform, Indian government agencies maintain independent websites on National Informatics Centre (NIC) infrastructure, with no single extraction pattern applicable across ministries. However, the **Press Information Bureau (PIB)** — operated by the Ministry of Information and Broadcasting — functions as a de facto centralization layer: most ministries route their press releases through PIB in addition to (or instead of) their own websites. This makes PIB the single most important ingestion point for government communications, but it also means that ministry-specific context (attachments, data tables, notification details) often requires a second fetch from the originating ministry's site. The **Gazette of India** (egazette.gov.in) serves as the constitutional publication vehicle for all federal law and notifications, analogous to Mexico's DOF.

India's government sources publish in both English and Hindi, with English dominating policy and foreign affairs communications and Hindi used for domestic-facing announcements. Some agencies (PIB, PMO) provide parallel outputs in both languages, creating opportunities for cross-language framing analysis.

---

## 1. OFFICIAL GOVERNMENT SOURCES: INDIA

### 1.1 Head of Government — Prime Minister's Office (PMO)

| Field | Detail |
|---|---|
| **Institution** | Prime Minister's Office (PMO) |
| **Domain** | `pmindia.gov.in` |
| **Entry Point URL** | `https://www.pmindia.gov.in/en/news-updates/` |
| **RSS/Atom Feed** | WordPress RSS exists at `https://www.pmindia.gov.in/en/feed/` but is non-functional (contains only a test post dated June 2024; not actively maintained). Treat as unavailable. |
| **Language** | English, Hindi (`/hi/` path prefix for Hindi) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. PM's speeches, statements, press releases, and foreign visit readouts published same-day. |
| **Content Format** | HTML (WordPress-based CMS). Speeches as HTML articles. Some PDFs for formal communiques. |
| **Extraction Method** | HTML scraping of `/en/news-updates/` listing page. WordPress REST API available at `https://www.pmindia.gov.in/wp-json/wordpress-popular-posts/v1/popular-posts` (limited utility — popular posts only, not chronological). Standard WordPress pagination. |
| **Editorial Orientation** | Official government position. All content produced by PMO communications team. Framing reflects BJP/NDA policy priorities and PM Modi's personal brand. |
| **Why This Source** | The authoritative source for PM-level diplomatic statements, foreign visit readouts, Cabinet Committee on Security (CCS) decisions, and major policy announcements. The gap between PMO language and MEA/MoD statements on the same event is an analytical signal. PM's Mann Ki Baat radio addresses (monthly, Hindi) surface domestic political messaging priorities. |
| **Access Notes** | No paywall, no authentication. WordPress-based site hosted on NIC infrastructure. No bot protection observed. The site also hosts an archive section for historical PM communications. |

**Additional entry points:**
- PM's speeches: `https://www.pmindia.gov.in/en/pms-speeches/`
- PM's speeches (tagged): `https://pmindia.gov.in/en/tag/pmspeech/`
- Media coverage: `https://www.pmindia.gov.in/en/media-coverage-1/`
- PIB mirror: PMO releases also published via PIB (see section 1.10a) with `mincode=2` filter

---

### 1.2 Foreign Ministry — Ministry of External Affairs (MEA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of External Affairs (MEA) |
| **Domain** | `mea.gov.in` |
| **Entry Point URL** | `https://www.mea.gov.in/press-releases.htm` |
| **RSS/Atom Feed** | None available. No RSS/Atom endpoints identified on mea.gov.in. |
| **Language** | English (primary); Hindi available for some content; bilateral documents sometimes in partner-country languages |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Spokesperson briefings published same-day. Press releases for bilateral meetings, multilateral events, and consular matters. |
| **Content Format** | HTML. Press releases and media briefings as HTML articles. Bilateral documents and treaty texts sometimes in PDF. |
| **Extraction Method** | HTML scraping of individual section listing pages. URL pattern: `https://www.mea.gov.in/{section}.htm?{id}/{Section_Name}`. Custom ASP-style CMS with distinct URL structures per section. |
| **Editorial Orientation** | Official foreign ministry position. Under External Affairs Minister S. Jaishankar, communications emphasize strategic autonomy, multi-alignment, and India's "rising power" narrative. Spokesperson briefings are notably precise in language — word choices (e.g., "noted" vs. "welcomed" vs. "expressed concern") carry calibrated diplomatic weight. |
| **Why This Source** | The only primary source for India's formal diplomatic positions, bilateral/multilateral joint statements, spokesperson briefings, and treaty database. Media briefing transcripts capture the full Q&A with journalists, often surfacing positions not in the formal press release. The response-to-media-queries section reveals what issues are generating external pressure. |
| **Access Notes** | No paywall, no authentication. Site is stable on NIC infrastructure. No bot protection observed. Content is fully open. The Indian Treaties Database provides searchable access to bilateral and multilateral agreements. |

**Additional entry points:**
- Speeches & statements: `https://www.mea.gov.in/Speeches-Statements.htm`
- Media briefings (spokesperson): `https://www.mea.gov.in/media-briefings.htm`
- Bilateral/multilateral documents: `https://www.mea.gov.in/bilateral-documents.htm`
- Response to media queries: `https://www.mea.gov.in/response-to-queries.htm`
- Lok Sabha Q&A (MEA): `https://www.mea.gov.in/lok-sabha.htm`
- Rajya Sabha Q&A (MEA): `https://www.mea.gov.in/rajya-sabha.htm`
- Indian Treaties Database: `https://www.mea.gov.in/treaty.htm`

---

### 1.3 Defense / Security — Ministry of Defence (MoD), Service Branches, CDS

#### 1.3a Ministry of Defence (MoD)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Defence (MoD) |
| **Domain** | `mod.gov.in` |
| **Entry Point URL** | `https://www.mod.gov.in/press-release` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English, Hindi |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-5 per week. Press releases cover defence procurement approvals (Defence Acquisition Council), policy changes, bilateral defense cooperation, and institutional announcements. |
| **Content Format** | HTML (Drupal-based CMS). Some attached PDFs for formal orders and annual reports. |
| **Extraction Method** | HTML scraping of `/press-release` listing page. Drupal pagination. |
| **Editorial Orientation** | Official defence policy position. Communications emphasize Atmanirbhar Bharat (self-reliance in defence), indigenization targets, and Make in India defence corridors. Operational details (casualties, setbacks) are systematically excluded. |
| **Why This Source** | Primary source for Defence Acquisition Council approvals, defence budget execution, bilateral defence agreements (Logistics Support Agreements, BECA, COMCASA-type pacts), and integrated theatre command restructuring. PIB also carries MoD releases, but the ministry site includes additional policy documents, annual reports, and department-specific content (DDP, DRDO links). |
| **Access Notes** | The site has intermittently returned connection errors. PIB (`pib.gov.in/newsite/pmreleases.aspx?mincode=33`) serves as a reliable fallback for MoD press releases. The Department of Defence Production (DDP) has a separate portal at `ddpmod.gov.in`. |

**Additional entry points:**
- MoD via PIB: `https://www.pib.gov.in/newsite/pmreleases.aspx?mincode=33`
- Department of Defence Production: `https://www.ddpmod.gov.in/`
- Defence Procurement Procedure documents: available on mod.gov.in under policy documents

#### 1.3b Indian Army

| Field | Detail |
|---|---|
| **Institution** | Indian Army |
| **Domain** | `indianarmy.nic.in` |
| **Entry Point URL** | `https://indianarmy.nic.in/media/releases/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-5 per week. Press releases cover exercises, operational developments (particularly LAC and LoC), humanitarian operations, and institutional events. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of `/media/releases/` listing page. |
| **Editorial Orientation** | Official military communication. Highly controlled — operational outcomes only. Border incidents reported in calibrated language; LAC/LoC details deliberately vague. |
| **Why This Source** | Direct window into Indian Army's operational tempo, exercise partnerships (Malabar, Tiger TRIUMPH, Yudh Abhyas), and LAC/LoC situation. Exercise partner selection and frequency are leading indicators of defence alignment shifts. |
| **Access Notes** | NIC-hosted. Site has occasionally returned connection errors. No bot protection observed when accessible. |

#### 1.3c Indian Navy

| Field | Detail |
|---|---|
| **Institution** | Indian Navy |
| **Domain** | `indiannavy.nic.in` / `indiannavy.gov.in` |
| **Entry Point URL** | `https://indiannavy.nic.in/archive/press-release` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-4 per week. Covers fleet deployments, maritime exercises, carrier battle group operations, shipbuilding milestones, and Indian Ocean Region (IOR) security operations. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of `/archive/press-release` listing page. |
| **Editorial Orientation** | Official naval communication. Emphasizes blue-water capability, IOR dominance, and indigenous shipbuilding (INS Vikrant-class, Project 75 submarines). Maritime doctrine publications surface strategic posture shifts. |
| **Why This Source** | The Indian Navy's IOR deployments and exercise partnerships (Quad Malabar, JIMEX with Japan, Tasman Saber with Australia) are among the clearest operational indicators of India's Indo-Pacific strategic alignment. Carrier battle group deployments during crises (e.g., May 2025 post-Pahalgam deployment to Arabian Sea) signal escalation posture. The updated Indian Maritime Doctrine 2025 was published through this channel. |
| **Access Notes** | Two domains exist: `indiannavy.nic.in` (older, NIC-hosted) and `indiannavy.gov.in` (newer portal). Both are occasionally slow. Press releases primarily on the nic.in domain. |

#### 1.3d Indian Air Force (IAF)

| Field | Detail |
|---|---|
| **Institution** | Indian Air Force (IAF) |
| **Domain** | `indianairforce.nic.in` |
| **Entry Point URL** | `https://indianairforce.nic.in/press-release` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 1-3 per week. Press releases cover air exercises, aircraft inductions (Rafale, Tejas), operational developments, and institutional events. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of `/press-release` listing page. |
| **Editorial Orientation** | Official air force communication. Emphasizes modernization, indigenous fighter development (Tejas Mk-IA, AMCA), and operational readiness. |
| **Why This Source** | IAF press releases on fighter acquisitions (Rafale Marine for Navy, additional Rafale for IAF, Tejas pipeline), air defence systems (S-400 operational status), and exercise participation provide capability indicators. The Technology Perspective and Capability Roadmap 2025 was published through MoD/IAF channels. |
| **Access Notes** | NIC-hosted. Latest news section at `https://indianairforce.nic.in/latest-news/` provides additional operational updates. |

---

### 1.4 Parliament — Lok Sabha and Rajya Sabha

#### 1.4a Lok Sabha (House of the People)

| Field | Detail |
|---|---|
| **Institution** | Lok Sabha (Lower House of Parliament) |
| **Domain** | `loksabha.nic.in` / `sansad.in` |
| **Entry Point URL** | `https://loksabha.nic.in/` (main portal); `https://sansad.in/ls/debates/introduction` (debates) |
| **RSS/Atom Feed** | None identified. |
| **Language** | English, Hindi |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily during session periods (Budget Session: Feb-May; Monsoon Session: Jul-Aug; Winter Session: Nov-Dec). Reduced during recess. |
| **Content Format** | HTML for questions and listings. Debates published as PDF (verbatim transcripts). Bills as HTML and PDF. |
| **Extraction Method** | HTML scraping of questions database. PDF download for debate transcripts. The Digital Sansad platform (`sansad.in`) provides a more modern interface. |
| **Editorial Orientation** | Institutional — verbatim proceedings. Question Hour transcripts reflect opposition positions on foreign/defence policy that no media outlet fully covers. |
| **Why This Source** | Parliamentary questions directed at MEA, MoD, and Finance Ministry force official responses on sensitive topics (LAC standoff details, defence procurement costs, trade agreement terms) that are otherwise classified or undisclosed. Starred questions require oral answers on the floor, generating unscripted exchanges. |
| **Access Notes** | Multiple legacy portals exist. The `sansad.in` (Digital Sansad) platform is the modernized unified portal. Older content remains on `loksabha.nic.in`. Debate search at `loksabhaph.nic.in/Debates/DebateAdvSearch13.aspx`. Press relations at `pprloksabha.sansad.in`. |

**Additional entry points:**
- Questions search: `https://loksabhaph.nic.in/Questions/Qtextsearch.aspx`
- Lok Sabha debates: `https://sansad.in/ls/debates/introduction`
- Press and Public Relations: `https://pprloksabha.sansad.in/`
- Parliament Digital Library: `https://eparlib.sansad.in/`

#### 1.4b Rajya Sabha (Council of States)

| Field | Detail |
|---|---|
| **Institution** | Rajya Sabha (Upper House of Parliament) |
| **Domain** | `rajyasabha.nic.in` / `sansad.in` |
| **Entry Point URL** | `https://rajyasabha.nic.in/` (main portal); `https://sansad.in/rs/debates/introduction` (debates) |
| **RSS/Atom Feed** | None identified. |
| **Language** | English, Hindi |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment |
| **Publication Frequency** | Daily during session periods. |
| **Content Format** | HTML for questions. PDF for debate transcripts. |
| **Extraction Method** | HTML scraping of questions database. PDF download for debate transcripts. Debate archive searchable at `rsdebate.nic.in` (DSpace-based repository with 741,000+ entries). |
| **Editorial Orientation** | Institutional — verbatim proceedings. Rajya Sabha debates tend to be more substantive on foreign policy than Lok Sabha due to nominated members and longer tenure. |
| **Why This Source** | The Rajya Sabha Standing Committee on External Affairs and the Standing Committee on Defence produce reports that review ministry performance and policy. These committee reports — when tabled — contain the most detailed parliamentary scrutiny of foreign and defence policy available. Rajya Sabha debates on the "India's World" programme and foreign affairs discussions are analytically richer than Lok Sabha equivalents. |
| **Access Notes** | `rsdebate.nic.in` is a DSpace-based digital repository with full-text search across debates from 1952 to present. Questions portal at `rajyasabha.nic.in/Questions/QuestionListStarred`. |

**Additional entry points:**
- Official debates archive: `https://rsdebate.nic.in/`
- Rajya Sabha debates on Digital Sansad: `https://sansad.in/rs/debates/officials`
- Questions (starred): `https://rajyasabha.nic.in/Questions/QuestionListStarred`

---

### 1.5 Official Gazette — The Gazette of India

| Field | Detail |
|---|---|
| **Institution** | The Gazette of India (Department of Publication, Ministry of Urban Development) |
| **Domain** | `egazette.gov.in` / `egazette.nic.in` |
| **Entry Point URL** | `https://egazette.gov.in/` (daily edition) |
| **RSS/Atom Feed** | None available. |
| **Language** | English, Hindi (bilingual publication — all gazette notifications published in both languages as constitutional requirement) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Gazette is the constitutional publication vehicle for all federal laws, regulations, executive orders, and treaty notifications |
| **Publication Frequency** | Daily (Extraordinary Gazettes published as needed, often multiple per day). Weekly Gazette published on Saturdays. |
| **Content Format** | **PDF** exclusively. Each notification is a separate PDF. Gazette ID format: `CG-DL-E-{date}-{number}` (Central Government, Delhi, Extraordinary). |
| **Extraction Method** | Index page scraping to identify new publications on the `Default.aspx` page, then PDF download and text extraction. Category-specific filtering available via `RecentUploads.aspx?Category={n}` (1=Bills & Acts, 2=Elections, 3=Land Acquisition, 4=Delhi Master Plan, 5=Recruitment Rules). Gazette Directory at `GazetteDirectory.aspx` provides browsable index. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law and notification. |
| **Why This Source** | Constitutional requirement: no federal law, international agreement ratification, defence procurement notification, or regulatory change is legally binding until published in the Gazette. This is the only source that provides definitive, timestamped legal text. All media and ministry press release reporting on legislation is downstream of Gazette publication. Defence-relevant notifications include arms export/import rules, defence offset policy changes, and territorial waters/airspace notifications. |
| **Access Notes** | Free access since October 2015 (e-publishing mandate). All parts, sections, and sub-sections are uploaded by Government of India Printing Presses. State gazettes published separately via state portals. No bot protection observed. PDFs are text-based (not scanned) for recent publications. |

**Additional entry points:**
- Gazette Directory: `https://egazette.gov.in/GazetteDirectory.aspx`
- Category-specific (Bills & Acts): `https://egazette.gov.in/RecentUploads.aspx?Category=1`
- State gazettes: linked from `https://egazette.gov.in/StateGazette.aspx`
- National Archives gazette notifications: `https://nationalarchives.nic.in/`

---

### 1.6 Finance Ministry — Ministry of Finance

| Field | Detail |
|---|---|
| **Institution** | Ministry of Finance (MoF) |
| **Domain** | `finmin.nic.in` / `finmin.gov.in` |
| **Entry Point URL** | `https://www.finmin.nic.in/` (main portal — press releases via PIB) |
| **RSS/Atom Feed** | None identified on finmin.nic.in. Releases routed through PIB RSS (see section 1.10a). |
| **Language** | English, Hindi |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week via PIB. Budget and Economic Survey documents published annually (February). Monthly economic reviews. |
| **Content Format** | HTML on finmin.nic.in. Budget documents, Economic Survey, and statistical reports as PDF. PIB releases as HTML. |
| **Extraction Method** | For press releases: monitor PIB with ministry filter. For policy documents and budget: scrape finmin.nic.in document sections. PDF extraction for budget documents, economic surveys, and statistical reports. |
| **Editorial Orientation** | Official fiscal policy position. Technical language, data-heavy. Under Finance Minister Nirmala Sitharaman, communications emphasize fiscal consolidation, capital expenditure growth, and digital economy transformation. |
| **Why This Source** | Primary source for Union Budget, Economic Survey, fiscal policy announcements, public debt management, FDI policy changes, tax treaty amendments, and bilateral/multilateral financial commitments. Defence budget allocations (the largest single ministry allocation) are announced here. The monthly economic review provides macroeconomic framing. |
| **Access Notes** | The main portal (`finmin.nic.in` / `finmin.gov.in`) has intermittently returned connection errors. The site has multiple department-specific sub-portals. PIB is the more reliable channel for press releases. Budget documents are available at `indiabudget.gov.in`. |

**Additional entry points:**
- Union Budget portal: `https://www.indiabudget.gov.in/`
- Department of Economic Affairs: `https://dea.gov.in/`
- Department of Expenditure: `https://doe.gov.in/`
- Department of Revenue: `https://dor.gov.in/`
- Department of Financial Services: `https://financialservices.gov.in/`
- DIPAM (Investment and Public Asset Management): `https://dipam.gov.in/`
- MoF via PIB: filter PIB releases by Finance Ministry

---

### 1.7 Central Bank — Reserve Bank of India (RBI)

| Field | Detail |
|---|---|
| **Institution** | Reserve Bank of India (RBI) |
| **Domain** | `rbi.org.in` |
| **Entry Point URL** | `https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx` (press releases); `https://rbi.org.in/scripts/Annualpolicy.aspx` (monetary policy statements) |
| **RSS/Atom Feed** | **Yes — five feeds available.** RSS hub page: `https://rbi.org.in/Scripts/rss.aspx`. Feeds: press releases, notifications, speeches, publications, tenders. |
| **Language** | English (primary); Hindi versions available for major publications |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 6 per year (bi-monthly, per MPC schedule). Press releases: multiple per week. Notifications/circulars: daily. Weekly statistical supplement. |
| **Content Format** | HTML for press releases and notifications. **PDF** for monetary policy statements, minutes, and publications. RSS feeds deliver structured XML. |
| **Extraction Method** | RSS feeds for press releases, notifications, speeches, and publications (structured, machine-readable XML). PDF download and extraction for monetary policy statements and minutes. HTML scraping for notifications and circulars. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Sanjay Malhotra, the MPC has maintained a focus on inflation targeting while supporting growth. RBI communications on rupee internationalization and CBDC (digital rupee) pilots reflect government-aligned strategic priorities. |
| **Why This Source** | RBI is the only source for authoritative monetary policy decisions, inflation forecasts, forex reserve data, and banking sector assessments. Its RSS feeds are the most machine-friendly government data source in India. RBI's foreign exchange reserves management and rupee settlement mechanism agreements (with Russia, UAE, etc.) are direct indicators of de-dollarization strategy and sanctions navigation. The Database on Indian Economy (`data.rbi.org.in`) provides structured time-series data. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained and reliable. The RBI website is one of the most technically robust Indian government sites. Email subscription service also available. |

**Key RSS feed URLs:**

| Feed | URL |
|---|---|
| Press releases | `https://rbi.org.in/pressreleases_rss.xml` |
| Notifications | `https://rbi.org.in/notifications_rss.xml` |
| Speeches | `https://rbi.org.in/speeches_rss.xml` |
| Publications | `https://rbi.org.in/Publication_rss.xml` |
| Tenders | `https://rbi.org.in/tenders_rss.xml` |

**Additional entry points:**
- Monetary policy overview: `https://rbi.org.in/scripts/FS_Overview.aspx?fn=2752`
- Database on Indian Economy: `https://data.rbi.org.in`
- Notifications: `https://rbi.org.in/Scripts/NotificationUser.aspx`
- Master Directions: `https://rbi.org.in/Scripts/BS_ViewMasterDirections.aspx`
- Publications portal: `https://rbi.org.in/Scripts/Publications.aspx`
- Search: `https://rbi.org.in/scripts/SearchResults.aspx`

---

### 1.8 Trade / Commerce — Ministry of Commerce & Industry

| Field | Detail |
|---|---|
| **Institution** | Ministry of Commerce & Industry (MoCI) — Department of Commerce + DPIIT |
| **Domain** | `commerce.gov.in` / `dpiit.gov.in` |
| **Entry Point URL** | `https://www.commerce.gov.in/press-releases/` (Dept. of Commerce); `https://www.dpiit.gov.in/` (DPIIT) |
| **RSS/Atom Feed** | None identified on either portal. |
| **Language** | English (primary); Hindi for some DPIIT content |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | Department of Commerce: monthly foreign trade press releases (15th of each month); trade agreement updates as events warrant. DPIIT: 2-3 per week covering FDI policy, PLI schemes, startup ecosystem, and industrial policy. |
| **Content Format** | HTML for press releases. PDF for trade statistics, FDI data, and policy documents. |
| **Extraction Method** | HTML scraping of `/press-releases/` listing page on commerce.gov.in (WordPress-based). DPIIT uses a different CMS — scrape document/announcement sections. |
| **Editorial Orientation** | Official trade policy position. Under Commerce Minister Piyush Goyal, communications emphasize export growth targets, FTA negotiations (EU, UK, GCC), PLI scheme achievements, and India's positioning as a China+1 manufacturing alternative. |
| **Why This Source** | Primary source for India's foreign trade statistics (monthly data with 30-day lag), FTA negotiation updates, anti-dumping/trade remedy decisions (via DGTR), FDI policy changes, and PLI scheme progress. The monthly foreign trade press release is the most-cited government economic data point internationally. DPIIT's FDI data provides quarterly sectoral and source-country breakdowns. |
| **Access Notes** | commerce.gov.in is stable and well-maintained. DPIIT site occasionally serves PDFs directly for press releases. DGFT (Directorate General of Foreign Trade) notifications at `dgft.gov.in` provide trade policy instrument details. |

**Additional entry points:**
- International trade hub: `https://www.commerce.gov.in/international-trade/`
- Trade statistics: `https://www.commerce.gov.in/trade-statistics/`
- Niryat (export) portal: `https://niryat.gov.in/`
- Trade analytics: `https://trade-analytics.commerce.gov.in/`
- DGFT notifications: `https://www.dgft.gov.in/`
- DGTR (trade remedies): `https://www.dgtr.gov.in/`
- DPIIT FDI data: available on dpiit.gov.in under FDI statistics section

---

### 1.9 Intelligence / National Security — NSC Secretariat, RAW

| Field | Detail |
|---|---|
| **Institution** | National Security Council Secretariat (NSCS) / Research and Analysis Wing (RAW) |
| **Domain** | No dedicated public website |
| **Entry Point URL** | None. NSCS functions as part of the PMO. RAW has no public web presence. |
| **RSS/Atom Feed** | None. |
| **Language** | N/A |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. The NSA's public statements are routed through PMO or PIB. RAW publishes nothing. |
| **Content Format** | N/A |
| **Extraction Method** | Periodic check of PMO and PIB for NSA-related statements. Monitor Gazette for organizational/budget changes to intelligence agencies. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. India's intelligence community has no public communications infrastructure. The National Security Adviser (Ajit Doval, serving third term since 2014) is the most powerful national security official, but his statements are channeled through PMO press releases or appear as attributed quotes in media coverage. The NSCS was given legal status in August 2019 via amendment to the Allocation of Business Rules, but this did not create a public-facing communications channel. RAW (Research and Analysis Wing) is India's external intelligence agency and has zero public presence by design. |
| **Access Notes** | The real intelligence signal surfaces through: (a) PMO/PIB statements referencing "NSA-level" discussions or CCS decisions; (b) MoD/MEA references to intelligence inputs; (c) leaks to defence correspondents at ThePrint, The Hindu, and Hindustan Times; (d) Gazette notifications of organizational/budget changes; (e) Parliamentary Standing Committee reports on Home Affairs and Defence (when tabled). The pipeline should flag any direct NSA statement via PMO as a high-priority anomaly — Doval speaks publicly only on matters of deliberate strategic signaling. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Press Information Bureau (PIB)

| Field | Detail |
|---|---|
| **Institution** | Press Information Bureau (PIB) — Ministry of Information & Broadcasting |
| **Domain** | `pib.gov.in` |
| **Entry Point URL** | `https://pib.gov.in/allRel.aspx` (all releases); `https://pib.gov.in/indexd.aspx` (desktop home) |
| **RSS/Atom Feed** | **Yes.** Press releases: `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3` (English) / `?Lang=2` (Hindi). Photos: `https://pib.gov.in/RssMain.aspx?ModId=8&Lang=1&Regid=3`. Media advisories: `https://pib.gov.in/RssMain.aspx?ModId=10&Lang=1&Regid=3`. RSS hub: `https://www.pib.gov.in/ViewRss.aspx`. |
| **Language** | English, Hindi, and 12 regional languages (Urdu, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Odia, Punjabi, Assamese, Manipuri) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains (cross-cutting government communication clearinghouse) |
| **Publication Frequency** | Daily — multiple releases per day. PIB is the single highest-volume government publication source in India, issuing 20-50 releases daily across all ministries. |
| **Content Format** | HTML (ASP.NET Web Forms). Individual releases at `PressReleseDetail.aspx?PRID={id}`. |
| **Extraction Method** | RSS feeds for real-time monitoring (press releases, photos, media advisories). HTML scraping of `allRel.aspx` for comprehensive archive access. Individual releases via `PressReleseDetail.aspx?PRID={id}`. PMO-specific releases filterable at `pmreleases.aspx?mincode=2`. Ministry-specific filtering via `mincode` parameter. Regional filtering via `Regid` parameter. |
| **Editorial Orientation** | Official government position across all ministries. PIB is the central clearinghouse — it publishes releases from every ministry, but all content is cleared through the respective ministry's communications wing. PIB Hindi releases sometimes contain framing differences from English versions, which is analytically significant. |
| **Why This Source** | PIB is the single most important Layer 2 source for India. It aggregates press releases from all central government ministries, including Defence, External Affairs, Finance, Commerce, and Home Affairs. A single PIB RSS subscription captures the output of 50+ ministries. Ministry-specific filtering via `mincode` parameter allows targeted monitoring. The multilingual output (14 languages) enables cross-language framing analysis — particularly Hindi vs. English differences on sensitive topics (Kashmir, Pakistan, China). |
| **Access Notes** | No paywall. ASP.NET Web Forms site on NIC infrastructure. RSS feeds are functional and reliable. Archive available from 2004 onwards at `archive.pib.gov.in`. Some pages use Akamai CDN. Mobile-specific pages at `AllReleasem.aspx`. |

**Key ministry filter codes (mincode parameter) for PIB:**

| Ministry | mincode | URL |
|---|---|---|
| PMO | 2 | `pib.gov.in/newsite/pmreleases.aspx?mincode=2` |
| Ministry of Defence | 33 | `pib.gov.in/newsite/pmreleases.aspx?mincode=33` |
| Ministry of External Affairs | 12 | `pib.gov.in/newsite/pmreleases.aspx?mincode=12` |
| Ministry of Finance | 7 | `pib.gov.in/newsite/pmreleases.aspx?mincode=7` |
| Ministry of Commerce & Industry | 3 | `pib.gov.in/newsite/pmreleases.aspx?mincode=3` |
| Ministry of Home Affairs | 11 | `pib.gov.in/newsite/pmreleases.aspx?mincode=11` |

#### 1.10b NITI Aayog

| Field | Detail |
|---|---|
| **Institution** | NITI Aayog (National Institution for Transforming India) |
| **Domain** | `niti.gov.in` |
| **Entry Point URL** | `https://www.niti.gov.in/` (main portal); press releases routed through PIB |
| **RSS/Atom Feed** | None identified on niti.gov.in. Releases via PIB RSS. |
| **Language** | English (primary); Hindi for some publications |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Institutional engagement |
| **Publication Frequency** | Publications: 2-3 per month (reports, policy papers, working papers). Press releases via PIB: 2-4 per week. |
| **Content Format** | HTML on niti.gov.in. Publications and reports as PDF. Data via National Data Analytics Platform (NDAP). |
| **Extraction Method** | HTML scraping for publications sections. PDF download for reports. PIB monitoring for press releases. |
| **Editorial Orientation** | Government policy think tank — reflects NDA strategic economic priorities. Under Vice Chairman (CEO-equivalent), produces government-commissioned analysis that prefigures policy. Not independent — its output represents official thinking. |
| **Why This Source** | NITI Aayog replaced the Planning Commission in 2015 and serves as the government's principal policy advisory body. Its publications — Fiscal Health Index, India Innovation Index, SDG India Index, Aspirational Districts Programme — shape resource allocation and reform priorities. The National Data Analytics Platform (`ndap.niti.gov.in`) is the most comprehensive open government data portal. ArthNITI economic bulletins provide the government's preferred macroeconomic framing. |
| **Access Notes** | Fully open. Publications at `niti.gov.in/publications/division-reports` and `niti.gov.in/documents/reports`. NDAP at `ndap.niti.gov.in` provides downloadable datasets with API access. |

**Additional entry points:**
- Division reports: `https://niti.gov.in/publications/division-reports`
- Policy papers: `https://niti.gov.in/publications/policy-and-research/policy-paper`
- Annual report: `https://niti.gov.in/publication/annual-report`
- NDAP (data platform): `https://ndap.niti.gov.in/`
- ArthNITI bulletin: `https://niti.gov.in/publications/arth-niti`

#### 1.10c Sansad TV (Parliament Television)

| Field | Detail |
|---|---|
| **Institution** | Sansad TV (formed from merger of Lok Sabha TV and Rajya Sabha TV) |
| **Domain** | `sansadtv.nic.in` |
| **Entry Point URL** | `https://sansadtv.nic.in/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Hindi, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily during parliamentary sessions. Weekly programming year-round. |
| **Content Format** | Video (live and archived). Transcripts in HTML/PDF for some programmes. |
| **Extraction Method** | Video monitoring (not suitable for automated text pipeline). Text extraction limited to programme descriptions and any published transcripts. The "India's World" programme on foreign affairs provides analytical content but requires manual review. |
| **Editorial Orientation** | Nonpartisan in proceedings broadcasts (verbatim). Editorial programming ("India's World," panel discussions) reflects a managed-centrist orientation. |
| **Why This Source** | Direct access to parliamentary debates on defence budgets, treaty ratifications, foreign policy statements, and Question Hour. "India's World" is a weekly foreign affairs discussion programme that hosts diplomats, academics, and former officials — useful for tracking establishment consensus. |
| **Access Notes** | Free streaming. Archived video available. YouTube channel provides additional access. Not ideal for automated pipeline due to video-primary format. Transcripts available via Lok Sabha and Rajya Sabha debate archives (see section 1.4). |

#### 1.10d Defence Research and Development Organisation (DRDO)

| Field | Detail |
|---|---|
| **Institution** | Defence Research and Development Organisation (DRDO) |
| **Domain** | `drdo.gov.in` |
| **Entry Point URL** | `https://www.drdo.gov.in/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English, Hindi |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | 1-3 per week. Press releases for missile tests, technology demonstrations, and institutional events. |
| **Content Format** | HTML. Technology achievement announcements with images. |
| **Extraction Method** | HTML scraping. Also monitor PIB for DRDO-related releases. |
| **Editorial Orientation** | Official defence R&D communication. Emphasizes indigenous capability development (missiles, radars, UAVs, NBC protection). Success-only reporting — test failures are never announced. |
| **Why This Source** | DRDO announcements of missile tests (Agni-V, BrahMos variants, hypersonic technology demonstrators), indigenous weapons system development (Tejas engine, Astra missile), and technology transfers to production agencies are leading indicators of defence capability evolution. Announcement timing is itself a signal — missile tests during diplomatic tensions serve as strategic messaging. |
| **Access Notes** | Website occasionally slow. PIB carries most DRDO press releases with additional context. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Single Platform |
|---|---|---|---|---|---|---|---|
| 1 | PMO | `pmindia.gov.in/en/news-updates/` | WordPress feed exists but non-functional | P1 | HTML | Daily | No |
| 2 | MEA | `mea.gov.in/press-releases.htm` | No | P1 | HTML/PDF | Daily | No |
| 3a | MoD | `mod.gov.in/press-release` | No | P1 | HTML | 3-5/week | No |
| 3b | Indian Army | `indianarmy.nic.in/media/releases/` | No | P1 | HTML | 2-5/week | No |
| 3c | Indian Navy | `indiannavy.nic.in/archive/press-release` | No | P1 | HTML | 2-4/week | No |
| 3d | IAF | `indianairforce.nic.in/press-release` | No | P1 | HTML | 1-3/week | No |
| 4a | Lok Sabha | `loksabha.nic.in` / `sansad.in` | No | P2 | HTML/PDF | Daily (session) | No |
| 4b | Rajya Sabha | `rajyasabha.nic.in` / `rsdebate.nic.in` | No | P2 | HTML/PDF | Daily (session) | No |
| 5 | Gazette of India | `egazette.gov.in` | No | P2 | PDF | Daily | No |
| 6 | Ministry of Finance | `finmin.nic.in` (via PIB) | Via PIB | P2 | HTML/PDF | 3-5/week | No |
| 7 | RBI | `rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx` | **Yes** (5 feeds) | P2 | HTML/PDF/RSS | Variable | No |
| 8 | Commerce & Industry | `commerce.gov.in/press-releases/` | No | P2 | HTML/PDF | Monthly + events | No |
| 9 | NSCS / RAW | None | No | P2 | N/A | Negligible | N/A |
| 10a | PIB | `pib.gov.in/allRel.aspx` | **Yes** (3 feeds) | P1 | HTML | Daily (20-50/day) | Yes (clearinghouse) |
| 10b | NITI Aayog | `niti.gov.in` (via PIB) | Via PIB | P2 | HTML/PDF | 2-4/week | No |
| 10c | Sansad TV | `sansadtv.nic.in` | No | P2 | Video | Daily (session) | No |
| 10d | DRDO | `drdo.gov.in` | [VERIFY] | P2 | HTML | 1-3/week | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# India Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/in.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: in_pib
    name: Press Information Bureau (PIB)
    domain: pib.gov.in
    entry_url: "https://pib.gov.in/allRel.aspx"
    rss_feed:
      press_releases_en: "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3"
      press_releases_hi: "https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3"
      photos: "https://pib.gov.in/RssMain.aspx?ModId=8&Lang=1&Regid=3"
      media_advisories: "https://pib.gov.in/RssMain.aspx?ModId=10&Lang=1&Regid=3"
    language: [en, hi]
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 1
    notes: >
      Single most important ingestion point. 20-50 releases/day across all ministries.
      Ministry-specific filtering via mincode parameter. Key mincodes: PMO=2, MoD=33, MEA=12,
      Finance=7, Commerce=3, Home=11. Available in 14 languages. Archive from 2004+.

  - id: in_pmo
    name: Prime Minister's Office (PMO)
    domain: pmindia.gov.in
    entry_url: "https://www.pmindia.gov.in/en/news-updates/"
    rss_feed: null  # WordPress feed exists but non-functional
    language: [en, hi]
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
    notes: >
      WordPress-based. WP REST API at /wp-json/ but limited utility.
      PMO releases also on PIB (mincode=2). Speech section at /en/pms-speeches/.

  - id: in_mea
    name: Ministry of External Affairs (MEA)
    domain: mea.gov.in
    entry_url: "https://www.mea.gov.in/press-releases.htm"
    rss_feed: null
    language: [en, hi]
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
      Multiple sections to monitor: press-releases.htm, media-briefings.htm,
      Speeches-Statements.htm, bilateral-documents.htm, response-to-queries.htm.
      Spokesperson briefing transcripts are same-day. Treaty database at /treaty.htm.

  - id: in_mod
    name: Ministry of Defence (MoD)
    domain: mod.gov.in
    entry_url: "https://www.mod.gov.in/press-release"
    rss_feed: null
    language: [en, hi]
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: >
      Drupal-based. Intermittent connectivity. Use PIB (mincode=33) as fallback.
      DDP at ddpmod.gov.in for defence production data.

  - id: in_army
    name: Indian Army
    domain: indianarmy.nic.in
    entry_url: "https://indianarmy.nic.in/media/releases/"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "LAC/LoC operational updates. Exercise announcements. Controlled release pattern."

  - id: in_navy
    name: Indian Navy
    domain: indiannavy.nic.in
    entry_url: "https://indiannavy.nic.in/archive/press-release"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: >
      IOR deployments and Quad exercise announcements. Maritime doctrine publications.
      Alternative domain at indiannavy.gov.in. Site occasionally slow.

  - id: in_iaf
    name: Indian Air Force (IAF)
    domain: indianairforce.nic.in
    entry_url: "https://indianairforce.nic.in/press-release"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Fighter inductions, air exercises, operational updates. Latest news at /latest-news/."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: in_lok_sabha
    name: Lok Sabha
    domain: loksabha.nic.in
    entry_url: "https://loksabha.nic.in/"
    rss_feed: null
    language: [en, hi]
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Questions at loksabhaph.nic.in. Digital Sansad at sansad.in/ls/.
      Debates as PDF transcripts. Session periods: Feb-May, Jul-Aug, Nov-Dec.

  - id: in_rajya_sabha
    name: Rajya Sabha
    domain: rajyasabha.nic.in
    entry_url: "https://rajyasabha.nic.in/"
    rss_feed: null
    language: [en, hi]
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Debate archive at rsdebate.nic.in (741,000+ entries, DSpace-based).
      Standing Committee reports on External Affairs and Defence are highest-value items.

  - id: in_gazette
    name: Gazette of India
    domain: egazette.gov.in
    entry_url: "https://egazette.gov.in/"
    rss_feed: null
    language: [en, hi]
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
      Constitutional publication vehicle. PDF-only. Gazette ID format: CG-DL-E-{date}-{number}.
      Category filtering at RecentUploads.aspx?Category={n}. Bills & Acts = 1.

  - id: in_finance
    name: Ministry of Finance
    domain: finmin.nic.in
    entry_url: "https://www.finmin.nic.in/"
    rss_feed: null  # use PIB
    language: [en, hi]
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Press releases via PIB (mincode=7). Budget at indiabudget.gov.in.
      Multiple department sub-portals: DEA, DoE, DoR, DFS, DIPAM.

  - id: in_rbi
    name: Reserve Bank of India (RBI)
    domain: rbi.org.in
    entry_url: "https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"
    rss_feed:
      press_releases: "https://rbi.org.in/pressreleases_rss.xml"
      notifications: "https://rbi.org.in/notifications_rss.xml"
      speeches: "https://rbi.org.in/speeches_rss.xml"
      publications: "https://rbi.org.in/Publication_rss.xml"
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: >
      Best machine-readable government source in India. 5 RSS feeds. Database on Indian Economy
      at data.rbi.org.in provides structured time-series. Monetary policy bi-monthly.
      Rupee settlement mechanisms and forex reserves data are strategic indicators.

  - id: in_commerce
    name: Ministry of Commerce & Industry
    domain: commerce.gov.in
    entry_url: "https://www.commerce.gov.in/press-releases/"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: monthly_plus_events
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Monthly trade data on 15th. WordPress-based. DPIIT at dpiit.gov.in for FDI/PLI data.
      DGFT at dgft.gov.in for trade policy notifications. Niryat portal at niryat.gov.in.

  - id: in_nscs
    name: National Security Council Secretariat / RAW
    domain: null
    entry_url: null
    rss_feed: null
    language: null
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: null
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: >
      No public website. Monitor PMO/PIB for NSA statements. Real signal via defence
      correspondents at ThePrint, The Hindu, Hindustan Times. Flag any direct NSA statement
      as high-priority anomaly.

  - id: in_niti_aayog
    name: NITI Aayog
    domain: niti.gov.in
    entry_url: "https://www.niti.gov.in/"
    rss_feed: null  # use PIB
    language: [en, hi]
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - institutional_engagement
    publication_frequency: "2-4_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Government policy think tank. Reports at /publications/division-reports.
      NDAP data platform at ndap.niti.gov.in provides API access.
      Press releases via PIB.

  - id: in_drdo
    name: Defence Research and Development Organisation (DRDO)
    domain: drdo.gov.in
    entry_url: "https://www.drdo.gov.in/"
    rss_feed: null  # [VERIFY]
    language: [en, hi]
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Missile test and indigenous weapons announcements. Success-only reporting.
      Also via PIB. Announcement timing during diplomatic tensions is a signal.

  - id: in_sansad_tv
    name: Sansad TV
    domain: sansadtv.nic.in
    entry_url: "https://sansadtv.nic.in/"
    rss_feed: null
    language: [en, hi]
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: video
    extraction_method: manual_review
    poll_interval_hours: 24
    notes: >
      Video-primary — not suitable for automated text pipeline. "India's World" programme
      covers foreign affairs. Transcripts via Lok Sabha/Rajya Sabha debate archives.

# NIC-hosted site shared configuration
nic_shared_config:
  hosting: "National Informatics Centre (NIC)"
  domain_families:
    - "*.nic.in"
    - "*.gov.in"
  common_issues:
    - "Sites occasionally return ECONNREFUSED (NIC infrastructure outages)"
    - "No unified template — each ministry has distinct CMS and URL patterns"
    - "Some sites (mod.gov.in, finmin.nic.in) have intermittent availability"
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "en-IN,en;q=0.9,hi;q=0.8"
  rate_limit: "max 1 request per 2 seconds per domain"
  fallback: "PIB (pib.gov.in) carries releases from most ministries"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Indian government communications are systematically crafted to project national strength, unity, and strategic purpose. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the delta between Hindi and English versions of the same announcement.

- **PMO**: Cross-reference PM's statements against same-day reporting in The Hindu and Indian Express. PMO framing in Hindi (Mann Ki Baat, PIB Hindi releases) frequently contains nationalist messaging absent from English versions — this delta is an analytical signal for domestic political constraints on diplomatic flexibility.
- **MEA**: Spokesperson briefings should be triangulated with The Hindu (strongest foreign affairs desk), Hindustan Times (establishment consensus), and ThePrint (defence-diplomatic nexus reporting). When MEA spokesperson language is unusually vague or evasive on a topic, it signals active diplomatic sensitivity. The response-to-queries section reveals what external pressures (human rights, Kashmir, minority treatment) are generating diplomatic friction.
- **MoD / Service branches**: Military press releases report exercises, inductions, and achievements but never operational setbacks, casualties (except posthumous awards), or procurement cost overruns. Cross-reference with ThePrint (best-in-class defence beat), FORCE Magazine (specialist depth), and MP-IDSA (doctrinal analysis). The timing of missile tests and capability announcements relative to diplomatic events is an intentional signaling mechanism.
- **PIB**: As the government clearinghouse, PIB volume and emphasis reveal bureaucratic priority. Cross-reference with all media sources for interpretation. Hindi vs. English PIB releases on the same event should be systematically compared — differences in emphasis, word choice, and framing reveal how the government calibrates messaging for different audiences.
- **RBI**: Monetary policy communications are technically rigorous and less subject to political distortion, but forward guidance language and the choice of emphasis in the Governor's statement reflect institutional positioning vis-a-vis the government. Cross-reference with The Economic Times (market interpretation), LiveMint (policy analysis), and Gateway House (geo-economic implications of rupee internationalization).
- **Finance Ministry**: Budget allocations and Economic Survey analysis are generally reliable in headline numbers but presentation framing (base year selection, nominal vs. real comparisons) can obscure trends. Cross-reference with LiveMint and The Economic Times. Defence budget analysis requires reading the detailed demand-for-grants documents, not just the headline allocation number.
- **NITI Aayog**: Government-commissioned analysis that prefigures policy. Cross-reference with Carnegie India and ORF for independent assessment. NITI publications on technology (semiconductors, AI, digital infrastructure) signal upcoming regulatory and industrial policy directions.
- **DRDO**: Success-only reporting on weapons development. Cross-reference with FORCE Magazine and ThePrint for realistic capability assessments. Failed tests are never announced officially — they surface through media leaks.

**4.2 The PIB centralization opportunity**

Unlike Mexico's gob.mx (which hosts ministry websites), India's PIB serves as a publication clearinghouse rather than a hosting platform. This means:
- PIB RSS captures output from 50+ ministries through a single feed
- Ministry-specific filtering is available via the `mincode` parameter
- PIB often publishes releases before the originating ministry's website updates
- However, PIB releases may omit attachments, data tables, and technical annexes that exist on the originating ministry's site
- Hindi and regional-language versions of the same release may have framing differences

The optimal strategy is: monitor PIB RSS as the primary ingestion feed, then fetch the originating ministry's site for additional context when a PIB release is flagged as relevant.

**4.3 The intelligence silence problem**

India's intelligence community (RAW, IB, NTRO, NSCS) produces zero public communications. This is a structural gap that cannot be filled by monitoring. Intelligence-relevant signals surface through:
- PMO/PIB references to "NSA-level" discussions or CCS (Cabinet Committee on Security) decisions
- MEA spokesperson responses that reference "intelligence inputs" or "security concerns"
- Defence correspondents' attributed quotes from "senior security officials" (ThePrint, The Hindu, Hindustan Times)
- Parliamentary Standing Committee reports on Defence and Home Affairs (when tabled)
- Gazette notifications of organizational/budget changes to intelligence agencies
- Ajit Doval's rare public statements — each is a deliberate strategic signal

The pipeline should not allocate resources to polling for NSCS/RAW content but should flag any NSA statement (via PMO or attributed media quotes) as high-priority.

**4.4 Legislative gap: committee proceedings**

The existing Source Intelligence Map identifies parliamentary transcripts as a potential signal source. The Standing Committee on External Affairs and the Standing Committee on Defence produce the most detailed parliamentary scrutiny of foreign and defence policy available in India. However:
- Committee reports are tabled in Parliament but not always digitized promptly
- The reports themselves are available through Parliament Library services but with variable lag
- Committee testimony from MEA, MoD, and RBI officials contains details that no media outlet fully covers
- The Rajya Sabha debate archive (`rsdebate.nic.in`) is the most accessible parliamentary text corpus, with full-text search across 741,000+ entries from 1952 to present

Prioritize: (a) Standing Committee on External Affairs reports, (b) Standing Committee on Defence reports, (c) Question Hour exchanges with MEA and MoD ministers, (d) Budget discussion transcripts on defence allocation.

**4.5 The bilingual framing signal**

India's government uniquely publishes in both English and Hindi (with PIB covering 14 languages total). This creates a systematic analytical opportunity:
- English versions target policymakers, diplomats, media, and international audiences
- Hindi versions target the mass electorate and domestic political stakeholders
- Differences in emphasis, word choice, and framing between the two versions reveal how the government calibrates messaging for different constituencies
- For example, defence cooperation agreements with the US may be framed in English as "deepening strategic partnership" while the Hindi version emphasizes "Atmanirbhar Bharat" (self-reliance) to reassure domestic audiences concerned about dependency
- This bilingual delta analysis requires Hindi-language NLP capability in the pipeline

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 PIB as Primary Ingestion Layer

PIB is the single most important government ingestion point for India — a single RSS subscription captures output from all central ministries. The recommended architecture:

1. **Primary feed**: Poll PIB RSS (English) every 60 minutes: `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3`
2. **Hindi feed**: Poll PIB RSS (Hindi) every 60 minutes: `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3`
3. **Release detail**: For each new item, fetch full text at `https://pib.gov.in/PressReleseDetail.aspx?PRID={id}`
4. **Ministry classification**: Extract ministry attribution from release header for routing to domain-specific analysis
5. **Supplementary fetch**: For P1 releases (MoD, MEA, PMO), also fetch the originating ministry's site for attachments and context

### 5.2 RSS-Enabled Sources (Priority for Automation)

Only two government source categories provide functional RSS feeds:

1. **PIB**: Three feeds (press releases, photos, media advisories) in English and Hindi. ASP.NET-generated RSS. This is the most operationally useful feed — it provides cross-ministry coverage through a single endpoint.

2. **RBI**: Five feeds (press releases, notifications, speeches, publications, tenders). XML-based RSS. Well-maintained and reliable. Press releases and notifications feeds are the most pipeline-relevant. The notifications feed captures regulatory changes affecting banking, forex, and capital markets.

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Four sources publish primarily or substantially in PDF:
- **Gazette of India**: All notifications are PDF. Text-based PDFs for recent publications (post-2015 digitization mandate). Gazette ID in filename enables deduplication.
- **RBI**: Monetary policy statements, MPC minutes, and quarterly reports are multi-page PDF. Well-structured, text-based.
- **Finance Ministry**: Union Budget documents, Economic Survey, and demand-for-grants are PDF. Table-heavy — require table extraction (tabula/camelot). Available at `indiabudget.gov.in`.
- **Parliamentary debates**: Lok Sabha and Rajya Sabha verbatim transcripts are PDF. Long-form documents (100+ pages per session day). Hindi/English mixed content.

### 5.4 Language and Encoding

Government sources publish primarily in English and Hindi. PIB provides content in 14 languages. Key considerations:
- All NIC-hosted sites serve UTF-8 encoded content
- Hindi content uses Devanagari script (Unicode block U+0900-U+097F)
- MEA bilateral documents may include third-language versions (French, Arabic, Russian, Chinese for respective partner countries)
- PIB Hindi releases use standard Hindi (`hi-IN` locale) — no significant dialectal variation
- Parliamentary debates contain code-switching between Hindi and English (common in Indian political discourse) — NLP pipeline must handle mixed-language text

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A PM foreign visit readout appears on PMO site, MEA site, and PIB (potentially in all 14 languages)
- Defence procurement approvals appear on MoD, PIB (MoD mincode), and sometimes individual service branch sites
- RBI monetary policy decisions appear on RBI press releases, PIB, and Finance Ministry references
- Legislative acts appear in the Gazette, PIB, and the relevant ministry's site

Implement content-hash deduplication. Use the originating agency as canonical: MEA for diplomatic, MoD for defence, RBI for monetary policy, Gazette for legal text. Use PIB as the discovery/triage layer, not the canonical source.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | PIB (RSS), MEA, PMO | Every 1-2 hours | Highest volume, policy-critical, real-time diplomatic signals |
| P1-Standard | MoD, Indian Army, Indian Navy, IAF | Every 4 hours | Lower frequency but high-priority when published |
| P2-Active | RBI (RSS), Finance, Commerce, Lok Sabha, Rajya Sabha | Every 6 hours | Regular publishing schedule, economic data |
| P2-Low | Gazette, NITI Aayog, DRDO, Sansad TV | Every 12 hours | Important but slower publication cycle |
| P2-Minimal | NSCS/RAW | Weekly | No public output; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| NIC infrastructure outage | All *.nic.in domains (Army, Navy, IAF, Lok Sabha, Rajya Sabha, Sansad TV) | PIB carries most ministry releases. Monitor @SpokespersonMoD, @MEAIndia, @PMOIndia on X for real-time communications. Government social media often precedes web publication. |
| mod.gov.in connectivity failure | MoD | PIB (mincode=33) for press releases. @SpokespersonMoD on X. |
| finmin.nic.in connectivity failure | Finance Ministry | PIB (mincode=7). @FinMinIndia on X. Department sub-portals (dea.gov.in, doe.gov.in) may remain accessible. |
| PIB RSS feed malfunction | PIB (primary feed) | Fall back to HTML scraping of `pib.gov.in/allRel.aspx`. Mobile endpoint at `AllReleasem.aspx` as secondary fallback. |
| egazette.gov.in unavailability | Gazette of India | National Archives gazette notifications at `nationalarchives.nic.in`. Gazette PDFs are also archived on Internet Archive (`archive.org/details/in.gazette`). |
| RBI RSS feed disruption | RBI | HTML scraping of `rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx`. RBI site is generally the most reliable government site. |
| Parliamentary site maintenance | Lok Sabha, Rajya Sabha | Digital Sansad (`sansad.in`) as alternative portal. Parliament Digital Library at `eparlib.sansad.in`. Sansad TV for proceedings video. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of NIC infrastructure, change in government administration, creation/dissolution of ministries, or changes to PIB's publication architecture. The bilingual monitoring capability (English + Hindi) should be tested against PIB's dual-language output during each review cycle.*
