# Cache Verification — 2026-05-04 Run Results

First production data with `cache_creation_input_tokens` /
`cache_read_input_tokens` captured by Phase 1 instrumentation. Three findings,
one of them a real bug we shipped.

## Predicted vs actual hit rates

| agent | predicted | actual hit rate | mean cache_read | verdict |
|---|---|---:|---:|---|
| style_editor | ~10K prefix, hit on calls 2-37 | **83.4%** | 9,156 | ✅ matched |
| editor | ~10-12K prefix, hit on calls 2-30 | **47.2%** | 10,997 | ✅ matched |
| regional_writer | ~10K prefix, hit on calls 2-6 | **45.2%** | 6,460 | ✅ matched (slightly under) |
| copyeditor | ~10K prefix, hit on calls 2-38 | **0%** | 0 | ❌ shipped a decorative cache |
| country | 0% (per-country cluster) | 11.8% mean | 11,851 | ⚠️ retry-driven outlier |

## The copyeditor bug

`cache_create=10,682` mean per call (cache writes happening), `cache_read=0`
across all 38 calls (no reads). Each copyeditor system prompt has a
country-specific `<leader_reference>` block appended at the end via
`structured_copyeditor.py:_build_leader_reference()` — different leader names
per country. Since `cache_control` hashes the full system block bytes, every
country gets a unique cache key. 38 cache writes, zero reads — same
"decorative cache" pattern we caught for country.py and government.

**Root cause was visible in the leverage_split data we already had.** The
within-cluster LCP analysis pooled copyeditor calls into one cluster
(`first 200 chars` matched), and reported `system_lcp=10,621`. But that
LCP is the SHARED prefix at the front; the cluster's calls also have a
divergent tail (the per-country leader_reference), and `cache_control` on
the whole block requires byte-for-byte match of the entire cached block,
not just the prefix.

The leverage_split.py gate (`savings/run > 0`) marked copyeditor ✅
because the within-cluster math says "n=38, prefix=10K, savings = 38 × 10K".
That math implicitly assumed the WHOLE prefix was identical across all 38.
It wasn't. The gate is a necessary but not sufficient check.

**Why Option B replay didn't catch it.** I ran the same trace's prompt
twice back-to-back. The bytes were identical, so the cache fired (as
reported: cache_create=10,397 on call 1, cache_read=10,397 on call 2). But
production sends 38 DIFFERENT countries' prompts; the same-input replay
hides the cross-input variance entirely.

**Fix shipped in this commit.** Two-block system: stable prefix (base +
style_guide) wrapped in a cached block, per-country leader_reference in a
second uncached block. The cache key for block 1 is identical across
countries. Predicted hit rate for next run: ~30-40% (similar to editor —
with 38 calls × ~10K prefix, savings ~370K tokens/run that we left on
the floor in Phase 3a).

## The country.py retry finding (changes Phase 3b decision)

Country.py's mean `cache_read=11,851` looked surprising — we'd predicted 0%.
Per-call breakdown: `fi` shows `cache_read=355,521` (one country only). All
29 other countries show 0. This is `fi` being retried multiple times within
the 5-min TTL after an initial failure — the cached prefix from call 1 was
read on each retry.

This is the "make recovery cheaper" case the user predicted earlier. Steady-
state cross-country reuse is still 0% as analyzed, but **retries do benefit**.

**Phase 3b plan was to delete country.py's `cache_control` as decorative.**
That call gets reversed: keeping the `cache_control` provides real retry
savings (fi alone saved ~355K tokens that would have been re-paid at full
input price without it). The 1.25× write premium on the steady-state 30
country writes is small (~29K wasted/run, ~58K/2wk) versus the retry savings.

Updated `country.py` comment in this commit explains the trade-off and
references Phase 4.5 for the structural fix (template restructure to enable
cross-country reuse).

## Lessons for the verification protocol

1. **Within-cluster LCP overstates cacheability when the cluster has a
   divergent tail.** LCP measures shared prefix; `cache_control` on the
   whole block needs full byte equality. If `mean_system_tokens > LCP +
   small_variable`, the block has a tail that breaks cross-call cache
   reuse. The leverage_split.py gate should add a check: flag when
   `cluster_mean_system - cluster_LCP > 500 tokens` (or similar) as a
   "tail-breaks-cache" warning even when `savings/run > 0`.

2. **Option B replay needs cross-input testing, not same-input.** Today's
   `option_b_replay.py` does 2 back-to-back calls with identical bytes;
   that only proves the API accepts the format. To catch
   "different-input → no cache hit" bugs, the replay should pull 2
   DIFFERENT traces per code path (e.g. `copyeditor_mx.json` then
   `copyeditor_au.json`) and verify cache_read > 0 on the second.

   This bug would have been visible in a 30-minute test before the PR
   merged. Worth fixing the script before the next caching change ships.

3. **Don't trust within-call mean as a proxy for cross-call behavior.**
   Country.py's 11.8% mean hit rate looked positive in aggregate but came
   entirely from one country's retries. Per-call distribution check is
   necessary; mean alone hides this.

## Updated leverage projections

After the copyeditor fix:

| agent | savings/run (prior estimate) | savings/run (revised) |
|---|---:|---:|
| editor | 368K | 368K (unchanged — was already correct) |
| copyeditor | 393K (predicted) → 0 (actual Phase 3a) → ~370K (post-fix) | ~370K |
| style_editor | 372K | 372K |
| regional_writer | 50K | 50K |
| **total/run** | **~1.18M** | **~1.16M** |

So we recover ~370K tokens/run that Phase 3a left on the floor. Total
editor-cluster steady-state savings now match the original prediction
once the fix lands and a Sunday run validates the actual hit rate.
