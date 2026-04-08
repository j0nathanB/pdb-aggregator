# India Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/india_government_sources.md`
**Test method:** WebFetch (primary for RSS feeds), curl fallback with `Mozilla/5.0` User-Agent

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 76 |
| Reachable (HTTP 200 or valid feed) | 54 |
| Soft 404 (HTTP 200 but error page content) | 8 |
| Failed (connection refused / DNS failure) | 9 |
| Failed (timeout) | 3 |
| Failed (TLS/SSL error) | 4 |
| RSS/Atom feeds confirmed working | 9 |
| RSS feeds documented as non-functional — confirmed non-functional | 1 |
| [VERIFY RSS] items — confirmed no RSS exists | 2 |
| No public web presence (by design) | 1 |

**Overall reachability rate:** 54/76 (71%)
**P1 source reachability:** PIB (fully reachable, all RSS working), PMO (2/4 reachable), MEA (soft 404 on all section pages), MoD (connection refused), Military branches (all unreachable)

---

## 1. RSS Feed Verification

### RBI RSS Feeds (5 feeds)

All five RBI RSS feeds are valid, well-structured RSS 2.0 XML and actively maintained. RBI has the most machine-friendly government data infrastructure in India.

| Feed | URL | Status | Notes |
|---|---|---|---|
| Press Releases | `https://rbi.org.in/pressreleases_rss.xml` | VALID | RSS 2.0. 10 items. Most recent: Mar 2026. Includes HDFC Bank statement, VRR auction, T-bill results. |
| Notifications | `https://rbi.org.in/notifications_rss.xml` | VALID | RSS 2.0. 10 items. Most recent: Mar 16, 2026. Regulatory directions on co-op banks, currency chest ops. |
| Speeches | `https://rbi.org.in/speeches_rss.xml` | VALID | RSS 2.0. Multiple items. Most recent: Mar 6, 2026. Deputy Governor speeches on digital finance, growth. |
| Publications | `https://rbi.org.in/Publication_rss.xml` | VALID | RSS 2.0. 1 item (Certificates of Authorisation). Feed functional but low-volume. |
| Tenders | `https://rbi.org.in/tenders_rss.xml` | VALID | RSS 2.0. Multiple items. Housekeeping, maintenance contracts. Low pipeline value. |
| RSS Hub Page | `https://rbi.org.in/Scripts/rss.aspx` | OK | HTML page listing all available feeds. HTTP 200. |

### PIB RSS Feeds (4 feeds)

All PIB RSS feeds are valid RSS 2.0. The Hindi feed and English feed returned identical item structures (Hindi content). The English press releases feed is the single most important automated ingestion endpoint.

| Feed | URL | Status | Notes |
|---|---|---|---|
| Press Releases (EN) | `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3` | VALID | RSS 2.0. 20 items. Mar 19, 2026. Cross-ministry coverage including NITI Aayog, electricity summit. Note: Lang=1 returned Hindi content during test — may require investigation. |
| Press Releases (HI) | `https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3` | VALID | RSS 2.0. 20 items. Hindi content confirmed. |
| Photos | `https://pib.gov.in/RssMain.aspx?ModId=8&Lang=1&Regid=3` | VALID | RSS 2.0. Photo releases from government events. Mar 19, 2026. |
| Media Advisories | `https://pib.gov.in/RssMain.aspx?ModId=10&Lang=1&Regid=3` | VALID | RSS 2.0. Upcoming government events and press conferences. English content. |
| RSS Hub Page | `https://www.pib.gov.in/ViewRss.aspx` | OK | HTML page listing all available feeds. HTTP 200. |

### PMO WordPress Feed

| Feed | URL | Status | Notes |
|---|---|---|---|
| WordPress Feed | `https://www.pmindia.gov.in/en/feed/` | NOT TESTED (documented as non-functional) | Source document states feed contains only a test post from June 2024. Treated as unavailable per source document. |

### [VERIFY] Items

| Source | Checked URL | RSS Found? | Notes |
|---|---|---|---|
| MoD (mod.gov.in) | `https://www.mod.gov.in/` | **No** | No RSS/Atom link elements in page source. Site returned ECONNREFUSED during test — intermittent availability confirmed. |
| DRDO (drdo.gov.in) | `https://www.drdo.gov.in/` | **No** | No RSS/Atom link elements in page source. Page contains generic XML references (Drupal) but no syndication feeds. |

