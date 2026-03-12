"""
Tests for Phase 0 — Global Context Brief module.

Verifies prompt construction and function signature without making LLM calls.
"""

import asyncio
import inspect

from src.phases.phase0 import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    format_user_prompt,
    run_phase_0,
)


class TestPromptContent:
    """Verify that system and user prompts contain the required content."""

    def test_system_prompt_contains_role(self):
        assert "Global Context Brief" in SYSTEM_PROMPT

    def test_system_prompt_contains_instructions(self):
        assert "What happened" in SYSTEM_PROMPT
        assert "Why it matters" in SYSTEM_PROMPT
        assert "What decisions or responses" in SYSTEM_PROMPT

    def test_system_prompt_forbids_individual_assessment(self):
        assert "Do NOT assess individual leaders" in SYSTEM_PROMPT

    def test_system_prompt_specifies_target_length(self):
        assert "500-800 words" in SYSTEM_PROMPT

    def test_user_prompt_template_has_placeholder(self):
        assert "{triggered_clusters}" in USER_PROMPT_TEMPLATE

    def test_user_prompt_template_has_header(self):
        assert "CROSS-CUTTING EVENTS THIS WEEK" in USER_PROMPT_TEMPLATE


class TestFormatUserPrompt:
    """Verify the user prompt helper formats correctly."""

    def test_substitutes_cluster_text(self):
        clusters = "Cluster A: US tariffs on steel affecting EU, Canada, Mexico"
        result = format_user_prompt(clusters)
        assert clusters in result
        assert "CROSS-CUTTING EVENTS THIS WEEK" in result
        assert "Produce the Global Context Brief" in result

    def test_empty_clusters(self):
        result = format_user_prompt("")
        # Should still produce a valid prompt, just with empty cluster section
        assert "CROSS-CUTTING EVENTS THIS WEEK" in result

    def test_multiline_clusters(self):
        clusters = "Cluster 1: NATO summit\nCluster 2: Oil price shock"
        result = format_user_prompt(clusters)
        assert "NATO summit" in result
        assert "Oil price shock" in result


class TestRunPhase0Signature:
    """Verify the function has the expected signature and properties."""

    def test_is_coroutine_function(self):
        # with_retry wraps it, but the wrapper should still be a coroutine
        assert asyncio.iscoroutinefunction(run_phase_0)

    def test_has_docstring(self):
        assert run_phase_0.__doc__ is not None
        assert "Global Context Brief" in run_phase_0.__doc__

    def test_accepts_triggered_clusters_param(self):
        sig = inspect.signature(run_phase_0)
        assert "triggered_clusters" in sig.parameters
        param = sig.parameters["triggered_clusters"]
        assert param.annotation == str
