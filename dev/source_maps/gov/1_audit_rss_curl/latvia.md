# Latvia Government Sources — URL Fetchability Test Results

**Date tested:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/latvia_government_sources.md`

---

## Summary

| Metric | Count |
|---|---|
| Total unique URLs tested | 55 |
| Fully accessible (HTTP 200 / content loads) | 44 |
| RSS feeds verified functional | 5 |
| RSS pages exist but empty ("No RSS feeds available") | 4 |
| HTTP 403 (blocked/forbidden) | 1 |
| HTTP 404 (not found) | 5 |
| Connection failure (timeout/unreachable) | 1 |
| Certificate error | 1 |

### Verdict

The vast majority of Latvia's government source URLs are accessible and return expected content. The two primary RSS feeds (MFA and EM) are confirmed functional with 20 items each. LIAA also has a working RSS feed. NATO's RSS feed URL returns 404 (likely moved). The EU Council blocks automated fetching (403). Canada.ca is reachable via WebFetch but times out with curl. One URL (vestnesis.lv/oficialie-pazinojumi/) returns 404 and one (fm.gov.lv/en/s/ta) returns 404, suggesting path changes.

---

## 1. Primary Entry Point URLs

| # | Institution | Entry Point URL | Method | Status | Notes |
|---|---|---|---|---|---|
| 1a | President | `https://www.president.lv/en/articles?page=0` | WebFetch | 200 OK | 10 articles visible. First: "On the National Security Council meeting" (2026-03-19) |
| 1b | Cabinet of Ministers | `https://www.mk.gov.lv/en/articles` | WebFetch | 200 OK | 10 articles, 64 pages. First: NB8 joint statement (2026-02-24) |
| 2 | MFA | `https://www.mfa.gov.lv/en/articles` | WebFetch | 200 OK | 10 articles. First: "Foreign Minister Braže to pay a working visit to Norway" (2026-03-19) |
| 3a | MoD | `https://www.mod.gov.lv/en/zinas` | WebFetch | 200 OK | News listing with filters. First: "NATO's Innovation Range for uncrewed systems held in Selija" (2026-03-18) |
| 3b | NBS | `https://www.mil.lv/en` | WebFetch | 200 OK | Homepage with news items. First: "Close air support control unit exercise 'FURIOUS WOLF 26-1'" |
| 4 | Saeima | `https://www.saeima.lv/en/news/saeima-news` | WebFetch | 200 OK | Press releases, 190 pages. First: "Saeima expands ban on mobile phones in schools" (2026-03-12) |
| 5a | Vestnesis | `https://www.vestnesis.lv/` | WebFetch | 200 OK | Issue Nr. 55 (2026-03-19) visible. Legal acts and announcements |
| 5b | Likumi.lv | `https://likumi.lv/` | WebFetch | 200 OK | Legislation database functional. Search and categories visible |
| 6 | Finance Ministry | `https://www.fm.gov.lv/en/articles` | WebFetch | 200 OK | First: "New local government finance equalization model" (2026-02-26) |
| 7a | Latvijas Banka (news) | `https://www.bank.lv/en/news/` | WebFetch | 200 OK | Navigation page loads, links to sub-sections |
| 7b | Latvijas Banka (press) | `https://www.bank.lv/en/news-and-events/news-and-articles/press-releases` | WebFetch | 200 OK | Press releases with pagination. First: "Latvijas Banka starts publishing deposit rate overview" (2023-04-20) |
| 8 | Min. of Economics | `https://www.em.gov.lv/en/articles` | WebFetch | 200 OK | First: "Minister of Economics Meets with U.S. Business Leaders at Mar-a-Lago" (2026-02-19) |
| 9a | VDD | `https://vdd.gov.lv/en/news/press-releases` | WebFetch | 200 OK | Page loads; press releases loaded via AJAX (JS-rendered) |
| 9b | SAB | `https://www.sab.gov.lv/en/news/` | WebFetch | 200 OK | First: "SAB's annual classified report 2025 and proposed plans for 2026 approved" (2026-03-17) |
| 9c | MIDD | `https://www.midd.gov.lv/en` | WebFetch | 200 OK | About page loads. No news section visible (institutional info only) |
| 9d | NSC | `https://www.president.lv/en/national-security-council` | WebFetch | 200 OK | Institutional page with composition and historical context |
| 10a | KNAB | `https://www.knab.gov.lv/en/articles` | WebFetch | 200 OK | First: "KNAB to become the contact point of whistleblowers" (2026-02-12) |
| 10b-i | NATO eFP | `https://www.nato.int/cps/en/natohq/topics_136388.htm` | WebFetch | 200 OK | NATO eastern flank page. Forward Land Forces, Air Defence, Baltic Sentry |
| 10b-ii | Canada DND | `https://www.canada.ca/en/department-national-defence.html` | WebFetch | 200 OK | DND homepage loads (curl times out but WebFetch works) |
| 10c-i | EU Council | `https://www.consilium.europa.eu/en/press/press-releases/` | curl | **403 Forbidden** | Blocks automated fetching. Bot protection active |
| 10c-ii | EEAS | `https://www.eeas.europa.eu/eeas/press-material_en` | WebFetch | 200 OK | Press material hub. 14,093 press releases, filterable |
| 10d | Baltic Assembly | `https://www.baltasam.org/` | WebFetch | 200 OK | Estonian Presidency 2026. News section active (Feb-Mar 2026 items) |

