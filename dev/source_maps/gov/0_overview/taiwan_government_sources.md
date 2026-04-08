# Official Government Sources Supplement: TAIWAN

**Primary language of political discourse: Mandarin Chinese (Traditional)**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — Taiwan (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Taiwan (Republic of China). It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Taiwan's government web infrastructure is decentralized — unlike Mexico's unified gob.mx platform, each ROC ministry and agency maintains independent web infrastructure with distinct URL patterns, content management systems, and publication workflows. Most agencies operate bilingual sites (Traditional Chinese primary, English secondary) under the `.gov.tw` top-level domain, but there is no shared extraction template. The Presidential Office and Executive Yuan function as parallel executive hubs: the Presidential Office handles sovereignty, defense, and cross-strait policy messaging, while the Executive Yuan manages day-to-day governance and cabinet-level policy communications. All official content uses Traditional Chinese characters (繁體字); Simplified Chinese content on any `.gov.tw` domain would indicate a PRC-sourced injection or cross-strait liaison context.

A distinctive feature of Taiwan's government information environment is the high quality of English-language sites maintained by MOFA, the Presidential Office, and the Central Bank — reflecting Taiwan's strategic need to communicate directly with international audiences given its exclusion from most international organizations. These English sites are not mere translations; they frequently contain original framing and emphasis calibrated for foreign policy audiences.

---

## 1. OFFICIAL GOVERNMENT SOURCES: TAIWAN

### 1.1 Head of Government — Presidential Office (總統府) & Executive Yuan (行政院)

#### 1.1a Office of the President (總統府)

| Field | Detail |
|---|---|
| **Institution** | Office of the President, Republic of China (Taiwan) (總統府) |
| **Domain** | `president.gov.tw` / `english.president.gov.tw` |
| **Entry Point URL** | `https://www.president.gov.tw/NEWS` (Chinese) / `https://english.president.gov.tw/News` (English) |
| **RSS/Atom Feed** | **Yes.** News releases: `https://www.president.gov.tw/RSSNEWS.aspx`. Presidential Gazette: `https://www.president.gov.tw/RSSGazette.aspx`. RSS info page: `https://english.president.gov.tw/Page/23` |
| **Language** | Traditional Chinese (primary); English (parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense, Domestic constraints |
| **Publication Frequency** | Daily or near-daily. News releases issued for all presidential meetings, speeches, foreign dignitary receptions, national security statements. The Presidential Gazette (總統府公報) publishes presidential decrees, promulgated laws, and personnel appointments. |
| **Content Format** | HTML (news releases with full text and photographs). Presidential Gazette in HTML/PDF. |
| **Extraction Method** | RSS feed polling for news releases and gazette publications. HTML scraping of `/NEWS` listing page as fallback. English site mirrors key releases with slight delay. |
| **Editorial Orientation** | Official presidential position. Under President Lai Ching-te (DPP), communications emphasize Taiwan's sovereignty, democratic identity, and resistance to PRC coercion. Framing calibrated for both domestic and international audiences — English releases frequently carry additional context absent from Chinese originals. |
| **Why This Source** | The single authoritative source for presidential statements on cross-strait relations, defense posture, diplomatic engagements, and constitutional matters. Presidential meeting readouts with foreign visitors (especially US, Japan, and European parliamentarians) are often the earliest signal of diplomatic posture shifts. The Presidential Gazette is the legal vehicle for promulgation of all laws and presidential decrees. |
| **Access Notes** | No paywall, no authentication required. Both Chinese and English sites freely accessible. RSS feeds functional. No observed bot protection. |

**Additional entry points:**
- Presidential speeches archive: `https://english.president.gov.tw/News` filtered by category
- Presidential Gazette archive: `https://www.president.gov.tw/Page/95` (Chinese)
- Video/multimedia: `https://english.president.gov.tw/Video`

#### 1.1b Executive Yuan (行政院)

| Field | Detail |
|---|---|
| **Institution** | Executive Yuan (行政院) |
| **Domain** | `ey.gov.tw` / `english.ey.gov.tw` |
| **Entry Point URL** | `https://www.ey.gov.tw/Page/5A898E83D438145A` (Chinese press releases) / `https://english.ey.gov.tw/Page/5A898E83D438145A` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English (parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains — the Executive Yuan coordinates cabinet policy across all ministries |
| **Publication Frequency** | Daily. Press releases issued after weekly cabinet meetings (Thursdays), policy announcements, Premier statements, and inter-ministerial coordination decisions. |
| **Content Format** | HTML. Press releases are full-text HTML with embedded images. Policy documents and reports linked as PDFs. URLs use opaque page IDs (e.g., `/Page/5A898E83D438145A`) rather than human-readable slugs. |
| **Extraction Method** | HTML scraping of press release listing pages. Page ID-based URL structure requires discovery of listing page IDs. No RSS available — periodic polling required. |
| **Editorial Orientation** | Official cabinet position. Under Premier Cho Jung-tai, communications emphasize policy implementation, economic resilience, and public service delivery. Less directly engaged with sovereignty/defense messaging than the Presidential Office. |
| **Why This Source** | The Executive Yuan is the highest administrative organ. Its press releases cover cabinet decisions, inter-ministerial policy coordination, economic stimulus packages, defense budget allocations, and responses to Legislative Yuan interpellations. Premier Cho's Thursday post-cabinet press conferences are the primary vehicle for government policy communication. |
| **Access Notes** | No paywall. English site well-maintained but with some publication lag. URL structure uses GUIDs/hashes, making link prediction difficult — must scrape listing pages for new entries. |

**Additional entry points:**
- Agency news aggregation: `https://english.ey.gov.tw/Page/FDB51B27DE3D4AF4`
- Important policies: `https://english.ey.gov.tw/Page/4B45023ECD498A37`
- Executive Yuan Gazette (行政院公報): `https://gazette.nat.gov.tw/` (see section 1.5)

---

### 1.2 Foreign Ministry — Ministry of Foreign Affairs (外交部 / MOFA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Foreign Affairs, ROC (Taiwan) (外交部) |
| **Domain** | `mofa.gov.tw` / `en.mofa.gov.tw` |
| **Entry Point URL** | `https://en.mofa.gov.tw/News.aspx?n=1329&sms=272` (Press Releases) / `https://en.mofa.gov.tw/News.aspx?n=1328&sms=273` (News and Events) |
| **RSS/Atom Feed** | **Yes — multiple feeds.** News and Events: `https://en.mofa.gov.tw/OpenData.aspx?SN=07564A7F01D47BAD`. Press Releases: `https://en.mofa.gov.tw/OpenData.aspx?SN=3273AA376FB01416`. Statements and Responses: `https://en.mofa.gov.tw/OpenData.aspx?SN=E57623EED610E7DF`. RSS info page: `https://en.mofa.gov.tw/Rss.aspx?n=1447` |
| **Language** | English (primary for international communications); Traditional Chinese (`mofa.gov.tw`) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | Daily or near-daily. Comunicados issued for bilateral meetings, treaty/agreement signings, responses to PRC diplomatic pressure, ally-count changes, international organization participation bids, and foreign minister statements. Volume spikes around UN General Assembly, WHA, and ICAO Assembly sessions. |
| **Content Format** | HTML. Well-structured press releases with clear categorization (News & Events, Press Releases, Statements & Responses, Background Information). Some bilateral agreement texts in PDF. |
| **Extraction Method** | RSS feed polling (three category-specific feeds). HTML scraping of `News.aspx` pages as fallback. URL parameters `n=` and `sms=` define content categories. |
| **Editorial Orientation** | Official foreign ministry position. Under Foreign Minister Lin Chia-lung (林佳龍), emphasis on "pragmatic diplomacy," international participation, and countering PRC's misuse of UN Resolution 2758. MOFA's English-language communications are among the most polished in the ROC government, reflecting the agency's role as Taiwan's primary international voice. |
| **Why This Source** | The only primary source for Taiwan's formal diplomatic positions, ally-count changes, bilateral agreement announcements, international organization participation bids, and official responses to PRC diplomatic pressure. The "Statements and Responses" category is particularly valuable — it provides MOFA's real-time reactions to PRC coercion, ally defections, and international exclusion events. Media coverage (Focus Taiwan, Taipei Times) is invariably derived from these releases. |
| **Access Notes** | No paywall, no authentication. English site is comprehensive and often updated simultaneously with or ahead of the Chinese site for international-audience content. RSS feeds use OpenData.aspx endpoints with unique SN parameters. Embassy/representative office releases available at `roc-taiwan.org/{office_code}/` subdomains. |

**Additional entry points:**
- Statements and Responses: `https://en.mofa.gov.tw/News.aspx?n=1330&sms=274`
- Background Information: `https://en.mofa.gov.tw/News.aspx?n=1331&sms=275`
- MOFA Chinese press room: `https://www.mofa.gov.tw/News.aspx?n=104&sms=70`
- Representative office network: individual `roc-taiwan.org` subdomains per mission (e.g., `roc-taiwan.org/us_en/`)

---

### 1.3 Defense Ministry — Ministry of National Defense (國防部 / MND)

| Field | Detail |
|---|---|
| **Institution** | Ministry of National Defense, ROC (Taiwan) (國防部) |
| **Domain** | `mnd.gov.tw` / `mnd.gov.tw/en` |
| **Entry Point URL** | `https://www.mnd.gov.tw/news/pressreleaselist` (Chinese press releases) / `https://www.mnd.gov.tw/en/news/PressReleaseList` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English (secondary site) |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense |
| **Publication Frequency** | Daily. Press releases cover PLA activity reports (ADIZ intrusions, naval transits), defense procurement, conscription policy, Han Kuang exercise updates, and military institutional matters. PLA activity updates published near-daily during periods of elevated tension. |
| **Content Format** | HTML. Press releases include text and frequently attached images (PLA aircraft identification photos, operational infographics). The biennial National Defense Report is published as a downloadable PDF. PLA regional activity data published on dedicated page with maps. |
| **Extraction Method** | HTML scraping of `/news/pressreleaselist` listing page. Individual articles at `/news/mnd/{article_id}` or `/news/pressrelease/{article_id}`. No RSS — requires periodic polling. |
| **Editorial Orientation** | Official military communication. Under Minister Wellington Koo (顧立雄), communications are notably more transparent than predecessors — MND now publishes daily PLA ADIZ intrusion data, submarine development updates, and defense procurement status. Framing emphasizes deterrence credibility, asymmetric warfare capabilities, and alliance-like cooperation with the US and Japan. |
| **Why This Source** | The sole authoritative source for ROC military posture: PLA activity monitoring data, defense budget and procurement announcements, conscription reform implementation, indigenous defense industry programs (submarine, missile), and Han Kuang exercise scenarios. The 2025 National Defense Report and the proposed NT$1.25 trillion special defense budget are current critical documents. MND's daily PLA activity reporting is unique — no other source provides this data at this tempo. |
| **Access Notes** | No paywall. English site at `/en` covers major releases but with reduced volume and some delay. No observed bot protection. Article URLs use numeric IDs. Some content (procurement details, operational specifics) published only in Chinese. |

**Additional entry points:**
- PLA regional activity/dynamics: `https://www.mnd.gov.tw/news/plaactlist`
- News clarifications: `https://www.mnd.gov.tw/news/pressreleaselist/cate/66`
- Ministry news: `https://www.mnd.gov.tw/news/mndlist`
- MND publications (NDR, QDR): `https://www.mnd.gov.tw/en` → Publications section
- Civil defense preparedness: `https://prepare.mnd.gov.tw`

---

### 1.4 Parliament — Legislative Yuan (立法院)

| Field | Detail |
|---|---|
| **Institution** | Legislative Yuan (立法院) |
| **Domain** | `ly.gov.tw` |
| **Entry Point URL** | `https://www.ly.gov.tw/Pages/List.aspx?nodeid=154` (News, Chinese) / `https://www.ly.gov.tw/EngPages/List.aspx?nodeid=348` (Official Gazette Dept., English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English (minimal — limited to institutional information) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Diplomatic alignment, Security & defense, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods (February–May, September–December). Reduced during recess. Session transcripts (議事錄) and gazette (立法院公報) published with multi-day lag. |
| **Content Format** | HTML for news and announcements. The Legislative Yuan Gazette (立法院公報) published via the Conference and Gazette Management System (`lci.ly.gov.tw`) in HTML and PDF. IVOD (Internet Video on Demand) provides full committee and plenary session recordings. |
| **Extraction Method** | HTML scraping of `Pages/List.aspx?nodeid=154` for news. Gazette content at `lci.ly.gov.tw` — separate system with different URL structure. IVOD at `ivod.ly.gov.tw` for video records. No RSS available — requires periodic polling. |
| **Editorial Orientation** | Institutional. In the current 11th Legislative Yuan (2024–2028), the KMT holds a plurality with TPP support, creating a divided government dynamic with the DPP executive. Legislative communications reflect majority (KMT-TPP) framing; the DPP caucus issues separate statements. |
| **Why This Source** | The Legislative Yuan is the primary arena for domestic constraint dynamics affecting foreign and defense policy. Committee hearings (Foreign Affairs & National Defense Committee, Budget Committee) produce testimony from ministers that surfaces positions not available through executive communications. Budget review (September–January), treaty ratification debates, and interpellation sessions (質詢) contain the highest-signal content. The December 2025 impeachment motion against President Lai demonstrates the legislature's capacity to generate acute institutional crises. |
| **Access Notes** | No paywall. English content extremely limited — the LY's international-facing communication is minimal compared to executive agencies. The `lci.ly.gov.tw` gazette system and `ivod.ly.gov.tw` video system operate on separate infrastructure. Some older committee proceedings available only in PDF scans. |

**Additional entry points:**
- Conference and Gazette System: `https://lci.ly.gov.tw/` (full gazette, committee records)
- IVOD (video proceedings): `https://ivod.ly.gov.tw/`
- Legislative Information System (Open Parliament): `https://www.ly.gov.tw/Pages/List.aspx?nodeid=154`
- Budget Center: `https://www.ly.gov.tw/Pages/List.aspx?nodeid=216`

---

### 1.5 Official Gazette — Executive Yuan Gazette (行政院公報)

| Field | Detail |
|---|---|
| **Institution** | Executive Yuan Gazette Information Network (行政院公報資訊網) |
| **Domain** | `gazette.nat.gov.tw` |
| **Entry Point URL** | `https://gazette.nat.gov.tw/` |
| **RSS/Atom Feed** | None identified. Open Data section available for bulk download. [VERIFY RSS] |
| **Language** | Traditional Chinese |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Gazette is the official publication vehicle for all administrative regulations, orders, and announcements |
| **Publication Frequency** | Daily (weekdays). Each issue contains multiple entries organized by functional chapter. |
| **Content Format** | HTML index pages organized by volume/issue/chapter. Individual entries in HTML with some PDF attachments. Nine functional chapters: General Administration (綜合行政), Interior (內政), Foreign Affairs & Defense (外交國防法務), Finance & Economics (財政經濟), Education & Culture (教育科技文化), Transportation (交通建設), Agriculture & Environment (農業環保), Health & Labor (衛生勞動), Appendices (附錄). |
| **Extraction Method** | HTML scraping of daily issue index pages. Content organized by chapter and content type (法規 regulations, 行政規則 administrative rules, 公告及送達 notices, 處分 dispositions, 特載 special features). Open Data section provides bulk downloadable datasets by period. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of regulations and administrative orders. |
| **Why This Source** | The Executive Yuan Gazette is the official publication vehicle for all administrative regulations, ministerial orders, and policy implementations. Unlike the Presidential Gazette (which covers promulgated laws and presidential decrees), this gazette covers the operational layer — implementing regulations, administrative rules, procurement notices, and personnel appointments. The Foreign Affairs & Defense chapter (外交國防法務篇, ~4,400 entries) and Finance & Economics chapter (財政經濟篇, ~34,800 entries) are highest-priority for pipeline monitoring. |
| **Access Notes** | No paywall. Open Data section provides downloadable datasets. Advanced search available with keyword and date-range filtering. Chinese-language only — no English translation of gazette content. |

**Additional entry points:**
- Presidential Gazette (總統府公報): published via `https://www.president.gov.tw/RSSGazette.aspx` (RSS) and archived at `https://www.president.gov.tw/Page/95`
- Legislative Yuan Gazette: `https://lci.ly.gov.tw/` (separate system, see section 1.4)

---

### 1.6 Finance Ministry — Ministry of Finance (財政部 / MOF)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Finance, ROC (Taiwan) (財政部) |
| **Domain** | `mof.gov.tw` / `mof.gov.tw/Eng` |
| **Entry Point URL** | `https://www.mof.gov.tw/Eng/multiplehtml/f48d641f159a4866b1d31c0916fbcc71` (English press releases) |
| **RSS/Atom Feed** | **Yes.** `https://www.mof.gov.tw/Eng/Rss` (English). Category-specific feeds available by appending `?categoryCode={code}` parameters: NTA (National Treasury), DOT (Taxation), CUS (Customs), FNP (National Property), IFA (International Fiscal Affairs), FaT (Financial & Trade Statistics). |
| **Language** | Traditional Chinese (primary); English (comprehensive parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3–5 per week. Press releases cover tax revenue data, customs/trade statistics, public debt operations, fiscal policy announcements, and international fiscal cooperation. Monthly revenue and trade statistics released on fixed schedules. |
| **Content Format** | HTML. Statistical releases frequently include data tables within HTML or linked PDF/Excel attachments. |
| **Extraction Method** | RSS feed polling (with category filtering). HTML scraping of press release listing as fallback. Category-specific URLs use `categoryCode` parameters. |
| **Editorial Orientation** | Official fiscal policy position. Technical, data-driven communications. Emphasis on fiscal discipline and revenue performance. |
| **Why This Source** | Primary source for ROC government fiscal data: tax revenue, customs receipts, public debt, and trade statistics. MOF's Customs Administration publishes trade data that reveals export dependency patterns (especially semiconductor exports to China/US) critical for economic statecraft analysis. International Fiscal Affairs releases cover tax treaty negotiations and OECD-alignment initiatives. |
| **Access Notes** | No paywall. English site well-maintained. RSS available with category filtering. Statistics and open data portal accessible. |

**Additional entry points:**
- Customs Administration trade statistics: `https://web.customs.gov.tw/` (English available)
- Events/announcements: `https://www.mof.gov.tw/Eng/multiplehtml/6642`
- Chinese press releases: `https://www.mof.gov.tw/multiplehtml/f48d641f159a4866b1d31c0916fbcc71`

---

### 1.7 Central Bank — Central Bank of the Republic of China (Taiwan) (中央銀行 / CBC)

| Field | Detail |
|---|---|
| **Institution** | Central Bank of the Republic of China (Taiwan) (中央銀行) |
| **Domain** | `cbc.gov.tw` |
| **Entry Point URL** | `https://www.cbc.gov.tw/en/lp-302-2.html` (English press releases) / `https://www.cbc.gov.tw/tw/lp-302-1.html` (Chinese press releases) |
| **RSS/Atom Feed** | **Yes.** Press releases feed: `https://www.cbc.gov.tw/tw/rss-302-1.xml` (Chinese). URL pattern for additional feeds: `https://www.cbc.gov.tw/{lang}/rss-{category_id}-{lang_id}.xml`. [VERIFY English RSS at `https://www.cbc.gov.tw/en/rss-302-2.xml`] |
| **Language** | Traditional Chinese (primary); English (comprehensive parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 4 per year (quarterly board meetings, typically in March, June, September, December). Press releases: weekly to bi-weekly covering foreign exchange, financial statistics, and policy communications. Special releases during market stress events. |
| **Content Format** | HTML for press releases. PDF for monetary policy decision statements, meeting minutes, and quarterly reports. Statistical data in HTML tables and downloadable Excel/CSV. |
| **Extraction Method** | RSS feed polling for press releases. HTML scraping as fallback. URL pattern: `/tw/cp-{article_id}-{hash}-1.html` for individual articles. Monetary policy decisions published as PDF. |
| **Editorial Orientation** | Technically independent central bank. Communications are data-driven and institutionally cautious. Under Governor Yang Chin-long (楊金龍, serving since 2018, reappointed), the CBC is known for conservative communication and active foreign exchange intervention to prevent excessive TWD appreciation — a politically sensitive issue given export sector dependence. |
| **Why This Source** | The only source for authoritative monetary policy decisions, foreign exchange reserve data, capital flow statistics, and official economic indicators. CBC quarterly board meeting decisions on the policy rate directly affect semiconductor industry financing and real estate markets. Foreign exchange reserve levels and intervention patterns are closely watched indicators of cross-strait economic resilience. The CBC's financial stability reports provide unique data on Taiwan's banking sector exposure to PRC markets. |
| **Access Notes** | No paywall. No observed bot protection. English site comprehensive — major publications available in both languages. RSS feed confirmed for Chinese press releases; English feed likely follows same URL pattern. Statistical database at `https://www.cbc.gov.tw/en/np-1038-2.html`. |

**Key publication schedule:**
| Publication | Frequency | Format |
|---|---|---|
| Monetary policy decision | Quarterly | PDF + press conference |
| Foreign exchange reserves | Monthly | HTML/press release |
| Financial statistics | Monthly | HTML + Excel |
| Financial Stability Report | Annual | PDF |
| CBC Annual Report | Annual | PDF |

---

### 1.8 Trade / Commerce — Ministry of Economic Affairs (經濟部 / MOEA) & Bureau of Foreign Trade (國際貿易署 / BOFT)

#### 1.8a Ministry of Economic Affairs (經濟部 / MOEA)

| Field | Detail |
|---|---|
| **Institution** | Ministry of Economic Affairs, ROC (Taiwan) (經濟部) |
| **Domain** | `moea.gov.tw` / `moea.gov.tw/MNS/english/` |
| **Entry Point URL** | `https://www.moea.gov.tw/MNS/english/news/News.aspx?kind=6&menu_id=176` (English news) |
| **RSS/Atom Feed** | **Yes.** `https://www.moea.gov.tw/MNS/english/news/NewsRSS.aspx?menu_id=1438` (English). [VERIFY Chinese RSS at equivalent path] |
| **Language** | Traditional Chinese (primary); English (parallel site) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 3–5 per week. Communications cover industrial policy, investment promotion, energy policy, semiconductor/technology statecraft, and bilateral economic cooperation agreements. |
| **Content Format** | HTML. Reports and white papers in PDF. Statistical data available via subordinate agencies. |
| **Extraction Method** | RSS feed polling. HTML scraping as fallback. ASP.NET URL structure with `kind=`, `menu_id=`, and `news_id=` parameters. |
| **Editorial Orientation** | Official economic policy position. Under Minister Kung Ming-hsin (龔明鑫), emphasis on supply chain resilience, semiconductor industry support, energy transition, and New Southbound Policy economic dimensions. MOEA is the institutional home for TSMC-relevant industrial policy, making its communications directly relevant to semiconductor statecraft analysis. |
| **Why This Source** | MOEA oversees industrial policy, investment, energy, and trade — making it the primary government source for economic statecraft signals. Its subordinate agencies (Industrial Development Administration, Energy Administration, Investment Commission) publish sector-specific data. MOEA communications on semiconductor policy, CHIPS Act coordination with the US, and PRC economic coercion responses are high-priority items. |
| **Access Notes** | No paywall. ASP.NET-based site. English site functional. RSS available. Some subordinate agency sites (IDA, Energy Administration) have separate infrastructure. |

#### 1.8b Bureau of Foreign Trade (國際貿易署 / BOFT)

| Field | Detail |
|---|---|
| **Institution** | International Trade Administration (formerly Bureau of Foreign Trade), MOEA (國際貿易署) |
| **Domain** | `trade.gov.tw` / `trade.gov.tw/English/` |
| **Entry Point URL** | `https://www.trade.gov.tw/Pages/List.aspx?nodeID=40` (Chinese news) / `https://www.trade.gov.tw/English/Pages/List.aspx?nodeID=86` (English news) |
| **RSS/Atom Feed** | **Yes.** RSS subscription page: `https://www.trade.gov.tw/StaticPage/RSS.aspx`. English RSS: `https://www.trade.gov.tw/English/StaticPage/RSS.aspx` |
| **Language** | Traditional Chinese (primary); English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Institutional engagement |
| **Publication Frequency** | 2–4 per week. Covers trade negotiations, FTA/ECA developments, CPTPP accession efforts, WTO participation, trade statistics, and exhibition/promotion activities. |
| **Content Format** | HTML. Trade statistics in HTML and downloadable formats. |
| **Extraction Method** | RSS feed polling. HTML scraping of listing pages as fallback. URL pattern: `Pages/detail.aspx?nodeID={node}&pid={article_id}`. |
| **Editorial Orientation** | Official trade policy position. Emphasis on trade liberalization, CPTPP accession, and diversification away from PRC market dependence under the New Southbound Policy. |
| **Why This Source** | Primary source for Taiwan's trade policy positions, FTA/ECA negotiations, CPTPP accession status, export control implementation, and trade statistics. BOFT's trade data reveals the structural dependency on semiconductor exports and the progress of supply-chain diversification — both critical economic statecraft indicators. |
| **Access Notes** | No paywall. Both Chinese and English sites functional. RSS available on both language versions. |

---

### 1.9 Intelligence / National Security — National Security Bureau (國家安全局 / NSB) & National Security Council (國家安全會議 / NSC)

#### 1.9a National Security Bureau (國家安全局 / NSB)

| Field | Detail |
|---|---|
| **Institution** | National Security Bureau (國家安全局) |
| **Domain** | `nsb.gov.tw` / `nsb.gov.tw/en/` |
| **Entry Point URL** | `https://www.nsb.gov.tw/` (Chinese) / `https://www.nsb.gov.tw/en/` (English) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English (limited) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense, Domestic constraints |
| **Publication Frequency** | Low — 3–6 major publications per year. The NSB publishes periodic reports on PRC infiltration, cyberattack statistics, and espionage case summaries. These reports are typically released to the Legislative Yuan and simultaneously covered by media. Daily/weekly operational communications do not exist in public channels. |
| **Content Format** | HTML (minimal). Major reports in PDF. The site requires JavaScript and uses dynamic rendering, making scraping more complex. |
| **Extraction Method** | Periodic check of `nsb.gov.tw` for new publications. JavaScript-rendered site may require headless browser. Primary signal comes through media coverage (Focus Taiwan, Taipei Times) of NSB Legislative Yuan testimony and report releases rather than direct website monitoring. |
| **Editorial Orientation** | Official intelligence assessment. NSB reports are calibrated to serve two audiences: the Legislative Yuan (oversight) and the public (threat awareness). Under the current director, reports on PRC cyber operations, cognitive warfare, and infiltration have become increasingly detailed and publicly accessible — reflecting a deliberate transparency strategy to build domestic support for defense spending. |
| **Why This Source** | The NSB's periodic reports are the only official window into Taiwan's intelligence assessment of PRC threats. The January 2026 report documenting 2.63 million daily PRC cyberattacks against Taiwan's critical infrastructure, and the 2025 report on PRC infiltration tactics targeting military veterans, are examples of high-value primary source material that shapes defense policy and public discourse. NSB testimony before the Legislative Yuan's Foreign Affairs and National Defense Committee frequently surfaces threat assessments unavailable elsewhere. |
| **Access Notes** | Website is sparse and JavaScript-dependent. English section minimal. Most NSB content reaches the public through Legislative Yuan testimony reported by Focus Taiwan and Taipei Times rather than direct website publication. Transparency portal available for organizational/budget information. |

#### 1.9b National Security Council (國家安全會議 / NSC)

| Field | Detail |
|---|---|
| **Institution** | National Security Council (國家安全會議) |
| **Domain** | No independent public website maintained |
| **Entry Point URL** | N/A — NSC communications are issued through the Presidential Office |
| **RSS/Atom Feed** | N/A |
| **Language** | Traditional Chinese / English (via Presidential Office) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense, Diplomatic alignment |
| **Publication Frequency** | Negligible direct output. NSC meetings are reported through Presidential Office press releases. |
| **Content Format** | N/A |
| **Extraction Method** | Monitor Presidential Office releases for NSC-related content (search terms: 國家安全會議, National Security Council, 國安高層會議). NSC Secretary-General Joseph Wu's (吳釗燮) public statements are issued through Presidential Office channels. |
| **Editorial Orientation** | N/A — the NSC does not issue independent public communications. |
| **Why This Source** | Included for completeness. The NSC is Taiwan's apex national security coordination body, chaired by the President, with the Secretary-General as its operational head. It does not maintain an independent website or issue direct public communications. NSC policy influence is surfaced through: (a) Presidential Office statements following "high-level national security meetings" (國安高層會議), (b) media reports attributing positions to "senior national security officials," and (c) the Secretary-General's occasional public speeches and international conference appearances. Joseph Wu, as current NSC Secretary-General and former Foreign Minister, is a key figure whose statements (when made) carry significant signal weight. |
| **Access Notes** | The NSC has a LinkedIn page but no operational website. All public-facing content routes through the Presidential Office. The FRS (Fondation pour la Recherche Stratégique) published a detailed analysis of the NSC's role in April 2025, noting the body employs 86 staff members. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Mainland Affairs Council (大陸委員會 / MAC)

| Field | Detail |
|---|---|
| **Institution** | Mainland Affairs Council (大陸委員會) |
| **Domain** | `mac.gov.tw` / `mac.gov.tw/en/` |
| **Entry Point URL** | `https://www.mac.gov.tw/en/News.aspx?n=2462&sms=262` (English press releases) [VERIFY URL — 403 observed, may require direct navigation] |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Domestic constraints, Institutional engagement |
| **Publication Frequency** | 2–5 per week. Press releases cover cross-strait policy statements, responses to PRC actions, public opinion surveys on cross-strait relations, and Strait Exchange Foundation (SEF) activities. |
| **Content Format** | HTML. Regular public opinion surveys published as PDF with data tables. Policy papers and cross-strait exchange statistics in PDF. |
| **Extraction Method** | HTML scraping of news listing pages. Some pages may return 403 errors — may require cookie/session handling. ASP.NET URL structure with `n=` and `sms=` parameters. |
| **Editorial Orientation** | Official cross-strait policy position. Under the DPP administration, MAC consistently frames cross-strait relations through the lens of ROC sovereignty, democratic governance, and rejection of PRC's "one country, two systems" formula. MAC's regular public opinion surveys (showing persistent majorities favoring the status quo) are politically significant data. |
| **Why This Source** | MAC is the dedicated government body for cross-strait policy — the single most consequential dimension of Taiwan's external relations. Its press releases are the first official government response to PRC actions (military exercises, diplomatic poaching, economic coercion, TAO statements). MAC's quarterly public opinion surveys on cross-strait relations and identity are the most authoritative polling data on Taiwan's most sensitive political question. MAC also publishes cross-strait exchange statistics (trade, tourism, personnel flows) that no other source aggregates. |
| **Access Notes** | English site may intermittently return 403 errors — Chinese site at `mac.gov.tw` is more reliably accessible. Some survey data and reports require navigating to publications subsections. The Strait Exchange Foundation (SEF, 海峽交流基金會) at `sef.org.tw` publishes related content on semi-official cross-strait dialogue. |

**Additional entry points:**
- MAC Chinese press releases: `https://www.mac.gov.tw/News.aspx?n=49&sms=39`
- Cross-strait statistics: `https://www.mac.gov.tw/en/np-4-2.html`
- Public opinion surveys: accessible via MAC publications section
- Strait Exchange Foundation: `https://www.sef.org.tw/`

#### 1.10b Overseas Community Affairs Council (僑務委員會 / OCAC)

| Field | Detail |
|---|---|
| **Institution** | Overseas Community Affairs Council (僑務委員會) |
| **Domain** | `ocac.gov.tw` |
| **Entry Point URL** | `https://www.ocac.gov.tw/OCAC/Eng/` (English) / `https://www.ocac.gov.tw/ocac/` (Chinese) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Traditional Chinese (primary); English |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | 2–3 per week. Covers overseas Taiwanese community engagement, diaspora mobilization, cultural diplomacy, and counter-PRC influence efforts in overseas Chinese communities. |
| **Content Format** | HTML. Some reports in PDF. |
| **Extraction Method** | HTML scraping. ASP.NET URL structure. |
| **Editorial Orientation** | Official position on overseas community engagement. Under the DPP, OCAC has shifted emphasis from "overseas Chinese" (華僑) to "overseas Taiwanese" (台僑) framing, reflecting the identity politics dimension of Taiwan's diplomacy. |
| **Why This Source** | OCAC is a unique institutional indicator for Taiwan's soft power and diaspora diplomacy. Its communications reveal government efforts to mobilize overseas communities for diplomatic support, counter PRC United Front activities in diaspora populations, and maintain cultural/economic ties with Taiwanese expatriates — particularly in the US, Japan, and Southeast Asia. OCAC programming shifts can signal changes in diplomatic strategy. |
| **Access Notes** | English site functional. No paywall. Social media presence on X (@OCAC_TAIWAN) and Instagram. |

#### 1.10c PRC Taiwan Affairs Office Monitoring (國台辦 / TAO)

| Field | Detail |
|---|---|
| **Institution** | PRC Taiwan Affairs Office (國務院台灣事務辦公室 / 國台辦) — monitored as adversary signal source |
| **Domain** | `gwytb.gov.cn` |
| **Entry Point URL** | `http://www.gwytb.gov.cn/xwdt/xwfb/` (press conference records) / `http://www.gwytb.gov.cn/xwdt/` (news section) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Simplified Chinese |
| **Type** | `government_aligned` (adversary government) |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Security & defense |
| **Publication Frequency** | Bi-weekly press conferences (typically Wednesday). Additional statements during crisis periods. |
| **Why This Source** | The TAO is Beijing's primary institutional channel for Taiwan policy communication. Its bi-weekly press conferences set the PRC's public posture on cross-strait issues — including responses to US arms sales, Taiwan's diplomatic activities, and domestic political developments. TAO rhetoric shifts (escalatory vs. conciliatory language, new formulations on "reunification timetable," sanctions threats against specific Taiwanese individuals) are leading indicators of PRC policy direction. Cross-reference TAO statements with MAC responses for the full cross-strait communication dynamic. |
| **Access Notes** | PRC government site. HTTP (not HTTPS) on some pages. Simplified Chinese only. No English translation. Content may be partially blocked or degraded from Taiwan-based IP addresses. Access from non-PRC jurisdictions generally functional. The TAO spokesperson's press conference transcripts are the highest-value content. |

#### 1.10d Semiconductor & Industrial Policy Sources (TSMC-relevant)

| Field | Detail |
|---|---|
| **Institution** | Industrial Development Administration (產業發展署 / IDA), National Science and Technology Council (國科會 / NSTC), Investment Commission (投資審議司) |
| **Domain** | `ida.gov.tw` / `nstc.gov.tw` / `moeaic.gov.tw` |
| **Entry Point URL** | `https://www.ida.gov.tw/` (IDA) / `https://www.nstc.gov.tw/` (NSTC) / `https://www.moeaic.gov.tw/` (Investment Commission) |
| **RSS/Atom Feed** | [VERIFY RSS for each] |
| **Language** | Traditional Chinese (primary); English (variable quality) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Variable. IDA: 2–3 per week on industrial development programs. NSTC: weekly on science/technology policy. Investment Commission: monthly FDI statistics, plus ad hoc rulings on inbound/outbound investment applications. |
| **Content Format** | HTML, PDF (reports, statistics). |
| **Extraction Method** | HTML scraping. Each agency has independent infrastructure. |
| **Editorial Orientation** | Official industrial/technology policy positions. |
| **Why This Source** | These agencies collectively govern the policy environment for Taiwan's semiconductor industry — the island's most strategically significant economic asset. IDA oversees industrial development programs including semiconductor supply chain support. NSTC coordinates R&D policy and science park administration (Hsinchu Science Park, home to TSMC HQ). The Investment Commission reviews outbound investment to PRC (critical for tracking tech transfer restrictions) and inbound FDI (relevant to US CHIPS Act coordination and allied reshoring efforts). |
| **Access Notes** | Variable site quality. IDA and NSTC have functional English sections. Investment Commission site is primarily Chinese with limited English. FDI statistics data is the highest-value automated extraction target. |

**Additional entry points:**
- Hsinchu Science Park Administration: `https://www.sipa.gov.tw/`
- TSMC corporate (for cross-reference): `https://www.tsmc.com/english/news-events`
- National Development Council economic data: `https://www.ndc.gov.tw/en/`

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Language |
|---|---|---|---|---|---|---|---|
| 1a | Presidential Office | `president.gov.tw/NEWS` | **Yes** (2 feeds) | P1 | HTML | Daily | zh-TW / en |
| 1b | Executive Yuan | `ey.gov.tw/Page/5A898E83D438145A` | [VERIFY] | P1 | HTML | Daily | zh-TW / en |
| 2 | MOFA | `en.mofa.gov.tw/News.aspx?n=1329&sms=272` | **Yes** (3 feeds) | P1 | HTML | Daily | en / zh-TW |
| 3 | MND | `mnd.gov.tw/news/pressreleaselist` | [VERIFY] | P1 | HTML | Daily | zh-TW / en |
| 4 | Legislative Yuan | `ly.gov.tw/Pages/List.aspx?nodeid=154` | [VERIFY] | P2 | HTML/PDF | Daily (session) | zh-TW |
| 5 | Executive Yuan Gazette | `gazette.nat.gov.tw/` | [VERIFY] | P2 | HTML/PDF | Daily | zh-TW |
| 6 | MOF | `mof.gov.tw/Eng/multiplehtml/...` | **Yes** | P2 | HTML | 3-5/week | zh-TW / en |
| 7 | CBC | `cbc.gov.tw/tw/lp-302-1.html` | **Yes** | P2 | HTML/PDF | Variable | zh-TW / en |
| 8a | MOEA | `moea.gov.tw/MNS/english/news/News.aspx` | **Yes** | P2 | HTML | 3-5/week | zh-TW / en |
| 8b | BOFT | `trade.gov.tw/Pages/List.aspx?nodeID=40` | **Yes** | P2 | HTML | 2-4/week | zh-TW / en |
| 9a | NSB | `nsb.gov.tw` | [VERIFY] | P2 | HTML/PDF | Low (3-6/year) | zh-TW |
| 9b | NSC | N/A (via Presidential Office) | N/A | P2 | N/A | Negligible | — |
| 10a | MAC | `mac.gov.tw/en/News.aspx?n=2462&sms=262` | [VERIFY] | P2 | HTML/PDF | 2-5/week | zh-TW / en |
| 10b | OCAC | `ocac.gov.tw/OCAC/Eng/` | [VERIFY] | P2 | HTML | 2-3/week | zh-TW / en |
| 10c | TAO (PRC) | `gwytb.gov.cn/xwdt/xwfb/` | No | P2 | HTML | Bi-weekly | zh-CN |
| 10d | IDA/NSTC/InvComm | `ida.gov.tw` / `nstc.gov.tw` / `moeaic.gov.tw` | [VERIFY] | P2 | HTML/PDF | Variable | zh-TW / en |

---

## 3. MONITORING CONFIGURATION

```yaml
# Taiwan Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/tw.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: tw_presidential_office
    name: Office of the President (總統府)
    domain: president.gov.tw
    entry_url: "https://www.president.gov.tw/NEWS"
    entry_url_en: "https://english.president.gov.tw/News"
    rss_feed:
      news_releases: "https://www.president.gov.tw/RSSNEWS.aspx"
      presidential_gazette: "https://www.president.gov.tw/RSSGazette.aspx"
    language: zh-TW
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
    notes: "RSS feeds for both news releases and gazette. English site mirrors major releases. Presidential statements on cross-strait policy and defense are highest-priority items."

  - id: tw_executive_yuan
    name: Executive Yuan (行政院)
    domain: ey.gov.tw
    entry_url: "https://www.ey.gov.tw/Page/5A898E83D438145A"
    entry_url_en: "https://english.ey.gov.tw/Page/5A898E83D438145A"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    language_secondary: en
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
    poll_interval_hours: 4
    notes: "GUID-based URL structure. Thursday post-cabinet press conferences are highest-signal. No RSS identified — scrape listing page."

  - id: tw_mofa
    name: Ministry of Foreign Affairs (外交部)
    domain: mofa.gov.tw
    entry_url: "https://en.mofa.gov.tw/News.aspx?n=1329&sms=272"
    rss_feed:
      news_events: "https://en.mofa.gov.tw/OpenData.aspx?SN=07564A7F01D47BAD"
      press_releases: "https://en.mofa.gov.tw/OpenData.aspx?SN=3273AA376FB01416"
      statements_responses: "https://en.mofa.gov.tw/OpenData.aspx?SN=E57623EED610E7DF"
    language: en
    language_secondary: zh-TW
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 2
    notes: "Three category-specific RSS feeds via OpenData endpoints. English site is primary for international communications. 'Statements and Responses' feed is highest-signal for real-time PRC coercion reactions."

  - id: tw_mnd
    name: Ministry of National Defense (國防部)
    domain: mnd.gov.tw
    entry_url: "https://www.mnd.gov.tw/news/pressreleaselist"
    entry_url_en: "https://www.mnd.gov.tw/en/news/PressReleaseList"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "No RSS identified. PLA activity page at /news/plaactlist updates near-daily. Article URLs use numeric IDs (/news/mnd/{id}). X account @MoNDefense provides real-time alerts."
    additional_urls:
      pla_activity: "https://www.mnd.gov.tw/news/plaactlist"
      news_clarifications: "https://www.mnd.gov.tw/news/pressreleaselist/cate/66"

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: tw_legislative_yuan
    name: Legislative Yuan (立法院)
    domain: ly.gov.tw
    entry_url: "https://www.ly.gov.tw/Pages/List.aspx?nodeid=154"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - diplomatic_alignment
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Gazette system at lci.ly.gov.tw (separate infrastructure). IVOD at ivod.ly.gov.tw. English content minimal. Foreign Affairs & National Defense Committee and Budget Committee sessions highest priority."

  - id: tw_gazette
    name: Executive Yuan Gazette (行政院公報)
    domain: gazette.nat.gov.tw
    entry_url: "https://gazette.nat.gov.tw/"
    rss_feed: null  # Open Data section available for bulk download. [VERIFY RSS]
    language: zh-TW
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
    poll_interval_hours: 12
    notes: "Nine functional chapters. Foreign Affairs & Defense chapter (外交國防法務篇) and Finance & Economics chapter (財政經濟篇) are highest priority. Open Data section for bulk access."

  - id: tw_mof
    name: Ministry of Finance (財政部)
    domain: mof.gov.tw
    entry_url: "https://www.mof.gov.tw/Eng/multiplehtml/f48d641f159a4866b1d31c0916fbcc71"
    rss_feed: "https://www.mof.gov.tw/Eng/Rss"
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Category-specific RSS via ?categoryCode= parameters (NTA, DOT, CUS, FNP, IFA, FaT). Customs Administration trade statistics at web.customs.gov.tw."

  - id: tw_cbc
    name: Central Bank (中央銀行)
    domain: cbc.gov.tw
    entry_url: "https://www.cbc.gov.tw/en/lp-302-2.html"
    rss_feed:
      press_releases_zh: "https://www.cbc.gov.tw/tw/rss-302-1.xml"
      press_releases_en: "https://www.cbc.gov.tw/en/rss-302-2.xml"  # [VERIFY]
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Quarterly monetary policy decisions (March, June, September, December) are highest-signal events. RSS confirmed for Chinese press releases. URL pattern: /tw/rss-{category}-1.xml."

  - id: tw_moea
    name: Ministry of Economic Affairs (經濟部)
    domain: moea.gov.tw
    entry_url: "https://www.moea.gov.tw/MNS/english/news/News.aspx?kind=6&menu_id=176"
    rss_feed: "https://www.moea.gov.tw/MNS/english/news/NewsRSS.aspx?menu_id=1438"
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 12
    notes: "Semiconductor/industrial policy communications. Subordinate agencies (IDA, Energy Admin, Investment Commission) have separate sites."

  - id: tw_boft
    name: Bureau of Foreign Trade (國際貿易署)
    domain: trade.gov.tw
    entry_url: "https://www.trade.gov.tw/Pages/List.aspx?nodeID=40"
    rss_feed: "https://www.trade.gov.tw/StaticPage/RSS.aspx"
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - institutional_engagement
    publication_frequency: "2-4_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 12
    notes: "Trade negotiations, CPTPP accession, export controls. English site at trade.gov.tw/English/."

  - id: tw_nsb
    name: National Security Bureau (國家安全局)
    domain: nsb.gov.tw
    entry_url: "https://www.nsb.gov.tw/"
    entry_url_en: "https://www.nsb.gov.tw/en/"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "3-6_per_year"
    content_format: html_pdf_mixed
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Low-frequency publisher. Flag any new publication as high-priority anomaly. JavaScript-rendered site may require headless browser. Primary signal via media coverage of NSB Legislative Yuan testimony."

  - id: tw_nsc
    name: National Security Council (國家安全會議)
    domain: null  # No independent website
    entry_url: null  # Monitor Presidential Office for NSC content
    rss_feed: null
    language: zh-TW
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: negligible
    content_format: null
    extraction_method: keyword_filter_on_presidential_office
    poll_interval_hours: null  # Captured via tw_presidential_office monitoring
    notes: "No independent web presence. Monitor Presidential Office releases for keywords: 國家安全會議, National Security Council, 國安高層會議. Secretary-General Joseph Wu statements routed through Presidential Office."

  - id: tw_mac
    name: Mainland Affairs Council (大陸委員會)
    domain: mac.gov.tw
    entry_url: "https://www.mac.gov.tw/en/News.aspx?n=2462&sms=262"
    entry_url_zh: "https://www.mac.gov.tw/News.aspx?n=49&sms=39"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - domestic_constraints
      - institutional_engagement
    publication_frequency: "2-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "English site may return 403 — use Chinese site as primary. Cross-strait opinion surveys are high-value data. Cross-reference with TAO press conferences for full cross-strait communication dynamic."

  - id: tw_ocac
    name: Overseas Community Affairs Council (僑務委員會)
    domain: ocac.gov.tw
    entry_url: "https://www.ocac.gov.tw/OCAC/Eng/"
    rss_feed: null  # [VERIFY]
    language: zh-TW
    language_secondary: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "2-3_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "Diaspora engagement and soft power indicator. X: @OCAC_TAIWAN."

  - id: tw_tao_monitor
    name: PRC Taiwan Affairs Office (國台辦) — adversary monitoring
    domain: gwytb.gov.cn
    entry_url: "http://www.gwytb.gov.cn/xwdt/xwfb/"
    rss_feed: null
    language: zh-CN
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
    publication_frequency: bi-weekly
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "PRC adversary source. Bi-weekly press conferences (typically Wednesday). HTTP site. May be degraded from Taiwan-based IPs. Simplified Chinese — requires separate text processing pipeline from ROC Traditional Chinese sources."

  - id: tw_industrial_policy
    name: IDA / NSTC / Investment Commission
    domain: ida.gov.tw
    entry_url: "https://www.ida.gov.tw/"
    additional_domains:
      - nstc.gov.tw
      - moeaic.gov.tw
    rss_feed: null  # [VERIFY for each]
    language: zh-TW
    language_secondary: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "Three separate agency sites. Investment Commission FDI rulings and statistics are highest-value target. NSTC for science park and R&D policy. IDA for industrial development programs."
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Taiwan's government communications are generally more transparent and substantive than many regional peers, reflecting both democratic accountability norms and the strategic imperative to maintain international credibility. However, communications are still calibrated to serve policy objectives, and the pipeline must treat government statements as evidence of *what the government wants to communicate*, not necessarily as complete accounts of policy reality. The interpretive value lies in: (a) what is said, (b) what is omitted, (c) the language register and framing choices, and (d) discrepancies between Chinese-language and English-language versions of the same announcement.

- **Presidential Office**: Cross-reference presidential statements with same-day coverage in Liberty Times (government-aligned perspective), United Daily News (opposition perspective), and Focus Taiwan (wire service framing). When the Presidential Office issues a statement in English that contains framing absent from the Chinese version, it signals international audience calibration — note the delta. Presidential meeting readouts with foreign visitors should be cross-referenced with the visitor's home-country media for the counterpart perspective.

- **MOFA**: Diplomatic communications should be triangulated with Focus Taiwan (CNA) for factual coverage, Taipei Times for editorial interpretation, and CommonWealth for economic-diplomatic context. MOFA's "Statements and Responses" releases are reactive — cross-reference with the triggering PRC/international event to assess proportionality of response. When MOFA and MAC issue parallel statements on the same cross-strait event, compare framing: MOFA targets international audiences, MAC targets domestic audiences. Divergence signals calibrated messaging, not policy confusion.

- **MND**: Defense communications are the most transparent in the region for PLA activity data (ADIZ intrusions, naval transits) but remain opaque on force readiness, procurement timelines, and operational capabilities. Cross-reference MND PLA activity reports with INDSR (defense think tank) analytical assessments and Taipei Times/Liberty Times defense correspondents. For procurement and budget data, cross-reference with Legislative Yuan Budget Committee proceedings (available via `lci.ly.gov.tw`). The Reporter (報導者) provides investigative coverage of defense procurement problems that MND communications never acknowledge.

- **Executive Yuan**: Cabinet policy announcements should be cross-referenced with CommonWealth (policy analysis), Storm Media (elite commentary), and United Daily News (opposition reaction). Premier Cho's post-cabinet press conferences are the primary venue for government policy messaging — compare with subsequent Legislative Yuan interpellation sessions for the opposition framing.

- **CBC**: Monetary policy decisions are technically rigorous and the least politically distorted source in the ROC government. However, the CBC's known preference for TWD intervention to support exporters means communications about exchange rate policy carry implicit industrial policy signals. Cross-reference with CommonWealth and The News Lens for independent economic analysis.

- **MAC**: Cross-strait policy statements are the most politically charged of all government communications. MAC statements must always be read alongside the triggering TAO statement or PRC action. MAC's regular public opinion surveys are high-value data but should be cross-referenced with TVBS Poll Center and Taiwan Foundation for Democracy surveys for methodological comparison. When all three surveys converge, the signal is strong; divergence suggests question-framing effects.

- **NSB**: Intelligence reports released to the public are deliberately calibrated for threat-awareness building. They present genuine data (cyberattack counts, espionage indictments) but the selection and framing serve the government's defense spending narrative. Cross-reference with INDSR for analytical context and Taipei Times/Focus Taiwan for Legislative Yuan testimony details that the official report may omit.

**4.2 The bilingual publication effect**

Taiwan's government is unusual in maintaining high-quality English-language parallel sites for most major agencies. This creates an analytical opportunity: comparing Chinese and English versions of the same announcement can reveal audience-specific framing. Key patterns:

- MOFA English releases frequently contain additional context paragraphs absent from Chinese versions — these are calibrated for foreign correspondents and international analysts.
- Presidential Office English releases sometimes soften sovereignty-assertive language present in the Chinese original, reflecting diplomatic pragmatism in international messaging.
- MND English releases are a subset of Chinese releases — monitoring only the English site misses significant content, particularly on domestic military affairs and procurement.
- MAC English releases may lag or be less detailed than Chinese versions — for cross-strait developments, always prioritize the Chinese release.

The pipeline should ingest both language versions and flag content deltas as analytically significant.

**4.3 The NSC/NSB silence problem**

Taiwan's intelligence and national security coordination apparatus produces minimal direct public communications. This is a structural gap similar to Mexico's CNI silence problem but with different signal pathways:

- **NSC**: No independent website. All signal routes through Presidential Office. The phrase "high-level national security meeting" (國安高層會議) in Presidential Office releases is the marker for NSC-level deliberation. Secretary-General Joseph Wu's international conference appearances (particularly at European and Japanese security forums) are rare but high-signal events.

- **NSB**: Periodic reports (3–6 per year) released to the Legislative Yuan are the primary output. These reports reach the public through media coverage (Focus Taiwan, Taipei Times) rather than direct website publication. The pipeline should monitor these media outlets for NSB-attributed content and treat any direct website publication as a high-priority anomaly.

The real intelligence-relevant signal environment in Taiwan operates through: (a) MND's daily PLA activity data, (b) INDSR analytical publications, (c) NSB reports surfaced via Legislative Yuan testimony, and (d) investigative reporting by The Reporter and Storm Media.

**4.4 The cross-strait communication dynamic**

Taiwan is unique among pipeline targets in that a critical analytical dimension requires monitoring an adversary government source (PRC TAO) alongside the target government sources (MAC, MOFA, Presidential Office). The MAC-TAO communication axis is the primary channel for cross-strait signaling:

- TAO bi-weekly press conferences set the PRC's public posture
- MAC responds within hours, typically same-day
- Presidential Office weighs in for high-significance events
- MOFA responds when the PRC action has international dimensions

The pipeline should implement paired monitoring: every TAO press conference should trigger an immediate check of MAC, MOFA, and Presidential Office channels for response statements. The *absence* of a response to a TAO provocation is itself analytically significant — it may indicate deliberate de-escalation or internal policy deliberation.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Infrastructure: No Shared Extraction Pattern

Unlike Mexico's gob.mx platform (7 agencies, one extraction template), Taiwan's government web infrastructure is fully decentralized. Each agency operates independent sites with distinct:

- **Content management systems**: ASP.NET (MOFA, MAC, BOFT, OCAC), custom CMS (MND, Presidential Office), Java-based (CBC), WordPress-like (some subordinate agencies)
- **URL patterns**: parametric (`?n=&sms=`), path-based (`/news/pressreleaselist`), GUID-based (`/Page/5A898E83D438145A`), sequential numeric (`/cp-{id}-{hash}-1.html`)
- **Feed formats**: RSS at `RSSNEWS.aspx` (Presidential Office), `OpenData.aspx?SN=` (MOFA), `.xml` (CBC), `NewsRSS.aspx` (MOEA), `RSS.aspx` (BOFT, MOF)

This requires agency-specific scraper modules rather than a parameterized shared scraper. However, the consistent use of the `.gov.tw` TLD and generally similar ASP.NET patterns across MOFA, MAC, BOFT, and OCAC allows some extraction logic reuse.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Six government sources provide confirmed or likely RSS feeds — significantly more than Mexico's two:

1. **Presidential Office**: Two feeds — news releases (`RSSNEWS.aspx`) and gazette (`RSSGazette.aspx`). Standard RSS format.

2. **MOFA**: Three category-specific feeds via `OpenData.aspx?SN=` endpoints (News & Events, Press Releases, Statements & Responses). These are the highest-value automated feeds in the Taiwan pipeline.

3. **MOF**: RSS at `/Eng/Rss` with category filtering via `?categoryCode=` parameters.

4. **CBC**: Press releases feed at `/tw/rss-302-1.xml`. URL pattern suggests additional category feeds may exist.

5. **MOEA**: English news RSS at `NewsRSS.aspx?menu_id=1438`.

6. **BOFT**: RSS at `/StaticPage/RSS.aspx` (both Chinese and English).

All other sources require HTML scraping or periodic page polling.

### 5.3 PDF Extraction Requirements

Three sources publish substantially in PDF:

- **CBC**: Monetary policy decision statements and minutes are multi-page PDF. Text-based, well-structured. Quarterly publication.
- **Executive Yuan Gazette**: Some entries published as PDF attachments. Text-based.
- **NSB**: Major threat assessment reports published as PDF via Legislative Yuan. Infrequent (3–6 per year) but high-value.
- **MND**: National Defense Report (biennial) is a comprehensive PDF (200+ pages). Defense white papers and special reports in PDF.

### 5.4 Language and Encoding

All ROC government sources publish in Traditional Chinese (繁體字, zh-TW). Most major agencies maintain parallel English sites of varying quality:

| Agency | English Site Quality | Coverage vs. Chinese |
|---|---|---|
| MOFA | Excellent | Near-complete; some original English content |
| Presidential Office | Good | Major releases; some delay |
| MND | Adequate | Subset of Chinese content |
| CBC | Good | Major publications bilateral |
| MOF | Good | Comprehensive |
| MOEA/BOFT | Adequate | Key releases |
| Executive Yuan | Adequate | Major releases with lag |
| MAC | Adequate | May return 403; less detailed |
| Legislative Yuan | Poor | Institutional info only |
| NSB | Minimal | Sparse |

All `.gov.tw` sites serve UTF-8. The TAO adversary source (`gwytb.gov.cn`) uses Simplified Chinese (简体字, zh-CN) — the pipeline must maintain separate Traditional/Simplified Chinese processing pathways. Do not attempt to convert between scripts for cross-referencing; instead, maintain parallel term lists (see the existing Source Intelligence Map's Localized Query Vocabulary for Traditional Chinese terms).

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:

- Presidential statements appear on the Presidential Office site, Executive Yuan (if policy-relevant), and are immediately carried by Focus Taiwan (CNA)
- Defense policy announcements may appear on MND, Presidential Office, Executive Yuan, and MOFA (if they have international dimensions)
- Cross-strait policy statements appear on MAC, Presidential Office, and MOFA simultaneously
- Budget and fiscal announcements cross-post between MOF, Executive Yuan, and MOEA
- Major legislation appears in the Presidential Gazette (promulgation), Executive Yuan Gazette (implementing regulations), and Legislative Yuan Gazette (legislative record)

Implement content-hash deduplication. Use the originating agency as canonical: MOFA for diplomatic content, MND for defense content, MAC for cross-strait content, CBC for monetary policy, MOF for fiscal data. Use the Presidential Office version as canonical when multiple agencies release the same presidential statement.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | MOFA (3 RSS feeds), MND | Every 2 hours | Daily publication; highest signal for diplomatic/defense posture shifts |
| P1-Standard | Presidential Office (RSS), Executive Yuan | Every 2–4 hours | Daily publication; policy-critical |
| P2-Active | MAC, CBC, MOF, MOEA, BOFT | Every 6 hours | Regular publishing; economic/cross-strait data |
| P2-Session | Legislative Yuan | Every 6 hours (session) / 24 hours (recess) | Frequency tied to legislative calendar |
| P2-Low | Gazette, OCAC, Industrial Policy agencies | Every 12–24 hours | Important but slower publication cycle |
| P2-Minimal | NSB | Weekly | Low-frequency publisher; flag any publication as anomaly |
| P2-Adversary | TAO | Every 12 hours | Bi-weekly press conferences; check for crisis-period escalation |
| P2-Derived | NSC | N/A | Captured via Presidential Office monitoring |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| Presidential Office site outage | Presidential Office, NSC (derived) | Monitor Focus Taiwan (`focustaiwan.tw`) which carries presidential releases within minutes. Presidential Office YouTube channel for video statements. X account monitoring. |
| MOFA RSS feed failure | MOFA | HTML scraping of `en.mofa.gov.tw/News.aspx` listing pages. Focus Taiwan carries all MOFA releases. Individual representative office sites (`roc-taiwan.org`) may carry embassy-level releases independently. |
| MND site outage | MND | Monitor @MoNDefense on X. INDSR (`indsr.org.tw`) frequently republishes MND data with analysis. Focus Taiwan and Taipei Times defense correspondents carry MND releases. |
| MAC 403 errors (English site) | MAC | Use Chinese site at `mac.gov.tw` as primary. Focus Taiwan and Taipei Times carry MAC releases in English. |
| CBC site downtime | CBC | Monetary policy decisions are simultaneously reported by Focus Taiwan, CNA, and international wires (Reuters, Bloomberg). Statistical data also available via National Statistics Bureau at `stat.gov.tw`. |
| TAO site inaccessible (from Taiwan/US IPs) | TAO monitoring | Xinhua and CCTV carry TAO press conference summaries. China Times (`chinatimes.com`) reprints TAO-aligned content — use as narrative proxy (see Source Intelligence Map entry for China Times). |
| Legislative Yuan gazette system downtime | Legislative Yuan | SIL-equivalent legislative tracking unavailable — fall back to media coverage of committee proceedings via Taipei Times parliamentary correspondents and Liberty Times legislative bureau. |
| NSB site JavaScript rendering failure | NSB | NSB content primarily reaches the public via media. Monitor Focus Taiwan and Taipei Times for NSB-attributed reporting. |

---

*This supplement should be reviewed quarterly or upon any of the following triggers: change in the Presidency or Premier, major restructuring of cabinet agencies, PRC escalation affecting government communication patterns, or significant changes to .gov.tw web infrastructure.*
