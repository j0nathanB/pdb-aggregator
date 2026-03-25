# Official Government Sources Supplement: POLAND

**Primary language of political discourse: Polish**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Poland (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Poland. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds and APIs, and provides the YAML manifest for pipeline integration.

Poland's government web infrastructure is partially centralized through the `gov.pl` portal — a unified platform operated by the Chancellery of the Prime Minister (KPRM) and the Ministry of Digital Affairs. Most ministries (MON, MSZ, MF, MRiT) publish press releases and news through `gov.pl/web/{agency-slug}` rather than maintaining fully independent press rooms. However, unlike Mexico's near-total centralization on gob.mx, several critical Polish institutions maintain independent web infrastructure: the President's office (`prezydent.pl`), the Parliament (`sejm.gov.pl`, `senat.gov.pl`), the central bank (`nbp.pl`), the security agencies (`abw.gov.pl`, `aw.gov.pl`), and the National Security Bureau (`bbn.gov.pl`). This creates a mixed extraction environment requiring both gov.pl-pattern scrapers and institution-specific modules. A notable strength is the Sejm's open API (`api.sejm.gov.pl`), which provides structured access to legislation, voting records, and parliamentary proceedings — one of the most machine-friendly parliamentary data sources in Europe.

---

## 1. OFFICIAL GOVERNMENT SOURCES: POLAND

### 1.1 Head of Government — President of the Republic + Prime Minister / KPRM

Poland has a semi-presidential system in which executive authority is divided between the President (head of state, with significant powers over defense, foreign policy, and legislation via veto) and the Prime Minister (head of government, leading the Council of Ministers). Both offices produce strategically significant communications.

#### 1.1a Kancelaria Prezydenta RP (Presidential Chancellery)

| Field | Detail |
|---|---|
| **Institution** | Kancelaria Prezydenta Rzeczypospolitej Polskiej (KPRP) |
| **Domain** | `prezydent.pl` (Polish) / `president.pl` (English) |
| **Entry Point URL** | `https://www.prezydent.pl/aktualnosci` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — check `prezydent.pl/rss` or `/feed`] |
| **Language** | Polish (primary); English at `president.pl/news` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Presidential communications include official statements, records of meetings with foreign leaders, bill signings and vetoes, National Security Council communiqués, and appointments. |
| **Content Format** | HTML articles with embedded images. Some formal documents (e.g., bills returned to Sejm with justification) attached as PDF. Photo galleries and video recordings of speeches published separately. |
| **Extraction Method** | HTML scraping of `prezydent.pl/aktualnosci` listing page. English mirror at `president.pl/news` covers major items with delay. Pagination via URL path parameters. |
| **Editorial Orientation** | Official presidential position. Under President Karol Nawrocki (inaugurated August 2025), communications reflect a national-conservative orientation with emphasis on sovereignty, defense investment, and historical memory policy. Expect institutional tension with PM Tusk's government on judicial reform and EU integration pace. |
| **Why This Source** | The President holds constitutionally significant powers: supreme command of the armed forces, appointment of the Chief of the General Staff, ratification of international agreements, and a legislative veto requiring 3/5 Sejm majority to override. Presidential statements on defense posture, NATO commitments, and bilateral relations (especially US, Ukraine, Germany) are primary signals. The cohabitation dynamic between Nawrocki (PiS-aligned) and Tusk (KO) makes presidential communications an active indicator of domestic constraint on foreign policy. |
| **Access Notes** | No paywall. The `prezydent.pl` domain is independent of the gov.pl platform and runs on its own infrastructure. The site is well-maintained and does not appear to use aggressive bot protection. The English-language `president.pl` site covers major items but with reduced volume and some delay. |

**Additional entry points:**
- For the media: `https://www.prezydent.pl/en/for-the-media/` — press office contact, accreditation
- National Security Council communiqués: published under aktualnosci but tagged with BBN/RBN context
- Presidential bills: submitted to Sejm and tracked via `api.sejm.gov.pl`

---

#### 1.1b Kancelaria Prezesa Rady Ministrów / KPRM (Chancellery of the Prime Minister)

| Field | Detail |
|---|---|
| **Institution** | Kancelaria Prezesa Rady Ministrów (KPRM) — Chancellery of the Prime Minister |
| **Domain** | `gov.pl/web/premier` |
| **Entry Point URL** | `https://www.gov.pl/web/premier/aktualnosci` |
| **RSS/Atom Feed** | None available. The gov.pl platform does not expose RSS feeds for individual ministry/agency pages. |
| **Language** | Polish (primary); English at `gov.pl/web/primeminister` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Daily. Multiple communications per day during Council of Ministers sessions (typically Tuesdays). Subsections: Wydarzenia (events), Decyzje rządu (government decisions), Komunikaty CIR (Government Information Centre communications), Zapowiedzi (announcements). |
| **Content Format** | HTML on gov.pl. Government decisions and CIR communications are text-based. Some attached PDFs for formal Council of Ministers decisions. |
| **Extraction Method** | HTML scraping of gov.pl listing pages. Key subsections to monitor: `gov.pl/web/premier/wydarzenia`, `gov.pl/web/premier/decyzje-rzadu`, `gov.pl/web/premier/komunikaty-cir`. Same gov.pl template across all sections. |
| **Editorial Orientation** | Official government position. Under PM Donald Tusk, communications emphasize EU integration, transatlantic solidarity, defense modernization, and rule-of-law restoration. The Government Information Centre (CIR) functions as the central messaging operation. |
| **Why This Source** | The PM's office produces the authoritative record of Council of Ministers decisions, which cover defense procurement approvals, EU negotiating positions, budget allocations, and legislative initiatives. CIR communications provide the government's rapid-response framing of breaking events. The PM's schedule of bilateral meetings (especially with German, French, Ukrainian, and US counterparts) is a leading indicator of diplomatic alignment shifts. |
| **Access Notes** | Gov.pl platform — shared infrastructure with all ministries. No paywall. Bot protection is minimal but rate limiting may apply. English-language mirror at `gov.pl/web/primeminister` covers major items. Social media accounts @PremierRP (X) and @KPRM_CIR (X) often publish ahead of the website. |

**Additional entry points:**
- Government decisions: `https://www.gov.pl/web/premier/decyzje-rzadu`
- CIR communications: `https://www.gov.pl/web/premier/komunikaty-cir`
- Upcoming events: `https://www.gov.pl/web/premier/zapowiedzi`
- English news: `https://www.gov.pl/web/primeminister`

---

### 1.2 Foreign Ministry — Ministerstwo Spraw Zagranicznych (MSZ)

| Field | Detail |
|---|---|
| **Institution** | Ministerstwo Spraw Zagranicznych (MSZ) — Ministry of Foreign Affairs |
| **Domain** | `gov.pl/web/dyplomacja` (Polish) / `gov.pl/web/diplomacy` (English) |
| **Entry Point URL** | `https://www.gov.pl/web/dyplomacja/aktualnosci` |
| **RSS/Atom Feed** | None available on gov.pl. Legacy MSZ site (`msz.gov.pl`) previously offered RSS but has been migrated. |
| **Language** | Polish (primary); English at `gov.pl/web/diplomacy/news-` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment (primary), Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Komunikaty (press releases) issued for diplomatic meetings, treaty actions, consular emergencies, multilateral statements, and minister travel readouts. Higher frequency during Polish EU Council Presidency periods. |
| **Content Format** | HTML on gov.pl. Formal diplomatic notes and treaty texts sometimes in PDF. Joint communiqués with foreign counterparts published bilingually. |
| **Extraction Method** | HTML scraping of gov.pl listing page at `gov.pl/web/dyplomacja/aktualnosci`. Same gov.pl template as KPRM. |
| **Editorial Orientation** | Official foreign ministry position. Under Foreign Minister Radosław Sikorski (since December 2023), communications emphasize European solidarity, Ukraine support, transatlantic alliance, and Poland's role as a regional security leader. Notably more assertive on Germany relations and EU institutional reform than predecessors. |
| **Why This Source** | The only primary source for Poland's formal diplomatic positions, treaty ratifications, ambassador appointments, bilateral/multilateral meeting readouts, and official responses to international crises. MSZ communications during Poland's EU Council Presidency (January-June 2025) are particularly significant for institutional engagement domain. Embassy-level communications from key posts (Washington, Berlin, Brussels, Kyiv) supplement the central feed. |
| **Access Notes** | Gov.pl platform infrastructure. The legacy `msz.gov.pl` domain still hosts some subsites, notably embassy portals (`{city}.msz.gov.pl`). The press office page at `msz.gov.pl/en/news/press_office/` may still be active. English coverage at `gov.pl/web/diplomacy` is comprehensive for major items. |

