# Goggle audit — 20260322 + 20260329 + 20260405 + 20260412

Aggregate of 4 weekly story_map runs (29 countries). For each (country, domain), counts URLs sent to story_map vs URLs that survived in the LLM's stories/single_source/unassigned output. Diff = URLs the LLM rejected as noise. Thresholds for surfacing candidates: drop-rate ≥ 80% AND ≥ 30 items (domains) / ≥ 20 items (paths).

Production filters in effect during these runs (where deployed): `_global_discards.txt` (34 domains), per-country goggle `$discard`, `off_topic_filters.csv` (29 rules). Discard leaks below should be ≈0 for runs ≥ 2026-05-11.

## Cross-country noise domains (discard candidates)

Domains that appear in ≥2 countries with high drop rate. Add to `_global_discards.txt` if the noise is structural (off-topic / spam / wrong-language / non-news). Domains touching a single country are listed in that country's section below.

| Domain | Input | Kept | Drop % | Countries |
|---|---:|---:|---:|---:|
| timesofindia.indiatimes.com | 275 | 48 | 83% | 21 |
| yle.fi | 253 | 47 | 81% | 3 |
| aftonbladet.se | 188 | 31 | 84% | 2 |
| cbc.ca | 170 | 28 | 84% | 9 |
| infobae.com | 162 | 14 | 91% | 19 |
| welt.de | 107 | 12 | 89% | 6 |
| theglobeandmail.com | 95 | 19 | 80% | 16 |
| thehindu.com | 88 | 17 | 81% | 16 |
| nation.com.pk | 88 | 5 | 94% | 7 |
| economictimes.indiatimes.com | 87 | 9 | 90% | 16 |
| indianexpress.com | 82 | 13 | 84% | 15 |
| en.interfax.com.ua | 76 | 15 | 80% | 4 |
| mirror.co.uk | 76 | 9 | 88% | 10 |
| gbnews.com | 73 | 12 | 84% | 16 |
| newsweek.com | 67 | 5 | 93% | 22 |
| bild.de | 67 | 12 | 82% | 6 |
| threads.com | 67 | 4 | 94% | 18 |
| globenewswire.com | 64 | 4 | 94% | 12 |
| n-tv.de | 64 | 5 | 92% | 4 |
| express.co.uk | 63 | 6 | 90% | 9 |
| t-online.de | 60 | 7 | 88% | 8 |
| elespanol.com | 59 | 9 | 85% | 11 |
| politico.com | 59 | 5 | 92% | 14 |
| zeit.de | 56 | 8 | 86% | 4 |
| ad-hoc-news.de | 56 | 3 | 95% | 16 |
| tagesspiegel.de | 52 | 4 | 92% | 3 |
| foxnews.com | 51 | 3 | 94% | 16 |
| npr.org | 50 | 3 | 94% | 15 |
| euronews.com | 50 | 6 | 88% | 16 |
| sueddeutsche.de | 50 | 6 | 88% | 5 |
| investing.com | 47 | 5 | 89% | 22 |
| faz.net | 46 | 2 | 96% | 7 |
| eleconomista.com.mx | 46 | 2 | 96% | 5 |
| nbcnews.com | 45 | 7 | 84% | 12 |
| milenio.com | 45 | 7 | 84% | 8 |
| lavanguardia.com | 44 | 4 | 91% | 9 |
| bbc.co.uk | 43 | 3 | 93% | 14 |
| lapresse.ca | 43 | 4 | 91% | 3 |
| cronista.com | 42 | 1 | 98% | 7 |
| tempo.co | 42 | 7 | 83% | 2 |

## Cross-country noise paths (off_topic_filters.csv candidates)

(domain, path-prefix) combos where the LLM drops most URLs. Strong candidates for adding to `off_topic_filters.csv`. Already-covered rows are flagged so you can ignore them.

