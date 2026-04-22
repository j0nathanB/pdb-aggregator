# Story Map Sidecar

Reference for the per-country-week JSON file written by the story_map
agent: `ledgers/story_maps/{code}_{week}.json`.

## Purpose

The sidecar is the durable, LLM-authored clustering output (headlines +
summaries + taxonomy labels) paired with the pass-through Brave article
metadata that seeded it. It is the canonical record of what the
story_map agent produced for a given country-week, and downstream
stages consume it rather than re-deriving anything from raw search
results.

## Write path

`ledger/storage.py::save_story_map` serializes a `StoryMapOutput` into
the sidecar. Called from `orchestrator.process_deep_dive` when
`story_map and story_map.stories` are both truthy; a partial or empty
map is **not** saved (so a prior sidecar survives a failed re-run —
this is what made the 2026-04-19 Other Stories remediation possible).

## Shape

### Top-level metadata (accounting, not text)

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `country` | str | LLM-echoed | Human-readable name, e.g. `"DE"` in current output |
| `code` | str | Set by save_story_map | 2-letter country code |
| `week` | str | Set by save_story_map | `"YYYY-MM-DD"` end_date |
| `analysis_date` | str | LLM-echoed | Usually equals `week` |
| `search_results_total` | int | Model's count | Total Brave+expansion results fed in |
| `stories_identified` | int | Model's count | Model's self-reported cluster count — can drift from `len(stories)` if tool_use was truncated mid-stream; see `newsletter/_trace_reader.py` / commit `82d2afd` for the gate |
| `off_topic_filtered` | int | Model's count | How many inputs the model rejected as off-topic |
| `noise_summary` | str | LLM-written | Optional free-text note about the noise floor. Usually empty. |

### `stories[]` — LLM-authored text

One entry per identified cluster.

| Field | Type | Source | Notes |
| --- | --- | --- | --- |
| `story_id` | str | LLM-assigned | Stable within the week, e.g. `"1"` |
| `headline` | str | **LLM-written** | Economist-style title, one line |
| `summary` | str | **LLM-written** | 1–3 sentences of prose |
| `actors_involved` | list[str] | **LLM-picked** | Names matching the country's configured actors |
| `signal_category_hint` | str | **LLM-picked enum** | One of `alignment_diplomatic`, `security_defense`, `economic_tech`, `institutional`, `domestic_regime`, `unclear` |
| `source_count` | str | LLM-computed | Count of articles in the cluster |
| `sources` | list[str] | LLM-distilled | Publisher domains, e.g. `["reuters.com", "welt.de"]` |
| `date_range` | str | LLM-inferred | `"YYYY-MM-DD to YYYY-MM-DD"` span |
| `representative_urls` | list[str] | LLM-picked | Top URLs for the cluster (used for Layer 2 extraction ranking) |

### `stories[].articles[]` — pass-through Brave metadata

Each cluster holds the input articles that seeded it. The LLM grouped
them; the fields are echoed verbatim from the Brave News response.

| Field | Type | Source |
| --- | --- | --- |
| `title` | str | Brave News result |
| `source` | str | Brave News result |
| `url` | str | Brave News result |
| `date` | str | Brave News result |

### `single_source_items[]`

Headlines that didn't cluster with anything else. Same shape as a
single article plus a `signal_category_hint`.

## Example

From `ledgers/story_maps/de_2026-04-19.json` (Germany, week ending
2026-04-19 — 14 stories):

```json
{
  "country": "DE",
  "code": "de",
  "week": "2026-04-19",
  "analysis_date": "2026-04-19",
  "search_results_total": 412,
  "stories_identified": 25,
  "off_topic_filtered": 47,
  "noise_summary": "",
  "stories": [
    {
      "story_id": "1",
      "headline": "Hannover Messe opens with Merz-Lula bilateral talks on trade, climate, and world order",
      "summary": "Chancellor Merz and Brazilian President Lula da Silva opened the Hannover industrial fair on April 19, holding bilateral…",
      "actors_involved": ["Merz", "CDU/CSU"],
      "signal_category_hint": "alignment_diplomatic",
      "source_count": "10",
      "sources": ["reuters.com", "welt.de", "n-tv.de"],
      "date_range": "2026-04-17 to 2026-04-19",
      "articles": [
        {
          "title": "Germany's Merz, Brazil's Lula stress close European-Brazilian cooperation",
          "source": "reuters.com",
          "url": "https://www.reuters.com/world/americas/germanys-merz-brazils-lula-stress-close-european-brazilian-cooperation-2026-04-19/",
          "date": "2026-04-19"
        }
      ],
      "representative_urls": [
        "https://www.reuters.com/world/americas/germanys-merz-brazils-lula-stress-close-european-brazilian-cooperation-2026-04-19/"
      ]
    }
  ],
  "single_source_items": []
}
```

## What the sidecar does NOT contain

- Raw Brave response bodies (only the normalized `{title, source, url,
  date}` per article).
- The story_map prompt or system instructions.
- The model's extended-thinking text.
- Token usage or run-cost accounting.

Those live in the trace file at `briefs/{YYYYMMDD}/traces/story_map_{code}.json`
when debugging is needed.

## Downstream consumers

1. **`entry.story_clusters`** — `orchestrator.process_deep_dive`
   derives `[{headline, summary, source_url, source_name}]` from
   `stories[]` and persists it on the weekly entry in
   `ledgers/countries/{code}.json`. This becomes the source of the
   "Other Stories" accordion and the at-a-glance card headlines.

2. **`CountryContent.story_map_data`** —
   `content_builder._build_country_content` attaches the full sidecar
   dict as a passthrough field so the region template can render a
   `## Notes` section with a collapsible `<ResponseField>` per story.

3. **Layer 2 extraction** — `representative_urls` and `source_count`
   feed ranking in the extraction step.

## Failure modes worth knowing

- **`stories_identified` ≠ `len(stories)`** — the tool_use response was
  truncated mid-array. The gate in `_tool_input_complete`
  (commit `82d2afd`) now falls back to free-form JSON before we hydrate
  a `StoryMapOutput`, so this should no longer produce an empty
  `stories[]` with non-zero `stories_identified`. If it still happens,
  the agent logs a WARNING at the accounting step.

- **No sidecar written despite a successful run** — means
  `story_map.stories` was empty or None. Check the trace: if
  `response_text` holds only scalar fields
  (`{"country": "...", "search_results_total": N}`), the tool_use was
  partial.

- **Sidecar is stale (from a prior run)** — a recovery that re-runs
  story_map will only overwrite the sidecar if the new `stories[]` is
  non-empty. This is intentional: a failed re-run won't clobber a good
  prior sidecar.
