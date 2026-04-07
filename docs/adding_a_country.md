# Adding a Country to the Middle Powers Monitor

## Overview

Adding a country requires creating four asset files (config, goggle, dossier, government config), updating one (or two) Python files, and running validation. The pipeline discovers countries dynamically from YAML, so most code is unchanged.

The end goal is a single command:

```bash
add_mpm_country pakistan pk near_east_south_asia
```

…that runs the full onboarding pipeline.

## Assets to Create

| File | Purpose |
|------|---------|
| `assets/country_configs/countries/{code}.yaml` | Actors, languages, blind spots, query vocabulary, Brave params |
| `assets/country_goggles/{code}.goggle` | Brave search boosting: tier 1–3 outlets, government domains, discard list |
| `assets/country_dossiers/{name}_dossier_{date}.md` | Structural context: actors, institutions, blind spots, historical patterns |
| `assets/government/{code}.yaml` | Government source discovery config |

## Code to Update

| File | Change |
|------|--------|
| `src/monitor/agents/regional.py` | Add country code to `REGION_COUNTRIES[Region.{REGION}]` |
| `src/monitor/collection/guardian.py` | Add Guardian API tag mapping (only if Guardian covers the country) |

No other code changes needed — `src/monitor/config.py` loads all `assets/country_configs/countries/*.yaml` automatically.

## What Doesn't Need Changing

- `src/monitor/config.py` — country discovery is dynamic
- `site/docs.json` — country appears in its region's existing page
- Templates / renderer — handles any number of countries per region
- Region enum — only changes if adding a new region entirely

## Pending: Pakistan

Pakistan (`pk`) is the next country to add, slotting into `Region.NEAR_EAST_SOUTH_ASIA`.

---

## The `add_mpm_country` Pipeline

Multi-phase onboarding script. Phases run sequentially because each depends on prior outputs. The script uses the **Anthropic API with the `web_search` tool** for all LLM calls.

### Phase 1: Dossier generation (3-pass LLM chain)

Prompts live in `dev/check_dossiers/prompts/updated_prompts/`. Each pass uses the Anthropic API with `web_search` to ground claims in reputable sources.

1. **Pass 1** (`pass_1 updated.md`): Sections 0–7 — foundational structure, political economy, geographic constraints, demographic fault lines, economic dependencies, energy/resource structure, fiscal/debt architecture, trade/sanctions exposure.
2. **Pass 2** (`pass_2 updated.md`): Sections 8–12 — environmental/climatic structure, illicit networks, information ecosystem, international institutional commitments, military/security DNA. Pass 1 output supplied as context. Footnote numbering continues from Pass 1.
3. **Pass 3** (`pass_3 updated.md`): Sections 13–20 — dissent/civil society, patron-client history, constitutional crises, collective memory, cross-facet intersection, key analytical judgments, watch indicators, pipeline integration notes. Pass 1+2 output supplied as context.
4. **Output structure**:
   - Individual passes: `assets/country_dossiers/_pass1/{name}_pass1_{date}.md`, `_pass2/`, `_pass3/`
   - Merged dossier: `assets/country_dossiers/{name}_dossier_{date}.md`
5. **Human review**: dossier requires editorial review before use.

### Phase 2: Source discovery and verification

Prompts live in `dev/source_maps/`.

6. **Reference dossier**: load the merged dossier as context for the curation prompt (Section 0 actors and Section 10 information ecosystem are most relevant).
7. **Source curation** (`source_curation_prompt_v2.md`): Anthropic API with `web_search` to identify domestic newspapers, wire services, think tanks. Output: markdown file at `dev/source_maps/media/source_maps/_drafts/{name}_curation.md`.
8. **Source audit** (`source_whitelist_audit_prompt_v2.md`): Anthropic API with `web_search` to verify and audit the curated list — checks editorial standards, ownership, political alignment, reliability. Output: `dev/source_maps/media/source_maps/_drafts/{name}_audit.md`.
9. **Government source discovery** (`government_sources_prompt.md`): Anthropic API with `web_search` to identify ministry pages, official feeds, parliamentary records. Output: `dev/source_maps/gov/_drafts/{name}_gov.md`.
10. **Verify against Brave Search** (`src/monitor/collection/brave.py`): for each curated domain, run a Brave query and confirm results are returned. Drop domains that return zero results.
11. **Verify against SearchAPI** (`src/monitor/collection/searchapi.py`): for each government domain, run a `site:domain` query via SearchAPI (Google) and confirm results. Drop domains that return zero results.
12. **Final source map**: write `dev/source_maps/media/source_maps/{name}.md` following the schema in `india.md` (intro paragraph, then ranked source list with field tables).

