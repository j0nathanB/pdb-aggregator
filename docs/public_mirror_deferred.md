# Public-facing mirror repo (deferred)

**Status:** Scoped, deferred. Set up when ready to publish the pipeline code without leaking prompts, dossiers, or ledgers.

## Goal

Maintain a "clean" public-facing repo (e.g., `middlepowers-monitor`) that contains the pipeline code and architecture documentation but **excludes** the LLM prompts, country dossiers, source curation, ledgers, traces, and dev/ scratch work. The current `pdb-aggregator` repo stays private and is the source of truth.

## Why two repos and not `.gitignore`

`.gitignore` only affects future commits in the same repo and doesn't change visibility — a repo is public or private as a whole. To selectively expose code without exposing the editorial assets, you need a separate repo.

## Recommended approach: Option A (separate public repo + sync script)

1. Create a new public GitHub repo (`middlepowers-monitor` or similar).
2. Write `scripts/sync_public.py` that:
   - Takes the path to a local clone of the public repo as a target
   - Copies an allowlisted set of paths into it
   - Replaces hidden directories with stub README files explaining they're not public
   - Updates a top-level README explaining the public repo is a snapshot
3. Run the sync manually when releasing updates (not on every commit). Review the diff before pushing.

The sync is one-way (private → public). The private repo always stays the source of truth.

## File allowlist / blocklist

| Path | Decision | Why |
|------|----------|-----|
| `src/monitor/` | **Public** | Pipeline code — most valuable for transparency |
| `tests/monitor/` | **Public** | Demonstrates correctness |
| `docs/` | **Public** (with review) | Architecture documentation |
| `requirements.txt`, `Dockerfile` | **Public** | Standard project metadata |
| `scripts/` | **Public** (with review) | `add_mpm_country.py`, `reedit.py`, `run_pipeline.py` are illustrative |
| `assets/prompts/` | **Hide** | LLM system prompts — editorial secret sauce |
| `assets/country_dossiers/` | **Hide** | Proprietary structural analysis |
| `assets/country_configs/countries/*.yaml` | **Hide** | Query vocab, blind spots, actor curation |
| `assets/country_goggles/*.goggle` | **Hide** | Source rankings (or publish — not strictly sensitive) |
| `assets/country_configs/extraction_routing.yaml` | **Hide** | Extraction strategy |
| `assets/government/*.yaml` | **Hide** | Government domain curation |
| `briefs/{date}/traces/` | **Hide** | Raw LLM responses, intermediate state |
| `ledgers/` | **Hide** | Running pipeline state |
| `dev/` | **Hide** | Scratch work, prompt experiments |
| `site/` | **Depends** | Published MDX is already public at middlepowers.fyi |

## Public repo README (suggested content)

```
# Middle Powers Monitor — pipeline code

This repository is a code-and-architecture snapshot of the Middle Powers Monitor (MPM) pipeline. It contains the Python source code, tests, and architecture documentation for the AI pipeline that produces MPM's weekly geopolitical intelligence briefs.

What is NOT in this repo (kept private):
- LLM system prompts
- Country structural dossiers
- Source curation, query vocabularies, extraction routing
- Pipeline traces and ledgers
- Dev/scratch work

Published briefs are at https://middlepowers.fyi.
Full methodology is at https://middlepowers.fyi/about.
```

## Why not the alternatives

- **`.gitignore` + `git filter-repo` to make the current repo public**: rewrites history, high risk, one mistake leaks forever, easy to accidentally include sensitive paths in future commits.
- **Branch-based public/private split**: confusing, easy to leak content, doesn't actually hide anything because all branches are visible.
- **Submodule split**: requires reorganizing the current repo. Non-trivial.

The two-repo approach is the safest because the private repo is never exposed and the sync is auditable.

## Effort estimate

- Allowlist refinement + script: 1 hour
- New public repo setup + initial sync: 30 min
- README + stub files for hidden directories: 30 min
- Testing the sync: 30 min

**Total: ~2.5 hours.**
