# Plan: reduce story_map input volume (goggle audit + formatter caps)

## Context

Investigating why `story_map` LLM output is getting truncated at the 24,192
`max_tokens` ceiling (see `dev/story_map_tool_use_plan.md` for the tool-use
fix to malformed JSON). That work is downstream — fixing JSON validity but
not output size. The upstream problem is that story_map receives 350k
characters of search-result text per country, and the LLM's clustering
output grows with input volume.

Investigation on the 2026-04-12 run (29 countries) found:

- **82% of items (9,456 / 11,483) sent to story_map come from unboosted
  domains** — the goggles' top-tier sources account for only 18% of the
  pool
- **148 results from `$discard`-listed domains leaked through** —
  Brave's `$discard` directive deranks but doesn't remove
- **4 of 5 search buckets** (`wire`, `domestic`, `vocab`) are empty for
  most countries — only `actor` fires, producing 400-500 near-duplicate
  results per country
- Heavy per-domain concentration: 28 welt.de, 34 ansa.it, etc. — many
  URLs per single outlet covering the same story

The full audit is in `dev/goggle_audit_2026-04-12.md` — top unboosted
domains per country and discard-leak counts.

## Why this matters

- Input bloat drives output bloat. Story_map writes JSON describing every
  cluster; 400 items produce more stories/longer article arrays than 200
  items would.
- The 350k-char input cap is already truncating 100-160 results per run for
  large countries (fr/it/mx/de). The pipeline has been running near-edge
  for a while.
- Cutting input volume by half would eliminate most of the output
  truncation, **and** let you raise clustering quality because the LLM sees
  less noise.

## Scope

### Part A: Goggle audit and expansion

Goggles were built from an incomplete seed (looks like think-tanks +
government portals + a few major outlets) and don't cover the mainstream
news sources that actually dominate Brave's results.

Examples of obvious mainstream outlets NOT in the goggles today but
appearing heavily in search results:

- **AU**: theguardian.com (Guardian AU — 18), abc.net.au (ABC — 17),
  smh.com.au (SMH — 11). Goggle currently has only 21 boosts total and
  only 3% of AU results come from boosted sources.
- **IT**: repubblica.it (top-3 Italian paper — 22 results, unboosted).
  Also tg24.sky.it (Sky Italia).
- **DE**: tagesschau.de (public broadcaster — 18, unboosted),
  n-tv.de (20), bild.de (15, tabloid — probably wants to be discarded).
- **FR**: franceinfo.fr (public broadcaster — 13), leparisien.fr (13),
  letelegramme.fr (14), bfmtv.com (14).
- **MX**: infobae.com (13), eleconomista.com.mx (10).

Task: for each of 30 countries, review the top 10-20 unboosted domains
from `dev/goggle_audit_2026-04-12.md` and assign tier-10/5/3/discard as
appropriate. The audit is already structured to make this a direct review
— look at the per-country "Top 10 unboosted domains" table, decide for
each one.

### Part B: In-pipeline discard enforcement

Brave's `$discard` is best-effort. 148 results from `$discard`-listed
domains came through on 2026-04-12. Worst offender: FR with 7 leaks (cnews,
valeursactuelles, rt.com variants — all politically-loaded sources the user
explicitly excluded).

Fix: add a post-fetch domain blocklist filter that runs after Brave results
come back. This gives deterministic exclusion regardless of Brave's
behavior. Source the blocklist from the goggle's `$discard` directives at
load time so there's a single source of truth.

Location: probably `src/monitor/collection/brave.py` — after
`search_news()` returns, filter results whose `source_domain` matches any
discard entry for that country.

### Part C: Formatter caps (defensive)

Even with better goggles and blocklists, single outlets can still dominate.
Add a per-domain cap in `_format_search_results` (story_map.py:159-184):

```python
def _add_results(results, source_label, per_domain_cap=10):
    domain_counts = Counter()
    for r in results:
        d = r.source_domain
        if domain_counts[d] >= per_domain_cap:
            # Log skipped; surface in dedup_record
            continue
        domain_counts[d] += 1
        ...
```

**Cap = 10** chosen based on analysis of the 2026-04-12 run (see notes
below). A cap of 5 would lose ~5% of output stories in the best case
because domains like `ansa.it` (34 input → 12 kept → 12 distinct stories)
cover many different stories per week at 1 article per story — each
article is its own story, not a near-duplicate. Cap=10 loses <1% of
stories best-case while still trimming the worst bloat cases
(`aftonbladet.se` 93→10, `yle.fi` 92→10, `lrt.lt` 87→10).

Story-diversity data from 2026-04-12 (per (country, domain), across all
29 countries):

| Input URLs from one domain | Median output stories | Median % dropped by LLM as noise |
|---:|---:|---:|
| 5 | 1 | 80% |
| 10 | 3 | 70% |
| 15 | 3.5 | 77% |
| 20 | 2 | 85% |
| 25-39 | 3 | 86% |

