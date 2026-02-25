"""
Debug output module for pipeline troubleshooting.

Saves intermediate results as JSON files at each pipeline step.
Enable with --debug flag or DEBUG_OUTPUT=1 environment variable.
"""

import json
import logging
import os
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Global debug state
_debug_enabled = False
_debug_dir: Optional[Path] = None


def enable_debug(output_dir: Optional[Path] = None):
    """Enable debug output."""
    global _debug_enabled, _debug_dir
    _debug_enabled = True

    if output_dir:
        _debug_dir = output_dir
    else:
        # Default to briefs/YYYYMMDD/debug/
        _debug_dir = Path("briefs") / datetime.now().strftime("%Y%m%d") / "debug"

    _debug_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Debug output enabled: {_debug_dir}")


def is_debug_enabled() -> bool:
    """Check if debug output is enabled."""
    return _debug_enabled or os.environ.get("DEBUG_OUTPUT", "").lower() in ("1", "true", "yes")


def get_debug_dir() -> Optional[Path]:
    """Get the debug output directory."""
    global _debug_dir

    if not is_debug_enabled():
        return None

    if _debug_dir is None:
        _debug_dir = Path("briefs") / datetime.now().strftime("%Y%m%d") / "debug"
        _debug_dir.mkdir(parents=True, exist_ok=True)

    return _debug_dir


def _serialize(obj: Any) -> Any:
    """Serialize objects for JSON output."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, "value"):  # Enum
        return obj.value
    elif hasattr(obj, "__dict__"):
        return {k: _serialize(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple)):
        return [_serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def save_debug_output(
    step: str,
    data: Any,
    leader_name: Optional[str] = None,
    suffix: str = "",
) -> Optional[Path]:
    """
    Save debug output for a pipeline step.

    Args:
        step: Pipeline step name (e.g., "fetch", "translate", "classify")
        data: Data to save (will be serialized to JSON)
        leader_name: Optional leader name for per-leader outputs
        suffix: Optional suffix for the filename

    Returns:
        Path to saved file, or None if debug is disabled
    """
    if not is_debug_enabled():
        return None

    debug_dir = get_debug_dir()
    if debug_dir is None:
        return None

    # Build filename
    parts = [step]
    if leader_name:
        safe_name = leader_name.lower().replace(" ", "_")
        parts.append(safe_name)
    if suffix:
        parts.append(suffix)

    filename = "_".join(parts) + ".json"
    filepath = debug_dir / filename

    try:
        serialized = _serialize(data)

        with open(filepath, "w") as f:
            json.dump(serialized, f, indent=2, default=str)

        logger.debug(f"Debug output saved: {filepath}")
        return filepath

    except Exception as e:
        logger.warning(f"Failed to save debug output {filepath}: {e}")
        return None


def save_dossier_results(
    leader_name: str,
    dossier,
) -> Optional[Path]:
    """Save dossier for a leader."""
    data = {
        "leader": leader_name,
        "timestamp": datetime.now().isoformat(),
        "dossier": dossier,
    }

    return save_debug_output("05_dossier", data, leader_name)


def save_synthesis_results(
    step: str,
    content: Any,
) -> Optional[Path]:
    """Save synthesis step results."""
    data = {
        "step": step,
        "timestamp": datetime.now().isoformat(),
        "content": content,
    }

    return save_debug_output(f"07_synthesis_{step}", data)


def save_final_brief(brief) -> Optional[Path]:
    """Save the final brief."""
    return save_debug_output("08_final_brief", brief)


def create_pipeline_summary(
    leader_stats: dict,
    thread_stats: dict,
    timing: Optional[dict] = None,
) -> Optional[Path]:
    """Create a summary of the entire pipeline run."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "leader_stats": leader_stats,
        "thread_stats": thread_stats,
        "timing": timing or {},
    }

    return save_debug_output("00_pipeline_summary", data)