| Domain | Path | Input | Kept | Drop % | Countries | Already covered |
|---|---|---:|---:|---:|---:|:---:|
| cbc.ca | /news/ | 161 | 28 | 83% | 9 |  |
| aftonbladet.se | /nyheter/ | 159 | 25 | 84% | 2 |  |
| welt.de | /politik/ | 89 | 11 | 88% | 3 |  |
| indianexpress.com | /article/ | 82 | 13 | 84% | 15 |  |
| yle.fi | /uutiset/ | 81 | 1 | 99% | 2 |  |
| en.interfax.com.ua | /news/ | 76 | 15 | 80% | 4 |  |
| globenewswire.com | /news-release/ | 64 | 4 | 94% | 12 |  |
| mirror.co.uk | /news/ | 64 | 8 | 88% | 8 |  |
| economictimes.indiatimes.com | /news/ | 56 | 8 | 86% | 11 |  |
| bild.de | /politik/ | 53 | 10 | 81% | 3 |  |
| t-online.de | /nachrichten/ | 52 | 7 | 87% | 5 |  |
| ad-hoc-news.de | /boerse/ | 52 | 3 | 94% | 16 | ✓ |
| npr.org | /2026/ | 49 | 2 | 96% | 15 |  |
| investing.com | /news/ | 44 | 5 | 89% | 22 |  |
| timesofindia.indiatimes.com | /city/ | 43 | 3 | 93% | 9 | ✓ |
| starnewskorea.com | /en/ | 43 | 2 | 95% | 3 |  |
| infobae.com | /mexico/ | 43 | 6 | 86% | 4 |  |
| n-tv.de | /politik/ | 42 | 4 | 90% | 2 |  |
| ilgiornale.it | /news/ | 42 | 7 | 83% | 1 |  |
| faz.net | /aktuell/ | 41 | 2 | 95% | 7 |  |
| politico.com | /news/ | 41 | 2 | 95% | 12 |  |
| m.echo24.cz | /a/ | 41 | 4 | 90% | 1 |  |
| zeit.de | /politik/ | 40 | 6 | 85% | 2 |  |
| news.online.ua | /en/ | 40 | 6 | 85% | 1 |  |
| bbc.co.uk | /news/ | 39 | 3 | 92% | 12 |  |
| sueddeutsche.de | /politik/ | 39 | 6 | 85% | 2 |  |
| pakistantoday.com.pk | /2026/ | 39 | 7 | 82% | 6 |  |
| jauns.lv | /raksts/ | 38 | 7 | 82% | 1 |  |
| prnewswire.com | /news-releases/ | 37 | 0 | 100% | 16 |  |
| hindustantimes.com | /world-news/ | 37 | 4 | 89% | 7 |  |
| timesofindia.indiatimes.com | /world/ | 37 | 5 | 86% | 10 |  |
| pbs.org | /newshour/ | 36 | 5 | 86% | 14 |  |
| dailypolitical.com | /2026/ | 36 | 0 | 100% | 15 |  |
| lapresse.ca | /actualites/ | 35 | 4 | 89% | 1 |  |
| en.namu.wiki | /w/ | 35 | 0 | 100% | 10 |  |
| express.co.uk | /news/ | 35 | 2 | 94% | 6 |  |
| digi24.ro | /stiri/ | 34 | 6 | 82% | 4 |  |
| tagesspiegel.de | /politik/ | 33 | 3 | 91% | 1 |  |
| tradingview.com | /news/ | 32 | 4 | 88% | 11 |  |
| uusisuomi.fi | /uutiset/ | 32 | 5 | 84% | 1 |  |
| timesofindia.indiatimes.com | /videos/ | 31 | 6 | 81% | 7 |  |
| ici.radio-canada.ca | /nouvelle/ | 31 | 4 | 87% | 2 |  |
| infodefensa.com | /texto-diario/ | 31 | 3 | 90% | 4 |  |
| infobae.com | /america/ | 31 | 3 | 90% | 12 |  |
| themarketsdaily.com | /2026/ | 30 | 0 | 100% | 12 |  |
| businessinsider.com.pl | /gospodarka/ | 30 | 6 | 80% | 1 |  |
| ukrinform.net | /rubric-ato/ | 29 | 5 | 83% | 5 |  |
| euronews.com | /2026/ | 29 | 4 | 86% | 13 |  |
| merkur.de | /politik/ | 29 | 1 | 97% | 1 |  |
| aol.com | /articles/ | 29 | 1 | 97% | 13 |  |
| cornucopia.se | /2026/ | 29 | 0 | 100% | 5 |  |
| ndtv.com | /world-news/ | 29 | 4 | 86% | 10 |  |
| m.economictimes.com | /news/ | 28 | 4 | 86% | 4 |  |
| radaronline.com | /p/ | 28 | 0 | 100% | 2 |  |
| latercera.com | /nacional/ | 27 | 3 | 89% | 2 |  |
| manilatimes.net | /2026/ | 27 | 0 | 100% | 15 |  |
| marketscreener.com | /news/ | 27 | 2 | 93% | 10 |  |
| estonia.news-pravda.com | /world/ | 27 | 5 | 81% | 1 |  |
| gbnews.com | /politics/ | 27 | 3 | 89% | 5 |  |
| sports.yahoo.com | /articles/ | 27 | 0 | 100% | 15 |  |

## Per-country breakdown

### AE  (1,153 items / 4 runs, 20% boosted, 28 $boost · 3 $discard in goggle)

