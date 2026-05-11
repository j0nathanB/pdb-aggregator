"""
cost_by_stage.py — aggregate per-stage API cost across recent pipeline runs.

Reads briefs/{date}/traces/*.json (one file per API call), buckets calls
by agent (= pipeline stage), and prints two views: per-run breakdown and
cross-run aggregate. Accounts for prompt caching: cache writes at 1.25x
base input, cache reads at 0.1x. Output tokens (incl. extended thinking)
priced at the output rate.

Usage:
    python dev/cost_by_stage.py                 # last 3 runs
    python dev/cost_by_stage.py --last 8
    python dev/cost_by_stage.py --briefs-dir path/to/briefs
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BRIEFS_DIR = REPO_ROOT / "briefs"
DEFAULT_SETTINGS_PATH = REPO_ROOT / "assets" / "country_configs" / "settings.yaml"

# Anthropic 5-min ephemeral cache pricing multipliers, applied to base input.
CACHE_WRITE_MULT = 1.25
CACHE_READ_MULT = 0.10

# Brief dirs are either YYYYMMDD or YYYY-MM-DD; ignore _old/, eval/, etc.
DATE_DIR_RE = re.compile(r"^\d{4}-?\d{2}-?\d{2}$")


def load_prices(settings_path: Path) -> tuple[float, float]:
    """Pull input/output $/Mtok from settings.yaml without a yaml dep."""
    in_cost, out_cost = 3.0, 15.0
    if not settings_path.exists():
        return in_cost, out_cost
    for line in settings_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("input_cost_per_mtok:"):
            in_cost = float(line.split(":", 1)[1].strip())
        elif line.startswith("output_cost_per_mtok:"):
            out_cost = float(line.split(":", 1)[1].strip())
    return in_cost, out_cost


def _as_num(v: Any) -> float:
    """Some traces contain non-numeric usage values (e.g. leaked AsyncMock
    reprs from dev runs). Treat anything non-numeric as 0 rather than crashing."""
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def cost_from_usage(usage: dict[str, Any], in_price: float, out_price: float) -> float:
    """USD cost for a single usage record, including cache pricing."""
    in_tok = _as_num(usage.get("input_tokens"))
    out_tok = _as_num(usage.get("output_tokens"))
    cw = _as_num(usage.get("cache_creation_input_tokens"))
    cr = _as_num(usage.get("cache_read_input_tokens"))
    return (
        in_tok * in_price
        + cw * in_price * CACHE_WRITE_MULT
        + cr * in_price * CACHE_READ_MULT
        + out_tok * out_price
    ) / 1_000_000


def load_run(traces_dir: Path) -> dict[str, dict[str, int]]:
    """Sum usage per agent across all trace files in a run.

    Returns {agent: {input_tokens, output_tokens, cache_creation_input_tokens,
    cache_read_input_tokens, call_count}}.
    """
    by_stage: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 0,
            "cache_read_input_tokens": 0,
            "call_count": 0,
        }
    )
    for trace_path in traces_dir.iterdir():
        if trace_path.suffix != ".json":
            continue
        try:
            trace = json.loads(trace_path.read_text())
        except json.JSONDecodeError:
            continue
        agent = trace.get("agent")
        usage = trace.get("usage")
        if not agent or not isinstance(usage, dict):
            continue
        bucket = by_stage[agent]
        for k in (
            "input_tokens",
            "output_tokens",
            "cache_creation_input_tokens",
            "cache_read_input_tokens",
        ):
            bucket[k] += _as_num(usage.get(k))
        bucket["call_count"] += 1
    return dict(by_stage)


def load_recent_runs(
    briefs_dir: Path, n: int, min_calls: int
) -> list[tuple[str, dict[str, dict[str, int]]]]:
    """Return the most recent n (run_id, by_stage) pairs that have trace data.

    Skips runs with fewer than min_calls traces — those are typically stub
    runs from dev experiments (e.g. a single triage call), not full pipeline
    runs, and would distort the aggregate.
    """
    if not briefs_dir.exists():
        raise FileNotFoundError(f"Briefs directory not found: {briefs_dir}")
    candidates = []
    for run_dir in briefs_dir.iterdir():
        if not run_dir.is_dir() or not DATE_DIR_RE.match(run_dir.name):
            continue
        traces_dir = run_dir / "traces"
        if not traces_dir.is_dir():
            continue
        # Strip dashes so 2026-05-03 sorts alongside 20260503.
        sort_key = run_dir.name.replace("-", "")
        candidates.append((sort_key, run_dir))
    candidates.sort(key=lambda c: c[0], reverse=True)

    out = []
    for _, run_dir in candidates:
        by_stage = load_run(run_dir / "traces")
        total_calls = sum(s["call_count"] for s in by_stage.values())
        if total_calls < min_calls:
            continue
        out.append((run_dir.name, by_stage))
        if len(out) >= n:
            break
    return out


def fmt_per_run(
    run_id: str,
    by_stage: dict[str, dict[str, int]],
    in_price: float,
    out_price: float,
) -> str:
    rows = []
    for stage, u in by_stage.items():
        rows.append((stage, u, cost_from_usage(u, in_price, out_price)))
    rows.sort(key=lambda r: -r[2])
    total = sum(r[2] for r in rows)

    lines = [
        f"\n=== {run_id}   total=${total:.2f} ===",
        f"{'stage':<18} {'calls':>5} {'in (k)':>9} {'cache_w (k)':>11} "
        f"{'cache_r (k)':>11} {'out (k)':>9} {'cost':>9} {'%':>5}",
        "-" * 90,
    ]
    for stage, u, cost in rows:
        pct = (cost / total * 100) if total else 0.0
        lines.append(
            f"{stage:<18} {u['call_count']:>5} "
            f"{u['input_tokens'] / 1000:>9,.1f} "
            f"{u['cache_creation_input_tokens'] / 1000:>11,.1f} "
            f"{u['cache_read_input_tokens'] / 1000:>11,.1f} "
            f"{u['output_tokens'] / 1000:>9,.1f} "
            f"${cost:>7,.2f} {pct:>4.1f}%"
        )
    return "\n".join(lines)


def fmt_aggregate(
    runs: list[tuple[str, dict[str, dict[str, int]]]],
    in_price: float,
    out_price: float,
) -> str:
    """Cross-run averages. The 'in N' column flags stages that don't run every
    week — useful to avoid misreading a sometimes-stage as a cheap stage."""
    agg: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "input_tokens": 0.0,
            "output_tokens": 0.0,
            "cache_creation_input_tokens": 0.0,
            "cache_read_input_tokens": 0.0,
            "call_count": 0.0,
            "runs": 0,
        }
    )
    for _, by_stage in runs:
        for stage, u in by_stage.items():
            b = agg[stage]
            for k in (
                "input_tokens",
                "output_tokens",
                "cache_creation_input_tokens",
                "cache_read_input_tokens",
                "call_count",
            ):
                b[k] += u[k]
            b["runs"] += 1

    n = len(runs)
    rows = []
    for stage, b in agg.items():
        avg_usage = {
            "input_tokens": b["input_tokens"] / n,
            "output_tokens": b["output_tokens"] / n,
            "cache_creation_input_tokens": b["cache_creation_input_tokens"] / n,
            "cache_read_input_tokens": b["cache_read_input_tokens"] / n,
        }
        avg_cost = cost_from_usage(avg_usage, in_price, out_price)
        rows.append(
            (
                stage,
                avg_usage,
                b["call_count"] / n,
                avg_cost,
                int(b["runs"]),
            )
        )
    rows.sort(key=lambda r: -r[3])
    total = sum(r[3] for r in rows)

    lines = [
        f"\n=== AGGREGATE (avg per run across {n} runs)   total=${total:.2f} ===",
        f"{'stage':<18} {'calls':>5} {'in (k)':>9} {'cache_w (k)':>11} "
        f"{'cache_r (k)':>11} {'out (k)':>9} {'cost':>9} {'%':>5} {'in N':>6}",
        "-" * 98,
    ]
    for stage, u, avg_calls, cost, run_count in rows:
        pct = (cost / total * 100) if total else 0.0
        lines.append(
            f"{stage:<18} {avg_calls:>5.1f} "
            f"{u['input_tokens'] / 1000:>9,.1f} "
            f"{u['cache_creation_input_tokens'] / 1000:>11,.1f} "
            f"{u['cache_read_input_tokens'] / 1000:>11,.1f} "
            f"{u['output_tokens'] / 1000:>9,.1f} "
            f"${cost:>7,.2f} {pct:>4.1f}% {run_count:>4}/{n}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--last", type=int, default=3, help="Number of recent runs (default 3)")
    parser.add_argument("--briefs-dir", type=Path, default=DEFAULT_BRIEFS_DIR)
    parser.add_argument("--settings", type=Path, default=DEFAULT_SETTINGS_PATH)
    parser.add_argument(
        "--min-calls",
        type=int,
        default=20,
        help="Skip runs with fewer than this many trace files (default 20 — filters "
        "stub/partial runs like a single triage call from a dev experiment)",
    )
    args = parser.parse_args()

    in_price, out_price = load_prices(args.settings)
    print(
        f"Prices: ${in_price}/Mtok in, ${out_price}/Mtok out  "
        f"(cache write ×{CACHE_WRITE_MULT}, cache read ×{CACHE_READ_MULT})"
    )

    runs = load_recent_runs(args.briefs_dir, args.last, args.min_calls)
    if not runs:
        print(f"No runs with trace data found under {args.briefs_dir}")
        return

    for run_id, by_stage in runs:
        print(fmt_per_run(run_id, by_stage, in_price, out_price))

    if len(runs) > 1:
        print(fmt_aggregate(runs, in_price, out_price))


if __name__ == "__main__":
    main()
