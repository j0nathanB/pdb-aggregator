# Goggle audit — 20260419 + 20260426 + 20260503 + 20260510 + 20260517

Aggregate of 5 weekly story_map runs (30 countries). For each (country, domain), counts URLs sent to story_map vs URLs that survived in the LLM's stories/single_source/unassigned output. Diff = URLs the LLM rejected as noise. Thresholds for surfacing candidates: drop-rate ≥ 80% AND ≥ 30 items (domains) / ≥ 20 items (paths).

Production filters in effect during these runs (where deployed): `_global_discards.txt` (22 domains), per-country goggle `$discard`, `off_topic_filters.csv` (21 rules). Discard leaks below should be ≈0 for runs ≥ 2026-05-11.

## Cross-country noise domains (discard candidates)

Domains that appear in ≥2 countries with high drop rate. Add to `_global_discards.txt` if the noise is structural (off-topic / spam / wrong-language / non-news). Domains touching a single country are listed in that country's section below.

| Domain | Input | Kept | Drop % | Countries |
|---|---:|---:|---:|---:|
| asatunews.co.id | 102 | 16 | 84% | 17 |
| commonslibrary.parliament.uk | 82 | 6 | 93% | 11 |
| stocktitan.net | 77 | 9 | 88% | 20 |
| cronista.com | 75 | 4 | 95% | 12 |
| ladepeche.fr | 69 | 13 | 81% | 8 |
| sports.yahoo.com | 69 | 2 | 97% | 13 |
| lanacion.com.ar | 68 | 13 | 81% | 13 |
| elconfidencialdigital.com | 68 | 12 | 82% | 5 |
| haberler.com | 68 | 10 | 85% | 4 |
| prnewswire.com | 64 | 3 | 95% | 21 |
| ouest-france.fr | 63 | 10 | 84% | 9 |
| mirror.co.uk | 62 | 9 | 85% | 15 |
| jawapos.com | 61 | 12 | 80% | 8 |
| tickerreport.com | 60 | 1 | 98% | 14 |
| politico.com | 59 | 6 | 90% | 13 |
| infomoney.com.br | 58 | 10 | 83% | 4 |
| as.com | 57 | 6 | 89% | 10 |
| elpais.com.uy | 53 | 1 | 98% | 5 |
| mundodeportivo.com | 51 | 1 | 98% | 14 |
| bbc.co.uk | 51 | 9 | 82% | 19 |
| zawya.com | 50 | 9 | 82% | 6 |
| clarin.com | 50 | 6 | 88% | 12 |
| fool.com | 50 | 2 | 96% | 12 |
| infodefensa.com | 49 | 8 | 84% | 2 |
| si.com | 45 | 2 | 96% | 12 |
| vsd.fr | 45 | 0 | 100% | 2 |
| boerse-express.com | 44 | 1 | 98% | 6 |
| ambito.com | 42 | 4 | 90% | 9 |
| marca.com | 41 | 4 | 90% | 11 |
| gurufocus.com | 41 | 8 | 80% | 9 |
| simplywall.st | 39 | 6 | 85% | 14 |
| jv.dk | 39 | 0 | 100% | 2 |
| cricbuzz.com | 39 | 0 | 100% | 5 |
| aksam.com.tr | 39 | 5 | 87% | 3 |
| kenh14.vn | 39 | 1 | 97% | 2 |
| expansion.com | 38 | 6 | 84% | 13 |
| elsiglodetorreon.com.mx | 38 | 5 | 87% | 6 |
| threads.com | 38 | 4 | 89% | 13 |
| actu.fr | 36 | 5 | 86% | 7 |
| app.com.pk | 36 | 6 | 83% | 2 |

## Cross-country noise paths (off_topic_filters.csv candidates)

(domain, path-prefix) combos where the LLM drops most URLs. Strong candidates for adding to `off_topic_filters.csv`. Already-covered rows are flagged so you can ignore them.

