"""Three-way token split per agent — the actual cacheable-prefix leverage.

Total input tokens per agent ≠ leverage. The leverage ceiling is:

    stable_prefix_tokens × calls_within_TTL

where stable_prefix can sit in the system prompt OR in the user message —
what matters is whether bytes are identical across calls. This script
computes the longest common prefix (LCP) across all system_prompts and
all user_messages within each agent, so we can see the actual cacheable
portion vs the variable tail.

For agents with multiple sub-templates (e.g. editor handles country/regional/
executive/style — 4 distinct system prompts), the within-agent LCP is small
and misleading. We auto-cluster by the first 200 chars of system_prompt to
detect sub-templates, then report per-cluster LCP.

Token estimate: char_count / 4 (rough English-text heuristic; close enough
for ranking purposes).

Usage:  .venv/bin/python dev/optimize_prompts/leverage_split.py
Output: dev/optimize_prompts/leverage_split_<today>.md
"""

import json
import statistics
from collections import defaultdict, OrderedDict
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEEKS = ["20260419", "20260426"]
CHARS_PER_TOKEN = 4
CLUSTER_KEY_LEN = 200  # chars of system_prompt that define a sub-template


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


def lcp(strings: list[str]) -> str:
    """Longest common prefix across a list of strings."""
    if not strings:
        return ""
    if len(strings) == 1:
        return strings[0]
    shortest = min(strings, key=len)
    for i, ch in enumerate(shortest):
        if any(s[i] != ch for s in strings):
            return shortest[:i]
    return shortest


def lcs(strings: list[str]) -> str:
    """Longest common suffix across a list of strings.

    Used for post-flip prefix estimation: today the editor agents' system
    prompts share the style guide at the END (after `task_prompt`). Reversing
    each string and computing LCP gives the longest common suffix — exactly
    what would become the cacheable prefix if we flipped to style-guide-first.
    """
    if not strings:
        return ""
    reversed_lcp = lcp([s[::-1] for s in strings])
    return reversed_lcp[::-1]


def to_tokens(s: str) -> int:
    return len(s) // CHARS_PER_TOKEN


def cluster_by_system(items: list[dict]) -> dict[str, list[dict]]:
    """Group items by the first CLUSTER_KEY_LEN chars of their system_prompt."""
    out = defaultdict(list)
    for it in items:
        key = (it.get("input", {}).get("system_prompt") or "")[:CLUSTER_KEY_LEN]
        out[key].append(it)
    return out


def split_for_cluster(items: list[dict]) -> dict:
    """For a homogeneous cluster, compute system LCP + user LCP + variable rest."""
    systems = [(it.get("input", {}).get("system_prompt") or "") for it in items]
    users = [(it.get("input", {}).get("user_message") or "") for it in items]

    sys_lcp = lcp(systems)
    user_lcp = lcp(users)

    sys_lengths = [len(s) for s in systems]
    user_lengths = [len(u) for u in users]
    total_chars = [sl + ul for sl, ul in zip(sys_lengths, user_lengths)]

    return {
        "n": len(items),
        "system_lcp_tokens": to_tokens(sys_lcp),
        "system_mean_tokens": int(statistics.mean(sys_lengths) / CHARS_PER_TOKEN) if sys_lengths else 0,
        "system_variable_tokens": int((statistics.mean(sys_lengths) - len(sys_lcp)) / CHARS_PER_TOKEN) if sys_lengths else 0,
        "user_lcp_tokens": to_tokens(user_lcp),
        "user_mean_tokens": int(statistics.mean(user_lengths) / CHARS_PER_TOKEN) if user_lengths else 0,
        "user_variable_tokens": int((statistics.mean(user_lengths) - len(user_lcp)) / CHARS_PER_TOKEN) if user_lengths else 0,
        "total_mean_tokens": int(statistics.mean(total_chars) / CHARS_PER_TOKEN) if total_chars else 0,
        "stable_prefix_tokens": to_tokens(sys_lcp) + to_tokens(user_lcp),
        "labels": [it.get("label", "?") for it in items[:5]],
    }


