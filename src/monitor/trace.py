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


def _traces_dir(run_date: date) -> Path:
    """Return the traces directory for a given run date, creating it if needed."""
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
        label: Instance label (e.g. "frontline_eastern_europe", "mx").
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

    # Filename: {agent}_{label}.json
    safe_label = label.replace(" ", "_").replace("/", "_").lower()
    filename = f"{agent}_{safe_label}.json"
    path = _traces_dir(run_date) / filename

    def _default(obj):
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        return str(obj)

    try:
        path.write_text(json.dumps(trace, indent=2, ensure_ascii=False, default=_default))
        logger.debug("Trace saved: %s", path)
    except Exception as e:
        logger.warning("Failed to save trace %s: %s", path, e)

    return path


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
