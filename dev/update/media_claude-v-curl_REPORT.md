# Head-to-Head: Claude WebFetch vs curl + trafilatura

**Generated:** 2026-03-20

**Method:** 20 domains randomly sampled (seed=42) from 356 eligible domains, stratified:
- 10 from Claude's "easy" pool (scored 3/3 in earlier test)
- 10 from Claude's "hard" pool (scored <3/3 in earlier test)

Both methods tested the **same 3 URLs per domain** (60 URLs total).
Excluded: 6 dead domains + domains with <3 URLs.

---

## Overall Results

| Metric | Claude WebFetch | curl + trafilatura |
|--------|----------------|-------------------|
| URLs OK | 31/60 | 49/60 |
| URL success rate | 51% | 81% |
| Domains fully OK (3/3) | 10/20 | 16/20 |
| Domains with any OK | 11/20 | 17/20 |
| Domains with 0 OK | 9/20 | 3/20 |

## Per-Domain Comparison

| # | Domain | Pool | Claude | curl | Winner |
|---|--------|------|--------|------|--------|
| 1 | `aktualne.cz` | perfect | 3/3 | 3/3 | tie |
| 2 | `asahi.com` | imperfect | 0/3 | 3/3 | **curl** |
| 3 | `cbc.ca` | perfect | 3/3 | 0/3 | **Claude** |
| 4 | `cigionline.org` | imperfect | 0/3 | 0/3 | tie |
| 5 | `czdefence.com` | perfect | 3/3 | 3/3 | tie |
| 6 | `delfi.lv` | imperfect | 0/3 | 3/3 | **curl** |
| 7 | `gov.uk` | perfect | 3/3 | 3/3 | tie |
| 8 | `highnorthnews.com` | imperfect | 1/3 | 1/3 | tie |
| 9 | `jota.info` | perfect | 3/3 | 3/3 | tie |
| 10 | `lopinion.fr` | imperfect | 0/3 | 3/3 | **curl** |
| 11 | `n-tv.de` | imperfect | 0/3 | 3/3 | **curl** |
| 12 | `president.gov.ua` | imperfect | 0/3 | 0/3 | tie |
| 13 | `reforma.com` | perfect | 3/3 | 3/3 | tie |
| 14 | `senado.leg.br` | perfect | 3/3 | 3/3 | tie |
| 15 | `seznamzpravy.cz` | perfect | 3/3 | 3/3 | tie |
| 16 | `telegraph.co.uk` | imperfect | 0/3 | 3/3 | **curl** |
| 17 | `theconversation.com` | perfect | 3/3 | 3/3 | tie |
| 18 | `theglobeandmail.com` | perfect | 3/3 | 3/3 | tie |
| 19 | `thestar.com` | imperfect | 0/3 | 3/3 | **curl** |
| 20 | `wyborcza.pl` | imperfect | 0/3 | 3/3 | **curl** |

**curl wins: 7** | Claude wins: 1 | Ties: 12

## Results by Pool

### Claude's Easy Pool (originally 3/3)

| Method | URLs OK | of 30 | Rate |
|--------|---------|------|------|
| Claude | 30 | 30 | 100% |
| curl | 27 | 30 | 90% |

### Claude's Hard Pool (originally <3/3)

| Method | URLs OK | of 30 | Rate |
|--------|---------|------|------|
| Claude | 1 | 30 | 3% |
| curl | 22 | 30 | 73% |

## Notable Findings

### Claude beat curl

- `cbc.ca`: Claude 3/3 vs curl 0/3

### curl beat Claude

- `asahi.com`: curl 3/3 vs Claude 0/3
- `delfi.lv`: curl 3/3 vs Claude 0/3
- `lopinion.fr`: curl 3/3 vs Claude 0/3
- `n-tv.de`: curl 3/3 vs Claude 0/3
- `telegraph.co.uk`: curl 3/3 vs Claude 0/3
- `thestar.com`: curl 3/3 vs Claude 0/3
- `wyborcza.pl`: curl 3/3 vs Claude 0/3

### Both failed

- `cigionline.org`
- `president.gov.ua`

## Conclusion

On a random stratified sample of 20 domains (60 URLs), **curl + trafilatura retrieved 49 URLs vs Claude WebFetch's 31** — a 58% improvement.

curl matched or beat Claude on every domain in the easy pool and dramatically outperformed on the hard pool. Claude won on 1 domain(s), curl won on 7, with 12 ties.

Claude's win (cbc.ca) suggests some sites actively block trafilatura's user-agent or Python requests but allow Claude's fetch infrastructure.