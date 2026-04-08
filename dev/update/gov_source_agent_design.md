# Government Source Agent — Design and Integration

## Architectural Impact

The introduction of Brave Search + Goggles (Layer 1) and a government monitoring layer (Layer 2) changes the pipeline's collection architecture. These notes document what changes from the v4 architecture, what stays the same, and the design of the new government source agent.

---

## Revised Collection Architecture

### Before (v4 Architecture)

The country agent performed both collection and analysis in a single call:
- Received: dossier + ledger + CountryConfig
- Used web_search/web_fetch to discover and extract articles
- Analyzed findings across five signal categories
- Produced the weekly entry

### After (v4.1 — Two-Layer Collection)

Collection is separated from analysis. Two parallel collection layers feed the country agent:

```
LAYER 1: NEWS DISCOVERY (Brave Search News API)
  Input: Actor/institution query terms + per-country Goggle
  Method: Brave News API with country, search_lang, freshness=pw
  Output: Ranked news articles (headlines, snippets, URLs)
  Extraction: Tiered chain (curl → web_fetch → Diffbot → Playwright → API)
  Runs: Weekly, per country (triage decides depth)

LAYER 2: GOVERNMENT SOURCE DISCOVERY (SearchAPI + Google)
  Input: Per-country government domain config
  Method: SearchAPI with site:-scoped queries against government domains
  Output: Government publications (statements, treaties,
          procurement notices, legislative records)
  Extraction: Same tiered chain as Layer 1
  Runs: Weekly, all 28 countries (no triage gating)

         ┌──────────────┐    ┌──────────────┐
         │   Layer 1    │    │   Layer 2    │
         │ Brave Search │    │  SearchAPI   │
         │  + Goggles   │    │  + Google    │
         └──────┬───────┘    └──────┬───────┘
                │                    │
                ▼                    ▼
         ┌──────────────┐    ┌──────────────┐
         │  Extraction  │    │  Extraction  │
         │  (shared     │    │  (shared     │
         │   chain)     │    │   chain)     │
         └──────┬───────┘    └──────┬───────┘
                │                    │
                │                    ▼
                │           ┌──────────────┐
                │           │  Gov Source   │
                │           │    Agent      │
                │           │ (processing)  │
                │           └──────┬───────┘
                │                  │
                ▼                  ▼
         ┌─────────────────────────────┐
         │       Country Agent         │
         │  (analysis, not collection) │
         └─────────────────────────────┘
```

### What This Changes

**Country agent no longer runs searches.** It receives pre-collected material from both layers and focuses entirely on analysis. This is a significant simplification of the country agent prompt — it no longer needs web_search/web_fetch tool instructions or search strategy guidance. It reads and assesses.

**Government monitoring runs for all 28 countries every week, regardless of triage.** Government sources publish on their own schedule. A foreign ministry press release about a treaty ratification doesn't wait for triage to decide the country is interesting. Layer 2 runs unconditionally, and its findings feed into triage (a significant government action appearing in Layer 2 output is itself a triage signal).

**Triage inputs expand.** Triage now reads three things per country: wire scan headlines (from Layer 1), domestic headline check (from Layer 1), and government source findings (from Layer 2). A country that looks quiet on wires but has a defense ministry procurement announcement in Layer 2 should be flagged for deep dive.

**CountryConfig expands.** Each country now carries:
- Actors and search terms (unchanged)
- A Goggle file (replaces the simple source whitelist)
- A government domain config (new — simplified from the Government Sources prompt output, listing institutional domains and query terms for SearchAPI)
- Known blind spots (unchanged)
- Localized query vocabulary (new — from the source curation prompt v2)

---

## Government Source Agent

### Role

The government source agent sits between Layer 2's discovery/extraction and the country agent. It processes official government content discovered via SearchAPI and produces a structured summary that the country agent can consume alongside Layer 1's news results.

This agent exists because government content is structurally different from news content:
- It requires classification as ground truth vs. intent signal
- It requires cross-referencing with the dossier's structural claims
- It often arrives as dense institutional text (procurement notices, treaty language, committee reports) that needs to be distilled to its analytical essentials
- The *framing* and *timing* of publication are themselves analytically significant

A country agent reading raw government content alongside news articles would struggle with these distinctions. The government source agent pre-processes government content so the country agent receives it in a consistent, analytically tagged format.

### What It Does

For each country, each week:

1. **Ingests Layer 2 output.** All content discovered via SearchAPI queries scoped to government domains and extracted through the tiered extraction chain — press releases, procurement notices, treaties, committee reports, central bank communications, etc.

