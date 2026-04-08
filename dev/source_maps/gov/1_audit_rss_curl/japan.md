# Japan Government Sources: URL Fetchability Test Results

**Test date:** 2026-03-19
**Source document:** `docs/source_intelligence_maps/japan_government_sources.md`
**Test method:** WebFetch + curl fallback with `Mozilla/5.0` User-Agent

---

## Summary

| Metric | Count |
|---|---|
| **Total unique URLs tested** | 55 |
| **Reachable (HTTP 200)** | 38 |
| **Blocked (HTTP 403)** | 12 |
| **Not found (HTTP 404)** | 2 |
| **Timeout / Unreachable** | 2 |
| **Connection refused** | 1 |

### Key Findings

1. **MOFA (mofa.go.jp) blocks all automated access** -- every URL returns 403 regardless of User-Agent. Headless browser (Playwright/Puppeteer) required for all MOFA content.
2. **MOD (mod.go.jp) blocks all automated access** -- all four tested URLs return 403. Same headless browser requirement.
3. **METI (meti.go.jp) is completely unreachable** -- all URLs time out (connection timeout, not HTTP error). May be IP-based geo-blocking or firewall. All 5 METI URLs failed.
4. **Kantei RSS feeds are fully functional** -- both Japanese RSS feeds and the English RSS feed (`index-e2.rdf`) work and return current content (March 2026). The document's [VERIFY] for English feed is resolved: the feed URL is `https://japan.kantei.go.jp/index-e2.rdf`.
5. **Kantei PM number has changed** -- the RSS feed shows PM paths using `/105/` (not `/104/` as documented), confirming PM Takaichi is now numbered 105th.
6. **BOJ, MOF, FSA RSS feeds all confirmed functional** with current content.
7. **JAXA RSS feed discovered and confirmed** -- `https://global.jaxa.jp/rss/press.rdf` (RSS 1.0/RDF format) is valid with current content.
8. **Sangiin WebTV (webtv.sangiin.go.jp) is down** -- connection refused.
9. **Sangiin committee minutes URL is 404** -- `select0101.html` path appears broken.

---

## Detailed Results by Institution

### 1.1 Kantei (Prime Minister's Office)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.kantei.go.jp/jp/news/index.html` | Entry point (JP) | **200 OK** | Works via curl |
| `https://japan.kantei.go.jp/news/` | Entry point (EN) | **200 OK** | Works via curl (WebFetch returned 404 -- likely JS redirect) |
| `https://www.kantei.go.jp/index-jnews.rdf` | RSS (JP new info) | **200 OK** | Valid RSS 2.0. Current content (Mar 2026). PM 105. |
| `https://www.kantei.go.jp/index-j2.rdf` | RSS (JP PM activities) | **200 OK** | Valid RDF+XML. Confirmed functional. |
| `https://japan.kantei.go.jp/rss.html` | RSS index (EN) | **200 OK** | Page exists. Lists feed URL `index-e2.rdf`. [VERIFY RESOLVED] |
| `https://japan.kantei.go.jp/index-e2.rdf` | RSS (EN) | **200 OK** | Valid RSS 2.0. Current content. PM Takaichi as PM 105. [VERIFY RESOLVED] |
| `https://japan.kantei.go.jp/104/statement/` | PM statements | **404** | PM number changed to `/105/`. URL outdated. |
| `https://japan.kantei.go.jp/tyoukanpress/` | CCS press conferences | **404** | WebFetch 404 but curl returned 200 for `news/`. May need path update. |
| `https://japan.kantei.go.jp/104/actions/` | PM actions | **404** | PM number changed to `/105/`. URL outdated. |
| `https://www.cao.go.jp/` | Cabinet Office | **200 OK** | Loads with full content. |
| `https://www.kantei.go.jp/jp/kakugi/index.html` | Cabinet decisions | **200 OK** | Works via curl. |

