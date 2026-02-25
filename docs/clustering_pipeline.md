# Clustering Pipeline

## Embeddings

`intfloat/multilingual-e5-small` via sentence-transformers. All leaders use the same model so embeddings are in the same latent space for cross-leader comparison. Before embedding, the leader's name is stripped from the text so the model clusters on *topic* rather than the shared subject. E5's `"passage: "` instruction prefix is applied.

## Pipeline (`EventClusteringAgent.process_leader`)

1. **Fetch snippets** — SearchAPI (Google News) with site-scoped queries per source. Returns titles + snippets only, no full text. Opinion pieces filtered out via URL patterns. Stale results outside the date range are discarded.

2. **Pre-filter** — `filter_relevant()` checks that snippets actually mention the leader's surname (with regex handling for Slavic declensions, transliteration variants, etc.).

3. **Embed** — Each snippet's `title + snippet` text is embedded with E5-multilingual-small.

4. **Cluster** — HDBSCAN groups embeddings into event clusters.

5. **Reason** — Single LLM call (`reason_about_clusters`) does dedup + story arc merging on the clusters.

6. **Score** — Clusters scored by importance (source count, wire coverage, etc.), split into top events vs. rest.

7. **Fetch full articles from Diffbot** — Only for:
   - **Top events** (up to `max_events_for_brief=5`): up to 3 articles each, prioritizing 1 wire + domestic sources for diversity
   - **Remaining corroborated events** (3+ sources): up to 3 articles each
   - **Remaining thin events** (<3 sources): just 1 article each

Diffbot is called selectively — only on URLs that survived clustering and scoring, not on every search result. Diffbot's NLP API (entity extraction, summaries) is disabled due to rate limits; only the article extraction endpoint is used.

## Key files

- `src/agents/event_clustering.py` — orchestrator
- `src/clustering/embedder.py` — embedding + pre-filtering
- `src/clustering/clusterer.py` — HDBSCAN clustering
- `src/clustering/scorer.py` — event scoring
- `src/clustering/cluster_reasoning.py` — LLM dedup + arc merging
- `src/fetcher/core.py` — `fetch_snippets_for_leader`, `fetch_full_articles`
- `src/fetcher/diffbot_nlp.py` — Diffbot integration
- `src/fetcher/opinion_filter.py` — opinion URL filtering
