# Architecture v4.1 — Revision: Story Map Agent + Single-Pass Search

## Date: 2026-03-23

## What Changed

Testing revealed that the country agent's analysis lacked breadth — it went deep on what it found but missed the overall shape of the week's media coverage. This revision adds a **Story Map Agent** between search and extraction that clusters raw search results into distinct stories, and restructures the deep-dive search into a **single pass** rather than duplicating triage and deep-dive queries.

---

## Revised Pipeline Flow

```
STEP 0: GOVERNMENT SOURCE DISCOVERY — Layer 2 (all 28 countries)
  SearchAPI queries scoped to government domains
  → extraction → Government Source Agent
  Output: classified government findings per country

STEP 1: TRIAGE (all 28 countries)
  Inputs per country:
    - Wire sweep: 1 broad Brave query, no Goggles, filtered to
      WIRE_DOMAINS (~20 results) — already implemented
    - Domestic sweep: 1 primary actor Brave query with Goggle
      + country params (~50 results) — already implemented
    - Government source findings (from Step 0)
    - Country posture summary from ledger
    - Global ledger context + triage implications
  Output: per-country depth decision (deep dive / maintenance)
  
  Triage search results are PRESERVED for deep-dive countries
  and flow into the story map alongside deep-dive expansion results.

STEP 1: TRIAGE (all 28 countries)
  Per country, two Brave queries (already implemented):
    - Wire sweep: broad query, no Goggles, filtered to WIRE_DOMAINS (~20 results)
    - Domestic sweep: primary actor query, with Goggle + country params (~50 results)
  Plus: government source findings (from Step 0)
        + country posture summary + global ledger context
  Output: per-country depth decision (deep dive / maintenance)

  CRITICAL: Triage search results are preserved, not discarded.
  For deep-dive countries, they flow forward into the story map.
  For maintenance countries, they are logged directly to the ledger.

STEP 2: DEEP-DIVE SEARCH EXPANSION (deep-dive countries only)
  Triage already found ~70 results per country (wire + domestic).
  The expansion adds targeted queries to fill gaps:
    - Actor queries: one per tracked actor/institution not already
      covered by triage's primary actor query (~5-7 queries)
    - Signal-category queries: one per vocabulary group (~5 queries)
    - Guardian API query (where applicable)
  Output: 150-250 additional results merged with triage results
  Total per country entering story map: ~220-320 results

STEP 3: STORY MAP AGENT (deep-dive countries only, NEW)
  Input: all raw search results for this country + actor list
  Task: cluster results into distinct stories, summarize each,
    record source count and source list per story, identify
    representative URLs for extraction
  Output: 15-30 story clusters with metadata
    + single-source items (not clustered, listed separately)
    + noise summary (off-topic results filtered)

STEP 4: SELECTIVE EXTRACTION (deep-dive countries only)
  Input: representative URLs from story map
    (top 1-2 per cluster + single-source items)
  Method: routing table dispatch (curl → Diffbot → Playwright → etc.)
  Guardian API results arrive pre-extracted (bypass extraction)
  Output: ~30-50 extracted articles

STEP 5: COUNTRY AGENT (deep-dive countries only)
  Input: story map (full media landscape with source counts)
    + extracted articles (depth for key stories)
    + Layer 2 government findings (primary evidence)
    + country dossier + country ledger
  Task: five-category posture assessment working from
    the story map as the primary organizing structure
  Output: weekly entry + updated signal categories + posture summary

STEP 6: DEVIL'S ADVOCATE (deep-dive countries only)
  Input: country agent weekly entry
  Output: adversarial review appended to weekly entry

STEP 7: LEDGER WRITE
  Deep-dive countries: full weekly entry with story map reference
  Maintenance countries: gov findings + wire headlines logged,
    posture summary lightly updated

STEP 8: REGIONAL SYNTHESIS (5 regions, stateless, parallel)
  (unchanged)

STEP 9: EXECUTIVE AGENT (sequential)
  (unchanged)

STEP 10: NEWSLETTER ASSEMBLY (deterministic)
  (unchanged)
```

---

## New Agent: Story Map Agent

**Role:** News desk editor that organizes raw search results into distinct stories. No analytical judgment — describes what the media covered, not what matters.

**Input:** Raw Brave search results (headlines + snippets, 250-500 items) + actor list from CountryConfig.

**Output:** 15-30 story clusters, each with:
- Synthesized headline and 1-2 sentence summary
- Actors involved
- Source count and source list (which outlets covered this story)
- Date range
- Representative URLs for extraction (best 1-2 articles)
- Signal category hint

Plus: single-source items (listed but not clustered), noise summary (off-topic results filtered with count).

