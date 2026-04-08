# Accessibility Test Results: LATVIA

**Sources tested:** 17

## Summary

| Metric | Count | Rate |
|---|---|---|
| Homepage reachable | 15 / 17 | 88% |
| Article fetchable | 10 / 17 | 59% |
| Full text extractable | 9 / 17 | 53% |
| RSS available | 11 / 17 | 65% |
| RSS full text | 9 / 17 | 53% |

---

## Per-Source Results

### 1. ✅ LSM

| Field | Result |
|---|---|
| **Domain** | `lsm.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.lsm.lv/raksts/kas-notiek-latvija/raksti/par-kas-notiek-latvija.a428255/ |
| **Publication date** | 2021-10-19 |
| **RSS available** | Yes |
| **RSS URL** | https://lsm.lv/rss |
| **RSS full text** | Yes |
| **Notes** | Free public media. Server-rendered HTML with extractable content. RSS at /rss provides full-text content. English service at eng.lsm.lv. Both HTML and RSS extraction viable. |

**First paragraph excerpt:** Svarīgi Krievijas iebrukums Ukrainā Karš Tuvajos Austrumos...

### 2. ✅ Delfi Latvia

| Field | Result |
|---|---|
| **Domain** | `delfi.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://delfi.lv/rss.xml |
| **RSS full text** | Yes |
| **Notes** | Free with ads. Homepage JS-rendered; article links not extractable from static HTML. RSS at /rss.xml provides full-text content - best extraction path. Russian version at rus.delfi.lv. |

### 3. ✅ TVNET

| Field | Result |
|---|---|
| **Domain** | `tvnet.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://www.tvnet.lv/term/555447/irana |
| **Publication date** | 2026-03-16 |
| **RSS available** | Yes |
| **RSS URL** | https://www.tvnet.lv/rss |
| **RSS full text** | Yes |
| **Notes** | Free with ads. Article pages load but body content is JS-rendered. RSS at /rss provides full-text content - best extraction path. Date extractable from structured data. |

### 4. Diena

| Field | Result |
|---|---|
| **Domain** | `diena.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.diena.lv/eveikals/prece/nakama-pietura/802270/ |
| **RSS available** | Yes |
| **RSS URL** | https://diena.lv/rss |
| **RSS full text** | No |
| **Notes** | Partially paywalled. Server-rendered HTML with extractable content on accessible pages. RSS at /rss provides headlines and summaries. |

**First paragraph excerpt:** Klajā nākusi dzejnieces un publicistes Andas Līces jaunākā grāmata, eseju krājums "Nākamā pietura".

### 5. NRA

| Field | Result |
|---|---|
| **Domain** | `nra.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://nra.lv/latvija/riga/516473-slegs-tirdzniecibas-cetru-mols.htm |
| **Publication date** | 2026-03-16 |
| **RSS available** | Yes |
| **RSS URL** | https://nra.lv/rss/jaunakas-zinas/ |
| **RSS full text** | Yes |
| **Notes** | Partially paywalled nationalist-conservative daily. Server-rendered HTML with extractable content. RSS at /rss/jaunakas-zinas/ provides full-text content. |

**First paragraph excerpt:** Otrdiena, 17.marts...

### 6. Latvijas Avize

| Field | Result |
|---|---|
| **Domain** | `la.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://la.lv/feed |
| **RSS full text** | Yes |
| **Notes** | Partially paywalled. Homepage JS-rendered; article links not extractable from static HTML. RSS (WordPress feed) at /feed provides full-text content - best extraction path. |

### 7. IR

| Field | Result |
|---|---|
| **Domain** | `ir.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://ir.lv/izdevums/ir/jaunakais |
| **RSS available** | Yes |
| **RSS URL** | https://ir.lv/rss |
| **RSS full text** | Yes |
| **Notes** | Paywalled investigative weekly. Listing pages accessible with some extractable content. RSS at /rss provides full-text content - best extraction path. |

**First paragraph excerpt:** Tēmas Politika Personības Kultūra Nauda Sabiedrība Labsajūta Eiropā...

### 8. Re:Baltica

| Field | Result |
|---|---|
| **Domain** | `rebaltica.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://rebaltica.lv/feed/ |
| **RSS full text** | Yes |
| **Notes** | Free investigative journalism center. Homepage loads but article links not extractable from static HTML. RSS (WordPress feed) at /feed/ provides full-text content - best extraction path. |