| Domain | Path | Input | Kept | Drop % | Countries | Already covered |
|---|---|---:|---:|---:|---:|:---:|
| finance.yahoo.com | /markets/ | 117 | 16 | 86% | 21 |  |
| ad-hoc-news.de | /boerse/ | 82 | 15 | 82% | 18 |  |
| commonslibrary.parliament.uk | /research-briefings/ | 82 | 6 | 93% | 11 |  |
| ladepeche.fr | /2026/ | 69 | 13 | 81% | 8 |  |
| prnewswire.com | /news-releases/ | 61 | 3 | 95% | 20 |  |
| tickerreport.com | /banking-finance/ | 60 | 1 | 98% | 14 |  |
| stocktitan.net | /sec-filings/ | 51 | 8 | 84% | 15 |  |
| infodefensa.com | /texto-diario/ | 49 | 8 | 84% | 2 |  |
| honvedelem.hu | /hirek/ | 49 | 0 | 100% | 1 |  |
| sports.yahoo.com | /articles/ | 47 | 2 | 96% | 13 |  |
| elconfidencialdigital.com | /articulo/ | 47 | 8 | 83% | 5 |  |
| zawya.com | /en/ | 46 | 7 | 85% | 6 |  |
| bbc.co.uk | /news/ | 46 | 8 | 83% | 16 |  |
| boerse-express.com | /news/ | 44 | 1 | 98% | 6 |  |
| gurufocus.com | /news/ | 41 | 8 | 80% | 9 |  |
| mirror.co.uk | /news/ | 40 | 6 | 85% | 14 |  |
| simplywall.st | /stocks/ | 38 | 5 | 87% | 14 |  |
| politico.com | /news/ | 38 | 4 | 89% | 11 |  |
| elsiglodetorreon.com.mx | /noticia/ | 38 | 5 | 87% | 6 |  |
| haberler.com | /guncel/ | 37 | 3 | 92% | 4 |  |
| insidermonkey.com | /blog/ | 35 | 0 | 100% | 16 |  |
| bnr.nl | /nieuws/ | 35 | 0 | 100% | 1 |  |
| latercera.com | /nacional/ | 35 | 5 | 86% | 4 |  |
| timesofindia.indiatimes.com | /city/ | 34 | 1 | 97% | 13 |  |
| ocafezinho.com | /2026/ | 34 | 6 | 82% | 3 |  |
| as.com | /futbol/ | 32 | 1 | 97% | 7 |  |
| mediaoffice.abudhabi | /en/ | 31 | 4 | 87% | 1 |  |
| forbes.com | /sites/ | 31 | 3 | 90% | 11 |  |
| infomoney.com.br | /mercados/ | 30 | 5 | 83% | 4 |  |
| rnz.co.nz | /news/ | 30 | 3 | 90% | 5 |  |
| fool.com | /earnings/ | 29 | 0 | 100% | 7 |  |
| dailyparliamenttimes.com | /2026/ | 27 | 3 | 89% | 2 |  |
| metropoles.com | /colunas/ | 26 | 3 | 88% | 5 |  |
| stocktitan.net | /news/ | 26 | 1 | 96% | 14 |  |
| thenational.scot | /news/ | 25 | 1 | 96% | 5 |  |
| nasional.sindonews.com | /read/ | 25 | 5 | 80% | 3 |  |
| ozbargain.com.au | /node/ | 25 | 0 | 100% | 2 |  |
| asatunews.co.id | /en/ | 24 | 4 | 83% | 10 |  |
| thehill.com | /homenews/ | 24 | 4 | 83% | 9 |  |
| bostonherald.com | /2026/ | 23 | 2 | 91% | 4 |  |
| mundodeportivo.com | /futbol/ | 23 | 0 | 100% | 7 |  |
| hercampus.com | /school/ | 23 | 0 | 100% | 2 |  |
| marca.com | /futbol/ | 22 | 0 | 100% | 8 |  |
| smallwarsjournal.com | /2026/ | 21 | 2 | 90% | 7 |  |
| elpais.com.uy | /informacion/ | 21 | 0 | 100% | 1 |  |
| spravy.pravda.sk | /svet/ | 21 | 4 | 81% | 1 |  |
| aktuality.sk | /clanok/ | 21 | 0 | 100% | 2 |  |
| 20min.ch | /story/ | 21 | 1 | 95% | 3 |  |
| birminghammail.co.uk | /news/ | 21 | 1 | 95% | 3 |  |
| foxnews.com | /politics/ | 21 | 3 | 86% | 7 |  |
| milanofinanza.it | /news/ | 21 | 2 | 90% | 1 |  |
| nzherald.co.nz | /nz/ | 21 | 0 | 100% | 3 |  |
| acorianooriental.pt | /noticia/ | 21 | 0 | 100% | 2 |  |
| washingtontimes.com | /news/ | 20 | 1 | 95% | 10 |  |
| defenseworld.net | /2026/ | 20 | 0 | 100% | 2 |  |
| elpais.com.uy | /opinion/ | 20 | 0 | 100% | 1 |  |

## Per-country breakdown

