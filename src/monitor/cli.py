"""
CLI interface for the Middle Powers Monitor pipeline.

Usage:
    python -m src.monitor.cli [command] [options]

Commands:
    run         Run the full weekly pipeline
    init        Initialize ledger(s) for country/countries
    triage      Run triage only (scan + depth decisions)
    assemble    Assemble newsletter from existing data
    status      Show pipeline status (ledger summaries)
"""

import argparse
import asyncio
import json
import logging
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from .config import (
    COUNTRY_LEDGERS_DIR,
    GLOBAL_LEDGER_PATH,
    CONFIGS_DIR,
    PROJECT_ROOT,
    Region,
    load_all_country_configs,
    load_country_config,
)
from .ledger.storage import (
    country_ledger_exists,
    global_ledger_exists,
    init_global_ledger,
    list_country_ledgers,
    load_country_ledger,
    load_global_ledger,
    save_country_ledger,
    save_global_ledger,
)
from .ledger.initialize import initialize_country_ledger

logger = logging.getLogger("monitor")


LOGS_DIR = PROJECT_ROOT / "logs"


def _add_log_handler(log_path: str) -> None:
    """Add an additional DEBUG-level file handler to the root logger."""
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S"))
    logging.getLogger().addHandler(handler)
    logging.getLogger("monitor").info("Also logging to %s", log_path)