**Additional entry points:**
- English news: `https://www.gov.pl/web/diplomacy/news-`
- Embassy-level communications (Brussels EU): `https://brukselaue.msz.gov.pl/en/`
- Embassy-level communications (Brussels NATO): `https://brukselanato.msz.gov.pl/en/`
- Press office: `https://www.msz.gov.pl/en/news/press_office/press_office_2`
- Polish EU Council Presidency: `https://polish-presidency.consilium.europa.eu/en/`

---

### 1.3 Defense Ministry — Ministerstwo Obrony Narodowej (MON)

| Field | Detail |
|---|---|
| **Institution** | Ministerstwo Obrony Narodowej (MON) — Ministry of National Defence |
| **Domain** | `gov.pl/web/obrona-narodowa` (Polish) / `gov.pl/web/national-defence` (English) |
| **Entry Point URL** | `https://www.gov.pl/web/obrona-narodowa/aktualnosci5` |
| **RSS/Atom Feed** | None available on gov.pl. |
| **Language** | Polish (primary); English at `gov.pl/web/national-defence/news` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy (primary), Diplomatic alignment (NATO/bilateral defense) |
| **Publication Frequency** | Daily. 3-7 communications per day covering procurement decisions, military exercises, NATO interoperability activities, force posture changes, personnel appointments, and institutional ceremonies. Significantly higher volume than most NATO peer ministries, reflecting Poland's $48B+ defense modernization programme. |
| **Content Format** | HTML on gov.pl. Press releases frequently include high-resolution photographs. Procurement announcements reference Agencja Uzbrojenia (Armaments Agency) decisions. Some attached PDFs for formal decisions. |
| **Extraction Method** | HTML scraping of gov.pl listing page. Same template as other gov.pl agencies. The legacy `mon.gov.pl` domain redirects to gov.pl but some archived content remains at `archiwum2019-en.mon.gov.pl`. |
| **Editorial Orientation** | Official defense policy position. Under Minister of National Defence Władysław Kosiniak-Kamysz (PSL — coalition partner), communications balance NATO integration emphasis with national defense industry promotion. The Agencja Uzbrojenia (Armaments Agency) publishes procurement details that MON press releases summarize. |
| **Why This Source** | Poland is NATO's sixth-largest defense spender (4%+ of GDP target) and the primary land-force power on the eastern flank. MON communications are the first-order source for: arms procurement decisions (K2 tanks, HIMARS, F-35, Patriot, submarine programme), NATO exercise participation, bilateral defense agreements (US, UK, South Korea, Ukraine), force posture changes (Shield of the East/Tarcza Wschód border fortification), and Territorial Defence Forces (WOT) development. The existing Source Intelligence Map identifies defense procurement pipeline as a key blind spot — MON is the primary official source for this domain. |
| **Access Notes** | Gov.pl platform. English coverage at `gov.pl/web/national-defence/news` is reasonably comprehensive. Social media account @Poland_MOD (X) publishes major items in English. The Agencja Uzbrojenia (Armaments Agency) has a separate website at `au.gov.pl` for procurement-specific communications. |

**Additional entry points:**
- English news: `https://www.gov.pl/web/national-defence/news`
- Agencja Uzbrojenia (Armaments Agency): `https://au.gov.pl/` [VERIFY URL]
- Sztab Generalny WP (General Staff): communications published through MON gov.pl page
- Wojska Obrony Terytorialnej (WOT/Territorial Defence): `https://www.gov.pl/web/obrona-terytorialna` [VERIFY URL]

---

### 1.4 Parliament / Legislature

#### 1.4a Sejm Rzeczypospolitej Polskiej (Lower House)

| Field | Detail |
|---|---|
| **Institution** | Sejm Rzeczypospolitej Polskiej (Sejm — Lower House of Parliament) |
| **Domain** | `sejm.gov.pl` |
| **Entry Point URL** | `https://www.sejm.gov.pl/sejm10.nsf/wydarzenia.xsp?symbol=MEDIA_KOMUNIKATY` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS channels list: `https://www.sejm.gov.pl/sejm10.nsf/rss.xsp`. Feeds available for: new parliamentary documents (druki), session agendas (porządek obrad), committee proceedings, and media communications. |
| **Language** | Polish (primary); English at `sejm.gov.pl/english.nsf/` (limited) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints (primary), Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods (typically 3-4 sitting weeks per month, September-July with summer and holiday recesses). Komunikaty (press releases) issued for plenary sessions, committee meetings, and Speaker-level diplomatic meetings. |
| **Content Format** | HTML (Domino/XPages-based CMS). Parliamentary documents (druki) in PDF. Stenographic records (sprawozdania stenograficzne) in HTML. Voting records available via both website and API. |
| **Extraction Method** | **Preferred: Sejm API** (`api.sejm.gov.pl`) for structured data — legislation, voting records, MP information, committee proceedings, and interpellations. RSS feeds for real-time updates on new documents and session agendas. HTML scraping of komunikaty page as fallback. The ELI API (`api.sejm.gov.pl/eli/`) provides structured access to legislation published in Dziennik Ustaw and Monitor Polski. |
| **Editorial Orientation** | Institutional. Communications reflect the Marshal (Speaker) of the Sejm's office. Committee-level communications may reflect majority-party framing. |
| **Why This Source** | The Sejm is the primary legislative chamber. Defense budget votes, EU treaty ratification, constitutional amendments, and enabling legislation for executive policy originate here. Committee testimony from MON, MSZ, and NBP officials appears in Sejm records before (or instead of) media coverage. The Sejm API is exceptionally well-designed, providing structured JSON access to the full legislative record — a rarity among European parliaments. |
| **Access Notes** | Independent infrastructure (not on gov.pl). The Domino/XPages CMS can be slow and occasionally returns bot-detection challenges. The API at `api.sejm.gov.pl` is the preferred extraction channel — RESTful, well-documented, no authentication required, JSON responses. |

**Key Sejm API endpoints:**

| Endpoint | URL | Data |
|---|---|---|
| Legislation (ELI) | `https://api.sejm.gov.pl/eli/acts/{DU\|MP}/{year}` | Acts published in Dziennik Ustaw / Monitor Polski |
| Act text (PDF) | `https://api.sejm.gov.pl/eli/acts/{pub}/{year}/{pos}/text.pdf` | Full text of legislation |
| Voting records | `https://api.sejm.gov.pl/sejm/term10/votings` | All plenary votes |
| Parliamentary documents | `https://api.sejm.gov.pl/sejm/term10/prints` | Bills, resolutions, reports |
| MP information | `https://api.sejm.gov.pl/sejm/term10/MP` | Current members' data |
| Interpellations | `https://api.sejm.gov.pl/sejm/term10/interpellations` | Parliamentary questions |
| Committee proceedings | `https://api.sejm.gov.pl/sejm/term10/committees` | Committee membership and sessions |

**Additional entry points:**
- RSS channels list: `https://www.sejm.gov.pl/sejm10.nsf/rss.xsp`
- Voting records browser: `https://www.sejm.gov.pl/sejm10.nsf/agent.xsp?symbol=posglos&NrKadencji=10`
- Parliamentary documents: `https://www.sejm.gov.pl/sejm10.nsf/druki.xsp`
- Committee schedule: `https://www.sejm.gov.pl/sejm10.nsf/PlanPosKom.xsp`
- Session agendas: `https://www.sejm.gov.pl/sejm10.nsf/PorzadekObrad.xsp`