⚠️  **58 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| cryptoverselawyers.io | 24 | 0 | 100% ⚠ already discarded |
| enterpriseam.com | 15 | 1 | 93% |
| mofa.gov.ae | 14 | 5 | 64% |
| it-boltwise.de | 14 | 0 | 100% ⚠ already discarded |
| sharjah24.ae | 13 | 4 | 69% |
| timesofindia.indiatimes.com | 13 | 2 | 85% |
| indianexpress.com | 12 | 0 | 100% |
| zawya.com | 11 | 3 | 73% |
| voiceofemirates.com | 11 | 1 | 91% |
| tradingview.com | 9 | 1 | 89% |
| economymiddleeast.com | 9 | 2 | 78% |
| economictimes.indiatimes.com | 9 | 0 | 100% |
| hindustantimes.com | 8 | 2 | 75% |
| moneytimes.com.br | 7 | 0 | 100% |
| gulfbusiness.com | 7 | 1 | 86% |

### AU  (1,171 items / 4 runs, 28% boosted, 27 $boost · 4 $discard in goggle)

⚠️  **60 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| dailymail.co.uk | 37 | 18 | 51% ⚠ already discarded |
| rba.gov.au | 11 | 5 | 55% |
| 20minutes.fr | 10 | 0 | 100% |
| timesofindia.indiatimes.com | 8 | 1 | 88% |
| latimes.com | 8 | 0 | 100% |
| canberratimes.com.au | 7 | 4 | 43% |
| tomsguide.com | 7 | 0 | 100% |
| investing.com | 6 | 0 | 100% |
| finance.yahoo.com | 6 | 0 | 100% |
| prismnews.com | 6 | 0 | 100% |
| economictimes.indiatimes.com | 6 | 0 | 100% |
| independent.co.uk | 5 | 2 | 60% |
| 7news.com.au | 5 | 2 | 60% |
| theglobeandmail.com | 5 | 0 | 100% |
| news.bloomberglaw.com | 5 | 0 | 100% |

### BR  (1,342 items / 4 runs, 35% boosted, 30 $boost · 3 $discard in goggle)

⚠️  **30 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| em.com.br | 57 | 32 | 44% |
| g1.globo.com | 46 | 24 | 48% |
| sociedademilitar.com.br | 27 | 6 | 78% |
| noticias.uol.com.br | 21 | 14 | 33% |
| terra.com.br | 17 | 7 | 59% |
| ocafezinho.com | 15 | 8 | 47% |
| jovempan.com.br | 12 | 7 | 42% |
| revistaforum.com.br | 11 | 6 | 45% |
| diariodocentrodomundo.com.br | 11 | 5 | 55% |
| correiobraziliense.com.br | 11 | 5 | 55% |
| vamoscruzazul.bolavip.com | 11 | 0 | 100% |
| brasil247.com | 10 | 5 | 50% ⚠ already discarded |
| oantagonista.com.br | 10 | 3 | 70% |
| ndmais.com.br | 10 | 2 | 80% |
| clickpetroleoegas.com.br | 10 | 1 | 90% |

### CA  (1,326 items / 4 runs, 43% boosted, 24 $boost · 6 $discard in goggle)

⚠️  **58 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| financialpost.com | 18 | 4 | 78% |
| torontosun.com | 15 | 4 | 73% ⚠ already discarded |
| ca.finance.yahoo.com | 15 | 3 | 80% |
| conservative.ca | 13 | 2 | 85% |
| goal.com | 11 | 0 | 100% ⚠ already discarded |
| newswire.ca | 10 | 2 | 80% |
| abc.net.au | 10 | 0 | 100% |
| ca.news.yahoo.com | 9 | 0 | 100% |
| moroccoworldnews.com | 9 | 0 | 100% |
| policymagazine.ca | 8 | 2 | 75% |
| castanet.net | 8 | 1 | 88% |
| foot-africa.com | 8 | 0 | 100% |
| vancouversun.com | 8 | 0 | 100% |
| thehub.ca | 7 | 2 | 71% |
| narcity.com | 7 | 2 | 71% ⚠ already discarded |

### CL  (1,287 items / 4 runs, 36% boosted, 27 $boost · 2 $discard in goggle)

⚠️  **24 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| alairelibre.cl | 19 | 0 | 100% |
| cronista.com | 19 | 0 | 100% |
| t13.cl | 17 | 6 | 65% |
| zona-militar.com | 16 | 3 | 81% |
| poder360.com.br | 14 | 0 | 100% |
| redimin.cl | 14 | 4 | 71% |
| puranoticia.pnt.cl | 12 | 9 | 25% |
| theclinic.cl | 11 | 3 | 73% |
| redgol.cl | 10 | 0 | 100% |
| radio.uchile.cl | 10 | 4 | 60% |
| g1.globo.com | 9 | 0 | 100% |
| voz.us | 9 | 0 | 100% |
| elciudadano.com | 8 | 2 | 75% ⚠ already discarded |
| elcomercio.pe | 8 | 0 | 100% |
| elespanol.com | 8 | 0 | 100% |

### CZ  (1,156 items / 4 runs, 13% boosted, 26 $boost · 4 $discard in goggle)

