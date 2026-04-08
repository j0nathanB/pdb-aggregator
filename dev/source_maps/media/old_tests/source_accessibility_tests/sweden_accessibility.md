# Accessibility Test Results: SWEDEN

**Sources tested:** 17

## Summary

| Metric | Count | Rate |
|---|---|---|
| Homepage reachable | 15 / 17 | 88% |
| Article fetchable | 8 / 17 | 47% |
| Full text extractable | 6 / 17 | 35% |
| RSS available | 11 / 17 | 65% |
| RSS full text | 3 / 17 | 18% |

---

## Per-Source Results

### 1. ✅ Sveriges Television (SVT)

| Field | Result |
|---|---|
| **Domain** | `svt.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.svt.se/nyheter/utrikes/lakare-utan-granser-kravs-mer-an-att-rafah-overgangen-oppnas |
| **Publication date** | 2026-03-17 |
| **RSS available** | Yes |
| **RSS URL** | https://www.svt.se/rss.xml |
| **RSS full text** | No |
| **Notes** | Free public broadcaster. Homepage and articles accessible. RSS provides summaries only (title + description). Also has /nyheter/rss.xml feed. |

**First paragraph excerpt:** Jon Gunnarsson Ruthman från Läkare utan gränser säger att öppnandet av gränsövergången i Rafah bara skulle få ett "symboliskt" värde.

### 2. Sveriges Radio (SR)

| Field | Result |
|---|---|
| **Domain** | `sverigesradio.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.sverigesradio.se/artikel/forsvarsmakten-agerar-efter-dodsfall-i-lumpen |
| **Publication date** | 2026-03-16 |
| **RSS available** | Yes |
| **RSS URL** | https://api.sr.se/api/rss/program/4540 |
| **RSS full text** | No |
| **Notes** | Free public broadcaster. Article text extractable from server-rendered HTML. RSS via API (Atom format for Ekot/news); summaries only. |

**First paragraph excerpt:** Generalläkare Claes Ivgren om utmaningen att få soldater att prata om psykisk ohälsa.

### 3. ✅ Dagens Nyheter (DN)

| Field | Result |
|---|---|
| **Domain** | `dn.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://www.dn.se/varlden/vance-bryter-tystnad-om-attacken-vi-har-en-smart-president/ |
| **Publication date** | 2026-03-16 |
| **RSS available** | Yes |
| **RSS URL** | https://www.dn.se/rss/ |
| **RSS full text** | No |
| **Notes** | Paywalled. Article page loads but body content is behind paywall or JS-rendered. RSS has titles and short descriptions. Date extractable from structured data. |

### 4. ✅ Svenska Dagbladet (SvD)

| Field | Result |
|---|---|
| **Domain** | `svd.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://www.svd.se/a/zOA3GO/israel-i-nya-attacker-mot-beirut |
| **Publication date** | 2026-03-17 |
| **RSS available** | Yes |
| **RSS URL** | https://www.svd.se/feed/articles.rss |
| **RSS full text** | No |
| **Notes** | Paywalled. Article page loads but body content behind paywall. RSS provides headlines with short description snippets. Dates available in RSS and structured data. |

### 5. Aftonbladet

| Field | Result |
|---|---|
| **Domain** | `aftonbladet.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/ |
| **RSS full text** | Yes |
| **Notes** | Homepage JS-rendered; article links not extractable from static HTML. RSS feed works well with HTML content in descriptions (full text). Best extraction path is via RSS. |

### 6. Expressen

| Field | Result |
|---|---|
| **Domain** | `expressen.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **Test article** | https://www.expressen.se/nyheter/varlden/skrev-bok-om-makens--dod-doms-for-mordet/ |
| **RSS available** | Yes |
| **RSS URL** | https://expressen.se/rss/nyheter |
| **RSS full text** | Yes |
| **Notes** | Homepage returned HTTP 200 in earlier tests but curl_status intermittently timed out. RSS feed works and contains HTML descriptions with article summaries. Article pages are JS-rendered. |

### 7. Dagens Industri (DI)

