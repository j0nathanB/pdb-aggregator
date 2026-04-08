# Claude Code — Implementation Brief (Steps 6+)

## Context

You are building the pipeline logic for the Middle Powers Monitor (MPM). The infrastructure layer (steps 1-5: project scaffolding, schemas, ledger operations, initialization) was built in the prior handoff. This brief covers steps 6-23: the two-layer collection architecture, all agent implementations, extraction chain, orchestration, newsletter assembly, and testing.

Read these documents completely before starting:

1. **`mpm_unified_architecture_v4.1.md`** — The authoritative architecture specification. Everything flows from this.
2. **`extraction_architecture.md`** — Extraction routing table design, parallel pool dispatch, Publisher API scaffolding.
3. **`gov_source_agent_design.md`** — Integration notes for the two-layer collection model.

Agent prompts are in the `prompts/` directory:
- `country_agent_deep_dive_v4.1.md`
- `devils_advocate_v4.1.md`
- `triage_agent_v4.1.md`
- `gov_source_agent.md`
- `regional_synthesis.md`
- `executive_agent.md`

Supporting documents:
- `regional_frameworks.md` — Five regional analytical frameworks (input to regional synthesis agent)
- `newsletter_assembly_spec.md` — Deterministic rendering rules
- `information_culture_classifications.md` — Per-country information culture tags
- `REPORT.md` (media) — Extraction test results for 377 news domains
- `REPORT.md` (government) — Extraction test results for 163 government sources

---

## What to Build

### Step 6: Layer 2 — SearchAPI Government Source Discovery

Build the SearchAPI client for government domain queries.

**How it works:**
- Each country has a government domain config (`government/{code}.yaml`) listing institutional domains and query terms
- The pipeline runs SearchAPI queries scoped to government domains via `site:` operators (e.g., `site:sre.gob.mx comunicado`)
- Queries are filtered to the past week (`freshness` or date range parameter)
- Layer 2 runs for all 28 countries every week, unconditionally — it is not gated by triage
- Returned URLs are passed to the extraction chain (Step 9)

**Government domain config schema:**
```yaml
country: Mexico
code: mx
information_culture: managed

domains:
  - domain: gob.mx
    institutions: [Presidency, SEDENA, SEMAR, SRE, SE]
    priority: P1
  - domain: sre.gob.mx
    institutions: [Foreign Ministry]
    priority: P1
  - domain: banxico.org.mx
    institutions: [Central Bank]
    priority: P2
  - domain: senado.gob.mx
    institutions: [Senate]
    priority: P2
  - domain: diputados.gob.mx
    institutions: [Chamber of Deputies]
    priority: P2
  - domain: dof.gob.mx
    institutions: [Official Gazette]
    priority: P2

query_terms:
  - "comunicado"
  - "acuerdo bilateral"
  - "decreto"
  - "adquisición"
  - "presupuesto"
```

**Query construction:** For each country, generate `site:{domain} {term}` queries. P1 domains get more query term combinations than P2. Total queries per country: ~3-8 depending on domain count.

**Output:** List of discovered URLs with metadata (domain, institution inferred from domain, date, snippet) ready for extraction.

### Step 7: Government Source Agent

Implement the government source agent as an LLM call per country.

**Input:** Extracted government content (from Step 9) + source interpretive context (government section) + country dossier (reference) + information culture tag.

**Prompt:** `prompts/gov_source_agent.md`

**Output schema:** As defined in the prompt — findings (classified as ground_truth/intent_signal/both, tagged with signal categories), discovery_gaps, extraction_failures.

**Runs:** For all 28 countries, after extraction completes. Lightweight for countries with no government content discovered. Many countries will have 0-3 findings per week.

### Step 8: Layer 1 — Brave Search News Discovery

Build the Brave News API client with per-country Goggle support.

**How it works:**
- Each country has a Goggle file (`goggles/{code}.goggle`) that ranks domestic media sources
- Pipeline runs topic queries using actor/institution search terms + localized vocabulary from the CountryConfig
- Brave News API parameters: `country`, `search_lang`, `freshness=pw`, plus the Goggle
- Layer 1 depth is determined by triage: deep-dive countries get full queries, maintenance countries use only the triage wire/headline check results

**For triage (all 28 countries):**
- Wire scan: 1-2 queries per country against wire sources (Reuters, AP, France24)
- Domestic headline check: 1-2 queries per country with the country Goggle applied
- Returns headlines and snippets only — no full extraction needed at triage stage

