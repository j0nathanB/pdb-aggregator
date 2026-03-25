# Official Government Sources Supplement: UKRAINE

**Primary language of political discourse: Ukrainian**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Ukraine (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Ukraine. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds and APIs, and provides the YAML manifest for pipeline integration.

Ukraine's government web infrastructure is decentralized — unlike Mexico's unified gob.mx platform, each Ukrainian ministry and state body maintains its own independent website under the `.gov.ua` top-level domain. This creates heterogeneous extraction requirements but also eliminates single-point-of-failure risk. A critical structural feature of Ukraine's government communications since February 2022 is the deliberate maintenance of parallel English-language editions across most major government websites. This reflects a wartime strategic communications posture designed to sustain international support, and means that many government sources can be ingested directly without machine translation. Under martial law, presidential communications carry outsized policy weight relative to parliament and cabinet — the Office of the President functions as the de facto center of gravity for all foreign policy, defense, and security messaging.

---

## 1. OFFICIAL GOVERNMENT SOURCES: UKRAINE

### 1.1 Head of Government — Office of the President of Ukraine

| Field | Detail |
|---|---|
| **Institution** | Office of the President of Ukraine (Офіс Президента України) |
| **Domain** | `president.gov.ua` |
| **Entry Point URL** | `https://www.president.gov.ua/en/news/all` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** All news: `https://www.president.gov.ua/en/rss/news/all.rss`. Speeches: `https://www.president.gov.ua/en/rss/news/speeches.rss`. Administration news: `https://www.president.gov.ua/en/rss/news/administration.rss`. Documents/decrees: `https://www.president.gov.ua/en/rss/documents/all.rss`. Ukrainian-language equivalents at `/rss/news/all.rss` (without `/en/`). |
| **Language** | Ukrainian (primary), English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints, Institutional engagement |
| **Publication Frequency** | Multiple times daily. Presidential addresses, decree texts, meeting readouts, NSDC decision announcements, and nightly video addresses published same-day. During active diplomatic periods, 10-20 items per day. |
| **Content Format** | HTML (articles with embedded video for nightly addresses). Decree texts in HTML. Some formal documents as PDF attachments. |
| **Extraction Method** | RSS feeds (preferred — well-structured, multiple category-specific feeds). HTML scraping as fallback. |
| **Editorial Orientation** | Official presidential position. All content produced by the Office of the President's communications team. Under martial law, this is the single most authoritative source for Ukraine's strategic posture. Framing reflects wartime unity messaging and international advocacy priorities. |
| **Why This Source** | Under martial law, the President exercises expanded executive authority. Presidential addresses, NSDC decisions enacted by presidential decree, bilateral meeting readouts, and the nightly video address collectively define Ukraine's official posture on war, diplomacy, reconstruction, and institutional reform. The nightly address is the single most-watched political communication in Ukraine and frequently contains forward-looking signals on diplomatic and military strategy. |
| **Access Notes** | No paywall, no authentication. English edition is comprehensive and maintained in near-real-time (1-3 hour lag for most content, nightly addresses often subtitled same-evening). RSS feeds are well-structured and reliable. Newsletter subscription available at `president.gov.ua/en/subscribe`. Some pages return 403 to automated fetchers — rotating User-Agent headers recommended. |

**Additional entry points:**
- Nightly video addresses: filtered via "Speeches" category or RSS feed `speeches.rss`
- Presidential decrees and orders: `https://www.president.gov.ua/en/documents/decrees` and RSS at `documents/all.rss`
- NSDC decisions (enacted by presidential decree): appear in both news and documents sections
- Zelensky Telegram channel: `https://t.me/V_Zelenskiy_official` (Ukrainian) — often publishes 15-30 minutes before the website

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| All news (EN) | `https://www.president.gov.ua/en/rss/news/all.rss` |
| Current events (EN) | `https://www.president.gov.ua/en/rss/news/last.rss` |
| Speeches (EN) | `https://www.president.gov.ua/en/rss/news/speeches.rss` |
| Administration news (EN) | `https://www.president.gov.ua/en/rss/news/administration.rss` |
| Documents (EN) | `https://www.president.gov.ua/en/rss/documents/all.rss` |
| All news (UK) | `https://www.president.gov.ua/rss/news/all.rss` |

---

### 1.2 Foreign Ministry — Ministry of Foreign Affairs of Ukraine (MFA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Foreign Affairs of Ukraine (Міністерство закордонних справ України) |
| **Domain** | `mfa.gov.ua` |
| **Entry Point URL** | `https://mfa.gov.ua/en/press-center` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS at `mfa.gov.ua/en/rss` or `/feed`] |
| **Language** | Ukrainian (primary), English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Comunicados issued for bilateral meetings, multilateral positioning, sanctions advocacy, Peace Formula diplomacy, EU accession benchmarks, and consular emergencies. Higher frequency during diplomatic summits and UN General Assembly sessions. |
| **Content Format** | HTML. Press statements, minister speeches, and bilateral meeting readouts. Some formal diplomatic notes in PDF. |
| **Extraction Method** | HTML scraping of press center pages. The MFA site uses a modern CMS with structured URL patterns. |
| **Editorial Orientation** | Official foreign ministry position. Under Foreign Minister Andrii Sybiha, communications emphasize the Peace Formula, EU and NATO integration, bilateral security agreements, and sanctions enforcement. English-language output is strategically calibrated for international audiences. |
| **Why This Source** | The only primary source for Ukraine's formal diplomatic positions, bilateral agreement texts, ambassador appointments, multilateral voting explanations, and Peace Formula progress updates. Media coverage of MFA activity is invariably derived from these communications. Divergence between MFA and presidential messaging (rare but significant) signals internal policy tension. |
| **Access Notes** | No paywall. English edition comprehensive — the MFA invests heavily in English-language communications as part of wartime international advocacy. Press center subdivided into Press Office, Spokesperson statements, and Minister activity. Social media presence: @MFA_Ukraine (X), @UkraineMFA (Facebook). Some pages return 403 to automated fetchers. |

**Additional entry points:**
- Press Office statements: `https://mfa.gov.ua/en/press-center/press-office`
- Minister activity/speeches: `https://mfa.gov.ua/en/press-center`
- Embassy-level communications: individual embassy websites (e.g., `usa.mfa.gov.ua`, `uk.mfa.gov.ua`)
- Consular affairs: `https://mfa.gov.ua/en/consular-affairs`

---

### 1.3 Defense / Security — Ministry of Defence, General Staff, Armed Forces