---

#### 1.4b Senat Rzeczypospolitej Polskiej (Upper House / Senate)

| Field | Detail |
|---|---|
| **Institution** | Senat Rzeczypospolitej Polskiej (Senate — Upper House of Parliament) |
| **Domain** | `senat.gov.pl` |
| **Entry Point URL** | `https://www.senat.gov.pl/aktualnosci/` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at `senat.gov.pl/rss` or `/feed`] |
| **Language** | Polish (primary); English at `senat.gov.pl/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | 2-5 per week during session periods. Communications cover plenary sessions, committee hearings, Marshal (Speaker) diplomatic activities, and institutional statements. |
| **Content Format** | HTML. Stenographic records of sessions available. Legislative documents in PDF. |
| **Extraction Method** | HTML scraping of aktualnosci/news page. Separate infrastructure from gov.pl and Sejm. |
| **Editorial Orientation** | Institutional — reflects the Marshal of the Senate's office. The Senate has historically maintained a more deliberative, less partisan tone than the Sejm. |
| **Why This Source** | The Senate has a 30-day review period for Sejm-passed legislation and can propose amendments (overridable by Sejm). While less powerful than the Sejm, Senate committee hearings on foreign affairs and defense often feature candid exchanges with government officials. The Senate also plays a unique role in Polish diaspora policy (Polonia affairs). |
| **Access Notes** | Independent infrastructure. Site returned HTTP 403 in testing — may require specific headers or have intermittent access issues. Social media at @PolskiSenat (X). |

---

### 1.5 Official Gazette — Dziennik Ustaw / Monitor Polski

| Field | Detail |
|---|---|
| **Institution** | Dziennik Ustaw Rzeczypospolitej Polskiej (Journal of Laws) + Monitor Polski (Official Gazette) |
| **Domain** | `dziennikustaw.gov.pl` (Dziennik Ustaw) / `monitorpolski.gov.pl` (Monitor Polski) / `isap.sejm.gov.pl` (ISAP — Internet System of Legal Acts) |
| **Entry Point URL** | `https://dziennikustaw.gov.pl/DU` (Journal of Laws) / `https://dziennikustaw.gov.pl/MP` (Monitor Polski) / `https://isap.sejm.gov.pl/` (ISAP search) |
| **RSS/Atom Feed** | None available on the gazette sites. The Sejm ELI API provides structured access to the same data (see section 1.4a). |
| **Language** | Polish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Dziennik Ustaw is the constitutional publication vehicle for all laws, and the Monitor Polski for government orders, international agreements, and official announcements |
| **Publication Frequency** | Daily (multiple publications per day). New acts are published continuously as they are signed and promulgated. |
| **Content Format** | **PDF** exclusively. Each act is published as a separate PDF document. The gazette websites provide HTML index pages linking to individual PDF documents. |
| **Extraction Method** | **Preferred: Sejm ELI API** (`api.sejm.gov.pl/eli/acts/DU/{year}` and `api.sejm.gov.pl/eli/acts/MP/{year}`) for structured metadata and PDF download. Alternative: HTML scraping of `dziennikustaw.gov.pl` index pages, then PDF download and text extraction. ISAP (`isap.sejm.gov.pl`) provides full-text search across the legal database. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. Published by the Government Centre for Legislation (Rządowe Centrum Legislacji) under the authority of the Prime Minister. |
| **Why This Source** | Constitutional requirement: no law is binding until published in the Dziennik Ustaw. International agreements, defense procurement framework laws, EU directive transposition, and fiscal legislation all appear here in definitive form. The ELI API makes Poland's legal gazette one of the most accessible in Europe for automated monitoring. |
| **Access Notes** | No paywall. PDF-only format for actual legal texts. The ISAP system at `isap.sejm.gov.pl` provides the most powerful search interface, including cross-references between acts, consolidation status, and amendment history. Electronic publication has been the official format since 2012. |

**Additional entry points:**
- ISAP search interface: `https://isap.sejm.gov.pl/isap.nsf/ByYear.xsp`
- Monitor Polski (government orders): `https://dziennikustaw.gov.pl/MP`
- ELI API for Dziennik Ustaw: `https://api.sejm.gov.pl/eli/acts/DU/{year}`
- ELI API for Monitor Polski: `https://api.sejm.gov.pl/eli/acts/MP/{year}`

---

### 1.6 Finance Ministry — Ministerstwo Finansów (MF)

| Field | Detail |
|---|---|
| **Institution** | Ministerstwo Finansów (MF) — Ministry of Finance |
| **Domain** | `gov.pl/web/finanse` (Polish) / `gov.pl/web/finance` (English) |
| **Entry Point URL** | `https://www.gov.pl/web/finanse/wiadomosci` |
| **RSS/Atom Feed** | None available on gov.pl. Legacy RSS feeds existed at `mf-arch2.mf.gov.pl/en/web/bip/rss-en` but this is an archived site. |
| **Language** | Polish (primary); English at `gov.pl/web/finance` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Communications cover budget execution, fiscal policy announcements, EU fund absorption (KPO — National Recovery Plan), tax policy changes, public debt management, and international financial cooperation. |
| **Content Format** | HTML on gov.pl. Statistical annexes and budget reports published as PDF. The Ministry also publishes data via dedicated portals (e.g., podatki.gov.pl for tax, KSeF for e-invoicing). |
| **Extraction Method** | HTML scraping of gov.pl listing page at `gov.pl/web/finanse/wiadomosci`. PDF extraction for statistical annexes. |
| **Editorial Orientation** | Official fiscal policy position. Under Minister Andrzej Domański, communications emphasize fiscal discipline, EU fund absorption, and modernization of the tax system (KSeF national e-invoice system). |
| **Why This Source** | Primary source for federal budget execution, public debt data, EU fund drawdown rates (KPO), tax revenue statistics, and fiscal policy announcements. Poland's defense spending increase (to 4%+ of GDP) makes MF budget communications directly relevant to the security/defense domain. EU fund absorption data is a key indicator for institutional engagement. |
| **Access Notes** | Gov.pl platform. The legacy `mf.gov.pl` domain redirects to gov.pl. Specialized portals: `podatki.gov.pl` (tax administration), `e-urzadskarbowy.pl` (e-tax office). English coverage at `gov.pl/web/finance` is limited. |

---

### 1.7 Central Bank — Narodowy Bank Polski (NBP)