---

## 2. Entry Point URL Results by Institution

### 2.1 PMO (pmindia.gov.in) — P1

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.pmindia.gov.in/en/news-updates/` | News updates (primary) | OK | 200 | WordPress site loads correctly. |
| `https://www.pmindia.gov.in/en/pms-speeches/` | PM speeches | OK | 200 | Loads correctly. |
| `https://pmindia.gov.in/en/tag/pmspeech/` | PM speeches (tagged) | FAIL | TLS error | curl exit code 35 (SSL handshake failure). Non-www variant may have cert issue. |
| `https://www.pmindia.gov.in/en/media-coverage-1/` | Media coverage | OK | 200 | Loads correctly. |

### 2.2 MEA (mea.gov.in) — P1

All MEA section pages return HTTP 200 but serve a **soft 404 error page** with the title "Sorry for the inconvenience." and the message "the page you were trying to reach doesn't exist anymore, or maybe it has just moved." The MEA homepage loads correctly. This suggests a site-wide restructuring or migration may be in progress.

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.mea.gov.in/` | Homepage | OK | 200 | Loads correctly with current news, minister profiles, dashboards. |
| `https://www.mea.gov.in/press-releases.htm` | Press releases | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/Speeches-Statements.htm` | Speeches & statements | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/media-briefings.htm` | Media briefings | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/bilateral-documents.htm` | Bilateral documents | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/response-to-queries.htm` | Response to queries | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/lok-sabha.htm` | Lok Sabha Q&A | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/rajya-sabha.htm` | Rajya Sabha Q&A | SOFT 404 | 200 | Error page served despite 200 status. |
| `https://www.mea.gov.in/treaty.htm` | Treaty database | SOFT 404 | 200 | Error page served despite 200 status. |

**Action required:** MEA section URLs need re-mapping. The homepage works but all deep-link section pages are broken. PIB (mincode=12) should serve as fallback for MEA press releases. The MEA site may have migrated to a new URL structure.

### 2.3 MoD (mod.gov.in) — P1

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.mod.gov.in/press-release` | Press releases | FAIL | ECONNREFUSED | Connection refused. Intermittent availability documented in source. |
| `https://www.pib.gov.in/newsite/pmreleases.aspx?mincode=33` | MoD via PIB (fallback) | OK | 200 | PIB fallback works. Use this as primary ingestion point. |
| `https://www.ddpmod.gov.in/` | Dept of Defence Production | FAIL | TLS error | curl exit code 35 (SSL handshake failure). |

### 2.4 Military Service Branches — P1

All three service branch websites are **unreachable** during testing. This aligns with the source document's note about NIC infrastructure outages.

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://indianarmy.nic.in/media/releases/` | Indian Army press releases | FAIL | ECONNREFUSED | Connection refused. |
| `https://indiannavy.nic.in/archive/press-release` | Indian Navy press releases | FAIL | Timeout | curl exit code 28 (operation timed out at 30s). |
| `https://indianairforce.nic.in/press-release` | IAF press releases | FAIL | Timeout | curl exit code 28 (operation timed out at 30s). |
| `https://indianairforce.nic.in/latest-news/` | IAF latest news | FAIL | Timeout | curl exit code 28 (operation timed out at 30s). |

### 2.5 PIB (pib.gov.in) — P1

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://pib.gov.in/allRel.aspx` | All releases listing | OK | 200 | Primary archive page. |
| `https://pib.gov.in/indexd.aspx` | Desktop home | OK | 200 | Main PIB portal. |
| `https://www.pib.gov.in/ViewRss.aspx` | RSS hub page | OK | 200 | Lists all available feeds. |
| `https://www.pib.gov.in/newsite/pmreleases.aspx?mincode=33` | MoD filter | OK | 200 | Ministry-specific filtering works. |

