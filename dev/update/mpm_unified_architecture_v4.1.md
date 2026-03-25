# Middle Powers Monitor — Unified Architecture v4.1

## Date: 2026-03-19

## Purpose

This document consolidates all architectural decisions made across multiple design conversations into a single implementation-ready specification. It supersedes: v4 of this document, the v2/v3 Implementation Plans, the Architecture Direction doc, the Collection Decision Brief, and the prior ledger schema definition. Where those documents conflict, this document reflects the resolved decision.

### Changes from v4

v4.1 introduces a two-layer collection architecture that separates collection from analysis:
- **Layer 1 (News Discovery)** replaces Claude's web_search with the **Brave Search News API + per-country Goggles** for source-prioritized news discovery
- **Layer 2 (Government Source Discovery)** adds **SearchAPI with Google results scoped to government domains** as a separate collection track
- A new **Government Source Agent** processes Layer 2 content before it reaches the country agent
- The **country agent becomes a pure analyst** — it no longer runs searches. It reads pre-collected material from both layers
- **Layer 2 runs before triage**, meaning government source findings can trigger deep-dive decisions
- **CountryConfig** expands to carry Goggle files, government domain configs, and localized query vocabulary
- **SearchAPI** is retained with a narrow role: Google-scoped queries against government domains only (Layer 2)
- Full article **extraction** uses a tiered fallback chain: curl+trafilatura → Claude web_fetch → Diffbot Article API → Playwright → Publisher APIs
- **Diffbot** is retained as Tier 3 extraction (complex layouts, metered paywalls), no longer used for discovery or NLP
- **Claude's web_fetch** is retained as Tier 2 extraction (clean HTML), no longer used for discovery by the country agent

---

## 1. What This System Does

The Middle Powers Monitor is an automated weekly OSINT analysis pipeline covering 28 countries across five editorial regions. It produces a narrative newsletter with analytical depth tracking how states are positioning themselves in the international order.

The publication's analytical thesis: rhetorical and structural alignment with the liberal international order are diverging. Being "pro-West" no longer reliably maps to "pro-LIO" when the West itself is fractured. The Monitor's distinctive contribution is distinguishing countries that rhetorically identify with liberal values from those structurally sustaining institutional architecture through treaty compliance, multilateral engagement, rule-of-law norms, and social compact durability. US retrenchment is treated as a structural condition, not a cyclical one.

---

## 2. What Changed from the Current System

The current system (`pdb-aggregator`) is a leader-centric pipeline: SearchAPI → Diffbot → E5 embeddings/HDBSCAN clustering → LLM significance scoring → per-leader dossier build → aggregate briefing → newsletter. It tracks 15 leaders with a custom ML stack.

The new system replaces this entirely:

| Dimension | Current System | New Architecture |
|-----------|---------------|-----------------|
| Unit of analysis | Leader (15) | Country (28) |
| Source discovery | SearchAPI → ML clustering | Brave Search News API + per-country Goggles (Layer 1) |
| Government sources | Not systematically collected | SearchAPI (Google) scoped to government domains (Layer 2) |
| Extraction | Diffbot Article + NLP endpoints | Tiered fallback: curl+trafilatura → Claude web_fetch → Diffbot → Playwright → Publisher API |
| Clustering | E5 embeddings + HDBSCAN | Eliminated — LLM handles grouping natively |
| Collection/analysis separation | Interleaved (LLM searches and analyzes) | Separated — two collection layers feed a pure-analyst country agent |
| Analytical structure | Event clustering → dossier build → aggregate | Gov monitoring → Triage → Country desk → Regional synthesis → Executive synthesis |
| Persistence | Running picture per leader (weekly markdown) | Country ledger (JSON, five signal categories) + global ledger |
| Cross-cutting analysis | Thread detection via semantic clustering | Stateless regional synthesis + global ledger dynamics |
| Publication | Single Opus renderer call | Deterministic assembly from structured JSON |
| ML dependencies | sentence-transformers, hdbscan, scipy, numpy | None |
| External APIs | SearchAPI, Diffbot | Brave Search News API (Layer 1 news discovery), SearchAPI (Layer 2 government discovery), Diffbot (Tier 3 extraction), Publisher APIs (Tier 5 extraction) |

---

## 3. Coverage

### Country Tiers

The 28 countries are organized into four analytical tiers. These are not geographic groupings — they describe each country's analytical role in the publication.

**The Shield (14):** European states testing whether autonomous defense capacity can be built without the US.
France, Germany, United Kingdom, Poland, Estonia, Lithuania, Latvia, Czech Republic, Romania, Norway, Sweden, Finland, Italy, Spain

**The Next Test (4):** Indo-Pacific states where deterrence credibility is being reassessed.
Japan, South Korea, Taiwan, Australia

**The Pivot (5):** Non-Western swing states whose alignment determines whether the liberal international order remains global or contracts into a Western bloc.
India, Turkey, Saudi Arabia, UAE, Indonesia

**The Periphery (4):** Americas — managing US proximity while asserting independent positioning.
Canada, Brazil, Mexico, Chile

**Ukraine** serves as "the crucible" — the most kinetic test of LIO defense — as backdrop and organizing context, not as a country desk subject.

Saudi Arabia and India are not middle powers. They're included as swing states whose positioning determines whether the LIO remains global or contracts.

### Editorial Regions (for newsletter structure)

These are editorial containers for the newsletter, not analytical units. No persistent regional state is maintained.

- The Americas: Canada, Mexico, Brazil, Chile
- Western Europe: France, Germany, UK, Italy, Spain, Norway, Sweden
- Frontline & Eastern Europe: Ukraine, Poland, Finland, Estonia, Lithuania, Latvia, Czech Republic, Romania
- Middle East, Turkey & South Asia: Turkey, Saudi Arabia, UAE, India
- Asia-Pacific: Taiwan, Japan, South Korea, Australia, Indonesia

### Phase 2 Expansion (deferred)

South Africa, Nigeria, Qatar, Singapore, Philippines. Argentina explicitly excluded — Milei's gutting of labor protections disqualifies it as a monitoring subject.

---

## 4. Five Signal Categories

The analytical lens applied to every country. These are fixed — they replace the dynamic thread model from earlier proposals. Each country always has all five categories; what changes is the content within them.

### 1. Alignment & Diplomatic Posture

Who is the state moving toward or away from? Tracks bilateral relationships, alliance dynamics, diplomatic signaling, summit outcomes, ambassador recalls, treaty commitments.

Maps to dossier sections: §14 (Patron-Client History), §17 (Cross-Facet Intersections)

### 2. Security & Defense Posture

How is the state securing itself physically? Tracks military deployments, defense procurement, joint exercises, arms transfers, security cooperation agreements, intelligence sharing, force posture changes.

