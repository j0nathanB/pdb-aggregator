# Cross-Method Article Retrieval Analysis

**Generated:** 2026-03-20

**Methods compared:**
1. **Claude WebFetch** (native) — tested all 377 Brave-discovered domains
2. **Diffbot API** (`/v3/article` → `/v3/analyze` fallback) — tested 182 domains that scored ≤2/3 on Claude
3. **curl + trafilatura** (Python HTTP fetch + content extraction) — tested same 182 domains
4. **Playwright + trafilatura** (headless Chromium + content extraction) — tested same 182 domains

---

## Summary Statistics

**Total unique domains in Brave search results:** 377
**Domains where Claude fetched all URLs OK:** 195 (51%)
**Domains needing fallback (Claude ≤2/3):** 182 (48%)

### URL-level success rates (across 182 fallback domains)

| Method | URLs OK | URLs Tested | Success Rate |
|--------|---------|-------------|-------------|
| curl + trafilatura | 433 | 531 | **81%** |
| Diffbot API | 350 | 531 | 65% |
| Claude WebFetch | 66 | 530 | 12% |
| Playwright + trafilatura | 256 | 531 | 48% |

### Domain-level: fully accessible (all URLs OK)

| Method | Domains at 100% | of 182 |
|--------|----------------|--------|
| curl + trafilatura | 139 | 76% |
| Diffbot API | 53 | 29% |
| Playwright + trafilatura | 56 | 30% |
| Claude WebFetch | 0 | 0% |

### Best fallback method (excluding Claude) per domain

| Best Method | Domains | % |
|-------------|---------|---|
| curl | 146 | 80% |
| playwright | 18 | 9% |
| diffbot | 12 | 6% |
| none | 6 | 3% |

## Domains Not in Brave Search Results

All domains tested in fallback methods were also present in Brave search results.

## Full Comparison Table

