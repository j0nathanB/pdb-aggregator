# Search Test Results: Comprehensive Report

**Date:** 2026-03-17
**Method:** WebSearch with `allowed_domains` filtering per source intelligence map
**Query:** Each country's head of government
**Time range:** Last 2 days

---

## Executive Summary

- **28 countries** tested with leader-name queries across source map domains
- **272 articles** found across all searches
- **116 / 517** domains returned at least one result (22%)
- **82 unique domains** blocked by Anthropic's web crawler
- **8 countries** had zero blocked domains

---

## Per-Country Results

| Country | Leader | Results | Domains w/ Results | Blocked | Hit Rate |
|---|---|---|---|---|---|
| Australia | Anthony Albanese | 10 | 5/15 | 5 | 33% |
| Brazil | Luiz Inácio Lula da Silva | 10 | 4/18 | 1 | 22% |
| Canada | Mark Carney | 10 | 3/16 | 3 | 19% |
| Chile | José Antonio Kast | 10 | 5/21 | 1 | 24% |
| Czech Republic | Andrej Babiš | 10 | 5/21 | 0 | 24% |
| Estonia | Kristen Michal | 10 | 2/13 | 3 | 15% |
| Finland | Petteri Orpo | 10 | 5/15 | 2 | 33% |
| France | Emmanuel Macron | 10 | 3/18 | 12 | 17% |
| Germany | Friedrich Merz | 10 | 4/19 | 8 | 21% |
| India | Narendra Modi | 10 | 4/19 | 7 | 21% |
| Indonesia | Prabowo Subianto | 10 | 3/23 | 0 | 13% |
| Italy | Giorgia Meloni | 10 | 4/19 | 3 | 21% |
| Japan | Sanae Takaichi | 10 | 5/24 | 5 | 21% |
| Latvia | Evika Siliņa | 10 | 2/17 | 2 | 12% |
| Lithuania | Inga Ruginienė | 10 | 4/17 | 4 | 24% |
| Mexico | Claudia Sheinbaum | 10 | 4/21 | 2 | 19% |
| Norway | Jonas Gahr Støre | 10 | 7/18 | 0 | 39% |
| Poland | Donald Tusk | 10 | 6/20 | 1 | 30% |
| Romania | Marcel Ciolacu | 10 | 5/19 | 1 | 26% |
| Saudi Arabia | Mohammed bin Salman | 10 | 5/18 | 0 | 28% |
| South Korea | Lee Jae-myung | 10 | 5/24 | 2 | 21% |
| Spain | Pedro Sanchez | 10 | 5/14 | 9 | 36% |
| Sweden | Ulf Kristersson | 10 | 2/10 | 7 | 20% |
| Taiwan | Lai Ching-te | 10 | 4/23 | 0 | 17% |
| Turkey | Recep Tayyip Erdogan | 10 | 4/20 | 0 | 20% |
| Uae | Mohammed bin Zayed Al Nahyan | 10 | 5/18 | 0 | 28% |
| Ukraine | Volodymyr Zelensky | 2 | 2/26 | 0 | 8% |
| United Kingdom | Keir Starmer | 10 | 4/11 | 9 | 36% |

---

## Blocked Domains (Anthropic Crawler Denied)

**82 unique domains** block Anthropic's web crawler via `robots.txt`.
These domains cannot be used with Claude's WebSearch `allowed_domains` parameter.
They should be excluded from the pipeline's WebSearch whitelist and accessed via
alternative channels (RSS, direct HTTP scraping, headless browser, or Google News API).

