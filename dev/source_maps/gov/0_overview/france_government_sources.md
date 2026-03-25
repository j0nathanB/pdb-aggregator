# Official Government Sources Supplement: FRANCE

**Primary language of political discourse: French**
**Date produced: 2026-03-18**
**Supplement to: Source Intelligence Map — France (Layer 1: Media)**

---

## PURPOSE

This document provides the complete Layer 2 government monitoring configuration for France. It catalogs official web presences across 10 institutional categories, maps entry-point URLs for press releases and official communications, identifies available RSS/Atom feeds, and provides the YAML manifest for pipeline integration.

France's government web infrastructure is decentralized compared to countries that use a unified portal (e.g., Mexico's gob.mx). Each ministry and institution maintains its own domain and content management system, producing distinct URL patterns, feed formats, and access characteristics. The principal shared element is the `.gouv.fr` top-level domain, which identifies official government sites. A significant structural feature of the French executive is the **dual executive system**: the President of the Republic (Élysée) sets strategic direction — particularly on defense, foreign policy, and nuclear deterrence (the *domaine réservé*) — while the Prime Minister (Matignon/info.gouv.fr) manages domestic policy and coordinates government action. Both produce independent press outputs that must be monitored. A second structural feature is the recent migration of the government portal from `gouvernement.fr` to `info.gouv.fr` (301 redirect in place), which affects legacy bookmarks and scrapers.

---

## 1. OFFICIAL GOVERNMENT SOURCES: FRANCE

### 1.1 Head of Government — Présidence de la République (Élysée) & Premier Ministre (Matignon)

#### 1.1a Présidence de la République (Élysée)

| Field | Detail |
|---|---|
| **Institution** | Présidence de la République |
| **Domain** | `elysee.fr` |
| **Entry Point URL** | `https://www.elysee.fr/toutes-les-actualites` |
| **RSS/Atom Feed** | RSS feeds listed at `https://www.elysee.fr/les-flux-rss`. Feed URLs not publicly enumerated on the page — autodiscovery via `<link rel="alternate" type="application/rss+xml">` in page source required. [VERIFY RSS — page exists but feed URLs not directly exposed in content] |
| **Language** | French (primary); English mirror at `elysee.fr/en/all-actualities` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Institutional engagement |
| **Publication Frequency** | Daily. Communiqués de presse, comptes rendus du Conseil des ministres, discours, déclarations, and readouts from bilateral/multilateral meetings. |
| **Content Format** | HTML articles. Some speeches available as PDF and video. |
| **Extraction Method** | HTML scraping of `/toutes-les-actualites` listing page. Articles follow the pattern `/emmanuel-macron/YYYY/MM/DD/slug`. RSS autodiscovery for feed polling if functional. |
| **Editorial Orientation** | Official presidential communication. All content produced by the Service de presse de l'Élysée. Framing reflects presidential priorities and the *domaine réservé* (defense, foreign affairs, nuclear). Under Macron, strong emphasis on European sovereignty, strategic autonomy, and multilateral leadership. |
| **Why This Source** | The single authoritative source for presidential statements, Conseil des ministres outcomes, bilateral summit readouts, and the President's diplomatic positions. In the Fifth Republic's semi-presidential system, the Élysée drives foreign policy and defense — making this the apex government source for diplomatic alignment and security domains. |
| **Access Notes** | No paywall, no authentication. English-language version available. Newsletter ("Cocorico") provides monthly digest. Agenda at `/agenda`. No known anti-scraping measures but rate limiting may apply. |

**Additional entry points:**
- Presidential agenda: `https://www.elysee.fr/agenda`
- English version: `https://www.elysee.fr/en/all-actualities`
- Newsletter: `https://www.elysee.fr/lettre-information`

---

#### 1.1b Premier Ministre / Gouvernement (Matignon)

| Field | Detail |
|---|---|
| **Institution** | Premier Ministre / Services du Gouvernement |
| **Domain** | `info.gouv.fr` (migrated from `gouvernement.fr`, which now 301-redirects) |
| **Entry Point URL** | `https://www.info.gouv.fr/suivre-l-actualite-du-premier-ministre` |
| **RSS/Atom Feed** | [VERIFY RSS — info.gouv.fr replaced gouvernement.fr in recent migration; legacy RSS feeds at gouvernement.fr may be broken] |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Domestic constraints, Economic & technological statecraft, Institutional engagement |
| **Publication Frequency** | Daily. Communiqués, discours du Premier ministre, comptes rendus du Conseil des ministres (joint with Élysée), dossiers de presse for policy initiatives. |
| **Content Format** | HTML. Dossiers de presse in PDF. |
| **Extraction Method** | HTML scraping of the actualités listing page. The migration from gouvernement.fr to info.gouv.fr means URL patterns may differ from historical references. |
| **Editorial Orientation** | Official government position. Under the current cohabitation-adjacent political configuration, Matignon communications reflect the PM's coalition management priorities, which may diverge from Élysée messaging on domestic policy. |
| **Why This Source** | The PM coordinates interministerial action and manages parliamentary relations. Matignon communiqués reveal the government's domestic legislative agenda, budgetary priorities, and coalition dynamics — the domestic constraint dimension that the Élysée typically does not address directly. In periods of cohabitation, Matignon becomes the dominant domestic policy voice. |
| **Access Notes** | No paywall. The `gouvernement.fr` → `info.gouv.fr` redirect is a 301 (permanent). Scrapers targeting gouvernement.fr must be updated. The site returned 403 on some automated requests, suggesting bot protection. |

**Additional entry points:**
- All government news: `https://www.info.gouv.fr/`
- PM-specific news: `https://www.info.gouv.fr/suivre-l-actualite-du-premier-ministre`

---

### 1.2 Foreign Ministry — Ministère de l'Europe et des Affaires étrangères (Quai d'Orsay)

| Field | Detail |
|---|---|
| **Institution** | Ministère de l'Europe et des Affaires étrangères |
| **Domain** | `diplomatie.gouv.fr` |
| **Entry Point URL** | `https://www.diplomatie.gouv.fr/fr/salle-de-presse/` |
| **RSS/Atom Feed** | **Yes — extensive feeds available.** Main news feed: `http://www.diplomatie.gouv.fr/spip.php?page=backend-fd`. Thematic feeds (security/disarmament, economic diplomacy, human rights, etc.) and geographic feeds (Africa, Americas, Asia-Oceania, Europe, North Africa/Middle East, Arctic) plus 195+ country-specific feeds. Full list at: `https://www.diplomatie.gouv.fr/fr/mentions-legales/les-flux-rss-de-france-diplomatie/` |
| **Language** | French (primary); some bilateral communiqués issued bilingually |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Security & defense autonomy |
| **Publication Frequency** | Daily. Communiqués for diplomatic meetings, ministerial travel, treaty actions, sanctions implementation, consular crises, multilateral votes. Higher frequency during G7/EU Council/UNGA periods. |
| **Content Format** | HTML (SPIP CMS). Some formal diplomatic notes in PDF. |
| **Extraction Method** | **RSS polling is the preferred method** — the SPIP-based feed system is well-maintained and comprehensive. HTML scraping of `/fr/salle-de-presse/toutes-les-actualites/` as fallback. |
| **Editorial Orientation** | Official French diplomatic position. Reflects France's doctrinal commitment to multilateralism, European sovereignty, UNSC permanent-member prerogatives, and Francophonie. Under current leadership, emphasis on Indo-Pacific strategy, Sahel recalibration, and EU strategic autonomy. |
| **Why This Source** | The only primary source for France's formal diplomatic positions, treaty ratifications, ambassador appointments, bilateral/multilateral meeting readouts, and sanctions implementation. The extensive RSS feed system makes this the most machine-friendly French government source. |
| **Access Notes** | No paywall. No significant anti-scraping measures. RSS feeds use HTTP (not HTTPS) URLs from the SPIP legacy system — both protocols appear to work. Newsletter subscriptions available at `/fr/mentions-legales/lettres-d-information/`. |

**Key RSS feed URLs:**