**For deep dive (8-12 countries per week):**
- Full query set: actor names + localized vocabulary terms, 15-20 queries per country
- Returns ranked articles for extraction

**Output:** List of discovered URLs with Brave metadata (title, snippet, source, date, Goggle boost tier) ready for extraction.

### Step 9: Extraction Tier Chain

Build the tiered extraction pipeline that serves both Layer 1 and Layer 2.

**Routing table:** `extraction/routing.yaml` — maps domains to their empirically best extraction method. Populated from the two REPORT.md files (377 media domains + 163 government sources). One global routing table serving both layers.

**Methods (in order of default preference for unknown domains):**

| Tier | Method | Implementation |
|------|--------|---------------|
| 0 | Claude web_fetch | Anthropic API web_fetch tool call |
| 1 | curl + trafilatura | Python `httpx` GET + `trafilatura.extract()` |
| 2 | Diffbot | `/v3/article` endpoint, fallback to `/v3/analyze` |
| 3 | Playwright | Headless Chromium via `playwright` Python library + `trafilatura.extract()` on rendered HTML |
| 4 | Publisher API | Guardian Open Platform (scaffolded), FT (scaffolded) |

**Parallel pool dispatch:**
```python
# Dispatch URLs to pools based on routing table
# All pools run concurrently via asyncio.gather()
pool_claude = [url for url in urls if routing[domain(url)] == "claude"]
pool_curl = [url for url in urls if routing[domain(url)] == "curl"]
pool_diffbot = [url for url in urls if routing[domain(url)] == "diffbot"]
pool_playwright = [url for url in urls if routing[domain(url)] == "playwright"]
pool_api = [url for url in urls if routing[domain(url)] == "publisher_api"]
pool_skip = [url for url in urls if routing[domain(url)] == "unreachable"]
```

**Fallback batch:** After primary pools complete, collect failures and dispatch to fallback methods per the routing table. One fallback pass. Anything still failed → snippet-only with `extraction_failed: true` flag.

**Concurrency limits:**
- Claude web_fetch: 10 concurrent
- curl: 20 concurrent
- Diffbot: 5 concurrent (rate limited)
- Playwright: 3 concurrent (resource heavy)
- Publisher APIs: 5 concurrent

**Rate limiting:** Max 1 request/second per domain regardless of method.

**Output per URL:**
```python
{
    "url": "https://...",
    "domain": "eluniversal.com.mx",
    "title": "...",
    "text": "...",              # Full extracted text, or None
    "snippet": "...",           # Always present from search results
    "extraction_method": "curl",  # Which method succeeded
    "extraction_failed": false,   # True if all methods failed
    "source_layer": "layer1" | "layer2",
    "metadata": { ... }        # Search result metadata
}
```

**Key implementation detail from the government source report:** Australian `.gov.au` sites systematically block Python user-agents but respond to Diffbot. Indian `.gov.in` sites block curl but respond to web_fetch/Diffbot. Lithuanian `.lrv.lt` sites are unreachable by all methods. These patterns are baked into the routing table.

### Step 10: Triage Agent

**Input assembly:** For each of 28 countries, assemble a triage packet:
- Wire scan headlines (from Step 8 triage queries)
- Domestic headline check (from Step 8 triage queries)
- Government source findings (from Step 7)
- Country posture summary (from ledger)
- Global ledger context (global_posture_summary + active_dynamics with triage_implications)

**Prompt:** `prompts/triage_agent_v4.1.md`

**Implementation:** Single LLM call with all 28 country packets in context. Output is structured JSON with per-country depth decisions.

**Output drives:** Which countries proceed to full Layer 1 queries (deep dive) vs. which stay at maintenance.

### Step 11: Country Agent (Deep Dive)

**Input assembly per country:**
- Layer 1 news results (extracted articles from Step 9, for this country)
- Layer 2 government findings (from Step 7, for this country)
- Country dossier (full)
- Country ledger (full, or truncated if too large)
- Source interpretive context

**Prompt:** `prompts/country_agent_deep_dive_v4.1.md`

**Implementation:** One LLM call per deep-dive country. Parallelized across countries with semaphore for rate limiting.

**Output:** Weekly entry + updated signal categories + updated posture summary. Validated against Pydantic schema before ledger write.