| # | Domain | Countries Affected | Impact |
|---|---|---|---|
| 1 | `20minutos.es` | Spain | Medium |
| 2 | `abc.es` | Spain | Medium |
| 3 | `abc.net.au` | Australia | Standard |
| 4 | `aftonbladet.se` | Sweden | Standard |
| 5 | `aripaev.ee` | Estonia | Standard |
| 6 | `asahi.com` | Japan | Medium |
| 7 | `bbc.co.uk` | United Kingdom | HIGH |
| 8 | `bbc.com` | United Kingdom | HIGH |
| 9 | `bhaskar.com` | India | Medium |
| 10 | `chosun.com` | South Korea | Medium |
| 11 | `corriere.it` | Italy | HIGH |
| 12 | `delfi.ee` | Estonia | Standard |
| 13 | `delfi.lt` | Lithuania | Standard |
| 14 | `delfi.lv` | Latvia | Standard |
| 15 | `di.se` | Sweden | Standard |
| 16 | `dn.se` | Sweden | Standard |
| 17 | `dw.com` | Germany | Medium |
| 18 | `economictimes.indiatimes.com` | India | Medium |
| 19 | `economist.com` | United Kingdom | HIGH |
| 20 | `efe.com` | Spain | Medium |
| 21 | `elconfidencial.com` | Spain | Medium |
| 22 | `eleconomista.com.mx` | Mexico | Medium |
| 23 | `elmundo.es` | Spain | Medium |
| 24 | `elpais.com` | Mexico, Spain | HIGH |
| 25 | `elta.lt` | Lithuania | Standard |
| 26 | `estadao.com.br` | Brazil | Medium |
| 27 | `expansion.com` | Spain | Medium |
| 28 | `expressen.se` | Sweden | Standard |
| 29 | `faz.net` | Germany | Standard |
| 30 | `financialpost.com` | Canada | Medium |
| 31 | `fr.de` | Germany | Medium |
| 32 | `ft.com` | United Kingdom | HIGH |
| 33 | `hindustantimes.com` | India | Medium |
| 34 | `hs.fi` | Finland | Standard |
| 35 | `indianexpress.com` | India | Medium |
| 36 | `intelligenceonline.com` | France | Medium |
| 37 | `is.fi` | Finland | Standard |
| 38 | `jagran.com` | India | Medium |
| 39 | `japan-forward.com` | Japan | Medium |
| 40 | `la-croix.com` | France | Medium |
| 41 | `la.lv` | Latvia | Standard |
| 42 | `lalettre.fr` | France | Medium |
| 43 | `larazon.es` | Spain | Medium |
| 44 | `lavanguardia.com` | Spain | Medium |
| 45 | `lefigaro.fr` | France | Medium |
| 46 | `lemonde.fr` | France | HIGH |
| 47 | `leparisien.fr` | France | Medium |
| 48 | `lesechos.fr` | France | Medium |
| 49 | `liberation.fr` | France | Medium |
| 50 | `libertatea.ro` | Romania | Standard |
| 51 | `limesonline.com` | Italy | Medium |
| 52 | `livemint.com` | India | Medium |
| 53 | `lopinion.fr` | France | Medium |
| 54 | `lrytas.lt` | Lithuania | Standard |
| 55 | `mediapart.fr` | France | Medium |
| 56 | `monde-diplomatique.fr` | France | Medium |
| 57 | `n-tv.de` | Germany | Medium |
| 58 | `nationalpost.com` | Canada | Medium |
| 59 | `ohtuleht.ee` | Estonia | Standard |
| 60 | `omni.se` | Sweden | Standard |
| 61 | `onet.pl` | Poland | Standard |
| 62 | `ouest-france.fr` | France | Medium |
| 63 | `politico.eu` | Germany, United Kingdom | Standard |
| 64 | `repubblica.it` | Italy | HIGH |
| 65 | `reuters.com` | Chile, Japan, United Kingdom | HIGH |
| 66 | `sankei.com` | Japan | Medium |
| 67 | `skynews.com.au` | Australia | Medium |
| 68 | `smh.com.au` | Australia | Medium |
| 69 | `spiegel.de` | Germany | HIGH |
| 70 | `sueddeutsche.de` | Germany | Medium |
| 71 | `svd.se` | Sweden | Standard |
| 72 | `sydsvenskan.se` | Sweden | Standard |
| 73 | `telegraph.co.uk` | United Kingdom | Medium |
| 74 | `theaustralian.com.au` | Australia | Medium |
| 75 | `theguardian.com` | Australia, United Kingdom | HIGH |
| 76 | `thehindu.com` | India | Medium |
| 77 | `thestar.com` | Canada | Medium |
| 78 | `thetimes.co.uk` | United Kingdom | Medium |
| 79 | `vz.lt` | Lithuania | Standard |
| 80 | `yna.co.kr` | South Korea | Standard |
| 81 | `yomiuri.co.jp` | Japan | Standard |
| 82 | `zeit.de` | Germany | Medium |

### By Region

- **Western Europe:** 50 blocked / 124 total domains (40%)
- **Eastern Europe & Baltics:** 11 blocked / 133 total domains (8%)
- **Asia-Pacific:** 19 blocked / 128 total domains (15%)
- **Americas:** 7 blocked / 76 total domains (9%)
- **Middle East:** 0 blocked / 56 total domains (0%)

---

## Implications for Pipeline Design

### WebSearch Channel
- 82 domains (16% of all source map domains) are inaccessible via Claude WebSearch
- Western European and Anglophone premium press is disproportionately blocked
- Government, think tank, and smaller regional outlets are largely unblocked
- Asian and Middle Eastern domains have the lowest block rates

### Recommended Multi-Channel Strategy

| Channel | Best For | Coverage |
|---|---|---|
| Claude WebSearch | Unblocked domains (govt, think tanks, regional press) | ~85% of source map domains |
| RSS feeds | Paywalled and bot-blocked major press | ~43% of sources have RSS |
| Google News API | Headline discovery across all sources | Broad but snippet-only |
| Direct HTTP/headless | Full text extraction from accessible sites | ~50% yield full text |
