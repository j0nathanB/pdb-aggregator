# Source Intelligence Map — Curation Prompt v2 (Brave Native)

## Usage

Replace `{{COUNTRY}}` and `{{LANGUAGE}}` with the target country and its primary language of political discourse. Run in Claude Research mode (Opus), one country at a time. For countries where political discourse operates in multiple languages (e.g., Ukraine: Ukrainian + Russian; Finland: Finnish + Swedish; Canada: English + French), note this in the `{{LANGUAGE}}` field and the prompt will handle it.

Expected runtime: one pass per country. Unlike the structural dossier, this does not require multi-pass generation.

### Changes from v1

This prompt replaces the Google News API hard-filter model with the **Brave Search News API + Goggles** architecture. Key differences:
- Sources are no longer binary include/exclude. Each source receives a **boost tier** that determines ranking priority.
- Source count is no longer constrained by API cost — boost rules don't add API calls.
- The output includes a **ready-to-use Goggle file** and **pipeline interpretive context** alongside the source assessment.
- **Notable Exclusions** are replaced by a **Discard List** (actively removed from results) and sources that simply don't earn a boost are left at organic ranking.

---

## Prompt

You are producing a **Source Intelligence Map** for **{{COUNTRY}}** (primary language of political discourse: **{{LANGUAGE}}**).

### Purpose

This document will be used to build a curated source-ranking overlay (a "Goggle") for an automated OSINT pipeline. The pipeline monitors how democratic middle powers are positioning themselves in the current international environment — tracking state posture across diplomatic alignment, defense/security autonomy, economic/technological statecraft, institutional engagement, and domestic political constraints on external action.

The pipeline uses the **Brave Search News API** with per-country Goggles applied. Instead of querying individual sources, the pipeline runs **topic-based queries** (e.g., leader name + policy topic) through the News API with:
- `country` and `search_lang` parameters to localize results
- `freshness=pw` (past week) for weekly pipeline cycles
- A country-specific Goggle that boosts high-signal sources and discards known noise

**How Goggles work:** A Goggle is a ranking overlay that re-orders search results. Sources with `$boost=3` surface first; `$boost=2` surface prominently; `$boost=1` surface when relevant. Sources with no rule appear at organic ranking — they can still surface if Brave ranks them highly for a specific query. Sources with `$discard` are actively removed from results.

This means **source count does not drive API cost**. Whether the Goggle contains 12 or 30 boost rules, the pipeline runs the same number of queries. Your job is to identify every source worth boosting and assign the right priority — not to minimize the list.

### What You Are Producing

You are identifying the sources that would allow an analyst to detect meaningful changes in this country's strategic posture, **ranked by priority**. The ranking determines which sources the pipeline sees first when multiple outlets cover the same event. You are also identifying noise sources that should be actively removed from results.

The five analytical domains:

1. **Diplomatic alignment** — who the state is moving toward or away from (summits, bilateral agreements, multilateral engagement)
2. **Security & defense autonomy** — how the state secures itself physically (procurement, exercises, basing, doctrine)
3. **Economic & technological statecraft** — how the state positions itself economically (trade deals, FDI screening, critical minerals, tech partnerships, currency diversification)
4. **Institutional engagement** — how the state relates to multilateral architecture (UN, regional bodies, international courts, new institutional alternatives)
5. **Domestic constraints on external action** — what internal dynamics enable or limit the state's external positioning (parliamentary opposition, coalition politics, public opinion, elite factionalism, economic pressure)

### Source Selection & Tiering Criteria

For each source you recommend, apply these filters first, then assign a boost tier:

**Include and boost if:**
- The outlet regularly publishes original reporting (not aggregation or syndication) on at least one of the five domains above
- The outlet is read by or influences the country's policy-making class, foreign policy establishment, or defense/security community
- The outlet provides a distinct analytical perspective not redundant with other recommended sources (editorial diversity matters)
- The outlet publishes in {{LANGUAGE}} or English (or both)
- The outlet serves a structural signaling function — even government-aligned outlets earn boost if they're the channel through which the government signals policy intent

