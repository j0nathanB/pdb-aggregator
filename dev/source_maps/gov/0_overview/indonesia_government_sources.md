# Official Government Sources Supplement: INDONESIA

**Primary language of political discourse: Indonesian (Bahasa Indonesia)**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Indonesia (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Indonesia. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Indonesia's government web infrastructure is decentralized. Unlike Mexico's unified gob.mx portal, each Indonesian ministry and agency maintains its own independent domain under the `.go.id` top-level pattern (e.g., `kemlu.go.id`, `kemenkeu.go.id`, `kemhan.go.id`). This means there is no single extraction template — each source requires a bespoke scraper configuration. The presidential communication function is split between two sites: `presidenri.go.id` (the President's official page, managed by the State Secretariat) and `setkab.go.id` (the Cabinet Secretariat, which publishes cabinet decisions, presidential regulations, and policy readouts). The military similarly maintains separate portals for the overarching TNI command (`tni.mil.id`) and each service branch (`tniad.mil.id`, `tnial.mil.id`, `tni-au.mil.id`), all under the `.mil.id` domain. Many government sites are built on WordPress, which means RSS feeds at `/feed/` are sometimes available even when not prominently linked. Content is overwhelmingly in Bahasa Indonesia; English sections exist on some sites but lag significantly or cover only a subset of releases.

---

## 1. OFFICIAL GOVERNMENT SOURCES: INDONESIA

### 1.1 Head of Government — Presidenri.go.id / Sekretariat Kabinet / Sekretariat Negara

#### 1.1a Laman Resmi Presiden RI (Official Presidential Website)

| Field | Detail |
|---|---|
| **Institution** | Laman Resmi Presiden Republik Indonesia |
| **Domain** | `presidenri.go.id` |
| **Entry Point URL** | `https://www.presidenri.go.id/siaran-pers/` |
| **RSS/Atom Feed** | `https://www.presidenri.go.id/feed/` [VERIFY RSS — WordPress site, feed likely exists] |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Press releases (siaran pers), presidential speeches (pidato), and photo/video galleries published same-day. |
| **Content Format** | HTML (WordPress). Speeches published as full-text HTML. Some PDF attachments for formal decrees. |
| **Extraction Method** | WordPress RSS feed (if confirmed) or HTML scraping of `/siaran-pers/` listing page. URL pattern: `presidenri.go.id/siaran-pers/{slug}/`. |
| **Editorial Orientation** | Official presidential communication. All content produced by the Presidential Communications Office (Biro Pers, Media, dan Informasi Sekretariat Presiden). Framing reflects Prabowo administration priorities. |
| **Why This Source** | The single authoritative source for presidential statements, bilateral meeting readouts, policy announcements, and state visit communiques. Under Prabowo, this site has published extensive coverage of defense diplomacy meetings, BRICS engagement, and economic policy directives. Presidential speeches at international fora (UNGA, WEF, G20) appear here in full text before media summaries. |
| **Access Notes** | Returns 403 to some automated requests — likely Cloudflare or server-side bot protection. Rate limiting may apply. WordPress-based site. |

**Additional entry points:**
- Presidential speeches: `https://www.presidenri.go.id/pidato/`
- Photo gallery: `https://www.presidenri.go.id/galeri-foto/`
- Video gallery: `https://www.presidenri.go.id/galeri-video/`

#### 1.1b Sekretariat Kabinet (Cabinet Secretariat)

| Field | Detail |
|---|---|
| **Institution** | Sekretariat Kabinet Republik Indonesia (Setkab) |
| **Domain** | `setkab.go.id` |
| **Entry Point URL** | `https://setkab.go.id/berita/` |
| **RSS/Atom Feed** | **Yes.** `https://setkab.go.id/feed/` — confirmed valid RSS 2.0 feed. |
| **Language** | Indonesian; English section at `setkab.go.id/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains (cabinet decisions, presidential regulations, policy directives) |
| **Publication Frequency** | Daily. Publishes cabinet meeting readouts, presidential regulations (Perpres), weekly summaries ("Catatan Sepekan"), and official commentary. |
| **Content Format** | HTML (WordPress). Full-text articles with embedded images and infographics. |
| **Extraction Method** | **RSS feed** (preferred — confirmed functional). Feed delivers full article content with publication timestamps. |
| **Editorial Orientation** | Official government position. Setkab produces the most detailed readouts of cabinet-level decisions. Under the Prabowo administration, Setkab communications emphasize efficiency programs, economic growth targets, and defense modernization. |
| **Why This Source** | Setkab is the pipeline's most valuable single Indonesian government source. It publishes the full text of presidential regulations, cabinet meeting outcomes, and detailed readouts of bilateral/multilateral summits — content that media outlets summarize but rarely reproduce in full. Defense budget decisions, trade policy directives, and institutional reform mandates appear here before or simultaneously with media coverage. The confirmed RSS feed makes it the most automation-friendly government source. |
| **Access Notes** | No paywall. WordPress-based. RSS feed is well-formed and regularly updated. English section (`/en/`) provides translated versions of major releases but lags by days. Social media presence: @setkabgoid on X, Instagram, Facebook, TikTok. |

**Additional entry points:**
- Presidential regulations: `https://setkab.go.id/category/peraturan/`
- Presidential speeches: `https://setkab.go.id/category/pidato/`
- English news: `https://setkab.go.id/en/category/news/`
- JDIH (legal information): `https://jdih.setkab.go.id/`

#### 1.1c Sekretariat Negara (State Secretariat)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Sekretariat Negara (Setneg) |
| **Domain** | `setneg.go.id` |
| **Entry Point URL** | `https://www.setneg.go.id/listcontent/listberita/berita_presiden_dan_pemerintah` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Domestic constraints |
| **Publication Frequency** | Daily. Publishes presidential news and government activities. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | Official government position. Setneg handles state protocol and presidential palace affairs; overlaps with but is distinct from Setkab. |
| **Why This Source** | Setneg publishes state ceremony protocols, credential presentations by foreign ambassadors (an indicator of diplomatic relationship status), and formal government announcements that do not appear on Setkab. |
| **Access Notes** | Separate infrastructure from Setkab. No known bot protection. |

---

### 1.2 Foreign Ministry — Kementerian Luar Negeri (Kemlu)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Luar Negeri Republik Indonesia (Kemlu) |
| **Domain** | `kemlu.go.id` |
| **Entry Point URL** | `https://kemlu.go.id/portal/id/list/berita/84/press-release` |
| **RSS/Atom Feed** | None identified. The site uses a JavaScript-heavy SPA framework that does not expose RSS. |
| **Language** | Indonesian (primary); English press releases at `https://kemlu.go.id/portal/en/list/berita/84/press-release` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Press releases (siaran pers) issued for diplomatic meetings, treaty actions, consular emergencies, multilateral votes, ASEAN engagement, and bilateral summits. |
| **Content Format** | HTML (JavaScript SPA). Individual press releases render as dynamic pages. |
| **Extraction Method** | HTML scraping with headless browser (Playwright/Puppeteer) required — the site loads content via JavaScript and returns a loading splash screen to standard HTTP clients. API endpoint discovery may yield a JSON feed. |
| **Editorial Orientation** | Official foreign ministry position. Reflects Indonesia's doctrinal "bebas aktif" (free and active) foreign policy. Under Foreign Minister Sugiono, communications emphasize BRICS membership, South-South cooperation, Palestine solidarity, and ASEAN centrality. |
| **Why This Source** | The only primary source for Indonesia's formal diplomatic positions, treaty ratifications, ambassador appointments, and bilateral/multilateral meeting readouts. The Annual Press Statement of the Minister for Foreign Affairs (Pernyataan Pers Tahunan Menteri Luar Negeri) is a key annual posture document. Media coverage of Kemlu activity is invariably derived from these releases. |
| **Access Notes** | The site is built as a single-page application (SPA) — standard HTTP GET requests return only a loading screen with JavaScript. Headless browser rendering is essential. English translations available for major statements but incomplete. Embassy-level portals exist at `kemlu.go.id/[city]/[lang]` (e.g., `kemlu.go.id/washington/en`). |

**Additional entry points:**
- Embassy portals: `https://kemlu.go.id/{city}/{lang}/` (e.g., `kemlu.go.id/washington/en`)
- Annual Press Statement: published each January on the press release archive
- ASEAN portal: linked from main Kemlu site during chairmanship years

---

### 1.3 Defense / Security — Kementerian Pertahanan (Kemhan), TNI

#### 1.3a Kementerian Pertahanan (Ministry of Defense)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Pertahanan Republik Indonesia (Kemhan) |
| **Domain** | `kemhan.go.id` |
| **Entry Point URL** | `https://www.kemhan.go.id/category/berita` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at kemhan.go.id/feed/] |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Berita (news) articles cover ministerial activities, defense cooperation agreements, procurement events, and institutional ceremonies. |
| **Content Format** | HTML. News articles with photos. Some linked PDFs for defense white papers and procurement regulations. |
| **Extraction Method** | HTML scraping of `/category/berita` listing page. WordPress-based — RSS feed may exist at `/feed/`. |
| **Editorial Orientation** | Official defense ministry communication. Under Minister Sjafrie Sjamsoeddin (Prabowo's appointee), communications emphasize the $125B defense modernization program, domestic defense industry development (industri pertahanan dalam negeri), and supplier diversification across Western, Russian, and Chinese platforms. |
| **Why This Source** | Primary source for defense white papers, procurement regulations, military exercise announcements, and defense cooperation agreements. Indonesia's Rafale fighter acquisition, Scorpene submarine deal, and defense industry indigenization policies are documented here. Procurement regulation changes signal shifts in supplier diversification strategy. |
| **Access Notes** | No paywall. Indonesian language only. PPID (public information portal) at `ppid.kemhan.go.id`. Legal information at `jdih.kemhan.go.id`. |

**Additional entry points:**
- PPID (transparency portal): `https://ppid.kemhan.go.id/`
- JDIH (legal information): `https://jdih.kemhan.go.id/`

#### 1.3b TNI Headquarters (Mabes TNI)

| Field | Detail |
|---|---|
| **Institution** | Tentara Nasional Indonesia — Markas Besar (TNI Headquarters) |
| **Domain** | `tni.mil.id` |
| **Entry Point URL** | `https://tni.mil.id/news.html` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Daily. News articles from Pusat Penerangan TNI (Puspen TNI — TNI Information Center) cover joint exercises, operational deployments, Commander of TNI (Panglima TNI) activities, and institutional events. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. SSL certificate issues have been observed — may require certificate validation bypass. |
| **Editorial Orientation** | Official military communication. Highly controlled — releases cover operational outcomes, ceremonies, and exercises but never casualties, intelligence operations, or procurement costs. |
| **Why This Source** | The only direct window into TNI's joint operational tempo and strategic priorities. Panglima TNI statements and joint exercise announcements reveal partner-country prioritization and capability development focus areas. |
| **Access Notes** | SSL certificate issues observed (`unable to verify the first certificate`). The `.mil.id` domain infrastructure is separate from civilian `.go.id` sites. |

#### 1.3c Service Branch Portals

| Branch | Domain | Entry Point | Priority |
|---|---|---|---|
| TNI Angkatan Darat (Army) | `tniad.mil.id` | `https://tniad.mil.id/berita/` | P2 |
| TNI Angkatan Laut (Navy) | `tnial.mil.id` | `https://www.tnial.mil.id/` | P2 |
| TNI Angkatan Udara (Air Force) | `tni-au.mil.id` | `https://tni-au.mil.id/berita/satuan` | P2 |

Service branch portals provide granular detail on branch-specific exercises, procurement, and deployments that the Mabes TNI site aggregates at headline level. The Navy portal (`tnial.mil.id`) is particularly valuable for monitoring South China Sea patrols, Natuna deployments, and maritime security exercises.

---

### 1.4 Parliament / Legislature

#### 1.4a Dewan Perwakilan Rakyat (DPR — House of Representatives)

| Field | Detail |
|---|---|
| **Institution** | Dewan Perwakilan Rakyat Republik Indonesia (DPR RI) |
| **Domain** | `dpr.go.id` / `emedia.dpr.go.id` |
| **Entry Point URL** | `https://emedia.dpr.go.id/` (primary news portal) / `https://www.dpr.go.id/berita` (institutional site) |
| **RSS/Atom Feed** | **Yes.** `https://emedia.dpr.go.id/feed/` — confirmed valid RSS 2.0 feed. Title: "E-Media DPR RI." Updated hourly. |
| **Language** | Indonesian; English section at `https://en.dpr.go.id/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Domestic constraints, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods (January-July, August-December with recess periods). E-Media publishes multiple articles per day. |
| **Content Format** | HTML (WordPress on E-Media). |
| **Extraction Method** | **RSS feed** (preferred — confirmed functional on E-Media). HTML scraping for the main `dpr.go.id/berita` site (returns 403 to some automated requests). |
| **Editorial Orientation** | Institutional. Reflects majority coalition framing but includes opposition statements and committee proceedings. |
| **Why This Source** | Treaty ratifications, defense budget deliberations, and committee hearings on foreign/security policy originate here. Commission I (Defense, Foreign Affairs, Information) proceedings are essential for monitoring legislative oversight of defense procurement and foreign policy. The confirmed RSS feed on E-Media makes this highly automation-friendly. |
| **Access Notes** | Main `dpr.go.id` returns 403 to some HTTP clients. E-Media (`emedia.dpr.go.id`) is more accessible and provides the same content. English site at `en.dpr.go.id` has limited content. Mobile app available (E-Media DPR RI on Google Play). |

**Additional entry points:**
- BKSAP (Inter-Parliamentary Cooperation Body): `https://ksap.dpr.go.id/` — covers parliamentary diplomacy
- English portal: `https://en.dpr.go.id/berita/`
- Legislative tracking: `https://www.dpr.go.id/uu/prolegnas`

#### 1.4b Majelis Permusyawaratan Rakyat (MPR — People's Consultative Assembly)

| Field | Detail |
|---|---|
| **Institution** | Majelis Permusyawaratan Rakyat Republik Indonesia (MPR RI) |
| **Domain** | `mpr.go.id` |
| **Entry Point URL** | `https://www.mpr.go.id/berita` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS at mpr.go.id/feed/] |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement |
| **Publication Frequency** | 2-5 per week. Lower frequency than DPR; MPR's primary constitutional functions are limited to constitutional amendments, presidential inauguration, and annual joint sessions. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | Institutional. MPR Chairman Ahmad Muzani (Gerindra) communications reflect governing coalition priorities. |
| **Why This Source** | MPR's Annual Session (Sidang Tahunan) in August features the presidential state address on government performance and budget priorities — a key annual posture document. Constitutional amendment debates, when they arise, signal structural shifts in governance. |
| **Access Notes** | JDIH (legal information) at `jdih.mpr.go.id`. Video gallery at `mpr.go.id/galeri/video`. |

---

### 1.5 Official Gazette — JDIH / Peraturan.go.id / Lembaran Negara

| Field | Detail |
|---|---|
| **Institution** | Direktorat Jenderal Peraturan Perundang-undangan (DITJEN PP, Directorate General of Legislation) / JDIH Nasional |
| **Domain** | `peraturan.go.id` / `jdihn.go.id` / `jdih.setneg.go.id` |
| **Entry Point URL** | `https://peraturan.go.id/` (primary search database) / `https://jdih.setneg.go.id/Terbaru` (latest legal products) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Indonesian; English interface at `https://peraturan.go.id/eng` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Lembaran Negara (State Gazette) is the constitutional publication vehicle for all laws, government regulations, and presidential regulations |
| **Publication Frequency** | Continuous. New regulations published as enacted. The `jdih.setneg.go.id/Terbaru` page lists the most recently promulgated legal products. |
| **Content Format** | **PDF** documents. All laws and regulations are published as official PDF texts. The `peraturan.go.id` database provides searchable metadata with links to PDF downloads. |
| **Extraction Method** | Metadata scraping of `peraturan.go.id` search results or `jdih.setneg.go.id/Terbaru` listing page. PDF download and text extraction for full regulation text. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law or regulation is legally binding until published in the Lembaran Negara (for laws, government regulations) or Berita Negara (for ministerial regulations). This is the only source providing definitive, timestamped legal text. Media reports on legislation are always downstream of gazette publication. Presidential regulations on defense procurement, trade restrictions, investment requirements, and institutional restructuring appear here. |
| **Access Notes** | `peraturan.go.id` provides a search interface with filters by type, year, and subject. English interface available at `/eng`. The database processes 5,800+ legal documents (2001-present). Multiple ministry-specific JDIH portals exist (e.g., `jdih.kemhan.go.id`, `jdih.setkab.go.id`) but `peraturan.go.id` and `jdih.setneg.go.id` are the most comprehensive. The `peraturan.bpk.go.id` (BPK audit board) database is a useful alternative mirror. |

**Key JDIH portals:**
| Portal | Domain | Coverage |
|---|---|---|
| DITJEN PP (primary database) | `peraturan.go.id` | All central and regional regulations |
| Setneg (State Secretariat) | `jdih.setneg.go.id` | Laws, Perppu, PP, Perpres |
| JDIHN (national network) | `jdihn.go.id` | Aggregator across all JDIH members |
| BPK (audit board) | `peraturan.bpk.go.id` | Mirror of national regulations |

---

### 1.6 Finance Ministry — Kementerian Keuangan (Kemenkeu)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Keuangan Republik Indonesia (Kemenkeu) |
| **Domain** | `kemenkeu.go.id` |
| **Entry Point URL** | `https://www.kemenkeu.go.id/informasi-publik/publikasi/siaran-pers` |
| **RSS/Atom Feed** | None identified. Site uses heavy JavaScript rendering. |
| **Language** | Indonesian (primary); English section available at `https://www.kemenkeu.go.id/en` [VERIFY URL] |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week. Siaran pers (press releases) issued for fiscal policy announcements, APBN (state budget) execution reports, tax policy changes, public debt operations, and macroeconomic assessments. |
| **Content Format** | HTML. Many press releases include statistical tables and link to PDF annexes. |
| **Extraction Method** | HTML scraping with headless browser — the site loads content via JavaScript frameworks (Bootstrap + custom). URL pattern: `kemenkeu.go.id/informasi-publik/publikasi/siaran-pers/{slug}`. |
| **Editorial Orientation** | Official fiscal policy position. Technical language, data-heavy. Under Minister Sri Mulyani Indrawati (reappointed under Prabowo), communications emphasize fiscal discipline, APBN efficiency, and growth targets. |
| **Why This Source** | Primary source for federal budget execution, public debt operations, tax revenue data, and fiscal policy announcements. Essential for Economic & Technological Statecraft domain — Kemenkeu press releases are the raw data that CNBC Indonesia and Kontan interpret. APBN realization reports and quarterly fiscal reviews provide the most authoritative economic performance data. |
| **Access Notes** | JavaScript-heavy site — may require headless browser. Fiscal policy research also at `fiskal.kemenkeu.go.id`. Budget data at `djpb.kemenkeu.go.id`. No known English-language RSS. |

**Additional entry points:**
- Badan Kebijakan Fiskal (Fiscal Policy Agency): `https://fiskal.kemenkeu.go.id/publikasi/siaran-pers`
- Budget realization data: `https://djpb.kemenkeu.go.id/`
- Custom & excise: `https://www.beacukai.go.id/`

---

### 1.7 Central Bank — Bank Indonesia (BI)

| Field | Detail |
|---|---|
| **Institution** | Bank Indonesia (BI) |
| **Domain** | `bi.go.id` |
| **Entry Point URL** | `https://www.bi.go.id/id/publikasi/ruang-media/news-release/default.aspx` (Indonesian) / `https://www.bi.go.id/en/publikasi/ruang-media/news-release/default.aspx` (English) |
| **RSS/Atom Feed** | None confirmed for press releases. BI's statistical data may have structured feeds via its API/data portal. [VERIFY RSS] |
| **Language** | Indonesian (primary); English versions for all major publications at `bi.go.id/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 12 per year (monthly Board of Governors meetings, typically third or fourth Thursday). Quarterly monetary policy reports. Weekly international reserves updates. Miscellaneous press releases: 3-5 per week. |
| **Content Format** | HTML for news releases. **PDF** for monetary policy decisions, minutes, and quarterly reports. ASP.NET-based site. |
| **Extraction Method** | HTML scraping of the news release listing page (ASP.NET infrastructure). PDF download for policy decisions. The site uses ASP.NET WebForms with ViewState — scraping requires handling postback patterns. Socket connection issues observed — implement robust retry logic. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. Under Governor Perry Warjiyo, BI has maintained a hawkish stance on rupiah stability. Communications emphasize "pro-stability" monetary policy and macroprudential measures. |
| **Why This Source** | Bank Indonesia is the only source for authoritative monetary policy decisions, inflation data, international reserves, and rupiah exchange rate policy. BI-Rate decisions directly affect investment flows and are cited by all financial media. BI's English-language publications are among the most comprehensive of any Indonesian government institution, making this a high-value source for the pipeline's English-language processing. |
| **Access Notes** | ASP.NET infrastructure — heavier page weights and ViewState handling required. Socket connection timeouts observed on direct fetch. English site at `bi.go.id/en/` provides comprehensive parallel content. Statistical data portal: `https://www.bi.go.id/id/statistik/`. BI also maintains SEKI (Statistik Ekonomi dan Keuangan Indonesia) data portal. |

**Key publication URLs:**
| Publication | URL |
|---|---|
| News releases (ID) | `bi.go.id/id/publikasi/ruang-media/news-release/default.aspx` |
| News releases (EN) | `bi.go.id/en/publikasi/ruang-media/news-release/default.aspx` |
| Monetary policy decisions | `bi.go.id/id/publikasi/ruang-media/news-release/` (filtered by "Keputusan Rapat Dewan Gubernur") |
| International reserves | `bi.go.id/id/statistik/ekonomi-keuangan/seki/` |
| Quarterly monetary policy report | `bi.go.id/id/publikasi/laporan/` |

---

### 1.8 Trade / Commerce — Kementerian Perdagangan (Kemendag)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Perdagangan Republik Indonesia (Kemendag) |
| **Domain** | `kemendag.go.id` |
| **Entry Point URL** | `https://www.kemendag.go.id/berita/siaran-pers` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Indonesian; Google Translate widget provides machine translation to English, Arabic, Chinese, French, Spanish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 3-7 per week. Siaran pers cover trade balance data, export/import regulations, commodity price interventions, bilateral trade negotiations, and FTA implementation. |
| **Content Format** | HTML. Paginated listing (438+ pages of historical releases). Individual releases include data tables and charts. |
| **Extraction Method** | HTML scraping of `/berita/siaran-pers` listing page. Pagination via `?page={n}` query parameter. |
| **Editorial Orientation** | Official trade policy position. Under Minister Budi Santoso (trade name varies by reporting), communications emphasize export market diversification, domestic market protection, trade surplus achievement, and UMKM (SME) export empowerment. |
| **Why This Source** | Primary source for trade policy announcements, export/import regulation changes, commodity export controls (nickel, palm oil, bauxite), FTA negotiations (RCEP implementation, Indonesia-EU CEPA), and bilateral trade data. Indonesia's downstream industrialization mandates (hilirisasi) — including the nickel export ban and smelter requirements — are documented through Kemendag regulations. |
| **Access Notes** | No paywall. May return "Request Rejected" to certain automated requests — implement rotating headers. No native English section; relies on Google Translate widget. |

**Additional entry points:**
- Foreign trade directorate: `https://ditjendaglu.kemendag.go.id/`
- Trade policy research: `https://bkperdag.kemendag.go.id/`
- Trade representatives abroad: linked from main navigation

---

### 1.9 Intelligence / National Security — Badan Intelijen Negara (BIN)

| Field | Detail |
|---|---|
| **Institution** | Badan Intelijen Negara (BIN — State Intelligence Agency) |
| **Domain** | `bin.go.id` |
| **Entry Point URL** | `https://www.bin.go.id/` |
| **RSS/Atom Feed** | None available. |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. BIN publishes virtually no operational or policy communications. The website is primarily institutional (organizational structure, career portal, contact information). |
| **Content Format** | Minimal HTML. |
| **Extraction Method** | Periodic check of `bin.go.id` for any new publications. The site actively rejects many HTTP requests ("Request Rejected"). |
| **Editorial Orientation** | N/A — effectively silent. |
| **Why This Source** | Included for completeness. BIN's public-facing communications are almost nonexistent — the agency operates through internal channels and has no public transparency obligations comparable to legislative bodies. Its website may surface organizational restructuring, leadership appointments (notably the BIN Director, currently Muhammad Arief Prasetyo under Prabowo), or recruitment drives that indicate institutional shifts. The real intelligence signal from BIN comes through leaks to Tempo and Tirto.id, or through Setkab readouts referencing intelligence assessments. |
| **Access Notes** | `bin.go.id` actively rejects automated requests. The LAPOR! (public complaint) portal includes BIN as an addressable institution at `lapor.go.id/instansi/badan-intelijen-negara`. Social media: @OfficialBIN_RI on X. |

**Note on Indonesia's NSC equivalent:** Indonesia does not have a formal National Security Council. Security coordination occurs through the Coordinating Ministry for Political, Legal, and Security Affairs (Kemenko Polhukam) at `polhukam.go.id`. Kemenko Polhukam press releases (`https://polhukam.go.id/` [VERIFY URL]) provide readouts of inter-ministerial security coordination meetings and may reference BIN assessments indirectly.

---

### 1.10 Country-Specific Institutions

#### 1.10a Pertamina (State Energy Company)

| Field | Detail |
|---|---|
| **Institution** | PT Pertamina (Persero) |
| **Domain** | `pertamina.com` |
| **Entry Point URL** | `https://www.pertamina.com/en/news-room/news-release` (English) / `https://www.pertamina.com/id/news-room/news-release` [VERIFY URL] (Indonesian) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Indonesian and English (parallel content) |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week. Siaran pers cover production data, refinery operations, fuel distribution, energy transition investments, geothermal development, and financial results. |
| **Content Format** | HTML. Press releases with embedded images and data. |
| **Extraction Method** | HTML scraping of news release listing page. Azure-hosted infrastructure (web-pertamina.azurewebsites.net observed in some URLs). |
| **Editorial Orientation** | State enterprise communication. Emphasizes energy sovereignty, production targets, downstream development, and energy transition narrative. Financial difficulties and debt are acknowledged in mandatory disclosures but not highlighted in press communications. |
| **Why This Source** | Pertamina is Indonesia's largest enterprise and a central instrument of energy statecraft. Production data, refinery output (including the troubled Balikpapan and Tuban mega-refinery projects), upstream investment decisions, and energy transition positioning directly affect fiscal stability, trade balance, and bilateral energy relationships (particularly with Saudi Arabia, UAE, Russia). Pertamina's procurement decisions signal energy partnership priorities. |
| **Access Notes** | Bilingual site (Indonesian/English). No paywall. Media contact: infopublik@pertamina.com. Pertamina Geothermal Energy (PGE) has a separate site at `pge.pertamina.com` with its own press releases. |

#### 1.10b Danantara (Sovereign Wealth Fund)

| Field | Detail |
|---|---|
| **Institution** | Badan Pengelola Investasi Daya Anagata Nusantara (BPI Danantara) |
| **Domain** | `danantaraindonesia.co.id` |
| **Entry Point URL** | `https://www.danantaraindonesia.co.id/media-center/press-releases` |
| **RSS/Atom Feed** | None identified. |
| **Language** | English (primary site language); Indonesian content available [VERIFY] |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | 2-5 per week. Press releases cover investment decisions, SOE restructuring, partnership announcements, and governance updates. |
| **Content Format** | HTML. Media center organized into News, Press Releases, and Highlights. |
| **Extraction Method** | HTML scraping of press releases listing page. |
| **Editorial Orientation** | State investment entity communication. Established under Law No. 1 of 2025, Danantara is the Prabowo administration's signature economic institution — managing ~$900B-$1T in SOE assets. Communications emphasize world-class governance, strategic investment returns, and industrialization acceleration. Governance concerns (transparency, accountability, Rosan Roeslani's dual roles) are not addressed in official communications. |
| **Why This Source** | Danantara is the single largest structural change to Indonesia's economic governance under Prabowo. Its investment decisions — covering nickel processing, clean energy, digital infrastructure, agriculture, and financial services — directly shape Indonesia's economic statecraft posture. The fund's interaction with international investors (Blackstone, Adia, Mubadala) and its management of SOE dividends are critical fiscal and diplomatic indicators. Bloomberg reporting (March 2026) on Danantara's "turbulent first year" underscores the gap between official communications and independent assessments. |
| **Access Notes** | English-first website (unusual for Indonesian government entities). Media contact: media@danantaraindonesia.com. Also note: `danantaraindonesia.org` exists as an alternative domain [VERIFY whether this redirects or is a separate entity]. |