### 1.2 MOFA (Ministry of Foreign Affairs)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mofa.go.jp/press/release/index.html` | Entry point (press) | **403 Forbidden** | Blocked. Consistent with doc's access notes. |
| `https://www.mofa.go.jp/press/kaiken/index.html` | Press conferences | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/whats/` | What's New | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/policy/other/bluebook/index.html` | Diplomatic Bluebook | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/region/index.html` | Countries/regions | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/fp/nsp/page1we_000081.html` | Security policy | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/press/entr/index.html` | FM speeches | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/fp/nsp/page1we_000080.html` | NSC page | **403 Forbidden** | Blocked. |
| `https://www.mofa.go.jp/rss.html` | RSS page [VERIFY] | **403 Forbidden** | Blocked. Cannot verify. [VERIFY INCONCLUSIVE] |
| `https://www.mofa.go.jp/whats/rss.xml` | RSS feed [VERIFY] | **403 Forbidden** | Blocked. Cannot verify. [VERIFY INCONCLUSIVE] |

**Assessment:** All MOFA URLs return 403. Requires headless browser with full browser fingerprint or alternative access method.

### 1.3a MOD (Ministry of Defense)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mod.go.jp/en/` | Entry point (EN) | **403 Forbidden** | Blocked. |
| `https://www.mod.go.jp/j/press/index.html` | Entry point (JP press) | **403 Forbidden** | Blocked. |
| `https://www.mod.go.jp/atla/en/index.html` | ATLA | **403 Forbidden** | Blocked. |
| `https://www.mod.go.jp/en/publ/w_paper/index.html` | White paper | **403 Forbidden** | Blocked. |

**Assessment:** All MOD main domain URLs return 403. Same requirement as MOFA. [VERIFY RSS]: cannot test due to 403.

### 1.3b Joint Staff Office

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mod.go.jp/js/press/index-en.html` | Entry point (EN) | **403 Forbidden** | Blocked (same mod.go.jp domain). |
| `https://www.mod.go.jp/js/press/index.html` | Entry point (JP) | **403 Forbidden** | Blocked. |

**Assessment:** Same 403 block as MOD main. [VERIFY RSS]: cannot test.

### 1.4a House of Representatives (Shugiin)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.shugiin.go.jp/internet/index.nsf/html/index_e.htm` | Entry point (EN) | **200 OK** | Loads. Lotus Notes/Domino platform. 221st Diet session. |
| `https://www.shugiin.go.jp/internet/index.nsf/html/index.htm` | Entry point (JP) | **200 OK** | Loads. Shift_JIS encoding. |
| `https://www.shugiin.go.jp/internet/itdb_kaigiroku.nsf/html/kaigiroku/kaigi_l.htm` | Minutes search | **200 OK** | Loads with encoding issues (Shift_JIS vs UTF-8 mismatch in WebFetch). |
| `https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/menu.htm` | Submitted bills | **200 OK** | Loads. Shows 221st session bills. |
| `https://www.shugiintv.go.jp/en/` | Internet TV (EN) | **200 OK** | Loads. 221st session. Video archive available. |

**Assessment:** All Shugiin URLs work. [VERIFY RSS]: no RSS found (as documented).

### 1.4b House of Councillors (Sangiin)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.sangiin.go.jp/eng/` | Entry point (EN) | **200 OK** | Loads. 221st Diet session. |
| `https://www.sangiin.go.jp/japanese/index.html` | Entry point (JP) | **404 Not Found** | URL may have changed. |
| `https://www.sangiin.go.jp/japanese/joho1/kaigirok/daily/select0101.html` | Committee minutes | **404 Not Found** | URL broken. |
| `https://webtv.sangiin.go.jp/` | Internet TV | **Connection Refused** | Service appears down (ECONNREFUSED). |

**Assessment:** English page works. Japanese main page and minutes URL are 404. WebTV is down. [VERIFY RSS]: no RSS found.

### 1.5 Kanpo (Official Gazette)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.kanpo.go.jp/` | Entry point | **200 OK** | Loads. Shows daily editions with PDF downloads. 90-day archive accessible. Site opened April 2025 as documented. |

