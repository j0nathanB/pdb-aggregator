"""
Shared LLM output sanitization utilities.

Every agent parser should route enum parsing, date parsing, and JSON
extraction through these helpers so that invalid LLM output degrades
gracefully instead of crashing the pipeline.
"""

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import TypeVar

logger = logging.getLogger(__name__)

E = TypeVar("E", bound=Enum)

# Module-level fallback counters — track how many fallbacks fired per context
_fallback_counts: dict[str, int] = {}


def get_fallback_summary() -> dict[str, int]:
    """Return fallback counts per context since last reset."""
    return dict(_fallback_counts)


def reset_fallback_counts() -> None:
    """Reset all fallback counters (call at start of pipeline run)."""
    _fallback_counts.clear()


def _record_fallback(context: str) -> None:
    """Increment the fallback counter for a context."""
    key = context or "unknown"
    _fallback_counts[key] = _fallback_counts.get(key, 0) + 1


# =============================================================================
# Safe parsers
# =============================================================================

def safe_enum(enum_class: type[E], value: str, default: E, context: str = "") -> E:
    """Parse an enum value, returning the default if invalid.

    >>> safe_enum(Movement, "bogus", Movement.NONE, context="country_mx")
    <Movement.NONE: 'none'>
    """
    try:
        return enum_class(value)
    except (ValueError, KeyError):
        ctx = f" [{context}]" if context else ""
        logger.warning(
            "Invalid %s value %r, using default %r%s",
            enum_class.__name__, value, default.value, ctx,
        )
        _record_fallback(context)
        return default


def safe_enum_list(
    enum_class: type[E], values: list, context: str = "",
) -> list[E]:
    """Parse a list of enum values, skipping invalid ones.

    >>> safe_enum_list(SignalCategory, ["alignment_diplomatic", "bogus"])
    [<SignalCategory.ALIGNMENT_DIPLOMATIC: 'alignment_diplomatic'>]
    """
    result = []
    for v in values:
        try:
            result.append(enum_class(v))
        except (ValueError, KeyError):
            ctx = f" [{context}]" if context else ""
            logger.warning(
                "Skipping invalid %s value %r%s",
                enum_class.__name__, v, ctx,
            )
            _record_fallback(context)
    return result


def safe_date(value, fallback: date, context: str = "") -> date:
    """Parse an ISO date string, returning the fallback if invalid.

    Handles None, non-string values, and malformed strings.
    """
    if isinstance(value, date) and not isinstance(value, type(None)):
        return value
    if not isinstance(value, str):
        return fallback
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        ctx = f" [{context}]" if context else ""
        logger.warning("Invalid date %r, using fallback %s%s", value, fallback, ctx)
        return fallback


def safe_int(
    value, default: int, min_val: int | None = None, max_val: int | None = None,
    context: str = "",
) -> int:
    """Parse an int, clamping to [min_val, max_val] and falling back to default."""
    try:
        result = int(value)
    except (ValueError, TypeError):
        ctx = f" [{context}]" if context else ""
        logger.warning("Invalid int %r, using default %d%s", value, default, ctx)
        return default
    if min_val is not None and result < min_val:
        result = min_val
    if max_val is not None and result > max_val:
        result = max_val
    return result


# =============================================================================
# JSON extraction
# =============================================================================

def extract_json(text: str, context: str = "") -> dict:
    """Extract a JSON object from LLM response text.

    Handles:
    - ```json fences
    - Prose before/after JSON
    - Nested objects with escaped braces in strings
    - Common LLM mistakes (missing commas, trailing commas, single quotes,
      unescaped newlines) via json-repair fallback

    Uses json.JSONDecoder().raw_decode() for correct string-escape handling
    instead of hand-rolled brace counting. Falls back to json-repair as a
    last resort — when this fires, we log a warning because repaired JSON
    can be structurally incorrect (the library guesses structure without
    knowing the schema).
    """
    cleaned = text.strip()

    # Strip markdown fences
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    # Try direct parse first (strict=False tolerates literal newlines in strings,
    # which LLMs frequently produce)
    try:
        return json.loads(cleaned, strict=False)
    except json.JSONDecodeError:
        pass

    # Find the first { and use raw_decode from there
    idx = cleaned.find("{")
    if idx == -1:
        ctx = f" [{context}]" if context else ""
        raise ValueError(f"No JSON object found in LLM response{ctx}")

    decoder = json.JSONDecoder(strict=False)
    try:
        obj, _ = decoder.raw_decode(cleaned, idx)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # Last resort: json-repair. Warn loudly because repaired JSON may be
    # structurally wrong — the library guesses structure without schema
    # knowledge, and downstream parsers may silently get malformed data.
    try:
        from json_repair import repair_json
        repaired = repair_json(cleaned, return_objects=True)
        if isinstance(repaired, dict) and repaired:
            ctx = f" [{context}]" if context else ""
            logger.warning(
                "JSON repair fallback used%s — original JSON was malformed. "
                "Repaired output may be structurally incorrect; verify downstream parsing.",
                ctx,
            )
            _record_fallback("json_repair_used")
            return repaired
    except ImportError:
        logger.debug("json-repair not installed; skipping repair fallback")
    except Exception as e:
        logger.debug("json-repair failed: %s", e)

    ctx = f" [{context}]" if context else ""
    raise ValueError(f"Could not parse JSON from LLM response{ctx}")


# =============================================================================
# Parse diagnostics
# =============================================================================

@dataclass
class FallbackRecord:
    field: str
    raw_value: str
    resolved_to: str
    context: str = ""


@dataclass
class SkipRecord:
    item_type: str
    reason: str
    context: str = ""


@dataclass
class ParseDiagnostics:
    """Accumulates coercions and skips during a single parse operation."""

    fallbacks: list[FallbackRecord] = field(default_factory=list)
    skipped: list[SkipRecord] = field(default_factory=list)

    def record_fallback(
        self, field_name: str, raw_value: str, resolved_to: str, context: str = "",
    ) -> None:
        self.fallbacks.append(FallbackRecord(field_name, raw_value, resolved_to, context))

    def record_skip(self, item_type: str, reason: str, context: str = "") -> None:
        self.skipped.append(SkipRecord(item_type, reason, context))

    @property
    def fallback_count(self) -> int:
        return len(self.fallbacks)

    @property
    def skip_count(self) -> int:
        return len(self.skipped)

    def escalate_if_needed(self, threshold: int = 5) -> None:
        """Raise if too many fallbacks fired, indicating severe parse degradation."""
        if self.fallback_count >= threshold:
            raise ValueError(
                f"Parse quality too low: {self.fallback_count} fallbacks, "
                f"{self.skip_count} skipped items"
            )
