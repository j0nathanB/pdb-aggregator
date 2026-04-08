# Australia Government Sources -- URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/australia_government_sources.md`
**Test methods:** WebFetch (headless browser-like), curl with Mozilla UA, fallback with HTTP/1.1

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 62 |
| Confirmed working (HTTP 200 / valid RSS) | 37 |
| Confirmed working (301 redirect, destination accessible) | 2 |
| Connection blocked by CDN/WAF (HTTP/2 stream error, Akamai) | 16 |
| Blocked by WAF (Incapsula) | 2 |
| HTTP 403 Forbidden | 2 |
| HTTP 404 Not Found | 4 |
| TLS certificate error | 1 |
| Timeout (WebFetch only, curl not attempted / also failed) | 0 |

**Key finding:** 16 URLs across Defence, DFAT, ASIO, ASD, ONI, and Industry domains are hosted behind Akamai CDN which drops HTTP/2 streams for non-browser clients. DNS resolves, TLS handshake completes, but the HTTP/2 stream returns `INTERNAL_ERROR (err 2)` before delivering any response. These are known live government websites accessible via real browsers. The pipeline will need a browser-based fetcher (Playwright/Puppeteer) or an Akamai-compatible HTTP client for these sources.

**VERIFY results:** PM RSS feed discovered at `pm.gov.au/rss.xml` (confirmed working, 50 items). PMC RSS at `pmc.gov.au/news-centre/rss` (returns 200 via curl, blocked by Incapsula via WebFetch). All other VERIFY items for RSS (DFAT, Defence, Industry, ASIO, ASD, Home Affairs, Austrade, nationalsecurity.gov.au) could not be confirmed due to CDN blocking, or returned 404.

---

## 1. PM & PM&C (Section 1.1)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.pm.gov.au/media` | Entry point | WebFetch | **OK** -- "Media \| Prime Minister of Australia", 248 pages of content | Working, clean HTML |
| `https://www.pm.gov.au/rss.xml` | RSS [VERIFY] | WebFetch | **OK** -- Valid RSS, "Prime Minister of Australia", 50 items | **VERIFIED: RSS exists** |
| `https://www.pm.gov.au/media/feed` | RSS [VERIFY] | curl | **404** | Not a valid path |
| `https://www.pm.gov.au/media/rss` | RSS [VERIFY] | curl | **404** | Not a valid path |
| `https://www.pm.gov.au/feed` | RSS [VERIFY] | curl | **404** | Not a valid path |
| `https://ministers.pmc.gov.au/` | Entry point | WebFetch | **OK** -- "Ministers' media centre", 6 ministers listed | Working |
| `https://www.pmc.gov.au/news-centre` | Entry point | curl | **200** (WebFetch returned empty) | Curl OK; WebFetch rendered blank |
| `https://www.pmc.gov.au/news-centre/rss` | RSS [VERIFY] | curl | **200** | Curl returns 200; WebFetch blocked by Incapsula WAF |
| `https://pmtranscripts.pmc.gov.au/` | Entry point | WebFetch | **OK** -- "PM Transcripts", ~26,000 items dating to 1940s | Working |
| `https://www.pmc.gov.au/international-policy-and-national-security/national-security` | Entry point (NSC) | curl | **200** | Working via curl; Incapsula blocks WebFetch |

---

## 2. DFAT / Foreign Minister (Section 1.2)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.foreignminister.gov.au/minister/penny-wong/media-releases` | Entry point | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://ministers.dfat.gov.au/Pages/RSS-Feed.aspx` | RSS hub | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.dfat.gov.au/news/departmental-media-releases` | Entry point | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.dfat.gov.au/news-speeches-and-media` | Entry point | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://ministers.dfat.gov.au/minister/tim-ayres/media-releases` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.dfat.gov.au/international-relations/security/sanctions` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.foreignminister.gov.au/rss` | RSS [VERIFY] | WebFetch | **TIMEOUT** -- Akamai likely | Cannot verify |
| `https://www.foreignminister.gov.au/feed` | RSS [VERIFY] | WebFetch | **TIMEOUT** -- Akamai likely | Cannot verify |

---

## 3. Defence (Section 1.3)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.defence.gov.au/news-events/releases` | Entry point | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | DNS resolves (23.211.139.201), TLS OK, stream killed |
| `https://www.minister.defence.gov.au/media-releases` | Entry point | WebFetch + curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.minister.defence.gov.au/news-media` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.defence.gov.au/news-events/news` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.defence.gov.au/about/reviews-inquiries` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.defence.gov.au/operations` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.defence.gov.au/news-events/rss` | RSS [VERIFY] | WebFetch | **TIMEOUT** -- Akamai likely | Cannot verify |
| `https://www.minister.defence.gov.au/rss` | RSS [VERIFY] | WebFetch | **TIMEOUT** -- Akamai likely | Cannot verify |

