# Diffbot Article Retrieval Test Report

**Generated:** 2026-03-20

**Method:** For each source domain that scored 2/3 or less on WebFetch, attempted to extract article content via Diffbot API (`/v3/article`, falling back to `/v3/analyze`). Used the same URLs tested in the WebFetch round.

---

**Total domains tested:** 182
**Total URL fetch attempts:** 531
**Successful extractions (OK):** 350 (65%)
**Empty response (EMPTY):** 13 (2%)
**Failed to fetch (FAILED):** 168 (31%)
**Extracted via /v3/article:** 223
**Extracted via /v3/analyze (fallback):** 127

**Fully accessible (all URLs OK):** 53 (29%)
**Partially accessible:** 108 (59%)
**Fully inaccessible (0 OK):** 21 (11%)

### Diffbot vs WebFetch comparison

- **Improved over WebFetch:** 141 domains (77%)
- **Same as WebFetch:** 36 domains (19%)
- **Worse than WebFetch:** 5 domains (2%)

## Full Results

| # | Domain | WebFetch | Diffbot | URL 1 | URL 2 | URL 3 | API Used |
|---|--------|---------|---------|-------|-------|-------|----------|
| 1 | `15min.lt` | 1/3 | 2/3 ↑ | OK | OK | FAILED | art, anlz, - |
| 2 | `abc.es` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 3 | `abc.net.au` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 4 | `aftenposten.no` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 5 | `aftonbladet.se` | 0/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 6 | `agenzianova.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, anlz, - |
| 7 | `agi.it` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, anlz |
| 8 | `al-monitor.com` | 2/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 9 | `alarabiya.net` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 10 | `alriyadh.com` | 0/1 | 0/1 | EMPTY | -- | -- | -, --, -- |
| 11 | `altinget.se` | 2/3 | 2/3 | OK | OK | FAILED | art, anlz, - |
| 12 | `ansa.it` | 2/3 | 3/3 ↑ | OK | OK | OK | art, anlz, anlz |
| 13 | `antena3.ro` | 2/3 | 2/3 | OK | FAILED | OK | art, -, anlz |
| 14 | `arabianbusiness.com` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, art |
| 15 | `arabnews.com` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, art |
| 16 | `aripaev.ee` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 17 | `aristeguinoticias.com` | 1/3 | 1/3 | FAILED | FAILED | OK | -, -, art |
| 18 | `asahi.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |
| 19 | `athenalab.org` | 2/3 | 2/3 | FAILED | OK | OK | -, art, art |
| 20 | `bbc.co.uk` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 21 | `bhaskar.com` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 22 | `bnamericas.com` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 23 | `canadiandefencereview.com` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 24 | `cebri.org` | 1/3 | 2/3 ↑ | OK | OK | FAILED | anlz, anlz, - |
| 25 | `chathamhouse.org` | 0/3 | 1/3 ↑ | FAILED | OK | FAILED | -, art, - |
| 26 | `chosun.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, anlz, - |
| 27 | `cigionline.org` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 28 | `cincodias.elpais.com` | 0/3 | 0/3 | FAILED | FAILED | EMPTY | -, -, - |
| 29 | `contexte.com` | 2/3 | 2/3 | OK | FAILED | OK | art, -, art |
| 30 | `corriere.it` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |
| 31 | `cw.com.tw` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 32 | `dagbladet.no` | 0/3 | 1/3 ↑ | OK | FAILED | FAILED | anlz, -, - |
| 33 | `defence.gov.au` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 34 | `defenceconnect.com.au` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 35 | `delfi.ee` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 36 | `delfi.lt` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 37 | `delfi.lv` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 38 | `denikn.cz` | 1/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 39 | `dgap.org` | 0/2 | 0/2 | FAILED | FAILED | -- | -, -, -- |
| 40 | `di.se` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 41 | `dn.no` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 42 | `dn.se` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 43 | `dw.com` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 44 | `e24.no` | 2/3 | 2/3 | FAILED | OK | OK | -, art, anlz |
| 45 | `eastasiaforum.org` | 0/3 | 0/3 | FAILED | EMPTY | EMPTY | -, -, - |
| 46 | `economictimes.indiatimes.com` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 47 | `economist.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 48 | `efe.com` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, art |
| 49 | `ekspress.delfi.ee` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 50 | `elconfidencial.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 51 | `elDiario.es` | 2/3 | 3/3 ↑ | OK | OK | OK | art, anlz, anlz |
| 52 | `eleconomista.com.mx` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 53 | `eleconomista.es` | 0/3 | 1/3 ↑ | FAILED | OK | FAILED | -, art, - |
| 54 | `elespanol.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |
| 55 | `elfinanciero.com.mx` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 56 | `elmundo.es` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, anlz |
| 57 | `elpais.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 58 | `eluniversal.com.mx` | 2/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 59 | `en.yna.co.kr` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 60 | `english.alarabiya.net` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 61 | `english.hani.co.kr` | 0/2 | 1/2 ↑ | OK | FAILED | -- | art, -, -- |
| 62 | `english.kyodonews.net` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 63 | `epl.delfi.ee` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 64 | `epw.in` | 1/3 | 3/3 ↑ | OK | OK | OK | art, art, anlz |
| 65 | `estadao.com.br` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |
| 66 | `ex-ante.cl` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 67 | `expansion.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 68 | `expressen.se` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 69 | `faz.net` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 70 | `filternyheter.no` | 1/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 71 | `folha.uol.com.br` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 72 | `forceindia.net` | 2/3 | 2/3 | OK | OK | FAILED | anlz, anlz, - |
| 73 | `fr.de` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 74 | `france24.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 75 | `ft.com` | 0/3 | 2/3 ↑ | EMPTY | OK | OK | -, art, anlz |
| 76 | `gatewayhouse.in` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, anlz |
| 77 | `gov.br` | 2/3 | 0/3 ↓ | FAILED | FAILED | FAILED | -, -, - |
| 78 | `hbl.fi` | 1/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 79 | `highnorthnews.com` | 1/3 | 1/3 | OK | FAILED | FAILED | art, -, - |
| 80 | `hilltimes.com` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, art |
| 81 | `hindustantimes.com` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 82 | `hn.cz` | 2/3 | 3/3 ↑ | OK | OK | OK | art, art, anlz |
| 83 | `hs.fi` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 84 | `icds.ee` | 1/2 | 0/2 ↓ | FAILED | FAILED | -- | -, -, -- |
| 85 | `indianexpress.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 86 | `indsr.org.tw` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 87 | `insightcrime.org` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 88 | `intelligenceonline.com` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 89 | `ir.lv` | 1/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 90 | `iROZHLAS.cz` | 0/2 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 91 | `is.fi` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 92 | `ispionline.it` | 0/3 | 1/3 ↑ | FAILED | EMPTY | OK | -, -, anlz |
| 93 | `jagran.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 94 | `jakartaglobe.id` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 95 | `japan-forward.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 96 | `japan.kantei.go.jp` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 97 | `kam.lt` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 98 | `kansanuutiset.fi` | 1/2 | 2/2 ↑ | OK | OK | -- | art, anlz, -- |
| 99 | `kauppalehti.fi` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 100 | `klassekampen.no` | 0/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 101 | `koreajoongangdaily.joins.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 102 | `kyivindependent.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 103 | `la-croix.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 104 | `la.lv` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 105 | `lalettre.fr` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 106 | `lavanguardia.com` | 0/3 | 2/3 ↑ | OK | OK | EMPTY | art, art, - |
| 107 | `lefigaro.fr` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 108 | `lemonde.fr` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, art |
| 109 | `leparisien.fr` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 110 | `lesechos.fr` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 111 | `liberation.fr` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 112 | `libertatea.ro` | 0/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 113 | `limesonline.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 114 | `livemint.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 115 | `lopinion.fr` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 116 | `lowyinstitute.org` | 0/1 | 1/1 ↑ | OK | -- | -- | art, --, -- |
| 117 | `lrytas.lt` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, anlz, - |
| 118 | `maaal.com` | 0/1 | 0/1 | EMPTY | -- | -- | -, --, -- |
| 119 | `mediapart.fr` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, anlz |
| 120 | `mexiconewsdaily.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 121 | `minerva.no` | 1/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 122 | `mnd.gov.tw` | 0/2 | 0/2 | FAILED | FAILED | -- | -, -, -- |
| 123 | `mod.go.jp` | 0/1 | 0/1 | FAILED | -- | -- | -, --, -- |
| 124 | `monde-diplomatique.fr` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, art |
| 125 | `morgenbladet.no` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 126 | `n-tv.de` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 127 | `nationalpost.com` | 0/3 | 3/3 ↑ | OK | OK | OK | art, art, art |
| 128 | `neweasterneurope.eu` | 2/3 | 2/3 | FAILED | OK | OK | -, art, art |
| 129 | `news.tvbs.com.tw` | 2/3 | 2/3 | FAILED | OK | OK | -, anlz, art |
| 130 | `nknews.org` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 131 | `nv.ua` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 132 | `oglobo.globo.com` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, anlz |
| 133 | `ohtuleht.ee` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, anlz |
| 134 | `omni.se` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, art |
| 135 | `onet.pl` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |
| 136 | `ouest-france.fr` | 0/3 | 2/3 ↑ | OK | FAILED | OK | anlz, -, art |
| 137 | `pauta.cl` | 2/3 | 2/3 | OK | OK | FAILED | anlz, art, - |
| 138 | `pf.org.tw` | 2/3 | 2/3 | OK | OK | FAILED | art, art, - |
| 139 | `politicaexterior.com` | 2/3 | 2/3 | FAILED | OK | OK | -, anlz, art |
| 140 | `politico.eu` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 141 | `president.gov.ua` | 0/3 | 0/3 | EMPTY | FAILED | EMPTY | -, -, - |
| 142 | `Profit.ro` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 143 | `razumkov.org.ua` | 2/3 | 1/3 ↓ | FAILED | FAILED | OK | -, -, art |
| 144 | `repubblica.it` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 145 | `respekt.cz` | 2/3 | 2/3 | OK | FAILED | OK | art, -, art |
| 146 | `reuters.com` | 0/3 | 1/3 ↑ | OK | FAILED | FAILED | art, -, - |
| 147 | `rp.pl` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 148 | `rus.err.ee` | 2/3 | 2/3 | OK | OK | FAILED | anlz, art, - |
| 149 | `sabq.org` | 0/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 150 | `spf.org` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 151 | `spiegel.de` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 152 | `storm.mg` | 2/3 | 3/3 ↑ | OK | OK | OK | anlz, art, art |
| 153 | `subrei.gob.cl` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, anlz |
| 154 | `sueddeutsche.de` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 155 | `suomenkuvalehti.fi` | 1/3 | 2/3 ↑ | OK | OK | FAILED | anlz, art, - |
| 156 | `svd.se` | 0/3 | 1/3 ↑ | OK | FAILED | FAILED | anlz, -, - |
| 157 | `sydsvenskan.se` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, anlz |
| 158 | `t24.com.tr` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 159 | `tagesspiegel.de` | 2/3 | 2/3 | OK | OK | FAILED | anlz, art, - |
| 160 | `takshashila.org.in` | 0/3 | 0/3 | FAILED | FAILED | FAILED | -, -, - |
| 161 | `talouselama.fi` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, art |
| 162 | `telegraph.co.uk` | 0/3 | 1/3 ↑ | OK | FAILED | FAILED | art, -, - |
| 163 | `thediplomat.com` | 0/3 | 1/3 ↑ | FAILED | FAILED | OK | -, -, art |
| 164 | `theguardian.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, anlz, - |
| 165 | `thehindu.com` | 0/3 | 2/3 ↑ | OK | OK | FAILED | art, art, - |
| 166 | `thenationalnews.com` | 1/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 167 | `thenewslens.com` | 0/3 | 1/3 ↑ | EMPTY | OK | EMPTY | -, art, - |
| 168 | `theprint.in` | 1/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 169 | `thestar.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 170 | `Tirto.id` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, anlz |
| 171 | `tokyo-np.co.jp` | 1/3 | 1/3 | FAILED | FAILED | OK | -, -, art |
| 172 | `tvnet.lv` | 2/3 | 1/3 ↓ | FAILED | FAILED | OK | -, -, art |
| 173 | `ussc.edu.au` | 2/3 | 1/3 ↓ | FAILED | FAILED | OK | -, -, art |
| 174 | `uusisuomi.fi` | 0/3 | 3/3 ↑ | OK | OK | OK | anlz, anlz, art |
| 175 | `valor.globo.com` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, art, anlz |
| 176 | `vz.lt` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 177 | `wam.ae` | 0/1 | 0/1 | EMPTY | -- | -- | -, --, -- |
| 178 | `welt.de` | 0/3 | 2/3 ↑ | FAILED | OK | OK | -, anlz, art |
| 179 | `www3.nhk.or.jp` | 0/3 | 1/3 ↑ | FAILED | OK | FAILED | -, anlz, - |
| 180 | `wyborcza.pl` | 0/3 | 3/3 ↑ | OK | OK | OK | art, anlz, art |
| 181 | `zeit.de` | 0/3 | 2/3 ↑ | OK | FAILED | OK | art, -, art |
| 182 | `zetatijuana.com` | 2/3 | 3/3 ↑ | OK | OK | OK | anlz, art, anlz |