### 9. Dienas Bizness

| Field | Result |
|---|---|
| **Domain** | `db.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Partially paywalled business publication. Homepage JS-rendered; article links not extractable. No RSS feed found. Would require headless browser. |

### 10. BNS Latvia

| Field | Result |
|---|---|
| **Domain** | `bns.lv` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Subscription wire service. Site not accessible via curl - may require authentication or blocks automated access. No public RSS feed. |

### 11. Saeima

| Field | Result |
|---|---|
| **Domain** | `saeima.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.saeima.lv/lv/aktualitates/saeimas-zinas |
| **RSS available** | Yes |
| **RSS URL** | https://saeima.lv/lv/feeds/news.rss |
| **RSS full text** | Yes |
| **Notes** | Free parliament site. Server-rendered HTML with extractable content. RSS at /lv/feeds/news.rss provides full-text content. Both HTML and RSS extraction viable. |

**First paragraph excerpt:** Lai šī tīmekļvietne darbotos, tā izmanto obligāti nepieciešamās sīkdatnes.

### 12. Ministry of Defence

| Field | Result |
|---|---|
| **Domain** | `mod.gov.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.mod.gov.lv/lv/robezas-stiprinasana/pretmobilitates-infrastrukturas-izveides-likums/biezak-uzdotie-jautajumi-par |
| **RSS available** | Yes |
| **RSS URL** | https://mod.gov.lv/rss.xml |
| **RSS full text** | Yes |
| **Notes** | Free government site. Server-rendered HTML with rich defense content. RSS at /rss.xml provides full-text. Both HTML and RSS extraction viable. |

**First paragraph excerpt:** Mēs esam gatavi aizsargāt Latviju no pirmā centimetra. Austrumu robežas nostiprināšana ir galvenais uzdevums Krievijas atturēšanai.

### 13. Ministry of Foreign Affairs

| Field | Result |
|---|---|
| **Domain** | `mfa.gov.lv` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Government site - connection timed out or blocked automated requests. May require browser-based access. |

### 14. VDD

| Field | Result |
|---|---|
| **Domain** | `vdd.gov.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://vdd.gov.lv/aktualitates/jaunumi/vdd-publice-ikgadejo-parskatu-par-identificetajiem-apdraudejumiem-un-istenoto-pretdarbibu |
| **Publication date** | 2026-02-02 |
| **RSS available** | No |
| **Notes** | Free security service site. Server-rendered HTML with extractable content including annual threat reports. No RSS feed. Date extractable from structured data. |

**First paragraph excerpt:** You are using an outdated browser. Please upgrade your browser to improve your experience.

### 15. Providus

| Field | Result |
|---|---|
| **Domain** | `providus.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Free think tank. Homepage loads but content JS-rendered or sparse. No article links extractable. No RSS feed found. Would require headless browser. |

### 16. LIIA

| Field | Result |
|---|---|
| **Domain** | `liia.lv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://liia.lv/en/news/event/belarus-today-human-rights-and-geopolitical-realities-1532 |
| **RSS available** | No |
| **Notes** | Free foreign policy think tank. Server-rendered HTML with extractable content. No RSS feed found. Event and publication pages accessible. |

**First paragraph excerpt:** LIIA News Publications Fellows Programmes Projects Opinions Contact...

### 17. The Baltic Times

| Field | Result |
|---|---|
| **Domain** | `baltictimes.com` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.baltictimes.com/search/jcms/start/0/ |
| **RSS available** | Yes |
| **RSS URL** | https://baltictimes.com/rss |
| **RSS full text** | No |
| **Notes** | Free English-language pan-Baltic outlet. Server-rendered HTML with extractable content. RSS at /rss provides headlines and summaries. |

**First paragraph excerpt:** TALLINN - Apollo Group, the largest entertainment and restaurant company in the Baltics, plans to open more than 100 restaurants in the Baltic s...
