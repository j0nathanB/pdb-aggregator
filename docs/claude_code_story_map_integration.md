# Claude Code — Story Map Integration

## Context

The triage phase is implemented and working — `src/monitor/agents/triage.py` runs two Brave searches per country (wire sweep + domestic sweep), then Phase 2 makes depth decisions via LLM call. Tests pass.

The problem: triage search results are currently discarded after the depth decision. The country agent runs its own searches independently, which duplicates work and sometimes drops stories that triage found.

This task connects the existing triage implementation to a new story map pipeline that ensures nothing gets lost between triage and analysis.

## What to Build

### 1. Triage Result Forwarding

Modify `scan_country()` in `src/monitor/agents/triage.py` to return the raw search results alongside the scan summary. Currently it returns only what Phase 2 needs for the depth decision. It should also return the full Brave result objects (headlines, snippets, URLs, source domains, dates) for both wire and domestic sweeps.

The orchestrator stores these results per country. For deep-dive countries, they flow into the story map. For maintenance countries, they get logged to the ledger as this week's headlines.

### 2. Deep-Dive Search Expansion

New module: `src/monitor/agents/search_expansion.py`

For each deep-dive country, run additional Brave queries that go beyond triage's single primary-actor domestic sweep:

```python
async def expand_search(
    country_config: CountryConfig,
    brave_client: BraveClient,
    triage_results: list[dict],  # Results already collected
) -> list[dict]:
    """
    Run targeted queries for actors and signal categories
    not covered by triage's primary actor query.
    
    Returns additional results to merge with triage results.
    """
    additional_results = []
    
    # Actor expansion: query for actors beyond the primary
    # (triage only searched the primary actor)
    for actor in country_config.actors:
        if actor.primary:
            continue  # Already covered by triage
        for term in actor.search_terms[:1]:  # Top search term per actor
            results = await brave_client.search_news(
                query=f'"{term}"',
                country_code=country_config.news_discovery.brave_params.country,
                search_lang=country_config.news_discovery.brave_params.search_lang,
                goggles_id=country_config.news_discovery.goggle_url,
                count=20,
            )
            additional_results.extend(results)
    
    # Signal-category vocabulary expansion
    vocab = country_config.news_discovery.query_vocabulary
    for category_terms in [
        vocab.diplomatic_alignment,
        vocab.security_defense,
        vocab.economic_tech,
        vocab.institutional,
        vocab.domestic_constraints,
    ]:
        if not category_terms:
            continue
        # Combine 2-3 terms per query to stay within query limits
        query = " OR ".join(f'"{t}"' for t in category_terms[:3])
        results = await brave_client.search_news(
            query=query,
            country_code=country_config.news_discovery.brave_params.country,
            search_lang=country_config.news_discovery.brave_params.search_lang,
            goggles_id=country_config.news_discovery.goggle_url,
            count=20,
        )
        additional_results.extend(results)
    
    # Deduplicate against triage results by URL
    triage_urls = {r["url"] for r in triage_results}
    new_results = [r for r in additional_results if r["url"] not in triage_urls]
    
    return new_results
```

Total additional queries per deep-dive country: ~10-12 (actors) + 5 (vocabulary) = ~15-17 queries. Combined with triage's 2 queries, each deep-dive country has ~17-19 total queries producing 220-350 results.

### 3. Story Map Agent

New module: `src/monitor/agents/story_map.py`

An LLM call that takes all search results (triage + expansion) and clusters them into distinct stories.

**Input:** All search results for this country (headlines, snippets, URLs, source domains, dates) + the country's actor list for disambiguation.

**Prompt:** `prompts/story_map_agent.md` (already written, in the prompts directory)

**Output:** Structured JSON conforming to the story map schema:
```json
{
  "country": "mx",
  "analysis_date": "2026-03-23",
  "search_results_total": 287,
  "stories_identified": 19,
  "off_topic_filtered": 23,
  "stories": [
    {
      "story_id": 1,
      "headline": "...",
      "summary": "...",
      "actors_involved": ["Sheinbaum", "SRE"],
      "signal_category_hint": "alignment_diplomatic",
      "source_count": 7,
      "sources": ["eluniversal.com.mx", "reforma.com", ...],
      "date_range": "2026-03-18 to 2026-03-20",
      "representative_urls": ["https://...", "https://..."]
    }
  ],
  "single_source_items": [...],
  "noise_summary": "..."
}
```