---

## 2. RSS / Atom Feed Tests

| # | Institution | RSS URL | Method | Status | Details |
|---|---|---|---|---|---|
| 2a | MFA (articles) | `https://www.mfa.gov.lv/en/rss/articles` | WebFetch | **VALID RSS 2.0** | 20 items. Title: "RSS jaunumi". Latest: "Foreign Minister Braže to pay a working visit to Norway" (2026-03-19) |
| 2b | MFA (events) | `https://www.mfa.gov.lv/en/rss/events` | WebFetch | **VALID RSS 2.0** | 20 items. Title: "RSS notikumi". Minister's schedule/activities |
| 8a | EM (articles) | `https://www.em.gov.lv/en/rss/articles` | WebFetch | **VALID RSS 2.0** | 20 items. Title: "RSS jaunumi". Latest: "Minister Meets with U.S. Business Leaders" (2026-02-19) |
| 8b | EM (events) | `https://www.em.gov.lv/en/rss/events` | WebFetch | **VALID RSS 2.0** | 2 items. Title: "RSS notikumi" |
| - | LIAA (articles) | `https://www.liaa.gov.lv/en/rss/articles` | WebFetch | **VALID RSS 2.0** | 20 items. Title: "RSS jaunumi" |
| 1a | President | `https://www.president.lv/en/rss` | WebFetch | Page exists, empty | "No RSS feeds avalible right now." |
| 1b | Cabinet | `https://www.mk.gov.lv/en/rss` | WebFetch | Page exists, empty | "No RSS feeds avalible right now." |
| 6 | Finance Min. | `https://www.fm.gov.lv/en/rss` | WebFetch | Page exists, empty | "No RSS feeds avalible right now." |
| 10a | KNAB | `https://www.knab.gov.lv/en/rss` | WebFetch | Page exists, empty | "No RSS feeds avalible right now." |
| 3a | MoD | `https://www.mod.gov.lv/en/rss` | curl | **404 Not Found** | No RSS page exists |
| 3b | NBS | `https://www.mil.lv/en/rss` | curl+WebFetch | **404 Not Found** | No RSS feed available |
| 9a | VDD | `https://vdd.gov.lv/en/rss` | curl | **Soft 404** | Returns HTTP 200 but serves a 404 error page |
| 9b | SAB | `https://www.sab.gov.lv/en/rss` | curl | **404 Not Found** | No RSS |
| 7 | Latvijas Banka | `https://www.bank.lv/en/rss` | curl | **404 Not Found** | No RSS |
| 10d | Baltic Assembly | `https://www.baltasam.org/rss` | curl | **404 Not Found** | No RSS |
| 10b | NATO News | `https://www.nato.int/cps/en/natolive/news.rss` | curl+WebFetch | **404 Not Found** | URL appears to have moved or been retired |
| 10b | Canada DND Atom | `https://www.canada.ca/content/canadasite/api/nws/fds/en/national-defence.atom` | curl | **Connection failure** | curl returns 000 (connection refused/timeout) |

---

## 3. Additional / Supplementary Entry Point URLs