### AE  (1,902 items / 5 runs, 16% boosted, 28 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| sharjah24.ae | 47 | 14 | 70% |
| zawya.com | 34 | 4 | 88% |
| mofa.gov.ae | 30 | 12 | 60% |
| hindustantimes.com | 22 | 16 | 27% |
| acorianooriental.pt | 20 | 0 | 100% |
| voiceofemirates.com | 17 | 4 | 76% |
| timesofindia.indiatimes.com | 16 | 10 | 38% |
| firstpost.com | 14 | 9 | 36% |
| tag911.ae | 12 | 3 | 75% |
| jpost.com | 12 | 7 | 42% |
| economictimes.indiatimes.com | 12 | 5 | 58% |
| mixvale.com.br | 12 | 0 | 100% |
| tribuneindia.com | 11 | 8 | 27% |
| foxnews.com | 10 | 5 | 50% |
| oilprice.com | 10 | 7 | 30% |

### AU  (1,837 items / 5 runs, 24% boosted, 27 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| dailymail.com | 39 | 22 | 44% |
| tvnota.com | 28 | 0 | 100% |
| boerse-express.com | 25 | 0 | 100% |
| canberratimes.com.au | 22 | 11 | 50% |
| fxstreet.com | 21 | 20 | 5% |
| ligaolahraga.com | 17 | 0 | 100% |
| commonslibrary.parliament.uk | 16 | 4 | 75% |
| ancashnoticias.com | 14 | 0 | 100% |
| theage.com.au | 13 | 8 | 38% |
| thenational.scot | 13 | 0 | 100% |
| news.bloomberglaw.com | 10 | 0 | 100% |
| asatunews.co.id | 10 | 0 | 100% |
| boerse.de | 9 | 0 | 100% |
| rba.gov.au | 9 | 3 | 67% |
| spectator.com.au | 8 | 4 | 50% |

### BR  (1,985 items / 5 runs, 31% boosted, 30 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| g1.globo.com | 40 | 22 | 45% |
| noticias.uol.com.br | 37 | 13 | 65% |
| ocafezinho.com | 32 | 6 | 81% |
| bleedcubbieblue.com | 27 | 0 | 100% |
| correiobraziliense.com.br | 26 | 18 | 31% |
| em.com.br | 26 | 11 | 58% |
| jornaldebrasilia.com.br | 25 | 8 | 68% |
| noticias.r7.com | 23 | 10 | 57% |
| revistaforum.com.br | 21 | 8 | 62% |
| terra.com.br | 20 | 10 | 50% |
| otempo.com.br | 20 | 8 | 60% |
| ndmais.com.br | 19 | 5 | 74% |
| sociedademilitar.com.br | 18 | 0 | 100% |
| iclnoticias.com.br | 17 | 5 | 71% |
| clickpetroleoegas.com.br | 15 | 2 | 87% |

### CA  (1,953 items / 5 runs, 31% boosted, 24 $boost · 6 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| financialpost.com | 30 | 20 | 33% |
| conservative.ca | 17 | 5 | 71% |
| policymagazine.ca | 15 | 14 | 7% |
| grazia.fr | 14 | 0 | 100% |
| ca.finance.yahoo.com | 13 | 6 | 54% |
| thehub.ca | 12 | 10 | 17% |
| ca.news.yahoo.com | 12 | 10 | 17% |
| foot-africa.com | 12 | 0 | 100% |
| thetyee.ca | 11 | 4 | 64% |
| tvanouvelles.ca | 11 | 6 | 45% |
| calgaryherald.com | 11 | 5 | 55% |
| dailysports.net | 11 | 0 | 100% |
| pentictonherald.ca | 11 | 4 | 64% |
| montrealgazette.com | 10 | 5 | 50% |
| abc.net.au | 10 | 0 | 100% |

### CL  (1,822 items / 5 runs, 28% boosted, 27 $boost · 2 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| aninews.in | 41 | 0 | 100% |
| lanacion.com.ar | 34 | 2 | 94% |
| tribuneindia.com | 31 | 0 | 100% |
| cronista.com | 25 | 1 | 96% |
| radio.uchile.cl | 21 | 15 | 29% |
| carasycaretas.com.uy | 21 | 0 | 100% |
| eldinamo.cl | 20 | 12 | 40% |
| redimin.cl | 19 | 2 | 89% |
| elconfidencialdigital.com | 17 | 0 | 100% |
| chilevision.cl | 16 | 10 | 38% |
| clarin.com | 16 | 0 | 100% |
| ambito.com | 15 | 0 | 100% |
| elobservador.com.uy | 13 | 0 | 100% |
| theclinic.cl | 13 | 9 | 31% |
| zona-militar.com | 13 | 2 | 85% |