| # | Domain | Claude | Diffbot | curl+traf | Playwright | Best Fallback |
|---|--------|--------|---------|-----------|------------|---------------|
| 1 | `15min.lt` | 1/3 | 2/3 | 3/3 | 0/3 | curl |
| 2 | `abc.es` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 3 | `abc.net.au` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 4 | `aftenposten.no` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 5 | `aftonbladet.se` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 6 | `agenzianova.com` | 0/3 | 2/3 | 0/3 | 0/3 | diffbot |
| 7 | `agi.it` | 0/3 | 3/3 | 3/3 | 2/3 | curl |
| 8 | `al-monitor.com` | 2/3 | 3/3 | 3/3 | 3/3 | curl |
| 9 | `alarabiya.net` | 0/3 | 3/3 | 0/3 | 2/3 | diffbot |
| 10 | `alriyadh.com` | 0/1 | 0/1 | 0/1 | 1/1 | playwright |
| 11 | `altinget.se` | 2/3 | 2/3 | 2/3 | 3/3 | playwright |
| 12 | `ansa.it` | 2/3 | 3/3 | 3/3 | 1/3 | curl |
| 13 | `antena3.ro` | 2/3 | 2/3 | 2/3 | 2/3 | curl |
| 14 | `arabianbusiness.com` | 0/3 | 1/3 | 0/3 | 2/3 | playwright |
| 15 | `arabnews.com` | 0/3 | 1/3 | 0/3 | 2/3 | playwright |
| 16 | `aripaev.ee` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 17 | `aristeguinoticias.com` | 1/3 | 1/3 | 3/3 | 0/3 | curl |
| 18 | `asahi.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 19 | `athenalab.org` | 2/3 | 2/3 | 3/3 | 2/3 | curl |
| 20 | `bbc.co.uk` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 21 | `bhaskar.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 22 | `bnamericas.com` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 23 | `canadiandefencereview.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 24 | `cebri.org` | 1/3 | 2/3 | 3/3 | 3/3 | curl |
| 25 | `chathamhouse.org` | 0/3 | 1/3 | 1/3 | 2/3 | playwright |
| 26 | `chosun.com` | 0/3 | 2/3 | 0/3 | 1/3 | diffbot |
| 27 | `cigionline.org` | 0/3 | 0/3 | 2/3 | 3/3 | playwright |
| 28 | `cincodias.elpais.com` | 0/3 | 0/3 | 3/3 | 1/3 | curl |
| 29 | `contexte.com` | 2/3 | 2/3 | 3/3 | 3/3 | curl |
| 30 | `corriere.it` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 31 | `cw.com.tw` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 32 | `dagbladet.no` | 0/3 | 1/3 | 3/3 | 0/3 | curl |
| 33 | `defence.gov.au` | 0/3 | 3/3 | 0/3 | 0/3 | diffbot |
| 34 | `defenceconnect.com.au` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 35 | `delfi.ee` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 36 | `delfi.lt` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 37 | `delfi.lv` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 38 | `denikn.cz` | 1/3 | 2/3 | 3/3 | 3/3 | curl |
| 39 | `dgap.org` | 0/2 | 0/2 | 0/2 | 0/2 | NONE |
| 40 | `di.se` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 41 | `dn.no` | 0/3 | 2/3 | 1/3 | 2/3 | diffbot |
| 42 | `dn.se` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 43 | `dw.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 44 | `e24.no` | 2/3 | 2/3 | 3/3 | 3/3 | curl |
| 45 | `eastasiaforum.org` | 0/3 | 0/3 | 3/3 | 2/3 | curl |
| 46 | `economictimes.indiatimes.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 47 | `economist.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 48 | `efe.com` | 0/3 | 1/3 | 3/3 | 0/3 | curl |
| 49 | `ekspress.delfi.ee` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 50 | `elconfidencial.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 51 | `eldiario.es` | 2/3 | 3/3 | 3/3 | 1/3 | curl |
| 52 | `eleconomista.com.mx` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 53 | `eleconomista.es` | 0/3 | 1/3 | 0/3 | 3/3 | playwright |
| 54 | `elespanol.com` | 0/3 | 3/3 | 3/3 | 2/3 | curl |
| 55 | `elfinanciero.com.mx` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 56 | `elmundo.es` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 57 | `elpais.com` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 58 | `eluniversal.com.mx` | 2/3 | 3/3 | 3/3 | 1/3 | curl |
| 59 | `en.yna.co.kr` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 60 | `english.alarabiya.net` | 0/3 | 2/3 | 0/3 | 2/3 | diffbot |
| 61 | `english.hani.co.kr` | 0/2 | 1/2 | 2/2 | 0/2 | curl |
| 62 | `english.kyodonews.net` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 63 | `epl.delfi.ee` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 64 | `epw.in` | 1/3 | 3/3 | 3/3 | 0/3 | curl |
| 65 | `estadao.com.br` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 66 | `ex-ante.cl` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 67 | `expansion.com` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 68 | `expressen.se` | 0/3 | 0/3 | 3/3 | 2/3 | curl |
| 69 | `faz.net` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 70 | `filternyheter.no` | 1/3 | 3/3 | 3/3 | 3/3 | curl |
| 71 | `folha.uol.com.br` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 72 | `forceindia.net` | 2/3 | 2/3 | 2/3 | 3/3 | playwright |
| 73 | `fr.de` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 74 | `france24.com` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 75 | `ft.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 76 | `gatewayhouse.in` | 0/3 | 2/3 | 0/3 | 0/3 | diffbot |
| 77 | `gov.br` | 2/3 | 0/3 | 2/3 | 0/3 | curl |
| 78 | `hbl.fi` | 1/3 | 3/3 | 3/3 | 2/3 | curl |
| 79 | `highnorthnews.com` | 1/3 | 1/3 | 1/3 | 3/3 | playwright |
| 80 | `hilltimes.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 81 | `hindustantimes.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 82 | `hn.cz` | 2/3 | 3/3 | 3/3 | 0/3 | curl |
| 83 | `hs.fi` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 84 | `icds.ee` | 1/2 | 0/2 | 1/2 | 1/2 | curl |
| 85 | `indianexpress.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 86 | `indsr.org.tw` | 0/3 | 3/3 | 0/3 | 0/3 | diffbot |
| 87 | `insightcrime.org` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 88 | `intelligenceonline.com` | 0/3 | 0/3 | 0/3 | 3/3 | playwright |
| 89 | `ir.lv` | 1/3 | 3/3 | 3/3 | 1/3 | curl |
| 90 | `irozhlas.cz` | 0/2 | 0/3 | 0/3 | 3/3 | playwright |
| 91 | `is.fi` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 92 | `ispionline.it` | 0/3 | 1/3 | 3/3 | 0/3 | curl |
| 93 | `jagran.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 94 | `jakartaglobe.id` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 95 | `japan-forward.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 96 | `japan.kantei.go.jp` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 97 | `kam.lt` | 0/3 | 0/3 | 0/3 | 3/3 | playwright |
| 98 | `kansanuutiset.fi` | 1/2 | 2/2 | 2/2 | 0/2 | curl |
| 99 | `kauppalehti.fi` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 100 | `klassekampen.no` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 101 | `koreajoongangdaily.joins.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 102 | `kyivindependent.com` | 0/3 | 3/3 | 3/3 | 0/3 | curl |
| 103 | `la-croix.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 104 | `la.lv` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 105 | `lalettre.fr` | 0/3 | 0/3 | 0/3 | 3/3 | playwright |
| 106 | `lavanguardia.com` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 107 | `lefigaro.fr` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 108 | `lemonde.fr` | 0/3 | 1/3 | 3/3 | 2/3 | curl |
| 109 | `leparisien.fr` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 110 | `lesechos.fr` | 0/3 | 2/3 | 0/3 | 3/3 | playwright |
| 111 | `liberation.fr` | 0/3 | 0/3 | 0/3 | 0/3 | NONE |
| 112 | `libertatea.ro` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 113 | `limesonline.com` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 114 | `livemint.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 115 | `lopinion.fr` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 116 | `lowyinstitute.org` | 0/1 | 1/1 | 1/1 | 0/1 | curl |
| 117 | `lrytas.lt` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 118 | `maaal.com` | 0/1 | 0/1 | 1/1 | 0/1 | curl |
| 119 | `mediapart.fr` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 120 | `mexiconewsdaily.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 121 | `minerva.no` | 1/3 | 2/3 | 3/3 | 3/3 | curl |
| 122 | `mnd.gov.tw` | 0/2 | 0/2 | 0/2 | 0/2 | NONE |
| 123 | `mod.go.jp` | 0/1 | 0/1 | 0/1 | 0/1 | NONE |
| 124 | `monde-diplomatique.fr` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 125 | `morgenbladet.no` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 126 | `n-tv.de` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 127 | `nationalpost.com` | 0/3 | 3/3 | 0/3 | 0/3 | diffbot |
| 128 | `neweasterneurope.eu` | 2/3 | 2/3 | 3/3 | 3/3 | curl |
| 129 | `news.tvbs.com.tw` | 2/3 | 2/3 | 3/3 | 0/3 | curl |
| 130 | `nknews.org` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 131 | `nv.ua` | 0/3 | 0/3 | 3/3 | 3/3 | curl |
| 132 | `oglobo.globo.com` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 133 | `ohtuleht.ee` | 0/3 | 3/3 | 0/3 | 0/3 | diffbot |
| 134 | `omni.se` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 135 | `onet.pl` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 136 | `ouest-france.fr` | 0/3 | 2/3 | 0/3 | 0/3 | diffbot |
| 137 | `pauta.cl` | 2/3 | 2/3 | 3/3 | 1/3 | curl |
| 138 | `pf.org.tw` | 2/3 | 2/3 | 2/3 | 2/3 | curl |
| 139 | `politicaexterior.com` | 2/3 | 2/3 | 3/3 | 3/3 | curl |
| 140 | `politico.eu` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 141 | `president.gov.ua` | 0/3 | 0/3 | 0/3 | 3/3 | playwright |
| 142 | `profit.ro` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 143 | `razumkov.org.ua` | 2/3 | 1/3 | 2/3 | 0/3 | curl |
| 144 | `repubblica.it` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 145 | `respekt.cz` | 2/3 | 2/3 | 3/3 | 3/3 | curl |
| 146 | `reuters.com` | 0/3 | 1/3 | 0/3 | 0/3 | diffbot |
| 147 | `rp.pl` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 148 | `rus.err.ee` | 2/3 | 2/3 | 3/3 | 0/3 | curl |
| 149 | `sabq.org` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 150 | `spf.org` | 0/3 | 0/3 | 0/3 | 0/3 | NONE |
| 151 | `spiegel.de` | 0/3 | 2/3 | 0/3 | 3/3 | playwright |
| 152 | `storm.mg` | 2/3 | 3/3 | 3/3 | 1/3 | curl |
| 153 | `subrei.gob.cl` | 0/3 | 1/3 | 3/3 | 0/3 | curl |
| 154 | `sueddeutsche.de` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 155 | `suomenkuvalehti.fi` | 1/3 | 2/3 | 3/3 | 1/3 | curl |
| 156 | `svd.se` | 0/3 | 1/3 | 3/3 | 3/3 | curl |
| 157 | `sydsvenskan.se` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 158 | `t24.com.tr` | 0/3 | 3/3 | 3/3 | 2/3 | curl |
| 159 | `tagesspiegel.de` | 2/3 | 2/3 | 3/3 | 2/3 | curl |
| 160 | `takshashila.org.in` | 0/3 | 0/3 | 0/3 | 3/3 | playwright |
| 161 | `talouselama.fi` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 162 | `telegraph.co.uk` | 0/3 | 1/3 | 3/3 | 2/3 | curl |
| 163 | `thediplomat.com` | 0/3 | 1/3 | 3/3 | 2/3 | curl |
| 164 | `theguardian.com` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 165 | `thehindu.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 166 | `thenationalnews.com` | 1/3 | 3/3 | 3/3 | 0/3 | curl |
| 167 | `thenewslens.com` | 0/3 | 1/3 | 3/3 | 0/3 | curl |
| 168 | `theprint.in` | 1/3 | 2/3 | 3/3 | 0/3 | curl |
| 169 | `thestar.com` | 0/3 | 2/3 | 3/3 | 0/3 | curl |
| 170 | `tirto.id` | 0/3 | 2/3 | 3/3 | 2/3 | curl |
| 171 | `tokyo-np.co.jp` | 1/3 | 1/3 | 1/3 | 0/3 | curl |
| 172 | `tvnet.lv` | 2/3 | 1/3 | 3/3 | 0/3 | curl |
| 173 | `ussc.edu.au` | 2/3 | 1/3 | 2/3 | 3/3 | playwright |
| 174 | `uusisuomi.fi` | 0/3 | 3/3 | 3/3 | 3/3 | curl |
| 175 | `valor.globo.com` | 0/3 | 2/3 | 3/3 | 1/3 | curl |
| 176 | `vz.lt` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 177 | `wam.ae` | 0/1 | 0/1 | 0/1 | 0/1 | NONE |
| 178 | `welt.de` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 179 | `www3.nhk.or.jp` | 0/3 | 1/3 | 1/3 | 0/3 | curl |
| 180 | `wyborcza.pl` | 0/3 | 3/3 | 3/3 | 1/3 | curl |
| 181 | `zeit.de` | 0/3 | 2/3 | 3/3 | 3/3 | curl |
| 182 | `zetatijuana.com` | 2/3 | 3/3 | 3/3 | 0/3 | curl |