⚠️  **86 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| m.echo24.cz | 41 | 4 | 90% |
| parlamentnilisty.cz | 28 | 4 | 86% ⚠ already discarded |
| echo24.cz | 18 | 2 | 89% |
| forum24.cz | 16 | 5 | 69% |
| spravy.pravda.sk | 16 | 2 | 88% |
| aktuality.sk | 16 | 2 | 88% |
| blesk.cz | 14 | 4 | 71% ⚠ already discarded |
| czdefence.cz | 13 | 0 | 100% |
| revistaquem.globo.com | 12 | 0 | 100% |
| eurozpravy.cz | 12 | 5 | 58% |
| terra.com.br | 9 | 0 | 100% |
| infobae.com | 9 | 0 | 100% |
| expats.cz | 9 | 0 | 100% |
| ekonomickydenik.cz | 9 | 2 | 78% |
| startitup.sk | 8 | 0 | 100% |

### DE  (1,357 items / 4 runs, 55% boosted, 32 $boost · 6 $discard in goggle)

⚠️  **90 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| bild.de | 55 | 12 | 78% ⚠ already discarded |
| zdfheute.de | 27 | 1 | 96% |
| stern.de | 22 | 3 | 86% |
| unsere-zeit.de | 19 | 0 | 100% |
| berliner-zeitung.de | 14 | 3 | 79% |
| morgenpost.de | 13 | 0 | 100% |
| ad-hoc-news.de | 11 | 0 | 100% |
| br.de | 10 | 0 | 100% |
| jungefreiheit.de | 10 | 2 | 80% ⚠ already discarded |
| deutschland.de | 10 | 0 | 100% |
| swr.de | 10 | 2 | 80% |
| web.de | 9 | 1 | 89% |
| boerse.de | 9 | 0 | 100% |
| tichyseinblick.de | 8 | 0 | 100% |
| nordkurier.de | 8 | 0 | 100% |

### EE  (1,399 items / 4 runs, 28% boosted, 20 $boost · 4 $discard in goggle)

⚠️  **204 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| estonia.news-pravda.com | 90 | 23 | 74% |
| uueduudised.ee | 81 | 33 | 59% ⚠ already discarded |
| mil.ee | 56 | 2 | 96% |
| lounaeestlane.ee | 19 | 4 | 79% |
| edf.fr | 19 | 0 | 100% |
| news.maxifoot.fr | 18 | 0 | 100% |
| uudis.net | 18 | 2 | 89% |
| pudelek.pl | 11 | 0 | 100% |
| independent.co.uk | 11 | 0 | 100% |
| mirror.co.uk | 10 | 0 | 100% |
| globenewswire.com | 10 | 2 | 80% |
| kaitseliit.ee | 9 | 2 | 78% |
| dailyrecord.co.uk | 8 | 0 | 100% |
| thenational.scot | 8 | 0 | 100% |
| adaur.ee | 8 | 1 | 88% |

### ES  (1,277 items / 4 runs, 35% boosted, 27 $boost · 4 $discard in goggle)

⚠️  **64 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| eldebate.com | 34 | 10 | 71% |
| libertaddigital.com | 27 | 4 | 85% |
| okdiario.com | 24 | 3 | 88% ⚠ already discarded |
| lasexta.com | 24 | 7 | 71% |
| infobae.com | 19 | 3 | 84% |
| theobjective.com | 17 | 7 | 59% |
| pressdigital.es | 17 | 7 | 59% |
| elperiodico.com | 16 | 2 | 88% |
| elconfidencialdigital.com | 15 | 8 | 47% |
| elindependiente.com | 15 | 6 | 60% |
| spain.news-pravda.com | 11 | 0 | 100% |
| esdiario.com | 10 | 4 | 60% |
| cadenaser.com | 10 | 1 | 90% |
| lne.es | 10 | 2 | 80% |
| lavozdegalicia.es | 9 | 3 | 67% |

### FI  (1,347 items / 4 runs, 46% boosted, 23 $boost · 0 $discard in goggle)

⚠️  **13 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| is.fi | 142 | 59 | 58% |
| sss.fi | 40 | 14 | 65% |
| maaseuduntulevaisuus.fi | 29 | 9 | 69% |
| demokraatti.fi | 15 | 6 | 60% |
| suomenmaa.fi | 14 | 6 | 57% |
| suomenuutiset.fi | 13 | 2 | 85% |
| tekniikkatalous.fi | 13 | 4 | 69% |
| vauva.fi | 11 | 2 | 82% |
| finland.news-pravda.com | 9 | 0 | 100% |
| ts.fi | 7 | 3 | 57% |
| ku.fi | 7 | 1 | 86% |
| uudenmaankokoomus.fi | 7 | 1 | 86% |
| ksml.fi | 7 | 1 | 86% |
| puolustusvoimat.fi | 7 | 2 | 71% |
| savonsanomat.fi | 6 | 1 | 83% |

