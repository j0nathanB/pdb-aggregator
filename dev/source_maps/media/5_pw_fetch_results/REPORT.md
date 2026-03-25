# Playwright + Trafilatura Article Extraction Test Report

**Generated:** 2026-03-20

**Method:** For each source domain that scored 2/3 or less in the Claude WebFetch test, launched a headless Chromium browser via Playwright to render the page (including JS execution, cookie consent dismissal, and lazy-load triggering), then extracted article content with `trafilatura.extract()`. A successful result means article content (>200 chars) was extracted from the rendered HTML.

**Tier:** 4 of 4 in extraction chain (Claude web_fetch → Diffbot → curl+trafilatura → Playwright+trafilatura)

---

**Total domains tested:** 182
**Total URL fetch attempts:** 531
**Successful article extractions (OK):** 256 (48%)
**Failed extractions (FAILED):** 275 (51%)

**Fully accessible domains (all URLs OK):** 56 (30%)
**Partially accessible domains:** 60 (32%)
**Fully inaccessible domains (0 OK):** 66 (36%)

## Comparison with Claude WebFetch

**Improved over WebFetch:** 104 domains
**Same as WebFetch:** 59 domains
**Worse than WebFetch:** 19 domains

## Full Results

| # | Domain | WebFetch Score | URL 1 | URL 2 | URL 3 | Playwright Score |
|---|--------|---------------|-------|-------|-------|-----------------|
| 1 | `15min.lt` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 2 | `abc.es` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 3 | `abc.net.au` | 0/3 | OK | OK | FAILED | 2/3 |
| 4 | `aftenposten.no` | 0/3 | OK | OK | OK | 3/3 |
| 5 | `aftonbladet.se` | 0/3 | OK | OK | OK | 3/3 |
| 6 | `agenzianova.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 7 | `agi.it` | 0/3 | OK | OK | FAILED | 2/3 |
| 8 | `al-monitor.com` | 2/3 | OK | OK | OK | 3/3 |
| 9 | `alarabiya.net` | 0/3 | FAILED | OK | OK | 2/3 |
| 10 | `alriyadh.com` | 0/1 | OK | -- | -- | 1/1 |
| 11 | `altinget.se` | 2/3 | OK | OK | OK | 3/3 |
| 12 | `ansa.it` | 2/3 | FAILED | OK | FAILED | 1/3 |
| 13 | `antena3.ro` | 2/3 | OK | OK | FAILED | 2/3 |
| 14 | `arabianbusiness.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 15 | `arabnews.com` | 0/3 | OK | FAILED | OK | 2/3 |
| 16 | `aripaev.ee` | 0/3 | OK | OK | OK | 3/3 |
| 17 | `aristeguinoticias.com` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 18 | `asahi.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 19 | `athenalab.org` | 2/3 | FAILED | OK | OK | 2/3 |
| 20 | `bbc.co.uk` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 21 | `bhaskar.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 22 | `bnamericas.com` | 0/3 | OK | OK | OK | 3/3 |
| 23 | `canadiandefencereview.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 24 | `cebri.org` | 1/3 | OK | OK | OK | 3/3 |
| 25 | `chathamhouse.org` | 0/3 | FAILED | OK | OK | 2/3 |
| 26 | `chosun.com` | 0/3 | FAILED | FAILED | OK | 1/3 |
| 27 | `cigionline.org` | 0/3 | OK | OK | OK | 3/3 |
| 28 | `cincodias.elpais.com` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 29 | `contexte.com` | 2/3 | OK | OK | OK | 3/3 |
| 30 | `corriere.it` | 0/3 | OK | OK | OK | 3/3 |
| 31 | `cw.com.tw` | 0/3 | OK | OK | OK | 3/3 |
| 32 | `dagbladet.no` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 33 | `defence.gov.au` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 34 | `defenceconnect.com.au` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 35 | `delfi.ee` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 36 | `delfi.lt` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 37 | `delfi.lv` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 38 | `denikn.cz` | 1/3 | OK | OK | OK | 3/3 |
| 39 | `dgap.org` | 0/2 | FAILED | FAILED | -- | 0/2 |
| 40 | `di.se` | 0/3 | OK | FAILED | OK | 2/3 |
| 41 | `dn.no` | 0/3 | OK | FAILED | OK | 2/3 |
| 42 | `dn.se` | 0/3 | OK | OK | OK | 3/3 |
| 43 | `dw.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 44 | `e24.no` | 2/3 | OK | OK | OK | 3/3 |
| 45 | `eastasiaforum.org` | 0/3 | FAILED | OK | OK | 2/3 |
| 46 | `economictimes.indiatimes.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 47 | `economist.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 48 | `efe.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 49 | `ekspress.delfi.ee` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 50 | `elconfidencial.com` | 0/3 | OK | FAILED | OK | 2/3 |
| 51 | `eldiario.es` | 2/3 | OK | FAILED | FAILED | 1/3 |
| 52 | `eleconomista.com.mx` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 53 | `eleconomista.es` | 0/3 | OK | OK | OK | 3/3 |
| 54 | `elespanol.com` | 0/3 | OK | FAILED | OK | 2/3 |
| 55 | `elfinanciero.com.mx` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 56 | `elmundo.es` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 57 | `elpais.com` | 0/3 | OK | OK | OK | 3/3 |
| 58 | `eluniversal.com.mx` | 2/3 | FAILED | FAILED | OK | 1/3 |
| 59 | `en.yna.co.kr` | 0/3 | FAILED | FAILED | OK | 1/3 |
| 60 | `english.alarabiya.net` | 0/3 | FAILED | OK | OK | 2/3 |
| 61 | `english.hani.co.kr` | 0/2 | FAILED | FAILED | -- | 0/2 |
| 62 | `english.kyodonews.net` | 0/3 | OK | OK | OK | 3/3 |
| 63 | `epl.delfi.ee` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 64 | `epw.in` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 65 | `estadao.com.br` | 0/3 | FAILED | FAILED | OK | 1/3 |
| 66 | `ex-ante.cl` | 0/3 | OK | OK | OK | 3/3 |
| 67 | `expansion.com` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 68 | `expressen.se` | 0/3 | FAILED | OK | OK | 2/3 |
| 69 | `faz.net` | 0/3 | OK | OK | OK | 3/3 |
| 70 | `filternyheter.no` | 1/3 | OK | OK | OK | 3/3 |
| 71 | `folha.uol.com.br` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 72 | `forceindia.net` | 2/3 | OK | OK | OK | 3/3 |
| 73 | `fr.de` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 74 | `france24.com` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 75 | `ft.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 76 | `gatewayhouse.in` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 77 | `gov.br` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 78 | `hbl.fi` | 1/3 | OK | FAILED | OK | 2/3 |
| 79 | `highnorthnews.com` | 1/3 | OK | OK | OK | 3/3 |
| 80 | `hilltimes.com` | 0/3 | OK | FAILED | OK | 2/3 |
| 81 | `hindustantimes.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 82 | `hn.cz` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 83 | `hs.fi` | 0/3 | OK | OK | OK | 3/3 |
| 84 | `icds.ee` | 1/2 | OK | FAILED | -- | 1/2 |
| 85 | `indianexpress.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 86 | `indsr.org.tw` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 87 | `insightcrime.org` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 88 | `intelligenceonline.com` | 0/3 | OK | OK | OK | 3/3 |
| 89 | `ir.lv` | 1/3 | FAILED | FAILED | OK | 1/3 |
| 90 | `irozhlas.cz` | 0/2 | OK | OK | OK | 3/3 |
| 91 | `is.fi` | 0/3 | OK | OK | OK | 3/3 |
| 92 | `ispionline.it` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 93 | `jagran.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 94 | `jakartaglobe.id` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 95 | `japan-forward.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 96 | `japan.kantei.go.jp` | 0/3 | OK | OK | OK | 3/3 |
| 97 | `kam.lt` | 0/3 | OK | OK | OK | 3/3 |
| 98 | `kansanuutiset.fi` | 1/2 | FAILED | FAILED | -- | 0/2 |
| 99 | `kauppalehti.fi` | 0/3 | OK | OK | OK | 3/3 |
| 100 | `klassekampen.no` | 0/3 | OK | OK | OK | 3/3 |
| 101 | `koreajoongangdaily.joins.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 102 | `kyivindependent.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 103 | `la-croix.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 104 | `la.lv` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 105 | `lalettre.fr` | 0/3 | OK | OK | OK | 3/3 |
| 106 | `lavanguardia.com` | 0/3 | OK | FAILED | OK | 2/3 |
| 107 | `lefigaro.fr` | 0/3 | OK | OK | OK | 3/3 |
| 108 | `lemonde.fr` | 0/3 | FAILED | OK | OK | 2/3 |
| 109 | `leparisien.fr` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 110 | `lesechos.fr` | 0/3 | OK | OK | OK | 3/3 |
| 111 | `liberation.fr` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 112 | `libertatea.ro` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 113 | `limesonline.com` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 114 | `livemint.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 115 | `lopinion.fr` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 116 | `lowyinstitute.org` | 0/1 | FAILED | -- | -- | 0/1 |
| 117 | `lrytas.lt` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 118 | `maaal.com` | 0/1 | FAILED | -- | -- | 0/1 |
| 119 | `mediapart.fr` | 0/3 | OK | OK | OK | 3/3 |
| 120 | `mexiconewsdaily.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 121 | `minerva.no` | 1/3 | OK | OK | OK | 3/3 |
| 122 | `mnd.gov.tw` | 0/2 | FAILED | FAILED | -- | 0/2 |
| 123 | `mod.go.jp` | 0/1 | FAILED | -- | -- | 0/1 |
| 124 | `monde-diplomatique.fr` | 0/3 | OK | OK | OK | 3/3 |
| 125 | `morgenbladet.no` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 126 | `n-tv.de` | 0/3 | OK | OK | OK | 3/3 |
| 127 | `nationalpost.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 128 | `neweasterneurope.eu` | 2/3 | OK | OK | OK | 3/3 |
| 129 | `news.tvbs.com.tw` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 130 | `nknews.org` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 131 | `nv.ua` | 0/3 | OK | OK | OK | 3/3 |
| 132 | `oglobo.globo.com` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 133 | `ohtuleht.ee` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 134 | `omni.se` | 0/3 | OK | OK | FAILED | 2/3 |
| 135 | `onet.pl` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 136 | `ouest-france.fr` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 137 | `pauta.cl` | 2/3 | OK | FAILED | FAILED | 1/3 |
| 138 | `pf.org.tw` | 2/3 | OK | OK | FAILED | 2/3 |
| 139 | `politicaexterior.com` | 2/3 | OK | OK | OK | 3/3 |
| 140 | `politico.eu` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 141 | `president.gov.ua` | 0/3 | OK | OK | OK | 3/3 |
| 142 | `profit.ro` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 143 | `razumkov.org.ua` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 144 | `repubblica.it` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 145 | `respekt.cz` | 2/3 | OK | OK | OK | 3/3 |
| 146 | `reuters.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 147 | `rp.pl` | 0/3 | OK | OK | OK | 3/3 |
| 148 | `rus.err.ee` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 149 | `sabq.org` | 0/3 | OK | OK | OK | 3/3 |
| 150 | `spf.org` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 151 | `spiegel.de` | 0/3 | OK | OK | OK | 3/3 |
| 152 | `storm.mg` | 2/3 | FAILED | OK | FAILED | 1/3 |
| 153 | `subrei.gob.cl` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 154 | `sueddeutsche.de` | 0/3 | OK | OK | OK | 3/3 |
| 155 | `suomenkuvalehti.fi` | 1/3 | OK | FAILED | FAILED | 1/3 |
| 156 | `svd.se` | 0/3 | OK | OK | OK | 3/3 |
| 157 | `sydsvenskan.se` | 0/3 | OK | OK | OK | 3/3 |
| 158 | `t24.com.tr` | 0/3 | FAILED | OK | OK | 2/3 |
| 159 | `tagesspiegel.de` | 2/3 | FAILED | OK | OK | 2/3 |
| 160 | `takshashila.org.in` | 0/3 | OK | OK | OK | 3/3 |
| 161 | `talouselama.fi` | 0/3 | OK | OK | OK | 3/3 |
| 162 | `telegraph.co.uk` | 0/3 | OK | FAILED | OK | 2/3 |
| 163 | `thediplomat.com` | 0/3 | FAILED | OK | OK | 2/3 |
| 164 | `theguardian.com` | 0/3 | FAILED | OK | FAILED | 1/3 |
| 165 | `thehindu.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 166 | `thenationalnews.com` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 167 | `thenewslens.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 168 | `theprint.in` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 169 | `thestar.com` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 170 | `tirto.id` | 0/3 | FAILED | OK | OK | 2/3 |
| 171 | `tokyo-np.co.jp` | 1/3 | FAILED | FAILED | FAILED | 0/3 |
| 172 | `tvnet.lv` | 2/3 | FAILED | FAILED | FAILED | 0/3 |
| 173 | `ussc.edu.au` | 2/3 | OK | OK | OK | 3/3 |
| 174 | `uusisuomi.fi` | 0/3 | OK | OK | OK | 3/3 |
| 175 | `valor.globo.com` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 176 | `vz.lt` | 0/3 | OK | OK | OK | 3/3 |
| 177 | `wam.ae` | 0/1 | FAILED | -- | -- | 0/1 |
| 178 | `welt.de` | 0/3 | OK | OK | OK | 3/3 |
| 179 | `www3.nhk.or.jp` | 0/3 | FAILED | FAILED | FAILED | 0/3 |
| 180 | `wyborcza.pl` | 0/3 | OK | FAILED | FAILED | 1/3 |
| 181 | `zeit.de` | 0/3 | OK | OK | OK | 3/3 |
| 182 | `zetatijuana.com` | 2/3 | FAILED | FAILED | FAILED | 0/3 |

## Improved Domains (Playwright > WebFetch)

- `abc.es`: 0/3 → 1/3
- `abc.net.au`: 0/3 → 2/3
- `aftenposten.no`: 0/3 → 3/3
- `aftonbladet.se`: 0/3 → 3/3
- `agi.it`: 0/3 → 2/3
- `al-monitor.com`: 2/3 → 3/3
- `alarabiya.net`: 0/3 → 2/3
- `alriyadh.com`: 0/1 → 1/1
- `altinget.se`: 2/3 → 3/3
- `arabianbusiness.com`: 0/3 → 2/3
- `arabnews.com`: 0/3 → 2/3
- `aripaev.ee`: 0/3 → 3/3
- `bnamericas.com`: 0/3 → 3/3
- `cebri.org`: 1/3 → 3/3
- `chathamhouse.org`: 0/3 → 2/3
- `chosun.com`: 0/3 → 1/3
- `cigionline.org`: 0/3 → 3/3
- `cincodias.elpais.com`: 0/3 → 1/3
- `contexte.com`: 2/3 → 3/3
- `corriere.it`: 0/3 → 3/3
- `cw.com.tw`: 0/3 → 3/3
- `delfi.lt`: 0/3 → 1/3
- `denikn.cz`: 1/3 → 3/3
- `di.se`: 0/3 → 2/3
- `dn.no`: 0/3 → 2/3
- `dn.se`: 0/3 → 3/3
- `e24.no`: 2/3 → 3/3
- `eastasiaforum.org`: 0/3 → 2/3
- `economictimes.indiatimes.com`: 0/3 → 2/3
- `economist.com`: 0/3 → 2/3
- `ekspress.delfi.ee`: 0/3 → 1/3
- `elconfidencial.com`: 0/3 → 2/3
- `eleconomista.es`: 0/3 → 3/3
- `elespanol.com`: 0/3 → 2/3
- `elmundo.es`: 0/3 → 1/3
- `elpais.com`: 0/3 → 3/3
- `en.yna.co.kr`: 0/3 → 1/3
- `english.alarabiya.net`: 0/3 → 2/3
- `english.kyodonews.net`: 0/3 → 3/3
- `epl.delfi.ee`: 0/3 → 1/3
- `estadao.com.br`: 0/3 → 1/3
- `ex-ante.cl`: 0/3 → 3/3
- `expansion.com`: 0/3 → 1/3
- `expressen.se`: 0/3 → 2/3
- `faz.net`: 0/3 → 3/3
- `filternyheter.no`: 1/3 → 3/3
- `folha.uol.com.br`: 0/3 → 1/3
- `forceindia.net`: 2/3 → 3/3
- `france24.com`: 0/3 → 1/3
- `ft.com`: 0/3 → 2/3
- `hbl.fi`: 1/3 → 2/3
- `highnorthnews.com`: 1/3 → 3/3
- `hilltimes.com`: 0/3 → 2/3
- `hs.fi`: 0/3 → 3/3
- `intelligenceonline.com`: 0/3 → 3/3
- `irozhlas.cz`: 0/2 → 3/3
- `is.fi`: 0/3 → 3/3
- `jagran.com`: 0/3 → 2/3
- `japan.kantei.go.jp`: 0/3 → 3/3
- `kam.lt`: 0/3 → 3/3
- `kauppalehti.fi`: 0/3 → 3/3
- `klassekampen.no`: 0/3 → 3/3
- `lalettre.fr`: 0/3 → 3/3
- `lavanguardia.com`: 0/3 → 2/3
- `lefigaro.fr`: 0/3 → 3/3
- `lemonde.fr`: 0/3 → 2/3
- `leparisien.fr`: 0/3 → 1/3
- `lesechos.fr`: 0/3 → 3/3
- `libertatea.ro`: 0/3 → 1/3
- `limesonline.com`: 0/3 → 1/3
- `mediapart.fr`: 0/3 → 3/3
- `minerva.no`: 1/3 → 3/3
- `monde-diplomatique.fr`: 0/3 → 3/3
- `n-tv.de`: 0/3 → 3/3
- `neweasterneurope.eu`: 2/3 → 3/3
- `nv.ua`: 0/3 → 3/3
- `oglobo.globo.com`: 0/3 → 1/3
- `omni.se`: 0/3 → 2/3
- `onet.pl`: 0/3 → 1/3
- `politicaexterior.com`: 2/3 → 3/3
- `president.gov.ua`: 0/3 → 3/3
- `profit.ro`: 0/3 → 1/3
- `repubblica.it`: 0/3 → 1/3
- `respekt.cz`: 2/3 → 3/3
- `rp.pl`: 0/3 → 3/3
- `sabq.org`: 0/3 → 3/3
- `spiegel.de`: 0/3 → 3/3
- `sueddeutsche.de`: 0/3 → 3/3
- `svd.se`: 0/3 → 3/3
- `sydsvenskan.se`: 0/3 → 3/3
- `t24.com.tr`: 0/3 → 2/3
- `takshashila.org.in`: 0/3 → 3/3
- `talouselama.fi`: 0/3 → 3/3
- `telegraph.co.uk`: 0/3 → 2/3
- `thediplomat.com`: 0/3 → 2/3
- `theguardian.com`: 0/3 → 1/3
- `tirto.id`: 0/3 → 2/3
- `ussc.edu.au`: 2/3 → 3/3
- `uusisuomi.fi`: 0/3 → 3/3
- `valor.globo.com`: 0/3 → 1/3
- `vz.lt`: 0/3 → 3/3
- `welt.de`: 0/3 → 3/3
- `wyborcza.pl`: 0/3 → 1/3
- `zeit.de`: 0/3 → 3/3

## Still Inaccessible (0 OK across WebFetch and Playwright)

- `agenzianova.com`
- `asahi.com`
- `bbc.co.uk`
- `bhaskar.com`
- `canadiandefencereview.com`
- `dagbladet.no`
- `defence.gov.au`
- `defenceconnect.com.au`
- `delfi.ee`
- `delfi.lv`
- `dgap.org`
- `dw.com`
- `efe.com`
- `eleconomista.com.mx`
- `elfinanciero.com.mx`
- `english.hani.co.kr`
- `fr.de`
- `gatewayhouse.in`
- `hindustantimes.com`
- `indianexpress.com`
- `indsr.org.tw`
- `insightcrime.org`
- `ispionline.it`
- `jakartaglobe.id`
- `japan-forward.com`
- `koreajoongangdaily.joins.com`
- `kyivindependent.com`
- `la-croix.com`
- `la.lv`
- `liberation.fr`
- `livemint.com`
- `lopinion.fr`
- `lowyinstitute.org`
- `lrytas.lt`
- `maaal.com`
- `mexiconewsdaily.com`
- `mnd.gov.tw`
- `mod.go.jp`
- `morgenbladet.no`
- `nationalpost.com`
- `nknews.org`
- `ohtuleht.ee`
- `ouest-france.fr`
- `politico.eu`
- `reuters.com`
- `spf.org`
- `subrei.gob.cl`
- `thehindu.com`
- `thenewslens.com`
- `thestar.com`
- `wam.ae`
- `www3.nhk.or.jp`

## Newly Accessible via Playwright (was 0/N in WebFetch)

- `abc.es`: 0/3 → 1/3
- `abc.net.au`: 0/3 → 2/3
- `aftenposten.no`: 0/3 → 3/3
- `aftonbladet.se`: 0/3 → 3/3
- `agi.it`: 0/3 → 2/3
- `alarabiya.net`: 0/3 → 2/3
- `alriyadh.com`: 0/1 → 1/1
- `arabianbusiness.com`: 0/3 → 2/3
- `arabnews.com`: 0/3 → 2/3
- `aripaev.ee`: 0/3 → 3/3
- `bnamericas.com`: 0/3 → 3/3
- `chathamhouse.org`: 0/3 → 2/3
- `chosun.com`: 0/3 → 1/3
- `cigionline.org`: 0/3 → 3/3
- `cincodias.elpais.com`: 0/3 → 1/3
- `corriere.it`: 0/3 → 3/3
- `cw.com.tw`: 0/3 → 3/3
- `delfi.lt`: 0/3 → 1/3
- `di.se`: 0/3 → 2/3
- `dn.no`: 0/3 → 2/3
- `dn.se`: 0/3 → 3/3
- `eastasiaforum.org`: 0/3 → 2/3
- `economictimes.indiatimes.com`: 0/3 → 2/3
- `economist.com`: 0/3 → 2/3
- `ekspress.delfi.ee`: 0/3 → 1/3
- `elconfidencial.com`: 0/3 → 2/3
- `eleconomista.es`: 0/3 → 3/3
- `elespanol.com`: 0/3 → 2/3
- `elmundo.es`: 0/3 → 1/3
- `elpais.com`: 0/3 → 3/3
- `en.yna.co.kr`: 0/3 → 1/3
- `english.alarabiya.net`: 0/3 → 2/3
- `english.kyodonews.net`: 0/3 → 3/3
- `epl.delfi.ee`: 0/3 → 1/3
- `estadao.com.br`: 0/3 → 1/3
- `ex-ante.cl`: 0/3 → 3/3
- `expansion.com`: 0/3 → 1/3
- `expressen.se`: 0/3 → 2/3
- `faz.net`: 0/3 → 3/3
- `folha.uol.com.br`: 0/3 → 1/3
- `france24.com`: 0/3 → 1/3
- `ft.com`: 0/3 → 2/3
- `hilltimes.com`: 0/3 → 2/3
- `hs.fi`: 0/3 → 3/3
- `intelligenceonline.com`: 0/3 → 3/3
- `irozhlas.cz`: 0/2 → 3/3
- `is.fi`: 0/3 → 3/3
- `jagran.com`: 0/3 → 2/3
- `japan.kantei.go.jp`: 0/3 → 3/3
- `kam.lt`: 0/3 → 3/3
- `kauppalehti.fi`: 0/3 → 3/3
- `klassekampen.no`: 0/3 → 3/3
- `lalettre.fr`: 0/3 → 3/3
- `lavanguardia.com`: 0/3 → 2/3
- `lefigaro.fr`: 0/3 → 3/3
- `lemonde.fr`: 0/3 → 2/3
- `leparisien.fr`: 0/3 → 1/3
- `lesechos.fr`: 0/3 → 3/3
- `libertatea.ro`: 0/3 → 1/3
- `limesonline.com`: 0/3 → 1/3
- `mediapart.fr`: 0/3 → 3/3
- `monde-diplomatique.fr`: 0/3 → 3/3
- `n-tv.de`: 0/3 → 3/3
- `nv.ua`: 0/3 → 3/3
- `oglobo.globo.com`: 0/3 → 1/3
- `omni.se`: 0/3 → 2/3
- `onet.pl`: 0/3 → 1/3
- `president.gov.ua`: 0/3 → 3/3
- `profit.ro`: 0/3 → 1/3
- `repubblica.it`: 0/3 → 1/3
- `rp.pl`: 0/3 → 3/3
- `sabq.org`: 0/3 → 3/3
- `spiegel.de`: 0/3 → 3/3
- `sueddeutsche.de`: 0/3 → 3/3
- `svd.se`: 0/3 → 3/3
- `sydsvenskan.se`: 0/3 → 3/3
- `t24.com.tr`: 0/3 → 2/3
- `takshashila.org.in`: 0/3 → 3/3
- `talouselama.fi`: 0/3 → 3/3
- `telegraph.co.uk`: 0/3 → 2/3
- `thediplomat.com`: 0/3 → 2/3
- `theguardian.com`: 0/3 → 1/3
- `tirto.id`: 0/3 → 2/3
- `uusisuomi.fi`: 0/3 → 3/3
- `valor.globo.com`: 0/3 → 1/3
- `vz.lt`: 0/3 → 3/3
- `welt.de`: 0/3 → 3/3
- `wyborcza.pl`: 0/3 → 1/3
- `zeit.de`: 0/3 → 3/3