| Field | Result |
|---|---|
| **Domain** | `di.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://di.se/rss |
| **RSS full text** | No |
| **Notes** | Paywalled financial daily. Homepage JS-rendered; no article links extractable from static HTML. RSS provides headlines and short summaries. |

### 8. Omni

| Field | Result |
|---|---|
| **Domain** | `omni.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Fully JS-rendered (Next.js). No article links extractable from static HTML. No RSS feed found. Aggregator model may require API or headless browser. |

### 9. Goteborgs-Posten

| Field | Result |
|---|---|
| **Domain** | `gp.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.gp.se/sport/fotboll/bk-hacken |
| **RSS available** | Yes |
| **RSS URL** | https://www.gp.se/rss |
| **RSS full text** | No |
| **Notes** | Partially paywalled. Homepage serves HTML with links. RSS at /rss returns valid feed (compressed). Podcast RSS also detected. Some article content extractable. |

**First paragraph excerpt:** Ikon direktflöde GP Direkt Ikon bokmärke Sparat Ikon följ Följer Meny Nyheter Göteborg...

### 10. Sydsvenskan

| Field | Result |
|---|---|
| **Domain** | `sydsvenskan.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://www.sydsvenskan.se/feeds/feed.xml |
| **RSS full text** | No |
| **Notes** | Paywalled (Bonnier). Homepage JS-rendered; article links not extractable from static HTML. RSS feed provides headlines and short descriptions only. |

### 11. Fokus

| Field | Result |
|---|---|
| **Domain** | `fokus.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.fokus.se/kultur/bokrecension/var-ar-brzezinski-nar-vi-behover-honom/ |
| **Publication date** | 2026-03-15 |
| **RSS available** | Yes |
| **RSS URL** | https://fokus.se/rss |
| **RSS full text** | Yes |
| **Notes** | Paywalled weekly magazine but some content accessible. Article pages render server-side with extractable paragraphs. RSS at /rss has full-text content. |

**First paragraph excerpt:** Prenumerera Logga in Mina sidor Aktuellt Veckans Fokus Krönikor Kultur Sticket Fackklubben...

### 12. Kvartal

| Field | Result |
|---|---|
| **Domain** | `kvartal.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Fully JS-rendered (Next.js). No article links extractable from static HTML. No RSS feed found. Would require headless browser for extraction. |

### 13. Altinget Sverige

| Field | Result |
|---|---|
| **Domain** | `altinget.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://altinget.se/rss |
| **RSS full text** | No |
| **Notes** | Free registration required for some content. Homepage JS-rendered. RSS provides headlines and short descriptions. Extraction best via RSS. |

### 14. ✅ Riksdag Official

| Field | Result |
|---|---|
| **Domain** | `riksdagen.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.riksdagen.se/sv/aktuellt/val-till-riksdagen/ |
| **RSS available** | No |
| **Notes** | Free government site. Server-rendered HTML with extractable content. No RSS feed found. Has open data API (riksdagen.se/sv/oppna-data/) for structured parliamentary data. |

**First paragraph excerpt:** Sök Aktuellt Val till riksdagen Dokument & lagar...

### 15. ✅ Regeringskansliet

| Field | Result |
|---|---|
| **Domain** | `government.se` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | HTTP 403 - blocks automated requests (curl/bots). Would need browser-based scraping or API access. No RSS feed found at standard paths. |

### 16. FOI

| Field | Result |
|---|---|
| **Domain** | `foi.se` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Connection timed out on all attempts. Site may block non-browser traffic or use DDoS protection. Would need browser-based scraping. |

### 17. UI

| Field | Result |
|---|---|
| **Domain** | `ui.se` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.ui.se/evenemang/kommande/vad-star-pa-spel-i-arktis/ |
| **RSS available** | No |
| **Notes** | Free think tank site. Server-rendered HTML with extractable content. No RSS feed found. Publication pages accessible. |

**First paragraph excerpt:** Betydelsen av Arktisregionen för Europas säkerhet har ökat väsentligt på senare år.
