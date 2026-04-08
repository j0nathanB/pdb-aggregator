# Official Government Sources Supplement: LATVIA

**Primary language of political discourse: Latvian**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Latvia (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Latvia. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Latvia's government web infrastructure is decentralized across independent ministry domains, all using the shared `gov.lv` top-level domain but operating on separate platforms and content management systems. Most ministries follow a common Drupal-based template (maintained by the State Chancellery's digital team) with a consistent URL pattern (`{ministry}.gov.lv/en/articles` for news). A notable feature is that several ministries expose RSS feeds at `{ministry}.gov.lv/en/rss`, though availability is inconsistent — some pages exist but return "No RSS feeds available right now." The President's Chancery (`president.lv`) and Parliament (`saeima.lv`) operate on fully independent infrastructure outside the `gov.lv` CMS. Security and intelligence services (VDD, SAB, MIDD) maintain minimal web presences with infrequent but high-value publications. Latvijas Banka (`bank.lv`) operates entirely independent infrastructure as a Eurosystem member.

---

## 1. OFFICIAL GOVERNMENT SOURCES: LATVIA

### 1.1 Head of Government

Latvia has a dual executive: the **President** (head of state, chairs the National Security Council, commander-in-chief) and the **Prime Minister** (head of government, leads the Cabinet of Ministers). Both must be monitored.

#### 1.1a President of Latvia — Valsts prezidenta kanceleja

| Field | Detail |
|---|---|
| **Institution** | Chancery of the President of Latvia (Valsts prezidenta kanceleja) |
| **Current Incumbent** | Edgars Rinkēvičs (since July 2023) |
| **Domain** | `president.lv` |
| **Entry Point URL** | `https://www.president.lv/en/articles?page=0` |
| **RSS/Atom Feed** | RSS page exists at `https://www.president.lv/en/rss` but currently returns "No RSS feeds available right now." |
| **Language** | Latvian (primary); English version available at `/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily or near-daily. The President maintains an active schedule of meetings, speeches, and foreign visits with corresponding news items. |
| **Content Format** | HTML articles. Individual articles at `/en/article/{slug}`. Pagination via `?page=N` query parameter. Gallery/photo section at `/en/news/news`. |
| **Extraction Method** | HTML scraping of `/en/articles` listing page. Each item links to a full-text article. Paginated (330+ pages of historical content). |
| **Editorial Orientation** | Official head-of-state communication. As a former Foreign Minister (2011-2023) and NATO's longest-serving foreign minister, Rinkēvičs's statements carry particular weight on security and foreign-policy matters. Framing reflects strong Euro-Atlantic orientation. |
| **Why This Source** | The President chairs the National Security Council, appoints the prime minister-designate, and represents Latvia at European Council summits. Presidential statements on Russia, NATO, and EU policy signal Latvia's strategic posture. Rinkēvičs's personal authority on foreign policy exceeds the constitutional role. |
| **Access Notes** | No paywall, no authentication required. No bot protection observed. Independent infrastructure (not on gov.lv CMS). |

**Additional entry points:**
- National Security Council information: `https://www.president.lv/en/national-security-council`
- Social media: `@President_LV` on X

---

#### 1.1b Prime Minister / Cabinet of Ministers — Ministru kabinets

| Field | Detail |
|---|---|
| **Institution** | Cabinet of Ministers (Ministru kabinets) |
| **Current PM** | Evika Siliņa (since September 2023; New Unity / Jaunā Vienotība) |
| **Domain** | `mk.gov.lv` |
| **Entry Point URL** | `https://www.mk.gov.lv/en/articles` |
| **RSS/Atom Feed** | RSS page exists at `https://www.mk.gov.lv/en/rss` but currently returns "No RSS feeds available right now." |
| **Language** | Latvian (primary); English version at `/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains — the Cabinet is the central policy-making body |
| **Publication Frequency** | Daily. Cabinet sessions are held weekly (typically Tuesdays). News items cover all ministerial portfolios. |
| **Content Format** | HTML articles. Individual articles at `/en/article/{slug}`. Filterable by ministry/category (Defence, Foreign Affairs, Finance, etc. — 20+ categories). Pagination via `?page=N`. |
| **Extraction Method** | HTML scraping of `/en/articles` listing page. Category filtering available via UI but not cleanly parameterized in URL. |
| **Editorial Orientation** | Official government communication. Reflects coalition policy (New Unity + Progressives + United List). Emphasis on security spending, EU integration, and Ukraine support. |
| **Why This Source** | The mk.gov.lv portal aggregates news from all ministries, making it the single most comprehensive government news endpoint. Cabinet decisions on defense spending (4.9% GDP in 2026), sanctions implementation, and coalition politics appear here first. Category filters for "Ministry of Defence," "Ministry of Foreign Affairs," and "NATO" allow targeted monitoring. |
| **Access Notes** | No paywall. Drupal-based CMS (gov.lv shared platform). No bot protection observed. |

**Additional entry points:**
- Cabinet composition: `https://www.mk.gov.lv/en/cabinet-composition`
- TAP portal (draft legislation): `https://tapportals.mk.gov.lv/` — contains draft regulations and policy documents under development

---

### 1.2 Foreign Ministry — Ārlietu ministrija (MFA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Foreign Affairs (Ārlietu ministrija) |
| **Current Minister** | Baiba Braže (since April 2024; former NATO Assistant Secretary General for Public Diplomacy) |
| **Domain** | `mfa.gov.lv` |
| **Entry Point URL** | `https://www.mfa.gov.lv/en/articles` |
| **RSS/Atom Feed** | **Yes — functional RSS feed.** Articles: `https://www.mfa.gov.lv/en/rss/articles` (RSS 2.0, verified, titled "RSS jaunumi", ~20 items). Events: `https://www.mfa.gov.lv/en/rss/events` |
| **Language** | Latvian (primary); English version comprehensive — the MFA maintains the most complete English-language content of any Latvian ministry |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Comunicados for EU Foreign Affairs Council positions, bilateral meetings, UN statements, consular updates. Minister Braže is highly active on EU and NATO platforms. |
| **Content Format** | HTML articles on gov.lv CMS. Full texts of speeches and statements published directly (e.g., annual Saeima foreign policy debate address, UN Security Council statements). Some PDF attachments for annual reports. |
| **Extraction Method** | **RSS polling** of `mfa.gov.lv/en/rss/articles` (preferred — verified functional, ~20 items, RSS 2.0). Fallback: HTML scraping of `/en/articles`. |
| **Editorial Orientation** | Official foreign ministry position. Strongly Euro-Atlantic. Under Braže, particularly hawkish on Russia sanctions, Ukraine support, and transatlantic solidarity. Latvia's decision to sever all economic ties with Russia by end of 2026 is a core policy theme. |
| **Why This Source** | The primary source for Latvia's formal diplomatic positions, EU Council statements, NATO postures, bilateral agreements, and multilateral engagement. The MFA's English-language content is authoritative and near-simultaneous with Latvian publication. Annual foreign policy debate address to the Saeima is a key strategic document. |
| **Access Notes** | No paywall. RSS feed verified functional (March 2026). Media contact: media@mfa.gov.lv. Social media: `@Latvian_MFA` on X, Facebook at `/LatvianMFA/`. |

