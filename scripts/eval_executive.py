"""
Evaluate new executive analyst + executive editor prompts.

Re-runs the executive synthesis (with the `executive_eval.md` analyst prompt)
and then the editorial chain (editor → copyeditor → style editor) for a given
brief date, writing the result to a markdown file for review.

Usage:
    python scripts/eval_executive.py --date 2026-04-05

Scope of eval:
    - Executive analyst: swaps `assets/prompts/executive.md` →
      `assets/prompts/executive_eval.md` via a monkey-patch local to
      `src.monitor.agents.executive`.
    - Executive editor (`EXECUTIVE_EDITOR_SYSTEM` inline constant in
      `src/monitor/newsletter/structured_editor.py`): picked up automatically
      because the user edits that constant directly in source. No patch needed.

Outputs:
    briefs/{YYYYMMDD}/eval/executive.md
        Post-editorial essay + raw briefing items (pre-edit) for comparison.

    briefs/{YYYYMMDD}/traces/executive_global_eval.json
        Raw trace of the eval analyst run (original executive_global.json
        is left untouched).

Safety:
    - Does NOT overwrite the saved global ledger on disk. `run_executive_agent`
      mutates the in-memory ledger, but this script never calls
      `save_global_ledger()`.
    - Does NOT touch site/briefs/ or any published MDX.
    - Loads each regional report for the target week from its
      `briefs/{date}/traces/regional_{region}.json` trace (date-specific), so
      older briefs are evaluated against their own week's cross-country
      analysis, not the latest pipeline run's regional state.
    - Global ledger is loaded as-is from disk (latest state) — for older briefs
      this means the analyst's "prior state" is newer than --date. Acceptable
      for prompt evaluation but not a full historical reproduction.
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitor import trace as trace_module
from src.monitor.agents import executive as executive_mod
from src.monitor.agents.executive import run_executive_agent
from src.monitor.agents.regional import (
    CrossCuttingDynamic,
    Gap,
    LowConfidenceItem,
    RegionalReport,
    RejectedDynamic,
)
from src.monitor.config import Region, load_prompt as _real_load_prompt
from src.monitor.ledger.storage import (
    list_country_ledgers,
    load_country_ledger,
    load_global_ledger,
    load_regional_report,
    load_story_map,
)
from src.monitor.newsletter.content_builder import build_all_pages
from src.monitor.newsletter.content_models import (
    ExecutiveBriefContent,
    OverviewPageContent,
)
from src.monitor.newsletter.structured_copyeditor import copyedit_executive
from src.monitor.newsletter.structured_editor import edit_executive, style_edit_prose

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("eval_executive")


# =============================================================================
# Patches: swap in the executive_eval analyst prompt; redirect traces to _eval
# =============================================================================

def _install_patches() -> None:
    """Reroute the executive analyst to the eval prompt and to an eval-suffixed trace.

    Why:
      - `run_executive_agent` calls `load_prompt("executive")` inline at
        `src/monitor/agents/executive.py:557` and again at line 578 (for the
        trace's system_prompt field). We override the name lookup on the
        executive module so any `load_prompt("executive")` resolves to the
        content of `executive_eval.md` instead. Other prompt names pass through
        unchanged.
      - `save_raw_response("executive", "global", ...)` and
        `update_trace_parsed(...)` would overwrite
        `briefs/{date}/traces/executive_global.json`. We wrap those functions
        so any `agent="executive"` call lands at `executive_global_eval.json`.
      - EXECUTIVE_EDITOR_SYSTEM is edited inline in structured_editor.py by the
        user — the editor stage picks up the edits automatically at import, so
        no patch is needed for that side.
    """
    # 1. Rebind load_prompt inside the executive module so "executive" → "executive_eval".
    def _patched_load_prompt(name: str, **kwargs):
        if name == "executive":
            name = "executive_eval"
        return _real_load_prompt(name, **kwargs)

    executive_mod.load_prompt = _patched_load_prompt

    # 2. Trace writers — suffix the label so the original executive_global.json stays intact.
    #    executive.py imports these at call time (`from ..trace import ...`), so patching
    #    attributes on the trace module is sufficient.
    _orig_save = trace_module.save_raw_response
    _orig_update = trace_module.update_trace_parsed

    def _save_raw_eval(agent, label, run_date, **kwargs):
        if agent == "executive":
            label = f"{label}_eval"
        return _orig_save(agent, label, run_date, **kwargs)

    def _update_parsed_eval(agent, label, run_date, parsed_output, diagnostics=None):
        if agent == "executive":
            label = f"{label}_eval"
        return _orig_update(agent, label, run_date, parsed_output, diagnostics)

    trace_module.save_raw_response = _save_raw_eval
    trace_module.update_trace_parsed = _update_parsed_eval

    logger.info(
        "Patches installed: analyst prompt=executive_eval, trace label suffix=_eval. "
        "EXECUTIVE_EDITOR_SYSTEM picked up from inline edits in structured_editor.py.",
    )


# =============================================================================
# State loading (week-specific entries where possible)
# =============================================================================

def _regional_report_from_trace(trace_path: Path) -> RegionalReport:
    """Reconstruct a RegionalReport from a regional_{region}.json trace file.

    Mirrors `src.monitor.ledger.storage.load_regional_report` but reads from
    `trace["output"]["parsed"]` instead of the persisted regional ledger (which
    is not date-indexed and only holds the latest run).
    """
    trace = json.loads(trace_path.read_text())
    parsed = trace.get("output", {}).get("parsed")
    if not parsed:
        raise ValueError(f"Trace has no parsed output: {trace_path}")

    return RegionalReport(
        region=Region(parsed["region"]),
        week=date.fromisoformat(parsed["week"]),
        regional_overview=parsed.get("regional_overview", ""),
        cross_cutting_dynamics=[
            CrossCuttingDynamic(**d) for d in parsed.get("cross_cutting_dynamics", [])
        ],
        dynamics_considered_and_rejected=[
            RejectedDynamic(**d) for d in parsed.get("dynamics_considered_and_rejected", [])
        ],
        gaps=[Gap(**g) for g in parsed.get("gaps", [])],
        low_confidence_items=[
            LowConfidenceItem(**i) for i in parsed.get("low_confidence_items", [])
        ],
    )


def _load_regional_reports_for_week(end_date: date) -> dict[Region, RegionalReport]:
    """Load all 5 regional reports for the given week from trace files.

    Prefers `briefs/{date}/traces/regional_{region}.json` (date-specific, always
    correct for the target week). Falls back to `ledgers/regional/{region}.json`
    with a warning if a trace is missing — that fallback only matches if
    end_date happens to be the latest pipeline run.
    """
    reports: dict[Region, RegionalReport] = {}
    traces_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "traces"

    for region in Region:
        trace_path = traces_dir / f"regional_{region.value}.json"
        if trace_path.exists():
            try:
                reports[region] = _regional_report_from_trace(trace_path)
                continue
            except Exception as e:
                logger.warning(
                    "Failed to reconstruct %s from %s: %s — will fall back",
                    region.value, trace_path, e,
                )

        # Fallback: load from ledgers/regional/ — only correct if end_date is latest.
        try:
            fallback = load_regional_report(region)
            if fallback.week != end_date:
                logger.warning(
                    "Regional %s fallback is for week %s, not %s — eval may be mixing weeks",
                    region.value, fallback.week, end_date,
                )
            reports[region] = fallback
        except FileNotFoundError:
            logger.error("No regional report available for %s (no trace, no ledger)", region.value)

    return reports


def _load_state_for_week(end_date: date):
    """Load ledgers + week-specific country entries + regional reports + global ledger.

    Regional reports come from the `briefs/{date}/traces/regional_*.json` files
    so that older briefs reconstitute their own week's cross-country analysis,
    not the latest pipeline run's state.

    Note: the global ledger is loaded as-is from disk — it reflects the current
    (latest) state, not a historical snapshot. For older briefs this means the
    executive analyst will see dynamics created after end_date in its "prior
    state". Acceptable for prompt evaluation but not a full reproduction.
    """
    country_ledgers = {}
    country_entries: dict = {}
    for code in list_country_ledgers():
        ledger = load_country_ledger(code)
        country_ledgers[code] = ledger

        week_entry = next(
            (e for e in ledger.weekly_entries if e.week == end_date),
            None,
        )
        if week_entry is None:
            latest = ledger.latest_entry()
            if latest:
                logger.warning(
                    "%s: no entry for %s, falling back to latest entry (%s)",
                    code, end_date, latest.week,
                )
                country_entries[code] = latest
        else:
            country_entries[code] = week_entry

    regional_reports = _load_regional_reports_for_week(end_date)
    global_ledger = load_global_ledger()

    story_maps = {}
    for code in country_ledgers:
        try:
            story_maps[code] = load_story_map(code, end_date)
        except FileNotFoundError:
            pass

    return country_ledgers, country_entries, regional_reports, global_ledger, story_maps


# =============================================================================
# Markdown rendering
# =============================================================================

def _render_markdown(
    overview: OverviewPageContent,
    brief: ExecutiveBriefContent,
    end_date: date,
) -> str:
    """Render the evaluated executive brief: post-edit essay + raw item dump."""
    week_start = (end_date - timedelta(days=6)).isoformat()

    lines: list[str] = [
        "# Executive Eval",
        "",
        f"_Brief week: {week_start} to {end_date.isoformat()}_  ",
        "_Analyst prompt: `executive_eval.md`_  ",
        "_Editor prompt: `EXECUTIVE_EDITOR_SYSTEM` inline edits in `structured_editor.py`_",
        "",
        "## Executive Brief (post-editorial chain)",
        "",
        brief.edited_essay or "_(empty)_",
        "",
        "---",
        "",
        f"## Raw Briefing Items (pre-edit) — {len(brief.items)} items",
        "",
    ]

    if not brief.items:
        lines += ["_(none)_", ""]

    for i, item in enumerate(brief.items, 1):
        regions = ", ".join(item.regions_involved) if item.regions_involved else "—"
        lines += [
            f"### {i}. {item.title}",
            "",
            f"- **Regions:** {regions}",
            f"- **Confidence:** {item.confidence}"
            + (f" — _{item.confidence_note}_" if item.confidence_note else ""),
            "",
            f"**What:** {item.what}",
            "",
            f"**Why it matters:** {item.why_it_matters}",
            "",
            f"**What to watch:** {item.what_to_watch}",
            "",
        ]

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

async def run(end_date: date) -> None:
    _install_patches()

    logger.info("Loading state for %s...", end_date)
    (
        country_ledgers,
        country_entries,
        regional_reports,
        global_ledger,
        story_maps,
    ) = _load_state_for_week(end_date)

    logger.info(
        "Loaded %d country ledgers, %d week-matched entries, %d regional reports",
        len(country_ledgers), len(country_entries), len(regional_reports),
    )

    if not regional_reports:
        logger.error("No regional reports loaded — cannot run executive synthesis")
        sys.exit(1)

    # Run executive analyst with the _eval prompt.
    # NOTE: run_executive_agent mutates global_ledger in place. We NEVER save
    # the result back to disk, so the on-disk ledger is preserved.
    logger.info("Running executive synthesis (eval)...")
    global_ledger = await run_executive_agent(
        regional_reports, global_ledger, end_date,
    )

    # Build structured content. We only use overview.executive_brief here.
    logger.info("Building structured content...")
    overview, _region_pages, _watchlist, _ = build_all_pages(
        global_ledger,
        regional_reports,
        country_ledgers,
        country_entries,
        end_date,
        story_maps=story_maps or None,
    )

    brief = overview.executive_brief
    if not brief.items:
        logger.error("Executive brief has no items after synthesis — nothing to edit")
        sys.exit(1)

    logger.info("Executive brief: %d briefing items to weave", len(brief.items))

    # Editorial chain on the executive brief.
    logger.info("Running executive editor...")
    brief = await edit_executive(brief, analysis_date=end_date)

    logger.info("Running executive copyeditor...")
    brief = await copyedit_executive(brief, analysis_date=end_date)

    logger.info("Running executive style editor...")
    if brief.edited_essay:
        result = await style_edit_prose(
            {"edited_essay": brief.edited_essay},
            "executive",
            analysis_date=end_date,
        )
        brief.edited_essay = result.get("edited_essay", brief.edited_essay)

    # Write markdown output.
    out_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "eval"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "executive.md"
    md_path.write_text(_render_markdown(overview, brief, end_date))
    logger.info("Wrote %s (%d bytes)", md_path, md_path.stat().st_size)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate executive_eval.md + inline EXECUTIVE_EDITOR_SYSTEM edits",
    )
    parser.add_argument("--date", required=True, help="Brief end date (YYYY-MM-DD)")
    args = parser.parse_args()

    end_date = date.fromisoformat(args.date)
    asyncio.run(run(end_date))


if __name__ == "__main__":
    main()
