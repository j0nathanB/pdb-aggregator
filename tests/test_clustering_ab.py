"""
A/B/C clustering comparison: Haiku 4.5 vs Sonnet 4.5 vs Production (Sonnet 4.0).

Loads cluster data from briefs/20260210/debug/, enriches with snippet text,
runs dedup and story arc detection with each model, and compares against
the actual production results.

Run:
    pytest tests/test_clustering_ab.py -v -s

Report saved to: tests/reports/clustering_ab_latest.txt
"""

import json
import copy
from datetime import datetime
from pathlib import Path

import numpy as np
import pytest

# Break circular import: clustering.__init__ -> agents.base -> agents.__init__ -> ...
from src.agents.base import complete  # noqa: F401
from src.clustering.dedup import deduplicate_clusters
from src.clustering.story_grouper import detect_story_arcs
from src.clustering.clusterer import EventCluster
from src.clustering.embedder import EmbeddedSnippet

DEBUG_DIR = Path(__file__).parent.parent / "briefs" / "20260210" / "debug"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "clusters"
REPORTS_DIR = Path(__file__).parent / "reports"

MODELS = {
    "sonnet-4.5": {"model": "claude-sonnet-4-5-20250929", "thinking_budget": 4000},
    "sonnet-4.6": {"model": "claude-sonnet-4-6", "thinking_budget": 4000},
}

PRODUCTION_MODEL = "claude-sonnet-4-20250514"


# =============================================================================
# Data loading
# =============================================================================


def _load_snippet_lookup(leader_slug: str) -> dict[str, dict[str, str]]:
    """Build URL → {"text": ..., "date": ...} lookup from 00_raw_snippets."""
    path = DEBUG_DIR / f"00_raw_snippets_{leader_slug}.json"
    with open(path) as f:
        data = json.load(f)
    lookup = {}
    for s in data.get("news_snippets", []) + data.get("opinion_snippets", []):
        lookup[s["url"]] = {
            "text": s.get("snippet", ""),
            "date": s.get("date", ""),
        }
    return lookup


def _load_debug_clusters(leader_slug: str) -> tuple[list[dict], str]:
    """Load raw cluster data from 02_clusters debug file."""
    path = DEBUG_DIR / f"02_clusters_{leader_slug}.json"
    with open(path) as f:
        data = json.load(f)
    return data["clusters"], data["leader"]


def _load_production_dedup(leader_slug: str) -> dict | None:
    """Load production dedup results from 03_dedup (None if no merges)."""
    path = DEBUG_DIR / f"03_dedup_{leader_slug}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def _load_production_story_arcs(leader_slug: str) -> dict | None:
    """Load production story arc results from 04_story_arcs (None if no merges)."""
    path = DEBUG_DIR / f"04_story_arcs_{leader_slug}.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def _build_event_clusters(
    debug_clusters: list[dict],
    snippet_lookup: dict[str, dict[str, str]],
) -> list[EventCluster]:
    """
    Build EventCluster objects from debug data with real snippet text and dates.

    Uses deterministic dummy embeddings (the LLM dedup call doesn't use them —
    only cluster merging does for centroid recomputation).
    """
    clusters = []
    for c in debug_clusters:
        snippets = []
        for s in c["snippets"]:
            info = snippet_lookup.get(s["url"], {})
            snippet_text = info.get("text", s["title"])
            date = info.get("date", "")

            # Deterministic embedding from URL hash
            seed = hash(s["url"]) % (2**31)
            rng = np.random.RandomState(seed)
            embedding = rng.randn(384).astype(np.float32)
            embedding = embedding / np.linalg.norm(embedding)

            snippets.append(EmbeddedSnippet(
                title=s["title"],
                snippet=snippet_text,
                url=s["url"],
                source_name=s["source_name"],
                source_type=s["source_type"],
                date=date,
                embedding=embedding,
            ))

        centroid = np.mean([s.embedding for s in snippets], axis=0)
        centroid = centroid / np.linalg.norm(centroid)

        clusters.append(EventCluster(
            id=c["id"],
            snippets=snippets,
            centroid=centroid,
        ))
    return clusters


