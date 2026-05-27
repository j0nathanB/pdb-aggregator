# Proposal: off-topic filtering for story_map input (Part D)

Generated from 2026-04-12 traces (29 country runs). URLs that appeared in
story_map input but did NOT land in the parsed output (i.e., the LLM dropped
them as noise/off-topic) are the basis of the recommendations below.

## Finding: the 70-90% 'noise drop' rate breaks down into 3 categories

1. **Propaganda / fake-news networks** with very high cross-country volume
2. **Off-topic domains** (sports/entertainment blogs) that are basically never useful
3. **Off-topic paths on legit domains** (e.g. `/sport/` on welt.de)

There's a fourth, much bigger category — **off-focus news** (legit news about
the wrong topic for the country brief — crime, local politics, weather). That's
*not* filterable by URL path, and Part D can't help with it. The LLM will
continue to drop this as noise. The upstream fix is Part A (better goggles)
and potentially a domain-level derank strategy.

---

## 1. Propaganda network additions (add to ALL country goggles as `$discard`)

Russian-linked disinformation network. 34 variants found
across the 2026-04-12 traces, leaking into multiple country runs:

- `au.news-pravda.com` — 1 appearances across 1 countries: au
- `austria.news-pravda.com` — 1 appearances across 1 countries: ua
- `balkan.news-pravda.com` — 1 appearances across 1 countries: kr
- `bulgaria.news-pravda.com` — 1 appearances across 1 countries: ua
- `burkina-faso.news-pravda.com` — 2 appearances across 2 countries: fr, jp
- `czechia.news-pravda.com` — 4 appearances across 1 countries: cz
- `denmark.news-pravda.com` — 2 appearances across 1 countries: no
- `deutsch.news-pravda.com` — 27 appearances across 2 countries: de, ua
- `estonia.news-pravda.com` — 29 appearances across 3 countries: ee, jp, ua
- `eu.news-pravda.com` — 12 appearances across 4 countries: ae, gb, jp, ua
- `finland.news-pravda.com` — 3 appearances across 2 countries: fi, jp
- `francais.news-pravda.com` — 1 appearances across 1 countries: fr
- `france.news-pravda.com` — 3 appearances across 1 countries: jp
- `germany.news-pravda.com` — 11 appearances across 4 countries: de, ee, sa, ua
- `hungary.news-pravda.com` — 3 appearances across 2 countries: jp, ua
- `italy.news-pravda.com` — 16 appearances across 2 countries: au, ua
- `japan.news-pravda.com` — 2 appearances across 1 countries: jp
- `latvia.news-pravda.com` — 9 appearances across 5 countries: ee, jp, lt, lv, ua
- `lt.news-pravda.com` — 10 appearances across 1 countries: lt
- `nato.news-pravda.com` — 15 appearances across 7 countries: cz, de, jp, ro, se, tw, ua
- `news-pravda.com` — 2 appearances across 1 countries: ua
- `norway.news-pravda.com` — 1 appearances across 2 countries: no, ua
- `poland.news-pravda.com` — 5 appearances across 2 countries: de, ua
- `rca.news-pravda.com` — 2 appearances across 2 countries: jp, ua
- `romania.news-pravda.com` — 1 appearances across 1 countries: ua
- `slovakia.news-pravda.com` — 2 appearances across 1 countries: cz
- `spain.news-pravda.com` — 9 appearances across 6 countries: cl, es, gb, sa, se, ua
- `spanish.news-pravda.com` — 1 appearances across 1 countries: cz
- `sweden.news-pravda.com` — 9 appearances across 2 countries: fr, se
- `trump.news-pravda.com` — 2 appearances across 1 countries: ua
- `turkey.news-pravda.com` — 1 appearances across 1 countries: jp
- `ua.news-pravda.com` — 14 appearances across 3 countries: ae, jp, ua
- `uk.news-pravda.com` — 5 appearances across 2 countries: jp, ua
- `usa.news-pravda.com` — 2 appearances across 2 countries: ca, ua

**Action**: add these to ALL 30 country goggles. The pattern `news-pravda.com`
and all subdomains should be globally banned. Consider adding an
`assets/country_goggles/_global_discards.txt` or similar shared mechanism
so propaganda additions don't require editing 30 files.

## 2. All-noise domain additions (per-country goggle $discard based on where they appear)

50 domains accumulated 10+ appearances in the 2026-04-12 run
with 0-1 kept — effectively always noise:

