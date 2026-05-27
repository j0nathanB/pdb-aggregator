"""
Baseline pass: score a published brief's final (post-style-editor) prose on
all four mechanical scorers. No API calls. Writes a JSON report summarising
per-section hits plus a per-scorer total so we can judge whether any scorer
has headroom before running the full eval.

Usage:
    .venv/bin/python dev/eval_copyedit_order/baseline.py --date 2026-04-12
    .venv/bin/python dev/eval_copyedit_order/baseline.py --date 2026-04-12 --out baseline.json
"""

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src"
sys.path.insert(0, str(SRC))

from monitor.config import PROJECT_ROOT  # noqa: E402

from scorers import (  # noqa: E402
    counts,
    extract_prose,
    load_leader_refs,
    score_all,
)


REGIONAL_LABEL_RE = "regional_"
EXECUTIVE_LABEL = "executive"


def _parse_date(s: str) -> date:
    if "-" in s:
        return datetime.strptime(s, "%Y-%m-%d").date()
    return datetime.strptime(s, "%Y%m%d").date()


def _section_codes(label: str, all_country_codes: list[str]) -> list[str]:
    """For a given trace label, which country configs scope the leader ref?
    Mirrors production — country label → that country; regional → its region
    members; executive → every country.
    """
    if label == EXECUTIVE_LABEL:
        return list(all_country_codes)
    if label.startswith(REGIONAL_LABEL_RE):
        # Build region → codes mapping by walking country configs
        from monitor.config import load_country_config
        region_name = label[len(REGIONAL_LABEL_RE):]
        codes = []
        for code in all_country_codes:
            try:
                cfg = load_country_config(code)
            except FileNotFoundError:
                continue
            if getattr(cfg, "region", None) and cfg.region.value == region_name:
                codes.append(code)
        return codes
    # Plain country label
    return [label] if label in all_country_codes else []


def _all_country_codes() -> list[str]:
    d = PROJECT_ROOT / "assets" / "country_configs" / "countries"
    return sorted(p.stem for p in d.glob("*.yaml"))


def run_baseline(run_date: date) -> dict:
    traces_dir = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / "traces"
    if not traces_dir.exists():
        raise SystemExit(f"No traces dir: {traces_dir}")

    all_codes = _all_country_codes()

    sections: dict[str, dict] = {}
    totals: dict[str, int] = {"bare_acronyms": 0, "acronym_chain_breaks": 0,
                               "stale_titles": 0, "foreign_quote_leakage": 0}

    for path in sorted(traces_dir.glob("style_editor_*.json")):
        label = path.stem[len("style_editor_"):]
        # Skip at-a-glance — different prompt, not in scope
        if label in ("at_a_glance", "watchlist"):
            continue
        trace = json.loads(path.read_text())
        parsed = trace.get("output", {}).get("parsed")
        if not parsed:
            continue
        text = extract_prose(parsed)
        codes = _section_codes(label, all_codes)
        refs = load_leader_refs(codes)
        scored = score_all(text, refs)
        c = counts(scored)
        sections[label] = {
            "char_count": len(text),
            "leader_refs_loaded": len(refs),
            "counts": c,
            "hits": scored,
        }
        for k, v in c.items():
            totals[k] += v

    return {
        "run_date": run_date.isoformat(),
        "section_count": len(sections),
        "totals": totals,
        "per_section_avg": {k: round(v / max(1, len(sections)), 3)
                             for k, v in totals.items()},
        "sections": sections,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD or YYYYMMDD")
    ap.add_argument("--out", default=None,
                     help="output path (default: briefs/{date}/eval/baseline.json)")
    args = ap.parse_args()

    run_date = _parse_date(args.date)
    report = run_baseline(run_date)

    if args.out:
        out = Path(args.out)
    else:
        out = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / "eval" / "baseline.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False))

    print(f"wrote {out}")
    print(f"sections: {report['section_count']}")
    print(f"totals: {report['totals']}")
    print(f"avg per section: {report['per_section_avg']}")


if __name__ == "__main__":
    main()
