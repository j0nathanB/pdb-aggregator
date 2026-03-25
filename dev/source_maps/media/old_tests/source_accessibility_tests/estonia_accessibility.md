# Accessibility Test Results: ESTONIA

**Sources tested:** 16

## Summary

| Metric | Count | Rate |
|---|---|---|
| Homepage reachable | 16 / 16 | 100% |
| Article fetchable | 11 / 16 | 69% |
| Full text extractable | 8 / 16 | 50% |
| RSS available | 10 / 16 | 62% |
| RSS full text | 4 / 16 | 25% |

---

## Per-Source Results

### 1. ✅ ERR

| Field | Result |
|---|---|
| **Domain** | `err.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://news.err.ee/rss |
| **RSS full text** | No |
| **Notes** | Free public broadcaster. Homepage JS-rendered; article links not extractable from static HTML. RSS at news.err.ee/rss provides headlines and summaries. Best extraction path is RSS or news.err.ee subdomain. |

### 2. ✅ Postimees

| Field | Result |
|---|---|
| **Domain** | `postimees.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://www.postimees.ee/8434656/suu-kinni-pankadel-ei-lubata-kontodel-alusetu-nuhkimise-peale-isegi-kaevata/comments |
| **Publication date** | 2026-03-17 |
| **RSS available** | Yes |
| **RSS URL** | https://www.postimees.ee/rss |
| **RSS full text** | No |
| **Notes** | Partially paywalled. Article page loads but body JS-rendered or behind paywall. Date extractable from structured data. RSS provides headlines and summaries. |

### 3. ✅ Eesti Paevaleht

| Field | Result |
|---|---|
| **Domain** | `epl.delfi.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://epl.delfi.ee/kategooria/120000945/juhtkiri |
| **RSS available** | No |
| **Notes** | Paywalled (Ekspress Grupp). Some content extractable from category pages. No standard RSS feed found at common paths. |

**First paragraph excerpt:** JUHTKIRI \| Internetikasiinode maksuvabastus tuleb kiirkorras tühistada

### 4. ✅ Delfi Estonia

| Field | Result |
|---|---|
| **Domain** | `delfi.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://www.delfi.ee/kategooria/120000482/uue-kodu-uudised |
| **RSS available** | No |
| **Notes** | Free with ads. Homepage loads but article text JS-rendered. Category pages partially extractable. No standard RSS feed found at delfi.ee. |

### 5. ✅ Eesti Ekspress

| Field | Result |
|---|---|
| **Domain** | `ekspress.delfi.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://ekspress.delfi.ee/kategooria/120000100/podcastid |
| **RSS available** | No |
| **Notes** | Paywalled investigative weekly (Ekspress Grupp). Category/listing pages render server-side with some extractable text. Individual article pages likely behind paywall. No RSS feed found. |

**First paragraph excerpt:** Eesti Ekspressi ajakirjanikud jätkavad lehes kajastatud teemasid, reageerivad vastukajale...

### 6. Aripaev

| Field | Result |
|---|---|
| **Domain** | `aripaev.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://aripaev.ee/rss |
| **RSS full text** | No |
| **Notes** | Paywalled business daily (fully digital). Homepage JS-rendered. RSS provides headlines and summaries. Article content behind paywall. |

### 7. Ohtuleht

| Field | Result |
|---|---|
| **Domain** | `ohtuleht.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://ohtuleht.ee/melu/1153376/karmid-suudistused-malluka-advokaat-meil-on-tunnistajad-kes-vaidavad-et-padar-ajas-kae-naise-intiimpiirkonda-ja-alandas-teda-soprade-ees |
| **Publication date** | 2026-03-16 |
| **RSS available** | Yes |
| **RSS URL** | https://ohtuleht.ee/rss |
| **RSS full text** | No |
| **Notes** | Partially paywalled tabloid. Article pages render server-side with extractable paragraphs. RSS provides headlines and summaries. |

**First paragraph excerpt:** Malluka advokaat Olavi-Jüri Luik rääkis enne istungit Õhtulehele, et tema klient ei ole esitanud ebaõigeid faktiväiteid.

### 8. Diplomaatia

| Field | Result |
|---|---|
| **Domain** | `diplomaatia.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://diplomaatia.ee/rss |
| **RSS full text** | Yes |
| **Notes** | Free security/foreign affairs magazine (ICDS). Homepage loads but article extraction needs direct URLs. RSS at /rss provides full-text content - best extraction path. |

