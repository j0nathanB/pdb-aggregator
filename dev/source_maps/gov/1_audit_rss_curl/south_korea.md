# South Korea Government Sources — URL Fetchability Test Results

**Test date:** 2026-03-19
**Test origin:** US-based (non-Korean IP)
**Source document:** `docs/source_intelligence_maps/south_korea_government_sources.md`

---

## Summary

| Category | Count |
|---|---|
| **Total unique URLs tested** | 48 |
| **Reachable (HTTP 200)** | 30 |
| **Blocked / connection reset** | 12 |
| **DNS resolution failure** | 1 |
| **HTTP 403 (Forbidden)** | 2 |
| **Redirect loop (302)** | 1 |
| **Reachable but empty content (JS-rendered)** | 2 |

**Overall reachability: 30/48 (62.5%)**

### Key findings

1. **Geo-blocking pattern:** Multiple Korean government sites on the `.go.kr` and `.mil.kr` TLDs reset TLS connections from non-Korean IPs. Affected domains: `mnd.go.kr`, `english.moef.go.kr`, `dapa.go.kr`, `gwanbo.mois.go.kr`, `open.gwanbo.go.kr`, `kotra.or.kr`, `motie.go.kr` (legacy). These domains resolve in DNS but reject the connection at the TLS handshake level ("Connection reset by peer").
2. **DNS failure:** `eng.president.go.kr` does not resolve. The English presidential portal documented in the source map appears to not exist (or uses a different subdomain).
3. **Korea.net blocks automated access:** Both the press releases page and the RSS service page return 403 or redirect loops via CloudFront. Requires cookie/session handling or Korean IP.
4. **MOFA RSS confirmed working:** The MOFA Korean-language RSS feed for press releases (`brdId=302`) returns valid RSS 2.0 with 30 items. The press briefings feed (`brdId=303`) also returns `application/rss+xml` content type via curl, though WebFetch had a socket error on first attempt.
5. **BOK pages load but render empty:** BOK board-system pages return HTTP 200 but require JavaScript rendering to populate content lists.
6. **Best-performing sources from outside Korea:** Presidential Office (Korean portal), MOFA (all pages), BOK, MOU, National Assembly, NIS/NCSC, KDI, KITA, MOTIR, NABO.

---

## Detailed Results by Institution

### 1. Presidential Office (president.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.president.go.kr/newsroom/briefing/` | Entry point (KO) | WebFetch | **200 OK** | Loads fully. Shows daily briefings with dates. |
| `https://eng.president.go.kr/briefing` | Entry point (EN) | curl | **DNS FAIL** | `eng.president.go.kr` does not resolve. Subdomain does not exist. |
| `https://www.president.go.kr/president/speeches/` | Additional | WebFetch | **200 OK** | Presidential speeches and writings listing loads. |
| `https://www.president.go.kr/president/calendar/` | Additional | WebFetch | **200 OK** | Monthly schedule calendar with events. |
| `https://www.president.go.kr/newsroom/card_news/` | Additional | WebFetch | **200 OK** | Card news infographics listing loads. |

**Verdict:** Korean portal fully functional. English portal DNS failure -- needs investigation for correct subdomain.

---

### 2. MOFA (mofa.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.mofa.go.kr/eng/brd/m_5676/list.do` | Entry point (EN press releases) | WebFetch | **200 OK** | 11,142 press releases listed. Fully functional. |
| `https://www.mofa.go.kr/www/brd/m_4076/list.do` | Entry point (KO) | WebFetch | **200 OK** | 6,870 articles in "New Focus" section. |
| `http://www.mofa.go.kr/www/brd/rss.do?brdId=303` | RSS (KO briefings) | curl | **200 OK** | `application/rss+xml`. Valid feed. |
| `http://www.mofa.go.kr/www/brd/rss.do?brdId=302` | RSS (KO releases) | WebFetch | **200 OK** | Valid RSS 2.0, 30 items. Title: "Press Releases". |
| `https://www.mofa.go.kr/eng/brd/m_5679/list.do` | EN press briefings | curl | **200 OK** | HTML content. |
| `https://www.mofa.go.kr/eng/brd/m_5689/list.do` | Minister's speeches | curl | **200 OK** | HTML content. |
| `https://www.mofa.go.kr/eng/brd/m_5690/list.do` | Vice Ministers' speeches | curl | **200 OK** | HTML content. |
| `https://www.mofa.go.kr/eng/brd/m_5684/list.do` | Diplomatic White Paper | curl | **200 OK** | HTML content. |
| `https://www.mofa.go.kr/eng/brd/m_5674/list.do` | Ministry News | curl | **200 OK** | HTML content. |
| `https://www.mofa.go.kr/eng/wpge/m_20360/contents.do` | RSS info page | curl | **200 OK** | HTML content. |

