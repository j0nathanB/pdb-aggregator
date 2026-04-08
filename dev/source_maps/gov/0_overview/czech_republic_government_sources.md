# Official Government Sources Supplement: CZECH REPUBLIC

**Primary language of political discourse: Czech**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Czech Republic (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for the Czech Republic. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Czech government digital infrastructure is decentralized — unlike Mexico's unified `gob.mx` platform, each Czech ministry and institution maintains its own independent website, typically under the `.gov.cz` domain (e.g., `vlada.gov.cz`, `mzv.gov.cz`, `mo.gov.cz`, `mf.gov.cz`). This means there is no single extraction pattern; each source requires its own scraper configuration. However, several sites share a common CMS (typically WordPress or custom PHP) and most publish in both Czech and English, with Czech-language content being substantially more complete. RSS availability is inconsistent: the Czech National Bank (CNB), the Senate, the Presidential Office (hrad.cz), and the Government Office (vlada.gov.cz) provide functional RSS feeds, while most ministries do not. The official gazette transitioned to a digital-first platform (e-Sbírka) in January 2024, which is still maturing through 2026.

---

## 1. OFFICIAL GOVERNMENT SOURCES: CZECH REPUBLIC

### 1.1 Head of Government — Office of the Government (Úřad vlády) and Presidential Office (Hrad)

#### 1.1a Office of the Government of the Czech Republic (Úřad vlády České republiky)

| Field | Detail |
|---|---|
| **Institution** | Úřad vlády České republiky (Office of the Government) |
| **Domain** | `vlada.gov.cz` |
| **Entry Point URL** | `https://vlada.gov.cz/scripts/detail.php?pgid=215` (Tiskové zprávy — press releases, Czech) / `https://vlada.gov.cz/en/media-centrum/aktualne/` (English press advisories) |
| **RSS/Atom Feed** | **Yes.** Czech: `https://www.vlada.cz/cs/urad/RSS/rss.xml` — English: `https://www.vlada.cz/en/rss.xml` |
| **Language** | Czech (primary); English (partial — major announcements, foreign-policy items) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints, Economic & technological statecraft |
| **Publication Frequency** | Daily. Press releases (tiskové zprávy) issued for cabinet sessions (typically Wednesdays), PM bilateral meetings, EU Council mandates, and coalition policy announcements. Press conferences (tiskové konference) archived with video/transcript. |
| **Content Format** | HTML articles. Press conference transcripts in HTML. Some attached PDFs for formal government resolutions (usnesení vlády). Photo and video sections available. |
| **Extraction Method** | RSS feed polling (preferred). HTML scraping of press release listing page as fallback. Article URLs follow pattern `/scripts/detail.php?pgid=...` or `/cz/media-centrum/tiskove-zpravy/...`. |
| **Editorial Orientation** | Official government position. All content produced by the Government Communications Department (Odbor komunikace). Under PM Babiš (ANO), framing reflects coalition priorities — pragmatic EU engagement, defense spending commitments, economic competitiveness. |
| **Why This Source** | The single authoritative source for cabinet decisions, coalition agreement implementation, PM foreign-travel readouts, and government policy announcements. Cabinet session outcomes (usnesení vlády) published here are the definitive record of executive action. The site also hosts the National Security Council (BRS) page, making it the only public-facing window into BRS meeting outcomes. |
| **Access Notes** | No paywall, no authentication. The site redirects from `vlada.cz` to `vlada.gov.cz`. English section is functional but substantially less complete than Czech. No bot protection observed. |

**Additional entry points:**
- Government meetings (usnesení vlády): `https://vlada.gov.cz/cz/jednani-vlady/`
- Scheduled events: `https://vlada.gov.cz/scripts/detail.php?pgid=1304`
- Press conferences archive: `https://vlada.gov.cz/scripts/detail.php?pgid=1306`
- National Security Council (BRS): `https://vlada.gov.cz/en/ppov/brs/office-of-the-government-of-the-czech-republic-23851/`

#### 1.1b Presidential Office — Prague Castle (Kancelář prezidenta republiky)

| Field | Detail |
|---|---|
| **Institution** | Kancelář prezidenta republiky (Office of the President) |
| **Domain** | `hrad.cz` |
| **Entry Point URL** | `https://www.hrad.cz/en/for-media/press-releases` (English) / `https://www.hrad.cz/cs/pro-media/tiskove-zpravy` (Czech) |
| **RSS/Atom Feed** | **Yes.** RSS page at `https://www.hrad.cz/en/for-media/rss` — specific feed URLs available for press releases and speeches. [VERIFY exact feed XML URLs — page returned 403 on automated fetch] |
| **Language** | Czech (primary); English (comprehensive — most press releases published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Institutional engagement |
| **Publication Frequency** | 3-7 per week. Press releases for presidential foreign visits, bilateral meetings, ambassador credential ceremonies, military appointments, and constitutional-role statements. Higher frequency during foreign travel. |
| **Content Format** | HTML articles. Speeches published in full text. Photo gallery with high-resolution images. |
| **Extraction Method** | RSS feed polling (preferred, if feed URLs can be verified). HTML scraping of press release listing page. Paginated listing at `/en/for-media/press-releases/strana-{n}`. |
| **Editorial Orientation** | Official presidential position. Under President Petr Pavel (inaugurated March 2023), communications reflect a firmly pro-NATO, pro-EU, Atlanticist orientation. Pavel's military background (former NATO Military Committee chairman) produces unusually substantive defense and security communications. |
| **Why This Source** | The Czech president has constitutional authority over foreign affairs (receives ambassadors, represents the state internationally) and military affairs (commander-in-chief). Pavel is the most internationally engaged Czech president since Havel. His bilateral meeting readouts, security-policy speeches, and ambassador-reception communications are primary diplomatic-alignment indicators. The PM-President relationship (Babiš-Pavel tensions on EU/Russia policy) is itself a domestic-constraint signal. |
| **Access Notes** | No paywall. The site at `hrad.cz` is well-maintained. English section is comprehensive. RSS page exists but returned 403 on automated fetch — may require standard browser headers. |

**Additional entry points:**
- President's speeches: `https://www.hrad.cz/en/president-of-the-cr/current-president-of-the-cr/selected-speeches-and-interviews`
- President's diary/agenda: `https://www.hrad.cz/en/president-of-the-cr/current-president-of-the-cr/diary`

---

### 1.2 Foreign Ministry — Ministerstvo zahraničních věcí (MZV)

| Field | Detail |
|---|---|
| **Institution** | Ministerstvo zahraničních věcí České republiky (MZV) |
| **Domain** | `mzv.gov.cz` (redirects from `mzv.cz`) |
| **Entry Point URL** | `https://mzv.gov.cz/jnp/en/issues_and_press/press_releases/index.html` (English press releases) / `https://mzv.gov.cz/jnp/cz/informace_a_tisk/tiskove_zpravy/index.html` (Czech) |
| **RSS/Atom Feed** | **No active feeds.** RSS page exists at `https://mzv.gov.cz/jnp/en/rss.html` but explicitly states "Sorry, no active RSS channels for now." |
| **Language** | Czech (primary); English (comprehensive — most press releases and statements published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Press releases for ministerial meetings, bilateral/multilateral statements, MFA positions on international events, travel advisories. Speeches published under minister's section. |
| **Content Format** | HTML articles on custom CMS. Formal diplomatic statements and MFA concept documents sometimes in PDF. |
| **Extraction Method** | HTML scraping of press release listing page. Article URLs follow pattern `/jnp/en/issues_and_press/press_releases/{slug}.html`. Separate sections for press releases, MFA statements, and minister's speeches/articles. |
| **Editorial Orientation** | Official foreign-policy position. Under Foreign Minister Petr Macinka, communications reflect Czech transatlantic commitment, strong Ukraine support, EU institutional engagement, and human rights focus (UN Human Rights Council). |
| **Why This Source** | The only primary source for Czech formal diplomatic positions, treaty actions, ambassador appointments, multilateral voting positions, and bilateral meeting readouts. The MZV published the 2025 Foreign Policy Concept, the foundational strategic document for Czech external posture. Media coverage of Czech foreign policy is invariably derived from MZV communications. |
| **Access Notes** | No paywall. The domain redirects from `mzv.cz` to `mzv.gov.cz`. English section is unusually comprehensive for a non-Anglophone foreign ministry. No bot protection observed. Embassy-level press releases are published on individual embassy subdomains (e.g., `mzv.gov.cz/washington`). |

**Additional entry points:**
- MFA statements: `https://mzv.gov.cz/jnp/en/issues_and_press/mfa_statements/index.html`
- Minister's speeches and articles: `https://mzv.gov.cz/jnp/en/about_the_ministry/organization_of_the_ministry/minister/speeches_and_articles/index.html`
- Embassy-level communications (US): `https://mzv.gov.cz/washington`
- Foreign Policy Concept documents: accessible via issues_and_press section

---

### 1.3 Defense Ministry — Ministerstvo obrany (MO)

| Field | Detail |
|---|---|
| **Institution** | Ministerstvo obrany České republiky (MO) |
| **Domain** | `mo.gov.cz` |
| **Entry Point URL** | `https://www.mo.gov.cz/en/news` (English newsroom) / `https://www.mo.gov.cz/scripts/detail.php?pgid=194` (newsroom via script) |
| **RSS/Atom Feed** | None identified. No RSS links visible on the site. |
| **Language** | Czech (primary); English (partial — key announcements, minister statements, NATO-related items) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Communications cover ministerial meetings, NATO commitments, defense procurement, military exercises, force structure changes, bilateral military cooperation, and arms-export notifications. |
| **Content Format** | HTML articles. Photo gallery and video sections available. Strategic documents (White Paper on Defence, Security Strategy) in PDF. Defense budget data in the "Facts File" section. |
| **Extraction Method** | HTML scraping of news listing page. Article URLs follow pattern `/scripts/detail.php?pgid=...`. Video and photo archives at separate paths. |
| **Editorial Orientation** | Official defense-policy position. Under Minister Jaromír Zůna, communications emphasize NATO certification, defense-spending trajectory toward 2% GDP, military modernization (SPYDER air defense, CAESAR howitzers, F-35 consideration), and European defense cooperation. |
| **Why This Source** | Primary source for defense-budget data, procurement contracts, NATO deployment decisions, bilateral military cooperation agreements, military exercise participation, and arms-export notifications. The "Facts File" section provides structured defense-budget time series. Czech defense procurement is a key signal for NATO burden-sharing compliance and European defense-industrial cooperation. |
| **Access Notes** | No paywall. English pages available but less comprehensive than Czech. Social media presence on X (Twitter), Instagram, and YouTube for real-time operational updates. |

**Additional entry points:**
- Strategic documents: `https://www.mo.gov.cz/en/ministry-of-defence/strategy-and-doctrine/`
- Defense budget / Facts File: `https://www.mo.gov.cz/en/ministry-of-defence/facts-file/`
- Armed Forces / Chief of General Staff: `https://www.mo.gov.cz/en/armed-forces/`
- Foreign operations: `https://www.mo.gov.cz/en/armed-forces/foreign-operations/`

---

### 1.4 Parliament / Legislature — Parlament České republiky

#### 1.4a Poslanecká sněmovna (Chamber of Deputies)

| Field | Detail |
|---|---|
| **Institution** | Poslanecká sněmovna Parlamentu České republiky (Chamber of Deputies) |
| **Domain** | `psp.cz` / `pspen.psp.cz` (English) |
| **Entry Point URL** | `https://www.psp.cz/sqw/hp.sqw?k=90` (Média — media section) / `https://pspen.psp.cz/` (English portal) |
| **RSS/Atom Feed** | RSS subscription referenced in site footer ("Odběr RSS") but specific feed URLs not publicly documented. [VERIFY RSS — check `https://www.psp.cz/rss/` or similar paths] |
| **Language** | Czech (primary); English (limited — institutional information at `pspen.psp.cz`) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods (approximately September-July with recesses). Press releases (tiskové zprávy) from the Press Office (Tiskové středisko). Plenary session schedules and vote records published continuously. |
| **Content Format** | HTML. The site uses a legacy SQW (script) system for most content. Stenographic records (stenoprotokoly) of plenary sessions published in full text. Vote records in structured format. |
| **Extraction Method** | HTML scraping. The legacy URL structure (`/sqw/hp.sqw?k=...`) requires parameter-based navigation. Stenoprotokoly at `https://www.psp.cz/eknih/` (digital library). Vote records at `https://www.psp.cz/sqw/hlasy.sqw`. |
| **Editorial Orientation** | Institutional. Press releases reflect the Speaker's office (currently Tomio Okamura, SPD) and committee chairs. Committee hearing outputs reflect the composition of the committee majority. |
| **Why This Source** | Treaty ratifications, defense-budget votes, EU mandate approvals, and enabling legislation for executive policy originate in the Chamber. Committee hearings — particularly the Foreign Affairs Committee (Výbor pro zahraniční věci), Defense Committee (Výbor pro obranu), and European Affairs Committee (Výbor pro evropské záležitosti) — produce testimony from ministers and officials that no media outlet fully covers. Stenographic records are the only verbatim source for parliamentary debate. |
| **Access Notes** | No paywall. The site architecture is legacy (PHP/SQW scripts) but functional. The English portal at `pspen.psp.cz` provides institutional information but not press releases or stenographic records. Live broadcasts available at `pspen.psp.cz/live-broadcast/`. |

**Additional entry points:**
- Stenographic records: `https://www.psp.cz/eknih/`
- Vote records: `https://www.psp.cz/sqw/hlasy.sqw`
- Bills tracker: `https://www.psp.cz/sqw/sbirka.sqw`
- Live broadcast: `https://pspen.psp.cz/live-broadcast/`

#### 1.4b Senát (Senate)

| Field | Detail |
|---|---|
| **Institution** | Senát Parlamentu České republiky (Senate) |
| **Domain** | `senat.cz` |
| **Entry Point URL** | `https://www.senat.cz/informace/pro_media/index-eng.php` (media section, English) / `https://www.senat.cz/zpravodajstvi/zpravy.php` (press releases, Czech) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Press releases: `https://www.senat.cz/zpravodajstvi/zpravy_rss.php`. Senate events: `https://www.senat.cz/zpravodajstvi/akce_rss.php`. Video records: `https://www.senat.cz/zpravodajstvi/videa_rss.php`. Recently discussed bills: `https://www.senat.cz/dokumenty/posledni_projednavane_tisky_rss.php`. Enrolled bills: `https://www.senat.cz/dokumenty/zarazene_neprojednavane_tisky_rss.php`. Laws passed in third reading (PSP): `https://www.senat.cz/dokumenty/zakony_3_psp_rss.php` |
| **Language** | Czech (primary); English (institutional pages at `/index-eng.php` paths) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Regular during session periods. Press releases issued for plenary sessions, committee meetings, Senate President's activities, and international parliamentary diplomacy. Legislative RSS feeds update as bills move through the process. |
| **Content Format** | HTML (PHP-based site). Press releases in text format. Legislative documents linked in RSS feeds (up to 2 MB for bill-related feeds). |
| **Extraction Method** | RSS feed polling (preferred — best RSS infrastructure in Czech government). HTML scraping as fallback. |
| **Editorial Orientation** | Institutional. The Senate traditionally skews more pro-Western/liberal than the Chamber due to its electoral system (majority runoff). Senate President's communications reflect institutional positioning. |
| **Why This Source** | The Senate has constitutional veto power over international treaties, constitutional amendments, and electoral law. Its Foreign Affairs, Defence, and Security Committee reviews defense cooperation agreements and intelligence oversight matters. The Senate's legislative RSS feeds provide the most machine-readable tracking of Czech lawmaking across the entire government digital ecosystem. Senate leadership has historically been more hawkish on Russia/China than the executive. |
| **Access Notes** | No paywall. RSS feeds are well-maintained and the most comprehensive government RSS offering in Czechia. English content limited to institutional information. |

---

### 1.5 Official Gazette — Sbírka zákonů / e-Sbírka

| Field | Detail |
|---|---|
| **Institution** | Sbírka zákonů a mezinárodních smluv (Collection of Laws and International Treaties) — administered by the Ministry of the Interior |
| **Domain** | `e-sbirka.cz` (new digital platform) / `aplikace.mv.gov.cz/sbirka-zakonu/` (legacy) |
| **Entry Point URL** | `https://www.e-sbirka.cz/` (primary, launched January 2024) / `https://aplikace.mv.gov.cz/sbirka-zakonu/getall.aspx` (legacy archive) |
| **RSS/Atom Feed** | None identified on either platform. [VERIFY RSS on e-sbirka.cz — new platform may add feeds as it matures] |
| **Language** | Czech |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Sbírka zákonů is the constitutional publication vehicle for all laws, regulations, international treaties, and constitutional court decisions |
| **Publication Frequency** | Continuous. New issues (částky) published as legislation is enacted. Constitutional court decisions, government regulations, and ministerial decrees published on an ongoing basis. |
| **Content Format** | The e-Sbírka platform provides structured digital versions of legislation with fragment-level identifiers. The legacy system serves PDF copies of gazette issues. |
| **Extraction Method** | The e-Sbírka platform (`e-sbirka.cz`) provides a search interface with structured metadata. The legacy system at `aplikace.mv.gov.cz/sbirka-zakonu/` supports date-range queries. PDF extraction for legacy documents. The new platform's API/data structure is still stabilizing through January 2026. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, international treaty, or government regulation is legally binding until published in the Sbírka zákonů. This is the definitive, timestamped legal text. The e-Sbírka platform (launched January 2024, with e-Legislativa integration through January 2026) represents a major modernization — structured, searchable legislation replacing PDF-only gazette issues. |
| **Access Notes** | Both platforms are freely accessible. The e-Sbírka platform is still maturing: identifiers of individual fragments may change until January 15, 2026 as the e-Legislativa system completes its rollout. The legacy system at `aplikace.mv.gov.cz` remains the authoritative archive for pre-2024 legislation. The Chamber of Deputies also mirrors the Sbírka at `https://www.psp.cz/sqw/sbirka.sqw`. |

**Additional entry points:**
- Ministry of Interior e-Sbírka information page: `https://mv.gov.cz/clanek/esbirka-a-elegislativa.aspx`
- Legacy Sbírka zákonů (full archive): `https://aplikace.mv.gov.cz/sbirka-zakonu/getall.aspx`
- Chamber of Deputies mirror: `https://www.psp.cz/sqw/sbirka.sqw`

---

### 1.6 Finance Ministry — Ministerstvo financí (MF)

| Field | Detail |
|---|---|
| **Institution** | Ministerstvo financí České republiky (MF) |
| **Domain** | `mf.gov.cz` / `mfcr.cz` (legacy, still active) |
| **Entry Point URL** | `https://mf.gov.cz/en/about-ministry/media-room/news-and-press-releases` (English) / `https://www.mfcr.cz/cs/informacni-servis/tiskove-zpravy/` (Czech) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — check `https://mf.gov.cz/rss/` or similar paths] |
| **Language** | Czech (primary); English (comprehensive — major fiscal policy announcements, debt management strategy, budget documents published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Press releases for fiscal policy announcements, state budget execution reports, public debt operations, EU fund management, tax policy changes, and macroeconomic forecasts. |
| **Content Format** | HTML articles. Year-based archive structure (`/news-and-press-releases/2026/`, `/2025/`, etc.). PDF attachments for budget documents, fiscal outlook reports, and debt management strategy. |
| **Extraction Method** | HTML scraping of news listing page. Year-based URL structure enables targeted historical queries. Individual article URLs follow pattern `/en/about-ministry/media-room/news-and-press-releases/{year}/{slug-number}`. |
| **Editorial Orientation** | Official fiscal policy position. Technical, data-heavy communications. Under the Babiš government, emphasis on fiscal consolidation, EU fund absorption, social bond issuance (first Czech social government bonds issued October 2025), and economic competitiveness agenda. |
| **Why This Source** | Primary source for state budget execution, public debt data, fiscal forecasts, EU fund allocation/absorption, tax reform proposals, and the annual Funding and Debt Management Strategy. Essential for Economic & Technological Statecraft domain — MF communications are the raw data that Hospodářské noviny and economic analysts interpret. The Monitor portal provides granular public finance data. |
| **Access Notes** | No paywall. The site is transitioning from `mfcr.cz` to `mf.gov.cz` — both domains currently active. English section is comprehensive for a finance ministry. No bot protection observed. |

**Additional entry points:**
- State budget data: `https://monitor.statnipokladna.gov.cz/` (Monitor — public finance information portal)
- Macroeconomic forecast: published quarterly via press releases
- Funding and Debt Management Strategy: annual publication under fiscal policy section

---

### 1.7 Central Bank — Česká národní banka (ČNB)

| Field | Detail |
|---|---|
| **Institution** | Česká národní banka (ČNB / CNB — Czech National Bank) |
| **Domain** | `cnb.cz` |
| **Entry Point URL** | `https://www.cnb.cz/en/cnb-news/` (news archive) / `https://www.cnb.cz/en/public/media-service/` (media service hub) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Press releases: `https://www.cnb.cz/en/.content/rss-feed/rss-feed_tz.xml` (verified functional, valid RSS 2.0). CNB Blog: `https://www.cnb.cz/en/.content/rss-feed/rss-feed_00023.rss`. RSS hub page: `https://www.cnb.cz/en/general/rss/` |
| **Language** | Czech (primary); English (comprehensive — press releases, monetary policy decisions, financial stability reports, and governor's speeches all published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (Bank Board meetings on scheduled dates). Press releases: multiple per week (countercyclical buffer decisions, regulatory actions, statistical data commentary, research priorities). Financial Stability Report: biannual. Inflation Reports: quarterly. Governor's speeches: ad hoc. |
| **Content Format** | HTML for press releases and news. PDF for monetary policy minutes, Financial Stability Reports, Inflation Reports, and research papers. RSS feed delivers structured press release data. |
| **Extraction Method** | RSS feed polling for press releases (preferred — verified functional). HTML scraping of media service pages for governor speeches and statistical commentary. PDF download for formal reports. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Aleš Michl, the CNB has pursued monetary normalization, maintained the countercyclical capital buffer, and issued first crypto-asset service provider authorizations under EU MiCA regulation. Michl's communication style is more market-oriented than predecessors. |
| **Why This Source** | The CNB is the only source for authoritative monetary policy decisions, inflation commentary, financial stability assessments, and regulatory actions (including crypto-asset regulation). Its press release RSS feed is the most reliable machine-readable government data source in Czechia. The CNB's commentary on statistical data (inflation, GDP) provides the official institutional interpretation that all financial media cite. The CNB also maintains the ARAD statistical database and publishes comprehensive balance-of-payments data relevant to trade and investment monitoring. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained and verified functional. Email subscription service available. English site is comprehensive. The CNB calendar at `/en/cnb-news/calendar/` provides advance scheduling for publications and events. |

**Key RSS feed URLs:**
| Feed | URL | Status |
|---|---|---|
| Press releases (EN) | `https://www.cnb.cz/en/.content/rss-feed/rss-feed_tz.xml` | Verified |
| CNB Blog (EN) | `https://www.cnb.cz/en/.content/rss-feed/rss-feed_00023.rss` | Verified |
| Press releases (CS) | `https://www.cnb.cz/cs/.content/rss-feed/rss-feed_tz.xml` | [VERIFY URL] |

**Additional entry points:**
- Monetary policy decisions: `https://www.cnb.cz/en/monetary-policy/bank-board-decisions/`
- Governor's speeches and interviews: `https://www.cnb.cz/en/public/media-service/governors-speeches-and-interviews/`
- CNB commentary on inflation/GDP: `https://www.cnb.cz/en/public/media-service/the-cnb-comments-on-the-statistical-data-on-inflation-and-gdp/`
- CNB calendar: `https://www.cnb.cz/en/cnb-news/calendar/`
- ARAD statistical database: `https://www.cnb.cz/arad/`

---

### 1.8 Trade / Industry — Ministerstvo průmyslu a obchodu (MPO)

| Field | Detail |
|---|---|
| **Institution** | Ministerstvo průmyslu a obchodu České republiky (MPO — Ministry of Industry and Trade) |
| **Domain** | `mpo.gov.cz` |
| **Entry Point URL** | `https://mpo.gov.cz/en/guidepost/for-the-media/press-releases/` (English) / `https://mpo.gov.cz/cz/rozcestnik/pro-media/tiskove-zpravy/` (Czech) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Czech (primary); English (partial — select press releases translated) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-5 per week. Communications cover trade policy, industrial strategy, energy policy, AI regulation, EU single market issues, science/research policy (transferred to MPO from March 2026), and FDI promotion. |
| **Content Format** | HTML articles. Policy documents and impact assessments in PDF. |
| **Extraction Method** | HTML scraping of press release listing page. Individual article URLs follow pattern `/en/guidepost/for-the-media/press-releases/{slug}-{number}/`. |
| **Editorial Orientation** | Official trade and industrial policy position. Under Minister Karel Havlíček (appointed December 2025), communications emphasize affordable energy, economic growth, investment support, reduced administrative burden, and Czech industrial competitiveness. The ministry absorbed science, research, and space activities agendas as of March 1, 2026. |
| **Why This Source** | Primary source for trade policy announcements, EU single market positions, energy policy (including pricing and supply diversification), industrial strategy, investment screening decisions, export controls, and dual-use technology regulation. The MPO's absorption of science/research/space agendas in 2026 makes it an increasingly important source for technological statecraft. Czech trade policy positions (particularly on China, Russia sanctions compliance, and EU trade defense) are first articulated here. |
| **Access Notes** | No paywall. English section functional but less complete than Czech. No bot protection observed. The MPO also prepared the Czech draft AI law (in line with EU AI Act implementation). |

**Additional entry points:**
- Energy policy section: `https://mpo.gov.cz/en/energy/`
- Trade policy section: `https://mpo.gov.cz/en/foreign-trade/`
- AI legislation: referenced in press releases (2025-2026)

---

### 1.9 Intelligence / National Security — BIS, ÚZSI, VZ, NÚKIB

#### 1.9a Bezpečnostní informační služba (BIS — Security Information Service)

| Field | Detail |
|---|---|
| **Institution** | Bezpečnostní informační služba (BIS — Security Information Service, domestic intelligence) |
| **Domain** | `bis.cz` |
| **Entry Point URL** | `https://www.bis.cz/en/` (English) / `https://www.bis.cz/` (Czech) |
| **RSS/Atom Feed** | None available. |
| **Language** | Czech (primary); English (comprehensive — annual reports and key institutional pages published bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Annual reports: 1 per year (typically published mid-year for the previous calendar year; 2024 report published July 2025). Ad hoc press releases: rare (1-3 per year for major events — e.g., Vrbětice expulsions, espionage arrests). |
| **Content Format** | Annual reports in PDF and HTML. No regular press release feed. |
| **Extraction Method** | Periodic check of `/annual-reports/` page for new annual report publication. Monitor main page for rare press statements. |
| **Editorial Orientation** | Intelligence-community institutional communication. Annual reports are carefully calibrated assessments of threat landscape. BIS has been consistently hawkish on Russian and Chinese intelligence threats under successive directors. |
| **Why This Source** | BIS annual reports are the single most important public intelligence product in Czechia. They provide authoritative assessments of Russian espionage, Chinese influence operations, proliferation risks, terrorism threats, and domestic extremism. The 2024 annual report covers Russian intelligence activities post-Vrbětice, Chinese tech-sector penetration, and hybrid-warfare threats. These reports set the analytical baseline for Czech security discourse and are widely cited by think tanks (European Values, AMO) and media (iROZHLAS, Respekt). |
| **Access Notes** | No paywall. The website is primarily institutional/informational — no news section, no RSS. Annual reports available at `https://www.bis.cz/annual-reports/`. Contact: info@bis.cz, +420 235 521 400. Social media: X (Twitter), Instagram. |

#### 1.9b Úřad pro zahraniční styky a informace (ÚZSI — Office for Foreign Relations and Information)

| Field | Detail |
|---|---|
| **Institution** | Úřad pro zahraniční styky a informace (ÚZSI — foreign intelligence service) |
| **Domain** | `uzsi.cz` |
| **Entry Point URL** | `https://www.uzsi.cz/en/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Czech; English (basic institutional information) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible. ÚZSI publishes virtually no public communications beyond basic institutional information. No annual reports are publicly released. |
| **Content Format** | Minimal HTML. |
| **Extraction Method** | Periodic check for any new content. Flag any publication as a high-priority anomaly. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. ÚZSI is the Czech foreign intelligence service, subordinate to the Ministry of the Interior. Unlike BIS, it does not publish annual reports. Any public statement from ÚZSI is inherently newsworthy due to rarity. The real intelligence signal from ÚZSI comes through: (a) BIS annual reports that reference ÚZSI coordination, (b) parliamentary intelligence oversight committee proceedings, (c) leaks to investigative media (Respekt, Deník N). |
| **Access Notes** | Minimal website. No practical monitoring value beyond anomaly detection. |

#### 1.9c Vojenské zpravodajství (VZ — Military Intelligence)

| Field | Detail |
|---|---|
| **Institution** | Vojenské zpravodajství (VZ — Military Intelligence) |
| **Domain** | `vzcr.gov.cz` / `vzcr.cz` |
| **Entry Point URL** | `https://vzcr.gov.cz/en` |
| **RSS/Atom Feed** | None available. |
| **Language** | Czech; English (institutional pages) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Rare. Annual reports published periodically. Institutional information on HUMINT, SIGINT, IMINT, OSINT capabilities. Cyber defence section updated occasionally. |
| **Content Format** | HTML. Annual reports in PDF. |
| **Extraction Method** | Periodic check for new publications or annual reports. |
| **Editorial Orientation** | Military intelligence institutional communication. Focus on cyber defence (CZE SATCEN — Satellite Center founded 2018), international cooperation, and threat assessment. |
| **Why This Source** | VZ is responsible for military intelligence including satellite imagery (CZE SATCEN), signals intelligence, and cyber defence. Annual reports — when published — provide assessments of military threats relevant to NATO planning. VZ's cyber defence reporting complements NÚKIB's civilian cybersecurity focus. |
| **Access Notes** | Minimal website. Both `vzcr.gov.cz` and `vzcr.cz` domains active. |

#### 1.9d Národní úřad pro kybernetickou a informační bezpečnost (NÚKIB — National Cyber and Information Security Agency)

| Field | Detail |
|---|---|
| **Institution** | Národní úřad pro kybernetickou a informační bezpečnost (NÚKIB) |
| **Domain** | `nukib.gov.cz` |
| **Entry Point URL** | `https://nukib.gov.cz/en/infoservis-en/news/` (English news) / `https://nukib.gov.cz/cs/infoservis/aktuality/` (Czech) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Czech (primary); English (comprehensive — news section, publications, reports all available bilingually) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | Multiple per month. News items for cybersecurity advisories, international conferences (Prague Cyber Security Conference), supply-chain risk assessments, regulatory actions (5G security, vendor restrictions), and NATO cyber cooperation. Publications and reports section updated periodically. |
| **Content Format** | HTML news articles. Reports and publications in PDF. Individual article URLs follow pattern `/en/infoservis-en/news/{ID}-{slug}`. |
| **Extraction Method** | HTML scraping of news listing page. Chronological listing with ID-based URLs enables efficient polling for new content. |
| **Editorial Orientation** | Technical/security-focused agency communication. NÚKIB has taken publicly hawkish positions on Chinese ICT supply-chain risks (Huawei/ZTE warnings) and Russian cyber threats. The agency co-hosts the Prague Cyber Security Conference with MZV, reflecting its foreign-policy relevance. |
| **Why This Source** | NÚKIB is the most publicly communicative Czech security institution. It issued the 2018 warning against Huawei/ZTE (the first in Europe), hosts the annual Prague Cyber Security Conference (400+ participants from 40+ countries in 2026), and coordinates with NATO on cyber defense. Its supply-chain security assessments directly affect technology procurement decisions across government and critical infrastructure. The 2026 National Cyber Security Strategy provides the strategic framework for Czech cyber posture. |
| **Access Notes** | No paywall. English section is comprehensive. No bot protection observed. The NÚKIB also hosts the Prague Cyber Security Conference jointly with MZV. |

**Additional entry points:**
- Publications and reports: `https://nukib.gov.cz/en/infoservis-en/publications-reports/`
- Cyber security section: `https://nukib.gov.cz/en/cyber-security/`
- Research NÚKIB: `https://nukib.gov.cz/en/cyber-security/research-nukib/`

---

### 1.10 Country-Specific Institutions

#### 1.10a Český statistický úřad (ČSÚ / CZSO — Czech Statistical Office)

| Field | Detail |
|---|---|
| **Institution** | Český statistický úřad (CZSO — Czech Statistical Office) |
| **Domain** | `csu.gov.cz` / `czso.cz` |
| **Entry Point URL** | `https://csu.gov.cz/news_releases_archive` (English news releases) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** News: `https://csu.gov.cz/rss/statistika/aktuality?jazyk=EN`. News Releases: `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=RI&jazyk=EN`. Analyses/Commentaries: `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Ana&jazyk=EN`. Press Releases: `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=TZ&jazyk=EN`. Publications: `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Pub&jazyk=EN` |
| **Language** | Czech (primary); English (comprehensive — news releases, statistical publications) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Scheduled. All news releases issued on pre-announced dates at 9:00 AM. GDP, inflation, trade balance, industrial production, unemployment, and demographic data published on a fixed calendar. |
| **Content Format** | HTML with structured data tables. PDF publications. RSS feeds deliver structured metadata. |
| **Extraction Method** | RSS feed polling (preferred — multiple well-structured feeds available). HTML scraping of news releases archive as fallback. |
| **Editorial Orientation** | Technically independent statistical authority. Data-driven, politically neutral by institutional mandate. |
| **Why This Source** | CZSO is the only authoritative source for macroeconomic data (GDP, inflation, trade balance, industrial production, employment) that the CNB, MF, and all economic media rely upon. Its scheduled release calendar enables predictive monitoring. The election-results portal at `volby.cz` (operated by CZSO) is the sole authoritative source for Czech electoral data. CZSO RSS feeds are among the best machine-readable government data sources in Czechia. |
| **Access Notes** | No paywall. RSS feeds are well-maintained. English site comprehensive. No bot protection. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| News (EN) | `https://csu.gov.cz/rss/statistika/aktuality?jazyk=EN` |
| News Releases (EN) | `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=RI&jazyk=EN` |
| Press Releases (EN) | `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=TZ&jazyk=EN` |
| Analyses (EN) | `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Ana&jazyk=EN` |
| Publications (EN) | `https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Pub&jazyk=EN` |

**Additional entry points:**
- Election results: `https://www.volby.cz/index_en.htm`
- Release calendar: published annually at CZSO

#### 1.10b ČEZ Group (State Energy Utility)

| Field | Detail |
|---|---|
| **Institution** | ČEZ, a. s. (majority state-owned energy utility) |
| **Domain** | `cez.cz` |
| **Entry Point URL** | `https://www.cez.cz/en/media/press-releases` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Czech (primary); English (investor relations and major press releases) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 2-5 per week. Press releases cover electricity generation, nuclear energy (Dukovany expansion, Temelín), renewable energy, financial results, grid infrastructure, and regional energy supply. |
| **Content Format** | HTML press releases. PDF for financial reports and investor presentations. |
| **Extraction Method** | HTML scraping of press release listing page. |
| **Editorial Orientation** | State enterprise communication (Czech state holds ~70% stake). Emphasis on energy security, nuclear expansion, decarbonization, and grid modernization. ČEZ communications reflect government energy strategy. |
| **Why This Source** | ČEZ is the dominant energy company in Central Europe and a strategic state asset. The Dukovany nuclear expansion (selecting contractor, massive capital investment) is Czechia's largest infrastructure project and has geopolitical implications (exclusion of Russian/Chinese bidders). ČEZ's financial health, generation mix, and investment plans directly affect Czech energy security and climate commitments. |
| **Access Notes** | Investor relations section at `cez.cz` provides English-language financial data. The company is publicly traded (Prague Stock Exchange, Warsaw Stock Exchange). |

#### 1.10c Národní bezpečnostní úřad (NBÚ — National Security Authority)

| Field | Detail |
|---|---|
| **Institution** | Národní bezpečnostní úřad (NBÚ — National Security Authority) |
| **Domain** | `nbu.gov.cz` |
| **Entry Point URL** | `https://www.nbu.gov.cz/en/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Czech (primary); English (institutional pages) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Low. Annual report on activities. Ad hoc announcements on security clearance policy, classified information protection, and personnel security. |
| **Content Format** | HTML. Annual reports in PDF. |
| **Extraction Method** | Periodic check for new publications. |
| **Editorial Orientation** | Security authority institutional communication. Technical focus on personnel security, industrial security, and classified information protection. |
| **Why This Source** | NBÚ administers security clearances for government officials and defense-industry personnel, and manages the Czech Republic's participation in NATO/EU classified information systems. Changes to clearance policies, security incidents involving classified information, or denial of clearances to political figures (historically a politically significant event in Czech politics) are signaled here. |
| **Access Notes** | Minimal public-facing content. Low monitoring priority. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Independent Infrastructure |
|---|---|---|---|---|---|---|---|
| 1a | Úřad vlády (Government Office) | `vlada.gov.cz/scripts/detail.php?pgid=215` | **Yes** (CS + EN) | P1 | HTML | Daily | Yes |
| 1b | Hrad (Presidential Office) | `hrad.cz/en/for-media/press-releases` | **Yes** [VERIFY feed URLs] | P1 | HTML | 3-7/week | Yes |
| 2 | MZV (Foreign Ministry) | `mzv.gov.cz/jnp/en/issues_and_press/press_releases/` | No (page says "no active channels") | P1 | HTML | Daily | Yes |
| 3 | MO (Defense Ministry) | `mo.gov.cz/en/news` | No | P1 | HTML | 3-7/week | Yes |
| 4a | Poslanecká sněmovna (Chamber) | `psp.cz/sqw/hp.sqw?k=90` | [VERIFY] | P2 | HTML | Daily (session) | Yes |
| 4b | Senát (Senate) | `senat.cz/zpravodajstvi/zpravy.php` | **Yes** (6 feeds) | P2 | HTML | Regular (session) | Yes |
| 5 | Sbírka zákonů / e-Sbírka | `e-sbirka.cz` | No | P2 | HTML/PDF | Continuous | Yes |
| 6 | MF (Finance Ministry) | `mf.gov.cz/en/.../news-and-press-releases` | No | P2 | HTML/PDF | 3-5/week | Yes |
| 7 | ČNB (Central Bank) | `cnb.cz/en/cnb-news/` | **Yes** (verified) | P2 | HTML/PDF/RSS | Variable | Yes |
| 8 | MPO (Industry & Trade) | `mpo.gov.cz/en/.../press-releases/` | No | P2 | HTML | 2-5/week | Yes |
| 9a | BIS (Domestic Intel) | `bis.cz/annual-reports/` | No | P2 | PDF | Annual | Yes |
| 9b | ÚZSI (Foreign Intel) | `uzsi.cz/en/` | No | P2 | Minimal | Negligible | Yes |
| 9c | VZ (Military Intel) | `vzcr.gov.cz/en` | No | P2 | HTML/PDF | Rare | Yes |
| 9d | NÚKIB (Cyber Security) | `nukib.gov.cz/en/infoservis-en/news/` | No | P2 | HTML/PDF | Multiple/month | Yes |
| 10a | CZSO (Statistical Office) | `csu.gov.cz/news_releases_archive` | **Yes** (5 feeds) | P2 | HTML/RSS | Scheduled | Yes |
| 10b | ČEZ (Energy Utility) | `cez.cz/en/media/press-releases` | [VERIFY] | P2 | HTML/PDF | 2-5/week | Yes |
| 10c | NBÚ (Security Authority) | `nbu.gov.cz/en/` | No | P2 | HTML/PDF | Low | Yes |

---

## 3. MONITORING CONFIGURATION

```yaml
# Czech Republic Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/cz.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: cz_vlada
    name: Úřad vlády České republiky (Government Office)
    domain: vlada.gov.cz
    entry_url: "https://vlada.gov.cz/scripts/detail.php?pgid=215"
    rss_feed:
      czech: "https://www.vlada.cz/cs/urad/RSS/rss.xml"
      english: "https://www.vlada.cz/en/rss.xml"
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "Cabinet sessions typically Wednesdays. BRS (National Security Council) page hosted here. RSS feeds available in both CS and EN."

  - id: cz_hrad
    name: Kancelář prezidenta republiky (Presidential Office)
    domain: hrad.cz
    entry_url: "https://www.hrad.cz/en/for-media/press-releases"
    rss_feed: "https://www.hrad.cz/en/for-media/rss"  # [VERIFY exact XML feed URL - RSS page returned 403 on automated fetch]
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - institutional_engagement
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 2
    notes: "President Pavel's bilateral meeting readouts and security speeches are high-value diplomatic alignment signals. RSS may require browser-standard headers."

  - id: cz_mzv
    name: Ministerstvo zahraničních věcí (MZV — Foreign Ministry)
    domain: mzv.gov.cz
    entry_url: "https://mzv.gov.cz/jnp/en/issues_and_press/press_releases/index.html"
    rss_feed: null  # RSS page exists but states "no active RSS channels"
    language: cs
    language_secondary: en
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
    notes: "Redirects from mzv.cz to mzv.gov.cz. Separate sections for press releases, MFA statements, and minister speeches. Embassy-level releases on per-country subdomains."

  - id: cz_mo
    name: Ministerstvo obrany (MO — Defense Ministry)
    domain: mo.gov.cz
    entry_url: "https://www.mo.gov.cz/en/news"
    rss_feed: null
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "Defense budget data in Facts File section. NATO certification, procurement, and deployment communications."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: cz_psp
    name: Poslanecká sněmovna (Chamber of Deputies)
    domain: psp.cz
    entry_url: "https://www.psp.cz/sqw/hp.sqw?k=90"
    rss_feed: null  # [VERIFY - RSS referenced in footer but URL unknown]
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Legacy SQW script system. Stenoprotokoly at /eknih/. Vote records at /sqw/hlasy.sqw. Speaker is Okamura (SPD)."

  - id: cz_senat
    name: Senát Parlamentu ČR (Senate)
    domain: senat.cz
    entry_url: "https://www.senat.cz/zpravodajstvi/zpravy.php"
    rss_feed:
      press_releases: "https://www.senat.cz/zpravodajstvi/zpravy_rss.php"
      events: "https://www.senat.cz/zpravodajstvi/akce_rss.php"
      videos: "https://www.senat.cz/zpravodajstvi/videa_rss.php"
      recently_discussed_bills: "https://www.senat.cz/dokumenty/posledni_projednavane_tisky_rss.php"
      enrolled_bills: "https://www.senat.cz/dokumenty/zarazene_neprojednavane_tisky_rss.php"
      laws_passed_third_reading: "https://www.senat.cz/dokumenty/zakony_3_psp_rss.php"
    language: cs
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: regular_session
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Best RSS infrastructure in Czech government. 6 separate feeds covering press, events, video, and legislative tracking. Treaty ratification and defense committee oversight."

  - id: cz_esbirka
    name: Sbírka zákonů / e-Sbírka (Official Gazette)
    domain: e-sbirka.cz
    entry_url: "https://www.e-sbirka.cz/"
    rss_feed: null
    language: cs
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: continuous
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "New digital platform launched Jan 2024, still maturing. Legacy archive at aplikace.mv.gov.cz/sbirka-zakonu/. Fragment IDs may change until Jan 2026."

  - id: cz_mf
    name: Ministerstvo financí (MF — Finance Ministry)
    domain: mf.gov.cz
    entry_url: "https://mf.gov.cz/en/about-ministry/media-room/news-and-press-releases"
    rss_feed: null  # [VERIFY]
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Transitioning from mfcr.cz to mf.gov.cz. Year-based archive structure. Monitor portal at monitor.statnipokladna.gov.cz for public finance data."

  - id: cz_cnb
    name: Česká národní banka (ČNB — Czech National Bank)
    domain: cnb.cz
    entry_url: "https://www.cnb.cz/en/cnb-news/"
    rss_feed:
      press_releases_en: "https://www.cnb.cz/en/.content/rss-feed/rss-feed_tz.xml"
      cnb_blog_en: "https://www.cnb.cz/en/.content/rss-feed/rss-feed_00023.rss"
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Press release RSS verified functional (RSS 2.0). Monetary policy decisions 8x/year. Calendar at /en/cnb-news/calendar/. Best machine-readable government source in CZ alongside CZSO."

  - id: cz_mpo
    name: Ministerstvo průmyslu a obchodu (MPO — Industry & Trade)
    domain: mpo.gov.cz
    entry_url: "https://mpo.gov.cz/en/guidepost/for-the-media/press-releases/"
    rss_feed: null  # [VERIFY]
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Absorbed science/research/space agendas from March 2026. Energy policy, trade, AI regulation."

  - id: cz_bis
    name: Bezpečnostní informační služba (BIS — Domestic Intelligence)
    domain: bis.cz
    entry_url: "https://www.bis.cz/annual-reports/"
    rss_feed: null
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: annual
    content_format: pdf
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Annual report is the single most important public intelligence product in CZ. Published mid-year for previous calendar year. Flag any new publication as high-priority."

  - id: cz_uzsi
    name: Úřad pro zahraniční styky a informace (ÚZSI — Foreign Intelligence)
    domain: uzsi.cz
    entry_url: "https://www.uzsi.cz/en/"
    rss_feed: null
    language: cs
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 720  # monthly
    notes: "Effectively silent agency. No annual reports published. Any publication is an anomaly worth flagging."

  - id: cz_vz
    name: Vojenské zpravodajství (VZ — Military Intelligence)
    domain: vzcr.gov.cz
    entry_url: "https://vzcr.gov.cz/en"
    rss_feed: null
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: rare
    content_format: html_pdf_mixed
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Also accessible at vzcr.cz. CZE SATCEN satellite center. Cyber defence section. Periodic annual reports."

  - id: cz_nukib
    name: Národní úřad pro kybernetickou a informační bezpečnost (NÚKIB)
    domain: nukib.gov.cz
    entry_url: "https://nukib.gov.cz/en/infoservis-en/news/"
    rss_feed: null  # [VERIFY]
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "multiple_per_month"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Most communicative Czech security institution. Prague Cyber Security Conference host. Supply-chain security assessments (Huawei/ZTE). Article URLs use numeric IDs for efficient change detection."

  - id: cz_czso
    name: Český statistický úřad (CZSO — Statistical Office)
    domain: csu.gov.cz
    entry_url: "https://csu.gov.cz/news_releases_archive"
    rss_feed:
      news_en: "https://csu.gov.cz/rss/statistika/aktuality?jazyk=EN"
      news_releases_en: "https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=RI&jazyk=EN"
      press_releases_en: "https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=TZ&jazyk=EN"
      analyses_en: "https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Ana&jazyk=EN"
      publications_en: "https://csu.gov.cz/rss/produkty?kodVlastnostiVystupu=Pub&jazyk=EN"
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: scheduled
    content_format: html_rss_mixed
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "All releases at pre-announced dates at 9:00 AM. 5 separate RSS feeds. Election results at volby.cz. Best RSS alongside CNB."

  - id: cz_cez
    name: ČEZ Group (State Energy Utility)
    domain: cez.cz
    entry_url: "https://www.cez.cz/en/media/press-releases"  # [VERIFY URL]
    rss_feed: null  # [VERIFY]
    language: cs
    language_secondary: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "2-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "~70% state-owned. Dukovany nuclear expansion is CZ's largest infrastructure project. Publicly traded (PSE, WSE)."

  - id: cz_nbu
    name: Národní bezpečnostní úřad (NBÚ — National Security Authority)
    domain: nbu.gov.cz
    entry_url: "https://www.nbu.gov.cz/en/"
    rss_feed: null
    language: cs
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: low
    content_format: html_pdf_mixed
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Security clearances and classified information protection. Low monitoring value except for clearance-related political events."
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Czech government communications are generally more transparent than many post-communist peers but remain systematically optimistic and framing-conscious. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage and opposition response.

- **Vlada.gov.cz (Government Office)**: Cross-reference cabinet decisions (usnesení vlády) against same-day reporting in Seznam Zprávy and iROZHLAS. Government press releases omit coalition tensions and dissenting ministerial views — Deník N and Respekt provide the coalition-dynamics layer that official communications strip out. When the government issues a press release on an EU Council position, compare with EUROPEUM's policy briefs for analytical depth on what the Czech position actually means in Brussels context.

- **Hrad.cz (Presidential Office)**: President Pavel's communications are substantive on security/defense but reflect his personal transatlantic orientation. Cross-reference with vlada.gov.cz to detect PM-President divergence — when Pavel and Babiš issue separate statements on the same issue (e.g., Ukraine aid, EU defense integration), the framing gap is itself a signal. Radio Prague International provides English-language synthesis of the presidential-governmental dynamic.

- **MZV (Foreign Ministry)**: Diplomatic comunicados should be triangulated with CT24 (public broadcaster, live coverage of MZV pressers), Deník N (analytical foreign-policy coverage), and AMO's "Agenda for Czech Foreign Policy" (annual strategic assessment). When MZV and IIR (the MFA-linked think tank) framing diverge, it signals internal policy debate within the foreign-policy establishment.

- **MO (Defense Ministry)**: Defense procurement announcements report decisions but not the political negotiations that shaped them. Cross-reference with CZDEFENCE (defense-trade press, technical detail), Respekt (investigative, procurement controversies), and Hospodářské noviny (budget/fiscal implications). The MO "Facts File" defense-budget data should be compared against MF fiscal data for consistency.

- **ČNB (Central Bank)**: Monetary policy decisions are technically rigorous and the least politically distorted government source. Cross-reference with Hospodářské noviny for market interpretation and domestic economic-policy debate. The ČNB's inflation/GDP commentary should be compared against CZSO's raw statistical releases to detect any interpretive framing choices.

- **BIS (Annual Reports)**: BIS annual reports are carefully calibrated — they reveal what the intelligence community wants the public and political class to know. Cross-reference with European Values Center for Security Policy (hawkish interpretation of Russian/Chinese threats), Respekt and iROZHLAS (investigative follow-up on BIS findings), and HlídacíPes (Vrbětice, foreign-influence investigations).

- **NÚKIB**: Cybersecurity advisories and supply-chain assessments are technically grounded but reflect NÚKIB's institutional position favoring vendor diversification away from Chinese suppliers. Cross-reference with MPO (industrial/trade perspective) and Hospodářské noviny (business impact analysis).

**4.2 The decentralized infrastructure effect**

Unlike Mexico's centralized gob.mx platform, Czech government sources operate on entirely independent infrastructure. Every ministry, agency, and institution maintains its own website with its own CMS, URL structure, and publication workflow. This means:
- No single point of failure — outage at one institution does not affect others
- No shared extraction pattern — each source requires its own scraper configuration
- No centralized content control — publication timing is institution-specific, not subject to central approval
- Higher maintenance burden — template changes at any single institution require scraper updates

The trade-off favors resilience and editorial independence at the cost of extraction complexity.

**4.3 The intelligence community silence gradient**

Czech intelligence agencies exhibit a clear gradient of public communication:
1. **NÚKIB** (most communicative): Regular news, conferences, reports, policy advisories
2. **BIS** (annual report only): One high-value publication per year, rare ad hoc statements
3. **VZ** (periodic): Occasional annual reports, institutional information
4. **ÚZSI** (effectively silent): No public communications beyond minimal institutional presence

This gradient means intelligence-relevant signals surface through different channels for each agency. For BIS, the annual report is the primary official channel, supplemented by leaks to Respekt and iROZHLAS. For ÚZSI, there is no official channel — signals come exclusively through parliamentary oversight proceedings and investigative journalism. For NÚKIB, the official channel is the primary signal source. The pipeline should calibrate polling frequency accordingly.

**4.4 The Babiš-ownership factor**

PM Babiš's return to office (late 2025) and his complex relationship with the MAFRA media group (sold from Agrofert in 2023 to Kaprain Group, but Agrofert reacquired by Babiš in October 2025 and placed in a new trust) creates a structural interpretive challenge. Government communications must be read against the knowledge that MAFRA outlets (iDNES.cz, MF DNES, Lidové noviny) — excluded from the Layer 1 media map for reliability reasons — may amplify or soften government messaging. The pipeline should treat government-MAFRA framing alignment as a signal of coordinated communication strategy rather than independent confirmation.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Architecture — Per-Source Scraper Configuration

Unlike Mexico's gob.mx platform, Czech government sources require individual scraper modules. However, several sources share characteristics that enable some configuration grouping:

- **PHP/script-based sites** (vlada.gov.cz, psp.cz, mo.gov.cz): URL structures use query parameters (`/scripts/detail.php?pgid=...`, `/sqw/hp.sqw?k=...`). Pagination via query parameters. Standard HTML extraction.
- **Custom CMS sites** (mzv.gov.cz, mf.gov.cz, mpo.gov.cz): Clean URL slugs (`/jnp/en/issues_and_press/press_releases/{slug}.html`). Standard HTML extraction.
- **RSS-enabled sites** (vlada.gov.cz, cnb.cz, senat.cz, csu.gov.cz, hrad.cz): Use RSS polling as primary extraction method. HTML scraping as fallback.
- **Institutional/minimal sites** (bis.cz, uzsi.cz, vzcr.gov.cz, nbu.gov.cz): Periodic checks for any new content. Flag any new publication as anomaly.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Four government institutions provide functional RSS feeds, representing the automation-ready tier:

1. **ČNB (Czech National Bank)**: Press releases RSS (verified functional, RSS 2.0). CNB Blog RSS. English-language feeds. The most reliable machine-readable government source.

2. **Senát (Senate)**: Six separate RSS feeds covering press releases, events, videos, and three legislative-tracking feeds. The most comprehensive RSS infrastructure in Czech government. Czech-language only.

3. **CZSO (Statistical Office)**: Five RSS feeds covering news, news releases, press releases, analyses, and publications. English-language feeds available. Scheduled publication times (9:00 AM) enable predictive polling.

4. **Vlada.gov.cz (Government Office)**: RSS feeds in Czech and English for government news. Feed URLs use the legacy `vlada.cz` domain (which redirects to `vlada.gov.cz`).

5. **Hrad.cz (Presidential Office)**: RSS page exists but specific feed URLs need verification (403 on automated fetch — may require browser-standard headers).

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Several sources publish substantial content in PDF:
- **BIS annual reports**: Multi-page PDF (50-100+ pages). Text-based, well-structured. Published once per year.
- **MF fiscal reports**: Budget execution, debt management strategy in PDF. Tables requiring extraction (tabula/camelot).
- **ČNB monetary policy minutes**: Multi-page PDF. Text-based, well-structured.
- **e-Sbírka/legacy Sbírka zákonů**: Legal texts in PDF (legacy system). The new e-Sbírka platform provides structured HTML.
- **MO strategic documents**: Defense White Paper, Security Strategy in PDF.

### 5.4 Language and Encoding

All government sources publish primarily in Czech. English availability varies significantly:
- **Comprehensive English**: ČNB, MZV, CZSO, Hrad.cz, BIS (annual reports), NÚKIB
- **Partial English**: vlada.gov.cz, MO, MF, MPO
- **Czech only or minimal English**: PSP, Senát, e-Sbírka, ÚZSI, VZ, NBÚ

All sites use UTF-8 encoding. The pipeline's Czech-language processing capability (cs language code in cz.yaml) is essential for comprehensive coverage. English-language feeds can supplement but not replace Czech-language monitoring.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A cabinet decision appears in vlada.gov.cz press releases, the Sbírka zákonů (as enacted), and relevant ministry press releases (MF, MO, MZV, MPO)
- Presidential statements on foreign visits appear in hrad.cz and MZV communications
- Defense procurement decisions appear in MO and vlada.gov.cz (cabinet approval)
- Intelligence-related policy appears in vlada.gov.cz (BRS meeting outcomes), BIS annual reports, and NÚKIB advisories
- Legislative actions appear in PSP records, Senát records, and the Sbírka zákonů

Implement content-hash deduplication. Use the originating institution as canonical: vlada.gov.cz for cabinet decisions, Sbírka zákonů for enacted legislation, the relevant ministry for sector-specific policy, and hrad.cz for presidential communications.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Vlada.gov.cz, MZV, Hrad.cz | Every 2 hours | Daily publication, policy-critical, diplomatic alignment signals |
| P1-Standard | MO | Every 4 hours | Slightly less frequent but high-priority when published |
| P2-Active | Senát, PSP, MF, ČNB, MPO, CZSO | Every 6 hours | Regular publishing schedule, RSS available for some |
| P2-Periodic | e-Sbírka, NÚKIB, ČEZ | Every 12 hours | Important but slower publication cycle |
| P2-Low | BIS, VZ, NBÚ | Weekly | Annual or rare publications; flag any new content as anomaly |
| P2-Minimal | ÚZSI | Monthly | Effectively silent; any publication is high-priority anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| vlada.gov.cz downtime | Government Office | Monitor ČTK (Czech News Agency) wire for government announcements. CTK typically carries government press releases within minutes. Government social media accounts on X. |
| MZV site outage | Foreign Ministry | Monitor MZV's X/Twitter account (@CzechMFA). Radio Prague International (`english.radio.cz`) covers MZV announcements in English. Embassy subdomains may remain accessible. |
| MO site outage | Defense Ministry | CZDEFENCE (`czdefence.com`) carries MO announcements. CTK wire. MO social media (X, Instagram, YouTube). |
| ČNB RSS feed failure | Central Bank | HTML scraping of `cnb.cz/en/cnb-news/` as fallback. Monetary policy decisions also carried immediately by CTK, Hospodářské noviny, and Reuters/Bloomberg. |
| Senát RSS feed failure | Senate | HTML scraping of `senat.cz/zpravodajstvi/zpravy.php`. Legislative tracking via SIL system at `sil.gobernacion.gob.mx` equivalent: `psp.cz/sqw/sbirka.sqw`. |
| e-Sbírka platform instability | Official Gazette | Legacy archive at `aplikace.mv.gov.cz/sbirka-zakonu/getall.aspx` remains operational. Chamber of Deputies mirror at `psp.cz/sqw/sbirka.sqw`. |
| hrad.cz RSS 403 errors | Presidential Office | HTML scraping of press release listing page. ČTK wire carries presidential communications. Radio Prague International provides English coverage. |
| Intelligence agency sites | BIS, ÚZSI, VZ | Given negligible publication frequency, downtime is indistinguishable from silence. Monitor CTK and investigative media (Respekt, iROZHLAS) for any intelligence-related announcements that would normally appear on agency sites. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of Czech government digital infrastructure, change in government administration, or creation/dissolution of government agencies. The e-Sbírka platform (launched January 2024) should be reassessed after its full stabilization, expected by mid-2026.*
