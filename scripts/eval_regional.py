"""
Evaluate a new regional synthesis prompt on one region/date.

Re-runs regional synthesis for a single region on a past brief date using the
`regional_synthesis_eval.md` prompt variant, then runs the downstream editorial
chain (editor → copyeditor → style editor) and writes the result to a markdown
file for review.

Usage:
    python scripts/eval_regional.py --date 2026-03-29 --region western_europe

Outputs:
    briefs/{YYYYMMDD}/eval/regional_{region}.md
        Markdown containing the post-editorial prose (card, lead, gaps) AND the
        raw RegionalReport content (cross-cutting dynamics, gaps, rejected, etc.)
        for side-by-side prompt evaluation.

    briefs/{YYYYMMDD}/traces/regional_{region}_eval.json
        Raw trace of the eval run (the original regional_{region}.json trace is
        left untouched).

Notes:
    - Does NOT overwrite the saved regional report at ledgers/regional/.
    - Does NOT patch the MDX on the published site — this is eval-only.
    - Picks the WeeklyEntry matching --date per country (falls back to latest
      entry with a warning if the week isn't present in that country's ledger).
    - Uses the current (latest) global ledger; only the regional page is
      consumed from build_all_pages, so staleness of the overview page is ok.
"""

import argparse
import asyncio
import logging
import sys
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitor import trace as trace_module
from src.monitor.agents import regional as regional_mod
from src.monitor.agents.regional import RegionalReport, run_regional_synthesis
from src.monitor.config import Region, load_prompt
from src.monitor.ledger.storage import (
    list_country_ledgers,
    load_all_regional_reports,
    load_country_ledger,
    load_global_ledger,
    load_story_map,
)
from src.monitor.newsletter.content_builder import build_all_pages
from src.monitor.newsletter.content_models import RegionPageContent
from src.monitor.newsletter.structured_copyeditor import copyedit_regional
from src.monitor.newsletter.structured_editor import edit_regional, style_edit_prose

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("eval_regional")


# =============================================================================
# Patches: swap in the _eval prompt; redirect regional traces to an _eval suffix
# =============================================================================

def _install_patches() -> None:
    """Reroute regional synthesis to the eval prompt and to eval-suffixed traces.

    Why:
      - The regional agent calls `load_prompt("regional_synthesis", ...)` via
        `_build_system_prompt`, so we override that function to load the `_eval`
        variant instead.
      - The agent also writes its trace via `save_raw_response("regional",
        region.value, ...)` and `update_trace_parsed(...)`, which would overwrite
        the original `briefs/{date}/traces/regional_{region}.json`. We wrap
        those functions so any `agent="regional"` call lands at
        `regional_{region}_eval.json` instead.
    """
    # 1. Prompt loader — use the _eval template.
    def _build_system_prompt_eval(region: Region) -> str:
        display_name = regional_mod.REGION_DISPLAY_NAMES.get(region, region.value)
        country_codes = regional_mod.get_region_countries(region)
        country_list = ", ".join(c.upper() for c in country_codes)
        return load_prompt(
            "eval/regional_synthesis_eval",
            REGION=display_name,
            COUNTRY_LIST=country_list,
        )

    regional_mod._build_system_prompt = _build_system_prompt_eval

    # 2. Trace writers — suffix the label so the original trace is preserved.
    #    regional.py imports these at call time (`from ..trace import ...`),
    #    so patching the attributes on the trace module is sufficient.
    _orig_save = trace_module.save_raw_response
    _orig_update = trace_module.update_trace_parsed

    def _save_raw_eval(agent, label, run_date, **kwargs):
        if agent == "regional":
            label = f"{label}_eval"
        return _orig_save(agent, label, run_date, **kwargs)

    def _update_parsed_eval(agent, label, run_date, parsed_output, diagnostics=None):
        if agent == "regional":
            label = f"{label}_eval"
        return _orig_update(agent, label, run_date, parsed_output, diagnostics)

    trace_module.save_raw_response = _save_raw_eval
    trace_module.update_trace_parsed = _update_parsed_eval

    logger.info("Patches installed: prompt=regional_synthesis_eval, trace label suffix=_eval")


# =============================================================================
# Pipeline state loading (week-specific entries)
# =============================================================================

