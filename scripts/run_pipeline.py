"""
Pipeline entrypoint — runs the weekly pipeline, commits results, and pushes.

Usage:
    python scripts/run_pipeline.py --date 2026-02-15
    python scripts/run_pipeline.py                     # auto-detect next date

Local mode:  Runs directly in the repo. Commits ledgers/ + site/briefs/.
Fargate mode: Clones the repo, runs from clone, commits + pushes to main.

Post-pipeline steps (S3 upload, preview email) are stubbed for later.
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("run_pipeline")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("REPO", "j0nathanb/pdb-aggregator")


# =============================================================================
# Date detection
# =============================================================================

def find_last_brief_date(project_root: Path) -> date | None:
    """Find the most recent brief date from site/briefs/."""
    briefs_dir = project_root / "site" / "briefs"
    if not briefs_dir.exists():
        return None
    dates = []
    for d in briefs_dir.iterdir():
        if d.is_dir():
            try:
                dates.append(date.fromisoformat(d.name))
            except ValueError:
                continue
    return max(dates) if dates else None


def determine_end_date(args: argparse.Namespace, project_root: Path) -> str:
    """Use --date if provided, otherwise last brief + 7 days."""
    if args.date:
        return args.date

    last = find_last_brief_date(project_root)
    if last:
        next_date = last + timedelta(days=7)
        logger.info("Last brief: %s → next date: %s", last, next_date)
        return next_date.isoformat()

    logger.warning("No prior briefs found, using today")
    return date.today().isoformat()


# =============================================================================
# Pipeline execution
# =============================================================================

def run_pipeline(end_date: str, project_root: Path, extra_args: list[str] | None = None) -> bool:
    """Run the monitor CLI pipeline via subprocess."""
    cmd = [
        sys.executable, "-m", "src.monitor.cli", "run",
        "--date", end_date,
    ]
    if extra_args:
        cmd.extend(extra_args)

    logger.info("Running: %s", " ".join(cmd))
    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode != 0:
        logger.error("Pipeline failed with exit code %d", result.returncode)
        return False

    logger.info("Pipeline completed successfully")
    return True


# =============================================================================
# Git operations
# =============================================================================

def commit_results(end_date: str, project_root: Path) -> bool:
    """Git add ledgers/ + site/briefs/ and commit if there are changes."""
    try:
        # Check for changes in the paths we care about
        status = subprocess.run(
            ["git", "status", "--porcelain", "ledgers/", "site/briefs/"],
            cwd=project_root, capture_output=True, text=True, check=True,
        )
        if not status.stdout.strip():
            logger.info("No changes to commit")
            return False

        subprocess.run(
            ["git", "add", "ledgers/", "site/briefs/"],
            cwd=project_root, check=True, capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Brief: {end_date}"],
            cwd=project_root, check=True, capture_output=True, text=True,
        )
        logger.info("Committed results for %s", end_date)
        return True

    except subprocess.CalledProcessError as e:
        logger.error("Commit failed: %s", e.stderr if e.stderr else e)
        return False


def push_to_remote(project_root: Path) -> bool:
    """Push to origin main. Skips if GITHUB_TOKEN is not set."""
    if not GITHUB_TOKEN:
        logger.warning("GITHUB_TOKEN not set, skipping push")
        return False

    env = {**os.environ, "GH_TOKEN": GITHUB_TOKEN}
    try:
        subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=project_root, check=True, capture_output=True, text=True, env=env,
        )
        logger.info("Pushed to origin main")
        return True
    except subprocess.CalledProcessError as e:
        logger.error("Push failed: %s", e.stderr)
        return False


# =============================================================================
# Clone (Fargate mode)
# =============================================================================

def clone_repo() -> Path:
    """Shallow-clone the repo for Fargate runs."""
    repo_dir = Path("/tmp/repo")
    if repo_dir.exists():
        shutil.rmtree(repo_dir)

    logger.info("Cloning %s...", REPO)
    subprocess.run(
        ["git", "clone", "--depth", "1",
         f"https://x-access-token:{GITHUB_TOKEN}@github.com/{REPO}.git",
         str(repo_dir)],
        check=True, capture_output=True, text=True,
    )

    # Configure git identity for commits
    subprocess.run(
        ["git", "config", "user.email", "pipeline@middlepowers.fyi"],
        cwd=repo_dir, check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "MPM Pipeline"],
        cwd=repo_dir, check=True, capture_output=True,
    )

    return repo_dir


def is_in_repo() -> bool:
    """Check if we're running inside a git repo (local mode)."""
    return (Path.cwd() / ".git").exists() or (Path(__file__).resolve().parent.parent / ".git").exists()


# =============================================================================
# Stubs (for future Fargate automation)
# =============================================================================

def upload_artifacts(end_date: str, project_root: Path) -> bool:
    """(Stub) Upload brief artifacts to S3."""
    bucket = os.environ.get("ARTIFACTS_BUCKET", "")
    if not bucket:
        logger.info("ARTIFACTS_BUCKET not set, skipping S3 upload")
        return False

    # TODO: Upload site/briefs/{end_date}/ contents to S3
    logger.warning("S3 upload not yet implemented")
    return False


def send_preview_email(end_date: str, pushed: bool) -> bool:
    """(Stub) Send preview email via SES."""
    alert_email = os.environ.get("ALERT_EMAIL", "")
    if not alert_email:
        logger.info("ALERT_EMAIL not set, skipping preview email")
        return False

    # TODO: Read pipeline summary from global ledger, send via SES
    logger.warning("Preview email not yet implemented")
    return False


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run the Middle Powers Monitor pipeline",
    )
    parser.add_argument("--date", help="End date (YYYY-MM-DD). Default: last brief + 7 days.")
    parser.add_argument("--no-commit", action="store_true", help="Skip auto-commit after pipeline")
    parser.add_argument("--no-push", action="store_true", help="Skip push to remote")
    args = parser.parse_args()

    # Determine project root and mode
    if is_in_repo():
        # Local mode — run in the current repo
        project_root = Path(__file__).resolve().parent.parent
        logger.info("Local mode (project root: %s)", project_root)
    else:
        # Fargate mode — clone the repo first
        logger.info("Fargate mode — cloning repo")
        project_root = clone_repo()

    end_date = determine_end_date(args, project_root)

    logger.info("=" * 60)
    logger.info("Middle Powers Monitor Pipeline")
    logger.info("  End date: %s", end_date)
    logger.info("  Project root: %s", project_root)
    logger.info("=" * 60)

    # Step 1: Run the pipeline
    success = run_pipeline(end_date, project_root)
    if not success:
        sys.exit(1)

    # Step 2: Commit results
    committed = False
    if not args.no_commit:
        committed = commit_results(end_date, project_root)

    # Step 3: Push to remote
    pushed = False
    if committed and not args.no_push:
        pushed = push_to_remote(project_root)

    # Step 4: Upload artifacts (stub)
    upload_artifacts(end_date, project_root)

    # Step 5: Send preview email (stub)
    send_preview_email(end_date, pushed)

    logger.info("=" * 60)
    logger.info("Done!")
    logger.info("  Brief: %s", end_date)
    logger.info("  Committed: %s", committed)
    logger.info("  Pushed: %s", pushed)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