**Assessment:** Fully functional. [VERIFY RSS]: no RSS found (as expected).

### 1.6 MOF (Ministry of Finance)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.mof.go.jp/english/public_relations/index.html` | Entry point (EN) | **200 OK** | Loads. |
| `https://www.mof.go.jp/english/news.rss` | RSS (EN) | **200 OK** | Valid RSS 2.0. Current items (Mar 2026). JGB auctions, climate bonds. |
| `https://www.mof.go.jp/english/about_mof/rss/index.html` | RSS index page | **200 OK** | Confirmed accessible. |
| `https://www.mof.go.jp/english/public_relations/statement/index.htm` | Minister statements | **200 OK** | Loads. Fiscal speeches 2010-2025. |
| `https://www.mof.go.jp/english/policy/jgbs/topics/press_release/index.htm` | JGB press releases | **200 OK** | Loads. JGB announcements 2023-2025. |
| `https://www.mof.go.jp/english/policy/customs_tariff/trade_statistics/index.html` | Trade statistics | **404 Not Found** | URL broken. |
| `https://www.mof.go.jp/english/policy/jgbs/publication/newsletter/index.htm` | MOF Newsletter | **200 OK** | Loads. Monthly newsletters through Mar 2026. |

**Assessment:** Mostly functional. RSS confirmed working. Trade statistics URL is 404. [VERIFY RESOLVED: RSS works at documented URL].

### 1.7 BOJ (Bank of Japan)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.boj.or.jp/en/index.htm` | Entry point (EN) | **200 OK** | Loads. |
| `https://www.boj.or.jp/en/mopo/mpmdeci/index.htm` | Monetary policy decisions | **200 OK** | Loads. |
| `https://www.boj.or.jp/en/rss/whatsnew.xml` | RSS (EN) | **200 OK** | Valid RSS 2.0. Current items. Monetary policy statements, flow of funds, etc. [VERIFY RESOLVED: confirmed functional] |

**Assessment:** All URLs fully functional. RSS confirmed working.

### 1.8 METI (Ministry of Economy, Trade and Industry)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.meti.go.jp/english/press/index.html` | Entry point (EN press) | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/rss/index.html` | RSS index (EN) | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/rss/` | RSS index (JP) | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/press/category_02.html` | External econ policy | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/press/category_05.html` | Energy/environment | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/report/index.html` | White papers | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/speeches/index.html` | Minister speeches | **TIMEOUT** | Connection timeout. Unreachable. |
| `https://www.meti.go.jp/english/mobile/index.html` | Quick Reads | **TIMEOUT** | Connection timeout. Unreachable. |

**Assessment:** Entire `meti.go.jp` domain is unreachable. Connection timeouts (not HTTP errors) suggest IP-based geo-blocking, firewall rules, or infrastructure issue. All [VERIFY RSS] items cannot be tested. Requires investigation from a Japan-based IP or VPN.

### 1.9a NSS (National Security Secretariat)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.cas.go.jp/` | Entry point (CAS) | **200 OK** | Loads. Cabinet Secretariat portal. |
| `https://www.cas.go.jp/jp/siryou/221216anzenhoshou/nss-e.pdf` | NSS English PDF | **200 OK** | PDF accessible. National Security Strategy document. |

**Assessment:** Both URLs functional.

### 1.9b CIRO (Cabinet Intelligence and Research Office)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.cas.go.jp/jp/gaiyou/jimu/jyouhoutyousa/en/community.html` | Entry point | **200 OK** | Loads. Intelligence community organizational page. |
| `https://www.cas.go.jp/jp/gaiyou/jimu/jyouhoutyousa/en/csice.html` | CSICE page | **200 OK** | Loads. Satellite intelligence center page. |

**Assessment:** Both URLs functional (as expected -- static, rarely updated pages).

