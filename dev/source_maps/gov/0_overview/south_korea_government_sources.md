# Official Government Sources Supplement: SOUTH KOREA

**Primary language of political discourse: Korean (한국어)**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — South Korea (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for South Korea. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

South Korean government web infrastructure is decentralized — unlike Mexico's unified gob.mx platform, each ROK ministry and agency maintains independent web domains under the `.go.kr` (government) or `.mil.kr` (military) top-level namespace. Most ministries operate parallel Korean-language and English-language portals, with the English versions typically hosted on `english.{agency}.go.kr` or `eng.{agency}.go.kr` subdomains. English-language content is substantive but delayed: official statements and press releases appear in Korean first, with English translations following hours to days later. The Korea Culture and Information Service (KOCIS) operates `korea.net` as a centralized English-language aggregation portal that republishes press releases from across government, providing a single ingestion point at the cost of some latency. MOFA is the only ministry confirmed to offer RSS feeds on its Korean-language press pages. The Bank of Korea's ECOS statistical system provides structured data access but not RSS.

---

## 1. OFFICIAL GOVERNMENT SOURCES: SOUTH KOREA

### 1.1 Head of Government — Office of the President (대통령실)

| Field | Detail |
|---|---|
| **Institution** | Office of the President of the Republic of Korea (대통령실) |
| **Domain** | `president.go.kr` (Korean) / `eng.president.go.kr` (English) |
| **Entry Point URL** | Korean: `https://www.president.go.kr/newsroom/briefing/` — English: `https://eng.president.go.kr/briefing` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Daily. Briefings, speeches, and press releases published same-day. Presidential schedule updated daily. |
| **Content Format** | HTML. Speeches and statements published as full-text HTML pages. Some attached PDFs for formal joint statements. Photo and video galleries in separate sections. |
| **Extraction Method** | HTML scraping of briefing listing pages. Korean and English portals have different URL structures but similar HTML templates. |
| **Editorial Orientation** | Official government position. Under President Lee Jae-myung, communications reflect the Democratic Party progressive agenda: engagement-oriented North Korea policy, recalibrated US alliance posture, and emphasis on multilateral diplomacy. |
| **Why This Source** | The single authoritative source for presidential statements, executive orders, summit readouts, and policy announcements. The briefing section carries the full text of presidential remarks, which frequently contain nuances not captured in media summaries. Presidential schedule reveals diplomatic meeting patterns. |
| **Access Notes** | No paywall. The site relocated from the Yongsan Presidential Office back to the Blue House (Cheong Wa Dae) complex in December 2025. Both Korean and English portals are accessible without authentication. Some pages may serve JavaScript-heavy content requiring headless browser rendering. |

**Additional entry points:**
- Presidential speeches: `https://www.president.go.kr/president/speeches/`
- Presidential schedule: `https://www.president.go.kr/president/calendar/`
- Card news (infographics): `https://www.president.go.kr/newsroom/card_news/`
- English briefing room: `https://eng.president.go.kr/briefing`

---

### 1.2 Foreign Ministry — Ministry of Foreign Affairs (외교부, MOFA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Foreign Affairs (외교부) |
| **Domain** | `mofa.go.kr` (Korean) / `mofa.go.kr/eng` (English) |
| **Entry Point URL** | English press releases: `https://www.mofa.go.kr/eng/brd/m_5676/list.do` — Korean press briefings: `https://www.mofa.go.kr/www/brd/m_4076/list.do` |
| **RSS/Atom Feed** | **Yes.** Korean press briefings: `http://www.mofa.go.kr/www/brd/rss.do?brdId=303` — Korean press releases: `http://www.mofa.go.kr/www/brd/rss.do?brdId=302` |
| **Language** | Korean (primary); English (comprehensive parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Comunicados issued for bilateral/multilateral meetings, treaty actions, consular emergencies, UN votes. |
| **Content Format** | HTML on both Korean and English portals. Formal diplomatic texts sometimes in PDF. The English portal follows a board-system URL pattern (`/eng/brd/m_{ID}/list.do`). |
| **Extraction Method** | RSS polling for Korean-language content (confirmed feeds). HTML scraping for English-language press releases (`/eng/brd/m_5676/list.do`). Board-system pagination via `pageNo` query parameter. |
| **Editorial Orientation** | Official foreign ministry position. Under the Lee Jae-myung administration, framing reflects a "balanced diplomacy" doctrine — maintaining the US alliance while pursuing engagement with China and North Korea. IFANS (the ministry's think tank) publications preview analytical framing before official statements. |
| **Why This Source** | The only primary source for ROK formal diplomatic positions, treaty ratifications, ambassador appointments, and bilateral/multilateral meeting readouts. MOFA is one of only two ROK government sources confirmed to provide RSS feeds. Media coverage of MOFA activity is invariably derived from these releases. |
| **Access Notes** | No paywall, no authentication required. The English portal is comprehensive — most press releases are translated within 24 hours. RSS feeds are on the Korean-language portal (HTTP, not HTTPS — verify certificate handling). |

**Additional entry points:**
- English press briefings: `https://www.mofa.go.kr/eng/brd/m_5679/list.do`
- Minister's speeches: `https://www.mofa.go.kr/eng/brd/m_5689/list.do`
- Vice Ministers' speeches: `https://www.mofa.go.kr/eng/brd/m_5690/list.do`
- Diplomatic White Paper: `https://www.mofa.go.kr/eng/brd/m_5684/list.do`
- Ministry News: `https://www.mofa.go.kr/eng/brd/m_5674/list.do`
- RSS information page: `https://www.mofa.go.kr/eng/wpge/m_20360/contents.do`

---

### 1.3 Defense / Security — Ministry of National Defense (국방부, MND) and Joint Chiefs of Staff (합참, JCS)

#### 1.3a Ministry of National Defense (MND)

| Field | Detail |
|---|---|
| **Institution** | Ministry of National Defense (국방부) |
| **Domain** | `mnd.go.kr` (Korean) / `mnd.go.kr/mbshome/mbs/mndEN/` (English) |
| **Entry Point URL** | Korean press: `https://www.mnd.go.kr/mbshome/mbs/mnd/subview.jsp?id=mnd_010701000000` — English news: `https://www.mnd.go.kr/user/boardList.action?command=view&page=1&boardId=O_47261&boardSeq=O_395756&id=mndEN_020100000000` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (parallel portal with reduced coverage) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Press releases cover alliance exercises, defense procurement, policy announcements, and personnel changes. Higher frequency during combined exercise periods (Ulchi Freedom Shield, Freedom Edge). |
| **Content Format** | HTML (board-system pages). MND White Paper published biennially as downloadable PDF. |
| **Extraction Method** | HTML scraping of board listing pages. The Korean portal uses a JSP-based board system with different URL patterns from the English portal's `boardList.action` structure. |
| **Editorial Orientation** | Official defense policy position. Under the Lee administration, communications reflect a more measured approach to alliance burden-sharing and greater emphasis on diplomatic solutions to North Korea. Defense reform continues as an institutional priority regardless of administration. |
| **Why This Source** | Primary source for ROK defense policy announcements, alliance exercise schedules, force posture changes, and defense procurement decisions. The biennial Defense White Paper is the most comprehensive public assessment of the North Korean threat. |
| **Access Notes** | Both portals accessible without authentication. The English portal is substantially less comprehensive than Korean — major policy announcements may appear in Korean only. Site can be slow to respond and may timeout. |

**Additional entry points:**
- MND Defense White Paper (English PDF): available through the English portal publications section
- MND spokesperson briefings: published on the Korean press page
- Seoul Defense Dialogue: event-specific communications during annual conference

#### 1.3b Joint Chiefs of Staff (JCS)

| Field | Detail |
|---|---|
| **Institution** | Joint Chiefs of Staff (합동참모본부) |
| **Domain** | `jcs.mil.kr` |
| **Entry Point URL** | English news: `https://www.jcs.mil.kr/user/boardList.action?command=view&page=1&boardId=O_122667&id=jcs2_eng_030000000000` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (limited) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 2-5 per week. Communications cover joint exercises, North Korean provocations (missile launches, GPS jamming, border incursions), and alliance coordination. Frequency spikes during security incidents. |
| **Content Format** | HTML (board-system pages). |
| **Extraction Method** | HTML scraping of board listing pages. The `.mil.kr` domain may have stricter access controls than `.go.kr` domains. |
| **Editorial Orientation** | Official military operational communication. JCS releases on North Korean provocations are the fastest official ROK response — typically within 30-60 minutes of a missile launch or border incident. |
| **Why This Source** | JCS is the first official source to confirm and characterize North Korean military provocations. Its statements set the initial framing for all subsequent media coverage and government response. During provocations, JCS releases provide technical details (missile type, trajectory, range) before any other source. |
| **Access Notes** | The `.mil.kr` domain may have access restrictions or more aggressive bot protection than civilian `.go.kr` sites. English content is limited to major announcements. Verify accessibility from non-Korean IP addresses. |

---

### 1.4 Parliament — National Assembly (국회)

| Field | Detail |
|---|---|
| **Institution** | National Assembly of the Republic of Korea (대한민국 국회) |
| **Domain** | `assembly.go.kr` / `korea.assembly.go.kr` |
| **Entry Point URL** | Main portal: `https://korea.assembly.go.kr:447/portalEn/main/main.do` (English) — Open Assembly: `https://open.assembly.go.kr` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (institutional portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods (September-December regular session; extraordinary sessions as convened). Reduced during recess. |
| **Content Format** | HTML. Legislative texts published as HTML and PDF. Committee proceedings in stenographic format (Korean only). |
| **Extraction Method** | HTML scraping. The main portal uses NetFunnel traffic management (JavaScript-based queue system) that may require headless browser rendering. Open Assembly (`open.assembly.go.kr`) provides a more accessible data interface. |
| **Editorial Orientation** | Institutional. Proceedings reflect the current National Assembly composition — Democratic Party majority under the 22nd National Assembly (2024-2028). Committee hearing transcripts are verbatim. |
| **Why This Source** | Treaty ratifications, defense budget approvals, and NIS oversight hearings originate here. Committee testimony from MOFA, MND, and NIS officials frequently surfaces intelligence assessments and policy positions not available through ministry press releases. The National Assembly's consent is constitutionally required for troop deployments abroad, defense agreements, and major treaty actions. |
| **Access Notes** | The main portal uses a traffic management system that may block automated access. Open Assembly provides an alternative access path. The site runs on non-standard port 447 for HTTPS. English-language content is limited to institutional information and selected bill summaries. |

**Additional entry points:**
- National Assembly Secretariat: `https://korea.assembly.go.kr/secretary/main/main.do`
- National Assembly Library (research service): `https://www.nanet.go.kr/english/`
- National Assembly Budget Office: `https://korea.nabo.go.kr/`
- Legislative Information System (LIKMS): `https://likms.assembly.go.kr/` [VERIFY URL]
- Bill information system: accessible through Open Assembly portal

---

### 1.5 Official Gazette — Gwanbo (관보)

| Field | Detail |
|---|---|
| **Institution** | Electronic Official Gazette (전자관보) — administered by Ministry of the Interior and Safety (MOIS) |
| **Domain** | `gwanbo.mois.go.kr` / `gwanbo.go.kr` |
| **Entry Point URL** | `https://gwanbo.mois.go.kr/` — Open data portal: `https://open.gwanbo.go.kr/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Gwanbo is the constitutional publication vehicle for all laws, presidential decrees, ministerial ordinances, and public notices |
| **Publication Frequency** | Daily (weekdays). Special editions (호외) for urgent promulgations. |
| **Content Format** | PDF. Each daily edition is published as a downloadable PDF document. Individual entries are indexed on the web portal. |
| **Extraction Method** | HTML scraping of the daily index page to identify new publications, then PDF download and text extraction. The Open Gwanbo portal (`open.gwanbo.go.kr`) may provide a more structured interface. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law, presidential decrees, and government notices. |
| **Why This Source** | Constitutional requirement: no law, presidential decree, or ministerial ordinance takes legal effect until published in the Gwanbo. This is the only source providing definitive, timestamped legal text. Treaty promulgations, defense-related presidential decrees, and trade regulation changes all appear here. Media reports on legislation are downstream of Gwanbo publication. |
| **Access Notes** | Korean-language only. No English translation of gazette content. The site may be slow or timeout. PDF extraction quality is generally good as documents are text-based rather than scanned. The MOIS administers the gazette — organizational changes at MOIS affect gazette operations. |

---

### 1.6 Finance Ministry — Ministry of Economy and Finance (기획재정부, MOEF)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Economy and Finance (기획재정부) |
| **Domain** | `moef.go.kr` (Korean) / `english.moef.go.kr` (English) |
| **Entry Point URL** | English press releases: `https://english.moef.go.kr/pc/selectTbPressCenterList.do?boardCd=N0001` — Korean press center: `https://www.moef.go.kr/nw/nes/nesdta.do` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (comprehensive parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 5-10 per week. Press releases cover fiscal policy, tax reform, budget execution, public debt management, economic forecasts, and international economic cooperation (G20, OECD, IMF Article IV). |
| **Content Format** | HTML. Many press releases link to PDF attachments containing statistical tables, budget documents, and economic outlook reports. English press releases are comprehensive — MOEF translates most major announcements. |
| **Extraction Method** | HTML scraping of the press center listing page. English portal uses a board-system URL pattern with `boardCd` parameter. |
| **Editorial Orientation** | Official fiscal policy position. The Deputy Prime Minister for Economy doubles as MOEF Minister, making MOEF communications the highest-level economic policy voice. Data-heavy, technically rigorous. |
| **Why This Source** | Primary source for ROK fiscal policy, budget execution data, sovereign debt management, economic outlook assessments, and Korea's positions in international economic forums. MOEF press releases on FX policy, capital market opening, and sovereign credit management are market-moving. Essential for the Economic & Technological Statecraft domain. |
| **Access Notes** | English portal is one of the most comprehensive English-language government sites in ROK. No paywall. MOEF maintains an active English-language X/Twitter presence at @moefkorea_eng. The site may occasionally serve connection-refused errors. |

**Additional entry points:**
- MOEF policy briefings: accessible through the Korean portal press center
- Korea Development Institute (KDI — MOEF-affiliated think tank): `https://www.kdi.re.kr/eng/`
- KDI Economic Outlook: `https://www.kdi.re.kr/eng/research/economy`

---

### 1.7 Central Bank — Bank of Korea (한국은행, BOK)

| Field | Detail |
|---|---|
| **Institution** | Bank of Korea (한국은행) |
| **Domain** | `bok.or.kr` (Korean) / `bok.or.kr/eng` (English) |
| **Entry Point URL** | English press releases: `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400423` — Monetary policy decisions: `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400022` |
| **RSS/Atom Feed** | None confirmed on the main web portal. [VERIFY — check Korean portal for RSS] |
| **Language** | Korean (primary); English (comprehensive parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (scheduled, typically Thursdays). Press releases: 3-5 per week. Financial Stability Report and Monetary Policy Report: quarterly. Economic Outlook: semi-annual. |
| **Content Format** | HTML for news listings. PDF for formal monetary policy decisions, minutes, and reports. The English portal uses a `newsDataEng` board system with `menuNo` parameters for section navigation. |
| **Extraction Method** | HTML scraping of board listing pages. PDF download and text extraction for formal publications. The ECOS statistical database (`https://ecos.bok.or.kr/#/?langCd=en`) provides structured economic data via a separate interface. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and policy-neutral by institutional mandate. BOK's independence is constitutionally protected but politically tested — the Lee administration's growth-oriented economic agenda creates tension with BOK's inflation mandate. |
| **Why This Source** | BOK is the sole authoritative source for monetary policy decisions, official economic forecasts, FX reserves data, and financial stability assessments. Monetary policy announcements move Korean and regional markets. BOK's assessment of economic conditions frequently diverges from MOEF's more optimistic framing, making cross-referencing essential. |
| **Access Notes** | No paywall. No known bot protection. English portal is among the most comprehensive central bank English sites in Asia. Statistical calendar at `https://www.bok.or.kr/eng/stats/statsPublictSchdul/listCldr.do?menuNo=400359` provides advance publication scheduling. ECOS data system provides API-style access to economic statistics. |

**Key publication sections (English):**

| Section | URL |
|---|---|
| Press Releases | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400423` |
| Monetary Policy Decisions | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400022` |
| Minutes of Monetary Policy Board | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400021` |
| BOK Issue Notes | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400409` |
| Monetary Policy Report | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400215` |
| Financial Stability Report | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400219` |
| Korea Economic Outlook | `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400413` |
| ECOS (statistics) | `https://ecos.bok.or.kr/#/?langCd=en` |

---

### 1.8 Trade / Commerce — Ministry of Trade, Industry and Resources (산업통상자원부, MOTIR, formerly MOTIE)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Trade, Industry and Resources (산업통상자원부) — renamed from Ministry of Trade, Industry and Energy (MOTIE) in 2025 after the energy portfolio was transferred to the Ministry of Climate, Energy and Environment |
| **Domain** | `motir.go.kr` (Korean) / `english.motir.go.kr` (English) — legacy: `motie.go.kr` / `english.motie.go.kr` |
| **Entry Point URL** | English portal: `https://english.motir.go.kr/` — English press releases: `https://english.motir.go.kr/eng/article/EATCL{articleId}` [VERIFY URL pattern] |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 3-5 per week. Communications cover trade negotiations, export/import data, FDI announcements, semiconductor/battery supply chain policy, FTA implementation, and industrial policy. Monthly trade statistics published within the first 10 days of each month. |
| **Content Format** | HTML. Trade statistics and reports in PDF. Monthly trade data summaries frequently include infographic images. |
| **Extraction Method** | HTML scraping of the press release listing pages. The domain transition from MOTIE to MOTIR may cause legacy URL issues — verify which domain is canonical. |
| **Editorial Orientation** | Official trade and industrial policy position. Under the Lee administration, emphasis on supply chain resilience, semiconductor sovereignty, and maintaining trade relationships with both the US and China. The ministry's messaging on US export controls affecting Korean chipmakers is politically sensitive. |
| **Why This Source** | Primary source for ROK trade policy, monthly trade statistics (Korea is the world's 6th largest exporter), FTA negotiations, semiconductor industry policy, and defense export data. Monthly trade data is a leading economic indicator closely watched by regional markets. The K-CHIPS Act implementation and supply chain diversification policies are tracked here. |
| **Access Notes** | The ministry was reorganized in 2025: energy functions moved to the new Ministry of Climate, Energy and Environment. The legacy `motie.go.kr` domain may still redirect. English portal content is substantive but may lag Korean releases. MOTIR maintains an English-language social media presence. |

**Additional entry points:**
- Korean Free Trade Zone portal: `https://www.motie.go.kr/kftz/en/index.do` [VERIFY — may redirect to MOTIR]
- KOTRA (Korea Trade-Investment Promotion Agency): `https://www.kotra.or.kr/english/`
- KITA (Korea International Trade Association): `https://www.kita.org/`

---

### 1.9 Intelligence / National Security — National Intelligence Service (국가정보원, NIS) and National Security Council (NSC)

#### 1.9a National Intelligence Service (NIS)

| Field | Detail |
|---|---|
| **Institution** | National Intelligence Service (국가정보원) |
| **Domain** | `nis.go.kr` (Korean) / `eng.nis.go.kr` (English) |
| **Entry Point URL** | English portal: `https://eng.nis.go.kr/` — Notices: `https://eng.nis.go.kr/ECM/1_3_1.do` |
| **RSS/Atom Feed** | None available. |
| **Language** | Korean (primary); English (institutional portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Negligible for press releases. Cyber security advisories published intermittently through the National Cyber Security Center (NCSC). Institutional announcements (recruitment, organizational) published occasionally. |
| **Content Format** | HTML. Cyber security publications in PDF. |
| **Extraction Method** | Periodic check of notice pages. NCSC portal (`https://www.ncsc.go.kr/eng/mainPage.do`) for cybersecurity advisories. |
| **Editorial Orientation** | Effectively silent on intelligence matters. Public communications are limited to cybersecurity advisories, counter-espionage awareness campaigns, and institutional information. |
| **Why This Source** | Included for completeness. NIS produces almost no public operational communications. Its real intelligence value surfaces through: (a) NIS director's closed-door National Assembly Intelligence Committee briefings, which are partially leaked to media; (b) cybersecurity advisories from NCSC; (c) institutional changes (budget, organization) published in the Gwanbo. Under the Lee administration, NIS is expected to refocus from domestic political surveillance toward foreign intelligence, which may marginally increase public-facing analytical output. |
| **Access Notes** | The English portal provides institutional information, descriptions of major duties (counter-intelligence, counter-terrorism, North Korea intelligence, cyber security, space security), and center descriptions. No press release section exists. The site is accessible from non-Korean IP addresses. |

**Associated centers (under NIS):**
- National Cyber Security Center (NCSC): `https://www.ncsc.go.kr/eng/mainPage.do`
- National Industrial Security Center
- Terrorism Information Integration Center
- National AI Security Center

#### 1.9b National Security Council (NSC) / Office of National Security (국가안보실)

| Field | Detail |
|---|---|
| **Institution** | National Security Council (국가안보회의) / Office of National Security (국가안보실) |
| **Domain** | No independent website. NSC communications are issued through the Presidential Office (`president.go.kr`). |
| **Entry Point URL** | NSC statements published via Presidential Office briefings: `https://www.president.go.kr/newsroom/briefing/` |
| **RSS/Atom Feed** | None (uses Presidential Office infrastructure). |
| **Language** | Korean (primary); English via Presidential Office English portal |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Event-driven. NSC convenes in response to North Korean provocations, regional security incidents, or major diplomatic developments. Readouts are issued through the Presidential Office within hours. |
| **Content Format** | HTML (Presidential Office briefing format). |
| **Extraction Method** | NSC readouts are captured through Presidential Office monitoring (section 1.1). No separate extraction needed. |
| **Editorial Orientation** | Reflects the President's national security posture. NSC readouts reveal the government's initial characterization of security events, which sets the tone for subsequent MND and MOFA responses. |
| **Why This Source** | NSC emergency meetings are the highest-level security coordination mechanism. Readouts from NSC sessions — typically identifying which officials attended and what decisions were made — are the earliest indicator of how the government will respond to security events. The speed of NSC convening (minutes vs. hours after a provocation) itself signals threat assessment severity. |
| **Access Notes** | No separate infrastructure to monitor. NSC readouts are a subset of Presidential Office communications. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Ministry of Unification (통일부)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Unification (통일부) |
| **Domain** | `unikorea.go.kr` (Korean) / `unikorea.go.kr/web/eng_unikorea/` (English) |
| **Entry Point URL** | English press releases: `https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000034` — English press briefings: `https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000035` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (comprehensive parallel portal) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | 3-5 per week. Regular spokesperson briefings. Policy announcements on inter-Korean relations, North Korean human rights, and unification policy. |
| **Content Format** | HTML. Board-system pages with sequential article IDs. Policy papers and annual work plans in PDF. |
| **Extraction Method** | HTML scraping of board listing pages. URL pattern: `/web/eng_unikorea/bbs/bbs_{boardId}/{articleId}`. Pagination via `cp` query parameter. |
| **Editorial Orientation** | Official unification/inter-Korean policy position. Under the Lee Jae-myung administration, the ministry has adopted a "peaceful coexistence" framework — explicitly stating principles of respecting the North's existing system, not pursuing unification by absorption, and not engaging in hostile acts. This represents a significant policy shift from the Yoon era. |
| **Why This Source** | South Korea-specific institution with no equivalent elsewhere. MOU is the primary source for inter-Korean policy, North Korean human rights positions, defector/refugee statistics, and the government's official assessment of inter-Korean relations. Changes in MOU messaging are the earliest indicators of shifts in Seoul's approach to Pyongyang. The MOU spokesperson's regular briefings provide the most granular inter-Korean policy commentary available. |
| **Access Notes** | English portal is well-maintained with regular press release translations. No paywall. The ministry hosts the annual Global Korea Forum on Korean Peninsula issues. |

**Additional entry points:**
- MOU News: `https://unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000167`
- North Korean Human Rights reports: published periodically through the press releases section
- Annual work plan: published each December/January

#### 1.10b Korea Culture and Information Service (KOCIS) / Korea.net

| Field | Detail |
|---|---|
| **Institution** | Korea Culture and Information Service (해외문화홍보원, KOCIS) — under Ministry of Culture, Sports and Tourism |
| **Domain** | `korea.net` |
| **Entry Point URL** | Press releases: `https://www.korea.net/Government/Briefing-Room/Press-Releases` |
| **RSS/Atom Feed** | **Yes.** RSS service page: `https://www.korea.net/Others/Subscribe-to-Koreanet/RSS-Service` [VERIFY individual feed URLs — site returned 403 during verification] |
| **Language** | English (primary); also available in Chinese, Japanese, Spanish, French, Arabic, Vietnamese, and other languages |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Economic & technological statecraft, Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily. Aggregates press releases from across all government ministries. Also publishes original feature articles and policy explainers. |
| **Content Format** | HTML. Press releases follow a standardized template with ministry attribution. |
| **Extraction Method** | RSS polling (if feeds verified as functional). HTML scraping of the press releases listing page. Articles are attributed to originating ministries via `insttCode` parameter. |
| **Editorial Orientation** | Government-aligned public diplomacy outlet. KOCIS's mandate is to "enhance Korea's national image" — content is systematically positive and promotional. However, its press releases section faithfully republishes ministry communications, making it a valuable single-ingestion-point for cross-government monitoring. |
| **Why This Source** | Korea.net is the single most efficient English-language ingestion point for ROK government communications. Rather than scraping 10+ ministry portals individually, monitoring Korea.net captures press releases from MOFA, MND, MOEF, MOTIR, MOU, and others in a single feed. The tradeoff is some latency (hours to a day behind ministry originals) and the absence of ministry-specific context. |
| **Access Notes** | The RSS service page exists but returned 403 during verification — the feeds may require specific User-Agent headers or may be intermittently unavailable. HTML scraping of the press releases page is a reliable fallback. No paywall. |

#### 1.10c Defense Acquisition Program Administration (방위사업청, DAPA)

| Field | Detail |
|---|---|
| **Institution** | Defense Acquisition Program Administration (방위사업청) |
| **Domain** | `dapa.go.kr` (Korean) / `dapa.go.kr/dapa_en` (English) |
| **Entry Point URL** | English portal: `https://www.dapa.go.kr/dapa_en/main.do` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); English (limited portal) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | 2-4 per week. Announcements cover defense procurement contracts, indigenous weapons development milestones (KF-21 fighter, SLBM, Hyunmoo missiles), arms export agreements, and defense industry policy. |
| **Content Format** | HTML. Procurement announcements and contract details sometimes in PDF. |
| **Extraction Method** | HTML scraping. The English portal is less comprehensive than Korean — major procurement announcements require Korean-language monitoring. |
| **Editorial Orientation** | Official defense acquisition position. DAPA communications emphasize indigenous capability development, defense export achievements, and procurement efficiency. |
| **Why This Source** | DAPA is the primary source for defense procurement decisions that directly indicate ROK defense-autonomy trajectory. Arms export contracts (K9 howitzer, FA-50 fighter, K2 tank), indigenous development programs (KF-21, next-gen submarine), and technology transfer agreements all surface through DAPA announcements. Korea's emergence as a top-10 arms exporter makes DAPA an increasingly important economic statecraft signal source. |
| **Access Notes** | English portal available but limited. Korean-language monitoring recommended for procurement-level detail. Accessible without authentication. |

#### 1.10d National Assembly Budget Office (국회예산정책처, NABO)

| Field | Detail |
|---|---|
| **Institution** | National Assembly Budget Office (국회예산정책처) |
| **Domain** | `nabo.go.kr` / `korea.nabo.go.kr` |
| **Entry Point URL** | `https://korea.nabo.go.kr/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Korean (primary); limited English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Monthly reports and analyses during budget season (September-December). Special reports on major spending programs. |
| **Content Format** | PDF reports. HTML summaries. |
| **Extraction Method** | HTML scraping of publications listing. PDF download for full reports. |
| **Editorial Orientation** | Non-partisan legislative analysis. NABO functions as the Korean equivalent of the US Congressional Budget Office — providing independent fiscal analysis to the National Assembly. |
| **Why This Source** | NABO's independent analysis of defense budgets, economic forecasts, and fiscal sustainability provides a critical counterpoint to MOEF's executive-branch framing. NABO cost estimates for defense programs and economic policy proposals are frequently at odds with government figures. |
| **Access Notes** | Primarily Korean-language. Selected reports available in English. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | English Portal |
|---|---|---|---|---|---|---|---|
| 1 | Presidential Office | `president.go.kr/newsroom/briefing/` | No | P1 | HTML | Daily | Yes (`eng.president.go.kr`) |
| 2 | MOFA | `mofa.go.kr/eng/brd/m_5676/list.do` | **Yes** (Korean) | P1 | HTML/PDF | Daily | Yes |
| 3a | MND | `mnd.go.kr/mbshome/mbs/mnd/subview.jsp?id=mnd_010701000000` | No | P1 | HTML/PDF | 3-7/week | Yes (limited) |
| 3b | JCS | `jcs.mil.kr/user/boardList.action?...` | No | P1 | HTML | 2-5/week | Yes (limited) |
| 4 | National Assembly | `korea.assembly.go.kr` / `open.assembly.go.kr` | No | P2 | HTML/PDF | Daily (session) | Yes (limited) |
| 5 | Gwanbo (Gazette) | `gwanbo.mois.go.kr` | No | P2 | PDF | Daily | No |
| 6 | MOEF | `english.moef.go.kr/pc/selectTbPressCenterList.do?boardCd=N0001` | No | P2 | HTML/PDF | 5-10/week | Yes |
| 7 | BOK | `bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400423` | No | P2 | HTML/PDF | Variable | Yes |
| 8 | MOTIR | `english.motir.go.kr/` | No | P2 | HTML/PDF | 3-5/week | Yes |
| 9a | NIS | `eng.nis.go.kr/` | No | P2 | HTML | Negligible | Yes (institutional only) |
| 9b | NSC | Via `president.go.kr` | No | P2 | HTML | Event-driven | Via Presidential Office |
| 10a | MOU | `unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000034` | No | P1 | HTML/PDF | 3-5/week | Yes |
| 10b | Korea.net (KOCIS) | `korea.net/Government/Briefing-Room/Press-Releases` | **Yes** [VERIFY] | P2 | HTML | Daily | English-primary |
| 10c | DAPA | `dapa.go.kr/dapa_en/main.do` | No | P2 | HTML/PDF | 2-4/week | Yes (limited) |
| 10d | NABO | `korea.nabo.go.kr/` | No | P2 | PDF/HTML | Monthly+ | Limited |

---

## 3. MONITORING CONFIGURATION

```yaml
# South Korea Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/kr.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: kr_presidential_office
    name: Office of the President (대통령실)
    domain: president.go.kr
    entry_url: "https://www.president.go.kr/newsroom/briefing/"
    entry_url_en: "https://eng.president.go.kr/briefing"
    rss_feed: null
    language: ko
    language_secondary: en
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
    notes: "Monitor both Korean and English portals. NSC readouts published here. JavaScript-heavy pages may require headless browser."

  - id: kr_mofa
    name: Ministry of Foreign Affairs (외교부)
    domain: mofa.go.kr
    entry_url: "https://www.mofa.go.kr/eng/brd/m_5676/list.do"
    entry_url_ko: "https://www.mofa.go.kr/www/brd/m_4076/list.do"
    rss_feed:
      press_briefings_ko: "http://www.mofa.go.kr/www/brd/rss.do?brdId=303"
      press_releases_ko: "http://www.mofa.go.kr/www/brd/rss.do?brdId=302"
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_and_html_scrape
    poll_interval_hours: 2
    notes: "RSS feeds available for Korean portal only (HTTP, not HTTPS). English press releases require HTML scraping. Board-system URL pattern: /eng/brd/m_{ID}/list.do."

  - id: kr_mnd
    name: Ministry of National Defense (국방부)
    domain: mnd.go.kr
    entry_url: "https://www.mnd.go.kr/mbshome/mbs/mnd/subview.jsp?id=mnd_010701000000"
    entry_url_en: "https://www.mnd.go.kr/mbshome/mbs/mndEN/"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "JSP-based board system. English portal has different URL structure from Korean. Site can be slow/timeout."

  - id: kr_jcs
    name: Joint Chiefs of Staff (합동참모본부)
    domain: jcs.mil.kr
    entry_url: "https://www.jcs.mil.kr/user/boardList.action?command=view&page=1&boardId=O_122667&id=jcs2_eng_030000000000"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "First official source for DPRK provocation responses. .mil.kr domain may have stricter access controls. Verify non-Korean IP access."

  - id: kr_mou
    name: Ministry of Unification (통일부)
    domain: unikorea.go.kr
    entry_url: "https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000034"
    entry_url_briefings: "https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000035"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 4
    notes: "South Korea-specific institution. Primary source for inter-Korean policy. Regular spokesperson briefings. Well-maintained English portal."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: kr_national_assembly
    name: National Assembly (국회)
    domain: assembly.go.kr
    entry_url: "https://korea.assembly.go.kr:447/portalEn/main/main.do"
    entry_url_open: "https://open.assembly.go.kr"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "NetFunnel traffic management may block automated access. Use open.assembly.go.kr as fallback. Non-standard HTTPS port 447."

  - id: kr_gwanbo
    name: Official Gazette (관보)
    domain: gwanbo.mois.go.kr
    entry_url: "https://gwanbo.mois.go.kr/"
    entry_url_open: "https://open.gwanbo.go.kr/"
    rss_feed: null
    language: ko
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
    notes: "Korean-only. All laws and presidential decrees published here. PDF text-based (not scanned). Open Gwanbo portal may be more automation-friendly."

  - id: kr_moef
    name: Ministry of Economy and Finance (기획재정부)
    domain: moef.go.kr
    entry_url: "https://english.moef.go.kr/pc/selectTbPressCenterList.do?boardCd=N0001"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "5-10_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Comprehensive English portal. Deputy PM doubles as MOEF Minister — highest-level economic policy voice. Active X/Twitter: @moefkorea_eng."

  - id: kr_bok
    name: Bank of Korea (한국은행)
    domain: bok.or.kr
    entry_url: "https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400423"
    entry_url_monetary_policy: "https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400022"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 6
    notes: "Monetary Policy Board meets 8 times/year. ECOS statistical database at ecos.bok.or.kr provides structured data. Statistical calendar available for advance scheduling."

  - id: kr_motir
    name: Ministry of Trade, Industry and Resources (산업통상자원부, formerly MOTIE)
    domain: motir.go.kr
    entry_url: "https://english.motir.go.kr/"
    entry_url_legacy: "https://english.motie.go.kr/eng/"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "3-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Renamed from MOTIE in 2025 (energy transferred to new ministry). Legacy motie.go.kr may redirect. Monthly trade statistics within first 10 days of month."

  - id: kr_nis
    name: National Intelligence Service (국가정보원)
    domain: nis.go.kr
    entry_url: "https://eng.nis.go.kr/"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent. NCSC (ncsc.go.kr) publishes cybersecurity advisories. Real NIS signal surfaces via leaked National Assembly Intelligence Committee briefings in media (Yonhap, Hankyoreh)."

  - id: kr_korea_net
    name: Korea.net (KOCIS)
    domain: korea.net
    entry_url: "https://www.korea.net/Government/Briefing-Room/Press-Releases"
    rss_feed: "https://www.korea.net/Others/Subscribe-to-Koreanet/RSS-Service"  # [VERIFY individual feed URLs]
    language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - economic_technological_statecraft
      - domestic_constraints
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 6
    notes: "Cross-government aggregation portal. Single English-language ingestion point for all ministry press releases. RSS may require specific headers (403 observed). Fallback to HTML scrape."

  - id: kr_dapa
    name: Defense Acquisition Program Administration (방위사업청)
    domain: dapa.go.kr
    entry_url: "https://www.dapa.go.kr/dapa_en/main.do"
    rss_feed: null
    language: ko
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "2-4_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Primary source for defense procurement and arms export contracts. English portal limited — Korean monitoring recommended for procurement detail."

  - id: kr_nabo
    name: National Assembly Budget Office (국회예산정책처)
    domain: nabo.go.kr
    entry_url: "https://korea.nabo.go.kr/"
    rss_feed: null
    language: ko
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: monthly_plus
    content_format: pdf
    extraction_method: pdf_download_extract
    poll_interval_hours: 24
    notes: "Independent fiscal analysis. Korean equivalent of US CBO. Peak activity during budget season (Sep-Dec)."

# Shared configuration notes
kr_shared_config:
  domain_pattern: "{agency}.go.kr (civilian) / {agency}.mil.kr (military)"
  board_system: "Most agencies use JSP-based board systems with pagination via pageNo/page query parameters"
  english_portals: "Most agencies maintain English portals at english.{agency}.go.kr or eng.{agency}.go.kr or {agency}.go.kr/eng"
  encoding: "UTF-8 throughout"
  bot_protection: "Generally minimal — Korean government sites rarely deploy aggressive bot protection. NetFunnel (National Assembly) and occasional CAPTCHA are exceptions."
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
  rate_limit: "max 1 request per 2 seconds per domain"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

South Korean government communications are more substantive and transparent than many peer countries but remain systematically selective in emphasis. The pipeline must never treat a government source as confirming objective reality — it confirms that the government has chosen to present a particular framing. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing and framing relative to independent media coverage.

- **Presidential Office**: Cross-reference presidential statements against same-day reporting in Yonhap (wire baseline), Korea Herald (centrist-conservative English interpretation), and Hankyoreh (progressive perspective). When Presidential Office framing diverges from Yonhap's characterization, it signals deliberate narrative construction. The Chosun Ilbo editorial board's response to presidential announcements is a proxy for conservative establishment reception.

- **MOFA**: Diplomatic press releases should be triangulated with Korea JoongAng Daily (conservative/alliance-focused interpretation), Hankyoreh English (progressive/engagement-focused interpretation), and The Diplomat (regional reception). When MOFA readouts of bilateral meetings diverge significantly from the counterpart government's readout, the gaps reveal negotiating positions and domestic audience framing. IFANS publications (Source Intelligence Map #10) often preview MOFA analytical framing weeks before official statements.

- **MND/JCS**: Defense communications report exercises, procurement, and policy positions but never reveal intelligence assessments, operational vulnerabilities, or alliance friction in detail. Cross-reference with NK News/NK Pro (North Korea threat context), 38 North (satellite imagery verification), and KIDA publications (Source Intelligence Map #11, defense institutional perspective). JCS provocation responses should be cross-referenced with US Forces Korea (USFK) and US Department of War releases to detect alliance coordination or messaging divergence.

- **MOU**: Unification Ministry framing on inter-Korean relations is the most politically charged of all ROK government communications. Under progressive administrations, MOU messaging emphasizes engagement possibilities; under conservatives, it emphasizes North Korean threats. Cross-reference with Korea Pro (analytical depth on inter-Korean dynamics), Chosun Ilbo (conservative establishment reaction), and Hankyoreh (progressive base alignment). MOU spokesperson briefings frequently contain conditional formulations ("if conditions are right...") that signal diplomatic feelers toward Pyongyang.

- **MOEF/BOK**: Cross-reference MOEF fiscal optimism against BOK's more conservative economic assessments. When MOEF and BOK diverge on growth forecasts, it reveals executive-central bank tension. KED Global and Seoul Economic Daily (Source Intelligence Map #12, #18) provide market interpretation. NABO's independent budget analysis provides the legislative counterpoint to MOEF framing, particularly on defense spending and social welfare tradeoffs.

- **MOTIR**: Trade data releases should be triangulated with KITA (Korea International Trade Association) analysis and KED Global reporting. Semiconductor and supply chain policy communications are particularly sensitive — MOTIR's framing on US export controls and China trade must be read against Korea Herald and Korea JoongAng Daily coverage to detect the gap between public positioning and private industry concerns.

- **DAPA**: Defense procurement announcements emphasize indigenous capability and export success. Cross-reference with KIDA (institutional defense analysis), Korea Economic Daily (financial/industrial dimension of defense exports), and Jane's Defence Weekly (independent technical assessment). DAPA arms export figures should be verified against SIPRI data for scale and significance.

**4.2 The decentralized infrastructure reality**

Unlike Mexico's centralized gob.mx platform, South Korea's government web infrastructure is fully decentralized — each ministry operates independent websites with different technologies (JSP board systems, custom CMS platforms, WordPress instances). This means:
- No single point of failure affects all sources
- No shared extraction pattern — each agency requires a custom scraper configuration
- Template changes at one agency do not propagate to others
- Publication timing is agency-autonomous (no central platform approval workflows)

Korea.net (KOCIS) partially compensates by aggregating press releases across government, but with latency and editorial curation that may filter out operationally relevant communications.

**4.3 The NIS intelligence gap**

South Korea's intelligence agency (NIS) produces almost no public communications, similar to Mexico's CNI. However, unlike Mexico, South Korea has an institutionalized mechanism for intelligence signal leakage: the National Assembly Intelligence Committee. NIS directors regularly brief this closed-door committee, and committee members — particularly from opposition parties — routinely leak key assessments to media. These leaks appear in:
- Yonhap News Agency (most reliable for accurate leak characterization)
- Hankyoreh (progressive perspective, often critical of NIS assessments)
- Chosun Ilbo (conservative perspective, often amplifying threat assessments)
- Korea Pro (analytical synthesis of leaked intelligence)

The pipeline should not allocate significant resources to polling NIS's website but should monitor media mentions of "국정원" (NIS) or "Intelligence Committee briefing" as high-priority trigger terms.

**4.4 The Korean-English language gap**

All ROK government sources publish in Korean first, with English translations following hours to days later. This creates a structural latency issue for English-only monitoring:
- Presidential Office: English translations of major speeches within 2-6 hours
- MOFA: English press releases typically same-day or next-day
- MND: English content significantly reduced compared to Korean portal
- MOU: Good English coverage but 12-24 hour delay
- MOEF: Comprehensive English with 6-12 hour delay
- MOTIR, DAPA, National Assembly: Limited English, significant delays

For time-sensitive monitoring (provocation responses, emergency NSC sessions, major policy announcements), Korean-language RSS from MOFA and direct Korean portal monitoring of the Presidential Office and JCS are essential. English-language sources (Korea.net, English ministry portals) function as confirmation and translation layers, not primary detection sources.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Extraction Architecture

Unlike Mexico's shared gob.mx template, South Korea requires agency-specific scraper modules. However, several common patterns emerge:

- **Board-system agencies** (MOFA, MND, BOK, MOU): Most ministries use JSP-based board systems with paginated listing pages. URL patterns typically include `boardId`, `menuNo`, or `brdId` parameters. Article URLs follow predictable patterns with sequential IDs.
- **Custom CMS agencies** (Presidential Office, MOEF): These use custom content management systems with different URL structures requiring dedicated scraper logic.
- **Military domain** (JCS): The `.mil.kr` domain may have access restrictions not present on `.go.kr` — test from multiple IP ranges and verify automated access capability.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Only two government sources provide confirmed or likely RSS feeds:

1. **MOFA** (confirmed): Two Korean-language RSS feeds — press briefings (`brdId=303`) and press releases (`brdId=302`). These are HTTP (not HTTPS) feeds — ensure the pipeline handles plaintext HTTP RSS correctly. These are the only confirmed government RSS feeds in the South Korea configuration and should be prioritized for automation.

2. **Korea.net / KOCIS** (likely): RSS service page exists at `korea.net/Others/Subscribe-to-Koreanet/RSS-Service` but returned 403 during verification. If functional, this would provide a single RSS endpoint aggregating across all government ministries in English. Verify with different User-Agent headers and from Korean IP ranges.

All other sources require HTML scraping with agency-specific configurations.

### 5.3 PDF Extraction Requirements

Three sources publish primarily or substantially in PDF:
- **Gwanbo (Official Gazette)**: All legal texts are PDF. Text-based (not scanned), good extraction quality. Korean-language only — machine translation pipeline required for analytical use.
- **BOK**: Monetary policy decisions, minutes, and major reports are multi-page PDF. Well-structured, text-based. Both Korean and English versions available.
- **NABO**: Independent budget analyses are published as PDF reports. Korean-language dominant.

### 5.4 Language and Encoding

All government sources publish in Korean (UTF-8). Most major ministries maintain English portals with substantive translations. Priority order for English-language government monitoring:
1. **Korea.net** — highest-volume English aggregation
2. **MOFA English** — most comprehensive individual ministry English portal
3. **MOEF English** — strong economic policy coverage
4. **BOK English** — comprehensive monetary/financial coverage
5. **MOU English** — good inter-Korean policy coverage

Korean-language monitoring is essential for: JCS provocation responses (minutes matter), Gwanbo (no English), DAPA procurement details, and National Assembly committee proceedings.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- A presidential statement appears in Presidential Office briefings, Korea.net, MOFA (if diplomatic), and Yonhap
- Defense-related announcements appear in MND, JCS, DAPA, and Korea.net
- Trade data appears in MOTIR, MOEF, Korea.net, and BOK publications
- Inter-Korean statements appear in MOU, Presidential Office, and MOFA

Implement content-hash deduplication. Use the originating ministry as the canonical version:
- MOFA for diplomatic communications
- MND/JCS for defense operations
- MOEF for fiscal/economic policy
- MOU for inter-Korean relations
- Presidential Office for presidential statements and NSC readouts

Korea.net should be treated as a secondary/confirmation source, not canonical.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Presidential Office, MOFA (RSS+scrape), JCS | Every 2 hours | Daily publication, policy-critical, provocation response |
| P1-Standard | MND, MOU | Every 4 hours | High priority but slightly lower frequency |
| P2-Active | MOEF, BOK, MOTIR, Korea.net, National Assembly | Every 6 hours | Regular publishing schedule |
| P2-Low | Gwanbo, DAPA, NABO | Every 12-24 hours | Important but slower publication cycle |
| P2-Minimal | NIS | Weekly | Effectively silent; flag any publication as anomaly |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| Individual ministry site outage | Single agency | Korea.net aggregates cross-government press releases in English. Yonhap carries verbatim government statements. |
| MOFA RSS feed failure | MOFA Korean-language monitoring | Fall back to HTML scraping of English press release listing at `/eng/brd/m_5676/list.do`. Korea.net also carries MOFA releases. |
| National Assembly NetFunnel blocking | National Assembly portal | Use `open.assembly.go.kr` as alternative access point. Yonhap National Assembly reporting captures most floor votes and committee outcomes. |
| JCS .mil.kr access restriction | JCS | Yonhap is the fastest media source for JCS provocation statements. USFK releases at `usfk.mil` provide allied perspective. Korea Herald and Korea JoongAng Daily carry JCS statements within minutes. |
| Korea.net RSS 403 errors | Korea.net aggregation | HTML scraping of the press releases listing page. Individual ministry English portals as direct alternatives. |
| Gwanbo site timeout | Official Gazette | National Library of Korea maintains an Official Gazette collection at `nl.go.kr/EN/contents/EN35300000000.do`. Legal databases (Korean Law Information Center) provide searchable law text. |
| BOK site maintenance | Bank of Korea | Bloomberg and Reuters carry BOK monetary policy decisions in real-time. KED Global provides same-day Korean-language interpretation. |

---

*This supplement should be reviewed quarterly or upon any major government restructuring, change in administration, or ministry reorganization (as occurred in 2025 with the MOTIE-to-MOTIR transition and creation of the Ministry of Climate, Energy and Environment).*