#### 1.3a Ministry of Defence of Ukraine (MoD)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Defence of Ukraine (Міністерство оборони України) |
| **Domain** | `mod.gov.ua` |
| **Entry Point URL** | `https://mod.gov.ua/en/news` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS at `mod.gov.ua/en/rss` or `/feed`] |
| **Language** | Ukrainian, English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Daily. 3-10 items per day covering weapons authorization, procurement, defense industry partnerships, welfare/social protection of military, digitalization, and institutional reform. |
| **Content Format** | HTML. News articles with embedded images. Some statistical reports in attached documents. |
| **Extraction Method** | HTML scraping of news listing page at `mod.gov.ua/en/news`. Modern CMS with clean URL structure. |
| **Editorial Orientation** | Official defense ministry communication. Under Minister Mykhailo Fedorov (appointed 2025), communications emphasize defense-tech innovation, domestic weapons production scaling, drone warfare capabilities, and NATO interoperability. Operational details are constrained by wartime OPSEC. |
| **Why This Source** | The MoD is the primary source for defense procurement policy, weapons authorization data (over 1,300 new models authorized in 2025), defense industry licensing, international defense cooperation agreements, and military welfare policy. Unlike the General Staff (operational focus), the MoD covers the institutional and industrial dimensions of defense. |
| **Access Notes** | No paywall. English edition well-maintained. Press section at `mod.gov.ua/en/press`. The MoD website was redesigned in 2024-2025 — legacy URLs from the old `mil.gov.ua` domain may no longer resolve. |

**Additional entry points:**
- Press/media section: `https://mod.gov.ua/en/press`
- General Staff page (within MoD): `https://mod.gov.ua/en/about-us/the-general-staff-of-the-armed-forces-of-ukraine`
- Defense procurement/industry: filtered within news section

#### 1.3b General Staff of the Armed Forces of Ukraine

| Field | Detail |
|---|---|
| **Institution** | General Staff of the Armed Forces of Ukraine (Генеральний штаб Збройних сил України) |
| **Domain** | `zsu.gov.ua` (official AFU site) / Facebook: `facebook.com/GeneralStaff.ua` |
| **Entry Point URL** | `https://www.zsu.gov.ua/en` (institutional) / `https://www.facebook.com/GeneralStaff.ua` (operational updates) |
| **RSS/Atom Feed** | None available. Operational updates published primarily via Facebook and Telegram. |
| **Language** | Ukrainian (primary); English translations of operational summaries posted on Facebook |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | **Twice daily** — morning (06:00 Kyiv) and evening (18:00 Kyiv) operational situation reports. Additional ad hoc statements on significant operational developments. |
| **Content Format** | Facebook posts (text with infographics showing Russian losses). The zsu.gov.ua website is more institutional (leadership, force structure, vision documents) than operational. |
| **Extraction Method** | Facebook page scraping or Facebook Graph API for operational updates. HTML scraping of zsu.gov.ua for institutional content. X/Twitter (@GeneralStaffUA) mirrors Facebook content. |
| **Editorial Orientation** | Official military communication. Daily operational summaries report Russian losses (personnel, equipment by category) and frontline engagement counts. These figures are consistently higher than independent estimates but the trends are directionally informative. Operational failures, Ukrainian casualties, and territorial losses are systematically omitted. |
| **Why This Source** | The twice-daily General Staff briefing is the foundational document for all frontline reporting in Ukraine. Every media outlet, think tank (ISW, DeepState), and OSINT analyst references these briefings. The reported Russian loss figures, while inflated in absolute terms, provide a consistent time-series for tracking operational tempo. |
| **Access Notes** | zsu.gov.ua is the institutional website; it does not carry the daily operational briefings. Those are published on Facebook (1M+ followers) and Telegram (`t.me/GeneralStaffZSU`). The X account @GeneralStaffUA provides English translations. Automated extraction requires Facebook scraping capability or Telegram API integration. |

**Additional entry points:**
- Facebook (primary for operational updates): `https://www.facebook.com/GeneralStaff.ua`
- X/Twitter (English): `https://x.com/GeneralStaffUA`
- Telegram (Ukrainian, fastest): `https://t.me/GeneralStaffZSU`
- Institutional website: `https://www.zsu.gov.ua/en`

#### 1.3c Armed Forces of Ukraine (ZSU) — Institutional Website

| Field | Detail |
|---|---|
| **Institution** | Armed Forces of Ukraine (Збройні сили України / ZSU) |
| **Domain** | `zsu.gov.ua` |
| **Entry Point URL** | `https://www.zsu.gov.ua/en` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Ukrainian, English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Irregular — institutional content (leadership changes, force structure, strategic vision documents) published as needed rather than on a daily cycle. |
| **Content Format** | HTML. Long-form strategic documents (e.g., "Vision of the General Staff on the development of the Armed Forces for the next 10 years"). |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | Institutional military communication. Strategic vision documents and leadership profiles. |
| **Why This Source** | The zsu.gov.ua website provides the institutional and strategic layer — force modernization plans, NATO interoperability roadmaps, and leadership biographies — that complements the General Staff's operational daily briefings. The 10-year development vision document is a key strategic planning signal. |
| **Access Notes** | Modern website launched 2024. Services section includes portals for military personnel and families. |

---

### 1.4 Parliament — Verkhovna Rada of Ukraine

| Field | Detail |
|---|---|
| **Institution** | Verkhovna Rada of Ukraine (Верховна Рада України) |
| **Domain** | `rada.gov.ua` |
| **Entry Point URL** | `https://www.rada.gov.ua/en/news/` |
| **RSS/Atom Feed** | Committee news RSS feeds available. [VERIFY specific feed URLs at `rada.gov.ua/rss`] |
| **Language** | Ukrainian (primary), English (limited — news section only; legislation in Ukrainian) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily during session periods. Reduced during recess. Under martial law with elections suspended (since 2022), parliamentary activity is a signal of institutional normalcy and reform momentum. |
| **Content Format** | HTML (news articles, draft legislation summaries). Legislation database at `zakon.rada.gov.ua` provides full text of laws. Open Data Portal at `data.rada.gov.ua` provides structured datasets. |
| **Extraction Method** | HTML scraping of news pages. Legislation database scraping at `zakon.rada.gov.ua`. Open Data Portal API for structured data (voting records, bill tracking). |
| **Editorial Orientation** | Institutional. Under martial law, the Rada operates with reduced pluralism — the ruling Servant of the People party dominates. Committee proceedings on EU accession legislation, defense budgets, and mobilization law are the primary analytical interest. |
| **Why This Source** | Legislative texts, committee hearing records, and voting records. The Rada's legislative output on EU accession harmonization (hundreds of bills required across negotiation clusters) is a quantifiable indicator of institutional reform momentum. Mobilization law debates and defense budget votes reveal domestic constraint dynamics. |
| **Access Notes** | English section limited to news; all legislation in Ukrainian. The portal notes it is still being tested and some functions may be unavailable. |

**Additional entry points:**
- Legislation database: `https://zakon.rada.gov.ua/laws?lang=en`
- Draft legislation: `https://www.rada.gov.ua/en/news/draft_legislation/`
- Documents: `https://www.rada.gov.ua/en/documents/`
- Open Data Portal: `https://data.rada.gov.ua/open/data/nd/en/`
- Research Service: `https://research.rada.gov.ua/en/documents/`
- Bill tracking (ITD system): `https://itd.rada.gov.ua`

---

### 1.5 Official Gazette — Ofitsiyniy Visnyk Ukrayiny / Uryadoviy Kuryer

