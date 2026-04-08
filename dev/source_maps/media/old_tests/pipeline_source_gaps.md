# Pipeline Sources Not Found in Source Intelligence Maps

Pipeline sources (from `configs/countries/*.yaml`) cross-referenced against their
country's Source Intelligence Map. Chile is excluded from this analysis.

---

## Summary

| Metric | Count |
|---|---|
| Total pipeline sources (excl. Chile) | 216 |
| Found in source maps | 107 (50%) |
| **Not found in source maps** | **109 (50%)** |

### By Category

| Category | Missing | Notes |
|---|---|---|
| Wire services | 77 | Global wires (reuters, AP, france24, aljazeera) — not country-specific |
| Government portals | 28 | Official sites in pipeline but not in source maps (which focus on journalism/analysis) |
| Domestic outlets | 4 | Pipeline sources not yet covered by source intelligence maps |

---

## Wire Services (Global — Not Country-Specific)

These appear in every country's pipeline config but were intentionally excluded from
per-country source maps since they are global services.

| Domain | Countries Using |
|---|---|
| `apnews.com` | 27 countries |
| `reuters.com` | 25 countries |
| `france24.com` | 23 countries |
| `aljazeera.com` | 2 countries |

---

## Government Portals Not in Source Maps

Official government sources in the pipeline that don't appear in the source maps.
Source maps included some government sources (e.g., `gov.uk`, `canada.ca`) but may
use different specific domains than the pipeline config.

| Country | Domain | Name |
|---|---|---|
| Australia | `pm.gov.au` | Prime Minister's Office |
| Canada | `pm.gc.ca` | Prime Minister's Office |
| Czech Republic | `vlada.cz` | Government portal |
| Czech Republic | `hrad.cz` | Prague Castle (Presidential office) |
| Estonia | `valitsus.ee` | Government portal |
| Finland | `presidentti.fi` | Presidential office |
| France | `elysee.fr` | Élysée Palace |
| France | `gouvernement.fr` | Government portal |
| Germany | `bundestag.de` | Bundestag |
| India | `pmindia.gov.in` | Prime Minister's Office |
| Indonesia | `presidenri.go.id` | Presidential office |
| Italy | `quirinale.it` | Presidential office |
| Latvia | `mk.gov.lv` | Government portal |
| Latvia | `president.lv` | Presidential office |
| Lithuania | `lrv.lt` | Government portal |
| Lithuania | `president.lt` | Presidential office |
| Poland | `gov.pl` | Government portal |
| Poland | `prezydent.pl` | Presidential office |
| Romania | `gov.ro` | Government portal |
| Saudi Arabia | `mfa.gov.sa` | Ministry of Foreign Affairs |
| South Korea | `president.go.kr` | Presidential office |
| Spain | `casareal.es` | Royal Household |
| Taiwan | `president.gov.tw` | Presidential office |
| Taiwan | `ey.gov.tw` | Executive Yuan |
| Turkey | `tccb.gov.tr` | Presidential office |
| Turkey | `mfa.gov.tr` | Ministry of Foreign Affairs |
| Uae | `mofaic.gov.ae` | Ministry of Foreign Affairs |
| Ukraine | `kmu.gov.ua` | Cabinet of Ministers |

---

## Domestic Sources Not in Source Maps

Pipeline domestic sources absent from the corresponding source intelligence map.
These should be reviewed for inclusion in the maps.

| Country | Domain | Name | Pipeline Tier | Triage Source |
|---|---|---|---|---|
| Czech Republic | `denikreferendum.cz` | Deník Referendum | 3 | No |
| India | `ndtv.com` | NDTV | 2 | Yes |
| Spain | `rtve.es` | RTVE | 2 | No |
| Turkey | `ahvalnews.com` | Ahval News | 2 | Yes |

---

## Per-Country Detail

### Australia

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `abc.net.au` | ABC (Australian Broadcasting) | domestic |
| ✅ | `smh.com.au` | Sydney Morning Herald | domestic |
| ✅ | `theaustralian.com.au` | The Australian | domestic |
| ❌ | `pm.gov.au` | Prime Minister's Office | government |
| ✅ | `defence.gov.au` | Department of Defence | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Brazil

**Pipeline:** 8 | **In map:** 5 | **Missing:** 3

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `folha.uol.com.br` | Folha de S.Paulo | domestic |
| ✅ | `oglobo.globo.com` | O Globo | domestic |
| ✅ | `estadao.com.br` | O Estado de S. Paulo | domestic |
| ✅ | `gov.br` | Federal Government portal | government |
| ✅ | `planalto.gov.br` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Canada

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `cbc.ca` | CBC News | domestic |
| ✅ | `globalnews.ca` | Global News | domestic |
| ✅ | `theglobeandmail.com` | Globe and Mail | domestic |
| ❌ | `pm.gc.ca` | Prime Minister's Office | government |
| ✅ | `canada.ca` | Government of Canada portal | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Czech Republic

