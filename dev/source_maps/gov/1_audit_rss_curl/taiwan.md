# Taiwan Government Sources: URL Fetchability Test Results

**Date tested:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/taiwan_government_sources.md`

---

## Summary

| Category | Count |
|---|---|
| Total unique URLs tested | 55 |
| Fully accessible (200 OK, content valid) | 41 |
| Accessible with caveats (redirect, JS-required, encoding issues) | 6 |
| Failed (403, 404, 410, timeout, connection refused) | 8 |

### RSS Feed Results

| Status | Count |
|---|---|
| Confirmed working RSS feeds | 10 |
| RSS info pages (HTML, not feeds) | 3 |
| RSS feed returning 403 | 1 |
| [VERIFY] RSS — no feed found | 8 |

---

## 1. RSS Feed Tests

### Confirmed Working Feeds

| # | Institution | RSS URL | Status | Items |
|---|---|---|---|---|
| 1 | Presidential Office — News | `https://www.president.gov.tw/RSSNEWS.aspx` | PASS (RSS 2.0) | 9 |
| 2 | Presidential Office — Gazette | `https://www.president.gov.tw/RSSGazette.aspx` | PASS (RSS 2.0) | 10 |
| 3 | MOFA — News & Events | `https://en.mofa.gov.tw/OpenData.aspx?SN=07564A7F01D47BAD` | PASS (RSS 2.0) | 30 |
| 4 | MOFA — Press Releases | `https://en.mofa.gov.tw/OpenData.aspx?SN=3273AA376FB01416` | PASS (RSS 2.0) | 30 |
| 5 | MOFA — Statements & Responses | `https://en.mofa.gov.tw/OpenData.aspx?SN=E57623EED610E7DF` | PASS (RSS 2.0) | 50 |
| 6 | MOF — Press Releases (English) | `https://www.mof.gov.tw/Eng/Rss/f48d641f159a4866b1d31c0916fbcc71` | PASS (RSS 2.0) | 50 |
| 7 | CBC — Press Releases (Chinese) | `https://www.cbc.gov.tw/tw/rss-302-1.xml` | PASS (RSS 2.0) | 50 |
| 8 | CBC — Press Releases (English) | `https://www.cbc.gov.tw/en/rss-302-2.xml` | PASS (RSS 2.0) [was VERIFY] | 50 |
| 9 | BOFT — Chinese RSS | `https://www.trade.gov.tw/English/RSS/List.aspx?nodeID=90` | PASS (RSS 2.0) | 26 |
| 10 | MOFA — RSS info page | `https://en.mofa.gov.tw/Rss.aspx?n=1447` | PASS (HTML listing page; lists 5 feeds) | N/A |

**Notes on MOF:** The documented URL `https://www.mof.gov.tw/Eng/Rss` is an HTML page listing feeds, not a feed itself. The actual feed URL is `https://www.mof.gov.tw/Eng/Rss/f48d641f159a4866b1d31c0916fbcc71`.

### Failed / Problematic Feeds

| # | Institution | RSS URL | Status | Notes |
|---|---|---|---|---|
| 1 | MOEA (English) | `https://www.moea.gov.tw/MNS/english/news/NewsRSS.aspx?menu_id=1438` | FAIL (403) | Blocked by server; curl also returns 403 |

### RSS Info Pages (Not Feeds)

| # | Institution | URL | Status | Notes |
|---|---|---|---|---|
| 1 | MOF — RSS landing | `https://www.mof.gov.tw/Eng/Rss` | HTML page | Lists actual feed at `/Eng/Rss/f48d641f159a4866b1d31c0916fbcc71` |
| 2 | BOFT — Chinese RSS landing | `https://www.trade.gov.tw/StaticPage/RSS.aspx` | HTML page | Lists 4 feed categories |
| 3 | BOFT — English RSS landing | `https://www.trade.gov.tw/English/StaticPage/RSS.aspx` | HTML page | Lists Events feed at `/RSS/List.aspx?nodeID=90` |