Maps to dossier sections: §12 (Military/Security DNA), §9 (Illicit Networks & Shadow Governance)

### 3. Economic & Technological Statecraft

How is the state using economic and technological tools to position itself? Tracks trade agreements, sanctions compliance/evasion, industrial policy, critical minerals, semiconductor positioning, de-dollarization moves, sovereign wealth fund deployments, FDI screening, technology transfer controls, development finance.

Maps to dossier sections: §6 (Economic Structure), §7 (Infrastructure)

### 4. Institutional Engagement & Order-Building

Where is the state investing diplomatic capital in multilateral architecture? Tracks engagement with any institutional framework — not just LIO institutions. BRICS+ participation is not coded as defection. Covers treaty ratification, institutional funding, voting patterns, reform proposals, alternative institution creation.

Maps to dossier sections: §11 (International Institutional Commitments)

### 5. Domestic & Regime Constraints

What internal dynamics enable or limit external positioning? Tracks elections, coalition dynamics, judicial developments, protest movements, media landscape shifts, currency crises, popular legitimacy. Framed to handle both democratic veto players and competitive authoritarian constraints (elite cohesion, populist legitimation).

Maps to dossier sections: §6 (Cleavage Structures), §13 (Dissent Infrastructure), §10 (Information Ecosystem)

---

## 5. Architecture

### Pipeline Flow

```
WEEKLY CYCLE:

  STEP 0: GOVERNMENT SOURCE DISCOVERY — Layer 2 (all 28 countries)
    Method: SearchAPI (Google results) scoped to government
      domains via site: operators, past week
    Extraction: same tiered chain as Layer 1
      (curl → Diffbot → Playwright → etc.)
    Runs unconditionally — not triage-gated
    Output: government content per country

  STEP 0.5: GOVERNMENT SOURCE AGENT (all 28 countries)
    Input: Layer 2 extracted content + source intelligence map
           + country dossier (reference)
    Task: Classify each item (ground truth / intent signal),
          tag with signal categories, extract analytical
          essentials, note cross-references with media
    Output: structured government findings per country

  STEP 1: TRIAGE (all 28 countries, parallel)
    Inputs per country:
      - Wire scan headlines (Layer 1: Brave News API,
        wire sources only)
      - Lightweight domestic check (Layer 1: Brave News API,
        1-2 queries against Goggle-boosted domestic sources)
      - Government source findings (from Step 0.5)
      - Country posture summary from ledger
      - Global ledger running picture + triage implications
    Output: per-country depth decision
      - DEEP DIVE: full analytical treatment
      - MAINTENANCE: log findings, light ledger update

  STEP 2: NEWS COLLECTION — Layer 1 (depth varies by triage)
    Deep-dive countries:
      - Discovery: Full Brave News API queries with per-country Goggle
        Actor/institution search terms + localized vocabulary
      - Extraction: For significant results, full article text via
        tiered fallback (curl → web_fetch → Diffbot → Playwright → API)
    Maintenance countries:
      - Wire + headline findings from triage step are sufficient
      - No additional Layer 1 queries or extraction

  STEP 3: COUNTRY AGENTS (parallel, depth varies)
    Deep-dive countries:
      - Receives: Layer 1 news results + Layer 2 gov findings
        + country dossier + country ledger
      - Pure analysis — no searching
      - Assessment across five signal categories
      - Structured country analysis with evidence,
        confidence scoring, source tiering
    Devil's advocate (separate call per deep-dive country):
      - Argues against the country agent's assessments
      - Checks government framing vs. independent verification
      - Flags single-source dependencies
    Country ledger updated with full weekly entry

    Maintenance countries:
      - Wire + headline + gov findings logged to ledger
      - Posture summary lightly updated
      - No country agent call, no devil's advocate

  STEP 4: REGIONAL SYNTHESIS (5 regions, stateless, parallel)
    Inputs: country analyses for constituent countries
    No regional ledger — fresh cross-country pattern
    detection each week
    Output: regional report (editorial grouping)
    Safeguards: confidence inheritance, apophenia check,
    rejection log

  STEP 5: EXECUTIVE AGENT (sequential)
    Inputs: 5 regional reports + global ledger
    Output: executive briefing + updated global ledger
    The global ledger update includes triage implications
    that steer next week's depth decisions

  STEP 6: NEWSLETTER ASSEMBLY (deterministic, no API)
    Inputs: all structured outputs
    Output: newsletter.md
```

### Two-Layer Collection Architecture

**Layer 1 — News Discovery and Extraction (Brave Search News API + Goggles + Tiered Extraction)**

Layer 1 has two sub-steps: discovery (finding articles) and extraction (getting full text).

**Discovery:** Each country has a Goggle file that ranks domestic media sources by analytical priority:
- Tier 1 sources (`$boost=3`): Papers of record, essential outlets — surface first
- Tier 2 sources (`$boost=2`): Domain specialists, opposition voices — surface prominently
- Tier 3 sources (`$boost=1`): Supplementary perspectives — surface when relevant
- Discard rules (`$discard`): Tabloids, content farms, misinformation — actively removed

The pipeline runs topic queries (actor names + localized vocabulary terms) through Brave's News API with country/language parameters and the Goggle applied. Brave returns headlines, snippets, URLs, and metadata — but not full article text. Source count doesn't drive API cost — Goggles are ranking overlays, not additional queries.

**Extraction:** For articles identified by Brave (Layer 1) or SearchAPI (Layer 2) as significant, the pipeline attempts full text extraction through a tiered fallback chain:

| Priority | Method | When to use | Cost |
|----------|--------|-------------|------|
| Tier 1 | curl + trafilatura | Default for most domains. Simple HTTP + content extraction. Highest success rate (81%). | Free |
| Tier 2 | Claude web_fetch | Clean HTML article pages without heavy JavaScript or anti-bot protection | Free (API call) |
| Tier 3 | Diffbot Article API | Complex layouts, metered paywalls, CMS-embedded content | Per-call |
| Tier 4 | Headless browser (Playwright) | JavaScript-rendered pages, anti-bot protection, sites requiring interaction | Infrastructure |
| Tier 5 | Publisher API | Outlets with structured API access (Guardian Open Platform, FT, others) | Varies by publisher |

Each domain in the extraction routing table is pre-assigned to its empirically best-performing method. The pipeline dispatches to the right tier immediately based on domain lookup, only falling back through the chain on unexpected failures. If all tiers fail, the article is processed from headline + snippet only, and any assessment relying on it is capped at confidence 2.

Both Layer 1 and Layer 2 use the same extraction chain. Government domain URLs discovered via SearchAPI are extracted through the same routing table as news articles discovered via Brave.