**Additional entry points:**
- RSS hub page: `https://www.mfa.gov.lv/en/rss`
- Annual report of the Minister of Foreign Affairs (PDF): published yearly, downloadable from the MFA site
- Embassy-level releases: individual embassy sites (not centralized)

---

### 1.3 Defense Ministry — Aizsardzības ministrija (MoD) & National Armed Forces (NBS)

#### 1.3a Ministry of Defence

| Field | Detail |
|---|---|
| **Institution** | Ministry of Defence (Aizsardzības ministrija) |
| **Current Minister** | Andris Sprūds |
| **Domain** | `mod.gov.lv` |
| **Entry Point URL** | `https://www.mod.gov.lv/en/zinas` |
| **RSS/Atom Feed** | No RSS feed available. `/en/rss` returns 404. |
| **Language** | Latvian (primary); English version available at `/en/` with comprehensive defense policy content |
| **Type** | `government_aligned` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-5 per week. News items cover NATO cooperation, procurement, defense budget, allied exercises, bilateral defense agreements. |
| **Content Format** | HTML articles. Individual articles at `/en/news/{slug}`. Annual reports in PDF at `/en/about-us/annual-reports-ministry-defence`. |
| **Extraction Method** | HTML scraping of `/en/zinas` listing page. Note: the English news URL uses the Latvian path segment `zinas` (not `news`). |
| **Editorial Orientation** | Official defense ministry communication. Emphasizes NATO integration, allied presence (Canadian-led multinational brigade), defense spending trajectory (4.9% GDP in 2026), and comprehensive national defense concept. |
| **Why This Source** | Latvia is a NATO frontline state with one of the highest defense-spending ratios in the Alliance. MoD communications signal procurement decisions (IRIS-T, drones), NATO exercise participation, bilateral defense MOUs, and the buildup of the Canadian-led NATO brigade. Defense policy is a defining issue for the current government. |
| **Access Notes** | No paywall. No bot protection observed. Documents section at `/en/dokumenti` contains defense policy papers. Media contact: prese@mod.gov.lv. |

**Additional entry points:**
- Defense policy documents: `https://www.mod.gov.lv/en/nozares-politika`
- Support for Ukraine tracker: `https://www.mod.gov.lv/en/support-ukraine`
- Cybersecurity section: `https://www.mod.gov.lv/en/cybersecurity`

#### 1.3b National Armed Forces — Nacionālie bruņotie spēki (NBS)

| Field | Detail |
|---|---|
| **Institution** | National Armed Forces (Nacionālie bruņotie spēki — NBS) |
| **Domain** | `mil.lv` |
| **Entry Point URL** | `https://www.mil.lv/en` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at mil.lv/en/rss] |
| **Language** | Latvian (primary); English available |
| **Type** | `government_aligned` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-4 per week. News covers exercises, NATO eFP operations, force development, recruitment. |
| **Content Format** | HTML articles with images. |
| **Extraction Method** | HTML scraping of main page news section. |
| **Editorial Orientation** | Official military communication. Operational updates on exercises, allied integration, and force structure. |
| **Why This Source** | NBS communications provide operational-level detail that MoD press releases do not — exercise names, unit deployments, allied force rotations. The NBS is expanding rapidly (target 8,000 professional soldiers) and reintroducing mandatory service, making force-development updates operationally relevant. |
| **Access Notes** | No paywall. Media contact: prese@mil.lv. NBS consists of Land Forces, Naval Forces, Air Force, and National Guard (Zemessardze). |

---

### 1.4 Parliament — Saeima

| Field | Detail |
|---|---|
| **Institution** | Saeima (Parliament of the Republic of Latvia) |
| **Domain** | `saeima.lv` |
| **Entry Point URL** | `https://www.saeima.lv/en/news/saeima-news` (press releases) |
| **RSS/Atom Feed** | The Saeima indicates RSS feeds are available at `https://www.saeima.lv/en/news/follow-the-updates` but the specific feed URLs are not clearly exposed on the page. [VERIFY RSS — check page source for feed URLs] |
| **Language** | Latvian (primary); English version at `/en/` covers key legislative news |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints, Security & defense autonomy |
| **Publication Frequency** | 3-5 per week during session periods. Reduced during recess. The Saeima operates in two sessions per year (September-December, January-June). |
| **Content Format** | HTML press releases. Live session broadcasts at `saeima.lv/en/live/`. Committee session schedules and agendas published. |
| **Extraction Method** | HTML scraping of `/en/news/saeima-news` listing page. Independent infrastructure (not on gov.lv CMS). |
| **Editorial Orientation** | Institutional parliamentary communication. Press releases cover legislative votes, committee activities, speaker's meetings, and inter-parliamentary delegations. |
| **Why This Source** | The Saeima votes on defense budgets, ratifies treaties, approves the National Security Concept, and conducts foreign/defense committee hearings. The annual foreign policy debate (where the Foreign Minister presents the yearly report) is a key strategic event. Coalition dynamics (New Unity + Progressives + United List) and opposition pressure from National Alliance are visible in parliamentary proceedings. |
| **Access Notes** | No paywall. Independent web infrastructure. Live session streaming available. IPEX (EU inter-parliamentary exchange) page at `secure.ipex.eu/IPEXL-WEB/parliaments/list_parliaments/lvsae`. |

**Additional entry points:**
- News overview: `https://www.saeima.lv/en/news`
- Live sessions: `https://www.saeima.lv/en/live/`
- Follow updates page (RSS): `https://www.saeima.lv/en/news/follow-the-updates`

---

### 1.5 Official Gazette — Latvijas Vēstnesis

| Field | Detail |
|---|---|
| **Institution** | Latvijas Vēstnesis (Official Gazette of the Republic of Latvia) |
| **Domain** | `vestnesis.lv` / `lv.lv` |
| **Entry Point URL** | `https://www.vestnesis.lv/` (official gazette issues) / `https://likumi.lv/` (consolidated legislation database) |
| **RSS/Atom Feed** | None identified. Likumi.lv offers email notifications for changes to specific laws (registered users) but no RSS. [VERIFY RSS at vestnesis.lv] |
| **Language** | Latvian (legislation is published only in Latvian; selected laws have unofficial English translations on likumi.lv) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the gazette is the constitutional publication vehicle for all laws, Cabinet regulations, and international agreements |
| **Publication Frequency** | Daily (electronic publication since 2013; no print edition). Each issue contains multiple legal acts. |
| **Content Format** | HTML on vestnesis.lv (individual legal acts). Likumi.lv provides consolidated (amended) versions in HTML. PDF downloads available for individual gazette issues. |
| **Extraction Method** | HTML scraping of vestnesis.lv daily index page to identify new publications. Likumi.lv search interface for targeted monitoring of specific legislation areas. URL pattern: `vestnesis.lv/op/YYYY/NNN.NN` (year/issue.item). |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, Cabinet regulation, or international agreement is legally binding until published in Latvijas Vēstnesis. This is the definitive source for sanctions implementation regulations, defense-spending legislation, and treaty ratifications. Likumi.lv complements by providing consolidated statute text with amendment history. |
| **Access Notes** | Free access to vestnesis.lv (since 2013 digitization). Likumi.lv is free; registered users get change notifications. VSIA "Latvijas Vēstnesis" is a state-owned enterprise under the Ministry of Justice (`tm.gov.lv`). Publisher: Bruņinieku 41, Rīga, LV-1011. Contact: valde@lv.lv. |

