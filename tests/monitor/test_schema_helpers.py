"""Tests for pydantic_to_tool_schema."""

import json
from enum import Enum
from typing import Optional

import pytest
from pydantic import BaseModel, Field

from src.monitor.schema_helpers import pydantic_to_tool_schema


class Color(str, Enum):
    RED = "red"
    BLUE = "blue"


class Leaf(BaseModel):
    name: str
    count: int = 0


class Branch(BaseModel):
    label: str
    color: Color
    leaves: list[Leaf] = Field(default_factory=list)
    primary: Leaf | None = None


class TestPydanticToToolSchema:
    def test_returns_plain_type_object(self):
        s = pydantic_to_tool_schema(Leaf)
        assert s["type"] == "object"
        assert set(s["properties"]) == {"name", "count"}
        assert s["required"] == ["name"]

    def test_no_refs_or_defs_remain(self):
        s = pydantic_to_tool_schema(Branch)
        j = json.dumps(s)
        assert "$ref" not in j
        assert "$defs" not in j

    def test_enum_inlined_as_enum_field(self):
        s = pydantic_to_tool_schema(Branch)
        color_schema = s["properties"]["color"]
        assert color_schema["type"] == "string"
        assert set(color_schema["enum"]) == {"red", "blue"}

    def test_nested_model_inlined(self):
        s = pydantic_to_tool_schema(Branch)
        leaves_schema = s["properties"]["leaves"]
        assert leaves_schema["type"] == "array"
        # Items should be the Leaf schema inline
        assert leaves_schema["items"]["type"] == "object"
        assert "name" in leaves_schema["items"]["properties"]

    def test_titles_stripped(self):
        s = pydantic_to_tool_schema(Branch)
        assert "title" not in s
        # Check nested levels too
        j = json.dumps(s)
        assert '"title":' not in j

    def test_real_models_produce_clean_schema(self):
        """Integration: the three models we actually use must round-trip."""
        from src.monitor.models import (
            WeeklyEntry, SignalCategoryAssessment, PostureSummary,
        )
        for cls in [WeeklyEntry, SignalCategoryAssessment, PostureSummary]:
            s = pydantic_to_tool_schema(cls)
            j = json.dumps(s)
            assert "$ref" not in j, f"{cls.__name__} still has $ref"
            assert "$defs" not in j, f"{cls.__name__} still has $defs"

    def test_cyclic_ref_raises(self):
        """If a model references itself (not a real case for us, but good
        to enforce), the helper should raise rather than recursing forever."""
        # Craft a synthetic cyclic schema by hand
        schema = {
            "type": "object",
            "properties": {"next": {"$ref": "#/$defs/Node"}},
            "$defs": {
                "Node": {
                    "type": "object",
                    "properties": {"next": {"$ref": "#/$defs/Node"}},
                },
            },
        }

        class FakeModel:
            @classmethod
            def model_json_schema(cls):
                return dict(schema)  # return a copy

        with pytest.raises(ValueError, match="cyclic"):
            pydantic_to_tool_schema(FakeModel)  # type: ignore[arg-type]

    def test_unresolvable_ref_raises(self):
        class FakeModel:
            @classmethod
            def model_json_schema(cls):
                return {
                    "type": "object",
                    "properties": {"x": {"$ref": "#/$defs/NotThere"}},
                    "$defs": {},
                }

        with pytest.raises(ValueError, match="Unresolved"):
            pydantic_to_tool_schema(FakeModel)  # type: ignore[arg-type]

    def test_unsupported_ref_format_raises(self):
        class FakeModel:
            @classmethod
            def model_json_schema(cls):
                return {
                    "type": "object",
                    "properties": {"x": {"$ref": "https://external/schema"}},
                    "$defs": {},
                }

        with pytest.raises(ValueError, match="Unsupported"):
            pydantic_to_tool_schema(FakeModel)  # type: ignore[arg-type]