| Field | Detail |
|---|---|
| **Institution** | Official Herald of Ukraine (Офіційний вісник України) and Government Courier (Урядовий кур'єр) |
| **Domain** | `zakon.rada.gov.ua` (legislation database) / `ukurier.gov.ua` (Government Courier) |
| **Entry Point URL** | `https://zakon.rada.gov.ua/laws/main/en/index` (legislation database — primary access point for official texts) |
| **RSS/Atom Feed** | None available. |
| **Language** | Ukrainian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the official gazette is the constitutional publication vehicle for all laws, presidential decrees, Cabinet resolutions, and international agreements |
| **Publication Frequency** | Daily. The Ofitsiyniy Visnyk Ukrayiny is a daily collection of legislative acts. Uryadoviy Kuryer (Government Courier) is the national daily newspaper of the executive branch, publishing presidential and ministerial decrees and parliamentary laws. |
| **Content Format** | HTML on `zakon.rada.gov.ua` (searchable database with full text of legislation). Uryadoviy Kuryer is a newspaper format (print and digital). |
| **Extraction Method** | Database search and scraping at `zakon.rada.gov.ua`. The legislation database is the most comprehensive and machine-accessible format for Ukrainian official texts. Date-range filtering and full-text search available. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, decree, or international agreement is legally binding until published in the official gazette. The `zakon.rada.gov.ua` database is the definitive, searchable repository. Media reports on legislation are always downstream of gazette publication. Under martial law, presidential decrees and NSDC decisions published here carry the force of law on defense, mobilization, and sanctions. |
| **Access Notes** | `zakon.rada.gov.ua` provides English abstracts for some documents but full texts are in Ukrainian. The database covers legislation from independence (1991) to present. No authentication required. Uryadoviy Kuryer at `ukurier.gov.ua` is the executive branch's official newspaper — among the top three newspapers in Ukraine by circulation. |

---

### 1.6 Finance Ministry — Ministry of Finance of Ukraine

| Field | Detail |
|---|---|
| **Institution** | Ministry of Finance of Ukraine (Міністерство фінансів України) |
| **Domain** | `mof.gov.ua` |
| **Entry Point URL** | `https://mof.gov.ua/en/news` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS at `mof.gov.ua/en/rss` or `/feed`] |
| **Language** | Ukrainian, English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week. Communications cover state budget execution, external financing (IMF/World Bank/EU disbursements), sovereign debt operations, war bond issuances, and fiscal policy announcements. Higher frequency during budget season (September-December) and IMF review periods. |
| **Content Format** | HTML (news articles). PDF for budget documents, statistical tables, and IMF program materials. Key documents include the annual State Budget, Budget Declaration, and monthly budget execution reports. |
| **Extraction Method** | HTML scraping of news listing page. PDF download and extraction for budget documents and statistical annexes. |
| **Editorial Orientation** | Official fiscal policy position. Data-heavy, technical language. Under wartime conditions, communications emphasize defense spending adequacy, external financing mobilization, and fiscal resilience. The 2025 budget allocated 26.3% of GDP to security and defense (UAH 2.23 trillion). |
| **Why This Source** | Primary source for state budget data, external financing flows ($52.4B secured in 2025), IMF program compliance, sovereign debt operations, and fiscal sustainability indicators. Essential for Economic & Technological Statecraft domain — all media reporting on Ukraine's fiscal position derives from MoF data. The wartime fiscal position is a leading indicator of Ukraine's capacity to sustain military operations. |
| **Access Notes** | No paywall. English edition well-maintained. Budget documents published as downloadable PDFs (e.g., `mof.gov.ua/storage/files/Ukraine%20State%20Budget%202025.pdf`). |

**Additional entry points:**
- Budget 2025 page: `https://mof.gov.ua/en/budget_of_2025-770`
- Budget Declaration 2025-2027: `https://mof.gov.ua/en/budget_declaration_for_2025-2027-733`
- State Budget financing tracker (wartime): available via news section

---

### 1.7 Central Bank — National Bank of Ukraine (NBU)

| Field | Detail |
|---|---|
| **Institution** | National Bank of Ukraine (Національний банк України / NBU) |
| **Domain** | `bank.gov.ua` |
| **Entry Point URL** | `https://bank.gov.ua/en/news/all` (news) / `https://bank.gov.ua/en/monetary` (monetary policy) |
| **RSS/Atom Feed** | None confirmed for news/press releases. However, the NBU provides a comprehensive **REST API** for structured data (see below). |
| **Language** | Ukrainian, English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (scheduled). Key policy rate press briefings follow each decision. Inflation reports: quarterly. News/communications: multiple times weekly. API data: daily/real-time updates for exchange rates, reserves, and financial market indicators. |
| **Content Format** | HTML for news and press briefings. PDF for monetary policy decisions, inflation reports, and financial stability reports. **REST API** for structured data (JSON/XML). |
| **Extraction Method** | REST API (preferred for structured data — exchange rates, key policy rate, reserves). HTML scraping for news articles and press briefing texts. PDF extraction for formal policy documents. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Andriy Pyshnyy, the NBU has maintained institutional credibility through wartime conditions — managing exchange rate flexibility, capital controls, and inflation targeting under extreme stress. |
| **Why This Source** | The NBU is the only source for authoritative monetary policy decisions, official exchange rates, international reserve levels, inflation data, and banking sector statistics. Its REST API is the most machine-friendly government data source in Ukraine. Under wartime conditions, NBU decisions on exchange rate policy, capital controls, and reserve management are critical indicators of economic sustainability. |
| **Access Notes** | No paywall. No bot protection observed on API endpoints. English-language site comprehensive. API documentation at `bank.gov.ua/en/open-data/api-dev`. All API endpoints support JSON (append `&json` parameter) and XML (default). |

**Key API endpoints:**
| Data | URL |
|---|---|
| Exchange rates (current) | `https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange` |
| Exchange rate (specific date) | `https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=YYYYMMDD` |
| Exchange rate (by currency) | `https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=YYYYMMDD` |
| Reference rate (12:00 fix) | `https://bank.gov.ua/NBUStatService/v1/statdirectory/dollar_info` |
| Key policy rate | `https://bank.gov.ua/NBUStatService/v1/statdirectory/key?date=YYYYMMDD` |
| UONIA (overnight rate) | `https://bank.gov.ua/NBU_uonia?id_api=UONIA_UnsecLoansDepo` |
| Government bonds (OVDP) | `https://bank.gov.ua/NBU_ovdp` |

**Additional entry points:**
- Statistics hub: `https://bank.gov.ua/en/statistic`
- Monetary policy instruments: `https://bank.gov.ua/en/monetary/tools`
- Financial sector statistics: `https://bank.gov.ua/en/statistic/sector-financial`
- External sector statistics: `https://bank.gov.ua/en/statistic/sector-external`
- Open data / API documentation: `https://bank.gov.ua/en/open-data/api-dev`

---

### 1.8 Trade / Economy — Ministry of Economy of Ukraine