def _load_state_for_week(end_date: date):
    """Load ledgers + week-specific entries + regional reports + story maps.

    For each country, pick the WeeklyEntry whose week == end_date; fall back to
    the latest entry with a warning if not found. This matters because running
    this script on a past brief means the country ledger's *latest* entry is
    newer than the week being evaluated.
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

    regional_reports = load_all_regional_reports()
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
    page: RegionPageContent,
    report: RegionalReport,
    region: Region,
    end_date: date,
) -> str:
    """Render the evaluated region to markdown: post-edit prose + raw report dump."""
    display = regional_mod.REGION_DISPLAY_NAMES.get(region, region.value)
    week_start = (end_date - timedelta(days=6)).isoformat()

    lines: list[str] = [
        f"# Regional Eval: {display}",
        "",
        f"_Brief week: {week_start} to {end_date.isoformat()}_  ",
        f"_Prompt: `regional_synthesis_eval.md`_",
        "",
        "## Card Summary",
        "",
        page.card_summary or "_(empty)_",
        "",
        "## Regional Lead (post-editorial chain)",
        "",
        page.regional_lead or "_(empty)_",
        "",
    ]

    if page.gap_paragraphs:
        lines += ["## Gap Paragraphs", ""]
        for gp in page.gap_paragraphs:
            lines.append(gp)
            lines.append("")

    lines += [
        "---",
        "",
        "## Raw Regional Synthesis Output (pre-edit)",
        "",
        "### Overview",
        "",
        report.regional_overview or "_(empty)_",
        "",
        f"### Cross-Cutting Dynamics ({len(report.cross_cutting_dynamics)})",
        "",
    ]
    if not report.cross_cutting_dynamics:
        lines += ["_(none)_", ""]
    for i, d in enumerate(report.cross_cutting_dynamics, 1):
        lines += [
            f"#### {i}. {d.title}",
            "",
            f"- **Countries:** {', '.join(d.countries_involved)}",
            f"- **Signal categories:** {', '.join(d.signal_categories)}",
            f"- **Pattern:** {d.pattern_type}  |  **Trend:** {d.trend}  "
            f"|  **Linkage:** {d.linkage_strength}  |  **Confidence:** {d.confidence}",
            "",
            f"**Assessment:** {d.assessment}",
            "",
        ]
        if d.significance:
            lines += [f"**Significance:** {d.significance}", ""]
        if d.linkage_justification:
            lines += [f"**Linkage justification:** {d.linkage_justification}", ""]
        if d.weakest_link:
            lines += [f"**Weakest link:** {d.weakest_link}", ""]
        if d.evidence_against_linkage:
            lines += [f"**Evidence against linkage:** {d.evidence_against_linkage}", ""]
        if d.competing_interpretation:
            lines += [f"**Competing interpretation:** {d.competing_interpretation}", ""]
        if d.confidence_inherited_from:
            inherit = ", ".join(
                f"{k}={v}" for k, v in d.confidence_inherited_from.items()
            )
            lines += [f"**Confidence inherited from:** {inherit}", ""]

    lines += [f"### Gaps ({len(report.gaps)})", ""]
    if not report.gaps:
        lines += ["_(none)_", ""]
    for g in report.gaps:
        lines.append(f"- **Expected:** {g.expected_dynamic}")
        if g.observed:
            lines.append(f"  - Observed: {g.observed}")
        if g.assessment:
            lines.append(f"  - Assessment: {g.assessment}")
    if report.gaps:
        lines.append("")

    lines += [f"### Low Confidence Items ({len(report.low_confidence_items)})", ""]
    if not report.low_confidence_items:
        lines += ["_(none)_", ""]
    for lc in report.low_confidence_items:
        lines.append(f"- (conf {lc.confidence}) {lc.item} — _{lc.origin}_")
        if lc.note:
            lines.append(f"  - Note: {lc.note}")
    if report.low_confidence_items:
        lines.append("")

    lines += [
        f"### Rejected Dynamics ({len(report.dynamics_considered_and_rejected)})",
        "",
    ]
    if not report.dynamics_considered_and_rejected:
        lines += ["_(none)_", ""]
    for r in report.dynamics_considered_and_rejected:
        countries = ", ".join(r.countries) if r.countries else "—"
        lines.append(f"- **{r.candidate_dynamic}** ({countries})")
        lines.append(f"  - Reason: {r.reason_rejected}")
    if report.dynamics_considered_and_rejected:
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# Main
# =============================================================================

async def run(end_date: date, region: Region) -> None:
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
        "Loaded %d country ledgers, %d week-matched entries, %d story maps",
        len(country_ledgers), len(country_entries), len(story_maps),
    )

    # Run regional synthesis for the target region with the _eval prompt.
    logger.info("Running regional synthesis (eval) for %s...", region.value)
    new_report = await run_regional_synthesis(
        region, country_ledgers, country_entries, end_date,
    )
    regional_reports[region] = new_report

    # Build structured content for all pages (we only use the one we care about).
    logger.info("Building structured content...")
    _overview, region_pages, _watchlist, _ = build_all_pages(
        global_ledger,
        regional_reports,
        country_ledgers,
        country_entries,
        end_date,
        story_maps=story_maps or None,
    )

    page = region_pages.get(region)
    if page is None:
        logger.error("build_all_pages did not produce a page for %s", region.value)
        sys.exit(1)

    # Editorial chain on the regional page.
    logger.info("Running regional editor...")
    page = await edit_regional(page, analysis_date=end_date)

    logger.info("Running regional copyeditor...")
    page = await copyedit_regional(page, analysis_date=end_date)

    logger.info("Running regional style editor...")
    if page.regional_lead:
        result = await style_edit_prose(
            {"regional_lead": page.regional_lead, "card_summary": page.card_summary},
            f"regional_{region.value}",
            analysis_date=end_date,
        )
        page.regional_lead = result.get("regional_lead", page.regional_lead)
        if "card_summary" in result:
            page.card_summary = result["card_summary"]

    # Write markdown output.
    out_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d") / "eval"
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"regional_{region.value}.md"
    md_path.write_text(_render_markdown(page, new_report, region, end_date))
    logger.info("Wrote %s (%d bytes)", md_path, md_path.stat().st_size)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate regional_synthesis_eval.md for one region/date",
    )
    parser.add_argument("--date", required=True, help="Brief end date (YYYY-MM-DD)")
    parser.add_argument(
        "--region",
        required=True,
        choices=[r.value for r in Region],
        help="Region to evaluate",
    )
    args = parser.parse_args()

    end_date = date.fromisoformat(args.date)
    region = Region(args.region)

    asyncio.run(run(end_date, region))


if __name__ == "__main__":
    main()