Layer 1 is triage-gated: deep-dive countries get full Brave queries with extraction. Maintenance countries rely on the wire/headline check from triage (headlines and snippets only — no full extraction needed). Layer 2 runs unconditionally for all 28 countries.

**Layer 2 — Government Source Discovery (SearchAPI + Google, site-scoped)**

Each country has a government domain config listing official institutional domains to search:
- P1 domains (foreign ministry, defense ministry, head of government): queried every cycle
- P2 domains (parliament, official gazette, central bank, trade ministry): queried every cycle

The pipeline uses SearchAPI with Google results, scoped to government domains via `site:` operators. Queries combine government domain scoping with relevant terms (e.g., `site:sre.gob.mx comunicado`, `site:gob.mx SEDENA adquisición`), filtered to the past week. This replaces direct RSS polling and Playwright-based government site scraping — Google indexes government content reliably, and SearchAPI provides structured access to those results.

Extraction uses the same tiered fallback chain as Layer 1 (curl → Diffbot → Playwright → etc.). Government domains already tested in the extraction report get their known-best method from the routing table.

Layer 2 runs unconditionally for all 28 countries every week, regardless of triage. Government sources publish on their own schedule. Layer 2 findings feed into triage as input — a significant government action can trigger a deep dive even if wires are quiet.

**Why two layers:**

News discovery (Layer 1) and government monitoring (Layer 2) serve complementary functions:
- Layer 1 tells the pipeline what the media is reporting — how events are being framed, contested, and contextualized domestically
- Layer 2 tells the pipeline what the government actually did — the announcement, the treaty text, the procurement record, the legislative language

The country agent needs both to produce grounded analysis. Media coverage without official sources lacks primary evidence. Government sources without media coverage lack independent verification and domestic reception context.

### Persistence Layer

Four categories of persistent objects:

**Country Ledger (28 files, `ledgers/countries/{code}.json`):**
Per-country analytical state organized around five signal categories. Updated every cycle — full entry for deep-dive weeks, light entry for maintenance weeks. Consumers: country agent, triage (posture summary only), devil's advocate.

**Global Ledger (1 file, `ledgers/global.json`):**
Cross-country dynamics, watchlist, analytical uncertainties. Updated by the executive agent only. Consumers: triage (posture summary + triage implications), executive agent (prior state), newsletter assembly (watchlist).

**Country Dossiers (28 files, `dossiers/{code}.md`, static):**
Structural reference documents. Updated quarterly or when structural claim status shows drift. Consumer: country agent (deep dive only), government source agent (reference).

**Collection Configuration (per country, static between curation cycles):**
- Goggle files (`goggles/{code}.goggle`): Brave Search ranking overlays for Layer 1 discovery. Generated by the Source Intelligence Map curation prompt.
- Extraction routing table (`extraction/routing.yaml`): Per-domain extraction method assignments based on empirical testing. Shared across all countries.
- Government domain configs (`government/{code}.yaml`): Layer 2 domain lists and query terms for SearchAPI government source discovery. Derived from the Government Sources curation prompt.
- Source interpretive context: per-source weighting statements loaded into agent system prompts.

Updated when sources change (media closures, government site restructuring, new outlets) — not on a weekly cycle.

### What Carries Week-over-Week Continuity

The global ledger is the sole cross-country continuity mechanism. It replaces the v3 feedback loop (executive questions steering desks). Instead of generating directed questions, the executive agent identifies dynamics with triage implications — which countries need attention and why. Triage reads these alongside wire scan results and makes contextually informed depth decisions.

Country ledgers carry per-country continuity. The posture summary and signal category assessments persist across weeks, allowing the country agent to measure change and the triage agent to assess whether new activity is significant.

No regional persistence exists. Regional synthesis runs stateless each week to avoid creating false analytical coherence around editorial groupings.

---

## 6. Country Ledger Schema

```json
{
  "country": "Mexico",
  "code": "mx",
  "tier": "periphery",
  "actors": [
    {"name": "Claudia Sheinbaum", "role": "President", "primary": true},
    {"name": "Juan Ramón de la Fuente", "role": "Foreign Minister (SRE)", "primary": false},
    {"name": "SEDENA", "role": "National Defense Secretariat", "primary": false}
  ],
  "last_updated": "2026-03-14",
  "created": "2026-03-01",

  "posture_summary": {
    "as_of": "2026-03-14",
    "text": "3-5 sentence analytical summary of current posture...",
    "category_status": {
      "alignment_diplomatic": "active | routine | quiet | escalating",
      "security_defense": "...",
      "economic_tech": "...",
      "institutional": "...",
      "domestic_regime": "..."
    },
    "last_deep_dive": "2026-03-14",
    "consecutive_maintenance_weeks": 0
  },

  "signal_categories": {
    "alignment_diplomatic": {
      "current_assessment": "Running analytical picture for this category...",
      "confidence": 4,
      "confidence_rationale": "Why this confidence level...",
      "key_actors": ["Sheinbaum", "de la Fuente", "SRE"],
      "dossier_sections_referenced": ["§14", "§17"],
      "last_updated": "2026-03-14"
    },
    "security_defense": { "..." : "same structure" },
    "economic_tech": { "..." : "same structure" },
    "institutional": { "..." : "same structure" },
    "domestic_regime": { "..." : "same structure" }
  },

  "weekly_entries": [
    {
      "week": "2026-03-14",
      "date_range": "2026-03-07 to 2026-03-14",
      "depth": "deep_dive | maintenance",
      "activity_level": {
        "rating": "high | moderate | low | quiet",
        "rationale": "Why this rating..."
      },
      "category_movements": {
        "alignment_diplomatic": {
          "movement": "significant | minor | none",
          "developments": [
            {
              "headline": "What happened",
              "date": "2026-03-14",
              "source": "Outlet name",
              "source_tier": 2,
              "source_url": "https://...",
              "summary": "Key details and context",
              "actors_involved": ["Sheinbaum"],
              "signal_category_relevance": "Why this matters for this category"
            }
          ],
          "prior_assessment": "What the desk believed before this week...",
          "updated_assessment": "What the desk believes now...",
          "confidence_change": {"from": 3, "to": 4, "reason": "..."}
        }
      },
      "unexpected_developments": [
        {
          "headline": "...",
          "date": "...",
          "source": "...",
          "source_tier": 2,
          "signal_category": "security_defense",
          "assessment": "Why this matters...",
          "disposition": "logged | elevated_to_category"
        }
      ],
      "absence_check": [
        {
          "expected": "What was expected to happen...",
          "signal_category": "security_defense",
          "occurred": false,
          "significance": "What the absence means...",
          "confidence": 2
        }
      ],
      "devils_advocate": {
        "challenges": ["Challenge 1...", "Challenge 2..."],
        "recommended_adjustments": ["Adjustment 1...", "Adjustment 2..."]
      },
      "self_corrections": [
        {
          "category": "domestic_regime",
          "prior_week": "2026-03-07",
          "original_claim": "What was previously assessed...",
          "correction": "What changed and why...",
          "root_cause": "Why the error occurred..."
        }
      ],
      "structural_claim_checks": [
        {
          "claim_ref": "STRUC-09-03",
          "claim_text": "The structural claim being tested...",
          "status": "confirmed | under_pressure | weakened | falsified",
          "evidence": "What evidence bears on this claim...",
          "confidence_in_claim": 3
        }
      ]
    }
  ],

  "structural_claim_status": [
    {
      "claim_ref": "STRUC-09-03",
      "claim_text": "...",
      "dossier_section": 9,
      "status": "confirmed | under_pressure | weakened | falsified",
      "last_checked": "2026-03-14",
      "evidence_summary": "...",
      "weeks_under_pressure": 0,
      "recommendation": "..."
    }
  ],

  "corrections_log": [
    {
      "correction_date": "2026-03-14",
      "original_week": "2026-03-07",
      "original_claim": "...",
      "corrected_to": "...",
      "category_affected": "domestic_regime",
      "root_cause": "..."
    }
  ],

  "consolidated_history": "Compressed summary of entries older than 8 weeks..."
}
```