def per_agent_split(traces: list[dict]) -> dict:
    by_agent = defaultdict(list)
    for t in traces:
        by_agent[t.get("agent", "?")].append(t)

    results = {}
    for agent, items in sorted(by_agent.items()):
        clusters = cluster_by_system(items)
        cluster_results = []
        for key, group in clusters.items():
            split = split_for_cluster(group)
            split["cluster_key_preview"] = key[:80].replace("\n", " ")
            cluster_results.append(split)
        cluster_results.sort(key=lambda c: -c["n"])
        results[agent] = cluster_results
    return results


def cross_call_system_lcp(traces: list[dict], agent: str) -> dict:
    """LCP across ALL system prompts for an agent, regardless of cluster.

    This is the actual cacheable shared content for cross-call cache reuse.
    Distinct from within-cluster LCP, which for n=1 clusters is just the
    full system prompt size (one call's content) — not shareable across
    other calls.

    The Phase 4 gate: if cross-call LCP / mean system size < 0.5, the
    agent has per-call variability (e.g. {{COUNTRY}} interpolation) and
    cache_control would replicate the country.py "decorative cache" bug.
    Defer to Phase 4.5 template restructure.
    """
    samples = []
    for t in traces:
        if t.get("agent") != agent:
            continue
        sp = (t.get("input") or {}).get("system_prompt") or ""
        if sp:
            samples.append(sp)
    if len(samples) < 2:
        return {"n_calls_pooled": len(samples), "lcp_tokens": 0, "mean_system_tokens": 0, "ratio": 0.0}
    cross_lcp = lcp(samples)
    mean_size = statistics.mean(len(s) for s in samples)
    return {
        "n_calls_pooled": len(samples),
        "lcp_tokens": to_tokens(cross_lcp),
        "mean_system_tokens": int(mean_size / CHARS_PER_TOKEN),
        "ratio": (len(cross_lcp) / mean_size) if mean_size else 0.0,
    }


def leverage_score(splits: list[dict]) -> dict:
    """Per-agent leverage = sum over clusters of stable_prefix * (n_calls - 1).

    First call writes the cache; the next (n-1) read it. Savings are
    stable_prefix tokens per cache hit, served at ~10% cost vs full price.

    `n` here comes from a per-week cluster (one week of traces in, one
    cluster's call count out). Result is therefore per-pipeline-run.
    """
    total_savings = 0
    for c in splits:
        savings = c["stable_prefix_tokens"] * max(0, c["n"] - 1)
        total_savings += savings
    return {"savings_per_run": total_savings}


def editor_post_flip_prefix(traces: list[dict]) -> dict:
    """Estimate the shared cacheable prefix across the editor cluster after
    the proposed `_build_system_prompt` order flip (style guide first).

    Today's order: `{base_prompt}\\n<style_guide>...</style_guide>` (editor
    + style_editor) or `{base}<style_guide>...</style_guide><leader_reference>`
    (copyeditor — appends per-country leader names AFTER the style guide).

    Post-flip: `<style_guide>...</style_guide>\\n{base_prompt}` — style guide
    becomes the shared prefix. Note: structured_copyeditor.py imports
    `_build_system_prompt` from structured_editor.py, so the same flip
    benefits copyeditor too — but copyeditor still has a per-country
    leader_reference tail, which doesn't affect the prefix.

    We compute the longest common SUFFIX two ways:

    1. **editor + style_editor only** (5 sub-templates, all end with
       `</style_guide>`) — gives the actual post-flip prefix size for those
       sites with no contamination from copyeditor's variable tail.
    2. **copyeditor pool** — confirms copyeditor's already-large within-cluster
       LCP is durable, since its tail varies but the head is stable.
    """
    seen = OrderedDict()  # cluster_key → (agent, system_prompt)
    for t in traces:
        if t.get("agent") not in {"editor", "copyeditor", "style_editor"}:
            continue
        sp = t.get("input", {}).get("system_prompt") or ""
        if not sp:
            continue
        key = sp[:CLUSTER_KEY_LEN]
        if key in seen:
            continue
        seen[key] = (t.get("agent"), sp)

    editor_samples = [sp for _, (a, sp) in seen.items() if a in {"editor", "style_editor"}]
    copy_samples = [sp for _, (a, sp) in seen.items() if a == "copyeditor"]

    def _summarize(samples: list[str]) -> dict:
        if len(samples) < 2:
            return {"n_subtemplates": len(samples), "lcs_tokens": 0, "lcp_tokens": 0}
        suffix = lcs(samples)
        prefix = lcp(samples)
        return {
            "n_subtemplates": len(samples),
            "lcs_chars": len(suffix),
            "lcs_tokens": to_tokens(suffix),
            "lcp_tokens": to_tokens(prefix),
            "suffix_head": suffix[:160].replace("\n", " "),
            "suffix_tail": suffix[-160:].replace("\n", " "),
        }

    return {
        "editor_and_style_editor": _summarize(editor_samples),
        "copyeditor": _summarize(copy_samples),
        "all_editors_pooled": _summarize(editor_samples + copy_samples),
    }