**Additional entry points:**
- Consolidated legislation: `https://likumi.lv/` (free, searchable, Latvian with some English translations)
- Official announcements section: `https://www.vestnesis.lv/oficialie-pazinojumi/`
- N-Lex (EU legislation gateway for Latvia): `https://n-lex.europa.eu/n-lex/legis_lv/latvijas_vestnesis_form`

---

### 1.6 Finance Ministry — Finanšu ministrija (FM)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Finance (Finanšu ministrija) |
| **Domain** | `fm.gov.lv` |
| **Entry Point URL** | `https://www.fm.gov.lv/en/articles` |
| **RSS/Atom Feed** | RSS page exists at `https://www.fm.gov.lv/en/rss` but currently returns "No RSS feeds available right now." |
| **Language** | Latvian (primary); English version available with budget and fiscal policy content |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 2-4 per week. Communications cover state budget, tax policy, EU funds management (FM serves as EU funds Managing Authority), fiscal forecasts, and Recovery and Resilience Facility implementation. |
| **Content Format** | HTML articles on gov.lv CMS. Budget documents and macroeconomic forecasts in PDF. |
| **Extraction Method** | HTML scraping of `/en/articles` listing page. Same gov.lv CMS template as other ministries. |
| **Editorial Orientation** | Official fiscal policy position. Technical and data-driven. GDP growth forecast revisions (2.6% for 2026) and budget priority communications emphasize security spending and social investment. |
| **Why This Source** | Primary source for Latvia's state budget (EUR 16.1B revenue, EUR 17.9B expenditure in 2026), fiscal policy, EU funds absorption, and macroeconomic forecasts. The 2026 budget's massive defense allocation (4.9% GDP) is a critical indicator of strategic priorities. FM's GDP forecasts are a leading indicator for economic health. |
| **Access Notes** | No paywall. No bot protection observed. National economy analysis section at `/en/s/ta`. De minimis aid search tool at `deminimismekletajs.fm.gov.lv`. |

**Additional entry points:**
- Budget 2026 documentation: accessible via news articles tagged with `#Budget2026`
- EU funds management: `https://www.fm.gov.lv/en/managing-authority`

---

### 1.7 Central Bank — Latvijas Banka

| Field | Detail |
|---|---|
| **Institution** | Latvijas Banka (Bank of Latvia) |
| **Current Governor** | Mārtiņš Kazāks |
| **Domain** | `bank.lv` / `macroeconomics.lv` |
| **Entry Point URL** | `https://www.bank.lv/en/news/` (news hub) / `https://www.bank.lv/en/news-and-events/news-and-articles/press-releases` (press releases) |
| **RSS/Atom Feed** | None identified on the current website. Newsletter subscription available at `https://www.bank.lv/en/subscribe`. [VERIFY RSS — bank.lv redesign may have removed previously available feeds] |
| **Language** | Latvian (primary); English version comprehensive (Eurosystem requirement) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Variable. Press releases: 2-4 per month. Macroeconomic forecasts: quarterly. Financial Stability Report: semi-annual. Statistics: continuous updates. ECB Governing Council monetary policy decisions: 6-8 per year (Latvia participates in the rotating Eurosystem vote). |
| **Content Format** | HTML for news. PDF for formal publications (Annual Report, Financial Stability Report, Macroeconomic Projections, Working Papers). Statistics via INTS database (interactive tables). |
| **Extraction Method** | HTML scraping of `/en/news/` listing page. PDF download for formal publications. Statistical data via INTS database API or direct table access. |
| **Editorial Orientation** | Technically independent central bank and ECB/Eurosystem member. Governor Kazāks is a visible public communicator on inflation, lending conditions, and Baltic economic convergence. Communications are data-driven and policy-neutral by institutional mandate. |
| **Why This Source** | Latvijas Banka is the authoritative source for macroeconomic forecasts (GDP 2.8% growth projected for 2026), financial stability assessments, banking sector supervision data, and balance-of-payments statistics. As an ECB Governing Council member, Kazāks's public statements on monetary policy carry weight beyond Latvia. The macroeconomics.lv portal provides expert analysis and commentary. |
| **Access Notes** | No paywall. No bot protection observed. Independent infrastructure (not on gov.lv CMS). Email newsletter at `/en/subscribe`. Statistics portal: `https://www.bank.lv/en/statistics`. |

**Key publication URLs:**
| Publication | URL |
|---|---|
| Press releases | `https://www.bank.lv/en/news-and-events/news-and-articles/press-releases` |
| Macroeconomic forecasts | `https://www.bank.lv/en/operational-areas/task-monetary-policy/forecasts` |
| Financial Stability Report | `https://www.bank.lv/en/news-and-events/financial-stability-report` |
| Annual Report | `https://www.bank.lv/en/news-and-events/annual-report` |
| Statistical data (INTS) | `https://www.bank.lv/en/statistics/stat-data` |
| Macroeconomics.lv (analysis) | `https://www.macroeconomics.lv/` |
| Working Papers | `https://www.bank.lv/en/news-and-events/discussion-papers` |
| Euro Area Bank Lending Survey | `https://www.bank.lv/en/news-and-events/euro-area-bank-lending-survey` |

---

