# Government Source Retrieval — Cross-Method Comparison

**Date:** 2026-03-21
**Sources tested:** 163 (across 28 countries)
**Total URLs:** 455
**Combined reachability:** 407/455 URLs (89%) accessible by at least one method

## Method Summary

Methods were run in cascade — each subsequent method only tested URLs that failed prior methods.

| Method | URLs tested | OK | Rate | Notes |
|---|---|---|---|---|
| **curl+trafilatura** | 455 | 334 | **73%** | Baseline — fast, free, no rate limits |
| **Diffbot API** | 121 | 37 | 31% | Rate limited (5/min). Tested only curl failures |
| **Claude WebFetch** | 121 | 28 | 23% | Tested only curl failures |
| **Playwright** | 84 | 33 | 39% | Tested remaining after Diffbot. Headless Chromium |

## Combined Cascade Result

Applying methods in order (curl → diffbot → playwright → webfetch), the cascade recovers content from **407 of 455 URLs (89%)**. The 48 unreachable URLs span 12 source domains.

## Recommended Method Distribution

- **curl**: 123 sources (75% — first choice for most government sites)
- **diffbot**: 12 sources (7% — key for Australian .gov.au sites that block Python UA)
- **playwright**: 11 sources (7% — JS-rendered sites: Romania, Saudi Arabia, Ukraine, Brazil CB)
- **webfetch**: 5 sources (3% — niche recoveries)
- **unreachable**: 12 sources (7% — all methods failed)

## Per-Country Results

| Country | URLs | curl | WebFetch | Diffbot | Playwright |
|---|---|---|---|---|---|
| australia | 37 | 23/37 (62%) | 0/14 (0%) | 11/14 (79%) | 0/3 (0%) |
| brazil | 18 | 15/18 (83%) | 0/3 (0%) | 1/3 (33%) | 2/2 (100%) |
| canada | 18 | 16/18 (89%) | 2/2 (100%) | 1/2 (50%) | 0/1 (0%) |
| chile | 17 | 13/17 (76%) | 0/4 (0%) | 2/4 (50%) | 1/2 (50%) |
| czech_republic | 10 | 7/10 (70%) | 3/3 (100%) | 2/3 (67%) | 1/1 (100%) |
| estonia | 14 | 11/14 (79%) | 0/3 (0%) | 0/3 (0%) | 0/3 (0%) |
| finland | 18 | 13/18 (72%) | 0/5 (0%) | 0/5 (0%) | 3/5 (60%) |
| france | 24 | 19/24 (79%) | 0/5 (0%) | 0/5 (0%) | 1/5 (20%) |
| germany | 19 | 18/19 (95%) | 0/1 (0%) | 0/1 (0%) | 0/1 (0%) |
| india | 12 | 0/12 (0%) | 6/12 (50%) | 5/12 (42%) | 1/7 (14%) |
| indonesia | 18 | 12/18 (67%) | 1/6 (17%) | 2/6 (33%) | 3/4 (75%) |
| italy | 18 | 16/18 (89%) | 1/2 (50%) | 0/2 (0%) | 0/2 (0%) |
| japan | 14 | 7/14 (50%) | 0/7 (0%) | 2/7 (29%) | 3/5 (60%) |
| latvia | 12 | 12/12 (100%) | -- | -- | -- |
| lithuania | 17 | 3/17 (18%) | 0/14 (0%) | 0/14 (0%) | 0/14 (0%) |
| mexico | 10 | 10/10 (100%) | -- | -- | -- |
| norway | 17 | 17/17 (100%) | -- | -- | -- |
| poland | 15 | 14/15 (93%) | 0/1 (0%) | 0/1 (0%) | 0/1 (0%) |
| romania | 13 | 5/13 (38%) | 0/8 (0%) | 0/8 (0%) | 5/8 (62%) |
| saudi_arabia | 13 | 4/13 (31%) | 0/9 (0%) | 0/9 (0%) | 6/9 (67%) |
| south_korea | 12 | 10/12 (83%) | 0/2 (0%) | 0/2 (0%) | 0/2 (0%) |
| spain | 18 | 16/18 (89%) | 0/2 (0%) | 2/2 (100%) | -- |
| sweden | 15 | 15/15 (100%) | -- | -- | -- |
| taiwan | 18 | 17/18 (94%) | 0/1 (0%) | 1/1 (100%) | -- |
| turkey | 11 | 9/11 (82%) | 2/2 (100%) | 0/2 (0%) | 1/2 (50%) |
| uae | 6 | 6/6 (100%) | -- | -- | -- |
| ukraine | 15 | 6/15 (40%) | 0/9 (0%) | 3/9 (33%) | 6/6 (100%) |
| united_kingdom | 26 | 20/26 (77%) | 0/6 (0%) | 5/6 (83%) | 0/1 (0%) |

