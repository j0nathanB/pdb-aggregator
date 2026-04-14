"""Tests for the shared LLM output sanitization module."""

from datetime import date

import pytest

from src.monitor.config import (
    CategoryStatus,
    ClaimStatus,
    Depth,
    DynamicStatus,
    LinkageType,
    Movement,
    SignalCategory,
)
from src.monitor.sanitize import (
    extract_json,
    get_fallback_summary,
    reset_fallback_counts,
    safe_date,
    safe_enum,
    safe_enum_list,
    safe_int,
)


# =============================================================================
# safe_enum
# =============================================================================

ALL_ENUMS = [
    (SignalCategory, "alignment_diplomatic", SignalCategory.ALIGNMENT_DIPLOMATIC),
    (Movement, "significant", Movement.SIGNIFICANT),
    (Depth, "deep_dive", Depth.DEEP_DIVE),
    (DynamicStatus, "emerging", DynamicStatus.EMERGING),
    (LinkageType, "parallel_behavior", LinkageType.PARALLEL_BEHAVIOR),
    (ClaimStatus, "confirmed", ClaimStatus.CONFIRMED),
    (CategoryStatus, "active", CategoryStatus.ACTIVE),
]


@pytest.mark.parametrize("enum_class,valid_value,expected", ALL_ENUMS)
def test_safe_enum_valid(enum_class, valid_value, expected):
    result = safe_enum(enum_class, valid_value, list(enum_class)[0])
    assert result == expected


@pytest.mark.parametrize("enum_class", [e[0] for e in ALL_ENUMS])
def test_safe_enum_invalid_returns_default(enum_class):
    default = list(enum_class)[0]
    result = safe_enum(enum_class, "totally_bogus_value", default, context="test")
    assert result == default


def test_safe_enum_empty_string():
    result = safe_enum(Movement, "", Movement.NONE)
    assert result == Movement.NONE


# =============================================================================
# safe_enum_list
# =============================================================================

def test_safe_enum_list_mixed():
    values = ["alignment_diplomatic", "bogus", "security_defense", "also_bogus"]
    result = safe_enum_list(SignalCategory, values, context="test")
    assert result == [SignalCategory.ALIGNMENT_DIPLOMATIC, SignalCategory.SECURITY_DEFENSE]


def test_safe_enum_list_empty():
    assert safe_enum_list(SignalCategory, []) == []


def test_safe_enum_list_all_invalid():
    result = safe_enum_list(Movement, ["x", "y", "z"])
    assert result == []


# =============================================================================
# safe_date
# =============================================================================

def test_safe_date_valid_string():
    assert safe_date("2026-03-14", date(2000, 1, 1)) == date(2026, 3, 14)


def test_safe_date_invalid_string():
    assert safe_date("not-a-date", date(2026, 1, 1)) == date(2026, 1, 1)


def test_safe_date_none():
    assert safe_date(None, date(2026, 1, 1)) == date(2026, 1, 1)


def test_safe_date_date_object():
    d = date(2026, 5, 1)
    assert safe_date(d, date(2000, 1, 1)) == d


def test_safe_date_int():
    assert safe_date(20260314, date(2026, 1, 1)) == date(2026, 1, 1)


# =============================================================================
# safe_int
# =============================================================================

def test_safe_int_valid():
    assert safe_int("42", 0) == 42


def test_safe_int_invalid():
    assert safe_int("abc", 5) == 5


def test_safe_int_none():
    assert safe_int(None, 3) == 3


def test_safe_int_clamped():
    assert safe_int(100, 3, min_val=1, max_val=5) == 5
    assert safe_int(-1, 3, min_val=1, max_val=5) == 1


# =============================================================================
# extract_json
# =============================================================================

def test_extract_json_bare():
    assert extract_json('{"key": "value"}') == {"key": "value"}


def test_extract_json_fenced():
    text = '```json\n{"key": "value"}\n```'
    assert extract_json(text) == {"key": "value"}


def test_extract_json_fenced_no_lang():
    text = '```\n{"key": "value"}\n```'
    assert extract_json(text) == {"key": "value"}


def test_extract_json_with_prose():
    text = 'Here is my analysis:\n\n{"key": "value"}\n\nI hope this helps.'
    assert extract_json(text) == {"key": "value"}


def test_extract_json_nested():
    text = '{"outer": {"inner": [1, 2, 3]}}'
    result = extract_json(text)
    assert result["outer"]["inner"] == [1, 2, 3]


def test_extract_json_escaped_braces_in_strings():
    text = '{"text": "Use {curly} braces like \\"{this}\\"", "count": 1}'
    result = extract_json(text)
    assert result["count"] == 1


def test_extract_json_no_json():
    with pytest.raises(ValueError, match="No JSON object found"):
        extract_json("This is just plain text with no JSON.")


def test_extract_json_empty():
    with pytest.raises(ValueError):
        extract_json("")


def test_extract_json_with_context():
    with pytest.raises(ValueError, match="executive"):
        extract_json("no json here", context="executive")



# =============================================================================
# Module-level fallback counters
# =============================================================================

def test_fallback_counters_track_safe_enum():
    reset_fallback_counts()
    safe_enum(Movement, "bogus", Movement.NONE, context="test_counter")
    safe_enum(Movement, "also_bogus", Movement.NONE, context="test_counter")
    safe_enum(Movement, "bad", Movement.NONE, context="other_context")
    summary = get_fallback_summary()
    assert summary["test_counter"] == 2
    assert summary["other_context"] == 1


def test_fallback_counters_track_safe_enum_list():
    reset_fallback_counts()
    safe_enum_list(SignalCategory, ["alignment_diplomatic", "bogus", "also_bad"], context="list_ctx")
    summary = get_fallback_summary()
    assert summary["list_ctx"] == 2


def test_fallback_counters_reset():
    reset_fallback_counts()
    safe_enum(Movement, "bogus", Movement.NONE, context="ctx")
    assert get_fallback_summary()["ctx"] == 1
    reset_fallback_counts()
    assert get_fallback_summary() == {}


def test_no_fallback_on_valid_enum():
    reset_fallback_counts()
    safe_enum(Movement, "significant", Movement.NONE, context="valid_ctx")
    assert "valid_ctx" not in get_fallback_summary()
