"""
Evaluation harness for the copyedit/style-edit order change.

Runs two configurations on the same post-editor input and produces side-by-side
diffs + scorer JSON.

Config A (current):   post-editor → copyedit (current prompt) → style-edit
Config B (proposed):  post-editor → style-edit → copyedit (narrowed prompt)

Both configurations are coupled on purpose — the narrowed prompt assumes it
runs after the style editor. We are evaluating the coupled change, not
factoring it into a 2×2.

Usage:
    # Smoke run on a single country
    .venv/bin/python dev/eval_copyedit_order/harness.py \\
        --date 2026-04-12 --sections de --n 1

    # Full countries run
    .venv/bin/python dev/eval_copyedit_order/harness.py \\
        --date 2026-04-12 --countries-only --n 3

    # With style-preservation rubric on a stratified sample
    .venv/bin/python dev/eval_copyedit_order/harness.py \\
        --date 2026-04-12 --countries-only --n 3 --rubric-sample de,ua,jp,in,mx,executive
"""

import argparse
import asyncio
import json
import logging
import sys
import time
from datetime import date, datetime
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load .env before importing monitor.config (which snapshots ANTHROPIC_API_KEY
# at import time). Matches the pattern used by src/monitor/collection/*.py.
from dotenv import load_dotenv  # noqa: E402
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from monitor.config import ANTHROPIC_API_KEY, MODEL, PROJECT_ROOT, THINKING_BUDGET_TOKENS  # noqa: E402
from monitor.newsletter.structured_copyeditor import COPYEDITOR_SYSTEM, _copyedit_prose  # noqa: E402
from monitor.newsletter.structured_editor import style_edit_prose  # noqa: E402

from scorers import counts, extract_prose, load_leader_refs, score_all  # noqa: E402

# Expected top-level keys per label kind — anything else is a JSON-integrity
# signal (the LLM invented a spurious field, typically because it mis-escaped
# an inner quote and prematurely closed a string).
EXPECTED_KEYS = {
    "country": {"narrative_body", "other_stories"},
    "regional": {"headline", "regional_lead", "gap_paragraphs", "card_summary"},
    "executive": {"headline", "edited_essay"},
}


def _classify_label(label: str) -> str:
    if label == "executive":
        return "executive"
    if label.startswith("regional_"):
        return "regional"
    return "country"


def _unexpected_keys(label: str, final: dict) -> list[str]:
    if not isinstance(final, dict):
        return []
    allowed = EXPECTED_KEYS[_classify_label(label)]
    return [k for k in final.keys() if k not in allowed]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("eval")
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("monitor").setLevel(logging.WARNING)


NARROWED_PROMPT_PATH = PROJECT_ROOT / "assets" / "prompts" / "editors" / "structured_copyeditor_narrowed.md"
NARROWED_COPYEDITOR = NARROWED_PROMPT_PATH.read_text()
CURRENT_COPYEDITOR = COPYEDITOR_SYSTEM


# ---------------------------------------------------------------------------
# Trace loading
# ---------------------------------------------------------------------------

def load_editor_output(run_date: date, label: str) -> dict:
    """Load the parsed output of editor_{label}.json — the shared input for both configs."""
    path = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / "traces" / f"editor_{label}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    t = json.loads(path.read_text())
    parsed = t.get("output", {}).get("parsed")
    if not isinstance(parsed, dict):
        raise ValueError(f"No parsed output in {path}")
    return parsed


def _section_codes(label: str, all_country_codes: list[str]) -> list[str]:
    if label == "executive":
        return list(all_country_codes)
    if label.startswith("regional_"):
        from monitor.config import load_country_config
        region_name = label[len("regional_"):]
        codes = []
        for code in all_country_codes:
            try:
                cfg = load_country_config(code)
            except FileNotFoundError:
                continue
            if getattr(cfg, "region", None) and cfg.region.value == region_name:
                codes.append(code)
        return codes
    return [label] if label in all_country_codes else []


def _all_country_codes() -> list[str]:
    d = PROJECT_ROOT / "assets" / "country_configs" / "countries"
    return sorted(p.stem for p in d.glob("*.yaml"))


# ---------------------------------------------------------------------------
# Config runners
# ---------------------------------------------------------------------------

async def run_config_a(
    editor_output: dict, label: str, country_codes: list[str],
    run_date: date, trace_root: Path,
) -> dict:
    """Current chain: copyedit (current prompt) → style."""
    cp = await _copyedit_prose(
        editor_output, label, run_date,
        country_codes=country_codes,
        system_prompt_text=CURRENT_COPYEDITOR,
        trace_root=trace_root,
    )
    final = await style_edit_prose(cp, label, run_date, trace_root=trace_root)
    return final


async def run_config_b(
    editor_output: dict, label: str, country_codes: list[str],
    run_date: date, trace_root: Path,
) -> dict:
    """Proposed chain: style → narrowed-copyedit."""
    st = await style_edit_prose(editor_output, label, run_date, trace_root=trace_root)
    final = await _copyedit_prose(
        st, label, run_date,
        country_codes=country_codes,
        system_prompt_text=NARROWED_COPYEDITOR,
        trace_root=trace_root,
    )
    return final


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

async def run_one(
    label: str, editor_output: dict, all_codes: list[str],
    run_date: date, eval_root: Path, n: int,
) -> dict:
    """Run Config A and Config B n times each on one section."""
    codes = _section_codes(label, all_codes)
    refs = load_leader_refs(codes)

    section_result: dict = {"label": label, "runs": []}

    for repeat in range(1, n + 1):
        trace_a = eval_root / f"config_a_r{repeat}"
        trace_b = eval_root / f"config_b_r{repeat}"

        t0 = time.time()
        try:
            final_a = await run_config_a(editor_output, label, codes, run_date, trace_a)
            text_a = extract_prose(final_a)
            scored_a = score_all(text_a, refs)
        except Exception as e:
            log.exception("Config A failed for %s r%d: %s", label, repeat, e)
            final_a, text_a, scored_a = {}, "", {k: [] for k in
                ("bare_acronyms", "acronym_chain_breaks", "stale_titles", "foreign_quote_leakage")}

        try:
            final_b = await run_config_b(editor_output, label, codes, run_date, trace_b)
            text_b = extract_prose(final_b)
            scored_b = score_all(text_b, refs)
        except Exception as e:
            log.exception("Config B failed for %s r%d: %s", label, repeat, e)
            final_b, text_b, scored_b = {}, "", {k: [] for k in
                ("bare_acronyms", "acronym_chain_breaks", "stale_titles", "foreign_quote_leakage")}

        elapsed = time.time() - t0

        section_result["runs"].append({
            "repeat": repeat,
            "elapsed_s": round(elapsed, 1),
            "config_a": {
                "final": final_a,
                "char_count": len(text_a),
                "counts": counts(scored_a),
                "hits": scored_a,
                "unexpected_keys": _unexpected_keys(label, final_a),
            },
            "config_b": {
                "final": final_b,
                "char_count": len(text_b),
                "counts": counts(scored_b),
                "hits": scored_b,
                "unexpected_keys": _unexpected_keys(label, final_b),
            },
        })
        log.info("%s r%d done in %.1fs — A %s | B %s",
                 label, repeat, elapsed,
                 section_result["runs"][-1]["config_a"]["counts"],
                 section_result["runs"][-1]["config_b"]["counts"])
    return section_result


async def run_all(
    run_date: date, labels: list[str], eval_root: Path,
    n: int, concurrency: int,
) -> dict:
    all_codes = _all_country_codes()
    sem = asyncio.Semaphore(concurrency)

    async def _bounded(label: str) -> dict:
        async with sem:
            try:
                editor_output = load_editor_output(run_date, label)
            except FileNotFoundError:
                log.warning("skip %s: no editor trace", label)
                return {"label": label, "skipped": "no_editor_trace"}
            return await run_one(label, editor_output, all_codes, run_date, eval_root, n)

    results = await asyncio.gather(*[_bounded(l) for l in labels])
    return {
        "run_date": run_date.isoformat(),
        "eval_root": str(eval_root),
        "n": n,
        "model": MODEL,
        "thinking_budget": THINKING_BUDGET_TOKENS,
        "labels": labels,
        "sections": {r["label"]: r for r in results},
    }


# ---------------------------------------------------------------------------
# Aggregation & diffs
# ---------------------------------------------------------------------------

def aggregate_scorer_counts(results: dict) -> dict:
    totals_a = {"bare_acronyms": 0, "acronym_chain_breaks": 0, "stale_titles": 0, "foreign_quote_leakage": 0}
    totals_b = dict(totals_a)
    bad_json_a = []  # [(label, repeat, unexpected_keys)]
    bad_json_b = []
    n_runs_a = 0
    n_runs_b = 0
    for label, section in results["sections"].items():
        if "runs" not in section:
            continue
        for run in section["runs"]:
            for k, v in run["config_a"]["counts"].items():
                totals_a[k] += v
            for k, v in run["config_b"]["counts"].items():
                totals_b[k] += v
            if run["config_a"].get("unexpected_keys"):
                bad_json_a.append([label, run["repeat"], run["config_a"]["unexpected_keys"]])
            if run["config_b"].get("unexpected_keys"):
                bad_json_b.append([label, run["repeat"], run["config_b"]["unexpected_keys"]])
            n_runs_a += 1
            n_runs_b += 1
    return {
        "config_a": {
            "totals": totals_a,
            "avg_per_run": {k: round(v / max(1, n_runs_a), 3) for k, v in totals_a.items()},
            "n_runs": n_runs_a,
            "json_integrity_violations": bad_json_a,
        },
        "config_b": {
            "totals": totals_b,
            "avg_per_run": {k: round(v / max(1, n_runs_b), 3) for k, v in totals_b.items()},
            "n_runs": n_runs_b,
            "json_integrity_violations": bad_json_b,
        },
        "delta_b_minus_a": {k: totals_b[k] - totals_a[k] for k in totals_a},
    }


def write_section_diff(results: dict, eval_root: Path) -> None:
    comparison_dir = eval_root / "comparison"
    comparison_dir.mkdir(parents=True, exist_ok=True)

    for label, section in results["sections"].items():
        if "runs" not in section:
            continue
        # Use repeat 1 for the diff
        run0 = section["runs"][0]
        a = run0["config_a"]
        b = run0["config_b"]
        out = comparison_dir / f"{label}.diff.md"

        lines = [
            f"# {label} — Config A vs Config B (repeat 1)",
            "",
            "## Scorer counts across all repeats",
            "",
            "| scorer | A (mean) | B (mean) |",
            "| --- | --- | --- |",
        ]
        a_totals = {k: 0 for k in a["counts"]}
        b_totals = dict(a_totals)
        for run in section["runs"]:
            for k, v in run["config_a"]["counts"].items():
                a_totals[k] += v
            for k, v in run["config_b"]["counts"].items():
                b_totals[k] += v
        n = len(section["runs"])
        for k in a_totals:
            lines.append(f"| {k} | {a_totals[k] / n:.2f} | {b_totals[k] / n:.2f} |")
        lines += ["", "## Config A (current: copyedit → style)", "", "```",
                  extract_prose(a["final"]), "```", "",
                  "## Config B (proposed: style → narrowed-copyedit)", "", "```",
                  extract_prose(b["final"]), "```"]
        out.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Style-preservation rubric
# ---------------------------------------------------------------------------

async def rubric_score(
    label: str, editor_output: dict, config_a_final: dict, config_b_final: dict,
    eval_root: Path, run_date: date,
) -> dict:
    """Single LLM call that scores both configs on 4 style-preservation dimensions."""
    import anthropic  # local — avoid import cost in non-rubric runs

    from monitor.rate_limit import anthropic_limiter
    from monitor.trace import save_raw_response, update_trace_parsed, extract_thinking, extract_usage
    from monitor.sanitize import extract_json

    rubric_prompt = (Path(__file__).resolve().parent / "rubric_prompt.md").read_text()

    payload = {
        "label": label,
        "editor_output": extract_prose(editor_output),
        "config_a_final": extract_prose(config_a_final),
        "config_b_final": extract_prose(config_b_final),
    }

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY, timeout=1200.0)
    async with anthropic_limiter():
        async with client.messages.stream(
            model=MODEL,
            max_tokens=THINKING_BUDGET_TOKENS + 4096,
            temperature=1,
            thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
            system=[{"type": "text", "text": rubric_prompt}],
            messages=[{"role": "user", "content": json.dumps(payload, indent=2, ensure_ascii=False)}],
        ) as stream:
            response = await stream.get_final_message()

    response_text = "\n".join(b.text for b in response.content if b.type == "text")

    trace_root = eval_root / "rubric"
    save_raw_response(
        "rubric", label, run_date,
        system_prompt=rubric_prompt, user_message=json.dumps(payload, ensure_ascii=False),
        response_text=response_text,
        thinking_text=extract_thinking(response), usage=extract_usage(response),
        trace_root=trace_root,
    )

    try:
        data = extract_json(response_text, context=f"rubric_{label}")
    except Exception as e:
        log.warning("rubric parse failed for %s: %s", label, e)
        return {"label": label, "error": str(e), "raw": response_text[:500]}

    update_trace_parsed("rubric", label, run_date, parsed_output=data, trace_root=trace_root)
    return {"label": label, "scores": data}