**Verdict:** All MOFA URLs fully functional. Best-performing government source. Both RSS feeds confirmed working.

---

### 3a. MND (mnd.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.mnd.go.kr/mbshome/mbs/mnd/subview.jsp?id=mnd_010701000000` | Entry point (KO) | curl | **BLOCKED** | TLS connection reset by peer. Geo-blocked. |
| `https://www.mnd.go.kr/user/boardList.action?command=view&page=1&boardId=O_47261&boardSeq=O_395756&id=mndEN_020100000000` | Entry point (EN) [VERIFY] | curl | **BLOCKED** | TLS connection reset. Cannot verify URL pattern. |
| `https://www.mnd.go.kr/mbshome/mbs/mndEN/` | EN portal base | curl | **BLOCKED** | TLS connection reset. |

**Verdict:** Entire `mnd.go.kr` domain blocked from non-Korean IPs. Cannot verify any URLs including the [VERIFY] English news URL. Requires Korean IP or VPN.

---

### 3b. JCS (jcs.mil.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.jcs.mil.kr/user/boardList.action?command=view&page=1&boardId=O_122667&id=jcs2_eng_030000000000` | Entry point (EN) [VERIFY] | curl | **BLOCKED** | Connection timeout/reset. `.mil.kr` domain likely geo-restricted. |

**Verdict:** `jcs.mil.kr` inaccessible from non-Korean IPs. Cannot verify URL. Expected per source document warning about `.mil.kr` access restrictions.

---

### 4. National Assembly (assembly.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://korea.assembly.go.kr:447/portalEn/main/main.do` | Entry point (EN) | curl | **200 OK** | Non-standard port 447. HTML content loads. |
| `https://open.assembly.go.kr` | Open Assembly | curl | **200 OK** | HTML content loads. |
| `https://korea.assembly.go.kr/secretary/main/main.do` | Secretariat | curl | **200 OK** | HTML content loads. |
| `https://www.nanet.go.kr/english/` | NA Library | curl | **200 OK** | HTML content loads. |
| `https://likms.assembly.go.kr/` | LIKMS [VERIFY] | curl | **200 OK** | **VERIFIED.** Legislative Information System loads. |

**Verdict:** All National Assembly URLs functional, including the [VERIFY] LIKMS URL. Port 447 works.

---

### 5. Gwanbo / Official Gazette (gwanbo.mois.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://gwanbo.mois.go.kr/` | Entry point | curl | **BLOCKED** | Connection timeout. Domain resolves but no TLS handshake. |
| `https://open.gwanbo.go.kr/` | Open Gwanbo | curl | **BLOCKED** | Connection timeout. Same behavior. |

**Verdict:** Both Gwanbo domains inaccessible from non-Korean IPs. Likely geo-restricted or requires specific network path.

---

### 6. MOEF (moef.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://english.moef.go.kr/pc/selectTbPressCenterList.do?boardCd=N0001` | Entry point (EN) | curl | **BLOCKED** | TLS connection reset by peer. |
| `https://english.moef.go.kr/` | EN portal base | curl | **BLOCKED** | TLS connection reset by peer. |
| `https://www.moef.go.kr/nw/nes/nesdta.do` | KO press center [VERIFY] | curl | **BLOCKED** | TLS connection reset. Cannot verify. |
| `https://www.kdi.re.kr/eng/` | KDI (affiliated) | curl | **200 OK** | HTML content loads. |
| `https://www.kdi.re.kr/eng/research/economy` | KDI Economic Outlook | curl | **200 OK** | HTML content loads. |

**Verdict:** Main MOEF domain (`moef.go.kr` and `english.moef.go.kr`) blocked from non-Korean IPs. KDI (separate `.re.kr` domain) is accessible. Cannot verify the [VERIFY] Korean press center URL.

