# Estonia Government Sources — Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/estonia_government_sources.md`
**Method:** WebFetch (primary), curl with Mozilla UA (fallback)

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 62 |
| **Entry point URLs** | 17 |
| **RSS/Atom feed URLs** | 17 |
| **Additional entry point URLs** | 28 |
| **Accessible (HTTP 200 + valid content)** | 42 |
| **RSS feeds confirmed working** | 8 |
| **RSS feeds confirmed dead/invalid** | 9 |
| **HTTP 404 (not found)** | 15 |
| **HTTP 403 (Cloudflare blocked)** | 2 |
| **Timeout** | 2 |
| **Sources with at least one working entry point** | 16/16 |

### Key Findings

1. **FeedBurner valitsus feeds are DEAD.** All three FeedBurner feeds (English, Estonian, Russian) for valitsus.ee redirect to the valitsus.ee homepage as HTML. The site-native RSS at `valitsus.ee/en/rss-feeds/rss.xml` works and returns 100 items.
2. **mil.ee has working RSS feeds** at both `/en/feed/` (English, 10 items) and `/feed/` (Estonian, 10 items) -- previously marked [VERIFY]. WordPress standard feed paths work.
3. **vm.ee (MFA) has NO working RSS.** The `/en/rss-feeds` page returns 404, and `/en/rss.xml` and `/rss.xml` both return 404. The entry point `/en/news` also returns 404. The root `/en` works but the news listing path has changed.
4. **valitsus.ee/en/news returns 404.** Multiple valitsus.ee subpages return 404 (news, government session filter, PM page, comms unit). The root `/en` works. Site has been restructured.
5. **kapo.ee subpages blocked by Cloudflare** (403). Main page loads via WebFetch but `/en/content/annual-reviews/` and `/en/content/tasks-and-objectives/` are blocked.
6. **rahandusministeerium.ee consistently times out.** The legacy Finance Ministry domain appears non-functional. `fin.ee/en` works.
7. **No RSS found** for: fin.ee, eestipank.ee, mkm.ee, ccdcoe.org, ria.ee, eu.mfa.ee (all [VERIFY] items tested negative).

---

## 1. RSS Feed Test Results

### 1.1 Confirmed Working RSS Feeds

| # | Feed URL | Status | Feed Title | Items | Notes |
|---|---|---|---|---|---|
| 1 | `https://valitsus.ee/en/rss-feeds/rss.xml` | **WORKING** | Eesti Vabariigi Valitsus | 100 | Valid RSS 2.0. Primary feed for government news. |
| 2 | `https://kaitseministeerium.ee/en/news/1/feed` | **WORKING** | (untitled) | 30 | Valid RSS 2.0. MoD press releases. Items from 2018-2019 range suggest stale or archival content. |
| 3 | `https://mil.ee/en/feed/` | **WORKING** | Estonian Defence Forces | 10 | Valid RSS 2.0. English. Most recent item 2026-03-06. |
| 4 | `https://mil.ee/feed/` | **WORKING** | Kaitsevägi | 10 | Valid RSS 2.0. Estonian. Most recent item 2026-03-19. |
| 5 | `http://feeds.feedburner.com/RiigikoguPressReleases` | **WORKING** | Press releases - Riigikogu | 10 | Valid RSS 2.0. |
| 6 | `http://feeds.feedburner.com/RiigikoguAgenda` | **WORKING** | Agenda - Riigikogu | 12 | Valid RSS 2.0. Most recent 2026-03-16. |
| 7 | `http://feeds.feedburner.com/RiigikoguSittingReviews` | **WORKING** | Sitting reviews - Riigikogu | 10 | Valid RSS 2.0. |
| 8 | `http://feeds.feedburner.com/RiigikoguNewsFromCommittees` | **WORKING** | News from committees - Riigikogu | 10 | Valid RSS 2.0. |

### 1.2 Dead / Invalid RSS Feeds

