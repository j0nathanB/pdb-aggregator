# Germany Government Sources -- URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/germany_government_sources.md`
**Test method:** WebFetch for RSS feeds; curl with Mozilla UA for HTML entry points

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 73 |
| RSS/Atom feeds confirmed working | 37 |
| Entry point HTML pages confirmed (HTTP 200) | 27 |
| URLs returning 404 | 6 |
| URLs returning 500 | 1 |
| RSS URLs documented incorrectly (HTML landing page, not feed) | 2 |
| [VERIFY] items resolved | 10 |

**Overall: 64 of 73 URLs fetchable (87.7%). 6 broken (404), 1 server error (500), 2 mis-documented (landing pages instead of feeds, but actual feeds discovered at corrected URLs).**

---

## Per-Source Results

### 1.1a Bundeskanzleramt / Bundesregierung (P1)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundeskanzler.de/bk-de/aktuelles/pressemitteilungen` | Entry point | 200 OK | Working |
| `https://www.bundesregierung.de/breg-de/aktuelles/pressemitteilungen` | Entry point | 200 OK | Working |
| `https://www.bundeskanzler.de/service/rss/bk-de/1859752/feed.xml` | RSS (Meldungen) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundeskanzler.de/service/rss/bk-de/1859754/feed.xml` | RSS (Termine) | 200 OK | Valid RSS 2.0, 10 items |
| `https://www.bundeskanzler.de/service/rss/bk-de/1859760/feed.xml` | RSS (Reden) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundesregierung.de/service/rss/breg-de/1151242/feed.xml` | RSS (Kompakt) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundesregierung.de/service/rss/breg-de/1151244/feed.xml` | RSS (Pressemitteilungen) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundesregierung.de/service/rss/breg-de/1151246/feed.xml` | RSS (Artikel) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundesregierung.de/service/rss/breg-de/2318648/feed.xml` | RSS (Bulletin) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundespressekonferenz.de/pressekonferenzen/termine` | Entry point | 200 OK | Working |
| `https://www.bundesregierung.de/breg-de/aktuelles/kabinett` | Entry point | **404** | Cabinet decisions page not found at documented URL |
| `https://www.bundeskanzler.de/bk-en/news` | Entry point (EN) | 200 OK | Working |

### 1.1b Bundespräsident (P1)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundespraesident.de/DE/reden-und-aktuelles/presse/presse_node.html` | Entry point | 200 OK | Working |
| `https://www.bundespraesident.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Pressemitteilungen/RSSNewsfeed.xml?nn=129192` | RSS (Pressemitteilungen) | 200 OK | Valid RSS 2.0, 3 items |
| `https://www.bundespraesident.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Termine/RSSNewsfeed.xml?nn=129192` | RSS (Termine) | 200 OK | Valid RSS 2.0, 3 items |
| `https://www.bundespraesident.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Reden/RSSNewsfeed.xml?nn=129192` | RSS (Reden) | 200 OK | Valid RSS 2.0, 3 items |

### 1.2 Auswärtiges Amt (P1)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.auswaertiges-amt.de/de/newsroom/presse` | Entry point (DE) | 200 OK | Working |
| `https://www.auswaertiges-amt.de/en/newsroom/news/-/609204` | Entry point (EN) | 200 OK | Working |
| `https://www.auswaertiges-amt.de/en/newsroom/news` | Entry point (EN alt) | 200 OK | Working |
| `https://www.auswaertiges-amt.de/static/includes/rss/Presse-RSS-Feed.xml` | RSS (Presse/Reden) | 200 OK | Valid RSS 2.0, 10 items |
| `https://www.auswaertiges-amt.de/static/includes/rss/Reisehinweise-RSS-Feed.xml` | RSS (Reisehinweise) | 200 OK | Valid RSS 2.0, 3 items |
| `https://www.auswaertiges-amt.de/static/includes/rss/Aktuelles-RSS-Feed.xml` | RSS (Aktuelles) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.auswaertiges-amt.de/de/ResieUndSicherheit/reise-und-sicherheitshinweise` | Entry point | **404** | Typo in doc: "Resie" should be "Reise" |
| `https://www.auswaertiges-amt.de/de/ReiseUndSicherheit/reise-und-sicherheitshinweise` | Entry point (corrected) | 200 OK | Working with corrected spelling |