| Field | Detail |
|---|---|
| **Institution** | Ministry of Economy of Ukraine (Міністерство економіки України) |
| **Domain** | `me.gov.ua` |
| **Entry Point URL** | `https://me.gov.ua/?lang=en-GB` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Ukrainian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Communications cover trade policy, EU integration economic benchmarks, reconstruction economics, agricultural trade (since July 2025 merger with Ministry of Agrarian Policy), investment climate, and sanctions implementation. |
| **Content Format** | HTML (news articles). PDF for trade statistics and policy documents. |
| **Extraction Method** | HTML scraping. The site uses GUID-based URLs for individual news items (e.g., `me.gov.ua/News/Detail?lang=en-GB&id={GUID}`). |
| **Editorial Orientation** | Official economic policy position. Emphasizes EU accession economic reforms, trade diversification away from Russian markets, reconstruction investment attraction, and agricultural export facilitation. |
| **Why This Source** | Primary source for trade policy announcements, EU accession economic harmonization progress, agricultural trade policy (critical given Ukraine's role as global grain exporter), reconstruction investment frameworks, and bilateral economic partnerships. The July 2025 merger absorbing the Ministries of Agrarian Policy and Environment expanded its portfolio significantly. |
| **Access Notes** | No paywall. English edition available but less comprehensive than MFA or President — some news items are Ukrainian-only. URL structure uses GUIDs rather than slugs, making URL prediction impossible; listing page scraping is required. |

---

### 1.9 Intelligence / National Security — SBU, GUR, NSDC (RNBO)

#### 1.9a Security Service of Ukraine (SBU / SSU)

| Field | Detail |
|---|---|
| **Institution** | Security Service of Ukraine (Служба безпеки України / SBU) |
| **Domain** | `ssu.gov.ua` (also accessible via `sbu.gov.ua`) |
| **Entry Point URL** | `https://ssu.gov.ua/en` |
| **RSS/Atom Feed** | None available. |
| **Language** | Ukrainian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | 3-7 per week. Operational press releases cover counterintelligence operations, counter-sabotage, FSB agent detentions, sanctions enforcement, and counter-recruitment campaigns targeting Russian intelligence activities. |
| **Content Format** | HTML. Press releases often include operational photographs and video (especially for seizures, detentions, and drone strike compilations). |
| **Extraction Method** | HTML scraping. The SBU site uses a modern CMS. |
| **Editorial Orientation** | Official security service communication. Under wartime conditions, the SBU has become significantly more public-facing than pre-2022, actively publishing operational results to demonstrate effectiveness and deter Russian intelligence recruitment. The Special Operations Centre "Alpha" regularly releases strike compilations. |
| **Why This Source** | The SBU provides the only official window into counterintelligence operations, internal security threats, sanctions enforcement actions, and the scale of Russian intelligence penetration attempts. Operational tempo (frequency and type of reported operations) is itself an analytical signal. The SBU's counter-recruitment campaigns targeting Ukrainian teenagers indicate the scale of Russian intelligence targeting of civilian populations. |
| **Access Notes** | Both `ssu.gov.ua` and `sbu.gov.ua` resolve to the same site. English edition available. Press center contact: `pressinfo@ssu.gov.ua`. Spokesperson: Artem Dekhtiarenko. Facebook: `facebook.com/SecurSerUkraine`. |

#### 1.9b Defence Intelligence of Ukraine (GUR / HUR)

| Field | Detail |
|---|---|
| **Institution** | Defence Intelligence of Ukraine (Головне управління розвідки / GUR) |
| **Domain** | `gur.gov.ua` |
| **Entry Point URL** | `https://gur.gov.ua/en/content/list-of-news/791.html` |
| **RSS/Atom Feed** | None available. |
| **Language** | Ukrainian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-5 per week. Publications include intelligence assessments (publicly released), operational reports, intercepted communications (selectively), and strategic analysis of Russian military capabilities and intentions. |
| **Content Format** | HTML. Articles, interviews, and video content. The operations section documents specific military intelligence operations. |
| **Extraction Method** | HTML scraping. The site uses a static-style CMS with numbered content URLs. |
| **Editorial Orientation** | Military intelligence communication. Under former chief Kyrylo Budanov (now Head of the Office of the President), GUR became unusually public-facing — a wartime anomaly for an intelligence service. Communications include strategic assessments designed to shape international perception of Russian vulnerabilities and Ukrainian operational capability. |
| **Why This Source** | GUR provides unique intelligence-derived assessments of Russian military capacity, force structure, equipment losses, and strategic intentions. Its public assessments on topics like Russian mobilization capacity, North Korean troop deployments, and Arctic military expansion are cited by Western intelligence communities and media. The operations section documents behind-the-lines activities. |
| **Access Notes** | No paywall. English edition maintained. X/Twitter: @DI_Ukraine. The GUR's public communications posture is unusually open for an intelligence agency — a deliberate wartime information warfare strategy. Note: as of July 2025, Budanov moved to Head of the Office of the President; current GUR chief Oleh Ivashchenko has maintained the public communications approach. |

**Additional entry points:**
- News: `https://gur.gov.ua/en/content/list-of-news/791.html`
- Operations: `https://gur.gov.ua/en/content/list-of-operations.html`
- Articles/analysis: `https://gur.gov.ua/en.html`

#### 1.9c National Security and Defence Council of Ukraine (NSDC / RNBO)

| Field | Detail |
|---|---|
| **Institution** | National Security and Defence Council of Ukraine (Рада національної безпеки і оборони України / RNBO) |
| **Domain** | `rnbo.gov.ua` |
| **Entry Point URL** | `https://www.rnbo.gov.ua/en/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Ukrainian, English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment, Domestic constraints |
| **Publication Frequency** | Irregular — driven by NSDC meeting schedule and specific policy decisions. 1-5 per week on average, with clusters around NSDC meetings and sanctions list updates. |
| **Content Format** | HTML. NSDC decisions are published as news items; the binding legal text appears as presidential decrees on `president.gov.ua`. |
| **Extraction Method** | HTML scraping. The site uses a relatively static template. URL pattern: `rnbo.gov.ua/en/Diialnist/{id}.html`. |
| **Editorial Orientation** | Official national security coordination body. Under martial law, the NSDC's role has expanded — its decisions, enacted by presidential decree, carry the force of law on sanctions, defense coordination, cybersecurity, and national security policy. |
| **Why This Source** | The NSDC is the constitutional coordination body for national security and defense policy under the President. Its decisions — particularly on sanctions (including the State Register of Sanctions), cybersecurity strategy, and defense sector coordination — are enacted as binding presidential decrees. NSDC sanctions list updates affect international enforcement and Russia-targeting policy. |
| **Access Notes** | No paywall. English edition available but less comprehensive than Ukrainian. As of July 2025, NSDC Secretary is Rustem Umerov (formerly Defense Minister). The NSDC also houses the National Cybersecurity Coordination Center (NCCC). |

**Additional entry points:**
- Activities/decisions: `https://www.rnbo.gov.ua/en/Diialnist/`
- State Register of Sanctions: referenced in NSDC decisions, accessible via `sanctions.nsdc.gov.ua` [VERIFY URL]
- National Cybersecurity Coordination Center: within RNBO structure

---

### 1.10 Country-Specific Institutions

#### 1.10a Energoatom (National Nuclear Energy Generating Company)

| Field | Detail |
|---|---|
| **Institution** | NNEGC Energoatom (НАЕК "Енергоатом") |
| **Domain** | `energoatom.com.ua` |
| **Entry Point URL** | `https://energoatom.com.ua/en` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Ukrainian, English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. News covers nuclear plant operations, Zaporizhzhia NPP occupation status, safety incidents, fuel supply diversification (away from Russian TVEL fuel), and international nuclear cooperation. |
| **Content Format** | HTML. News categories include Company news, ZNPP (Zaporizhzhia) news, KhNPP (Khmelnytskyi) news, SUNPP (South Ukraine) news, and RNPP (Rivne) news. |
| **Extraction Method** | HTML scraping. The site was redesigned recently — legacy content at `old.energoatom.com.ua`. |
| **Editorial Orientation** | State enterprise communication. Emphasizes operational continuity under wartime conditions, nuclear safety, and fuel supply diversification from Russia to Western suppliers (Westinghouse, Orano). Zaporizhzhia NPP communications are shaped by the occupation context and IAEA monitoring. |
| **Why This Source** | Energoatom operates 4 NPPs with 15 reactors providing approximately 55% of Ukraine's electricity — making nuclear energy a critical wartime infrastructure issue. The Zaporizhzhia NPP (Europe's largest nuclear plant) remains under Russian occupation, creating a persistent nuclear safety crisis monitored by the IAEA. Fuel supply diversification from Russian to Western sources is a major energy security indicator. Orano enrichment services agreement signed March 2025. |
| **Access Notes** | No paywall. English edition available. LinkedIn presence active. Legacy site at `old.energoatom.com.ua/app-eng/`. |