### FR  (1,189 items / 4 runs, 45% boosted, 31 $boost · 5 $discard in goggle)

⚠️  **65 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| ouest-france.fr | 43 | 12 | 72% |
| actu.orange.fr | 26 | 6 | 77% |
| huffingtonpost.fr | 24 | 17 | 29% |
| gala.fr | 22 | 8 | 64% ⚠ already discarded |
| actu.fr | 19 | 3 | 84% |
| sudouest.fr | 18 | 7 | 61% |
| rtl.fr | 16 | 9 | 44% |
| lejdd.fr | 13 | 4 | 69% |
| closermag.fr | 13 | 1 | 92% ⚠ already discarded |
| tf1info.fr | 12 | 4 | 67% |
| cnews.fr | 12 | 2 | 83% ⚠ already discarded |
| bvoltaire.fr | 11 | 4 | 64% |
| lexpress.fr | 10 | 1 | 90% |
| challenges.fr | 10 | 3 | 70% |
| francebleu.fr | 10 | 1 | 90% |

### GB  (1,424 items / 4 runs, 22% boosted, 23 $boost · 6 $discard in goggle)

⚠️  **264 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| dailymail.co.uk | 66 | 22 | 67% ⚠ already discarded |
| express.co.uk | 48 | 6 | 88% ⚠ already discarded |
| gbnews.com | 44 | 9 | 80% ⚠ already discarded |
| mirror.co.uk | 42 | 8 | 81% ⚠ already discarded |
| people.com | 17 | 3 | 82% ⚠ already discarded |
| yahoo.com | 16 | 0 | 100% |
| standard.co.uk | 15 | 4 | 73% |
| onaquietday.org | 15 | 0 | 100% ⚠ already discarded |
| aol.com | 14 | 2 | 86% |
| news.sky.com | 13 | 3 | 77% |
| cityam.com | 13 | 5 | 62% |
| britbrief.co.uk | 13 | 0 | 100% ⚠ already discarded |
| bankofengland.co.uk | 13 | 0 | 100% |
| instyle.com | 10 | 4 | 60% |
| hellomagazine.com | 9 | 3 | 67% |

### ID  (1,297 items / 4 runs, 30% boosted, 31 $boost · 3 $discard in goggle)

⚠️  **31 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| news.detik.com | 32 | 12 | 62% |
| mirror.co.uk | 13 | 0 | 100% |
| latercera.com | 13 | 0 | 100% |
| golkarpedia.com | 12 | 0 | 100% |
| metrotvnews.com | 9 | 3 | 67% |
| cbc.ca | 9 | 0 | 100% |
| finance.detik.com | 9 | 1 | 89% |
| gelora.co | 9 | 1 | 89% |
| detik.com | 8 | 1 | 88% |
| merdeka.com | 8 | 2 | 75% ⚠ already discarded |
| bloombergtechnoz.com | 8 | 3 | 62% |
| saltwire.com | 8 | 0 | 100% |
| nasional.sindonews.com | 8 | 3 | 62% |
| suara.com | 7 | 3 | 57% ⚠ already discarded |
| infobanknews.com | 7 | 1 | 86% |

### IN  (1,305 items / 4 runs, 28% boosted, 28 $boost · 4 $discard in goggle)

⚠️  **42 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| timesofindia.indiatimes.com | 128 | 40 | 69% |
| ndtv.com | 31 | 19 | 39% |
| news18.com | 31 | 12 | 61% |
| indiatoday.in | 22 | 11 | 50% |
| idrw.org | 18 | 3 | 83% |
| dosisfutbolera.com | 17 | 0 | 100% ⚠ already discarded |
| news.webindia123.com | 16 | 5 | 69% |
| newkerala.com | 15 | 5 | 67% |
| newindianexpress.com | 14 | 6 | 57% |
| m.economictimes.com | 14 | 2 | 86% |
| dailypioneer.com | 12 | 4 | 67% |
| timesnownews.com | 11 | 5 | 55% ⚠ already discarded |
| english.mathrubhumi.com | 11 | 1 | 91% |
| bankersadda.com | 11 | 0 | 100% |
| moneycontrol.com | 10 | 4 | 60% |

### IT  (1,367 items / 4 runs, 42% boosted, 30 $boost · 4 $discard in goggle)

⚠️  **13 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| ilgiornale.it | 42 | 7 | 83% |
| ilfoglio.it | 17 | 5 | 71% |
| adnkronos.com | 16 | 8 | 50% |
| today.it | 16 | 5 | 69% |
| fanpage.it | 16 | 5 | 69% |
| virgilio.it | 14 | 5 | 64% |
| tgcom24.mediaset.it | 13 | 10 | 23% |
| agenziagiornalisticaopinione.it | 13 | 2 | 85% |
| zazoom.it | 12 | 0 | 100% |
| askanews.it | 11 | 2 | 82% |
| affaritaliani.it | 11 | 3 | 73% |
| ilpost.it | 11 | 4 | 64% |
| huffingtonpost.it | 11 | 4 | 64% |
| laverita.info | 9 | 1 | 89% |
| quotidiano.net | 9 | 3 | 67% |