| Field | Detail |
|---|---|
| **Institution** | Narodowy Bank Polski (NBP) — National Bank of Poland |
| **Domain** | `nbp.pl` |
| **Entry Point URL** | `https://nbp.pl/polityka-pieniezna/dokumenty-rpp/komunikaty-z-posiedzen-rpp/` (Monetary Policy Council communications) |
| **RSS/Atom Feed** | None identified for press releases. However, the **NBP Web API** at `api.nbp.pl` provides structured data access for exchange rates and gold prices (see below). [VERIFY RSS at `nbp.pl/rss`] |
| **Language** | Polish (primary); English at `nbp.pl/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary Policy Council (RPP) decisions: monthly (typically first Wednesday of each month, except February and August). Press conferences after each decision. Quarterly inflation reports. Weekly data publications. API data: daily updates for exchange rates. |
| **Content Format** | HTML for communications and press releases. **PDF** for monetary policy decisions, minutes (after 6-week delay), inflation reports, and Financial Stability Reports. API returns JSON and XML. |
| **Extraction Method** | **Preferred: NBP Web API** (`api.nbp.pl`) for exchange rate and gold price data — RESTful, well-documented, no authentication, JSON/XML responses. HTML scraping of `nbp.pl/polityka-pieniezna/` for monetary policy decisions and communications. PDF download for formal reports. |
| **Editorial Orientation** | Constitutionally independent central bank. Communications are data-driven and technically rigorous. Under Governor Adam Glapiński (appointed 2016, reappointed 2022), the NBP has been perceived as politically influenced — rate decisions and communication timing have drawn criticism for alignment with PiS political calendar. The Tusk government has limited tools to influence NBP given Glapiński's term extends to 2028. |
| **Why This Source** | NBP is the sole source for authoritative monetary policy decisions, official exchange rates (used for all government transactions), inflation expectations, and financial stability assessments. The NBP Web API is the most machine-friendly government data source in Poland. Monetary policy announcements (particularly rate decisions and forward guidance) move markets and are cited by all financial media. The political tension between the NBP Governor and the Tusk government is itself a signal for the domestic constraints domain. |
| **Access Notes** | No paywall. The `nbp.pl` site uses Imperva/Incapsula bot protection, which may block automated scrapers. The API at `api.nbp.pl` does not appear to have the same restrictions. HTTPS required for API access since August 2025. English-language site at `nbp.pl/en/` mirrors major publications. |

**NBP Web API endpoints:**

| Endpoint | URL | Data |
|---|---|---|
| Exchange rate tables (A) | `https://api.nbp.pl/api/exchangerates/tables/A/` | Mid-market rates for major currencies |
| Exchange rate tables (B) | `https://api.nbp.pl/api/exchangerates/tables/B/` | Mid-market rates for minor currencies |
| Exchange rate tables (C) | `https://api.nbp.pl/api/exchangerates/tables/C/` | Buy/sell rates |
| Specific currency rate | `https://api.nbp.pl/api/exchangerates/rates/A/{code}/` | Rate for a specific currency code |
| Gold prices | `https://api.nbp.pl/api/cenyzlota/` | Current and historical gold prices |
| Historical data | Append `/{startDate}/{endDate}/` to any endpoint | Date-range queries |

**Additional entry points:**
- MPC press releases (English): `https://nbp.pl/en/monetary-policy/mpc-documents/monetary-policy-council-press-releases/`
- Inflation reports: `https://nbp.pl/en/monetary-policy/mpc-documents/inflation-reports/`
- Financial Stability Report: `https://nbp.pl/en/financial-stability/`
- API documentation: `https://api.nbp.pl/en.html`
- Statistics calendar: `https://nbp.pl/en/statistic-and-financial-reporting/calendar/`

---

### 1.8 Trade / Economy — Ministerstwo Rozwoju i Technologii (MRiT)

| Field | Detail |
|---|---|
| **Institution** | Ministerstwo Rozwoju i Technologii (MRiT) — Ministry of Economic Development and Technology |
| **Domain** | `gov.pl/web/rozwoj-technologia` (Polish) / `gov.pl/web/development-technology` (English) |
| **Entry Point URL** | `https://www.gov.pl/web/rozwoj-technologia/aktualnosci` [VERIFY URL — may use `/wiadomosci`] |
| **RSS/Atom Feed** | None available on gov.pl. |
| **Language** | Polish (primary); English at `gov.pl/web/development-technology` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-4 per week. Communications cover trade policy, FDI promotion, industrial policy, EU Single Market implementation, construction and spatial planning regulation, and technology/innovation initiatives. |
| **Content Format** | HTML on gov.pl. Trade statistics and reports in PDF. |
| **Extraction Method** | HTML scraping of gov.pl listing page. Same template as other gov.pl agencies. |
| **Editorial Orientation** | Official trade and industrial policy position. Emphasizes Poland's competitiveness, nearshoring opportunities (post-Ukraine war supply chain restructuring), EU Cohesion Fund absorption, and industrial modernization. |
| **Why This Source** | Primary source for trade policy announcements, FDI data, industrial strategy, and EU Single Market regulatory implementation. Poland's position as a beneficiary of supply chain restructuring away from Russia/China and toward Central Europe makes MRiT communications relevant to the diplomatic alignment domain. The ministry also oversees the Polish Investment and Trade Agency (PAIH). |
| **Access Notes** | Gov.pl platform. The Ministry of Economic Development and Technology handles economy and trade functions; note that some trade policy communications may also originate from the Ministry of Foreign Affairs (MSZ) or the PM's office for bilateral trade negotiations. PAIH (Polish Investment and Trade Agency) has a separate portal at `paih.gov.pl`. |

**Additional entry points:**
- PAIH (Polish Investment and Trade Agency): `https://www.paih.gov.pl/en`
- English site: `https://www.gov.pl/web/development-technology`

---

### 1.9 Intelligence / National Security — ABW, AW, BBN/RBN

Poland's intelligence and national security architecture involves three key institutions: the Internal Security Agency (ABW), the Foreign Intelligence Agency (AW), and the National Security Bureau (BBN), which serves as the President's national security advisory body and secretariat for the National Security Council (RBN).

#### 1.9a Agencja Bezpieczeństwa Wewnętrznego (ABW — Internal Security Agency)

| Field | Detail |
|---|---|
| **Institution** | Agencja Bezpieczeństwa Wewnętrznego (ABW) — Internal Security Agency |
| **Domain** | `abw.gov.pl` |
| **Entry Point URL** | `https://www.abw.gov.pl/pl/aktualnosci` [VERIFY URL] |
| **RSS/Atom Feed** | None available. |
| **Language** | Polish (primary); English at `abw.gov.pl/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Low — approximately 2-5 publications per month. Communications issued for espionage arrests, terrorism-related detentions, cybersecurity incidents, and institutional statements. No routine operational reporting. |
| **Content Format** | HTML. Minimal — short press releases. |
| **Extraction Method** | Periodic check of aktualnosci page. Low-frequency monitoring sufficient. |
| **Editorial Orientation** | Controlled institutional communication. ABW publishes only what it wants public — typically post-arrest announcements designed to demonstrate operational capability. |
| **Why This Source** | ABW's public communications, while infrequent, are high-signal. Espionage arrests (particularly Russian/Belarusian), counterterrorism operations, and cybersecurity advisories directly affect the security/defense domain. The agency's role in protecting classified defense procurement information makes its operational announcements relevant to tracking foreign intelligence threats to Poland's defense modernization. Under the Tusk government, ABW leadership has been restructured, and investigations into previous government use of Pegasus spyware are ongoing — the agency's public statements on these matters are a domestic constraints signal. |
| **Access Notes** | Independent domain (not gov.pl). English site at `abw.gov.pl/en/` covers major items. Minimal site — no bot protection concerns. |

#### 1.9b Agencja Wywiadu (AW — Foreign Intelligence Agency)

| Field | Detail |
|---|---|
| **Institution** | Agencja Wywiadu (AW) — Foreign Intelligence Agency |
| **Domain** | `aw.gov.pl` |
| **Entry Point URL** | `https://aw.gov.pl/pl/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Polish (primary); English at `aw.gov.pl/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible. AW publishes virtually no operational or policy communications. The website is primarily institutional (organizational structure, legal framework, recruitment). |
| **Content Format** | Minimal HTML. |
| **Extraction Method** | Weekly periodic check. Any new publication should be flagged as a high-priority anomaly. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. AW's public communications are almost nonexistent. Its website provides legal framework documents and recruitment information but no operational content. Real intelligence signal from AW surfaces through leaks to investigative outlets, parliamentary oversight committee proceedings, and presidential/PM statements referencing intelligence assessments. The current head is Colonel Bartosz Jarmuszkiewicz. |
| **Access Notes** | Independent domain. Minimal static site. |

#### 1.9c Biuro Bezpieczeństwa Narodowego (BBN — National Security Bureau) / Rada Bezpieczeństwa Narodowego (RBN — National Security Council)