def setup_logging(level: str = "INFO", log_file: str | None = None) -> None:
    log_level = getattr(logging, level.upper())
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    # Console handler (respects --log-level)
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(logging.Formatter(fmt, datefmt="%H:%M:%S"))

    handlers: list[logging.Handler] = [console]

    # File handler — always writes at DEBUG level for full trace
    if log_file is None:
        LOGS_DIR.mkdir(exist_ok=True)
        log_file = str(LOGS_DIR / f"pipeline_{date.today().isoformat()}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt=datefmt))
    handlers.append(file_handler)

    logging.basicConfig(level=logging.DEBUG, handlers=handlers)
    # httpx logs full request URLs at INFO, which exposes API tokens passed
    # as query params (Diffbot, SearchAPI). Clamp to WARNING so secrets stay
    # out of stdout, log files, and CloudWatch.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("monitor").info("Logging to %s", log_file)


# =============================================================================
# Commands
# =============================================================================

async def cmd_init(args: argparse.Namespace) -> None:
    """Initialize country ledger(s)."""
    if args.country == "all":
        configs = load_all_country_configs()
        if not configs:
            print("No country configs found in configs/countries/")
            return
        codes = sorted(configs.keys())
    else:
        codes = [args.country]

    for code in codes:
        if country_ledger_exists(code) and not args.force:
            print(f"  {code}: ledger exists (use --force to reinitialize)")
            continue

        config = load_country_config(code)
        print(f"  {code}: initializing {config.country}...")
        ledger = await initialize_country_ledger(config)
        save_country_ledger(ledger)
        print(f"  {code}: done — {len(ledger.structural_claim_status)} structural claims")

    # Initialize global ledger if needed
    if not global_ledger_exists():
        init_global_ledger()
        print("  global: initialized empty global ledger")


STAGE_ORDER = ["desk", "regional", "executive", "newsletter", "publishing"]


def _should_run(stage: str, resume_from: str | None) -> bool:
    """Return True if this stage should execute (not skipped by --resume-from)."""
    if resume_from is None:
        return True
    return STAGE_ORDER.index(stage) >= STAGE_ORDER.index(resume_from)


def _load_pipeline_state(end_date: date) -> tuple[dict, dict, dict, object]:
    """Load all pipeline state from disk for resume or standalone commands.

    Returns (country_ledgers, country_entries, regional_reports, global_ledger).
    """
    from .ledger.storage import load_all_regional_reports

    country_ledgers = {}
    country_entries: dict = {}
    for code in list_country_ledgers():
        ledger = load_country_ledger(code)
        country_ledgers[code] = ledger
        entry = ledger.latest_entry()
        if entry:
            country_entries[code] = entry

    regional_reports = load_all_regional_reports()
    global_ledger = load_global_ledger() if global_ledger_exists() else None
    return country_ledgers, country_entries, regional_reports, global_ledger


async def cmd_run(args: argparse.Namespace) -> None:
    """Run the full weekly pipeline."""
    from .orchestrator import run_desk_pipeline
    from .agents.regional import run_all_regional_syntheses, REGION_COUNTRIES
    from .agents.executive import run_executive_agent
    from .newsletter.assembly import assemble_newsletter, assemble_newsletter_pages
    from .newsletter.publish import publish_brief
    from .run_recorder import RunRecorder

    end_date = date.fromisoformat(args.date) if args.date else date.today()
    country_codes = [args.country] if args.country else None
    resume_from = getattr(args, "resume_from", None)

    # Validate mutually exclusive flags
    if resume_from and args.skip_synthesis:
        print("Error: --resume-from and --skip-synthesis are mutually exclusive.")
        return
    if resume_from and args.triage_only:
        print("Error: --resume-from and --triage-only are mutually exclusive.")
        return

    # Initialize run recorder and redirect log file into the run folder
    recorder = RunRecorder()
    _add_log_handler(recorder.log_path)
    recorder.init_manifest(end_date, country_codes)

    # Hash prompts and reset diagnostics counters
    from .sanitize import reset_fallback_counts, get_fallback_summary
    reset_fallback_counts()
    prompt_hashes = recorder.record_prompt_hashes()

    # Validate prior run on resume
    if resume_from:
        prior = RunRecorder.find_latest_manifest()
        if prior is None:
            print("No prior run with manifest found. Run without --resume-from first.")
            return
        _, prior_manifest = prior
        prior_date = prior_manifest.get("end_date")
        if prior_date != end_date.isoformat():
            print(f"Warning: prior run was for {prior_date}, resuming for {end_date}")
        # Check for prompt changes since prior run
        changed = RunRecorder.check_prompt_changes(prompt_hashes, prior_manifest)
        if changed:
            print(f"Warning: prompts changed since prior run: {', '.join(changed)}")
        print(f"Resuming from {resume_from} (prior run: {prior_manifest.get('run_id')})")
    else:
        # Snapshot ledgers before any mutations (fresh runs only)
        recorder.snapshot_ledgers()

    # Pre-load state from disk when resuming
    country_entries: dict = {}
    country_ledgers: dict = {}
    regional_reports: dict = {}
    global_ledger = None

    if resume_from:
        country_ledgers, country_entries, regional_reports, global_ledger = _load_pipeline_state(end_date)

    # ---- Stage: desk ----
    if _should_run("desk", resume_from):
        recorder.start_stage("desk")
        try:
            print(f"Running desk pipeline (end_date={end_date})...")
            desk_result = await run_desk_pipeline(
                country_codes=country_codes,
                end_date=end_date,
                max_concurrent=args.concurrency,
                skip_triage=args.skip_triage,
                recorder=recorder,
            )
            recorder.complete_stage("desk")
        except Exception as e:
            recorder.fail_stage("desk", str(e))
            raise

        print(
            f"  Desk: {len(desk_result.deep_dive_results)} deep dives, "
            f"{len(desk_result.maintenance_results)} maintenance, "
            f"{len(desk_result.failed_results)} failed"
        )

        if desk_result.failed_results:
            for r in desk_result.failed_results:
                print(f"  FAILED: {r.code} — {r.error}")

        if args.triage_only:
            if desk_result.triage:
                print("\nTriage decisions:")
                for d in desk_result.triage.decisions:
                    print(f"  {d.code}: {d.depth.value} — {d.rationale[:100]}")
            return

        # Collect entries and ledgers from desk results
        for cr in desk_result.country_results:
            if cr.success:
                country_entries[cr.code] = cr.weekly_entry
            if country_ledger_exists(cr.code):
                country_ledgers[cr.code] = load_country_ledger(cr.code)
    else:
        recorder.skip_stage("desk")

    if args.skip_synthesis:
        print("Skipping synthesis and assembly (--skip-synthesis)")
        print("Done.")
        return

    # ---- Stage: regional ----
    if _should_run("regional", resume_from):
        recorder.start_stage("regional")
        try:
            print("Running regional synthesis...")
            regional_reports = await run_all_regional_syntheses(
                country_ledgers, country_entries, end_date, args.concurrency
            )
            from .ledger.storage import save_regional_report
            for region, report in regional_reports.items():
                save_regional_report(report)
                n_dynamics = len(report.cross_cutting_dynamics)
                print(f"  {region.value}: {n_dynamics} cross-cutting dynamics")
            recorder.complete_stage("regional")
        except Exception as e:
            recorder.fail_stage("regional", str(e))
            raise
    else:
        recorder.skip_stage("regional")

    # ---- Stage: executive ----
    if _should_run("executive", resume_from):
        recorder.start_stage("executive")
        try:
            print("Running executive synthesis...")
            global_ledger = load_global_ledger()
            global_ledger = await run_executive_agent(regional_reports, global_ledger, end_date)
            save_global_ledger(global_ledger)

            latest = global_ledger.latest_entry()
            if latest:
                print(f"  Briefing items: {len(latest.executive_briefing_items)}")
                print(f"  Dynamics created: {latest.dynamics_created}")
                print(f"  Dynamics updated: {latest.dynamics_updated}")
            recorder.complete_stage("executive")
        except Exception as e:
            recorder.fail_stage("executive", str(e))
            raise
    else:
        recorder.skip_stage("executive")
        if global_ledger is None:
            global_ledger = load_global_ledger()

    # ---- Stage: newsletter (structured content → editor → copyeditor) ----
    if _should_run("newsletter", resume_from):
        recorder.start_stage("newsletter")
        try:
            from .newsletter.content_builder import build_all_pages
            from .newsletter.structured_editor import edit_all, style_edit_all
            from .newsletter.structured_copyeditor import copyedit_all
            from .newsletter.regional_writer import write_all_regional_essays
            from .newsletter.global_writer import write_global_essay

            print("Building structured content...")
            from .ledger.storage import load_story_map
            story_maps_data: dict[str, dict] = {}
            for code in country_ledgers:
                try:
                    story_maps_data[code] = load_story_map(code, end_date)
                except FileNotFoundError:
                    pass

            overview_content, region_page_contents, watchlist_content, at_a_glance_content = build_all_pages(
                global_ledger, regional_reports, country_ledgers, country_entries, end_date,
                story_maps=story_maps_data or None,
            )

            # Round 1: Edit country summaries + watchlist
            print("Round 1: Editing country summaries...")
            overview_content, region_page_contents, watchlist_content = await edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="countries",
            )
            overview_content, region_page_contents, watchlist_content = await copyedit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="countries",
            )
            overview_content, region_page_contents, watchlist_content = await style_edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="countries",
            )

            # Regional Writer: produce regional essays from edited country prose
            print("Writing regional essays...")
            region_page_contents = await write_all_regional_essays(
                region_page_contents, max_concurrent=args.concurrency,
            )

            # Round 2: Edit regional essays
            print("Round 2: Editing regional essays...")
            overview_content, region_page_contents, watchlist_content = await edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="regional",
            )
            overview_content, region_page_contents, watchlist_content = await copyedit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="regional",
            )
            overview_content, region_page_contents, watchlist_content = await style_edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="regional",
            )

            # Global Writer: produce global essay from edited regional prose
            print("Writing global essay...")
            overview_content = await write_global_essay(
                overview_content, region_page_contents,
            )

            # Round 3: Edit global essay
            print("Round 3: Editing global essay...")
            overview_content, region_page_contents, watchlist_content = await edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="executive",
            )
            overview_content, region_page_contents, watchlist_content = await copyedit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="executive",
            )
            overview_content, region_page_contents, watchlist_content = await style_edit_all(
                overview_content, region_page_contents, watchlist_content,
                analysis_date=end_date, max_concurrent=args.concurrency, scope="executive",
            )

            recorder.complete_stage("newsletter")
        except Exception as e:
            recorder.fail_stage("newsletter", str(e))
            raise
    else:
        recorder.skip_stage("newsletter")
        # Build unedited content for the publishing stage
        from .newsletter.content_builder import build_all_pages as _build
        from .ledger.storage import load_story_map
        _sm: dict[str, dict] = {}
        for code in country_ledgers:
            try:
                _sm[code] = load_story_map(code, end_date)
            except FileNotFoundError:
                pass
        overview_content, region_page_contents, watchlist_content, at_a_glance_content = _build(
            global_ledger, regional_reports, country_ledgers, country_entries, end_date,
            story_maps=_sm or None,
        )

    # ---- Stage: publishing (render templates → MDX → publish) ----
    if _should_run("publishing", resume_from):
        recorder.start_stage("publishing")
        try:
            from .newsletter.renderer import render_pages

            print("Rendering templates → MDX...")
            pages = render_pages(overview_content, region_page_contents, watchlist_content, at_a_glance_content)

            brief_dir = publish_brief(pages, end_date)
            print(f"  Site published to {brief_dir}")
            recorder.complete_stage("publishing")
        except Exception as e:
            recorder.fail_stage("publishing", str(e))
            raise
    else:
        recorder.skip_stage("publishing")

    # Print cost and diagnostics summary
    if recorder._manifest and "usage" in recorder._manifest:
        usage = recorder._manifest["usage"]
        print(f"\nToken usage: {usage['total_input_tokens']:,} in / {usage['total_output_tokens']:,} out")
        print(f"Estimated cost: ${usage.get('estimated_cost_usd', 0):.2f}")

    fallbacks = get_fallback_summary()
    if fallbacks:
        total = sum(fallbacks.values())
        print(f"Parse fallbacks: {total} total across {len(fallbacks)} contexts")
        for ctx, count in sorted(fallbacks.items(), key=lambda x: -x[1])[:5]:
            print(f"  {ctx}: {count}")

    print("Done.")


