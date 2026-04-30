# Baseline Prompt-Token Analysis — 2026-04-28

Source: weekly Sunday pipeline runs at `briefs/20260419` and `briefs/20260426`.
Cache fields are absent from these traces (instrumentation lands in this same PR);
this analysis uses `input_tokens` as a proxy for cache-firing behavior.

## Q1 — Is country.py's cache_control producing cross-country reuse?

**Test:** if cache was firing across the 28 country calls per week, calls 2-28
would have much smaller `input_tokens` than call 1 (which writes the cache).
Uniform `input_tokens` across all 28 = cache is NOT producing cross-country reuse.

Coefficient of variation (stdev/mean) close to 0 = uniform = cache not helping cross-country.

### Week 20260419

- Country calls: 30
- input_tokens: min=39,816, median=56,820, mean=58,871, max=82,817
- stdev=9,427, **coefficient of variation = 0.16**

Lowest 3 + highest 3 by input_tokens:

  - de: 39,816
  - no: 47,423
  - cz: 48,715
  - es: 72,918
  - cl: 74,352
  - lv: 82,817

### Week 20260426

- Country calls: 30
- input_tokens: min=53,815, median=72,010, mean=75,629, max=106,549
- stdev=12,968, **coefficient of variation = 0.171**

Lowest 3 + highest 3 by input_tokens:

  - pk: 53,815
  - ee: 55,332
  - ae: 60,772
  - jp: 97,071
  - lv: 100,585
  - lt: 106,549

## Q2 — Per-agent baseline hit rates

All agents except `country` have no `cache_control` today — baseline is 0 by
construction. Listing per-agent call counts and token volumes confirms what's
uninstrumented.

### Week 20260419

| agent | calls | total input | mean input | median input | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| copyeditor | 39 | 481,395 | 12,343 | 12,110 | 991 | 10,969 | 15,331 |
| country | 30 | 1,766,147 | 58,871 | 56,820 | 9,427 | 39,816 | 82,817 |
| devils_advocate | 30 | 242,173 | 8,072 | 7,940 | 1,261 | 5,831 | 11,224 |
| editor | 38 | 801,741 | 21,098 | 21,974 | 3,070 | 10,874 | 26,207 |
| executive | 1 | 38,374 | 38,374 | 38,374 | 0 | 38,374 | 38,374 |
| global_writer | 1 | 16,942 | 16,942 | 16,942 | 0 | 16,942 | 16,942 |
| government | 30 | 365,158 | 12,171 | 9,812 | 9,334 | 3,975 | 52,268 |
| regional | 6 | 78,536 | 13,089 | 12,902 | 1,537 | 10,770 | 15,151 |
| regional_writer | 6 | 87,001 | 14,500 | 14,632 | 1,069 | 13,338 | 16,210 |
| story_map | 29 | 3,149,943 | 108,618 | 112,423 | 20,438 | 56,739 | 152,853 |
| style_editor | 37 | 410,878 | 11,104 | 11,120 | 268 | 10,495 | 11,632 |

### Week 20260426

| agent | calls | total input | mean input | median input | stdev | min | max |
|---|---:|---:|---:|---:|---:|---:|---:|
| copyeditor | 38 | 476,809 | 12,547 | 12,457 | 929 | 11,186 | 15,408 |
| country | 30 | 2,268,882 | 75,629 | 72,010 | 12,968 | 53,815 | 106,549 |
| devils_advocate | 30 | 252,494 | 8,416 | 8,396 | 1,290 | 4,492 | 11,377 |
| editor | 37 | 867,624 | 23,449 | 24,003 | 3,101 | 13,950 | 28,507 |
| executive | 1 | 39,489 | 39,489 | 39,489 | 0 | 39,489 | 39,489 |
| global_writer | 1 | 16,368 | 16,368 | 16,368 | 0 | 16,368 | 16,368 |
| government | 30 | 336,266 | 11,208 | 9,209 | 8,291 | 3,906 | 46,056 |
| regional | 6 | 84,788 | 14,131 | 14,297 | 1,994 | 10,653 | 16,880 |
| regional_writer | 6 | 91,228 | 15,204 | 14,610 | 1,176 | 14,300 | 17,046 |
| story_map | 30 | 3,291,494 | 109,716 | 111,542 | 19,432 | 64,663 | 155,409 |
| style_editor | 37 | 410,718 | 11,100 | 11,244 | 398 | 10,131 | 11,702 |

## Q3 — Per-agent leverage budget

Total `input_tokens` per agent across both weeks ranks the leverage opportunity.
An agent with 3M input tokens and a stable system prefix beats one with 100K.

| agent | 2-week total input | 2-week total output | rank by input volume |
|---|---:|---:|---:|
| story_map | 6,441,437 | 1,695,461 | 1 |
| country | 4,035,029 | 1,140,968 | 2 |
| editor | 1,669,365 | 396,609 | 3 |
| copyeditor | 958,204 | 605,941 | 4 |
| style_editor | 821,596 | 441,342 | 5 |
| government | 701,424 | 553,872 | 6 |
| devils_advocate | 494,667 | 200,594 | 7 |
| regional_writer | 178,229 | 53,440 | 8 |
| regional | 163,324 | 144,820 | 9 |
| executive | 77,863 | 46,479 | 10 |
| global_writer | 33,310 | 9,692 | 11 |

## Deep dive — mx, de across both weeks

If country.py's cache was firing on re-runs (same country, different weeks within
5-min TTL — unlikely across week-apart runs but instructive for prompt-size variance),
we'd see it here. Mostly this shows per-country prompt-size baseline.

### mx

- week 20260419: input=59,550, output=18,289
- week 20260426: input=71,913, output=21,556

### de

- week 20260419: input=39,816, output=10,050
- week 20260426: input=70,223, output=24,026

## Verdicts

**Q1:** See coefficient of variation above. CV < 0.1 = strong evidence cache
is NOT producing cross-country reuse (input_tokens uniform = each call paid full
prompt cost). CV > 0.3 = some calls smaller, possibly cache-related (more likely
ledger-size variance). Definitive answer awaits Sunday run with cache fields.

**Q2:** Confirmed — every non-country agent has 0% cache hit rate today (no
`cache_control` in their request shape). Floor for Phase 4 hit-rate alerting.

**Q3:** Top-ranked agents by 2-week input volume are the highest-leverage targets.
Compare to the editor cluster (which has the additional shared-prefix opportunity
across 5 agents) when prioritizing.