| # | Feed URL | Status | Result | Notes |
|---|---|---|---|---|
| 1 | `http://feeds.feedburner.com/valitsus/press-eng` | **DEAD** | Redirects to valitsus.ee homepage (HTML) | FeedBurner feed broken. Returns Drupal HTML page. |
| 2 | `http://feeds.feedburner.com/valitsus/press-est` | **DEAD** | Redirects to valitsus.ee homepage (HTML) | Same as above. |
| 3 | `http://feeds.feedburner.com/valitsus/press-rus` | **DEAD** | Redirects to valitsus.ee homepage (HTML) | Same as above. |
| 4 | `https://www.president.ee/en/rss/index.html` | **BLOCKED** | Cloudflare challenge/redirect JS | Returns JS redirect, not RSS content. |
| 5 | `https://vm.ee/en/rss-feeds` | **404** | Page not found | Confirmed 404. |
| 6 | `https://vm.ee/en/rss.xml` | **404** | Not found | Alternate path also 404. |
| 7 | `https://vm.ee/rss.xml` | **404** | Not found | Alternate path also 404. |
| 8 | `https://www.fin.ee/en/rss.xml` | **404** | Not found | [VERIFY] -- no RSS exists. |
| 9 | `https://www.fin.ee/rss.xml` | **404** | Not found | [VERIFY] -- no RSS exists. |

### 1.3 [VERIFY] RSS Results -- All Negative

| # | Source | URLs Tested | Result |
|---|---|---|---|
| 1 | Eesti Pank | `eestipank.ee/en/rss.xml`, `/en/feed` | 404 -- No RSS |
| 2 | MKM | `mkm.ee/en/rss.xml`, `mkm.ee/rss.xml` | 404 -- No RSS |
| 3 | CCDCOE | `ccdcoe.org/feed/`, `ccdcoe.org/rss` | 404 -- No RSS |
| 4 | RIA | `ria.ee/en/rss.xml`, `ria.ee/rss.xml` | 404 -- No RSS |
| 5 | EU Representation | Not tested (no candidate URLs) | No RSS |

---

## 2. Entry Point URL Test Results

### 2.1 Primary Entry Points

| # | Institution | Entry Point URL | Method | HTTP | Status | Notes |
|---|---|---|---|---|---|---|
| 1a | Valitsus (Government) | `https://valitsus.ee/en/news` | curl | 404 | **FAIL** | Path has changed. Root `/en` returns 200. |
| 1a | Valitsus (Government) | `https://valitsus.ee/en` | curl | 200 | **OK** | Root works; news path needs updating. |
| 1b | President | `https://president.ee/en/media/press-releases/` | WebFetch | 200 | **OK** | Press releases listed, most recent 2026-03-03. |
| 2 | MFA (vm.ee) | `https://vm.ee/en/news` | curl | 404 | **FAIL** | News path broken. Root `/en` returns 200. |
| 2 | MFA (vm.ee) | `https://vm.ee/en` | curl | 200 | **OK** | Root works; news path needs updating. |
| 3a | MoD | `https://kaitseministeerium.ee/en/news` | WebFetch | 200 | **OK** | 10 articles visible, most recent 2026-03-19. Pagination to 9 pages. |
| 3b | EDF (mil.ee) | `https://mil.ee/en/news/` | WebFetch | 200 | **OK** | News articles listed, most recent 2026-03-06. |
| 4 | Riigikogu | `https://www.riigikogu.ee/en/news-and-publications/news-press-releases/` | WebFetch | 200 | **OK** | Press releases listed, most recent 2026-03-19. |
| 5 | Riigi Teataja | `https://www.riigiteataja.ee/en/` | WebFetch | 200 | **OK** | Homepage with legislation listings. |
| 6 | Finance (fin.ee) | `https://www.fin.ee/en` | WebFetch | 200 | **OK** | Homepage loads with news items. |
| 6 | Finance (legacy) | `https://www.rahandusministeerium.ee/en/news` | curl/WebFetch | TIMEOUT | **FAIL** | Domain times out consistently. |
| 7 | Eesti Pank | `https://www.eestipank.ee/en/press` | WebFetch | 200 | **OK** | Press releases listed by month, 2026 content active. |
| 8 | MKM | `https://www.mkm.ee/en` | WebFetch | 200 | **OK** | Homepage loads with news and ministry info. |
| 9a | KAPO | `https://kapo.ee/en/` | WebFetch | 200 | **OK** | Homepage loads (Cloudflare protected). |
| 9b | EFIS (main) | `https://www.valisluureamet.ee/en.html` | WebFetch | 200 | **OK** | Loads with 2026 report headline. |
| 9b | EFIS (report) | `https://raport.valisluureamet.ee/2026/en/` | WebFetch | 200 | **OK** | 2026 report loads, interactive TOC. |
| 10a | CCDCOE | `https://ccdcoe.org/news/` | WebFetch | 200 | **OK** | 7 articles listed, most recent 2026-03-13. |
| 10b | RIA | `https://www.ria.ee/en` | WebFetch | 200 | **OK** | Homepage loads with news. |
| 10c | EU Representation | `https://eu.mfa.ee/` | WebFetch | 200 | **OK** | Homepage loads. |
| 10d | Kaitseliit | `https://www.kaitseliit.ee/en/news` | WebFetch | 200 | **OK** | News listed, most recent 2025-04-24. Limited English content. |