| Institution | URL | Method | Status | Notes |
|---|---|---|---|---|
| MFA RSS hub | `https://www.mfa.gov.lv/en/rss` | WebFetch | 200 OK | Lists 2 feeds (articles, events) |
| EM RSS hub | `https://www.em.gov.lv/en/rss` | WebFetch | 200 OK | Lists 2 feeds (articles, events) |
| EM economic situation | `https://www.em.gov.lv/en/economic-situation-0` | WebFetch | 200 OK | Economic Development Report 2024, macroeconomic reviews |
| LIAA main | `https://www.liaa.gov.lv/en` | WebFetch | 200 OK | Investment agency site functional |
| LIAA RSS hub | `https://www.liaa.gov.lv/en/rss` | WebFetch | 200 OK | Lists articles and events RSS feeds |
| Cabinet composition | `https://www.mk.gov.lv/en/cabinet-composition` | WebFetch | 200 OK | Current government structure, 15 officials |
| TAP portal | `https://tapportals.mk.gov.lv/` | WebFetch | 200 OK | Legal acts project portal. Latvian only |
| MoD defense policy | `https://www.mod.gov.lv/en/nozares-politika` | WebFetch | 200 OK | Defence policy sections, NATO, comprehensive defence |
| MoD Support Ukraine | `https://www.mod.gov.lv/en/support-ukraine` | WebFetch | 200 OK | 665M EUR military aid (2022-2025), drone coalition details |
| MoD Cybersecurity | `https://www.mod.gov.lv/en/cybersecurity` | WebFetch | 200 OK | National Cyber Security Law (2024), National Cyber Security Centre |
| Saeima news overview | `https://www.saeima.lv/en/news` | WebFetch | 200 OK | Schedule and navigation, social media links |
| Saeima follow updates | `https://www.saeima.lv/en/news/follow-the-updates` | WebFetch | 200 OK | **No RSS feed URLs found** on the page despite indication |
| Saeima live sessions | `https://www.saeima.lv/en/live/` | curl | 200 OK | Page accessible |
| Vestnesis announcements | `https://www.vestnesis.lv/oficialie-pazinojumi/` | curl | **404 Not Found** | URL may have changed |
| N-Lex Latvia | `https://n-lex.europa.eu/n-lex/legis_lv/latvijas_vestnesis_form` | curl | 200 OK | EU legislation gateway for Latvia |
| FM managing authority | `https://www.fm.gov.lv/en/managing-authority` | WebFetch | 200 OK | EU funds info. EUR 10.5B cohesion policy for Latvia |
| FM national economy | `https://www.fm.gov.lv/en/s/ta` | curl | **404 Not Found** | Path may have changed |
| Bank.lv forecasts | `https://www.bank.lv/en/operational-areas/task-monetary-policy/forecasts` | curl | 200 OK | Accessible |
| Bank.lv financial stability | `https://www.bank.lv/en/news-and-events/financial-stability-report` | curl | 200 OK | Accessible |
| Bank.lv annual report | `https://www.bank.lv/en/news-and-events/annual-report` | curl | 200 OK | Accessible |
| Bank.lv stat data | `https://www.bank.lv/en/statistics/stat-data` | WebFetch | 200 OK | Statistical data hub with latest figures (Q4 2025) |
| Bank.lv working papers | `https://www.bank.lv/en/news-and-events/discussion-papers` | curl | 200 OK | Accessible |
| Bank.lv lending survey | `https://www.bank.lv/en/news-and-events/euro-area-bank-lending-survey` | curl | 200 OK | Accessible |
| Bank.lv subscribe | `https://www.bank.lv/en/subscribe` | curl | 200 OK | Newsletter subscription page |
| Macroeconomics.lv | `https://www.macroeconomics.lv/` | curl | 200 OK | **Certificate error** with WebFetch, but curl returns 200 |
| KNAB annual reports | `https://www.knab.gov.lv/en/annual-reports` | curl | 200 OK | Accessible |
| MIDD areas of activity | `https://www.midd.gov.lv/en/areas-activity` | curl | 200 OK | Accessible |

---

## 4. [VERIFY] Items — Resolution