---

## 4. Parliament of Australia (Section 1.4)

### 4a. Senate RSS Feeds

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.aph.gov.au/Parliamentary_Business/Hansard` | Entry point | WebFetch | **OK** -- "Hansard -- Parliament of Australia", March 2026 transcripts | Working |
| `https://www.aph.gov.au/Parliamentary_Business/Senate_Estimates` | Entry point | WebFetch | **OK** -- "Senate estimates -- Parliament of Australia", 8 committees listed | Working |
| `https://www.aph.gov.au/Parliamentary_Business/Hansard/Search` | Entry point | WebFetch | **OK** -- "Search Hansard -- Parliament of Australia" | Working |
| `https://www.aph.gov.au/senate/rss/new_inquiries` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "New Senate Committee Inquiries", 100 items | Working |
| `https://www.aph.gov.au/senate/rss/reports` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Senate Committee Reports Tabled", 70 items | Working |
| `https://www.aph.gov.au/senate/rss/red` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Today's Senate Committee Hearings", 1 item | Working |
| `https://www.aph.gov.au/senate/rss/upcoming_hearings` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Upcoming Senate Committee Hearings", 3 items | Working |
| `https://www.aph.gov.au/senate/rss/senators_details` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Updates to Senators' Details", 1 item | Working |

### 4b. House of Representatives RSS Feeds

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.aph.gov.au/house/rss/media_releases` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "DHR Media Releases", 3 items | Working |
| `https://www.aph.gov.au/house/rss/house_inquiries` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "House Inquiries", 0 items (empty but valid) | Working (structurally valid) |
| `https://www.aph.gov.au/house/rss/joint_inquiries` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Joint Inquiries", 0 items (empty but valid) | Working (structurally valid) |
| `https://www.aph.gov.au/house/rss/divisions` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Divisions", 0 items (empty but valid) | Working (structurally valid, populates during session) |
| `https://www.aph.gov.au/house/rss/daily_program` | RSS | WebFetch | **OK** -- Valid RSS 2.0, "Daily Program", 0 items (empty but valid) | Working (structurally valid) |

### 4c. Parliamentary Committees

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.aph.gov.au/Parliamentary_Business/Committees/Joint/Intelligence_and_Security` | Entry point | WebFetch | **OK** -- "Parliamentary Joint Committee on Intelligence and Security", 2 active inquiries | Working |
| `https://www.aph.gov.au/Parliamentary_Business/Committees/Joint/Foreign_Affairs_Defence_and_Trade` | Entry point | WebFetch | **OK** -- "Joint Standing Committee on Foreign Affairs, Defence and Trade", 3 active inquiries | Working |

### 4d. Parliamentary Library RSS

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://parlinfo.aph.gov.au/parlInfo/feeds/rss.w3p;adv=yes;orderBy=date-eFirst;page=0;query=Dataset%3Abillsdgs,prspub;resCount=Default` | RSS | WebFetch | **403 Forbidden** | ParlInfo RSS feeds blocked |
| `https://parlinfo.aph.gov.au/parlInfo/feeds/rss.w3p;adv=yes;orderBy=date-eFirst;page=0;query=Date%3AthisYear%20Dataset%3Abillsdgs;resCount=100` | RSS | WebFetch | **403 Forbidden** | ParlInfo RSS feeds blocked |

---

## 5. Federal Register of Legislation (Section 1.5)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.legislation.gov.au/gazettes` | Entry point | WebFetch | **OK** -- "Gazettes - Federal Register of Legislation" | Working |
| `https://www.legislation.gov.au/` | Entry point | WebFetch | **OK** -- "Federal Register of Legislation - Home Page" | Working |

---

## 6. Treasury (Section 1.6)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://treasury.gov.au/media-release` | Entry point | WebFetch | **OK** -- "Media Releases \| Treasury.gov.au", 64 releases, 7 pages | Working |
| `https://ministers.treasury.gov.au/ministers/jim-chalmers-2022/media-releases` | Entry point | WebFetch | **OK** -- "Media releases \| Treasury Ministers", RSS feed access noted | Working |
| `https://ministers.treasury.gov.au/ministers/jim-chalmers-2022/transcripts` | Entry point | WebFetch | **OK** -- "Transcripts \| Treasury Ministers", 50 pages of content | Working |
| `https://treasury.gov.au/media` | Entry point | WebFetch | **OK** -- "Media \| Treasury.gov.au" | Working |
| `https://budget.gov.au/` | Entry point | WebFetch | **OK** -- "Budget.gov.au \| Budget 2025-26" | Working |
| `https://firb.gov.au/` | Entry point | WebFetch | **TLS ERROR** -- ERR_TLS_CERT_ALTNAME_INVALID | Certificate mismatch; curl also returns 000 |

