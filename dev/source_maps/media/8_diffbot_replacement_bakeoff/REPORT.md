# Diffbot → Browserbase Bake-off Report

**Generated:** 2026-04-09T09:56:05
**Wall time:** 2447s
**URLs tested:** 111 across 42 domains

## Method-level success

| Method | Success (>= 200 chars) | % |
|---|---|---|
| curl | 17 / 111 | 15.3% |
| diffbot | 80 / 111 | 72.1% |
| playwright | 98 / 111 | 88.3% |
| browserbase | 103 / 111 | 92.8% |

## Bucket classification

| Bucket | Description | Domains |
|---|---|---|
| A | curl or playwright alone suffices — drop diffbot | 6 |
| B | browserbase replaces diffbot | 32 |
| C | both work — browserbase first, diffbot last-resort | 2 |
| D | only diffbot reliable — keep diffbot | 1 |
| E | nothing reliable — manual review | 1 |

## Per-domain results

| Domain | curl | diffbot | playwright | browserbase | Bucket | Action |
|---|---|---|---|---|---|---|
| `axios.com` | 0/2 | 2/2 | 2/2 | 2/2 | B | browserbase 2/2 >= diffbot 2/2 — replace with bb |
| `bernardinai.lt` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `brecorder.com` | 0/3 | 1/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 1/3 — replace with bb |
| `cbn.globo.com` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `chosun.com` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `cnews.fr` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `dawn.com` | 0/3 | 1/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 1/3 — replace with bb |
| `de.euronews.com` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `defence-blog.com` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `dn.no` | 3/3 | 3/3 | 3/3 | 3/3 | A | curl 3/3 — drop diffbot |
| `economist.com` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `euromaidanpress.com` | 0/3 | 0/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 0/3 — replace with bb |
| `firstonline.info` | 0/1 | 1/1 | 1/1 | 1/1 | B | browserbase 1/1 >= diffbot 1/1 — replace with bb |
| `gp.se` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `hedgeweek.com` | 0/2 | 0/2 | 2/2 | 2/2 | B | browserbase 2/2 >= diffbot 0/2 — replace with bb |
| `inc42.com` | 0/2 | 2/2 | 0/2 | 2/2 | B | browserbase 2/2 >= diffbot 2/2 — replace with bb |
| `investing.com` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `jauns.lv` | 3/3 | 2/3 | 3/3 | 3/3 | A | curl 3/3 — drop diffbot |
| `kedglobal.com` | 1/3 | 2/3 | 1/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `lejdd.fr` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `nationalpost.com` | 3/3 | 3/3 | 3/3 | 3/3 | A | curl 3/3 — drop diffbot |
| `news.ltn.com.tw` | 1/3 | 1/3 | 1/3 | 1/3 | E | nothing reliable (curl 1/3 / bb 1/3 / diffbot 1/3 / pw 1/3) |
| `news.usni.org` | 0/2 | 1/2 | 2/2 | 1/2 | A | playwright 2/2 covers — drop diffbot |
| `ohtuleht.ee` | 3/3 | 2/3 | 3/3 | 3/3 | A | curl 3/3 — drop diffbot |
| `ouest-france.fr` | 2/3 | 1/3 | 2/3 | 2/3 | A | curl 2/3 — drop diffbot |
| `pbs.org` | 0/3 | 1/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 1/3 — replace with bb |
| `poder360.com.br` | 0/3 | 3/3 | 3/3 | 1/3 | D | only diffbot reliable (3/3 vs bb 1/3) — keep diffbot |
| `politico.com` | 0/3 | 3/3 | 3/3 | 2/3 | C | both work (bb 2/3, diffbot 3/3) — bb first, diffbot last |
| `portaldeprefeitura.com.br` | 0/1 | 1/1 | 1/1 | 1/1 | B | browserbase 1/1 >= diffbot 1/1 — replace with bb |
| `replicaonline.ro` | 0/1 | 1/1 | 1/1 | 1/1 | B | browserbase 1/1 >= diffbot 1/1 — replace with bb |
| `reuters.com` | 0/3 | 3/3 | 0/3 | 2/3 | C | both work (bb 2/3, diffbot 3/3) — bb first, diffbot last |
| `rte.ie` | 0/2 | 2/2 | 2/2 | 2/2 | B | browserbase 2/2 >= diffbot 2/2 — replace with bb |
| `sustainablejapan.jp` | 0/1 | 0/1 | 1/1 | 1/1 | B | browserbase 1/1 >= diffbot 0/1 — replace with bb |
| `t24.com.tr` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `theclinic.cl` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `thediplomat.com` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `thehindu.com` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `thenewdaily.com.au` | 0/3 | 3/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |
| `thestatesman.com` | 0/1 | 1/1 | 1/1 | 1/1 | B | browserbase 1/1 >= diffbot 1/1 — replace with bb |
| `time.com` | 1/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `urdupoint.com` | 0/3 | 2/3 | 3/3 | 3/3 | B | browserbase 3/3 >= diffbot 2/3 — replace with bb |
| `washingtonpost.com` | 0/3 | 3/3 | 0/3 | 3/3 | B | browserbase 3/3 >= diffbot 3/3 — replace with bb |