**Pipeline:** 8 | **In map:** 2 | **Missing:** 6

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `seznamzpravy.cz` | Seznam Zprávy | domestic |
| ✅ | `irozhlas.cz` | iROZHLAS (Czech Radio) | domestic |
| ❌ | `denikreferendum.cz` | Deník Referendum | domestic |
| ❌ | `vlada.cz` | Government portal | government |
| ❌ | `hrad.cz` | Prague Castle (Presidential office) | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Estonia

**Pipeline:** 7 | **In map:** 3 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `err.ee` | ERR (Estonian Public Broadcasting) | domestic |
| ✅ | `postimees.ee` | Postimees | domestic |
| ✅ | `delfi.ee` | Delfi Estonia | domestic |
| ❌ | `valitsus.ee` | Government portal | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Finland

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `yle.fi` | Yle (Finnish Broadcasting) | domestic |
| ✅ | `hs.fi` | Helsingin Sanomat | domestic |
| ✅ | `iltalehti.fi` | Iltalehti | domestic |
| ✅ | `valtioneuvosto.fi` | Government portal | government |
| ❌ | `presidentti.fi` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### France

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `lemonde.fr` | Le Monde | domestic |
| ✅ | `lefigaro.fr` | Le Figaro | domestic |
| ✅ | `liberation.fr` | Libération | domestic |
| ❌ | `elysee.fr` | Élysée Palace | government |
| ❌ | `gouvernement.fr` | Government portal | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ✅ | `france24.com` | france24.com | wire |

### Germany

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `spiegel.de` | Der Spiegel | domestic |
| ✅ | `faz.net` | Frankfurter Allgemeine Zeitung | domestic |
| ✅ | `sueddeutsche.de` | Süddeutsche Zeitung | domestic |
| ✅ | `bundesregierung.de` | Federal Government portal | government |
| ❌ | `bundestag.de` | Bundestag | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### India

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ❌ | `ndtv.com` | NDTV | domestic |
| ✅ | `thehindu.com` | The Hindu | domestic |
| ✅ | `indianexpress.com` | Indian Express | domestic |
| ❌ | `pmindia.gov.in` | Prime Minister's Office | government |
| ✅ | `mea.gov.in` | Ministry of External Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Indonesia

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `kompas.com` | Kompas | domestic |
| ✅ | `tempo.co` | Tempo | domestic |
| ✅ | `thejakartapost.com` | Jakarta Post | domestic |
| ❌ | `presidenri.go.id` | Presidential office | government |
| ✅ | `kemlu.go.id` | Ministry of Foreign Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Italy

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `corriere.it` | Corriere della Sera | domestic |
| ✅ | `repubblica.it` | La Repubblica | domestic |
| ✅ | `ansa.it` | ANSA | domestic |
| ✅ | `governo.it` | Government portal | government |
| ❌ | `quirinale.it` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Japan

**Pipeline:** 8 | **In map:** 7 | **Missing:** 1

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `nhk.or.jp` | NHK | domestic |
| ✅ | `asahi.com` | Asahi Shimbun | domestic |
| ✅ | `nikkei.com` | Nikkei | domestic |
| ✅ | `kantei.go.jp` | Prime Minister's Office | government |
| ✅ | `mofa.go.jp` | Ministry of Foreign Affairs | government |
| ✅ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ✅ | `kyodonews.net` | kyodonews.net | wire |

### Latvia

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `lsm.lv` | LSM (Latvian Public Media) | domestic |
| ✅ | `delfi.lv` | Delfi Latvia | domestic |
| ✅ | `tvnet.lv` | TVnet | domestic |
| ❌ | `mk.gov.lv` | Government portal | government |
| ❌ | `president.lv` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Lithuania

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `lrt.lt` | LRT (Lithuanian National Radio and Television) | domestic |
| ✅ | `delfi.lt` | Delfi Lithuania | domestic |
| ✅ | `15min.lt` | 15min | domestic |
| ❌ | `lrv.lt` | Government portal | government |
| ❌ | `president.lt` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Mexico

**Pipeline:** 10 | **In map:** 7 | **Missing:** 3

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `eluniversal.com.mx` | El Universal | domestic |
| ✅ | `reforma.com` | Reforma | domestic |
| ✅ | `jornada.com.mx` | La Jornada | domestic |
| ✅ | `proceso.com.mx` | Proceso | domestic |
| ✅ | `animalpolitico.com` | Animal Político | domestic |
| ✅ | `gob.mx` | Government portal | government |
| ✅ | `sre.gob.mx` | SRE | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Norway