### CZ  (1,844 items / 5 runs, 14% boosted, 26 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| m.echo24.cz | 41 | 26 | 37% |
| denik.cz | 33 | 17 | 48% |
| forum24.cz | 31 | 25 | 19% |
| spravy.pravda.sk | 29 | 4 | 86% |
| czdefence.cz | 28 | 9 | 68% |
| echo24.cz | 27 | 10 | 63% |
| teraz.sk | 23 | 1 | 96% |
| reflex.cz | 22 | 18 | 18% |
| theplaylist.net | 21 | 0 | 100% |
| aktuality.sk | 20 | 0 | 100% |
| novinky.cz | 19 | 12 | 37% |
| ekonomickydenik.cz | 13 | 11 | 15% |
| ad-hoc-news.de | 12 | 0 | 100% |
| infobae.com | 12 | 0 | 100% |
| thehockeynews.com | 12 | 0 | 100% |

### DE  (1,965 items / 5 runs, 45% boosted, 32 $boost · 6 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| zdfheute.de | 47 | 26 | 45% |
| berliner-zeitung.de | 39 | 12 | 69% |
| stern.de | 38 | 20 | 47% |
| web.de | 23 | 10 | 57% |
| finanzen.net | 21 | 5 | 76% |
| swr.de | 21 | 7 | 67% |
| oldenburger-onlinezeitung.de | 19 | 10 | 47% |
| mdr.de | 18 | 5 | 72% |
| morgenpost.de | 17 | 9 | 47% |
| bnd.com | 17 | 0 | 100% |
| augsburger-allgemeine.de | 16 | 4 | 75% |
| tag24.de | 15 | 3 | 80% |
| br.de | 13 | 8 | 38% |
| news.de | 13 | 8 | 38% |
| boerse.de | 12 | 9 | 25% |

### EE  (1,725 items / 5 runs, 26% boosted, 20 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| mil.ee | 50 | 17 | 66% |
| lounaeestlane.ee | 45 | 21 | 53% |
| globenewswire.com | 27 | 19 | 30% |
| 20min.ch | 17 | 0 | 100% |
| news.maxifoot.fr | 16 | 0 | 100% |
| adaur.ee | 15 | 9 | 40% |
| independent.co.uk | 13 | 0 | 100% |
| mirror.co.uk | 13 | 0 | 100% |
| uudis.net | 12 | 6 | 50% |
| titrespresse.com | 12 | 0 | 100% |
| edf.fr | 11 | 0 | 100% |
| online.le.ee | 10 | 4 | 60% |
| pravda.com.ua | 9 | 6 | 33% |
| eestikirik.ee | 9 | 1 | 89% |
| polizeiticker.ch | 9 | 0 | 100% |

### ES  (1,841 items / 5 runs, 34% boosted, 27 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| elconfidencialdigital.com | 45 | 12 | 73% |
| eldebate.com | 41 | 15 | 63% |
| elperiodico.com | 38 | 22 | 42% |
| libertaddigital.com | 37 | 19 | 49% |
| infobae.com | 29 | 14 | 52% |
| europapress.es | 29 | 10 | 66% |
| theobjective.com | 28 | 14 | 50% |
| ideal.es | 22 | 15 | 32% |
| lasexta.com | 20 | 13 | 35% |
| esdiario.com | 19 | 11 | 42% |
| heraldo.es | 17 | 8 | 53% |
| lasprovincias.es | 17 | 7 | 59% |
| diariosur.es | 16 | 3 | 81% |
| lavozdegalicia.es | 16 | 6 | 62% |
| informacion.es | 16 | 1 | 94% |

### FI  (1,559 items / 5 runs, 29% boosted, 23 $boost · 0 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| is.fi | 50 | 36 | 28% |
| maaseuduntulevaisuus.fi | 36 | 15 | 58% |
| sss.fi | 30 | 14 | 53% |
| demokraatti.fi | 29 | 17 | 41% |
| puolustusvoimat.fi | 21 | 7 | 67% |
| ksml.fi | 19 | 9 | 53% |
| tekniikkatalous.fi | 15 | 3 | 80% |
| kokoomus.fi | 15 | 7 | 53% |
| suomenmaa.fi | 14 | 9 | 36% |
| ts.fi | 14 | 7 | 50% |
| aamulehti.fi | 11 | 7 | 36% |
| ess.fi | 11 | 5 | 55% |
| infobae.com | 11 | 1 | 91% |
| esaimaa.fi | 10 | 4 | 60% |
| kymensanomat.fi | 10 | 3 | 70% |

