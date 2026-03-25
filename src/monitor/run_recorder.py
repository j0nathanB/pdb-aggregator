"""
Run recorder: writes each pipeline step's output to a timestamped folder.

Each run creates a folder like updated_architecture/20260323_213032/
containing numbered JSON files for every pipeline step, plus the log file.
"""

import json
import logging
import shutil
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT

logger = logging.getLogger(__name__)

RUNS_DIR = PROJECT_ROOT / "updated_architecture"


def _serialize(obj: Any) -> Any:
    """Convert pipeline objects to JSON-serializable dicts."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {str(k): _serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(v) for v in obj]
    if isinstance(obj, set):
        return [_serialize(v) for v in sorted(obj, key=str)]
    # Pydantic models
    if hasattr(obj, "model_dump"):
        return _serialize(obj.model_dump())
    # Dataclasses
    if is_dataclass(obj) and not isinstance(obj, type):
        return _serialize(asdict(obj))
    # Objects with to_dict
    if hasattr(obj, "to_dict"):
        return _serialize(obj.to_dict())
    # Objects with __dict__
    if hasattr(obj, "__dict__"):
        return _serialize(obj.__dict__)
    # Fallback
    return str(obj)


class RunRecorder:
    """Records pipeline step outputs to a timestamped run folder."""

    def __init__(self, run_dir: Path | None = None):
        if run_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.run_dir = RUNS_DIR / timestamp
        else:
            self.run_dir = run_dir
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self._step_counter: dict[str, int] = {}
        logger.info("Run recorder: %s", self.run_dir)

    @property
    def log_path(self) -> str:
        """Path for the pipeline log file inside this run folder."""
        return str(self.run_dir / "pipeline.log")

    def write(self, step: str, data: Any, suffix: str = "") -> Path:
        """Write a step output as JSON.

        Args:
            step: Step identifier like "01_layer2" or "05_story_map".
            data: Any serializable data (dataclasses, pydantic models, dicts).
            suffix: Optional suffix like "_mx" for per-country files.

        Returns:
            Path to the written file.
        """
        filename = f"{step}{suffix}.json"
        path = self.run_dir / filename
        path.write_text(
            json.dumps(_serialize(data), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.debug("Run recorder: wrote %s", filename)
        return path

    def write_summary(self, data: Any) -> Path:
        """Write the final pipeline summary."""
        return self.write("99_pipeline_summary", data)