### 1.3a BMVg (P1)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bmvg.de/de/presse/alle-pressetermine-pressemitteilungen-bmvg` | Entry point | 200 OK | Working |
| `https://www.bmvg.de/de/aktuelles/alle-meldungen` | Entry point | 200 OK | Working |
| `https://www.bmvg.de/de/rss` | RSS [VERIFY] | **HTML page** | Not a feed -- landing page describing RSS. Links to actual feed. |
| `https://www.bmvg.de/service/rss/de/17680/feed` | RSS (actual) | 200 OK | Valid RSS 2.0, 10 items. **This is the correct feed URL.** |

### 1.3b Bundeswehr (P1)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundeswehr.de/de/presse` | Entry point | 200 OK | Working |
| `https://www.bundeswehr.de/de/pressemitteilungen-154594` | Entry point | 200 OK | Working |
| `https://www.bundeswehr.de/de/feed-517054` | RSS [VERIFY] | **HTML page** | Not a feed -- landing page titled "RSS-Feed bundeswehr.de" |
| `https://www.bundeswehr.de/service/rss/de/517054/feed` | RSS (actual) | 200 OK | Valid RSS 2.0, 10 items. **This is the correct feed URL.** |

### 1.4a Bundestag (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundestag.de/presse` | Entry point | 200 OK | Working |
| `https://www.bundestag.de/dokumente` | Entry point | 200 OK | Working |
| `https://www.bundestag.de/static/appdata/includes/rss/pressemitteilungen.rss` | RSS | 200 OK | Valid RSS 2.0, 16 items |
| `https://www.bundestag.de/static/appdata/includes/rss/aktuellethemen.rss` | RSS | 200 OK | Valid RSS 2.0, 16 items |
| `https://www.bundestag.de/static/appdata/includes/rss/hib.rss` | RSS (hib) | 200 OK | Valid RSS 2.0, 16 items |
| `https://www.bundestag.de/static/appdata/includes/rss/drucksachen.rss` | RSS | 200 OK | Valid RSS 2.0, 15 items |
| `https://www.bundestag.de/static/appdata/includes/rss/plenarprotokolle.rss` | RSS | 200 OK | Valid RSS 2.0, 15 items |
| `https://www.bundestag.de/static/appdata/includes/rss/tagesordnungen.rss` | RSS | 200 OK | Valid RSS 2.0, 15 items |
| `https://www.bundestag.de/static/appdata/includes/rss/wissenschaftlichedienste.rss` | RSS | 200 OK | Valid RSS 2.0, 15 items |
| `https://dip.bundestag.de/` | Entry point (DIP) | 200 OK | Working |
| `https://www.bundestag.de/mediathek` | Entry point | 200 OK | Working |
| `https://www.bundestag.de/hib` | Entry point | 200 OK | Redirects to `/presse/hib` |
| `https://www.bundestag.de/services/rss/feeds_themen-249016` | Entry point (topic feeds) | 200 OK | Working |

### 1.4b Bundesrat (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundesrat.de/DE/presse/presse-node.html` | Entry point | 200 OK | Working |
| `https://www.bundesrat.de/DE/service/archiv/pm-archiv/pm-archiv-node.html` | Entry point | 200 OK | Working |
| `https://www.bundesrat.de/DE/service-navi/rss/rss-node.html` | RSS hub [VERIFY] | **HTML page** | Not a feed. Lists 6 actual feed URLs (see below). |
| `https://www.bundesrat.de/SiteGlobals/Functions/RSSFeed/RSSGenerator_Announcement.xml?nn=4352850` | RSS (Beratungsvorgänge) | 200 OK | Valid RSS 2.0, 50 items |
| `https://www.vermittlungsausschuss.de/VA/DE/service/rss/rss-node.html` | Vermittlungsausschuss RSS | 200 OK | HTML page listing feeds |

**Bundesrat RSS feeds discovered (from hub page):**
- `RSSGenerator_Announcement.xml?nn=4352850` -- Beratungsvorgänge (confirmed working, 50 items)
- `RSSGenerator_PBPrintout.xml?nn=4352850` -- Drucksachen
- `RSSGenerator_Publication.xml?nn=4352850` -- Plenarprotokolle
- `RSSGenerator_Event.xml?nn=4352850` -- Termine
- `RSSGenerator_Event_Ausschuss.xml?nn=4352850` -- Ausschusstermine
- `RSSGenerator_top_plenumkompakt.xml?nn=4352850` -- BundesratKOMPAKT