def _use_fixture_clusters(leader_slug: str, snippet_lookup: dict[str, dict[str, str]]) -> list[EventCluster] | None:
    """Try to load clusters from test fixtures (have proper E5 embeddings)."""
    fixture_path = FIXTURES_DIR / f"{leader_slug}.json"
    if not fixture_path.exists():
        return None

    with open(fixture_path) as f:
        data = json.load(f)

    clusters = []
    for c in data["clusters"]:
        snippets = []
        for s in c["snippets"]:
            info = snippet_lookup.get(s["url"], {})
            snippet_text = info.get("text", s["title"])
            date = info.get("date", "")
            snippets.append(EmbeddedSnippet(
                title=s["title"],
                snippet=snippet_text,
                url=s["url"],
                source_name=s["source_name"],
                source_type=s["source_type"],
                date=date,
                embedding=np.array(s["embedding"]),
            ))

        clusters.append(EventCluster(
            id=c["id"],
            snippets=snippets,
            centroid=np.array(c["centroid"]),
        ))
    return clusters


# =============================================================================
# Merge analysis
# =============================================================================


def _analyze_merges(input_clusters: list[EventCluster], output_clusters: list[EventCluster]) -> dict:
    """Determine which clusters were merged by comparing input vs output."""
    input_ids = {c.id for c in input_clusters}
    output_ids = {c.id for c in output_clusters}
    new_ids = output_ids - input_ids

    merges = []
    for oc in output_clusters:
        if oc.id in new_ids:
            output_urls = {s.url for s in oc.snippets}
            sources = []
            for ic in input_clusters:
                input_urls = {s.url for s in ic.snippets}
                if input_urls & output_urls:
                    sources.append(ic.id)
            merges.append({
                "merged_id": oc.id,
                "source_ids": sources,
                "title": oc.representative_title,
                "snippet_count": len(oc.snippets),
                "source_count": oc.unique_source_count,
            })

    return {
        "input_count": len(input_clusters),
        "output_count": len(output_clusters),
        "merge_count": len(input_clusters) - len(output_clusters),
        "merges": merges,
        "output_ids": [c.id for c in output_clusters],
    }


def _analyze_production_merges(pre: list[dict], post: list[dict]) -> dict:
    """Analyze production merges from debug dict data."""
    pre_ids = {c["id"] for c in pre}
    post_ids = {c["id"] for c in post}
    new_ids = post_ids - pre_ids

    merges = []
    for pc in post:
        if pc["id"] in new_ids:
            post_urls = {s["url"] for s in pc["snippets"]}
            sources = []
            for pre_c in pre:
                pre_urls = {s["url"] for s in pre_c["snippets"]}
                if pre_urls & post_urls:
                    sources.append(pre_c["id"])
            merges.append({
                "merged_id": pc["id"],
                "source_ids": sources,
                "title": pc["title"],
                "snippet_count": len(pc["snippets"]),
                "source_count": pc["source_count"],
            })

    return {
        "input_count": len(pre),
        "output_count": len(post),
        "merge_count": len(pre) - len(post),
        "merges": merges,
        "output_ids": [c["id"] for c in post],
    }


# =============================================================================
# Report accumulator (persists across tests within a session)
# =============================================================================


_report_data = {}


def _init_report():
    """Initialize or load existing report data."""
    global _report_data
    json_path = REPORTS_DIR / "clustering_ab_latest.json"
    if json_path.exists():
        with open(json_path) as f:
            _report_data = json.load(f)
    else:
        _report_data = {}
    _report_data.update({
        "generated_at": datetime.now().isoformat(),
        "run_date": "2026-02-10",
        "models": {k: v["model"] for k, v in MODELS.items()},
        "production_model": PRODUCTION_MODEL,
    })
    _report_data.setdefault("leaders", {})