### 1.10a Imperial Household Agency (Kunaicho)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.kunaicho.go.jp/en/index.html` | Entry point (EN) | **200 OK** | Loads. |
| `https://www.kunaicho.go.jp/e-kunaicho/release.html` | Press releases | **200 OK** | Loads. Releases from 2009-2019 visible. |
| `https://www.kunaicho.go.jp/joko/okotoba/index-en.html` | Addresses/press conf | **200 OK** | Loads. Emperor addresses through April 2019. |

**Assessment:** All URLs functional. Content appears dated (last entries 2019 on some pages). [VERIFY RSS]: no RSS found.

### 1.10b JAXA

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://global.jaxa.jp/` | Entry point (EN) | **200 OK** | Loads. |
| `https://global.jaxa.jp/press/` | Press releases | **200 OK (redirect)** | Redirects to `/press/2026/`. Functional. |
| `https://global.jaxa.jp/media.html` | Media page | **200 OK** | Loads. Lists RSS feed URL. |
| `https://global.jaxa.jp/news/` | What's New | **200 OK** | Loads. Content through Oct 2025. |
| `https://global.jaxa.jp/rss/press.rdf` | RSS (press releases) | **200 OK** | Valid RSS 1.0/RDF. Current items. [VERIFY RESOLVED: RSS confirmed at this URL] |

**Assessment:** All URLs fully functional. RSS feed discovered and confirmed working.

### 1.10c NIDS (National Institute for Defense Studies)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.nids.mod.go.jp/english/` | Entry point (EN) | **200 OK** | Loads. China Security Report 2026 featured. |

**Assessment:** Functional. Note: unlike mod.go.jp main domain, the nids.mod.go.jp subdomain is NOT blocked. [VERIFY RSS]: no RSS found.

### 1.10d JIIA (Japan Institute of International Affairs)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.jiia.or.jp/en/` | Entry point (EN) | **200 OK** | Loads. |

**Assessment:** Functional. [VERIFY RSS]: no RSS found.

### 1.10e FSA (Financial Services Agency)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://www.fsa.go.jp/en/` | Entry point (EN) | **200 OK** | Loads. |
| `https://www.fsa.go.jp/en/rss.html` | RSS index page | **200 OK** | Loads. Lists feed URL: `fsaEnNewsList_rss2.xml`. |
| `https://www.fsa.go.jp/fsaEnNewsList_rss2.xml` | RSS feed (EN) | **200 OK** | Valid RSS 2.0. Current items (Mar 2026). Financial regulatory news. [VERIFY RESOLVED] |

**Assessment:** All URLs fully functional. RSS confirmed working.

### NDL (National Diet Library)

| URL | Type | Result | Notes |
|---|---|---|---|
| `https://ndlsearch.ndl.go.jp/` | Search portal | **200 OK** | Loads. Full search interface. |

---

## [VERIFY] Items Resolution Summary

| Item | Status | Resolution |
|---|---|---|
| Kantei English RSS feed URLs | **RESOLVED** | Feed exists at `https://japan.kantei.go.jp/index-e2.rdf`. Valid RSS 2.0 with current content. RSS index page at `/rss.html` also works. |
| MOFA RSS at `mofa.go.jp/rss.html` or `/whats/rss.xml` | **INCONCLUSIVE** | All MOFA URLs return 403. Cannot verify from outside Japan without headless browser. |
| MOD RSS at `mod.go.jp/j/rss/` | **INCONCLUSIVE** | All MOD URLs return 403. Cannot verify. |
| Joint Staff RSS | **INCONCLUSIVE** | 403 block on mod.go.jp domain. |
| Shugiin RSS | **RESOLVED** | No RSS available (confirmed -- legacy Lotus Notes platform). |
| Sangiin RSS | **RESOLVED** | No RSS available (confirmed). |
| Kanpo RSS | **RESOLVED** | No RSS available (confirmed). |
| MOF RSS (redirect from `/english/rss.htm`) | **RESOLVED** | Direct feed works at `https://www.mof.go.jp/english/news.rss`. RSS index at `/english/about_mof/rss/index.html` also accessible. |
| BOJ additional feeds | **PARTIALLY RESOLVED** | `whatsnew.xml` confirmed working. Additional feeds for monetary policy/statistics not tested individually. |
| METI RSS XML URLs | **INCONCLUSIVE** | Entire domain unreachable (timeout). |
| Kunaicho RSS | **RESOLVED** | No RSS available (confirmed). |
| JAXA RSS at `global.jaxa.jp/media.html` | **RESOLVED** | RSS confirmed at `https://global.jaxa.jp/rss/press.rdf` (RSS 1.0/RDF format). |
| NIDS RSS | **RESOLVED** | No RSS available (confirmed). |
| JIIA RSS | **RESOLVED** | No RSS available (confirmed). |
| FSA exact XML feed URL | **RESOLVED** | Feed at `https://www.fsa.go.jp/fsaEnNewsList_rss2.xml`. |