### Country Ledger Rules

**Structure:**
- All five signal categories must exist at all times
- Every deep-dive weekly entry must have a movement assessment for all five categories (even if "none")
- Maintenance entries require only: depth flag, any wire/headline findings, posture summary update
- Confidence scores are 1-5 integers everywhere
- Source tiers are 1-4 integers everywhere

**Lifecycle:**
- `current_assessment` in signal_categories is overwritten on deep-dive weeks; prior version preserved in weekly entry's `prior_assessment` field
- Weekly entries are append-only — never modified after write
- Corrections log entries must have root cause
- Structural claim references must match dossier claim IDs
- Full entries retained for 8 recent weeks; older entries compressed into `consolidated_history`; originals archived to `ledgers/archive/{code}_weeks_N-M.json`

**Staleness:**
- `consecutive_maintenance_weeks` >= 4 should trigger a deep dive regardless of triage findings (prevent stale analysis)
- Structural claims with `status: falsified` trigger dossier refresh recommendation
- Devil's advocate section required for deep-dive entries, absent for maintenance entries

---

## 7. Global Ledger Schema

```json
{
  "last_updated": "2026-03-14",
  "created": "2026-03-01",

  "global_posture_summary": {
    "as_of": "2026-03-14",
    "text": "3-5 sentence summary of the global analytical environment...",
    "signal_environment": {
      "most_active_categories": ["alignment_diplomatic", "security_defense"],
      "quietest_categories": ["economic_tech"],
      "geographic_hotspots": ["frontline_eastern_europe", "americas"],
      "geographic_quiet_zones": ["asia_pacific"]
    }
  },

  "active_dynamics": [
    {
      "dynamic_id": 1,
      "title": "Descriptive title of the cross-country dynamic",
      "created_week": "2026-03-07",
      "last_updated": "2026-03-14",
      "status": "emerging | developing | established | monitoring | weakening | resolved",
      "current_assessment": "What the executive analyst currently believes about this dynamic...",
      "countries_involved": ["mx", "in", "fr"],
      "signal_categories_touched": ["alignment_diplomatic", "security_defense"],
      "evidence_strength": {
        "confidence": 3,
        "supporting_country_confidences": {"mx": 4, "in": 2, "fr": 4},
        "weakest_link": "What makes this assessment most vulnerable...",
        "linkage_type": "parallel_behavior | interaction_effect | institutional | absence",
        "linkage_assessment": "Why these events are connected beyond coincidence..."
      },
      "competing_interpretation": "Strongest alternative explanation...",
      "what_to_watch": "Leading indicators for next week...",
      "triage_implications": {
        "countries_to_flag": ["tr", "br", "id"],
        "reason": "Why triage should consider flagging these countries..."
      },
      "weeks_active": 2,
      "consecutive_unchanged_weeks": 0
    }
  ],

  "watchlist": [
    {
      "item": "Description of what to watch...",
      "signal_category": "security_defense",
      "countries": ["fr", "de"],
      "why_it_matters": "Why this is worth tracking...",
      "trigger": "What event or threshold would elevate this...",
      "added_week": "2026-03-14"
    }
  ],

  "weekly_entries": [
    {
      "week": "2026-03-14",
      "executive_briefing_items": [
        {
          "title": "Theme title for newsletter lead",
          "regions_involved": ["americas", "western_europe"],
          "what": "What is happening (2-3 sentences)...",
          "why_it_matters": "Strategic significance (2-3 sentences)...",
          "what_to_watch": "Leading indicators...",
          "confidence": 3,
          "confidence_note": "Why this confidence, what's the weakest link..."
        }
      ],
      "dynamics_created": [2],
      "dynamics_updated": [1],
      "dynamics_archived": [],
      "items_considered_rejected": [
        {
          "candidate": "Pattern that was considered...",
          "reason_rejected": "Why it doesn't rise to executive-level significance..."
        }
      ],
      "self_corrections": [
        {
          "dynamic_id": 1,
          "prior_assessment": "What was previously believed...",
          "correction": "What changed...",
          "root_cause": "Why the error occurred..."
        }
      ]
    }
  ],

  "archived_dynamics": [],
  "consolidated_history": "Compressed summary of entries older than 8 weeks..."
}
```

### Global Ledger Rules

- Single writer: only the executive agent writes to this ledger
- Dynamic IDs unique within the ledger
- `items_considered_rejected` must not be empty (forces critical evaluation)
- `triage_implications` country codes must be valid
- `consecutive_unchanged_weeks` >= 3 should prompt the executive agent to update, downgrade, or archive the dynamic
- Confidence inheritance: dynamic confidence cannot exceed the lowest supporting country confidence
- 8-week retention for full weekly entries; older entries compressed

---

## 8. CountryConfig Schema

Each country carries configuration that drives the pipeline. Populated from three sources: dossier §0 extraction (actors), Source Intelligence Map curation prompt (Goggle file + query vocabulary), and Government Sources curation prompt (government domain config).

