# Middle Powers Monitor — Architecture Diagrams

Source of truth: `src/monitor/` as of 2026-04-21. Tests (`tests/monitor/`) are omitted by request.

---

## 1. System Context

External services, local state, and the CLI surface around the `monitor` package.

```mermaid
flowchart LR
    subgraph External["External services"]
        BRAVE[Brave News API]
        SEARCHAPI[SearchAPI]
        GUARDIAN[Guardian API]
        ANTHROPIC[Anthropic API<br/>claude-sonnet-4-6]
    end

    subgraph Repo["Repository state"]
        CONFIGS[assets/country_configs/*.yaml<br/>30 countries]
        PROMPTS[assets/prompts/*.md]
        GOGGLES[assets/country_goggles/*.goggle]
        DOSSIERS[assets/country_dossiers/*.md]
        LEDGERS[ledgers/<br/>countries · regional · global · story_maps]
        TRACES[briefs/&lcub;date&rcub;/traces/<br/>per-stage JSON]
        SITE[site/briefs/&lcub;date&rcub;/<br/>published MDX]
    end

    CLI["CLI: python -m monitor<br/>run · recover · triage · assemble · publish · replay · status"]
    PKG[["src/monitor package"]]

    CLI --> PKG
    PKG --> ANTHROPIC
    PKG --> BRAVE
    PKG --> SEARCHAPI
    PKG --> GUARDIAN
    CONFIGS --> PKG
    PROMPTS --> PKG
    GOGGLES --> PKG
    DOSSIERS --> PKG
    PKG <--> LEDGERS
    PKG --> TRACES
    PKG --> SITE
    SITE -. Mintlify deploy .-> FYI[middlepowers.fyi]
```

---

## 2. Weekly Pipeline

End-to-end flow of `cmd_run`, following `orchestrator.run_desk_pipeline` → regional → executive → newsletter → publishing. Every stage also writes a trace JSON file to `briefs/{date}/traces/`.

```mermaid
flowchart TD
    START(["cmd_run(end_date, country_codes?)"]) --> L2

    subgraph DESK["Desk pipeline — per-country, concurrent"]
        direction TB
        L2["1. Layer 2<br/>government source collection<br/>agents/government.py"]
        DOMAINS["2. Assemble domain lists<br/>assemble_country_domains"]
        TRIAGE["3. Triage scan + depth decision<br/>agents/triage.py"]
        EXPAND["4. Search expansion<br/>agents/expansion.py + collection/brave.py"]
        STORY["5. Story Map clustering<br/>agents/story_map.py"]
        EXTRACT["6. Selective extraction<br/>collection/extract.py"]
        COUNTRY["7. Country Agent — 5-signal analysis<br/>agents/country.py"]
        DA["8. Devils Advocate<br/>agents/devils_advocate.py"]
        APPLY["9. Apply to ledger<br/>ledger/storage.py"]

        L2 --> DOMAINS --> TRIAGE --> EXPAND --> STORY --> EXTRACT --> COUNTRY --> DA --> APPLY
    end

    APPLY --> REGIONAL["10. Regional Synthesis — 6 regions<br/>agents/regional.py"]
    REGIONAL --> EXEC["11. Executive Synthesis<br/>agents/executive.py"]

    EXEC --> BUILD

    subgraph NEWS["Newsletter assembly — 3 edit rounds"]
        direction TB
        BUILD["12. build_all_pages<br/>newsletter/content_builder.py"]

        subgraph R1["Round 1 — country scope"]
            direction LR
            E1["edit_all"] --> C1["copyedit_all"] --> S1["style_edit_all"]
        end

        RW["write_all_regional_essays<br/>regional_writer.py"]

        subgraph R2["Round 2 — regional scope"]
            direction LR
            E2["edit_all"] --> C2["copyedit_all"] --> S2["style_edit_all"]
        end

        GW["write_global_essay<br/>global_writer.py"]

        subgraph R3["Round 3 — executive scope"]
            direction LR
            E3["edit_all"] --> C3["copyedit_all"] --> S3["style_edit_all"]
        end

        BUILD --> E1
        S1 --> RW --> E2
        S2 --> GW --> E3
    end

    S3 --> RENDER

    subgraph PUB["Publishing"]
        direction TB
        RENDER["13. render_pages<br/>Jinja2 templates to MDX<br/>newsletter/renderer.py"]
        PUBLISH["14. publish_brief<br/>write site/briefs/{date}/<br/>newsletter/publish.py"]
        RENDER --> PUBLISH
    end

    PUBLISH --> DONE(["7 MDX pages:<br/>overview + at-a-glance + 5 region pages"])

    REC[["RunRecorder<br/>run_recorder.py"]]
    REC -. "snapshots ledgers,<br/>hashes prompts,<br/>records timings and cost" .-> DESK
    REC -.-> REGIONAL
    REC -.-> EXEC
    REC -.-> NEWS
    REC -.-> PUB
```