**Pipeline:** 7 | **In map:** 4 | **Missing:** 3

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `nrk.no` | NRK (Norwegian Broadcasting) | domestic |
| ✅ | `vg.no` | VG | domestic |
| ✅ | `aftenposten.no` | Aftenposten | domestic |
| ✅ | `regjeringen.no` | Government portal | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Poland

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `wyborcza.pl` | Gazeta Wyborcza | domestic |
| ✅ | `tvn24.pl` | TVN24 | domestic |
| ✅ | `onet.pl` | Onet | domestic |
| ❌ | `gov.pl` | Government portal | government |
| ❌ | `prezydent.pl` | Presidential office | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Romania

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `digi24.ro` | Digi24 | domestic |
| ✅ | `hotnews.ro` | HotNews | domestic |
| ✅ | `g4media.ro` | G4Media | domestic |
| ❌ | `gov.ro` | Government portal | government |
| ✅ | `presidency.ro` | Presidential administration | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Saudi Arabia

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `arabnews.com` | Arab News | domestic |
| ✅ | `saudigazette.com.sa` | Saudi Gazette | domestic |
| ✅ | `aleqt.com` | Al Eqtisadiah | domestic |
| ✅ | `spa.gov.sa` | Saudi Press Agency | government |
| ❌ | `mfa.gov.sa` | Ministry of Foreign Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `aljazeera.com` | aljazeera.com | wire |

### South Korea

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `koreaherald.com` | Korea Herald | domestic |
| ✅ | `en.yna.co.kr` | Yonhap News Agency | domestic |
| ✅ | `chosun.com` | Chosun Ilbo | domestic |
| ❌ | `president.go.kr` | Presidential office | government |
| ✅ | `mofa.go.kr` | Ministry of Foreign Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Spain

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `elpais.com` | El País | domestic |
| ✅ | `elmundo.es` | El Mundo | domestic |
| ❌ | `rtve.es` | RTVE | domestic |
| ✅ | `lamoncloa.gob.es` | Government portal (Moncloa) | government |
| ❌ | `casareal.es` | Royal Household | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Sweden

**Pipeline:** 8 | **In map:** 5 | **Missing:** 3

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `svt.se` | SVT (Swedish Television) | domestic |
| ✅ | `dn.se` | Dagens Nyheter | domestic |
| ✅ | `svd.se` | Svenska Dagbladet | domestic |
| ✅ | `government.se` | Government portal | government |
| ✅ | `riksdagen.se` | Riksdag | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Taiwan

**Pipeline:** 8 | **In map:** 3 | **Missing:** 5

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `focustaiwan.tw` | Focus Taiwan (CNA English) | domestic |
| ✅ | `taipeitimes.com` | Taipei Times | domestic |
| ✅ | `ltn.com.tw` | Liberty Times | domestic |
| ❌ | `president.gov.tw` | Presidential office | government |
| ❌ | `ey.gov.tw` | Executive Yuan | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Turkey

**Pipeline:** 8 | **In map:** 2 | **Missing:** 6

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `dailysabah.com` | Daily Sabah | domestic |
| ❌ | `ahvalnews.com` | Ahval News | domestic |
| ✅ | `bianet.org` | Bianet | domestic |
| ❌ | `tccb.gov.tr` | Presidential office | government |
| ❌ | `mfa.gov.tr` | Ministry of Foreign Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### Uae

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `thenationalnews.com` | The National | domestic |
| ✅ | `gulfnews.com` | Gulf News | domestic |
| ✅ | `khaleejtimes.com` | Khaleej Times | domestic |
| ✅ | `wam.ae` | WAM (Emirates News Agency) | government |
| ❌ | `mofaic.gov.ae` | Ministry of Foreign Affairs | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `aljazeera.com` | aljazeera.com | wire |

### Ukraine

**Pipeline:** 8 | **In map:** 4 | **Missing:** 4

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `pravda.com.ua` | Ukrainska Pravda | domestic |
| ✅ | `liga.net` | Liga.net | domestic |
| ✅ | `zn.ua` | Dzerkalo Tyzhnia (Mirror Weekly) | domestic |
| ✅ | `president.gov.ua` | Presidential office | government |
| ❌ | `kmu.gov.ua` | Cabinet of Ministers | government |
| ❌ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |

### United Kingdom

**Pipeline:** 8 | **In map:** 6 | **Missing:** 2

| Status | Domain | Name | Category |
|---|---|---|---|
| ✅ | `bbc.co.uk` | BBC News | domestic |
| ✅ | `theguardian.com` | The Guardian | domestic |
| ✅ | `ft.com` | Financial Times | domestic |
| ✅ | `gov.uk` | UK Government portal | government |
| ✅ | `parliament.uk` | UK Parliament | government |
| ✅ | `reuters.com` | reuters.com | wire |
| ❌ | `apnews.com` | apnews.com | wire |
| ❌ | `france24.com` | france24.com | wire |