#### 1.10b Naftogaz Group

| Field | Detail |
|---|---|
| **Institution** | Naftogaz of Ukraine (НАК "Нафтогаз України") |
| **Domain** | `naftogaz.com` |
| **Entry Point URL** | `https://www.naftogaz.com/en/news` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS at `naftogaz.com/en/rss` or `/feed`] |
| **Language** | Ukrainian, English (comprehensive) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Communications cover gas production, gas trading and storage, energy infrastructure attacks, financial results, and international energy partnerships. |
| **Content Format** | HTML. News articles categorized by topic (gas production, gas trading, etc.). Financial reports in PDF. Press center at `/en/press_center`. Current releases at `/en/current-releases`. |
| **Extraction Method** | HTML scraping of news listing page. |
| **Editorial Orientation** | State enterprise communication. Emphasizes energy security, European gas market integration, infrastructure resilience under Russian attacks, and corporate governance reform. Under CEO Serhii Koretskyi (appointed April 2025). |
| **Why This Source** | Naftogaz is Ukraine's largest state-owned company and the national oil and gas operator. Its communications are essential for tracking energy security (Russian attacks on gas infrastructure — 6 attacks in a single week reported January 2026), European energy market integration (ORLEN gas supply contract), underground gas storage utilization (critical for European energy security), and corporate governance reform (a key EU accession benchmark). Net profit UAH 38B in 2024, up 64% from 2023. EIB lent EUR 300M for energy resilience. |
| **Access Notes** | No paywall. English edition comprehensive and well-maintained. Naftogaz has invested in professional English-language corporate communications for investor relations and international partnership purposes. |

**Additional entry points:**
- News by category: `https://www.naftogaz.com/en/news/category/gas-production`, `/gas-trading`, etc.
- Press center / media: `https://www.naftogaz.com/en/press_center`
- Current releases: `https://www.naftogaz.com/en/current-releases`

#### 1.10c Ukrenergo (National Power Company)

| Field | Detail |
|---|---|
| **Institution** | NPC Ukrenergo (НЕК "Укренерго") |
| **Domain** | `ua.energy` |
| **Entry Point URL** | `https://ua.energy/en/` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Ukrainian, English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Security & defense autonomy |
| **Publication Frequency** | 2-5 per week. News covers grid operations, Russian attacks on energy infrastructure, power system balance, European grid synchronization (ENTSO-E), and infrastructure restoration. |
| **Content Format** | HTML. News articles with operational data on power system status. |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | State enterprise communication. Ukrenergo is the transmission system operator — its communications on grid status, scheduled/emergency outages, and infrastructure damage are operationally significant rather than merely promotional. |
| **Why This Source** | Ukrenergo operates Ukraine's high-voltage electricity transmission network and is the sole TSO. It became the 40th member of ENTSO-E (European grid operator association) in January 2024, completing synchronization with the Continental European grid — a major energy sovereignty milestone. Russian systematic targeting of energy infrastructure makes Ukrenergo's operational status reports a real-time indicator of infrastructure resilience and civilian impact. |
| **Access Notes** | No paywall. English edition available. LinkedIn active. Media section at `ua.energy/for_media/`. |

#### 1.10d Cabinet of Ministers of Ukraine

| Field | Detail |
|---|---|
| **Institution** | Cabinet of Ministers of Ukraine (Кабінет Міністрів України) |
| **Domain** | `kmu.gov.ua` |
| **Entry Point URL** | `https://www.kmu.gov.ua/en` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Ukrainian, English (comprehensive parallel edition) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Cabinet coordinates executive policy across all ministries |
| **Publication Frequency** | Daily. High volume — aggregates announcements from all ministries and publishes Cabinet resolutions, government decisions, and cross-ministerial policy updates. |
| **Content Format** | HTML. Government decision search at `/en/npasearch`. Timeline format at `/en/timeline`. |
| **Extraction Method** | HTML scraping of news and timeline pages. Government decision search interface for structured queries. |
| **Editorial Orientation** | Official government executive position. Under Prime Minister Yuliia Svyrydenko, communications emphasize reconstruction, EU accession reforms, and wartime economic management. |
| **Why This Source** | The KMU portal aggregates outputs from all ministries into a single feed and publishes Cabinet resolutions that implement presidential decrees and parliamentary legislation. The General Staff daily briefings are also syndicated here. Essential for monitoring cross-ministerial policy coordination, particularly on reconstruction, EU integration, and economic stabilization. |
| **Access Notes** | No paywall. English edition comprehensive. Government decision search available at `kmu.gov.ua/en/npasearch`. |