### FR  (1,768 items / 5 runs, 38% boosted, 31 $boost · 5 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| huffingtonpost.fr | 44 | 25 | 43% |
| ouest-france.fr | 42 | 9 | 79% |
| actu.orange.fr | 35 | 19 | 46% |
| tf1info.fr | 32 | 17 | 47% |
| actu.fr | 26 | 4 | 85% |
| europe1.fr | 26 | 12 | 54% |
| boursorama.com | 24 | 8 | 67% |
| lejdd.fr | 23 | 11 | 52% |
| sudouest.fr | 20 | 10 | 50% |
| rtl.fr | 20 | 9 | 55% |
| moneyvox.fr | 17 | 1 | 94% |
| latribune.fr | 16 | 8 | 50% |
| lexpress.fr | 15 | 3 | 80% |
| lanouvellerepublique.fr | 15 | 4 | 73% |
| midilibre.fr | 15 | 6 | 60% |

### GB  (2,103 items / 5 runs, 20% boosted, 23 $boost · 6 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| dailymail.com | 40 | 28 | 30% |
| bankofengland.co.uk | 21 | 7 | 67% |
| foxnews.com | 20 | 7 | 65% |
| bostonherald.com | 20 | 0 | 100% |
| standard.co.uk | 17 | 11 | 35% |
| aol.com | 15 | 6 | 60% |
| telegraph.co.uk | 15 | 7 | 53% |
| cnbc.com | 14 | 12 | 14% |
| manchestereveningnews.co.uk | 14 | 8 | 43% |
| spectator.com | 13 | 10 | 23% |
| news.sky.com | 12 | 8 | 33% |
| metro.co.uk | 12 | 7 | 42% |
| el-balad.com | 12 | 5 | 58% |
| nbcnews.com | 11 | 9 | 18% |
| the-independent.com | 11 | 8 | 27% |

### HU  (1,915 items / 5 runs, 49% boosted, 39 $boost · 6 $discard in goggle)

⚠️  **79 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| dailynewshungary.com | 46 | 27 | 41% |
| blikk.hu | 32 | 9 | 72% ⚠ already discarded |
| hungary.news-pravda.com | 25 | 14 | 44% |
| szeretlekmagyarorszag.hu | 24 | 13 | 46% |
| penzcentrum.hu | 19 | 4 | 79% |
| hang.hu | 16 | 7 | 56% |
| kuruc.info | 16 | 3 | 81% |
| startlap.hu | 13 | 3 | 77% |
| promotions.hu | 11 | 3 | 73% |
| privatbankar.hu | 11 | 4 | 64% |
| borsonline.hu | 11 | 0 | 100% |
| divany.hu | 9 | 0 | 100% |
| ladepeche.fr | 8 | 0 | 100% |
| magyarjelen.hu | 8 | 2 | 75% |
| kyivpost.com | 7 | 7 | 0% |

### ID  (1,973 items / 5 runs, 29% boosted, 31 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| news.detik.com | 44 | 19 | 57% |
| jpnn.com | 43 | 22 | 49% |
| latercera.com | 37 | 0 | 100% |
| asatunews.co.id | 35 | 11 | 69% |
| globalconvertx.com | 18 | 0 | 100% |
| nasional.sindonews.com | 17 | 5 | 71% |
| koran-jakarta.com | 17 | 3 | 82% |
| gelora.co | 14 | 4 | 71% |
| mirror.co.uk | 14 | 0 | 100% |
| cbc.ca | 13 | 0 | 100% |
| golkarpedia.com | 12 | 2 | 83% |
| birminghammail.co.uk | 12 | 0 | 100% |
| beritajatim.com | 12 | 9 | 25% |
| inews.id | 11 | 6 | 45% |
| saltwire.com | 11 | 0 | 100% |

### IN  (1,940 items / 5 runs, 25% boosted, 28 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| timesofindia.indiatimes.com | 50 | 40 | 20% |
| ndtv.com | 50 | 38 | 24% |
| aninews.in | 36 | 20 | 44% |
| indiatoday.in | 35 | 23 | 34% |
| newkerala.com | 29 | 13 | 55% |
| newsable.asianetnews.com | 25 | 10 | 60% |
| firstpost.com | 24 | 18 | 25% |
| sports.yahoo.com | 24 | 0 | 100% |
| news18.com | 23 | 17 | 26% |
| pinstripealley.com | 23 | 0 | 100% |
| deccanchronicle.com | 21 | 11 | 48% |
| cbsnews.com | 18 | 0 | 100% |
| shop.ssbcrack.com | 17 | 3 | 82% |
| m.economictimes.com | 16 | 14 | 12% |
| socialnews.xyz | 16 | 8 | 50% |

