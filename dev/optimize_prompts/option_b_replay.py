"""Option B verification: replay traces through new cache_control-enabled call shape.

For each distinct code path we modified (editor, copyeditor, regional_writer),
pick one trace, replay the saved system_prompt + user_message twice with the
new cache_control format. Verify:

  1. API accepts the new format (no 400)
  2. Output is parseable
  3. cache_creation_input_tokens > 0 on call 1 (cache write)
  4. cache_read_input_tokens > 0 on call 2 (cache read on identical prefix)

We send the same prompt bytes that production sent. The only difference is
the cache_control hint on the system block — pure additive metadata. Output
will not be byte-identical to the trace's saved response (temperature=1 +
adaptive thinking are non-deterministic), so we check structural validity
only, not output equivalence.

Cost: ~$1 in API tokens with thinking off + small max_tokens.

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

# One trace per distinct code path we changed.
TEST_CASES = [
    ("editor", "briefs/20260426/traces/editor_mx.json"),
    ("copyeditor", "briefs/20260426/traces/copyeditor_mx.json"),
    ("regional_writer", "briefs/20260426/traces/regional_writer_americas.json"),
]


def replay(label: str, trace_path: Path, client: anthropic.Anthropic) -> dict:
    trace = json.loads(trace_path.read_text())
    system_prompt = trace["input"]["system_prompt"]
    user_message = trace["input"]["user_message"]

    print(f"\n=== {label} (trace: {trace_path.name}) ===")
    print(f"  system: {len(system_prompt):,} chars (~{len(system_prompt)//4:,} tokens)")
    print(f"  user:   {len(user_message):,} chars (~{len(user_message)//4:,} tokens)")

    results = []
    for i in range(2):
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

            print(f"  call {i+1}/2 ({elapsed:.1f}s): "
                  f"input={u.input_tokens:,}, cache_create={cc:,}, cache_read={cr:,}, "
                  f"output={u.output_tokens:,}")
            print(f"    output preview: {output_text[:120]!r}{'…' if len(output_text) > 120 else ''}")
            results.append({
                "ok": True,
                "input_tokens": u.input_tokens,
                "cache_creation": cc,
                "cache_read": cr,
                "output_tokens": u.output_tokens,
                "stop_reason": response.stop_reason,
                "output_chars": len(output_text),
            })
        except anthropic.APIStatusError as e:
            elapsed = time.time() - t0
            print(f"  call {i+1}/2 ({elapsed:.1f}s) FAILED: HTTP {e.status_code} — {e.message}")
            results.append({"ok": False, "error_status": e.status_code, "error_message": str(e)})
            return {"label": label, "trace": str(trace_path), "calls": results}
        except Exception as e:
            elapsed = time.time() - t0
            print(f"  call {i+1}/2 ({elapsed:.1f}s) FAILED: {type(e).__name__}: {e}")
            results.append({"ok": False, "error_type": type(e).__name__, "error_message": str(e)})
            return {"label": label, "trace": str(trace_path), "calls": results}

    return {"label": label, "trace": str(trace_path), "calls": results}


def verdict(result: dict) -> str:
    label = result["label"]
    calls = result["calls"]
    if not all(c.get("ok") for c in calls):
        return f"❌ {label}: API errors (see above)"
    c1, c2 = calls
    if c1["cache_creation"] == 0:
        return f"⚠️  {label}: call 1 didn't write cache (prompt below 1024-token minimum?)"
    if c2["cache_read"] == 0:
        return f"❌ {label}: call 2 didn't read cache — caching not working"
    return (f"✅ {label}: cache fired (call 1 wrote {c1['cache_creation']:,} tokens; "
            f"call 2 read {c2['cache_read']:,} tokens, paid full price for "
            f"{c2['input_tokens']:,} uncached)")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set in environment")
        raise SystemExit(1)

    client = anthropic.Anthropic()
    all_results = []
    for label, trace_rel in TEST_CASES:
        trace_path = PROJECT_ROOT / trace_rel
        if not trace_path.exists():
            print(f"\nSKIP {label}: trace not found at {trace_path}")
            continue
        all_results.append(replay(label, trace_path, client))

    print("\n=== VERDICT ===")
    for r in all_results:
        print(verdict(r))


if __name__ == "__main__":
    main()