### 1.8 Trade / Economy — Ekonomikas ministrija (EM)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Economics (Ekonomikas ministrija) |
| **Current Minister** | Viktors Valainis |
| **Domain** | `em.gov.lv` |
| **Entry Point URL** | `https://www.em.gov.lv/en/articles` |
| **RSS/Atom Feed** | **Yes — functional RSS feed.** Articles: `https://www.em.gov.lv/en/rss/articles` (RSS 2.0, verified, titled "RSS jaunumi", ~20 items). Events: `https://www.em.gov.lv/en/rss/events` |
| **Language** | Latvian (primary); English version available |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-4 per week. Communications cover investment attraction, energy policy, trade, EU single market, and economic development. |
| **Content Format** | HTML articles on gov.lv CMS. Economic development reports in PDF. |
| **Extraction Method** | **RSS polling** of `em.gov.lv/en/rss/articles` (preferred — verified functional). Fallback: HTML scraping of `/en/articles`. |
| **Editorial Orientation** | Official economic policy position. Under Valainis, emphasis on investment attraction (particularly from US business — Mar-a-Lago meetings), energy storage and renewables, and digital economy. |
| **Why This Source** | Primary source for trade policy, investment climate, energy policy (critical given Latvia's pivot away from Russian energy), EU single market positions, and economic forecasts. The Ministry's economic situation reports provide macroeconomic context. Latvia's decision to sever all economic ties with Russia by end of 2026 generates significant EM policy output. |
| **Access Notes** | No paywall. RSS verified functional (March 2026). Economic situation data at `/en/economic-situation-0`. |

**Additional entry points:**
- RSS hub: `https://www.em.gov.lv/en/rss`
- Economic situation overview: `https://www.em.gov.lv/en/economic-situation-0`
- LIAA (Investment and Development Agency): `https://www.liaa.gov.lv/en` (has its own RSS at `/en/rss`)

---

### 1.9 Intelligence / National Security

Latvia has three national security institutions and a National Security Council. None produces high-frequency public communications, but their infrequent publications are high-value.

#### 1.9a State Security Service — Valsts drošības dienests (VDD)

| Field | Detail |
|---|---|
| **Institution** | State Security Service (Valsts drošības dienests — VDD) |
| **Domain** | `vdd.gov.lv` |
| **Entry Point URL** | `https://vdd.gov.lv/en/news/press-releases` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Latvian (primary); English versions of press releases and annual reports available |
| **Type** | `security_defense` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | 2-4 per month. Press releases cover counterintelligence operations, espionage arrests, sanctions violations, counterterrorism, and election security. Annual report published in February (covering previous year). |
| **Content Format** | HTML press releases. Annual report in PDF (English translation provided). |
| **Extraction Method** | HTML scraping of `/en/news/press-releases` listing page. Annual report PDF download. |
| **Editorial Orientation** | Official security service communication. VDD is the lead agency for counterintelligence, counterterrorism, and protection of constitutional order. Communications are factual and operational — detentions, prosecutions, threat assessments. |
| **Why This Source** | VDD press releases provide real-time intelligence on Russian espionage and sabotage operations in Latvia (Starlink supply networks to Russia, railway infrastructure arson, election interference). The annual report is the most comprehensive publicly available assessment of threats to Latvia's national security, including Russian hybrid warfare, Chinese academic espionage, and domestic extremism. |
| **Access Notes** | No paywall. Separate infrastructure from gov.lv CMS. Annual report 2025 available at `https://www.vdd.gov.lv/uploads/` (PDF). |

#### 1.9b Constitution Protection Bureau — Satversmes aizsardzības birojs (SAB)

| Field | Detail |
|---|---|
| **Institution** | Constitution Protection Bureau (Satversmes aizsardzības birojs — SAB) |
| **Domain** | `sab.gov.lv` |
| **Entry Point URL** | `https://www.sab.gov.lv/en/news/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Latvian (primary); English annual reports available |
| **Type** | `security_defense` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Low — 4-8 press releases per year. Annual report published in January (covering previous year). |
| **Content Format** | HTML news items. Annual report in PDF (English version at `sab.gov.lv/files/uploads/`). |
| **Extraction Method** | Periodic check of `/en/news/`. Annual report PDF download. |
| **Editorial Orientation** | Official intelligence/counterintelligence communication. SAB handles intelligence, counterintelligence, and protection of state secrets. More strategic/analytical tone than VDD's operational focus. |
| **Why This Source** | SAB's annual report provides the intelligence community's strategic threat assessment — Russian hybrid instruments, cyber attacks, influence operations. The 2025 report (published January 2026) warned that Russia continues to develop new hybrid instruments to influence Latvia. SAB annual reports are cited in the existing Source Intelligence Map as a key source for understanding Russian-speaking community dynamics. |
| **Access Notes** | No paywall. Annual report 2025 (English): `https://www.sab.gov.lv/files/uploads/2026/01/SABs-annual-report_2025_ENG.pdf`. |

#### 1.9c Defence Intelligence and Security Service — Militārās izlūkošanas un drošības dienests (MIDD)

| Field | Detail |
|---|---|
| **Institution** | Defence Intelligence and Security Service (Militārās izlūkošanas un drošības dienests — MIDD) |
| **Current Director** | Indulis Krēķis (since 2002) |
| **Domain** | `midd.gov.lv` |
| **Entry Point URL** | `https://www.midd.gov.lv/en` |
| **RSS/Atom Feed** | None available. |
| **Language** | Latvian (primary); English overview available |
| **Type** | `security_defense` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. MIDD publishes virtually no press communications. Website provides institutional information only. |
| **Content Format** | Minimal HTML. |
| **Extraction Method** | Periodic check of main page for any new publications. Flag any new content as high-priority anomaly. |
| **Editorial Orientation** | N/A — effectively silent. MIDD is the national SIGINT authority and military counterintelligence service. |
| **Why This Source** | Included for completeness. MIDD's public-facing presence is institutional only. Intelligence signal from MIDD surfaces through: (a) joint press releases with VDD (e.g., espionage detentions), (b) MoD communications referencing MIDD assessments, (c) Saeima committee testimony. |
| **Access Notes** | Minimal website. Under subordination of the Defence Minister. Areas of activity described at `/en/areas-activity`. |

#### 1.9d National Security Council — Nacionālās drošības padome

| Field | Detail |
|---|---|
| **Institution** | National Security Council (Nacionālās drošības padome) |
| **Domain** | `president.lv` (subsection) |
| **Entry Point URL** | `https://www.president.lv/en/national-security-council` |
| **RSS/Atom Feed** | None (part of president.lv, which has no active RSS). |
| **Language** | Latvian; English summaries |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Irregular — meetings are convened by the President as needed. 4-8 published meeting summaries per year. |
| **Content Format** | HTML on president.lv. Meeting summaries are brief communiqués. |
| **Extraction Method** | Captured via president.lv article scraping (NSC meetings appear in the general news feed). |
| **Editorial Orientation** | Official. The NSC coordinates national security policy across government institutions. |
| **Why This Source** | NSC meetings signal escalation of security concerns — the President convenes the NSC for significant threat developments. The NSC Secretary and National Security Advisor (Ilze Milta, appointed August 2024) shapes the security policy agenda. NSC meeting announcements are leading indicators of strategic-level policy shifts. |
| **Access Notes** | No separate site — monitored via president.lv article feed. |

---

### 1.10 Country-Specific Institutions

#### 1.10a KNAB — Corruption Prevention and Combating Bureau

| Field | Detail |
|---|---|
| **Institution** | Corruption Prevention and Combating Bureau (Korupcijas novēršanas un apkarošanas birojs — KNAB) |
| **Domain** | `knab.gov.lv` |
| **Entry Point URL** | `https://www.knab.gov.lv/en/articles` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at knab.gov.lv/en/rss] |
| **Language** | Latvian (primary); English available |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints |
| **Publication Frequency** | 1-3 per week. Communications cover anti-corruption investigations, political party financing oversight, whistleblower protection (KNAB became the whistleblower contact point from March 2026), and pre-election campaign monitoring. |
| **Content Format** | HTML articles. Annual reports in PDF. |
| **Extraction Method** | HTML scraping of `/en/articles` listing page. |
| **Editorial Orientation** | Independent anti-corruption authority. KNAB has historically been a significant institutional actor — its investigations of oligarchs (Lembergs, Šlesers) and political party finances have shaped Latvian politics. |
| **Why This Source** | KNAB's party finance rulings and corruption investigations directly affect the domestic political landscape. Oligarchic influence on media (Diena, NRA) and politics is a documented pattern that KNAB investigations illuminate. KNAB's new role as whistleblower contact point (March 2026) expands its monitoring remit. |
| **Access Notes** | No paywall. Annual reports at `/en/annual-reports`. Gov.lv CMS platform. |

