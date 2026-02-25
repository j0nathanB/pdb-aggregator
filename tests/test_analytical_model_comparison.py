"""
A/B comparison: Haiku vs Sonnet for analytical clustering tasks.

Runs dedup, story arc detection, and title merge with both models on the same
fixtures, then saves a side-by-side report for human review.

Run manually:
    pytest tests/test_analytical_model_comparison.py -v --timeout=600 -s

Report saved to: tests/reports/analytical_ab_<timestamp>.json
"""

import json
import asyncio
import copy
from datetime import datetime
from pathlib import Path

import pytest

from src.clustering.dedup import deduplicate_clusters
from src.clustering.story_grouper import detect_story_arcs
from src.agents.base import extract_json_from_response
from tests.conftest import load_clusters


REPORTS_DIR = Path(__file__).parent / "reports"

MODELS = {
    "haiku": {
        "model": "claude-haiku-4-5-20251001",
        "thinking_budget": 4000,
    },
    "sonnet": {
        "model": "claude-sonnet-4-5-20250929",
        "thinking_budget": 4000,
    },
}


def _cluster_summary(clusters):
    """Summarize clusters for the report."""
    return [
        {
            "id": c.id,
            "title": c.representative_title,
            "source_count": c.unique_source_count,
            "snippet_count": len(c.snippets),
        }
        for c in clusters
    ]


@pytest.mark.timeout(600)
class TestAnalyticalModelComparison:
    """A/B test: Haiku vs Sonnet on clustering tasks."""

    @pytest.mark.asyncio
    async def test_dedup_comparison(self):
        """Compare dedup output between Haiku and Sonnet."""
        clusters_orig, leader_name = load_clusters("mark_carney")

        results = {}
        for label, params in MODELS.items():
            # Deep copy clusters so merges from one run don't affect the other
            clusters = copy.deepcopy(clusters_orig)

            deduped = await deduplicate_clusters(
                clusters,
                leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )

            results[label] = {
                "input_count": len(clusters_orig),
                "output_count": len(deduped),
                "merges": len(clusters_orig) - len(deduped),
                "clusters": _cluster_summary(deduped),
            }

            print(f"\n[dedup/{label}] {len(clusters_orig)} -> {len(deduped)} clusters")
            for c in deduped:
                print(f"  {c.id}: {c.representative_title[:60]} ({len(c.snippets)} snippets)")

        self._save_stage("dedup", leader_name, results)

        # Both should return valid results
        for label in MODELS:
            assert results[label]["output_count"] > 0
            assert results[label]["output_count"] <= results[label]["input_count"]

    @pytest.mark.asyncio
    async def test_story_arcs_comparison(self):
        """Compare story arc detection between Haiku and Sonnet."""
        clusters, leader_name = load_clusters("mark_carney")
        titles = [c.representative_title for c in clusters]

        results = {}
        for label, params in MODELS.items():
            arcs = await detect_story_arcs(
                titles,
                leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )

            results[label] = {
                "arc_count": len(arcs),
                "arcs": [
                    {
                        "indices": arc,
                        "titles": [titles[i] for i in arc],
                    }
                    for arc in arcs
                ],
            }

            print(f"\n[story_arcs/{label}] {len(arcs)} arcs detected")
            for arc in arcs:
                print(f"  {arc}: {[titles[i][:40] + '...' for i in arc]}")

        self._save_stage("story_arcs", leader_name, results)

        # Both should return valid results (empty is acceptable)
        for label in MODELS:
            for arc_info in results[label]["arcs"]:
                assert len(arc_info["indices"]) >= 2

    @pytest.mark.asyncio
    async def test_cluster_reasoning_comparison(self):
        """Compare combined cluster reasoning between Haiku and Sonnet."""
        from src.clustering.cluster_reasoning import reason_about_clusters

        clusters, leader_name = load_clusters("mark_carney")

        results = {}
        for label, params in MODELS.items():
            result_clusters = await reason_about_clusters(
                clusters,
                leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )

            results[label] = {
                "input_count": len(clusters),
                "output_count": len(result_clusters),
                "titles": [c.representative_title for c in result_clusters],
            }

            print(f"\n[cluster_reasoning/{label}] {len(clusters)} -> {len(result_clusters)} clusters")

        self._save_stage("cluster_reasoning", leader_name, results)

    def _save_stage(self, stage: str, leader_name: str, results: dict):
        """Append a stage result to the report file."""
        _save_to_report(stage, leader_name, results)