### IT  (1,931 items / 5 runs, 31% boosted, 30 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| ilgiornale.it | 50 | 19 | 62% |
| zazoom.it | 48 | 24 | 50% |
| adnkronos.com | 42 | 19 | 55% |
| fanpage.it | 41 | 15 | 63% |
| quotidiano.net | 31 | 15 | 52% |
| ilrestodelcarlino.it | 31 | 9 | 71% |
| ilmattino.it | 23 | 4 | 83% |
| ilgazzettino.it | 22 | 7 | 68% |
| milanofinanza.it | 21 | 2 | 90% |
| secoloditalia.it | 17 | 1 | 94% |
| huffingtonpost.it | 17 | 4 | 76% |
| virgilio.it | 14 | 6 | 57% |
| lanazione.it | 13 | 0 | 100% |
| tgcom24.mediaset.it | 13 | 5 | 62% |
| agenziagiornalisticaopinione.it | 13 | 2 | 85% |

### JP  (1,267 items / 4 runs, 14% boosted, 30 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| telegrafi.com | 23 | 0 | 100% |
| fr-fans.nl | 16 | 0 | 100% |
| fr12.nl | 15 | 0 | 100% |
| sot.com.al | 13 | 0 | 100% |
| asahi.com | 11 | 11 | 0% |
| rijnmond.nl | 11 | 0 | 100% |
| scmp.com | 10 | 9 | 10% |
| veriu.info | 9 | 0 | 100% |
| lajmi.net | 8 | 0 | 100% |
| 1908.nl | 8 | 0 | 100% |
| mainichi.jp | 7 | 7 | 0% |
| radiokosovaelire.com | 7 | 0 | 100% |
| economictimes.indiatimes.com | 7 | 3 | 57% |
| japan-forward.com | 7 | 6 | 14% |
| tokyoreporter.com | 7 | 0 | 100% |

### KR  (1,885 items / 5 runs, 24% boosted, 31 $boost · 2 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| jpost.com | 22 | 0 | 100% |
| forbes.com | 19 | 2 | 89% |
| nation.com.pk | 13 | 0 | 100% |
| en.bloomingbit.io | 13 | 11 | 15% |
| phonearena.com | 13 | 2 | 85% |
| en.namu.wiki | 13 | 0 | 100% |
| asiae.co.kr | 12 | 9 | 25% |
| turkiyetoday.com | 11 | 0 | 100% |
| taipeitimes.com | 10 | 1 | 90% |
| smallwarsjournal.com | 10 | 0 | 100% |
| technobezz.com | 10 | 2 | 80% |
| manilatimes.net | 10 | 1 | 90% |
| androidpolice.com | 9 | 0 | 100% |
| economictimes.indiatimes.com | 9 | 0 | 100% |
| scmp.com | 8 | 2 | 75% |

### LT  (1,097 items / 5 runs, 27% boosted, 22 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| vsd.fr | 44 | 0 | 100% |
| lsdp.lt | 40 | 9 | 78% |
| kauno.diena.lt | 37 | 22 | 41% |
| m.kauno.diena.lt | 22 | 14 | 36% |
| ve.lt | 18 | 13 | 28% |
| klaipeda.diena.lt | 14 | 9 | 36% |
| globenewswire.com | 14 | 12 | 14% |
| lrytas.lt | 11 | 10 | 9% |
| aina.lt | 11 | 9 | 18% |
| nashaniva.com | 11 | 3 | 73% |
| augsburger-allgemeine.de | 10 | 0 | 100% |
| aujourd8.net | 10 | 0 | 100% |
| eng.lsm.lv | 9 | 6 | 33% |
| jp.lt | 9 | 9 | 0% |
| alkas.lt | 9 | 6 | 33% |

### LV  (1,485 items / 5 runs, 31% boosted, 24 $boost · 1 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| jv.dk | 38 | 0 | 100% |
| ozbargain.com.au | 24 | 0 | 100% |
| infobae.com | 16 | 1 | 94% |
| blueprint.ng | 16 | 0 | 100% |
| informer.rs | 14 | 0 | 100% |
| dailyknicks.com | 14 | 0 | 100% |
| bnn-news.com | 12 | 12 | 0% |
| irishstar.com | 10 | 0 | 100% |
| trend.az | 10 | 10 | 0% |
| ogrenet.lv | 9 | 5 | 44% |
| foxnews.com | 9 | 0 | 100% |
| finance.yahoo.com | 9 | 0 | 100% |
| punchng.com | 9 | 0 | 100% |
| blic.rs | 8 | 0 | 100% |
| ad-hoc-news.de | 8 | 0 | 100% |

