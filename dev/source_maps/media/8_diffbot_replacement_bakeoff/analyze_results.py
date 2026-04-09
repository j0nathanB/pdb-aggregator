"""Analyze bake-off results.

Produces:
  1. Per-domain method scores (curl / diffbot / playwright / browserbase)
  2. Bucket classification:
       A. curl works (>= 2/3) — drop diffbot entirely
       B. Browserbase wins (bb >= diffbot AND bb >= 2/3) — replace
       C. Both work (both >= 2/3) — browserbase first, diffbot last-resort
       D. Only Diffbot (diffbot 3/3, bb < 2/3) — keep diffbot
       E. Neither works — manual review
  3. Recommended per-domain routing change
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RESULTS = HERE / "results.json"
REPORT = HERE / "REPORT.md"


def score_for(records: list[dict], method: str) -> tuple[int, int]:
    """Returns (successes, total) for a method given a list of result records
    for a single domain. Success = text_ok (>= 200 chars extracted)."""
    ok = sum(1 for r in records if r[method].get("text_ok"))
    return ok, len(records)


def classify(domain: str, records: list[dict]) -> tuple[str, str]:
    """Return (bucket_letter, reasoning)."""
    curl_ok, curl_n = score_for(records, "curl")
    diffbot_ok, diffbot_n = score_for(records, "diffbot")
    pw_ok, pw_n = score_for(records, "playwright")
    bb_ok, bb_n = score_for(records, "browserbase")

    def rate(ok: int, n: int) -> float:
        return ok / n if n else 0.0

    if rate(curl_ok, curl_n) >= 2 / 3:
        return ("A", f"curl {curl_ok}/{curl_n} — drop diffbot")
    if bb_ok >= diffbot_ok and rate(bb_ok, bb_n) >= 2 / 3:
        return ("B", f"browserbase {bb_ok}/{bb_n} >= diffbot {diffbot_ok}/{diffbot_n} — replace with bb")
    if rate(bb_ok, bb_n) >= 2 / 3 and rate(diffbot_ok, diffbot_n) >= 2 / 3:
        return ("C", f"both work (bb {bb_ok}/{bb_n}, diffbot {diffbot_ok}/{diffbot_n}) — bb first, diffbot last")
    if rate(diffbot_ok, diffbot_n) == 1.0 and rate(bb_ok, bb_n) < 2 / 3:
        return ("D", f"only diffbot reliable ({diffbot_ok}/{diffbot_n} vs bb {bb_ok}/{bb_n}) — keep diffbot")
    if rate(pw_ok, pw_n) >= 2 / 3:
        return ("A", f"playwright {pw_ok}/{pw_n} covers — drop diffbot")
    return ("E", f"nothing reliable (curl {curl_ok}/{curl_n} / bb {bb_ok}/{bb_n} / diffbot {diffbot_ok}/{diffbot_n} / pw {pw_ok}/{pw_n})")


def main() -> None:
    if not RESULTS.exists():
        print(f"No results at {RESULTS} — run the bake-off first")
        return

    data = json.loads(RESULTS.read_text())
    records = data["results"]

    # Group by domain
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_domain[r["domain"]].append(r)

    # Per-domain classification
    domain_rows = []
    bucket_counts = Counter()
    for domain in sorted(by_domain.keys()):
        domain_records = by_domain[domain]
        curl_ok, curl_n = score_for(domain_records, "curl")
        diffbot_ok, diffbot_n = score_for(domain_records, "diffbot")
        pw_ok, pw_n = score_for(domain_records, "playwright")
        bb_ok, bb_n = score_for(domain_records, "browserbase")
        bucket, reasoning = classify(domain, domain_records)
        bucket_counts[bucket] += 1
        domain_rows.append({
            "domain": domain,
            "curl": f"{curl_ok}/{curl_n}",
            "diffbot": f"{diffbot_ok}/{diffbot_n}",
            "playwright": f"{pw_ok}/{pw_n}",
            "browserbase": f"{bb_ok}/{bb_n}",
            "bucket": bucket,
            "reasoning": reasoning,
        })

    # Aggregate method totals
    total_curl = sum(score_for(by_domain[d], "curl")[0] for d in by_domain)
    total_diffbot = sum(score_for(by_domain[d], "diffbot")[0] for d in by_domain)
    total_pw = sum(score_for(by_domain[d], "playwright")[0] for d in by_domain)
    total_bb = sum(score_for(by_domain[d], "browserbase")[0] for d in by_domain)
    total_urls = len(records)

    # Build markdown report
    lines = []
    lines.append("# Diffbot → Browserbase Bake-off Report")
    lines.append("")
    lines.append(f"**Generated:** {data['generated_at']}")
    lines.append(f"**Wall time:** {data['wall_time_seconds']:.0f}s")
    lines.append(f"**URLs tested:** {total_urls} across {data['total_domains']} domains")
    lines.append("")
    lines.append("## Method-level success")
    lines.append("")
    lines.append("| Method | Success (>= 200 chars) | % |")
    lines.append("|---|---|---|")
    for name, total in [("curl", total_curl), ("diffbot", total_diffbot),
                        ("playwright", total_pw), ("browserbase", total_bb)]:
        pct = total / total_urls * 100 if total_urls else 0
        lines.append(f"| {name} | {total} / {total_urls} | {pct:.1f}% |")
    lines.append("")

    # Bucket summary
    lines.append("## Bucket classification")
    lines.append("")
    bucket_desc = {
        "A": "curl or playwright alone suffices — drop diffbot",
        "B": "browserbase replaces diffbot",
        "C": "both work — browserbase first, diffbot last-resort",
        "D": "only diffbot reliable — keep diffbot",
        "E": "nothing reliable — manual review",
    }
    lines.append("| Bucket | Description | Domains |")
    lines.append("|---|---|---|")
    for b in ["A", "B", "C", "D", "E"]:
        lines.append(f"| {b} | {bucket_desc[b]} | {bucket_counts.get(b, 0)} |")
    lines.append("")

    # Per-domain table
    lines.append("## Per-domain results")
    lines.append("")
    lines.append("| Domain | curl | diffbot | playwright | browserbase | Bucket | Action |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in domain_rows:
        lines.append(
            f"| `{row['domain']}` | {row['curl']} | {row['diffbot']} | "
            f"{row['playwright']} | {row['browserbase']} | {row['bucket']} | {row['reasoning']} |"
        )
    lines.append("")

    # Routing recommendations
    lines.append("## Routing recommendations")
    lines.append("")
    lines.append("Apply these to `assets/country_configs/extraction_routing.yaml`:")
    lines.append("")
    for row in domain_rows:
        d = row["domain"]
        b = row["bucket"]
        if b == "A":
            lines.append(f"- `{d}`: remove diffbot from fallbacks (curl or playwright alone)")
        elif b == "B":
            lines.append(f"- `{d}`: replace diffbot with browserbase")
        elif b == "C":
            lines.append(f"- `{d}`: `fallbacks: [playwright, browserbase, diffbot]`")
        elif b == "D":
            lines.append(f"- `{d}`: keep diffbot as primary fallback (no browserbase replacement)")
        elif b == "E":
            lines.append(f"- `{d}`: **manual review** — no reliable method found")

    REPORT.write_text("\n".join(lines))
    print(f"Wrote {REPORT}")
    print()
    print("Summary:")
    for b in ["A", "B", "C", "D", "E"]:
        print(f"  Bucket {b} ({bucket_desc[b][:50]:<50}): {bucket_counts.get(b, 0)}")


if __name__ == "__main__":
    main()
