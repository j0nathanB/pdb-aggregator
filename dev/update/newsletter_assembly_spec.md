# Newsletter Assembly Specification

## Purpose

The newsletter assembly step is deterministic — no LLM calls. It takes structured JSON outputs from the pipeline and renders them into the final Markdown publication. This document defines the rendering rules, editorial decisions, and formatting conventions.

The assembly is the last step in the pipeline. By the time it runs, all analytical work is complete. The assembly's job is presentation, not analysis.

---

## Inputs

The assembly reads from:

1. **Global ledger** → `ledgers/global.json`
   - `weekly_entry.executive_briefing_items` → Executive Brief section
   - `watchlist` → Watchlist section
   - `global_posture_summary` → optional metadata

2. **Regional reports** → `output/regional/{region}_{date}.json` (5 files)
   - `cross_cutting_dynamics` → Regional lead paragraphs
   - `gaps` → folded into regional leads where relevant
   - `low_confidence_items` → omitted from newsletter (internal use only)
   - `dynamics_considered_and_rejected` → omitted from newsletter (internal use only)

3. **Country analyses** → `output/country_reports/{code}_{date}.json` (28 files)
   - `weekly_entry` → Country entry
   - `updated_posture_summary` → Country entry summary line
   - `updated_signal_categories` → Country entry detail
   - `weekly_entry.devils_advocate` → "Between the Lines" box

4. **Triage decisions** → `output/triage/triage_{date}.json`
   - `decisions` → determines which countries get full entries vs. maintenance entries

---

## Output

A single Markdown file: `output/newsletters/mpm_{date}.md`

---

## Newsletter Structure and Rendering Rules

### Header

```markdown
# The Middle Powers Monitor
## Week of {date_range_start} to {date_range_end}

*Covering 28 countries across five regions. {deep_dive_count} countries received full analytical treatment this week; {maintenance_count} were held at maintenance.*
```

The italicized line gives the reader transparency about coverage depth. Pull `deep_dive_count` and `maintenance_count` from the triage output.

---

### Executive Brief

**Source:** `global_ledger.weekly_entry.executive_briefing_items`

**Target length:** 800-1200 words total across all items.

**Rendering:**

For each briefing item, render as a subsection:

```markdown
### {item.title}

{item.what}

{item.why_it_matters}

*Confidence: {confidence_label}. {item.confidence_note}*

*What to watch: {item.what_to_watch}*
```

**Confidence label mapping:**
- 5 → "High confidence"
- 4 → "Moderate-high confidence"
- 3 → "Moderate confidence"
- 2 → "Low confidence"
- 1 → "Very low confidence"

**Ordering:** Items ordered by confidence descending. Highest-confidence theme leads.

**Competing narratives:** Not rendered in the newsletter. They exist in the structured data for analytical audit but would clutter the reader-facing product. The confidence note implicitly captures uncertainty.

---

### Regional Sections

Five sections, one per region, in this fixed order:
1. Frontline & Eastern Europe
2. Western Europe
3. Asia-Pacific
4. Middle East, Turkey & South Asia
5. The Americas

This ordering puts the highest-stakes regions first (active conflict zone, autonomous defense capacity, latent conflict scenario) and the lower-urgency regions last. It is fixed — it does not change based on which region had the most activity this week.

Each regional section has two parts: a regional lead and country entries.

#### Regional Lead

**Source:** `regional_report.cross_cutting_dynamics`

**Rendering:**

```markdown
---

## Frontline & Eastern Europe

{Render each cross_cutting_dynamic as a narrative paragraph. 
Do not use the JSON field names. Convert the structured 
assessment, significance, and trend into flowing prose.
Include the confidence and linkage strength parenthetically
only if confidence <= 3 or linkage is weak/speculative.}

{If regional_report.gaps contains items, append a paragraph:
"Notably absent this week: {gap.expected_dynamic}. {gap.assessment}"}
```

**Target length:** 2-4 paragraphs per region. Regions with no cross-cutting dynamics get a single paragraph noting this: "No significant cross-country dynamics emerged in {region} this week. Country-level developments are covered below."