async def cmd_triage(args: argparse.Namespace) -> None:
    """Run triage only."""
    from .agents.triage import run_triage

    end_date = date.fromisoformat(args.date) if args.date else date.today()
    configs = load_all_country_configs()

    ledgers = {}
    for code in configs:
        if country_ledger_exists(code):
            ledgers[code] = load_country_ledger(code)

    global_ledger = load_global_ledger() if global_ledger_exists() else None

    print(f"Running triage for {len(configs)} countries...")
    output = await run_triage(
        list(configs.values()), ledgers, global_ledger, end_date, args.concurrency
    )

    print(f"\nDeep dive ({len(output.deep_dive_countries)}):")
    for d in output.decisions:
        if d.depth.value == "deep_dive":
            triggers = ", ".join(d.triggered_by) if d.triggered_by else "none"
            print(f"  {d.code} ({d.country}): [{triggers}] {d.rationale[:120]}")

    print(f"\nMaintenance ({len(output.maintenance_countries)}):")
    for d in output.decisions:
        if d.depth.value == "maintenance":
            print(f"  {d.code} ({d.country})")


async def cmd_assemble(args: argparse.Namespace) -> None:
    """Assemble newsletter from existing ledger data."""
    from .newsletter.assembly import assemble_newsletter

    end_date = date.fromisoformat(args.date) if args.date else date.today()

    if not global_ledger_exists():
        print("No global ledger found. Run the pipeline first.")
        return

    country_ledgers, country_entries, regional_reports, global_ledger = _load_pipeline_state(end_date)

    newsletter = assemble_newsletter(
        global_ledger, regional_reports, country_ledgers, country_entries, end_date
    )

    if args.output:
        Path(args.output).write_text(newsletter)
        print(f"Newsletter written to {args.output}")
    else:
        print(newsletter)


