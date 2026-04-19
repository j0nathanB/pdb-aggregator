"""
Trace persistence for LLM agent inputs and outputs.

Saves raw model I/O to briefs/{date}/traces/ so pipeline runs can be
inspected after the fact. Each agent call produces one JSON file.
"""

import dataclasses
import json
import logging
from datetime import date
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT

logger = logging.getLogger(__name__)

TRACES_DIR_NAME = "traces"


def _traces_dir(run_date: date, trace_root: Path | None = None) -> Path:
    """Return the traces directory for a given run date, creating it if needed.

    If trace_root is provided, traces are written under that directory instead
    of the production briefs/ tree. Used by evaluation harnesses to avoid
    clobbering production traces.
    """
    if trace_root is not None:
        d = trace_root / run_date.strftime("%Y%m%d") / TRACES_DIR_NAME
    else:
        d = PROJECT_ROOT / "briefs" / run_date.strftime("%Y%m%d") / TRACES_DIR_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_trace(
    agent: str,
    label: str,
    run_date: date,
    *,
    system_prompt: str = "",
    user_message: str = "",
    response_text: str = "",
    parsed_output: Any = None,
    thinking_text: str = "",
    usage: dict | None = None,
    extra: dict | None = None,
) -> Path:
    """Save a trace file for one agent invocation.

    Args:
        agent: Agent name (e.g. "regional", "executive", "country").
        label: Instance label (e.g. "central_eastern_europe", "mx").
        run_date: Pipeline run date.
        system_prompt: The system prompt sent to the model.
        user_message: The user message sent to the model.
        response_text: Raw text response from the model.
        parsed_output: Parsed/structured output (must be JSON-serializable).
        thinking_text: Extended thinking content, if captured.
        usage: Token usage dict (input_tokens, output_tokens).
        extra: Any additional metadata to include.

    Returns:
        Path to the saved trace file.
    """
    trace = {
        "agent": agent,
        "label": label,
        "run_date": run_date.isoformat(),
        "input": {
            "system_prompt": system_prompt,
            "user_message": user_message,
        },
        "output": {
            "response_text": response_text,
            "parsed": parsed_output,
            "thinking": thinking_text,
        },
        "usage": usage or {},
    }
    if extra:
        trace["extra"] = extra

    path = _trace_path(agent, label, run_date)

    try:
        path.write_text(json.dumps(trace, indent=2, ensure_ascii=False, default=_default_serializer))
        logger.debug("Trace saved: %s", path)
    except Exception as e:
        logger.warning("Failed to save trace %s: %s", path, e)

    return path


def _trace_path(agent: str, label: str, run_date: date, trace_root: Path | None = None) -> Path:
    """Return the path for a trace file (does not create it)."""
    safe_label = label.replace(" ", "_").replace("/", "_").lower()
    filename = f"{agent}_{safe_label}.json"
    return _traces_dir(run_date, trace_root) / filename


def _default_serializer(obj):
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    return str(obj)


def save_raw_response(
    agent: str,
    label: str,
    run_date: date,
    *,
    system_prompt: str = "",
    user_message: str = "",
    response_text: str = "",
    thinking_text: str = "",
    usage: dict | None = None,
    extra: dict | None = None,
    trace_root: Path | None = None,
) -> Path:
    """Save raw API response IMMEDIATELY after the call, BEFORE parsing.

    This must be called before any parsing. If parsing crashes,
    this file is the recovery point — the raw response_text is on disk.
    """
    trace = {
        "agent": agent,
        "label": label,
        "run_date": run_date.isoformat(),
        "status": "raw",
        "input": {
            "system_prompt": system_prompt,
            "user_message": user_message,
        },
        "output": {
            "response_text": response_text,
            "parsed": None,
            "thinking": thinking_text,
        },
        "usage": usage or {},
    }
    if extra:
        trace["extra"] = extra

    path = _trace_path(agent, label, run_date, trace_root)
    try:
        path.write_text(json.dumps(trace, indent=2, ensure_ascii=False, default=_default_serializer))
        logger.debug("Raw trace saved: %s", path)
    except Exception as e:
        logger.warning("Failed to save raw trace %s: %s", path, e)

    return path


def update_trace_parsed(
    agent: str,
    label: str,
    run_date: date,
    parsed_output: Any,
    diagnostics: dict | None = None,
    trace_root: Path | None = None,
) -> Path:
    """Update an existing trace with parsed output after successful parsing.

    If this is never called (because parsing crashed), the trace file
    still exists with status="raw" and the full response_text.
    """
    path = _trace_path(agent, label, run_date, trace_root)
    try:
        trace = json.loads(path.read_text())
        trace["status"] = "parsed"
        trace["output"]["parsed"] = parsed_output
        if diagnostics:
            trace["diagnostics"] = diagnostics
        path.write_text(json.dumps(trace, indent=2, ensure_ascii=False, default=_default_serializer))
        logger.debug("Trace updated with parsed output: %s", path)
    except FileNotFoundError:
        logger.warning("Cannot update trace — raw trace not found: %s", path)
    except Exception as e:
        logger.warning("Failed to update trace %s: %s", path, e)

    return path


def load_trace(agent: str, label: str, run_date: date) -> dict | None:
    """Load a trace file from disk. Returns None if not found."""
    path = _trace_path(agent, label, run_date)
    if not path.exists():
        return None
    return json.loads(path.read_text())


def list_traces(run_date: date) -> list[dict]:
    """List all traces for a given run date."""
    traces_dir = _traces_dir(run_date)
    results = []
    for path in sorted(traces_dir.glob("*.json")):
        try:
            results.append(json.loads(path.read_text()))
        except (json.JSONDecodeError, OSError):
            logger.warning("Skipping unreadable trace: %s", path)
    return results


def extract_thinking(response) -> str:
    """Extract thinking text from an Anthropic response object."""
    parts = []
    for block in response.content:
        if block.type == "thinking":
            parts.append(block.thinking)
    return "\n".join(parts)


def extract_usage(response) -> dict:
    """Extract token usage from an Anthropic response object."""
    u = response.usage
    return {
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
    }