#### 1.10b NATO Enhanced Forward Presence (eFP) — Canadian-led Multinational Brigade

| Field | Detail |
|---|---|
| **Institution** | NATO Enhanced Forward Presence (eFP) in Latvia / Canadian Armed Forces in Latvia |
| **Domain** | `canada.ca` (DND) / `nato.int` |
| **Entry Point URL** | `https://www.canada.ca/en/department-national-defence.html` (DND press releases) / `https://www.nato.int/cps/en/natohq/topics_136388.htm` (eFP overview) |
| **RSS/Atom Feed** | DND: `https://www.canada.ca/content/canadasite/api/nws/fds/en/national-defence.atom` [VERIFY RSS — Canada.ca Atom feed pattern]. NATO newsroom RSS: `https://www.nato.int/cps/en/natolive/news.rss` |
| **Language** | English, French (DND); English (NATO) |
| **Type** | `security_defense` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | DND: 1-3 per week on Latvia-specific items. NATO eFP: monthly communiqués plus exercise-related updates. |
| **Content Format** | HTML. |
| **Extraction Method** | RSS polling for NATO newsroom. HTML scraping/keyword filtering for Canada DND press releases mentioning "Latvia." |
| **Editorial Orientation** | Allied military communication. Canadian DND releases cover force rotation, exercise participation, and bilateral defense cooperation. NATO releases provide Alliance-level context. |
| **Why This Source** | The existing Source Intelligence Map identifies NATO brigade buildup as a blind spot — "Canadian-led multinational brigade operational details classified." Canadian DND releases and NATO eFP communiqués are the primary public sources for allied force presence details that Latvian MoD communications reference but do not fully detail. |
| **Access Notes** | Both sites are free. NATO newsroom has RSS. Canada.ca may require Atom feed parsing. |

#### 1.10c EU Council / EEAS — Latvia-relevant Communications

| Field | Detail |
|---|---|
| **Institution** | Council of the European Union / European External Action Service (EEAS) |
| **Domain** | `consilium.europa.eu` / `eeas.europa.eu` |
| **Entry Point URL** | `https://www.consilium.europa.eu/en/press/press-releases/` (Council) / `https://www.eeas.europa.eu/eeas/press-material_en` (EEAS) |
| **RSS/Atom Feed** | Council: `https://www.consilium.europa.eu/en/press/press-releases/?filters=2025&Page=1` (filterable, RSS available). EEAS: RSS feeds available at various topic pages. |
| **Language** | English (primary working language for press releases) |
| **Type** | `institutional` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily. Council conclusions, sanctions packages, foreign affairs council outcomes. |
| **Content Format** | HTML with PDF council conclusions. |
| **Extraction Method** | RSS polling with keyword filtering for "Latvia" and Baltic-relevant topics (Russia sanctions, Eastern Partnership, defense). |
| **Editorial Orientation** | EU institutional communication. Council conclusions reflect negotiated positions — Latvia's positions are embedded within collective EU statements. |
| **Why This Source** | EU sanctions on Russia, European Council conclusions on defense, and Foreign Affairs Council outcomes directly shape Latvia's policy space. Minister Braže's statements at EU FAC are published on both the MFA and Council sites — the Council version provides the multilateral context. |
| **Access Notes** | Free. Well-structured press release archive with date and topic filtering. |

#### 1.10d Baltic Cooperation — NB8 / Baltic Assembly / Baltic Council of Ministers