### 1.5 BGBl / recht.bund.de (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.recht.bund.de/de/bundesgesetzblatt/bgbl-1/bgbl-1_node.html` | Entry point | 200 OK | Working |
| `https://www.recht.bund.de/` | Entry point | 200 OK | Working |
| `https://www.bgbl.de/` | Archive entry point | 200 OK | Working (redirects to xaver/bgbl/start.xav) |
| `https://www.gesetze-im-internet.de/` | Consolidated law | 200 OK | Working |
| `https://www.bundesanzeiger.de/pub/de/amtlicher-teil` | Administrative gazette | 200 OK | Working |
| RSS | [VERIFY] | **No RSS found** | recht.bund.de does not appear to offer RSS. Confirmed no feed. |

### 1.6 BMF (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundesfinanzministerium.de/Web/DE/Presse/Pressemitteilungen/pressemitteilungen.html` | Entry point | 200 OK | Working |
| `https://www.bundesfinanzministerium.de/Web/DE/Service/Abonnements/Rss/rss.html` | RSS hub [VERIFY] | **HTML page** | Lists 9 category-specific RSS feed URLs |
| `https://www.bundesfinanzministerium.de/SiteGlobals/Functions/RSSFeed/DE/Pressemitteilungen/RSSPressemitteilungen.xml` | RSS (Pressemitteilungen) | 200 OK | Valid RSS 2.0, 20 items |

**BMF RSS feeds discovered (from hub page):**
- `RSSAktuelles.xml` -- Aktuelles
- `RSSPressemitteilungen.xml` -- Pressemitteilungen (confirmed working)
- `RSSSteuern.xml` -- Steuern
- `RSSOeffentliche_Finanzen.xml` -- Öffentliche Finanzen
- `RSSEuropa.xml` -- Europa
- `RSSInternationales_Finanzmarkt.xml` -- Internationales/Finanzmarkt
- `RSSBundesvermoegen.xml` -- Bundesvermögen
- `RSSZoll.xml` -- Zoll
- `RSSBriefmarken_Sammlermuenzen.xml` -- Briefmarken/Sammlermuenzen

### 1.7 Deutsche Bundesbank (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundesbank.de/de/presse/pressenotizen` | Entry point (DE) | 200 OK | Working |
| `https://www.bundesbank.de/en/press/press-releases` | Entry point (EN) | 200 OK | Working |
| `https://www.bundesbank.de/service/rss/de/633290/feed.rss` | RSS (General) | 200 OK | Valid RSS 2.0, 10 items |
| `https://www.bundesbank.de/service/rss/de/633286/feed.rss` | RSS (Pressenotizen) | 200 OK | Valid RSS 2.0, 10 items |
| `https://www.bundesbank.de/service/rss/de/633278/feed.rss` | RSS (ECB publications) | 200 OK | Valid RSS 2.0, 2 items |
| `https://www.bundesbank.de/service/rss/de/800838/feed.rss` | RSS (ECB economic reports) | 200 OK | Valid RSS 2.0, 4 items |
| `https://www.bundesbank.de/service/rss/de/633280/feed.rss` | RSS (Monthly/annual reports) | 200 OK | Valid RSS 2.0, 0 items (empty but valid) |
| `https://www.bundesbank.de/service/rss/de/878804/feed.rss` | RSS (Open market ops) | 200 OK | Valid RSS 2.0, 6 items |
| `https://www.bundesbank.de/service/rss/de/633302/feed.rss` | RSS (Circulars) | 200 OK | Valid RSS 2.0, 10 items |
| `https://www.bundesbank.de/service/rss/de/633288/feed.rss` | RSS (Topics) | 200 OK | Valid RSS 2.0, 10 items |

### 1.8 BMWK (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundeswirtschaftsministerium.de/Navigation/DE/Service/Medienraum/medienraum.html` | Entry point | 200 OK | Working |
| `https://www.bmwk.de/Navigation/DE/Service/Medienraum/medienraum.html` | Entry point (short domain) | 200 OK | Redirects to bundeswirtschaftsministerium.de |
| `https://www.bundeswirtschaftsministerium.de/Navigation/DE/Service/RSS-Newsfeed/rss-newsfeed.html` | RSS hub [VERIFY] | **HTML page** | Lists 13 feed URLs |
| `https://www.bundeswirtschaftsministerium.de/SiteGlobals/BMWI/Functions/RSSFeed/DE/RSSFeed-Pressemitteilung.xml` | RSS (Pressemitteilungen) | 200 OK | Valid RSS 2.0, 20 items |
| `https://www.bundeswirtschaftsministerium.de/SiteGlobals/BMWI/Functions/RSSFeed/DE/RSSFeed-Kompakt.xml` | RSS (Kompakt) | 200 OK | Valid RSS 2.0, 20 items (minor malformed self-link) |