## Routing recommendations

Apply these to `assets/country_configs/extraction_routing.yaml`:

- `axios.com`: replace diffbot with browserbase
- `bernardinai.lt`: replace diffbot with browserbase
- `brecorder.com`: replace diffbot with browserbase
- `cbn.globo.com`: replace diffbot with browserbase
- `chosun.com`: replace diffbot with browserbase
- `cnews.fr`: replace diffbot with browserbase
- `dawn.com`: replace diffbot with browserbase
- `de.euronews.com`: replace diffbot with browserbase
- `defence-blog.com`: replace diffbot with browserbase
- `dn.no`: remove diffbot from fallbacks (curl or playwright alone)
- `economist.com`: replace diffbot with browserbase
- `euromaidanpress.com`: replace diffbot with browserbase
- `firstonline.info`: replace diffbot with browserbase
- `gp.se`: replace diffbot with browserbase
- `hedgeweek.com`: replace diffbot with browserbase
- `inc42.com`: replace diffbot with browserbase
- `investing.com`: replace diffbot with browserbase
- `jauns.lv`: remove diffbot from fallbacks (curl or playwright alone)
- `kedglobal.com`: replace diffbot with browserbase
- `lejdd.fr`: replace diffbot with browserbase
- `nationalpost.com`: remove diffbot from fallbacks (curl or playwright alone)
- `news.ltn.com.tw`: **manual review** — no reliable method found
- `news.usni.org`: remove diffbot from fallbacks (curl or playwright alone)
- `ohtuleht.ee`: remove diffbot from fallbacks (curl or playwright alone)
- `ouest-france.fr`: remove diffbot from fallbacks (curl or playwright alone)
- `pbs.org`: replace diffbot with browserbase
- `poder360.com.br`: keep diffbot as primary fallback (no browserbase replacement)
- `politico.com`: `fallbacks: [playwright, browserbase, diffbot]`
- `portaldeprefeitura.com.br`: replace diffbot with browserbase
- `replicaonline.ro`: replace diffbot with browserbase
- `reuters.com`: `fallbacks: [playwright, browserbase, diffbot]`
- `rte.ie`: replace diffbot with browserbase
- `sustainablejapan.jp`: replace diffbot with browserbase
- `t24.com.tr`: replace diffbot with browserbase
- `theclinic.cl`: replace diffbot with browserbase
- `thediplomat.com`: replace diffbot with browserbase
- `thehindu.com`: replace diffbot with browserbase
- `thenewdaily.com.au`: replace diffbot with browserbase
- `thestatesman.com`: replace diffbot with browserbase
- `time.com`: replace diffbot with browserbase
- `urdupoint.com`: replace diffbot with browserbase
- `washingtonpost.com`: replace diffbot with browserbase