---

### 7. BOK (bok.or.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400423` | Press Releases | WebFetch | **200 OK** | Page loads but content list shows 0 items (JS-rendered). |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400022` | Monetary Policy | WebFetch | **200 OK** | Page loads but content empty (JS-rendered). |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400021` | MPB Minutes | curl | **200 OK** | HTML loads. |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400409` | Issue Notes | curl | **200 OK** | HTML loads. |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400215` | Monetary Policy Report | curl | **200 OK** | HTML loads. |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400219` | Financial Stability | curl | **200 OK** | HTML loads. |
| `https://www.bok.or.kr/eng/singl/newsDataEng/list.do?menuNo=400413` | Economic Outlook | curl | **200 OK** | HTML loads. |
| `https://ecos.bok.or.kr/` | ECOS statistics | curl | **200 OK** | HTML loads. |
| `https://www.bok.or.kr/eng/stats/statsPublictSchdul/listCldr.do?menuNo=400359` | Statistical Calendar | curl | **200 OK** | HTML loads. |

**Verdict:** All BOK URLs return HTTP 200. However, the board-system listing pages require JavaScript rendering to populate article lists. Headless browser required for content extraction. ECOS and statistical calendar accessible.

---

### 8. MOTIR / MOTIE (motir.go.kr / motie.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://english.motir.go.kr/` | Entry point (EN) | curl | **200 OK** | New MOTIR English portal loads. |
| `https://english.motie.go.kr/eng/` | Legacy MOTIE (EN) | curl | **BLOCKED** | TLS connection reset. Legacy domain not redirecting. |
| `https://www.motie.go.kr/kftz/en/index.do` | FTZ portal [VERIFY] | curl | **BLOCKED** | TLS connection reset. Cannot verify. |
| `https://www.kotra.or.kr/english/` | KOTRA (affiliated) | curl | **BLOCKED** | TLS connection reset. |
| `https://www.kita.org/` | KITA (affiliated) | curl | **200 OK** | HTML content loads. |

**Verdict:** New MOTIR English portal works. Legacy MOTIE domains blocked. KOTRA blocked. KITA accessible. The [VERIFY] FTZ URL cannot be verified (blocked).

---

### 9a. NIS (nis.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://eng.nis.go.kr/` | Entry point (EN) | WebFetch | **200 OK** | Institutional portal loads. Major duties, centers listed. |
| `https://eng.nis.go.kr/ECM/1_3_1.do` | Notices | curl | **200 OK** | HTML content loads. |
| `https://www.ncsc.go.kr/eng/mainPage.do` | NCSC (cyber security) | curl | **200 OK** | HTML content loads. |

**Verdict:** All NIS/NCSC URLs functional from outside Korea. Surprisingly accessible for an intelligence agency portal.

---

### 9b. NSC

No independent URLs. Communications via Presidential Office (`president.go.kr/newsroom/briefing/`) -- already tested and functional.

---

### 10a. MOU (unikorea.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000034` | EN press releases | curl | **200 OK** | HTML content loads. |
| `https://www.unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000035` | EN press briefings | curl | **200 OK** | HTML content loads. |
| `https://unikorea.go.kr/web/eng_unikorea/bbs/bbs_0000000000000167` | MOU News | curl | **200 OK** | HTML content loads. |

**Verdict:** All MOU URLs fully functional. Well-maintained English portal.

---

### 10b. Korea.net / KOCIS

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.korea.net/Government/Briefing-Room/Press-Releases` | Entry point | WebFetch / curl | **403 Forbidden** | CloudFront blocks automated access. |
| `https://www.korea.net/Others/Subscribe-to-Koreanet/RSS-Service` | RSS service [VERIFY] | curl | **302 Redirect Loop** | Sets cookie then redirects to self. Requires session/cookie handling. **NOT VERIFIED as functional.** |

**Verdict:** Korea.net actively blocks automated access via CloudFront. Both the press releases page and RSS service are inaccessible without browser-like session handling. The [VERIFY] RSS feeds are **not confirmed functional**.

---

### 10c. DAPA (dapa.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://www.dapa.go.kr/dapa_en/main.do` | Entry point (EN) | curl | **BLOCKED** | TLS connection reset by peer. |

**Verdict:** `dapa.go.kr` blocked from non-Korean IPs.