## Domains Rescued by Diffbot (0 on WebFetch → OK on Diffbot)

- `abc.es` (3/3)
- `abc.net.au` (2/3)
- `aftenposten.no` (2/3)
- `aftonbladet.se` (2/3)
- `agenzianova.com` (2/3)
- `agi.it` (3/3)
- `alarabiya.net` (3/3)
- `arabianbusiness.com` (1/3)
- `arabnews.com` (1/3)
- `aripaev.ee` (2/3)
- `asahi.com` (3/3)
- `bbc.co.uk` (3/3)
- `bhaskar.com` (2/3)
- `bnamericas.com` (2/3)
- `canadiandefencereview.com` (3/3)
- `chathamhouse.org` (1/3)
- `chosun.com` (2/3)
- `corriere.it` (3/3)
- `cw.com.tw` (2/3)
- `dagbladet.no` (1/3)
- `defence.gov.au` (3/3)
- `defenceconnect.com.au` (3/3)
- `delfi.ee` (2/3)
- `delfi.lt` (2/3)
- `delfi.lv` (2/3)
- `di.se` (2/3)
- `dn.no` (2/3)
- `dn.se` (2/3)
- `dw.com` (3/3)
- `economictimes.indiatimes.com` (2/3)
- `economist.com` (2/3)
- `efe.com` (1/3)
- `ekspress.delfi.ee` (3/3)
- `elconfidencial.com` (2/3)
- `eleconomista.com.mx` (3/3)
- `eleconomista.es` (1/3)
- `elespanol.com` (3/3)
- `elfinanciero.com.mx` (3/3)
- `elmundo.es` (3/3)
- `elpais.com` (3/3)
- `en.yna.co.kr` (3/3)
- `english.alarabiya.net` (2/3)
- `english.hani.co.kr` (1/2)
- `english.kyodonews.net` (3/3)
- `epl.delfi.ee` (2/3)
- `estadao.com.br` (3/3)
- `ex-ante.cl` (3/3)
- `expansion.com` (3/3)
- `faz.net` (2/3)
- `folha.uol.com.br` (3/3)
- `fr.de` (2/3)
- `france24.com` (3/3)
- `ft.com` (2/3)
- `gatewayhouse.in` (2/3)
- `hilltimes.com` (2/3)
- `hindustantimes.com` (3/3)
- `hs.fi` (3/3)
- `indianexpress.com` (2/3)
- `indsr.org.tw` (3/3)
- `insightcrime.org` (2/3)
- `is.fi` (3/3)
- `ispionline.it` (1/3)
- `jagran.com` (2/3)
- `jakartaglobe.id` (3/3)
- `japan-forward.com` (3/3)
- `japan.kantei.go.jp` (2/3)
- `kauppalehti.fi` (2/3)
- `klassekampen.no` (2/3)
- `koreajoongangdaily.joins.com` (2/3)
- `kyivindependent.com` (3/3)
- `la-croix.com` (2/3)
- `la.lv` (2/3)
- `lavanguardia.com` (2/3)
- `lefigaro.fr` (2/3)
- `lemonde.fr` (1/3)
- `leparisien.fr` (2/3)
- `lesechos.fr` (2/3)
- `libertatea.ro` (2/3)
- `limesonline.com` (2/3)
- `livemint.com` (2/3)
- `lopinion.fr` (2/3)
- `lowyinstitute.org` (1/1)
- `lrytas.lt` (2/3)
- `mediapart.fr` (3/3)
- `mexiconewsdaily.com` (2/3)
- `monde-diplomatique.fr` (2/3)
- `morgenbladet.no` (2/3)
- `n-tv.de` (2/3)
- `nationalpost.com` (3/3)
- `nknews.org` (2/3)
- `oglobo.globo.com` (3/3)
- `ohtuleht.ee` (3/3)
- `omni.se` (2/3)
- `onet.pl` (3/3)
- `ouest-france.fr` (2/3)
- `politico.eu` (2/3)
- `Profit.ro` (2/3)
- `repubblica.it` (2/3)
- `reuters.com` (1/3)
- `rp.pl` (2/3)
- `sabq.org` (2/3)
- `spiegel.de` (2/3)
- `subrei.gob.cl` (1/3)
- `sueddeutsche.de` (2/3)
- `svd.se` (1/3)
- `sydsvenskan.se` (3/3)
- `t24.com.tr` (3/3)
- `talouselama.fi` (2/3)
- `telegraph.co.uk` (1/3)
- `thediplomat.com` (1/3)
- `theguardian.com` (2/3)
- `thehindu.com` (2/3)
- `thenewslens.com` (1/3)
- `thestar.com` (2/3)
- `Tirto.id` (2/3)
- `uusisuomi.fi` (3/3)
- `valor.globo.com` (2/3)
- `vz.lt` (2/3)
- `welt.de` (2/3)
- `www3.nhk.or.jp` (1/3)
- `wyborcza.pl` (3/3)
- `zeit.de` (2/3)

## Still Inaccessible (0 OK on both WebFetch and Diffbot)

- `alriyadh.com`
- `cigionline.org`
- `cincodias.elpais.com`
- `dgap.org`
- `eastasiaforum.org`
- `expressen.se`
- `intelligenceonline.com`
- `iROZHLAS.cz`
- `kam.lt`
- `lalettre.fr`
- `liberation.fr`
- `maaal.com`
- `mnd.gov.tw`
- `mod.go.jp`
- `nv.ua`
- `president.gov.ua`
- `spf.org`
- `takshashila.org.in`
- `wam.ae`