| Field | Detail |
|---|---|
| **Institution** | Baltic Assembly / Baltic Council of Ministers / NB8 (Nordic-Baltic Eight) |
| **Domain** | `baltasam.org` (Baltic Assembly) |
| **Entry Point URL** | `https://www.baltasam.org/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English |
| **Type** | `institutional` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Low — monthly or less. Session declarations, committee resolutions, joint statements. NB8 leader statements published via national executive channels (president.lv, mk.gov.lv). |
| **Content Format** | HTML. Joint statements in PDF. |
| **Extraction Method** | Periodic check of baltasam.org. NB8 statements captured via president.lv and mk.gov.lv monitoring. |
| **Editorial Orientation** | Multilateral Baltic institutional communication. Reflects consensus positions across Estonia, Latvia, Lithuania (and Nordic partners in NB8 format). |
| **Why This Source** | Baltic cooperation is a defining feature of Latvia's foreign policy. Joint Baltic positions on Russia, energy security, defense, and EU policy amplify individual country positions. NB8 summits (adding Denmark, Finland, Iceland, Norway, Sweden) are a key regional coordination format. The existing Source Intelligence Map includes `Baltijas sadarbība` (Baltic cooperation) and `Ziemeļvalstu sadarbība` (Nordic cooperation) as core query vocabulary. |
| **Access Notes** | baltasam.org is intermittently maintained. Primary signal comes via national government channels. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | gov.lv CMS |
|---|---|---|---|---|---|---|---|
| 1a | President (Chancery) | `president.lv/en/articles` | No (page exists, empty) | P1 | HTML | Daily | No |
| 1b | Cabinet of Ministers | `mk.gov.lv/en/articles` | No (page exists, empty) | P1 | HTML | Daily | Yes |
| 2 | MFA | `mfa.gov.lv/en/articles` | **Yes** (`/en/rss/articles`) | P1 | HTML | Daily | Yes |
| 3a | MoD | `mod.gov.lv/en/zinas` | No (404) | P1 | HTML | 3-5/week | Yes |
| 3b | NBS | `mil.lv/en` | [VERIFY] | P1 | HTML | 2-4/week | No |
| 4 | Saeima | `saeima.lv/en/news/saeima-news` | [VERIFY] | P2 | HTML | 3-5/week (session) | No |
| 5 | Latvijas Vēstnesis | `vestnesis.lv` / `likumi.lv` | No | P2 | HTML/PDF | Daily | No |
| 6 | Finance Ministry | `fm.gov.lv/en/articles` | No (page exists, empty) | P2 | HTML/PDF | 2-4/week | Yes |
| 7 | Latvijas Banka | `bank.lv/en/news/` | No (newsletter only) | P2 | HTML/PDF | Variable | No |
| 8 | Ministry of Economics | `em.gov.lv/en/articles` | **Yes** (`/en/rss/articles`) | P2 | HTML | 2-4/week | Yes |
| 9a | VDD | `vdd.gov.lv/en/news/press-releases` | [VERIFY] | P2 | HTML/PDF | 2-4/month | No |
| 9b | SAB | `sab.gov.lv/en/news/` | [VERIFY] | P2 | HTML/PDF | 4-8/year | No |
| 9c | MIDD | `midd.gov.lv/en` | No | P2 | Minimal | Negligible | No |
| 9d | NSC | `president.lv/en/national-security-council` | No | P2 | HTML | 4-8/year | No |
| 10a | KNAB | `knab.gov.lv/en/articles` | [VERIFY] | P2 | HTML/PDF | 1-3/week | Yes |
| 10b | NATO eFP / Canada DND | `canada.ca` / `nato.int` | **Yes** (NATO RSS) | P2 | HTML | 1-3/week | No |
| 10c | EU Council / EEAS | `consilium.europa.eu` / `eeas.europa.eu` | **Yes** | P2 | HTML/PDF | Daily | No |
| 10d | Baltic Assembly | `baltasam.org` | [VERIFY] | P2 | HTML | Monthly | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Latvia Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/lv.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: lv_president
    name: President of Latvia (Valsts prezidenta kanceleja)
    domain: president.lv
    entry_url: "https://www.president.lv/en/articles?page=0"
    rss_feed: null  # Page exists at /en/rss but returns empty
    language: lv
    language_en: true
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
    notes: "Chairs National Security Council. Independent infrastructure (not gov.lv CMS). Pagination: ?page=N."

  - id: lv_cabinet
    name: Cabinet of Ministers (Ministru kabinets)
    domain: mk.gov.lv
    entry_url: "https://www.mk.gov.lv/en/articles"
    rss_feed: null  # Page exists at /en/rss but returns empty
    language: lv
    language_en: true
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
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Aggregates news from all ministries. Category filters available (Defence, Foreign Affairs, Finance, NATO, EU). TAP portal at tapportals.mk.gov.lv for draft legislation."

  - id: lv_mfa
    name: Ministry of Foreign Affairs (Ārlietu ministrija)
    domain: mfa.gov.lv
    entry_url: "https://www.mfa.gov.lv/en/articles"
    rss_feed:
      articles: "https://www.mfa.gov.lv/en/rss/articles"
      events: "https://www.mfa.gov.lv/en/rss/events"
    language: lv
    language_en: true
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "RSS verified functional (March 2026). RSS 2.0, ~20 items, titled 'RSS jaunumi'. Best English-language content of any Latvian ministry. Minister Braže highly active on EU/NATO."

  - id: lv_mod
    name: Ministry of Defence (Aizsardzības ministrija)
    domain: mod.gov.lv
    entry_url: "https://www.mod.gov.lv/en/zinas"
    rss_feed: null  # /en/rss returns 404
    language: lv
    language_en: true
    type: government_aligned
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "English news URL uses Latvian path 'zinas'. Procurement, NATO cooperation, defense budget. 4.9% GDP defense spending in 2026."

  - id: lv_nbs
    name: National Armed Forces (Nacionālie bruņotie spēki — NBS)
    domain: mil.lv
    entry_url: "https://www.mil.lv/en"
    rss_feed: null  # [VERIFY]
    language: lv
    language_en: true
    type: government_aligned
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Operational-level content: exercises, NATO eFP, force structure. Media contact: prese@mil.lv."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: lv_saeima
    name: Saeima (Parliament)
    domain: saeima.lv
    entry_url: "https://www.saeima.lv/en/news/saeima-news"
    rss_feed: null  # RSS indicated at /en/news/follow-the-updates but feed URLs not exposed [VERIFY]
    language: lv
    language_en: true
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
      - security_defense_autonomy
    publication_frequency: "3-5_per_week_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Independent infrastructure. Live sessions streamed. Annual foreign policy debate in January. Budget debates Sep-Dec."

  - id: lv_vestnesis
    name: Latvijas Vēstnesis (Official Gazette)
    domain: vestnesis.lv
    entry_url: "https://www.vestnesis.lv/"
    alt_entry_url: "https://likumi.lv/"
    rss_feed: null
    language: lv
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Electronic-only since 2013. URL pattern: vestnesis.lv/op/YYYY/NNN.NN. Likumi.lv for consolidated legislation. Registered likumi.lv users can get email change notifications."

  - id: lv_finance
    name: Ministry of Finance (Finanšu ministrija)
    domain: fm.gov.lv
    entry_url: "https://www.fm.gov.lv/en/articles"
    rss_feed: null  # Page exists at /en/rss but returns empty
    language: lv
    language_en: true
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "2-4_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "State budget, fiscal policy, EU funds management. GDP forecast revisions. #Budget2026 tagged content."

  - id: lv_central_bank
    name: Latvijas Banka
    domain: bank.lv
    entry_url: "https://www.bank.lv/en/news/"
    alt_entry_urls:
      press_releases: "https://www.bank.lv/en/news-and-events/news-and-articles/press-releases"
      forecasts: "https://www.bank.lv/en/operational-areas/task-monetary-policy/forecasts"
      macroeconomics: "https://www.macroeconomics.lv/"
    rss_feed: null  # Newsletter at /en/subscribe; no RSS identified
    language: lv
    language_en: true
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "ECB/Eurosystem member. Governor Kazāks on ECB Governing Council. Macroeconomic forecasts quarterly. INTS statistical database for data. Newsletter subscription at /en/subscribe."

  - id: lv_economy
    name: Ministry of Economics (Ekonomikas ministrija)
    domain: em.gov.lv
    entry_url: "https://www.em.gov.lv/en/articles"
    rss_feed:
      articles: "https://www.em.gov.lv/en/rss/articles"
      events: "https://www.em.gov.lv/en/rss/events"
    language: lv
    language_en: true
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 12
    notes: "RSS verified functional. Investment attraction, energy policy, trade. LIAA (liaa.gov.lv) has separate RSS for investment news."

  - id: lv_vdd
    name: State Security Service (VDD)
    domain: vdd.gov.lv
    entry_url: "https://vdd.gov.lv/en/news/press-releases"
    rss_feed: null  # [VERIFY]
    language: lv
    language_en: true
    type: security_defense
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "2-4_per_month"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Counterintelligence operations, espionage arrests, sanctions enforcement. Annual report in February (PDF, English available). Flag any new publication immediately."

  - id: lv_sab
    name: Constitution Protection Bureau (SAB)
    domain: sab.gov.lv
    entry_url: "https://www.sab.gov.lv/en/news/"
    rss_feed: null  # [VERIFY]
    language: lv
    language_en: true
    type: security_defense
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "4-8_per_year"
    content_format: html_pdf_mixed
    extraction_method: periodic_check
    poll_interval_hours: 24
    notes: "Annual report in January (English PDF). Strategic threat assessment. Flag any publication as high-priority."

  - id: lv_midd
    name: Defence Intelligence and Security Service (MIDD)
    domain: midd.gov.lv
    entry_url: "https://www.midd.gov.lv/en"
    rss_feed: null
    language: lv
    language_en: true
    type: security_defense
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent. National SIGINT authority. Signal comes via VDD joint releases and MoD references. Flag any publication as high-priority anomaly."

  - id: lv_knab
    name: Corruption Prevention Bureau (KNAB)
    domain: knab.gov.lv
    entry_url: "https://www.knab.gov.lv/en/articles"
    rss_feed: null  # [VERIFY at /en/rss]
    language: lv
    language_en: true
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
    publication_frequency: "1-3_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Party finance oversight, anti-corruption investigations. Became whistleblower contact point March 2026."

  - id: lv_nato_efp
    name: NATO eFP Latvia / Canada DND
    domain: nato.int
    entry_url: "https://www.nato.int/cps/en/natohq/topics_136388.htm"
    alt_entry_url: "https://www.canada.ca/en/department-national-defence.html"
    rss_feed:
      nato_news: "https://www.nato.int/cps/en/natolive/news.rss"
    language: en
    type: security_defense
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: rss_poll_with_keyword_filter
    poll_interval_hours: 12
    keyword_filter: ["Latvia", "Baltic", "eFP", "battlegroup"]
    notes: "NATO RSS filtered for Latvia-relevant content. Canada DND for brigade rotation details. Addresses blind spot identified in Source Intelligence Map."

  - id: lv_eu_council
    name: EU Council / EEAS
    domain: consilium.europa.eu
    entry_url: "https://www.consilium.europa.eu/en/press/press-releases/"
    rss_feed: "https://www.consilium.europa.eu/en/press/press-releases/?filters=2026"  # [VERIFY RSS endpoint]
    language: en
    type: institutional
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_with_keyword_filter
    poll_interval_hours: 12
    keyword_filter: ["Latvia", "Baltic", "Eastern", "Russia sanctions"]
    notes: "Council conclusions, sanctions packages. Minister Braže statements at FAC published here."

  - id: lv_baltic_assembly
    name: Baltic Assembly
    domain: baltasam.org
    entry_url: "https://www.baltasam.org/"
    rss_feed: null  # [VERIFY]
    language: en
    type: institutional
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: monthly
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Low-frequency but signals Baltic consensus positions. NB8 statements captured via president.lv/mk.gov.lv."

# Shared gov.lv CMS configuration
gov_lv_shared_config:
  base_url_pattern: "https://www.{ministry}.gov.lv/en/articles"
  ministries_on_platform:
    - mk    # Cabinet of Ministers
    - mfa   # Foreign Affairs
    - mod   # Defence (note: news at /en/zinas not /en/articles)
    - fm    # Finance
    - em    # Economics
    - knab  # Corruption Prevention Bureau
  rss_pattern: "https://www.{ministry}.gov.lv/en/rss/articles"
  rss_verified:
    - mfa   # Functional
    - em    # Functional
  rss_page_exists_but_empty:
    - mk
    - fm
    - president.lv  # Not on gov.lv but same behavior
  cms: drupal
  pagination: query_parameter  # ?page=N
  bot_protection: none_observed
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "lv,en;q=0.9"
  rate_limit: "max 1 request per 2 seconds per ministry"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Latvian government communications are generally factual and less prone to the systematic optimism seen in some countries, but they remain selective in what they emphasize and omit. The pipeline must treat government sources as confirming that the government has chosen to state a fact publicly — the interpretive value lies in what is said, what is omitted, and the timing relative to media coverage.

- **President (president.lv)**: Cross-reference presidential statements with LSM (eng.lsm.lv) analysis and Delfi Latvia coverage. When presidential and prime ministerial framing diverge (possible given the dual-executive structure), it signals internal coalition tension or constitutional boundary disputes. Rinkēvičs's foreign-policy statements carry unusual authority given his decade as Foreign Minister — compare with MFA output to detect where presidential and ministerial positions differ.

- **Cabinet (mk.gov.lv)**: Cross-reference Cabinet decisions with Saeima proceedings (saeima.lv) and IR magazine (ir.lv, investigative). Cabinet-level defense and budget decisions should be triangulated with Finance Ministry data (fm.gov.lv) and LSM budget reporting. The mk.gov.lv aggregation of all ministerial news makes it the fastest indicator of cross-portfolio policy developments.

- **MFA (mfa.gov.lv)**: Diplomatic communications should be triangulated with BNS Latvia (wire service — provides first-mover reporting), LSM English (eng.lsm.lv — contextual analysis), and LIIA (liia.lv — independent foreign policy analysis). When MFA and LIIA framing converge, it suggests policy consensus; divergence indicates policy debate within the expert community. For EU-level positions, cross-reference with EU Council press releases (consilium.europa.eu).

- **MoD/NBS (mod.gov.lv, mil.lv)**: Defense communications report procurement, exercises, and allied cooperation but rarely discuss capability gaps, operational shortfalls, or budget pressures. Cross-reference with Re:Baltica (rebaltica.lv — investigative journalism on defense spending), IR (ir.lv — investigative), and Canadian DND releases (canada.ca — allied perspective on the multinational brigade). The existing Source Intelligence Map notes that no specialist defense-procurement publication exists in Latvia — MoD press releases and investigative journalism must fill this gap.

- **VDD/SAB**: Security service communications are operational (VDD) or strategic (SAB). Cross-reference with LSM defense/security coverage (eng.lsm.lv/article/society/defence/) and Delfi Latvia. When VDD press releases reference joint operations with MIDD or foreign partner services, this signals cross-border intelligence cooperation. Annual reports from both agencies should be analyzed alongside the Saeima's annual foreign policy debate and the National Security Concept.

- **Latvijas Banka**: Macroeconomic data is technically rigorous and independent. Cross-reference with Finance Ministry forecasts (fm.gov.lv) — divergence between Latvijas Banka and FM GDP forecasts signals methodological or policy disagreement. Cross-reference with Dienas Bizness (db.lv — business press interpretation) and the macroeconomics.lv commentary.

- **Latvijas Vēstnesis / Likumi.lv**: Legal text is authoritative and definitive. When media reports on legislation diverge from the gazette text, the gazette is canonical. Sanctions implementation regulations, defense-spending authorizations, and treaty ratifications are only legally binding upon publication in Latvijas Vēstnesis.

**4.2 The dual-executive dynamic**

Latvia's President and Prime Minister operate in overlapping spheres that create interpretive complexity:
- The **President** chairs the National Security Council, represents Latvia at European Council summits, and has constitutional authority to propose the dissolution of the Saeima
- The **Prime Minister** leads day-to-day government policy through the Cabinet of Ministers
- Foreign and security policy is effectively shared — the MFA reports to the PM but the President's constitutional role and Rinkēvičs's personal authority create a dual-authority pattern
- Both president.lv and mk.gov.lv must be monitored for foreign/security policy signals; divergence between the two is an analytically significant indicator

**4.3 The trilateral security agency problem**

Latvia has three security/intelligence agencies (VDD, SAB, MIDD) with overlapping mandates and different publication patterns:
- **VDD** (State Security Service): Most active publisher. Counterintelligence, counterterrorism, election security. 2-4 press releases per month plus annual report.
- **SAB** (Constitution Protection Bureau): Annual report only (January). Strategic threat assessment — Russian hybrid instruments, cyber attacks.
- **MIDD** (Defence Intelligence and Security Service): Effectively silent. National SIGINT authority.

The pipeline should: (a) treat any MIDD or SAB publication as a high-priority anomaly, (b) cross-reference VDD press releases with MoD and MFA communications for context, (c) monitor both VDD and SAB annual reports as anchor documents for the annual threat assessment cycle. The existing Source Intelligence Map correctly identifies SAB annual reports as key sources for understanding the Russian-speaking community dynamics blind spot.

**4.4 The Russian-language monitoring gap**

The existing Source Intelligence Map identifies the Russian-language information space as a critical coverage gap, exacerbated by the 2026 ban on Russian-language public media content. Government sources are published in Latvian and English — none publish in Russian. This means government communications about policies affecting the Russian-speaking community (approximately 25% of the population) cannot be triangulated against Russian-language community sentiment through official channels. The pipeline must supplement with rus.delfi.lv (the primary remaining Russian-language news portal) for community-level reception of government policy. VDD and SAB annual reports provide the security services' assessment of this information space.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Gov.lv CMS Architecture

Six of Latvia's government source categories operate on the shared gov.lv Drupal CMS (mk, mfa, mod, fm, em, knab). This creates partial extraction efficiency but with important caveats:

- **URL pattern**: `https://www.{ministry}.gov.lv/en/articles` for most ministries — **exception**: MoD uses `/en/zinas` for news
- **Article URL pattern**: `https://www.{ministry}.gov.lv/en/article/{slug}`
- **Pagination**: `?page=N` query parameter
- **RSS pattern**: `https://www.{ministry}.gov.lv/en/rss/articles` — but only MFA and EM have functional feeds; others return empty pages
- **No bot protection observed** on any gov.lv site
- **Template is consistent** but not identical — some ministries have additional category filters (mk.gov.lv has 20+ categories)