| Item | Documented Claim | Test Result | Verdict |
|---|---|---|---|
| mil.lv/en/rss (NBS RSS) | Unknown if RSS exists | 404 Not Found | **No RSS available.** Use HTML scraping of mil.lv/en |
| saeima.lv RSS (via follow-the-updates page) | RSS indicated at `/en/news/follow-the-updates` | Page loads but contains **no RSS feed URLs** — only social media links | **No RSS available.** The page does not expose feed URLs |
| vestnesis.lv RSS | Unknown if RSS exists | vestnesis.lv/en/rss returns 404 | **No RSS available.** Note: likumi.lv has RSS for legal categories (mentioned on likumi.lv page) |
| VDD RSS | Unknown | vdd.gov.lv/en/rss returns soft 404 (200 status, 404 page content) | **No RSS available.** Use HTML scraping |
| SAB RSS | Unknown | sab.gov.lv/en/rss returns 404 | **No RSS available.** Use periodic check |
| KNAB RSS | Unknown | knab.gov.lv/en/rss page exists but says "No RSS feeds avalible right now" | **No RSS available.** Same status as mk.gov.lv and fm.gov.lv (gov.lv CMS RSS not enabled) |
| Baltic Assembly RSS | Unknown | baltasam.org/rss returns 404 | **No RSS available.** Use periodic check |
| bank.lv RSS | Unknown, possibly removed in redesign | bank.lv/en/rss returns 404 | **No RSS available.** Newsletter subscription at /en/subscribe is only option |
| Canada DND Atom feed | `canada.ca/content/canadasite/api/nws/fds/en/national-defence.atom` | Connection failure (curl returns 000) | **Feed URL invalid or retired.** Main DND page accessible via WebFetch |
| NATO news RSS | `nato.int/cps/en/natolive/news.rss` | 404 Not Found | **Feed URL has moved or been retired.** Main eFP page accessible |
| EU Council RSS | Press release feeds referenced but specific RSS URL not documented | consilium.europa.eu returns 403 for main press page | **Blocked by bot protection.** Needs browser-based or API access |
| Vestnesis official announcements | `vestnesis.lv/oficialie-pazinojumi/` | 404 Not Found | **URL has changed.** Main vestnesis.lv page still functional |
| FM national economy section | `fm.gov.lv/en/s/ta` | 404 Not Found | **URL has changed.** Main articles page still functional |

---

## 5. Key Findings and Recommendations

### Working well (no changes needed)
- **MFA RSS** (`mfa.gov.lv/en/rss/articles`): Best government RSS source. 20 items, current (same-day), RSS 2.0.
- **EM RSS** (`em.gov.lv/en/rss/articles`): Functional, 20 items, RSS 2.0.
- **LIAA RSS** (`liaa.gov.lv/en/rss/articles`): Not in original manifest but functional. Consider adding.
- All **P1 entry point pages** (president.lv, mk.gov.lv, mfa.gov.lv, mod.gov.lv, mil.lv) load correctly with current content.
- All **P2 entry point pages** (saeima.lv, vestnesis.lv, likumi.lv, fm.gov.lv, bank.lv, em.gov.lv, vdd.gov.lv, sab.gov.lv, midd.gov.lv, knab.gov.lv, baltasam.org) load correctly.

### Needs attention
- **NATO RSS** (`nato.int/cps/en/natolive/news.rss`): 404. Need to find current NATO RSS feed URL.
- **Canada DND Atom**: Connection failure. Need to find current feed URL or use HTML scraping.
- **EU Council**: 403 on press releases page. Requires browser-like headers or API access.
- **macroeconomics.lv**: SSL certificate issue (WebFetch fails, curl succeeds). May need certificate pinning bypass.

### URLs to update in manifest
- `vestnesis.lv/oficialie-pazinojumi/` — 404, needs new path
- `fm.gov.lv/en/s/ta` — 404, needs new path

### VDD extraction note
- VDD press releases page loads but content is **JavaScript-rendered via AJAX**. Standard HTML scraping will not capture items. Requires headless browser or API endpoint discovery.

### Gov.lv CMS RSS status
- 4 ministries have RSS pages that say "No RSS feeds avalible right now": president.lv, mk.gov.lv, fm.gov.lv, knab.gov.lv
- Only MFA and EM have functional RSS on the gov.lv CMS
- MoD has no RSS page at all (404)
- Periodic rechecking recommended as the platform may enable RSS incrementally