Add a Pydantic model for story map output validation.

### 4. Selective Extraction

Extract full article text only for:
- Representative URLs from each story cluster (top 1-2 per cluster)
- Single-source item URLs
- Guardian API results (arrive pre-extracted, bypass extraction chain)

Use the existing extraction routing table (`extraction/routing.yaml`) and parallel pool dispatch. Total extractions per deep-dive country: ~30-50.

### 5. Country Agent Input Assembly

Modify the country agent's input assembly in the orchestrator to pass:
- The story map (full structured output from step 3)
- Extracted articles (keyed to story_id and URL)
- Layer 2 government findings (unchanged)
- Country dossier + ledger (unchanged)

The country agent prompt (`prompts/country_agent_deep_dive_v4.2.md`) already expects story map input — it was updated for this.

### 6. Orchestrator Pipeline

Update `src/monitor/orchestrator.py` to implement this sequence for deep-dive countries:

```python
async def run_deep_dive(country_code: str, triage_results: list[dict]):
    config = load_country_config(country_code)
    
    # Step 1: Expand search beyond triage
    expansion_results = await expand_search(config, brave_client, triage_results)
    all_results = triage_results + expansion_results
    
    # Step 2: Story map
    story_map = await run_story_map_agent(config, all_results)
    
    # Step 3: Selective extraction
    urls_to_extract = collect_representative_urls(story_map)
    extracted = await extract_articles(urls_to_extract)  # routing table dispatch
    
    # Step 4: Guardian API (if applicable)
    guardian_articles = await guardian_extract_for_country(...)  # if country in GUARDIAN_COUNTRIES
    
    # Step 5: Country agent
    weekly_entry = await run_country_agent(
        config=config,
        story_map=story_map,
        extracted_articles=extracted + guardian_articles,
        gov_findings=gov_findings,  # from Layer 2
        dossier=dossier,
        ledger=ledger,
    )
    
    # Step 6: Devil's advocate
    critique = await run_devils_advocate(weekly_entry)
    weekly_entry.devils_advocate = critique
    
    # Step 7: Ledger write
    await append_weekly_entry(country_code, weekly_entry)
```

For maintenance countries:
```python
async def run_maintenance(country_code: str, triage_results: list[dict], gov_findings: dict):
    # Log triage headlines + gov findings to ledger
    # Update posture summary lightly
    # No story map, no extraction, no country agent
    await log_maintenance_entry(country_code, triage_results, gov_findings)
```

## What NOT to Change

- Triage Phase 1 (Brave searches) — already working
- Triage Phase 2 (LLM depth decision) — already working
- Layer 2 government source discovery — built separately
- Devil's advocate, regional synthesis, executive agent — unchanged
- Ledger operations — unchanged

## File Touchpoints

| File | Change |
|------|--------|
| `src/monitor/agents/triage.py` | Return raw search results alongside scan summary |
| `src/monitor/agents/search_expansion.py` | NEW — targeted queries beyond triage |
| `src/monitor/agents/story_map.py` | NEW — LLM clustering of search results |
| `src/monitor/agents/country.py` | Update input assembly to accept story map |
| `src/monitor/orchestrator.py` | Connect triage → expansion → story map → extraction → country agent |
| `src/monitor/schemas/story_map.py` | NEW — Pydantic models for story map output |
| `prompts/story_map_agent.md` | Already exists — load as template |
| `tests/monitor/test_story_map.py` | NEW — test clustering output, schema validation |

## Test

Run the full pipeline for Mexico, week of March 16-23, 2026. Validate:
1. Triage results (wire + domestic) appear in the story map input
2. Search expansion adds targeted actor/vocabulary results
3. Story map produces 15-25 distinct story clusters
4. Extraction runs only for representative URLs (~30-50 total)
5. Country agent receives story map with source counts visible
6. No stories from triage are silently dropped