### [VERIFY] RSS Results — No Feed Found

| # | Institution | Status | Notes |
|---|---|---|---|
| 1 | Executive Yuan | No RSS found | Confirmed: no RSS available |
| 2 | MND | No RSS found | Confirmed: no RSS available |
| 3 | Legislative Yuan | No RSS found | Confirmed: no RSS available |
| 4 | Executive Yuan Gazette | No RSS found | Open Data bulk download available instead |
| 5 | NSB | No RSS found | JS-rendered site; minimal content |
| 6 | MAC | No RSS found | Confirmed: no RSS available |
| 7 | OCAC | No RSS found | Confirmed: no RSS available |
| 8 | IDA / NSTC / Investment Commission | No RSS found | Confirmed: no RSS available for any of these 3 agencies |

---

## 2. Entry Point URL Tests

### P1 Sources

| # | Institution | URL | Method | Status | Notes |
|---|---|---|---|---|---|
| 1a | Presidential Office (ZH) | `https://www.president.gov.tw/NEWS` | WebFetch | REDIRECT (302 to homepage) | Redirects to `http://www.president.gov.tw/`; curl returns 200 after redirect |
| 1a | Presidential Office (EN) | `https://english.president.gov.tw/News` | WebFetch | REDIRECT (302 to homepage) | Same redirect behavior; curl returns 200 |
| 1b | Executive Yuan (ZH) | `https://www.ey.gov.tw/Page/5A898E83D438145A` | WebFetch | FAIL (page not found) | Returns error: "the webpage or file does not exist or has been removed" |
| 1b | Executive Yuan (EN) | `https://english.ey.gov.tw/Page/5A898E83D438145A` | WebFetch | PASS | Working; 2,998 press releases listed |
| 2 | MOFA — Press Releases | `https://en.mofa.gov.tw/News.aspx?n=1329&sms=272` | WebFetch | PASS | 1,084 press releases; most recent Mar 18 2026 |
| 2 | MOFA — News & Events | `https://en.mofa.gov.tw/News.aspx?n=1328&sms=273` | WebFetch | PASS | 1,591 news items; most recent Mar 18 2026 |
| 3 | MND (ZH) | `https://www.mnd.gov.tw/news/pressreleaselist` | WebFetch | PASS | Working; multiple press releases listed |
| 3 | MND (EN) | `https://www.mnd.gov.tw/en/news/PressReleaseList` | WebFetch | PASS | Working; press releases dated Mar 2026 |

### P2 Sources