#### 1.10c Coordinating Ministry for Economic Affairs (Kemenko Perekonomian)

| Field | Detail |
|---|---|
| **Institution** | Kementerian Koordinator Bidang Perekonomian |
| **Domain** | `ekon.go.id` |
| **Entry Point URL** | `https://ekon.go.id/publikasi/1/siaran-pers` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Indonesian |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week. Siaran pers cover macroeconomic coordination, inter-ministerial policy decisions, economic outlook briefings, and Indonesia Economic Outlook events. |
| **Content Format** | HTML. URL pattern: `ekon.go.id/publikasi/detail/{id}/{slug}`. |
| **Extraction Method** | HTML scraping of siaran pers listing page. |
| **Editorial Orientation** | Official economic coordination position. Under Coordinating Minister Airlangga Hartarto (Golkar), communications present a unified economic narrative aggregating Kemenkeu, Kemendag, Bank Indonesia, and investment ministry positions. |
| **Why This Source** | The Coordinating Ministry aggregates economic policy positions across multiple line ministries into unified communications. Particularly valuable for tracking: (a) the government's response to external economic shocks (US tariffs, commodity price swings), (b) Indonesia's economic growth narrative (8% target), and (c) inter-ministerial coordination on downstream industrialization (hilirisasi) policy. |
| **Access Notes** | No paywall. Clean URL structure. |