async def run_rubric(
    results: dict, run_date: date, eval_root: Path, sample_labels: list[str],
) -> list[dict]:
    scores = []
    for label in sample_labels:
        section = results["sections"].get(label)
        if not section or "runs" not in section:
            continue
        try:
            editor_output = load_editor_output(run_date, label)
        except FileNotFoundError:
            continue
        # Use repeat 1 for rubric to keep cost flat
        run0 = section["runs"][0]
        r = await rubric_score(label, editor_output,
                                run0["config_a"]["final"], run0["config_b"]["final"],
                                eval_root, run_date)
        scores.append(r)
        log.info("rubric %s: %s", label, r.get("scores", {}).get("config_a", "err"))
    return scores


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_date(s: str) -> date:
    if "-" in s:
        return datetime.strptime(s, "%Y-%m-%d").date()
    return datetime.strptime(s, "%Y%m%d").date()


def _resolve_labels(run_date: date, sections_arg: str | None, countries_only: bool) -> list[str]:
    traces_dir = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / "traces"
    editor_labels = sorted(p.stem[len("editor_"):] for p in traces_dir.glob("editor_*.json"))

    if sections_arg:
        requested = [s.strip() for s in sections_arg.split(",") if s.strip()]
        missing = [s for s in requested if s not in editor_labels]
        if missing:
            log.warning("no editor trace for: %s", ", ".join(missing))
        return [s for s in requested if s in editor_labels]

    if countries_only:
        return [l for l in editor_labels
                if not l.startswith("regional_") and l != "executive"]

    return editor_labels


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD or YYYYMMDD")
    ap.add_argument("--sections", default=None, help="comma-separated label list (default: all)")
    ap.add_argument("--countries-only", action="store_true")
    ap.add_argument("--n", type=int, default=1, help="repeats per (section, config)")
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--run-id", default=None, help="subdir under briefs/{date}/eval/ (default: timestamp)")
    ap.add_argument("--rubric-sample", default=None,
                     help="comma-separated labels to run style-preservation rubric on")
    args = ap.parse_args()

    if not ANTHROPIC_API_KEY:
        raise SystemExit("ANTHROPIC_API_KEY not set")

    run_date = _parse_date(args.date)
    labels = _resolve_labels(run_date, args.sections, args.countries_only)
    if not labels:
        raise SystemExit("no labels to run")

    run_id = args.run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    eval_root = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / "eval" / run_id
    eval_root.mkdir(parents=True, exist_ok=True)

    log.info("eval_root: %s", eval_root)
    log.info("labels (%d): %s", len(labels), ", ".join(labels))
    log.info("n=%d, concurrency=%d, model=%s", args.n, args.concurrency, MODEL)

    results = await run_all(run_date, labels, eval_root, args.n, args.concurrency)

    aggregated = aggregate_scorer_counts(results)
    log.info("aggregated: %s", json.dumps(aggregated, indent=2))

    # Write per-section diffs + summary
    write_section_diff(results, eval_root)

    summary_path = eval_root / "summary.json"
    summary = {"aggregated": aggregated, "results": results}
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    log.info("wrote %s", summary_path)

    if args.rubric_sample:
        sample = [s.strip() for s in args.rubric_sample.split(",") if s.strip()]
        log.info("running rubric on %d sections: %s", len(sample), sample)
        rubric_scores = await run_rubric(results, run_date, eval_root, sample)
        (eval_root / "rubric.json").write_text(json.dumps(rubric_scores, indent=2, ensure_ascii=False))
        log.info("wrote %s", eval_root / "rubric.json")


if __name__ == "__main__":
    asyncio.run(main())