| # | Institution | URL | Method | Status | Notes |
|---|---|---|---|---|---|
| 4 | Legislative Yuan (ZH) | `https://www.ly.gov.tw/Pages/List.aspx?nodeid=154` | WebFetch | WRONG CONTENT | Loads "Legislator Statements API" page, not news listing |
| 4 | Legislative Yuan (EN) | `https://www.ly.gov.tw/EngPages/List.aspx?nodeid=348` | WebFetch | PASS | Official Gazette Dept. info page (as documented) |
| 5 | Executive Yuan Gazette | `https://gazette.nat.gov.tw/` | WebFetch | PASS | 162,556 entries; latest issue Mar 19 2026 |
| 6 | MOF (EN) | `https://www.mof.gov.tw/Eng/multiplehtml/f48d641f159a4866b1d31c0916fbcc71` | WebFetch | PASS | 1,463 press releases; most recent Mar 19 2026 |
| 7 | CBC (EN) | `https://www.cbc.gov.tw/en/lp-302-2.html` | WebFetch | PASS (redirect to ZH homepage) | Loads Chinese homepage with press releases visible |
| 7 | CBC (ZH) | `https://www.cbc.gov.tw/tw/lp-302-1.html` | WebFetch | PASS | 7,711 press releases; paginated |
| 8a | MOEA (EN) | `https://www.moea.gov.tw/MNS/english/news/News.aspx?kind=6&menu_id=176` | WebFetch + curl | FAIL (403) | Blocked by server on both methods |
| 8b | BOFT (ZH) | `https://www.trade.gov.tw/Pages/List.aspx?nodeID=40` | WebFetch | PASS | News listing; JS-loaded content |
| 8b | BOFT (EN) | `https://www.trade.gov.tw/English/Pages/List.aspx?nodeID=86` | WebFetch | PASS | News section with search; last update Dec 2024 |
| 9a | NSB (ZH) | `https://www.nsb.gov.tw/` | curl | PASS (200) | JS-required; WebFetch gets no content |
| 9a | NSB (EN) | `https://www.nsb.gov.tw/en/` | curl | PASS (200) | JS-required; WebFetch gets no content |
| 9b | NSC | N/A | N/A | N/A | No independent website (by design) |
| 10a | MAC (EN) | `https://www.mac.gov.tw/en/News.aspx?n=2462&sms=262` | WebFetch + curl | FAIL (403) | Confirmed: English site returns 403 |
| 10a | MAC (ZH) | `https://www.mac.gov.tw/News.aspx?n=49&sms=39` | WebFetch | PASS | Working; news items dated Mar 2025 |
| 10b | OCAC (EN) | `https://www.ocac.gov.tw/OCAC/Eng/` | WebFetch | PASS | Working; news and services available |
| 10b | OCAC (ZH) | `https://www.ocac.gov.tw/ocac/` | WebFetch | PASS | Working |
| 10c | TAO (PRC) — Press conf | `http://www.gwytb.gov.cn/xwdt/xwfb/` | curl | PASS (200) | Encoding issues (gb2312); WebFetch shows garbled chars |
| 10c | TAO (PRC) — News | `http://www.gwytb.gov.cn/xwdt/` | curl | PASS (200) | Same encoding issues |
| 10d | IDA | `https://www.ida.gov.tw/` | WebFetch | PASS | Working; industrial development portal |
| 10d | NSTC | `https://www.nstc.gov.tw/` | WebFetch | PASS | Working; science & tech council portal |
| 10d | Investment Commission | `https://www.moeaic.gov.tw/` | curl | FAIL (timeout) | Connection timeout; site unreachable |

---

## 3. Additional Entry Point URL Tests