Notes:

- `cmd_recover` reuses the same stages scoped to one or more countries. With `--skip-regional` it preserves other countries' prose by reading prior MDX back (`_extract_country_narratives_from_mdx` in `cli.py`).
- `--resume-from` checkpoints between the five top-level stages (`desk`, `regional`, `executive`, `newsletter`, `publishing`) by reloading ledgers/traces from disk.

---

## 3. Package Layout

Modules inside `src/monitor/` and how they compose. Arrows are "imports from / calls into."

```mermaid
flowchart LR
    CLI[cli.py<br/>argparse entrypoints]
    ORCH[orchestrator.py<br/>run_desk_pipeline]

    subgraph AGENTS["agents/ — 11 LLM agents"]
        direction TB
        A_GOV[government.py]
        A_TRI[triage.py]
        A_EXP[expansion.py]
        A_SM[story_map.py]
        A_CTY[country.py]
        A_DA[devils_advocate.py]
        A_REG[regional.py]
        A_EXEC[executive.py]
        A_ED[editor.py]
        A_CE[copyeditor.py]
        A_ST[style_editor.py]
    end

    subgraph COLL["collection/ — sources"]
        C_BR[brave.py]
        C_SA[searchapi.py]
        C_GU[guardian.py]
        C_EX[extract.py]
    end

    subgraph LED["ledger/"]
        L_INIT[initialize.py]
        L_STO[storage.py]
        L_CON[consolidation.py]
        L_VAL[validation.py]
    end

    subgraph NL["newsletter/"]
        direction TB
        N_CB[content_builder.py]
        N_CM[content_models.py]
        N_SE[structured_editor.py]
        N_SC[structured_copyeditor.py]
        N_RW[regional_writer.py]
        N_GW[global_writer.py]
        N_ASM[assembly.py]
        N_REN[renderer.py<br/>Jinja2]
        N_PUB[publish.py]
        N_TPL[templates/<br/>overview · region · at-a-glance .mdx.j2]
        N_REN --> N_TPL
    end

    subgraph INFRA["Cross-cutting"]
        direction TB
        CFG[config.py]
        MOD[models.py]
        SAN[sanitize.py]
        SCH[schema_helpers.py<br/>tool_use schemas]
        VAL[validation.py]
        RET[retry.py]
        RL[rate_limit.py]
        TR[trace.py]
        RR[run_recorder.py]
        TIM[timing.py]
    end

    CLI --> ORCH
    CLI --> NL
    CLI --> LED
    CLI --> RR

    ORCH --> AGENTS
    ORCH --> COLL
    ORCH --> LED
    ORCH --> RR

    AGENTS --> SCH
    AGENTS --> SAN
    AGENTS --> RET
    AGENTS --> RL
    AGENTS --> TR
    AGENTS --> MOD
    AGENTS --> CFG

    COLL --> CFG
    COLL --> RL

    NL --> AGENTS
    NL --> LED
    NL --> MOD

    LED --> MOD
    LED --> VAL
```

---

## 4. Data Flow Summary

| Input | Transforms via | Output |
|---|---|---|
| Country YAMLs + goggles + dossiers | Layer 2 + triage + expansion + extraction | Raw article corpus (in-memory + `briefs/{date}/traces/`) |
| Raw corpus | Story Map → Country Agent → Devil's Advocate | `ledgers/countries/{code}.json` weekly entry |
| Country ledgers | Regional agent (per region) | `ledgers/regional/{region}_{date}.json` |
| Regional reports | Executive agent | `ledgers/global.json` entry |
| All ledgers + story maps | `build_all_pages` → 3 edit rounds → renderer | `site/briefs/{date}/*.mdx` (7 pages) |

---

## Regenerating this document

The diagrams above are hand-maintained. If the pipeline topology changes:

1. Stage list: re-check `cmd_run` in `src/monitor/cli.py` and `run_desk_pipeline` in `src/monitor/orchestrator.py`.
2. Agent list: `ls src/monitor/agents/`.
3. Newsletter ordering: the three `edit_all → copyedit_all → style_edit_all` blocks in `cmd_run` interleaved with `write_all_regional_essays` and `write_global_essay`.
