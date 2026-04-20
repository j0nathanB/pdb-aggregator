"""
JSON-schema helpers for Anthropic tool-use definitions.

Pydantic v2 emits JSON schemas with `$defs` and `$ref` for nested models.
Anthropic's tool_use `input_schema` accepts those, but inlined schemas are
easier for the model to reason about and avoid any reference-resolution
edge cases. This module provides a small helper that:

- Generates a schema from a Pydantic model.
- Recursively resolves all `$ref` entries against `$defs`, replacing them
  with the inlined schema.
- Strips Pydantic-internal cosmetic fields (`title`) that Anthropic doesn't
  use.

Kept intentionally small. Tested in `tests/monitor/test_schema_helpers.py`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def pydantic_to_tool_schema(model_cls: type[BaseModel]) -> dict[str, Any]:
    """Produce an Anthropic-compatible `input_schema` from a Pydantic model.

    All `$ref` entries are resolved against the model's `$defs` and inlined
    recursively. `title` fields are dropped.
    """
    raw = model_cls.model_json_schema()
    defs = raw.pop("$defs", {})
    return _inline(raw, defs, active=())


def _inline(node: Any, defs: dict[str, Any], active: tuple[str, ...]) -> Any:
    """Walk a schema node, replacing `$ref` with the inlined def.

    `active` tracks the chain of $def names currently being resolved —
    if we encounter a $ref to one already in-flight, we have a cycle.
    """
    if isinstance(node, dict):
        if "$ref" in node:
            ref = node["$ref"]
            if not ref.startswith("#/$defs/"):
                raise ValueError(f"Unsupported $ref: {ref}")
            name = ref.removeprefix("#/$defs/")
            if name in active:
                raise ValueError(
                    f"Schema has cyclic $ref through {' → '.join((*active, name))}"
                )
            target = defs.get(name)
            if target is None:
                raise ValueError(f"Unresolved $ref: {ref}")
            return _inline(target, defs, active + (name,))
        return {
            k: _inline(v, defs, active)
            for k, v in node.items()
            if k != "title"
        }
    if isinstance(node, list):
        return [_inline(v, defs, active) for v in node]
    return node