#### 1.10d OJK (Financial Services Authority)

| Field | Detail |
|---|---|
| **Institution** | Otoritas Jasa Keuangan (OJK — Financial Services Authority) |
| **Domain** | `ojk.go.id` |
| **Entry Point URL** | `https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/` / `https://ojk.go.id/en/berita-dan-kegiatan/siaran-pers/` |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Indonesian; English section available |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 2-5 per week. Siaran pers cover banking surveillance, capital market regulation, fintech licensing, and financial stability assessments. |
| **Content Format** | HTML. Some PDF attachments for surveillance reports. ASP.NET-based. |
| **Extraction Method** | HTML scraping. ASP.NET infrastructure similar to Bank Indonesia. |
| **Editorial Orientation** | Independent regulatory authority. Technical, data-driven communications. |
| **Why This Source** | OJK's banking surveillance reports (LSPI) and capital market regulation decisions affect foreign investor access and financial sector stability — key inputs to the Economic & Technological Statecraft domain. OJK's regulatory actions on digital finance, cryptocurrency, and foreign bank licensing signal Indonesia's financial openness posture. |
| **Access Notes** | Bilingual site. ASP.NET infrastructure. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Infrastructure |
|---|---|---|---|---|---|---|---|
| 1a | Presiden RI | `presidenri.go.id/siaran-pers/` | [VERIFY] | P1 | HTML | Daily | WordPress |
| 1b | Setkab | `setkab.go.id/berita/` | **Yes** | P1 | HTML | Daily | WordPress |
| 1c | Setneg | `setneg.go.id/listcontent/listberita/...` | [VERIFY] | P2 | HTML | Daily | Custom |
| 2 | Kemlu | `kemlu.go.id/portal/id/list/berita/84/press-release` | No | P1 | HTML (SPA) | Daily | JavaScript SPA |
| 3a | Kemhan | `kemhan.go.id/category/berita` | [VERIFY] | P1 | HTML | 3-7/week | WordPress |
| 3b | TNI (Mabes) | `tni.mil.id/news.html` | No | P1 | HTML | Daily | Custom (.mil.id) |
| 3c | TNI AD/AL/AU | `tniad.mil.id/berita/` etc. | No | P2 | HTML | Variable | Custom (.mil.id) |
| 4a | DPR (E-Media) | `emedia.dpr.go.id/` | **Yes** | P2 | HTML | Daily (session) | WordPress |
| 4b | MPR | `mpr.go.id/berita` | [VERIFY] | P2 | HTML | 2-5/week | Custom |
| 5 | JDIH / Peraturan.go.id | `peraturan.go.id` / `jdih.setneg.go.id` | No | P2 | PDF | Continuous | Custom |
| 6 | Kemenkeu | `kemenkeu.go.id/informasi-publik/publikasi/siaran-pers` | No | P2 | HTML | 3-7/week | JavaScript-heavy |
| 7 | Bank Indonesia | `bi.go.id/id/publikasi/ruang-media/news-release/` | [VERIFY] | P2 | HTML/PDF | Variable | ASP.NET |
| 8 | Kemendag | `kemendag.go.id/berita/siaran-pers` | No | P2 | HTML | 3-7/week | Custom |
| 9 | BIN | `bin.go.id` | No | P2 | Minimal | Negligible | Custom |
| 10a | Pertamina | `pertamina.com/en/news-room/news-release` | No | P2 | HTML | 3-7/week | Azure |
| 10b | Danantara | `danantaraindonesia.co.id/media-center/press-releases` | No | P2 | HTML | 2-5/week | Custom |
| 10c | Kemenko Perekonomian | `ekon.go.id/publikasi/1/siaran-pers` | [VERIFY] | P2 | HTML | 3-5/week | Custom |
| 10d | OJK | `ojk.go.id/id/berita-dan-kegiatan/siaran-pers/` | [VERIFY] | P2 | HTML | 2-5/week | ASP.NET |