```yaml
country: Mexico
code: mx
tier: periphery
region: americas

actors:
  - name: Claudia Sheinbaum
    role: President
    primary: true
    search_terms: ["Sheinbaum", "Claudia Sheinbaum"]
  - name: Juan Ramón de la Fuente
    role: Foreign Minister (SRE)
    primary: false
    search_terms: ["de la Fuente", "Juan Ramón de la Fuente"]
  - name: SEDENA
    role: National Defense Secretariat
    primary: false
    search_terms: ["SEDENA", "Secretaría de la Defensa Nacional"]
  - name: SEMAR
    role: Navy Secretariat
    primary: false
    search_terms: ["SEMAR", "Secretaría de Marina"]
  - name: SRE
    role: Foreign Affairs Secretariat
    primary: false
    search_terms: ["SRE", "Secretaría de Relaciones Exteriores"]
  - name: Banxico
    role: Central Bank
    primary: false
    search_terms: ["Banxico", "Banco de México"]
  - name: Morena
    role: Governing party
    primary: false
    search_terms: ["Morena"]

languages:
  primary: es
  additional: []
  metadata: en

# Layer 1: News Discovery (Brave Search + Goggles)
news_discovery:
  goggle_file: goggles/mx.goggle
  extraction_config: extraction/mx.yaml
  brave_params:
    country: MX
    search_lang: es
    freshness: pw
  query_vocabulary:
    diplomatic_alignment:
      - "relaciones bilaterales"
      - "acuerdo diplomático"
      - "cancillería"
      - "cumbre bilateral"
      - "embajador"
    security_defense:
      - "SEDENA"
      - "adquisición militar"
      - "cooperación en seguridad"
      - "Guardia Nacional"
      - "despliegue militar"
    economic_tech:
      - "inversión extranjera"
      - "tratado comercial"
      - "Banxico"
      - "nearshoring"
      - "minerales críticos"
    institutional:
      - "OEA"
      - "Naciones Unidas"
      - "G20"
      - "ratificación tratado"
    domestic_constraints:
      - "reforma constitucional"
      - "coalición legislativa"
      - "Morena"
      - "oposición"
      - "Diputados"

# Layer 2: Government Source Discovery (SearchAPI + Google)
government_discovery:
  config_file: government/mx.yaml

# Source interpretive context (loaded into agent prompts)
interpretive_context_file: context/mx_sources.md

blind_spots:
  - domain: Defense procurement
    reason: No dedicated defense press; SEDENA/SEMAR communicate through controlled bulletins only
    where_signal_lives: SEDENA/SEMAR official bulletins, leaked documents in Proceso or Animal Político
  - domain: Real-time security
    reason: Telegram/WhatsApp channels precede news coverage but are not ingestible
    where_signal_lives: Local journalists who monitor these channels; downstream reporting lag of 12-48 hours
  - domain: Legislative proceedings
    reason: Committee testimony not covered by media
    where_signal_lives: gob.mx portals, Senate/Chamber of Deputies websites

search:
  triage_queries_max: 3      # wire + domestic headline checks during triage
  deep_dive_queries_max: 20  # full Brave News API queries during deep dive
```

The Goggle file, government domain config, and interpretive context file are generated by their respective curation prompts and stored as separate files referenced by the config. They are not embedded in the YAML — they're too large and have independent update cycles. The extraction routing table (`extraction/routing.yaml`) is global, not per-country — it maps domains to extraction methods based on empirical testing across all sources.

---

## 9. Triage Design

### Inputs

Per country:
- Wire scan results: headlines from Reuters, AP, AFP via Brave News API (past 7 days)
- Lightweight domestic check: 1-2 Brave News API queries with country Goggle applied, headlines and snippets only
- Government source findings: structured output from the government source agent (Step 0.5) — ground truth and intent signal items, or "no new content" for quiet sources
- Country posture summary from ledger (compact: text + category_status + consecutive_maintenance_weeks)

Global context:
- Global ledger `global_posture_summary`
- Global ledger `active_dynamics` — specifically the `triage_implications` fields

### Output

```json
{
  "triage_date": "2026-03-14",
  "decisions": [
    {
      "country": "mx",
      "depth": "deep_dive",
      "rationale": "Wire coverage shows Sheinbaum-Trump military intervention confrontation. Alignment_diplomatic was already active; this represents potential escalation. Multiple wire sources (Reuters, AP) corroborate.",
      "triggered_by": ["wire_coverage", "category_escalation"],
      "signal_categories_flagged": ["alignment_diplomatic"]
    },
    {
      "country": "ee",
      "depth": "maintenance",
      "rationale": "No wire mentions. No domestic headline activity. Last deep dive was 2 weeks ago. No global ledger triage implications reference Estonia.",
      "triggered_by": []
    },
    {
      "country": "tw",
      "depth": "deep_dive",
      "rationale": "No wire mentions, but global ledger dynamic #2 (semiconductor supply chain absence) specifically flags Taiwan for investigation. Absence may be analytically significant given approaching CHIPS Act review deadline.",
      "triggered_by": ["global_ledger_implication"],
      "signal_categories_flagged": ["economic_tech"]
    }
  ]
}
```

### Triage Decision Criteria

Flag for **deep dive** when any of:
- Wire or domestic headlines show a development that could change posture in any signal category
- Wire or domestic coverage contradicts the current posture summary
- Government source findings include significant ground truth items (treaty signed, procurement announced, forces deployed, legislation enacted) — the pipeline may be ahead of media coverage
- Government source findings show unexpected silence from a P1 source (foreign ministry or defense ministry not publishing during an active period)
- Expected activity is absent and the absence is analytically significant
- Global ledger `triage_implications` flag this country
- `consecutive_maintenance_weeks` >= 4 (staleness override — force a deep dive to refresh analysis)

Flag for **maintenance** when:
- Coverage shows only routine activity consistent with posture summary
- Government sources show only routine publications or expected silence
- No wire or domestic mentions and no global ledger flags
- Last deep dive was recent and no intervening changes

### Triage Cost

28 countries × (wire scan + 1-2 domestic queries via Brave News API) + government source findings from Layer 2 (SearchAPI queries against government domains). Brave News API costs vary by plan. SearchAPI costs are per-query. The return is avoiding ~16-20 full deep-dive cycles that would cost significantly more.

---

## 10. Agent Responsibilities

### Government Source Agent (New in v4.1)

**Input:** Layer 2 content (government publications discovered via SearchAPI and extracted through the tiered extraction chain) + source intelligence map (government section) + country dossier (reference).

**Task:** For each new government publication: classify as ground truth, intent signal, or both. Tag with signal categories. Extract analytical essentials — what happened, structural significance, framing note, cross-reference suggestion. Note when SearchAPI returned no results for government domains that normally produce weekly content.

**Output:** Structured JSON per country with findings and any discovery gaps. Feeds triage and country agent.

