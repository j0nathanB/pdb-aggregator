"""Tests for CLI argument parsing and command routing."""

import pytest
from src.monitor.cli import build_parser, _should_run


class TestParser:
    def test_no_command_shows_help(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.command is None

    def test_init_command(self):
        parser = build_parser()
        args = parser.parse_args(["init", "mx"])
        assert args.command == "init"
        assert args.country == "mx"
        assert not args.force

    def test_init_force(self):
        parser = build_parser()
        args = parser.parse_args(["init", "mx", "--force"])
        assert args.force

    def test_init_all(self):
        parser = build_parser()
        args = parser.parse_args(["init", "all"])
        assert args.country == "all"

    def test_run_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["run"])
        assert args.command == "run"
        assert args.country is None
        assert args.date is None
        assert args.concurrency == 5
        assert not args.skip_triage
        assert not args.triage_only

    def test_run_single_country(self):
        parser = build_parser()
        args = parser.parse_args(["run", "--country", "mx"])
        assert args.country == "mx"

    def test_run_with_date(self):
        parser = build_parser()
        args = parser.parse_args(["run", "--date", "2026-03-14"])
        assert args.date == "2026-03-14"

    def test_run_flags(self):
        parser = build_parser()
        args = parser.parse_args([
            "run", "--skip-triage", "--triage-only",
            "--concurrency", "10",
        ])
        assert args.skip_triage
        assert args.triage_only
        assert args.concurrency == 10

    def test_run_skip_synthesis(self):
        parser = build_parser()
        args = parser.parse_args(["run", "--skip-synthesis"])
        assert args.skip_synthesis

    def test_run_resume_from(self):
        parser = build_parser()
        args = parser.parse_args(["run", "--resume-from", "publishing"])
        assert args.resume_from == "publishing"

    def test_run_resume_from_all_choices(self):
        parser = build_parser()
        for choice in ["regional", "executive", "newsletter", "publishing"]:
            args = parser.parse_args(["run", "--resume-from", choice])
            assert args.resume_from == choice

    def test_run_resume_from_invalid(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["run", "--resume-from", "desk"])

    def test_run_resume_from_default_is_none(self):
        parser = build_parser()
        args = parser.parse_args(["run"])
        assert args.resume_from is None


class TestShouldRun:
    def test_no_resume_runs_everything(self):
        for stage in ["desk", "regional", "executive", "newsletter", "publishing"]:
            assert _should_run(stage, None) is True

    def test_resume_from_regional_skips_desk(self):
        assert _should_run("desk", "regional") is False
        assert _should_run("regional", "regional") is True
        assert _should_run("executive", "regional") is True
        assert _should_run("publishing", "regional") is True

    def test_resume_from_publishing_skips_all_but_publishing(self):
        assert _should_run("desk", "publishing") is False
        assert _should_run("regional", "publishing") is False
        assert _should_run("executive", "publishing") is False
        assert _should_run("newsletter", "publishing") is False
        assert _should_run("publishing", "publishing") is True


    def test_triage_command(self):
        parser = build_parser()
        args = parser.parse_args(["triage", "--date", "2026-03-14"])
        assert args.command == "triage"
        assert args.date == "2026-03-14"

    def test_assemble_command(self):
        parser = build_parser()
        args = parser.parse_args(["assemble", "--output", "out.md"])
        assert args.command == "assemble"
        assert args.output == "out.md"

    def test_status_command(self):
        parser = build_parser()
        args = parser.parse_args(["status"])
        assert args.command == "status"

    def test_log_level(self):
        parser = build_parser()
        args = parser.parse_args(["--log-level", "DEBUG", "status"])
        assert args.log_level == "DEBUG"


class TestStatusCommand:
    def test_runs_without_error(self, tmp_path, monkeypatch):
        """Status command should work even with no data."""
        import src.monitor.config as cfg
        import src.monitor.ledger.storage as storage

        # Point to empty dirs
        monkeypatch.setattr(cfg, "CONFIGS_DIR", tmp_path / "configs")
        (tmp_path / "configs").mkdir()
        monkeypatch.setattr(storage, "COUNTRY_LEDGERS_DIR", tmp_path / "ledgers")
        (tmp_path / "ledgers").mkdir()
        monkeypatch.setattr(storage, "GLOBAL_LEDGER_PATH", tmp_path / "global.json")

        from src.monitor.cli import cmd_status
        import argparse
        # Should not raise
        cmd_status(argparse.Namespace())