def cmd_publish(args: argparse.Namespace) -> None:
    """Publish existing ledger data to the Mintlify site (no LLM calls)."""
    from .newsletter.assembly import assemble_newsletter_pages
    from .newsletter.publish import publish_brief

    end_date = date.fromisoformat(args.date) if args.date else date.today()

    if not global_ledger_exists():
        print("No global ledger found. Run the pipeline first.")
        return

    country_ledgers, country_entries, regional_reports, global_ledger = _load_pipeline_state(end_date)

    from .ledger.storage import load_story_map
    story_maps_data: dict[str, dict] = {}
    for code in country_ledgers:
        try:
            story_maps_data[code] = load_story_map(code, end_date)
        except FileNotFoundError:
            pass

    pages = assemble_newsletter_pages(
        global_ledger, regional_reports, country_ledgers, country_entries, end_date,
        story_maps=story_maps_data or None,
    )
    brief_dir = publish_brief(pages, end_date)
    print(f"Published {len(pages)} pages to {brief_dir}")


def cmd_replay(args: argparse.Namespace) -> None:
    """Replay parsing from saved traces — no API calls needed."""
    from .trace import list_traces, load_trace, update_trace_parsed

    run_date = date.fromisoformat(args.date)
    traces = list_traces(run_date)

    if not traces:
        print(f"No traces found for {run_date}")
        return

    # Filter by agent/label
    if args.agent:
        traces = [t for t in traces if t["agent"] == args.agent]
    if args.label:
        traces = [t for t in traces if t["label"] == args.label]

    if not traces:
        print("No matching traces found.")
        return

    # Parser dispatch table — maps agent names to parse functions
    from .agents.executive import parse_executive_response
    from .agents.country import parse_country_response
    from .agents.regional import parse_regional_response
    from .agents.devils_advocate import parse_devils_advocate_response
    from .agents.triage import parse_triage_response
    from .agents.story_map import parse_story_map_response
    from .agents.government import _parse_response as parse_government_response

    replayed = 0
    skipped = 0
    failed = 0

    for trace in traces:
        agent = trace["agent"]
        label = trace["label"]
        status = trace.get("status", "parsed")  # old traces without status are treated as parsed

        if status == "parsed" and not args.force:
            skipped += 1
            continue

        response_text = trace["output"]["response_text"]
        if not response_text:
            print(f"  {agent}/{label}: no response_text, skipping")
            skipped += 1
            continue

        try:
            parsed = None
            if agent == "executive":
                parsed = parse_executive_response(response_text)
            elif agent == "country":
                from .agents.country import CountryLedger
                parsed = parse_country_response(response_text, run_date, f"replay", None)
            elif agent == "regional":
                from .config import Region
                try:
                    region = Region(label)
                except ValueError:
                    region = Region.AMERICAS
                parsed = parse_regional_response(response_text, region, run_date)
            elif agent == "devils_advocate":
                parsed = parse_devils_advocate_response(response_text)
            elif agent == "triage":
                decisions, summary = parse_triage_response(response_text)
                parsed = {"decisions": [d.__dict__ for d in decisions], "summary": summary}
            elif agent == "story_map":
                parsed = parse_story_map_response(response_text)
            elif agent == "government":
                parsed = parse_government_response(response_text)
            else:
                print(f"  {agent}/{label}: no parser for agent '{agent}', skipping")
                skipped += 1
                continue

            update_trace_parsed(agent, label, run_date, parsed_output=parsed)
            print(f"  {agent}/{label}: replayed successfully")
            replayed += 1

        except Exception as e:
            print(f"  {agent}/{label}: parse failed — {e}")
            failed += 1

    print(f"\nReplay complete: {replayed} replayed, {skipped} skipped, {failed} failed")


