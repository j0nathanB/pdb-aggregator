# SearchAPI Government Source Discovery — Experiment Report

**Date:** 2026-03-21
**Scope:** 28 countries, 181 government source domains
**API:** SearchAPI.io Google Search (`engine=google`)
**Output:** Per-country JSON files in this directory

---

## Objective

Test whether SearchAPI's Google Search endpoint can reliably discover recent content from known government source domains across all 28 countries in our monitoring universe. The goal is to collect URLs for a subsequent content-fetching experiment — can we extract the actual page content from these government sites?

## Method

For each country, we ran `site:{domain} {search_term}` queries with the following parameters:

| Parameter | Value | Purpose |
|---|---|---|
| `engine` | `google` | Google search via SearchAPI |
| `q` | `site:{domain} {term}` | Scope results to a specific government domain |
| `location` | Capital city (SearchAPI canonical format) | Geo-locate the search origin |
| `gl` | ISO country code | Google country targeting |
| `hl` | Local language code | Interface language |
| `time_period` | `last_month` | Restrict to content indexed in the past 30 days |

Search terms were chosen to be **broad and high-recall** — words like "budget", "security", "sanctions", "inflation" in the local language — to cast a wide net rather than target specific topics.

Google returns up to 10 organic results per query. Each result yields a URL, title, date, and snippet.

## Results Summary

| Metric | Value |
|---|---|
| Countries searched | 28 |
| Total source domains | 181 |
| Sources returning results | 163 (90%) |
| Sources returning zero | 18 (10%) |
| Total URLs collected | 1,338 |
| Average URLs per country | 47.8 |

## Results by Country

| Country | Sources | URLs | Location | gl | Top Domain (results) |
|---|---|---|---|---|---|
| Australia | 14/15 | 101 | Canberra,Australia | au | aph.gov.au (346) |
| United Kingdom | 9/10 | 82 | London,England,United Kingdom | gb | gov.uk (9,390) |
| France | 8/8 | 79 | Paris,Ile-de-France,France | fr | legifrance.gouv.fr (1,350) |
| Germany | 7/7 | 60 | Berlin,Germany | de | bundestag.de (1,830) |
| Taiwan | 6/6 | 57 | Taipei City,Taiwan | tw | mnd.gov.tw (478) |
| Brazil | 6/6 | 56 | Brasilia,Federal District,Brazil | br | senado.leg.br (739) |
| Indonesia | 6/6 | 56 | Jakarta,Indonesia | id | kemenkeu.go.id (291) |
| Spain | 6/6 | 56 | Madrid,Spain | es | defensa.gob.es (208) |
| Japan | 6/6 | 55 | Tokyo,Japan | jp | mod.go.jp (3,000) |
| Canada | 6/6 | 52 | Ottawa,Ontario,Canada | ca | canada.ca (3,790) |
| Italy | 6/6 | 52 | Rome,Lazio,Italy | it | difesa.it (438) |
| Sweden | 6/6 | 51 | Stockholm,Stockholm County,Sweden | se | regeringen.se (859) |
| Poland | 5/6 | 49 | Warsaw,Masovian Voivodeship,Poland | pl | gov.pl (1,730) |
| Norway | 6/6 | 47 | Oslo,Norway | no | regjeringen.no (1,120) |
| Finland | 6/6 | 42 | Helsinki,Uusimaa,Finland | fi | valtioneuvosto.fi (170) |
| Lithuania | 6/6 | 41 | Vilnius,Vilnius County,Lithuania | lt | lrv.lt (114) |
| India | 4/6 | 40 | New Delhi,India | in | pmindia.gov.in (261) |
| Latvia | 4/6 | 40 | Riga,Latvia | lv | mod.gov.lv (76) |
| Romania | 5/6 | 40 | Bucharest,Romania | ro | gov.ro (1,580) |
| Ukraine | 6/6 | 39 | Kyiv,Kyiv City,Ukraine | ua | rada.gov.ua (75) |
| Chile | 6/6 | 38 | Santiago,Santiago Metropolitan Region,Chile | cl | senado.cl (54) |
| Estonia | 5/6 | 38 | Tallinn,Harju County,Estonia | ee | vm.ee (26) |
| South Korea | 5/6 | 33 | Seoul,South Korea | kr | mofa.go.kr (852) |
| Mexico | 4/6 | 32 | Mexico City,Mexico | mx | gob.mx/sre (728) |
| Turkey | 4/6 | 30 | *(none — unsupported)* | tr | msb.gov.tr (68) |
| Saudi Arabia | 5/5 | 29 | Riyadh,Riyadh Province,Saudi Arabia | sa | mod.gov.sa (26) |
| Czech Republic | 4/6 | 23 | Prague,Czechia | cz | cnb.cz (76) |
| UAE | 2/4 | 20 | Abu Dhabi,United Arab Emirates | ae | mofa.gov.ae (243) |

## Domains Returning Zero Results (18)

These are domains where the `site:` + search term combination returned no indexed content in the past month:

| Country | Domain | Likely Reason |
|---|---|---|
| Australia | oni.gov.au | Near-zero publication frequency (intelligence agency) |
| Czech Republic | vlada.cz | Low indexing or CMS that blocks Google |
| Czech Republic | psp.cz | Low indexing of parliamentary content |
| Estonia | kaitseministeerium.ee | Sparse publisher |
| India | finmin.nic.in | Legacy domain, content may have migrated |
| India | rbi.org.in | May use different URL structure than expected |
| Latvia | saeima.lv | Parliament content may not be well-indexed |
| Latvia | bank.lv | Central bank, possibly low recent volume |
| Mexico | gob.mx/sedena | Military — `site:` on subpath doesn't work for gob.mx |
| Mexico | gob.mx/hacienda | Same subpath issue as above |
| Poland | premier.gov.pl | Low-volume publisher |
| Romania | bnr.ro | Central bank, possibly low recent volume |
| South Korea | assembly.go.kr | Parliamentary content may not be well-indexed in Google |
| Turkey | tccb.gov.tr | Presidency — sparse publication or indexing issues |
| Turkey | hmb.gov.tr | Treasury — same issue |
| UAE | mod.gov.ae | Military — possibly not indexed by Google |
| UAE | centralbank.ae | Low recent volume or indexing issues |
| UK | gchq.gov.uk | Intelligence agency — near-zero publication frequency |

## Issues Encountered and Fixes

### 1. SearchAPI Location Format (Critical)

SearchAPI requires Google's canonical location strings, which include the region/state/province — not just `City,Country`. The initial run failed with `400 Bad Request` for 16 countries.

**Fix:** Tested location variants per country. Correct format examples:
- `London,England,United Kingdom` (not `London,United Kingdom`)
- `Paris,Ile-de-France,France` (not `Paris,France`)
- `Ottawa,Ontario,Canada` (not `Ottawa,Canada`)
- `Taipei City,Taiwan` (not `Taipei,Taiwan`)

**Exception:** Turkey has no recognized SearchAPI location. We fall back to `gl=tr` only.

### 2. Google `gl` Country Code (UK)

Google uses `gl=gb` for the United Kingdom, not `gl=uk`. The initial config used `uk`, causing 400 errors for all UK sources.

### 3. Subpath Domains (Poland, Mexico, Brazil)

Countries using centralized government portals (e.g., `gov.pl/dyplomacja`, `gob.mx/sedena`, `gov.br/planalto`) don't work well with Google's `site:` operator scoped to a URL path. Google `site:` only reliably scopes to domain level.

**Fix (Poland):** Changed from `site:gov.pl/dyplomacja sankcje` to `site:gov.pl dyplomacja sankcje` — putting the subpath keyword into the search terms instead. This brought Poland from 2/6 sources (20 URLs) to 5/6 sources (49 URLs).

**Remaining:** Mexico's `gob.mx/sedena` and `gob.mx/hacienda` still return zero and would benefit from the same treatment.

## Observations

### What Works Well
- **English-speaking countries and EU members** produce the highest URL yield, likely due to better Google indexing and more web-native government publishing.
- **Parliamentary sites** are consistently high-yield: `aph.gov.au` (346), `bundestag.de` (1,830), `senat.fr` (864), `senado.leg.br` (739).
- **Central banks** are reliably indexed across all countries — even small ones like Czech CNB (76 results) and Estonia's Eesti Pank (6 results).
- **Defense ministries** are the top publisher in many countries: Japan (3,000), UK (1,290), Italy (438), Spain (208).

### What Works Less Well
- **Intelligence agencies** are near-silent (ONI, GCHQ, ASIO) — expected, and these agencies are better monitored via annual report calendar polling.
- **Middle East sources** (Saudi Arabia, UAE) yield fewer results — may reflect lower Google indexing of Arabic-language government content, or less web-native publishing.
- **Centralized portal countries** (Poland `gov.pl`, Mexico `gob.mx`, Brazil `gov.br`) need search term adjustments since `site:` doesn't scope to URL paths.

### Signal Quality
The URLs collected are a mix of:
1. **High-signal policy content** — press releases, ministerial statements, sanctions updates, budget speeches, bilateral joint statements
2. **Structural/procedural pages** — committee listings, FAQ pages, organizational charts
3. **Transcripts** — press conferences, parliamentary debates, interviews

For the next phase (content fetching), we should prioritize URLs from news/media/release sections and filter out structural pages.

## Script

The repeatable script is `search_gov_sources.py` in this directory:

```bash
# Single country
python3 search_gov_sources.py australia

# Multiple countries
python3 search_gov_sources.py australia france united_kingdom

# All 28 countries
python3 search_gov_sources.py --all

# List configured countries
python3 search_gov_sources.py --list
```

## Next Steps

1. **Content fetching experiment** — attempt to fetch and extract text from the 1,338 collected URLs to determine which government sites allow programmatic access vs. block bots
2. **Fix remaining subpath domains** — apply the Poland fix to Mexico and Brazil
3. **Add pagination** — currently capped at 10 results per source; for high-volume domains we could paginate to collect more URLs
4. **Tune search terms** — some domains would benefit from more specific or multiple queries (e.g., separate "AUKUS" and "budget" searches for `defence.gov.au`)