### Step 12: Devil's Advocate

**Input:** The country agent's weekly entry (before ledger write).

**Prompt:** `prompts/devils_advocate_v4.1.md`

**Implementation:** One LLM call per deep-dive country, after the country agent completes. Output appended to the weekly entry's `devils_advocate` field.

### Step 13: Country Desk Orchestrator

This is the core pipeline orchestration. The sequence:

```
1. Layer 2: SearchAPI government queries (all 28 countries, parallel)
2. Extraction: Extract government URLs (routing table dispatch)
3. Gov Source Agent: Process government content (all 28 countries, parallel LLM calls)
4. Layer 1 Triage: Brave wire scan + domestic headlines (all 28 countries)
5. Triage Agent: Depth decisions (single LLM call)
6. Layer 1 Deep Dive: Brave full queries for flagged countries
7. Extraction: Extract news URLs (routing table dispatch)
8. Country Agents: Analysis calls (parallel, deep-dive countries only)
9. Devil's Advocate: Adversarial review (parallel, deep-dive countries only)
10. Ledger Write: Merge agent output + devil's advocate, validate, write
11. Maintenance Write: Log triage findings for maintenance countries
```

Steps 1-3 run before triage. Steps 4-5 determine depth. Steps 6-11 run depth-dependent. Failed steps are handled per the architecture doc's failure handling rules (quarantine country, proceed with remaining, etc.).

### Step 14: Regional Synthesis

**Input per region:** Country analyses for constituent countries (from Step 13) + regional framework document.

**Prompt:** `prompts/regional_synthesis.md`

**Framework documents:** `frameworks/regional_frameworks.md` — split into five separate inputs, one per region.

**Implementation:** 5 parallel LLM calls, one per region. Can run as soon as all constituent country agents in that region have completed.

**Stateless:** No regional ledger. Fresh analysis each week.

### Step 15: Executive Agent

**Input:** 5 regional reports + global ledger (prior state).

**Prompt:** `prompts/executive_agent.md`

**Implementation:** Single LLM call, sequential (runs after all regional syntheses complete).

**Output:** Updated global ledger (including executive briefing items, dynamic management, watchlist, triage implications for next week).

### Step 16: Newsletter Assembly

**Input:** All structured outputs from the pipeline.

**Spec:** `newsletter_assembly_spec.md`

**Implementation:** Pure Python, no LLM calls. Deterministic rendering from structured JSON to Markdown. Follow the spec exactly for section ordering, formatting, length targets, and edge cases.

### Step 17: CLI Interface

```bash
# Full pipeline
python -m src.main --all

# Single country desk (no regional/executive)
python -m src.main --country mx

# Single region (runs constituent desks + regional synthesis)
python -m src.main --region americas

# Triage only (show depth decisions without running desks)
python -m src.main --triage-only

# Skip to regional (reuse existing desk reports)
python -m src.main --regional-only

# Skip to executive (reuse existing regional reports)
python -m src.main --executive-only

# Assemble newsletter from existing outputs
python -m src.main --assemble

# Dry run (show what would execute)
python -m src.main --all --dry-run

# Specific date
python -m src.main --all --date 2026-03-21

# Compress old ledger entries
python -m src.main --compress --country mx
python -m src.main --compress --all
```

### Step 18: Error Handling

Implement retry logic, quarantine, and graceful degradation per the architecture doc Section 15. Key rules:
- Layer 2 failure → proceed with Layer 1 only
- Layer 1 failure → proceed with Layer 2 only, lower confidence
- Triage failure for a country → default to maintenance
- Country agent failure → quarantine country, proceed with remaining for regional synthesis
- Regional synthesis failure → executive works from available reports
- Executive failure → newsletter assembles without executive brief
- Devil's advocate failure → weekly entry written without adversarial section
- All agent calls: max 2 retries with schema validation between attempts

### Step 19: Consolidation

Implement ledger compression per architecture doc Section 14:
- Country ledgers: compress entries older than 8 weeks into `consolidated_history`
- Global ledger: same 8-week retention
- Archive originals before compression
- Trigger automatically when entry count exceeds retention window

### Step 20: End-to-End Test with Mexico

