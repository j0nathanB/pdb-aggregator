"""
Read prior editor / writer outputs from `briefs/{date}/traces/`.

Why this exists: editor/copyeditor/style_editor output is durable only in
traces (the polished `narrative_body`, `regional_lead`, `edited_essay`,
`other_stories`, `card_summary`, `headline`). `build_all_pages` rebuilds
the in-memory content models from the ledger every run with those
fields empty, so any scoped run (recovery, resume, partial re-render)
that doesn't re-edit a given country/region/executive would silently
fall back to template empty-state output.

Calling `load_prior_editor_output` during content construction seeds
those fields from the latest polished trace. Subsequent editor passes
overwrite for targeted content; non-targets keep prior prose.

Failure mode: when no trace exists (first run for this week) or every
candidate trace fails to parse, returns None. Callers proceed with
the default empty fields and the editor generates them fresh.
"""

import json
import logging
import re
from datetime import date

from ..config import PROJECT_ROOT

logger = logging.getLogger(__name__)

_FENCE_RE = re.compile(r"^```(?:json)?\n?|\n?```$", re.MULTILINE)


def _parse_trace_response(response_text: str) -> dict | None:
    """Strip markdown fences and parse response_text as JSON. None if invalid."""
    if not response_text:
        return None
    rt = response_text.strip()
    # Strip ```json ... ``` fences that the free-form JSON path sometimes emits.
    if rt.startswith("```"):
        rt = _FENCE_RE.sub("", rt).strip()
    try:
        data = json.loads(rt)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def load_prior_editor_output(
    end_date: date,
    trace_stems: list[str],
) -> dict:
    """Merge editor outputs from multiple traces, preferring earlier stems.

    Different stages emit different field sets: the style_editor trace has
    `narrative_body` only; copyeditor has `narrative_body` + `other_stories`;
    regional_writer has `regional_lead` + `headline`; etc. We want each
    field from the MOST polished trace that has it. So we walk the
    priority list and fill in fields only when they're still missing.

    Args:
        end_date: The brief's end date; determines the briefs/{YYYYMMDD}/traces/
            directory.
        trace_stems: File stems to try, in priority order (most polished
            first). For a country narrative:
                ["style_editor_pl", "copyeditor_pl", "editor_pl"]

    Returns:
        Dict merged across the parseable traces. Empty dict if no trace
        parses. Caller does `.get("narrative_body")` / `.get("other_stories")`
        etc. to extract fields.
    """
    traces_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "traces"
    if not traces_dir.exists():
        return {}
    merged: dict = {}
    for stem in trace_stems:
        path = traces_dir / f"{stem}.json"
        if not path.exists():
            continue
        try:
            trace = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.debug("trace_reader: %s unreadable: %s", path.name, e)
            continue
        output = trace.get("output") or {}
        parsed = _parse_trace_response(output.get("response_text", ""))
        if parsed is None:
            continue
        for key, value in parsed.items():
            # Skip fields we've already filled from a higher-priority trace.
            # Skip empty strings / empty lists — treat as "not present".
            if key in merged:
                continue
            if isinstance(value, str) and not value.strip():
                continue
            if isinstance(value, list) and not value:
                continue
            merged[key] = value
    return merged