**What it replaces:** The old pipeline's HDBSCAN clustering + summarizer agent. The LLM does both clustering and summarization in one pass, without embeddings or ML infrastructure.

**Analytical value:** The story map preserves **coverage distribution** as a signal. The country agent sees not just what happened but how much attention each story received. A story covered by 8 outlets vs. one covered by 1 outlet tells the agent something about the domestic information environment — even before assessing analytical significance.

**Prompt:** `prompts/story_map_agent.md`

---

## Revised Agent Inputs

### Country Agent — Input Changes

The country agent's Layer 1 input changes from "extracted articles" to "story map + extracted articles":

**Old (v4.1):**
- Layer 1 results: ranked extracted articles from Brave
- Layer 2 findings: government source agent output
- Dossier + ledger

**New (v4.1 revised):**
- Story map: full media landscape (15-30 story clusters with source counts, summaries, signal category hints)
- Extracted articles: full text for representative articles from each story cluster
- Layer 2 findings: government source agent output (unchanged)
- Dossier + ledger (unchanged)

The country agent reads the story map first to understand the shape of the week, then reads extracted articles for depth on specific stories. This gives it both breadth (what was covered) and depth (what the articles actually say).

**New analytical capability:** After completing the five-category assessment, the country agent reviews the story map for high-prominence stories (5+ sources) that it didn't flag as significant. If the media is heavily covering something the agent assessed as not posture-relevant, the agent notes this in its activity level rationale — the coverage distribution itself is a domestic_regime signal.

### Triage Agent — Input Changes

Triage runs two Brave searches per country (wire sweep + domestic sweep) rather than a single wire check. This matches what Claude Code already implemented.

**Current (implemented):**
- Wire sweep: broad Brave query, no Goggles, filtered to WIRE_DOMAINS (~20 results)
- Domestic sweep: primary actor query with Goggle + country params (~50 results)
- Government source findings (Layer 2)
- Country posture summaries
- Global ledger context

**Key change from v4.1:** Triage search results are no longer discarded after the depth decision. For deep-dive countries, the wire + domestic results flow forward into the story map agent alongside deep-dive expansion results. For maintenance countries, triage results are logged directly to the ledger.

The triage agent prompt (v4.2) should be updated to restore the domestic sweep in its input description, reflecting what was actually built.

---

## Cost Impact

**Triage queries:** 2 per country × 28 countries = 56 Brave queries (already implemented, unchanged).

**Deep-dive expansion queries:** ~10-12 per deep-dive country × 10 avg = ~100-120 additional Brave queries per week. These are the targeted actor/vocabulary queries that go beyond triage's single primary-actor sweep.

**New LLM call:** Story map agent, 1 call per deep-dive country per week (~10 calls). Lightweight — processes headlines/snippets only, no full articles in context. Estimated ~$0.02-0.05 per call.

**Extraction budget:** More targeted. Extraction runs only on representative URLs from story clusters (~30-50 per country) rather than on all search results. Net extraction cost is similar or lower than extracting everything.

**Net cost change:** Small increase from expansion queries. Offset by more targeted extraction.

---

## Implementation Order Change

In the steps 6+ handoff, the implementation order for Steps 8-12 changes:

**Old:**
```
8.  Layer 1 integration (Brave client)
9.  Extraction tier chain
10. Triage agent
11. Country agent
12. Devil's advocate
```

**New:**
```
8.  Layer 1 integration (Brave client)
9.  Extraction tier chain
10. Triage agent (revised — wire check only, no domestic queries)
11. Story map agent (NEW)
12. Country agent (revised — story map as input)
13. Devil's advocate
```

---

## Documents Affected

| Document | Change needed |
|----------|--------------|
| `mpm_unified_architecture_v4.1.md` | Pipeline flow, triage-to-deep-dive handoff, new story map step |
| `prompts/triage_agent_v4.2.md` | Restore domestic sweep in input description (was removed in v4.2 but implementation kept it) |
| `prompts/country_agent_deep_dive_v4.2.md` | Already updated — story map as input |
| `prompts/story_map_agent.md` | Already written, no changes needed |
| `claude_code_handoff_steps_6_plus.md` | Add story map agent step, triage result forwarding, deep-dive expansion |
| `extraction_architecture.md` | Note that extraction is driven by story map representative URLs |
| `newsletter_assembly_spec.md` | No change — assembly reads from country agent output, not the story map |
| `src/monitor/agents/triage.py` | Already implemented — needs data forwarding (return search results alongside depth decisions) |
| `src/monitor/orchestrator.py` | Needs triage → story map pipeline connection |
