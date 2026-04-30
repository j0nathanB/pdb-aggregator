"""Baseline prompt-token analysis from existing traces.

Answers three questions ahead of Phase 2 instrumentation landing:

  1. Country agent — does cache_control produce cross-country reuse today?
     (Proxy: if input_tokens is uniform across 28 country calls in a week,
     cache is NOT firing cross-country — every call paid full prompt cost.)

  2. Per-agent baseline hit rates — what's the floor before any caching?
     (All agents except country.py have no cache_control today, so this
     is 0 by construction. Confirmed by enumeration.)

  3. Per-agent prompt-token volume — what's the total leverage budget?

Cache field analysis from extract_usage() is NOT available for these
traces — that instrumentation landed in this same PR and needs the next
Sunday run to produce data. This script makes the most of what's on disk.

Usage:  .venv/bin/python dev/optimize_prompts/baseline_analysis.py
Output: dev/optimize_prompts/baseline_analysis_<today>.md
"""

import json
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEEKS = ["20260419", "20260426"]
DEEP_DIVE_COUNTRIES = ["mx", "de"]


def load_traces(week: str) -> list[dict]:
    out = []
    for p in sorted((PROJECT_ROOT / "briefs" / week / "traces").glob("*.json")):
        try:
            t = json.loads(p.read_text())
            t["_filename"] = p.name
            t["_week"] = week
            out.append(t)
        except (json.JSONDecodeError, OSError):
            pass
    return out


def agent_label(t: dict) -> tuple[str, str]:
    return t.get("agent", "?"), t.get("label", "?")


def usage_in(t: dict) -> int:
    return (t.get("usage") or {}).get("input_tokens") or 0


def usage_out(t: dict) -> int:
    return (t.get("usage") or {}).get("output_tokens") or 0


def per_agent_summary(traces: list[dict]) -> list[dict]:
    by_agent = defaultdict(list)
    for t in traces:
        by_agent[agent_label(t)[0]].append(t)
    rows = []
    for agent, items in sorted(by_agent.items()):
        ins = [usage_in(t) for t in items if usage_in(t) > 0]
        outs = [usage_out(t) for t in items if usage_out(t) > 0]
        if not ins:
            continue
        rows.append({
            "agent": agent,
            "calls": len(items),
            "total_input": sum(ins),
            "total_output": sum(outs),
            "mean_input": int(statistics.mean(ins)),
            "median_input": int(statistics.median(ins)),
            "stdev_input": int(statistics.stdev(ins)) if len(ins) > 1 else 0,
            "min_input": min(ins),
            "max_input": max(ins),
        })
    return rows


def country_cross_country_uniformity(traces: list[dict]) -> dict:
    """Q1 proxy: if input_tokens is uniform across 28 country calls in a week,
    cache_control is NOT producing cross-country reuse."""
    by_week = defaultdict(list)
    for t in traces:
        if t.get("agent") == "country":
            by_week[t["_week"]].append((t.get("label"), usage_in(t)))
    out = {}
    for week, calls in by_week.items():
        ins = [n for _, n in calls if n > 0]
        if not ins:
            continue
        cv = (statistics.stdev(ins) / statistics.mean(ins)) if len(ins) > 1 else 0
        out[week] = {
            "n": len(ins),
            "min": min(ins),
            "max": max(ins),
            "mean": int(statistics.mean(ins)),
            "median": int(statistics.median(ins)),
            "stdev": int(statistics.stdev(ins)) if len(ins) > 1 else 0,
            "coefficient_of_variation": round(cv, 3),
            "calls_sorted": sorted(calls, key=lambda x: x[1] or 0)[:3]
                          + sorted(calls, key=lambda x: x[1] or 0)[-3:],
        }
    return out


def deep_dive_countries(traces: list[dict], codes: list[str]) -> dict:
    """Per-country trace data across both weeks."""
    out = {}
    for code in codes:
        out[code] = []
        for t in traces:
            if t.get("agent") == "country" and t.get("label") == code:
                out[code].append({
                    "week": t["_week"],
                    "input_tokens": usage_in(t),
                    "output_tokens": usage_out(t),
                })
    return out


