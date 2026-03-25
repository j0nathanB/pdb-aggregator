# Accessibility Test Results: LITHUANIA

**Sources tested:** 17

## Summary

| Metric | Count | Rate |
|---|---|---|
| Homepage reachable | 12 / 17 | 71% |
| Article fetchable | 2 / 17 | 12% |
| Full text extractable | 2 / 17 | 12% |
| RSS available | 6 / 17 | 35% |
| RSS full text | 3 / 17 | 18% |

---

## Per-Source Results

### 1. ✅ LRT

| Field | Result |
|---|---|
| **Domain** | `lrt.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://lrt.lt/?rss |
| **RSS full text** | Yes |
| **Notes** | Free public broadcaster. Homepage JS-rendered; article links not extractable from static HTML. RSS at /?rss provides full-text content with HTML - best extraction path. English service at lrt.lt/en. |

### 2. ✅ Delfi.lt

| Field | Result |
|---|---|
| **Domain** | `delfi.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://delfi.lt/rss |
| **RSS full text** | No |
| **Notes** | Free with ads. Homepage JS-rendered; article text not extractable from static HTML. RSS at /rss provides headlines and summaries. |

### 3. ✅ 15min.lt

| Field | Result |
|---|---|
| **Domain** | `15min.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://15min.lt/rss |
| **RSS full text** | Yes |
| **Notes** | Free with ads. Homepage JS-rendered. RSS at /rss provides full-text content - best extraction path. |

### 4. Lietuvos rytas

| Field | Result |
|---|---|
| **Domain** | `lrytas.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://lrytas.lt/rss |
| **RSS full text** | Yes |
| **Notes** | Partially paywalled. Homepage JS-rendered; no article links extractable from static HTML. RSS at /rss provides full-text content - best extraction path. |

### 5. Verslo zinios

| Field | Result |
|---|---|
| **Domain** | `vz.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://vz.lt/rss |
| **RSS full text** | No |
| **Notes** | Paywalled business daily (Bonnier). Homepage JS-rendered. RSS provides headlines and summaries. Article content behind paywall. |

### 6. Siena

| Field | Result |
|---|---|
| **Domain** | `siena.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Free investigative outlet. Homepage loads but is JS-rendered with no article links in static HTML. No RSS feed found. Would require headless browser for extraction. |

### 7. Laisves TV

| Field | Result |
|---|---|
| **Domain** | `laisves.tv` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Video-first investigative outlet (primarily YouTube). Website is a WordPress landing page with JS rendering. No RSS feed. Primary content is on YouTube; extraction via YouTube API would be more effective. |

### 8. BNS Lithuania

| Field | Result |
|---|---|
| **Domain** | `bns.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Subscription wire service. Public website is a login/subscription page. Full content requires paid subscription. No public RSS feed. |

### 9. ELTA

| Field | Result |
|---|---|
| **Domain** | `elta.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://elta.lt/lt/paslaugos/1 |
| **RSS available** | No |
| **Notes** | Wire service (owned by Ekspress Grupp/Delfi). Public-facing pages are service descriptions, not news articles. Feeds into Delfi. No public RSS. News content requires subscription or accessed via Delfi. |

**First paragraph excerpt:** ELTA – Lietuvos naujienų ir fotoinformacijų agentūra, kasdien parengianti per 600 informacijų bei fotoinformacijų apie svarbiausius Lietuvos ir pasaulio įvykius.

### 10. Veidas

| Field | Result |
|---|---|
| **Domain** | `veidas.lt` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Domain unreachable - connection refused/timed out. Weekly magazine may have relocated or ceased online publication. |

### 11. IQ.lt

| Field | Result |
|---|---|
| **Domain** | `iq.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Free analysis platform. Homepage loads but is JS-rendered with no article links in static HTML. No RSS feed found. Would require headless browser. |

### 12. Seimas

| Field | Result |
|---|---|
| **Domain** | `lrs.lt` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Parliament site - connection timed out or blocked automated requests. May require browser-based access or use of specific API endpoints. |

### 13. Ministry of National Defence

| Field | Result |
|---|---|
| **Domain** | `kam.lt` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Government site - connection timed out or blocked automated requests. Lithuanian government sites (.lt) appear to have strict bot filtering. |

### 14. Ministry of Foreign Affairs

| Field | Result |
|---|---|
| **Domain** | `urm.lt` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Government site - connection timed out or blocked automated requests. Lithuanian government sites (.lt) appear to have strict bot filtering. |

### 15. VSD

| Field | Result |
|---|---|
| **Domain** | `vsd.lt` |
| **Homepage reachable** | No (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Intelligence service site - connection timed out or blocked automated requests. Annual threat assessment reports may be available as PDFs but site blocks curl. |

### 16. The Baltic Times

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

### 17. EESC

| Field | Result |
|---|---|
| **Domain** | `eesc.lt` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | No |
| **Notes** | Free think tank. Homepage loads but content is JS-rendered or sparse. No article links extractable. No RSS feed found. Publications may be PDFs. |
