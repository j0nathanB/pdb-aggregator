# CLAUDE.md

## Project Overview

Middle Powers Monitor — AI-powered geopolitical intelligence system. 30 countries, 5 regions, weekly batch pipeline. Published at middlepowers.fyi (Mintlify).

### Pipeline (14 stages)

Gov Source Discovery → Triage (depth decisions) → Search Expansion → Story Map Agent (clustering) → Selective Extraction → Country Agent (5-signal analysis) → Devil's Advocate → Ledger Write → Regional Synthesis → Executive Synthesis → Newsletter Assembly (deterministic) → Editor → Style Editor → Copyeditor → Card Summary → Publish

### Key Paths

- Pipeline code: `src/monitor/` (orchestrator, agents, collection, newsletter, models, cli)
- 11 LLM agents: `src/monitor/agents/` (country, triage, expansion, story_map, government, devils_advocate, regional, executive, editor, copyeditor, style_editor)
- Prompts: `assets/prompts/*.md`
- Country configs: `assets/country_configs/countries/*.yaml` (30 files)
- Goggles: `assets/country_goggles/*.goggle`
- Dossiers: `assets/country_dossiers/*.md`
- Settings: `assets/country_configs/settings.yaml`
- Extraction routing: `assets/country_configs/extraction_routing.yaml`
- Ledgers: `ledgers/` (countries, regional, global, story_maps)
- Pipeline traces: `briefs/{date}/traces/`
- Published output: `site/briefs/{date}/` (7 MDX files per week)
- Tests: `tests/monitor/` (28 modules, 643 tests, pytest + pytest-asyncio)
- Architecture doc: `docs/mpm_unified_architecture_v4.md`

### Model & Specs

- Model: claude-sonnet-4-6 (thinking_budget: 16000)
- 5 signal categories: alignment_diplomatic, security_defense, economic_tech, institutional, domestic_regime
- Python env: `.venv/bin/python`

## Critical Rules

### Never overwrite site/briefs/ without committing first

NEVER run `git checkout`, `publish`, or any operation that overwrites `site/briefs/` without first committing the current state. Edited prose costs significant API calls to regenerate — treat `site/briefs/` as precious output, not regenerable artifacts.

1. After ANY pipeline run that writes to `site/briefs/`, commit immediately before doing anything else
2. Before running `publish` CLI command, check if `site/briefs/` has uncommitted changes and commit them first
3. Before ANY `git checkout` or `git restore` on site files, verify what you're about to lose

### Always commit briefs after pipeline runs

After any pipeline run that produces site output (including partial re-runs for individual countries), commit the `site/briefs/` directory along with any code changes. The pipeline's editor and copyeditor stages produce polished prose that costs significant API tokens to regenerate. Don't treat brief output as disposable.