Record skipped counts in `dedup_record` for visibility. Don't trim
snippet length — story_map does both clustering and filtering from the
snippet alone (it never sees full article text; that happens later in
the extraction stage). Shorter snippets = worse clustering and worse
off-topic detection.

### Part D: URL-path filtering for off-topic sections

The LLM currently drops 70-90% of input URLs as off-topic
(sports/entertainment/lifestyle). This is an *enormous* amount of noise
wasting input tokens. Examples from the 2026-04-12 run:

- `aftonbladet.se`: 93 input URLs → 4 kept (96% noise)
- `yle.fi`: 92 → 10 (89% noise)
- `lrt.lt`: 87 → 5 (94% noise)
- `lsm.lv`: 31 → 11 (65% noise)
- `ansa.it`: 34 → 12 (65% noise)

Most of this noise is recognizable from URL paths alone without reading
the snippet: `/sport/`, `/deportes/`, `/esportes/`, `/fussball/`,
`/entertainment/`, `/celebrity/`, `/lifestyle/`, `/gaming/`, `/fashion/`,
etc. Filtering at the URL-path level drops items **before** story_map
sees them — cutting tokens without touching snippet quality for the
items that remain.

Precedent: `opinion_filters.csv` (referenced from
`src/monitor/collection/extract.py:75`) already implements the pattern
for opinion pieces:

```csv
domain,opinion_type,opinion_pattern
welt.de,path,/meinung/
```

Supported rule types in the existing loader: `path` (startswith),
`subdomain` (exact), `regex` (compiled pattern).

Task: add `off_topic_filters.csv` with the same schema, covering
per-domain and cross-cutting off-topic paths. Wire it into the pipeline
at a point BEFORE `_format_search_results` — probably in
`src/monitor/collection/brave.py` or `src/monitor/agents/expansion.py`
where results are first assembled. Log drops per filter for visibility.

Starter set from observed noise patterns (verify per-domain before
merging):

- German papers: `/sport/`, `/sport-`, `/panorama/`, `/leute/`, `/unterhaltung/`
- Spanish/LatAm: `/deportes/`, `/entretenimiento/`, `/espectaculos/`, `/gente/`
- Portuguese (BR): `/esportes/`, `/cultura/`, `/celebridades/`
- Italian: `/sport/`, `/spettacoli/`, `/gossip/`
- Nordic: `/sport/`, `/sport-`, `/kultur/`, `/nöjen/`, `/urheilu/`
- English tabloid-ish: `/showbiz/`, `/tvshowbiz/`, `/celebrity/`, `/entertainment/`

This is the highest-leverage volume reduction available without touching
anything else. A single well-placed path filter on aftonbladet.se alone
would cut ~90 URLs from the SE input on a typical week.

### Part E: Investigate empty search buckets

Separate diagnostic. Why are `triage_wire`, `triage_domestic`, and
`vocab_results` empty for most countries? Expected pipeline behavior, or
broken? Look at `src/monitor/agents/expansion.py` to understand what
populates these, and run a test on one country to see whether they SHOULD
have content.

If they're broken: fixing them adds diversity and probably improves
clustering quality (different search strategies surface different stories).
If they're intentionally empty: the four-pool design is misleading — rename
or consolidate.

## Implementation order

1. **Part B first** (discard enforcement) — smallest change, deterministic
   impact, immediately cleans politically-loaded outlets from the pool.
2. **Part D** (URL-path filters for off-topic sections) — highest volume
   leverage; drops the 70-90% noise before it reaches the LLM. Build
   `off_topic_filters.csv` from observed patterns, wire in before
   story_map formatting.
3. **Part C** (per-domain cap=10) — defensive backstop after B and D.
   Catches anything the goggles and URL filters don't.
4. **Part A** (goggle expansion) — manual-review-heavy but high-leverage.
   Do country-by-country from the audit file.
5. **Part E** (empty-buckets investigation) — diagnostic; its outcome
   dictates whether more work is needed.

Parts B and D will measurably reduce input volume even before goggle work.
Expected outcome after all five: input drops from the 350k-char cap to
somewhere in the 100-180k range for most countries, output truncation goes
away, clustering quality improves because the LLM sees a cleaner pool.

## Validation

After each part lands, re-run the audit script against the new traces
(same methodology as `dev/goggle_audit_2026-04-12.md` generation) and
check:

- % from boosted sources goes up (target: >50% from boosted, not 18%)
- Discard leaks drop to 0 (Part B)
- Noise-drop rate by the LLM drops from 70-90% toward ~30% because most
  off-topic URLs never reach it (Part D)
- No single domain exceeds per-domain cap of 10 (Part C)
- Total item count per country drops meaningfully (Parts A+C+D)
- No story_map output truncation at max_tokens (downstream effect)

## Related work

- `dev/story_map_tool_use_plan.md` — fixes JSON validity via tool-use.
  Orthogonal to this plan; both should land, but order doesn't matter.
- `max_tokens` bump (called out in the tool-use plan) — separate one-line
  change. With this plan's volume cuts it may become unnecessary.
