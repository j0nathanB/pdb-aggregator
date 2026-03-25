# United Kingdom Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/united_kingdom_government_sources.md`
**Test method:** WebFetch (primary), curl with browser User-Agent (fallback)

---

## Summary

| Category | Count |
|---|---|
| **Total unique URLs tested** | 55 |
| **OK (200 / valid feed)** | 44 |
| **FAILED (403 — bot protection)** | 5 |
| **FAILED (404 — not found)** | 4 |
| **FAILED (500 — server error)** | 1 |
| **BLOCKED (WAF/admin block)** | 1 |
| **N/A (no public URL)** | 1 |

**Overall reachability: 80% (44/55)**

The 5 Parliament-domain 403s are caused by Cloudflare/WAF bot protection across all `*.parliament.uk` domains. These sites load normally in browsers. The 4 GOV.UK 404s indicate URL path changes since the document was authored. Gov.gg (Guernsey) is returning a persistent 500 server error. Gov.im (Isle of Man) blocks automated access via WAF.

---

## 1. GOV.UK Atom Feeds (P1 + P2)

All GOV.UK Atom feeds are fully functional with 20 entries per page. No bot protection.

| # | Institution | Atom Feed URL | Status | Entries |
|---|---|---|---|---|
| 1 | PM's Office (No. 10) | `https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street.atom` | **OK** | 20 |
| 2 | FCDO | `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office.atom` | **OK** | 20 |
| 3 | MOD | `https://www.gov.uk/government/organisations/ministry-of-defence.atom` | **OK** | 20 |
| 4 | HM Treasury | `https://www.gov.uk/government/organisations/hm-treasury.atom` | **OK** | 20 |
| 5 | DBT | `https://www.gov.uk/government/organisations/department-for-business-and-trade.atom` | **OK** | 20 |

---

## 2. GOV.UK Entry Point Pages

| # | Institution | Entry Point URL | Status |
|---|---|---|---|
| 1 | PM's Office | `https://www.gov.uk/government/organisations/prime-ministers-office-10-downing-street` | **OK** (200) |
| 2 | FCDO | `https://www.gov.uk/government/organisations/foreign-commonwealth-development-office` | **OK** (200) |
| 3 | MOD | `https://www.gov.uk/government/organisations/ministry-of-defence` | **OK** (200) |
| 4 | HM Treasury | `https://www.gov.uk/government/organisations/hm-treasury` | **OK** (200) |
| 5 | DBT | `https://www.gov.uk/government/organisations/department-for-business-and-trade` | **OK** (200) |

---

## 3. GOV.UK Additional Entry Points

| URL | Status | Notes |
|---|---|---|
| `https://www.gov.uk/search/news-and-communications?organisations%5B%5D=prime-ministers-office-10-downing-street&content_store_document_type%5B%5D=speech` | **OK** (200) | 8,479 results. Working filter. |
| `https://www.gov.uk/email-signup?link=/government/organisations/prime-ministers-office-10-downing-street` | **OK** (200) | Email signup page loads. |
| `https://www.gov.uk/government/collections/uk-sanctions-list` | **FAIL** (404) | URL path has changed or collection removed. |
| `https://www.gov.uk/foreign-travel-advice` | **OK** (200) | 226 countries listed. |
| `https://devtracker.fcdo.gov.uk/` | **OK** (200) | Development Tracker loads. |
| `https://www.gov.uk/government/organisations/ministry-of-defence/about/statistics` | **OK** (200) | MOD statistics page loads. |
| `https://www.gov.uk/government/collections/budget-documents` | **FAIL** (404) | URL path has changed or collection removed. |
| `https://www.gov.uk/government/collections/public-finances-statistics` | **FAIL** (404) | URL path has changed or collection removed. |
| `https://www.gov.uk/government/collections/financial-sanctions-regime-specific-consolidated-lists-and-general-guidance` | **FAIL** (404) | URL path has changed or collection removed. |
| `https://www.gov.uk/government/collections/the-uks-trade-agreements` | **OK** (200) | 40 agreements with 74 countries listed. |
| `https://www.gov.uk/government/collections/national-security-and-investment-act` | **OK** (200) | NSI Act guidance hub loads. |
| `https://www.gov.uk/government/collections/strategic-export-controls` | **FAIL** (404) | URL path has changed or collection removed. |

---

## 4. Bank of England RSS Feeds

All Bank of England RSS feeds are fully functional. RSS 2.0 format. No bot protection.