Sources outside gov.lv (president.lv, saeima.lv, bank.lv, vdd.gov.lv, sab.gov.lv, midd.gov.lv, mil.lv, vestnesis.lv, knab.gov.lv) operate on fully independent infrastructure requiring individual scrapers.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Only two domestic government sources provide verified functional RSS feeds:

1. **MFA** (`mfa.gov.lv/en/rss/articles`): RSS 2.0, ~20 items, titled "RSS jaunumi". Verified functional March 2026. This is the highest-value RSS source — P1 priority, daily publication, comprehensive English content.

2. **Ministry of Economics** (`em.gov.lv/en/rss/articles`): RSS 2.0, ~20 items. Verified functional March 2026. P2 priority.

Additionally, external sources provide RSS:
3. **NATO Newsroom** (`nato.int/cps/en/natolive/news.rss`): Requires keyword filtering for Latvia/Baltic relevance.
4. **EU Council**: Press release feeds available with topic filtering.

All other sources require HTML scraping. The gov.lv CMS RSS infrastructure exists (pages at `/en/rss`) but most ministries return "No RSS feeds available right now" — this may change as the digital team enables feeds. The pipeline should periodically recheck `/en/rss` pages for mk.gov.lv, fm.gov.lv, and mod.gov.lv.

### 5.3 PDF Extraction Requirements

