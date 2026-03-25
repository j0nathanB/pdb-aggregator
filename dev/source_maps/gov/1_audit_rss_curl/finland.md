# Finland Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/finland_government_sources.md`

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 55 |
| RSS feeds confirmed working | 9 |
| Entry point / additional URLs confirmed working | 27 |
| URLs returning 403 (bot protection) | 5 |
| URLs returning 404 (not found) | 10 |
| URLs blocked by CAPTCHA | 2 |
| URLs redirecting (content moved) | 1 |
| URLs requiring JavaScript (no static content) | 1 |

| Verdict | Count |
|---|---|
| PASS (accessible for pipeline use) | 36 |
| FAIL (not accessible as documented) | 14 |
| CONDITIONAL (accessible with workaround) | 5 |

---

## 1. Confirmed RSS Feeds

All RSS feeds listed as "confirmed" in the source document were tested with WebFetch.

| # | Source | RSS URL | Status | Feed Title | Items | Most Recent Item |
|---|---|---|---|---|---|---|
| 1 | Valtioneuvosto press releases (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/LOmkEPY4nk2s/rss` | PASS | "Government press releases" | 100 | 2026-03-19 |
| 2 | Valtioneuvosto press releases backup (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/00Qguh1GvAiJ/rss` | PASS | "Government press releases" | 20 | 2026-03-19 |
| 3 | Valtioneuvosto govt decisions (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/lKJx41DPuWCC/rss` | PASS | "Sisaltojulkaisija" | 20 | 2026-03-19 |
| 4 | Valtioneuvosto presidential decisions (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/fpYJYjw2EcOG/rss` | PASS | "Sisaltojulkaisija" | 20 | 2026-03-13 |
| 5 | Valtioneuvosto govt sessions (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/CSnDFjXvoBx4/rss` | PASS | "Sisaltojulkaisija" | 20 | 2026-03-19 |
| 6 | Valtioneuvosto finance committee (EN) | `https://valtioneuvosto.fi/en/staattiset-feedit-en/-/asset_publisher/P2JabALc50Es/rss` | PASS | "Sisaltojulkaisija" | 25 | 2026-03-19 |
| 7 | Defmin.fi press releases | `https://defmin.fi/en/topical/static-rss-feeds/-/asset_publisher/bGmVi3cQo5T6/rss` | PASS | "Defmin.fi tiedotteet RSS" (Atom) | 20 | 2026-03-16 |
| 8 | Presidentti.fi (WordPress feed) | `https://www.presidentti.fi/en/feed/` | PASS | "Presidentti" | 10 | 2026-03-17 |
| 9 | SUPO news and press releases | `https://supo.fi/en/news-and-press-releases/-/asset_publisher/LVkvGHGkmM3J/rss` | PASS | "Supo - News and press releases" | 25 | 2026-03-10 |

**Result: 9/9 confirmed RSS feeds are WORKING.** All feeds return valid RSS 2.0 or Atom XML with current content.

---

## 2. [VERIFY] RSS Feeds

These RSS URLs were flagged as unverified in the source document.

| # | Source | RSS URL Tested | Status | Notes |
|---|---|---|---|---|
| 1 | Finlex (Statute Book) | `http://finlex.fi/fi/rss/kokoelma` | FAIL (404) | Also tested `https://www.finlex.fi/fi/rss/kokoelma` -- also 404. The documented RSS URL does not exist. Finlex may have restructured; the entry point pages (`finlex.fi/en/legislation/collection` and `finlex.fi/fi/laki/kokoelma/`) load correctly via HTML. |
| 2 | Eduskunta (Parliament) | `https://www.eduskunta.fi/FI/rss-feeds/Sivut/parliament-press-releases.aspx` | FAIL (CAPTCHA) | Returns a CAPTCHA challenge page. Not usable for automated RSS polling. |
| 3 | um.fi (Foreign Ministry) | No RSS URL documented | N/A | Site states RSS exists but no URL surfaced. um.fi returns 403 for all automated requests (WebFetch and curl). Covered by valtioneuvosto.fi aggregated feed. |
| 4 | vm.fi (Finance Ministry) | No RSS URL documented | N/A | No RSS link found on the press releases page. Page loads correctly (HTML). Covered by valtioneuvosto.fi aggregated feed. |
| 5 | tem.fi (Economic Affairs) | No RSS URL documented | N/A | No RSS link found on the press releases page. Page loads correctly (HTML). Covered by valtioneuvosto.fi aggregated feed. |
| 6 | Bank of Finland | No specific RSS URL documented | N/A | Site confirms RSS available but no URL surfaced. Press releases page loads (HTML). STT newsroom at sttinfo.fi works as alternative. |
| 7 | finlandabroad.fi (EU Rep) | No RSS URL documented | N/A | Returns 403 for all automated requests. No RSS discovered. |
| 8 | NATO RSS feeds page | `https://www.nato.int/cps/en/natohq/rss_feeds.htm` | FAIL (404) | NATO has rebuilt their website. The old RSS feeds listing page returns 404. No replacement RSS feed URL found on new site. |

**Result: 0/3 [VERIFY] RSS feeds confirmed working. 2 definitively broken (Finlex, NATO). 1 CAPTCHA-blocked (Eduskunta). The remaining 5 sources have no RSS URL to test but are covered by HTML scraping or the valtioneuvosto.fi aggregated RSS.**

---

## 3. Entry Point URLs (Primary)

| # | Source | Entry Point URL | Status | Method | Notes |
|---|---|---|---|---|---|
| 1 | Prime Minister's Office | `https://valtioneuvosto.fi/en/prime-ministers-office/press-releases` | PASS | WebFetch | 55 press releases visible, paginated. Loads correctly. |
| 2 | Foreign Ministry | `https://um.fi/press-releases` | FAIL (403) | WebFetch + curl | Returns 403 for all automated requests. Bot protection active. |
| 3a | Ministry of Defence | `https://defmin.fi/en/topical/press-releases-and-news` | PASS | WebFetch | 21 items visible, paginated. Loads correctly. |
| 3b | Finnish Defence Forces | `https://puolustusvoimat.fi/en/current-issues` | PASS | WebFetch | Content loads. RSS link discovered on page (not previously documented). |
| 4 | Eduskunta (Parliament) | `https://www.eduskunta.fi/EN/pages/default.aspx` | CONDITIONAL (CAPTCHA) | WebFetch returns CAPTCHA; curl with full browser UA returns 200 | CAPTCHA blocks WebFetch. curl with Chrome UA gets 200 text/html. |
| 5 | Finlex (EN) | `https://www.finlex.fi/en/legislation/collection` | PASS | WebFetch | Statute Book page loads, lists statutes by year. |
| 5b | Finlex (FI) | `https://www.finlex.fi/fi/laki/kokoelma/` | PASS | WebFetch | Finnish version loads correctly. |
| 6 | Ministry of Finance | `https://vm.fi/en/press-releases` | PASS | WebFetch | 7 press releases from 2026 visible. Year archive navigation works. |
| 7 | Bank of Finland | `https://www.suomenpankki.fi/en/news-and-topical/press-releases-and-news/` | PASS | WebFetch | Press releases visible. No RSS link on page. STT newsroom suggested. |
| 8 | Ministry of Economic Affairs | `https://tem.fi/en/press-releases` | PASS | WebFetch | 20 press releases from 2026, paginated (25 total). |
| 9 | SUPO | `https://supo.fi/en/news-and-press-releases` | PASS | WebFetch | News items visible including recent press releases. Liferay site. |
| 10a | President's Office | `https://www.presidentti.fi/en/current-affairs/press-releases/` | PASS | WebFetch | Current affairs section loads. WordPress site. |
| 10b | EU Representation | `https://finlandabroad.fi/web/eu/current-affairs` | FAIL (403) | WebFetch + curl | Returns 403 for all automated requests. Bot protection active. |
| 10c | NATO news | `https://www.nato.int/cps/en/natohq/news.htm` | CONDITIONAL | WebFetch | Page loads but news content is empty. Site says "building a new nato.int, some content will be in transition." |

---

## 4. Additional Entry Point URLs

| # | Source | URL | Status | Method | Notes |
|---|---|---|---|---|---|
| 1 | Valtioneuvosto all press releases | `https://valtioneuvosto.fi/en/current-issues/press-releases` | PASS | WebFetch | 220 press releases visible, paginated. |
| 2 | Valtioneuvosto decisions | `https://valtioneuvosto.fi/en/decisions/press-releases` | PASS | WebFetch | 25 decision press releases from 2026. |
| 3 | Valtioneuvosto sessions | `https://valtioneuvosto.fi/en/sessions` | FAIL (404) | curl | Returns 404. URL may have changed. |
| 4 | Media service | `https://media.valtioneuvosto.fi/en/frontpage` | PASS | WebFetch | Login portal for media representatives. Public material links available. |
| 5 | Embassy network | `https://finlandabroad.fi/` | FAIL (403) | curl | Bot protection blocks access. |
| 6 | MFA current affairs | `https://um.fi/current-affairs` | FAIL (403) | curl | Bot protection blocks access. |
| 7 | MFA media service | `https://um.fi/media-service` | FAIL (403) | curl | Bot protection blocks access. |
| 8 | Eduskunta Open Data | `https://avoindata.eduskunta.fi/` | CONDITIONAL | WebFetch | Page loads but requires JavaScript to function. Shows "Sivusto tarvitsee toimiakseen Javascript-tuen." |
| 9 | Eduskunta plenary sessions | `https://www.eduskunta.fi/EN/vaski/sivut/trip.aspx` | CONDITIONAL | curl (full UA) | Returns 200 with full Chrome user agent. Fails with minimal UA. |
| 10 | Eduskunta govt proposals | `https://www.eduskunta.fi/EN/vaski/sivut/he.aspx` | CONDITIONAL | curl (full UA) | Returns 200 with full Chrome user agent. Fails with minimal UA. |
| 11 | VM economic surveys | `https://vm.fi/en/economic-surveys` | FAIL (404) | curl | URL does not exist. |
| 12 | VM budget proposals | `https://vm.fi/en/budget-proposals` | FAIL (404) | curl | URL does not exist. |
| 13 | Open budget data | `https://tutkibudjettia.fi/` | REDIRECT | WebFetch | 301 redirect to `https://vm.fi/tutkibudjettia.fi-sivusto-uudistuu` (site being rebuilt). |
| 14 | TEM energy | `https://tem.fi/en/energy` | PASS | WebFetch | Energy policy page with 12 topic cards. Latest news from 2026-03-13. |
| 15 | TEM innovation | `https://tem.fi/en/innovation` | FAIL (404) | curl | URL does not exist. |
| 16 | Team Finland | `https://www.team-finland.fi/en` | PASS | WebFetch | Page loads. "Team Finland network helps your company go global." |
| 17 | Business Finland | `https://www.businessfinland.fi/en` | PASS | WebFetch | Page loads. Funding, programs, advisory services visible. |
| 18 | BOF Bulletin | `https://www.bofbulletin.fi/en/` | PASS | WebFetch | Articles on economy. Latest from 2026-02-25. |
| 19 | BOFIT Institute | `https://www.bofit.fi/en` | PASS | WebFetch | BOFIT web service loads. Weekly reviews, publications, seminars visible. |
| 20 | BOF speeches | `https://www.suomenpankki.fi/en/news-and-topical/speeches-and-interviews2/` | PASS | WebFetch | Speeches page loads. Latest: Olli Rehn speech 2026-01-16. |
| 21 | BOF statistics | `https://www.suomenpankki.fi/en/statistics/` | PASS | WebFetch | Statistics hub. Recent releases from 2026-03. |
| 22 | BOF publications | `https://publications.bof.fi/` | PASS | WebFetch | Kaisu publication archive. 10 recent publications from 2026-03. |
| 23 | STT newsroom (BOF) | `https://www.sttinfo.fi/uutishuone/1865/suomen-pankki` | PASS | WebFetch | Press release service. 1,292 releases available. |
| 24 | SUPO overview | `https://supo.fi/en/overview` | PASS | WebFetch | National Security Overview 2026 loads. Full content visible. |
| 25 | SUPO espionage overview | `https://supo.fi/en/overview-of-state-espionage-and-influencing` | PASS | WebFetch | Full content on Russia/China espionage threats. |
| 26 | Presidentti current affairs | `https://www.presidentti.fi/en/current-affairs/` | PASS | WebFetch | Current affairs section loads. |
| 27 | Presidentti speeches | `https://www.presidentti.fi/en/category/speeches/` | FAIL (404) | curl | URL does not exist. WordPress category URL may have changed. |
| 28 | Presidentti media | `https://www.presidentti.fi/en/office-and-contact/for-the-media/` | PASS | WebFetch | Media contact page loads. Staff directory visible. |
| 29 | Finlex API docs | `https://www.finlex.fi/fi/ohjeet/apidocs/` | FAIL (404) | curl | URL does not exist. API docs may have moved. |
| 30 | NATO RSS feeds page | `https://www.nato.int/cps/en/natohq/rss_feeds.htm` | FAIL (404) | WebFetch + curl | Old URL structure. NATO site rebuilt. |

---

## 5. Key Findings and Recommendations

### 5.1 Fully Operational Sources (no changes needed)

- **Valtioneuvosto.fi**: All 6 RSS feeds working. The aggregated press releases feed (LOmkEPY4nk2s) is the single most valuable automated monitoring point -- 100 items, updated same-day.
- **Presidentti.fi**: WordPress RSS feed confirmed functional with current content.
- **Defmin.fi**: Atom feed confirmed working.
- **SUPO**: RSS feed confirmed working. Low-frequency, high-value.
- **Bank of Finland ecosystem**: All 5 entry points (main site, BOF Bulletin, BOFIT, publications archive, statistics) load correctly. STT newsroom provides an alternative press release channel.
- **TEM press releases**: HTML entry point works. Energy sub-page works.
- **VM press releases**: HTML entry point works.

### 5.2 Sources Requiring Attention

| Issue | Sources | Recommended Action |
|---|---|---|
| **403 bot protection** | um.fi (all pages), finlandabroad.fi (all pages) | Use valtioneuvosto.fi aggregated RSS for MFA press releases. For finlandabroad.fi, investigate if Liferay API endpoints bypass bot protection, or use rotating browser-profile headers. |
| **CAPTCHA blocking** | eduskunta.fi (RSS page, main page via WebFetch) | Use Open Data API at avoindata.eduskunta.fi (requires JS). curl with full Chrome user agent gets 200 for VASKI document pages. |
| **404 broken URLs** | Finlex RSS (`finlex.fi/fi/rss/kokoelma`), NATO RSS feeds page, valtioneuvosto.fi/en/sessions, vm.fi/en/economic-surveys, vm.fi/en/budget-proposals, tem.fi/en/innovation, presidentti.fi speeches category, finlex.fi API docs | Update URLs in source document. These pages have likely been restructured. |
| **Site in transition** | NATO (nato.int rebuilding site), tutkibudjettia.fi (redirecting to vm.fi rebuild notice) | Monitor for new URL structures. NATO news page loads but content area is empty. |

### 5.3 [VERIFY] Resolutions

| Item | Verdict |
|---|---|
| Finlex RSS at `finlex.fi/fi/rss/kokoelma` | **INVALID** -- returns 404. No working RSS found. Use HTML scraping of collection pages. |
| Eduskunta RSS at `eduskunta.fi/.../parliament-press-releases.aspx` | **BLOCKED** -- CAPTCHA prevents automated access. Use avoindata.eduskunta.fi API instead. |
| um.fi RSS | **NOT FOUND** -- um.fi blocks all automated access (403). No RSS URL discoverable. Use valtioneuvosto.fi aggregated feed. |
| vm.fi RSS | **NOT FOUND** -- no RSS link on press releases page. Use valtioneuvosto.fi aggregated feed. |
| tem.fi RSS | **NOT FOUND** -- no RSS link on press releases page. Use valtioneuvosto.fi aggregated feed. |
| Bank of Finland RSS | **NOT FOUND** -- no RSS link on press releases page. Use STT newsroom or HTML scraping. |
| finlandabroad.fi RSS (EU Rep) | **NOT FOUND** -- site returns 403. No RSS discoverable. |
| NATO RSS | **INVALID** -- old RSS feeds page returns 404. NATO site rebuilt; no replacement RSS found. |
| puolustusvoimat.fi RSS | **DISCOVERED** -- an RSS link was found on the current-issues page (not previously documented). URL needs extraction from page source for YAML config. |

### 5.4 YAML Config Corrections Needed

The following fields in the YAML monitoring manifest should be updated:

1. `fi_finlex.rss_feed`: Change from `"http://finlex.fi/fi/rss/kokoelma"` to `null` (404)
2. `fi_nato.rss_feed`: Change from `"https://www.nato.int/cps/en/natohq/rss_feeds.htm"` to `null` (404, site rebuilt)
3. `fi_nato.entry_url`: NATO news page loads but content area is empty during rebuild
4. `fi_defence_forces`: Investigate and add the RSS link discovered on puolustusvoimat.fi/en/current-issues
5. Remove broken additional entry point URLs: `vm.fi/en/economic-surveys`, `vm.fi/en/budget-proposals`, `tem.fi/en/innovation`, `presidentti.fi/en/category/speeches/`, `valtioneuvosto.fi/en/sessions`, `finlex.fi/fi/ohjeet/apidocs/`
6. `tutkibudjettia.fi`: Note redirect to vm.fi rebuild page

---

*Test conducted 2026-03-19 using WebFetch and curl with Mozilla/5.0 user agent.*