def cmd_status(args: argparse.Namespace) -> None:
    """Show pipeline status."""
    # Configs
    configs = load_all_country_configs()
    print(f"Configured countries: {len(configs)}")
    for code in sorted(configs):
        cfg = configs[code]
        status = "✓" if country_ledger_exists(code) else "—"
        print(f"  {status} {code} ({cfg.country}) [{cfg.tier.value}]")

    # Ledgers
    ledger_codes = list_country_ledgers()
    print(f"\nInitialized ledgers: {len(ledger_codes)}")
    for code in ledger_codes:
        ledger = load_country_ledger(code)
        ps = ledger.posture_summary
        print(
            f"  {code}: {len(ledger.weekly_entries)} entries, "
            f"last_updated={ledger.last_updated}, "
            f"maintenance_weeks={ps.consecutive_maintenance_weeks}"
        )
        if ledger.needs_deep_dive:
            print(f"       ⚠ Staleness override pending")

    # Global ledger
    print()
    if global_ledger_exists():
        gl = load_global_ledger()
        print(f"Global ledger: {len(gl.active_dynamics)} active dynamics, "
              f"{len(gl.watchlist)} watchlist items, "
              f"last_updated={gl.last_updated}")
    else:
        print("Global ledger: not initialized")


# =============================================================================
# Argument parsing
# =============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="monitor",
        description="Middle Powers Monitor — weekly geopolitical analysis pipeline",
    )
    parser.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Console log level (file always logs at DEBUG)",
    )
    parser.add_argument(
        "--log-file",
        help="Log file path (default: logs/pipeline_YYYY-MM-DD.log)",
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init
    p_init = subparsers.add_parser("init", help="Initialize country ledger(s)")
    p_init.add_argument("country", help="Country code or 'all'")
    p_init.add_argument("--force", action="store_true", help="Reinitialize existing ledgers")

    # run
    p_run = subparsers.add_parser("run", help="Run the full weekly pipeline")
    p_run.add_argument("--country", help="Single country code to process")
    p_run.add_argument("--date", help="End date (YYYY-MM-DD), default today")
    p_run.add_argument("--concurrency", type=int, default=5, help="Max concurrent API calls")
    p_run.add_argument("--skip-triage", action="store_true", help="Skip triage scan entirely")
    p_run.add_argument("--triage-only", action="store_true", help="Run triage only, no agents")
    p_run.add_argument("--skip-synthesis", action="store_true",
                        help="Skip regional/executive synthesis and newsletter assembly")
    p_run.add_argument("--resume-from",
                        choices=["regional", "executive", "newsletter", "publishing"],
                        help="Resume from this stage (skips prior stages, loads state from disk)")

    # triage
    p_triage = subparsers.add_parser("triage", help="Run triage only")
    p_triage.add_argument("--date", help="End date (YYYY-MM-DD)")
    p_triage.add_argument("--concurrency", type=int, default=10)

    # assemble
    p_assemble = subparsers.add_parser("assemble", help="Assemble newsletter from existing data")
    p_assemble.add_argument("--date", help="End date (YYYY-MM-DD)")
    p_assemble.add_argument("--output", "-o", help="Output file path")

    # publish
    p_publish = subparsers.add_parser("publish", help="Publish brief to Mintlify site")
    p_publish.add_argument("--date", help="End date (YYYY-MM-DD)")

    # replay
    p_replay = subparsers.add_parser("replay", help="Replay parsing from saved traces (no API calls)")
    p_replay.add_argument("--date", required=True, help="Run date (YYYY-MM-DD)")
    p_replay.add_argument("--agent", help="Filter to specific agent (e.g. executive, country)")
    p_replay.add_argument("--label", help="Filter to specific label (e.g. mx, global)")
    p_replay.add_argument("--force", action="store_true", help="Re-parse even if already parsed")

    # status
    subparsers.add_parser("status", help="Show pipeline status")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    setup_logging(args.log_level, log_file=args.log_file)

    if args.command == "status":
        cmd_status(args)
    elif args.command == "init":
        asyncio.run(cmd_init(args))
    elif args.command == "run":
        asyncio.run(cmd_run(args))
    elif args.command == "triage":
        asyncio.run(cmd_triage(args))
    elif args.command == "assemble":
        asyncio.run(cmd_assemble(args))
    elif args.command == "publish":
        cmd_publish(args)
    elif args.command == "replay":
        cmd_replay(args)


if __name__ == "__main__":
    main()