### 9. ICDS

| Field | Result |
|---|---|
| **Domain** | `icds.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | No |
| **Test article** | https://icds.ee/en/category/publications/ |
| **Publication date** | 2026-03-16 |
| **RSS available** | No |
| **Notes** | Free think tank. Publication listing pages accessible but individual publication content may be JS-rendered or in PDF format. No RSS feed found. |

### 10. Propastop

| Field | Result |
|---|---|
| **Domain** | `propastop.org` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://www.propastop.org/feed/ |
| **RSS full text** | Yes |
| **Notes** | Free Defence League volunteer blog. Homepage loads but article links not extracted. RSS (WordPress feed) provides full-text content - best extraction path. |

### 11. ✅ ERR Russian Service

| Field | Result |
|---|---|
| **Domain** | `rus.err.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://rus.err.ee/1609968539/1482-j-den-vojny-v-krasnodarskom-krae-v-rezultate-ataki-bespilotnika-zagorelas-neftebaza |
| **RSS available** | Yes |
| **RSS URL** | https://rus.err.ee/rss |
| **RSS full text** | No |
| **Notes** | Free public broadcaster Russian service. Server-rendered HTML with some extractable content. RSS provides headlines and summaries. |

**First paragraph excerpt:** Грузовик столкнулся с автобусом...

### 12. Riigikogu

| Field | Result |
|---|---|
| **Domain** | `riigikogu.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | No |
| **Full text extractable** | No |
| **RSS available** | Yes |
| **RSS URL** | https://riigikogu.ee/rss |
| **RSS full text** | Yes |
| **Notes** | Free parliament site. Homepage accessible. RSS feed provides full-text content including committee transcripts and news. Best extraction path is RSS. |

### 13. Ministry of Foreign Affairs

| Field | Result |
|---|---|
| **Domain** | `vm.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://vm.ee/tegevus-valdkonnad/relvastuskontroll-ja-maharelvastumine/relvastuskontrolli-ja-maharelvastumise |
| **RSS available** | No |
| **Notes** | Free government site. Server-rendered HTML with extractable content. No RSS feed found. Policy pages and press releases accessible. |

**First paragraph excerpt:** Rohkem infot juurdepääsetavuse kohta leiad siit.

### 14. Ministry of Defence

| Field | Result |
|---|---|
| **Domain** | `kaitseministeerium.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://kaitseministeerium.ee/et/eesmargid-tegevused/laiapohjaline-riigikaitse/toetused-riigikaitselistele-projektidele |
| **RSS available** | Yes |
| **RSS URL** | https://kaitseministeerium.ee/rss.xml |
| **RSS full text** | Yes |
| **Notes** | Free government site. Server-rendered HTML. RSS at /rss.xml provides full-text content. Both HTML and RSS extraction viable. |

**First paragraph excerpt:** Kaitseministeerium toetab ettevõtmisi, mille eesmärk on arendada Eesti elanike kaitsetahet.

### 15. BNS

| Field | Result |
|---|---|
| **Domain** | `bns.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://www.bns.ee/topic/648/news/70097832/ |
| **RSS available** | Yes |
| **RSS URL** | https://bns.ee/rss.xml |
| **RSS full text** | No |
| **Notes** | Subscription wire service. Public-facing site loads with limited content. Full wire feed requires subscription. RSS at /rss.xml provides headlines. |

**First paragraph excerpt:** BNS on uudisteagentuur, mis on suunatud professionaalsele info kasutajale ja meediale.

### 16. Maaleht

| Field | Result |
|---|---|
| **Domain** | `maaleht.ee` |
| **Homepage reachable** | Yes (HTTP ?) |
| **Article fetchable** | Yes |
| **Full text extractable** | Yes |
| **Test article** | https://maaleht.ee/kategooria/67118944/uudised |
| **RSS available** | No |
| **Notes** | Partially paywalled rural weekly (Ekspress Grupp). Category pages render server-side with extractable content. No standard RSS feed found. |

**First paragraph excerpt:** Eestimaa elu ja inimesi puudutavad olulisemad uudised Eestist