Run 2 consecutive simulated weekly cycles covering:
- Both collection layers (SearchAPI + Brave)
- Full extraction chain
- Government source agent → triage → country agent → devil's advocate
- Regional synthesis (Americas, with Mexico as sole deep-dive country)
- Executive synthesis
- Newsletter assembly
- Ledger state carries correctly from week 1 to week 2
- Global ledger triage implications from week 1 influence week 2's triage

This is the validation gate. Do not proceed to multi-country until Mexico passes.

### Steps 21-23: Scale to 28 Countries

After Mexico validates:
21. Run source curation prompts for remaining 27 countries (Goggle files + government domain configs)
22. Populate CountryConfigs for all countries (actor extraction + config assembly)
23. Full 28-country integration test

---

## Project Structure (Steps 6+)

```
src/
├── collection/
│   ├── __init__.py
│   ├── brave.py            # Brave News API client + Goggle loading
│   ├── searchapi.py         # SearchAPI client for government queries
│   └── query.py             # Query construction (actor terms, vocabulary, site-scoping)
├── extraction/
│   ├── __init__.py
│   ├── router.py            # Routing table loader + pool dispatch
│   ├── curl_extractor.py    # httpx + trafilatura
│   ├── diffbot_extractor.py # Diffbot Article API
│   ├── playwright_extractor.py # Headless Chromium + trafilatura
│   ├── webfetch_extractor.py   # Claude web_fetch
│   ├── publisher_apis/
│   │   ├── __init__.py
│   │   ├── base.py          # PublisherAPI abstract base
│   │   ├── guardian.py      # Guardian Open Platform (stub)
│   │   └── ft.py            # FT Content API (stub)
│   └── orchestrator.py      # Parallel pool dispatch + fallback
├── agents/
│   ├── __init__.py
│   ├── gov_source.py        # Government source agent
│   ├── triage.py            # Triage agent
│   ├── country.py           # Country agent (deep dive)
│   ├── devils_advocate.py   # Devil's advocate
│   ├── regional.py          # Regional synthesis
│   └── executive.py         # Executive agent
├── pipeline/
│   ├── __init__.py
│   ├── orchestrator.py      # Full pipeline orchestration (Steps 1-11 above)
│   ├── country_desk.py      # Per-country desk workflow
│   └── maintenance.py       # Maintenance country processing
├── assembly/
│   ├── __init__.py
│   └── newsletter.py        # Deterministic Markdown rendering
├── main.py                  # CLI entry point
└── ...                      # (existing from steps 1-5: schemas/, ledger/, config.py, etc.)
```

---

## Technical Decisions

- **All agent calls use `claude-sonnet-4-20250514`** unless analytical quality proves insufficient for executive synthesis, in which case that single call upgrades to Opus
- **Structured output via Pydantic validation:** Every agent call's output is parsed and validated against the Pydantic schema before use. On validation failure, retry with error message appended to prompt (max 2 retries)
- **Async throughout:** All collection, extraction, and agent calls use `async`/`await` with `asyncio.gather()` for parallelism and `asyncio.Semaphore()` for rate limiting
- **Extraction routing table** (`extraction/routing.yaml`) is a static YAML file loaded at startup. It merges data from both REPORT.md files (media + government sources) into one table
- **Agent prompts are loaded from files**, not hardcoded in Python. Template variables ({{COUNTRY}}, {{ANALYSIS_DATE}}, etc.) are substituted at call time
- **All pipeline outputs are JSON files** written to `output/` subdirectories, timestamped by analysis date
- **Logging:** Structured logging (JSON format) for all collection, extraction, agent, and orchestration steps. Include timing, token counts, and success/failure status

---

## What NOT to Build

- No web UI or dashboard
- No real-time monitoring (this is a weekly batch pipeline)
- No database (JSON files for persistence)
- No authentication or multi-user support
- No automated deployment (manual run or cron for now)
- No CountryConfigs beyond Mexico (other countries populated in Step 22)
- No source curation automation (Goggle files and government configs are generated via Research mode prompts, not by this pipeline)

---

## Reference

The architecture doc (`mpm_unified_architecture_v4.1.md`) is the authoritative source. If anything in this brief conflicts with the architecture doc, the architecture doc wins.

The existing infrastructure from steps 1-5 (schemas, ledger operations, config loading, initialization) should be used as-is. Build on top of it, don't restructure it.

The two REPORT.md files contain the empirical extraction test data that should be converted into the routing table. Every domain in those files should have an entry in `extraction/routing.yaml`.