def render_markdown(per_agent_rows: list[list[dict]], cross_country: dict,
                    deep: dict) -> str:
    lines = [
        f"# Baseline Prompt-Token Analysis — {date.today().isoformat()}",
        "",
        "Source: weekly Sunday pipeline runs at `briefs/20260419` and `briefs/20260426`.",
        "Cache fields are absent from these traces (instrumentation lands in this same PR);",
        "this analysis uses `input_tokens` as a proxy for cache-firing behavior.",
        "",
        "## Q1 — Is country.py's cache_control producing cross-country reuse?",
        "",
        "**Test:** if cache was firing across the 28 country calls per week, calls 2-28",
        "would have much smaller `input_tokens` than call 1 (which writes the cache).",
        "Uniform `input_tokens` across all 28 = cache is NOT producing cross-country reuse.",
        "",
        "Coefficient of variation (stdev/mean) close to 0 = uniform = cache not helping cross-country.",
        "",
    ]
    for week, stats in sorted(cross_country.items()):
        lines.extend([
            f"### Week {week}",
            "",
            f"- Country calls: {stats['n']}",
            f"- input_tokens: min={stats['min']:,}, median={stats['median']:,}, "
            f"mean={stats['mean']:,}, max={stats['max']:,}",
            f"- stdev={stats['stdev']:,}, **coefficient of variation = {stats['coefficient_of_variation']}**",
            "",
            "Lowest 3 + highest 3 by input_tokens:",
            "",
        ])
        for label, n in stats["calls_sorted"]:
            lines.append(f"  - {label}: {n:,}")
        lines.append("")

    lines.extend([
        "## Q2 — Per-agent baseline hit rates",
        "",
        "All agents except `country` have no `cache_control` today — baseline is 0 by",
        "construction. Listing per-agent call counts and token volumes confirms what's",
        "uninstrumented.",
        "",
    ])
    for week_idx, rows in enumerate(per_agent_rows):
        week = WEEKS[week_idx]
        lines.extend([
            f"### Week {week}",
            "",
            "| agent | calls | total input | mean input | median input | stdev | min | max |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ])
        for r in rows:
            lines.append(
                f"| {r['agent']} | {r['calls']} | {r['total_input']:,} | "
                f"{r['mean_input']:,} | {r['median_input']:,} | {r['stdev_input']:,} | "
                f"{r['min_input']:,} | {r['max_input']:,} |"
            )
        lines.append("")

    lines.extend([
        "## Q3 — Per-agent leverage budget",
        "",
        "Total `input_tokens` per agent across both weeks ranks the leverage opportunity.",
        "An agent with 3M input tokens and a stable system prefix beats one with 100K.",
        "",
        "| agent | 2-week total input | 2-week total output | rank by input volume |",
        "|---|---:|---:|---:|",
    ])
    combined = defaultdict(lambda: {"input": 0, "output": 0})
    for rows in per_agent_rows:
        for r in rows:
            combined[r["agent"]]["input"] += r["total_input"]
            combined[r["agent"]]["output"] += r["total_output"]
    ranked = sorted(combined.items(), key=lambda kv: -kv[1]["input"])
    for rank, (agent, c) in enumerate(ranked, 1):
        lines.append(f"| {agent} | {c['input']:,} | {c['output']:,} | {rank} |")
    lines.append("")

    lines.extend([
        f"## Deep dive — {', '.join(DEEP_DIVE_COUNTRIES)} across both weeks",
        "",
        "If country.py's cache was firing on re-runs (same country, different weeks within",
        "5-min TTL — unlikely across week-apart runs but instructive for prompt-size variance),",
        "we'd see it here. Mostly this shows per-country prompt-size baseline.",
        "",
    ])
    for code, rows in deep.items():
        lines.append(f"### {code}")
        lines.append("")
        for r in rows:
            lines.append(f"- week {r['week']}: input={r['input_tokens']:,}, output={r['output_tokens']:,}")
        lines.append("")

    lines.extend([
        "## Verdicts",
        "",
        "**Q1:** See coefficient of variation above. CV < 0.1 = strong evidence cache",
        "is NOT producing cross-country reuse (input_tokens uniform = each call paid full",
        "prompt cost). CV > 0.3 = some calls smaller, possibly cache-related (more likely",
        "ledger-size variance). Definitive answer awaits Sunday run with cache fields.",
        "",
        "**Q2:** Confirmed — every non-country agent has 0% cache hit rate today (no",
        "`cache_control` in their request shape). Floor for Phase 4 hit-rate alerting.",
        "",
        "**Q3:** Top-ranked agents by 2-week input volume are the highest-leverage targets.",
        "Compare to the editor cluster (which has the additional shared-prefix opportunity",
        "across 5 agents) when prioritizing.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    out_dir = PROJECT_ROOT / "dev" / "optimize_prompts"
    all_traces = []
    per_agent_rows = []
    for week in WEEKS:
        traces = load_traces(week)
        all_traces.extend(traces)
        per_agent_rows.append(per_agent_summary(traces))

    cross_country = country_cross_country_uniformity(all_traces)
    deep = deep_dive_countries(all_traces, DEEP_DIVE_COUNTRIES)

    md = render_markdown(per_agent_rows, cross_country, deep)
    out_path = out_dir / f"baseline_analysis_{date.today().isoformat()}.md"
    out_path.write_text(md)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