def render_md(per_week_splits: dict, ranked: list[tuple], post_flip: dict) -> str:
    L = [
        f"# Three-Way Token Split — {date.today().isoformat()}",
        "",
        "Source: 2 weekly Sunday runs (`briefs/20260419` + `briefs/20260426`).",
        "Token estimate: chars/4 (English-text heuristic; ranking-grade, not billing-grade).",
        "",
        "## How to read this",
        "",
        "Per agent, calls are clustered by their system_prompt template (first 200",
        "chars). Within each cluster:",
        "- `system LCP` = longest common prefix across all system prompts (tokens)",
        "- `user LCP` = longest common prefix across all user messages (tokens)",
        "- `stable prefix` = system LCP + user LCP — the cacheable ceiling per call",
        "- `system var` / `user var` = mean variable tail per call",
        "",
        "**`n` and savings are per single pipeline run** (one week's worth of calls",
        "in that cluster). Leverage = `stable_prefix × (n_calls - 1)` — first call",
        "writes the cache, the next (n-1) read it.",
        "",
        "## Leverage ranking",
        "",
        "**The load-bearing column is `savings/run`.** It captures whether at least",
        "one cluster has `n>1` with a sizable within-cluster prefix — i.e., whether",
        "`cache_control` will produce reads on subsequent calls.",
        "",
        "`top-cluster prefix` shows the LCP within the largest cluster. For agents",
        "with `n=1` (where every call lands in its own cluster), this is just the",
        "size of one call's system prompt and is NOT shareable across calls — those",
        "agents need template restructure (Phase 4.5), not `cache_control`.",
        "",
        "`cross-call LCP / ratio` is diagnostic for the Phase 4.5 priority: high",
        "ratio means the agent has structurally shareable content across all calls",
        "today; low ratio means per-call variability (e.g. `{{COUNTRY}}` in system",
        "prompt) requires template restructure to unlock cross-call caching.",
        "",
        "**Phase 4 gate:** ✅ ship `cache_control` if `savings/run > 0`. ❌ defer",
        "to Phase 4.5 if `savings/run == 0` and `ratio < 0.5` (per-call clusters).",
        "⚠️ low-volume (n=1 throughout, but content is structurally stable) — single-call",
        "agents don't benefit from cache_control regardless.",
        "",
        "| rank | agent | top-cluster prefix | top-cluster calls/run | savings/run | cross-call LCP | ratio | gate |",
        "|---:|---|---:|---:|---:|---:|---:|:---:|",
    ]
    for rank, (agent, score, top_cluster, xcall) in enumerate(ranked, 1):
        ratio = xcall.get("ratio", 0.0)
        savings = score["savings_per_run"]
        if savings > 0:
            gate = "✅"
        elif ratio >= 0.5:
            gate = "⚠️"  # n=1 single-call agent, content stable but no leverage
        else:
            gate = "❌"  # per-call clusters — needs Phase 4.5 restructure
        L.append(
            f"| {rank} | {agent} | {top_cluster['stable_prefix_tokens']:,} "
            f"| {top_cluster['n']} | {savings:,} "
            f"| {xcall.get('lcp_tokens', 0):,} | {ratio:.2f} | {gate} |"
        )
    L.append("")

    L.extend([
        "## Post-flip prefix verification (the Phase 3a load-bearing claim)",
        "",
        "Phase 3a flips `_build_system_prompt` in `newsletter/structured_editor.py`",
        "to put the style guide FIRST. The leverage estimate depends on what size",
        "of shared prefix that flip actually unlocks across the editor sites.",
        "",
        "We measure today's longest common SUFFIX (LCS) of the system prompts —",
        "that's the style-guide-tail block, which becomes the prefix after the flip.",
        "Pooled two ways because copyeditor has a per-country `<leader_reference>`",
        "tail that breaks LCS when included; the editor + style_editor pool is the",
        "clean signal.",
        "",
        "### editor + style_editor pool (the cleanly cacheable group)",
        "",
        f"- distinct sub-templates: **{post_flip['editor_and_style_editor']['n_subtemplates']}**",
        f"- LCP today (current order): **{post_flip['editor_and_style_editor'].get('lcp_tokens', 0):,} tokens**",
        f"- **LCS today = post-flip prefix size: {post_flip['editor_and_style_editor'].get('lcs_tokens', 0):,} tokens** ({post_flip['editor_and_style_editor'].get('lcs_chars', 0):,} chars)",
        "",
        "Suffix preview (head — what becomes the prefix):",
        "",
        f"> `{post_flip['editor_and_style_editor'].get('suffix_head', '')}…`",
        "",
        "Suffix preview (tail):",
        "",
        f"> `…{post_flip['editor_and_style_editor'].get('suffix_tail', '')}`",
        "",
        "### copyeditor pool (separate code path, but uses same _build_system_prompt)",
        "",
        f"- distinct sub-templates: **{post_flip['copyeditor']['n_subtemplates']}**",
        f"- LCP today (already cached today within each cluster): **{post_flip['copyeditor'].get('lcp_tokens', 0):,} tokens**",
        f"- LCS today: **{post_flip['copyeditor'].get('lcs_tokens', 0):,} tokens** (typically smaller — per-country leader_reference at end)",
        "",
        "### all editors pooled (control — confirms the LCS contamination problem)",
        "",
        f"- LCS across all {post_flip['all_editors_pooled']['n_subtemplates']} pooled: **{post_flip['all_editors_pooled'].get('lcs_tokens', 0):,} tokens**",
        "",
        "Pooling all together collapses LCS because copyeditor's variable tail",
        "doesn't match editor's `</style_guide>` ending. Use the split pools above.",
        "",
    ])

    for week_label, splits in per_week_splits.items():
        L.extend([f"## Per-cluster split — week {week_label}", ""])
        for agent, clusters in splits.items():
            L.append(f"### {agent}")
            L.append("")
            L.append("| cluster | calls | system LCP | system var | user LCP | user var | stable prefix | total mean |")
            L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
            for i, c in enumerate(clusters):
                preview = c["cluster_key_preview"][:60]
                L.append(
                    f"| #{i} `{preview}…` | {c['n']} | {c['system_lcp_tokens']:,} "
                    f"| {c['system_variable_tokens']:,} | {c['user_lcp_tokens']:,} "
                    f"| {c['user_variable_tokens']:,} | **{c['stable_prefix_tokens']:,}** "
                    f"| {c['total_mean_tokens']:,} |"
                )
            L.append("")
    return "\n".join(L)