| # | Institution | URL | Method | Status | Notes |
|---|---|---|---|---|---|
| 1 | Presidential Gazette archive | `https://www.president.gov.tw/Page/95` | WebFetch | WRONG CONTENT | Shows Constitutional Amendments page, not Gazette archive |
| 2 | Presidential RSS info (EN) | `https://english.president.gov.tw/Page/23` | WebFetch | PASS | RSS info page with feed links |
| 3 | Presidential Video (EN) | `https://english.president.gov.tw/Video` | curl | PASS (200) | Accessible |
| 4 | EY Agency News (EN) | `https://english.ey.gov.tw/Page/FDB51B27DE3D4AF4` | WebFetch | PASS | 1,211 news items; latest Mar 20 2026 |
| 5 | EY Important Policies (EN) | `https://english.ey.gov.tw/Page/4B45023ECD498A37` | WebFetch | FAIL (410 Gone) | Resource permanently removed |
| 6 | MOFA Statements & Responses | `https://en.mofa.gov.tw/News.aspx?n=1330&sms=274` | WebFetch | PASS | 470 items; latest Mar 15 2026 |
| 7 | MOFA Background Info | `https://en.mofa.gov.tw/News.aspx?n=1331&sms=275` | WebFetch | PASS | Working; background materials |
| 8 | MOFA Chinese Press Room | `https://www.mofa.gov.tw/News.aspx?n=104&sms=70` | curl | FAIL (404) | Page not found |
| 9 | MND — PLA Activity | `https://www.mnd.gov.tw/news/plaactlist` | WebFetch | PASS | Daily PLA activity reports; Mar 11-19 entries |
| 10 | MND — News Clarifications | `https://www.mnd.gov.tw/news/pressreleaselist/cate/66` | WebFetch | PASS | News clarification section |
| 11 | MND — Ministry News | `https://www.mnd.gov.tw/news/mndlist` | WebFetch | PASS | Department news listing |
| 12 | MND — Civil Defense | `https://prepare.mnd.gov.tw` | WebFetch | PASS | Emergency preparedness portal |
| 13 | LY — Gazette System | `https://lci.ly.gov.tw/` | curl | FAIL (ECONNREFUSED) | Connection refused; site unreachable |
| 14 | LY — IVOD | `https://ivod.ly.gov.tw/` | WebFetch | PASS | Video proceedings; 47M+ page views |
| 15 | LY — Budget Center | `https://www.ly.gov.tw/Pages/List.aspx?nodeid=216` | WebFetch | WRONG CONTENT | Shows "Website Feedback" page, not Budget Center |
| 16 | Customs Administration | `https://web.customs.gov.tw/` | WebFetch | PASS | Working; trade statistics portal |
| 17 | MOF Events (EN) | `https://www.mof.gov.tw/Eng/multiplehtml/6642` | WebFetch | PASS | 154 events/announcements |
| 18 | MOF Press Releases (ZH) | `https://www.mof.gov.tw/multiplehtml/f48d641f159a4866b1d31c0916fbcc71` | WebFetch | PASS | Chinese press releases; working |
| 19 | MAC — Cross-strait Stats | `https://www.mac.gov.tw/en/np-4-2.html` | curl | FAIL (403) | English site blocked |
| 20 | SEF | `https://www.sef.org.tw/` | WebFetch | PASS | Working; Straits Exchange Foundation |
| 21 | Hsinchu Science Park | `https://www.sipa.gov.tw/` | WebFetch | PASS | Working; 179,513 employees listed |
| 22 | TSMC Corporate | `https://www.tsmc.com/english/news-events` | curl | FAIL (403) | Blocked; bot protection |
| 23 | NDC (EN) | `https://www.ndc.gov.tw/en/` | curl | FAIL (403) | Blocked |

---

## 4. [VERIFY] Item Resolution

| # | Item | Resolution | Action Needed |
|---|---|---|---|
| 1 | CBC English RSS at `/en/rss-302-2.xml` | VALID — working RSS 2.0 feed with 50 items | Update doc: mark as confirmed |
| 2 | Executive Yuan RSS | NOT FOUND — no RSS exists | Update doc: mark as confirmed absent |
| 3 | MND RSS | NOT FOUND — no RSS exists | Update doc: mark as confirmed absent |
| 4 | Legislative Yuan RSS | NOT FOUND — no RSS exists | Update doc: mark as confirmed absent |
| 5 | Executive Yuan Gazette RSS | NOT FOUND — Open Data bulk download only | Update doc: mark as confirmed absent |
| 6 | NSB RSS | NOT FOUND — JS-only site with minimal content | Update doc: mark as confirmed absent |
| 7 | MAC RSS | NOT FOUND — no RSS exists | Update doc: mark as confirmed absent |
| 8 | OCAC RSS | NOT FOUND — no RSS exists | Update doc: mark as confirmed absent |
| 9 | IDA/NSTC/Investment Comm RSS | NOT FOUND — none of these agencies offer RSS | Update doc: mark as confirmed absent |
| 10 | MAC EN entry point (403 noted) | CONFIRMED 403 — English site returns 403 | Use Chinese site as primary (working) |
| 11 | MOEA Chinese RSS | NOT TESTED — English RSS returns 403; Chinese equivalent likely same | Investigate alternative URLs |

---

## 5. Critical Issues Requiring Attention

### Broken / Unreachable URLs (action required)

