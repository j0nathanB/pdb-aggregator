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

    # Initialize run recorder and redirect log file into the run folder
    recorder = RunRecorder()
    _add_log_handler(recorder.log_path)

    # Step 1-4: Desk pipeline (triage → country agents → devil's advocate → ledger write)
    print(f"Running desk pipeline (end_date={end_date})...")
    desk_result = await run_desk_pipeline(
        country_codes=country_codes,
        end_date=end_date,
        max_concurrent=args.concurrency,
        skip_triage=args.skip_triage,
        force_deep_dive=args.force_deep_dive,
        recorder=recorder,
    )

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

    # Collect entries and ledgers for downstream steps
    country_entries = {}
    country_ledgers = {}
    for cr in desk_result.country_results:
        if cr.success:
            country_entries[cr.code] = cr.weekly_entry
        if country_ledger_exists(cr.code):
            country_ledgers[cr.code] = load_country_ledger(cr.code)

    if not args.skip_synthesis:
        # Step 5: Regional synthesis
        print("Running regional synthesis...")
        regional_reports = await run_all_regional_syntheses(
            country_ledgers, country_entries, end_date, args.concurrency
        )
        from .ledger.storage import save_regional_report
        for region, report in regional_reports.items():
            save_regional_report(report)
            n_dynamics = len(report.cross_cutting_dynamics)
            print(f"  {region.value}: {n_dynamics} cross-cutting dynamics")

        # Step 6: Executive synthesis
        print("Running executive synthesis...")
        global_ledger = load_global_ledger()
        global_ledger = await run_executive_agent(regional_reports, global_ledger, end_date)
        save_global_ledger(global_ledger)

        latest = global_ledger.latest_entry()
        if latest:
            print(f"  Briefing items: {len(latest.executive_briefing_items)}")
            print(f"  Dynamics created: {latest.dynamics_created}")
            print(f"  Dynamics updated: {latest.dynamics_updated}")

        # Step 7: Newsletter assembly
        print("Assembling newsletter...")
        newsletter = assemble_newsletter(
            global_ledger, regional_reports, country_ledgers, country_entries, end_date
        )

        # Step 8: Editor — rewrite country sections into style-guide prose
        from .agents.editor import edit_newsletter
        print("Editing country sections...")
        newsletter = await edit_newsletter(
            newsletter, country_ledgers, country_entries, max_concurrent=args.concurrency
        )

        # Step 9: Copyeditor — mechanical polish (names, abbreviations)
        from .agents.copyeditor import copyedit_newsletter
        print("Copy-editing...")
        newsletter = await copyedit_newsletter(newsletter, max_concurrent=args.concurrency)

        output_dir = PROJECT_ROOT / "briefs" / end_date.strftime("%Y%m%d")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "newsletter.md"
        output_path.write_text(newsletter)
        print(f"  Newsletter written to {output_path}")

        # Step 10: Publish to Mintlify site
        print("Publishing to site...")
        pages = assemble_newsletter_pages(
            global_ledger, regional_reports, country_ledgers, country_entries, end_date
        )

        # Edit + copyedit multi-page output
        from .agents.editor import edit_region_page, edit_overview_page
        from .agents.copyeditor import copyedit_newsletter as copyedit

        # Edit overview page (executive brief)
        if "overview" in pages:
            latest = global_ledger.latest_entry()
            items = latest.executive_briefing_items if latest else []
            if items:
                print("Editing executive brief...")
                pages["overview"] = await edit_overview_page(pages["overview"], items)
            pages["overview"] = await copyedit(pages["overview"], max_concurrent=args.concurrency)

        # Edit region pages (regional lead + country sections)
        for slug in list(pages.keys()):
            if slug != "overview" and slug != "watchlist":
                pages[slug] = await edit_region_page(
                    pages[slug], regional_reports, country_ledgers, country_entries,
                    max_concurrent=args.concurrency,
                )
                pages[slug] = await copyedit(pages[slug], max_concurrent=args.concurrency)

        brief_dir = publish_brief(pages, end_date)
        print(f"  Site published to {brief_dir}")
    else:
        print("Skipping synthesis and assembly (--skip-synthesis)")

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
    from .ledger.storage import load_all_regional_reports

    end_date = date.fromisoformat(args.date) if args.date else date.today()

    if not global_ledger_exists():
        print("No global ledger found. Run the pipeline first.")
        return

    global_ledger = load_global_ledger()
    country_ledgers = {}
    country_entries: dict = {}
    for code in list_country_ledgers():
        ledger = load_country_ledger(code)
        country_ledgers[code] = ledger
        entry = ledger.latest_entry()
        country_entries[code] = entry

    regional_reports = load_all_regional_reports()

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
    from .ledger.storage import load_all_regional_reports

    end_date = date.fromisoformat(args.date) if args.date else date.today()

    if not global_ledger_exists():
        print("No global ledger found. Run the pipeline first.")
        return

    global_ledger = load_global_ledger()
    country_ledgers = {}
    country_entries: dict = {}
    for code in list_country_ledgers():
        ledger = load_country_ledger(code)
        country_ledgers[code] = ledger
        entry = ledger.latest_entry()
        country_entries[code] = entry

    regional_reports = load_all_regional_reports()

    pages = assemble_newsletter_pages(
        global_ledger, regional_reports, country_ledgers, country_entries, end_date
    )
    brief_dir = publish_brief(pages, end_date)
    print(f"Published {len(pages)} pages to {brief_dir}")


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
    p_run.add_argument("--skip-triage", action="store_true", help="Skip triage, deep dive all")
    p_run.add_argument("--force-deep-dive", action="store_true", help="Force all to deep dive")
    p_run.add_argument("--triage-only", action="store_true", help="Run triage only, no agents")
    p_run.add_argument("--skip-synthesis", action="store_true",
                        help="Skip regional/executive synthesis and newsletter assembly")

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


if __name__ == "__main__":
    main()