| Feed | URL |
|---|---|
| All France Diplomatie news | `http://www.diplomatie.gouv.fr/spip.php?page=backend-fd` |
| Travel advisories | `http://www.diplomatie.gouv.fr/spip.php?page=backend_fcv` |
| Security, Disarmament & Non-Proliferation | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=9035` |
| Economic Diplomacy & Foreign Trade | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=901` |
| Human Rights | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1048` |
| France & United Nations | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1032` |
| Africa (geographic) | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1063` |
| North Africa / Middle East | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1062` |
| Americas | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1059` |
| Asia-Oceania | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=62294` |
| Europe | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=5128` |
| Francophonie | `http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1040` |

**Additional entry points:**
- Press room: `https://www.diplomatie.gouv.fr/fr/salle-de-presse/`
- All news: `https://www.diplomatie.gouv.fr/fr/salle-de-presse/toutes-les-actualites/`
- Ministers' agenda: `https://www.diplomatie.gouv.fr/fr/salle-de-presse/agenda-des-ministres/`

---

### 1.3 Defense Ministry — Ministère des Armées

| Field | Detail |
|---|---|
| **Institution** | Ministère des Armées et des Anciens combattants |
| **Domain** | `defense.gouv.fr` |
| **Entry Point URL** | `https://www.defense.gouv.fr/salle-de-presse` |
| **RSS/Atom Feed** | No RSS feeds identified on the current site. [VERIFY RSS — the ministry's site has been redesigned multiple times; legacy feeds may exist at undiscovered URLs] |
| **Language** | French (primary); English press room at `/en/press-room` |
| **Type** | `legislative_official` |
| **Priority** | **P1** |
| **Domain Coverage** | Security & defense autonomy, Diplomatic alignment |
| **Publication Frequency** | Daily. The press room contains 1,960+ items across categories: communiqués (801), notes aux rédactions (734), agenda (117), dossiers de presse (64), discours (57), and MINARM-specific releases (98). |
| **Content Format** | HTML. Dossiers de presse in PDF. Multimedia content (video, photos) for major operations. |
| **Extraction Method** | HTML scraping of `/salle-de-presse` with category filtering. Content types are filterable by category on the listing page. The site appears to use a Drupal-based CMS. |
| **Editorial Orientation** | Official defense communication. Highly controlled — emphasizes operational capability, defense-industrial achievements, and alliance contributions. Nuclear deterrence details are minimal (presidential *domaine réservé*). Under current minister Sébastien Lecornu (now PM — verify successor), communications emphasize the Loi de programmation militaire (LPM) 2024-2030 execution and European defense cooperation. |
| **Why This Source** | Primary source for OPEX (overseas operations) updates, LPM implementation, defense procurement announcements, arms export decisions, and military posture shifts. Communiqués on joint exercises and alliance activities reveal defense alignment signals. The English press room enables cross-language pipeline processing. |
| **Access Notes** | No paywall. The press room URL redirects from `/salle-presse` to `/salle-de-presse`. Press contacts and archives available at `/presse/agendas-autorites/contacts-presse` and `/presse/archives-presse`. "Actu Défense" weekly video summary at `/presse/actu-defense`. |

**Additional entry points:**
- Communiqués de presse (defense industry): `https://www.defense.gouv.fr/siae/communiques-presse`
- English press room: `https://www.defense.gouv.fr/en/press-room`
- Press archives: `https://www.defense.gouv.fr/presse/archives-presse`
- Actu Défense (weekly video): `https://www.defense.gouv.fr/presse/actu-defense`

---

### 1.4 Parliament — Assemblée nationale & Sénat

#### 1.4a Assemblée nationale (National Assembly)

| Field | Detail |
|---|---|
| **Institution** | Assemblée nationale |
| **Domain** | `assemblee-nationale.fr` |
| **Entry Point URL** | `https://www.assemblee-nationale.fr/dyn/actualites-communiques` [VERIFY URL] |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Feed hub: `https://www.assemblee-nationale.fr/dyn/les-fils-rss-de-l-assemblee-nationale`. Key feeds include parliamentary documents, session reports (comptes rendus), and press releases (communiqués de presse). Feed URL pattern: `https://www.assemblee-nationale.fr/rss/communiques-de-presse.xml` [VERIFY RSS] |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Domestic constraints, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | Daily during session periods (October-June with recesses). Reduced during intersession. Comptes rendus published within 24 hours of each séance. |
| **Content Format** | HTML. Comptes rendus intégraux (verbatim transcripts) in HTML and PDF. Commission reports in PDF. |
| **Extraction Method** | RSS polling for new documents and communiqués. HTML scraping of commission pages for hearing transcripts. Video portal at `assemblee-nationale.fr/video/` for committee hearings. |
| **Editorial Orientation** | Institutional. Reflects majority-coalition framing in official communications, but comptes rendus are verbatim transcripts of all interventions, including opposition. |
| **Why This Source** | Budget votes (including defense budget), constitutional reform debates, treaty ratification, commission d'enquête hearings on defense/foreign affairs, and questions au gouvernement — all originate here. The Commission des affaires étrangères and Commission de la défense nationale et des forces armées produce hearings with ministers and senior officials that contain signals not found in media coverage. |
| **Access Notes** | No paywall. Multiple subdomain generations coexist (www2.assemblee-nationale.fr for legacy content). Site can be slow. Rate limiting observed on some automated requests (429 responses). |

**Additional entry points:**
- RSS feed hub: `https://www.assemblee-nationale.fr/dyn/les-fils-rss-de-l-assemblee-nationale`
- Online services/subscriptions: `https://www.assemblee-nationale.fr/dyn/s-abonner-aux-services-en-ligne-de-l-assemblee-nationale`
- Video portal (committee hearings): `https://www.assemblee-nationale.fr/video/?o=cm`

#### 1.4b Sénat (Senate)

| Field | Detail |
|---|---|
| **Institution** | Sénat |
| **Domain** | `senat.fr` |
| **Entry Point URL** | `https://www.senat.fr/communiques/index.html` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** Press releases: `https://www.senat.fr/rss/presse.rss` (RSS) / `https://www.senat.fr/rss/presse.xml` (Atom). Reports: `https://www.senat.fr/rss/rapports.rss`. Bills & resolutions: `https://www.senat.fr/rss/textes.rss`. Videos: `http://videos.senat.fr/video/videos.rss`. Plus 34 thematic feeds at `https://www.senat.fr/themes/rss/therssX.rss` (where X is theme ID). Full list at: `https://www.senat.fr/flux-rss.html` |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Domestic constraints |
| **Publication Frequency** | Daily during session periods. Committee reports published on a rolling basis. |
| **Content Format** | HTML. Reports in PDF. Comptes rendus in HTML (searchable via `/basile/rechercheSeance.do`). |
| **Extraction Method** | **RSS polling is the preferred method** — well-structured feeds for press releases, reports, and bills. HTML scraping of comptes rendus for full-text commission hearing transcripts. |
| **Editorial Orientation** | Institutional. The Senate's cross-party committees produce some of France's most substantive foreign policy and defense analysis through information reports (*rapports d'information*). |
| **Why This Source** | Treaty ratifications require Senate approval. The Senate's Commission des affaires étrangères, de la défense et des forces armées is France's most authoritative parliamentary body on foreign/defense policy. Its rapports d'information on arms exports, military operations, and diplomatic posture are primary analytical sources that feed media coverage. Ambassador hearings before this commission provide unique access to diplomatic appointments. |
| **Access Notes** | No paywall. RSS feeds are well-maintained and reliable. The video portal (videos.senat.fr) provides recordings of committee hearings. Public Sénat (publicsenat.fr) is the Senate's public television channel — covered in the Layer 1 media map. |

**Additional entry points:**
- RSS feed hub: `https://www.senat.fr/flux-rss.html`
- Press releases: `https://www.senat.fr/communiques/index.html`
- Commission reports search: `https://www.senat.fr/basile/rechercheAutresCRCom.do`
- Session transcripts search: `https://www.senat.fr/basile/rechercheSeance.do`

---

### 1.5 Official Gazette — Journal Officiel de la République Française (JORF) / Légifrance

| Field | Detail |
|---|---|
| **Institution** | Journal Officiel de la République Française (JORF), published by the Direction de l'information légale et administrative (DILA) |
| **Domain** | `journal-officiel.gouv.fr` (portal) / `legifrance.gouv.fr` (legal database) |
| **Entry Point URL** | `https://www.legifrance.gouv.fr/jorf/jo` (daily JORF edition) / `https://www.journal-officiel.gouv.fr/` (portal) |
| **RSS/Atom Feed** | No native RSS on Légifrance or journal-officiel.gouv.fr. **Third-party solution available**: `https://legifrss.org/latest` provides an unofficial RSS proxy of JORF publications with filtering by `nature` (e.g., `decret`, `loi`, `arrete`) and `author` (ministry). Pattern: `https://legifrss.org/latest?nature=decret&author=...`. Email subscription for daily JORF summary available via `https://www.legifrance.gouv.fr/abonnement.do`. JORF open data available at `https://www.data.gouv.fr/datasets/jorf-les-donnees-de-l-edition-lois-et-decrets-du-journal-officiel`. |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | All five domains — the JORF is the constitutional publication vehicle for all laws, decrees, arrêtés, international agreements, and executive orders |
| **Publication Frequency** | Daily (Lois et décrets edition, published every morning). Additional editions for associations, BOAMP (public procurement), and BALO (mandatory financial notices). |
| **Content Format** | HTML on Légifrance (structured legal text with article-level granularity). PDF available for individual texts. The journal-officiel.gouv.fr portal uses an OpenDataSoft-based interface. |
| **Extraction Method** | Email subscription for daily summary (most reliable for alerting). LegifrSS third-party RSS for automated polling. Légifrance API for structured data access (JORF open data via data.gouv.fr). HTML scraping of `/jorf/jo` for daily edition index. |
| **Editorial Orientation** | Official legal publication. No editorial content — purely the text of law. |
| **Why This Source** | Constitutional requirement: no law, decree, international agreement, or regulatory text is legally binding until published in the JORF. This is the only source providing definitive, timestamped legal text. Media reports on legislation are always downstream of JORF publication. Defense-relevant texts include arms export authorizations, military operation decrees, and international agreement ratifications. |
| **Access Notes** | Légifrance imposes bot protection (403 on some automated requests). The `legifrance.gouv.fr/abonnement.do` page provides free email subscriptions for the daily JORF summary. The JORF open data API at data.gouv.fr is the most machine-friendly access path. |

**Additional entry points:**
- Daily JORF on Légifrance: `https://www.legifrance.gouv.fr/jorf/jo`
- JORF open data: `https://www.data.gouv.fr/datasets/jorf-les-donnees-de-l-edition-lois-et-decrets-du-journal-officiel`
- LegifrSS (third-party RSS): `https://legifrss.org/latest`
- Email subscription: `https://www.legifrance.gouv.fr/abonnement.do`

---

### 1.6 Finance Ministry — Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique (Bercy)

| Field | Detail |
|---|---|
| **Institution** | Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique |
| **Domain** | `economie.gouv.fr` |
| **Entry Point URL** | `https://www.economie.gouv.fr/actualites` |
| **RSS/Atom Feed** | **Yes — multiple feeds available.** All news: `https://www.economie.gouv.fr/rss/toutesactualites`. RSS hub page: `https://www.economie.gouv.fr/rss`. Department-specific feeds available at: `https://www.economie.gouv.fr/tous-les-fils-d-infos`. Specific feeds include DAJ (Direction des Affaires juridiques): `https://www.economie.gouv.fr/daj/rss` and Tracfin (anti-money-laundering): `https://www.economie.gouv.fr/tracfin/sabonner-au-flux-rss`. |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | Daily. Communiqués cover fiscal policy, budget execution, tax reform, industrial policy, digital sovereignty initiatives, sanctions implementation, and public procurement. |
| **Content Format** | HTML. Statistical reports and budget documents in PDF. |
| **Extraction Method** | **RSS polling is the preferred method** — the all-news feed provides comprehensive coverage. HTML scraping as fallback. |
| **Editorial Orientation** | Official fiscal and economic policy position. "Bercy" is the metonym for the Finance Ministry. Communications emphasize fiscal responsibility, economic competitiveness, and industrial sovereignty. Under current leadership, strong emphasis on "souveraineté industrielle et numérique" (industrial and digital sovereignty). |
| **Why This Source** | Primary source for budget execution, fiscal policy, sanctions implementation, trade defense measures, and industrial policy. Bercy controls the Direction générale du Trésor (economic diplomacy), the Direction générale des finances publiques (tax collection), and Tracfin (financial intelligence). Essential for the Economic & Technological Statecraft domain. |
| **Access Notes** | No paywall. RSS feeds functional and well-maintained. The site returned 403 on some direct fetches — likely Cloudflare or similar bot protection. The feeds themselves are typically accessible. |

**Additional entry points:**
- RSS hub: `https://www.economie.gouv.fr/rss`
- All department feeds: `https://www.economie.gouv.fr/tous-les-fils-d-infos`
- Direction générale du Trésor (economic diplomacy): `https://www.tresor.economie.gouv.fr/Articles` (news) / `https://www.tresor.economie.gouv.fr/qui-sommes-nous/espace-presse` (press)
- Tracfin (financial intelligence): `https://www.economie.gouv.fr/tracfin`

---

### 1.7 Central Bank — Banque de France

| Field | Detail |
|---|---|
| **Institution** | Banque de France |
| **Domain** | `banque-france.fr` |
| **Entry Point URL** | `https://www.banque-france.fr/fr/communiques-de-presse` (press releases) / `https://www.banque-france.fr/fr/publications-et-statistiques/publications` (publications) |
| **RSS/Atom Feed** | No RSS feeds identified on the current site. [VERIFY RSS — the 2023-2024 site redesign may have removed or relocated legacy feeds. Check `<link>` autodiscovery in page source.] |
| **Language** | French (primary); English versions for major publications at `banque-france.fr/en` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft |
| **Publication Frequency** | Monetary policy decisions: 8 per year (following ECB Governing Council meetings — the Banque de France Governor is a member). Publications: weekly to monthly (Stat Info, Bulletin, financial stability reports). Press releases: 2-5 per week. |
| **Content Format** | PDF for formal publications (Bulletin, financial stability review, monetary policy statements). HTML for press releases and Stat Info. Statistics via Webstat portal (`webstat.banque-france.fr`). |
| **Extraction Method** | HTML scraping of press releases page. PDF download for publications. Webstat API for structured statistical data (SDMX format). |
| **Editorial Orientation** | Technically independent central bank within the Eurosystem. Communications are data-driven and institutionally neutral. The Governor's interventions (speeches, interviews) at `/fr/gouverneur` provide forward-looking signals on monetary policy and financial stability. As a Eurosystem member, the Banque de France's positions interact with ECB policy — divergences signal French-specific economic conditions. |
| **Why This Source** | Authoritative source for French economic data (GDP estimates, inflation, balance of payments, financial stability), sovereign debt market analysis, and the Governor's perspective on ECB monetary policy. The Webstat portal provides structured data access. Publications like the Bulletin de la Banque de France and financial stability assessments shape media and market interpretation of French economic conditions. |
| **Access Notes** | No paywall. Publications portal at `publications.banque-france.fr`. Webstat data portal at `webstat.banque-france.fr` (SDMX-compatible, machine-readable). Statistical publication calendar at `webstat.banque-france.fr/fr/calendrier-publications-statistiques/`. Newsletter subscription available. |

**Additional entry points:**
- Press releases: `https://www.banque-france.fr/fr/communiques-de-presse`
- Press room: `https://www.banque-france.fr/fr/espace-presse`
- Governor interventions: `https://www.banque-france.fr/fr/gouverneur`
- Statistics: `https://www.banque-france.fr/fr/publications-et-statistiques/statistiques`
- Webstat portal: `https://webstat.banque-france.fr/`
- Publications portal: `https://publications.banque-france.fr/`

---

### 1.8 Trade — Direction générale du Trésor (DG Trésor)

| Field | Detail |
|---|---|
| **Institution** | Direction générale du Trésor (DG Trésor), under Ministère de l'Économie |
| **Domain** | `tresor.economie.gouv.fr` |
| **Entry Point URL** | `https://www.tresor.economie.gouv.fr/Articles` (news/articles) |
| **RSS/Atom Feed** | No RSS feeds identified. Newsletter ("Les nouvelles du Trésor") available at `https://www.tresor.economie.gouv.fr/publications/les-nouvelles-du-tresor`. |
| **Language** | French (primary); English institutional page at `/Institutionnel/the-french-treasury` |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Diplomatic alignment |
| **Publication Frequency** | 2-5 articles per week. Publications (Trésor-Éco policy briefs, economic forecasts) on a monthly schedule. |
| **Content Format** | HTML for articles. PDF for Trésor-Éco policy briefs. |
| **Extraction Method** | HTML scraping of `/Articles` listing page. PDF extraction for Trésor-Éco publications. |
| **Editorial Orientation** | Technocratic — the DG Trésor is the operational arm of French economic diplomacy, managing bilateral economic relations, trade negotiations (as part of EU common commercial policy), investment screening (foreign investment control), and France's positions in international financial institutions (IMF, World Bank, EBRD). Communications are analytical and data-driven. |
| **Why This Source** | France does not have a standalone Trade Ministry — trade policy is handled by the DG Trésor under Bercy and coordinated with the EU's Directorate-General for Trade. The DG Trésor manages France's economic counselor network (170+ posts worldwide), foreign investment screening, export credit (via Bpifrance Assurance Export), and positions at international financial institutions. Trésor-Éco policy briefs are influential in shaping French positions on EU trade policy, sanctions design, and macroeconomic coordination. |
| **Access Notes** | No paywall. The site is functional but somewhat institutional. Press space at `/qui-sommes-nous/espace-presse`. The Permanent Representation's economic section in Brussels is also under DG Trésor: `https://www.tresor.economie.gouv.fr/RP-DP/810`. |

**Additional entry points:**
- Publications: `https://www.tresor.economie.gouv.fr/publications`
- Press space: `https://www.tresor.economie.gouv.fr/qui-sommes-nous/espace-presse`
- Trésor International: `https://www.tresor.economie.gouv.fr/tresor-international`
- EU Permanent Rep (economic): `https://www.tresor.economie.gouv.fr/RP-DP/810`

---

### 1.9 Intelligence / National Security Council — SGDSN, DGSE, DGSI

#### 1.9a Secrétariat général de la défense et de la sécurité nationale (SGDSN)

| Field | Detail |
|---|---|
| **Institution** | Secrétariat général de la défense et de la sécurité nationale (SGDSN) |
| **Domain** | `sgdsn.gouv.fr` |
| **Entry Point URL** | `https://www.sgdsn.gouv.fr/publications` |
| **RSS/Atom Feed** | No RSS feeds identified. |
| **Language** | French (English summary page at `/sgdsn-english`) |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Low — 2-5 publications per month. Increased frequency around elections (coordination bulletins) and cyber/influence events. |
| **Content Format** | HTML. Some publications in PDF. |
| **Extraction Method** | HTML scraping of `/publications` listing page. Periodic check recommended given low frequency. |
| **Editorial Orientation** | The SGDSN serves as the secretariat for the Conseil de défense et de sécurité nationale (CDSN), chaired by the President. It is France's closest equivalent to a National Security Council secretariat. Communications are rare and carefully controlled. Under its purview: Vigipirate threat-level system, ANSSI (cybersecurity agency), and coordination of intelligence community oversight. |
| **Why This Source** | The SGDSN is the interministerial coordination hub for defense and national security policy. Its publications are infrequent but high-signal: Vigipirate level changes, Revue nationale stratégique (National Strategic Review), foreign digital interference bulletins (INESIA), and cybersecurity alerts via ANSSI. Any new SGDSN publication should be treated as a high-priority anomaly. |
| **Access Notes** | No paywall. Minimal site. The SGDSN's three stated missions are "Anticiper, Prévenir, Protéger" (Anticipate, Prevent, Protect). Recent publications focus on foreign digital interference ("Ingérences numériques étrangères") and electoral coordination. |

#### 1.9b Direction générale de la sécurité extérieure (DGSE)

| Field | Detail |
|---|---|
| **Institution** | Direction générale de la sécurité extérieure (DGSE) |
| **Domain** | `dgse.gouv.fr` |
| **Entry Point URL** | `https://www.dgse.gouv.fr/` [VERIFY URL] |
| **RSS/Atom Feed** | None. |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy |
| **Publication Frequency** | Negligible. The DGSE's website is primarily a recruitment and institutional presentation portal. |
| **Content Format** | HTML. |
| **Extraction Method** | Periodic check (monthly). Flag any new publication as high-priority anomaly. |
| **Editorial Orientation** | France's external intelligence service (equivalent to MI6/CIA). Effectively silent on operations. The site's primary purpose is recruitment. |
| **Why This Source** | Included for completeness. The DGSE publishes virtually no operational or policy communications. Intelligence-relevant signals surface through: (a) investigative media leaks (Intelligence Online, Mediapart, Le Monde investigations), (b) Defense Ministry communiqués referencing "renseignement," (c) parliamentary Délégation parlementaire au renseignement (DPR) reports, and (d) SGDSN publications. |
| **Access Notes** | Minimal institutional site. No monitoring value beyond detecting organizational/recruitment changes that may indicate institutional shifts. |

#### 1.9c Direction générale de la sécurité intérieure (DGSI)

| Field | Detail |
|---|---|
| **Institution** | Direction générale de la sécurité intérieure (DGSI) |
| **Domain** | `dgsi.interieur.gouv.fr` |
| **Entry Point URL** | `https://www.dgsi.interieur.gouv.fr/` [VERIFY URL] |
| **RSS/Atom Feed** | None. |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | Negligible. Like the DGSE, the DGSI website is primarily institutional and recruitment-focused. |
| **Content Format** | HTML. |
| **Extraction Method** | Periodic check (monthly). |
| **Editorial Orientation** | France's domestic intelligence/counterintelligence service (equivalent to MI5/FBI counterintelligence). Reports to the Minister of the Interior. |
| **Why This Source** | Included for completeness. The DGSI occasionally publishes annual activity reports or "flash" advisories on economic security threats (foreign investment screening, industrial espionage). These are high-signal when they appear. Real DGSI signals surface through: (a) Interior Ministry communiqués on counterterrorism operations, (b) judicial proceedings (the DGSI works closely with the Parquet national antiterroriste), and (c) investigative media. |
| **Access Notes** | Minimal institutional site under interieur.gouv.fr subdomain. |

---

### 1.10 Country-Specific Institutions

#### 1.10a Représentation permanente de la France auprès de l'Union européenne (RPUE)

| Field | Detail |
|---|---|
| **Institution** | Représentation permanente de la France auprès de l'Union européenne |
| **Domain** | `ue.delegfrance.org` |
| **Entry Point URL** | `https://ue.delegfrance.org/` |
| **RSS/Atom Feed** | **Yes.** RSS feed available at `https://ue.delegfrance.org/spip.php?page=rss` (SPIP CMS). |
| **Language** | French |
| **Type** | `government_aligned` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Institutional engagement, Economic & technological statecraft |
| **Publication Frequency** | 3-5 per week during EU Council periods. Lower frequency between summits. Spikes during French EU Council Presidency rotations (last: January-June 2022; next: 2035). |
| **Content Format** | HTML (SPIP CMS). |
| **Extraction Method** | RSS polling via SPIP feed. HTML scraping as fallback. |
| **Editorial Orientation** | Official French position on EU institutional proceedings. The RPUE (~200 staff, ~100 counselors) is France's interface with all EU institutions. Communications cover Council formations, COREPER preparations, and French ministerial participation in EU meetings. |
| **Why This Source** | The RPUE provides the only real-time view of French positions in EU Council negotiations across all policy domains — foreign affairs (FAC), defense (FAC Defense), economic affairs (ECOFIN), trade (TTE), and justice/home affairs (JHA). Media coverage of EU Council meetings rarely captures France's specific positions as clearly as RPUE communiqués. |
| **Access Notes** | No paywall. SPIP-based site with RSS. Social media presence on X, Instagram, Facebook, and LinkedIn. The DG Trésor's economic section at the RPUE is separately accessible at `tresor.economie.gouv.fr/RP-DP/810`. |

#### 1.10b ANSSI (Agence nationale de la sécurité des systèmes d'information)

| Field | Detail |
|---|---|
| **Institution** | Agence nationale de la sécurité des systèmes d'information (ANSSI) |
| **Domain** | `cyber.gouv.fr` (formerly `ssi.gouv.fr`) |
| **Entry Point URL** | `https://cyber.gouv.fr/actualites` [VERIFY URL] |
| **RSS/Atom Feed** | [VERIFY RSS at cyber.gouv.fr] |
| **Language** | French (primary); some advisories in English |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Security & defense autonomy, Economic & technological statecraft |
| **Publication Frequency** | 2-5 per week. Alerts (CERT-FR) published in near-real-time for critical vulnerabilities. |
| **Content Format** | HTML. CERT-FR advisories in structured HTML. |
| **Extraction Method** | HTML scraping of actualités page. CERT-FR advisories via `https://www.cert.ssi.gouv.fr/` [VERIFY — may have migrated to cyber.gouv.fr]. |
| **Editorial Orientation** | France's national cybersecurity authority, attached to the SGDSN. Publishes technical advisories, threat assessments, and cybersecurity policy guidance. ANSSI is a regulatory body under the NIS2 directive transposition. |
| **Why This Source** | ANSSI advisories and threat reports provide the cyber dimension of France's security posture. Attribution of state-sponsored cyberattacks (when published) is a high-signal diplomatic event. ANSSI's role in EU cybersecurity regulation (NIS2, Cyber Resilience Act) makes it relevant to economic statecraft. |
| **Access Notes** | No paywall. CERT-FR advisories are freely accessible. The domain migration from ssi.gouv.fr to cyber.gouv.fr may still be in progress. |

#### 1.10c Overseas Territories — Ministère des Outre-mer

| Field | Detail |
|---|---|
| **Institution** | Ministère des Outre-mer |
| **Domain** | `outre-mer.gouv.fr` |
| **Entry Point URL** | `https://www.outre-mer.gouv.fr/` [VERIFY URL] |
| **RSS/Atom Feed** | [VERIFY RSS] |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Diplomatic alignment, Security & defense autonomy, Domestic constraints |
| **Publication Frequency** | 2-5 per week. |
| **Content Format** | HTML. |
| **Extraction Method** | HTML scraping. |
| **Editorial Orientation** | Official communications on France's overseas territories (Nouvelle-Calédonie, Polynésie française, Mayotte, Guadeloupe, Martinique, Guyane, Réunion, Saint-Pierre-et-Miquelon, Wallis-et-Futuna, etc.). |
| **Why This Source** | France's overseas territories give it the world's second-largest exclusive economic zone (EEZ) and military presence in the Indo-Pacific, Caribbean, and Indian Ocean. Territorial unrest (New Caledonia 2024-2025), sovereignty referendums, and base agreements are strategic signals for France's global military posture. The Sahel withdrawal has increased the relative strategic importance of overseas territories as force-projection platforms. |
| **Access Notes** | No paywall. The site's structure and reliability should be verified as the ministry has undergone several reorganizations. |

#### 1.10d Cour des comptes (Court of Audit)

| Field | Detail |
|---|---|
| **Institution** | Cour des comptes |
| **Domain** | `ccomptes.fr` |
| **Entry Point URL** | `https://www.ccomptes.fr/fr/publications` |
| **RSS/Atom Feed** | [VERIFY RSS at ccomptes.fr] |
| **Language** | French |
| **Type** | `legislative_official` |
| **Priority** | **P2** |
| **Domain Coverage** | Economic & technological statecraft, Domestic constraints |
| **Publication Frequency** | 2-4 reports per month. Major annual report in February. Thematic reports published on a rolling schedule. |
| **Content Format** | HTML summaries. Full reports in PDF (often 100+ pages). |
| **Extraction Method** | HTML scraping of publications listing. PDF download for full reports. |
| **Editorial Orientation** | France's supreme audit institution, constitutionally independent. Reports are analytically rigorous and frequently critical of government policy execution. The Cour has no enforcement power but its findings shape parliamentary debate and media coverage. |
| **Why This Source** | Cour des comptes reports on defense spending, military procurement programs (e.g., SCAF/FCAS, Rafale exports), overseas operations costs, nuclear deterrent expenditure, and diplomatic network efficiency provide the most detailed publicly available financial analysis of France's external action instruments. Reports often surface waste, delays, and cost overruns that Defense Ministry communications omit. |
| **Access Notes** | No paywall. Reports freely downloadable in PDF. The annual report receives extensive media coverage. |

---

## 2. GOVERNMENT SOURCE SUMMARY

| # | Institution | Entry Point URL | RSS Available | Priority | Content Format | Frequency | Independent Domain |
|---|---|---|---|---|---|---|---|
| 1a | Élysée | `elysee.fr/toutes-les-actualites` | [VERIFY] | P1 | HTML | Daily | Yes |
| 1b | PM / info.gouv.fr | `info.gouv.fr/suivre-l-actualite-du-premier-ministre` | [VERIFY] | P1 | HTML/PDF | Daily | Yes |
| 2 | Quai d'Orsay | `diplomatie.gouv.fr/fr/salle-de-presse/` | **Yes** (extensive) | P1 | HTML | Daily | Yes |
| 3 | Ministère des Armées | `defense.gouv.fr/salle-de-presse` | No | P1 | HTML/PDF | Daily | Yes |
| 4a | Assemblée nationale | `assemblee-nationale.fr/dyn/...` | **Yes** (multiple) | P2 | HTML/PDF | Daily (session) | Yes |
| 4b | Sénat | `senat.fr/communiques/index.html` | **Yes** (multiple) | P2 | HTML/PDF | Daily (session) | Yes |
| 5 | JORF / Légifrance | `legifrance.gouv.fr/jorf/jo` | Via LegifrSS (third-party) | P2 | HTML/PDF | Daily | Yes |
| 6 | Bercy (Économie) | `economie.gouv.fr/actualites` | **Yes** (multiple) | P2 | HTML/PDF | Daily | Yes |
| 7 | Banque de France | `banque-france.fr/fr/communiques-de-presse` | No | P2 | PDF/HTML | Variable | Yes |
| 8 | DG Trésor (Trade) | `tresor.economie.gouv.fr/Articles` | No | P2 | HTML/PDF | 2-5/week | Subdomain |
| 9a | SGDSN | `sgdsn.gouv.fr/publications` | No | P2 | HTML/PDF | 2-5/month | Yes |
| 9b | DGSE | `dgse.gouv.fr` | No | P2 | HTML | Negligible | Yes |
| 9c | DGSI | `dgsi.interieur.gouv.fr` | No | P2 | HTML | Negligible | Subdomain |
| 10a | RPUE (EU Perm Rep) | `ue.delegfrance.org` | **Yes** (SPIP) | P2 | HTML | 3-5/week | Yes |
| 10b | ANSSI | `cyber.gouv.fr` | [VERIFY] | P2 | HTML | 2-5/week | Yes |
| 10c | Outre-mer | `outre-mer.gouv.fr` | [VERIFY] | P2 | HTML | 2-5/week | Yes |
| 10d | Cour des comptes | `ccomptes.fr/fr/publications` | [VERIFY] | P2 | PDF/HTML | 2-4/month | Yes |

---

## 3. MONITORING CONFIGURATION

```yaml
# France Government Sources — Layer 2 Monitoring Manifest
# Generated: 2026-03-18
# Supplements: configs/countries/fr.yaml

government_sources:
  # --- P1: HIGH PRIORITY (poll every 2-4 hours) ---

  - id: fr_elysee
    name: Présidence de la République (Élysée)
    domain: elysee.fr
    entry_url: "https://www.elysee.fr/toutes-les-actualites"
    rss_feed: null  # [VERIFY — page exists at /les-flux-rss but feed URLs not exposed]
    language: fr
    type: legislative_official
    priority: P1
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Dual executive apex — drives foreign policy and defense. English mirror at /en/all-actualities. Newsletter 'Cocorico' for monthly digest."

  - id: fr_matignon
    name: Premier Ministre / Gouvernement
    domain: info.gouv.fr
    entry_url: "https://www.info.gouv.fr/suivre-l-actualite-du-premier-ministre"
    rss_feed: null  # [VERIFY — migration from gouvernement.fr may have broken legacy feeds]
    language: fr
    type: legislative_official
    priority: P1
    domain_coverage:
      - domestic_constraints
      - economic_technological_statecraft
      - institutional_engagement
    publication_frequency: daily
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "Migrated from gouvernement.fr (301 redirect). Bot protection observed (403). PM coordinates interministerial action and parliamentary relations."

  - id: fr_quai_dorsay
    name: Ministère de l'Europe et des Affaires étrangères (Quai d'Orsay)
    domain: diplomatie.gouv.fr
    entry_url: "https://www.diplomatie.gouv.fr/fr/salle-de-presse/toutes-les-actualites/"
    rss_feed:
      main_news: "http://www.diplomatie.gouv.fr/spip.php?page=backend-fd"
      travel_advisories: "http://www.diplomatie.gouv.fr/spip.php?page=backend_fcv"
      security_disarmament: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=9035"
      economic_diplomacy: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=901"
      human_rights: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1048"
      france_un: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1032"
      africa: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1063"
      north_africa_middle_east: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1062"
      americas: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=1059"
      asia_oceania: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=62294"
      europe: "http://www.diplomatie.gouv.fr/spip.php?page=backend&id_rubrique=5128"
    language: fr
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
    notes: "Best RSS infrastructure of any French government source. SPIP CMS. 195+ country-specific feeds also available. Full feed list at /fr/mentions-legales/les-flux-rss-de-france-diplomatie/."

  - id: fr_defense
    name: Ministère des Armées
    domain: defense.gouv.fr
    entry_url: "https://www.defense.gouv.fr/salle-de-presse"
    rss_feed: null  # [VERIFY — no feeds found on current site]
    language: fr
    type: legislative_official
    priority: P1
    domain_coverage:
      - security_defense_autonomy
      - diplomatic_alignment
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 2
    notes: "1,960+ items in press room. Category-filterable (communiqués, notes, discours, dossiers). English press room at /en/press-room. Redirect from /salle-presse to /salle-de-presse."

  # --- P2: STANDARD PRIORITY (poll every 6-12 hours) ---

  - id: fr_assemblee
    name: Assemblée nationale
    domain: assemblee-nationale.fr
    entry_url: "https://www.assemblee-nationale.fr/dyn/les-fils-rss-de-l-assemblee-nationale"
    rss_feed:
      communiques_presse: "https://www.assemblee-nationale.fr/rss/communiques-de-presse.xml"  # [VERIFY]
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - domestic_constraints
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: rss_poll_or_html_scrape
    poll_interval_hours: 6
    notes: "Multiple generations of subdomains (www2, www). Rate limiting observed (429). Video portal for committee hearings."

  - id: fr_senat
    name: Sénat
    domain: senat.fr
    entry_url: "https://www.senat.fr/communiques/index.html"
    rss_feed:
      press_releases: "https://www.senat.fr/rss/presse.rss"
      reports: "https://www.senat.fr/rss/rapports.rss"
      bills_resolutions: "https://www.senat.fr/rss/textes.rss"
      videos: "http://videos.senat.fr/video/videos.rss"
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - domestic_constraints
    publication_frequency: "daily_session"
    content_format: html_pdf_mixed
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Best parliamentary RSS infrastructure. 34 thematic feeds (therssX.rss pattern). Commission des affaires étrangères, de la défense et des forces armées is the key committee. Full feed list at /flux-rss.html."

  - id: fr_jorf
    name: Journal Officiel (JORF) / Légifrance
    domain: legifrance.gouv.fr
    entry_url: "https://www.legifrance.gouv.fr/jorf/jo"
    rss_feed:
      legifrss_third_party: "https://legifrss.org/latest"
    language: fr
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
    extraction_method: rss_poll_and_email_subscription
    poll_interval_hours: 6
    notes: "No native RSS. LegifrSS (third-party) supports filtering: ?nature=decret&author=... JORF open data at data.gouv.fr. Email subscription at legifrance.gouv.fr/abonnement.do. Bot protection (403) on main site."

  - id: fr_bercy
    name: Ministère de l'Économie (Bercy)
    domain: economie.gouv.fr
    entry_url: "https://www.economie.gouv.fr/actualites"
    rss_feed:
      all_news: "https://www.economie.gouv.fr/rss/toutesactualites"
      daj: "https://www.economie.gouv.fr/daj/rss"
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: daily
    content_format: html_pdf_mixed
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "Full RSS hub at /rss. Department-specific feeds at /tous-les-fils-d-infos. Tracfin RSS at /tracfin/sabonner-au-flux-rss. Bot protection (403) on some direct requests."

  - id: fr_banque_de_france
    name: Banque de France
    domain: banque-france.fr
    entry_url: "https://www.banque-france.fr/fr/communiques-de-presse"
    rss_feed: null  # [VERIFY — site redesign may have removed feeds]
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
    publication_frequency: variable
    content_format: pdf_html_mixed
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 6
    notes: "Eurosystem member. Governor at /fr/gouverneur. Webstat API (SDMX) at webstat.banque-france.fr for structured data. Publications portal at publications.banque-france.fr. English site available."

  - id: fr_dg_tresor
    name: Direction générale du Trésor
    domain: tresor.economie.gouv.fr
    entry_url: "https://www.tresor.economie.gouv.fr/Articles"
    rss_feed: null
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - diplomatic_alignment
    publication_frequency: "2-5_per_week"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "France's economic diplomacy arm. No standalone Trade Ministry — DG Trésor handles trade under EU common commercial policy. Newsletter at /publications/les-nouvelles-du-tresor."

  - id: fr_sgdsn
    name: SGDSN (Secrétariat général de la défense et de la sécurité nationale)
    domain: sgdsn.gouv.fr
    entry_url: "https://www.sgdsn.gouv.fr/publications"
    rss_feed: null
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "2-5_per_month"
    content_format: html_pdf_mixed
    extraction_method: html_scrape
    poll_interval_hours: 24
    notes: "NSC-equivalent secretariat. Infrequent but high-signal. Vigipirate, Revue nationale stratégique, INESIA (foreign interference). Flag any new publication as anomaly."

  - id: fr_dgse
    name: DGSE (Direction générale de la sécurité extérieure)
    domain: dgse.gouv.fr
    entry_url: "https://www.dgse.gouv.fr/"  # [VERIFY]
    rss_feed: null
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Effectively silent — recruitment/institutional site only. Real signals via Intelligence Online, Mediapart, and parliamentary DPR reports."

  - id: fr_dgsi
    name: DGSI (Direction générale de la sécurité intérieure)
    domain: dgsi.interieur.gouv.fr
    entry_url: "https://www.dgsi.interieur.gouv.fr/"  # [VERIFY]
    rss_feed: null
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: negligible
    content_format: html
    extraction_method: periodic_check
    poll_interval_hours: 168  # weekly
    notes: "Domestic counterintelligence. Occasional economic security flashes. Signals surface via Interior Ministry communiqués and judicial proceedings."

  - id: fr_rpue
    name: Représentation permanente de la France auprès de l'UE (RPUE)
    domain: ue.delegfrance.org
    entry_url: "https://ue.delegfrance.org/"
    rss_feed: "https://ue.delegfrance.org/spip.php?page=rss"
    language: fr
    type: government_aligned
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - institutional_engagement
      - economic_technological_statecraft
    publication_frequency: "3-5_per_week"
    content_format: html
    extraction_method: rss_poll
    poll_interval_hours: 6
    notes: "SPIP CMS with RSS. ~200 staff. Covers French positions across all EU Council formations."

  - id: fr_anssi
    name: ANSSI (Agence nationale de la sécurité des systèmes d'information)
    domain: cyber.gouv.fr
    entry_url: "https://cyber.gouv.fr/actualites"  # [VERIFY]
    rss_feed: null  # [VERIFY]
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - security_defense_autonomy
      - economic_technological_statecraft
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "National cybersecurity authority under SGDSN. CERT-FR advisories for critical vulnerabilities. Domain migration from ssi.gouv.fr to cyber.gouv.fr. Attribution of state-sponsored cyberattacks is high-signal."

  - id: fr_outre_mer
    name: Ministère des Outre-mer
    domain: outre-mer.gouv.fr
    entry_url: "https://www.outre-mer.gouv.fr/"  # [VERIFY]
    rss_feed: null  # [VERIFY]
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - diplomatic_alignment
      - security_defense_autonomy
      - domestic_constraints
    publication_frequency: "2-5_per_week"
    content_format: html
    extraction_method: html_scrape
    poll_interval_hours: 12
    notes: "Overseas territories give France 2nd-largest EEZ globally. Indo-Pacific, Caribbean, Indian Ocean presence. New Caledonia sovereignty tensions are ongoing."

  - id: fr_cour_comptes
    name: Cour des comptes
    domain: ccomptes.fr
    entry_url: "https://www.ccomptes.fr/fr/publications"
    rss_feed: null  # [VERIFY]
    language: fr
    type: legislative_official
    priority: P2
    domain_coverage:
      - economic_technological_statecraft
      - domestic_constraints
    publication_frequency: "2-4_per_month"
    content_format: pdf
    extraction_method: html_scrape_and_pdf_extract
    poll_interval_hours: 24
    notes: "Supreme audit institution. Reports on defense procurement, OPEX costs, nuclear deterrent spending. Annual report in February. Often critical — high analytical value."

# Extraction notes — France-specific considerations
france_specific_config:
  tld_pattern: ".gouv.fr"
  note: "Unlike Mexico's gob.mx, France has no unified government portal. Each ministry maintains independent infrastructure."
  bot_protection:
    - domain: info.gouv.fr
      type: "likely_cloudflare"
      notes: "403 on some automated requests"
    - domain: legifrance.gouv.fr
      type: "likely_cloudflare"
      notes: "403 on automated requests. Use JORF open data API as alternative."
    - domain: economie.gouv.fr
      type: "likely_cloudflare"
      notes: "403 on direct HTML fetch. RSS feeds typically accessible."
    - domain: assemblee-nationale.fr
      type: "rate_limiting"
      notes: "429 responses observed"
  recommended_headers:
    User-Agent: "Mozilla/5.0 (compatible; PDB-Monitor/1.0)"
    Accept-Language: "fr-FR,fr;q=0.9"
  rate_limit: "max 1 request per 3 seconds per domain"
```

---

## 4. INTERPRETIVE CONTEXT

### Source-Weighting Statements

**4.1 Government sources vs. media sources: triangulation protocol**

French government communications are professionalized, carefully framed, and structurally oriented toward projecting competence and consensus. The pipeline must never treat a government source as confirming a fact — it confirms only that the government has chosen to state that fact publicly. The interpretive value lies in three dimensions: (a) what is said, (b) what is omitted, and (c) the timing relative to media coverage.

- **Élysée**: Cross-reference presidential statements against same-day reporting in Le Monde (center-left, close to Élysée sources) and Le Figaro (center-right, Dassault-owned — critical on domestic policy, supportive on defense). Discrepancies between Élysée communiqués and Le Monde's Élysée correspondents' reporting reveal the gap between official messaging and internal policy reality. L'Opinion provides the Macronist-adjacent analytical frame.

- **Matignon / info.gouv.fr**: Cross-reference PM communications against parliamentary coverage by LCP/Public Sénat and Le Monde's political desk. In the current fragmented parliament, divergences between Matignon and Élysée messaging signal coalition stress. Mediapart provides the investigative counterweight on domestic governance.

- **Quai d'Orsay**: Diplomatic communiqués should be triangulated with France 24 (state-funded international broadcaster — detects official framing) and Le Monde diplomatique (critical-structuralist counter-frame). When Quai d'Orsay and France 24 framing diverges from Le Monde's editorial coverage, it typically signals internal debate between diplomatic service professionals and political leadership. Intelligence Online provides the behind-the-scenes diplomatic maneuvering layer.

- **Ministère des Armées**: Defense communiqués report operational capability and institutional achievements but systematically omit casualties, cost overruns, and procurement delays. Cross-reference with Revue Défense Nationale (defense establishment perspective), Le Figaro (strong defense sourcing via Dassault connection), and Cour des comptes reports (financial reality check). Intelligence Online and La Lettre A track defense contract maneuvering and senior military appointments.

- **Parliament (Assemblée + Sénat)**: Legislative communications reflect majority-party framing, but verbatim comptes rendus provide unfiltered access to all parliamentary voices. Cross-reference committee hearing testimony with Contexte (legislative process specialist) and Le Monde's parliamentary desk. Senate rapports d'information are the most substantive publicly available policy analyses — often more rigorous than government documents.

- **Banque de France**: Central bank communications are technically rigorous and less subject to political distortion than ministerial output. Cross-reference with Les Echos (France's leading business daily — LVMH/Arnault owned, strong Bercy sourcing) and the ECB's own communications for eurozone-level context. Divergences between the Governor's public statements and ECB messaging signal France-specific economic tensions.

- **Bercy / DG Trésor**: Economic policy communications emphasize competitiveness, industrial sovereignty, and fiscal responsibility. Cross-reference fiscal data with Les Echos and the Cour des comptes annual report. The DG Trésor's Trésor-Éco policy briefs often preview French positions on EU economic governance debates weeks before formal Council positions.

- **SGDSN / Intelligence services**: SGDSN publications are rare but high-signal — treat any new publication as requiring immediate analysis. Intelligence service communications are effectively nonexistent; signals surface through investigative outlets (Intelligence Online, Mediapart, Le Monde investigations) and parliamentary DPR reports.

**4.2 The decentralized infrastructure effect**

Unlike Mexico's centralized gob.mx platform, France's government web infrastructure is fully decentralized: each institution maintains independent domains, CMS systems (SPIP, Drupal, custom), and publication workflows. This creates:

- **Resilience**: No single point of failure — a Quai d'Orsay outage does not affect Bercy or the Sénat.
- **Complexity**: Multiple extraction patterns required (SPIP RSS for Quai d'Orsay and RPUE; Drupal scraping for Defense; custom HTML for Élysée and info.gouv.fr; SharePoint/custom for Assemblée nationale).
- **Migration risk**: The gouvernement.fr → info.gouv.fr migration demonstrates that French government domains can change without warning. Monitor HTTP redirects and update configurations promptly.
- **Inconsistent bot protection**: Some sites (info.gouv.fr, Légifrance, economie.gouv.fr) deploy bot protection; others (senat.fr, diplomatie.gouv.fr) are fully open. Protection policies can change.

**4.3 The dual executive interpretation challenge**

France's semi-presidential system means that Élysée and Matignon communications must be read in relationship to each other, not independently. Key interpretive principles:

- On foreign policy and defense (the *domaine réservé*), the Élysée is authoritative. Matignon communications on these topics reflect presidential direction.
- On domestic policy, budgetary execution, and parliamentary management, Matignon is the operational authority. Élysée involvement in domestic issues signals either presidential priority-setting or executive tension.
- During cohabitation (President and PM from opposing political families), the two streams become adversarial. Even in non-cohabitation periods, the current fragmented parliament creates significant PM-President divergence on domestic constraints.
- When both Élysée and Matignon issue separate communiqués on the same event, compare framing — divergences indicate internal executive tension.

**4.4 The intelligence silence problem**

France's intelligence agencies (DGSE, DGSI) produce effectively zero public communications. The SGDSN publishes infrequently. This is a structural gap that cannot be filled by monitoring official sites. Intelligence-relevant signals surface through:

- Investigative media: Intelligence Online, Mediapart, Le Monde investigations
- Parliamentary oversight: Délégation parlementaire au renseignement (DPR) annual reports
- Defense Ministry communiqués referencing "renseignement" or intelligence-derived information
- SGDSN publications on foreign interference (INESIA bulletins)
- ANSSI/CERT-FR advisories that attribute cyberattacks to state actors
- JORF publications of organizational/budget changes for intelligence services

The pipeline should not allocate significant resources to polling DGSE/DGSI websites but should flag any new publication as a high-priority anomaly.

---

## 5. PIPELINE INTEGRATION NOTES

### 5.1 RSS-Enabled Sources (Priority for Automation)

Five French government sources provide functional RSS feeds, making them the highest-priority targets for automated monitoring:

1. **Quai d'Orsay (diplomatie.gouv.fr)**: The most comprehensive RSS infrastructure — a main news feed plus thematic feeds (security, economic diplomacy, human rights, etc.), geographic feeds (6 regions), and 195+ country-specific feeds. SPIP-based, well-maintained. Use HTTP URLs (the feeds use `http://` not `https://` in their canonical URLs, though both protocols work).

2. **Sénat (senat.fr)**: Four main feeds (press releases, reports, bills, videos) plus 34 thematic feeds. Well-structured and reliable. The press releases feed (`/rss/presse.rss`) is the most relevant for pipeline monitoring.

3. **Bercy (economie.gouv.fr)**: All-news feed at `/rss/toutesactualites`. Department-specific feeds for DAJ and Tracfin. The all-news feed may include non-policy content (consumer information, job postings) — filter by ministerial attachment when available.

4. **RPUE (ue.delegfrance.org)**: SPIP-based RSS feed. Covers French positions in EU Council formations. Lower volume but high signal-to-noise ratio.

5. **Assemblée nationale**: Feed structure exists but specific URLs require verification. The feed hub page at `/dyn/les-fils-rss-de-l-assemblee-nationale` is the authoritative source.

**Third-party RSS**: LegifrSS (`legifrss.org/latest`) provides an unofficial but functional RSS proxy for the JORF, with filtering by text type and authoring ministry.

All other sources require HTML scraping or periodic page polling.

### 5.2 PDF Extraction Requirements

Several sources publish substantially in PDF:

- **Cour des comptes**: Full reports (100+ pages) in PDF. Text-based, well-structured. Summary pages available in HTML.
- **Banque de France**: Formal publications (Bulletin, financial stability review) in PDF. Text-based. Webstat API provides structured data access (SDMX) for statistical series.
- **JORF / Légifrance**: Legal texts available in both HTML and PDF. HTML is preferred for automated extraction; PDF for archival.
- **Ministère des Armées**: Dossiers de presse in PDF. Communiqués in HTML.
- **Senate/Assembly**: Commission reports and rapports d'information in PDF. Comptes rendus in HTML.

### 5.3 Language and Encoding

All government sources publish in French. Notable bilingual availability:

- **Élysée**: English mirror at `/en/all-actualities` — useful for cross-language validation
- **Quai d'Orsay**: Some bilateral communiqués issued bilingually
- **Ministère des Armées**: English press room at `/en/press-room`
- **Banque de France**: English site at `/en` — major publications available in English
- **SGDSN**: English summary page at `/sgdsn-english`
- **DG Trésor**: English institutional page available

All French government sites use UTF-8 encoding. The pipeline's `languages.primary: fr` configuration in `fr.yaml` is correct; the `metadata: en` field enables English-language sources for pipeline metadata and cross-referencing.

### 5.4 Deduplication Across Sources

French government announcements frequently appear on multiple channels simultaneously:

- A presidential foreign policy statement appears on Élysée, Quai d'Orsay, and info.gouv.fr
- A defense policy announcement appears on Élysée (if presidential), Ministère des Armées, and info.gouv.fr
- Treaty ratifications appear on Quai d'Orsay, Sénat, Assemblée nationale, and JORF
- EU Council outcomes appear on Élysée, Quai d'Orsay, RPUE, and info.gouv.fr
- Fiscal announcements appear on Bercy, info.gouv.fr, and Banque de France
- Defense procurement/budget reports appear on Ministère des Armées, Cour des comptes, and Bercy

Implement content-hash deduplication. Use the originating authority as canonical:
- Foreign policy → Quai d'Orsay
- Defense operational → Ministère des Armées
- Presidential → Élysée
- Legal/regulatory → JORF
- Fiscal/economic → Bercy
- Monetary → Banque de France
- EU institutional → RPUE

### 5.5 Monitoring Schedule Recommendations

| Priority | Sources | Poll Interval | Rationale |
|---|---|---|---|
| P1-Critical | Élysée, Matignon, Quai d'Orsay | Every 2 hours | Daily publication, policy-critical. Quai d'Orsay RSS enables efficient polling. |
| P1-Standard | Ministère des Armées | Every 2 hours | Daily publication, no RSS — requires HTML scraping |
| P2-Active | Sénat, Assemblée, Bercy, RPUE, Banque de France | Every 6 hours | Regular publishing schedule. Sénat/Bercy have RSS. |
| P2-Standard | JORF, DG Trésor, ANSSI, Outre-mer, Cour des comptes | Every 12-24 hours | Important but lower frequency or periodic publication |
| P2-Minimal | SGDSN, DGSE, DGSI | Weekly (SGDSN: daily during elections/crises) | Effectively silent agencies. Flag any publication as anomaly. |

### 5.6 Failure Modes and Fallbacks

| Failure Mode | Affected Sources | Fallback |
|---|---|---|
| info.gouv.fr bot protection (403) | Matignon/Government | Monitor @gouvernementFR and @Matignon on X. info.gouv.fr content is often syndicated to France 24 within minutes. |
| Légifrance bot protection (403) | JORF | Use LegifrSS third-party RSS (`legifrss.org/latest`). JORF open data API at data.gouv.fr. Email subscription at `/abonnement.do`. |
| Quai d'Orsay SPIP RSS failure | Foreign Ministry | HTML scraping of `/fr/salle-de-presse/toutes-les-actualites/` listing page. France 24 syndicates major diplomatic communiqués. |
| Assemblée nationale rate limiting (429) | National Assembly | Reduce poll frequency. Use RSS feeds if verified. LCP (La Chaîne Parlementaire) at lcp.fr provides parallel coverage. |
| defense.gouv.fr restructuring | Defense Ministry | Monitor @Defense_gouv on X. Revue Défense Nationale (defnat.com) provides parallel defense communication tracking. |
| Banque de France site outage | Central Bank | ECB website (ecb.europa.eu) publishes eurozone-level decisions. Les Echos and Bloomberg relay Banque de France communications. Webstat API may remain accessible independently. |
| Domain migration (e.g., gouvernement.fr → info.gouv.fr pattern) | Any `.gouv.fr` domain | Monitor HTTP 301 redirects. The DILA (Direction de l'information légale et administrative) manages the `.gouv.fr` domain space — institutional changes and ministry reorganizations trigger domain changes. |

### 5.7 Seasonal and Cyclical Patterns

French government publication follows distinct cyclical patterns that affect monitoring resource allocation:

| Period | Pattern | Monitoring Adjustment |
|---|---|---|
| January | New Year addresses (Élysée), Cour des comptes annual report preparation | Standard |
| February | Cour des comptes annual report release | Increase Cour des comptes polling |
| March-April | Spring EU Council | Increase RPUE, Quai d'Orsay, Élysée polling |
| May-June | Senate committee reports surge, legislative session close | Increase parliamentary polling |
| July-August | Government recess. Minimal publications except Élysée (foreign travel) | Reduce parliamentary polling; maintain Élysée/Quai d'Orsay |
| September | Budget season (Projet de loi de finances), Assemblée reconvenes | Increase Bercy, Assemblée, Matignon polling |
| October | UNGA (New York), EU Council | Increase Élysée, Quai d'Orsay |
| November-December | Budget vote, year-end EU Council, LPM execution reports | Increase all parliamentary and Bercy sources |
| Electoral periods | SGDSN election coordination bulletins, ANSSI heightened alert | Increase SGDSN to daily polling; add ANSSI CERT-FR |

---

*This supplement should be reviewed quarterly or upon any major government reshuffle (remaniement ministériel), domain migration within the `.gouv.fr` space, or change in the dual executive configuration (e.g., new cohabitation, new Prime Minister appointment).*