### JP  (1,019 items / 4 runs, 21% boosted, 30 $boost · 3 $discard in goggle)

⚠️  **42 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| asahi.com | 17 | 13 | 24% |
| telegrafi.com | 15 | 0 | 100% |
| timesofindia.indiatimes.com | 11 | 0 | 100% |
| rijnmond.nl | 11 | 0 | 100% |
| npr.org | 8 | 0 | 100% |
| gala.fr | 8 | 0 | 100% |
| radiokosovaelire.com | 8 | 0 | 100% |
| pbs.org | 6 | 0 | 100% |
| veriu.info | 6 | 0 | 100% |
| fr12.nl | 6 | 0 | 100% |
| fcupdate.nl | 6 | 0 | 100% |
| ameblo.jp | 5 | 1 | 80% |
| mainichi.jp | 5 | 3 | 40% |
| naruto.fandom.com | 5 | 0 | 100% |
| economictimes.indiatimes.com | 5 | 0 | 100% |

### KR  (1,298 items / 4 runs, 35% boosted, 31 $boost · 2 $discard in goggle)

⚠️  **47 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| starnewskorea.com | 29 | 2 | 93% ⚠ already discarded |
| kapanlagi.com | 22 | 0 | 100% |
| en.namu.wiki | 19 | 0 | 100% |
| newsweek.com | 11 | 0 | 100% |
| timesofindia.indiatimes.com | 9 | 0 | 100% |
| en.bloomingbit.io | 9 | 5 | 44% |
| forbes.com | 9 | 2 | 78% |
| hvg.hu | 8 | 0 | 100% |
| dvidshub.net | 8 | 0 | 100% |
| military.com | 8 | 0 | 100% |
| nation.com.pk | 8 | 0 | 100% |
| independent.co.uk | 7 | 0 | 100% |
| phonearena.com | 7 | 1 | 86% |
| telex.hu | 6 | 0 | 100% |
| understandingwar.org | 6 | 0 | 100% |

### LT  (1,208 items / 4 runs, 47% boosted, 22 $boost · 4 $discard in goggle)

⚠️  **119 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| lt.news-pravda.com | 80 | 18 | 78% |
| respublika.lt | 17 | 5 | 71% ⚠ already discarded |
| lsdp.lt | 15 | 0 | 100% |
| lrytas.lt | 14 | 7 | 50% |
| globenewswire.com | 14 | 2 | 86% |
| laikas.lt | 11 | 3 | 73% |
| invenglobal.com | 10 | 0 | 100% |
| aina.lt | 9 | 5 | 44% |
| madeinvilnius.lt | 9 | 2 | 78% |
| reform.news | 9 | 2 | 78% |
| team-aaa.com | 9 | 0 | 100% |
| kauno.diena.lt | 8 | 4 | 50% |
| vsd.fr | 8 | 0 | 100% |
| sb.by | 8 | 0 | 100% |
| alkas.lt | 7 | 1 | 86% |

### LV  (1,217 items / 4 runs, 38% boosted, 24 $boost · 1 $discard in goggle)

⚠️  **90 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| latvia.news-pravda.com | 40 | 8 | 80% |
| jv.dk | 29 | 0 | 100% |
| nbssport.co.ug | 19 | 0 | 100% ⚠ already discarded |
| tv3.lv | 12 | 6 | 50% |
| bnn-news.com | 9 | 7 | 22% |
| ozbargain.com.au | 9 | 0 | 100% |
| foxnews.com | 8 | 0 | 100% |
| informer.rs | 8 | 0 | 100% |
| alo.rs | 7 | 0 | 100% |
| timesofindia.indiatimes.com | 7 | 1 | 86% |
| dzentlmenis.lv | 6 | 6 | 0% |
| si.com | 6 | 0 | 100% ⚠ already discarded |
| sports.yahoo.com | 6 | 0 | 100% ⚠ already discarded |
| bieb.knab.nl | 6 | 0 | 100% |
| newsweek.com | 6 | 0 | 100% |

### MX  (1,377 items / 4 runs, 37% boosted, 31 $boost · 4 $discard in goggle)