**What to omit:**
- `dynamics_considered_and_rejected` — internal analytical discipline, not reader-facing
- `low_confidence_items` — quarantined for a reason
- `evidence_against_linkage` — internal rigor check, not editorial content
- `confidence_inherited_from` — too granular for the reader

#### Country Entries (Deep Dive)

**Source:** Country analysis for countries where triage decision was `deep_dive`.

**Rendering:**

```markdown
### {country_name}

{updated_posture_summary.text}

**Key developments:**

{For each signal category where movement == "significant" or "minor",
render the top development as a brief item:}

- **{signal_category_display_name}:** {development.summary} *({source}, {date})*

{If unexpected_developments exist:}
- **Unexpected:** {development.headline}. {development.assessment}

{If absence_check items with significance exist:}
- **Notable absence:** {absence.expected} — {absence.significance}

> **Between the Lines:** {Render the devil's advocate challenges
> as a brief analytical note. Pick the single most significant
> challenge — not all of them. Frame it as "The adversarial 
> review flagged..." or "Worth noting:" followed by the 
> substance of the challenge. 1-3 sentences max.}
```

**Signal category display names:**
- `alignment_diplomatic` → "Diplomatic"
- `security_defense` → "Security"
- `economic_tech` → "Economic"
- `institutional` → "Institutional"
- `domestic_regime` → "Domestic"

**Ordering of developments within a country entry:** Significant movements first, then minor, then unexpected, then absences. Within the same movement level, order by confidence descending.

**Maximum developments per country:** 5. If more than 5 significant/minor developments exist, select the 5 with highest confidence scores. The full record exists in the structured data; the newsletter is a curated view.

**Confidence rendering in country entries:** Do not show numeric confidence scores at the country level. The reader doesn't need per-development confidence in the newsletter — that's for the analyst and the upstream synthesis layers. Exception: if a development has confidence <= 2, append *(preliminary)* after the source attribution to signal that the finding is not fully corroborated.

#### Country Entries (Maintenance)

**Source:** Country analysis for countries where triage decision was `maintenance`.

**Rendering:**

```markdown
### {country_name}

{updated_posture_summary.text} No significant developments this week.
```

If the maintenance entry has wire/headline findings logged, render a single line:

```markdown
### {country_name}

{updated_posture_summary.text} Wire coverage noted {brief one-line summary of findings}; no full analysis conducted.
```

Maintenance entries do not get "Key developments," "Between the Lines," or any detailed rendering. They exist in the newsletter so the reader knows the country is being monitored, but they don't consume editorial space.

#### Country Ordering Within Regions

Within each regional section, countries are ordered:
1. Deep-dive countries first, ordered by activity level (high → moderate → low)
2. Maintenance countries last, in fixed alphabetical order

This puts the most newsworthy entries at the top of each region.

---

### Watchlist

**Source:** `global_ledger.watchlist`

**Rendering:**

```markdown
---

## Watchlist

*Items worth monitoring that didn't make the executive briefing.*

{For each watchlist item:}

- **{item.item}** ({country_names}): {item.why_it_matters} *Trigger: {item.trigger}.*
```

**Ordering:** By signal category, then alphabetically within category. Group items by category with a light visual separator if there are more than 5 items.

**Maximum items:** 10. If the global ledger watchlist has more than 10 items, select the 10 with the most recent `added_week` dates. Older watchlist items are presumably being tracked through active dynamics or have become stale.

---

### Footer

```markdown
---

*The Middle Powers Monitor tracks 28 countries across five regions, analyzing state positioning through five analytical dimensions: diplomatic alignment, security posture, economic statecraft, institutional engagement, and domestic constraints. Published weekly.*

*This edition: {date}*
```

---

## Formatting Conventions

**Markdown flavor:** Standard CommonMark. No HTML. No custom CSS. The output should render correctly in any Markdown viewer, Obsidian, or static site generator (Jekyll, Hugo).

**Headers:** H1 for publication title only. H2 for regional sections and Watchlist. H3 for country entries and executive briefing themes. No H4 or deeper.

**Emphasis:** Bold for development category labels and watchlist item titles. Italic for confidence notes, metadata, and source attributions. No underline.

