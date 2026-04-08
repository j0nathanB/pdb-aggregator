# Official Government Sources Supplement: SWEDEN

**Primary language of political discourse: Swedish**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Sweden (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Sweden. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Sweden's government web infrastructure is split across two parallel portals: `regeringen.se` (Swedish) and `government.se` (English). Both are operated by the Government Offices (Regeringskansliet) and cover all ministries under a single domain — press releases from the Foreign Ministry, Defence Ministry, and Finance Ministry are all published through the same platform with ministry-level filtering. This creates a centralized extraction pattern similar to Mexico's `gob.mx` but with an important difference: the Swedish system exposes dynamically generated RSS feeds for filtered content, making automation significantly easier. Outside the Regeringskansliet portal, the Riksdag, Riksbank, Försvarsmakten (Armed Forces), and security/intelligence agencies maintain fully independent web infrastructure. Sweden's government transparency culture means most agencies publish proactively, though intelligence and security agencies (SÄPO, MUST, FRA) are characteristically restrained.

---

## 1. OFFICIAL GOVERNMENT SOURCES: SWEDEN

### 1.1 Head of Government — Regeringskansliet (Government Offices)

| Field | Detail |
|---|---|
| **Institution** | Regeringskansliet (Government Offices of Sweden) |
| **Domain** | `regeringen.se` (Swedish) / `government.se` (English) |
| **Entry Point URL** | `https://www.regeringen.se/pressmeddelanden/` (Swedish) / `https://www.government.se/press-releases/` (English) |
| **RSS/Atom Feed** | **Yes — dynamically generated.** The regeringen.se platform generates RSS feeds from any filtered view. The English-language feed for all press releases is available at: `https://www.government.se/Filter/RssFeed?filterType=Taxonomy&filterByType=FilterablePageBase&preFilteredCategories=2069,2070,2071,2072,2073,2074,2075,2076,2077,2078,2079,2082,2083,2124,2125,2126,2127,2128,2129,2130,2131,2132,2133,2134,2135,2137,2138,2139,2140,2141,2142,2143,2144,2145,2146,2147,2189&rootPageReference=0` Ministry-specific feeds can be constructed by filtering by Statsrådsberedningen (Prime Minister's Office) on the press releases page and copying the generated RSS URL. |
| **Language** | Swedish (primary); English (parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Multiple press releases per day covering all ministries. The Prime Minister's Office (Statsrådsberedningen) publishes statements, government decisions (regeringsbeslut), and press conference invitations. |
| **Content Format** | HTML articles on regeringen.se/government.se. Some policy documents and government bills (propositioner) attached as PDF. |
| **Extraction Method** | RSS polling of dynamically generated feeds filtered by Statsrådsberedningen. HTML scraping as fallback. Individual press releases follow URL pattern: `/pressmeddelanden/YYYY/MM/title-slug/`. |
| **Editorial Orientation** | Official government position. All content is produced by the Government Offices' communications staff. Under the Kristersson government (Moderates + Liberals + Christian Democrats, supported by Sweden Democrats via Tidö Agreement), framing reflects center-right coalition priorities: NATO integration, increased defense spending, tighter migration, and law enforcement. |
| **Why This Source** | The single authoritative source for government policy statements, ministerial appointments, government bills, and official positions on NATO, EU, and bilateral relations. Press releases precede or accompany all major policy announcements. |
| **Access Notes** | No paywall, no authentication required. No bot protection observed. The English-language government.se site provides parallel coverage of major announcements but is not comprehensive — some press releases appear only in Swedish. |

**Additional entry points:**
- Government decisions (Regeringsbeslut): `https://www.regeringen.se/regeringens-politik/regeringsbeslut/`
- Speeches: `https://www.regeringen.se/tal/`
- Government bills (Propositioner): `https://www.regeringen.se/rattsliga-dokument/proposition/`
- Prime Minister's page: `https://www.government.se/prime-minister/`

---

### 1.2 Foreign Ministry — Utrikesdepartementet (UD)

| Field | Detail |
|---|---|
| **Institution** | Utrikesdepartementet (Ministry for Foreign Affairs) |
| **Domain** | `regeringen.se` / `government.se` |
| **Entry Point URL** | `https://www.regeringen.se/pressmeddelanden/?teleFilter=Utrikesdepartementet` (Swedish, filtered by UD) / `https://www.government.se/government-of-sweden/ministry-for-foreign-affairs/` (English ministry page) |
| **RSS/Atom Feed** | **Yes — dynamically generated.** Filter the pressmeddelanden page by "Utrikesdepartementet" and use the generated RSS link. The UD travel advisory feed uniquely includes full body text, not just title and summary. |
| **Language** | Swedish (primary); English (parallel site, most diplomatic communications published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Press releases issued for diplomatic meetings, bilateral visits, multilateral positions (UN, EU, NATO, OSCE), sanctions, development aid decisions, consular emergencies. |
| **Content Format** | HTML on regeringen.se. Formal diplomatic statements sometimes bilingual. Policy strategies and country strategies published as PDF. |
| **Extraction Method** | RSS polling of UD-filtered feed. Same regeringen.se platform as Statsrådsberedningen. |
| **Editorial Orientation** | Official foreign policy position. Under Foreign Minister Maria Malmer Stenergard, communications emphasize Sweden's new NATO member posture, transatlantic alignment, support for Ukraine, EU engagement, and values-based foreign policy (democracy, human rights). The UD maintains Sweden's traditional emphasis on multilateralism and development cooperation alongside the NATO pivot. |
| **Why This Source** | The only primary source for Sweden's formal diplomatic positions, bilateral readouts, sanctions implementations, ambassador appointments, and multilateral voting positions. Critical for tracking Sweden's post-accession NATO integration and evolving EU positions. |
| **Access Notes** | Same regeringen.se infrastructure. The Diplomatic Portal (`government.se/government-of-sweden/ministry-for-foreign-affairs/diplomatic-portal/`) provides structured information for diplomatic missions. Sweden Abroad portal (`swedenabroad.se`) hosts embassy-specific communications. |

**Additional entry points:**
- Diplomatic Portal: `https://www.government.se/government-of-sweden/ministry-for-foreign-affairs/diplomatic-portal/`
- Sweden Abroad (embassy network): `https://www.swedenabroad.se/`
- Country strategies: `https://www.government.se/government-policy/foreign-policy/`
- UD travel advisories: `https://www.regeringen.se/uds-reseinformation/` (RSS feed includes full text)

---

### 1.3 Defense / Security — Försvarsdepartementet, Försvarsmakten

#### 1.3a Försvarsdepartementet (Ministry of Defence)

| Field | Detail |
|---|---|
| **Institution** | Försvarsdepartementet (Ministry of Defence) |
| **Domain** | `regeringen.se` / `government.se` |
| **Entry Point URL** | `https://www.regeringen.se/pressmeddelanden/?teleFilter=Försvarsdepartementet` (filtered by Defence Ministry) / `https://www.government.se/government-of-sweden/ministry-of-defence/` |
| **RSS/Atom Feed** | **Yes — dynamically generated.** Filter pressmeddelanden by "Försvarsdepartementet" and use the generated RSS link. |
| **Language** | Swedish (primary); English (key announcements) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | 3-5 per week. Press releases cover defense budget decisions, NATO integration milestones, military cooperation agreements, conscription policy, procurement decisions, and totalförsvar (total defense) initiatives. |
| **Content Format** | HTML on regeringen.se. Defense bills and inquiry reports (SOU/Ds) published as PDF. |
| **Extraction Method** | RSS polling of Försvarsdepartementet-filtered feed. Same platform. |
| **Editorial Orientation** | Official defense policy position. Under Defense Minister Pål Jonson, communications emphasize rapid NATO integration, defense spending increases toward and beyond 2% of GDP, Gotland reinforcement, total defense concept, and Nordic defense cooperation (NORDEFCO). |
| **Why This Source** | Primary source for defense policy decisions, NATO integration progress, bilateral defense agreements (especially with US, Finland, Norway, UK), and defense procurement announcements. Media coverage of defense policy is downstream of these releases. |
| **Access Notes** | Same regeringen.se infrastructure. |

#### 1.3b Försvarsmakten (Swedish Armed Forces)

| Field | Detail |
|---|---|
| **Institution** | Försvarsmakten (Swedish Armed Forces) |
| **Domain** | `forsvarsmakten.se` |
| **Entry Point URL** | `https://www.forsvarsmakten.se/sv/aktuellt/` (Swedish) / `https://www.forsvarsmakten.se/en/news/` (English) |
| **RSS/Atom Feed** | **Yes.** `https://www.forsvarsmakten.se/sv/aktuellt/feed.rss` [VERIFY RSS — URL found in search results but returned 404 on direct fetch; may require browser User-Agent] |
| **Language** | Swedish (primary); English (selected content) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. News items cover exercises, NATO activities, operational updates, recruitment, conscription, organizational changes. Higher frequency during major exercises (Aurora, Nordic Response, Steadfast Defender). |
| **Content Format** | HTML articles. Press images and video via MyNewsdesk. |
| **Extraction Method** | RSS polling (if feed confirmed). HTML scraping of `/sv/aktuellt/` listing page as fallback. Försvarsmakten also uses MyNewsdesk (`mynewsdesk.com/com/forsvarsmakten`) for press distribution. |
| **Editorial Orientation** | Official military communication. Communications are professional and operationally focused. Unlike some defense establishments, Försvarsmakten is relatively open about exercises, deployments, and capability development — but classified operational details (Gotland deployments, signals intelligence, submarine operations) are excluded. |
| **Why This Source** | The direct window into Swedish military operational tempo, NATO exercise participation, and capability development. Försvarsmakten's communications reveal prioritization of threats (Russia, Baltic Sea, hybrid warfare, cyber) and the pace of NATO integration at the operational level. |
| **Access Notes** | Independent infrastructure (not on regeringen.se). MyNewsdesk channel provides additional press materials and media contact information. Press contacts available 24/7 via +46-8-788-88-88 or info@mil.se. |

**Additional entry points:**
- MyNewsdesk press room: `https://www.mynewsdesk.com/com/forsvarsmakten`
- Press contacts: `https://www.forsvarsmakten.se/en/news/press-contacts/`
- MUST annual review (PDF): Published annually at `https://www.forsvarsmakten.se/siteassets/2-om-forsvarsmakten/dokument/musts-arsoversikter/`

---

### 1.4 Parliament — Riksdagen

| Field | Detail |
|---|---|
| **Institution** | Sveriges Riksdag (Swedish Parliament) |
| **Domain** | `riksdagen.se` |
| **Entry Point URL** | `https://www.riksdagen.se/sv/aktuellt/` (news) / `https://www.riksdagen.se/en/news/` (English) |
| **RSS/Atom Feed** | **Yes — multiple structured feeds via the Open Data API.** |
| **Language** | Swedish (primary); English (institutional/procedural content) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods (September-June with breaks). Government bills, committee reports, and plenary decisions published continuously. Reduced during summer recess (late June-early September). |
| **Content Format** | HTML (news articles). Structured data via the Open Data API (`data.riksdagen.se`). Government bills, committee reports, and plenary minutes available as HTML and PDF. |
| **Extraction Method** | RSS feeds from `data.riksdagen.se` (preferred). HTML scraping of news page as supplement. The Open Data API provides machine-readable access to all parliamentary documents. |
| **Editorial Orientation** | Institutional — the Riksdag publishes content from all parties. News articles are neutral summaries of parliamentary proceedings. Individual party positions are visible in motions and interpellation debates. |
| **Why This Source** | Parliamentary proceedings reveal the political constraints on government foreign and defense policy. Committee reports from Utrikesutskottet (Foreign Affairs Committee) and Försvarsutskottet (Defence Committee) contain expert testimony and policy analysis not available elsewhere. Budget votes and interpellations surface dissent on NATO, defense spending, and EU policy. The Riksdag's open data infrastructure is exceptionally well-structured for automated monitoring. |
| **Access Notes** | No paywall. Open Data API at `data.riksdagen.se` provides programmatic access. Well-documented API with multiple output formats (XML, JSON, RSS). |

**Key RSS feed URLs:**

| Feed | URL |
|---|---|
| Decisions (Beslut i korthet) | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=bet&beslutad=1&sort=beslutsdag&sortorder=desc&utformat=rss` |
| Government Proposals (Propositioner) | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=prop&sort=datum&sortorder=desc&utformat=rss` |
| Member Motions (Motioner) | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=mot&sort=datum&sortorder=desc&utformat=rss` |
| Questions & Interpellations | `https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=ip,fr,frs,ku-anm&sort=datum&sortorder=desc&utformat=rss` |
| Custom feeds | Construct via `data.riksdagen.se/dokumentlista/?` with query parameters for document type, committee, date range, and `utformat=rss` |

**Additional entry points:**
- Documents & Laws search: `https://www.riksdagen.se/sv/dokument-och-lagar/`
- Open Data portal: `https://data.riksdagen.se/`
- Email subscription: `https://www.riksdagen.se/sv/folj-och-prenumerera/prenumerera-via-e-post/`

---

### 1.5 Official Gazette — Svensk författningssamling (SFS)

| Field | Detail |
|---|---|
| **Institution** | Svensk författningssamling (Swedish Code of Statutes) |
| **Domain** | `svenskforfattningssamling.se` |
| **Entry Point URL** | `https://svenskforfattningssamling.se/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Swedish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the SFS is the constitutional publication vehicle for all Swedish laws (lagar) and ordinances (förordningar) |
| **Publication Frequency** | Continuous. New statutes are published as they are enacted. Amendments published with each legislative change. |
| **Content Format** | HTML on `svenskforfattningssamling.se` (since April 1, 2018 — the official and authentic digital version). Each statute receives an SFS number (e.g., SFS 2024:123). Consolidated texts include all amendments. |
| **Extraction Method** | HTML scraping of the publication listing. The site provides a statutes register with searchable metadata (SFS number, title, date, responsible ministry). Riksdagen.se also hosts SFS documents in its document database. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of enacted law. Published by the Government Offices (Regeringskansliet). |
| **Why This Source** | Constitutional requirement: no Swedish law or ordinance is legally binding until published in the SFS. This is the only source for definitive, authenticated legal text. Media reports on legislation are always downstream of SFS publication. Critical for tracking defense legislation, NATO-related legal frameworks, sanctions implementations, and foreign investment screening laws. |
| **Access Notes** | No paywall, no authentication. Statutes issued prior to April 1, 2018 are available in the Government Offices' legal databases or at the Riksdag Library. The legal information portal `lagrummet.se` aggregates Swedish legal sources. |

**Additional entry points:**
- Lagrummet (legal information portal): `https://lagrummet.se/`
- Riksdagen SFS database: `https://www.riksdagen.se/sv/dokument-och-lagar/` (filter by "Svensk författningssamling")
- Government Offices legal database: `https://www.regeringen.se/rattsliga-dokument/`

---

### 1.6 Finance Ministry — Finansdepartementet

| Field | Detail |
|---|---|
| **Institution** | Finansdepartementet (Ministry of Finance) |
| **Domain** | `regeringen.se` / `government.se` |
| **Entry Point URL** | `https://www.regeringen.se/pressmeddelanden/?teleFilter=Finansdepartementet` (filtered by Finance Ministry) / `https://www.government.se/government-of-sweden/ministry-of-finance/` |
| **RSS/Atom Feed** | **Yes — dynamically generated.** Filter pressmeddelanden by "Finansdepartementet" and use the generated RSS link. |
| **Language** | Swedish (primary); English (key fiscal announcements, budget summaries) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | 3-5 per week. Press releases cover budget proposals (budgetpropositioner), economic forecasts, tax policy, state-owned enterprise governance, financial market regulation, digital policy, and AI strategy. |
| **Content Format** | HTML on regeringen.se. Budget bills and economic forecasts published as PDF with extensive statistical annexes. |
| **Extraction Method** | RSS polling of Finansdepartementet-filtered feed. Same platform as other ministries. |
| **Editorial Orientation** | Official fiscal policy position. Under Finance Minister Elisabeth Svantesson (Moderate Party), communications emphasize fiscal discipline, economic recovery, competitiveness, digital transformation, and AI strategy. Budget presentations frame defense spending increases alongside fiscal consolidation. |
| **Why This Source** | Primary source for the Budget Bill (budgetproposition, typically September), Spring Fiscal Policy Bill (vårproposition, April), and economic forecasts. Defense spending commitments, development aid allocations, and sanctions-related fiscal measures all originate here. Essential for the Economic & Technological Statecraft domain. |
| **Access Notes** | Same regeringen.se infrastructure. The Riksgälden (National Debt Office) at `riksgalden.se` provides complementary data on government debt and borrowing. |

**Additional entry points:**
- Budget documents: `https://www.regeringen.se/rattsliga-dokument/proposition/?teleFilter=Finansdepartementet`
- Economic forecasts: `https://www.government.se/government-policy/the-budget-and-fiscal-policy/`
- Riksgälden (Debt Office): `https://www.riksgalden.se/en/press-and-publications/press-releases-and-news/`
- Riksgälden RSS: `https://www.riksgalden.se/en/press-and-publications/subscribe/rss-on-riksgalden.se/`

---

### 1.7 Central Bank — Sveriges Riksbank

| Field | Detail |
|---|---|
| **Institution** | Sveriges Riksbank |
| **Domain** | `riksbank.se` |
| **Entry Point URL** | `https://www.riksbank.se/sv/press-och-publicerat/` (Swedish) / `https://www.riksbank.se/en-gb/press-and-published/` (English) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS subscription page: `https://www.riksbank.se/en-gb/press-and-published/subscribe-via-rss/`. Categories include: press releases, notices, calendar events, speeches, and minutes of monetary policy meetings. The Riksbank also distributes press releases via TT (Swedish news agency) portal. |
| **Language** | Swedish (primary); English (parallel versions for all major publications) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: approximately 6 per year (scheduled). Monetary Policy Reports: 3 per year. Financial Stability Reports: 2 per year. Press releases, speeches, and notices: weekly. |
| **Content Format** | HTML for press releases and notices. PDF for Monetary Policy Reports, Financial Stability Reports, and minutes. Structured data available for some economic indicators. |
| **Extraction Method** | RSS feeds (preferred) for press releases, notices, speeches, and minutes. PDF extraction for reports. The Riksbank's RSS infrastructure is well-maintained and reliable. |
| **Editorial Orientation** | Technically independent central bank (the world's oldest, est. 1668). Communications are data-driven and policy-neutral by institutional mandate. Under Governor Erik Thedéen (since January 2023), the Riksbank has navigated rate cuts from peak levels while maintaining credibility on inflation targeting (2% CPI target). New Riksbank Act (effective January 2023) reinforces independence. |
| **Why This Source** | The Riksbank is the sole authority for monetary policy decisions, inflation targeting, financial stability assessments, and official economic indicators. Monetary policy decisions move the krona (SEK) and affect the fiscal space for defense spending. Financial stability reports assess risks to the Swedish banking system (systemically important for the Nordics/Baltics). The Riksbank's assessments of geopolitical risks to financial stability are increasingly relevant. |
| **Access Notes** | No paywall. No bot protection observed. Both Swedish and English versions comprehensive. The Riksbank's e-krona (digital currency) project communications appear under press releases. Email subscription available alongside RSS. |

**Key RSS content categories:**
| Category | Content |
|---|---|
| Press releases | Monetary policy decisions, major announcements |
| Notices | Operational communications, market operations |
| Speeches | Governor and Deputy Governors' public remarks |
| Minutes | Monetary policy meeting minutes (published ~2 weeks after decision) |
| Calendar | Upcoming events, publication schedule |

**Additional entry points:**
- Monetary policy decisions: `https://www.riksbank.se/en-gb/press-and-published/notices-and-press-releases/press-releases/`
- Statistics: `https://www.riksbank.se/en-gb/statistics/`
- Monetary Policy Report: `https://www.riksbank.se/en-gb/monetary-policy/monetary-policy-report/`
- Financial Stability Report: `https://www.riksbank.se/en-gb/financial-stability/financial-stability-report/`

---

### 1.8 Trade / Commerce — Utrikesdepartementet (Handelspolitik) and Agencies

Sweden does not have a standalone trade ministry. Trade policy (handelspolitik) falls under the Ministry for Foreign Affairs (UD), with the Minister for Foreign Trade responsible. Implementation and analysis are handled by the National Board of Trade (Kommerskollegium) and Business Sweden (trade and investment promotion).

#### 1.8a Kommerskollegium (National Board of Trade)

| Field | Detail |
|---|---|
| **Institution** | Kommerskollegium (National Board of Trade Sweden) |
| **Domain** | `kommerskollegium.se` |
| **Entry Point URL** | `https://www.kommerskollegium.se/en/` (English) / `https://www.kommerskollegium.se/` (Swedish) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Swedish and English (bilingual publications) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-4 reports and publications per month. Analysis and policy briefs on trade policy, EU internal market, WTO, tariffs, and trade barriers. |
| **Content Format** | HTML with PDF reports. |
| **Extraction Method** | HTML scraping of publications page. |
| **Editorial Orientation** | Government agency with analytical independence. Founded 1651. Provides policy analysis and recommendations on trade policy to the government. Strongly pro-free-trade institutional orientation. |
| **Why This Source** | Sweden's primary analytical body for trade policy — provides assessments of EU trade agreements, sanctions impact on Swedish trade, tariff analyses, and EU internal market functioning. Reports on trade barriers and protectionism trends are essential for Economic & Technological Statecraft domain. Particularly relevant for tracking US tariff impacts on Swedish exports and EU trade policy positions. |
| **Access Notes** | No paywall. Reports published in both Swedish and English. The agency answers to the Ministry for Foreign Affairs. |

#### 1.8b Business Sweden

| Field | Detail |
|---|---|
| **Institution** | Business Sweden (Swedish Trade & Invest Council) |
| **Domain** | `business-sweden.com` |
| **Entry Point URL** | `https://www.business-sweden.com/about-us/media/press-releases/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Swedish and English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 1-3 per week. Press releases cover trade promotion, FDI, export statistics, and market reports. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping of press releases listing. |
| **Editorial Orientation** | Government-owned trade promotion body (jointly owned by government and Swedish industry). Communications emphasize Swedish export success, investment attractiveness, and trade opportunities. |
| **Why This Source** | Provides ground-level intelligence on Swedish trade flows, FDI trends, and export market conditions. Business Sweden's presence in 40+ markets gives early signals on trade disruptions, sanctions impacts, and nearshoring/friendshoring trends. The "Made with Sweden" initiative (launched December 2025) specifically targets free trade promotion amid rising protectionism. |
| **Access Notes** | No paywall. Team Sweden collaborative platform connects Business Sweden with other government trade actors. |

#### 1.8c ISP (Inspektionen för strategiska produkter)

| Field | Detail |
|---|---|
| **Institution** | Inspektionen för strategiska produkter (Inspectorate of Strategic Products) |
| **Domain** | `isp.se` |
| **Entry Point URL** | `https://isp.se/` (Swedish) / `https://isp.se/eng` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Swedish (primary); English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | Infrequent press releases. Annual report on Swedish military exports published yearly. |
| **Content Format** | HTML, PDF (annual reports and statistics). |
| **Extraction Method** | Periodic check for new publications. Annual export report is the key document. |
| **Editorial Orientation** | Independent regulatory authority. Factual and legalistic. |
| **Why This Source** | ISP controls exports of military equipment and dual-use items, implements international sanctions, and serves as Sweden's foreign direct investment screening authority. The annual military export report reveals the scope and direction of Swedish arms exports (Saab, BAE Hägglunds, etc.) — essential for understanding Sweden's defense-industrial relationships. The FDI screening role is increasingly important given Chinese/Russian investment concerns. |
| **Access Notes** | No paywall. Answers to the Ministry for Foreign Affairs. |

---

### 1.9 Intelligence / National Security — SÄPO, MUST, FRA

#### 1.9a Säkerhetspolisen (SÄPO — Swedish Security Service)

| Field | Detail |
|---|---|
| **Institution** | Säkerhetspolisen (Swedish Security Service) |
| **Domain** | `sakerhetspolisen.se` |
| **Entry Point URL** | `https://www.sakerhetspolisen.se/ovriga-sidor/nyheter.html` (news) / `https://sakerhetspolisen.se/ovriga-sidor/pressrum.html` (press room) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Swedish (primary); English section available at `sakerhetspolisen.se/ovriga-sidor/other-languages/english-engelska.html` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Low — 1-3 publications per month. News items cover threat assessments, counter-espionage operations (when public), terrorism-related actions, and institutional announcements. The annual threat assessment (Årsbok) is the key publication. |
| **Content Format** | HTML (news articles). PDF (annual threat assessment, thematic reports). |
| **Extraction Method** | HTML scraping of nyheter (news) page. Periodic check for new publications. SÄPO also distributes press releases via TT (Swedish news agency) at `via.tt.se/pressrum/3236713/sakerhetspolisen`. |
| **Editorial Orientation** | Security agency communication — controlled and deliberate. SÄPO publishes selectively but, unlike many peer agencies, does issue public threat assessments, counter-espionage warnings, and influence operation alerts. Since Russia's invasion of Ukraine, SÄPO communications have become more direct about Russian intelligence threats to Sweden. |
| **Why This Source** | SÄPO's annual threat assessment is the definitive public document on threats to Swedish security — covering espionage, terrorism, influence operations, and threats to the constitution. Individual news items on espionage arrests, expelled diplomats, and elevated threat levels are high-signal events. SÄPO's assessment of the Russian intelligence threat and hybrid warfare tactics is critical context for defense and diplomatic analysis. |
| **Access Notes** | No paywall. Press office reachable at +46 10 568 79 00 and press@sakerhetspolisen.se. The English-language section provides translated versions of major publications. |

#### 1.9b MUST (Militära underrättelse- och säkerhetstjänsten)

| Field | Detail |
|---|---|
| **Institution** | Militära underrättelse- och säkerhetstjänsten (Military Intelligence and Security Service) |
| **Domain** | `forsvarsmakten.se` (subsection) |
| **Entry Point URL** | `https://www.forsvarsmakten.se/en/about-the-swedish-armed-forces/organisation/joint-forces/military-intelligence-and-security-service-must/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Swedish; English (limited) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Annual — the MUST Årsöversikt (Annual Review) is the only regular public publication. Occasional press releases issued through Försvarsmakten channels. |
| **Content Format** | PDF (annual review, typically 30-50 pages). |
| **Extraction Method** | Annual check for Årsöversikt publication at `forsvarsmakten.se/siteassets/2-om-forsvarsmakten/dokument/musts-arsoversikter/`. Monitor Försvarsmakten news for MUST-related items. |
| **Editorial Orientation** | Military intelligence — highly controlled. The annual review provides MUST's unclassified assessment of global security threats, with focus on Russia, China, the Baltic Sea region, and cyber/hybrid threats. The publication is carefully calibrated to be informative without compromising sources. |
| **Why This Source** | The MUST annual review is one of the most valuable open-source intelligence products from any Nordic country. It provides the Swedish military intelligence community's assessment of Russian military capabilities, Chinese strategic intentions, and threats to Swedish security that directly inform defense policy. Its assessments are frequently cited by Swedish and Nordic media. |
| **Access Notes** | MUST has no independent website. All public communications route through Försvarsmakten. The annual review PDF is posted to the Försvarsmakten document repository. |

#### 1.9c FRA (Försvarets radioanstalt — National Defence Radio Establishment)

| Field | Detail |
|---|---|
| **Institution** | Försvarets radioanstalt (FRA) |
| **Domain** | `fra.se` |
| **Entry Point URL** | `https://www.fra.se/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Swedish (primary); English summary at `fra.se/system/engelska/english.4.55af049f184e92956c42ca2.html` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Minimal — FRA publishes an annual report and occasional press statements. Public-facing communications are rare. |
| **Content Format** | HTML (minimal). PDF (annual report). |
| **Extraction Method** | Periodic check of fra.se for new publications. |
| **Editorial Orientation** | Signals intelligence agency — effectively silent on operational matters. Public communications focus on cybersecurity advisory role and institutional information. Since FRA's expanded mandate for signals intelligence (the "FRA-lagen"), the agency has made modest efforts at public transparency while maintaining operational secrecy. |
| **Why This Source** | Included for completeness. FRA's public communications are minimal, but any new publication should be flagged as a high-priority anomaly. FRA's cybersecurity advisory function generates occasional public alerts on threats to Swedish critical infrastructure. The annual report may contain insights into the cyber threat landscape. The real signals intelligence value of FRA's work surfaces through government policy decisions informed by classified briefings. |
| **Access Notes** | Minimal website. FRA is organized under the Ministry of Defence. |

---

### 1.10 Country-Specific Institutions

#### 1.10a FOI (Totalförsvarets forskningsinstitut — Swedish Defence Research Agency)

| Field | Detail |
|---|---|
| **Institution** | Totalförsvarets forskningsinstitut (FOI — Swedish Defence Research Agency) |
| **Domain** | `foi.se` |
| **Entry Point URL** | `https://www.foi.se/en/foi/news-and-pressroom.html` (English) / `https://www.foi.se/nyheter-och-press.html` (Swedish) |
| **RSS/Atom Feed** | **Yes.** RSS news page: `https://www.foi.se/en/foi/misc/rss-news.html` [VERIFY exact feed URL — the page lists news items but the direct RSS/XML URL may differ] |
| **Language** | Swedish and English (many publications bilingual) |
| **Type** | `security_defense` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | 2-4 publications per week (reports, briefs, news items). Major research reports published monthly. |
| **Content Format** | HTML (news). PDF (research reports, policy briefs — typically 20-80 pages). |
| **Extraction Method** | RSS feed (if functional). HTML scraping of news page. Report publications indexed in the FOI publication database. |
| **Editorial Orientation** | Government research agency with analytical independence. FOI is Europe's leading defense research institute. Publications are evidence-based and peer-reviewed. The agency provides the Swedish government with research and analysis on defense, security, and total defense topics. Reports on Russian military capability, Chinese strategic behavior, and Baltic security are essential reading. |
| **Why This Source** | FOI produces the most analytically rigorous open-source defense research in the Nordic region. Its Russia studies program (led by prominent analysts) produces assessments of Russian military capability, doctrine, and intentions that are cited across European defense establishments. FOI's analysis of hybrid threats, autonomous systems, and defense-industrial trends directly informs Swedish defense policy. Critical complement to Försvarsmakten's operational perspective. |
| **Access Notes** | No paywall. Most reports freely downloadable. FOI is organized under the Ministry of Defence. The agency also operates the CBRN defense center and environmental security research programs. |

#### 1.10b NATO Integration — Sweden's New Membership

| Field | Detail |
|---|---|
| **Institution** | NATO (Sweden's membership effective March 7, 2024) |
| **Domain** | `nato.int` |
| **Entry Point URL** | `https://www.nato.int/cps/en/natohq/news.htm` / Sweden-specific: `https://www.nato.int/cps/en/natohq/topics_52535.htm` |
| **RSS/Atom Feed** | **Yes.** `https://www.nato.int/cps/en/natohq/news.htm?type=newsAtom` [VERIFY RSS] |
| **Language** | English (primary); French |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy |
| **Publication Frequency** | Daily. Press releases, communiqués, Secretary General statements, exercise announcements, and summit declarations. |
| **Content Format** | HTML. PDF for formal communiqués and summit declarations. |
| **Extraction Method** | RSS feed. Filter for Sweden-related content via keyword matching (Sweden, Swedish, Nordic, Baltic). |
| **Editorial Orientation** | Alliance institutional communication. Sweden's integration narrative within NATO communications emphasizes Nordic-Baltic coherence, interoperability, and the strategic value of Sweden's geography and defense capabilities. |
| **Why This Source** | Sweden acceded to NATO on March 7, 2024, making NATO communications a new primary source for understanding Sweden's alliance obligations, exercise commitments, and collective defense posture. NATO communiqués and exercise announcements directly constrain and shape Swedish defense policy. Sweden's first NATO defense planning cycle and force commitments will be reflected in NATO-level communications. |
| **Access Notes** | No paywall. NATO also operates a dedicated newsroom and multimedia platform. |

#### 1.10c EU Institutions — Sweden's EU Engagement

| Field | Detail |
|---|---|
| **Institution** | Council of the EU / European Commission (Sweden-relevant) |
| **Domain** | `consilium.europa.eu` / `ec.europa.eu` |
| **Entry Point URL** | `https://www.consilium.europa.eu/en/press/press-releases/` |
| **RSS/Atom Feed** | **Yes.** Council RSS: `https://www.consilium.europa.eu/en/rss/` [VERIFY RSS] |
| **Language** | English (primary working language); all EU languages |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily. Council conclusions, European Council summit outcomes, sanctions decisions, foreign affairs council outcomes. |
| **Content Format** | HTML, PDF (formal conclusions and decisions). |
| **Extraction Method** | RSS feed with keyword filtering for Sweden-relevant content. |
| **Editorial Orientation** | EU institutional communication. Sweden's positions are embedded within consensus-based Council outcomes. |
| **Why This Source** | EU Council conclusions on sanctions (Russia, Belarus), Common Security and Defence Policy (CSDP), trade agreements, and energy policy directly bind Sweden. European Council summit conclusions set strategic direction. The Foreign Affairs Council (FAC) outcomes reveal Sweden's alignment with EU consensus or dissent positions. |
| **Access Notes** | No paywall. The European Council/Council of the EU maintains extensive press archives. |

#### 1.10d Nordic Cooperation — Nordiska ministerrådet / NORDEFCO

| Field | Detail |
|---|---|
| **Institution** | Nordiska ministerrådet (Nordic Council of Ministers) / NORDEFCO (Nordic Defence Cooperation) |
| **Domain** | `norden.org` / `nordefco.org` |
| **Entry Point URL** | `https://www.norden.org/en/news` / `https://www.nordefco.org/` |
| **RSS/Atom Feed** | None identified for NORDEFCO. Norden.org may have RSS. [VERIFY RSS] |
| **Language** | Scandinavian languages (Swedish, Danish, Norwegian) and English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Institutional engagement |
| **Publication Frequency** | Norden.org: several per week. NORDEFCO: infrequent (communiqués from ministerial meetings, typically 1-2 per year). |
| **Content Format** | HTML. PDF for formal declarations and vision documents. |
| **Extraction Method** | HTML scraping. NORDEFCO content is sparse — monitor for ministerial meeting communiqués. |
| **Editorial Orientation** | Nordic institutional communication. Emphasis on joint Nordic positions and cooperation frameworks. With all five Nordic countries now in NATO, the cooperation agenda has deepened significantly on defense matters. |
| **Why This Source** | Nordic cooperation is foundational to Swedish foreign and defense policy. The Nordic-Baltic Eight (NB8) format, NORDEFCO defense cooperation (now all within NATO), and Nordic Council political declarations shape Sweden's regional posture. Joint Nordic positions on Russia, Arctic policy, and EU engagement carry weight beyond individual national positions. |
| **Access Notes** | No paywall. NORDEFCO's web presence is modest. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Regeringen.se Platform |
|---|---|---|---|---|---|---|---|
| 1 | Regeringskansliet (PM's Office) | `regeringen.se/pressmeddelanden/` | **Yes** (dynamic) | P1 | HTML | Daily | Yes |
| 2 | Utrikesdepartementet (UD) | `regeringen.se/pressmeddelanden/?teleFilter=Utrikesdepartementet` | **Yes** (dynamic) | P1 | HTML/PDF | Daily | Yes |
| 3a | Försvarsdepartementet | `regeringen.se/pressmeddelanden/?teleFilter=Försvarsdepartementet` | **Yes** (dynamic) | P1 | HTML/PDF | 3-5/week | Yes |
| 3b | Försvarsmakten | `forsvarsmakten.se/sv/aktuellt/` | **Yes** [VERIFY] | P1 | HTML | 3-7/week | No |
| 4 | Riksdagen | `riksdagen.se/sv/aktuellt/` | **Yes** (multiple) | P2 | HTML/Data | Daily (session) | No |
| 5 | SFS (Official Gazette) | `svenskforfattningssamling.se/` | [VERIFY] | P2 | HTML | Continuous | No |
| 6 | Finansdepartementet | `regeringen.se/pressmeddelanden/?teleFilter=Finansdepartementet` | **Yes** (dynamic) | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | Riksbanken | `riksbank.se/sv/press-och-publicerat/` | **Yes** (multiple) | P2 | HTML/PDF | Variable | No |
| 8a | Kommerskollegium | `kommerskollegium.se/en/` | [VERIFY] | P2 | HTML/PDF | 2-4/month | No |
| 8b | Business Sweden | `business-sweden.com/about-us/media/press-releases/` | [VERIFY] | P2 | HTML | 1-3/week | No |
| 8c | ISP | `isp.se/` | [VERIFY] | P2 | HTML/PDF | Infrequent | No |
| 9a | SÄPO | `sakerhetspolisen.se/ovriga-sidor/nyheter.html` | No | P2 | HTML/PDF | 1-3/month | No |
| 9b | MUST | `forsvarsmakten.se` (subsection) | No | P2 | PDF | Annual | No |
| 9c | FRA | `fra.se` | No | P2 | HTML/PDF | Minimal | No |
| 10a | FOI | `foi.se/en/foi/news-and-pressroom.html` | **Yes** [VERIFY] | P2 | HTML/PDF | 2-4/week | No |
| 10b | NATO (Sweden) | `nato.int/cps/en/natohq/news.htm` | **Yes** | P2 | HTML/PDF | Daily | No |
| 10c | EU Council | `consilium.europa.eu/en/press/press-releases/` | **Yes** | P2 | HTML/PDF | Daily | No |
| 10d | Nordic Cooperation | `norden.org/en/news` / `nordefco.org` | [VERIFY] | P2 | HTML | Variable | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Sweden Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/se.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: se_regeringskansliet
    name: Regeringskansliet (Government Offices / PM)
    domain: regeringen.se
    entry_url: "https://www.regeringen.se/pressmeddelanden/"
    entry_url_en: "https://www.government.se/press-releases/"
    rss_feed: "https://www.government.se/Filter/RssFeed?filterType=Taxonomy&filterByType=FilterablePageBase&preFilteredCategories=2069,2070,2071,2072,2073,2074,2075,2076,2077,2078,2079,2082,2083,2124,2125,2126,2127,2128,2129,2130,2131,2132,2133,2134,2135,2137,2138,2139,2140,2141,2142,2143,2144,2145,2146,2147,2189&rootPageReference=0"
    language: sv
    language_secondary: en
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
    notes: "Dynamic RSS from government.se covers all ministries. Filter by Statsrådsberedningen for PM-specific. English site parallels major releases. No bot protection observed."

  - id: se_utrikesdepartementet
    name: Utrikesdepartementet (Ministry for Foreign Affairs)
    domain: regeringen.se
    entry_url: "https://www.regeringen.se/pressmeddelanden/?teleFilter=Utrikesdepartementet"
    entry_url_en: "https://www.government.se/government-of-sweden/ministry-for-foreign-affairs/"
    rss_feed: null  # Dynamic — generate by filtering pressmeddelanden by UD, then extract RSS URL
    language: sv
    language_secondary: en
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
    notes: "UD travel advisory RSS uniquely includes full body text. Embassy-level releases at swedenabroad.se."

  - id: se_forsvarsdepartementet
    name: Försvarsdepartementet (Ministry of Defence)
    domain: regeringen.se
    entry_url: "https://www.regeringen.se/pressmeddelanden/?teleFilter=Försvarsdepartementet"
    rss_feed: null  # Dynamic — generate by filtering pressmeddelanden by Försvarsdepartementet
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "NATO integration, defense budget, total defense. Same regeringen.se platform."

  - id: se_forsvarsmakten
    name: Försvarsmakten (Swedish Armed Forces)
    domain: forsvarsmakten.se
    entry_url: "https://www.forsvarsmakten.se/sv/aktuellt/"
    entry_url_en: "https://www.forsvarsmakten.se/en/news/"
    rss_feed: "https://www.forsvarsmakten.se/sv/aktuellt/feed.rss"  # [VERIFY - may require browser UA]
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 4
    notes: "MyNewsdesk press room at mynewsdesk.com/com/forsvarsmakten. 24/7 press contact: +46-8-788-88-88."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: se_riksdagen
    name: Sveriges Riksdag (Parliament)
    domain: riksdagen.se
    entry_url: "https://www.riksdagen.se/sv/aktuellt/"
    rss_feed:
      decisions: "https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=bet&beslutad=1&sort=beslutsdag&sortorder=desc&utformat=rss"
      government_proposals: "https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=prop&sort=datum&sortorder=desc&utformat=rss"
      motions: "https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=mot&sort=datum&sortorder=desc&utformat=rss"
      questions_interpellations: "https://data.riksdagen.se/dokumentlista/?avd=dokument&doktyp=ip,fr,frs,ku-anm&sort=datum&sortorder=desc&utformat=rss"
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html_data
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Exceptionally well-structured Open Data API at data.riksdagen.se. Custom RSS feeds constructable via query parameters. Utrikesutskottet and Försvarsutskottet reports are high-priority."

  - id: se_sfs
    name: Svensk författningssamling (SFS — Official Gazette)
    domain: svenskforfattningssamling.se
    entry_url: "https://svenskforfattningssamling.se/"
    rss_feed: null  # [VERIFY]
    language: sv
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: continuous
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Official and authentic digital version since April 2018. Lagrummet.se provides aggregated legal search. Also indexed via riksdagen.se document database."

  - id: se_finansdepartementet
    name: Finansdepartementet (Ministry of Finance)
    domain: regeringen.se
    entry_url: "https://www.regeringen.se/pressmeddelanden/?teleFilter=Finansdepartementet"
    rss_feed: null  # Dynamic — generate by filtering
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Budget Bill (Sep), Spring Fiscal Policy Bill (Apr). Riksgälden at riksgalden.se provides government debt data with RSS."

  - id: se_riksbanken
    name: Sveriges Riksbank (Central Bank)
    domain: riksbank.se
    entry_url: "https://www.riksbank.se/en-gb/press-and-published/notices-and-press-releases/press-releases/"
    rss_feed: "https://www.riksbank.se/en-gb/press-and-published/subscribe-via-rss/"  # Hub page; individual feed URLs available per category
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "RSS feeds for press releases, notices, speeches, minutes, calendar. ~6 rate decisions/year. English versions comprehensive. Also distributes via TT."

  - id: se_kommerskollegium
    name: Kommerskollegium (National Board of Trade)
    domain: kommerskollegium.se
    entry_url: "https://www.kommerskollegium.se/en/"
    rss_feed: null  # [VERIFY]
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-4_per_month"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "Trade policy analysis. EU internal market. Answers to MFA."

  - id: se_business_sweden
    name: Business Sweden
    domain: business-sweden.com
    entry_url: "https://www.business-sweden.com/about-us/media/press-releases/"
    rss_feed: null  # [VERIFY]
    language: en
    language_secondary: sv
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "Trade promotion body. 40+ market presence. Made with Sweden initiative (Dec 2025)."

  - id: se_isp
    name: ISP (Inspectorate of Strategic Products)
    domain: isp.se
    entry_url: "https://isp.se/"
    rss_feed: null  # [VERIFY]
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: infrequent
    content_format: html_pdf_mixed
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Arms export control, dual-use, FDI screening, sanctions. Annual military export report is key document."

  - id: se_sapo
    name: Säkerhetspolisen (SÄPO — Security Service)
    domain: sakerhetspolisen.se
    entry_url: "https://www.sakerhetspolisen.se/ovriga-sidor/nyheter.html"
    rss_feed: null
    language: sv
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "1-3_per_month"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Annual threat assessment (Årsbok) is key. Counter-espionage, terrorism, influence ops. Press via TT: via.tt.se/pressrum/3236713/sakerhetspolisen"

  - id: se_must
    name: MUST (Military Intelligence and Security Service)
    domain: forsvarsmakten.se
    entry_url: "https://www.forsvarsmakten.se/en/about-the-swedish-armed-forces/organisation/joint-forces/military-intelligence-and-security-service-must/"
    rss_feed: null
    language: sv
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: annual
    content_format: pdf
    extraction_method: periodic_check
    poll_interval_hours: 720  # monthly
    notes: "Annual review (Årsöversikt) is sole regular publication. PDF at forsvarsmakten.se/siteassets/. High analytical value."

  - id: se_fra
    name: FRA (National Defence Radio Establishment)
    domain: fra.se
    entry_url: "https://www.fra.se/"
    rss_feed: null
    language: sv
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: minimal
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 720  # monthly
    notes: "SIGINT agency. Effectively silent. Any new publication is a high-priority anomaly. Cybersecurity advisories possible."

  - id: se_foi
    name: FOI (Swedish Defence Research Agency)
    domain: foi.se
    entry_url: "https://www.foi.se/en/foi/news-and-pressroom.html"
    rss_feed: "https://www.foi.se/en/foi/misc/rss-news.html"  # [VERIFY exact XML URL]
    language: sv
    language_secondary: en
    type: security_defense
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "2-4_per_week"
    content_format: html_pdf_mixed
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 12
    notes: "Europe's leading defense research institute. Russia studies, Baltic security, hybrid threats, autonomous systems. Free publications."

  - id: se_nato
    name: NATO (Sweden-relevant)
    domain: nato.int
    entry_url: "https://www.nato.int/cps/en/natohq/news.htm"
    rss_feed: "https://www.nato.int/cps/en/natohq/news.htm?type=newsAtom"  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_with_keyword_filter
    poll_interval_hours: 6
    filter_keywords:
      - Sweden
      - Swedish
      - Nordic
      - Baltic
      - NORDEFCO
    notes: "Sweden acceded March 7, 2024. Filter for Sweden-relevant content. Summit communiqués, exercise announcements, defense planning."

  - id: se_eu_council
    name: Council of the EU (Sweden-relevant)
    domain: consilium.europa.eu
    entry_url: "https://www.consilium.europa.eu/en/press/press-releases/"
    rss_feed: null  # [VERIFY at consilium.europa.eu/en/rss/]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_with_keyword_filter
    poll_interval_hours: 12
    filter_keywords:
      - Sweden
      - Swedish
      - Nordic
    notes: "Council conclusions, sanctions decisions, FAC outcomes. Keyword filter for Sweden-relevant content."

  - id: se_nordic_cooperation
    name: Nordic Council of Ministers / NORDEFCO
    domain: norden.org
    entry_url: "https://www.norden.org/en/news"
    entry_url_nordefco: "https://www.nordefco.org/"
    rss_feed: null  # [VERIFY at norden.org]
    language: en
    language_secondary: sv
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - institutional_engagement
    publication_frequency: variable
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "All five Nordic countries now in NATO. NORDEFCO ministerial meetings 1-2/year. Joint Nordic positions on Russia, Arctic, EU."

# Extraction pattern for regeringen.se ministries
regeringen_se_shared_config:
  base_url_pattern: "https://www.regeringen.se/pressmeddelanden/?teleFilter={ministry_name}"
  ministries_on_platform:
    - Statsrådsberedningen  # PM's Office
    - Utrikesdepartementet  # Foreign Affairs
    - Försvarsdepartementet  # Defence
    - Finansdepartementet  # Finance
    - Justitiedepartementet  # Justice
    - Klimat- och näringslivsdepartementet  # Climate & Enterprise
    - Kulturdepartementet  # Culture
    - Landsbygds- och infrastrukturdepartementet  # Rural & Infrastructure
    - Socialdepartementet  # Social Affairs
    - Utbildningsdepartementet  # Education
  english_parallel: "https://www.government.se/press-releases/"
  rss_generation: dynamic  # Filter page, then extract RSS URL from page
  press_release_url_pattern: "/pressmeddelanden/{YYYY}/{MM}/{title-slug}/"
  bot_protection: none_observed
  rate_limit: "conservative — max 1 request per 2 seconds"
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "sv-SE,sv;q=0.9,en;q=0.8"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Swedish government communications are more substantive and less propagandistic than many peer countries, reflecting a strong tradition of public transparency (the principle of offentlighetsprincipen — public access to official documents dates to 1766). Nevertheless, framing choices are deliberate, and the pipeline must treat government statements as indicators of official posture rather than objective truth.

- **Regeringskansliet/Statsrådsberedningen**: Cross-reference PM statements against same-day reporting in SVT (public broadcaster, most trusted source per the Source Intelligence Map) and DN (Dagens Nyheter, liberal prestige daily). Divergence between government framing and SVT's editorial line signals genuine political controversy. SvD (Svenska Dagbladet) provides a sympathetic-but-independent conservative perspective that may reveal coalition internal tensions the government press release omits.

- **Utrikesdepartementet (UD)**: Diplomatic communications should be triangulated with SR Ekot (radio news service, breaks diplomatic stories) and DN's foreign affairs desk. For NATO and EU policy, cross-reference with FOI research publications (Layer 2) and Kvartal (expert commentary). When UD and Aftonbladet (Social Democratic editorial alignment) diverge on foreign policy, it signals opposition strategy formation.

- **Försvarsdepartementet / Försvarsmakten**: Defense policy communications present achievements and commitments but not operational challenges, procurement delays, or capability gaps. Cross-reference with DI (Dagens Industri, defense-industrial coverage per the Source Intelligence Map), FOI (analytical depth), and Expressen (investigative defense reporting). Aftonbladet's defense coverage reveals Social Democratic/trade union positions on defense spending and NATO obligations.

- **Riksdagen**: Parliamentary records are the most complete but least accessible source. Committee reports from Utrikesutskottet (Foreign Affairs) and Försvarsutskottet (Defence) contain expert testimony and minority opinions not covered in media. Cross-reference with Altinget Sverige (specialized parliamentary journalism per the Source Intelligence Map) for interpreted context.

- **Riksbanken**: Monetary policy communications are technically rigorous and less subject to political framing, but emphasis choices in communications signal institutional priorities. Cross-reference with DI (market interpretation) and SvD (conservative fiscal commentary). The Riksbank's Financial Stability Report assessments of geopolitical risk are increasingly valuable and should be triangulated with FOI and MUST assessments.

- **SÄPO / MUST / FRA**: Security and intelligence publications are infrequent but high-signal. When SÄPO issues a public threat assessment or counter-espionage warning, it is news. Cross-reference with SVT (investigative unit), DN (national security desk), and SR (Ekot). The MUST annual review should be compared with FOI research publications and NATO intelligence assessments for consistency.

- **FOI**: Research publications are analytically independent and generally trustworthy, but FOI is a government agency and its research agenda reflects government priorities. Cross-reference with UI (Swedish Institute of International Affairs, per the Source Intelligence Map) for alternative analytical frameworks, particularly on multilateral engagement and non-aligned traditions.

**4.2 The regeringen.se centralization effect**

Five of Sweden's government source categories publish through the centralized regeringen.se/government.se platform. This creates operational efficiency (single extraction pattern, dynamic RSS) but means:
- Platform-wide changes to the CMS affect all ministry feeds simultaneously
- The Regeringskansliet's communications staff can control publication timing across all ministries
- Swedish-only content is more comprehensive than English; some politically sensitive releases appear only in Swedish
- The dynamic RSS generation means RSS URLs may change if the platform's taxonomy IDs are updated

Sources outside regeringen.se (Riksdagen, Riksbanken, Försvarsmakten, SÄPO, MUST, FRA, FOI, SFS) operate on fully independent infrastructure and are not subject to these constraints.

**4.3 The intelligence triad: SÄPO + MUST + FRA**

Sweden's three intelligence/security agencies operate under different communication paradigms:
- **SÄPO** (civilian security service): Most communicative of the three. Annual threat assessment, periodic counter-espionage alerts, and occasional news items on terrorism and influence operations. Press office is responsive.
- **MUST** (military intelligence): Publishes one annual review. Otherwise silent. The annual review is analytically valuable — comparable to DNI's Annual Threat Assessment in the US, though shorter and more focused.
- **FRA** (signals intelligence): Effectively silent. Annual report is minimal. Cybersecurity advisories are the only operational publications.

The pipeline should treat any SÄPO or MUST publication as a high-priority event. FRA publications should be flagged as anomalies. The real intelligence signal from these agencies surfaces through:
- Government policy decisions informed by classified briefings (visible in Försvarsdepartementet communications)
- Leaks to investigative media (SVT's Uppdrag Granskning, DN's investigative unit)
- FOI research that draws on declassified or semi-public intelligence assessments
- SÄPO's TT press distribution channel (via.tt.se)

**4.4 Sweden's NATO transition: new information dynamics**

Sweden's NATO accession (March 7, 2024) has created new information dynamics that this supplement captures:
- **NATO-level communications** now contain binding commitments and exercise obligations that constrain Swedish defense policy — these did not exist before accession
- **Försvarsmakten's publication frequency** has increased as NATO exercises and interoperability activities generate more reportable events
- **Försvarsdepartementet** now publishes NATO-related content (host nation agreements, infrastructure investments, force planning) that has no precedent in Swedish government communications
- **The Tidö Agreement** (the informal governing arrangement with Sweden Democrats) creates a domestic political constraint on NATO policy that is poorly visible in government communications but surfaces in Riksdag interpellations and Aftonbladet/SVT opposition coverage

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for regeringen.se

The regeringen.se platform hosts press releases from all government ministries. A single extraction module with ministry-filter parameterization can service all five monitored ministries:

- **URL pattern**: `https://www.regeringen.se/pressmeddelanden/?teleFilter={ministry_name}`
- **Ministry filters**: `Statsrådsberedningen`, `Utrikesdepartementet`, `Försvarsdepartementet`, `Finansdepartementet`, `Justitiedepartementet`
- **Press release URL pattern**: `/pressmeddelanden/{YYYY}/{MM}/{title-slug}/`
- **RSS generation**: Dynamic — filter the pressmeddelanden page by ministry, then extract the RSS subscription URL from the page. The English-language site (government.se) provides a pre-built RSS URL with taxonomy category IDs.
- **Rate limit**: No bot protection observed, but enforce minimum 2-second intervals between requests as good practice.
- **Character encoding**: UTF-8 throughout. Swedish characters (å, ä, ö, Å, Ä, Ö) must be preserved.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Sweden has significantly better RSS infrastructure than many countries. Five government source categories provide functional RSS feeds:

1. **Regeringen.se / Government.se**: Dynamically generated RSS from any filtered view. The English-language feed provides a pre-built URL with all ministry categories. Ministry-specific feeds can be constructed by filtering.

2. **Riksdagen (Open Data API)**: Four pre-built RSS feeds (decisions, proposals, motions, questions/interpellations) plus the ability to construct custom feeds via `data.riksdagen.se` query parameters. This is the most machine-friendly government data source in Sweden.

3. **Riksbanken**: RSS feeds organized by content category (press releases, notices, speeches, minutes, calendar). Subscription management page at `riksbank.se/en-gb/press-and-published/subscribe-via-rss/`.

4. **Försvarsmakten**: RSS feed at `forsvarsmakten.se/sv/aktuellt/feed.rss` [VERIFY — may require browser-like User-Agent header].

5. **FOI**: RSS news page at `foi.se/en/foi/misc/rss-news.html` [VERIFY exact XML feed URL].

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Several sources publish substantially in PDF:
- **SFS (Official Gazette)**: Legal texts published as authenticated HTML (post-2018) — less PDF-dependent than many gazettes.
- **Riksbanken**: Monetary Policy Reports, Financial Stability Reports, and meeting minutes are multi-page PDF. Well-structured, text-based.
- **FOI**: Research reports are PDF (20-80 pages). Text-based, with charts and tables.
- **MUST**: Annual review is PDF (30-50 pages). Text-based.
- **SÄPO**: Annual threat assessment is PDF. May include infographics.
- **Finansdepartementet**: Budget bills and economic forecasts include PDF statistical annexes with tables requiring structured extraction.

### 5.4 Language and Encoding

All government sources publish primarily in Swedish. The following sources provide comprehensive English parallel versions:
- **Government.se** (English mirror of regeringen.se): Most major announcements, though coverage is not 100%
- **Riksbanken**: Full English versions of all major publications and press releases
- **FOI**: Many research reports published bilingually
- **Riksdagen**: Institutional/procedural content in English; parliamentary documents in Swedish only
- **Försvarsmakten**: Selected news items in English

All content is UTF-8 encoded. Swedish-specific characters (å, ä, ö and their uppercase forms) must be preserved in extraction and indexing. Query vocabulary (see Localized Query Vocabulary in the Source Intelligence Map) uses these characters extensively.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A defense policy announcement appears in Försvarsdepartementet press releases, Försvarsmakten news, and potentially Riksdagen documents
- Foreign policy statements appear in UD press releases, government.se English versions, and Riksdagen interpellation records
- Budget decisions appear in Finansdepartementet releases, Riksdagen voting records, and SFS publications (legal text)
- NATO-related content appears in Försvarsdepartementet releases, Försvarsmakten news, and NATO.int communications

Implement content-hash deduplication. Use the following canonical source hierarchy:
1. **Riksdagen** for enacted legislation and formal votes
2. **SFS** for authenticated legal text
3. **Originating ministry** (UD for diplomatic, Försvarsdepartementet for defense) for policy announcements
4. **Försvarsmakten** for operational military content
5. **Riksbanken** for monetary policy

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | UD, Försvarsdepartementet, Statsrådsberedningen | Every 2 hours | Daily publication, policy-critical for NATO/defense/diplomacy |
| P1-Standard | Försvarsmakten | Every 4 hours | Frequent but operational rather than policy-setting |
| P2-Active | Riksdagen, Riksbanken, Finansdepartementet, FOI | Every 6 hours | Regular publishing, structured data feeds |
| P2-Standard | SÄPO, Kommerskollegium, Business Sweden, NATO, EU Council | Every 12 hours | Important but lower frequency |
| P2-Low | SFS, Nordic Cooperation, ISP | Every 24 hours | Important but slow publication cycle |
| P2-Minimal | MUST, FRA | Monthly | Annual publications only; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| regeringen.se platform outage | Statsrådsberedningen, UD, Försvarsdepartementet, Finansdepartementet | Monitor government.se (English parallel site, separate infrastructure path). Follow @LenaHallengren (govt press secretary) and @SweMFA on X. SVT and DN typically republish government press releases within minutes. |
| Riksdagen data API downtime | Riksdagen RSS feeds | HTML scraping of `riksdagen.se/sv/aktuellt/`. Email subscription as backup. |
| Försvarsmakten site issues | Försvarsmakten news | MyNewsdesk channel (`mynewsdesk.com/com/forsvarsmakten`). Follow @Forsvarsmakten on X. |
| Riksbanken site issues | Riksbanken RSS feeds | TT (Swedish news agency) distribution. DI and SvD republish monetary policy decisions immediately. |
| SÄPO site outage | SÄPO news | TT press distribution at `via.tt.se/pressrum/3236713/sakerhetspolisen`. SVT breaks SÄPO news independently. |
| FOI site issues | FOI publications | Policy Commons archive (`policycommons.net/orgs/swedish-defence-research-agency-se/`). FOI publications also indexed by Google Scholar. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of the regeringen.se platform, change in government (next scheduled election: September 2026), change in NATO force planning cycle, or significant reorganization of Swedish defense/intelligence agencies.*