2. **Classifies each item.** Is this:
   - **Ground truth** — establishes a fact (treaty signed, contract awarded, legislation enacted, forces deployed)
   - **Intent signal** — reveals government positioning or framing (press release emphasizing "strategic partnership," defense white paper language, budget allocation priorities)
   - **Both** — a factual announcement whose framing is also analytically significant

3. **Tags with signal category.** Which of the five categories does this item most directly touch? Some items touch multiple categories (a defense procurement that also involves a bilateral partnership is both security_defense and alignment_diplomatic).

4. **Extracts analytical essentials.** For each item, produces:
   - What happened (1-2 sentences, factual)
   - Why it matters structurally (1 sentence, referencing dossier sections where relevant)
   - What the framing reveals (1 sentence, for intent signals — what did the government choose to emphasize or omit?)
   - Source institution and publication date
   - Cross-reference note: which media sources from Layer 1 are likely to cover this, and what additional context they'd provide

5. **Produces a structured summary** that the country agent receives as input.

### What It Does NOT Do

- It does not assess posture change. That's the country agent's job.
- It does not search for additional context. It works only from Layer 2 content.
- It does not compare to the ledger. It processes content as it arrives, without analytical memory.
- It does not run for a subset of countries. It processes whatever Layer 2 fetched, for all countries.

### Output Schema

```json
{
  "country": "mx",
  "processing_date": "2026-03-14",
  "items_processed": 7,
  "items_with_findings": 3,

  "findings": [
    {
      "source_institution": "SRE (Foreign Ministry)",
      "source_url": "https://sre.gob.mx/...",
      "publication_date": "2026-03-12",
      "content_type": "ground_truth",
      "signal_categories": ["alignment_diplomatic"],

      "what_happened": "SRE published the text of a revised bilateral security cooperation framework with Canada, signed during de la Fuente's Ottawa visit.",
      "structural_significance": "Per §14, bilateral security frameworks have historically been the mechanism through which Mexico manages US expectations about security cooperation scope. A Canada-specific framework may signal diversification of security partnerships beyond the US bilateral.",
      "framing_note": "The press release frames this as 'deepening hemispheric security architecture' — language that positions the agreement as multilateral in spirit, not a bilateral hedge against the US.",
      "cross_reference": "Check Layer 1 results from Reforma and El Universal for domestic media framing of the same agreement. Media may frame it differently than SRE's official language."
    },
    {
      "source_institution": "SEDENA (Defense Ministry)",
      "source_url": "https://www.gob.mx/sedena/...",
      "publication_date": "2026-03-14",
      "content_type": "both",
      "signal_categories": ["security_defense"],

      "what_happened": "SEDENA announced procurement of 12 Black Hawk helicopters from Lockheed Martin for counter-narcotics operations.",
      "structural_significance": "US-origin defense procurement reinforces the operational cooperation track of the dual-track US relationship per §12. The counter-narcotics framing limits the sovereignty implications — this is security cooperation, not military alignment.",
      "framing_note": "Friday afternoon publication with no press conference. Minimized visibility suggests the government prefers this not to become a domestic debate about military dependency on the US.",
      "cross_reference": "Check whether any Layer 1 source picked this up. If not, this is a Layer 2-only finding — the pipeline would have missed it without government monitoring."
    }
  ],

  "no_new_content": [
    {
      "source_institution": "Banxico (Central Bank)",
      "expected_frequency": "event_driven",
      "assessment": "No new policy communications. Normal — Banxico's next scheduled decision is March 27."
    },
    {
      "source_institution": "Senate Foreign Affairs Committee",
      "expected_frequency": "periodic",
      "assessment": "No new committee reports. Normal — session is in recess until March 20."
    }
  ],

  "fetch_failures": [
    {
      "source_institution": "Official Gazette (DOF)",
      "error": "Playwright timeout — page failed to render within 30 seconds",
      "priority": "P2",
      "recommendation": "Retry next cycle. If persistent, check for site restructuring."
    }
  ]
}
```

### Integration Points

**Feeds triage:** The government source agent's findings are included in the triage input packet. A country with significant government findings (ground truth items, especially in alignment_diplomatic or security_defense) should influence the triage decision toward deep dive, even if wire coverage is quiet.

**Feeds country agent:** The country agent receives the government source agent's structured findings alongside Layer 1 news results. The country agent treats government findings as pre-processed primary source material — it doesn't need to re-extract or re-classify them, but it does need to integrate them into its five-category assessment.