⚠️  **38 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| elimparcial.com | 17 | 1 | 94% |
| diario.mx | 16 | 0 | 100% |
| informador.mx | 15 | 1 | 93% |
| as.com | 14 | 0 | 100% |
| marca.com | 13 | 0 | 100% ⚠ already discarded |
| eldiariodechihuahua.mx | 12 | 0 | 100% |
| mipuntodevista.com.mx | 11 | 0 | 100% |
| lasillarota.com | 11 | 3 | 73% |
| mundodeportivo.com | 9 | 0 | 100% ⚠ already discarded |
| politica.expansion.mx | 9 | 2 | 78% |
| nmas.com.mx | 8 | 1 | 88% |
| elnacional.cat | 8 | 0 | 100% |
| forbes.com.mx | 8 | 2 | 75% |
| periodicocorreo.com.mx | 8 | 0 | 100% |
| unotv.com | 7 | 1 | 86% |

### NO  (1,362 items / 4 runs, 27% boosted, 25 $boost · 3 $discard in goggle)

⚠️  **187 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| sagat.no | 120 | 2 | 98% ⚠ already discarded |
| inyheter.no | 29 | 11 | 62% |
| adressa.no | 19 | 6 | 68% |
| forsvaret.no | 18 | 3 | 83% |
| ad-hoc-news.de | 18 | 2 | 89% |
| sol.no | 16 | 6 | 62% |
| dailypolitical.com | 16 | 0 | 100% ⚠ already discarded |
| bt.no | 15 | 5 | 67% |
| abcnyheter.no | 14 | 2 | 86% |
| themarketsdaily.com | 14 | 0 | 100% |
| defenseworld.net | 14 | 0 | 100% |
| document.no | 11 | 5 | 55% |
| smp.no | 11 | 2 | 82% |
| tickerreport.com | 10 | 0 | 100% ⚠ already discarded |
| dr.dk | 9 | 0 | 100% |

### PK  (1,415 items / 4 runs, 24% boosted, 37 $boost · 4 $discard in goggle)

⚠️  **29 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| timesofindia.indiatimes.com | 30 | 1 | 97% |
| hindustantimes.com | 23 | 1 | 96% |
| moneycontrol.com | 22 | 8 | 64% |
| news18.com | 22 | 4 | 82% |
| indiatoday.in | 20 | 5 | 75% |
| ndtv.com | 19 | 2 | 89% |
| threads.com | 18 | 0 | 100% |
| dailyparliamenttimes.com | 12 | 0 | 100% |
| tribuneindia.com | 12 | 2 | 83% |
| theprint.in | 11 | 2 | 82% |
| minutemirror.com.pk | 11 | 1 | 91% |
| openpr.com | 11 | 0 | 100% |
| en.sedaily.com | 11 | 0 | 100% |
| news.abplive.com | 10 | 1 | 90% |
| lavanguardia.com | 10 | 0 | 100% |

### PL  (1,316 items / 4 runs, 52% boosted, 33 $boost · 4 $discard in goggle)

⚠️  **64 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| fakt.pl | 41 | 12 | 71% ⚠ already discarded |
| bankier.pl | 26 | 3 | 88% |
| newsweek.pl | 24 | 8 | 67% |
| goniec.pl | 19 | 2 | 89% |
| wprost.pl | 18 | 8 | 56% |
| przegladsportowy.onet.pl | 15 | 4 | 73% |
| onet.pl | 13 | 3 | 77% |
| wiadomosci.dziennik.pl | 12 | 6 | 50% |
| sport.interia.pl | 12 | 1 | 92% |
| portalsamorzadowy.pl | 10 | 3 | 70% |
| nczas.info | 10 | 0 | 100% |
| wiadomosci.radiozet.pl | 9 | 2 | 78% |
| sportowefakty.wp.pl | 8 | 0 | 100% |
| konfederacja.pl | 8 | 0 | 100% |
| polskieradio24.pl | 8 | 2 | 75% |

### RO  (1,423 items / 4 runs, 20% boosted, 27 $boost · 4 $discard in goggle)

⚠️  **114 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| antena3.ro | 25 | 9 | 64% ⚠ already discarded |
| cotidianul.ro | 21 | 12 | 43% |
| romaniatv.net | 20 | 8 | 60% ⚠ already discarded |
| mediafax.ro | 16 | 6 | 62% |
| bnr.nl | 16 | 0 | 100% |
| observatornews.ro | 15 | 8 | 47% |
| battinews.com | 15 | 0 | 100% ⚠ already discarded |
| timesofindia.indiatimes.com | 13 | 1 | 92% |
| playtech.ro | 13 | 1 | 92% |
| jurnalul.ro | 12 | 3 | 75% |
| stirileprotv.ro | 12 | 3 | 75% |
| metropoles.com | 11 | 0 | 100% |
| jornaldocomercio.com | 10 | 0 | 100% |
| realitatea.net | 10 | 2 | 80% ⚠ already discarded |
| capital.ro | 10 | 4 | 60% |

### SA  (1,371 items / 4 runs, 13% boosted, 23 $boost · 3 $discard in goggle)