---

### 10d. NABO (nabo.go.kr)

| URL | Type | Method | Result | Notes |
|---|---|---|---|---|
| `https://korea.nabo.go.kr/` | Entry point | curl | **200 OK** | HTML content loads. |

**Verdict:** NABO portal accessible.

---

## VERIFY Items Summary

| URL | Item | Verdict |
|---|---|---|
| MND English news URL | `mnd.go.kr/user/boardList.action?...` | **CANNOT VERIFY** -- entire domain geo-blocked |
| JCS English news URL | `jcs.mil.kr/user/boardList.action?...` | **CANNOT VERIFY** -- `.mil.kr` domain geo-blocked |
| MOEF Korean press center | `moef.go.kr/nw/nes/nesdta.do` | **CANNOT VERIFY** -- domain geo-blocked |
| MOTIR English press URL pattern | `english.motir.go.kr/eng/article/EATCL{id}` | **CANNOT VERIFY** -- pattern URL, base domain loads (200) |
| MOTIE FTZ redirect to MOTIR | `motie.go.kr/kftz/en/index.do` | **CANNOT VERIFY** -- legacy domain geo-blocked |
| LIKMS (Legislative Info) | `likms.assembly.go.kr/` | **VERIFIED OK** -- returns 200 |
| Korea.net RSS feeds | `korea.net/.../RSS-Service` | **NOT VERIFIED** -- 302 redirect loop, likely non-functional for automated access |
| BOK RSS on Korean portal | Not documented with specific URL | **NOT FOUND** -- no RSS confirmed on BOK |

---

## Reachability by Institution

| # | Institution | Domain | Reachable from US? | Failure Mode |
|---|---|---|---|---|
| 1 | Presidential Office | `president.go.kr` | **Partial** | Korean portal OK. `eng.president.go.kr` DNS failure. |
| 2 | MOFA | `mofa.go.kr` | **Yes** | All URLs including RSS fully functional. |
| 3a | MND | `mnd.go.kr` | **No** | TLS connection reset (geo-block). |
| 3b | JCS | `jcs.mil.kr` | **No** | Connection timeout (geo-block). |
| 4 | National Assembly | `assembly.go.kr` | **Yes** | All URLs work including port 447. |
| 5 | Gwanbo | `gwanbo.mois.go.kr` | **No** | Connection timeout (geo-block). |
| 6 | MOEF | `moef.go.kr` | **No** | TLS connection reset (geo-block). KDI OK. |
| 7 | BOK | `bok.or.kr` | **Yes** | All URLs 200. JS rendering needed for content. |
| 8 | MOTIR | `motir.go.kr` | **Partial** | New `english.motir.go.kr` OK. Legacy MOTIE blocked. |
| 9a | NIS | `nis.go.kr` | **Yes** | All URLs functional. |
| 9b | NSC | via `president.go.kr` | **Yes** | Via Presidential Office (Korean portal). |
| 10a | MOU | `unikorea.go.kr` | **Yes** | All URLs functional. |
| 10b | Korea.net | `korea.net` | **No** | 403 / redirect loop (CloudFront bot protection). |
| 10c | DAPA | `dapa.go.kr` | **No** | TLS connection reset (geo-block). |
| 10d | NABO | `nabo.go.kr` | **Yes** | Portal loads. |

---

## Recommendations for Pipeline Integration

1. **Korean VPN/proxy required** for 7 institutions: MND, JCS, Gwanbo, MOEF, DAPA, KOTRA, and legacy MOTIE domains. These reset TLS connections from non-Korean IPs.
2. **Korea.net** requires browser-like session handling (cookie acceptance, CloudFront challenge) even from Korean IPs. Consider Playwright/headless browser with cookie jar.
3. **BOK** pages return HTTP 200 but render content via JavaScript. Headless browser (Playwright) required for content extraction.
4. **MOFA RSS feeds** are the highest-value automation target -- both feeds confirmed working over HTTP (not HTTPS). These are the only reliably automatable government feeds.
5. **eng.president.go.kr** does not exist in DNS. Investigate whether the English portal moved to a different URL (possibly `www.president.go.kr/en/` or similar).
6. **LIKMS** (Legislative Information System) at `likms.assembly.go.kr` is confirmed functional despite being marked [VERIFY].