### MX  (2,005 items / 5 runs, 35% boosted, 31 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| elimparcial.com | 42 | 12 | 71% |
| informador.mx | 37 | 19 | 49% |
| eldiariodechihuahua.mx | 28 | 9 | 68% |
| cronista.com | 23 | 3 | 87% |
| tribuna.com.mx | 22 | 4 | 82% |
| razon.com.mx | 21 | 4 | 81% |
| aksam.com.tr | 20 | 0 | 100% |
| 24-horas.mx | 18 | 11 | 39% |
| ambito.com | 16 | 2 | 88% |
| unotv.com | 16 | 8 | 50% |
| lasillarota.com | 16 | 5 | 69% |
| diario.mx | 15 | 9 | 40% |
| tribunademexico.com | 15 | 5 | 67% |
| elnacional.cat | 13 | 0 | 100% |
| tiempo.com.mx | 13 | 8 | 38% |

### NO  (1,756 items / 5 runs, 28% boosted, 25 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| tickerreport.com | 31 | 0 | 100% |
| abcnyheter.no | 27 | 11 | 59% |
| inyheter.no | 23 | 16 | 30% |
| forsvaret.no | 21 | 3 | 86% |
| sol.no | 19 | 15 | 21% |
| defenseworld.net | 19 | 0 | 100% |
| frifagbevegelse.no | 17 | 14 | 18% |
| stocktitan.net | 17 | 3 | 82% |
| finance.yahoo.com | 16 | 8 | 50% |
| dr.dk | 14 | 0 | 100% |
| ad-hoc-news.de | 14 | 10 | 29% |
| frp.no | 13 | 5 | 62% |
| smp.no | 12 | 5 | 58% |
| nyheder.tv2.dk | 11 | 0 | 100% |
| bt.no | 11 | 5 | 55% |

### PK  (2,008 items / 5 runs, 21% boosted, 37 $boost · 4 $discard in goggle)

⚠️  **54 discard leak(s)** — post-fetch filter should have caught these. Likely from runs predating the 2026-05-11 deployment of the filter.

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| timesofindia.indiatimes.com | 38 | 16 | 58% |
| hindustantimes.com | 35 | 18 | 49% |
| finance.yahoo.com | 33 | 0 | 100% |
| ndtv.com | 26 | 15 | 42% |
| bolnews.com | 26 | 11 | 58% ⚠ already discarded |
| firstpost.com | 25 | 20 | 20% |
| indiatoday.in | 24 | 11 | 54% |
| dailyparliamenttimes.com | 24 | 3 | 88% |
| pakistan.shafaqna.com | 23 | 11 | 52% |
| dailytimes.com.pk | 23 | 9 | 61% |
| indianexpress.com | 22 | 7 | 68% |
| gurufocus.com | 22 | 0 | 100% |
| tribuneindia.com | 20 | 10 | 50% |
| arabnews.com | 20 | 11 | 45% |
| dunyanews.tv | 17 | 11 | 35% |

### PL  (1,854 items / 5 runs, 41% boosted, 33 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| bankier.pl | 50 | 18 | 64% |
| goniec.pl | 39 | 24 | 38% |
| wiadomosci.radiozet.pl | 36 | 17 | 53% |
| wprost.pl | 34 | 12 | 65% |
| newsweek.pl | 30 | 15 | 50% |
| onet.pl | 29 | 8 | 72% |
| portalsamorzadowy.pl | 20 | 3 | 85% |
| next.gazeta.pl | 19 | 7 | 63% |
| radiomaryja.pl | 18 | 9 | 50% |
| wykop.pl | 18 | 2 | 89% |
| nczas.info | 18 | 3 | 83% |
| polskieradio24.pl | 17 | 6 | 65% |
| natemat.pl | 15 | 8 | 47% |
| tokfm.pl | 15 | 10 | 33% |
| wgospodarce.pl | 15 | 7 | 53% |

### RO  (1,994 items / 5 runs, 20% boosted, 27 $boost · 4 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| mediafax.ro | 44 | 21 | 52% |
| bnr.nl | 40 | 0 | 100% |
| cotidianul.ro | 34 | 25 | 26% |
| jurnalul.ro | 33 | 21 | 36% |
| libertatea.ro | 31 | 20 | 35% |
| bursa.ro | 30 | 17 | 43% |
| stirileprotv.ro | 30 | 20 | 33% |
| business24.ro | 25 | 10 | 60% |
| cricbuzz.com | 25 | 0 | 100% |
| spotmedia.ro | 23 | 15 | 35% |
| republica.ro | 22 | 18 | 18% |
| caleaeuropeana.ro | 22 | 6 | 73% |
| observatornews.ro | 21 | 14 | 33% |
| buzoienii.ro | 18 | 2 | 89% |
| opiniabuzau.ro | 16 | 3 | 81% |