| Field | Detail |
|---|---|
| **Institution** | Biuro Bezpieczeństwa Narodowego (BBN) — National Security Bureau; serves as secretariat for the Rada Bezpieczeństwa Narodowego (RBN — National Security Council) |
| **Domain** | `bbn.gov.pl` (Polish) / `en.bbn.gov.pl` (English) |
| **Entry Point URL** | `https://www.bbn.gov.pl/pl/wydarzenia/` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Polish (primary); English at `en.bbn.gov.pl/en/news` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy (primary), Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Communications cover National Security Council sessions, presidential meetings with military/intelligence leadership, national security strategy documents, and BBN analytical publications. |
| **Content Format** | HTML. Strategic documents (National Security Strategy, Strategic Defence Review) published as PDF. |
| **Extraction Method** | HTML scraping of wydarzenia (events) page. English mirror at `en.bbn.gov.pl/en/news`. |
| **Editorial Orientation** | Reflects the President's national security priorities. Under President Nawrocki, expect emphasis on Eastern flank security, defense spending, and sovereign security capabilities. BBN has historically been the intellectual engine for Poland's national security doctrine, producing the National Security Strategy and Strategic Defence Review documents. |
| **Why This Source** | BBN communications reveal presidential-level security assessments and priorities that may diverge from the PM-led government's positions (cohabitation effect). National Security Council (RBN) session communiqués — issued after meetings chaired by the President with participation of the PM, defense minister, foreign minister, and intelligence chiefs — are the highest-level signal of Poland's security posture consensus or disagreement. The BBN's National Security Strategy (last published 2020) and its updates frame Poland's strategic threat assessment. |
| **Access Notes** | Independent domain (not gov.pl). English site at `en.bbn.gov.pl` covers major items. The BBN is a presidential body — its website infrastructure is independent of the PM-controlled gov.pl platform. @BBN_PL on X. |

**Additional entry points:**
- English news: `https://en.bbn.gov.pl/en/news`
- National Security Strategy documents: published on BBN website
- RBN (National Security Council) communiqués: published as BBN news items after each session

---

### 1.10 Country-Specific Institutions

#### 1.10a Stałe Przedstawicielstwo RP przy UE (Permanent Representation to the EU)

| Field | Detail |
|---|---|
| **Institution** | Stałe Przedstawicielstwo Rzeczypospolitej Polskiej przy Unii Europejskiej — Permanent Representation of Poland to the EU |
| **Domain** | `brukselaue.msz.gov.pl` / `gov.pl/web/eu` |
| **Entry Point URL** | `https://www.gov.pl/web/eu` |
| **RSS/Atom Feed** | None available. |
| **Language** | Polish and English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | 2-4 per week. Communications cover EU Council working group positions, COREPER deliberations (summary level), bilateral meetings with EU officials, and Poland's negotiating positions on major EU files. |
| **Content Format** | HTML on gov.pl and MSZ embassy subdomain. |
| **Extraction Method** | HTML scraping of gov.pl/web/eu. Cross-reference with embassy subdomain at `brukselaue.msz.gov.pl/en/`. |
| **Editorial Orientation** | Reflects Poland's official EU negotiating position. Particularly relevant during Poland's EU Council Presidency (January-June 2025) and its aftermath. |
| **Why This Source** | Poland's EU representation is the front line for institutional engagement — Council votes, EU budget negotiations, KPO (National Recovery Plan) drawdowns, rule-of-law dialogue, and the EU enlargement file (especially Ukraine's accession). Communications from this post provide early indicators of Poland's positioning on EU institutional reform, defense integration, and migration policy. |
| **Access Notes** | Dual infrastructure: gov.pl platform and MSZ embassy subdomain. Contact: `bebrustpe@msz.gov.pl`. |

#### 1.10b Stałe Przedstawicielstwo RP przy NATO (Permanent Delegation to NATO)

| Field | Detail |
|---|---|
| **Institution** | Stałe Przedstawicielstwo RP przy NATO — Polish Delegation to NATO |
| **Domain** | `brukselanato.msz.gov.pl` |
| **Entry Point URL** | `https://brukselanato.msz.gov.pl/en/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Polish and English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | 1-3 per week. Communications cover NATO Council deliberations (Poland's positions), bilateral meetings at NATO HQ, and Polish contributions to NATO operations and initiatives. |
| **Content Format** | HTML on MSZ embassy subdomain. |
| **Extraction Method** | HTML scraping of brukselanato.msz.gov.pl. |
| **Editorial Orientation** | Official Polish NATO policy. Emphasizes eastern flank security, Article 5 credibility, and Polish burden-sharing leadership (4%+ GDP defense spending). |
| **Why This Source** | Poland is the dominant land-force power on NATO's eastern flank and hosts significant allied force presence (US, UK). The NATO delegation's communications reveal Poland's positions on NATO strategic concept implementation, force posture decisions, alliance burden-sharing debates, and responses to Russian/Belarusian provocations. |
| **Access Notes** | MSZ embassy subdomain infrastructure. Social media at @PLinnato (X). |

#### 1.10c Three Seas Initiative (Inicjatywa Trójmorza)

| Field | Detail |
|---|---|
| **Institution** | Three Seas Initiative (Inicjatywa Trójmorza / 3SI) — multilateral platform |
| **Domain** | `3seas.eu` |
| **Entry Point URL** | `https://3seas.eu/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Economic & technological statecraft |
| **Publication Frequency** | Low — event-driven (annual summit, business forum). Periodic updates on infrastructure projects and investment fund activities. |
| **Content Format** | HTML. Summit declarations and project documentation in PDF. |
| **Extraction Method** | Periodic check of main site. Event-driven monitoring around annual summits. |
| **Editorial Orientation** | Multilateral platform reflecting consensus of 13 Central/Eastern European EU member states. Poland (co-founder with Croatia in 2015) has historically been the initiative's primary champion. |
| **Why This Source** | The Three Seas Initiative is a key vehicle for Poland's regional leadership ambition — connecting Baltic, Adriatic, and Black Sea states through energy, transport, and digital infrastructure. Poland's government has appointed a dedicated Government Plenipotentiary for the Three Seas Initiative. The initiative's investment fund and project pipeline are indicators of Poland's regional economic statecraft. The 2025 Warsaw summit was a major milestone. |
| **Access Notes** | International platform site. Also monitor Polish government communications about 3SI through KPRM and MSZ channels. The Three Seas Initiative Research Center at `3si.politic.edu.pl` provides academic analysis. |

#### 1.10d Główny Urząd Statystyczny (GUS — Statistics Poland)

| Field | Detail |
|---|---|
| **Institution** | Główny Urząd Statystyczny (GUS) — Statistics Poland |
| **Domain** | `stat.gov.pl` |
| **Entry Point URL** | `https://stat.gov.pl/en/` |
| **RSS/Atom Feed** | **Yes.** RSS channels available at `https://stat.gov.pl/en/rss/` |
| **Language** | Polish and English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Daily. Statistical releases follow a pre-published calendar. Key indicators: GDP, CPI/inflation, industrial production, trade balance, unemployment, demographics. |
| **Content Format** | HTML for flash estimates and press releases. PDF for detailed statistical publications. The GUS API portal (`api.stat.gov.pl`) provides structured data access. |
| **Extraction Method** | RSS feeds for publication alerts. GUS API (`api.stat.gov.pl`) for structured statistical data in JSON format. |
| **Editorial Orientation** | Institutional — non-partisan statistical authority. EU/Eurostat methodology compliance. |
| **Why This Source** | GUS provides the authoritative economic data that underlies all economic/technological statecraft analysis. GDP growth, inflation, trade balance, and industrial production data are essential context for interpreting government policy decisions. The GUS API and RSS feeds make it one of the most automation-friendly Polish government sources. |
| **Access Notes** | No paywall. RSS feeds functional. API at `api.stat.gov.pl` provides RESTful access to statistical databases. English-language coverage is comprehensive. |