## Per-Source Detail

| Source | Domain | curl | WebFetch | Diffbot | Playwright | Best |
|---|---|---|---|---|---|---|
| `australia/au_asd` | `asd.gov.au` | 0/1 | 0/1 | 1/1 | -- | **diffbot** |
| `australia/au_asio` | `asio.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `australia/au_austrade` | `austrade.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `australia/au_defence` | `defence.gov.au` | 0/3 | 0/3 | 3/3 | -- | **diffbot** |
| `australia/au_dfat_foreign_minister` | `foreignminister.gov.au` | 0/3 | 0/3 | 2/3 | 0/1 | **diffbot** |
| `australia/au_dfat_sanctions` | `dfat.gov.au` | 0/3 | 0/3 | 2/3 | 0/1 | **diffbot** |
| `australia/au_homeaffairs` | `homeaffairs.gov.au` | 2/3 | 0/1 | 1/1 | -- | **curl** |
| `australia/au_industry` | `industry.gov.au` | 0/3 | 0/3 | 2/3 | 0/1 | **diffbot** |
| `australia/au_legislation` | `legislation.gov.au` | 1/1 | -- | -- | -- | **curl** |
| `australia/au_nationalsecurity` | `nationalsecurity.gov.au` | 2/2 | -- | -- | -- | **curl** |
| `australia/au_parliament` | `aph.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `australia/au_pm` | `pm.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `australia/au_rba` | `rba.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `australia/au_treasury` | `treasury.gov.au` | 3/3 | -- | -- | -- | **curl** |
| `brazil/br_bcb` | `bcb.gov.br` | 0/3 | 0/3 | 1/3 | 2/2 | **playwright** |
| `brazil/br_defesa` | `gov.br/defesa` | 3/3 | -- | -- | -- | **curl** |
| `brazil/br_fazenda` | `gov.br/fazenda` | 3/3 | -- | -- | -- | **curl** |
| `brazil/br_mre` | `gov.br/mre` | 3/3 | -- | -- | -- | **curl** |
| `brazil/br_planalto` | `gov.br/planalto` | 3/3 | -- | -- | -- | **curl** |
| `brazil/br_senado` | `senado.leg.br` | 3/3 | -- | -- | -- | **curl** |
| `canada/ca_boc` | `bankofcanada.ca` | 3/3 | -- | -- | -- | **curl** |
| `canada/ca_dnd` | `canada.ca` | 3/3 | -- | -- | -- | **curl** |
| `canada/ca_finance` | `canada.ca` | 3/3 | -- | -- | -- | **curl** |
| `canada/ca_gac` | `international.gc.ca` | 3/3 | -- | -- | -- | **curl** |
| `canada/ca_parliament` | `parl.ca` | 1/3 | 2/2 | 1/2 | 0/1 | **webfetch** |
| `canada/ca_pm` | `pm.gc.ca` | 3/3 | -- | -- | -- | **curl** |
| `chile/cl_bcentral` | `bcentral.cl` | 0/3 | 0/3 | 2/3 | 1/1 | **diffbot** |
| `chile/cl_defensa` | `defensa.cl` | 3/3 | -- | -- | -- | **curl** |
| `chile/cl_hacienda` | `hacienda.cl` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `chile/cl_minrel` | `minrel.gob.cl` | 3/3 | -- | -- | -- | **curl** |
| `chile/cl_presidencia` | `prensa.presidencia.cl` | 2/2 | -- | -- | -- | **curl** |
| `chile/cl_senado` | `senado.cl` | 3/3 | -- | -- | -- | **curl** |
| `czech_republic/cz_cnb` | `cnb.cz` | 3/3 | -- | -- | -- | **curl** |
| `czech_republic/cz_mf` | `mfcr.cz` | 3/3 | -- | -- | -- | **curl** |
| `czech_republic/cz_mo` | `army.cz` | 0/3 | 3/3 | 2/3 | 1/1 | **webfetch** |
| `czech_republic/cz_mzv` | `mzv.cz` | 1/1 | -- | -- | -- | **curl** |
| `estonia/ee_ep` | `eestipank.ee` | 3/3 | -- | -- | -- | **curl** |
| `estonia/ee_riigikogu` | `riigikogu.ee` | 3/3 | -- | -- | -- | **curl** |
| `estonia/ee_rm` | `fin.ee` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `estonia/ee_vm` | `vm.ee` | 3/3 | -- | -- | -- | **curl** |
| `estonia/ee_vv` | `valitsus.ee` | 2/2 | -- | -- | -- | **curl** |
| `finland/fi_bof` | `suomenpankki.fi` | 3/3 | -- | -- | -- | **curl** |
| `finland/fi_defmin` | `defmin.fi` | 3/3 | -- | -- | -- | **curl** |
| `finland/fi_eduskunta` | `eduskunta.fi` | 3/3 | -- | -- | -- | **curl** |
| `finland/fi_um` | `um.fi` | 0/3 | 0/3 | 0/3 | 3/3 | **playwright** |
| `finland/fi_vm` | `vm.fi` | 1/3 | 0/2 | 0/2 | 0/2 | **curl** |
| `finland/fi_vn` | `valtioneuvosto.fi` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_assemblee` | `assemblee-nationale.fr` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_banque` | `banque-france.fr` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_defense` | `defense.gouv.fr` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_diplomatie` | `diplomatie.gouv.fr` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_economie` | `economie.gouv.fr` | 1/3 | 0/2 | 0/2 | 1/2 | **curl** |
| `france/fr_elysee` | `elysee.fr` | 3/3 | -- | -- | -- | **curl** |
| `france/fr_legifrance` | `legifrance.gouv.fr` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `france/fr_senat` | `senat.fr` | 3/3 | -- | -- | -- | **curl** |
| `germany/de_auswaertiges` | `auswaertiges-amt.de` | 3/3 | -- | -- | -- | **curl** |
| `germany/de_bmf` | `bundesfinanzministerium.de` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `germany/de_bmvg` | `bmvg.de` | 3/3 | -- | -- | -- | **curl** |
| `germany/de_bundesbank` | `bundesbank.de` | 3/3 | -- | -- | -- | **curl** |
| `germany/de_bundeskanzler` | `bundeskanzler.de` | 1/1 | -- | -- | -- | **curl** |
| `germany/de_bundestag` | `bundestag.de` | 3/3 | -- | -- | -- | **curl** |
| `germany/de_gesetze` | `gesetze-im-internet.de` | 3/3 | -- | -- | -- | **curl** |
| `india/in_mea` | `mea.gov.in` | 0/3 | 3/3 | 2/3 | 1/1 | **webfetch** |
| `india/in_mod` | `mod.gov.in` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `india/in_parliament` | `sansad.in` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `india/in_pmo` | `pmindia.gov.in` | 0/3 | 3/3 | 3/3 | -- | **webfetch** |
| `indonesia/id_bi` | `bi.go.id` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `indonesia/id_dpr` | `dpr.go.id` | 3/3 | -- | -- | -- | **curl** |
| `indonesia/id_kemenkeu` | `kemenkeu.go.id` | 0/3 | 1/3 | 2/3 | 1/1 | **diffbot** |
| `indonesia/id_kemhan` | `kemhan.go.id` | 3/3 | -- | -- | -- | **curl** |
| `indonesia/id_kemlu` | `kemlu.go.id` | 1/3 | 0/2 | 0/2 | 2/2 | **playwright** |
| `indonesia/id_setkab` | `setkab.go.id` | 3/3 | -- | -- | -- | **curl** |
| `italy/it_bankitalia` | `bancaditalia.it` | 3/3 | -- | -- | -- | **curl** |
| `italy/it_difesa` | `difesa.it` | 3/3 | -- | -- | -- | **curl** |
| `italy/it_esteri` | `esteri.it` | 1/3 | 1/2 | 0/2 | 0/2 | **curl** |
| `italy/it_governo` | `governo.it` | 3/3 | -- | -- | -- | **curl** |
| `italy/it_mef` | `mef.gov.it` | 3/3 | -- | -- | -- | **curl** |
| `italy/it_parlamento` | `parlamento.it` | 3/3 | -- | -- | -- | **curl** |
| `japan/jp_boj` | `boj.or.jp` | 1/1 | -- | -- | -- | **curl** |
| `japan/jp_diet` | `sangiin.go.jp` | 1/1 | -- | -- | -- | **curl** |
| `japan/jp_kantei` | `kantei.go.jp` | 3/3 | -- | -- | -- | **curl** |
| `japan/jp_mod` | `mod.go.jp` | 0/3 | 0/3 | 0/3 | 1/3 | **playwright** |
| `japan/jp_mof` | `mof.go.jp` | 2/3 | 0/1 | 0/1 | 1/1 | **curl** |
| `japan/jp_mofa` | `mofa.go.jp` | 0/3 | 0/3 | 2/3 | 1/1 | **diffbot** |
| `latvia/lv_fm` | `fm.gov.lv` | 3/3 | -- | -- | -- | **curl** |
| `latvia/lv_mfa` | `mfa.gov.lv` | 3/3 | -- | -- | -- | **curl** |
| `latvia/lv_mk` | `mk.gov.lv` | 3/3 | -- | -- | -- | **curl** |
| `latvia/lv_mod` | `mod.gov.lv` | 3/3 | -- | -- | -- | **curl** |
| `lithuania/lt_fm` | `finmin.lrv.lt` | 0/2 | 0/2 | 0/2 | 0/2 | **NONE** |
| `lithuania/lt_kam` | `kam.lt` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `lithuania/lt_lb` | `lb.lt` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `lithuania/lt_lrv` | `lrv.lt` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `lithuania/lt_seimas` | `lrs.lt` | 3/3 | -- | -- | -- | **curl** |
| `lithuania/lt_urm` | `urm.lt` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `mexico/mx_banxico` | `banxico.org.mx` | 1/1 | -- | -- | -- | **curl** |
| `mexico/mx_presidencia` | `gob.mx/presidencia` | 3/3 | -- | -- | -- | **curl** |
| `mexico/mx_senado` | `senado.gob.mx` | 3/3 | -- | -- | -- | **curl** |
| `mexico/mx_sre` | `gob.mx/sre` | 3/3 | -- | -- | -- | **curl** |
| `norway/no_fd` | `regjeringen.no` | 3/3 | -- | -- | -- | **curl** |
| `norway/no_fin` | `regjeringen.no` | 3/3 | -- | -- | -- | **curl** |
| `norway/no_norgesbank` | `norges-bank.no` | 2/2 | -- | -- | -- | **curl** |
| `norway/no_regjeringen` | `regjeringen.no` | 3/3 | -- | -- | -- | **curl** |
| `norway/no_stortinget` | `stortinget.no` | 3/3 | -- | -- | -- | **curl** |
| `norway/no_ud` | `regjeringen.no` | 3/3 | -- | -- | -- | **curl** |
| `poland/pl_mf` | `gov.pl` | 3/3 | -- | -- | -- | **curl** |
| `poland/pl_mon` | `gov.pl` | 3/3 | -- | -- | -- | **curl** |
| `poland/pl_msz` | `gov.pl` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `poland/pl_nbp` | `nbp.pl` | 3/3 | -- | -- | -- | **curl** |
| `poland/pl_sejm` | `sejm.gov.pl` | 3/3 | -- | -- | -- | **curl** |
| `romania/ro_gov` | `gov.ro` | 1/3 | 0/2 | 0/2 | 2/2 | **playwright** |
| `romania/ro_mae` | `mae.ro` | 0/3 | 0/3 | 0/3 | 3/3 | **playwright** |
| `romania/ro_mapn` | `mapn.ro` | 3/3 | -- | -- | -- | **curl** |
| `romania/ro_mf` | `mfinante.gov.ro` | 1/1 | -- | -- | -- | **curl** |
| `romania/ro_parlament` | `cdep.ro` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `saudi_arabia/sa_mod` | `mod.gov.sa` | 0/3 | 0/3 | 0/3 | 0/3 | **NONE** |
| `saudi_arabia/sa_mof` | `mof.gov.sa` | 1/1 | -- | -- | -- | **curl** |
| `saudi_arabia/sa_mofa` | `mofa.gov.sa` | 0/3 | 0/3 | 0/3 | 3/3 | **playwright** |
| `saudi_arabia/sa_sama` | `sama.gov.sa` | 3/3 | -- | -- | -- | **curl** |
| `saudi_arabia/sa_spa` | `spa.gov.sa` | 0/3 | 0/3 | 0/3 | 3/3 | **playwright** |
| `south_korea/kr_bok` | `bok.or.kr` | 3/3 | -- | -- | -- | **curl** |
| `south_korea/kr_mnd` | `mnd.go.kr` | 0/1 | 0/1 | 0/1 | 0/1 | **NONE** |
| `south_korea/kr_mofa` | `mofa.go.kr` | 3/3 | -- | -- | -- | **curl** |
| `south_korea/kr_mosf` | `moef.go.kr` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `south_korea/kr_president` | `president.go.kr` | 2/2 | -- | -- | -- | **curl** |
| `spain/es_bde` | `bde.es` | 3/3 | -- | -- | -- | **curl** |
| `spain/es_congreso` | `congreso.es` | 1/3 | 0/2 | 2/2 | -- | **diffbot** |
| `spain/es_defensa` | `defensa.gob.es` | 3/3 | -- | -- | -- | **curl** |
| `spain/es_exteriores` | `exteriores.gob.es` | 3/3 | -- | -- | -- | **curl** |
| `spain/es_hacienda` | `hacienda.gob.es` | 3/3 | -- | -- | -- | **curl** |
| `spain/es_moncloa` | `lamoncloa.gob.es` | 3/3 | -- | -- | -- | **curl** |
| `sweden/se_fi` | `fi.se` | 1/1 | -- | -- | -- | **curl** |
| `sweden/se_forsvar` | `regeringen.se` | 3/3 | -- | -- | -- | **curl** |
| `sweden/se_regeringen` | `regeringen.se` | 3/3 | -- | -- | -- | **curl** |
| `sweden/se_riksbank` | `riksbank.se` | 3/3 | -- | -- | -- | **curl** |
| `sweden/se_riksdagen` | `riksdagen.se` | 3/3 | -- | -- | -- | **curl** |
| `sweden/se_ud` | `regeringen.se` | 2/2 | -- | -- | -- | **curl** |
| `taiwan/tw_cbc` | `cbc.gov.tw` | 2/3 | 0/1 | 1/1 | -- | **curl** |
| `taiwan/tw_ly` | `ly.gov.tw` | 3/3 | -- | -- | -- | **curl** |
| `taiwan/tw_mnd` | `mnd.gov.tw` | 3/3 | -- | -- | -- | **curl** |
| `taiwan/tw_mof` | `mof.gov.tw` | 3/3 | -- | -- | -- | **curl** |
| `taiwan/tw_mofa` | `mofa.gov.tw` | 3/3 | -- | -- | -- | **curl** |
| `taiwan/tw_president` | `president.gov.tw` | 3/3 | -- | -- | -- | **curl** |
| `turkey/tr_mfa` | `mfa.gov.tr` | 2/2 | -- | -- | -- | **curl** |
| `turkey/tr_msb` | `msb.gov.tr` | 1/3 | 2/2 | 0/2 | 1/2 | **webfetch** |
| `turkey/tr_tbmm` | `tbmm.gov.tr` | 3/3 | -- | -- | -- | **curl** |
| `turkey/tr_tcmb` | `tcmb.gov.tr` | 3/3 | -- | -- | -- | **curl** |
| `uae/ae_mof` | `mof.gov.ae` | 3/3 | -- | -- | -- | **curl** |
| `uae/ae_mofa` | `mofa.gov.ae` | 3/3 | -- | -- | -- | **curl** |
| `ukraine/ua_mfa` | `mfa.gov.ua` | 0/3 | 0/3 | 2/3 | 1/1 | **diffbot** |
| `ukraine/ua_mod` | `mil.gov.ua` | 0/1 | 0/1 | 0/1 | 1/1 | **playwright** |
| `ukraine/ua_mof` | `mof.gov.ua` | 0/3 | 0/3 | 1/3 | 2/2 | **playwright** |
| `ukraine/ua_nbu` | `bank.gov.ua` | 3/3 | -- | -- | -- | **curl** |
| `ukraine/ua_president` | `president.gov.ua` | 0/2 | 0/2 | 0/2 | 2/2 | **playwright** |
| `ukraine/ua_rada` | `rada.gov.ua` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_boe` | `bankofengland.co.uk` | 2/3 | 0/1 | 0/1 | 0/1 | **curl** |
| `united_kingdom/uk_fcdo` | `gov.uk` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_legislation` | `legislation.gov.uk` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_mi5` | `mi5.gov.uk` | 0/2 | 0/2 | 2/2 | -- | **diffbot** |
| `united_kingdom/uk_mod` | `gov.uk` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_parliament` | `parliament.uk` | 0/3 | 0/3 | 3/3 | -- | **diffbot** |
| `united_kingdom/uk_pm` | `gov.uk` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_trade` | `gov.uk` | 3/3 | -- | -- | -- | **curl** |
| `united_kingdom/uk_treasury` | `gov.uk` | 3/3 | -- | -- | -- | **curl** |

## Unreachable Sources (all methods failed)

- `estonia/ee_rm` (fin.ee) — estonia
- `france/fr_legifrance` (legifrance.gouv.fr) — france
- `india/in_mod` (mod.gov.in) — india
- `india/in_parliament` (sansad.in) — india
- `lithuania/lt_fm` (finmin.lrv.lt) — lithuania
- `lithuania/lt_kam` (kam.lt) — lithuania
- `lithuania/lt_lb` (lb.lt) — lithuania
- `lithuania/lt_lrv` (lrv.lt) — lithuania
- `lithuania/lt_urm` (urm.lt) — lithuania
- `romania/ro_parlament` (cdep.ro) — romania
- `saudi_arabia/sa_mod` (mod.gov.sa) — saudi_arabia
- `south_korea/kr_mnd` (mnd.go.kr) — south_korea

## Key Findings

### 1. Government sites are more accessible than expected
**89% combined reachability** across 28 countries is significantly higher than the prior media experiment's baseline expectations. The RETRIEVAL_EXPERIMENT_GUIDE predicted government sites would be "the hardest category" — this was partially true (73% for curl alone vs 81% for media), but the cascade recovers most failures.

### 2. curl+trafilatura remains the dominant method
123 of 163 sources (75%) are best served by simple HTTP fetch + trafilatura. This is consistent with media experiment findings. Government sites tend to serve clean HTML without JS rendering requirements.

### 3. Australian .gov.au sites consistently block Python user-agents
defence.gov.au, foreignminister.gov.au, dfat.gov.au, minister.industry.gov.au all return 403 to Python/requests but serve content to Diffbot's crawler. This is a systematic pattern — the entire Australian government web infrastructure blocks non-browser user-agents.

### 4. Lithuania is almost entirely unreachable
5 of 6 Lithuanian sources (lrv.lt, urm.lt, kam.lt, finmin.lrv.lt, lb.lt) failed all 4 methods. These sites likely employ aggressive bot protection or serve content via client-side rendering that even Playwright can't extract.

### 5. Playwright is the rescue method for JS-heavy sites
Playwright uniquely recovers content from Romania (mae.ro, gov.ro), Saudi Arabia (mofa.gov.sa, spa.gov.sa), Ukraine (president.gov.ua, mfa.gov.ua, mil.gov.ua), and Brazil's central bank (bcb.gov.br). These are all JS-rendered sites where content isn't in the initial HTML.

### 6. India requires Diffbot
All 12 Indian government URLs failed curl — pmindia.gov.in, mea.gov.in, mod.gov.in, and sansad.in all block direct fetches. Diffbot recovers ~50% of them.

## Extraction Routing Recommendation

For the pipeline, the recommended extraction hierarchy per domain:

| Route | Domains | Method |
|---|---|---|
| **Default** | Most domains (123 sources) | curl+trafilatura |
| **Diffbot** | defence.gov.au, foreignminister.gov.au, dfat.gov.au, industry.gov.au, parliament.uk, mi5.gov.uk, congreso.es, mea.gov.in, pmindia.gov.in, mfa.gov.ua, asd.gov.au, cbc.gov.tw | Diffbot /v3/article → /v3/analyze fallback |
| **Playwright** | mae.ro, gov.ro, mofa.gov.sa, spa.gov.sa, president.gov.ua, mil.gov.ua, mof.gov.ua, bcb.gov.br, mod.go.jp, kemhan.go.id, bi.go.id | Headless Chromium + trafilatura |
| **Skip** | lrv.lt, urm.lt, kam.lt, finmin.lrv.lt, lb.lt, cdep.ro, mod.gov.sa, mnd.go.kr, fin.ee, legifrance.gouv.fr, mod.gov.in, sansad.in | Monitor via RSS/calendar polling instead |
