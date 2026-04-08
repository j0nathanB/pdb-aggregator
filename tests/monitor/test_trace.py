"""Tests for the trace persistence module (two-phase trace writes)."""

import json
from datetime import date
from pathlib import Path

import pytest

from src.monitor.trace import (
    save_raw_response,
    save_trace,
    update_trace_parsed,
    load_trace,
    list_traces,
    _trace_path,
)


@pytest.fixture
def trace_dir(tmp_path, monkeypatch):
    """Point traces to a temp directory."""
    monkeypatch.setattr("src.monitor.trace.PROJECT_ROOT", tmp_path)
    return tmp_path


class TestSaveRawResponse:
    def test_creates_trace_with_status_raw(self, trace_dir):
        path = save_raw_response(
            "executive", "global", date(2026, 3, 14),
            system_prompt="You are an analyst.",
            user_message="Analyze this.",
            response_text='{"some": "json"}',
            thinking_text="I think...",
            usage={"input_tokens": 1000, "output_tokens": 500},
        )
        assert path.exists()
        trace = json.loads(path.read_text())
        assert trace["status"] == "raw"
        assert trace["agent"] == "executive"
        assert trace["label"] == "global"
        assert trace["output"]["response_text"] == '{"some": "json"}'
        assert trace["output"]["parsed"] is None
        assert trace["output"]["thinking"] == "I think..."
        assert trace["usage"]["input_tokens"] == 1000

    def test_saves_extra_metadata(self, trace_dir):
        save_raw_response(
            "country", "mx", date(2026, 3, 14),
            response_text="test",
            extra={"search_log": [{"query": "mexico", "results_count": 5}]},
        )
        trace = load_trace("country", "mx", date(2026, 3, 14))
        assert trace["extra"]["search_log"][0]["query"] == "mexico"

    def test_filename_sanitization(self, trace_dir):
        path = save_raw_response(
            "editor", "regional/americas", date(2026, 3, 14),
            response_text="test",
        )
        assert "editor_regional_americas.json" == path.name


class TestUpdateTraceParsed:
    def test_updates_status_to_parsed(self, trace_dir):
        save_raw_response(
            "executive", "global", date(2026, 3, 14),
            response_text='{"key": "value"}',
        )
        update_trace_parsed(
            "executive", "global", date(2026, 3, 14),
            parsed_output={"key": "value"},
        )
        trace = load_trace("executive", "global", date(2026, 3, 14))
        assert trace["status"] == "parsed"
        assert trace["output"]["parsed"] == {"key": "value"}
        assert trace["output"]["response_text"] == '{"key": "value"}'

    def test_preserves_raw_fields(self, trace_dir):
        save_raw_response(
            "country", "mx", date(2026, 3, 14),
            system_prompt="prompt",
            user_message="message",
            response_text="raw text",
            thinking_text="thinking",
            usage={"input_tokens": 100, "output_tokens": 50},
        )
        update_trace_parsed("country", "mx", date(2026, 3, 14), parsed_output={"parsed": True})
        trace = load_trace("country", "mx", date(2026, 3, 14))
        assert trace["input"]["system_prompt"] == "prompt"
        assert trace["input"]["user_message"] == "message"
        assert trace["output"]["response_text"] == "raw text"
        assert trace["output"]["thinking"] == "thinking"
        assert trace["usage"]["input_tokens"] == 100

    def test_adds_diagnostics(self, trace_dir):
        save_raw_response("executive", "global", date(2026, 3, 14), response_text="test")
        update_trace_parsed(
            "executive", "global", date(2026, 3, 14),
            parsed_output={},
            diagnostics={"fallbacks": 2, "skipped": 1},
        )
        trace = load_trace("executive", "global", date(2026, 3, 14))
        assert trace["diagnostics"]["fallbacks"] == 2

    def test_noop_if_raw_not_found(self, trace_dir):
        # Should not raise
        update_trace_parsed("nonexistent", "agent", date(2026, 3, 14), parsed_output={})


class TestLoadTrace:
    def test_loads_existing_trace(self, trace_dir):
        save_raw_response("triage", "decisions", date(2026, 3, 14), response_text="test")
        trace = load_trace("triage", "decisions", date(2026, 3, 14))
        assert trace is not None
        assert trace["agent"] == "triage"

    def test_returns_none_for_missing(self, trace_dir):
        assert load_trace("nonexistent", "agent", date(2026, 3, 14)) is None


class TestListTraces:
    def test_lists_all_traces_for_date(self, trace_dir):
        save_raw_response("executive", "global", date(2026, 3, 14), response_text="exec")
        save_raw_response("country", "mx", date(2026, 3, 14), response_text="mx")
        save_raw_response("country", "br", date(2026, 3, 14), response_text="br")

        traces = list_traces(date(2026, 3, 14))
        assert len(traces) == 3
        agents = {t["agent"] for t in traces}
        assert agents == {"executive", "country"}

    def test_empty_for_no_traces(self, trace_dir):
        traces = list_traces(date(2026, 3, 14))
        assert traces == []


class TestBackwardCompat:
    def test_save_trace_still_works(self, trace_dir):
        """Old save_trace function produces a valid trace file."""
        path = save_trace(
            "executive", "global", date(2026, 3, 14),
            system_prompt="prompt",
            user_message="message",
            response_text="response",
            parsed_output={"key": "value"},
        )
        trace = json.loads(path.read_text())
        assert trace["agent"] == "executive"
        assert trace["output"]["parsed"] == {"key": "value"}
        # Old traces don't have status field — that's fine
        assert "status" not in trace or trace.get("status") is not None

    def test_load_trace_reads_old_format(self, trace_dir):
        """load_trace can read traces written by old save_trace (no status field)."""
        save_trace(
            "regional", "americas", date(2026, 3, 14),
            response_text="old format",
            parsed_output={"old": True},
        )
        trace = load_trace("regional", "americas", date(2026, 3, 14))
        assert trace is not None
        assert trace["output"]["response_text"] == "old format"


class TestTwoPhaseFlow:
    def test_raw_survives_parse_crash(self, trace_dir):
        """Simulates the key scenario: raw saved, parse crashes, raw is recoverable."""
        save_raw_response(
            "executive", "global", date(2026, 3, 14),
            response_text='{"valid": "json but unparseable by agent"}',
            usage={"input_tokens": 5000, "output_tokens": 2000},
        )

        # Simulate parse crash — update_trace_parsed never called
        # The raw trace should still be on disk
        trace = load_trace("executive", "global", date(2026, 3, 14))
        assert trace["status"] == "raw"
        assert trace["output"]["response_text"] == '{"valid": "json but unparseable by agent"}'
        assert trace["output"]["parsed"] is None
        assert trace["usage"]["input_tokens"] == 5000

    def test_full_two_phase_flow(self, trace_dir):
        """Full happy path: save raw → parse succeeds → update parsed."""
        save_raw_response(
            "country", "mx", date(2026, 3, 14),
            response_text='{"weekly_entry": {}}',
        )

        # Parse succeeds
        parsed = {"weekly_entry": {"week": "2026-03-14"}}
        update_trace_parsed("country", "mx", date(2026, 3, 14), parsed_output=parsed)

        trace = load_trace("country", "mx", date(2026, 3, 14))
        assert trace["status"] == "parsed"
        assert trace["output"]["parsed"] == parsed
        assert trace["output"]["response_text"] == '{"weekly_entry": {}}'