@pytest.mark.timeout(600)
class TestMultilingualComparison:
    """A/B on non-English clusters to test cross-lingual robustness."""

    @pytest.mark.asyncio
    async def test_dedup_spanish_comparison(self):
        """Compare dedup on Spanish-titled clusters."""
        clusters_orig, leader_name = load_clusters("claudia_sheinbaum")

        results = {}
        for label, params in MODELS.items():
            clusters = copy.deepcopy(clusters_orig)
            deduped = await deduplicate_clusters(
                clusters,
                leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )
            results[label] = {
                "input_count": len(clusters_orig),
                "output_count": len(deduped),
                "merges": len(clusters_orig) - len(deduped),
                "clusters": _cluster_summary(deduped),
            }
            print(f"\n[dedup_es/{label}] {len(clusters_orig)} -> {len(deduped)} clusters")

        _save_to_report("dedup_spanish", leader_name, results)

        # Both should handle Spanish without errors
        for label in MODELS:
            assert results[label]["output_count"] > 0

    @pytest.mark.asyncio
    async def test_story_arcs_ukrainian_comparison(self):
        """Compare story arcs on Ukrainian-titled clusters."""
        clusters, leader_name = load_clusters("volodymyr_zelenskyy")
        titles = [c.representative_title for c in clusters]

        results = {}
        for label, params in MODELS.items():
            arcs = await detect_story_arcs(
                titles,
                leader_name,
                model=params["model"],
                thinking_budget=params["thinking_budget"],
            )
            results[label] = {
                "arc_count": len(arcs),
                "arcs": [
                    {"indices": arc, "titles": [titles[i] for i in arc]}
                    for arc in arcs
                ],
            }
            print(f"\n[story_arcs_uk/{label}] {len(arcs)} arcs")

        _save_to_report("story_arcs_ukrainian", leader_name, results)

        for label in MODELS:
            for arc_info in results[label]["arcs"]:
                assert len(arc_info["indices"]) >= 2


# =============================================================================
# Report persistence + formatting
# =============================================================================