---

## 7. Reserve Bank of Australia (Section 1.7)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.rba.gov.au/media-releases/` | Entry point | WebFetch | **OK** -- "Media Releases \| RBA", archive 1991-2026 | Working |
| `https://www.rba.gov.au/monetary-policy/int-rate-decisions/` | Entry point | WebFetch | **OK** -- "Monetary Policy Decisions -- 2026 \| RBA" | Working |
| `https://www.rba.gov.au/updates/rss-feeds.html` | RSS hub | WebFetch | **OK** -- Lists 10 RSS feeds | Working |
| `https://www.rba.gov.au/rss/rss-cb-media-releases.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0 (RDF), "Media Releases", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-exchange-rates.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Exchange Rates", 21 items | Working |
| `https://www.rba.gov.au/rss/rss-cb-speeches.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Speeches", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-speeches-webcast.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Webcast of Speeches", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-bulletin.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Bulletin", 3 items | Working |
| `https://www.rba.gov.au/rss/rss-cb-fsr.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Financial Stability Review", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-smp.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Statements on Monetary Policy", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-rdp.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Research Discussion Papers", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-foi.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Freedom of Information", 1 item | Working |
| `https://www.rba.gov.au/rss/rss-cb-changes-to-tables.xml` | RSS | WebFetch | **OK** -- Valid RSS 1.0, "Changes to Statistical Tables", 1 item | Working |

---

## 8. Trade & Industry (Section 1.8)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://ministers.dfat.gov.au/minister/tim-ayres/media-releases` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | Same CDN issue as all DFAT |
| `https://www.industry.gov.au/news` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.minister.industry.gov.au/ministers/media-releases` | Entry point | curl | **BLOCKED** -- Akamai HTTP/2 stream error | CDN blocks non-browser clients |
| `https://www.minister.industry.gov.au/ministers/pages/subscribe-receive-updates` | VERIFY RSS | WebFetch | **TIMEOUT** -- Akamai likely | Cannot verify |

---

## 9. Intelligence / National Security (Section 1.9)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.oni.gov.au/` | Entry point | WebFetch + curl | **BLOCKED** -- WebFetch socket closed; curl HTTP/2 error (000) | CDN blocks non-browser clients |
| `https://intelligence.gov.au` | Entry point | curl | **301** redirect | Redirects (likely to oni.gov.au or similar); final destination also blocked |
| `https://www.asio.gov.au/resources/speeches-and-statements` | Entry point | WebFetch + curl | **BLOCKED** -- Timeout/000 | CDN blocks non-browser clients |
| `https://www.aph.gov.au/Parliamentary_Business/Committees/Joint/Intelligence_and_Security` | Entry point | WebFetch | **OK** -- See Parliament section | Working |
| `https://www.pmc.gov.au/international-policy-and-national-security/national-security` | Entry point (NSC) | curl | **200** | Working via curl |

---

## 10. Country-Specific Institutions (Section 1.10)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.asd.gov.au/news-media` | Entry point [VERIFY URL] | WebFetch + curl | **BLOCKED** -- Timeout/000 | CDN blocks non-browser clients |
| `https://cyber.gov.au` | Entry point | curl | **301** redirect | Redirects; final destination blocked (Akamai) |
| `https://www.homeaffairs.gov.au/news-media` | Entry point | curl | **200** | Working |
| `https://minister.homeaffairs.gov.au/` | Entry point | curl | **200** | Working |
| `https://www.austrade.gov.au/en/news` | Entry point [VERIFY URL] | curl + WebFetch | **404** -- Path not found | **INVALID URL: /en/news returns 404** |
| `https://www.austrade.gov.au/news` | Corrected URL | curl + WebFetch | **200** -- Redirects to Analysis page; 43 articles | Correct path is `/news` (redirects to analysis/insights) |
| `https://www.austrade.gov.au/` | Root | curl | **200** | Root domain works |
| `https://www.nationalsecurity.gov.au/` | Entry point | curl | **200** | Working |

---

## 11. Third-Party / Supplementary

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.openaustralia.org.au/api/` | API docs | WebFetch | **TIMEOUT** | WebFetch timed out; curl also 000 |
| `https://www.openaustralia.org.au/alert/` | Alerts page | WebFetch | **OK** -- "OpenAustralia.org Email Alerts", working registration form | Working |

---

## VERIFY Item Results

