"""Tests for the run recorder."""

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import pytest

from src.monitor.run_recorder import RunRecorder, STAGE_ORDER, _serialize


@dataclass
class FakeResult:
    code: str
    values: list[str] = field(default_factory=list)


class TestSerialize:
    def test_primitives(self):
        assert _serialize("hello") == "hello"
        assert _serialize(42) == 42
        assert _serialize(True) is True

    def test_date(self):
        assert _serialize(date(2026, 3, 23)) == "2026-03-23"

    def test_dict(self):
        assert _serialize({"a": 1, "b": date(2026, 1, 1)}) == {"a": 1, "b": "2026-01-01"}

    def test_list(self):
        assert _serialize([1, "two", date(2026, 1, 1)]) == [1, "two", "2026-01-01"]

    def test_set(self):
        result = _serialize({3, 1, 2})
        assert result == [1, 2, 3]

    def test_dataclass(self):
        result = _serialize(FakeResult(code="mx", values=["a", "b"]))
        assert result == {"code": "mx", "values": ["a", "b"]}

    def test_none(self):
        assert _serialize(None) is None


class TestRunRecorder:
    def test_creates_run_dir(self, tmp_path):
        run_dir = tmp_path / "test_run"
        recorder = RunRecorder(run_dir=run_dir)
        assert run_dir.exists()

    def test_write_step(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run1")
        path = recorder.write("01_layer2", {"code": "mx", "count": 5}, suffix="_mx")
        assert path.name == "01_layer2_mx.json"
        data = json.loads(path.read_text())
        assert data == {"code": "mx", "count": 5}

    def test_write_dataclass(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run2")
        path = recorder.write("04_expansion", FakeResult("br", ["x"]), suffix="_br")
        data = json.loads(path.read_text())
        assert data == {"code": "br", "values": ["x"]}

    def test_write_summary(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run3")
        path = recorder.write_summary({"deep_dives": ["mx"], "failed": []})
        assert path.name == "99_pipeline_summary.json"

    def test_log_path(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run4")
        assert recorder.log_path.endswith("pipeline.log")

    def test_default_run_dir_uses_timestamp(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.monitor.run_recorder.RUNS_DIR", tmp_path)
        recorder = RunRecorder()
        assert recorder.run_dir.parent == tmp_path
        # Folder name should be YYYYMMDD_HHMMSS format
        name = recorder.run_dir.name
        assert len(name) == 15  # 8 + 1 + 6
        assert name[8] == "_"


class TestManifest:
    def test_init_manifest_creates_file(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run")
        path = recorder.init_manifest(date(2026, 3, 14), None)
        assert path.name == "manifest.json"
        manifest = json.loads(path.read_text())
        assert manifest["end_date"] == "2026-03-14"
        assert manifest["country_codes"] is None
        for stage in STAGE_ORDER:
            assert manifest["stages"][stage]["status"] == "pending"

    def test_init_manifest_with_country_codes(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.init_manifest(date(2026, 3, 14), ["mx", "br"])
        manifest = json.loads((tmp_path / "run" / "manifest.json").read_text())
        assert manifest["country_codes"] == ["mx", "br"]

    def test_stage_lifecycle(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.init_manifest(date(2026, 3, 14), None)

        recorder.start_stage("desk")
        manifest = json.loads((tmp_path / "run" / "manifest.json").read_text())
        assert manifest["stages"]["desk"]["status"] == "running"
        assert "started_at" in manifest["stages"]["desk"]

        recorder.complete_stage("desk")
        manifest = json.loads((tmp_path / "run" / "manifest.json").read_text())
        assert manifest["stages"]["desk"]["status"] == "completed"
        assert "completed_at" in manifest["stages"]["desk"]

    def test_fail_stage(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.init_manifest(date(2026, 3, 14), None)
        recorder.start_stage("executive")
        recorder.fail_stage("executive", "rate limit exceeded")
        manifest = json.loads((tmp_path / "run" / "manifest.json").read_text())
        assert manifest["stages"]["executive"]["status"] == "failed"
        assert manifest["stages"]["executive"]["error"] == "rate limit exceeded"

    def test_skip_stage(self, tmp_path):
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.init_manifest(date(2026, 3, 14), None)
        recorder.skip_stage("desk")
        manifest = json.loads((tmp_path / "run" / "manifest.json").read_text())
        assert manifest["stages"]["desk"]["status"] == "skipped"

    def test_manifest_noop_without_init(self, tmp_path):
        """Stage methods are no-ops if init_manifest was never called."""
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.start_stage("desk")  # should not raise
        assert not (tmp_path / "run" / "manifest.json").exists()

    def test_manifest_atomic_write(self, tmp_path):
        """Manifest uses tmp+rename — no .tmp file left behind."""
        recorder = RunRecorder(run_dir=tmp_path / "run")
        recorder.init_manifest(date(2026, 3, 14), None)
        assert not (tmp_path / "run" / "manifest.tmp").exists()
        assert (tmp_path / "run" / "manifest.json").exists()


class TestFindLatestManifest:
    def test_finds_most_recent(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.monitor.run_recorder.RUNS_DIR", tmp_path)

        # Create two runs — the later one should be found
        r1 = RunRecorder(run_dir=tmp_path / "20260314_100000")
        r1.init_manifest(date(2026, 3, 14), None)

        r2 = RunRecorder(run_dir=tmp_path / "20260321_100000")
        r2.init_manifest(date(2026, 3, 21), None)

        result = RunRecorder.find_latest_manifest()
        assert result is not None
        recorder, manifest = result
        assert manifest["end_date"] == "2026-03-21"

    def test_returns_none_when_no_manifests(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.monitor.run_recorder.RUNS_DIR", tmp_path)
        assert RunRecorder.find_latest_manifest() is None

    def test_returns_none_when_no_runs_dir(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.monitor.run_recorder.RUNS_DIR", tmp_path / "nonexistent")
        assert RunRecorder.find_latest_manifest() is None

    def test_skips_runs_without_manifest(self, monkeypatch, tmp_path):
        monkeypatch.setattr("src.monitor.run_recorder.RUNS_DIR", tmp_path)

        # Old run without manifest
        (tmp_path / "20260314_100000").mkdir()
        (tmp_path / "20260314_100000" / "01_layer2.json").write_text("{}")

        # Newer run with manifest
        r = RunRecorder(run_dir=tmp_path / "20260321_100000")
        r.init_manifest(date(2026, 3, 21), None)

        result = RunRecorder.find_latest_manifest()
        assert result is not None
        _, manifest = result
        assert manifest["end_date"] == "2026-03-21"


class TestSnapshotLedgers:
    def test_snapshot_copies_ledgers(self, tmp_path, monkeypatch):
        # Set up fake ledger directories
        countries_dir = tmp_path / "ledgers" / "countries"
        countries_dir.mkdir(parents=True)
        (countries_dir / "mx.json").write_text('{"code": "mx"}')
        (countries_dir / "br.json").write_text('{"code": "br"}')

        global_path = tmp_path / "ledgers" / "global.json"
        global_path.write_text('{"last_updated": "2026-03-14"}')

        regional_dir = tmp_path / "ledgers" / "regional"
        regional_dir.mkdir()
        (regional_dir / "americas.json").write_text('{"region": "americas"}')

        monkeypatch.setattr("src.monitor.run_recorder.PROJECT_ROOT", tmp_path)
        # Patch the config imports used inside snapshot_ledgers
        monkeypatch.setattr("src.monitor.config.PROJECT_ROOT", tmp_path)
        monkeypatch.setattr("src.monitor.config.COUNTRY_LEDGERS_DIR", countries_dir)
        monkeypatch.setattr("src.monitor.config.GLOBAL_LEDGER_PATH", global_path)
        monkeypatch.setattr("src.monitor.config.REGIONAL_REPORTS_DIR", regional_dir)

        run_dir = tmp_path / "runs" / "test_run"
        recorder = RunRecorder(run_dir=run_dir)
        snap_dir = recorder.snapshot_ledgers()

        assert (snap_dir / "countries" / "mx.json").exists()
        assert (snap_dir / "countries" / "br.json").exists()
        assert (snap_dir / "global.json").exists()
        assert (snap_dir / "regional" / "americas.json").exists()

        # Verify content matches
        assert json.loads((snap_dir / "countries" / "mx.json").read_text()) == {"code": "mx"}

    def test_snapshot_handles_missing_dirs(self, tmp_path, monkeypatch):
        """Snapshot doesn't fail if some ledger dirs don't exist yet."""
        monkeypatch.setattr("src.monitor.config.COUNTRY_LEDGERS_DIR", tmp_path / "nope")
        monkeypatch.setattr("src.monitor.config.GLOBAL_LEDGER_PATH", tmp_path / "nope.json")
        monkeypatch.setattr("src.monitor.config.REGIONAL_REPORTS_DIR", tmp_path / "also_nope")

        recorder = RunRecorder(run_dir=tmp_path / "run")
        snap_dir = recorder.snapshot_ledgers()
        assert snap_dir.exists()
        # No files copied, but no error
        assert list(snap_dir.iterdir()) == []