---

## 3. MONITORING CONFIGURATION

```yaml
# Indonesia Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/id.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: id_presiden
    name: Laman Resmi Presiden RI
    domain: presidenri.go.id
    entry_url: "https://www.presidenri.go.id/siaran-pers/"
    rss_feed: "https://www.presidenri.go.id/feed/"  # [VERIFY - WordPress, likely exists]
    language: id
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 2
    notes: "WordPress site. Returns 403 to some automated requests — may need headless browser fallback."

  - id: id_setkab
    name: Sekretariat Kabinet
    domain: setkab.go.id
    entry_url: "https://setkab.go.id/berita/"
    rss_feed: "https://setkab.go.id/feed/"  # CONFIRMED functional RSS 2.0
    language: id
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
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "Most valuable Indonesian government source. Confirmed RSS feed. English at /en/."

  - id: id_kemlu
    name: Kementerian Luar Negeri (Kemlu)
    domain: kemlu.go.id
    entry_url: "https://kemlu.go.id/portal/id/list/berita/84/press-release"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html_spa
    extraction_method: headless_browser_scrape
    poll_interval_hours: 2
    notes: "SPA site — requires Playwright/Puppeteer. English releases at /portal/en/. Embassy portals at kemlu.go.id/{city}/{lang}/."

  - id: id_kemhan
    name: Kementerian Pertahanan (Kemhan)
    domain: kemhan.go.id
    entry_url: "https://www.kemhan.go.id/category/berita"
    rss_feed: null  # [VERIFY at /feed/]
    language: id
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "WordPress-based. Defense white papers and procurement regulations in linked PDFs."

  - id: id_tni
    name: TNI Headquarters (Mabes TNI)
    domain: tni.mil.id
    entry_url: "https://tni.mil.id/news.html"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "SSL certificate issues — may need certificate validation bypass. Separate .mil.id infrastructure."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: id_setneg
    name: Sekretariat Negara
    domain: setneg.go.id
    entry_url: "https://www.setneg.go.id/listcontent/listberita/berita_presiden_dan_pemerintah"
    rss_feed: null  # [VERIFY]
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - domestic_constraints
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Credential presentations, state ceremonies, protocol matters."

  - id: id_dpr
    name: DPR RI (E-Media)
    domain: emedia.dpr.go.id
    entry_url: "https://emedia.dpr.go.id/"
    rss_feed: "https://emedia.dpr.go.id/feed/"  # CONFIRMED functional RSS 2.0
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - domestic_constraints
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Confirmed RSS feed. Commission I (defense/foreign affairs) proceedings are highest value. English at en.dpr.go.id."

  - id: id_mpr
    name: MPR RI
    domain: mpr.go.id
    entry_url: "https://www.mpr.go.id/berita"
    rss_feed: null  # [VERIFY]
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Annual Session (Sidang Tahunan) in August is the key event. Lower frequency outside session."

  - id: id_jdih
    name: JDIH / Peraturan.go.id
    domain: peraturan.go.id
    entry_url: "https://peraturan.go.id/"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
      - institutional_engagement
      - domestic_constraints
    publication_frequency: continuous
    content_format: pdf
    extraction_method: html_scrape_and_pdf_download
    poll_interval_hours: 6
    notes: "All laws/regulations published as PDFs. English interface at /eng. Cross-check with jdih.setneg.go.id/Terbaru for latest."

  - id: id_kemenkeu
    name: Kementerian Keuangan (Kemenkeu)
    domain: kemenkeu.go.id
    entry_url: "https://www.kemenkeu.go.id/informasi-publik/publikasi/siaran-pers"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: headless_browser_scrape
    poll_interval_hours: 6
    notes: "JavaScript-heavy site. APBN execution data critical. Fiscal policy research at fiskal.kemenkeu.go.id."

  - id: id_bi
    name: Bank Indonesia
    domain: bi.go.id
    entry_url: "https://www.bi.go.id/id/publikasi/ruang-media/news-release/default.aspx"
    rss_feed: null  # [VERIFY]
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 6
    notes: "ASP.NET site — ViewState handling required. Socket timeouts observed. English parallel at bi.go.id/en/. Monthly BI-Rate decisions. International reserves weekly."

  - id: id_kemendag
    name: Kementerian Perdagangan (Kemendag)
    domain: kemendag.go.id
    entry_url: "https://www.kemendag.go.id/berita/siaran-pers"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Pagination via ?page={n}. May reject automated requests. Google Translate widget for English."

  - id: id_bin
    name: Badan Intelijen Negara (BIN)
    domain: bin.go.id
    entry_url: "https://www.bin.go.id/"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent agency. Rejects most automated requests. Real signal via Tempo/Tirto leaks. Flag any publication as anomaly."

  - id: id_pertamina
    name: Pertamina
    domain: pertamina.com
    entry_url: "https://www.pertamina.com/en/news-room/news-release"
    rss_feed: null
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Bilingual (ID/EN). Azure-hosted. PGE subsidiary at pge.pertamina.com."

  - id: id_danantara
    name: Danantara (Sovereign Wealth Fund)
    domain: danantaraindonesia.co.id
    entry_url: "https://www.danantaraindonesia.co.id/media-center/press-releases"
    rss_feed: null
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "English-first site. ~$900B-$1T AUM. Governance transparency concerns. Media: media@danantaraindonesia.com."

  - id: id_ekon
    name: Kemenko Perekonomian
    domain: ekon.go.id
    entry_url: "https://ekon.go.id/publikasi/1/siaran-pers"
    rss_feed: null  # [VERIFY]
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Aggregates economic policy across line ministries. Indonesia Economic Outlook events."

  - id: id_ojk
    name: Otoritas Jasa Keuangan (OJK)
    domain: ojk.go.id
    entry_url: "https://ojk.go.id/id/berita-dan-kegiatan/siaran-pers/"
    rss_feed: null  # [VERIFY]
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "ASP.NET site. Banking surveillance, fintech regulation. English at ojk.go.id/en/."

  # --- TNI Service Branches (P2-Low) ---

  - id: id_tniad
    name: TNI Angkatan Darat (Army)
    domain: tniad.mil.id
    entry_url: "https://tniad.mil.id/berita/"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Army-specific exercises, deployments, procurement."

  - id: id_tnial
    name: TNI Angkatan Laut (Navy)
    domain: tnial.mil.id
    entry_url: "https://www.tnial.mil.id/"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Critical for South China Sea patrols, Natuna deployments, maritime exercises."

  - id: id_tniau
    name: TNI Angkatan Udara (Air Force)
    domain: tni-au.mil.id
    entry_url: "https://tni-au.mil.id/berita/satuan"
    rss_feed: null
    language: id
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Air force exercises, Rafale integration, air defense deployments."
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Indonesian government communications are systematically positive and omission-heavy. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage.

- **Presiden RI / Setkab**: Cross-reference presidential statements against same-day reporting in Kompas and Tempo. Setkab readouts of cabinet meetings frequently contain policy directives that Detik and CNN Indonesia report at headline level without the regulatory detail. When Setkab and Kompas framing diverges, it signals elite discomfort with the policy direction.
- **Kemlu**: Diplomatic press releases should be triangulated with The Jakarta Post (diplomatic community perspective), Republika (Islamic constituency reaction on OIC/Palestine/Muslim-bilateral issues), and CSIS Jakarta (analytical depth). When Kemlu and Republika framing diverges on a bilateral relationship (e.g., China, Saudi Arabia), it signals tension between foreign policy establishment preferences and Islamic constituency demands.
- **Kemhan / TNI**: Military bulletins report exercises, cooperation agreements, and ceremonies but never procurement costs, operational setbacks, or Papua security casualties. Cross-reference with Tempo (investigative military coverage — the only outlet that intermittently penetrates this space), indonesiadefense.com (defense industry analysis), and IISS/Janes (external defense assessment). The frequency and partner-country composition of joint exercise announcements on tni.mil.id is itself an alignment indicator.
- **Bank Indonesia**: Monetary policy decisions are technically rigorous and less subject to political distortion, but the selection of forward guidance language and emphasis reflects institutional positioning vis-a-vis the executive. Cross-reference BI-Rate decisions with CNBC Indonesia (market interpretation), Kontan (banking sector impact), and Bisnis Indonesia (real economy effects).
- **Kemenkeu**: Fiscal data is generally reliable in headline numbers but presentation framing (base period selection, seasonal adjustment, definition of "efficiency savings") can obscure trends. Cross-reference with Kontan and CNBC Indonesia for independent fiscal analysis. Sri Mulyani's press conferences are particularly valuable as she speaks with unusual candor for an Indonesian minister.
- **Kemendag**: Trade data is reliable but policy framing systematically overstates success ("surplus achievement") while underplaying vulnerability (commodity price dependence, single-market concentration). Cross-reference with Bisnis Indonesia (supply chain detail) and Bloomberg/Reuters (international trade friction reporting).
- **Pertamina / Danantara**: State enterprise and sovereign wealth fund communications systematically overstate achievements and understate governance problems. Pertamina production targets should be cross-referenced with Platts/Argus (independent production data) and Tempo/Tirto.id (investigative reporting on mega-refinery delays). Danantara governance claims should be cross-referenced with Bloomberg (March 2026 long-form investigation), East Asia Forum (governance analysis), and Kompas/Tempo (SOE asset management scrutiny).

**4.2 The decentralization challenge**

Unlike Mexico's unified gob.mx platform, Indonesia's government web infrastructure is fully decentralized across dozens of independent domains and technology stacks. This creates several operational implications:

- Each source requires a bespoke scraper or at minimum a distinct configuration profile
- Technology stacks range from WordPress (Setkab, Kemhan, E-Media DPR, Presiden RI) to ASP.NET (Bank Indonesia, OJK) to custom JavaScript SPAs (Kemlu) to legacy HTML (TNI)
- Outages are source-specific rather than platform-wide — a single infrastructure failure will not disable all government monitoring
- No shared bot protection pattern — each site has its own access control mechanisms
- URL patterns, pagination schemes, and content structures are entirely heterogeneous

The WordPress-based sites (Setkab, Presiden RI, Kemhan, E-Media DPR) offer the most consistent extraction opportunity, as they may all expose `/feed/` RSS endpoints and follow standard WordPress HTML templates.

**4.3 The BIN silence problem**

Indonesia's intelligence agency (BIN) produces effectively zero public communications. This is more extreme than Mexico's CNI — BIN's website actively rejects automated access and contains almost no substantive content. Intelligence-relevant signals surface through:
- Leaks to investigative media (Tempo, Tirto.id)
- Setkab readouts that reference "intelligence assessments" or "threat briefings" in cabinet meeting contexts
- Kemenko Polhukam (Coordinating Ministry for Political, Legal, and Security Affairs) communications referencing inter-agency security coordination
- DPR Commission I proceedings where BIN Director testifies (reported via E-Media DPR)
- Changes in BIN leadership, organizational structure, or budget (surfaced via JDIH regulatory publications)

The pipeline should not allocate significant resources to polling BIN's website but should flag any new publication as a high-priority anomaly.

**4.4 The Bahasa Indonesia barrier**

All government sources except Danantara and Pertamina publish primarily in Bahasa Indonesia. English translations exist on Setkab (`/en/`), Kemlu (select releases), Bank Indonesia (`/en/`), and OJK (`/en/`), but these lag by hours to days and cover only a subset of releases. The pipeline must process Bahasa Indonesia text natively. Key implications:
- Machine translation (Google Translate, DeepL) handles Bahasa Indonesia adequately for headline triage but struggles with bureaucratic/legal Indonesian (e.g., "penyelenggaraan pemerintahan daerah dalam rangka percepatan pembangunan" — local governance implementation in the framework of accelerated development)
- Localized query vocabulary from the Source Intelligence Map (Section: Localized Query Vocabulary) must be applied to government source extraction
- Acronym density in Indonesian government communications is extremely high (APBN, RPJMN, RKAKL, DIPA, etc.) — the pipeline should maintain an Indonesian government acronym dictionary

**4.5 Legislative gap: committee proceedings**

The existing Source Intelligence Map identifies parliamentary transcripts as a monitoring opportunity. DPR Commission I (Defense, Foreign Affairs, Information) hearings include testimony from Kemhan, Kemlu, TNI, and BIN officials that no media outlet fully covers. However:
- Committee proceedings are published through E-Media DPR (RSS available) at headline level
- Full transcripts are not systematically published online — they appear in the Risalah Sidang (session minutes) which are intermittently accessible at `dpr.go.id`
- Priority monitoring: (a) Commission I sessions on defense procurement and foreign policy, (b) Commission XI sessions on fiscal/monetary policy (BI/OJK testimony), (c) Budget Committee (Badan Anggaran) sessions during RAPBN review (August-October)

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Technology Stack Diversity

Indonesia's government sources span five distinct technology stacks, requiring different extraction approaches:

| Stack | Sources | Extraction Approach |
|---|---|---|
| **WordPress** | Setkab, Presiden RI, Kemhan, E-Media DPR | RSS feed polling (preferred) + HTML scraping fallback. Standard WordPress `/feed/` endpoint. |
| **JavaScript SPA** | Kemlu, Kemenkeu | Headless browser (Playwright/Puppeteer). Standard HTTP returns loading screens only. API endpoint discovery may yield JSON feeds. |
| **ASP.NET** | Bank Indonesia, OJK | ViewState-aware scraping. Handle postback patterns and session state. Socket timeout resilience required. |
| **Custom HTML** | TNI (.mil.id sites), Setneg, MPR, Kemendag, Kemenko Perekonomian | Standard HTML scraping. SSL certificate issues on .mil.id domains. Bot protection varies by site. |
| **Modern web** | Pertamina (Azure), Danantara | Standard HTML scraping. Clean, well-structured markup. |

### 5.2 RSS-Enabled Sources (Priority for Automation)

Only two government sources have confirmed functional RSS feeds:

1. **Setkab (Cabinet Secretariat)**: `https://setkab.go.id/feed/` — confirmed RSS 2.0. Delivers full article content with timestamps. This is the single most automation-friendly and highest-value Indonesian government source.