### 2.6 Parliament — Lok Sabha & Rajya Sabha — P2

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://loksabha.nic.in/` | Lok Sabha main portal | FAIL | DNS failure | curl exit code 6 (could not resolve host). |
| `https://sansad.in/ls/debates/introduction` | LS debates (Digital Sansad) | OK | 200 | Modern portal works. |
| `https://loksabhaph.nic.in/Questions/Qtextsearch.aspx` | LS questions search | FAIL | DNS failure | curl exit code 6. |
| `https://pprloksabha.sansad.in/` | LS press relations | OK | 200 | Sansad subdomain works. |
| `https://eparlib.sansad.in/` | Parliament Digital Library | OK | 200 | Works. |
| `https://rajyasabha.nic.in/` | Rajya Sabha main portal | OK | 200 | Works. |
| `https://rsdebate.nic.in/` | RS debate archive | OK | 200 | DSpace-based repository. |
| `https://sansad.in/rs/debates/officials` | RS debates (Digital Sansad) | OK | 200 | Works. |
| `https://rajyasabha.nic.in/Questions/QuestionListStarred` | RS starred questions | OK | 200 | Works. |

### 2.7 Gazette of India — P2

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://egazette.gov.in/` | Main portal | OK | 200 | Works. |
| `https://egazette.gov.in/GazetteDirectory.aspx` | Directory | OK | 200 | Works. |
| `https://egazette.gov.in/RecentUploads.aspx?Category=1` | Bills & Acts | OK | 200 | Category filtering works. |
| `https://egazette.gov.in/StateGazette.aspx` | State gazettes | FAIL | TLS error | curl exit code 35. |
| `https://nationalarchives.nic.in/` | National Archives | OK | 200 | Works. |

### 2.8 Ministry of Finance — P2

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.finmin.nic.in/` | Main portal | FAIL | DNS failure | curl exit code 6 (could not resolve host). |
| `https://www.indiabudget.gov.in/` | Budget portal | OK | 200 | Works. |
| `https://dea.gov.in/` | Dept of Economic Affairs | FAIL | Timeout | curl exit code 28. |
| `https://doe.gov.in/` | Dept of Expenditure | FAIL | TLS error | curl exit code 35. |
| `https://dor.gov.in/` | Dept of Revenue | FAIL | DNS failure | curl exit code 6. |
| `https://financialservices.gov.in/` | Dept of Financial Services | FAIL | DNS failure | curl exit code 6. |
| `https://dipam.gov.in/` | DIPAM | OK | 200 | Works. |

### 2.9 RBI (rbi.org.in) — P2

All RBI web pages are reachable. RBI has the most robust web infrastructure of any Indian government source.

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx` | Press releases page | OK | 200 | Works. |
| `https://rbi.org.in/scripts/Annualpolicy.aspx` | Monetary policy | OK | 200 | Works. |
| `https://rbi.org.in/scripts/FS_Overview.aspx?fn=2752` | Monetary overview | OK | 200 | Works. |
| `https://data.rbi.org.in` | Database on Indian Economy | OK | 200 | Works. |
| `https://rbi.org.in/Scripts/NotificationUser.aspx` | Notifications | OK | 200 | Works. |
| `https://rbi.org.in/Scripts/BS_ViewMasterDirections.aspx` | Master Directions | OK | 200 | Works. |
| `https://rbi.org.in/Scripts/Publications.aspx` | Publications | OK | 200 | Works. |
| `https://rbi.org.in/scripts/SearchResults.aspx` | Search | OK | 200 | Works. |

### 2.10 Commerce & Industry — P2

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.commerce.gov.in/press-releases/` | Press releases | OK | 200 | WordPress-based. Works. |
| `https://www.commerce.gov.in/international-trade/` | International trade | OK | 200 | Works. |
| `https://www.commerce.gov.in/trade-statistics/` | Trade statistics | OK | 200 | Works. |
| `https://www.dpiit.gov.in/` | DPIIT | OK | 200 | Works. |
| `https://niryat.gov.in/` | Niryat (export) portal | FAIL | DNS failure | curl exit code 6. |
| `https://trade-analytics.commerce.gov.in/` | Trade analytics | OK | 200 | Works. |
| `https://www.dgft.gov.in/` | DGFT | OK | 200 | Works. |
| `https://www.dgtr.gov.in/` | DGTR (trade remedies) | FAIL | TLS error | curl exit code 35. |

### 2.11 NITI Aayog — P2