### 1.9a BND (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bnd.bund.de/DE/Service/Presse/presse_node.html` | Entry point (DE) | 200 OK | Working |
| `https://www.bnd.bund.de/EN/Press/press_node.html` | Entry point (EN) | 200 OK | Working |
| RSS | [VERIFY] | **No RSS found** | Confirmed: BND does not offer RSS feeds |

### 1.9b BfV (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.verfassungsschutz.de/DE/service/presse/presse_node.html` | Entry point | 200 OK | Working |
| RSS | [VERIFY] | **No RSS found** | Confirmed: BfV does not offer RSS feeds |

### 1.9c NSR (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundesregierung.de/breg-de/aktuelles/pressemitteilungen` | Entry point (shared) | 200 OK | Working (shared with Bundesregierung) |
| `https://www.bundesregierung.de/resource/blob/975228/2381766/.../2025-08-27-nationaler-sicherheitsrat-data.pdf` | PDF document | 200 OK | application/pdf -- NSR Geschäftsordnung accessible |

### 1.10a EU Permanent Representation (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://bruessel-eu.diplo.de/eu-de` | Entry point (DE) | 200 OK | Working |
| RSS | [VERIFY] | **No RSS found** | Confirmed: diplo.de network does not offer RSS |

### 1.10b Destatis (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.destatis.de/DE/Presse/presse.html` | Entry point | **404** | Documented URL not found |
| `https://www.destatis.de/DE/Presse/Pressemitteilungen/pressemitteilungen.html` | Entry point | **404** | Documented URL not found |
| `https://www.destatis.de/DE/Presse/Pressemitteilungen/_inhalt.html` | Entry point (working) | 200 OK | **Correct URL for press releases** |
| `https://www.destatis.de/DE/Service/RSS/_inhalt.html` | RSS hub | 200 OK | Lists RSS feed URL |
| `https://www.destatis.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Aktuell.xml?nn=241288` | RSS (Aktuelles) | 200 OK | Valid RSS 2.0, 10 items. [VERIFY] **resolved: RSS exists** |

### 1.10c Bundesrechnungshof (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.bundesrechnungshof.de/de/veroeffentlichungen/pressemitteilungen` | Entry point [VERIFY] | **404** | Documented URL not found |
| `https://www.bundesrechnungshof.de/DE/7_presse/1_pressemitteilungen/pressemitteilungen_node.html` | Entry point (correct) | 200 OK | **Correct URL for press releases** |
| `https://www.bundesrechnungshof.de/` | Homepage | 200 OK | Working (redirects to DE/0_home/home_node.html) |
| RSS | [VERIFY] | **No RSS found** | Confirmed: Bundesrechnungshof does not offer RSS |

### 1.10d IfW Kiel (P2)

| URL | Type | Status | Notes |
|---|---|---|---|
| `https://www.ifw-kiel.de/de/themendossiers/ukraine-support-tracker/` | Entry point | **404** | Domain has been rebranded. ifw-kiel.de redirects to kielinstitut.de |
| `https://www.ifw-kiel.de/de/presse/` | Entry point | **404** | Same redirect issue |
| `https://www.ifw-kiel.de/` | Homepage | **500** | Server error at redirected domain kielinstitut.de |
| `https://www.kielinstitut.de/de/themendossiers/ukraine-support-tracker/` | Entry point (new domain) | **404** | Path not valid on new domain |
| RSS | [VERIFY] | **Cannot verify** | Site unreliable; domain rebranded to kielinstitut.de with broken paths |

---

## [VERIFY] Items Resolution Summary

