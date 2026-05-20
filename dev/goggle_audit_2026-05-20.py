"""Aggregate audit of story_map noise across recent weekly runs.

Reads story_map_*.json traces from N runs, diffs each call's input URLs
against the kept URLs (stories/single_source/unassigned), and surfaces:

- Per-country: total volume, % from boosted sources, top unboosted domains,
  and post-fetch-discard leak count (should be 0 after 2026-05-11).
- Cross-country: top noise domains (discard candidates) and top noise
  (domain, path-prefix) combos (off_topic_filters.csv candidates).

Replaces the one-run snapshot in dev/goggle_audit_2026-04-12.md.

Usage:
    .venv/bin/python dev/goggle_audit_2026-05-20.py
    .venv/bin/python dev/goggle_audit_2026-05-20.py --runs 20260503 20260510 20260517
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from monitor.collection.brave import (  # noqa: E402
    GLOBAL_ALLOWLIST_PATH,
    GLOBAL_DISCARDS_PATH,
    GOGGLES_DIR,
    OFF_TOPIC_FILTERS_PATH,
    _is_discarded,
    _is_off_topic_url,
    _load_off_topic_filters,
    _parse_global_allowlist,
    _parse_global_discards,
    _parse_goggle_boosts,
    _parse_goggle_discards,
)

DEFAULT_RUNS = ["20260419", "20260426", "20260503", "20260510", "20260517"]

NOISE_RATE_THRESHOLD = 0.80
MIN_VOLUME_DOMAIN = 30
MIN_VOLUME_PATH = 20

URL_IN_RE = re.compile(r"URL:\s+(https?://\S+)")
URL_ANY_RE = re.compile(r"https?://[^\s\"'<>]+")


def extract_domain(url: str) -> str:
    try:
        host = (urlparse(url).hostname or "").lower()
    except Exception:
        return ""
    if host.startswith("www."):
        host = host[4:]
    return host


def path_prefix(url: str, depth: int = 1) -> str:
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        return "/"
    return "/" + "/".join(parts[:depth]) + "/"


def parse_output_urls(response_text: str) -> set[str]:
    """Extract URLs the LLM kept (stories/single_source/unassigned).

    Story_map traces come in two shapes: tool_use serialized via
    json.dumps(..., indent=2) (raw JSON), or text-path output wrapped in
    ```json fences. Strip the fence then parse; fall back to regex if
    parse fails (json_repair fallbacks can be structurally weird)."""
    if not response_text:
        return set()
    text = response_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return set(URL_ANY_RE.findall(text))
    urls: set[str] = set()
    for story in data.get("stories", []) or []:
        for a in story.get("articles", []) or []:
            if u := a.get("url"):
                urls.add(u)
        for u in story.get("representative_urls", []) or []:
            urls.add(u)
    for item in data.get("single_source_items", []) or []:
        if u := item.get("url"):
            urls.add(u)
    for item in data.get("unassigned", []) or []:
        if u := item.get("url"):
            urls.add(u)
    return urls


def load_trace(path: Path) -> tuple[list[str], set[str]] | None:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    user_msg = data.get("input", {}).get("user_message", "")
    output_text = data.get("output", {}).get("response_text", "")
    return URL_IN_RE.findall(user_msg), parse_output_urls(output_text)


def is_boosted(domain: str, boosts: frozenset[str]) -> bool:
    if not domain or not boosts:
        return False
    if domain in boosts:
        return True
    return any(domain.endswith("." + b) for b in boosts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--runs", nargs="+", default=DEFAULT_RUNS)
    parser.add_argument("--briefs-dir", type=Path, default=REPO_ROOT / "briefs")
    parser.add_argument(
        "--out", type=Path, default=REPO_ROOT / "dev" / "goggle_audit_2026-05-20.md"
    )
    args = parser.parse_args()

    global_discards = _parse_global_discards(GLOBAL_DISCARDS_PATH)
    global_allowlist = _parse_global_allowlist(GLOBAL_ALLOWLIST_PATH)
    off_topic_rules = _load_off_topic_filters(OFF_TOPIC_FILTERS_PATH)

    # Aggregations across all runs
    cc_domain: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"input": 0, "kept": 0}
    )
    domain_totals: dict[str, dict[str, int]] = defaultdict(
        lambda: {"input": 0, "kept": 0, "countries": set()}
    )
    domain_path: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"input": 0, "kept": 0, "countries": set(), "off_topic_covered": 0}
    )
    country_meta: dict[str, dict] = defaultdict(
        lambda: {"items": 0, "runs": 0, "discard_leaks": 0, "off_topic_covered_kept": 0}
    )

    country_boosts: dict[str, frozenset[str]] = {}
    country_discards: dict[str, frozenset[str]] = {}

    runs_used = []
    for run_id in args.runs:
        run_dir = args.briefs_dir / run_id / "traces"
        if not run_dir.exists():
            print(f"WARN: {run_dir} not found, skipping", file=sys.stderr)
            continue
        traces = sorted(run_dir.glob("story_map_*.json"))
        if not traces:
            print(f"WARN: no story_map traces in {run_dir}, skipping", file=sys.stderr)
            continue
        runs_used.append(run_id)
        for trace_path in traces:
            cc = trace_path.stem.removeprefix("story_map_")
            result = load_trace(trace_path)
            if result is None:
                continue
            input_urls, kept_urls = result
            if cc not in country_boosts:
                gp = GOGGLES_DIR / f"{cc}.goggle"
                country_boosts[cc] = _parse_goggle_boosts(gp)
                country_discards[cc] = _parse_goggle_discards(gp) | global_discards

            country_meta[cc]["runs"] += 1
            country_meta[cc]["items"] += len(input_urls)

            for url in input_urls:
                domain = extract_domain(url)
                if not domain:
                    continue
                kept = url in kept_urls

                cc_domain[(cc, domain)]["input"] += 1
                domain_totals[domain]["input"] += 1
                domain_totals[domain]["countries"].add(cc)

                p = path_prefix(url)
                dp_key = (domain, p)
                domain_path[dp_key]["input"] += 1
                domain_path[dp_key]["countries"].add(cc)
                if _is_off_topic_url(url, off_topic_rules):
                    domain_path[dp_key]["off_topic_covered"] += 1

                if kept:
                    cc_domain[(cc, domain)]["kept"] += 1
                    domain_totals[domain]["kept"] += 1
                    domain_path[dp_key]["kept"] += 1

                if _is_discarded(domain, country_discards[cc]):
                    country_meta[cc]["discard_leaks"] += 1

    if not runs_used:
        print("ERROR: no runs with story_map traces found", file=sys.stderr)
        sys.exit(1)

    # Build report
    lines: list[str] = []
    lines.append(f"# Goggle audit — {' + '.join(runs_used)}")
    lines.append("")
    lines.append(
        f"Aggregate of {len(runs_used)} weekly story_map runs ({len(country_meta)} "
        f"countries). For each (country, domain), counts URLs sent to story_map vs "
        f"URLs that survived in the LLM's stories/single_source/unassigned output. "
        f"Diff = URLs the LLM rejected as noise. Thresholds for surfacing candidates: "
        f"drop-rate ≥ {int(NOISE_RATE_THRESHOLD * 100)}% AND ≥ {MIN_VOLUME_DOMAIN} "
        f"items (domains) / ≥ {MIN_VOLUME_PATH} items (paths)."
    )
    lines.append("")
    lines.append(
        f"Production filters in effect during these runs (where deployed): "
        f"`_global_discards.txt` ({len(global_discards)} domains), per-country goggle "
        f"`$discard`, `off_topic_filters.csv` ({len(off_topic_rules)} rules). "
        f"Discard leaks below should be ≈0 for runs ≥ 2026-05-11."
    )
    lines.append("")

    # Cross-country noise domains (discard candidates)
    lines.append("## Cross-country noise domains (discard candidates)")
    lines.append("")
    lines.append(
        "Domains that appear in ≥2 countries with high drop rate. Add to "
        "`_global_discards.txt` if the noise is structural (off-topic / "
        "spam / wrong-language / non-news). Domains touching a single country "
        "are listed in that country's section below."
    )
    lines.append("")
    candidates_global: list[tuple[str, int, int, int]] = []
    for domain, agg in domain_totals.items():
        inp = agg["input"]
        kept = agg["kept"]
        countries = len(agg["countries"])
        if inp < MIN_VOLUME_DOMAIN or countries < 2:
            continue
        drop_rate = (inp - kept) / inp
        if drop_rate < NOISE_RATE_THRESHOLD:
            continue
        # Skip domains already in any discard list (verifying, not surfacing)
        if domain in global_discards:
            continue
        candidates_global.append((domain, inp, kept, countries))
    candidates_global.sort(key=lambda x: -x[1])
    lines.append("| Domain | Input | Kept | Drop % | Countries |")
    lines.append("|---|---:|---:|---:|---:|")
    for domain, inp, kept, countries in candidates_global[:40]:
        drop_pct = 100 * (inp - kept) / inp
        lines.append(f"| {domain} | {inp} | {kept} | {drop_pct:.0f}% | {countries} |")
    if not candidates_global:
        lines.append("| _none above threshold_ | | | | |")
    lines.append("")

    # Cross-country noise paths (off_topic_filters.csv candidates)
    lines.append("## Cross-country noise paths (off_topic_filters.csv candidates)")
    lines.append("")
    lines.append(
        "(domain, path-prefix) combos where the LLM drops most URLs. Strong "
        "candidates for adding to `off_topic_filters.csv`. Already-covered rows "
        "are flagged so you can ignore them."
    )
    lines.append("")
    path_candidates: list[tuple[str, str, int, int, int, bool]] = []
    for (domain, prefix), agg in domain_path.items():
        inp = agg["input"]
        kept = agg["kept"]
        if inp < MIN_VOLUME_PATH:
            continue
        drop_rate = (inp - kept) / inp
        if drop_rate < NOISE_RATE_THRESHOLD:
            continue
        # Skip noise-by-default paths (root or single-segment landing pages)
        if prefix in ("/", "//"):
            continue
        countries = len(agg["countries"])
        already = agg["off_topic_covered"] >= inp * 0.5
        path_candidates.append((domain, prefix, inp, kept, countries, already))
    path_candidates.sort(key=lambda x: -x[2])
    lines.append("| Domain | Path | Input | Kept | Drop % | Countries | Already covered |")
    lines.append("|---|---|---:|---:|---:|---:|:---:|")
    for domain, prefix, inp, kept, countries, already in path_candidates[:60]:
        drop_pct = 100 * (inp - kept) / inp
        mark = "✓" if already else ""
        lines.append(
            f"| {domain} | {prefix} | {inp} | {kept} | {drop_pct:.0f}% | {countries} | {mark} |"
        )
    if not path_candidates:
        lines.append("| _none above threshold_ | | | | | | |")
    lines.append("")

    # Per-country
    lines.append("## Per-country breakdown")
    lines.append("")
    for cc in sorted(country_meta.keys()):
        meta = country_meta[cc]
        boosts = country_boosts.get(cc, frozenset())
        effective_boosts = boosts | global_allowlist
        total = meta["items"]
        boosted_count = sum(
            cnt["input"]
            for (c, d), cnt in cc_domain.items()
            if c == cc and is_boosted(d, effective_boosts)
        )
        pct_boosted = (100 * boosted_count / total) if total else 0.0
        lines.append(
            f"### {cc.upper()}  "
            f"({total:,} items / {meta['runs']} runs, "
            f"{pct_boosted:.0f}% boosted, "
            f"{len(boosts)} $boost · {len(country_discards.get(cc, frozenset()) - global_discards)} "
            f"$discard in goggle)"
        )
        lines.append("")
        if meta["discard_leaks"]:
            lines.append(
                f"⚠️  **{meta['discard_leaks']} discard leak(s)** — post-fetch filter "
                f"should have caught these. Likely from runs predating the 2026-05-11 "
                f"deployment of the filter."
            )
            lines.append("")
        cc_unboosted = [
            (d, cnt["input"], cnt["kept"])
            for (c, d), cnt in cc_domain.items()
            if c == cc and not is_boosted(d, effective_boosts)
        ]
        cc_unboosted.sort(key=lambda x: -x[1])
        lines.append("**Top 15 unboosted domains:**")
        lines.append("")
        lines.append("| Domain | Input | Kept | Drop % |")
        lines.append("|---|---:|---:|---:|")
        for d, inp, kept in cc_unboosted[:15]:
            drop_pct = 100 * (inp - kept) / inp if inp else 0
            flag = ""
            if d in global_discards or d in country_discards.get(cc, frozenset()):
                flag = " ⚠ already discarded"
            lines.append(f"| {d} | {inp} | {kept} | {drop_pct:.0f}%{flag} |")
        lines.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n")

    # Console summary
    print(f"Wrote audit to {args.out}")
    print(f"  Runs: {', '.join(runs_used)}")
    print(f"  Countries: {len(country_meta)}")
    print(f"  Cross-country discard candidates: {len(candidates_global)}")
    print(f"  Cross-country path candidates: {len(path_candidates)}")
    total_leaks = sum(m["discard_leaks"] for m in country_meta.values())
    print(f"  Total discard leaks across all runs: {total_leaks}")


if __name__ == "__main__":
    main()