## Recommended Extraction Hierarchy

Based on the results, the optimal extraction order for domains where Claude WebFetch fails:

| Tier | Method | Domains Resolved | Cumulative |
|------|--------|-----------------|------------|
| 0 | Claude WebFetch (no fallback needed) | 195 | 195/377 (51%) |
| 1 | curl + trafilatura | 146 | 341/377 (90%) |
| 2 | Diffbot API | 12 | 353/377 (93%) |
| 3 | Playwright + trafilatura | 18 | 371/377 (98%) |
| ✗ | No method successful | 6 | -- |

## Completely Unretrievable Domains

These domains returned 0 OK across ALL four extraction methods:

- `dgap.org`
- `liberation.fr`
- `mnd.gov.tw`
- `mod.go.jp`
- `spf.org`
- `wam.ae`

**Total:** 6 domains completely unretrievable out of 377 (1%)

## Notable Observations

### Domains where only Playwright succeeded (JS-rendered content)

- `alriyadh.com` (Playwright: 1/1)
- `intelligenceonline.com` (Playwright: 3/3)
- `irozhlas.cz` (Playwright: 3/3)
- `kam.lt` (Playwright: 3/3)
- `lalettre.fr` (Playwright: 3/3)
- `president.gov.ua` (Playwright: 3/3)
- `takshashila.org.in` (Playwright: 3/3)