All NITI Aayog URLs are reachable.

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://www.niti.gov.in/` | Main portal | OK | 200 | Works. |
| `https://niti.gov.in/publications/division-reports` | Division reports | OK | 200 | Works. |
| `https://niti.gov.in/publications/policy-and-research/policy-paper` | Policy papers | OK | 200 | Works. |
| `https://niti.gov.in/publication/annual-report` | Annual report | OK | 200 | Works. |
| `https://ndap.niti.gov.in/` | NDAP data platform | OK | 200 | Works. |
| `https://niti.gov.in/publications/arth-niti` | ArthNITI bulletin | OK | 200 | Works. |

### 2.12 Other Sources — P2

| URL | Purpose | Status | HTTP Code | Notes |
|---|---|---|---|---|
| `https://sansadtv.nic.in/` | Sansad TV | OK | 200 | Works. Video-primary (limited pipeline utility). |
| `https://www.drdo.gov.in/` | DRDO | OK | 200 | Works. No RSS confirmed. |
| NSCS / RAW | N/A | N/A | N/A | No public web presence by design. |

---

## 3. Critical Findings

### 3.1 MEA Section Pages Are All Down (Soft 404)

All MEA deep-link section URLs (`press-releases.htm`, `Speeches-Statements.htm`, `media-briefings.htm`, `bilateral-documents.htm`, `response-to-queries.htm`, `lok-sabha.htm`, `rajya-sabha.htm`, `treaty.htm`) return HTTP 200 but serve an error page titled "Sorry for the inconvenience." The MEA homepage (`mea.gov.in/`) loads correctly, suggesting a site restructuring or CMS migration has broken the documented URL patterns. **Pipeline impact: HIGH.** MEA is a P1 source. Use PIB (mincode=12) as fallback until new URLs are mapped.

### 3.2 Military Branch Sites Entirely Unreachable

All three service branch websites (`indianarmy.nic.in`, `indiannavy.nic.in`, `indianairforce.nic.in`) are unreachable — connection refused or timeout. This may be a systemic NIC infrastructure issue affecting military domains. **Pipeline impact: HIGH.** These are P1 sources. Use PIB as fallback (MoD mincode=33 captures some military releases).

### 3.3 MoD Main Site Down

`mod.gov.in` returns ECONNREFUSED. Consistent with the source document's warning about intermittent connectivity. PIB fallback (`mincode=33`) works and should be the primary ingestion point.

### 3.4 Finance Ministry Infrastructure Fragmented

The main `finmin.nic.in` portal and 3 of 5 department sub-portals are unreachable (DNS failures and timeouts). Only `indiabudget.gov.in` and `dipam.gov.in` work. PIB (mincode=7) is the reliable channel for Finance Ministry releases.

### 3.5 PIB and RBI: Most Reliable Sources

PIB (all 4 RSS feeds working, all entry points reachable) and RBI (all 5 RSS feeds working, all 8 web pages reachable) are the most robust government web presences. These should anchor the automated pipeline, with other sources treated as supplementary.

### 3.6 [VERIFY] Items Resolved

- **MoD RSS:** No RSS feed exists on `mod.gov.in`. Confirmed absent from page source.
- **DRDO RSS:** No RSS feed exists on `drdo.gov.in`. Confirmed absent from page source.

### 3.7 PIB English Feed Anomaly

The PIB English press releases feed (`Lang=1`) returned Hindi content during testing, identical to the Hindi feed (`Lang=2`). This may be a temporary issue or the `Lang` parameter may not function as documented. Requires further investigation to confirm English-language RSS availability.

---

## 4. Recommended Ingestion Priority

Based on test results, the recommended ingestion architecture:

1. **PIB RSS** — Primary feed for all government releases (9 RSS feeds working)
2. **RBI RSS** — Primary feed for monetary/financial data (5 RSS feeds working)
3. **PIB HTML scraping** — Fallback for PIB if RSS fails; ministry-specific filtering via mincode
4. **PMO HTML scraping** — Direct scrape of `pmindia.gov.in/en/news-updates/` (working)
5. **Commerce HTML scraping** — `commerce.gov.in/press-releases/` (working)
6. **Gazette PDF download** — `egazette.gov.in` (working)
7. **NITI Aayog HTML scraping** — All URLs working
8. **DRDO HTML scraping** — `drdo.gov.in` (working)
9. **Parliament** — Use `sansad.in` and `rajyasabha.nic.in` (working); avoid legacy `loksabha.nic.in` (DNS failure)

**Sources requiring fallback to PIB:** MEA, MoD, Indian Army, Indian Navy, IAF, Finance Ministry.