⚠️  **35 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| timesofindia.indiatimes.com | 25 | 2 | 92% |
| arabnews.pk | 19 | 8 | 58% |
| hindustantimes.com | 19 | 1 | 95% |
| houseofsaud.com | 18 | 5 | 72% |
| indianexpress.com | 14 | 0 | 100% |
| gulfnews.com | 12 | 0 | 100% |
| jpost.com | 9 | 1 | 89% |
| news18.com | 8 | 0 | 100% |
| timesofisrael.com | 7 | 3 | 57% |
| voiceofemirates.com | 7 | 1 | 86% |
| marketscreener.com | 7 | 0 | 100% |
| laprovence.com | 7 | 0 | 100% |
| latinatu.it | 7 | 0 | 100% |
| indiatoday.in | 6 | 0 | 100% |
| timesnownews.com | 6 | 0 | 100% |

### SE  (1,341 items / 4 runs, 41% boosted, 25 $boost · 3 $discard in goggle)

⚠️  **35 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| placera.se | 17 | 1 | 94% |
| yle.fi | 15 | 1 | 93% |
| cornucopia.se | 14 | 0 | 100% |
| efn.se | 11 | 3 | 73% |
| globenewswire.com | 11 | 0 | 100% |
| fxstreet.com | 10 | 1 | 90% |
| sydostran.se | 9 | 1 | 89% |
| etc.se | 9 | 2 | 78% |
| sweden.news-pravda.com | 9 | 0 | 100% |
| goal.com | 8 | 0 | 100% ⚠ already discarded |
| marcusoscarsson.se | 7 | 0 | 100% |
| thelocal.se | 7 | 1 | 86% |
| bulletin.nu | 7 | 4 | 43% |
| sydkusten.es | 7 | 0 | 100% |
| sports.yahoo.com | 6 | 0 | 100% ⚠ already discarded |

### TR  (1,377 items / 4 runs, 25% boosted, 30 $boost · 6 $discard in goggle)

⚠️  **142 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| sabah.com.tr | 34 | 9 | 74% ⚠ already discarded |
| haber7.com | 27 | 9 | 67% ⚠ already discarded |
| ahaber.com.tr | 23 | 8 | 65% ⚠ already discarded |
| aa.com.tr | 20 | 7 | 65% |
| haberler.com | 18 | 6 | 67% |
| odatv.com | 17 | 3 | 82% ⚠ already discarded |
| sondakika.com | 15 | 7 | 53% |
| takvim.com.tr | 15 | 3 | 80% ⚠ already discarded |
| yenicaggazetesi.com | 14 | 3 | 79% |
| tgrthaber.com | 13 | 1 | 92% |
| nefes.com.tr | 13 | 2 | 85% |
| yenisafak.com | 12 | 4 | 67% |
| thehindu.com | 12 | 0 | 100% |
| haber.mynet.com | 12 | 5 | 58% |
| babaocagi.com.tr | 11 | 2 | 82% |

### TW  (1,371 items / 4 runs, 17% boosted, 24 $boost · 2 $discard in goggle)

⚠️  **79 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| cbc.ca | 76 | 0 | 100% |
| starnewskorea.com | 35 | 0 | 100% ⚠ already discarded |
| radaronline.com | 25 | 0 | 100% |
| vnexpress.net | 16 | 0 | 100% |
| scmp.com | 15 | 2 | 87% |
| english.news.cn | 14 | 4 | 71% |
| dailymail.co.uk | 14 | 0 | 100% |
| nzherald.co.nz | 12 | 0 | 100% |
| usmagazine.com | 12 | 0 | 100% |
| newsable.asianetnews.com | 10 | 5 | 50% |
| military.com | 9 | 0 | 100% |
| rnz.co.nz | 9 | 0 | 100% |
| ca.news.yahoo.com | 9 | 0 | 100% |
| vietgiaitri.com | 8 | 0 | 100% |
| newsweek.com | 8 | 1 | 88% |

### UA  (1,435 items / 4 runs, 33% boosted, 27 $boost · 3 $discard in goggle)

⚠️  **160 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| news.online.ua | 40 | 6 | 85% |
| deutsch.news-pravda.com | 25 | 0 | 100% |
| ua.news-pravda.com | 22 | 1 | 95% |
| africafootunited.com | 18 | 0 | 100% |
| news.stonybrook.edu | 15 | 0 | 100% |
| italy.news-pravda.com | 15 | 0 | 100% |
| ukrinform.es | 13 | 1 | 92% |
| ua.news | 12 | 5 | 58% |
| news-pravda.com | 12 | 1 | 92% ⚠ already discarded |
| tsn.ua | 12 | 0 | 100% |
| espn.com | 11 | 0 | 100% |
| euromaidanpress.com | 11 | 3 | 73% |
| ukranews.com | 10 | 3 | 70% |
| eu.news-pravda.com | 10 | 2 | 80% |
| economictimes.indiatimes.com | 9 | 0 | 100% |