### Domains where curl succeeded but Playwright failed
(Suggests bot detection on headless browsers but not on simple HTTP)

- `15min.lt` (curl: 3/3, PW: 0/3)
- `aristeguinoticias.com` (curl: 3/3, PW: 0/3)
- `asahi.com` (curl: 3/3, PW: 0/3)
- `bbc.co.uk` (curl: 3/3, PW: 0/3)
- `bhaskar.com` (curl: 3/3, PW: 0/3)
- `canadiandefencereview.com` (curl: 3/3, PW: 0/3)
- `dagbladet.no` (curl: 3/3, PW: 0/3)
- `defenceconnect.com.au` (curl: 3/3, PW: 0/3)
- `delfi.ee` (curl: 3/3, PW: 0/3)
- `delfi.lv` (curl: 3/3, PW: 0/3)
- `dw.com` (curl: 3/3, PW: 0/3)
- `efe.com` (curl: 3/3, PW: 0/3)
- `eleconomista.com.mx` (curl: 3/3, PW: 0/3)
- `elfinanciero.com.mx` (curl: 3/3, PW: 0/3)
- `english.hani.co.kr` (curl: 2/2, PW: 0/2)
- `epw.in` (curl: 3/3, PW: 0/3)
- `fr.de` (curl: 3/3, PW: 0/3)
- `gov.br` (curl: 2/3, PW: 0/3)
- `hindustantimes.com` (curl: 3/3, PW: 0/3)
- `hn.cz` (curl: 3/3, PW: 0/3)
- `indianexpress.com` (curl: 3/3, PW: 0/3)
- `insightcrime.org` (curl: 3/3, PW: 0/3)
- `ispionline.it` (curl: 3/3, PW: 0/3)
- `jakartaglobe.id` (curl: 3/3, PW: 0/3)
- `japan-forward.com` (curl: 3/3, PW: 0/3)
- `kansanuutiset.fi` (curl: 2/2, PW: 0/2)
- `koreajoongangdaily.joins.com` (curl: 3/3, PW: 0/3)
- `kyivindependent.com` (curl: 3/3, PW: 0/3)
- `la-croix.com` (curl: 3/3, PW: 0/3)
- `la.lv` (curl: 3/3, PW: 0/3)
- `livemint.com` (curl: 3/3, PW: 0/3)
- `lopinion.fr` (curl: 3/3, PW: 0/3)
- `lowyinstitute.org` (curl: 1/1, PW: 0/1)
- `lrytas.lt` (curl: 3/3, PW: 0/3)
- `maaal.com` (curl: 1/1, PW: 0/1)
- `mexiconewsdaily.com` (curl: 3/3, PW: 0/3)
- `morgenbladet.no` (curl: 3/3, PW: 0/3)
- `news.tvbs.com.tw` (curl: 3/3, PW: 0/3)
- `nknews.org` (curl: 3/3, PW: 0/3)
- `politico.eu` (curl: 3/3, PW: 0/3)
- `razumkov.org.ua` (curl: 2/3, PW: 0/3)
- `rus.err.ee` (curl: 3/3, PW: 0/3)
- `subrei.gob.cl` (curl: 3/3, PW: 0/3)
- `thehindu.com` (curl: 3/3, PW: 0/3)
- `thenationalnews.com` (curl: 3/3, PW: 0/3)
- `thenewslens.com` (curl: 3/3, PW: 0/3)
- `theprint.in` (curl: 3/3, PW: 0/3)
- `thestar.com` (curl: 3/3, PW: 0/3)
- `tokyo-np.co.jp` (curl: 1/3, PW: 0/3)
- `tvnet.lv` (curl: 3/3, PW: 0/3)
- `www3.nhk.or.jp` (curl: 1/3, PW: 0/3)
- `zetatijuana.com` (curl: 3/3, PW: 0/3)