2. **E-Media DPR RI (Parliament)**: `https://emedia.dpr.go.id/feed/` — confirmed RSS 2.0. Title: "E-Media DPR RI — Pusat Pemberitaan Parlemen." Updated hourly during session periods.

**Probable RSS sources** (WordPress sites where `/feed/` likely exists but is unconfirmed):
- `presidenri.go.id/feed/` — WordPress-based, feed likely functional
- `kemhan.go.id/feed/` — WordPress-based, feed likely functional

All other sources require HTML scraping, headless browser rendering, or periodic page polling.

### 5.3 PDF Extraction Requirements

Three sources publish primarily or substantially in PDF:
- **JDIH / Peraturan.go.id**: All laws and regulations are PDF. Text-based PDFs (post-2010); older documents may be scanned images requiring OCR.
- **Bank Indonesia**: Monetary policy decisions, minutes, and quarterly reports are multi-page PDF. Well-structured, text-based.
- **Kemenkeu**: Statistical annexes to press releases are PDF with tables. May require table extraction (tabula/camelot).

### 5.4 Language and Encoding

All government sources publish in Bahasa Indonesia as the primary language. English availability:

| Source | English Availability |
|---|---|
| Setkab | Partial — `setkab.go.id/en/` (lagging subset) |
| Kemlu | Partial — select releases at `/portal/en/` |
| Bank Indonesia | Comprehensive — `bi.go.id/en/` (parallel content) |
| OJK | Partial — `ojk.go.id/en/` |
| Pertamina | Full — bilingual site |
| Danantara | Full — English-first site |
| All others | Indonesian only (some with Google Translate widget) |