def _save_to_report(stage: str, leader_name: str, results: dict):
    """Append a stage result to the JSON report."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "analytical_ab_latest.json"

    if report_path.exists():
        with open(report_path) as f:
            report = json.load(f)
    else:
        report = {
            "generated_at": datetime.now().isoformat(),
            "models": {k: v["model"] for k, v in MODELS.items()},
            "stages": {},
        }

    report["stages"][stage] = results

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Regenerate the formatted comparison after every stage
    _write_formatted_report(report)


def _write_formatted_report(report: dict):
    """Write a human-readable side-by-side comparison file."""
    out = []
    w = out.append

    models = report["models"]
    labels = list(models.keys())
    col_a, col_b = labels[0], labels[1]
    name_a, name_b = models[col_a], models[col_b]

    w(f"{'=' * 80}")
    w(f"  ANALYTICAL MODEL A/B COMPARISON")
    w(f"  Generated: {report['generated_at']}")
    w(f"  Model A: {name_a}  ('{col_a}')")
    w(f"  Model B: {name_b}  ('{col_b}')")
    w(f"{'=' * 80}")

    stages = report.get("stages", {})

    # --- Dedup stages ---
    for stage_key in ["dedup", "dedup_spanish"]:
        if stage_key not in stages:
            continue
        stage = stages[stage_key]
        leader = {
            "dedup": "Mark Carney (English)",
            "dedup_spanish": "Claudia Sheinbaum (Spanish)",
        }.get(stage_key, stage_key)

        w("")
        w(f"{'─' * 80}")
        w(f"  DEDUP — {leader}")
        w(f"{'─' * 80}")
        w("")
        w(f"  {'':40s}  {col_a:>18s}  {col_b:>18s}")
        w(f"  {'Input clusters':40s}  {stage[col_a]['input_count']:>18d}  {stage[col_b]['input_count']:>18d}")
        w(f"  {'Output clusters':40s}  {stage[col_a]['output_count']:>18d}  {stage[col_b]['output_count']:>18d}")
        w(f"  {'Merges':40s}  {stage[col_a]['merges']:>18d}  {stage[col_b]['merges']:>18d}")

        # Side-by-side cluster list
        clusters_a = stage[col_a].get("clusters", [])
        clusters_b = stage[col_b].get("clusters", [])
        ids_a = {c["id"] for c in clusters_a}
        ids_b = {c["id"] for c in clusters_b}
        all_ids = []
        seen = set()
        for c in clusters_a + clusters_b:
            if c["id"] not in seen:
                all_ids.append(c["id"])
                seen.add(c["id"])

        w("")
        w(f"  {'ID':<14s}  {'Title':<42s}  {col_a:>8s}  {col_b:>8s}")
        w(f"  {'─' * 14}  {'─' * 42}  {'─' * 8}  {'─' * 8}")

        lookup_a = {c["id"]: c for c in clusters_a}
        lookup_b = {c["id"]: c for c in clusters_b}
        for cid in all_ids:
            ca = lookup_a.get(cid)
            cb = lookup_b.get(cid)
            title = (ca or cb)["title"][:42]
            snip_a = f"{ca['snippet_count']}s/{ca['source_count']}src" if ca else "—"
            snip_b = f"{cb['snippet_count']}s/{cb['source_count']}src" if cb else "—"
            marker = ""
            if ca and not cb:
                marker = "  << only A"
            elif cb and not ca:
                marker = "  << only B"
            w(f"  {cid:<14s}  {title:<42s}  {snip_a:>8s}  {snip_b:>8s}{marker}")

    # --- Story arcs stages ---
    for stage_key in ["story_arcs", "story_arcs_ukrainian"]:
        if stage_key not in stages:
            continue
        stage = stages[stage_key]
        leader = {
            "story_arcs": "Mark Carney (English)",
            "story_arcs_ukrainian": "Volodymyr Zelenskyy (Ukrainian)",
        }.get(stage_key, stage_key)

        w("")
        w(f"{'─' * 80}")
        w(f"  STORY ARCS — {leader}")
        w(f"{'─' * 80}")
        w("")
        w(f"  {'':40s}  {col_a:>18s}  {col_b:>18s}")
        w(f"  {'Arcs detected':40s}  {stage[col_a]['arc_count']:>18d}  {stage[col_b]['arc_count']:>18d}")

        max_arcs = max(len(stage[col_a]["arcs"]), len(stage[col_b]["arcs"]))
        for i in range(max_arcs):
            w("")
            arc_a = stage[col_a]["arcs"][i] if i < len(stage[col_a]["arcs"]) else None
            arc_b = stage[col_b]["arcs"][i] if i < len(stage[col_b]["arcs"]) else None

            w(f"  Arc {i + 1}:")
            w(f"    {col_a + ':':10s} {_format_arc(arc_a)}")
            w(f"    {col_b + ':':10s} {_format_arc(arc_b)}")

            match = "SAME" if arc_a and arc_b and arc_a["indices"] == arc_b["indices"] else "DIFFERENT"
            w(f"    verdict:   {match}")

    # --- Title merge ---
    if "title_merge" in stages:
        stage = stages["title_merge"]
        w("")
        w(f"{'─' * 80}")
        w(f"  TITLE MERGE — Mark Carney (English)")
        w(f"{'─' * 80}")
        w("")
        w(f"  Input titles:")
        for t in stage[col_a]["input_titles"]:
            w(f"    - {t}")
        w("")
        w(f"  {col_a + ':':10s} {stage[col_a]['merged_title']}")
        w(f"  {col_b + ':':10s} {stage[col_b]['merged_title']}")

    w("")
    w(f"{'=' * 80}")

    report_path = REPORTS_DIR / "analytical_ab_latest.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(out) + "\n")


def _format_arc(arc):
    """Format a single arc for display."""
    if arc is None:
        return "—"
    titles = [t[:50] + ("..." if len(t) > 50 else "") for t in arc["titles"]]
    return f"indices {arc['indices']}: " + " + ".join(f'"{t}"' for t in titles)