**Leave at organic ranking (no Goggle rule) if:**
- The outlet publishes some relevant content but is largely redundant with a boosted source
- The outlet is competent but doesn't produce enough original reporting to justify prioritizing it over other sources in the top 20 results
- The outlet was considered but doesn't meet the threshold for boost — it's not harmful, just not worth pushing to the top

**Discard if:**
- The outlet is primarily entertainment, lifestyle, sports, or tabloid with sensationalized political coverage that would displace higher-value results
- The outlet is a content farm or pure aggregator that republishes wire copy without adding value
- The outlet has known patterns of misinformation that would degrade pipeline analysis
- The outlet's presence in results would consistently waste a slot that a boosted source should fill

**Do NOT discard if:**
- The outlet is merely mediocre — leave it at organic ranking
- The outlet is government-aligned — boost it with a clear flag, don't discard it
- The outlet is a personal blog or Substack — these won't typically appear in Brave News Search results, so discarding them is unnecessary

### Boost Weight Scale

| Weight | Goggle rule | Meaning | Criteria |
|--------|-------------|---------|----------|
| **Tier 1** | `$boost=3` | Essential — surface first | Produces original reporting in ≥2 analytical domains; unique structural role (paper of record, government gazette, top defence/security outlet); content regularly unavailable elsewhere |
| **Tier 2** | `$boost=2` | Important — surface prominently | Strong on 1–2 specific domains; fills a distinct editorial lens (opposition voice, investigative, specialist); not fully redundant with any Tier 1 source |
| **Tier 3** | `$boost=1` | Supplementary — surface when relevant | Useful perspective or domain niche; some overlap with higher-tier sources but adds interpretive diversity or occasional unique reporting |

**Tier calibration guidance:**
- Aim for **3–5 Tier 1 sources** per country. These are the outlets an analyst would check first every morning. If you have more than 5, you're diluting what "essential" means.
- Aim for **4–8 Tier 2 sources**. These fill specific domain or editorial niches.
- **Tier 3 is uncapped** but should be used with intention. Every Tier 3 source should have a clear reason it isn't just left at organic ranking.
- Total boosted sources will typically fall in the **12–25 range** depending on media ecosystem density. A country like the UK or France will land higher; Estonia or Latvia will land lower.

### Output Structure

Produce the following for **{{COUNTRY}}**:

---

#### MEDIA LANDSCAPE SUMMARY

In 3–5 sentences, describe the structure of this country's media environment as it relates to foreign/security policy coverage. Address: concentration of ownership, degree of press independence, whether foreign/security policy is primarily covered by generalist outlets or specialist press, and any significant recent changes (closures, ownership transfers, government crackdowns) that affect the source landscape. Note which language(s) political discourse primarily operates in, and whether English-language domestic outlets exist with meaningful original reporting.

---

#### RECOMMENDED SOURCES

For each source, provide:

| Field | Description |
|---|---|
| **Name** | Outlet name as commonly referenced |
| **Domain** | Primary web domain (e.g., `lemonde.fr`) |
| **Language** | Primary publication language |
| **Type** | One of: `paper_of_record`, `business_financial`, `security_defense`, `political_specialist`, `opposition_aligned`, `government_aligned`, `regional`, `investigative`, `legislative_official`, `wire`, `think_tank` |
| **Boost Tier** | `Tier 1`, `Tier 2`, or `Tier 3` — with the corresponding Goggle rule (`$boost=3`, `$boost=2`, `$boost=1`) |
| **Domain Coverage** | Which of the 5 signal domains this outlet most reliably covers. List 1–3. |
| **Editorial Orientation** | 1–2 sentences: ownership, political lean, known biases, relationship to government. Be specific — "center-left" is less useful than "owned by [X], editorially critical of current government's NATO spending commitments, historically aligned with [party/faction]." |
| **Why This Source / Why This Tier** | 1–2 sentences: what analytical gap does this outlet fill that no other recommended source covers? Why does it earn this specific tier rather than one higher or lower? |
| **Access Notes** | Known paywall status (hard paywall, metered, free). Note: under the Goggle model, hard paywalls affect *extraction* (Diffbot may not get full text) but not *discovery* (Brave indexes paywalled content). Mark extraction-problematic sources with `[EXTRACTION FLAG]`. Mark uncertain status with `[VERIFY]`. |