**Does not:** Assess posture change (country agent's job). Search for additional context. Compare to the ledger. Run for a subset of countries — processes whatever Layer 2 discovered.

**Runs:** Every week for all 28 countries, before triage. Lightweight for quiet countries (mostly "no new content" entries).

### Triage Agent

**Input:** Wire results + domestic headline check (Layer 1) + government source findings (Layer 2) + 28 country posture summaries + global ledger context.

**Task:** For each country, decide deep dive or maintenance. Output structured JSON with rationale.

**Does not:** Search for articles, read dossiers, update ledgers, or make analytical assessments.

### Country Agent (Deep Dive)

**Input:** Layer 1 news results (Brave Search articles, ranked by Goggle priority) + Layer 2 government findings (structured output from government source agent) + country dossier (full) + country ledger (full) + source interpretive context.

**Task:** Read pre-collected material from both layers. Analyze findings across all five signal categories. Layer 2 provides ground truth (what the government did); Layer 1 provides media coverage (how it was received, contested, contextualized). When both layers cover the same event, use Layer 2 for what happened and Layer 1 for domestic reception. Produce structured country analysis with evidence, confidence scoring (1-5), source tiering (1-4), absence checks, self-corrections, and structural claim checks. Update signal category assessments and posture summary.

**Output:** Weekly entry for the country ledger + updated signal_categories + updated posture_summary.

**Does not:** Run searches or fetch articles — all collection is done by Layers 1 and 2 before the country agent runs. Does not make cross-country comparisons, update the global ledger, or access other countries' data.

### Devil's Advocate (Separate Call, Deep Dive Only)

**Input:** The country agent's weekly entry (before ledger write).

**Task:** Argue against each assessment. Generate the strongest competing explanation. Flag single-source dependencies and government-messaging-only evidence. Identify assessments that persist from ease of sourcing rather than analytical importance. Check whether the country agent appropriately distinguished between government framing (intent signals from Layer 2) and independently verified facts — if an assessment rests primarily on government source content without Layer 1 media corroboration, that's a challenge.

**Output:** `devils_advocate` section appended to the weekly entry.

**Does not:** Run searches, update assessments, or override the country agent. Its output is advisory — it becomes part of the record but doesn't automatically change confidence scores.

### Regional Synthesis Agent (Stateless)

**Input:** Country analyses for constituent countries in the region. No regional ledger, no prior regional state.

**Task:** Identify cross-country patterns visible only when reading reports together. Focus on: parallel behavior (coordination vs. contagion vs. coincidence), interaction effects (Country A's action creating consequences in Country B), institutional dynamics, contradictions between stated and observed positions, and gaps (expected dynamics not appearing).

**Output:** Regional report with cross-cutting dynamics, confidence inheritance from country-level data, apophenia safeguards (evidence against linkage, linkage strength rating, rejection log of considered-and-dismissed patterns).

**Does not:** Re-analyze source material, access country ledgers, or maintain state across weeks. Works exclusively from the structured country analyses provided.

**Safeguards:**
- Confidence inheritance: regional claims cannot exceed the lowest confidence of their supporting country data
- Low-confidence quarantine: country assessments scored 1-2 listed separately, not synthesized into dynamics
- Rejection log required — an empty rejection log suggests insufficient critical evaluation

### Executive Agent

**Input:** 5 regional reports + global ledger (prior state).

**Task:** Identify 3-5 developments, patterns, or structural shifts visible only at the global level. Update the global ledger: create/update/archive dynamics, update watchlist, write weekly entry with briefing items and rejection log. Generate triage implications for next week's cycle.

**Output:** Updated global ledger (including executive briefing items that flow to newsletter) + triage implications embedded in active dynamics.

**Does not:** Run searches, modify country ledgers, or access source material.

### Newsletter Assembly (Deterministic, No LLM)

**Input:** All structured JSON outputs — executive briefing items, regional reports, country analyses, watchlist.

**Task:** Assemble newsletter from structured data into the publication template. Mechanical formatting only — no summarization, no editorial judgment.

**Output:** `newsletter.md`

---

## 11. Newsletter Structure

```markdown
# The Middle Powers Monitor
## Week of [date range]

### Executive Brief
[800-1200 words. Rendered from executive_briefing_items in
global ledger weekly entry. Convert each item into 2-3
narrative paragraphs. This is the lead section and the
reason people subscribe.]

---

### The Americas
[Regional lead: rendered from americas regional report.
Convert cross_cutting_dynamics into 2-3 narrative paragraphs.]

#### Canada
[From country analysis: 1-paragraph summary from posture
summary + key developments as brief items + "Between the
Lines" analytical note from devil's advocate challenges]

#### Mexico
[Same format]

#### Brazil
[Same format]

#### Chile
[Same format]

---

### Western Europe
[Regional lead]
#### France / Germany / UK / Italy / Spain / Norway / Sweden

---

### Frontline & Eastern Europe
[Regional lead]
#### Ukraine / Poland / Finland / Estonia / Lithuania /
Latvia / Czech Republic / Romania

---

### Middle East, Turkey & South Asia
[Regional lead]
#### Turkey / Saudi Arabia / UAE / India

---

### Asia-Pacific
[Regional lead]
#### Taiwan / Japan / South Korea / Australia / Indonesia

---

### Watchlist
[Pulled from global ledger watchlist. Items worth tracking
that didn't make the executive briefing. Formatted as
brief items with trigger conditions.]
```

**Editorial tone:** Analytical narrative with structural depth, not bullet-point briefing. Closer to The Economist's "World This Week" — authoritative but engaging, structurally informed but readable. State uncertainty where it exists without apologizing for it. The reader is a sophisticated generalist who wants to understand how the world is changing, not just what happened.

**Maintenance countries** get a shorter entry: posture summary + "No significant developments this week" or brief note on wire findings. They don't get "Between the Lines" or detailed development items.

---

## 12. Source Reliability Framework

### Source Tiers

- **Tier 1:** Official government statements, court filings, regulatory documents. High reliability, low independence. Government messaging alone caps confidence at 2.
- **Tier 2:** Major wire services (Reuters, AP, AFP) and newspapers of record (El Universal, Reforma, Le Monde, etc.)
- **Tier 3:** Regional press, specialist outlets, investigative journalism platforms
- **Tier 4:** Opinion, commentary, social media, anonymous sourcing

### Confidence Scale

- **5:** Multiple independent Tier 1-2 sources corroborate, no significant counter-evidence
- **4:** 2+ independent sources, minor gaps
- **3:** Single strong source, or multiple sources with caveats
- **2:** Single source, government messaging only, or indirect evidence
- **1:** Speculative, inferred from absence, or based on opinion/commentary only

Confidence scores travel upward through the pipeline. Regional claims cannot exceed the lowest confidence of their supporting country data. Executive themes carry full provenance to the lowest supporting country confidence.

---

## 13. Ledger Initialization

### Cold Start (New Country)

**Step 1 — Mechanical extraction (no API call):** Script reads CountryConfig and populates structural fields: country, code, tier, actors. Initializes weekly_entries, corrections_log as empty. Extracts structural claim IDs from dossier to seed `structural_claim_status` with all claims set to `confirmed`.

**Step 2 — Initialization call (one API call):** LLM reads the country dossier and produces the initial posture summary and five signal category `current_assessment` fields. This is a structural baseline, not a news sweep. All initial confidence scores tagged as `baseline` or set to 3.

**Step 3 — First cycle:** Mandatory deep dive regardless of triage (no prior posture summary to evaluate against). After first cycle, the country enters normal triage rotation.

### Global Ledger Initialization

Created empty with no active dynamics or watchlist items. The first executive synthesis cycle populates it. Triage runs without global ledger input on the first cycle.

---

## 14. Consolidation and Maintenance

### Country Ledger Consolidation

- Full weekly entries retained for 8 most recent weeks
- Entries older than 8 weeks compressed into `consolidated_history` by a separate LLM call that preserves: category assessment changes, corrections, structural claim status changes, and executive-relevant findings
- Compression discards: individual article references, full development details, source URLs
- Original entries archived to `ledgers/archive/{code}_weeks_N-M.json`
- Triggered automatically when entry count exceeds retention window (not a manual cron job)

### Global Ledger Consolidation

Same 8-week retention. Archived dynamics preserved in `archived_dynamics` array. Weekly entries older than 8 weeks compressed. The global posture summary and active dynamics are always current.

### Dossier Refresh

Triggered by structural claim status. When a country ledger shows multiple claims as `weakened` or `falsified`, the quarterly human review should prioritize that country for dossier regeneration. This is the one essential human gate — everything else is automated.

---

## 15. Operational Considerations

### Concurrency and Rate Limiting

Layer 2 (government source discovery via SearchAPI) runs first — 28 countries × 2-5 site-scoped queries each. Then extraction runs for discovered URLs. Then government source agent processes results. Then triage runs with Layer 2 findings as input. Then Layer 1 (Brave News API) queries run for deep-dive countries with extraction. Then country agents run in parallel. Use semaphores to limit concurrent API calls based on Brave, SearchAPI, and Anthropic tier limits. Exponential backoff with jitter for rate limit errors.

### Failure Handling

- If Layer 2 (SearchAPI) fails for a country, the government source agent logs the gap. Country agent proceeds with Layer 1 data only, with a note that government source coverage is incomplete this week.
- If Layer 2 returns no results for a government domain, this is logged but is not necessarily an error — some government institutions publish infrequently.
- If Layer 1 (Brave) fails for a country, the country agent works from Layer 2 government findings only, with forced lower confidence on media-dependent assessments.
- If triage fails for a country, default to maintenance (safe — missed deep dive is better than pipeline crash)
- If a country agent fails after retries, quarantine that country, log failure, proceed with remaining countries for regional synthesis
- If regional synthesis fails, the executive agent works from available regional reports + raw country analyses for the missing region
- If the executive agent fails, newsletter assembles from regional and country outputs only, with a note that the executive brief is unavailable
- Devil's advocate failure is non-blocking — the weekly entry gets written without the adversarial section, flagged for human review
- Government source agent failure for a country is non-blocking — triage and country agent proceed with Layer 1 data only

### Extraction Brittleness

Both layers use the same tiered extraction chain, dispatched via a static routing table based on empirical testing (377 domains tested, 4 methods each). The routing table assigns each domain to its known-best extraction method:

- **curl + trafilatura** is the dominant method — resolves 80% of domains where Claude fails, at 81% URL-level success rate
- **Claude web_fetch** works for 51% of all domains as primary
- **Diffbot** is uniquely effective for 12 domains (institutional sites, some Arabic outlets, reuters.com partially)
- **Playwright** is uniquely effective for 18 domains (JS-rendered government sites, intelligence outlets, some paywalled publications)

When the pre-assigned method fails, the pipeline tries fallback methods per the routing table. When all methods fail, the article is processed from headline + snippet only, with any relying assessment capped at confidence 2. Extraction failures are logged per-domain to trigger routing table updates when success rates degrade.

Six domains are completely unretrievable across all methods (dgap.org, liberation.fr, mnd.gov.tw, mod.go.jp, spf.org, wam.ae). These go to snippet-only by default.

### Context Window Management

The country agent's deep-dive call is the heaviest: full dossier + full ledger + Layer 1 results + Layer 2 findings + interpretive context. The two-layer collection model increases input size compared to v4 (where the agent searched and therefore controlled what it saw). Monitor token counts. If input exceeds limits:
- Truncate Layer 1 results to top N articles (Goggle ranking ensures highest-priority sources survive truncation)
- Serve truncated ledger (posture summary + signal categories + last 4 weekly entries + consolidated history)
- Layer 2 findings are compact and should not need truncation

### Model Selection

`claude-sonnet-4-20250514` for all agents. Government source agent and triage are lightweight calls well-suited to Sonnet. Country agent and executive agent are heavier but Sonnet handles the analytical work. If executive synthesis quality proves insufficient, that single call can be upgraded to Opus.

---

## 16. Cost Estimation

| Component | Per-week estimate |
|-----------|------------------|
| Layer 2: Government source discovery (SearchAPI queries) | ~$2-4 |
| Government source agent (28 countries × lightweight LLM call) | ~$1-2 |
| Triage (28 wire scans + domestic checks via Brave + LLM triage call) | ~$2-4 |
| Layer 1 discovery: Brave News API (deep-dive queries, ~10 countries × 15-20 queries) | ~$5-15 (depends on Brave plan) |
| Layer 1 extraction: Diffbot calls (Tier 3 fallback, ~30-50 articles/week) | ~$3-5 |
| Layer 1 extraction: Claude web_fetch, Playwright, Publisher APIs | ~$0-2 (mostly infrastructure) |
| Deep-dive country agents (10 avg × analysis call) | ~$8-15 |
| Devil's advocate (10 separate calls) | ~$2-4 |
| Maintenance updates (18 avg × light processing) | ~$1-2 |
| Regional synthesis (5 calls) | ~$2-3 |
| Executive synthesis (1 call) | ~$1-2 |
| Consolidation (amortized) | ~$0.50 |
| **Total** | **~$26-55/week** |
| **Annual** | **~$1,350-2,850/year** |

Layer 2 costs are SearchAPI per-query charges for government domain searches. Brave News API pricing depends on plan tier. Estimates assume Sonnet pricing for all LLM calls. First few weeks of production will calibrate these numbers.

---

## 17. Implementation Order

1. **Project scaffolding:** directories, config loading, JSON schema validation
2. **CountryConfig for Mexico:** actor extraction from dossier §0, Goggle file from source curation prompt, government domain config from government sources prompt
3. **Country ledger schema:** Pydantic models, validation, read/write operations
4. **Global ledger schema:** Pydantic models, validation, read/write operations
5. **Ledger initialization:** mechanical extraction + initialization call
6. **Layer 2 integration:** SearchAPI client with site-scoped government domain queries for Mexico
7. **Government source agent:** prompt, output schema, processing pipeline
8. **Layer 1 integration:** Brave News API client with Goggle support, query construction with localized vocabulary
9. **Extraction tier chain:** curl+trafilatura integration, Claude web_fetch integration, Diffbot Article API client, Playwright extraction, Publisher API clients (Guardian, FT, others as identified). Static routing table from empirical test data.
10. **Triage agent:** prompt, output schema, three-input triage (wire + domestic + gov findings)
11. **Country agent (deep dive):** prompt, output schema, two-layer input handling
12. **Devil's advocate:** prompt, output schema
13. **Country desk orchestrator:** Layer 2 → gov source agent → triage → Layer 1 + extraction → country agent → devil's advocate → ledger write
14. **Regional synthesis:** prompt, output schema, stateless cross-country analysis
15. **Executive agent:** prompt, output schema, global ledger read/write
16. **Newsletter assembly:** deterministic Markdown rendering from structured outputs
17. **CLI interface:** `--all`, `--country`, `--region`, `--triage-only`, `--assemble`, `--dry-run`
18. **Error handling:** retries, quarantine, graceful degradation per layer
19. **Consolidation:** ledger compression routine with archival
20. **End-to-end test with Mexico:** 2 consecutive simulated weekly cycles covering both layers + extraction
21. **Source curation for remaining 27 countries:** Goggle files + government domain configs
22. **CountryConfig for remaining 27 countries:** actor extraction + config assembly
23. **Full 28-country integration test**

**Critical path:** Steps 1-20 with Mexico only. Do not attempt multi-country before the single-country pipeline is validated end-to-end across two consecutive cycles, including both collection layers and the extraction tier chain.

---

## 18. What Was Dropped

These components from the current system and prior proposals are explicitly not part of this architecture:

- **ML pipeline:** E5 embeddings, HDBSCAN clustering, sentence-transformers, scipy, numpy
- **SearchAPI as primary news discovery:** Replaced by Brave Search News API with Goggles (Layer 1). SearchAPI retained for Layer 2 government domain queries only.
- **Diffbot as primary discovery/NLP tool:** Retained as Tier 3 extraction method for articles with complex layouts. No longer used for entity extraction or NLP — the LLM handles analysis.
- **Claude's web_search in the country agent:** The country agent no longer runs searches — discovery is handled by Brave (Layer 1) and SearchAPI (Layer 2). Claude's web_fetch is retained as Tier 2 extraction for clean HTML articles.
- **Playwright for news articles:** Retained as Tier 4 extraction fallback for JS-rendered pages across both layers.
- **RSS polling infrastructure:** Eliminated. Government source discovery uses SearchAPI + Google indexing instead of direct RSS feed monitoring.
- **Government monitoring manifests (complex YAML):** Replaced by simple government domain configs listing institutional domains and query terms for SearchAPI.
- **Paragon taxonomy:** Event type / leader role / impact level classification system
- **Dynamic thread lifecycle:** Thread creation, naming, hypothesis/disconfirmation, staleness detection, retirement
- **Regional ledgers:** Regional synthesis is stateless
- **v3 feedback loop:** Executive questions replaced by global ledger triage implications
- **GlobalPulse agent:** Top-down global context pre-pass eliminated
- **Per-leader unit of analysis:** Country replaces leader as the organizing principle
- **Running Analytical Picture (markdown format):** Replaced by country ledger (JSON)
- **Hypothesis-driven thread framing:** Replaced by five fixed signal categories with running assessments
- **LLM-driven newsletter rendering:** Replaced by deterministic assembly

---

## 19. What Remains to Design

- **Agent prompt revisions:** Country agent prompt needs revision to remove search instructions and add two-layer input handling. Triage prompt needs revision to include Layer 2 findings. Devil's advocate prompt needs government framing check added. (Prompts exist from v4 but need targeted updates for v4.1.)
- **Regional framework documents:** Analytical frameworks for each of five editorial regions. (Complete — five frameworks exist.)
- **Newsletter assembly logic:** Deterministic rendering rules. (Complete — assembly spec exists.)
- **Source curation execution:** Run source curation prompt v2 and government sources prompt for all 28 countries to generate Goggle files and government domain configs.
- **Extraction tier chain implementation:** curl+trafilatura integration, Claude web_fetch integration, Diffbot Article API client, Playwright extraction runners, Publisher API clients. Static routing table based on empirical test data (377 domains tested).
- **SearchAPI integration for Layer 2:** Client for site-scoped Google queries against government domains. Narrow role — government discovery only.
- **Brave Search API integration:** Client library, Goggle loading, query construction with localized vocabulary.
- **Observability:** Logging, monitoring, and alerting for both collection layers and all agent calls.

---

## 20. Key Principles

These emerged from the design process and should govern implementation decisions:

- **Collection and analysis are separated.** Layer 1 (Brave + Goggles) and Layer 2 (government monitoring) handle collection. The country agent handles analysis. This mirrors how actual intelligence organizations operate and prevents the analyst from shaping what it sees.
- **Government sources are primary evidence; media sources are secondary.** Layer 2 tells the pipeline what the government did. Layer 1 tells the pipeline how it was received. The country agent needs both to produce grounded analysis.
- **The wire scan decides what matters, not configuration.** No static assumptions about which countries are important. Every week starts fresh, informed by the global ledger and government source findings.
- **Signal categories are an analytical lens, not a collection mechanism.** The five categories organize assessment, not collection. Collection is organized by source type (news vs. government) and source priority (Goggle tiers).
- **The dossier is the localization layer.** No manual vocabulary porting, no per-country query dictionaries. The dossier and source intelligence map provide the structural context that makes collection meaningful.
- **Budget should correlate with activity.** You spend more when more is happening. The triage architecture achieves this naturally for Layer 1. Layer 2 runs unconditionally but is cheap (SearchAPI queries against government domains).
- **Events over coverage.** The goal is reporting what leaders and institutions actually did, not how journalists framed it. Layer 2 ensures the pipeline sees primary evidence even when media doesn't cover it.
- **Multilingual sourcing is non-negotiable.** English-only sources systematically miss domestic stories and misclassify actor roles. Brave's language parameters and per-country Goggles ensure domestic-language sources surface.
- **Bottom-up over top-down.** Government monitoring and news discovery feed country agents. Country agents feed regional synthesis. Regional synthesis feeds the executive agent. The newsletter assembles. No single layer imposes a frame on the layers below it — except the global ledger, which gently steers attention through triage implications.