**Additional entry points:**
- Government decisions search: `https://www.kmu.gov.ua/en/npasearch`
- Timeline: `https://www.kmu.gov.ua/en/timeline?type=posts`
- Government team: `https://www.kmu.gov.ua/en/team`

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS/API Available | Priority | Content Format | Frequency | English Edition |
|---|---|---|---|---|---|---|---|
| 1 | Office of the President | `president.gov.ua/en/news/all` | **Yes** (RSS, multiple feeds) | P1 | HTML | Multiple daily | Yes (comprehensive) |
| 2 | MFA | `mfa.gov.ua/en/press-center` | [VERIFY] | P1 | HTML/PDF | Daily | Yes (comprehensive) |
| 3a | MoD | `mod.gov.ua/en/news` | [VERIFY] | P1 | HTML | Daily (3-10/day) | Yes (comprehensive) |
| 3b | General Staff (ZSU) | `facebook.com/GeneralStaff.ua` | No (social media) | P1 | Social media posts | Twice daily | Yes (X/Twitter) |
| 3c | AFU institutional | `zsu.gov.ua/en` | [VERIFY] | P1 | HTML | Irregular | Yes |
| 4 | Verkhovna Rada | `rada.gov.ua/en/news/` | Committee RSS | P2 | HTML | Daily (session) | Limited |
| 5 | Official Gazette | `zakon.rada.gov.ua/laws/main/en/index` | No | P2 | HTML | Daily | Abstracts only |
| 6 | Ministry of Finance | `mof.gov.ua/en/news` | [VERIFY] | P2 | HTML/PDF | 3-7/week | Yes |
| 7 | NBU | `bank.gov.ua/en/news/all` | **Yes** (REST API) | P2 | HTML/PDF/API | Variable | Yes (comprehensive) |
| 8 | Ministry of Economy | `me.gov.ua/?lang=en-GB` | [VERIFY] | P2 | HTML | 2-5/week | Partial |
| 9a | SBU | `ssu.gov.ua/en` | No | P2 | HTML | 3-7/week | Yes |
| 9b | GUR | `gur.gov.ua/en.html` | No | P2 | HTML | 2-5/week | Yes |
| 9c | NSDC (RNBO) | `rnbo.gov.ua/en/` | No | P2 | HTML | 1-5/week | Yes |
| 10a | Energoatom | `energoatom.com.ua/en` | [VERIFY] | P2 | HTML | 3-7/week | Yes |
| 10b | Naftogaz | `naftogaz.com/en/news` | [VERIFY] | P2 | HTML/PDF | 3-5/week | Yes (comprehensive) |
| 10c | Ukrenergo | `ua.energy/en/` | [VERIFY] | P2 | HTML | 2-5/week | Yes |
| 10d | Cabinet of Ministers | `kmu.gov.ua/en` | [VERIFY] | P2 | HTML | Daily | Yes (comprehensive) |

---

## 3. MONITORING CONFIGURATION