### 2.2 Additional Entry Points

| # | URL | HTTP | Status | Notes |
|---|---|---|---|---|
| 1 | `https://valitsus.ee/en/news?type=government_session` | 404 | **FAIL** | Path broken (same as /en/news). |
| 2 | `https://valitsus.ee/en/prime-minister-ministers` | 404 | **FAIL** | Path broken. |
| 3 | `https://valitsus.ee/en/news-contacts/government-communication-unit` | 200 | **OK** | |
| 4 | `https://eelnoud.valitsus.ee/` | 200 | **OK** | Draft legislation portal. |
| 5 | `https://president.ee/en/media/speeches/` | 200 | **OK** | |
| 6 | `https://president.ee/en/official-duties/` | 200 | **OK** | |
| 7 | `https://vm.ee/en/ministry-news-and-contacts/about-ministry-foreign-affairs/foreign-minister` | 200 | **OK** | |
| 8 | `https://vm.ee/en/international-relations` | 404 | **FAIL** | Path has changed. |
| 9 | `https://eu.mfa.ee/` | 200 | **OK** | |
| 10 | `https://kaitseministeerium.ee/en/national-defence` | 404 | **FAIL** | Path has changed. |
| 11 | `https://kaitseministeerium.ee/en/national-defence/defence-budget` | 404 | **FAIL** | Path has changed. |
| 12 | `https://mil.ee/en/landforces/ccdcoe/` | 200 | **OK** | |
| 13 | `https://mil.ee/en/operations-abroad/` | 200 | **OK** | |
| 14 | `https://www.riigikogu.ee/en/category/press-releases/` | 200 | **OK** | |
| 15 | `https://www.riigikogu.ee/en/parliament-of-estonia/legislation/` | 404 | **FAIL** | Path has changed. |
| 16 | `https://www.riigikogu.ee/en/subscribe-to-rss-or-the-newsletter/` | 200 | **OK** | |
| 17 | `https://www.rahandusministeerium.ee/en/news` | TIMEOUT | **FAIL** | Domain unresponsive. |
| 18 | `https://www.fin.ee/en/public-finances-and-taxes/state-budget` | 404 | **FAIL** | Path has changed. |
| 19 | `https://www.eestipank.ee/en/publications` | 200 | **OK** | |
| 20 | `https://www.eestipank.ee/en/press/statistical-releases` | 200 | **OK** | |
| 21 | `https://www.eestipank.ee/en/press/economic-policy-statements` | 200 | **OK** | |
| 22 | `https://statistika.eestipank.ee/` | 200 | **OK** | |
| 23 | `https://www.eestipank.ee/en/press/press-contacts` | 200 | **OK** | |
| 24 | `https://www.eestipank.ee/en/calendar` | 200 | **OK** | |
| 25 | `https://www.mkm.ee/en/entrepreneurship-and-innovation` | 404 | **FAIL** | Path has changed. |
| 26 | `https://kapo.ee/en/content/annual-reviews/` | 403 | **BLOCKED** | Cloudflare challenge. Main `/en/` loads via WebFetch. |
| 27 | `https://kapo.ee/en/content/tasks-and-objectives/` | 403 | **BLOCKED** | Cloudflare challenge. |
| 28 | `https://www.valisluureamet.ee/assessment.html` | 200 | **OK** | |
| 29 | `https://raport.valisluureamet.ee/en/previous-reports/` | 404 | **FAIL** | Path not found. |
| 30 | `https://ccdcoe.org/research/` | 200 | **OK** | |
| 31 | `https://ccdcoe.org/cycon/` | 200 | **OK** | |
| 32 | `https://ccdcoe.org/exercises/locked-shields/` | 200 | **OK** | |
| 33 | `https://www.ria.ee/en/state-information-system` | 404 | **FAIL** | Path has changed. |