### Phase 3: Extraction routing

13. **Test extraction methods per verified domain**: for each confirmed source, run the 4-method experiment from `dev/source_maps/media/RETRIEVAL_EXPERIMENT_GUIDE.md` (curl+trafilatura → diffbot → playwright → browserbase). Record which method successfully extracts article content for each domain.
14. **Build extraction routing entry**: append per-domain `primary` method, `confidence`, and `fallbacks` chain to `assets/country_configs/extraction_routing.yaml`.
15. **Update brave_sources.yaml**: append verified source mappings to `assets/country_configs/brave_sources.yaml`.

### Phase 4: Config generation

16. **Generate goggle file** at `assets/country_goggles/{code}.goggle`. Inferred tier rules:
    - **Tier 1 (boost=3)**: 4–6 most authoritative national broadsheets and the dominant agenda-setting outlet, regardless of language.
    - **Tier 2 (boost=2)**: 6–10 secondary national outlets + key government domains (foreign ministry, PM office, parliament).
    - **Tier 3 (boost=1)**: 4–8 think tanks, academic journals, specialized analytical outlets.
    - **Discard**: tabloids, partisan rage bait, low-signal aggregators identified in the audit phase.
17. **Generate country config YAML** at `assets/country_configs/countries/{code}.yaml`: actors (with primary flag and search terms), languages, blind spots, query vocabulary by signal category, Brave API params, references to goggle file and extraction config.
18. **Generate government config YAML** at `assets/government/{code}.yaml`: government domains, ministry pages, official feeds. Referenced by the country config's `government_discovery.config_file`.

### Phase 5: Integration

19. **Update `REGION_COUNTRIES`** in `src/monitor/agents/regional.py`: add the country code to its region list.
20. **Update Guardian mapping** in `src/monitor/collection/guardian.py`: only if Guardian publishes a country tag.
21. **Update `site/about.mdx`**: bump the country count in the lead paragraph and add the country to its region's `<Card>` list.
22. **Update `site/llms.txt`**: bump the country count in the blockquote and the **Coverage** section, and add the country to its region's bullet.
23. **Validation triage scan**: run `python -m src.monitor.cli run --country {code} --triage-only --date {today}` to confirm Brave queries return results and extraction succeeds on a sample.
24. **First full single-country run**: `python -m src.monitor.cli run --country {code} --date {today}` to verify end-to-end.

### Phase 6: Final report

25. **Comprehensive onboarding report**: write a markdown file at `dev/check_dossiers/onboarding_reports/{name}_{date}.md` listing every output path, the verification results from each phase, dropped sources with reasons, extraction method coverage, and the validation run summary. Surface anything that requires human review before the country goes into the next weekly pipeline.

---

## Summary of LLM calls

| Phase | Step | Prompt | Tool |
|-------|------|--------|------|
| 1 | 1 | `pass_1 updated.md` | Anthropic + web_search |
| 1 | 2 | `pass_2 updated.md` | Anthropic + web_search |
| 1 | 3 | `pass_3 updated.md` | Anthropic + web_search |
| 2 | 7 | `source_curation_prompt_v2.md` | Anthropic + web_search |
| 2 | 8 | `source_whitelist_audit_prompt_v2.md` | Anthropic + web_search |
| 2 | 9 | `government_sources_prompt.md` | Anthropic + web_search |

Six LLM calls total. Phases 3–6 are deterministic.