**Blockquotes:** Used only for "Between the Lines" analytical notes. This visually distinguishes adversarial review from the main analytical content.

**Lists:** Bulleted lists for developments within country entries and watchlist items. No numbered lists anywhere — the newsletter is not a ranking.

**Links:** Do not include source URLs in the newsletter. The structured data has them for audit; the newsletter reader doesn't need them. Source names and dates are sufficient attribution.

**Length targets:**
- Executive Brief: 800-1200 words
- Regional lead: 150-400 words per region
- Deep-dive country entry: 150-300 words
- Maintenance country entry: 30-60 words
- Watchlist: 200-400 words total
- Full newsletter: 4,000-7,000 words depending on activity level

---

## Edge Cases

**All countries in a region are at maintenance.** Render the regional lead as: "All {region} countries were held at maintenance this week. No significant developments warranted full analytical treatment." Then render the maintenance entries.

**No executive briefing items.** This should not happen — the executive agent is required to produce at least one. If it somehow does, render: "No system-level dynamics met the threshold for executive-level analysis this week. See regional sections for country-level developments."

**Empty watchlist.** Omit the Watchlist section entirely rather than rendering an empty section.

**A deep-dive country with all categories at "none" movement.** This can happen — triage flagged it based on wire/headline activity that the deep dive found to be less significant than expected. Render it as a deep-dive entry with the posture summary and a note: "Full analysis conducted; no significant posture changes identified despite initial indicators."

**Devil's advocate section is missing** (failure case). Omit the "Between the Lines" blockquote. Do not render a placeholder.

---

## Assembly Logic (Pseudocode)

```python
def assemble_newsletter(date, date_range_start, date_range_end):
    # Load all inputs
    global_ledger = load_global_ledger()
    triage = load_triage(date)
    regional_reports = {r: load_regional(r, date) for r in REGIONS}
    country_reports = {c: load_country_report(c, date) for c in COUNTRIES}
    
    sections = []
    
    # Header
    sections.append(render_header(date_range_start, date_range_end, triage))
    
    # Executive Brief
    briefing_items = global_ledger.weekly_entry.executive_briefing_items
    briefing_items.sort(key=lambda x: x.confidence, reverse=True)
    sections.append(render_executive_brief(briefing_items))
    
    # Regional sections
    for region in REGION_ORDER:
        regional_report = regional_reports[region]
        region_countries = get_countries_for_region(region)
        
        # Split into deep-dive and maintenance
        deep_dive = [c for c in region_countries 
                     if triage.get_decision(c) == "deep_dive"]
        maintenance = [c for c in region_countries 
                       if triage.get_decision(c) == "maintenance"]
        
        # Sort deep-dive by activity level
        deep_dive.sort(key=lambda c: activity_sort_key(country_reports[c]))
        maintenance.sort(key=lambda c: c.name)  # alphabetical
        
        sections.append(render_regional_lead(region, regional_report))
        
        for country in deep_dive:
            sections.append(render_deep_dive_entry(country, country_reports[country]))
        
        for country in maintenance:
            sections.append(render_maintenance_entry(country, country_reports[country]))
    
    # Watchlist
    if global_ledger.watchlist:
        watchlist = sorted(global_ledger.watchlist, 
                          key=lambda x: x.added_week, reverse=True)[:10]
        sections.append(render_watchlist(watchlist))
    
    # Footer
    sections.append(render_footer(date))
    
    return "\n\n".join(sections)

REGION_ORDER = [
    "frontline_eastern_europe",
    "western_europe", 
    "asia_pacific",
    "middle_east_turkey_south_asia",
    "americas"
]
```

---

## What the Assembly Does NOT Do

- No summarization, paraphrasing, or editorial rewriting. Text from structured outputs is rendered as-is (with formatting applied).
- No analytical judgment. The assembly doesn't decide what's important — that was done by the agents.
- No confidence recalculation. Confidence scores flow through unchanged.
- No filtering beyond the specified rules (max 5 developments, max 10 watchlist items, single devil's advocate challenge selection).
- No LLM calls. If the structured data is poorly written, it shows up in the newsletter as poorly written. This is by design — it creates a feedback pressure to improve upstream prompt quality.
