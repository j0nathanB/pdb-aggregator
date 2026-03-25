"""Tests for the run recorder."""

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import pytest

from src.monitor.run_recorder import RunRecorder, _serialize


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
