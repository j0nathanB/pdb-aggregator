"""
Run recorder: writes each pipeline step's output to a timestamped folder.

Each run creates a folder like updated_architecture/20260323_213032/
containing numbered JSON files for every pipeline step, plus the log file
and a manifest tracking stage status for resumability.
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

STAGE_ORDER = ["desk", "regional", "executive", "newsletter", "publishing"]


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
        self._manifest: dict | None = None
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

    # =========================================================================
    # Manifest — stage status tracking for resumability
    # =========================================================================

    def init_manifest(self, end_date: date, country_codes: list[str] | None) -> Path:
        """Create manifest.json with all stages pending."""
        self._manifest = {
            "run_id": self.run_dir.name,
            "started_at": datetime.now().isoformat(),
            "end_date": end_date.isoformat(),
            "country_codes": country_codes,
            "stages": {s: {"status": "pending"} for s in STAGE_ORDER},
        }
        return self._write_manifest()

    def start_stage(self, stage: str) -> None:
        """Mark a stage as running."""
        if self._manifest is None:
            return
        self._manifest["stages"][stage] = {
            "status": "running",
            "started_at": datetime.now().isoformat(),
        }
        self._write_manifest()

    def complete_stage(self, stage: str) -> None:
        """Mark a stage as completed."""
        if self._manifest is None:
            return
        entry = self._manifest["stages"][stage]
        entry["status"] = "completed"
        entry["completed_at"] = datetime.now().isoformat()
        self._write_manifest()

    def fail_stage(self, stage: str, error: str) -> None:
        """Mark a stage as failed with an error message."""
        if self._manifest is None:
            return
        entry = self._manifest["stages"][stage]
        entry["status"] = "failed"
        entry["error"] = error
        entry["failed_at"] = datetime.now().isoformat()
        self._write_manifest()

    def skip_stage(self, stage: str) -> None:
        """Mark a stage as skipped (for --resume-from)."""
        if self._manifest is None:
            return
        self._manifest["stages"][stage] = {"status": "skipped"}
        self._write_manifest()

    def _write_manifest(self) -> Path:
        """Atomic write of manifest.json (tmp + rename)."""
        path = self.run_dir / "manifest.json"
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._manifest, indent=2, ensure_ascii=False))
        tmp.rename(path)
        return path

    @classmethod
    def find_latest_manifest(cls) -> tuple["RunRecorder", dict] | None:
        """Find the most recent run directory containing a manifest.

        Returns (recorder, manifest_dict) or None if no manifests exist.
        """
        if not RUNS_DIR.exists():
            return None
        for run_dir in sorted(RUNS_DIR.iterdir(), reverse=True):
            if not run_dir.is_dir():
                continue
            manifest_path = run_dir / "manifest.json"
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text())
                recorder = cls(run_dir=run_dir)
                recorder._manifest = manifest
                return recorder, manifest
        return None

    # =========================================================================
    # Usage tracking — aggregate token costs per stage
    # =========================================================================

    def record_usage(self, stage: str, input_tokens: int, output_tokens: int) -> None:
        """Record token usage for a stage."""
        if self._manifest is None:
            return
        if "usage" not in self._manifest:
            self._manifest["usage"] = {
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "by_stage": {},
            }
        usage = self._manifest["usage"]
        usage["total_input_tokens"] += input_tokens
        usage["total_output_tokens"] += output_tokens
        if stage not in usage["by_stage"]:
            usage["by_stage"][stage] = {"input_tokens": 0, "output_tokens": 0}
        usage["by_stage"][stage]["input_tokens"] += input_tokens
        usage["by_stage"][stage]["output_tokens"] += output_tokens

        # Estimate cost from settings
        from .config import load_settings
        settings = load_settings()
        input_cost = settings.get("input_cost_per_mtok", 3.0)
        output_cost = settings.get("output_cost_per_mtok", 15.0)
        usage["estimated_cost_usd"] = round(
            usage["total_input_tokens"] / 1_000_000 * input_cost
            + usage["total_output_tokens"] / 1_000_000 * output_cost,
            2,
        )
        self._write_manifest()

    def aggregate_usage_from_traces(self, stage: str, run_date: date) -> None:
        """Scan trace files and aggregate usage into the manifest."""
        from .trace import list_traces
        traces = list_traces(run_date)
        total_in = 0
        total_out = 0
        for trace in traces:
            usage = trace.get("usage", {})
            total_in += usage.get("input_tokens", 0)
            total_out += usage.get("output_tokens", 0)
        if total_in or total_out:
            self.record_usage(stage, total_in, total_out)

    # =========================================================================
    # Prompt hashing — detect changes between runs
    # =========================================================================

    def record_prompt_hashes(self) -> dict[str, str]:
        """Hash all prompt files and store in manifest."""
        import hashlib
        from .config import PROMPTS_DIR

        hashes = {}
        if PROMPTS_DIR.exists():
            for p in sorted(PROMPTS_DIR.glob("*.md")):
                hashes[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()[:12]

        if self._manifest is not None:
            self._manifest["prompt_hashes"] = hashes
            self._write_manifest()

        return hashes

    @staticmethod
    def check_prompt_changes(current_hashes: dict[str, str], prior_manifest: dict) -> list[str]:
        """Compare current prompt hashes against a prior manifest. Returns list of changed prompts."""
        prior_hashes = prior_manifest.get("prompt_hashes", {})
        changed = []
        for name, current_hash in current_hashes.items():
            prior_hash = prior_hashes.get(name)
            if prior_hash and prior_hash != current_hash:
                changed.append(name)
        # Also check for new prompts
        for name in current_hashes:
            if name not in prior_hashes:
                changed.append(f"{name} (new)")
        return changed

    # =========================================================================
    # Ledger snapshots — pre-run backup for rollback
    # =========================================================================

    def snapshot_ledgers(self) -> Path:
        """Copy all ledger files into the run dir for rollback.

        Snapshots: country ledgers, global ledger, regional reports.
        """
        from .config import COUNTRY_LEDGERS_DIR, GLOBAL_LEDGER_PATH, REGIONAL_REPORTS_DIR

        snap_dir = self.run_dir / "snapshots"
        snap_dir.mkdir(exist_ok=True)

        if COUNTRY_LEDGERS_DIR.exists():
            shutil.copytree(
                COUNTRY_LEDGERS_DIR, snap_dir / "countries", dirs_exist_ok=True,
            )
        if GLOBAL_LEDGER_PATH.exists():
            shutil.copy2(GLOBAL_LEDGER_PATH, snap_dir / "global.json")
        if REGIONAL_REPORTS_DIR.exists():
            shutil.copytree(
                REGIONAL_REPORTS_DIR, snap_dir / "regional", dirs_exist_ok=True,
            )

        logger.info("Ledger snapshots saved to %s", snap_dir)
        return snap_dir
