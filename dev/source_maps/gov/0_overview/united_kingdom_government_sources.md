# Official Government Sources Supplement: UNITED KINGDOM

**Primary language of political discourse: English**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — United Kingdom (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for the United Kingdom. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Government sources in the United Kingdom are structurally centralized through the **GOV.UK** platform — a unified digital portal operated by the Government Digital Service (GDS) within the Cabinet Office. All ministerial departments (No. 10, FCDO, MOD, HM Treasury, DBT) publish press releases, policy papers, speeches, and statistical releases through GOV.UK rather than maintaining independent press rooms. Each department has a standardized Atom feed at `https://www.gov.uk/government/organisations/{org-slug}.atom`. This creates a single extraction pattern for most departments and a highly consistent data structure. However, it also means a single point of failure if GOV.UK experiences downtime or restructuring. Key institutions outside GOV.UK — the Bank of England, Parliament (Hansard, select committees), The Gazette, and devolved administrations (Scottish Government, Welsh Government, Northern Ireland Executive) — maintain fully independent web infrastructure with varying levels of machine-readable access.

---

## 1. OFFICIAL GOVERNMENT SOURCES: UNITED KINGDOM

### 1.1 Head of Government — Prime Minister's Office (10 Downing Street)

| Field | Detail |
|---|---|
| **Institution** | Prime Minister's Office, 10 Downing Street |
| **Domain** | `gov.uk/government/organisations/prime-ministers-office-10-downing-street` |
| **Entry Point URL** | `https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street` |
| **Atom Feed** | **Yes.** `https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street.atom` |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defence autonomy, Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily. Readouts of bilateral meetings, press conference transcripts, statements on international events, policy announcements, and appointment notices. Volume increases during international summits and crises. |
| **Content Format** | HTML on GOV.UK. Atom feed provides structured entries with title, summary, and link to full-text HTML page. Some attached PDFs for joint communiques and formal agreements. |
| **Extraction Method** | Atom feed polling. Each entry links to a full-text HTML article page at `gov.uk/government/news/{slug}` or `gov.uk/government/speeches/{slug}`. |
| **Editorial Orientation** | Official government position. All content produced by No. 10 communications team. Framing reflects governing party (Labour, as of 2024) policy priorities. |
| **Why This Source** | The single authoritative source for PM bilateral meeting readouts, Downing Street press conference transcripts, and statements on foreign and defence policy. PM readouts — particularly the formula used to describe discussions with foreign leaders — are primary indicators of diplomatic alignment shifts. |
| **Access Notes** | No paywall, no authentication required. GOV.UK is well-engineered for machine access; Atom feeds are reliable and well-maintained. No bot protection observed on feed endpoints. |

**Additional entry points:**
- Press conferences and speeches: `https://www.gov.uk/search/news-and-communications?organisations%5B%5D=prime-ministers-office-10-downing-street&content_store_document_type%5B%5D=speech`
- Email subscription: `https://www.gov.uk/email-signup?link=/government/organisations/prime-ministers-office-10-downing-street`

---

### 1.2 Foreign Ministry — Foreign, Commonwealth & Development Office (FCDO)

| Field | Detail |
|---|---|
| **Institution** | Foreign, Commonwealth & Development Office (FCDO) |
| **Domain** | `gov.uk/government/organisations/foreign-commonwealth-development-office` |
| **Entry Point URL** | `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office` |
| **Atom Feed** | **Yes.** `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom` |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Multiple times daily. Comunicados for diplomatic meetings, sanctions designations, travel advisories, ministerial statements, ODA allocations, consular notices, and ambassador appointments. |
| **Content Format** | HTML on GOV.UK. Sanctions listings and treaty texts often in PDF. Country-specific travel advice in structured HTML. |
| **Extraction Method** | Atom feed polling. Filtered searches available: `https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D=foreign-commonwealth-development-office` |
| **Editorial Orientation** | Official foreign policy position. Under Foreign Secretary David Lammy, communications emphasize "progressive realism," NATO commitment, and post-Brexit bilateral relationship-building. |
| **Why This Source** | The only primary source for UK diplomatic positions, sanctions designations, treaty actions, bilateral meeting readouts (when led by the Foreign Secretary rather than PM), and ambassador appointments. All UK media diplomatic reporting derives from FCDO statements or is triangulated against them. |
| **Access Notes** | Same GOV.UK infrastructure as No. 10. FCDO Newsdesk (monitored 24/7) can be contacted via press@fcdo.gov.uk. Development Tracker at `devtracker.fcdo.gov.uk` provides open data on UK aid spending. |

**Additional entry points:**
- Sanctions: `https://www.gov.uk/government/collections/uk-sanctions-list`
- Travel advice (all countries): `https://www.gov.uk/foreign-travel-advice`
- FCDO Development Tracker: `https://devtracker.fcdo.gov.uk/`
- World news stories (by country): `https://www.gov.uk/search/news-and-communications?organisations%5B%5D=foreign-commonwealth-development-office&world_locations%5B%5D={country-slug}`

---

### 1.3 Defence Ministry — Ministry of Defence (MOD)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Defence (MOD) |
| **Domain** | `gov.uk/government/organisations/ministry-of-defence` |
| **Entry Point URL** | `https://www.gov.uk/government/organisations/ministry-of-defence` |
| **Atom Feed** | **Yes.** `https://www.gov.uk/government/organisations/ministry-of-defence.atom` |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defence autonomy, Diplomatic alignment |
| **Publication Frequency** | Daily. Press releases covering deployments, procurement announcements, defence cooperation agreements, service personnel matters, and operational updates. Volume increases during active deployments or defence reviews. |
| **Content Format** | HTML on GOV.UK. Defence statistics and equipment plans in PDF. Strategic Defence Review and White Papers in PDF. |
| **Extraction Method** | Atom feed polling. Same GOV.UK template as other departments. |
| **Editorial Orientation** | Official defence policy position. MOD communications emphasize NATO commitment, force readiness, and the UK's "NATO First" posture from the 2025 Strategic Defence Review. Defence procurement communications systematically highlight economic benefits (jobs, industrial base) rather than cost overruns. |
| **Why This Source** | The only authoritative source for deployment announcements, defence cooperation agreements, procurement decisions, and force structure changes. The 2025 SDR commitment to 2.5% GDP defence spending by 2027 makes MOD budget execution communications particularly important. |
| **Access Notes** | Same GOV.UK infrastructure. Defence Equipment & Support (DE&S) has a separate news section at `des.mod.uk/news/`. MOD Press Office on X: @DefenceHQPress. |

**Additional entry points:**
- MOD statistics and data: `https://www.gov.uk/government/organisations/ministry-of-defence/about/statistics`
- Defence Equipment Plan: published annually via GOV.UK publications
- UK Defence Intelligence updates on Ukraine: published via @DefenceHQ on X (frequently cited by media but not on GOV.UK in real-time)

---

### 1.4 Parliament — House of Commons, House of Lords, Hansard, Select Committees

#### 1.4a Hansard (Official Report of Parliamentary Debates)

| Field | Detail |
|---|---|
| **Institution** | Hansard — Official Report |
| **Domain** | `hansard.parliament.uk` |
| **Entry Point URL** | `https://hansard.parliament.uk/` |
| **RSS/Atom Feed** | None available on hansard.parliament.uk itself. Parliament provides RSS feeds for bills at `parliament.uk/site-information/rss-feeds/` but Hansard debates do not have a dedicated RSS feed. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — verbatim record of parliamentary debate |
| **Publication Frequency** | Daily during sitting periods (typically Mon-Thu for Commons, Mon-Wed for Lords). An uncorrected "rolling" feed is published approximately 3 hours after the sitting commences; a corrected, searchable version replaces it by 6am the next working day. |
| **Content Format** | HTML. Structured by sitting day, debate, and contribution. Full-text searchable. |
| **Extraction Method** | HTML scraping of `hansard.parliament.uk/commons/latestsittingday` and `hansard.parliament.uk/lords/latestsittingday`. The Parliament API at `api.parliament.uk` provides some structured data access, though Hansard speech data has limited API coverage. TheyWorkForYou (`theyworkforyou.com/api/`) provides a third-party API wrapper. |
| **Editorial Orientation** | Verbatim record — no editorial orientation. Hansard is the constitutional record of everything said in Parliament. |
| **Why This Source** | Ministerial statements, oral questions (PMQs, Foreign Secretary questions, Defence Secretary questions), and urgent debates are first-order signals of government policy positions. Opposition questions reveal domestic constraints on external action. The verbatim record captures nuance that media summaries compress or omit. |
| **Access Notes** | Free. No paywall. The Parliament Developer Hub at `developer.parliament.uk` provides API documentation. Historic Hansard (pre-2005) available at `api.parliament.uk/historic-hansard/`. |

#### 1.4b Select Committees (Commons and Lords)

| Field | Detail |
|---|---|
| **Institution** | UK Parliament Select Committees |
| **Domain** | `committees.parliament.uk` |
| **Entry Point URL** | `https://committees.parliament.uk/` |
| **RSS/Atom Feed** | None identified on committees.parliament.uk. [VERIFY RSS] |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — depending on committee |
| **Publication Frequency** | Variable. Reports published upon completion of inquiries (several per committee per session). Oral evidence sessions during sitting periods. Written evidence published on a rolling basis. |
| **Content Format** | HTML for committee pages and oral evidence transcripts. Reports published as HTML with parallel PDF. Written evidence in HTML. |
| **Extraction Method** | HTML scraping of individual committee publication pages. Key committees for this pipeline: Defence Committee (`committees.parliament.uk/committee/24/defence-committee/publications/`), Foreign Affairs Committee, International Relations and Defence Committee (Lords), Treasury Committee, Intelligence and Security Committee (see section 1.9). |
| **Editorial Orientation** | Cross-party. Committee reports reflect negotiated cross-party consensus, making them uniquely valuable — they reveal the range of parliamentary opinion rather than any single party's position. |
| **Why This Source** | Committee inquiry reports and oral evidence sessions produce original intelligence not available elsewhere. FCDO, MOD, and HM Treasury officials testify before committees, and these transcripts contain detailed policy positions that do not appear in press releases. Committee reports on arms exports, defence procurement, and foreign policy are cited as authoritative by media and think tanks. |
| **Access Notes** | Free. No paywall. Publications searchable by committee, session, and keyword at `committees.parliament.uk/publications/`. Oral evidence sessions are broadcast live on `parliamentlive.tv`. |

**Key committees for pipeline monitoring:**

| Committee | Chamber | URL Slug | Domain Coverage |
|---|---|---|---|
| Foreign Affairs Committee | Commons | `committee/78/foreign-affairs-committee/` | Diplomatic alignment, Institutional engagement |
| Defence Committee | Commons | `committee/24/defence-committee/` | Security & defence autonomy |
| Treasury Committee | Commons | `committee/158/treasury-committee/` | Economic & technological statecraft |
| International Trade Committee | Commons | `committee/444/business-and-trade-committee/` | Economic & technological statecraft |
| International Relations & Defence | Lords | `committee/360/international-relations-and-defence-committee/` | Diplomatic alignment, Security & defence |
| Joint Committee on National Security Strategy | Joint | `committee/111/national-security-strategy-joint-committee/` | Security & defence, Diplomatic alignment |

#### 1.4c UK Parliament (Bills and Legislation)

| Field | Detail |
|---|---|
| **Institution** | UK Parliament — Parliamentary Business |
| **Domain** | `parliament.uk` |
| **Entry Point URL** | `https://www.parliament.uk/business/bills-and-legislation/` |
| **RSS/Atom Feed** | **Yes.** Bills before Parliament RSS feed available via `parliament.uk/site-information/rss-feeds/`. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | During session periods. Bills RSS updated as bills progress through stages. |
| **Content Format** | HTML. Bill texts on `bills.parliament.uk`. |
| **Extraction Method** | RSS feed for bill progression. Parliament API at `api.parliament.uk` for structured data. |
| **Editorial Orientation** | Institutional — procedural record. |
| **Why This Source** | Tracks legislation relevant to foreign/defence/trade policy as it progresses through Parliament. The parliamentary prerogative convention (requiring Commons vote before military action) makes bill and motion tracking operationally relevant. |
| **Access Notes** | Free. Parliament API provides structured access to bill data, divisions (votes), and member information. |

---

### 1.5 Official Gazette — The Gazette (London, Edinburgh, Belfast)

| Field | Detail |
|---|---|
| **Institution** | The Gazette (The London Gazette, The Edinburgh Gazette, The Belfast Gazette) |
| **Domain** | `thegazette.co.uk` |
| **Entry Point URL** | `https://www.thegazette.co.uk/` |
| **RSS/Atom Feed** | **Yes.** Atom feed available via search-based URL: `https://www.thegazette.co.uk/all-notices/notice/data.feed?categorycode={code}&results-page-size={n}`. Also supports content negotiation with `Accept: application/atom+xml`. Users can generate custom RSS feeds from saved search criteria via MyGazette accounts. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Gazette is the constitutional publication vehicle for Royal proclamations, statutory instruments, sanctions notices, honours, military promotions, and insolvency notices |
| **Publication Frequency** | Daily (weekdays). Supplements published as needed. Continuous since 1665. |
| **Content Format** | HTML, XML/RDFa, JSON, and PDF. The Gazette provides a full REST API with content in multiple machine-readable formats. Individual notices available as HTML, XML, and JSON. Complete editions available as PDF. |
| **Extraction Method** | REST API polling via Atom feed endpoint. Notice feed pattern: `/{service}/notice/data.feed` where service is `all-notices`, `insolvency`, or `wills-and-probate`. Category codes filter by notice type (e.g., 11 for State notices). Content negotiation supported. Developer documentation at `github.com/TheGazette/DevDocs`. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of legally mandated notices. |
| **Why This Source** | Constitutional requirement: sanctions designations, statutory instruments, royal proclamations, military appointments, and corporate insolvency notices must be gazetted to take legal effect. Sanctions notices in The Gazette are the definitive legal instrument — FCDO press releases announce intent, but gazette notices create the legal obligation. |
| **Access Notes** | Free to search and read. No authentication required for basic access. MyGazette account enables saved searches and custom RSS feeds. API documentation on GitHub. Data reuse information at `thegazette.co.uk/data`. The Gazette is operated by The Stationery Office (TSO) on behalf of HMSO. |

**Key category codes for pipeline monitoring:**

| Category | Code | Relevance |
|---|---|---|
| State/Royal Proclamations | 11 | Diplomatic alignment, institutional |
| Honours & Awards | Various | Institutional engagement |
| Financial sanctions | Various under State | Economic statecraft |
| Military promotions/appointments | Various | Security & defence |

---

### 1.6 Finance Ministry — HM Treasury

| Field | Detail |
|---|---|
| **Institution** | HM Treasury |
| **Domain** | `gov.uk/government/organisations/hm-treasury` |
| **Entry Point URL** | `https://www.gov.uk/government/organisations/hm-treasury` |
| **Atom Feed** | **Yes.** `https://www.gov.uk/government/organisations/hm-treasury.atom` |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | 3-5 per week. Announcements cover fiscal policy, Budget/Spending Review decisions, financial sanctions implementation, investment incentives, freeport designations, and subsidy control decisions. Volume spikes around fiscal events (Budget, Autumn Statement, Spending Review). |
| **Content Format** | HTML on GOV.UK. Budget documents, Red Book, and OBR forecasts published as PDF. Statistical bulletins in PDF and ODS (spreadsheet). |
| **Extraction Method** | Atom feed polling. Same GOV.UK template as other departments. Budget and fiscal event documents require PDF extraction. |
| **Editorial Orientation** | Official fiscal policy position. Under Chancellor Rachel Reeves, communications emphasize fiscal rules compliance, growth strategy, and public investment narrative. Treasury traditionally presents data in the most favourable framing allowed by the fiscal rules. |
| **Why This Source** | Primary source for fiscal policy that directly constrains defence spending, ODA budgets, and trade policy. The defence spending trajectory (2.5% GDP target), aid spending level (0.5% vs 0.7% GNI debate), and sanctions implementation all flow through Treasury. OBR independence provides a counterweight — OBR forecasts published on GOV.UK are less subject to Treasury framing. |
| **Access Notes** | Same GOV.UK infrastructure. Office for Budget Responsibility (OBR) publications at `obr.uk`. HM Revenue & Customs trade statistics at `gov.uk/government/organisations/hm-revenue-customs`. |

**Additional entry points:**
- Budget documents: `https://www.gov.uk/government/collections/budget-documents`
- Fiscal data: `https://www.gov.uk/government/collections/public-finances-statistics`
- Financial sanctions (joint with FCDO): `https://www.gov.uk/government/collections/financial-sanctions-regime-specific-consolidated-lists-and-general-guidance`

---

### 1.7 Central Bank — Bank of England

| Field | Detail |
|---|---|
| **Institution** | Bank of England |
| **Domain** | `bankofengland.co.uk` |
| **Entry Point URL** | `https://www.bankofengland.co.uk/news` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS hub: `https://www.bankofengland.co.uk/rss`. Key feeds include: News, Publications, Speeches, Statistics, Prudential Regulation, Bank Insights, and Events. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary Policy Committee (MPC) decisions: 8 per year (Thursdays at 12:00 noon). Monetary Policy Reports: quarterly. Financial Stability Reports: biannual. Speeches: weekly. Statistics: regular schedule. |
| **Content Format** | HTML for news and commentary. **PDF** for Monetary Policy Reports, Financial Stability Reports, MPC minutes, and working papers. RSS feeds deliver structured summaries with links to full documents. |
| **Extraction Method** | RSS feed polling for all categories. PDF download and extraction for formal reports and MPC minutes. |
| **Editorial Orientation** | Institutionally independent central bank. Communications are data-driven and policy-neutral by statutory mandate. Under Governor Andrew Bailey, the Bank maintains operational independence from HM Treasury, though coordination occurs on financial stability matters. |
| **Why This Source** | The Bank of England is the only source for authoritative monetary policy decisions, inflation forecasts, financial stability assessments, and sterling-relevant economic indicators. MPC decisions move global markets. The Bank's Financial Policy Committee assessments of systemic risk are primary indicators for economic statecraft analysis. Speeches by MPC members are closely parsed for forward guidance signals. |
| **Access Notes** | No paywall. No bot protection observed on RSS endpoints. Well-maintained, reliable feeds. Email subscription service also available. The Bank also has a GOV.UK presence at `gov.uk/government/organisations/bank-of-england` but the primary content hub is `bankofengland.co.uk`. |

**Key RSS feed URLs:**

| Feed | URL |
|---|---|
| News | `https://www.bankofengland.co.uk/rss/news` |
| Publications | `https://www.bankofengland.co.uk/rss/publications` |
| Speeches | `https://www.bankofengland.co.uk/rss/speeches` |
| Statistics | `https://www.bankofengland.co.uk/rss/statistics` |
| Prudential Regulation | `https://www.bankofengland.co.uk/rss/prudential-regulation-publications` |
| Bank Insights | `https://www.bankofengland.co.uk/rss/bank-insights` |
| Events | `https://www.bankofengland.co.uk/rss/events` |

---

### 1.8 Trade Ministry — Department for Business and Trade (DBT)

| Field | Detail |
|---|---|
| **Institution** | Department for Business and Trade (DBT) |
| **Domain** | `gov.uk/government/organisations/department-for-business-and-trade` |
| **Entry Point URL** | `https://www.gov.uk/government/organisations/department-for-business-and-trade` |
| **Atom Feed** | **Yes.** `https://www.gov.uk/government/organisations/department-for-business-and-trade.atom` |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 3-5 per week. Communications cover trade negotiations, FTA progress, investment screening decisions (National Security and Investment Act), export control changes, tariff adjustments, freeport designations, and trade statistics. |
| **Content Format** | HTML on GOV.UK. Trade agreement texts in PDF. Statistical releases in PDF and ODS. |
| **Extraction Method** | Atom feed polling. Same GOV.UK template as other departments. |
| **Editorial Orientation** | Official trade policy position. DBT was formed in February 2023 by merging the Department for International Trade (DIT) and elements of the Department for Business, Energy & Industrial Strategy (BEIS). Communications emphasize UK's post-Brexit independent trade policy, CPTPP membership, and investment attraction. |
| **Why This Source** | Primary source for trade agreement negotiations, CPTPP implementation, investment screening decisions under the National Security and Investment Act 2021, export control changes, and trade statistics. Post-Brexit, UK trade policy is a primary instrument of diplomatic alignment — FTA partner selection signals strategic orientation. |
| **Access Notes** | Same GOV.UK infrastructure. The predecessor Department for International Trade archives remain accessible at `gov.uk/government/organisations/department-for-international-trade`. Trade data also at `uktradeinfo.com` (HMRC). |

**Additional entry points:**
- Trade agreements tracker: `https://www.gov.uk/government/collections/the-uks-trade-agreements`
- National Security and Investment Act decisions: `https://www.gov.uk/government/collections/national-security-and-investment-act`
- Export control notices: `https://www.gov.uk/government/collections/strategic-export-controls`

---

### 1.9 Intelligence / National Security — SIS (MI6), GCHQ, MI5, Intelligence and Security Committee (ISC), National Security Council (NSC)

#### 1.9a Secret Intelligence Service (SIS / MI6)

| Field | Detail |
|---|---|
| **Institution** | Secret Intelligence Service (SIS / MI6) |
| **Domain** | `sis.gov.uk` |
| **Entry Point URL** | `https://www.sis.gov.uk/` |
| **RSS/Atom Feed** | None available. |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible. SIS publishes virtually no operational or policy communications. The website is primarily a recruitment and institutional information portal. The Chief of SIS ("C") delivers occasional public speeches (1-2 per year), which are published on the site. |
| **Content Format** | HTML. Speeches in HTML. |
| **Extraction Method** | Periodic check of `sis.gov.uk` for new speeches or institutional statements. |
| **Editorial Orientation** | N/A — effectively silent on operational matters. |
| **Why This Source** | Included for completeness. SIS's public-facing communications are almost nonexistent. However, speeches by the Chief of SIS are high-signal events — each one is extensively analysed by media and think tanks. The most recent public speeches have addressed China, Russia, and technology-enabled espionage. When "C" speaks publicly, it is a deliberate strategic communication. |
| **Access Notes** | Public website. No paywall. No bot protection. |

#### 1.9b Government Communications Headquarters (GCHQ)

| Field | Detail |
|---|---|
| **Institution** | Government Communications Headquarters (GCHQ) |
| **Domain** | `gchq.gov.uk` |
| **Entry Point URL** | `https://www.gchq.gov.uk/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Economic & technological statecraft |
| **Publication Frequency** | Low. GCHQ publishes more frequently than SIS — press releases on cybersecurity advisories, institutional events, and technology partnerships appear several times per month. The National Cyber Security Centre (NCSC), a public-facing arm of GCHQ, publishes more regularly. |
| **Content Format** | HTML. NCSC advisories in structured HTML. |
| **Extraction Method** | HTML scraping. NCSC alerts and advisories at `ncsc.gov.uk` are the higher-value monitoring target. |
| **Editorial Orientation** | Institutional communication. NCSC advisories are technically detailed and operationally useful. GCHQ institutional communications emphasize technology innovation and recruitment. |
| **Why This Source** | NCSC cyber threat advisories are first-order signals of state-attributed cyber threats. GCHQ's rare public statements on signals intelligence partnerships (Five Eyes) and technology policy inform the technological statecraft domain. |
| **Access Notes** | Public website. NCSC at `ncsc.gov.uk` has a more active publication schedule and provides email alert subscription. |

**Additional entry point:**
- NCSC advisories and guidance: `https://www.ncsc.gov.uk/section/keep-up-to-date/threat-reports`
- NCSC news: `https://www.ncsc.gov.uk/news`

#### 1.9c Intelligence and Security Committee of Parliament (ISC)

| Field | Detail |
|---|---|
| **Institution** | Intelligence and Security Committee of Parliament (ISC) |
| **Domain** | `isc.independent.gov.uk` |
| **Entry Point URL** | `https://isc.independent.gov.uk/reports/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy |
| **Publication Frequency** | Low. Annual Reports published yearly. Special reports published upon completion of inquiries — typically 2-4 per parliamentary session. Government responses published separately. |
| **Content Format** | PDF for reports. HTML for summaries and press releases. Reports at `isc.independent.gov.uk/wp-content/uploads/`. |
| **Extraction Method** | Periodic check of reports page. PDF download and extraction for full reports. |
| **Editorial Orientation** | Cross-party parliamentary committee. ISC reports reflect negotiated consensus across party lines — making them the most authoritative publicly available assessment of intelligence community performance and priorities. Reports are partially redacted on national security grounds. |
| **Why This Source** | The ISC is the only body with statutory oversight of MI6, MI5, and GCHQ. Its reports — including the China report, Russia report, and International Partnerships report — are the closest the public gets to an official assessment of UK intelligence priorities and capabilities. Government responses to ISC reports reveal how much the executive accepts or resists parliamentary scrutiny of intelligence activity. |
| **Access Notes** | Free. Reports published as accessible PDFs. Government responses also published at `gov.uk/government/publications/`. The ISC's Annual Report 2023-2025 was published in December 2025. |

#### 1.9d National Security Council (NSC)

| Field | Detail |
|---|---|
| **Institution** | National Security Council |
| **Domain** | `gov.uk` (no dedicated site) |
| **Entry Point URL** | N/A — the NSC has no public-facing web presence |
| **RSS/Atom Feed** | None. |
| **Language** | English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defence autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible direct output. NSC decisions surface through No. 10 statements, FCDO/MOD announcements, and the Integrated Review / Strategic Defence Review documents. |
| **Content Format** | N/A. |
| **Extraction Method** | No direct monitoring possible. NSC-relevant signals are captured through No. 10 and FCDO feeds. |
| **Editorial Orientation** | N/A. |
| **Why This Source** | Included for completeness. The NSC is the apex decision-making body for UK national security and foreign policy, chaired by the PM. It produces no public output — its decisions are communicated through departmental channels. The Integrated Review and Strategic Defence Review are the NSC's primary public-facing products, published as GOV.UK policy papers. |
| **Access Notes** | The National Security Adviser leads the NSC secretariat. NSC membership and terms of reference published at `gov.uk/government/groups/national-security-council`. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Scottish Government (gov.scot)

| Field | Detail |
|---|---|
| **Institution** | Scottish Government |
| **Domain** | `gov.scot` |
| **Entry Point URL** | `https://www.gov.scot/news/` |
| **RSS/Atom Feed** | None confirmed. The Scottish Government offers email subscription (daily/weekly alerts via Mailchimp) but no RSS/Atom feed was identified on the news page. [VERIFY RSS] |
| **Language** | English (primary); some publications bilingual English/Gaelic |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment (on devolved matters with foreign policy implications) |
| **Publication Frequency** | Daily. News releases, ministerial statements, policy publications, and First Minister's engagements. |
| **Content Format** | HTML. Publications in HTML and PDF. |
| **Extraction Method** | HTML scraping of `gov.scot/news/`. Email subscription available via `eepurl.com/gEp6KP`. |
| **Editorial Orientation** | Devolved government position (currently SNP-led). Communications may diverge from UK Government positions on defence (Trident basing at Faslane/Coulport), immigration, and EU relations. |
| **Why This Source** | Scottish Government positions on Trident, NATO (in context of independence), immigration, and EU alignment directly constrain or complicate UK foreign and defence policy. Faslane is home to the UK's entire submarine-based nuclear deterrent — Scottish Government positions on nuclear weapons are operationally significant. The Scottish Government's external affairs activity (e.g., engagement with EU institutions, Nordic cooperation) creates a second diplomatic channel that sometimes diverges from FCDO positions. |
| **Access Notes** | Free. Scottish Parliament (Holyrood) at `parliament.scot` is the legislative body — separate from the Scottish Government. |

#### 1.10b Welsh Government (gov.wales)

| Field | Detail |
|---|---|
| **Institution** | Welsh Government |
| **Domain** | `gov.wales` |
| **Entry Point URL** | `https://media.service.gov.wales/news/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English and Welsh (bilingual by statutory requirement) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints |
| **Publication Frequency** | Daily. Press releases, ministerial statements, and policy publications. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of media.service.gov.wales. Senedd (Welsh Parliament) media at `senedd.wales/media/`. |
| **Editorial Orientation** | Devolved government position (currently Labour-led, aligned with UK Government on most foreign/defence policy). |
| **Why This Source** | Lower priority than Scottish Government for foreign/defence analysis, but relevant for (a) Welsh defence industry and procurement (e.g., steelworks in Port Talbot with defence supply chain implications), (b) post-Brexit trade impacts on Welsh agriculture, and (c) intra-Labour party dynamics when Welsh Labour diverges from Westminster Labour. |
| **Access Notes** | Free. `gov.wales` is bilingual English/Welsh. Senedd Cymru (Welsh Parliament) at `senedd.wales`. |

#### 1.10c Northern Ireland Executive (northernireland.gov.uk)

| Field | Detail |
|---|---|
| **Institution** | Northern Ireland Executive |
| **Domain** | `northernireland.gov.uk` |
| **Entry Point URL** | `https://www.northernireland.gov.uk/press-releases` |
| **RSS/Atom Feed** | RSS alerts available on the press releases page. [VERIFY RSS URL] |
| **Language** | English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment (Windsor Framework), Economic & technological statecraft |
| **Publication Frequency** | Variable. Dependent on power-sharing stability — the Executive was suspended from February 2022 to February 2024. When operational, daily press releases. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping or RSS (if confirmed) of press releases page. Northern Ireland Assembly at `niassembly.gov.uk` for legislative business. |
| **Editorial Orientation** | Coalition government (DUP/Sinn Féin power-sharing). Communications reflect cross-community consensus, which means they are bland on controversial issues and substantive only on agreed positions. |
| **Why This Source** | The Windsor Framework (governing Northern Ireland's post-Brexit trading arrangements) makes Northern Ireland Executive communications uniquely relevant to UK-EU relations and trade policy. Stormont's positions on border arrangements, regulatory alignment, and the Protocol directly affect UK diplomatic and trade posture. The identified blind spot in the Source Intelligence Map — "Northern Ireland power-sharing dynamics receive minimal coverage in London-based media" — makes direct monitoring essential. |
| **Access Notes** | Free. The Executive Office at `executiveoffice-ni.gov.uk` covers First and deputy First Minister communications. NI Assembly at `niassembly.gov.uk` for committee proceedings and debates. Belfast Telegraph and Irish News (cited in gb.yaml blind spots) provide supplementary coverage. |

#### 1.10d Crown Dependencies (Jersey, Guernsey, Isle of Man)

| Field | Detail |
|---|---|
| **Institution** | Crown Dependencies — States of Jersey, States of Guernsey, Isle of Man Government |
| **Domain** | `gov.je` / `gov.gg` / `gov.im` |
| **Entry Point URL** | `https://www.gov.je/News/Pages/index.aspx` / `https://www.gov.gg/news` / `https://www.gov.im/news/` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Variable. Lower volume than devolved administrations. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. Low priority — periodic manual check sufficient unless a sanctions/financial regulation issue escalates. |
| **Editorial Orientation** | Self-governing dependencies with independent fiscal and regulatory frameworks. |
| **Why This Source** | Crown Dependencies are significant offshore financial centres. Jersey, Guernsey, and the Isle of Man are outside the UK but the UK is responsible for their defence and international relations. Financial sanctions, beneficial ownership transparency, and tax regulation changes in Crown Dependencies have implications for UK economic statecraft and City of London regulatory alignment. Monitor only when sanctions, financial regulation, or beneficial ownership issues escalate. |
| **Access Notes** | Free. Low-priority monitoring. |

#### 1.10e Legislation.gov.uk

| Field | Detail |
|---|---|
| **Institution** | The National Archives — Legislation.gov.uk |
| **Domain** | `legislation.gov.uk` |
| **Entry Point URL** | `https://www.legislation.gov.uk/new` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Atom feeds for all legislation types: UK Public General Acts, UK Statutory Instruments, Scottish Statutory Instruments, Acts of Senedd Cymru, Northern Ireland legislation, and draft legislation. Feed URL pattern: `https://www.legislation.gov.uk/new/{type}/data.feed` |
| **Language** | English (Welsh for Senedd legislation) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — legislation is the binding output of policy across all areas |
| **Publication Frequency** | Daily. New legislation published simultaneously or within 24 hours of its printed form. Published by publication date rather than enactment date. |
| **Content Format** | HTML and XML. Legislation text available in HTML, XML (CLML — Crown Legislation Markup Language), PDF, and RDF. Atom feeds provide structured metadata. |
| **Extraction Method** | Atom feed polling. Feeds support pagination and archiving. Developer documentation at `legislation.gov.uk/developer/formats/atom`. |
| **Editorial Orientation** | Official legal text. No editorial content. |
| **Why This Source** | Complements The Gazette as the definitive source of enacted legislation. Statutory Instruments implementing sanctions, trade agreements, defence procurement regulations, and export controls are published here. The structured XML format enables automated detection of new legislation by subject area. |
| **Access Notes** | Free. Open data under Open Government Licence. Full developer documentation available. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS/Atom Available | Priority | Content Format | Frequency | GOV.UK Platform |
|---|---|---|---|---|---|---|---|
| 1 | PM's Office (No. 10) | `gov.uk/government/organisations/prime-ministers-office-10-downing-street` | **Yes** (Atom) | P1 | HTML | Daily | Yes |
| 2 | FCDO | `gov.uk/government/organisations/foreign-commonwealth-development-office` | **Yes** (Atom) | P1 | HTML/PDF | Multiple daily | Yes |
| 3 | MOD | `gov.uk/government/organisations/ministry-of-defence` | **Yes** (Atom) | P1 | HTML/PDF | Daily | Yes |
| 4a | Hansard | `hansard.parliament.uk` | No | P2 | HTML | Daily (sitting) | No |
| 4b | Select Committees | `committees.parliament.uk` | [VERIFY] | P2 | HTML/PDF | Variable | No |
| 4c | Parliament (Bills) | `parliament.uk` | **Yes** (RSS) | P2 | HTML | Session | No |
| 5 | The Gazette | `thegazette.co.uk` | **Yes** (Atom/API) | P2 | HTML/XML/JSON/PDF | Daily | No |
| 6 | HM Treasury | `gov.uk/government/organisations/hm-treasury` | **Yes** (Atom) | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | Bank of England | `bankofengland.co.uk` | **Yes** (RSS, multiple) | P2 | HTML/PDF/RSS | Variable | No |
| 8 | DBT | `gov.uk/government/organisations/department-for-business-and-trade` | **Yes** (Atom) | P2 | HTML/PDF | 3-5/week | Yes |
| 9a | SIS (MI6) | `sis.gov.uk` | No | P2 | HTML | Negligible | No |
| 9b | GCHQ / NCSC | `gchq.gov.uk` / `ncsc.gov.uk` | [VERIFY] | P2 | HTML | Low/Monthly | No |
| 9c | ISC | `isc.independent.gov.uk` | [VERIFY] | P2 | PDF | 2-4/session | No |
| 9d | NSC | N/A (no public site) | No | P2 | N/A | Negligible | No |
| 10a | Scottish Government | `gov.scot/news/` | [VERIFY] | P2 | HTML | Daily | No |
| 10b | Welsh Government | `media.service.gov.wales/news/` | [VERIFY] | P2 | HTML | Daily | No |
| 10c | NI Executive | `northernireland.gov.uk/press-releases` | [VERIFY] | P2 | HTML | Variable | No |
| 10d | Crown Dependencies | `gov.je` / `gov.gg` / `gov.im` | [VERIFY] | P2 | HTML | Low | No |
| 10e | Legislation.gov.uk | `legislation.gov.uk/new` | **Yes** (Atom) | P2 | HTML/XML/PDF | Daily | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# United Kingdom Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/gb.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: gb_pm_office
    name: Prime Minister's Office, 10 Downing Street
    domain: gov.uk
    entry_url: "https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street"
    atom_feed: "https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street.atom"
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: atom_feed
    poll_interval_hours: 2
    notes: "PM bilateral readouts, press conferences, policy announcements. Atom feed well-maintained."

  - id: gb_fcdo
    name: Foreign, Commonwealth & Development Office (FCDO)
    domain: gov.uk
    entry_url: "https://www.gov.uk/government/organisations/foreign-commonwealth-development-office"
    atom_feed: "https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom"
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: multiple_daily
    content_format: html_pdf_mixed
    extraction_method: atom_feed
    poll_interval_hours: 2
    notes: "Diplomatic statements, sanctions designations, travel advisories, ODA. FCDO Newsdesk monitored 24/7."

  - id: gb_mod
    name: Ministry of Defence (MOD)
    domain: gov.uk
    entry_url: "https://www.gov.uk/government/organisations/ministry-of-defence"
    atom_feed: "https://www.gov.uk/government/organisations/ministry-of-defence.atom"
    language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: atom_feed
    poll_interval_hours: 2
    notes: "Deployments, procurement, SDR implementation, NATO commitments. DE&S news at des.mod.uk separate."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: gb_hansard
    name: Hansard (Official Parliamentary Report)
    domain: hansard.parliament.uk
    entry_url: "https://hansard.parliament.uk/"
    atom_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: daily_sitting
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Rolling feed updated ~3hrs after sitting begins. Corrected version by 6am next day. TheyWorkForYou API at theyworkforyou.com/api/ as alternative."

  - id: gb_select_committees
    name: UK Parliament Select Committees
    domain: committees.parliament.uk
    entry_url: "https://committees.parliament.uk/"
    atom_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    key_committees:
      - slug: "committee/78/foreign-affairs-committee/"
        name: Foreign Affairs Committee
      - slug: "committee/24/defence-committee/"
        name: Defence Committee
      - slug: "committee/158/treasury-committee/"
        name: Treasury Committee
      - slug: "committee/360/international-relations-and-defence-committee/"
        name: International Relations and Defence Committee (Lords)
      - slug: "committee/111/national-security-strategy-joint-committee/"
        name: Joint Committee on NSS
    notes: "Committee reports are cross-party consensus documents. Oral evidence transcripts contain original intelligence."

  - id: gb_parliament_bills
    name: UK Parliament Bills
    domain: parliament.uk
    entry_url: "https://www.parliament.uk/business/bills-and-legislation/"
    rss_feed: "https://www.parliament.uk/site-information/rss-feeds/"  # General RSS hub
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: session_period
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 12
    notes: "Bills RSS for tracking legislation through stages. Parliament API at api.parliament.uk for structured data."

  - id: gb_gazette
    name: The Gazette (London, Edinburgh, Belfast)
    domain: thegazette.co.uk
    entry_url: "https://www.thegazette.co.uk/"
    atom_feed:
      all_notices: "https://www.thegazette.co.uk/all-notices/notice/data.feed"
      state_notices: "https://www.thegazette.co.uk/all-notices/notice/data.feed?categorycode=11"
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
    content_format: html_xml_json_pdf
    extraction_method: atom_api
    poll_interval_hours: 6
    notes: "REST API with Atom, JSON, XML output. Sanctions notices are legally binding instruments. Developer docs at github.com/TheGazette/DevDocs."

  - id: gb_hm_treasury
    name: HM Treasury
    domain: gov.uk
    entry_url: "https://www.gov.uk/government/organisations/hm-treasury"
    atom_feed: "https://www.gov.uk/government/organisations/hm-treasury.atom"
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: atom_feed
    poll_interval_hours: 6
    notes: "Fiscal policy, Budget, Spending Review, sanctions implementation. OBR at obr.uk provides independent forecasts."

  - id: gb_bank_of_england
    name: Bank of England
    domain: bankofengland.co.uk
    entry_url: "https://www.bankofengland.co.uk/news"
    rss_feed:
      news: "https://www.bankofengland.co.uk/rss/news"
      publications: "https://www.bankofengland.co.uk/rss/publications"
      speeches: "https://www.bankofengland.co.uk/rss/speeches"
      statistics: "https://www.bankofengland.co.uk/rss/statistics"
      prudential_regulation: "https://www.bankofengland.co.uk/rss/prudential-regulation-publications"
      bank_insights: "https://www.bankofengland.co.uk/rss/bank-insights"
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best machine-readable government source in the UK. Multiple category-specific RSS feeds. MPC decisions 8x/year Thursdays at noon. No bot protection."

  - id: gb_dbt
    name: Department for Business and Trade (DBT)
    domain: gov.uk
    entry_url: "https://www.gov.uk/government/organisations/department-for-business-and-trade"
    atom_feed: "https://www.gov.uk/government/organisations/department-for-business-and-trade.atom"
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: atom_feed
    poll_interval_hours: 12
    notes: "Trade negotiations, FTAs, CPTPP, investment screening (NSI Act), export controls."

  - id: gb_sis
    name: Secret Intelligence Service (SIS / MI6)
    domain: sis.gov.uk
    entry_url: "https://www.sis.gov.uk/"
    atom_feed: null
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent. Chief's speeches (1-2/year) are high-signal events. Flag any new publication as anomaly."

  - id: gb_gchq_ncsc
    name: GCHQ / National Cyber Security Centre (NCSC)
    domain: gchq.gov.uk
    entry_url: "https://www.ncsc.gov.uk/news"
    atom_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: monthly
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "NCSC advisories are higher-value target than GCHQ institutional comms. Cyber threat attribution statements are first-order signals."

  - id: gb_isc
    name: Intelligence and Security Committee (ISC)
    domain: isc.independent.gov.uk
    entry_url: "https://isc.independent.gov.uk/reports/"
    atom_feed: null  # [VERIFY]
    language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-4_per_session"
    content_format: pdf
    extraction_method: periodic_check_and_pdf_extract
    poll_interval_hours: 168  # weekly
    notes: "Annual reports and special inquiry reports. Cross-party consensus documents. China report, Russia report are landmark publications."

  - id: gb_scottish_gov
    name: Scottish Government
    domain: gov.scot
    entry_url: "https://www.gov.scot/news/"
    atom_feed: null  # [VERIFY - email alerts only confirmed]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Trident basing, Scottish independence implications for NATO, EU alignment positions. No RSS confirmed — email subscription via Mailchimp."

  - id: gb_welsh_gov
    name: Welsh Government
    domain: gov.wales
    entry_url: "https://media.service.gov.wales/news/"
    atom_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "Lower priority. Relevant for defence industry (Port Talbot steel), post-Brexit agriculture impacts."

  - id: gb_ni_executive
    name: Northern Ireland Executive
    domain: northernireland.gov.uk
    entry_url: "https://www.northernireland.gov.uk/press-releases"
    atom_feed: null  # [VERIFY - RSS alerts mentioned on page]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Windsor Framework implementation. Power-sharing stability affects output. NI Assembly at niassembly.gov.uk."

  - id: gb_legislation
    name: Legislation.gov.uk
    domain: legislation.gov.uk
    entry_url: "https://www.legislation.gov.uk/new"
    atom_feed:
      all_legislation: "https://www.legislation.gov.uk/new/data.feed"
      uk_public_acts: "https://www.legislation.gov.uk/new/ukpga/data.feed"
      uk_statutory_instruments: "https://www.legislation.gov.uk/new/uksi/data.feed"
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
    content_format: html_xml_pdf
    extraction_method: atom_feed
    poll_interval_hours: 6
    notes: "Statutory Instruments for sanctions, export controls, trade. CLML (XML) format enables automated subject detection."

# GOV.UK shared extraction configuration
gov_uk_shared_config:
  atom_feed_pattern: "https://www.gov.uk/government/organisations/{org-slug}.atom"
  organisations_on_platform:
    - prime-ministers-office-10-downing-street
    - foreign-commonwealth-development-office
    - ministry-of-defence
    - hm-treasury
    - department-for-business-and-trade
  news_search_pattern: "https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D={org-slug}"
  content_url_patterns:
    news: "https://www.gov.uk/government/news/{article-slug}"
    speeches: "https://www.gov.uk/government/speeches/{speech-slug}"
    publications: "https://www.gov.uk/government/publications/{publication-slug}"
  bot_protection: none  # GOV.UK does not employ bot protection on feeds
  rate_limit: "no explicit rate limit documented; recommend max 1 request per 5 seconds"
  encoding: utf-8
  feed_format: atom_1.0
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

UK government communications through GOV.UK are professional, well-structured, and published rapidly — but they are official positions, not independent reporting. The pipeline must treat every government source as confirming only that the government has chosen to state a particular position publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage.

- **No. 10 (PM's Office)**: Cross-reference bilateral meeting readouts against BBC News (for the broadest audience framing) and the Financial Times (for elite/market framing). PM readouts use carefully calibrated diplomatic language — changes in formula (e.g., "raised concerns" vs. "expressed serious concern") are meaningful and should be compared to the other party's readout of the same meeting. Cross-reference with Politico London Playbook for insider Westminster context on the political motivations behind timing and framing.

- **FCDO**: Diplomatic statements should be triangulated with Reuters (fastest independent report on UK diplomatic moves), The Guardian (which frequently publishes FCDO-critical analysis from its foreign correspondent network), and Chatham House analysis (for expert assessment of UK positioning). When FCDO and The Times framing converges precisely, it often signals a managed government briefing — The Times is the establishment outlet most frequently used for deliberate kite-flying.

- **MOD**: Defence press releases report outcomes (deployments, contracts, exercises) but systematically minimise cost overruns, capability gaps, and procurement delays. Cross-reference with RUSI (the most authoritative independent defence analysis), UK Defence Journal (free-access defence news that breaks stories before broadsheet analysis), and Janes (gold-standard technical assessment). The Telegraph has the strongest independent defence reporting tradition among broadsheets and provides the right-flank perspective on whether defence spending commitments are being met.

- **HM Treasury**: Budget and fiscal communications are technically accurate in headline numbers but presentation framing (base period selection, counterfactual assumptions) can obscure trends. The OBR (Office for Budget Responsibility) provides the independent counterweight — its forecasts published on GOV.UK are not subject to Treasury framing. Cross-reference with the Financial Times (sharpest independent fiscal analysis) and The Economist (structural economic assessment).

- **Bank of England**: MPC decisions and Monetary Policy Reports are technically rigorous and less subject to political distortion than Treasury output. However, the emphasis and framing in Governor Bailey's press conferences and MPC members' speeches contain forward guidance signals that require interpretation. Cross-reference with the Financial Times (which employs dedicated BoE-watchers) and Reuters (fastest market-moving wire).

- **Parliament (Hansard/Committees)**: Hansard is verbatim and therefore the most reliable text source. The interpretive challenge is volume — filtering signal from procedural noise. Select committee reports are cross-party consensus documents and carry more weight than individual MP statements. Cross-reference committee findings with IISS and Chatham House analysis (which frequently respond to committee reports) and with The New Statesman and The Spectator for the left-right reaction spectrum.

- **Devolved Administrations**: Scottish Government communications on defence and foreign policy diverge from UK Government positions when independence or Trident are at stake. Cross-reference with BBC Scotland (impartial) and The Herald/The Scotsman (Scottish broadsheets with distinct perspectives). For Northern Ireland, cross-reference Executive communications on Windsor Framework implementation with Belfast Telegraph, Irish News, and Slugger O'Toole (as identified in the gb.yaml blind spots).

**4.2 The GOV.UK centralisation effect**

Five of the UK's ten government source categories publish through the centralised GOV.UK platform with standardised Atom feeds. This creates significant operational efficiency:
- A single feed parser handles all five GOV.UK departments
- Consistent Atom format eliminates per-source parsing logic
- No bot protection on feed endpoints (unlike Mexico's gob.mx Cloudflare challenges)
- URL patterns are stable and well-documented

However, centralisation means:
- Platform-wide outages affect all five departments simultaneously
- Template or feed format changes propagate across all departments
- The Government Digital Service (GDS) controls the publication infrastructure — departments publish content but GDS controls the platform
- Email subscription service (via GOV.UK Notify) is the government's preferred distribution channel, not feeds — long-term feed maintenance is not guaranteed

Sources outside GOV.UK (Bank of England, Parliament, The Gazette, devolved administrations, intelligence agencies) operate on independent infrastructure and are not subject to these constraints.

**4.3 The intelligence silence problem**

The UK's intelligence agencies (MI6/SIS, MI5, GCHQ) produce minimal public communications. This is a structural gap that cannot be filled by direct monitoring. Intelligence-relevant signals surface through:
- ISC reports (the only statutory oversight output — published 2-4 times per session)
- NCSC cyber threat advisories (the public-facing arm of GCHQ, most active of the intelligence agencies online)
- Rare speeches by intelligence chiefs (the Chief of SIS, Director General of MI5, Director of GCHQ each speak publicly 1-2 times per year — these are high-signal events)
- RUSI and IISS analysis (think tanks with close intelligence community relationships)
- Declassified UK (adversarial investigative outlet, FOI-based)
- The Guardian and BBC investigative reporting (both have track records on intelligence stories — Snowden, Skripal)

The pipeline should not allocate significant resources to polling SIS or GCHQ websites but should flag any new publication as a high-priority anomaly.

**4.4 The Five Eyes blind spot**

The gb.yaml configuration identifies "Five Eyes intelligence cooperation" as a blind spot where "classified arrangements rarely surface in open-source reporting." Government sources cannot fill this gap. The ISC's "International Partnerships" report and its government response (published on GOV.UK) are the closest official sources. Supplementary signals come from RUSI analyses, parliamentary questions in Hansard, and occasional leaks to broadsheets. AUKUS-related communications — which bridge defence procurement and intelligence cooperation — surface through MOD and FCDO feeds and are the most visible Five Eyes-adjacent signal.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for GOV.UK

The GOV.UK platform hosts 5 of the primary monitored government endpoints, all with standardised Atom feeds. A single feed parser module can service all five:

- **Atom feed pattern**: `https://www.gov.uk/government/organisations/{org-slug}.atom`
- **Organisation slugs**: `prime-ministers-office-10-downing-street`, `foreign-commonwealth-development-office`, `ministry-of-defence`, `hm-treasury`, `department-for-business-and-trade`
- **Filtered news feed pattern**: `https://www.gov.uk/search/news-and-communications.atom?organisations%5B%5D={org-slug}`
- **Article URL patterns**: `gov.uk/government/news/{slug}`, `gov.uk/government/speeches/{slug}`, `gov.uk/government/publications/{slug}`
- **Rate limit**: No explicit rate limit documented; recommend maximum 1 request per 5 seconds as courtesy
- **Bot protection**: None observed on Atom feed endpoints. GOV.UK is designed for machine access
- **Feed format**: Atom 1.0 (RFC 4287), UTF-8 encoded, `xml:lang="en-GB"`

### 5.2 RSS/Atom-Enabled Sources (Priority for Automation)

The UK has the strongest feed infrastructure of any country in the pipeline. Seven government source categories provide functional RSS or Atom feeds:

1. **GOV.UK departments** (No. 10, FCDO, MOD, HM Treasury, DBT): Standardised Atom feeds. Well-maintained, reliable. 20 entries per feed page. Atom format with proper pagination.

2. **Bank of England**: Seven category-specific RSS feeds (news, publications, speeches, statistics, prudential regulation, bank insights, events). The best machine-readable government source in the UK.

3. **The Gazette**: REST API with Atom, JSON, and XML output. Search-based feeds with category code filtering. The most technically sophisticated government data API in the UK. Developer documentation on GitHub.

4. **Legislation.gov.uk**: Atom feeds for all legislation types with pagination and archiving. Structured XML (CLML) format enables automated subject-area detection.

5. **UK Parliament**: RSS feeds for bills. Hansard does not have feeds but the Parliament API at `api.parliament.uk` provides structured data access for some parliamentary content.

All other sources (devolved administrations, intelligence agencies, select committees) require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Three source categories publish substantially in PDF:
- **Bank of England**: Monetary Policy Reports, Financial Stability Reports, MPC minutes, and working papers are multi-page PDFs. Text-based, well-structured, suitable for standard text extraction.
- **HM Treasury**: Budget documents (Red Book), Spending Reviews, and statistical annexes in PDF. Tables may require structured table extraction (tabula/camelot).
- **ISC Reports**: Annual and special reports published as accessible PDFs. Partially redacted on national security grounds — redacted sections appear as blacked-out text.
- **Select Committee Reports**: Published as both HTML and PDF. HTML version preferred for extraction; PDF as fallback.

### 5.4 Language and Encoding

All government sources publish in English. No translation pipeline required. Specific exceptions:
- Welsh Government (`gov.wales`): Bilingual English/Welsh by statutory requirement. English content is the monitoring target.
- Scottish Government (`gov.scot`): Some publications in Gaelic. English is primary.
- Legislation.gov.uk: Senedd Cymru legislation published bilingually. English version is the monitoring target.

All GOV.UK content is UTF-8 encoded. Parliament, Bank of England, and The Gazette sites are also UTF-8. No legacy encoding issues identified (unlike Mexico's occasional Latin-1 issues).

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A sanctions designation appears in FCDO statements, The Gazette (legally binding notice), HM Treasury (financial sanctions), and legislation.gov.uk (statutory instrument)
- Defence cooperation agreements appear in No. 10 readouts, MOD press releases, and FCDO statements
- Budget and fiscal policy appears in HM Treasury, No. 10, and Bank of England commentary
- Trade agreements appear in DBT, FCDO, No. 10, and The Gazette

Implement content-hash deduplication. Use the following canonical source hierarchy:
- **Sanctions**: The Gazette notice is the legally binding canonical version
- **Legislation**: Legislation.gov.uk is the definitive enacted text
- **Diplomatic**: FCDO statement is canonical for foreign policy; No. 10 readout is canonical for PM-level bilateral
- **Defence**: MOD press release is canonical for operational/procurement matters
- **Fiscal**: HM Treasury announcement is canonical; OBR forecast is the independent counterweight
- **Monetary**: Bank of England MPC decision is canonical and should never be deduplicated against Treasury commentary

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | No. 10, FCDO, MOD | Every 2 hours | Multiple daily publications, policy-critical. Atom feeds make this low-cost. |
| P2-Active | HM Treasury, DBT, Bank of England, The Gazette, Legislation.gov.uk, Hansard | Every 6 hours | Regular publishing schedule. Feed-enabled (except Hansard). |
| P2-Standard | Select Committees, Parliament Bills, Scottish Gov, NI Executive | Every 12 hours | Important but lower frequency. HTML scraping required for most. |
| P2-Low | Welsh Government, NCSC/GCHQ, Crown Dependencies | Every 24 hours | Relevant but slower publication cycle. |
| P2-Minimal | SIS (MI6), ISC | Weekly | Effectively silent; flag any publication as high-priority anomaly. |
| P2-Minimal | NSC | N/A | No direct monitoring possible. Captured via No. 10/FCDO feeds. |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| GOV.UK platform outage | No. 10, FCDO, MOD, HM Treasury, DBT | Monitor @10DowningStreet, @FCDOGovUK, @DefenceHQ, @hmtreasury, @biztradegovuk on X. GOV.UK outages are rare (>99.9% uptime historically) but when they occur, social media posts precede web restoration. GovWire (`govwire.co.uk/rss`) provides third-party RSS aggregation of GOV.UK content. |
| Hansard site unavailable | Hansard | TheyWorkForYou (`theyworkforyou.com`) mirrors Hansard content with API access. Parliament API at `api.parliament.uk` provides alternative structured access. |
| Bank of England RSS disruption | Bank of England | The Bank also publishes major announcements via its GOV.UK page (`gov.uk/government/organisations/bank-of-england`). Financial Times and Reuters provide near-real-time reporting of MPC decisions. |
| The Gazette API disruption | The Gazette | Gazette notices for sanctions are also announced via FCDO press releases. PDF editions available for manual download. TSO operates the site and publishes maintenance notices. |
| Devolved administration sites down | Scottish Gov, Welsh Gov, NI Executive | BBC Scotland, BBC Wales, BBC Northern Ireland provide comprehensive coverage. Social media accounts (@scotgov, @WelshGovernment) remain active during outages. |
| Parliament committee site restructuring | Select Committees | Individual committee X accounts (@CommonsDefence, @CommonsForeign, @CommonsFinance) post publication announcements. Parallel Parliament (`parallelparliament.co.uk`) indexes committee activity. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of the GOV.UK platform, machinery-of-government changes (department mergers/splits), change in government administration, devolution settlement changes, or intelligence community organisational reform.*