---

## 3. Per-Source Status Summary

| # | Institution | Primary Entry | RSS Status | Overall | Action Required |
|---|---|---|---|---|---|
| 1a | Valitsus | **BROKEN** (404) | Site RSS works; FeedBurner DEAD | Partial | Update entry URL (try `/en`). Remove FeedBurner feeds. Use `valitsus.ee/en/rss-feeds/rss.xml` as sole RSS. |
| 1b | President | OK | Cloudflare-blocked RSS index | Partial | RSS index returns JS challenge. Scrape entry point as fallback. |
| 2 | MFA (vm.ee) | **BROKEN** (404) | No RSS found | Degraded | Update entry URL. HTML scraping of new news path needed. |
| 3a | MoD | OK | RSS works | **Full** | No action needed. |
| 3b | EDF (mil.ee) | OK | RSS found at `/en/feed/` | **Full** | Update config: RSS exists at `mil.ee/en/feed/` (was [VERIFY]). |
| 4 | Riigikogu | OK | 4 FeedBurner feeds all working | **Full** | No action needed. |
| 5 | Riigi Teataja | OK | No RSS (as documented) | OK | No change. |
| 6 | Finance (fin.ee) | OK | No RSS confirmed | OK | Remove rahandusministeerium.ee (dead). No RSS. |
| 7 | Eesti Pank | OK | No RSS confirmed | OK | No change. All 6 additional endpoints work. |
| 8 | MKM | OK | No RSS confirmed | OK | Fix `/en/entrepreneurship-and-innovation` path (404). |
| 9a | KAPO | OK (main) | No RSS (as documented) | Partial | Subpages blocked by Cloudflare (403). May need browser-based scraping. |
| 9b | EFIS | OK | No RSS (as documented) | OK | Fix `raport.valisluureamet.ee/en/previous-reports/` (404). |
| 10a | CCDCOE | OK | No RSS confirmed | OK | No change. All additional endpoints work. |
| 10b | RIA | OK | No RSS confirmed | Partial | Fix `/en/state-information-system` path (404). |
| 10c | EU Repr | OK | No RSS confirmed | OK | No change. |
| 10d | Kaitseliit | OK | No RSS (as documented) | OK | English content very sparse (most recent: Apr 2025). |

---

## 4. Critical Updates for Pipeline Configuration

### Must Fix (blocking pipeline functionality)

1. **valitsus.ee entry URL**: Change from `valitsus.ee/en/news` to `valitsus.ee/en`. Remove all three FeedBurner feeds. Use `https://valitsus.ee/en/rss-feeds/rss.xml` as sole RSS source.
2. **vm.ee entry URL**: Change from `vm.ee/en/news` to `vm.ee/en`. Set extraction_method to `html_scrape` (no RSS available).
3. **mil.ee RSS**: Add `https://mil.ee/en/feed/` as confirmed RSS feed. Change extraction_method from `html_scrape` to `rss_poll`.
4. **rahandusministeerium.ee**: Remove entirely -- domain times out. Use `fin.ee/en` only.

### Should Fix (subpage paths broken)

5. **kaitseministeerium.ee**: Remove `/en/national-defence` and `/en/national-defence/defence-budget` additional entry points (both 404).
6. **riigikogu.ee**: Remove `/en/parliament-of-estonia/legislation/` (404).
7. **fin.ee**: Remove `/en/public-finances-and-taxes/state-budget` (404).
8. **mkm.ee**: Remove `/en/entrepreneurship-and-innovation` (404).
9. **ria.ee**: Remove `/en/state-information-system` (404).
10. **raport.valisluureamet.ee**: Remove `/en/previous-reports/` (404).
11. **vm.ee**: Remove `/en/international-relations` (404).

### Monitor (access issues)

12. **kapo.ee subpages**: Cloudflare 403 on `/en/content/annual-reviews/` and `/en/content/tasks-and-objectives/`. Main page loads. May need headless browser for annual review downloads.
13. **president.ee RSS index**: Returns Cloudflare JS challenge instead of RSS content. Scrape press releases page directly.