Three sources publish significantly in PDF:
- **Latvijas Vēstnesis**: Legal texts are HTML on vestnesis.lv (post-2013) but some documents have PDF attachments. Likumi.lv consolidated laws are HTML.
- **Latvijas Banka**: Formal publications (Annual Report, Financial Stability Report, Macroeconomic Projections) are multi-page PDF. Well-structured, text-based.
- **VDD/SAB Annual Reports**: High-value PDF documents (50-80 pages). English translations available. Text-based PDF, extractable.
- **MoD Annual Reports**: Available at `/en/about-us/annual-reports-ministry-defence`. PDF format.

### 5.4 Language and Encoding

All government sources publish in Latvian as the primary language. English versions are available for most sources but with varying completeness:
- **Comprehensive English**: MFA (near-complete), Latvijas Banka (Eurosystem requirement), president.lv (near-complete)
- **Substantial English**: MoD, VDD, SAB (annual reports), mk.gov.lv, em.gov.lv
- **Limited English**: fm.gov.lv, saeima.lv (key items only), KNAB
- **Latvian only**: Latvijas Vēstnesis/likumi.lv (some unofficial English translations), MIDD (overview only)

All gov.lv CMS content is UTF-8 encoded. Independent sites (president.lv, saeima.lv, bank.lv) are also UTF-8. No encoding issues observed.

For pipeline purposes, English-language endpoints (`/en/`) should be preferred where available. For the gazette (vestnesis.lv) and legislation (likumi.lv), Latvian-language monitoring with automated translation is required. The localized query vocabulary in the existing Source Intelligence Map (section "Localized Query Vocabulary") provides the necessary Latvian-language search terms.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- Cabinet decisions appear on mk.gov.lv **and** on the originating ministry's site (e.g., a defense budget decision on both mk.gov.lv and mod.gov.lv)
- Presidential foreign-policy statements appear on president.lv **and** may be echoed on mfa.gov.lv
- NB8/Baltic cooperation statements appear on president.lv/mk.gov.lv **and** on baltasam.org
- Legislative acts appear in Latvijas Vēstnesis (vestnesis.lv) **and** on likumi.lv (consolidated) **and** in Saeima proceedings
- Defense/security items may appear on mod.gov.lv, mil.lv, mk.gov.lv, and in VDD/SAB press releases

Implement content-hash deduplication. Use the originating institution as canonical: MFA for diplomatic, MoD for defense, FM for fiscal, VDD/SAB for security, vestnesis.lv for legal text. When mk.gov.lv aggregation captures an item before the ministry's own site publishes it, use mk.gov.lv as the timestamp source but the ministry site as the canonical source.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-RSS | MFA | Every 2 hours (RSS) | Verified RSS, daily publication, highest diplomatic value |
| P1-Scrape | President, Cabinet, MoD, NBS | Every 2-4 hours | Daily/near-daily publication, security-critical |
| P2-RSS | Ministry of Economics | Every 12 hours (RSS) | Verified RSS, moderate frequency |
| P2-Active | Saeima, FM, Latvijas Banka, KNAB, VDD | Every 6-12 hours | Regular publishing, moderate priority |
| P2-Periodic | Latvijas Vēstnesis, SAB, NATO eFP, EU Council | Every 6-24 hours | Daily (gazette) or infrequent but high-value |
| P2-Minimal | MIDD, Baltic Assembly, NSC | Weekly | Effectively silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| Gov.lv CMS outage | mk, mfa, mod, fm, em, knab | Monitor @Abordziba (MoD), @Latvian_MFA, @MK_gov_lv on X. LSM (lsm.lv) typically republishes government communications within 30 minutes. |
| President.lv downtime | President, NSC | Monitor @President_LV on X. LSM covers presidential activities comprehensively. |
| Saeima.lv downtime | Saeima | IPEX (secure.ipex.eu) for EU-related parliamentary activity. LSM parliamentary coverage. |
| MFA RSS feed failure | MFA | Fall back to HTML scraping of `mfa.gov.lv/en/articles`. Monitor @Latvian_MFA on X. |
| VDD/SAB website downtime | VDD, SAB | Annual reports available via multiple mirrors (EU security cooperation portals). Operational press releases echoed by LSM and BNS within minutes. |
| Bank.lv downtime | Latvijas Banka | ECB website (ecb.europa.eu) for monetary policy decisions. macroeconomics.lv for analysis. |
| Vestnesis.lv downtime | Official Gazette | Likumi.lv provides the same legal text in consolidated form. N-Lex (n-lex.europa.eu) provides EU-level access to Latvian legislation. |
| NATO/EU site restructuring | NATO eFP, EU Council | NATO press releases available via multiple mirror domains. EU Council content mirrored on EEAS. |

---

*This supplement should be reviewed quarterly or upon any major change in government composition (coalition change, new PM/President), restructuring of the gov.lv CMS platform, or changes to the security service institutional architecture. The RSS availability status of gov.lv ministries should be rechecked monthly — the digital team appears to be rolling out RSS incrementally.*