def main() -> None:
    out_dir = PROJECT_ROOT / "dev" / "optimize_prompts"
    per_week_splits = {}
    combined_splits = defaultdict(list)
    all_traces = []
    for week in WEEKS:
        traces = load_traces(week)
        all_traces.extend(traces)
        splits = per_agent_split(traces)
        per_week_splits[week] = splits
        for agent, clusters in splits.items():
            combined_splits[agent].extend(clusters)

    # Rank: pick each agent's largest cluster (by per-week n_calls) as the rep
    # and compute per-run savings.
    ranked = []
    for agent, all_clusters in combined_splits.items():
        all_clusters.sort(key=lambda c: -c["n"])
        top = all_clusters[0]
        score = leverage_score([top])
        xcall = cross_call_system_lcp(all_traces, agent)
        ranked.append((agent, score, top, xcall))
    ranked.sort(key=lambda x: -x[1]["savings_per_run"])

    post_flip = editor_post_flip_prefix(all_traces)

    md = render_md(per_week_splits, ranked, post_flip)
    out_path = out_dir / f"leverage_split_{date.today().isoformat()}.md"
    out_path.write_text(md)
    print(f"Wrote {out_path}")
    e = post_flip["editor_and_style_editor"]
    c = post_flip["copyeditor"]
    print(f"Post-flip prefix (editor+style_editor): {e.get('lcs_tokens', 0):,} tokens "
          f"across {e['n_subtemplates']} sub-templates")
    print(f"Copyeditor today's LCP within cluster: {c.get('lcp_tokens', 0):,} tokens "
          f"across {c['n_subtemplates']} sub-templates")


if __name__ == "__main__":
    main()