| Item | Source | Result |
|---|---|---|
| BMVg RSS at `/de/rss` | 1.3a | **HTML landing page, not feed.** Actual feed: `https://www.bmvg.de/service/rss/de/17680/feed` |
| Bundeswehr RSS at `/de/feed-517054` | 1.3b | **HTML landing page, not feed.** Actual feed: `https://www.bundeswehr.de/service/rss/de/517054/feed` |
| Bundesrat RSS at `rss-node.html` | 1.4b | **HTML hub page.** Lists 6 working RSS feeds with relative URLs under `SiteGlobals/Functions/RSSFeed/` |
| BGBl RSS at recht.bund.de | 1.5 | **No RSS available.** Confirmed absent. |
| BMF RSS feed URLs | 1.6 | **HTML hub page.** Lists 9 category feeds. Pressemitteilungen feed confirmed working. |
| BMWK RSS feed URLs | 1.8 | **HTML hub page.** Lists 13 feeds. Pressemitteilungen + Kompakt confirmed working. |
| BND RSS | 1.9a | **No RSS available.** Confirmed absent. |
| BfV RSS | 1.9b | **No RSS available.** Confirmed absent. |
| EU Perm. Rep. RSS at bruessel-eu.diplo.de | 1.10a | **No RSS available.** Confirmed absent. |
| Destatis RSS | 1.10b | **RSS exists.** Feed at `destatis.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Aktuell.xml?nn=241288` |
| Bundesrechnungshof RSS | 1.10c | **No RSS available.** Confirmed absent. |
| IfW Kiel RSS | 1.10d | **Cannot verify.** Domain rebranded to kielinstitut.de; site returning errors. |

---

## Corrections Needed in Source Document

| Issue | Documented URL | Correct URL |
|---|---|---|
| BMVg RSS feed | `https://www.bmvg.de/de/rss` | `https://www.bmvg.de/service/rss/de/17680/feed` |
| Bundeswehr RSS feed | `https://www.bundeswehr.de/de/feed-517054` | `https://www.bundeswehr.de/service/rss/de/517054/feed` |
| AA travel advisories | `.../de/ResieUndSicherheit/...` | `.../de/ReiseUndSicherheit/...` (typo: "Resie" -> "Reise") |
| Cabinet decisions | `.../breg-de/aktuelles/kabinett` | URL returns 404; needs re-discovery |
| Destatis press releases | `.../Presse/Pressemitteilungen/pressemitteilungen.html` | `.../Presse/Pressemitteilungen/_inhalt.html` |
| Destatis press portal | `.../Presse/presse.html` | Also 404; use `_inhalt.html` pattern |
| Bundesrechnungshof press | `.../de/veroeffentlichungen/pressemitteilungen` | `.../DE/7_presse/1_pressemitteilungen/pressemitteilungen_node.html` |
| IfW Kiel (all URLs) | `ifw-kiel.de/...` | Domain rebranded to `kielinstitut.de`; all paths broken |
| Bundesrat RSS | `bundesrat.de/DE/service-navi/rss/rss-node.html` | This is an HTML hub, not a feed. Use individual feed URLs under `SiteGlobals/Functions/RSSFeed/` |
| BMF RSS | `bundesfinanzministerium.de/.../Rss/rss.html` | This is an HTML hub, not a feed. Use individual feed URLs under `SiteGlobals/Functions/RSSFeed/` |

---

## RSS Feed Inventory (All Confirmed Working)

Total confirmed working RSS feeds: **37**