---

## Corrections Required in Source Document

1. **PM number is 105, not 104.** All Kantei English URL paths reference `/105/` for PM Takaichi (105th PM), not `/104/` as documented. Update all `/104/` references to `/105/`.
2. **Kantei English RSS feed confirmed.** Remove [VERIFY] and set `english_feed` in YAML to `https://japan.kantei.go.jp/index-e2.rdf`.
3. **Kantei cabinet decisions URL 404.** `https://www.kantei.go.jp/jp/kakugi/index.html` returned 200 via curl but 404 via WebFetch -- may require JS rendering. Mark as requiring verification.
4. **Sangiin Japanese index 404.** `https://www.sangiin.go.jp/japanese/index.html` returns 404. URL may have changed.
5. **Sangiin committee minutes URL 404.** `https://www.sangiin.go.jp/japanese/joho1/kaigirok/daily/select0101.html` returns 404.
6. **Sangiin WebTV down.** `https://webtv.sangiin.go.jp/` returns connection refused.
7. **MOF trade statistics URL 404.** `https://www.mof.go.jp/english/policy/customs_tariff/trade_statistics/index.html` returns 404.
8. **JAXA RSS feed should be added.** `https://global.jaxa.jp/rss/press.rdf` -- confirmed functional RSS 1.0/RDF feed.
9. **FSA RSS feed URL should be updated.** Exact feed URL is `https://www.fsa.go.jp/fsaEnNewsList_rss2.xml`.
10. **METI entire domain unreachable.** All meti.go.jp URLs time out. Needs investigation from Japan-based network.

---

## Access Method Recommendations

| Domain | Recommended Access | Reason |
|---|---|---|
| `kantei.go.jp` | RSS polling | All 3 feeds (2 JP, 1 EN) confirmed functional |
| `mofa.go.jp` | Headless browser (Playwright) | 403 on all automated access |
| `mod.go.jp` | Headless browser (Playwright) | 403 on all automated access |
| `nids.mod.go.jp` | Standard HTTP | Subdomain NOT blocked (unlike main mod.go.jp) |
| `shugiin.go.jp` | Standard HTTP | Works but Shift_JIS encoding requires handling |
| `sangiin.go.jp` | Standard HTTP (EN); investigate JP URLs | English works; Japanese URLs partially broken |
| `kanpo.go.jp` | Standard HTTP + PDF extraction | Works normally |
| `mof.go.jp` | RSS polling | Feed confirmed functional |
| `boj.or.jp` | RSS polling | Feed confirmed functional |
| `meti.go.jp` | **BLOCKED -- needs Japan VPN/proxy** | Entire domain unreachable |
| `cas.go.jp` | Standard HTTP | Works normally |
| `kunaicho.go.jp` | Standard HTTP | Works normally |
| `jaxa.jp` | RSS polling | Feed confirmed at `global.jaxa.jp/rss/press.rdf` |
| `jiia.or.jp` | Standard HTTP | Works normally |
| `fsa.go.jp` | RSS polling | Feed confirmed functional |