| Feed | URL | Status | Entries |
|---|---|---|---|
| News | `https://www.bankofengland.co.uk/rss/news` | **OK** | 50 |
| Publications | `https://www.bankofengland.co.uk/rss/publications` | **OK** | 50 |
| Speeches | `https://www.bankofengland.co.uk/rss/speeches` | **OK** | 50 |
| Statistics | `https://www.bankofengland.co.uk/rss/statistics` | **OK** | 50 |
| Prudential Regulation | `https://www.bankofengland.co.uk/rss/prudential-regulation-publications` | **OK** | 50 |
| Bank Insights | `https://www.bankofengland.co.uk/rss/bank-insights` | **OK** | 4 |
| Events | `https://www.bankofengland.co.uk/rss/events` | **OK** | 50 |
| RSS Hub Page | `https://www.bankofengland.co.uk/rss` | **OK** (200) | Lists 8 feed categories |
| News Entry Point | `https://www.bankofengland.co.uk/news` | **OK** (200) | — |

Note: The RSS hub page lists an 8th feed ("Explainers") not documented in the source map.

---

## 5. The Gazette Feeds

| Feed | URL | Status | Entries |
|---|---|---|---|
| All Notices | `https://www.thegazette.co.uk/all-notices/notice/data.feed` | **OK** | 10 (of 4.7M total) |
| State Notices (cat 11) | `https://www.thegazette.co.uk/all-notices/notice/data.feed?categorycode=11` | **OK** | 10 (of 43,787 total) |
| Entry Point | `https://www.thegazette.co.uk/` | **OK** (200) | — |

---

## 6. Legislation.gov.uk Feeds

| Feed | URL | Status | Entries |
|---|---|---|---|
| All New Legislation | `https://www.legislation.gov.uk/new/data.feed` | **OK** | 20 (12 pages) |
| UK Public General Acts | `https://www.legislation.gov.uk/new/ukpga/data.feed` | **OK** | 20 (12 pages) |
| UK Statutory Instruments | `https://www.legislation.gov.uk/new/uksi/data.feed` | **OK** | 20 (12 pages) |
| Entry Point | `https://www.legislation.gov.uk/new` | **OK** (200) | — |

---

## 7. Parliament Sites

All `*.parliament.uk` domains return **403** to automated requests (WebFetch and curl). Cloudflare/WAF bot protection is active across the entire Parliament digital estate.

| Institution | URL | Status | Notes |
|---|---|---|---|
| Hansard | `https://hansard.parliament.uk/` | **FAIL** (403) | Bot protection. Loads in browser. |
| Select Committees | `https://committees.parliament.uk/` | **FAIL** (403) | Bot protection. Loads in browser. |
| Parliament Bills | `https://www.parliament.uk/business/bills-and-legislation/` | **FAIL** (403) | Bot protection. Loads in browser. |
| Parliament RSS Hub | `https://www.parliament.uk/site-information/rss-feeds/` | **FAIL** (403) | Bot protection. Cannot verify RSS feed URLs. |

**Pipeline implication:** Parliament sites will require either (a) a headless browser with JS execution for scraping, (b) the Parliament API at `api.parliament.uk`, or (c) the TheyWorkForYou third-party API as a proxy.

---

## 8. Intelligence / National Security

| Institution | URL | Status | Notes |
|---|---|---|---|
| SIS (MI6) | `https://www.sis.gov.uk/` | **FAIL** (403) | Bot protection or geo-blocking. |
| GCHQ | `https://www.gchq.gov.uk/` | **OK** (200) | No RSS found. Confirmed no feed. |
| NCSC Threat Reports | `https://www.ncsc.gov.uk/section/keep-up-to-date/threat-reports` | **OK** (200) | Loads correctly. |
| NCSC News | `https://www.ncsc.gov.uk/news` | **OK** (200) | RSS link found in footer. |
| NCSC All RSS Feed | `https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml` | **OK** | 20 entries. Valid RSS 2.0. |
| ISC Reports | `https://isc.independent.gov.uk/reports/` | **OK** (200) | WordPress site. No RSS found. |
| NSC | N/A | **N/A** | No public web presence. |

### NCSC RSS Feeds Discovered (not in source document)

| Feed | URL |
|---|---|
| All | `https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml` |
| Guidance | `https://www.ncsc.gov.uk/api/1/services/v1/guidance-rss-feed.xml` |
| News | `https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml` |
| Blog Posts | `https://www.ncsc.gov.uk/api/1/services/v1/blog-post-rss-feed.xml` |
| Threat Reports | `https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml` |