def _save_report():
    """Save JSON and regenerate formatted report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORTS_DIR / "clustering_ab_latest.json"
    with open(json_path, "w") as f:
        json.dump(_report_data, f, indent=2, ensure_ascii=False)

    _write_formatted_report(_report_data)


# =============================================================================
# Test class
# =============================================================================


class TestClusteringAB:
    """A/B/C comparison: Haiku 4.5 vs Sonnet 4.5 vs Production on clustering."""

    @pytest.mark.asyncio
    async def test_mark_carney(self):
        await self._run_leader("mark_carney", "Mark Carney")

    @pytest.mark.asyncio
    async def test_claudia_sheinbaum(self):
        await self._run_leader("claudia_sheinbaum", "Claudia Sheinbaum")

    @pytest.mark.asyncio
    async def test_volodymyr_zelenskyy(self):
        await self._run_leader("volodymyr_zelenskyy", "Volodymyr Zelenskyy")

    async def _run_leader(self, leader_slug: str, leader_name: str):
        """Run full dedup + story arc comparison for one leader."""
        _init_report()

        print(f"\n{'=' * 60}")
        print(f"  {leader_name}")
        print(f"{'=' * 60}")

        # Load data
        debug_clusters, _ = _load_debug_clusters(leader_slug)
        snippet_lookup = _load_snippet_lookup(leader_slug)
        prod_dedup = _load_production_dedup(leader_slug)
        prod_arcs = _load_production_story_arcs(leader_slug)

        # Build EventCluster objects (prefer fixture embeddings, fall back to deterministic)
        clusters_orig = _use_fixture_clusters(leader_slug, snippet_lookup)
        if clusters_orig is None:
            clusters_orig = _build_event_clusters(debug_clusters, snippet_lookup)

        leader_data = {
            "leader_name": leader_name,
            "input_clusters": _serialize_clusters(debug_clusters, snippet_lookup),
            "dedup": {},
            "story_arcs": {},
        }

        # ── DEDUP ──
        for label, params in MODELS.items():
            clusters = copy.deepcopy(clusters_orig)
            deduped = await deduplicate_clusters(
                clusters, leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )
            leader_data["dedup"][label] = _analyze_merges(clusters_orig, deduped)
            n_in = len(clusters_orig)
            n_out = len(deduped)
            print(f"  [dedup/{label}] {n_in} → {n_out} clusters ({n_in - n_out} merges)")

        # Production dedup
        if prod_dedup:
            leader_data["dedup"]["production"] = _analyze_production_merges(
                debug_clusters, prod_dedup["clusters"],
            )
            print(f"  [dedup/production] {prod_dedup['before']} → {prod_dedup['after']} clusters")
        else:
            leader_data["dedup"]["production"] = {
                "input_count": len(debug_clusters),
                "output_count": len(debug_clusters),
                "merge_count": 0,
                "merges": [],
                "output_ids": [c["id"] for c in debug_clusters],
            }
            print(f"  [dedup/production] no merges")

        # ── STORY ARCS ──
        # Run on production post-dedup titles for fair A/B comparison
        if prod_dedup:
            arc_input = prod_dedup["clusters"]
        else:
            arc_input = debug_clusters

        arc_titles = [c["title"] for c in arc_input]
        arc_ids = [c["id"] for c in arc_input]

        # Build dates and snippet texts for story arc detection
        arc_dates = []
        arc_snippet_texts = []
        for c in arc_input:
            if c.get("snippets"):
                first_url = c["snippets"][0].get("url", "")
                info = snippet_lookup.get(first_url, {})
                arc_dates.append(info.get("date", ""))
                arc_snippet_texts.append(info.get("text", ""))
            else:
                arc_dates.append("")
                arc_snippet_texts.append("")

        leader_data["story_arcs"]["input"] = [
            {"id": cid, "title": t} for cid, t in zip(arc_ids, arc_titles)
        ]

        for label, params in MODELS.items():
            arcs = await detect_story_arcs(
                arc_titles, leader_name,
                dates=arc_dates,
                snippets=arc_snippet_texts,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )
            leader_data["story_arcs"][label] = {
                "arc_count": len(arcs),
                "arcs": [
                    {
                        "indices": arc,
                        "cluster_ids": [arc_ids[i] for i in arc],
                        "titles": [arc_titles[i] for i in arc],
                    }
                    for arc in arcs
                ],
            }
            print(f"  [story_arcs/{label}] {len(arcs)} arcs")

        # Production story arcs (derive merges by comparing pre/post IDs)
        if prod_arcs:
            post_dedup_ids = set(arc_ids)
            post_arc_ids = {c["id"] for c in prod_arcs["clusters"]}
            added_ids = post_arc_ids - post_dedup_ids

            prod_arc_groups = []
            for pc in prod_arcs["clusters"]:
                if pc["id"] in added_ids:
                    post_urls = {s["url"] for s in pc["snippets"]}
                    sources = []
                    for ac in arc_input:
                        ac_urls = {s["url"] for s in ac["snippets"]}
                        if ac_urls & post_urls:
                            sources.append(ac["id"])
                    prod_arc_groups.append({
                        "cluster_ids": sources,
                        "merged_id": pc["id"],
                        "title": pc["title"],
                    })

            leader_data["story_arcs"]["production"] = {
                "arc_count": len(prod_arc_groups),
                "arcs": prod_arc_groups,
            }
            print(f"  [story_arcs/production] {len(prod_arc_groups)} arcs")
        else:
            leader_data["story_arcs"]["production"] = {"arc_count": 0, "arcs": []}
            print(f"  [story_arcs/production] no arcs")

        # Save results
        _report_data["leaders"][leader_slug] = leader_data
        _save_report()

        # Assertions
        for label in MODELS:
            d = leader_data["dedup"][label]
            assert d["output_count"] > 0
            assert d["output_count"] <= d["input_count"]


def _serialize_clusters(debug_clusters: list[dict], snippet_lookup: dict[str, dict[str, str]]) -> list[dict]:
    """Serialize input clusters with full snippet text and dates."""
    result = []
    for c in debug_clusters:
        snippets = []
        for s in c["snippets"]:
            info = snippet_lookup.get(s["url"], {})
            snippets.append({
                "title": s["title"],
                "source_name": s["source_name"],
                "source_type": s["source_type"],
                "url": s["url"],
                "snippet_text": info.get("text", ""),
                "date": info.get("date", ""),
            })
        result.append({
            "id": c["id"],
            "title": c["title"],
            "source_count": c["source_count"],
            "has_wire": c.get("has_wire", False),
            "snippet_count": len(snippets),
            "snippets": snippets,
        })
    return result


# =============================================================================
# Formatted report
# =============================================================================


def _write_formatted_report(data: dict):
    """Write comprehensive human-readable comparison report with full snippet text."""
    out = []
    w = out.append

    models = data["models"]
    prod_model = data["production_model"]
    all_labels = list(models.keys()) + ["production"]

    w(f"{'=' * 100}")
    w(f"  CLUSTERING A/B/C COMPARISON — {data.get('run_date', '?')} Run")
    w(f"  Generated: {data['generated_at']}")
    w(f"  Model A: {models.get('haiku', '?')}  ('haiku')")
    w(f"  Model B: {models.get('sonnet', '?')}  ('sonnet')")
    w(f"  Model C: {prod_model}  ('production')")
    w(f"{'=' * 100}")

    for leader_slug, ld in data.get("leaders", {}).items():
        leader_name = ld.get("leader_name", leader_slug)
        input_clusters = ld.get("input_clusters", [])

        # ── INPUT CLUSTERS ──
        w("")
        w(f"{'━' * 100}")
        w(f"  {leader_name.upper()} — Input Clusters ({len(input_clusters)})")
        w(f"{'━' * 100}")

        for c in input_clusters:
            wire = " ★wire" if c.get("has_wire") else ""
            w("")
            w(f"  [{c['id']}] \"{c['title']}\"")
            w(f"       {c['snippet_count']} snippets, {c['source_count']} unique sources{wire}")

            for j, s in enumerate(c["snippets"]):
                is_last = j == len(c["snippets"]) - 1
                branch = "└─" if is_last else "├─"
                cont = "  " if is_last else "│ "
                w(f"       {branch} [{s['source_name']}/{s['source_type']}]")
                w(f"       {cont}   \"{s['title']}\"")
                if s.get("snippet_text"):
                    # Show snippet text, truncated to ~200 chars
                    text = s["snippet_text"]
                    if len(text) > 200:
                        text = text[:200] + "..."
                    w(f"       {cont}   {text}")

        # ── DEDUP RESULTS ──
        dedup = ld.get("dedup", {})
        w("")
        w(f"{'─' * 100}")
        w(f"  {leader_name.upper()} — Dedup Comparison")
        w(f"{'─' * 100}")
        w("")

        # Summary table
        hdr = f"  {'':35s}"
        for lbl in all_labels:
            hdr += f"  {lbl:>12s}"
        w(hdr)

        for row_label, key in [("Input clusters", "input_count"), ("Output clusters", "output_count"), ("Merges", "merge_count")]:
            row = f"  {row_label:35s}"
            for lbl in all_labels:
                val = dedup.get(lbl, {}).get(key, "—")
                row += f"  {val:>12}"
            w(row)

        # Merge decisions per model
        w("")
        for lbl in all_labels:
            d = dedup.get(lbl, {})
            merges = d.get("merges", [])
            if merges:
                w(f"  {lbl} merge decisions:")
                for m in merges:
                    src = " + ".join(f"[{s}]" for s in m["source_ids"])
                    w(f"    {src}  →  [{m['merged_id']}] \"{m['title'][:80]}\"")
                    w(f"    ({m.get('snippet_count', '?')} snippets, {m.get('source_count', '?')} sources)")
            else:
                w(f"  {lbl}: no merges")

        # Agreement summary
        merge_sets = {}
        for lbl in all_labels:
            d = dedup.get(lbl, {})
            merges = d.get("merges", [])
            key = tuple(tuple(sorted(m["source_ids"])) for m in merges)
            merge_sets[lbl] = key
        unique_decisions = set(merge_sets.values())
        w("")
        if len(unique_decisions) == 1:
            w(f"  ✓ All three models agree on dedup decisions")
        else:
            w(f"  ⚠ Models disagree on dedup:")
            for lbl in all_labels:
                merges = dedup.get(lbl, {}).get("merges", [])
                if merges:
                    groups = ", ".join(f"{m['source_ids']}" for m in merges)
                    w(f"    {lbl:12s}: merge {groups}")
                else:
                    w(f"    {lbl:12s}: no merges")

        # ── STORY ARC RESULTS ──
        arcs = ld.get("story_arcs", {})
        w("")
        w(f"{'─' * 100}")
        w(f"  {leader_name.upper()} — Story Arc Comparison")
        w(f"{'─' * 100}")

        # Show input titles (post-dedup)
        arc_input = arcs.get("input", [])
        if arc_input:
            w("")
            w(f"  Input (post-dedup): {len(arc_input)} clusters")
            for i, t in enumerate(arc_input):
                w(f"    [{i:2d}] {t['id']:20s}  \"{t['title'][:70]}\"")

        # Summary
        w("")
        hdr = f"  {'':35s}"
        for lbl in all_labels:
            hdr += f"  {lbl:>12s}"
        w(hdr)
        row = f"  {'Arcs detected':35s}"
        for lbl in all_labels:
            val = arcs.get(lbl, {}).get("arc_count", "—")
            row += f"  {val:>12}"
        w(row)

        # Arc details per model
        w("")
        for lbl in all_labels:
            a = arcs.get(lbl, {})
            arc_list = a.get("arcs", [])
            if arc_list:
                w(f"  {lbl} arcs:")
                for i, arc in enumerate(arc_list):
                    if "indices" in arc:
                        # Haiku/Sonnet format: indices into post-dedup list
                        ids = arc.get("cluster_ids", [])
                        w(f"    Arc {i+1}: {ids}")
                        for t in arc.get("titles", []):
                            w(f"      • \"{t[:85]}\"")
                    elif "merged_id" in arc:
                        # Production format: cluster_ids → merged_id
                        w(f"    Arc {i+1}: {arc['cluster_ids']} → [{arc['merged_id']}]")
                        if arc.get("title"):
                            w(f"      → \"{arc['title'][:85]}\"")
                w("")
            else:
                w(f"  {lbl}: no arcs")
                w("")

    w(f"{'=' * 100}")

    report_path = REPORTS_DIR / "clustering_ab_latest.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(out) + "\n")
