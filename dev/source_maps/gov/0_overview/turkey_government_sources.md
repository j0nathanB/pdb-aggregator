# Official Government Sources Supplement: TURKEY

**Primary language of political discourse: Turkish**
**Date produced: 2026-03-19**
**Supplement to: Source Intelligence Map — Turkey (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for Turkey. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

Turkish government web infrastructure is decentralized — unlike Mexico's unified gob.mx platform, each ministry and institution maintains its own independent domain and content management system. The Presidency (tccb.gov.tr) and Directorate of Communications (iletisim.gov.tr) function as dual hubs for executive messaging, with the Directorate increasingly serving as the consolidated press office for presidential and National Security Council (MGK) communications. Most ministerial sites (hmb.gov.tr, ticaret.gov.tr, msb.gov.tr) are JavaScript-heavy single-page applications that resist simple HTML scraping, requiring headless browser rendering for reliable extraction. The Central Bank (tcmb.gov.tr) is the notable exception, maintaining well-structured RSS feeds and a traditional server-rendered site. Turkey's hyper-presidential system since 2018 means that the Presidency and Directorate of Communications are the authoritative sources for policy signals — ministerial sites often lag or merely republish presidential framing.

---

## 1. OFFICIAL GOVERNMENT SOURCES: TURKEY

### 1.1 Head of Government — Cumhurbaşkanlığı (Presidency of the Republic)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti Cumhurbaşkanlığı (Presidency of the Republic of Türkiye) |
| **Domain** | `tccb.gov.tr` |
| **Entry Point URL** | `https://www.tccb.gov.tr/haberler/` (news) / `https://www.tccb.gov.tr/faaliyetler/basinaciklamalari/` (press statements) |
| **RSS/Atom Feed** | **Yes.** RSS hub at `https://www.tccb.gov.tr/rss` — categories include press statements (Basın Açıklamaları), spokesperson announcements, and news. [VERIFY RSS — page consistently times out; feed URL confirmed via search but live validation not completed] |
| **Language** | Turkish (primary); English edition at `tccb.gov.tr/en/` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints, Institutional engagement |
| **Publication Frequency** | Daily. Multiple items per day covering presidential meetings, phone calls with foreign leaders, decree announcements, and press statements. |
| **Content Format** | HTML. Press statements and news articles are full-text HTML. Some attached PDFs for formal decrees. Video and photo galleries are separate sections. |
| **Extraction Method** | HTML scraping of `/haberler/` and `/faaliyetler/basinaciklamalari/` listing pages. RSS polling if feeds are confirmed functional. The site is server-rendered (not SPA) but loads slowly and intermittently times out. |
| **Editorial Orientation** | Official presidential position. All content is produced by the Presidency's communications directorate. Under Turkey's hyper-presidential system (since 2018 constitutional changes), this is the single most authoritative source for policy direction across all domains. |
| **Why This Source** | The definitive source for presidential statements, foreign leader meetings, decree announcements, cabinet decisions, and the official framing of Turkish foreign and security policy. Under the presidential system, the cabinet serves at the president's pleasure — Presidency communications supersede ministerial statements in authority. |
| **Access Notes** | No paywall. The site intermittently times out under load. English edition provides parallel translations of major statements. Social media accounts (@tcbestepe for Turkish, @trpresidency for English on X) often publish faster than the website. |

**Additional entry points:**
- Speeches: `https://www.tccb.gov.tr/receptayyiperdogan/konusmalar/` (Turkish) / `https://tccb.gov.tr/en/receptayyiperdogan/speeches/` (English)
- Spokesperson statements: `https://www.tccb.gov.tr/en/activites/spokesperson/`
- Presidential decrees: published simultaneously in the Resmî Gazete (see section 1.5)
- Live broadcasts: `https://tccb.gov.tr/canliyayin`
- Cabinet: `https://www.tccb.gov.tr/kabine/`

---

### 1.2 Foreign Ministry — Dışişleri Bakanlığı (MFA)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti Dışişleri Bakanlığı (Ministry of Foreign Affairs) |
| **Domain** | `mfa.gov.tr` |
| **Entry Point URL** | `https://www.mfa.gov.tr/sub.en.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4` (latest press releases, English) |
| **RSS/Atom Feed** | **Yes.** Three feeds available via `https://www.mfa.gov.tr/rss.en.mfa`: (1) Latest Press Releases: `https://www.mfa.gov.tr/en.rss.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4` (2) Latest Developments: `https://www.mfa.gov.tr/en.rss.mfa?7342a8d1-3117-42aa-8ddd-01adb5653889` (3) Other Papers and Links: `https://www.mfa.gov.tr/en.rss.mfa?45b45ccf-8814-4029-9224-5685e8ca3542` |
| **Language** | Turkish (primary); English parallel publication for most diplomatic communications |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily or near-daily. Comunicados issued for bilateral meetings, multilateral votes, consular matters, treaty actions, and regional developments. Press lines (spokesperson responses) published on demand. |
| **Content Format** | HTML on mfa.gov.tr. Formal diplomatic notes sometimes in PDF. The MFA uses a GUID-based URL system rather than human-readable slugs. |
| **Extraction Method** | RSS polling (preferred — MFA is one of only two government sources with confirmed RSS feeds). HTML scraping as fallback. The GUID-based URL pattern requires following links from listing pages rather than constructing URLs. |
| **Editorial Orientation** | Official foreign ministry position. Under Foreign Minister Hakan Fidan (former MIT chief since 2023), communications reflect a distinctly strategic and intelligence-informed worldview. Emphasis on Turkish mediation capacity, regional autonomy, and multi-vector diplomacy. |
| **Why This Source** | The primary source for Turkey's formal diplomatic positions, bilateral/multilateral meeting readouts, treaty actions, consular statements, and press lines on international developments. Media coverage of Turkish foreign policy is invariably derived from MFA comunicados. Fidan's tenure has made MFA communications unusually aligned with intelligence-community framing. |
| **Access Notes** | No paywall, no authentication required. The site is server-rendered and generally accessible. RSS feeds confirmed functional. The Turkish-language site mirrors the English site but uses `/sub.tr.mfa?{GUID}` and `/tr.rss.mfa?{GUID}` patterns. |

**Additional entry points:**
- Press releases and statements: `https://www.mfa.gov.tr/sub.en.mfa?248a41bb-6744-4d91-91f7-500bd7a2cac1`
- Press lines (spokesperson): `https://www.mfa.gov.tr/press-lines.en.mfa`
- Joint declarations: `https://www.mfa.gov.tr/sub.en.mfa?b5e241ce-5e51-4ef2-a6e6-f7453d560256`
- Press conferences: `https://www.mfa.gov.tr/sub.en.mfa?8f787923-31b2-4ba0-92c1-eb548658ce3f`
- Minister speeches: `https://www.mfa.gov.tr/sub.en.mfa?e626bae4-6615-1813-9ab7-4d9e6c71f171`
- Minister interviews: `https://www.mfa.gov.tr/sub.en.mfa?4804c277-892f-4812-9371-1fe393b93a1c`

---

### 1.3 Defense / Security — Millî Savunma Bakanlığı (MSB), Türk Silahlı Kuvvetleri (TSK)

#### 1.3a Millî Savunma Bakanlığı (Ministry of National Defence — MSB)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti Millî Savunma Bakanlığı (Ministry of National Defence) |
| **Domain** | `msb.gov.tr` |
| **Entry Point URL** | `https://www.msb.gov.tr/en-US` (English) / `https://www.msb.gov.tr/` (Turkish) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish (primary); English edition available |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | 3-7 per week. Press releases cover operations (anti-terror strikes, neutralized combatants), bilateral military engagements, NATO activities, and ministerial meetings. |
| **Content Format** | HTML (JavaScript-heavy SPA). Press releases include infographic images with operational statistics (neutralization counts, seized materiel). |
| **Extraction Method** | Headless browser rendering required — the site is a React/Angular SPA that returns minimal HTML without JavaScript execution. API endpoints may exist beneath the SPA but are undocumented. |
| **Editorial Orientation** | Official military communication. Highly controlled — reports operational outcomes (neutralized combatants, seized weapons) using standardized terminology. Never reports own casualties or operational failures. The term "etkisiz hale getirilen" (neutralized) is the standard euphemism. |
| **Why This Source** | The only direct source for official Turkish military operational reporting, cross-border operations (Syria, Iraq), NATO coordination, and defense diplomacy. Frequency and content of bulletins reveal operational tempo and geographic focus. What is not reported is as significant as what is. |
| **Access Notes** | The site consistently times out for external crawlers. Headless browser with Turkish IP or VPN may be required. The English edition at `/en-US` provides parallel content for major releases. |

#### 1.3b Türk Silahlı Kuvvetleri (Turkish Armed Forces — TSK)

| Field | Detail |
|---|---|
| **Institution** | Türk Silahlı Kuvvetleri Genelkurmay Başkanlığı (General Staff of the Turkish Armed Forces) |
| **Domain** | `tsk.tr` |
| **Entry Point URL** | `https://www.tsk.tr/` |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Irregular. The General Staff has been subordinated to the Ministry of Defence since 2018 reforms; most operational communications now route through MSB. TSK site provides institutional information and some operational updates. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. Less complex than MSB site. |
| **Editorial Orientation** | Institutional military. Post-2016 coup attempt reorganization placed TSK under civilian (MSB) authority. Independent communications are now rare. |
| **Why This Source** | Historical institutional presence. Since 2018, most operational press communications route through MSB. TSK site is primarily useful for institutional announcements (command changes, military exercises, ceremony announcements). |
| **Access Notes** | The site is less frequently updated than MSB. Access is generally reliable. |

---

### 1.4 Parliament — Türkiye Büyük Millet Meclisi (TBMM)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Büyük Millet Meclisi (Grand National Assembly of Turkey — TBMM) |
| **Domain** | `tbmm.gov.tr` |
| **Entry Point URL** | `https://www.tbmm.gov.tr/meclis-haber/meclis-baskani` (Speaker news) / `https://www.tbmm.gov.tr/Tutanaklar/SonTutanak` (latest session minutes) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods (October-July with recesses). Reduced during summer recess. Session minutes (tutanaklar) published within days. |
| **Content Format** | HTML. Session minutes are long-form HTML. Committee minutes (komisyon tutanakları) are separate. Laws and decisions available as HTML and PDF. |
| **Extraction Method** | HTML scraping. The site is server-rendered with a structured URL pattern. Session minutes at `/Tutanaklar/`, laws at `/Yasama/Kanunlar`, committee records at `/Tutanaklar/KomisyonTutanaklari`. |
| **Editorial Orientation** | Institutional — reflects the parliamentary majority (AKP-MHP People's Alliance coalition) in Speaker's statements, but session minutes contain full opposition interventions and debate text. |
| **Why This Source** | Committee hearings on foreign affairs, defense, and EU accession reveal intra-coalition tensions and opposition positions. Constitutional amendment debates (particularly regarding Kurdish peace process and presidential term limits), budget deliberations, and treaty ratifications originate here. Session minutes capture the full spectrum of political positions in ways that government-aligned media systematically omit. |
| **Access Notes** | No paywall. Site is generally accessible but can be slow. Historical records from 1908 to present are digitized. The law and decision information system (`/kanun-ve-karar-bilgi-sistemi`) provides structured search across all legislation. |

**Additional entry points:**
- News hub (by category): `/meclis-haber/meclis-baskani` (Speaker), `/meclis-haber/meclis` (Parliament), `/meclis-haber/yasama` (Legislation), `/meclis-haber/komisyon` (Commission), `/meclis-haber/milletvekilleri` (Deputies)
- Press appointments: `/Home/BasinRandevu`
- Session minutes search: `/Tutanaklar/TutanakSorgu`
- Commission minutes: `/Tutanaklar/KomisyonTutanaklari`
- Bill proposals: `/yasama/kanun-teklifleri`
- Laws database: `/Yasama/Kanunlar`
- Presidential decrees: `/yasama/cumhurbaskanligi-kararnamaleri`
- Parliamentary decisions: `/Yasama/Kararlar`

---

### 1.5 Official Gazette — Resmî Gazete

| Field | Detail |
|---|---|
| **Institution** | Resmî Gazete (Official Gazette of the Republic of Türkiye) |
| **Domain** | `resmigazete.gov.tr` |
| **Entry Point URL** | `https://www.resmigazete.gov.tr/` (current day's edition) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the Resmî Gazete is the constitutional publication vehicle for all laws, presidential decrees, regulations, international agreements, and executive orders |
| **Publication Frequency** | Daily (Monday-Saturday). Multiple issues per day possible for urgent decrees. |
| **Content Format** | HTML index pages linking to individual articles. Full-text HTML for recent publications. PDF downloads available for individual issues. Mobile apps for iOS and Android (`T.C. Resmî Gazete`). |
| **Extraction Method** | HTML scraping of daily index page. Date-based navigation for archives. Advanced search with filtering by date range, legislation type, and issuing institution. Full archive from February 7, 1921 to present. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, presidential decree, regulation, or international agreement is legally binding until published in the Resmî Gazete. This is the only source providing definitive, timestamped legal text. Media reports on legislation are always downstream of Resmî Gazete publication. Defense procurement notices, sanctions implementations, trade agreement ratifications, and institutional restructurings all appear here first. |
| **Access Notes** | No paywall. The site is maintained by the Presidency's Department of Legal Affairs and Legislation (Hukuk ve Mevzuat Genel Müdürlüğü). Content is organized into three main sections: Yasama (Legislative), Yürütme ve İdare (Executive & Administrative), and Yargı (Judiciary). Contact: +90 312 525 3427, Beştepe, Ankara. |

---

### 1.6 Finance Ministry — Hazine ve Maliye Bakanlığı (HMB)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti Hazine ve Maliye Bakanlığı (Ministry of Treasury and Finance) |
| **Domain** | `hmb.gov.tr` |
| **Entry Point URL** | `https://www.hmb.gov.tr/haberler` (news) / `https://www.hmb.gov.tr/kategori/basin-duyurulari` (press releases) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish (primary); English edition at `en.hmb.gov.tr` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week. Press releases (basın duyuruları) cover fiscal policy, public debt operations, Treasury borrowing auctions, tax policy, and budget execution. Ministerial announcements (bakanlık duyuruları) cover institutional matters. |
| **Content Format** | JavaScript SPA — requires headless browser rendering. Individual press releases follow URL pattern `https://www.hmb.gov.tr/haberler/{slug}`. PDF attachments for Treasury financing programs, borrowing statistics, and fiscal reports hosted at `ms.hmb.gov.tr/uploads/`. |
| **Extraction Method** | Headless browser rendering required — the site is a React SPA returning "You need to enable JavaScript to run this app" to standard crawlers. PDF download for statistical annexes and financing programs from `ms.hmb.gov.tr`. |
| **Editorial Orientation** | Official fiscal policy position. Under Finance Minister Mehmet Şimşek (since 2023), communications emphasize fiscal discipline, inflation targeting, and market confidence — a deliberate departure from prior unorthodox messaging. Technical language, data-heavy. |
| **Why This Source** | Primary source for Turkey's fiscal policy, Treasury borrowing auctions, public debt data, Medium-Term Program (OVP), and budget execution. Şimşek's communications are closely watched by international markets as a signal of Turkey's commitment to orthodox economic policy. Treasury financing program and borrowing statistics directly affect sovereign credit assessments. |
| **Access Notes** | SPA requires JavaScript. English portal at `en.hmb.gov.tr` provides parallel content for major releases. Press contact: basin@hmb.gov.tr, +90 312 204 74 51. Public finance data also available through dedicated portals. Total 2025 international financing reached USD 13 billion. |

**Additional entry points:**
- Press releases: `https://www.hmb.gov.tr/kategori/basin-duyurulari`
- Ministry announcements: `https://www.hmb.gov.tr/kategori/bakanlik-duyurulari`
- English press releases: `https://en.hmb.gov.tr/en-US/Pages/PRESS-RELEASES`
- Treasury financing program: published as PDF at `ms.hmb.gov.tr/uploads/`
- Medium-Term Program (OVP): `https://en.hmb.gov.tr/mtp`
- Public finance data: `https://en.hmb.gov.tr/public-finance`

---

### 1.7 Central Bank — Türkiye Cumhuriyet Merkez Bankası (TCMB)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyet Merkez Bankası (Central Bank of the Republic of Türkiye — TCMB) |
| **Domain** | `tcmb.gov.tr` |
| **Entry Point URL** | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Press+Releases` (English press releases) |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** RSS hub: `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS`. Five dedicated feeds covering publications, data, governor remarks, press releases, and MPC decisions. |
| **Language** | Turkish (primary); English parallel publication for all major communications |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary Policy Committee (MPC/PPK) decisions: 8 per year (scheduled). Inflation reports: quarterly. Press releases: variable (2-5 per week). Data releases: daily/weekly per data release calendar. |
| **Content Format** | HTML for press releases and announcements. PDF for monetary policy decisions, minutes, inflation reports, and financial stability reports. RSS feeds deliver structured notification data. |
| **Extraction Method** | RSS feeds for structured monitoring (preferred — TCMB has the best machine-readable feeds among Turkish government sources). PDF download and extraction for formal policy documents. HTML scraping for supplementary communications. |
| **Editorial Orientation** | Technically independent central bank. Under Governor Fatih Karahan (since 2024), communications reflect return to orthodox monetary policy — tight policy stance, inflation targeting, data-driven guidance. Independence perception remains sensitive given Turkey's history of presidential intervention in rate decisions. |
| **Why This Source** | TCMB is the sole source for authoritative monetary policy decisions, policy rate announcements, inflation expectations, reserve data, and official economic indicators. MPC decisions move the lira and are cited by all financial media. The degree of policy tightening (or easing) is a primary indicator of whether Turkey's orthodox policy pivot is sustainable. RSS feeds make TCMB the most automation-friendly government data source in Turkey. |
| **Access Notes** | No paywall. No bot protection observed. RSS feeds are well-maintained and reliable. E-alert subscription available at `https://appg.tcmb.gov.tr/ILEIYAZ/view/aboneForm.jsp?dil=EN`. Data release calendar at `https://appg.tcmb.gov.tr/igmvytsfe-dis/en`. English site fully functional. |

**Key RSS feed URLs:**
| Feed | URL |
|---|---|
| Press Releases | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Press+Releases` |
| MPC Decisions | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/MPC+Decisions` |
| Remarks by Governor | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Remarks+by+Governor` |
| Publications | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Publications` |
| Data | `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Data` |

**Additional entry points:**
- Announcements hub: `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements`
- Remarks by Governor: `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Remarks+by+Governor`
- Press briefings: `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Press+Briefings`
- Calendar: `https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Calendar`

---

### 1.8 Trade / Commerce — Ticaret Bakanlığı

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti Ticaret Bakanlığı (Ministry of Trade) |
| **Domain** | `ticaret.gov.tr` / `trade.gov.tr` (English) |
| **Entry Point URL** | `https://ticaret.gov.tr/haberler` (news, Turkish) / `https://www.trade.gov.tr/` (English portal) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish (primary); English edition at `trade.gov.tr` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 3-5 per week. Communications cover trade negotiations, customs regulations, export/import data, bilateral trade agreements, sanctions implementation, and anti-dumping actions. |
| **Content Format** | HTML. The Turkish site at `ticaret.gov.tr` hosts the press center content. The English portal at `trade.gov.tr` is a separate domain for international trade promotion. |
| **Extraction Method** | HTML scraping of `ticaret.gov.tr/haberler`. The English site at `trade.gov.tr` returned 404 errors on the `/en` path — use the root domain. May require headless browser rendering. |
| **Editorial Orientation** | Official trade policy position. Emphasizes Turkey's positioning as a trade hub, customs union modernization with the EU, bilateral trade agreements, and export diversification. |
| **Why This Source** | Primary source for Turkish trade policy: customs union negotiations with the EU, bilateral trade agreements (particularly with Gulf states, African Union, Turkic states), sanctions implementation and circumvention monitoring, anti-dumping investigations, and export control decisions. Turkey's role as a sanctions intermediary (Russia trade) makes Trade Ministry communications a critical monitoring target. |
| **Access Notes** | The Turkish site at `ticaret.gov.tr` hosts the primary press content. The English promotional site at `trade.gov.tr` is a separate infrastructure. The Economy Library (kutuphane.ticaret.gov.tr) provides additional research publications. |

**Additional entry points:**
- Economy Library: `https://kutuphane.ticaret.gov.tr/en/haberler`
- Trade data: published through TurkStat (tuik.gov.tr) rather than the ministry directly

---

### 1.9 Intelligence / National Security — MİT, MGK

#### 1.9a Millî İstihbarat Teşkilatı (National Intelligence Organization — MİT)

| Field | Detail |
|---|---|
| **Institution** | Millî İstihbarat Teşkilatı (National Intelligence Organization — MİT) |
| **Domain** | `mit.gov.tr` |
| **Entry Point URL** | `https://www.mit.gov.tr/en/index.html` (English) / `https://www.mit.gov.tr/` (Turkish) |
| **RSS/Atom Feed** | None available. |
| **Language** | Turkish (primary); English sections available |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Minimal for routine communications. Annual report published once per year (February). Occasional activity pages updated for major operations. |
| **Content Format** | HTML. The site is primarily institutional/informational. Activity reports at `/sayfa_faaliyetler_9.html`. Annual report is a significant publication. |
| **Extraction Method** | Periodic check of mit.gov.tr for any new publications. Annual report monitoring (typically released in February). Activity pages for operational claims. |
| **Editorial Orientation** | Intelligence agency communication — historically silent, but under İbrahim Kalın (MİT President since 2023, former presidential spokesperson), the organization has become notably more public-facing. The 2025 annual report was an unprecedented public intelligence assessment covering global security, counterterrorism, counter-espionage, and intelligence diplomacy. |
| **Why This Source** | Included for both completeness and substantive value. Unlike most intelligence agencies globally, MİT under Kalın has adopted a public communication strategy — the 2025 annual report contained sweeping assessments of global security trends, thwarted espionage networks, and intelligence diplomacy operations. MİT's 2025 budget was TL 36.31 billion. The annual report is a significant primary source for understanding Turkey's threat perception and intelligence priorities. |
| **Access Notes** | The site is accessible without authentication. Content is sparse between annual report releases. The real-time intelligence signal from MİT comes through: (a) the annual report, (b) Anadolu Agency reports citing "security sources," (c) Directorate of Communications announcements on operations, and (d) leaks to government-aligned media (Sabah, Yeni Şafak). |

#### 1.9b Millî Güvenlik Kurulu (National Security Council — MGK)

| Field | Detail |
|---|---|
| **Institution** | Millî Güvenlik Kurulu Genel Sekreterliği (Secretariat General of the National Security Council — MGK) |
| **Domain** | `mgk.gov.tr` |
| **Entry Point URL** | `https://www.mgk.gov.tr/` / `https://www.mgk.gov.tr/index.php/39-duyurular` (announcements) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Bimonthly MGK meeting communiqués (bildiri) — approximately 6 per year. The MGK meets every two months under presidential chairmanship. Supplementary announcements for bilateral security meetings with foreign counterparts. |
| **Content Format** | HTML. Meeting communiqués are the primary output. Institutional information and bilateral meeting reports also published. |
| **Extraction Method** | HTML scraping. The site is a lightweight PHP/Joomla-based site. Communiqués at `/index.php/39-duyurular`. |
| **Editorial Orientation** | Formal consensus document of the military-civilian security establishment. MGK communiqués are carefully negotiated texts that signal the collective position of the President, military chiefs, and key ministers on security threats, foreign policy, and defense priorities. |
| **Why This Source** | MGK communiqués are the single most authoritative signal of Turkey's official threat assessment and security policy direction. The communiqué language — which threats are named, in what order, and with what intensity — is parsed by analysts as the definitive statement of Turkish security doctrine. The 2025 renewal of the National Security Policy Document (MGSB-2025, replacing MGSB-2020) was announced via MGK. However, the primary publication channel for MGK communiqués is the Directorate of Communications (iletisim.gov.tr), not the MGK site itself. |
| **Access Notes** | The MGK site (`mgk.gov.tr`) publishes institutional information and some bilateral meeting reports, but the actual MGK communiqués are consistently published first and most completely on `iletisim.gov.tr`. Monitor both. |

**MGK communiqué publication pattern (via iletisim.gov.tr):**
- January 22, 2025: `https://www.iletisim.gov.tr/turkce/haberler/detay/milli-guvenlik-kurulu-mgk-cumhurbaskani-erdogan-baskanliginda-toplandi-22-01-25`
- May 22, 2025: `https://www.iletisim.gov.tr/turkce/haberler/detay/milli-guvenlik-kurulu-mgk-cumhurbaskani-erdogan-baskanliginda-toplandi-22-05-25`
- July 30, 2025: `https://www.iletisim.gov.tr/turkce/haberler/detay/milli-guvenlik-kurulu-toplantisi-cumhurbaskani-erdogan-baskanliginda-basladi-30-07-25`
- September 30, 2025: `https://www.iletisim.gov.tr/turkce/haberler/detay/milli-guvenlik-kurulu-cumhurbaskani-erdogan-baskanliginda-toplandi-30-09-25`

---

### 1.10 Country-Specific Institutions

#### 1.10a Cumhurbaşkanlığı İletişim Başkanlığı (Directorate of Communications)

| Field | Detail |
|---|---|
| **Institution** | Türkiye Cumhuriyeti İletişim Başkanlığı (Directorate of Communications) |
| **Domain** | `iletisim.gov.tr` |
| **Entry Point URL** | `https://www.iletisim.gov.tr/turkce/haberler/` (Turkish news) / `https://www.iletisim.gov.tr/english` (English portal) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS — the site may have an undocumented feed] |
| **Language** | Turkish (primary); English edition available |
| **Type** | `government_aligned` |
| **Priority** | **P1** |
| **Domain Coverage** | All five domains — functions as the consolidated government press office |
| **Publication Frequency** | Daily. Multiple items per day. The Directorate is the primary publication channel for MGK communiqués, presidential activities, and whole-of-government messaging campaigns. |
| **Content Format** | HTML. Articles follow URL pattern: `iletisim.gov.tr/turkce/haberler/detay/{slug}`. Also publishes the Turkish press review (daily summary of newspaper coverage). |
| **Extraction Method** | HTML scraping of the news listing page. The site has an SSL certificate issue (unable to verify first certificate) that may require certificate validation bypass in the scraper. |
| **Editorial Orientation** | Official government communications directorate. Established by Presidential Decree No. 14 (July 2018), replacing the defunct Press and Information General Directorate. Under Director Burhanettin Duran, functions as the centralized government messaging apparatus — framing narratives, countering "disinformation" (per the Centre for Combatting Disinformation), and publishing the Turkish press review. |
| **Why This Source** | The Directorate of Communications is the de facto consolidated press office for the Turkish presidency and executive branch. It is the primary publication channel for MGK communiqués, presidential press statements, and coordinated government messaging. The Turkish press review (`/english/turkish-press`) provides the government's own daily summary of media coverage — a meta-source revealing which narratives the government considers significant. |
| **Access Notes** | SSL certificate may cause issues for automated fetching. English edition functional. Social media: @Communications on X. The Directorate also operates the Centre for Combatting Disinformation, which publishes weekly disinformation bulletins. |

**Additional entry points:**
- Turkish press review: `https://www.iletisim.gov.tr/ENGLISH/turkish-press`
- English news: `https://www.iletisim.gov.tr/english/haberler/`

#### 1.10b Türk İşbirliği ve Koordinasyon Ajansı (TİKA)

| Field | Detail |
|---|---|
| **Institution** | Türk İşbirliği ve Koordinasyon Ajansı (Turkish Cooperation and Coordination Agency — TİKA) |
| **Domain** | `tika.gov.tr` |
| **Entry Point URL** | `https://tika.gov.tr/en/` (English) / `https://tika.gov.tr/` (Turkish) |
| **RSS/Atom Feed** | None identified. [VERIFY RSS] |
| **Language** | Turkish (primary); English edition available |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement |
| **Publication Frequency** | 3-5 per week. Communications cover development assistance projects across Africa, Central Asia, the Balkans, and the Middle East. |
| **Content Format** | HTML. Project reports and news articles. Turkish Development Assistance Reports published annually as PDF. |
| **Extraction Method** | HTML scraping. The site appears to be a standard CMS. |
| **Editorial Orientation** | Official development agency communication. Emphasizes Turkey's humanitarian and development footprint, soft power projection, and Turkic world engagement. |
| **Why This Source** | TİKA is the primary instrument of Turkish soft power projection and development diplomacy. Its project announcements reveal Turkey's geographic priorities for influence-building — Africa (rapidly expanding), Central Asia (Turkic states), Balkans, and former Ottoman territories. TİKA activity is a leading indicator of diplomatic alignment shifts. Publications section includes Turkish Development Assistance Reports with aggregate ODA data. |
| **Access Notes** | No paywall. English edition provides good coverage of major projects. Press room at `/en/press-room/`. Publications at `/en/press-room/publications/turkish-development-assistance-reports/`. |

#### 1.10c Savunma Sanayii Başkanlığı (SSB — Defence Industry Agency)

| Field | Detail |
|---|---|
| **Institution** | Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (Presidency of Defence Industries — SSB) |
| **Domain** | `ssb.gov.tr` |
| **Entry Point URL** | `https://www.ssb.gov.tr/haberler` (news) |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish (primary); some English content |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | 3-7 per week. News items cover defense procurement contracts, indigenous development milestones (KAAN fighter, Bayraktar drones, MILGEM corvettes, TOGG vehicles), defense exports, IDEF fair coverage, and bilateral defense industry cooperation. |
| **Content Format** | HTML. News articles at `/haberler` with individual items at `/haber/{slug}`. PDF documents for R&D calls, technology roadmaps, and annual reports. Weekly roundup feature ("Türk Savunma Sanayiinde Bu Hafta Neler Oldu?"). |
| **Extraction Method** | HTML scraping of `/haberler` listing page. The site is server-rendered and generally accessible. PDF downloads from `ssb.gov.tr/Images/Uploads/` and `arge.ssb.gov.tr`. |
| **Editorial Orientation** | Official defence industry communication. Under SSB President Prof. Dr. Haluk Görgün, communications emphasize indigenous production ("yerli ve milli"), defense export growth ($10+ billion in 2025), and Turkey's positioning as a top-tier defense exporter. Promotional tone. |
| **Why This Source** | SSB is the central coordinating body for Turkey's defense industry — a strategic priority of the Erdoğan government and a key dimension of Turkey's geopolitical leverage. Procurement contracts, defense export agreements, indigenous development milestones (KAAN fifth-gen fighter, Bayraktar TB3, HISAR air defense), and IDEF exhibition announcements all originate here. Defense exports are a primary instrument of Turkish influence in Africa, Central Asia, and the Gulf. |
| **Access Notes** | Site generally accessible. R&D portal at `arge.ssb.gov.tr`. Defence industry 360 overview at `ssb.gov.tr/savunmasanayii360/`. Annual ALFA reports published as PDF. |

**Additional entry points:**
- R&D portal: `https://arge.ssb.gov.tr/`
- SAGA R&D calls: `https://arge.ssb.gov.tr/Kurumsal/Sayfalar/saga.aspx`
- Defence Industry 360: `https://ssb.gov.tr/savunmasanayii360/tr/hakkimizda`

#### 1.10d ASFAT (Askeri Fabrika ve Tersane İşletme A.Ş.)

| Field | Detail |
|---|---|
| **Institution** | ASFAT A.Ş. (Military Factory and Shipyard Management Inc.) |
| **Domain** | `asfat.com.tr` |
| **Entry Point URL** | `https://www.asfat.com.tr/` [VERIFY URL] |
| **RSS/Atom Feed** | None identified. |
| **Language** | Turkish |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Low — primarily event-driven (IDEF fair, major contract signings, MRO milestones). |
| **Content Format** | HTML. |
| **Extraction Method** | Periodic check. Low-frequency source. |
| **Editorial Orientation** | State defense enterprise. Under General Manager Prof. Mustafa İlbaş, ASFAT is positioning itself as a regional hub for military aircraft MRO (maintenance, repair, overhaul) and naval construction. |
| **Why This Source** | ASFAT manages Turkey's military factories and shipyards — the state-owned manufacturing arm complementing SSB's procurement coordination and private-sector contractors (Baykar, TAI, Roketsan). Naval construction contracts (air defense destroyers, submarines) and MRO agreements with foreign militaries are announced through ASFAT. |
| **Access Notes** | Lower profile than SSB. Major announcements typically covered through SSB and defence media (Defence Turkey, C4Defence). |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | SPA/JS Required |
|---|---|---|---|---|---|---|---|
| 1 | Cumhurbaşkanlığı (Presidency) | `tccb.gov.tr/haberler/` | [VERIFY] | P1 | HTML | Daily | No (slow) |
| 2 | MFA (Dışişleri) | `mfa.gov.tr/sub.en.mfa?{GUID}` | **Yes** (3 feeds) | P1 | HTML | Daily | No |
| 3a | MSB (Defence Ministry) | `msb.gov.tr` | No | P1 | HTML/SPA | 3-7/week | **Yes** |
| 3b | TSK (General Staff) | `tsk.tr` | No | P1 | HTML | Irregular | No |
| 4 | TBMM (Parliament) | `tbmm.gov.tr/meclis-haber/` | No | P2 | HTML | Daily (session) | No |
| 5 | Resmî Gazete | `resmigazete.gov.tr` | No | P2 | HTML/PDF | Daily | No |
| 6 | HMB (Treasury & Finance) | `hmb.gov.tr/haberler` | No | P2 | SPA | 3-7/week | **Yes** |
| 7 | TCMB (Central Bank) | `tcmb.gov.tr/.../Press+Releases` | **Yes** (5 feeds) | P2 | HTML/PDF/RSS | Variable | No |
| 8 | Ticaret Bakanlığı (Trade) | `ticaret.gov.tr/haberler` | No | P2 | HTML | 3-5/week | Partial |
| 9a | MİT (Intelligence) | `mit.gov.tr` | No | P2 | HTML | Annual + minimal | No |
| 9b | MGK (National Security Council) | `mgk.gov.tr` | No | P2 | HTML | Bimonthly | No |
| 10a | İletişim Başkanlığı (Dir. of Comms) | `iletisim.gov.tr/turkce/haberler/` | [VERIFY] | P1 | HTML | Daily | No |
| 10b | TİKA | `tika.gov.tr/en/` | [VERIFY] | P2 | HTML | 3-5/week | No |
| 10c | SSB (Defence Industry) | `ssb.gov.tr/haberler` | No | P2 | HTML | 3-7/week | No |
| 10d | ASFAT | `asfat.com.tr` | No | P2 | HTML | Low | No |

---

## 3. MONITORING CONFIGURATION

```yaml
# Turkey Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-19
# Supplements: configs/countries/tr.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: tr_presidency
    name: Cumhurbaşkanlığı (Presidency)
    domain: tccb.gov.tr
    entry_url: "https://www.tccb.gov.tr/haberler/"
    alt_entry_urls:
      - "https://www.tccb.gov.tr/faaliyetler/basinaciklamalari/"
      - "https://www.tccb.gov.tr/en/news/"
    rss_feed: "https://www.tccb.gov.tr/rss"  # [VERIFY — confirmed via search, not validated live]
    language: tr
    alt_language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape_or_rss
    poll_interval_hours: 2
    notes: "Site intermittently times out. RSS feed existence confirmed but not live-validated. English edition at tccb.gov.tr/en/. Social media (@tcbestepe, @trpresidency) often publishes faster than website."

  - id: tr_mfa
    name: Dışişleri Bakanlığı (MFA)
    domain: mfa.gov.tr
    entry_url: "https://www.mfa.gov.tr/sub.en.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4"
    rss_feed:
      press_releases: "https://www.mfa.gov.tr/en.rss.mfa?ad9093da-8e71-4678-a1b6-05f297baadc4"
      latest_developments: "https://www.mfa.gov.tr/en.rss.mfa?7342a8d1-3117-42aa-8ddd-01adb5653889"
      other_papers: "https://www.mfa.gov.tr/en.rss.mfa?45b45ccf-8814-4029-9224-5685e8ca3542"
    language: tr
    alt_language: en
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
    notes: "Best-structured government source after TCMB. RSS feeds confirmed functional. GUID-based URL system. Turkish feeds use /tr.rss.mfa?{GUID} pattern. Under FM Hakan Fidan (former MIT chief), MFA comms are unusually strategic."

  - id: tr_msb
    name: Millî Savunma Bakanlığı (MSB)
    domain: msb.gov.tr
    entry_url: "https://www.msb.gov.tr/"
    alt_entry_urls:
      - "https://www.msb.gov.tr/en-US"
    rss_feed: null
    language: tr
    alt_language: en
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: "3-7_per_week"
    content_format: html_spa
    extraction_method: headless_browser
    poll_interval_hours: 4
    notes: "React/Angular SPA — requires headless browser rendering. Frequently times out for external crawlers. Reports operational outcomes (neutralized combatants) but never own casualties."

  - id: tr_tsk
    name: Türk Silahlı Kuvvetleri (TSK General Staff)
    domain: tsk.tr
    entry_url: "https://www.tsk.tr/"
    rss_feed: null
    language: tr
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: irregular
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Subordinated to MSB since 2018. Most operational comms now route through MSB. Primarily institutional announcements."

  - id: tr_iletisim
    name: İletişim Başkanlığı (Directorate of Communications)
    domain: iletisim.gov.tr
    entry_url: "https://www.iletisim.gov.tr/turkce/haberler/"
    alt_entry_urls:
      - "https://www.iletisim.gov.tr/english"
      - "https://www.iletisim.gov.tr/ENGLISH/turkish-press"
    rss_feed: null  # [VERIFY]
    language: tr
    alt_language: en
    type: government_aligned
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Primary publication channel for MGK communiqués. SSL certificate issue may require bypass. Turkish press review at /ENGLISH/turkish-press is a valuable meta-source."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: tr_tbmm
    name: Türkiye Büyük Millet Meclisi (TBMM)
    domain: tbmm.gov.tr
    entry_url: "https://www.tbmm.gov.tr/meclis-haber/meclis-baskani"
    alt_entry_urls:
      - "https://www.tbmm.gov.tr/Tutanaklar/SonTutanak"
      - "https://www.tbmm.gov.tr/Tutanaklar/KomisyonTutanaklari"
      - "https://www.tbmm.gov.tr/yasama/kanun-teklifleri"
    rss_feed: null
    language: tr
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Session minutes contain full debate text. Committee minutes (foreign affairs, defense, EU accession) reveal positions not in media. Historical archive from 1908."

  - id: tr_resmi_gazete
    name: Resmî Gazete (Official Gazette)
    domain: resmigazete.gov.tr
    entry_url: "https://www.resmigazete.gov.tr/"
    rss_feed: null
    language: tr
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
    notes: "Constitutional publication requirement — all laws, decrees, regulations legally binding only upon publication here. Archive from 1921. Three sections: Yasama, Yürütme ve İdare, Yargı."

  - id: tr_hmb
    name: Hazine ve Maliye Bakanlığı (HMB)
    domain: hmb.gov.tr
    entry_url: "https://www.hmb.gov.tr/kategori/basin-duyurulari"
    alt_entry_urls:
      - "https://www.hmb.gov.tr/haberler"
      - "https://en.hmb.gov.tr/en-US/Pages/PRESS-RELEASES"
    rss_feed: null
    language: tr
    alt_language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html_spa
    extraction_method: headless_browser
    poll_interval_hours: 6
    notes: "React SPA — returns 'You need to enable JavaScript' to standard crawlers. PDF reports at ms.hmb.gov.tr/uploads/. Contact: basin@hmb.gov.tr. Under Şimşek, signals orthodox fiscal policy."

  - id: tr_tcmb
    name: Türkiye Cumhuriyet Merkez Bankası (TCMB)
    domain: tcmb.gov.tr
    entry_url: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Announcements/Press+Releases"
    rss_feed:
      press_releases: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Press+Releases"
      mpc_decisions: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/MPC+Decisions"
      governor_remarks: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Remarks+by+Governor"
      publications: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Publications"
      data: "https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Bottom+Menu/Other/RSS/Data"
    language: tr
    alt_language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_rss_mixed
    extraction_method: rss_poll_and_pdf_extract
    poll_interval_hours: 6
    notes: "Best machine-readable government source in Turkey. 5 RSS feeds covering all major output categories. MPC decisions 8x/year. E-alert subscription available. Full English site. No bot protection."

  - id: tr_ticaret
    name: Ticaret Bakanlığı (Ministry of Trade)
    domain: ticaret.gov.tr
    entry_url: "https://ticaret.gov.tr/haberler"
    alt_entry_urls:
      - "https://www.trade.gov.tr/"
    rss_feed: null
    language: tr
    alt_language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "English trade promotion site at trade.gov.tr is separate infrastructure. Critical for sanctions circumvention monitoring (Russia trade). Economy Library at kutuphane.ticaret.gov.tr."

  - id: tr_mit
    name: Millî İstihbarat Teşkilatı (MİT)
    domain: mit.gov.tr
    entry_url: "https://www.mit.gov.tr/en/index.html"
    rss_feed: null
    language: tr
    alt_language: en
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: annual_plus_minimal
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Annual report (February) is a significant primary source under Kalın's public-facing approach. 2025 budget: TL 36.31B. Flag any new publication as high-priority anomaly."

  - id: tr_mgk
    name: Millî Güvenlik Kurulu (MGK)
    domain: mgk.gov.tr
    entry_url: "https://www.mgk.gov.tr/index.php/39-duyurular"
    rss_feed: null
    language: tr
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: bimonthly
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 168  # weekly — communiqués published on iletisim.gov.tr first
    notes: "Bimonthly communiqués are THE authoritative security doctrine signal. Primary publication via iletisim.gov.tr, not mgk.gov.tr. Joomla-based site."

  - id: tr_tika
    name: TİKA
    domain: tika.gov.tr
    entry_url: "https://tika.gov.tr/en/"
    rss_feed: null  # [VERIFY]
    language: tr
    alt_language: en
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Soft power projection instrument. Geographic distribution of projects reveals diplomatic alignment priorities (Africa expanding, Central Asia, Balkans)."

  - id: tr_ssb
    name: Savunma Sanayii Başkanlığı (SSB)
    domain: ssb.gov.tr
    entry_url: "https://www.ssb.gov.tr/haberler"
    rss_feed: null
    language: tr
    type: government_aligned
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "3-7_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 6
    notes: "Central defense procurement coordinator. Weekly roundup feature. R&D at arge.ssb.gov.tr. Defense exports >$10B in 2025. IDEF coverage intensive."

  - id: tr_asfat
    name: ASFAT A.Ş.
    domain: asfat.com.tr
    entry_url: "https://www.asfat.com.tr/"  # [VERIFY URL]
    rss_feed: null
    language: tr
    type: government_aligned
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: low
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "State military factory/shipyard enterprise. Major announcements covered via SSB and defence media. MRO hub strategy under GM İlbaş."
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

Turkish government communications operate within a hyper-presidential information architecture where the Presidency and Directorate of Communications set the frame, and ministerial communications elaborate within that frame. The pipeline must treat government sources as signaling instruments — they confirm what the government wants known, when it wants it known, and how it wants it framed. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to independent media coverage.

- **Presidency (TCCB)**: Cross-reference presidential statements against same-day Anadolu Agency (AA) coverage for the official frame, and against Cumhuriyet and Sozcu for the opposition reading. Discrepancies between TCCB statements and AA reporting reveal internal messaging calibration. When TCCB and AA diverge on emphasis, it signals evolving policy positioning.

- **MFA**: Diplomatic communications should be triangulated with Al-Monitor Turkey (independent Washington-based analysis), Hurriyet Daily News (government-aligned English window), and Middle East Eye (investigative, especially on Syria/Libya/Kurdish dimensions). When MFA press lines use notably stronger or softer language than AA on the same event, it indicates inter-institutional positioning — particularly relevant given Fidan's intelligence background and direct relationship with the President.

- **MSB/TSK**: Military bulletins report operations using standardized "neutralized" (etkisiz hale getirilen) language but never own casualties, operational setbacks, or procurement costs. Cross-reference with Defence Turkey and C4Defence (industry-aligned, with operational access), Mezopotamya Agency/MA (Kurdish perspective on cross-border operations), and Bianet (human rights dimensions of military operations). The discrepancy between MSB neutralization claims and independent reporting is itself an analytical data point.

- **İletişim Başkanlığı (Directorate of Communications)**: This is the meta-source — its daily Turkish press review reveals which media narratives the government considers significant enough to amplify or counter. Cross-reference its framing against Medyascope (independent video analysis), T24 (independent long-form), and Duvar English (stories government-aligned media suppress). MGK communiqués published via the Directorate should be analyzed for threat-ordering (which threats named first) and intensity language.

- **TCMB**: Monetary policy decisions are technically rigorous but the selection of what to emphasize in communications reflects institutional positioning vis-à-vis presidential preferences. Cross-reference with Bloomberg HT (the only dedicated financial platform), El Financiero equivalents, and IMF Article IV consultations. The degree of divergence between TCMB guidance and presidential statements on rates is the key independence indicator.

- **HMB (Treasury & Finance)**: Under Şimşek, communications signal orthodox fiscal commitment — but presentation framing (base period selection, seasonal adjustments) can obscure underlying trends. Cross-reference with Bloomberg HT, Financial Times Turkey coverage, and Ahval News (independent economic analysis).

- **SSB/ASFAT**: Defense industry communications are systematically promotional — export figures and indigenous development milestones are emphasized while cost overruns, delivery delays, and performance issues are omitted. Cross-reference with Defence Turkey and C4Defence (which have industry access but are industry-aligned), Jane's Defence Weekly (external technical assessment), and SIPRI data (independent arms trade statistics).

**4.2 The dual-hub architecture: Presidency + Directorate of Communications**

Unlike Mexico's centralized gob.mx platform, Turkey's government web infrastructure is decentralized across independent domains. However, at the executive level, two sites function as a dual-hub:

1. **tccb.gov.tr** (Presidency) — publishes presidential activities, statements, speeches, and decree announcements
2. **iletisim.gov.tr** (Directorate of Communications) — publishes consolidated government messaging, MGK communiqués, the daily Turkish press review, and coordinated narrative campaigns

These two sources together capture the executive branch's complete public communication output. Ministerial sites (MSB, HMB, ticaret.gov.tr) provide domain-specific detail but rarely break new policy ground — policy direction flows from the presidency downward.

**4.3 The MİT transparency shift**

Turkey's intelligence agency (MİT) has undergone an unusual transformation under İbrahim Kalın (appointed 2023). Unlike most intelligence agencies globally, MİT now publishes a substantial annual report with assessments of global security trends, counterterrorism operations, counter-espionage successes, and intelligence diplomacy activities. The 2025 annual report included details on thwarted espionage networks and expanded technical intelligence capabilities (AI, satellite intelligence, cyber intelligence). This represents a deliberate public communication strategy — the annual report is a primary source for understanding Turkey's official threat perception. However, operational intelligence continues to surface through:
- Anadolu Agency reports citing "security sources" (güvenlik kaynakları)
- Directorate of Communications announcements on counter-terror operations
- Government-aligned media (Sabah, Yeni Şafak) receiving selective leaks
- MSB operational bulletins referencing intelligence-led targeting

The pipeline should monitor MİT's site weekly for the annual report (typically February) and flag any other publication as a high-priority anomaly.

**4.4 The SPA problem: JavaScript-heavy government sites**

Three critical government sources — MSB (defence), HMB (treasury/finance), and partially ticaret.gov.tr (trade) — are built as JavaScript single-page applications (React/Angular) that return minimal HTML to standard crawlers. This creates a structural extraction challenge:

- **MSB**: Returns effectively empty HTML without JS rendering. Requires Playwright/Puppeteer headless browser with Turkish locale settings.
- **HMB**: Returns "You need to enable JavaScript to run this app." Same headless browser requirement.
- **Ticaret.gov.tr**: Partially rendered but some content requires JS.

In contrast, TCMB, MFA, TBMM, Resmî Gazete, and SSB are server-rendered and accessible to standard HTTP crawlers.

**4.5 The MGK communiqué: Turkey's most authoritative security signal**

The bimonthly MGK communiqué (bildiri) is the single most important government document for security and foreign policy analysis. It represents the formal consensus of the President, Chief of General Staff, service commanders, and key ministers (Foreign Affairs, Interior, Defence, Justice). Analytical protocol:

- **Threat ordering**: Which threats are named first indicates prioritization (PKK/YPG, Fethullahist Terrorist Organization/FETÖ, ISIS, Aegean/Mediterranean disputes, etc.)
- **Intensity language**: Escalation from "monitoring" (takip ediliyor) to "necessary measures will be taken" (gerekli tedbirler alınacaktır) to "determined struggle will continue" (kararlı mücadele sürdürülecektir) signals operational intent
- **Omissions**: Threats that disappear from communiqués indicate de-prioritization or deliberate silence (relevant for Kurdish peace process monitoring)
- **New terminology**: Introduction of new threat categories or geographic references signals emerging priorities

The National Security Policy Document (MGSB), renewed in January 2025 as MGSB-2025, is the classified strategic framework — the communiqué is the only public window into its content.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 Decentralized Architecture — No Shared Extraction Pattern

Unlike Mexico's gob.mx platform (one extraction pattern for seven agencies), Turkey's government sources each maintain independent infrastructure requiring separate scraper configurations:

- **Server-rendered sites** (standard HTML scraping): MFA, TBMM, Resmî Gazete, SSB, TİKA, MGK, MİT, TSK
- **SPA sites** (headless browser required): MSB, HMB
- **Intermittent/slow sites** (retry with backoff): TCCB (Presidency), ticaret.gov.tr
- **RSS-enabled sites** (preferred polling): MFA (3 feeds), TCMB (5 feeds), possibly TCCB (unverified)
- **SSL-problematic sites**: iletisim.gov.tr (certificate verification failure observed)

No single scraper module can service all sources. Each requires independent configuration.

### 5.2 RSS-Enabled Sources (Priority for Automation)

Two government sources provide confirmed functional RSS feeds:

1. **MFA (Dışişleri Bakanlığı)**: Three feeds covering press releases, latest developments, and other papers. GUID-based URL system. Available in both Turkish (`/tr.rss.mfa?{GUID}`) and English (`/en.rss.mfa?{GUID}`). This is the most reliable way to monitor Turkish diplomatic communications.

2. **TCMB (Central Bank)**: Five feeds covering press releases, MPC decisions, governor remarks, publications, and data releases. The most comprehensive RSS infrastructure among Turkish government sources. English feeds available. E-alert email subscription also available as a backup channel.

A third source — **TCCB (Presidency)** — has an RSS hub at `tccb.gov.tr/rss` confirmed via search results, but live validation was not completed due to persistent timeouts. If confirmed functional, this would be a high-value automation target.

All other sources require HTML scraping or headless browser rendering.

### 5.3 PDF Extraction Requirements

Four sources publish primarily or substantially in PDF:
- **Resmî Gazete**: All legal texts available as PDF alongside HTML. Text-based, well-structured.
- **TCMB**: Monetary policy decisions, minutes, inflation reports, and financial stability reports are multi-page PDF. Text-based, well-structured. Bilingual (Turkish + English).
- **HMB**: Treasury financing programs, borrowing statistics, and fiscal reports published as PDF at `ms.hmb.gov.tr/uploads/`. Tables require structured extraction.
- **SSB**: R&D calls, technology roadmaps, and annual ALFA reports in PDF at `ssb.gov.tr/Images/Uploads/` and `arge.ssb.gov.tr`.

### 5.4 Language and Encoding

All government sources publish primarily in Turkish. English parallel editions are available for:
- **Full English sites**: TCCB (`/en/`), MFA (`.en.mfa` pattern), TCMB (full English site), HMB (`en.hmb.gov.tr`), İletişim Başkanlığı (`/english`), TİKA (`/en/`), MSB (`/en-US`)
- **No English edition**: TBMM, Resmî Gazete, Ticaret Bakanlığı (domestic site), MGK, SSB (mostly Turkish, some English), ASFAT

The pipeline should prefer English feeds where available for keyword monitoring efficiency, falling back to Turkish-language scraping with the localized query vocabulary from the Layer 1 Source Intelligence Map. All sites use UTF-8 encoding. The MFA GUID-based URL system requires special handling — URLs are not human-readable and must be followed from listing pages or RSS feeds.

### 5.5 Deduplication Across Sources

Government announcements frequently appear on multiple channels simultaneously:
- Presidential statements appear on TCCB, İletişim Başkanlığı, and Anadolu Agency
- MGK communiqués appear on İletişim Başkanlığı, TCCB, and MGK's own site (delayed)
- Defense operations appear on MSB, TSK, and İletişim Başkanlığı
- Presidential decrees appear on TCCB and Resmî Gazete
- Monetary policy decisions appear on TCMB (all 5 RSS feeds) and HMB
- Trade agreements appear on Ticaret Bakanlığı, MFA, and Resmî Gazete
- Defense procurement appear on SSB, MSB, and ASFAT

Implement content-hash deduplication. Use Resmî Gazete as the canonical version for legal texts. Use the originating agency (MFA for diplomatic, MSB for military, TCMB for monetary) as canonical for operational communications. Use İletişim Başkanlığı as canonical for MGK communiqués.

### 5.6 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | İletişim Başkanlığı, MFA (RSS), TCCB | Every 2 hours | Daily publication, policy-critical, consolidated executive messaging |
| P1-Standard | MSB, TSK | Every 4 hours (MSB) / 12 hours (TSK) | MSB is primary military source; TSK subordinated since 2018 |
| P2-Active | TBMM, Resmî Gazete, HMB, TCMB (RSS), Ticaret, SSB | Every 6 hours | Regular publishing schedule, structured data |
| P2-Low | TİKA, MGK, ASFAT | Every 12 hours (TİKA) / weekly (MGK, ASFAT) | Lower frequency, event-driven |
| P2-Minimal | MİT | Weekly | Annual report + anomaly detection |

### 5.7 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| TCCB timeout/unavailability | Presidency | Monitor @tcbestepe (Turkish) and @trpresidency (English) on X. İletişim Başkanlığı republishes presidential content. |
| MSB SPA rendering failure | Defence Ministry | Anadolu Agency (aa.com.tr) publishes MSB bulletins within minutes. Defence Turkey and C4Defence provide parallel coverage. Monitor @taboraborcom on X. |
| HMB SPA rendering failure | Treasury & Finance | Bloomberg HT covers all major HMB announcements. PDF reports accessible directly at ms.hmb.gov.tr/uploads/. Monitor @HMBakanligi on X. |
| İletişim.gov.tr SSL failure | Directorate of Communications | TCCB carries parallel presidential content. MGK communiqués also published (delayed) on mgk.gov.tr. AA carries all major government statements. |
| MFA RSS feed interruption | Foreign Ministry | HTML scraping of mfa.gov.tr press release listing page as fallback. Daily Sabah and Hurriyet Daily News carry MFA statements in English. |
| TCMB RSS feed interruption | Central Bank | HTML scraping of TCMB announcements page. Bloomberg HT and Reuters carry all MPC decisions instantly. E-alert email subscription as backup. |
| Resmî Gazete unavailability | Official Gazette | Mobile apps (iOS/Android) may remain functional. Mevzuat.gov.tr (legislation information system) provides parallel access to legal texts. |
| General Turkish site access issues | All Turkish gov sites | Some Turkish government sites implement geo-blocking or challenge pages for non-Turkish IPs. Turkish VPN/proxy may be required for reliable automated access. |

---

*This supplement should be reviewed quarterly or upon any major restructuring of Turkish government web infrastructure, change in ministerial portfolios, or constitutional/institutional reform affecting the executive-legislative balance.*