```yaml
# Ukraine Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/ua.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: ua_president
    name: Office of the President of Ukraine
    domain: president.gov.ua
    entry_url: "https://www.president.gov.ua/en/news/all"
    rss_feed:
      all_news: "https://www.president.gov.ua/en/rss/news/all.rss"
      speeches: "https://www.president.gov.ua/en/rss/news/speeches.rss"
      administration: "https://www.president.gov.ua/en/rss/news/administration.rss"
      documents: "https://www.president.gov.ua/en/rss/documents/all.rss"
      all_news_uk: "https://www.president.gov.ua/rss/news/all.rss"
    language: en  # English edition as primary (UK edition via separate RSS)
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
      - institutional_engagement
    publication_frequency: multiple_daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "Multiple RSS feeds available. Nightly address is the key daily signal. Telegram (t.me/V_Zelenskiy_official) often publishes 15-30 min before website. Some pages return 403 — rotate User-Agent."

  - id: ua_mfa
    name: Ministry of Foreign Affairs of Ukraine
    domain: mfa.gov.ua
    entry_url: "https://mfa.gov.ua/en/press-center"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Peace Formula diplomacy, EU/NATO integration, bilateral security agreements. English edition comprehensive. Embassy-level releases on per-country subdomains."

  - id: ua_mod
    name: Ministry of Defence of Ukraine
    domain: mod.gov.ua
    entry_url: "https://mod.gov.ua/en/news"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Defense procurement, weapons authorization, defense industry. Redesigned 2024-2025; legacy mil.gov.ua URLs may not resolve."

  - id: ua_general_staff
    name: General Staff of the Armed Forces of Ukraine
    domain: facebook.com
    entry_url: "https://www.facebook.com/GeneralStaff.ua"
    rss_feed: null
    language: uk  # Primary in Ukrainian; English on X/Twitter
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: twice_daily
    content_format: social_media
    extraction_method: facebook_scrape_or_api
    poll_interval_hours: 2
    social_media:
      facebook: "https://www.facebook.com/GeneralStaff.ua"
      telegram: "https://t.me/GeneralStaffZSU"
      twitter: "https://x.com/GeneralStaffUA"
    notes: "Twice-daily operational briefings (06:00, 18:00 Kyiv). The foundational document for all frontline reporting. Facebook is primary; Telegram is fastest; X has English translations."

  - id: ua_zsu
    name: Armed Forces of Ukraine (institutional)
    domain: zsu.gov.ua
    entry_url: "https://www.zsu.gov.ua/en"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: irregular
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Institutional site — force structure, strategic vision, leadership. Not for daily operational updates (those are on General Staff social media)."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: ua_rada
    name: Verkhovna Rada of Ukraine
    domain: rada.gov.ua
    entry_url: "https://www.rada.gov.ua/en/news/"
    rss_feed: null  # Committee RSS feeds available [VERIFY specific URLs]
    language: uk  # English section limited
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: daily_session
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "EU accession legislation, mobilization law, defense budget. Elections suspended under martial law. Legislation DB at zakon.rada.gov.ua. Open Data at data.rada.gov.ua."

  - id: ua_gazette
    name: Official Gazette (Zakon DB / Uryadoviy Kuryer)
    domain: zakon.rada.gov.ua
    entry_url: "https://zakon.rada.gov.ua/laws/main/en/index"
    rss_feed: null
    language: uk  # English abstracts only
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Definitive searchable legislation database. All laws, decrees, resolutions. Full text in Ukrainian only; English abstracts for some documents."

  - id: ua_mof
    name: Ministry of Finance of Ukraine
    domain: mof.gov.ua
    entry_url: "https://mof.gov.ua/en/news"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "State budget, external financing ($52.4B in 2025), IMF compliance, war bonds. PDF budget documents. 26.3% of GDP to defense in 2025."

  - id: ua_nbu
    name: National Bank of Ukraine (NBU)
    domain: bank.gov.ua
    entry_url: "https://bank.gov.ua/en/news/all"
    rss_feed: null  # No RSS, but REST API available
    api:
      exchange_rates: "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
      key_policy_rate: "https://bank.gov.ua/NBUStatService/v1/statdirectory/key"
      dollar_reference: "https://bank.gov.ua/NBUStatService/v1/statdirectory/dollar_info"
      government_bonds: "https://bank.gov.ua/NBU_ovdp"
      uonia: "https://bank.gov.ua/NBU_uonia?id_api=UONIA_UnsecLoansDepo"
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_api_mixed
    extraction_method: api_poll_and_html_scrape
    poll_interval_hours: 6
    notes: "Best machine-readable government source in Ukraine. REST API for exchange rates, key rate, reserves (JSON/XML). 8 monetary policy decisions/year. API docs at bank.gov.ua/en/open-data/api-dev."

  - id: ua_economy
    name: Ministry of Economy of Ukraine
    domain: me.gov.ua
    entry_url: "https://me.gov.ua/?lang=en-GB"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Trade, EU accession economics, reconstruction investment, agricultural trade. Merged with Agrarian Policy and Environment ministries (July 2025). GUID-based URLs — listing page scraping required."

  - id: ua_sbu
    name: Security Service of Ukraine (SBU)
    domain: ssu.gov.ua
    entry_url: "https://ssu.gov.ua/en"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Counterintelligence, counter-sabotage, sanctions enforcement. Also accessible via sbu.gov.ua. Unusually public-facing for wartime security service."

  - id: ua_gur
    name: Defence Intelligence of Ukraine (GUR)
    domain: gur.gov.ua
    entry_url: "https://gur.gov.ua/en/content/list-of-news/791.html"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Intelligence-derived assessments of Russian military capacity, strategic intentions. Unusually open public communications — deliberate wartime info strategy. Current chief: Oleh Ivashchenko."

  - id: ua_nsdc
    name: National Security and Defence Council (RNBO)
    domain: rnbo.gov.ua
    entry_url: "https://www.rnbo.gov.ua/en/"
    rss_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
      - domestic_constraints
    publication_frequency: "1-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "NSDC decisions enacted as presidential decrees. Sanctions lists, cybersecurity strategy, defense coordination. Secretary: Rustem Umerov (since July 2025)."

  - id: ua_energoatom
    name: Energoatom
    domain: energoatom.com.ua
    entry_url: "https://energoatom.com.ua/en"
    rss_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "4 NPPs, 15 reactors, ~55% of Ukraine's electricity. Zaporizhzhia NPP under Russian occupation. Fuel diversification from Russia to Westinghouse/Orano."

  - id: ua_naftogaz
    name: Naftogaz Group
    domain: naftogaz.com
    entry_url: "https://www.naftogaz.com/en/news"
    rss_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Largest state company. Gas production/trading, energy infrastructure attacks, European gas storage. CEO: Serhii Koretskyi (since April 2025)."

  - id: ua_ukrenergo
    name: Ukrenergo
    domain: ua.energy
    entry_url: "https://ua.energy/en/"
    rss_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - security_defense_autonomy
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Sole electricity TSO. ENTSO-E member since Jan 2024. Grid status reports during Russian infrastructure attacks are real-time resilience indicators."

  - id: ua_kmu
    name: Cabinet of Ministers of Ukraine
    domain: kmu.gov.ua
    entry_url: "https://www.kmu.gov.ua/en"
    rss_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Aggregates all ministry outputs. Government decision search at kmu.gov.ua/en/npasearch. Syndicates General Staff briefings. PM: Yuliia Svyrydenko."

# No shared platform — each Ukrainian government body maintains independent infrastructure
# unlike Mexico's gob.mx centralization
infrastructure_notes:
  domain_pattern: "*.gov.ua for government bodies; *.com.ua for state enterprises"
  shared_platform: false
  bot_protection: "Some .gov.ua sites return 403 to automated fetchers. Rotating User-Agent headers recommended."
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "uk,en;q=0.9"
  rate_limit: "max 1 request per 3 seconds per domain"
  encoding: "UTF-8 (universal across Ukrainian government sites)"
  english_editions: "Unusually comprehensive — wartime strategic communications investment means most government sites have full English editions"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Ukrainian government communications under martial law are shaped by two simultaneous imperatives: domestic morale maintenance and international support mobilization. The pipeline must treat government sources as revealing the official posture — what the government chooses to communicate publicly — rather than as confirming ground truth. The interpretive value lies in four dimensions: (a) what is said, (b) what is omitted, (c) the timing relative to media coverage, and (d) divergence between Ukrainian-language and English-language versions of the same communication (which reveals audience-specific messaging calibration).

- **Office of the President**: Cross-reference nightly addresses and presidential statements against same-day reporting in Ukrainska Pravda (UP) and Kyiv Independent. UP's known tension with the Office of the President (see Layer 1 map) means that discrepancies between presidential framing and UP's reporting are analytically significant — they indicate the boundaries of wartime messaging discipline. When UP's Ekonomichna Pravda or Yevropeiska Pravda diverge from official presidential framing on EU accession or economic policy, it signals elite dissatisfaction with the pace or direction of policy.

- **MFA**: Diplomatic communications should be triangulated with Yevropeiska Pravda / European Pravda (the only dedicated EU/NATO integration outlet) and Kyiv Independent (English-language diplomatic coverage). When MFA messaging on Peace Formula progress diverges from European Pravda's assessment, it indicates a gap between diplomatic aspiration and institutional reality.

- **MoD / General Staff**: The twice-daily General Staff briefing reports Russian losses (personnel and equipment by category) that are systematically higher than independent estimates (Mediazona, BBC Russian Service verified databases). However, the trends within the General Staff's own time-series are directionally informative — spikes and drops in reported contact intensity correlate with operationally significant periods. Cross-reference with Defense Express (defense industry), Militarnyi (operational coverage), ISW daily assessments, and DeepState mapping for ground-truth triangulation.

- **NBU / Ministry of Finance**: Economic data from NBU and MoF is technically rigorous — the NBU maintains IMF-standard statistical practices and the MoF publishes detailed budget execution data. Presentation framing may emphasize resilience over vulnerability, but the underlying numbers are reliable. Cross-reference with Interfax-Ukraine (first to publish economic data releases), Ekonomichna Pravda (independent economic analysis), and the Centre for Economic Strategy War Economy Tracker (structured independent dataset).

- **SBU / GUR**: Security and intelligence communications serve dual purposes — operational reporting and information warfare. The SBU's counterintelligence reports (FSB agent detentions, counter-sabotage) provide genuine operational data but are selectively released for deterrence and morale purposes. GUR's strategic assessments (Russian military capacity, North Korean troop deployments) are intelligence-derived but calibrated for public consumption. Cross-reference with Texty.org.ua (data journalism on information operations) and NV (elite policy debates including security policy).

- **Energoatom / Naftogaz / Ukrenergo**: State energy enterprise communications during wartime are essential real-time indicators of infrastructure resilience but systematically understate damage severity (for morale and OPSEC reasons). Cross-reference with Liga.net (energy sector coverage), Interfax-Ukraine (energy data), and IAEA reports (for Zaporizhzhia NPP specifically).

**4.2 The wartime English-language communications effect**

A distinctive feature of Ukraine's government communications infrastructure — with no parallel in peacetime governance — is the systematic investment in English-language parallel editions across virtually all government websites. This wartime innovation serves Ukraine's strategic objective of maintaining international support and creates an operational advantage for pipeline automation (direct ingestion without machine translation). However, it also means that English-language government content is explicitly calibrated for international audiences:

- English editions may omit domestically sensitive content (mobilization controversies, internal political friction, corruption cases)
- Framing in English editions may be more explicitly aligned with Western policy frameworks than the Ukrainian originals
- The pipeline should monitor both Ukrainian-language and English-language editions of high-priority sources (President, MFA, MoD) to detect audience-specific messaging divergence

This dual-language monitoring is a unique analytical opportunity: divergence between Ukrainian and English messaging on the same event reveals the gap between domestic governance reality and international advocacy posture.

**4.3 The NSDC-Presidential decree pipeline**

Ukraine's national security decision-making under martial law follows a distinctive institutional pathway: the NSDC formulates decisions (sanctions lists, defense coordination measures, cybersecurity policy) that are enacted by the President as legally binding decrees. This means national security policy appears across three sources simultaneously:

- NSDC website (`rnbo.gov.ua`) — decision announcements
- Presidential website (`president.gov.ua`) — decree texts
- Official Gazette (`zakon.rada.gov.ua`) — legally binding published text

The pipeline must recognize this as a single decision appearing in three places, not three separate decisions. Use the `zakon.rada.gov.ua` publication as canonical for legal text, the NSDC announcement for policy context, and the presidential decree for timing.

**4.4 The General Staff social media dependency**

The most operationally important government source — the General Staff's twice-daily briefing — is published exclusively on social media (Facebook, Telegram, X) rather than on a government website. This creates:

- **Extraction complexity**: Requires social media scraping or API integration rather than standard web scraping
- **Platform risk**: Facebook access policies, Telegram API rate limits, and X/Twitter API costs are all external dependencies
- **Verification difficulty**: Social media posts lack the structured metadata (publication timestamps, document identifiers) of government website content
- **Fallback**: The Cabinet of Ministers website (`kmu.gov.ua`) syndicates General Staff briefings, but with variable delay (30-120 minutes)

The pipeline should designate the Telegram channel (`t.me/GeneralStaffZSU`) as the fastest source, the Facebook page as the most complete (includes infographics), and `kmu.gov.ua` as the structured-web fallback.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Infrastructure — No Shared Extraction Pattern

Unlike Mexico's gob.mx platform (which hosts 7 of 17 endpoints under a single URL pattern), Ukraine's government web infrastructure is fully decentralized. Each ministry and agency maintains its own domain, CMS, URL structure, and content template. This means:

- No single scraper module can service multiple agencies
- Each source requires its own extraction configuration (URL patterns, pagination, content selectors)
- No single point of failure — if one ministry's site goes down, others remain accessible
- Template changes at one agency do not propagate to others

The tradeoff is higher initial configuration effort but greater operational resilience.

### 5.2 RSS and API-Enabled Sources (Priority for Automation)

Two government sources provide machine-readable feeds:

1. **Office of the President**: Multiple RSS feeds covering news, speeches, administration, and documents — in both Ukrainian and English. These are well-structured standard RSS 2.0 feeds. **This is the single most important automated feed in the Ukraine government source set.**

2. **NBU (National Bank of Ukraine)**: REST API providing structured data on exchange rates, key policy rate, government bonds, and interbank rates in JSON and XML formats. Technical documentation at `bank.gov.ua/en/open-data/api-dev`. Updated as of January 2026 with a new `_special_` field. **This is the best machine-readable financial data source in Ukraine.**

All other sources require HTML scraping or social media extraction.

### 5.3 PDF Extraction Requirements

Three sources publish substantially in PDF:

- **Ministry of Finance**: State Budget documents, budget declarations, and monthly execution reports. Well-structured text PDFs. IMF program documents also published as PDF (e.g., Country Report No. 25/78).
- **NBU**: Monetary policy decisions, inflation reports, financial stability reports. Text-based, well-structured PDFs.
- **Official Gazette (zakon.rada.gov.ua)**: While the legislation database presents most content as HTML, some formal documents are available only as PDF. Historical documents may require OCR.

### 5.4 Language and Encoding

All government sources publish in Ukrainian as their primary language. Most maintain parallel English editions of varying comprehensiveness:

| Tier | Sources | English Coverage |
|---|---|---|
| Full parallel English | President, MFA, MoD, NBU, MoF, Naftogaz, KMU | Near-complete; 1-3 hour lag for translations |
| Substantial English | SBU, GUR, NSDC, Energoatom, Ukrenergo | Most major items; some Ukrainian-only content |
| Limited English | Rada, Ministry of Economy | News summaries only; legislation/detail in Ukrainian |
| Ukrainian only | Official Gazette, Uryadoviy Kuryer | Abstracts only on zakon.rada.gov.ua |

All sites use UTF-8 encoding. Machine translation from Ukrainian is highly reliable for structured government communications (formal language, consistent terminology).

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:

- NSDC decisions appear on `rnbo.gov.ua`, `president.gov.ua` (as decrees), and `zakon.rada.gov.ua` (as gazette entries)
- General Staff briefings appear on Facebook, Telegram, X, and `kmu.gov.ua`
- Defense procurement announcements appear on `mod.gov.ua` and `kmu.gov.ua`
- Energy infrastructure attack reports appear on Energoatom, Naftogaz, and Ukrenergo simultaneously
- Cabinet resolutions appear on `kmu.gov.ua` and `zakon.rada.gov.ua`

Implement content-hash deduplication. Use `zakon.rada.gov.ua` as canonical for legal texts. Use the originating agency (MFA for diplomatic, MoD for defense procurement, General Staff for operational) as canonical for operational communications. For energy infrastructure attacks, use Ukrenergo (grid operator) as canonical for electricity impact and Naftogaz for gas infrastructure impact.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | President (RSS), MFA, MoD | Every 2 hours | Daily publication, policy-critical. Presidential RSS should be polled more frequently. |
| P1-Operational | General Staff (social media) | Every 2 hours | Twice-daily briefings are the foundational operational document. Telegram channel is fastest. |
| P2-Active | Rada, MoF, NBU (API), SBU, GUR, KMU | Every 6 hours | Regular publishing schedule, significant analytical value |
| P2-Standard | Gazette, Economy, NSDC, Energoatom, Naftogaz, Ukrenergo | Every 12 hours | Important but less frequent publication |
| P2-Institutional | ZSU website | Every 24 hours | Institutional content updated infrequently; strategic documents are high-value but rare |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| .gov.ua domain-level disruption (Russian cyberattack) | All government .gov.ua sites | Monitor official Telegram channels and X/Twitter accounts. Ukrainian government has invested heavily in social media redundancy precisely for this scenario. Ukrinform (`ukrinform.net`) syndicates government communications within minutes. |
| Facebook access restriction | General Staff daily briefings | Telegram channel (`t.me/GeneralStaffZSU`) carries same content. X/Twitter (@GeneralStaffUA) provides English versions. `kmu.gov.ua` syndicates with 30-120 min delay. |
| NBU API endpoint failure | Exchange rates, key policy rate | HTML scraping of `bank.gov.ua/en/monetary` for policy decisions. Interfax-Ukraine publishes NBU data releases within minutes. |
| Energy enterprise site outage | Energoatom, Naftogaz, Ukrenergo | IAEA reports for nuclear safety. Liga.net and Interfax-Ukraine for energy data. Official Telegram channels for each enterprise. |
| English edition unavailable / delayed | All sources | Fall back to Ukrainian-language edition with machine translation. Ukrainian government text (formal register) translates reliably. |
| Wartime infrastructure damage to hosting | Any source | Ukrainian government websites are hosted on distributed infrastructure (including international CDNs) to mitigate physical infrastructure targeting. Social media channels (Telegram, X) serve as the primary resilience layer. |

---

*This supplement should be reviewed quarterly or upon: (a) changes in Ukraine's martial law status, (b) major government reshuffles, (c) ceasefire or peace negotiations altering the wartime communications posture, (d) changes to .gov.ua infrastructure, or (e) any transition from wartime to peacetime institutional arrangements that would restructure the NSDC-presidential decree pipeline or General Staff communications protocols.*
