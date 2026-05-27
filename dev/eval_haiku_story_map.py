"""
eval_haiku_story_map.py — A/B-replay existing story_map traces against Haiku 4.5.

Loads briefs/{date}/traces/story_map_{code}.json, sends the captured
system_prompt + user_message to claude-haiku-4-5 with identical params
(thinking budget, tool schema), parses the Haiku response through the
existing hydrate_story_map / parse_story_map_response, then diffs against
the original Sonnet output stored in the trace.

Mechanical metrics only — no LLM-as-judge. Watch:
  - stories_identified delta
  - URL overlap % (Sonnet URLs found in any Haiku story)
  - source-count distribution per story
  - tokens, cost (Haiku $1/$5/Mtok vs Sonnet $3/$15/Mtok), latency

Output: dev/eval_haiku_story_map/{date}/haiku_{code}.json per call (cached
on disk; rerun with --force to overwrite), and a markdown report at
dev/eval_haiku_story_map/{date}/report.md.

Usage:
    python dev/eval_haiku_story_map.py --date 20260503 --countries mx,jp,br,fi
    python dev/eval_haiku_story_map.py --date 20260503 --countries mx --force
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Make `src.monitor` importable when run as `python dev/eval_haiku_story_map.py`
# from the repo root (matches the convention in other dev/ scripts).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import anthropic

# Reuse the production parsing so Haiku output is hydrated exactly like Sonnet's.
from src.monitor.agents.story_map import (
    RECORD_STORY_MAP_TOOL,
    RECORD_STORY_MAP_TOOL_NAME,
    hydrate_story_map,
    parse_story_map_response,
)
from src.monitor.config import THINKING_BUDGET_TOKENS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = REPO_ROOT / "dev" / "eval_haiku_story_map"

HAIKU_MODEL = "claude-haiku-4-5"
# Prices per million tokens (input / output). Haiku 4.5 numbers per Anthropic
# pricing page; Sonnet 4.6 numbers from this repo's settings.yaml.
PRICES = {
    "haiku": (1.0, 5.0),
    "sonnet": (3.0, 15.0),
}
# Same shape story_map.py uses: 16k thinking + 16k visible output.
MAX_TOKENS = THINKING_BUDGET_TOKENS + 16384


# ---- Replay ----


@dataclass
class HaikuRun:
    """One Haiku replay output, cached to disk for reproducibility."""

    code: str
    parsed: dict | None  # hydrated StoryMapOutput dict, None on failure
    response_text: str
    used_tool: bool
    used_fallback: bool
    usage: dict[str, int]
    latency_s: float
    error: str | None = None


def _build_replay_params(system_prompt: str, user_message: str, use_tool: bool) -> dict:
    """Construct the messages.create kwargs that mirror story_map.py:_call."""
    params: dict[str, Any] = dict(
        model=HAIKU_MODEL,
        max_tokens=MAX_TOKENS,
        temperature=1,
        thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET_TOKENS},
        # No cache_control here — we're hitting Haiku once per call in the
        # eval; cache premium would be a small but pointless cost.
        system=[{"type": "text", "text": system_prompt}],
        messages=[{"role": "user", "content": user_message}],
    )
    if use_tool:
        params["tools"] = [RECORD_STORY_MAP_TOOL]
    return params


def _extract_text_and_tool_use(response: Any) -> tuple[dict | None, str]:
    """Same shape as story_map._extract_text_and_tool_use, inlined to avoid
    cross-module coupling on a private."""
    tool_input: dict | None = None
    text_content = ""
    for block in response.content:
        if block.type == "text" and not text_content:
            text_content = block.text
        elif (
            block.type == "tool_use"
            and getattr(block, "name", None) == RECORD_STORY_MAP_TOOL_NAME
        ):
            tool_input = getattr(block, "input", None)
    return tool_input, text_content


def _tool_input_complete(t: dict | None) -> bool:
    if not isinstance(t, dict):
        return False
    for key in ("stories", "single_source_items", "unassigned"):
        if key not in t or not isinstance(t[key], list):
            return False
    return True


async def replay_one(
    client: anthropic.AsyncAnthropic,
    code: str,
    system_prompt: str,
    user_message: str,
) -> HaikuRun:
    """Call Haiku with the captured prompts; fall back to no-tool on partial
    tool_use (same policy story_map.py uses)."""
    params = _build_replay_params(system_prompt, user_message, use_tool=True)

    async def _call(p: dict) -> Any:
        # Streaming is required because the non-streaming endpoint has a 10-min
        # SDK timeout, and our calls can exceed that with a 16k thinking budget
        # on the largest countries. Matches story_map.py's production behavior.
        async with client.messages.stream(**p) as stream:
            return await stream.get_final_message()

    start = time.monotonic()
    try:
        response = await _call(params)
    except Exception as e:
        logger.error("Haiku %s: API call failed: %s", code, e)
        return HaikuRun(
            code=code, parsed=None, response_text="", used_tool=True,
            used_fallback=False, usage={}, latency_s=time.monotonic() - start,
            error=f"{type(e).__name__}: {e}",
        )

    tool_input, text_content = _extract_text_and_tool_use(response)
    used_fallback = False
    if not _tool_input_complete(tool_input):
        logger.warning(
            "Haiku %s: partial/missing tool_use (input=%d out=%d) — retrying no-tool",
            code, response.usage.input_tokens, response.usage.output_tokens,
        )
        try:
            fallback_params = _build_replay_params(system_prompt, user_message, use_tool=False)
            response = await _call(fallback_params)
            tool_input, text_content = _extract_text_and_tool_use(response)
            used_fallback = True
        except Exception as e:
            logger.error("Haiku %s: no-tool fallback failed: %s", code, e)
            return HaikuRun(
                code=code, parsed=None, response_text=text_content,
                used_tool=True, used_fallback=True, usage={},
                latency_s=time.monotonic() - start,
                error=f"fallback {type(e).__name__}: {e}",
            )

    parsed_obj = None
    try:
        if tool_input is not None:
            parsed_obj = hydrate_story_map(tool_input)
        elif text_content:
            parsed_obj = parse_story_map_response(text_content)
    except Exception as e:
        logger.error("Haiku %s: parse failed: %s", code, e)

    parsed_dict = None
    if parsed_obj is not None:
        # StoryMapOutput is a dataclass — convert to dict for serialization.
        from dataclasses import asdict
        parsed_dict = asdict(parsed_obj)

    return HaikuRun(
        code=code,
        parsed=parsed_dict,
        response_text=text_content,
        used_tool=tool_input is not None,
        used_fallback=used_fallback,
        usage={
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cache_creation_input_tokens": getattr(
                response.usage, "cache_creation_input_tokens", 0
            ) or 0,
            "cache_read_input_tokens": getattr(
                response.usage, "cache_read_input_tokens", 0
            ) or 0,
        },
        latency_s=time.monotonic() - start,
        error=None,
    )


def load_or_run(
    cache_path: Path,
    runner: callable,
    force: bool,
) -> HaikuRun:
    """Synchronous cache wrapper — only call the API if not cached."""
    if cache_path.exists() and not force:
        d = json.loads(cache_path.read_text())
        return HaikuRun(**d)
    run = asyncio.run(runner())
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(run.__dict__, indent=2, default=str))
    return run


# ---- Diff metrics ----


def _all_urls(parsed: dict) -> list[str]:
    urls: list[str] = []
    for s in parsed.get("stories", []) or []:
        urls.extend(s.get("representative_urls") or [])
        for art in s.get("articles") or []:
            if art.get("url"):
                urls.append(art["url"])
    for ssi in parsed.get("single_source_items", []) or []:
        if ssi.get("url"):
            urls.append(ssi["url"])
    return urls


def _story_urls(stories: list[dict]) -> list[set[str]]:
    """Per-story set of URLs (representative + article)."""
    out = []
    for s in stories:
        urls = set(s.get("representative_urls") or [])
        for a in s.get("articles") or []:
            if a.get("url"):
                urls.add(a["url"])
        out.append(urls)
    return out


def _url_overlap_pct(sonnet: dict, haiku: dict) -> float:
    """% of Sonnet's URLs that appear anywhere in Haiku's stories."""
    son_urls = set(_all_urls(sonnet))
    if not son_urls:
        return 0.0
    haiku_urls = set(_all_urls(haiku))
    return 100.0 * len(son_urls & haiku_urls) / len(son_urls)


def _match_stories(
    sonnet_stories: list[dict], haiku_stories: list[dict]
) -> tuple[list[tuple[int, int, float]], list[int], list[int]]:
    """Greedy best-match Sonnet → Haiku by Jaccard URL overlap. Returns
    (matched_pairs, sonnet_orphans, haiku_orphans). Each pair is
    (sonnet_idx, haiku_idx, jaccard)."""
    son_urls = _story_urls(sonnet_stories)
    haiku_urls = _story_urls(haiku_stories)
    used_haiku: set[int] = set()
    pairs: list[tuple[int, int, float]] = []
    son_orphans: list[int] = []

    for si, surls in enumerate(son_urls):
        best_hi, best_j = -1, 0.0
        for hi, hurls in enumerate(haiku_urls):
            if hi in used_haiku or not (surls and hurls):
                continue
            inter = len(surls & hurls)
            union = len(surls | hurls)
            j = inter / union if union else 0.0
            if j > best_j:
                best_hi, best_j = hi, j
        if best_hi >= 0 and best_j >= 0.1:  # 10% Jaccard floor — looser is noise
            pairs.append((si, best_hi, best_j))
            used_haiku.add(best_hi)
        else:
            son_orphans.append(si)

    haiku_orphans = [i for i in range(len(haiku_stories)) if i not in used_haiku]
    return pairs, son_orphans, haiku_orphans


def _cost(usage: dict, model: str) -> float:
    in_p, out_p = PRICES[model]
    return (
        usage.get("input_tokens", 0) * in_p
        + usage.get("output_tokens", 0) * out_p
    ) / 1_000_000


def _source_count_stats(stories: list[dict]) -> tuple[float, int]:
    """(mean, max) of source_count across stories — 0/0 if no stories."""
    if not stories:
        return 0.0, 0
    counts = [s.get("source_count", 0) or 0 for s in stories]
    return sum(counts) / len(counts), max(counts)


# ---- Report ----


def render_country_row(
    code: str,
    sonnet: dict,
    sonnet_usage: dict,
    haiku_run: HaikuRun,
) -> dict:
    """Compute all diff metrics for one country. Returns a dict that the
    Markdown renderer turns into a table row + drilldown section."""
    haiku_parsed = haiku_run.parsed or {}
    son_stories = sonnet.get("stories", []) or []
    hai_stories = haiku_parsed.get("stories", []) or []

    son_mean_src, son_max_src = _source_count_stats(son_stories)
    hai_mean_src, hai_max_src = _source_count_stats(hai_stories)

    if hai_stories:
        pairs, son_orphans, haiku_orphans = _match_stories(son_stories, hai_stories)
        url_overlap = _url_overlap_pct(sonnet, haiku_parsed)
    else:
        pairs, son_orphans, haiku_orphans = [], list(range(len(son_stories))), []
        url_overlap = 0.0

    return {
        "code": code,
        "error": haiku_run.error,
        "sonnet_stories": len(son_stories),
        "haiku_stories": len(hai_stories),
        "sonnet_single_source": len(sonnet.get("single_source_items") or []),
        "haiku_single_source": len(haiku_parsed.get("single_source_items") or []),
        "sonnet_off_topic": sonnet.get("off_topic_filtered", 0),
        "haiku_off_topic": haiku_parsed.get("off_topic_filtered", 0),
        "url_overlap_pct": url_overlap,
        "sonnet_mean_src": son_mean_src,
        "haiku_mean_src": hai_mean_src,
        "sonnet_max_src": son_max_src,
        "haiku_max_src": hai_max_src,
        "matched_pairs": len(pairs),
        "sonnet_orphans": len(son_orphans),
        "haiku_orphans": len(haiku_orphans),
        "sonnet_in_tok": sonnet_usage.get("input_tokens", 0),
        "sonnet_out_tok": sonnet_usage.get("output_tokens", 0),
        "haiku_in_tok": haiku_run.usage.get("input_tokens", 0),
        "haiku_out_tok": haiku_run.usage.get("output_tokens", 0),
        "sonnet_cost": _cost(sonnet_usage, "sonnet"),
        "haiku_cost": _cost(haiku_run.usage, "haiku"),
        "haiku_latency_s": haiku_run.latency_s,
        "haiku_used_fallback": haiku_run.used_fallback,
        "pairs": pairs,
        "son_orphans": son_orphans,
        "haiku_orphans_idx": haiku_orphans,
        "son_stories": son_stories,
        "hai_stories": hai_stories,
    }


def render_markdown(date: str, rows: list[dict]) -> str:
    """Render the side-by-side markdown report."""
    out = [
        f"# Haiku 4.5 vs Sonnet 4.6 — story_map eval, {date}",
        "",
        "Mechanical replay. Identical system + user prompts; only `model` swapped. "
        "URL overlap = % of Sonnet's URLs (representative + article) present in any "
        "Haiku story. Story-pair matching is greedy by Jaccard URL overlap, 10% floor.",
        "",
        "## Per-country summary",
        "",
        "| Code | Stories (S→H) | Single-src (S→H) | Off-topic (S→H) | URL overlap | "
        "Avg src/story (S→H) | Matched / S orph / H orph | $ (S→H) | Δ$ | Lat (s) |",
        "|------|---------------|------------------|-----------------|-------------|"
        "----------------------|---------------------------|---------|-----|--------|",
    ]
    total_s_cost = 0.0
    total_h_cost = 0.0
    for r in rows:
        if r["error"]:
            out.append(
                f"| **{r['code']}** | — | — | — | — | — | — | — | — | "
                f"**ERROR: {r['error']}** |"
            )
            continue
        s_cost = r["sonnet_cost"]
        h_cost = r["haiku_cost"]
        total_s_cost += s_cost
        total_h_cost += h_cost
        out.append(
            f"| **{r['code']}** "
            f"| {r['sonnet_stories']}→{r['haiku_stories']} "
            f"| {r['sonnet_single_source']}→{r['haiku_single_source']} "
            f"| {r['sonnet_off_topic']}→{r['haiku_off_topic']} "
            f"| {r['url_overlap_pct']:.0f}% "
            f"| {r['sonnet_mean_src']:.1f}→{r['haiku_mean_src']:.1f} "
            f"(max {r['sonnet_max_src']}→{r['haiku_max_src']}) "
            f"| {r['matched_pairs']} / {r['sonnet_orphans']} / {r['haiku_orphans']} "
            f"| ${s_cost:.2f}→${h_cost:.2f} "
            f"| **−${s_cost - h_cost:.2f}** "
            f"| {r['haiku_latency_s']:.1f} |"
        )
    if total_s_cost or total_h_cost:
        out.append(
            f"| **total** | | | | | | | "
            f"**${total_s_cost:.2f}→${total_h_cost:.2f}** | "
            f"**−${total_s_cost - total_h_cost:.2f}** | |"
        )

    out += [
        "",
        "## Per-country drilldown",
        "",
    ]
    for r in rows:
        out += _render_drilldown(r)
        out.append("")

    out += [
        "## How to read this",
        "",
        "- **URL overlap >70%**: Haiku is clustering the same events as Sonnet.",
        "- **Stories delta within ±20%**: Haiku found ~the same shape of week.",
        "- **Avg src/story comparable**: Haiku isn't under-attributing multi-source events.",
        "- **High Haiku orphans**: Haiku splintered events Sonnet kept together "
        "(or hallucinated stories — eyeball them).",
        "- **High Sonnet orphans**: Haiku missed events Sonnet caught (worst case).",
        "",
    ]
    return "\n".join(out)


def _render_drilldown(r: dict) -> list[str]:
    if r.get("error"):
        return [f"### {r['code']}", f"**ERROR**: {r['error']}", ""]
    out = [
        f"### {r['code']}",
        "",
        f"Haiku replay: input={r['haiku_in_tok']:,} out={r['haiku_out_tok']:,} "
        f"tokens, latency={r['haiku_latency_s']:.1f}s"
        + (" **[no-tool fallback]**" if r["haiku_used_fallback"] else ""),
        "",
    ]
    son_stories = r["son_stories"]
    hai_stories = r["hai_stories"]
    pairs = sorted(r["pairs"], key=lambda p: -p[2])  # best matches first

    if pairs:
        out.append("**Matched stories** (best 6 by URL overlap):")
        out.append("")
        for si, hi, j in pairs[:6]:
            s_head = son_stories[si].get("headline", "")[:80]
            h_head = hai_stories[hi].get("headline", "")[:80]
            out.append(
                f"- jaccard={j:.2f}  S: _{s_head}_  ↔  H: _{h_head}_"
            )
        out.append("")

    if r["son_orphans"]:
        out.append(f"**Sonnet stories with no Haiku match** ({len(r['son_orphans'])}):")
        out.append("")
        for si in r["son_orphans"][:5]:
            s = son_stories[si]
            out.append(
                f"- {s.get('headline','')[:100]} "
                f"(sources={s.get('source_count', 0)})"
            )
        if len(r["son_orphans"]) > 5:
            out.append(f"- ... +{len(r['son_orphans']) - 5} more")
        out.append("")

    if r["haiku_orphans_idx"]:
        out.append(f"**Haiku stories with no Sonnet match** ({len(r['haiku_orphans_idx'])}):")
        out.append("")
        for hi in r["haiku_orphans_idx"][:5]:
            s = hai_stories[hi]
            out.append(
                f"- {s.get('headline','')[:100]} "
                f"(sources={s.get('source_count', 0)})"
            )
        if len(r["haiku_orphans_idx"]) > 5:
            out.append(f"- ... +{len(r['haiku_orphans_idx']) - 5} more")
        out.append("")

    return out


# ---- CLI ----


async def _run_replays_async(
    client: anthropic.AsyncAnthropic,
    targets: list[tuple[str, str, str, Path]],
    force: bool,
) -> list[HaikuRun]:
    """Run replays in parallel for all (code, sys, user, cache_path) targets.

    Cached results are loaded synchronously up front; only uncached targets
    hit the API.
    """
    out_runs: dict[str, HaikuRun] = {}
    pending: list[tuple[str, str, str, Path]] = []
    for code, sys_prompt, user_msg, cache_path in targets:
        if cache_path.exists() and not force:
            d = json.loads(cache_path.read_text())
            out_runs[code] = HaikuRun(**d)
            logger.info("Haiku %s: cached, skipping API call", code)
        else:
            pending.append((code, sys_prompt, user_msg, cache_path))

    if pending:
        logger.info("Haiku: replaying %d countries (parallel)", len(pending))
        results = await asyncio.gather(
            *[replay_one(client, code, s, u) for code, s, u, _ in pending]
        )
        for (code, _, _, cache_path), run in zip(pending, results):
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(run.__dict__, indent=2, default=str))
            out_runs[code] = run

    return [out_runs[code] for code, _, _, _ in targets]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--date", required=True, help="Brief date directory (e.g. 20260503)")
    parser.add_argument(
        "--countries", required=True, help="Comma-separated country codes (e.g. mx,jp,br,fi)"
    )
    parser.add_argument("--force", action="store_true", help="Re-run Haiku even if cached")
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY not set")

    codes = [c.strip() for c in args.countries.split(",") if c.strip()]
    traces_dir = REPO_ROOT / "briefs" / args.date / "traces"
    cache_dir = EVAL_DIR / args.date

    targets = []
    sonnet_by_code: dict[str, tuple[dict, dict]] = {}  # code -> (parsed, usage)
    for code in codes:
        trace_path = traces_dir / f"story_map_{code}.json"
        if not trace_path.exists():
            logger.error("Missing trace: %s", trace_path)
            continue
        trace = json.loads(trace_path.read_text())
        sys_prompt = trace["input"]["system_prompt"]
        user_msg = trace["input"]["user_message"]
        sonnet_by_code[code] = (trace["output"]["parsed"], trace.get("usage", {}))
        targets.append((code, sys_prompt, user_msg, cache_dir / f"haiku_{code}.json"))

    if not targets:
        raise SystemExit("No usable traces found")

    client = anthropic.AsyncAnthropic()
    haiku_runs = asyncio.run(_run_replays_async(client, targets, args.force))

    rows = []
    for (code, _, _, _), run in zip(targets, haiku_runs):
        sonnet_parsed, sonnet_usage = sonnet_by_code[code]
        rows.append(render_country_row(code, sonnet_parsed, sonnet_usage, run))

    report_path = cache_dir / "report.md"
    report_path.write_text(render_markdown(args.date, rows))
    logger.info("Report written to %s", report_path)
    # Also print a one-line summary to stdout so the run is obviously done.
    n_ok = sum(1 for r in rows if not r["error"])
    print(f"\nDone. {n_ok}/{len(rows)} replays succeeded. Report: {report_path}")


if __name__ == "__main__":
    main()