**Additional entry points:**
- RSS feeds: `https://stat.gov.pl/en/rss/`
- GUS API portal: `https://api.stat.gov.pl/Home/Index?lang=en`
- Publication calendar: published annually
- Regional statistical offices also maintain RSS at `{city}.stat.gov.pl/en/rss/`

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS/API Available | Priority | Content Format | Frequency | gov.pl Platform |
|---|---|---|---|---|---|---|---|
| 1a | Prezydent RP (KPRP) | `prezydent.pl/aktualnosci` | [VERIFY] | P1 | HTML/PDF | Daily | No |
| 1b | Premier / KPRM | `gov.pl/web/premier/aktualnosci` | No | P1 | HTML | Daily | Yes |
| 2 | MSZ (Foreign Affairs) | `gov.pl/web/dyplomacja/aktualnosci` | No | P1 | HTML/PDF | Daily | Yes |
| 3 | MON (Defence) | `gov.pl/web/obrona-narodowa/aktualnosci5` | No | P1 | HTML | Daily | Yes |
| 4a | Sejm | `sejm.gov.pl/.../MEDIA_KOMUNIKATY` | **Yes** (RSS + API) | P2 | HTML/PDF | Daily (session) | No |
| 4b | Senat | `senat.gov.pl/aktualnosci/` | [VERIFY] | P2 | HTML | 2-5/week (session) | No |
| 5 | Dziennik Ustaw / Monitor Polski | `dziennikustaw.gov.pl/DU` | **Yes** (ELI API) | P2 | PDF | Daily | No |
| 6 | MF (Finance) | `gov.pl/web/finanse/wiadomosci` | No | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | NBP (Central Bank) | `nbp.pl/.../komunikaty-z-posiedzen-rpp/` | **Yes** (Web API) | P2 | PDF/HTML/API | Variable | No |
| 8 | MRiT (Development/Technology) | `gov.pl/web/rozwoj-technologia/aktualnosci` | No | P2 | HTML | 2-4/week | Yes |
| 9a | ABW (Internal Security) | `abw.gov.pl/pl/aktualnosci` | No | P2 | HTML | 2-5/month | No |
| 9b | AW (Foreign Intelligence) | `aw.gov.pl` | No | P2 | Minimal | Negligible | No |
| 9c | BBN (Nat. Security Bureau) | `bbn.gov.pl/pl/wydarzenia/` | No | P2 | HTML/PDF | 2-5/week | No |
| 10a | Perm. Rep. to EU | `gov.pl/web/eu` / `brukselaue.msz.gov.pl` | No | P2 | HTML | 2-4/week | Mixed |
| 10b | Perm. Del. to NATO | `brukselanato.msz.gov.pl` | No | P2 | HTML | 1-3/week | No |
| 10c | Three Seas Initiative | `3seas.eu` | No | P2 | HTML/PDF | Event-driven | No |
| 10d | GUS (Statistics) | `stat.gov.pl` | **Yes** (RSS + API) | P2 | HTML/PDF/API | Daily | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Poland Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/pl.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: pl_prezydent
    name: Kancelaria Prezydenta RP (KPRP)
    domain: prezydent.pl
    entry_url: "https://www.prezydent.pl/aktualnosci"
    rss_feed: null  # [VERIFY]
    language: pl
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
    notes: "Independent infrastructure (not gov.pl). English mirror at president.pl/news. Cohabitation dynamics with PM Tusk make presidential statements high-signal."

  - id: pl_kprm
    name: Kancelaria Prezesa Rady Ministrów (KPRM)
    domain: gov.pl
    entry_url: "https://www.gov.pl/web/premier/aktualnosci"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    additional_urls:
      - "https://www.gov.pl/web/premier/decyzje-rzadu"
      - "https://www.gov.pl/web/premier/komunikaty-cir"
    notes: "Council of Ministers decisions (Tuesdays). CIR rapid-response communications. @PremierRP and @KPRM_CIR on X often publish first."

  - id: pl_msz
    name: Ministerstwo Spraw Zagranicznych (MSZ)
    domain: gov.pl
    entry_url: "https://www.gov.pl/web/dyplomacja/aktualnosci"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Embassy-level releases at {city}.msz.gov.pl. English at gov.pl/web/diplomacy. EU Council Presidency communications especially significant."

  - id: pl_mon
    name: Ministerstwo Obrony Narodowej (MON)
    domain: gov.pl
    entry_url: "https://www.gov.pl/web/obrona-narodowa/aktualnosci5"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "High volume (3-7/day). Covers $48B+ procurement programme. English at gov.pl/web/national-defence/news. Agencja Uzbrojenia at au.gov.pl for procurement detail."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: pl_sejm
    name: Sejm Rzeczypospolitej Polskiej
    domain: sejm.gov.pl
    entry_url: "https://www.sejm.gov.pl/sejm10.nsf/wydarzenia.xsp?symbol=MEDIA_KOMUNIKATY"
    rss_feed: "https://www.sejm.gov.pl/sejm10.nsf/rss.xsp"  # Multiple channel feeds available
    api_endpoints:
      legislation: "https://api.sejm.gov.pl/eli/acts/{publisher}/{year}"
      votings: "https://api.sejm.gov.pl/sejm/term10/votings"
      prints: "https://api.sejm.gov.pl/sejm/term10/prints"
      MPs: "https://api.sejm.gov.pl/sejm/term10/MP"
      interpellations: "https://api.sejm.gov.pl/sejm/term10/interpellations"
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html_json_pdf
    extraction_method: api_and_rss
    poll_interval_hours: 6
    notes: "Sejm API is exceptionally well-designed — preferred extraction channel. RSS for real-time alerts. Domino CMS may block scrapers."

  - id: pl_senat
    name: Senat Rzeczypospolitej Polskiej
    domain: senat.gov.pl
    entry_url: "https://www.senat.gov.pl/aktualnosci/"
    rss_feed: null  # [VERIFY]
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "2-5_per_week_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "30-day legislative review window. HTTP 403 observed in testing — may need specific headers. @PolskiSenat on X."

  - id: pl_dziennik_ustaw
    name: Dziennik Ustaw / Monitor Polski
    domain: dziennikustaw.gov.pl
    entry_url: "https://dziennikustaw.gov.pl/DU"
    rss_feed: null
    api_endpoints:
      eli_du: "https://api.sejm.gov.pl/eli/acts/DU/{year}"
      eli_mp: "https://api.sejm.gov.pl/eli/acts/MP/{year}"
      act_pdf: "https://api.sejm.gov.pl/eli/acts/{pub}/{year}/{pos}/text.pdf"
    language: pl
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
    extraction_method: api_and_pdf_extract
    poll_interval_hours: 6
    notes: "Use Sejm ELI API as primary access channel. ISAP at isap.sejm.gov.pl for full-text legal search."

  - id: pl_mf
    name: Ministerstwo Finansów (MF)
    domain: gov.pl
    entry_url: "https://www.gov.pl/web/finanse/wiadomosci"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Budget execution, KPO fund absorption, public debt. Defense spending data (4%+ GDP) relevant to security domain. English at gov.pl/web/finance."

  - id: pl_nbp
    name: Narodowy Bank Polski (NBP)
    domain: nbp.pl
    entry_url: "https://nbp.pl/polityka-pieniezna/dokumenty-rpp/komunikaty-z-posiedzen-rpp/"
    rss_feed: null  # [VERIFY]
    api_endpoints:
      exchange_rates_a: "https://api.nbp.pl/api/exchangerates/tables/A/"
      exchange_rates_b: "https://api.nbp.pl/api/exchangerates/tables/B/"
      exchange_rates_c: "https://api.nbp.pl/api/exchangerates/tables/C/"
      gold_prices: "https://api.nbp.pl/api/cenyzlota/"
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_html_api
    extraction_method: api_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "NBP Web API at api.nbp.pl for exchange rates/gold — no auth, JSON/XML. Imperva bot protection on main site. MPC decisions monthly (first Wed). English at nbp.pl/en/."

  - id: pl_mrit
    name: Ministerstwo Rozwoju i Technologii (MRiT)
    domain: gov.pl
    entry_url: "https://www.gov.pl/web/rozwoj-technologia/aktualnosci"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Trade policy, FDI, industrial strategy. PAIH (investment agency) at paih.gov.pl provides supplementary trade data."

  - id: pl_abw
    name: Agencja Bezpieczeństwa Wewnętrznego (ABW)
    domain: abw.gov.pl
    entry_url: "https://www.abw.gov.pl/pl/aktualnosci"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-5_per_month"
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 24
    notes: "Low frequency but high signal. Espionage arrests, counter-terrorism, cybersecurity. Any publication should be flagged for immediate review."

  - id: pl_aw
    name: Agencja Wywiadu (AW)
    domain: aw.gov.pl
    entry_url: "https://aw.gov.pl/pl/"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent agency. Website is institutional/recruitment only. Flag any new publication as high-priority anomaly."

  - id: pl_bbn
    name: Biuro Bezpieczeństwa Narodowego (BBN)
    domain: bbn.gov.pl
    entry_url: "https://www.bbn.gov.pl/pl/wydarzenia/"
    rss_feed: null  # [VERIFY]
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html_pdf
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Presidential NSC body. RBN session communiqués are high-signal. English at en.bbn.gov.pl/en/news. Independent of gov.pl (presidential infrastructure)."

  - id: pl_eu_rep
    name: Stałe Przedstawicielstwo RP przy UE
    domain: brukselaue.msz.gov.pl
    entry_url: "https://www.gov.pl/web/eu"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Dual infrastructure: gov.pl and MSZ embassy subdomain. EU Council Presidency aftermath tracking."

  - id: pl_nato_del
    name: Stałe Przedstawicielstwo RP przy NATO
    domain: brukselanato.msz.gov.pl
    entry_url: "https://brukselanato.msz.gov.pl/en/"
    rss_feed: null
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "1-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Eastern flank security positions. @PLinnato on X."

  - id: pl_3seas
    name: Three Seas Initiative (Inicjatywa Trójmorza)
    domain: 3seas.eu
    entry_url: "https://3seas.eu/"
    rss_feed: null  # [VERIFY]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - economic_technological_statecraft
    publication_frequency: event_driven
    content_format: html_pdf
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Multilateral platform. Monitor around annual summits. Poland is co-founder and primary champion."

  - id: pl_gus
    name: Główny Urząd Statystyczny (GUS)
    domain: stat.gov.pl
    entry_url: "https://stat.gov.pl/en/"
    rss_feed: "https://stat.gov.pl/en/rss/"
    api_endpoint: "https://api.stat.gov.pl/Home/Index?lang=en"
    language: pl
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html_pdf_api
    extraction_method: rss_poll_and_api
    poll_interval_hours: 6
    notes: "RSS feeds functional. API at api.stat.gov.pl for structured data. Publication calendar available. English coverage comprehensive."