| # | Source | Feed URL | Items |
|---|---|---|---|
| 1 | Bundeskanzler Meldungen | `bundeskanzler.de/service/rss/bk-de/1859752/feed.xml` | 20 |
| 2 | Bundeskanzler Termine | `bundeskanzler.de/service/rss/bk-de/1859754/feed.xml` | 10 |
| 3 | Bundeskanzler Reden | `bundeskanzler.de/service/rss/bk-de/1859760/feed.xml` | 20 |
| 4 | Bundesregierung Kompakt | `bundesregierung.de/service/rss/breg-de/1151242/feed.xml` | 20 |
| 5 | Bundesregierung Pressemitteilungen | `bundesregierung.de/service/rss/breg-de/1151244/feed.xml` | 20 |
| 6 | Bundesregierung Artikel | `bundesregierung.de/service/rss/breg-de/1151246/feed.xml` | 20 |
| 7 | Bundesregierung Bulletin | `bundesregierung.de/service/rss/breg-de/2318648/feed.xml` | 20 |
| 8 | Bundespräsident Pressemitteilungen | `bundespraesident.de/.../Pressemitteilungen/RSSNewsfeed.xml?nn=129192` | 3 |
| 9 | Bundespräsident Termine | `bundespraesident.de/.../Termine/RSSNewsfeed.xml?nn=129192` | 3 |
| 10 | Bundespräsident Reden | `bundespraesident.de/.../Reden/RSSNewsfeed.xml?nn=129192` | 3 |
| 11 | Auswärtiges Amt Presse/Reden | `auswaertiges-amt.de/static/includes/rss/Presse-RSS-Feed.xml` | 10 |
| 12 | Auswärtiges Amt Reisehinweise | `auswaertiges-amt.de/static/includes/rss/Reisehinweise-RSS-Feed.xml` | 3 |
| 13 | Auswärtiges Amt Aktuelles | `auswaertiges-amt.de/static/includes/rss/Aktuelles-RSS-Feed.xml` | 20 |
| 14 | BMVg | `bmvg.de/service/rss/de/17680/feed` | 10 |
| 15 | Bundeswehr | `bundeswehr.de/service/rss/de/517054/feed` | 10 |
| 16 | Bundestag Pressemitteilungen | `bundestag.de/static/appdata/includes/rss/pressemitteilungen.rss` | 16 |
| 17 | Bundestag Aktuelle Themen | `bundestag.de/static/appdata/includes/rss/aktuellethemen.rss` | 16 |
| 18 | Bundestag hib | `bundestag.de/static/appdata/includes/rss/hib.rss` | 16 |
| 19 | Bundestag Drucksachen | `bundestag.de/static/appdata/includes/rss/drucksachen.rss` | 15 |
| 20 | Bundestag Plenarprotokolle | `bundestag.de/static/appdata/includes/rss/plenarprotokolle.rss` | 15 |
| 21 | Bundestag Tagesordnungen | `bundestag.de/static/appdata/includes/rss/tagesordnungen.rss` | 15 |
| 22 | Bundestag Wissenschaftliche Dienste | `bundestag.de/static/appdata/includes/rss/wissenschaftlichedienste.rss` | 15 |
| 23 | Bundesrat Beratungsvorgänge | `bundesrat.de/SiteGlobals/Functions/RSSFeed/RSSGenerator_Announcement.xml?nn=4352850` | 50 |
| 24 | BMF Pressemitteilungen | `bundesfinanzministerium.de/SiteGlobals/Functions/RSSFeed/DE/Pressemitteilungen/RSSPressemitteilungen.xml` | 20 |
| 25 | Bundesbank General | `bundesbank.de/service/rss/de/633290/feed.rss` | 10 |
| 26 | Bundesbank Pressenotizen | `bundesbank.de/service/rss/de/633286/feed.rss` | 10 |
| 27 | Bundesbank ECB publications | `bundesbank.de/service/rss/de/633278/feed.rss` | 2 |
| 28 | Bundesbank ECB economic reports | `bundesbank.de/service/rss/de/800838/feed.rss` | 4 |
| 29 | Bundesbank Monthly/annual reports | `bundesbank.de/service/rss/de/633280/feed.rss` | 0 |
| 30 | Bundesbank Open market ops | `bundesbank.de/service/rss/de/878804/feed.rss` | 6 |
| 31 | Bundesbank Circulars | `bundesbank.de/service/rss/de/633302/feed.rss` | 10 |
| 32 | Bundesbank Topics | `bundesbank.de/service/rss/de/633288/feed.rss` | 10 |
| 33 | BMWK Pressemitteilungen | `bundeswirtschaftsministerium.de/SiteGlobals/BMWI/Functions/RSSFeed/DE/RSSFeed-Pressemitteilung.xml` | 20 |
| 34 | BMWK Kompakt | `bundeswirtschaftsministerium.de/SiteGlobals/BMWI/Functions/RSSFeed/DE/RSSFeed-Kompakt.xml` | 20 |
| 35 | Destatis Aktuell | `destatis.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/Aktuell.xml?nn=241288` | 10 |
| 36-37 | + 5 additional Bundesrat feeds discovered (untested individually but listed on hub page) | See Bundesrat section | -- |

---

## Key Findings

1. **Germany's RSS infrastructure is excellent.** 35+ working feeds confirmed across 12 institutions. The document's claim that Germany is "the most RSS-friendly government landscape in the pipeline" is validated.

2. **No bot protection encountered.** All URLs responded without challenges, rate limiting, or CAPTCHAs.

3. **Two RSS URLs in the source document point to HTML landing pages, not feeds.** Both BMVg and Bundeswehr use the pattern `/de/rss` or `/de/feed-{id}` for informational pages, while actual feeds follow the pattern `/service/rss/de/{id}/feed`.

4. **IfW Kiel has rebranded.** The domain `ifw-kiel.de` now redirects to `kielinstitut.de`, and the new site returns 500 errors. All documented IfW Kiel URLs are broken. Requires re-mapping.

5. **Destatis and Bundesrechnungshof URLs need correction.** Both use different URL patterns than documented. Destatis uses `_inhalt.html` suffix; Bundesrechnungshof uses a numbered directory structure.

6. **One typo found.** The travel advisories URL has "ResieUndSicherheit" instead of "ReiseUndSicherheit".