| Domain | Total noise | Countries where it appeared | Suggested action |
|---|---:|---|---|
| `nation.com.pk` | 31 | jp, kr, pk, sa | ? |
| `welt.de` | 28 | de, ro | German paper, cross-country leak |
| `sagat.no` | 28 | no | ? |
| `economictimes.indiatimes.com` | 27 | ae, au, cl, fr, id, in, jp, lv, ro, sa,  | Indian paper, cross-country leak |
| `en.interfax.com.ua` | 27 | ro, ua | ? |
| `express.co.uk` | 21 | au, gb, lv, no, tw | ? |
| `sueddeutsche.de` | 21 | cz, de, ua | German paper, cross-country leak |
| `nbssport.co.ug` | 20 | ca, lv | sports aggregator |
| `merkur.de` | 18 | de, ro, se | ? |
| `starnewskorea.com` | 17 | gb, kr, tw | entertainment |
| `indiatoday.in` | 17 | in, lt, pk, ro, sa, tw | Indian paper, cross-country leak |
| `newsable.asianetnews.com` | 16 | ae, br, gb, in, kr, lv, tw, ua | ? |
| `nbcnews.com` | 16 | ae, au, gb, in, kr, lv, pk, sa, se, tw | ? |
| `lapresse.ca` | 15 | ca, fr | Canadian/French paper, cross-country leak |
| `marketbeat.com` | 15 | ca, es, lv, mx, no, pk, pl, tw | spam/SEO |
| `letelegramme.fr` | 15 | ca, ee, fr | Canadian/French paper, cross-country leak |
| `zeit.de` | 15 | cz, de | German paper, cross-country leak |
| `onaquietday.org` | 15 | gb, no | blog spam |
| `battinews.com` | 15 | ro | blog spam |
| `dailypolitical.com` | 14 | ca, es, lv, no, pk, pl, sa | spam/SEO |
| `di.se` | 14 | se | ? |
| `it-boltwise.de` | 13 | ae, de | ? |
| `newsweek.com` | 12 | ae, kr, lv, mx, no, tr, tw, ua | ? |
| `excelsior.com.mx` | 12 | br, cl, cz, ee, mx | ? |
| `elpais.com.uy` | 12 | cl | ? |
| `eleconomista.com.mx` | 12 | cl, cz, mx | ? |
| `tagesspiegel.de` | 12 | de, se | ? |
| `gbnews.com` | 12 | gb, jp, kr | ? |
| `zazoom.it` | 12 | it, sa | ? |
| `infomoney.com.br` | 11 | ae, br, lv | ? |

Caveats:
- Some of these are *legitimate domestic papers* that leaked into OTHER countries'
  queries (e.g. welt.de into Romania) — DO NOT globally discard those. Handle by
  adding to the non-home country's goggle as a `$discard`, or better: improve the
  home-country goggle so domestic sources outrank imported coverage.
- The propaganda domains and sports aggregators ARE safe to globally discard.

## 3. Path-level filters (`off_topic_filters.csv` proposal)

21 domain+path combinations with noise≥3, kept≤1 in the 2026-04-12 run.
Would drop ~78 URLs per run of that profile.

Schema mirrors `opinion_filters.csv`:
`domain,filter_type,filter_pattern,country,rationale`

Starter CSV (review per-row before adoption):

```csv
domain,filter_type,filter_pattern,country,rationale
closermag.fr,path,/people/,fr,noise=7 kept=1 in fr
timesofindia.indiatimes.com,path,/sports/,multi,noise=6 kept=0 in au,kr,ro,ua
yahoo.com,path,/entertainment/,gb,noise=6 kept=0 in gb
starnewskorea.com,path,/music/,tw,noise=5 kept=0 in tw
alairelibre.cl,path,/futbol/,cl,noise=4 kept=0 in cl
timesofindia.indiatimes.com,path,/entertainment/,multi,noise=4 kept=0 in ee,gb,pk,sa
dailymail.co.uk,path,/tvshowbiz/,multi,noise=4 kept=0 in gb,ro,tw
heavy.com,path,/sports/,multi,noise=3 kept=0 in au,in,lv
ohtuleht.ee,path,/sport/,ee,noise=3 kept=0 in ee
bbc.com,path,/sport/,multi,noise=3 kept=0 in ee,gb,ro
heraldo.es,path,/deportes/,fi,noise=3 kept=0 in fi
express.co.uk,path,/showbiz/,gb,noise=3 kept=0 in gb
gmanetwork.com,path,/showbiz/,id,noise=3 kept=0 in id
rotowire.com,path,/baseball/,multi,noise=3 kept=0 in in,pl
telegraaf.nl,path,/sport/,jp,noise=3 kept=0 in jp
indiatoday.in,path,/sports/,lt,noise=3 kept=0 in lt
elnacional.cat,path,/deportes/,mx,noise=3 kept=0 in mx
bunte.de,path,/entertainment/,multi,noise=3 kept=0 in pk,ro
hindustantimes.com,path,/entertainment/,sa,noise=3 kept=0 in sa
shieldsgazette.com,path,/sport/,sa,noise=3 kept=0 in sa
expressen.se,path,/sport/,se,noise=3 kept=0 in se
```

## 4. Implementation notes

- The path-filter CSV gives modest gains (~85 URLs/run) — worth doing for
  unambiguous cases, but low-leverage overall.
- The bigger wins are (1) propaganda/spam domain discards and (2) Part A goggle
  completeness for each country's home sources.
- Suggested loader API:

  ```python
  # src/monitor/collection/filters.py
  def load_off_topic_filters() -> list[dict]: ...
  def is_off_topic_url(url: str, country_code: str | None = None) -> bool: ...
  ```

  Called from `brave.search_news` alongside the discard check (Part B). Same
  control surface: log count of drops per country per run.