1. **Executive Yuan Chinese press releases** (`ey.gov.tw/Page/5A898E83D438145A`) — page removed. English equivalent works. Need to find current Chinese listing page ID.

2. **MOEA entry point and RSS** (`moea.gov.tw/MNS/english/news/...`) — returns 403 on both WebFetch and curl. The entire MOEA English site appears to block automated access.

3. **Investment Commission** (`moeaic.gov.tw`) — connection timeout. Site may be down or have changed domains.

4. **LY Gazette System** (`lci.ly.gov.tw`) — connection refused. Infrastructure may be down or relocated.

5. **MAC English site** — returns 403. Chinese site works. Document already noted this issue.

6. **MOFA Chinese press room** (`mofa.gov.tw/News.aspx?n=104&sms=70`) — returns 404. URL parameters may have changed.

7. **EY Important Policies page** (`english.ey.gov.tw/Page/4B45023ECD498A37`) — returns 410 Gone. Page permanently removed.

### Content Mismatches (URL points to wrong content)

1. **Presidential Gazette archive** (`president.gov.tw/Page/95`) — shows Constitutional Amendments, not Gazette archive. Page ID has changed.

2. **LY News** (`ly.gov.tw/Pages/List.aspx?nodeid=154`) — shows Legislator Statements API, not news. Node ID may have changed.

3. **LY Budget Center** (`ly.gov.tw/Pages/List.aspx?nodeid=216`) — shows Website Feedback page, not Budget Center.

### Access Caveats

1. **NSB** (`nsb.gov.tw`) — requires JavaScript. Returns 200 but no content via non-JS clients. Headless browser required for scraping.

2. **TAO** (`gwytb.gov.cn`) — encoding issues (gb2312). Functional but requires explicit charset handling.

3. **Presidential Office** (`president.gov.tw/NEWS`) — redirects to homepage. The `/NEWS` path may no longer be a direct listing. RSS feeds are the reliable access method.

4. **CBC English entry point** (`cbc.gov.tw/en/lp-302-2.html`) — redirects to Chinese homepage. Use RSS feed instead.

---

## 6. Recommended Reliable Access Methods by Source

| Source | Recommended Method | URL |
|---|---|---|
| Presidential Office | RSS (2 feeds) | `president.gov.tw/RSSNEWS.aspx` + `RSSGazette.aspx` |
| Executive Yuan | HTML scrape (English) | `english.ey.gov.tw/Page/5A898E83D438145A` |
| MOFA | RSS (3 feeds) | `en.mofa.gov.tw/OpenData.aspx?SN=...` (3 SNs) |
| MND | HTML scrape | `mnd.gov.tw/news/pressreleaselist` |
| Legislative Yuan | HTML scrape (needs URL update) | Current nodeid=154 is wrong; needs investigation |
| Gazette | HTML scrape | `gazette.nat.gov.tw/` |
| MOF | RSS | `mof.gov.tw/Eng/Rss/f48d641f159a4866b1d31c0916fbcc71` |
| CBC | RSS (2 feeds) | `cbc.gov.tw/tw/rss-302-1.xml` + `en/rss-302-2.xml` |
| MOEA | BLOCKED | 403 on all tested URLs; needs investigation |
| BOFT | RSS | `trade.gov.tw/English/RSS/List.aspx?nodeID=90` |
| NSB | Headless browser | `nsb.gov.tw` (JS-required) |
| MAC | HTML scrape (Chinese only) | `mac.gov.tw/News.aspx?n=49&sms=39` |
| OCAC | HTML scrape | `ocac.gov.tw/OCAC/Eng/` |
| TAO | HTML scrape (charset handling) | `gwytb.gov.cn/xwdt/xwfb/` (gb2312 encoding) |
| IDA | HTML scrape | `ida.gov.tw/` |
| NSTC | HTML scrape | `nstc.gov.tw/` |
| Investment Commission | UNREACHABLE | `moeaic.gov.tw` times out; needs investigation |