**Composition guidance:** Aim for approximately:
- 2–3 papers of record (Tier 1–2)
- 1–2 business/financial outlets (Tier 2)
- 1–2 security/defense outlets or beats (Tier 1–2 if dedicated defense press exists; note which generalist outlets partially fill this if not)
- 1–2 political specialist or investigative outlets (Tier 2–3)
- 1–2 outlets representing opposition or minority political perspectives (Tier 2–3 — the pipeline needs domestic contestation)
- 1–2 regional or specialist international outlets with original analysis (Tier 2–3)
- 1 government-affiliated or official source for policy announcements, legislative records, or defense procurement notices (Tier 1–2, flagged clearly as government-aligned)
- 1 think tank or analytical outlet providing structural depth (Tier 2–3)
- 1 wire service with a strong local bureau (Tier 2–3 — provides baseline event coverage)

If a category doesn't apply (e.g., no dedicated defense press exists), note the gap and explain which generalist outlets partially fill it.

---

#### DISCARD LIST

List outlets that should be actively removed from Brave Search results via `$discard` rules. For each:

| Outlet | Domain | Discard Reason |
|---|---|---|
| [Name] | `domain` | [1 sentence: why this outlet would degrade result quality — tabloid noise, content farm, misinformation pattern, pure aggregation] |

