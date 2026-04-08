# Output Format v2: Story-Centric Briefings

## Overview

Shift from per-leader-organized output to story-centric output. Both per-leader dossiers and the aggregate briefing follow the same structure. The aggregate briefing synthesizes across leader dossiers rather than generating independently.

## Per-Leader Dossier

Each leader's dossier is built independently through the same pipeline: fetch content from that leader's sources, cluster, score, and write out.

### Sections

#### Main Stories (up to 7)

The most significant stories for this leader, regardless of whether they are international or domestic in scope. Selection driven by cluster quality and source coverage count. No hard requirement to reach 7.

Each story includes:
- Narrative summary of the event/development
- Leader actions and reactions
- Explicitly stated positions only — no speculative analysis

If a leader has no international stories, domestic stories fill Main Stories. Main Stories should not be empty — every leader has news.

#### International Stories

Events with international scope or multi-country involvement that did not make Main Stories. Summaries of each event or combined summaries if clustered.

#### Domestic Stories

Events with national or regional scope that did not make Main Stories. Singleton rollups where applicable (e.g., "infrastructure projects in X, Y, Z" as a combined summary).

#### Between the Lines

Themes that may not be immediately evident from the stories. Things to watch as events develop. Grounded in the week's content, not general trajectory speculation.

#### Domestic Context (future — see TODO)

Background political and structural context for the leader's country. Separate data flow from domestic source search and clustering.

## Aggregate Briefing

Built by looking across all per-leader dossiers. Identifies overlapping stories across leaders and synthesizes combined narratives.

### Sections

#### Main Stories (up to 7)

Two types of stories qualify:
1. **Shared stories** — Where multiple leaders' clusters cover the same event (e.g., a Macron-Starmer bilateral appears in both dossiers). The aggregator examines topics/clusters, named entities, and summaries from each leader's dossier and writes a combined narrative.
2. **Standalone high-coverage stories** — A single leader's story with enough source coverage to warrant top billing.

Same rules as per-leader: narrative + actions/reactions + explicit positions only.

#### International Stories

International-scope events across all leaders that did not make Main Stories.

#### Domestic Stories

Domestic-scope events across all leaders that did not make Main Stories. Grouped by country or region where appropriate.

#### Between the Lines

Two parts:

1. **Thematic analysis** — Themes and connections surfaced across all topics/events in the briefing.
2. **Per-leader summaries** — One-line summaries drawn from each leader's Between the Lines section.

Example:
```
Between the Lines
- Ukraine is poised to defeat Russia
- Mexico's trade deal with Canada is significant
- Zelenskyy: Diplomatic success before elections; note Europe's reaction
- Sheinbaum: Economic complexity addressed; watch for upcoming elections
```

## Pipeline Implications

### Per-Leader Pipeline (no change to flow, output structure changes)

```
fetch snippets → embed → cluster → score → fetch full articles → extract entities
→ build dossier (Main Stories / International / Domestic / Between the Lines)
```

Entity extraction and named entity comparison across sources within a cluster are important for comprehensive summaries. Each source's entities/events should be present in the fleshed-out cluster summary.

### Aggregate Pipeline

```
collect all leader dossiers
→ identify overlapping clusters across leaders (entity/topic matching)
→ synthesize shared stories from cross-leader cluster data
→ rank and select Main Stories (shared + standalone high-coverage)
→ distribute remaining stories to International / Domestic
→ generate Between the Lines (thematic analysis + per-leader summaries)
```

## TODO

- [ ] **Domestic Context flow**: Search domestic news components of domestic sources, cluster results, and generate background context per country. Separate from event-driven news.
- [ ] **Foreign ministry expansion**: Expand source search to include foreign ministry sources to improve international story coverage, particularly for leaders/countries with limited wire coverage.
