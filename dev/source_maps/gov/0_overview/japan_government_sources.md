# Official Government Sources Supplement: JAPAN

**Primary language of political discourse: Japanese (日本語)**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Japan (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Japan. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Japan's government web infrastructure is decentralized — unlike Mexico's unified `gob.mx` platform, each ministry and agency operates its own independent website under the `.go.jp` top-level domain (e.g., `kantei.go.jp`, `mofa.go.jp`, `mod.go.jp`). This requires separate extraction patterns for each source but also means no single point of failure can take down the entire government monitoring layer. A distinctive strength of Japan's official web ecosystem is its **extensive English-language publishing**: the Prime Minister's Office, MOFA, MOD, MOF, METI, and BOJ all maintain substantive English-language sites with press releases, transcripts, and policy documents published with relatively short delays (often same-day or next-day). Several agencies provide RSS feeds in RSS 1.0 (RDF) format. Government press conferences — particularly the Chief Cabinet Secretary's twice-daily pressers and MOFA's regular Foreign Minister press conferences — are a primary channel for official signaling and are published as full transcripts in both Japanese and English.

---

## 1. OFFICIAL GOVERNMENT SOURCES: JAPAN

### 1.1 Head of Government — Prime Minister's Office (首相官邸 / Kantei) & Cabinet Office

| Field | Detail |
|---|---|
| **Institution** | Prime Minister's Office of Japan (首相官邸) / Cabinet Office (内閣府) |
| **Domain** | `kantei.go.jp` (Japanese) / `japan.kantei.go.jp` (English) |
| **Entry Point URL** | Japanese: `https://www.kantei.go.jp/jp/news/index.html` / English: `https://japan.kantei.go.jp/news/` |
| **RSS/Atom Feed** | **Yes (RSS 1.0 / RDF).** Japanese feeds: New Information `https://www.kantei.go.jp/index-jnews.rdf`, PM Activities `https://www.kantei.go.jp/index-j2.rdf`. English feeds available at `https://japan.kantei.go.jp/rss.html` [VERIFY exact English feed URLs — page returns 404 intermittently]. |
| **Language** | Japanese (primary); English (comprehensive parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Daily. Chief Cabinet Secretary press conferences (官房長官記者会見) held twice daily (AM and PM). PM press conferences after summits, major policy decisions, and crises. Policy announcements, cabinet decisions, and PM activities published same-day. |
| **Content Format** | HTML (articles and transcripts). Some policy documents in PDF. Press conference transcripts are long-form HTML. |
| **Extraction Method** | RSS polling for new items (Japanese feeds confirmed functional). HTML scraping of English site news listing page. PM press conferences at `japan.kantei.go.jp/{PM-number}/statement/` (currently `104` for PM Takaichi). Chief Cabinet Secretary pressers at `japan.kantei.go.jp/tyoukanpress/YYYYMM/index.html`. |
| **Editorial Orientation** | Official government position. All content produced by the Cabinet Public Relations Office (内閣広報室). Framing reflects the governing coalition's (LDP-Komeito) policy priorities. |
| **Why This Source** | The single authoritative source for cabinet decisions, PM statements, and the twice-daily Chief Cabinet Secretary press conferences — Japan's primary channel for official government positions on all policy matters. The CCS pressers are where government positions on diplomatic incidents, defense matters, and domestic controversies are formally stated and where journalists probe for policy shifts. English transcripts published with short delay. |
| **Access Notes** | No paywall, no authentication required. No bot protection observed. The English site uses a PM-number prefix (`/104/` for Takaichi) that changes with each new prime minister, requiring URL updates on leadership transitions. Japanese site RSS feeds are well-maintained. |

**Additional entry points:**
- PM press conferences (English): `https://japan.kantei.go.jp/104/statement/`
- CCS press conferences (English): `https://japan.kantei.go.jp/tyoukanpress/`
- PM activities (English): `https://japan.kantei.go.jp/104/actions/`
- Cabinet Office (内閣府) main site: `https://www.cao.go.jp/` (policy councils, white papers, economic indicators)
- Cabinet decisions: `https://www.kantei.go.jp/jp/kakugi/index.html`

---

### 1.2 Foreign Ministry — Ministry of Foreign Affairs (外務省 / MOFA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Foreign Affairs of Japan (外務省 / MOFA) |
| **Domain** | `mofa.go.jp` |
| **Entry Point URL** | Press releases (English): `https://www.mofa.go.jp/press/release/index.html` / Press conferences (English): `https://www.mofa.go.jp/press/kaiken/index.html` / What's New: `https://www.mofa.go.jp/whats/` |
| **RSS/Atom Feed** | None confirmed. MOFA does not appear to maintain public RSS feeds for press releases or news updates. [VERIFY RSS — check `mofa.go.jp/rss.html` or `mofa.go.jp/whats/rss.xml`] |
| **Language** | Japanese and English (comprehensive parallel content) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Press releases issued for bilateral meetings, treaty actions, UN votes, sanctions, ODA, and consular matters. Foreign Minister press conferences held regularly (typically twice weekly). |
| **Content Format** | HTML. Press releases follow a consistent template. Press conference transcripts are full Q&A in HTML. The annual Diplomatic Bluebook (外交青書) is published as a major HTML/PDF document. |
| **Extraction Method** | HTML scraping of press release listing page (`/press/release/index.html`). Press releases use URL pattern: `mofa.go.jp/press/release/pressite_000001_XXXXX.html`. Press conferences at `/press/kaiken/kaikenwe_000001_XXXXX.html`. |
| **Editorial Orientation** | Official foreign ministry position. Reflects Japan's doctrinal commitments to the US alliance, Free and Open Indo-Pacific, rules-based international order, and multilateralism. Language shifts in characterizing bilateral relationships (e.g., China, South Korea, Russia) are analytically significant. |
| **Why This Source** | The only primary source for Japan's formal diplomatic positions, treaty ratifications, bilateral meeting readouts, sanctions implementation, and ODA commitments. Foreign Minister press conference transcripts reveal positions not always captured in the formal press release. The English-language output is among the most comprehensive of any foreign ministry globally. |
| **Access Notes** | No paywall, no authentication. Site occasionally returns 403 errors on automated access — may require standard browser headers. English content is typically published same-day or next-day. |

**Additional entry points:**
- Diplomatic Bluebook: `https://www.mofa.go.jp/policy/other/bluebook/index.html`
- Countries & regions pages: `https://www.mofa.go.jp/region/index.html`
- Japan's Security Policy (NSS, alliances): `https://www.mofa.go.jp/fp/nsp/page1we_000081.html`
- Speeches/statements by FM: `https://www.mofa.go.jp/press/entr/index.html`

---

### 1.3 Defense Ministry — Ministry of Defense (防衛省 / MOD) & Joint Staff Office (統合幕僚監部)

#### 1.3a Ministry of Defense (MOD)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Defense (防衛省 / MOD) |
| **Domain** | `mod.go.jp` |
| **Entry Point URL** | English: `https://www.mod.go.jp/en/` / Japanese press releases: `https://www.mod.go.jp/j/press/index.html` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS at `mod.go.jp/j/rss/` or similar] |
| **Language** | Japanese (primary); English (key documents, white papers, selected press releases) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Defense Minister press conferences (typically twice weekly after cabinet meetings). Press releases on SDF operations, defense cooperation, exercises, and procurement. Annual "Defense of Japan" white paper (防衛白書). |
| **Content Format** | HTML. White papers and major policy documents in PDF. Defense budget materials in PDF with statistical tables. |
| **Extraction Method** | HTML scraping of press release listing pages. English site at `/en/` provides translated key documents. Japanese press releases at `/j/press/`. Defense Minister press conferences at `/j/press/kisha/`. |
| **Editorial Orientation** | Official defense establishment position. Communications emphasize threat environment (China, North Korea, Russia), alliance cooperation, and capability buildup. Framing reflects the 2022 National Security Strategy and three security documents (安保三文書). |
| **Why This Source** | Primary source for defense policy announcements, SDF operational reports, defense budget breakdowns, and bilateral/multilateral defense cooperation. The "Defense of Japan" white paper is the definitive annual assessment of the security environment as seen by Japan's defense establishment. ATLA (Acquisition, Technology & Logistics Agency) publications on defense procurement and equipment transfer are housed under MOD. |
| **Access Notes** | No paywall. Site occasionally returns 403 on automated access. English section covers key documents but is less comprehensive than MOFA's English output. Defense Minister press conferences are Japanese-only transcripts with no systematic English translation. |

#### 1.3b Joint Staff Office (統合幕僚監部)

| Field | Detail |
|---|---|
| **Institution** | Joint Staff Office (統合幕僚監部) |
| **Domain** | `mod.go.jp/js/` |
| **Entry Point URL** | English: `https://www.mod.go.jp/js/press/index-en.html` / Japanese: `https://www.mod.go.jp/js/press/index.html` |
| **RSS/Atom Feed** | None confirmed. [VERIFY RSS] |
| **Language** | Japanese (primary); English (intercept/scramble press releases) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Multiple per week. Press releases issued for Chinese/Russian military activity near Japan (aircraft intercepts, naval transits), SDF operational events, and joint exercises. |
| **Content Format** | HTML press releases with embedded images/maps showing aircraft flight paths and naval vessel tracks. |
| **Extraction Method** | HTML scraping of press release listing page. English-language intercept reports use standardized format with maps. |
| **Editorial Orientation** | Operational military communication. Intercept/scramble reports are factual with standardized language. The frequency and detail of these reports is itself an indicator of threat perception. |
| **Why This Source** | The only primary source for real-time reporting on foreign military activity near Japan — Chinese PLA Navy/Air Force and Russian military operations in the East China Sea, Sea of Japan, and Pacific approaches. These press releases are widely cited by international media and defense analysts. Published in English with maps, making them immediately usable. |
| **Access Notes** | Free. English intercept reports are reliably published. Maritime Self-Defense Force also has a separate press release page at `mod.go.jp/msdf/en/release/`. |

**Additional entry points:**
- ATLA (Acquisition, Technology & Logistics Agency): `https://www.mod.go.jp/atla/en/index.html`
- Defense of Japan (white paper): `https://www.mod.go.jp/en/publ/w_paper/index.html`
- GSDF/MSDF/ASDF individual service sites under `mod.go.jp` subdomains

---

### 1.4 Parliament / Legislature — National Diet (国会)

#### 1.4a House of Representatives (衆議院 / Shūgiin)

| Field | Detail |
|---|---|
| **Institution** | House of Representatives (衆議院) |
| **Domain** | `shugiin.go.jp` |
| **Entry Point URL** | English: `https://www.shugiin.go.jp/internet/index.nsf/html/index_e.htm` / Japanese: `https://www.shugiin.go.jp/internet/index.nsf/html/index.htm` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese (primary); English (institutional/structural pages only — no translated proceedings) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Daily during Diet sessions (regular session: January-June; extraordinary sessions convened as needed). Session schedules, submitted bills, committee hearing records, and voting results. |
| **Content Format** | HTML. Committee hearing minutes (議事録) in long-form HTML. Bill texts in HTML/PDF. Built on Lotus Notes/Domino web platform (`.nsf` URLs). |
| **Extraction Method** | HTML scraping. Lotus Notes/Domino-based URL structure (`index.nsf/html/...`). Committee proceedings database searchable but not RSS-enabled. Internet TV (live/archived video) at `shugiintv.go.jp`. |
| **Editorial Orientation** | Institutional. Proceedings are verbatim records. Committee testimony from ministers and officials is the primary content of analytical value. |
| **Why This Source** | Diet committee hearings — particularly Foreign Affairs, Security, and Budget committees — are where opposition parties interrogate government officials on defense, diplomatic, and economic policy. Minister responses during interpellations frequently reveal positions not stated in press conferences. Bill submission tracking reveals legislative priorities. Japanese-language only for proceedings. |
| **Access Notes** | No paywall. Legacy Lotus Notes/Domino platform makes scraping challenging. House of Representatives Internet TV (`shugiintv.go.jp`) provides live and archived video of plenary and committee sessions. |

**Additional entry points:**
- Minutes/proceedings search: `https://www.shugiin.go.jp/internet/itdb_kaigiroku.nsf/html/kaigiroku/kaigi_l.htm`
- Submitted bills: `https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/menu.htm`
- Internet TV: `https://www.shugiintv.go.jp/en/`

#### 1.4b House of Councillors (参議院 / Sangiin)

| Field | Detail |
|---|---|
| **Institution** | House of Councillors (参議院) |
| **Domain** | `sangiin.go.jp` |
| **Entry Point URL** | English: `https://www.sangiin.go.jp/eng/` / Japanese: `https://www.sangiin.go.jp/japanese/index.html` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese (primary); English (institutional pages only) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily during Diet sessions. Upper house election cycle (every 3 years, half the seats) creates regular political inflection points. |
| **Content Format** | HTML. Committee minutes in long-form HTML. |
| **Extraction Method** | HTML scraping. Separate infrastructure from the House of Representatives. |
| **Editorial Orientation** | Institutional. Verbatim records. |
| **Why This Source** | The House of Councillors plays a distinct role in treaty ratification and constitutional amendment procedures. Upper house elections serve as mid-term referenda on the governing coalition. Committee testimony parallels the lower house but with different committee membership and questioning dynamics. |
| **Access Notes** | No paywall. Less comprehensive web presence than the House of Representatives. Internet TV available at `webtv.sangiin.go.jp`. |

**Additional entry points:**
- Committee minutes search: `https://www.sangiin.go.jp/japanese/joho1/kaigirok/daily/select0101.html`
- Internet TV: `https://webtv.sangiin.go.jp/`
- National Diet Library legislative search (covers both houses): `https://ndlsearch.ndl.go.jp/`

---

### 1.5 Official Gazette — Kanpō (官報)

| Field | Detail |
|---|---|
| **Institution** | Official Gazette (官報) — published by the Cabinet Office (内閣府) as of April 2025 |
| **Domain** | `kanpo.go.jp` |
| **Entry Point URL** | `https://www.kanpo.go.jp/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Kanpō is the constitutional publication vehicle for all laws, cabinet orders, treaties, ministerial ordinances, and official notifications |
| **Publication Frequency** | Daily (weekdays). Regular edition (本紙), extra editions (号外), and government procurement supplement (政府調達). |
| **Content Format** | PDF. As of April 1, 2025, the Kanpō transitioned from paper to electronic publication as the legally authoritative format under the Act on Publication of the Official Gazette (令和5年法律第85号). |
| **Extraction Method** | PDF download from daily edition pages. Free access to editions published within the past 90 days. Historical search requires paid subscription through the National Printing Bureau (国立印刷局). |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, treaty, cabinet order, or ministerial ordinance takes legal effect until published in the Kanpō. This is the definitive, timestamped legal text. Media and ministry press releases about new legislation are always downstream of Kanpō publication. The April 2025 digitization makes electronic monitoring more straightforward than the previous paper-primary system. |
| **Access Notes** | Free access to past 90 days of editions at `kanpo.go.jp`. The paid Official Gazette Information Search Service (官報情報検索サービス) provides full historical search. The previous Internet Kanpō site operated by the National Printing Bureau (`kanpo.npb.go.jp`) closed March 31, 2025, with content migrated to the Cabinet Office site. Japanese-language only. |

---

### 1.6 Finance Ministry — Ministry of Finance (財務省 / MOF)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Finance (財務省 / MOF) |
| **Domain** | `mof.go.jp` |
| **Entry Point URL** | English: `https://www.mof.go.jp/english/public_relations/index.html` / Japanese: `https://www.mof.go.jp/public_relations/index.html` |
| **RSS/Atom Feed** | **Yes.** English What's New RSS: `https://www.mof.go.jp/english/news.rss` [VERIFY exact URL — redirect from `/english/rss.htm` to `/english/about_mof/rss/index.html`]. Japanese RSS also available. |
| **Language** | Japanese (primary); English (substantial parallel site — press releases, JGB data, minister statements) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Communications cover fiscal policy, JGB (Japanese Government Bond) issuance, customs/tariff policy, international financial diplomacy (G7/G20 finance), public debt management, and budget execution. Finance Minister press conferences after cabinet meetings. |
| **Content Format** | HTML. Statistical data and budget documents in PDF/Excel. JGB auction results in structured HTML/CSV. |
| **Extraction Method** | RSS polling for What's New feed. HTML scraping of press release pages. PDF/Excel download for fiscal data. |
| **Editorial Orientation** | Official fiscal policy position. MOF is institutionally committed to fiscal consolidation and maintaining market confidence in JGBs. Communications are technically rigorous and data-heavy. |
| **Why This Source** | Primary source for Japan's fiscal policy, public debt management, customs and tariff actions, and international financial diplomacy. MOF's role in G7/G20 finance tracks and IMF/World Bank engagement makes it essential for institutional engagement monitoring. Currency intervention decisions (coordinated with BOJ) and trade-related tariff actions originate here. |
| **Access Notes** | No paywall. RSS feeds confirmed available. English section includes minister's statements, press releases on JGBs, trade statistics, and customs policy. The MOF Newsletter provides regular summaries of policy activity. |

**Additional entry points:**
- Minister's statements (English): `https://www.mof.go.jp/english/public_relations/statement/index.htm`
- JGB press releases (English): `https://www.mof.go.jp/english/policy/jgbs/topics/press_release/index.htm`
- Trade statistics: `https://www.mof.go.jp/english/policy/customs_tariff/trade_statistics/index.html`
- MOF Newsletter: `https://www.mof.go.jp/english/policy/jgbs/publication/newsletter/index.htm`

---

### 1.7 Central Bank — Bank of Japan (日本銀行 / BOJ)

| Field | Detail |
|---|---|
| **Institution** | Bank of Japan (日本銀行 / BOJ) |
| **Domain** | `boj.or.jp` |
| **Entry Point URL** | English: `https://www.boj.or.jp/en/index.htm` / Monetary policy decisions: `https://www.boj.or.jp/en/mopo/mpmdeci/index.htm` |
| **RSS/Atom Feed** | **Yes.** What's New (English): `https://www.boj.or.jp/en/rss/whatsnew.xml`. [VERIFY additional feeds for monetary policy, statistics, research] |
| **Language** | Japanese (primary); English (comprehensive parallel site for all major publications) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary Policy Board meets 8 times per year (scheduled dates published in advance). Statements, minutes, and Outlook Report published per schedule. Research papers, speeches, and statistics published continuously. Tankan survey quarterly. |
| **Content Format** | HTML for announcements. PDF for monetary policy statements, minutes, Outlook Report, working papers, and speeches. Statistical data in CSV/Excel. |
| **Extraction Method** | RSS polling for What's New feed. HTML scraping of monetary policy decisions page. PDF download for statements and minutes. Meeting schedule published annually at `/en/mopo/mpmsche_minu/index.htm`. |
| **Editorial Orientation** | Technically independent central bank. Communications are analytically rigorous and data-driven. Under Governor Kazuo Ueda (appointed April 2023), the BOJ has been navigating the exit from ultra-loose monetary policy — every word choice in statements regarding yield curve control, inflation outlook, and forward guidance is closely parsed by markets. |
| **Why This Source** | The BOJ is the only source for authoritative monetary policy decisions, inflation/growth forecasts, and the Tankan survey (the most closely watched business sentiment indicator in Japan). Monetary policy normalization is a structural story with implications for yen valuation, JGB markets, and Japan's fiscal sustainability. The BOJ's English-language publishing is among the best of any central bank. |
| **Access Notes** | No paywall. No bot protection observed. RSS feed confirmed functional. English site mirrors virtually all major Japanese-language publications. The Institute for Monetary and Economic Studies (IMES) at `boj.or.jp/en/research/imes/` publishes academic-quality research. |

**Key BOJ publication schedule:**
| Publication | Frequency | Notes |
|---|---|---|
| Monetary Policy Statement | 8/year | Same-day English translation |
| Outlook Report (展望レポート) | Quarterly | Growth and inflation forecasts |
| Minutes | ~6 weeks after meeting | Full discussion summary |
| Summary of Opinions | ~1 week after meeting | Quick summary of views |
| Tankan Survey | Quarterly (April, July, October, December) | Business sentiment benchmark |
| Governor press conferences | After each MPM | Full transcript in English |
| Financial System Report | Biannual | Systemic risk assessment |

---

### 1.8 Trade Ministry — Ministry of Economy, Trade and Industry (経済産業省 / METI)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Economy, Trade and Industry (経済産業省 / METI) |
| **Domain** | `meti.go.jp` |
| **Entry Point URL** | English press releases: `https://www.meti.go.jp/english/press/index.html` / English RSS: `https://www.meti.go.jp/english/rss/index.html` |
| **RSS/Atom Feed** | **Yes.** RSS feeds available at `https://www.meti.go.jp/english/rss/index.html`. Japanese RSS at `https://www.meti.go.jp/rss/`. [VERIFY exact feed XML URLs from the RSS index page] |
| **Language** | Japanese (primary); English (comprehensive press releases, white papers, minister speeches) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | Daily or near-daily. Press releases organized by category: Economic & Industrial, External Economic Policy, Energy & Environment, Safety & Security. Minister press conferences after cabinet meetings. |
| **Content Format** | HTML for press releases. PDF for white papers, trade statistics, and policy reports. The annual "White Paper on International Economy and Trade" is a major publication. |
| **Extraction Method** | RSS polling for new releases. HTML scraping of categorized press release pages. Press releases organized by category at `/english/press/category_01.html` through `category_06.html`. |
| **Editorial Orientation** | Official trade and industrial policy position. METI is the institutional home of Japan's economic security strategy, semiconductor policy, supply chain resilience initiatives, and export control regime. Communications reflect the 2022 Economic Security Promotion Act framework. |
| **Why This Source** | Primary source for Japan's trade policy, export controls (including semiconductor equipment restrictions targeting China), economic security legislation, energy policy, and industrial strategy. METI's role in CPTPP, RCEP, and bilateral trade negotiations makes it essential for both economic statecraft and diplomatic alignment domains. The "METI Quick Reads" provide accessible summaries of policy initiatives. |
| **Access Notes** | No paywall. RSS confirmed available. English section is among the most comprehensive of any Japanese ministry. Press conferences and minister speeches translated to English. |

**Additional entry points:**
- External Economic Policy releases: `https://www.meti.go.jp/english/press/category_02.html`
- Energy & Environment releases: `https://www.meti.go.jp/english/press/category_05.html`
- White Papers & Reports: `https://www.meti.go.jp/english/report/index.html`
- Minister press conferences: `https://www.meti.go.jp/english/speeches/index.html`
- METI Quick Reads: `https://www.meti.go.jp/english/mobile/index.html`

---

### 1.9 Intelligence / National Security — National Security Secretariat (NSS) & Cabinet Intelligence and Research Office (CIRO)

#### 1.9a National Security Secretariat (国家安全保障局 / NSS)

| Field | Detail |
|---|---|
| **Institution** | National Security Secretariat (国家安全保障局 / NSS) — department of the Cabinet Secretariat |
| **Domain** | `cas.go.jp` (Cabinet Secretariat) |
| **Entry Point URL** | NSS information is embedded within the Cabinet Secretariat site. National Security Strategy: `https://www.cas.go.jp/jp/siryou/221216anzenhoshou/nss-e.pdf` (English translation). NSC page at MOFA: `https://www.mofa.go.jp/fp/nsp/page1we_000080.html` |
| **RSS/Atom Feed** | None available. |
| **Language** | Japanese (primary); English (key strategic documents only) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible for public communications. The NSS operates as a coordinating body within the Cabinet Secretariat. Major strategic documents (NSS, NDS, DCBP — the "three security documents") are published at multi-year intervals. The NSC (National Security Council) four-minister and nine-minister meetings are not publicly reported in detail. |
| **Content Format** | PDF for strategic documents. No regular HTML press releases. |
| **Extraction Method** | Periodic check of `cas.go.jp` for new national security-related publications. Monitor Kantei press conferences for NSC meeting readouts. |
| **Editorial Orientation** | N/A for public communications. The 2022 National Security Strategy and companion documents represent the most comprehensive statement of Japan's strategic posture. |
| **Why This Source** | Included for completeness and to capture periodic strategic document publications. The NSS Secretary General (who doubles as National Security Advisor) is a key figure whose meetings with foreign counterparts are reported through Kantei and MOFA channels rather than NSS directly. The real signal from NSS comes through its influence on other agencies' outputs. |
| **Access Notes** | `cas.go.jp` is the Cabinet Secretariat's main portal. NSS does not have a dedicated public website. Strategic documents are published as PDFs on the Cabinet Secretariat site with English translations. |

#### 1.9b Cabinet Intelligence and Research Office (内閣情報調査室 / CIRO)

| Field | Detail |
|---|---|
| **Institution** | Cabinet Intelligence and Research Office (内閣情報調査室 / CIRO, commonly "Naichō") |
| **Domain** | `cas.go.jp` |
| **Entry Point URL** | English organizational page: `https://www.cas.go.jp/jp/gaiyou/jimu/jyouhoutyousa/en/community.html` |
| **RSS/Atom Feed** | None available. |
| **Language** | Japanese (minimal); English (organizational overview only) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. CIRO publishes virtually no public-facing communications. It has an English-language page describing the Japanese Intelligence Community structure, which is useful for organizational understanding but provides no operational or analytical intelligence. |
| **Content Format** | Minimal HTML. |
| **Extraction Method** | Periodic check for any new publications. Flag any publication as a high-priority anomaly. |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. CIRO is Japan's principal civilian intelligence agency, coordinating the intelligence community (including the Cabinet Satellite Intelligence Center / CSICE at `cas.go.jp/jp/gaiyou/jimu/jyouhoutyousa/en/csice.html`). Its public communications are almost nonexistent — intelligence-relevant signals from CIRO come through leaks to media, Kantei press conferences referencing intelligence assessments, and Diet committee testimony. |
| **Access Notes** | Organizational pages on `cas.go.jp` are static and rarely updated. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Imperial Household Agency (宮内庁)

| Field | Detail |
|---|---|
| **Institution** | Imperial Household Agency (宮内庁 / Kunai-chō) |
| **Domain** | `kunaicho.go.jp` |
| **Entry Point URL** | English: `https://www.kunaicho.go.jp/en/index.html` / Press releases: `https://www.kunaicho.go.jp/e-kunaicho/release.html` / Addresses and press conferences: `https://www.kunaicho.go.jp/joko/okotoba/index-en.html` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese (primary); English (institutional pages, addresses by Emperor/Empress, press releases) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Low frequency. Announcements cover state visits, imperial audiences with foreign heads of state, ceremonial events, and official statements by the Emperor. |
| **Content Format** | HTML. Addresses and speeches in HTML. Public relations materials at `/en/kunaicho/kohoshiryo/index.html`. |
| **Extraction Method** | HTML scraping of press release and addresses pages. Low frequency — weekly polling sufficient. |
| **Editorial Orientation** | Institutional, ceremonial. The Emperor is constitutionally a "symbol of the State" with no political power — but imperial audiences with foreign leaders and the Emperor's public statements carry diplomatic and symbolic weight. |
| **Why This Source** | State visits and imperial audiences are among Japan's highest-level diplomatic signals. The scheduling and protocol of imperial interactions with foreign leaders (who receives an audience, the order of state visits) reflects diplomatic priorities. Emperor Naruhito's statements on peace, war remembrance, and international cooperation carry significant symbolic weight domestically and regionally. |
| **Access Notes** | No paywall. English content available for key addresses and press releases. Contact: Press and Public Relations Office, Tel: 03-3213-1111. |

#### 1.10b Japan Aerospace Exploration Agency (JAXA / 宇宙航空研究開発機構)

| Field | Detail |
|---|---|
| **Institution** | Japan Aerospace Exploration Agency (JAXA) |
| **Domain** | `jaxa.jp` / `global.jaxa.jp` (English) |
| **Entry Point URL** | English: `https://global.jaxa.jp/` / Press releases: `https://global.jaxa.jp/press/` / Media page: `https://global.jaxa.jp/media.html` |
| **RSS/Atom Feed** | Available via media page. [VERIFY exact RSS feed URLs at `global.jaxa.jp/media.html`] |
| **Language** | Japanese (primary); English (comprehensive) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | Several per week. Press releases cover launches, satellite operations, international space cooperation, and research programs. |
| **Content Format** | HTML. Technical reports in PDF. |
| **Extraction Method** | RSS polling (if confirmed). HTML scraping of press release pages. What's New at `global.jaxa.jp/news/`. |
| **Editorial Orientation** | Scientific/technical institution. Increasingly relevant to security domain as Japan develops space-based ISR capabilities, quasi-zenith satellite system (QZSS), and space domain awareness. |
| **Why This Source** | JAXA's activities increasingly intersect with security policy — space-based maritime domain awareness, ISR satellite launches, ballistic missile detection support, and international space cooperation (especially with NASA and ESA). Japan's 2023 Space Security Initiative and the growing dual-use nature of space assets make JAXA monitoring relevant to defense autonomy assessment. |
| **Access Notes** | No paywall. English site is comprehensive. Media page indicates RSS availability. |

#### 1.10c National Institute for Defense Studies (NIDS / 防衛研究所)

| Field | Detail |
|---|---|
| **Institution** | National Institute for Defense Studies (防衛研究所 / NIDS) |
| **Domain** | `nids.mod.go.jp` |
| **Entry Point URL** | English: `https://www.nids.mod.go.jp/english/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese (primary); English (major publications) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Monthly (research papers, commentaries). Major annual publications: "East Asian Strategic Review" and "NIDS China Security Report." |
| **Content Format** | HTML (commentaries). PDF (research papers, annual publications). |
| **Extraction Method** | HTML scraping of publications page. PDF download for major reports. |
| **Editorial Orientation** | Semi-official defense-establishment perspective. Analytically rigorous. NIDS is MOD's internal think tank — its assessments signal how the defense establishment views the security environment before those views become policy. |
| **Why This Source** | Already in the Layer 1 media map (Source #13). Included here for Layer 2 completeness. The annual "NIDS China Security Report" is the most authoritative Japanese government-adjacent assessment of China's military capabilities and intentions. "East Asian Strategic Review" provides the broader regional security context. |
| **Access Notes** | Free. Major publications in English. |

#### 1.10d Japan Institute of International Affairs (JIIA / 国際問題研究所)

| Field | Detail |
|---|---|
| **Institution** | Japan Institute of International Affairs (国際問題研究所 / JIIA) |
| **Domain** | `jiia.or.jp` |
| **Entry Point URL** | English: `https://www.jiia.or.jp/en/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Japanese (primary); English (commentaries, policy briefs) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Weekly (commentaries, policy briefs). Annual "Strategic Yearbook." |
| **Content Format** | HTML (commentaries). PDF (research papers, yearbook). |
| **Extraction Method** | HTML scraping of English publications page. |
| **Editorial Orientation** | Centrist-establishment. MOFA-proximate — JIIA is MOFA's principal affiliated think tank. Internationalist, pro-alliance. |
| **Why This Source** | Already in Layer 1 media map (Source #14). JIIA commentaries signal diplomatic establishment thinking on alliance management, multilateral engagement, Indo-Pacific strategy, and regional order. Track-1.5 dialogue reports provide insight into unofficial diplomatic channels. |
| **Access Notes** | Free. English commentaries and research papers available. |

#### 1.10e Financial Services Agency (金融庁 / FSA)

| Field | Detail |
|---|---|
| **Institution** | Financial Services Agency (金融庁 / FSA) |
| **Domain** | `fsa.go.jp` |
| **Entry Point URL** | English: `https://www.fsa.go.jp/en/` / RSS: `https://www.fsa.go.jp/en/rss.html` |
| **RSS/Atom Feed** | **Yes.** RSS feeds available at `https://www.fsa.go.jp/en/rss.html`. |
| **Language** | Japanese (primary); English (regulatory announcements, policy documents) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Multiple per week. Regulatory actions, policy statements, financial inspection results, and international financial regulatory coordination. |
| **Content Format** | HTML. PDF for formal regulatory documents. |
| **Extraction Method** | RSS polling. HTML scraping. |
| **Editorial Orientation** | Financial regulatory authority. Communications cover banking supervision, securities regulation, insurance oversight, and fintech policy. |
| **Why This Source** | FSA's regulatory actions affect international financial flows, cross-border investment, and Japan's position in global financial governance. Relevant to economic statecraft when FSA actions intersect with sanctions enforcement, anti-money-laundering compliance, or cryptocurrency regulation. |
| **Access Notes** | No paywall. RSS confirmed available. English site provides key regulatory documents. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | English Site |
|---|---|---|---|---|---|---|---|
| 1 | Kantei (PM Office) | `japan.kantei.go.jp/news/` | **Yes** (RDF) | P1 | HTML | Daily | Yes (comprehensive) |
| 2 | MOFA | `mofa.go.jp/press/release/index.html` | [VERIFY] | P1 | HTML | Daily | Yes (comprehensive) |
| 3a | MOD | `mod.go.jp/en/` | [VERIFY] | P1 | HTML/PDF | Daily | Yes (key documents) |
| 3b | Joint Staff | `mod.go.jp/js/press/index-en.html` | [VERIFY] | P1 | HTML | Multiple/week | Yes (intercept reports) |
| 4a | House of Representatives | `shugiin.go.jp` | [VERIFY] | P2 | HTML | Daily (session) | Minimal |
| 4b | House of Councillors | `sangiin.go.jp` | [VERIFY] | P2 | HTML | Daily (session) | Minimal |
| 5 | Kanpō (Official Gazette) | `kanpo.go.jp` | [VERIFY] | P2 | PDF | Daily | No |
| 6 | MOF | `mof.go.jp/english/public_relations/` | **Yes** | P2 | HTML/PDF | Daily | Yes (comprehensive) |
| 7 | BOJ | `boj.or.jp/en/` | **Yes** | P2 | PDF/HTML | Variable | Yes (comprehensive) |
| 8 | METI | `meti.go.jp/english/press/index.html` | **Yes** | P2 | HTML/PDF | Daily | Yes (comprehensive) |
| 9a | NSS | `cas.go.jp` (embedded) | No | P2 | PDF | Rare | Key documents only |
| 9b | CIRO | `cas.go.jp` (embedded) | No | P2 | Minimal | Negligible | Organizational only |
| 10a | Imperial Household Agency | `kunaicho.go.jp/en/` | [VERIFY] | P2 | HTML | Low | Yes (addresses, releases) |
| 10b | JAXA | `global.jaxa.jp/` | [VERIFY] | P2 | HTML/PDF | Multiple/week | Yes (comprehensive) |
| 10c | NIDS | `nids.mod.go.jp/english/` | [VERIFY] | P2 | PDF | Monthly | Major publications |
| 10d | JIIA | `jiia.or.jp/en/` | [VERIFY] | P2 | HTML/PDF | Weekly | Commentaries |
| 10e | FSA | `fsa.go.jp/en/` | **Yes** | P2 | HTML/PDF | Multiple/week | Yes (regulatory) |

---

## 3. MONITORING CONFIGURATION

```yaml
# Japan Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/jp.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: jp_kantei
    name: Prime Minister's Office (首相官邸)
    domain: kantei.go.jp
    entry_url: "https://japan.kantei.go.jp/news/"
    rss_feed:
      new_information_ja: "https://www.kantei.go.jp/index-jnews.rdf"
      pm_activities_ja: "https://www.kantei.go.jp/index-j2.rdf"
      english_feed: null  # [VERIFY at japan.kantei.go.jp/rss.html]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 2
    notes: >
      Twice-daily CCS press conferences are primary signal channel.
      PM number prefix in English URLs changes on leadership transition (currently /104/ for Takaichi).
      RSS feeds in RSS 1.0 (RDF) format.

  - id: jp_mofa
    name: Ministry of Foreign Affairs (外務省)
    domain: mofa.go.jp
    entry_url: "https://www.mofa.go.jp/press/release/index.html"
    rss_feed: null  # [VERIFY]
    language: ja
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
    notes: >
      Comprehensive English site. Press releases at /press/release/,
      FM press conferences at /press/kaiken/. May return 403 on automated
      access — use standard browser User-Agent headers.

  - id: jp_mod
    name: Ministry of Defense (防衛省)
    domain: mod.go.jp
    entry_url: "https://www.mod.go.jp/j/press/index.html"
    rss_feed: null  # [VERIFY]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: >
      English site at /en/ covers key documents and white papers.
      Defense Minister press conferences Japanese-only.
      May return 403 — use standard browser headers.

  - id: jp_joint_staff
    name: Joint Staff Office (統合幕僚監部)
    domain: mod.go.jp
    entry_url: "https://www.mod.go.jp/js/press/index-en.html"
    rss_feed: null  # [VERIFY]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "multiple_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: >
      English-language intercept/scramble reports with maps.
      Standardized format for PLA/Russian military activity near Japan.
      MSDF separate releases at /msdf/en/release/.

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: jp_shugiin
    name: House of Representatives (衆議院)
    domain: shugiin.go.jp
    entry_url: "https://www.shugiin.go.jp/internet/index.nsf/html/index.htm"
    rss_feed: null  # [VERIFY]
    language: ja
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Lotus Notes/Domino platform (.nsf URLs). Japanese-only for proceedings.
      Committee minutes (議事録) are primary analytical content.
      Internet TV at shugiintv.go.jp for live/archived video.

  - id: jp_sangiin
    name: House of Councillors (参議院)
    domain: sangiin.go.jp
    entry_url: "https://www.sangiin.go.jp/japanese/index.html"
    rss_feed: null  # [VERIFY]
    language: ja
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: >
      Treaty ratification role. Upper house elections every 3 years (half seats).
      Internet TV at webtv.sangiin.go.jp.

  - id: jp_kanpo
    name: Official Gazette (官報)
    domain: kanpo.go.jp
    entry_url: "https://www.kanpo.go.jp/"
    rss_feed: null  # [VERIFY]
    language: ja
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
      Transitioned to electronic-primary publication April 1, 2025.
      Free access to past 90 days. Historical search requires paid subscription.
      Japanese-only. All laws, treaties, cabinet orders legally effective only after Kanpō publication.

  - id: jp_mof
    name: Ministry of Finance (財務省)
    domain: mof.go.jp
    entry_url: "https://www.mof.go.jp/english/public_relations/index.html"
    rss_feed:
      whats_new_en: "https://www.mof.go.jp/english/news.rss"  # [VERIFY — redirect observed]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - institutional_engagement
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 6
    notes: >
      Comprehensive English site. JGB data, trade statistics, minister statements.
      RSS feed URL may redirect — verify canonical feed URL.

  - id: jp_boj
    name: Bank of Japan (日本銀行)
    domain: boj.or.jp
    entry_url: "https://www.boj.or.jp/en/mopo/mpmdeci/index.htm"
    rss_feed:
      whats_new_en: "https://www.boj.or.jp/en/rss/whatsnew.xml"
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_html_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: >
      Best English-language central bank output globally.
      MPM decisions 8/year. Tankan quarterly. RSS confirmed functional.
      Governor press conferences transcribed in English.

  - id: jp_meti
    name: Ministry of Economy, Trade and Industry (経済産業省)
    domain: meti.go.jp
    entry_url: "https://www.meti.go.jp/english/press/index.html"
    rss_feed:
      english_feed: "https://www.meti.go.jp/english/rss/index.html"  # [VERIFY exact XML URL from index]
      japanese_feed: "https://www.meti.go.jp/rss/"  # [VERIFY exact XML URL]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 6
    notes: >
      Comprehensive English press releases by category.
      Economic security, semiconductors, export controls, trade negotiations.
      METI Quick Reads for accessible policy summaries.

  - id: jp_nss
    name: National Security Secretariat (国家安全保障局)
    domain: cas.go.jp
    entry_url: "https://www.cas.go.jp/"
    rss_feed: null
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: rare
    content_format: pdf
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: >
      Effectively no regular public output. Strategic documents (NSS, NDS, DCBP)
      published at multi-year intervals. NSC meeting readouts come through Kantei.
      Flag any new publication as high-priority anomaly.

  - id: jp_ciro
    name: Cabinet Intelligence and Research Office (内閣情報調査室)
    domain: cas.go.jp
    entry_url: "https://www.cas.go.jp/jp/gaiyou/jimu/jyouhoutyousa/en/community.html"
    rss_feed: null
    language: ja
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: >
      Effectively silent. Organizational pages only.
      Intelligence signal comes through leaks to media and Diet testimony.

  - id: jp_kunaicho
    name: Imperial Household Agency (宮内庁)
    domain: kunaicho.go.jp
    entry_url: "https://www.kunaicho.go.jp/e-kunaicho/release.html"
    rss_feed: null  # [VERIFY]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: low
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: >
      State visits and imperial audiences signal diplomatic priorities.
      Emperor's addresses carry symbolic diplomatic weight.

  - id: jp_jaxa
    name: Japan Aerospace Exploration Agency (JAXA)
    domain: jaxa.jp
    entry_url: "https://global.jaxa.jp/press/"
    rss_feed: null  # [VERIFY at global.jaxa.jp/media.html]
    language: ja
    language_secondary: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "multiple_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: >
      Increasingly security-relevant: space-based ISR, QZSS, missile detection support.
      Comprehensive English site.

  - id: jp_nids
    name: National Institute for Defense Studies (防衛研究所)
    domain: nids.mod.go.jp
    entry_url: "https://www.nids.mod.go.jp/english/"
    rss_feed: null  # [VERIFY]
    language: ja
    language_secondary: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: monthly
    content_format: pdf
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: >
      Annual 'East Asian Strategic Review' and 'NIDS China Security Report'
      are key semi-official threat assessments. Also in Layer 1 media map.

  - id: jp_jiia
    name: Japan Institute of International Affairs (国際問題研究所)
    domain: jiia.or.jp
    entry_url: "https://www.jiia.or.jp/en/"
    rss_feed: null  # [VERIFY]
    language: ja
    language_secondary: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: weekly
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: >
      MOFA-affiliated think tank. Commentaries signal diplomatic establishment thinking.
      Also in Layer 1 media map.

  - id: jp_fsa
    name: Financial Services Agency (金融庁)
    domain: fsa.go.jp
    entry_url: "https://www.fsa.go.jp/en/"
    rss_feed: "https://www.fsa.go.jp/en/rss.html"  # [VERIFY exact XML feed URL]
    language: ja
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "multiple_per_week"
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 12
    notes: >
      Financial regulation, sanctions enforcement, AML compliance.
      RSS confirmed available.

# Shared configuration notes for Japan government sources
japan_shared_config:
  tld: ".go.jp"
  infrastructure: decentralized  # Each ministry operates independently
  common_issues:
    - "403 responses on automated access (MOFA, MOD) — use standard browser User-Agent"
    - "RSS 1.0 (RDF) format used by older feeds — requires RDF parser"
    - "PM URL prefix changes on leadership transition (/104/ for Takaichi)"
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "ja,en;q=0.9"
  rate_limit: "max 1 request per 3 seconds per domain"
  encoding: "UTF-8 (standard across all .go.jp sites)"
  english_coverage: >
    Japan's English-language government publishing is exceptionally strong.
    Kantei, MOFA, MOD, MOF, METI, and BOJ all maintain comprehensive English sites.
    For most P1 sources, English output is sufficient for baseline monitoring,
    with Japanese-language deep-dives required only for Diet proceedings,
    CCS presser nuances, and defense minister Q&A.
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Japanese government communications are more technically rigorous and less overtly propagandistic than many national contexts, but they are nonetheless carefully managed. The pipeline must treat government sources as confirming the government's chosen public position — not necessarily the underlying reality. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) shifts in language over time (particularly in characterizing bilateral relationships and threat assessments).

- **Kantei (PM Office / CCS pressers)**: Cross-reference CCS press conference statements against same-day reporting in Kyodo News (centrist wire) and NHK (public broadcaster, government-proximate). When the CCS uses formulaic language ("we are closely monitoring the situation" / 注視している), it signals awareness without commitment. Deviations from formulaic language are analytically significant. Cross-check against Asahi Shimbun (center-left) for opposition framing of the same statement. When Asahi and Yomiuri report the same CCS statement with similar interpretation, it signals genuine cross-spectrum consensus on the government's position.

- **MOFA**: Diplomatic press releases should be triangulated with Kyodo News (which often receives MOFA backgrounding), The Japan Times (English-language depth), and Nikkei Asia (economic diplomacy lens). Watch for shifts in language toward specific countries — e.g., changes in how China, South Korea, or Russia are characterized in press releases. MOFA's annual Diplomatic Bluebook is a benchmark for tracking year-over-year shifts in diplomatic posture. Cross-reference with JIIA commentaries (MOFA-affiliated) for semi-official analytical framing.

- **MOD / Joint Staff**: Defense bulletins are operationally factual (intercept reports include flight paths and vessel types) but selective in what they highlight. The frequency of Joint Staff press releases on PLA/Russian activity near Japan is itself an indicator — increased frequency signals heightened operational tempo or political intent to publicize threats. Cross-reference with Yomiuri Shimbun (conservative, pro-defense) for defense establishment framing, Asahi Shimbun for critical counterpoint on defense spending and SDF expansion, and NIDS publications for analytical depth. Sankei Shimbun marks the hawkish boundary — when Sankei calls a MOD response insufficient, it signals right-wing pressure.

- **BOJ**: Monetary policy communications are the most technically rigorous government output in Japan and the least subject to political distortion. However, the selection of what to emphasize in press conferences and the Outlook Report reflects institutional positioning on the timing and pace of policy normalization. Cross-reference with Nikkei (deepest financial journalism in Japan), Reuters Tokyo bureau (international market perspective), and The Japan Times for analytical summaries.

- **MOF**: Fiscal data is generally reliable in headline numbers, but MOF's institutional commitment to fiscal consolidation colors the framing of budget reports and public debt communications. Cross-reference with Nikkei for independent fiscal analysis and Nikkei Asia for the international investor perspective.

- **METI**: Trade and industrial policy announcements should be triangulated with Nikkei (domestic business impact), Nikkei Asia (regional trade implications), and Reuters (how Japan's trade partners perceive the moves). METI's export control announcements — particularly regarding semiconductor equipment — require cross-referencing with US Commerce Department (BIS) announcements and Chinese media reactions to assess alignment and friction within the multilateral export control framework.

- **Diet proceedings**: Committee testimony is the rawest form of government communication — ministers responding to opposition questioning under parliamentary privilege. When a minister's committee answer contradicts or goes beyond the official CCS position, it reveals policy tensions. Cross-reference with Tokyo Shimbun (left-progressive, aggressive on government accountability) and NHK parliamentary broadcasts.

**4.2 Japan's decentralized government web architecture**

Unlike Mexico's centralized `gob.mx` platform, Japan's government sources operate on fully independent infrastructure under the `.go.jp` TLD. Each ministry maintains its own CMS, design template, and publication workflow. This has several implications:

- **No single point of failure**: A problem with `mofa.go.jp` does not affect `mod.go.jp` or `kantei.go.jp`
- **No shared extraction pattern**: Each source requires a separate scraper with source-specific URL patterns, pagination logic, and HTML templates
- **Independent publication timing**: Each ministry controls its own publication schedule without platform-level approval workflows
- **Variable quality of English output**: Some ministries (MOFA, BOJ, METI) have excellent English sites; others (Diet websites, Kanpō) are Japanese-only
- **Variable technical maturity**: BOJ and METI provide RSS feeds; MOFA and MOD apparently do not; Diet websites run on legacy Lotus Notes/Domino

**4.3 The NSS/CIRO silence problem**

Japan's intelligence and national security coordination apparatus (NSS + CIRO) produces effectively zero public communications. This is a structural gap that cannot be filled by monitoring. Intelligence-relevant signals surface through:

- **Kantei**: CCS press conferences where journalists ask about intelligence assessments or NSC deliberations
- **MOFA/MOD**: Policy outputs that reflect NSC decisions (without attributing them)
- **Diet testimony**: When NSS Secretary General or CIRO Director General testifies before parliamentary committees (rare but analytically valuable)
- **Media leaks**: Investigative reporting by Kyodo, Jiji Press, or individual reporters at Yomiuri/Asahi
- **Think tank proxies**: NIDS (MOD-affiliated) and JIIA (MOFA-affiliated) publications that signal evolving strategic thinking

The pipeline should not allocate significant resources to polling NSS/CIRO pages but should flag any new publication as a high-priority anomaly.

**4.4 The Japan-specific English-language advantage**

Japan is unusual among non-Anglophone countries in the breadth and depth of its government English-language publishing. This creates a monitoring advantage but also a trap:

- **Advantage**: P1 sources (Kantei, MOFA, MOD Joint Staff) can be monitored primarily through English-language output with high fidelity
- **Trap**: The deepest political intelligence — Diet interpellations, CCS presser nuances, party faction dynamics, bureaucratic maneuvering between ministries — remains Japanese-language only. English translations, when they exist, are often sanitized or simplified
- **Recommendation**: Use English sources as the baseline monitoring layer; deploy Japanese-language monitoring for Diet proceedings, defense minister Q&A, and any source where English output is delayed or absent

**4.5 Leadership transition URL instability**

A Japan-specific infrastructure issue: the Kantei English site embeds the prime minister's ordinal number in the URL path (e.g., `/104/` for PM Takaichi, the 104th Prime Minister). On every leadership transition — which can occur frequently given Japan's parliamentary system — all URL paths for PM statements, actions, and press conferences change. The pipeline must detect leadership transitions (easily via the Kantei homepage) and update URL patterns accordingly. Historical content under previous PM numbers remains accessible.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Architecture — No Shared Extraction Pattern

Unlike Mexico's `gob.mx` platform, Japan's government sources require individual scraper configurations for each domain. Key patterns:

- **Kantei**: RSS feeds (RDF format) for Japanese content. English site uses date-based URL patterns (`/YYYYMM/`) for press conferences and PM-number-based paths (`/104/`) for statements/actions.
- **MOFA**: Press releases at `/press/release/pressite_000001_XXXXX.html`. Press conferences at `/press/kaiken/kaikenwe_000001_XXXXX.html`. Sequential numbering — new items have higher numbers.
- **MOD**: Subdomain-based organization (`/js/` for Joint Staff, `/msdf/` for MSDF, `/atla/` for ATLA). Each subsection has its own press release listing page.
- **Diet websites**: Lotus Notes/Domino platform (`.nsf` URLs). Non-standard URL structure. Committee minutes database requires date-based navigation.
- **Kanpō**: Daily PDF editions at `kanpo.go.jp`. Date-based navigation. PDF text extraction required.
- **BOJ**: Clean URL structure. Meeting schedule published annually. Document-type suffixes (`_ron`, `_koen`, `_dan`) indicate content type.
- **METI**: Category-based press release pages (`/category_01.html` through `/category_06.html`). Month-based archive pages.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Five government sources provide confirmed or likely RSS feeds:

1. **Kantei**: RSS 1.0 (RDF) feeds for new information and PM activities (Japanese). Confirmed functional. English feed availability uncertain.
2. **MOF**: RSS feed for English "What's New" content. Redirect from legacy URL observed — canonical URL needs verification.
3. **BOJ**: XML feed for English "What's New." Confirmed functional at `boj.or.jp/en/rss/whatsnew.xml`.
4. **METI**: RSS feeds available for both English and Japanese content. Feed index pages confirmed; exact XML URLs need extraction from index pages.
5. **FSA**: RSS feeds available. Feed index page confirmed at `fsa.go.jp/en/rss.html`.

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Three sources publish primarily or substantially in PDF:

- **Kanpō**: All legal texts are PDF. Post-April 2025 editions are text-based PDFs (not scanned images). Daily extraction pipeline needed.
- **BOJ**: Monetary policy statements, minutes, Outlook Report, and working papers are multi-page PDF. Well-structured, text-based.
- **MOD**: "Defense of Japan" white paper, defense budget documents, and ATLA publications are PDF. Annual/periodic extraction.
- **MOF**: JGB-related statistical documents and budget materials often in PDF/Excel.

### 5.4 Language and Encoding

Japan's government sources are bilingual (Japanese primary, English secondary) to a degree unusual among non-Anglophone countries. All `.go.jp` sites use UTF-8 encoding.

| Source | English Coverage Level |
|---|---|
| Kantei | **High** — PM/CCS press conferences, statements, activities translated |
| MOFA | **High** — near-complete English mirror of press releases and speeches |
| MOD (main) | **Medium** — key documents and white papers; defense minister pressers Japanese-only |
| Joint Staff | **High** — intercept reports published in English with maps |
| Diet | **Low** — institutional pages only; proceedings Japanese-only |
| Kanpō | **None** — Japanese-only |
| MOF | **High** — comprehensive English site |
| BOJ | **Very High** — virtually all major publications translated |
| METI | **High** — press releases, white papers, speeches translated |
| NSS/CIRO | **Low** — strategic documents only |
| Imperial Household | **Medium** — addresses and key releases |
| JAXA | **High** — comprehensive English site |

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels:

- **Diplomatic events**: Covered by Kantei (PM-level readouts), MOFA (bilateral meeting press releases), and sometimes MOD (if defense cooperation is involved)
- **Defense policy**: Covered by Kantei (cabinet decisions), MOD (defense minister presser), and Joint Staff (operational implications)
- **Economic policy**: Covered by Kantei (cabinet decisions), METI (trade/industry), MOF (fiscal), and sometimes BOJ (monetary policy coordination)
- **Legislation**: Appears in Kantei (cabinet decision), Diet proceedings (committee deliberation), and Kanpō (legal publication)

Implement content-hash deduplication. Use the originating ministry (MOFA for diplomatic, MOD for defense, METI for trade) as canonical for domain-specific items. Use Kantei as canonical for cross-domain policy announcements. Use Kanpō as canonical for legal texts.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Kantei, MOFA | Every 2 hours | Daily publication, primary policy signaling channels |
| P1-Standard | MOD, Joint Staff | Every 4 hours | High-value when published; Joint Staff intercept reports time-sensitive |
| P2-Active | MOF, BOJ, METI, Diet (session) | Every 6 hours | Regular publishing schedule, RSS where available |
| P2-Standard | Kanpō, JAXA, FSA, Imperial Household | Every 12-24 hours | Important but lower velocity |
| P2-Low | NIDS, JIIA | Every 24 hours | Think tank publications on weekly/monthly cycle |
| P2-Minimal | NSS, CIRO | Weekly | Effectively silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| 403 response on automated access | MOFA, MOD | Rotate User-Agent headers. Use headless browser (Playwright/Puppeteer). MOFA and MOD press releases are also reported by Kyodo News within minutes. |
| Kantei PM-number URL path change | Kantei English site | Detect leadership transition via Kantei homepage. Update `/104/` prefix to new PM's ordinal number. Old PM's content remains accessible under the old prefix. |
| Diet website Lotus Notes/Domino issues | Shugiin, Sangiin | NHK parliamentary broadcasts cover key committee sessions. National Diet Library (`ndlsearch.ndl.go.jp`) provides searchable proceedings archive. |
| Kanpō site downtime | Kanpō | Cabinet Office general site (`cao.go.jp/others/soumu/kanpo/`) provides information about the Kanpō. Ministry-level press releases announce their own legislation before Kanpō publication. |
| BOJ RSS feed failure | BOJ | HTML scraping of What's New page at `boj.or.jp/en/whatsnew/index.htm`. BOJ monetary policy decisions are simultaneously reported by all wire services (Kyodo, Jiji, Reuters, Bloomberg). |
| Domain-wide `.go.jp` DNS issues | All government sources | Extremely rare. Kyodo News and NHK are primary fallbacks for all government announcements. Government social media accounts (@JPN_PMO, @MofaJapan_en, @ModJapan_en) on X/Twitter provide real-time backup. |

---

*This supplement should be reviewed quarterly, upon any prime ministerial transition (which triggers URL structure changes), or upon significant restructuring of government web infrastructure. The April 2025 Kanpō digitization was the most recent major infrastructure change.*