| Item | Claim | Result | Action |
|---|---|---|---|
| PM RSS at `pm.gov.au/media/feed` or `/rss` | Possible RSS | **RSS found at `pm.gov.au/rss.xml`** (50 items, valid) | Update YAML: set `rss_feed: "https://www.pm.gov.au/rss.xml"` |
| PMC RSS at `pmc.gov.au/news-centre` | Possible RSS | **RSS found at `pmc.gov.au/news-centre/rss`** (curl 200, Incapsula blocks WebFetch) | Update YAML: set PMC RSS |
| DFAT RSS at `foreignminister.gov.au/rss` or `/feed` | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| Defence RSS at `defence.gov.au/news-events` | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| Defence ministerial RSS at `minister.defence.gov.au` | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| Treasury ministerial RSS on `ministers.treasury.gov.au` | Possible RSS | **WebFetch reports RSS feed access noted on page** | Likely exists; page loads OK |
| Industry RSS at `minister.industry.gov.au` | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| ASIO RSS | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| ASD RSS | Possible RSS | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| ASD URL `asd.gov.au/news-media` | Verify path | **Cannot verify** -- Akamai blocks all access | Needs browser-based testing |
| Home Affairs RSS | Possible RSS | **Not found** via curl (page returns 200, no RSS path tested positive) | Likely no RSS |
| Austrade RSS | Possible RSS | **Not found** | No RSS identified |
| Austrade URL `austrade.gov.au/en/news` | Verify path | **404 -- INVALID**. Correct path: `austrade.gov.au/news` | Update entry point URL |
| nationalsecurity.gov.au RSS | No RSS expected | **Confirmed: no RSS** | As documented |
| legislation.gov.au API/RSS | Possible API | **No RSS or API found** | As documented |
| ParlInfo RSS feeds | Documented RSS | **403 Forbidden** | ParlInfo RSS feeds are access-restricted |
| `firb.gov.au` | Entry point | **TLS certificate error** (ERR_TLS_CERT_ALTNAME_INVALID) | Certificate misconfigured; access FIRB via `treasury.gov.au` links instead |

---

## CDN/WAF Blocking Pattern

**Akamai-hosted domains (16 URLs, all returning HTTP/2 stream INTERNAL_ERROR):**
- `foreignminister.gov.au`
- `ministers.dfat.gov.au`
- `dfat.gov.au`
- `defence.gov.au`
- `minister.defence.gov.au`
- `industry.gov.au`
- `minister.industry.gov.au`
- `oni.gov.au`
- `asio.gov.au`
- `asd.gov.au`
- `intelligence.gov.au` (redirects)
- `cyber.gov.au` (redirects)

These domains all connect successfully at the TCP/TLS level but the Akamai CDN terminates the HTTP/2 stream before delivering content. This affects curl, wget, and WebFetch equally. A headless browser (Playwright, Puppeteer) or a properly configured HTTP client that presents full browser TLS fingerprinting (e.g., `curl-impersonate`) would be required.

**Incapsula-hosted domains (2 URLs, WAF challenge):**
- `pmc.gov.au` -- curl returns 200 but WebFetch gets blocked by Incapsula JS challenge

**Domains accessible via simple HTTP clients (curl/WebFetch):**
- `pm.gov.au`, `ministers.pmc.gov.au`, `pmtranscripts.pmc.gov.au`
- `aph.gov.au` (all parliamentary URLs)
- `legislation.gov.au`
- `treasury.gov.au`, `ministers.treasury.gov.au`, `budget.gov.au`
- `rba.gov.au` (all RSS feeds and pages)
- `homeaffairs.gov.au`, `minister.homeaffairs.gov.au`
- `austrade.gov.au`
- `nationalsecurity.gov.au`
- `openaustralia.org.au`

---

## Pipeline Recommendations

1. **Use RSS where available (27 confirmed feeds):** RBA (10 feeds), Parliament Senate (5 feeds), Parliament House (5 feeds), PM (1 feed), PMC (1 feed). These are the most reliable automated monitoring paths.

2. **Browser-based scraping required for Akamai domains:** DFAT, Defence, Industry, ONI, ASIO, ASD all require Playwright/Puppeteer or `curl-impersonate` to bypass Akamai bot detection.

3. **Fix documented URLs:**
   - `austrade.gov.au/en/news` -> `austrade.gov.au/news`
   - `firb.gov.au` has TLS issues; link via `treasury.gov.au` instead
   - PM RSS: add `https://www.pm.gov.au/rss.xml` (confirmed working)

4. **ParlInfo RSS feeds return 403:** The two Parliamentary Library RSS feeds documented in the source map are access-restricted. Alternative: scrape ParlInfo HTML search results or use OpenAustralia API.

5. **Treasury ministerial RSS:** `ministers.treasury.gov.au` pages reference RSS access; likely functional but exact feed URL needs browser-based verification.