# Extraction pattern for gov.pl agencies
gov_pl_shared_config:
  base_url_pattern: "https://www.gov.pl/web/{agency_slug}/{section}"
  agencies_on_platform:
    - slug: premier
      sections: [aktualnosci, decyzje-rzadu, komunikaty-cir, zapowiedzi]
    - slug: dyplomacja
      sections: [aktualnosci]
    - slug: obrona-narodowa
      sections: [aktualnosci5]
    - slug: finanse
      sections: [wiadomosci]
    - slug: rozwoj-technologia
      sections: [aktualnosci]
    - slug: eu
      sections: []  # main page
  pagination: query_parameter_or_path
  bot_protection: minimal  # less aggressive than gob.mx
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "pl-PL,pl;q=0.9,en;q=0.5"
  rate_limit: "max 1 request per 2 seconds per agency"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Polish government communications are professionally produced but systematically present the issuing institution's perspective. The pipeline must treat government sources as confirming what the government has chosen to state publicly — not as confirming facts. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing and language relative to media coverage.

- **Prezydent RP (KPRP)**: Presidential statements on defense and foreign policy should be triangulated against same-day KPRM (PM office) communications to detect cohabitation friction. When presidential and PM framing diverges on NATO commitments, EU integration, or Ukraine policy, it signals domestic constraint on external action. Cross-reference with TVN24 (liberal framing) and Republika TV (conservative framing) to gauge how each side's base receives the presidential position. Rzeczpospolita provides the most balanced centre-right analysis of presidential initiatives.

- **KPRM / Premier**: Council of Ministers decisions should be triangulated against Gazeta Wyborcza (pro-government liberal perspective), Rzeczpospolita (independent centre-right analysis), and Do Rzeczy/wPolityce (opposition conservative framing). CIR rapid-response communications are reactive framing — compare against PAP wire copy for the factual baseline. The PM's bilateral meeting readouts should be cross-referenced with counterpart government communiqués (especially German Bundeskanzleramt, French Elysée, Ukrainian Presidential Office).

- **MSZ (Foreign Affairs)**: Diplomatic komunikaty should be triangulated against PISM analysis (government-adjacent think tank providing depth that official communications lack) and OSW analysis (for Eastern neighbourhood context). When MSZ and PISM framing diverge, it may signal internal policy debate. For EU institutional matters, cross-reference with Notes from Poland (English-language synthesis) and Dziennik Gazeta Prawna (EU regulation detail).