### SA  (2,112 items / 5 runs, 12% boosted, 23 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| asatunews.co.id | 25 | 0 | 100% |
| arabnews.pk | 16 | 8 | 50% |
| ligaolahraga.com | 16 | 0 | 100% |
| themirror.com | 14 | 8 | 43% |
| antaranews.com | 13 | 0 | 100% |
| sana.sy | 12 | 10 | 17% |
| thenationalnews.com | 11 | 5 | 55% |
| sports.yahoo.com | 11 | 2 | 82% |
| chroniclelive.co.uk | 11 | 3 | 73% |
| viva.co.id | 11 | 0 | 100% |
| gulfnews.com | 10 | 7 | 30% |
| titrespresse.com | 10 | 0 | 100% |
| el-balad.com | 10 | 2 | 80% |
| essentiallysports.com | 9 | 6 | 33% |
| ansa.it | 9 | 0 | 100% |

### SE  (1,809 items / 5 runs, 30% boosted, 25 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| fool.com | 23 | 0 | 100% |
| globenewswire.com | 23 | 5 | 78% |
| yle.fi | 21 | 1 | 95% |
| finance.yahoo.com | 19 | 1 | 95% |
| regeringen.se | 18 | 15 | 17% |
| se.headtopics.com | 15 | 8 | 47% |
| cornucopia.se | 13 | 5 | 62% |
| efn.se | 13 | 12 | 8% |
| fxstreet.com | 13 | 11 | 15% |
| marcusoscarsson.se | 12 | 9 | 25% |
| placera.se | 12 | 6 | 50% |
| etc.se | 10 | 5 | 50% |
| realtid.se | 10 | 5 | 50% |
| hd.se | 10 | 3 | 70% |
| fotbolldirekt.se | 10 | 0 | 100% |

### TR  (1,996 items / 5 runs, 22% boosted, 30 $boost · 6 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| haberler.com | 49 | 10 | 80% |
| turkiyegazetesi.com.tr | 29 | 12 | 59% |
| dunya.com | 28 | 14 | 50% |
| aa.com.tr | 25 | 15 | 40% |
| sondakika.com | 25 | 12 | 52% |
| star.com.tr | 24 | 9 | 62% |
| yenicaggazetesi.com | 22 | 8 | 64% |
| haberturk.com | 22 | 9 | 59% |
| memurlar.net | 21 | 11 | 48% |
| nefes.com.tr | 21 | 5 | 76% |
| aksam.com.tr | 18 | 5 | 72% |
| ntv.com.tr | 17 | 4 | 76% |
| cnnturk.com | 16 | 5 | 69% |
| ensonhaber.com | 15 | 5 | 67% |
| haber.mynet.com | 15 | 7 | 53% |

### TW  (2,103 items / 5 runs, 15% boosted, 24 $boost · 2 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| cbc.ca | 50 | 0 | 100% |
| kenh14.vn | 34 | 0 | 100% |
| ca.news.yahoo.com | 33 | 0 | 100% |
| vietgiaitri.com | 25 | 0 | 100% |
| finance.yahoo.com | 24 | 16 | 33% |
| rnz.co.nz | 24 | 0 | 100% |
| nzherald.co.nz | 24 | 0 | 100% |
| antaranews.com | 12 | 0 | 100% |
| scmp.com | 12 | 7 | 42% |
| seekingalpha.com | 11 | 11 | 0% |
| jpnn.com | 10 | 0 | 100% |
| collider.com | 10 | 0 | 100% |
| saostar.vn | 9 | 0 | 100% |
| vnexpress.net | 9 | 0 | 100% |
| newsable.asianetnews.com | 9 | 8 | 11% |

### UA  (2,088 items / 5 runs, 29% boosted, 27 $boost · 3 $discard in goggle)

**Top 15 unboosted domains:**

| Domain | Input | Kept | Drop % |
|---|---:|---:|---:|
| news.online.ua | 32 | 6 | 81% |
| independent.co.uk | 22 | 17 | 23% |
| yahoo.com | 22 | 14 | 36% |
| hercampus.com | 22 | 0 | 100% |
| euromaidanpress.com | 21 | 12 | 43% |
| ukranews.com | 20 | 8 | 60% |
| africafootunited.com | 18 | 0 | 100% |
| ukrinform.ua | 18 | 3 | 83% |
| odessa-journal.com | 17 | 10 | 41% |
| ukrinform.es | 17 | 5 | 71% |
| obozrevatel.com | 17 | 1 | 94% |
| tsn.ua | 16 | 4 | 75% |
| en.hvylya.net | 14 | 7 | 50% |
| glavnoe.in.ua | 14 | 7 | 50% |
| nashaniva.com | 13 | 3 | 77% |