**Feeds devil's advocate:** The devil's advocate can check whether the country agent appropriately distinguished between government framing (intent signal) and independently verified fact (ground truth). If the country agent treats a government intent signal as established fact, that's a challenge.

---

## Impact on Existing Prompts

### Country Agent (Deep Dive)

The country agent prompt needs revision. Key changes:

**Remove:** All search instructions (Phase 2: Collect). The country agent no longer runs web_search or web_fetch. It receives pre-collected material.

**Add:** A new input block description for the two collection layers:

> **LAYER 1 RESULTS** — News articles discovered through Brave Search with your country's Goggle applied. These are ranked by source tier (Tier 1 sources surface first). You receive headlines, snippets, and full article text where extraction succeeded. Treat these as media reporting — independent coverage with editorial perspective.
>
> **LAYER 2 RESULTS** — Government source findings from the government monitoring agent. These are pre-classified as ground truth (establishes a fact) or intent signal (reveals positioning). Each finding includes structural significance notes and cross-reference suggestions. Treat these as primary source material — what the government actually said or did, with framing analysis included.
>
> When Layer 1 and Layer 2 cover the same event, use Layer 2 for what happened and Layer 1 for how it was received, contested, or contextualized domestically.

**Revise Phase 2** from "Collect" to "Read and Integrate" — the agent reads pre-collected material rather than conducting searches.

**Revise source discipline section** to address how to handle the two layers' different evidentiary weight.

### Triage Agent

Add Layer 2 findings to the triage input packet:

> **Government source findings:** For each country, a summary of new government content discovered through direct monitoring. Items classified as ground truth (new facts) or intent signals (new framing). May be empty for countries where government sources published nothing new this week.

Add a triage trigger:

> **Government source activity:** A significant ground truth finding from Layer 2 (treaty signed, procurement announced, forces deployed) warrants deep dive even if wire coverage hasn't picked it up yet — the pipeline may be ahead of media coverage.

### Devil's Advocate

Add a check:

> **Government framing vs. independent verification.** Did the country agent treat government intent signals as established facts? If an assessment rests primarily on government source content without independent media corroboration, it should carry lower confidence — government sources tell you what the government wants known, not necessarily what happened.

### CountryConfig

The simple source whitelist is replaced by:

```yaml
sources:
  goggle_file: goggles/mx.goggle    # Brave Goggles file
  government_manifest: manifests/mx_gov.yaml  # Layer 2 monitoring config
  wire:
    - reuters.com
    - apnews.com
    - france24.com
  query_vocabulary:                   # from source curation prompt v2
    diplomatic_alignment: [...]
    security_defense: [...]
    economic_tech: [...]
    institutional: [...]
    domestic_constraints: [...]
```

---

## Layer 2 Runs Independently of Triage

This is an important architectural point. Layer 1 (Brave news search) is triage-gated for depth — deep-dive countries get full queries, maintenance countries get headline checks only. Layer 2 (government monitoring) runs for all 28 countries every week regardless of triage.

Why: government sources publish on their own schedule. A foreign ministry treaty announcement doesn't wait for the pipeline to decide the country is interesting. Running SearchAPI queries against government domains for 28 countries is cheap (28 × 2-5 queries, minimal API cost) and the government source agent processing is lightweight for countries with no new content.

This means Layer 2 can surface findings that *cause* a country to get flagged at triage. The flow becomes:

```
Layer 2 runs (all 28 countries)
  → Government source agent processes findings
    → Findings fed to triage alongside wire scan
      → Triage decides depth (informed by gov findings)
        → Layer 1 runs (depth varies by triage decision)
          → Country agent receives both layers' output
```

Layer 2 runs *before* triage. Layer 1's depth is *determined by* triage. This is a sequencing change from the v4 architecture where everything happened after triage.

---

## What Still Needs to Happen

1. **Revise the country agent prompt** to remove search instructions and add two-layer input handling
2. **Revise the triage agent prompt** to include Layer 2 findings as input
3. **Revise the devil's advocate prompt** to add government framing check
4. **Update the architecture doc (v4 → v4.1)** to reflect two-layer collection
5. **Run source curation prompt v2** for all 28 countries to generate Goggle files
6. **Run government sources prompt** for all 28 countries to generate government domain configs
7. **Build Layer 2 integration:** SearchAPI client with site-scoped government domain queries
8. **Build the government source agent:** prompt + orchestration
9. **Update CountryConfig schema** to carry Goggle file path, government domain config path, and query vocabulary