- **MON (Defence)**: Defense procurement announcements present decisions favourably without cost-benefit analysis or delivery risk assessment. Cross-reference with Defence24 (specialist independent analysis — the single most important supplement to MON communications), Rzeczpospolita (defence budget scrutiny), and international defence press (Jane's, IISS). Defence24 frequently provides technical detail and timeline analysis absent from official MON releases.

- **NBP**: Monetary policy decisions are technically rigorous but the political dynamics of the Glapiński governorship mean that rate decision timing and forward guidance language require political reading. Cross-reference with Dziennik Gazeta Prawna (financial analysis), Rzeczpospolita (macro-economic interpretation), and international financial media. The gap between NBP inflation forecasts and MF budget assumptions is itself a signal.

- **Sejm / Senat**: Legislative proceedings are voluminous. Prioritize: (a) foreign affairs committee (komisja spraw zagranicznych) sessions, (b) national defence committee (komisja obrony narodowej), (c) EU affairs committee, (d) budget committee during annual budget review. Cross-reference committee testimony with PAP wire coverage — PAP typically covers committee hearings in detail.

- **BBN / RBN**: National Security Council communiqués are consensus documents — their language reflects what the President and PM could agree to state jointly. When RBN communiqués are delayed or unusually terse, it signals disagreement. Cross-reference with OKO.press and Gazeta Wyborcza for leaked accounts of RBN deliberations.

**4.2 The gov.pl partial centralization effect**

Five of Poland's government source categories publish through the gov.pl platform (KPRM, MSZ, MON, MF, MRiT). This creates operational efficiency but also means:
- Platform-wide outages affect all five sources simultaneously
- Template changes propagate across all agencies
- The Ministry of Digital Affairs controls the platform infrastructure
- However, unlike Mexico's gob.mx, several critical Polish sources operate on fully independent infrastructure (Prezydent, Sejm, Senat, NBP, ABW, AW, BBN), reducing single-point-of-failure risk

Sources outside gov.pl operate on diverse, independent infrastructure — from the Sejm's Domino/XPages CMS to the NBP's Imperva-protected site to the President's independent web platform. This diversity requires multiple extraction modules but provides resilience.

**4.3 The cohabitation signal**

Poland's semi-presidential system creates a structurally significant monitoring dynamic absent in purely parliamentary systems. When the President (Nawrocki, PiS-aligned) and PM (Tusk, KO-led coalition) disagree, the disagreement surfaces as divergent framing in KPRP vs. KPRM communications on the same events. Key domains for cohabitation friction:
- **Defense**: The President is supreme commander; the PM controls the defense budget and procurement decisions
- **Foreign policy**: The President represents Poland internationally and ratifies treaties; the PM sets diplomatic strategy
- **Legislation**: The President can veto Sejm-passed legislation, requiring a 3/5 majority to override
- **Intelligence**: The President chairs the RBN (National Security Council); the PM oversees ABW and AW operationally

Monitor both KPRP and KPRM communications on the same events and flag divergent language as a domestic constraints indicator.

**4.4 The intelligence silence problem**

Poland's intelligence agencies (ABW, AW) produce minimal public communications — ABW publishes 2-5 items per month; AW publishes virtually nothing. This is a structural gap that cannot be filled by monitoring official channels. Intelligence-relevant signals surface through:
- Leaks to investigative media (Gazeta Wyborcza, OKO.press, Onet investigations)
- Sejm special committee proceedings (komisja ds. służb specjalnych — sessions are classified but members occasionally brief media)
- BBN/RBN communications that reference intelligence assessments
- MON communications referencing "threat assessments" from security services
- ABW post-arrest announcements (which reveal operational priorities retrospectively)

The pipeline should not allocate significant resources to polling AW's website but should flag any new ABW publication for immediate review, and should tag any KPRM, MON, or BBN communication referencing intelligence agencies as high-priority.

**4.5 The Sejm API advantage**

The Sejm API (`api.sejm.gov.pl`) is one of the most comprehensive and well-designed parliamentary APIs in Europe. It provides structured JSON access to legislation, voting records, MP data, interpellations, and committee proceedings. For pipeline purposes, the API should be the primary channel for legislative monitoring rather than HTML scraping — it provides:
- Real-time voting records (critical for tracking coalition cohesion on defense/foreign policy votes)
- Full legislative text via ELI API (the same data published in Dziennik Ustaw)
- Interpellations (parliamentary questions to ministers — often surface policy tensions before media coverage)
- Committee membership changes (indicator of political reshuffling)

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Shared Extraction Architecture for gov.pl

The gov.pl platform hosts 5 of 19 monitored government endpoints. A single scraper module with agency-slug parameterization can service all five:

- **URL pattern**: `https://www.gov.pl/web/{slug}/{section}`
- **Agency slugs and sections**:
  - `premier`: aktualnosci, decyzje-rzadu, komunikaty-cir, zapowiedzi
  - `dyplomacja`: aktualnosci
  - `obrona-narodowa`: aktualnosci5
  - `finanse`: wiadomosci
  - `rozwoj-technologia`: aktualnosci
- **Pagination**: Query parameter or path-based (varies by section)
- **Rate limit**: Enforce minimum 2-second intervals between requests.
- **Bot protection**: Minimal — less aggressive than Mexico's gob.mx. Standard HTTP headers should suffice. No Cloudflare challenges observed in testing.

### 5.2 API-Enabled Sources (Priority for Automation)

Poland offers three high-quality government APIs — significantly more than most European countries:

1. **Sejm API** (`api.sejm.gov.pl`): RESTful, no authentication, JSON responses. Covers legislation (ELI), voting records, MP data, interpellations, and committee proceedings. The single most valuable automated data source in the Polish government ecosystem. Documentation at `api.sejm.gov.pl/API_pl.html`.

2. **NBP Web API** (`api.nbp.pl`): RESTful, no authentication, JSON/XML responses. Exchange rates (tables A/B/C), gold prices, historical data. HTTPS required since August 2025. Documentation at `api.nbp.pl/en.html`.

3. **GUS API** (`api.stat.gov.pl`): RESTful access to statistical databases. GDP, CPI, trade balance, industrial production, demographics. Documentation at `api.stat.gov.pl/Home/Index?lang=en`.

### 5.3 RSS-Enabled Sources

Two government sources provide functional RSS feeds:

1. **Sejm**: Multiple RSS channels at `sejm.gov.pl/sejm10.nsf/rss.xsp` covering new parliamentary documents, session agendas, committee proceedings, and media communications. Domino-based RSS feeds — may require namespace handling.

2. **GUS (Statistics Poland)**: RSS at `stat.gov.pl/en/rss/` for publication alerts. Regional statistical offices also provide RSS at `{city}.stat.gov.pl/rss/`.

All other sources require HTML scraping or API polling.

### 5.4 PDF Extraction Requirements

Three sources publish primarily or substantially in PDF:
- **Dziennik Ustaw / Monitor Polski**: All legal texts are PDF. Well-structured, text-based PDFs (electronic publication since 2012 — no OCR needed). Accessible via ELI API.
- **NBP**: Monetary policy decisions, MPC minutes (6-week delay), inflation reports, and Financial Stability Reports are multi-page PDF. Text-based, well-structured.
- **BBN**: National Security Strategy, Strategic Defence Review, and other strategic documents are PDF.

### 5.5 Language and Encoding

All government sources publish primarily in Polish. English-language coverage varies:
- **Comprehensive English**: NBP (parallel publications), GUS (parallel publications), Sejm (API data language-neutral), MSZ (via `gov.pl/web/diplomacy`), MON (via `gov.pl/web/national-defence`)
- **Partial English**: Prezydent (via `president.pl`), BBN (via `en.bbn.gov.pl`), ABW (via `abw.gov.pl/en`)
- **Minimal/No English**: MF, MRiT, Senat, Dziennik Ustaw

All gov.pl content is UTF-8 encoded. Independent sites (Sejm, Senat, NBP) may vary but modern Polish web infrastructure is consistently UTF-8. Normalize to UTF-8 on ingestion as a precaution.

### 5.6 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A Council of Ministers decision appears in KPRM decyzje-rzadu, the relevant ministry's aktualnosci, and (if legislative) eventually in Dziennik Ustaw
- Defense procurement decisions appear in MON, KPRM, and sometimes Prezydent communications
- International agreements appear in MSZ, KPRM, Prezydent (ratification), and Dziennik Ustaw (publication)
- National Security Council outcomes appear in BBN, Prezydent, and sometimes KPRM communications

Implement content-hash deduplication. Use the Dziennik Ustaw/ELI API publication as the canonical version for legal texts. Use the originating ministry (MSZ for diplomatic, MON for defense) as canonical for policy communications. For cohabitation analysis, retain both Prezydent and KPRM versions of the same event to enable divergence detection.

### 5.7 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Prezydent, KPRM, MSZ | Every 2 hours | Daily publication, policy-critical, cohabitation signal |
| P1-Standard | MON | Every 2 hours | High volume (3-7/day), defense procurement critical |
| P2-Active (API) | Sejm (API), NBP (API), GUS (API/RSS) | Every 6 hours | Structured data, high automation potential |
| P2-Active (scrape) | Dziennik Ustaw, MF, BBN, EU Rep, NATO Del | Every 6-12 hours | Regular publishing schedule |
| P2-Low | Senat, MRiT, 3SI | Every 12 hours | Lower frequency, session-dependent |
| P2-Minimal | ABW | Every 24 hours | Low frequency; flag any new publication immediately |
| P2-Silent | AW | Weekly | Effectively silent; flag any publication as anomaly |

### 5.8 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| gov.pl platform outage | KPRM, MSZ, MON, MF, MRiT | Monitor @PremierRP, @KPRM_CIR, @Poland_MOD, @MSZ_RP on X. PAP wire service at `pap.pl` typically carries government communications within minutes. |
| Sejm Domino CMS bot block | Sejm website | Use Sejm API (`api.sejm.gov.pl`) — independent infrastructure from the website CMS. RSS feeds may also remain functional during CMS issues. |
| NBP Imperva block | NBP website | Use NBP Web API (`api.nbp.pl`) for exchange rate data — separate infrastructure. For monetary policy decisions, monitor PAP and Dziennik Gazeta Prawna for immediate coverage. |
| prezydent.pl downtime | Prezydent RP | Monitor @prezydentpl on X and `president.pl` (English mirror, may be on different infrastructure). BBN (`bbn.gov.pl`) often carries presidential security-related communications. |
| Senat 403 errors | Senat | Monitor @PolskiSenat on X. PAP covers major Senate proceedings. SIL (Legislative Information System) at `sil.gobernacion.gob.mx` [N/A for Poland — no direct equivalent]. |
| Embassy subdomain issues | EU Rep, NATO Del | Use gov.pl/web/eu as primary. For NATO delegation, monitor @PLinnato on X. |
| API rate limiting | Sejm API, NBP API, GUS API | Implement exponential backoff. Cache responses. APIs are generally generous with rate limits but no formal SLAs. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of the gov.pl platform, change in government administration (especially post-election), presidential transition, or creation/dissolution of ministries. The cohabitation dynamic between President Nawrocki and PM Tusk is a particularly volatile factor that may change the relative importance of presidential vs. PM communications.*