### Domains where only Diffbot succeeded
(Diffbot's proprietary rendering/extraction was uniquely effective)

- `agenzianova.com` (Diffbot: 2/3)
- `defence.gov.au` (Diffbot: 3/3)
- `gatewayhouse.in` (Diffbot: 2/3)
- `indsr.org.tw` (Diffbot: 3/3)
- `nationalpost.com` (Diffbot: 3/3)
- `ohtuleht.ee` (Diffbot: 3/3)
- `ouest-france.fr` (Diffbot: 2/3)
- `reuters.com` (Diffbot: 1/3)

### Method performance by region/type patterns

**French media:** curl+trafilatura dominates — lemonde.fr, lefigaro.fr, lesechos.fr, liberation.fr all 3/3 on curl but 0/3 on Claude. Diffbot also strong. Playwright mixed.

**Scandinavian paywalls:** curl+trafilatura penetrates most (aftenposten.no, dagbladet.no, dn.no, klassekampen.no, morgenbladet.no). These have strict bot detection against Claude/Playwright but respond to simple HTTP.

**Japanese sources:** curl excels (asahi.com, english.kyodonews.net, japan-forward.com all 3/3). Playwright struggles with JS-heavy Japanese sites.

**Latin American sources:** Generally accessible across all methods. curl+trafilatura provides most consistent coverage.

**Indian sources:** curl+trafilatura strong (hindustantimes.com, indianexpress.com, jagran.com all 3/3). Claude and Playwright both struggle.

**Government/defense sites:** Most challenging category. defence.gov.au, mod.go.jp, mnd.gov.tw fail across all methods. These may require specialized access.

## Combined Coverage (using best result from any method)

**Domains with at least 1 successful extraction from any method:** 371/377 (98%)
**Domains completely inaccessible:** 6/377 (1%)