---

## 9. Devolved Administrations

| Institution | URL | Status | RSS Found? | Notes |
|---|---|---|---|---|
| Scottish Government | `https://www.gov.scot/news/` | **OK** (200) | **No** | Email subscription only (Mailchimp). 8,962 news results. |
| Welsh Government | `https://media.service.gov.wales/news/` | **OK** (200) | **No** | 3,814 news items. No feed. |
| NI Executive | `https://www.northernireland.gov.uk/press-releases` | **OK** (200) | **No** | 13,515 press releases. No RSS despite doc suggesting one. |

---

## 10. Crown Dependencies

| Institution | URL | Status | RSS Found? | Notes |
|---|---|---|---|---|
| Jersey (gov.je) | `https://www.gov.je/News/Pages/index.aspx` | **FAIL** (404) | **No** | Documented URL is dead. |
| Jersey (gov.je) | `https://www.gov.je/News/` | **OK** (200) | **No** | Correct working URL (path changed). |
| Guernsey (gov.gg) | `https://www.gov.gg/news` | **FAIL** (500) | **No** | Server error. Root domain also 500. |
| Guernsey (gov.gg) | `https://www.gov.gg/` | **FAIL** (500) | — | Entire site appears down. |
| Isle of Man (gov.im) | `https://www.gov.im/news/` | **BLOCKED** | **No** | WAF "Request Rejected" page. Admin-blocked. |

---

## 11. [VERIFY] Items Resolution

| Item | Source Document Claim | Test Result | Verdict |
|---|---|---|---|
| Select Committees RSS | `[VERIFY RSS]` — none identified | 403 on all parliament.uk; cannot test directly | **UNVERIFIED** — blocked by bot protection |
| GCHQ/NCSC RSS | `[VERIFY RSS]` — none identified for GCHQ | GCHQ: confirmed **no RSS**. NCSC: **RSS found** (5 feeds) | **RESOLVED** — NCSC has RSS; GCHQ does not |
| ISC RSS | `[VERIFY RSS]` — none identified | Confirmed **no RSS**. WordPress site, no feed links. | **CONFIRMED: No RSS** |
| Scottish Gov RSS | `[VERIFY RSS]` — email only confirmed | Confirmed **no RSS**. Email subscription via Mailchimp only. | **CONFIRMED: No RSS** |
| Welsh Gov RSS | `[VERIFY RSS]` — none identified | Confirmed **no RSS**. | **CONFIRMED: No RSS** |
| NI Executive RSS | `[VERIFY RSS URL]` — RSS alerts mentioned | Confirmed **no RSS** despite doc suggestion. No feed links on page. | **CONFIRMED: No RSS** |
| Crown Dependencies RSS | `[VERIFY RSS]` — none confirmed | Jersey: no RSS. Guernsey: site down (500). IoM: blocked. | **CONFIRMED: No RSS** (Jersey). Others untestable. |

---

## Recommended Source Document Updates

1. **NCSC RSS feeds should be added** to section 1.9b. Five category-specific RSS feeds are available at `ncsc.gov.uk/api/1/services/v1/*.xml`. The `atom_feed: null # [VERIFY]` for `gb_gchq_ncsc` in the YAML should be updated to include these NCSC feeds.

2. **Four GOV.UK collection URLs are returning 404** and need updated paths:
   - `gov.uk/government/collections/uk-sanctions-list`
   - `gov.uk/government/collections/budget-documents`
   - `gov.uk/government/collections/public-finances-statistics`
   - `gov.uk/government/collections/financial-sanctions-regime-specific-consolidated-lists-and-general-guidance`
   - `gov.uk/government/collections/strategic-export-controls`

3. **Jersey URL should be updated** from `gov.je/News/Pages/index.aspx` to `gov.je/News/`.

4. **Guernsey (gov.gg) is currently unreachable** (500 server error). Monitor for recovery.

5. **Isle of Man (gov.im) blocks automated access.** Requires browser-based approach or manual monitoring.

6. **Parliament sites require headless browser or API access.** All `*.parliament.uk` domains enforce Cloudflare bot protection. The Parliament API at `api.parliament.uk` or TheyWorkForYou API should be used instead.

7. **SIS (sis.gov.uk) returns 403** to automated requests. Given negligible publication frequency, manual periodic checks are sufficient.

8. **Bank of England has an 8th feed** ("Explainers") not documented in the source map, visible on the RSS hub page.