**Calibration:** Be conservative with discards. A source must be *positively harmful* to result quality, not merely unimpressive. If an outlet is mediocre but occasionally carries something useful, leave it at organic ranking (don't list it here or in recommended sources). The discard list should typically contain **3–8 outlets** — the most prominent noise sources that would otherwise consume result slots.

---

#### ORGANIC RANKING NOTES

In 2–3 sentences, note any outlets that were considered for boost but left at organic ranking, and why. This helps the pipeline operator understand what's in the "middle ground" — sources the pipeline might encounter in results that aren't boosted but aren't discarded either.

---

#### COVERAGE GAP ASSESSMENT

In 2–3 sentences, identify the most significant remaining blind spots after your recommended sources are configured. What types of stories or signals would an analyst still miss? Are there important information channels in this country that exist outside traditional media (Telegram channels, parliamentary transcripts, government gazettes, military blogs) that the pipeline should be aware of even if they can't be easily ingested?

---

#### STRUCTURAL COVERAGE CHECK

Confirm which source(s) fill each structural role:

| Structural Role | Source(s) | Tier |
|---|---|---|
| Government leak channel / policy kite-flying | | |
| Opposition voice | | |
| Defence/security first-mover | | |
| Policy-elite discourse (what decision-makers read) | | |
| Domestic-language depth (N/A for English-dominant) | | |
| Official government source | | |
| Analytical/think tank depth | | |
| Wire service (local bureau) | | |

---

#### LOCALIZED QUERY VOCABULARY

For each of the five signal domains, provide 5–8 **search terms in {{LANGUAGE}}** that would surface relevant stories from this country's domestic press. These are not translations of English analytical vocabulary — they are the actual terms, phrases, and institutional names that journalists and political commentators in this country use when reporting on these topics.

**Format:**

**1. Diplomatic Alignment**
- `"term_1"` — [brief gloss: what this term captures]
- `"term_2"` — [brief gloss]
- ...

**2. Security & Defense Autonomy**
- `"term_1"` — [brief gloss]
- ...

**3. Economic & Technological Statecraft**
- `"term_1"` — [brief gloss]
- ...

**4. Institutional Engagement**
- `"term_1"` — [brief gloss]
- ...

**5. Domestic Constraints**
- `"term_1"` — [brief gloss]
- ...

**Calibration guidance:** The best terms are the ones that would appear in a headline or lede about a posture-relevant event. Avoid abstract analytical vocabulary that appears in academic papers but not in news copy. Prefer institutional names (e.g., the actual name of the defense ministry, the parliamentary foreign affairs committee), policy-specific terms (e.g., the name of a defense procurement program), and action verbs/nouns that signal something happened (e.g., the local-language equivalent of "signed," "deployed," "ratified," "vetoed"). Include acronyms and abbreviations that journalists routinely use without expansion.

---

#### QUERY CONFIGURATION

```
country: [ISO 3166-1 alpha-2 code]
search_lang: [ISO 639-1 code(s)]
freshness: pw
```

**Multi-language notes:** [If the country's media operates in multiple languages, specify which languages cover which analytical domains and whether queries should be run in multiple languages per cycle]

**Suggested query patterns:** [3–5 example queries combining leader names with localized vocabulary terms, formatted as actual Brave News API query strings. Show how the Goggle + query + language filter combination would work in practice.]

---

#### GOGGLE FILE

```goggle
! name: MPM {{COUNTRY}}
! description: MPM pipeline source prioritization for {{COUNTRY}}
! public: false
! author: MPM Pipeline

! --- Tier 1: Essential (boost=3) ---
$boost=3,site=[domain]
...

! --- Tier 2: Important (boost=2) ---
$boost=2,site=[domain]
...

! --- Tier 3: Supplementary (boost=1) ---
$boost=1,site=[domain]
...

! --- Discard: Noise ---
$discard,site=[domain]
...
```

---

#### INTERPRETIVE CONTEXT

For each Tier 1 and Tier 2 source, provide a single-sentence source-weighting statement the pipeline LLM should use when interpreting articles from this outlet:

> "Articles from [outlet] about [topic domain] should be interpreted as [interpretive adjustment] because [ownership/editorial dynamic]."

Where a source serves multiple interpretive functions across different domains, provide one statement per domain. Be specific enough that the pipeline can act on it — "centre-left" is not an interpretive adjustment; "editorially sympathetic to Labour's defense spending commitments and likely to frame procurement decisions as adequate even when independent analysts disagree" is.

This section is designed to be extracted and loaded into the pipeline's system prompt alongside the structural country dossier. It is **not** included in the Goggle file.

---

### Calibration Notes

- **Prioritize signal detection over source quality.** The pipeline's core question is "how is this state positioning itself?" Sources that surface *actions* (procurement decisions, treaty ratifications, votes, deployments, bilateral meetings) are more valuable than sources that surface *commentary*. Commentary sources have value for the Domestic Constraints domain, but the pipeline's primary need is event detection.
- **Structural role outweighs journalistic quality.** A government-controlled outlet that signals policy intent earns a boost even if its journalism is propagandistic — the pipeline needs the signal, and the interpretive context tells the LLM how to read it. Flag the alignment clearly.
- **Be honest about confidence.** If you are uncertain about an outlet's current status (it may have closed, changed ownership, or moved behind a hard paywall), say so. Mark with `[VERIFY]` and the pipeline operator will check.
- **This is not a press freedom assessment.** Government-aligned outlets are not automatically excluded or downranked. The pipeline needs to see what the government is signaling.
- **English-language domestic outlets matter.** If this country has English-language outlets with original reporting (not just translations of domestic-language coverage), include them. They often serve the diplomatic community and foreign business, covering angles that domestic-language press skips.
- **Non-English domestic sources get a boost premium.** For countries where the domestic-language media ecosystem carries signals that don't propagate to English-language outlets, domestic-language sources should be boosted at or above the level their English-language equivalents would receive. The pipeline's translation layer handles the language barrier; the Goggle's job is to ensure these sources surface.
- **Think about the top 20.** Brave returns up to 20 results per query. Your boost assignments determine which 20 results the pipeline sees. Every Tier 1 source should be in that top 20 for any query touching its domain. Every discard is a source you're confident should never occupy one of those 20 slots.
