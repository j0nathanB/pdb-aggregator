"""Option B verification: replay traces through new cache_control-enabled call shape.

For each distinct code path we modified (editor, copyeditor, regional_writer),
load TWO different production traces and send three calls per code path:

  1. trace A  → writes cache for A's bytes
  2. trace A  → should hit cache (same-input cache mechanism works)
  3. trace B  → should hit cache only if A's cached prefix matches B's prefix
                (cross-input cache key check)

The cross-input check is what catches "per-call variability inside the
cached block" bugs — the trap that shipped the copyeditor 0% hit rate on
2026-05-03. Same-input replay alone (the prior version of this script)
gives a false positive: the bytes are identical so the cache fires, but
production sends different countries' prompts and gets per-input cache
keys that never read each other.

Verdicts:
  ✅ same-input AND cross-input reads → cache works as designed
  ⚠️ same-input reads but cross-input is 0 → per-call variability in
     cached block (cache fires per-input, not cross-call) — this is
     the copyeditor-style bug
  ❌ same-input doesn't read → cache mechanism broken or format rejected

Cost: ~$1.50 in API tokens with thinking off + small max_tokens.

Usage:  .venv/bin/python dev/optimize_prompts/option_b_replay.py
"""

import json
import os
import time
from pathlib import Path

import anthropic

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load .env if present (the pipeline's CLI does this; we do it manually here)
_env_path = PROJECT_ROOT / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2048

# Two different traces per distinct code path. Different countries/regions
# so the cross-input check has byte-different inputs.
TEST_CASES = [
    ("editor", [
        "briefs/20260503/traces/editor_mx.json",
        "briefs/20260503/traces/editor_au.json",
    ]),
    ("copyeditor", [
        "briefs/20260503/traces/copyeditor_mx.json",
        "briefs/20260503/traces/copyeditor_au.json",
    ]),
    ("regional_writer", [
        "briefs/20260503/traces/regional_writer_americas.json",
        "briefs/20260503/traces/regional_writer_western_europe.json",
    ]),
]


def _send(label: str, system_prompt: str, user_message: str, tag: str, client: anthropic.Anthropic) -> dict:
    """Send one API call with cache_control on system, return usage summary."""
    t0 = time.time()
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=[{
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": user_message}],
        )
        elapsed = time.time() - t0
        u = response.usage
        cc = getattr(u, "cache_creation_input_tokens", 0) or 0
        cr = getattr(u, "cache_read_input_tokens", 0) or 0
        text_blocks = [b.text for b in response.content if getattr(b, "type", None) == "text"]
        output_text = "".join(text_blocks)

        print(f"  {tag} ({elapsed:.1f}s): input={u.input_tokens:,}, "
              f"cache_create={cc:,}, cache_read={cr:,}, output={u.output_tokens:,}")
        return {
            "ok": True,
            "tag": tag,
            "input_tokens": u.input_tokens,
            "cache_creation": cc,
            "cache_read": cr,
            "output_tokens": u.output_tokens,
            "output_preview": output_text[:120],
        }
    except anthropic.APIStatusError as e:
        elapsed = time.time() - t0
        print(f"  {tag} ({elapsed:.1f}s) FAILED: HTTP {e.status_code} — {e.message}")
        return {"ok": False, "tag": tag, "error_status": e.status_code, "error_message": str(e)}
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  {tag} ({elapsed:.1f}s) FAILED: {type(e).__name__}: {e}")
        return {"ok": False, "tag": tag, "error_type": type(e).__name__, "error_message": str(e)}


def replay(label: str, trace_paths: list[Path], client: anthropic.Anthropic) -> dict:
    """Send 3 calls per code path: A, A (same-input check), B (cross-input check)."""
    trace_a = json.loads(trace_paths[0].read_text())
    trace_b = json.loads(trace_paths[1].read_text())
    sp_a = trace_a["input"]["system_prompt"]
    um_a = trace_a["input"]["user_message"]
    sp_b = trace_b["input"]["system_prompt"]
    um_b = trace_b["input"]["user_message"]

    print(f"\n=== {label} ===")
    print(f"  trace A: {trace_paths[0].name} (system={len(sp_a):,} chars)")
    print(f"  trace B: {trace_paths[1].name} (system={len(sp_b):,} chars)")

    calls = [
        _send(label, sp_a, um_a, "1/3 A (write)", client),
        _send(label, sp_a, um_a, "2/3 A (same-input)", client),
        _send(label, sp_b, um_b, "3/3 B (cross-input)", client),
    ]
    return {"label": label, "traces": [str(p) for p in trace_paths], "calls": calls}


def verdict(result: dict) -> str:
    label = result["label"]
    calls = result["calls"]
    if not all(c.get("ok") for c in calls):
        return f"❌ {label}: API errors (see above)"
    c1, c2, c3 = calls
    if c1["cache_creation"] == 0:
        return f"⚠️  {label}: call 1 didn't write cache (prompt below 1024-token minimum?)"
    if c2["cache_read"] == 0:
        return f"❌ {label}: same-input replay didn't read cache — cache mechanism broken"
    if c3["cache_read"] == 0:
        return (f"⚠️  {label}: same-input cache works but cross-input got 0 reads — "
                f"per-call variability in cached block (copyeditor-style bug)")
    return (f"✅ {label}: cache works cross-input "
            f"(write={c1['cache_creation']:,}, same-input read={c2['cache_read']:,}, "
            f"cross-input read={c3['cache_read']:,})")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in environment")
        raise SystemExit(1)

    client = anthropic.Anthropic()
    all_results = []
    for label, trace_rels in TEST_CASES:
        trace_paths = [PROJECT_ROOT / r for r in trace_rels]
        missing = [p for p in trace_paths if not p.exists()]
        if missing:
            print(f"\nSKIP {label}: traces not found: {[str(p) for p in missing]}")
            continue
        all_results.append(replay(label, trace_paths, client))

    print("\n=== VERDICT ===")
    for r in all_results:
        print(verdict(r))


if __name__ == "__main__":
    main()