All sites serve UTF-8 encoded content. The `.mil.id` military sites may have encoding inconsistencies — normalize to UTF-8 on ingestion.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A presidential regulation appears in Presiden RI, Setkab, and JDIH/Peraturan.go.id
- Cabinet meeting outcomes appear in Setkab, Setneg, and line ministry sites
- Defense cooperation agreements appear in Kemhan, TNI, and Kemlu
- Economic policy announcements appear in Kemenko Perekonomian, Kemenkeu, and Kemendag
- Trade agreement actions appear in Kemlu, Kemendag, and Kemenko Perekonomian

Implement content-hash deduplication. Use the JDIH/Peraturan.go.id publication as the canonical version for legal texts. Use the originating ministry (Kemlu for diplomatic, Kemhan for defense) as canonical for operational communications. Use Setkab as canonical for cabinet-level policy decisions.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Setkab (RSS), Kemlu, Presiden RI | Every 2 hours | Daily publication, policy-critical, cabinet decisions |
| P1-Standard | Kemhan, TNI (Mabes) | Every 4 hours | Less frequent but high-priority when published |
| P2-Active | DPR/E-Media (RSS), JDIH, Kemenkeu, BI, Kemendag, Pertamina, Danantara | Every 6 hours | Regular publishing schedule |
| P2-Low | Setneg, MPR, Kemenko Perekonomian, OJK, TNI branches | Every 12 hours | Important but slower publication cycle |
| P2-Minimal | BIN | Weekly | Effectively silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| WordPress site downtime | Setkab, Presiden RI, Kemhan, E-Media DPR | Monitor @setkabgoid, @Abordo_Kemhan on X. Setkab content often republished by Antara within minutes. |
| Kemlu SPA rendering failure | Kemlu | Monitor @kemabordo_ri on X and Instagram @kemlu_ri. Major diplomatic statements are simultaneously released to Antara wire. |
| TNI .mil.id SSL certificate issues | TNI, TNIAD, TNIAL, TNIAU | Antara's defense desk republishes Puspen TNI releases. Detik.com defense coverage is derived from TNI releases with minimal delay. |
| Bank Indonesia ASP.NET timeout | Bank Indonesia | BI-Rate decisions are simultaneously announced via press conference (covered by CNBC Indonesia, Kontan). English releases at bi.go.id/en/ may have different infrastructure path. |
| Kemenkeu JavaScript rendering failure | Kemenkeu | Monitor fiskal.kemenkeu.go.id (Fiscal Policy Agency) as alternative entry point. CNBC Indonesia and Kontan publish Kemenkeu releases near-simultaneously. |
| BIN access rejection | BIN | Expected state — BIN rejects most automated access. No viable fallback; intelligence signals come through media leaks, not BIN publications. |
| Kemendag "Request Rejected" | Kemendag | Rotate User-Agent headers and request intervals. Alternative: Kemenko Perekonomian (ekon.go.id) often publishes overlapping trade policy announcements. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of Indonesian government web infrastructure, change in cabinet composition (which typically triggers ministry domain/content reorganization), or creation/dissolution of government agencies (e.g., further evolution of Danantara's institutional structure or any Kemenko reorganization under the Prabowo administration).*
