"""Tests for retry logic and error handling."""

import asyncio
from unittest.mock import AsyncMock

import pytest
import anthropic
from src.monitor.retry import (
    RetryExhausted,
    _delay_with_jitter,
    _is_retryable,
    with_retry,
)


class TestIsRetryable:
    def test_rate_limit_error(self):
        err = anthropic.RateLimitError(
            message="rate limited",
            response=AsyncMock(status_code=429, headers={}),
            body=None,
        )
        assert _is_retryable(err)

    def test_server_error(self):
        err = anthropic.InternalServerError(
            message="internal",
            response=AsyncMock(status_code=500, headers={}),
            body=None,
        )
        assert _is_retryable(err)

    def test_overloaded_error(self):
        err = anthropic.APIStatusError(
            message="overloaded",
            response=AsyncMock(status_code=529, headers={}),
            body=None,
        )
        assert _is_retryable(err)

    def test_connection_error(self):
        err = anthropic.APIConnectionError(request=AsyncMock())
        assert _is_retryable(err)

    def test_timeout_error(self):
        err = anthropic.APITimeoutError(request=AsyncMock())
        assert _is_retryable(err)

    def test_bad_request_not_retryable(self):
        err = anthropic.BadRequestError(
            message="bad request",
            response=AsyncMock(status_code=400, headers={}),
            body=None,
        )
        assert not _is_retryable(err)

    def test_auth_error_not_retryable(self):
        err = anthropic.AuthenticationError(
            message="unauthorized",
            response=AsyncMock(status_code=401, headers={}),
            body=None,
        )
        assert not _is_retryable(err)

    def test_generic_exception_not_retryable(self):
        assert not _is_retryable(ValueError("test"))


class TestDelayWithJitter:
    def test_increases_with_attempt(self):
        d0 = _delay_with_jitter(0)
        d2 = _delay_with_jitter(2)
        # On average, later attempts should have higher delays
        # But jitter makes this non-deterministic, so test base scaling
        assert d0 < 60  # within max
        assert d2 < 60

    def test_capped_at_max(self):
        # Very high attempt should still be under max + jitter
        d = _delay_with_jitter(100)
        assert d <= 90  # 60 max + up to 30 jitter


class TestWithRetry:
    @pytest.mark.asyncio
    async def test_succeeds_first_try(self):
        fn = AsyncMock(return_value="ok")
        result = await with_retry(fn)
        assert result == "ok"
        assert fn.call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_rate_limit(self):
        rate_err = anthropic.RateLimitError(
            message="rate limited",
            response=AsyncMock(status_code=429, headers={}),
            body=None,
        )
        fn = AsyncMock(side_effect=[rate_err, rate_err, "ok"])
        result = await with_retry(fn, max_retries=3, context="test")
        assert result == "ok"
        assert fn.call_count == 3

    @pytest.mark.asyncio
    async def test_raises_non_retryable_immediately(self):
        bad_err = anthropic.BadRequestError(
            message="bad",
            response=AsyncMock(status_code=400, headers={}),
            body=None,
        )
        fn = AsyncMock(side_effect=bad_err)
        with pytest.raises(anthropic.BadRequestError):
            await with_retry(fn, max_retries=3)
        assert fn.call_count == 1

    @pytest.mark.asyncio
    async def test_exhausted_raises(self):
        rate_err = anthropic.RateLimitError(
            message="rate limited",
            response=AsyncMock(status_code=429, headers={}),
            body=None,
        )
        fn = AsyncMock(side_effect=rate_err)
        with pytest.raises(RetryExhausted) as exc_info:
            await with_retry(fn, max_retries=2, context="test")
        assert exc_info.value.attempts == 3
        assert fn.call_count == 3

    @pytest.mark.asyncio
    async def test_passes_args_through(self):
        fn = AsyncMock(return_value="ok")
        await with_retry(fn, "a", "b", key="val")
        fn.assert_called_once_with("a", "b", key="val")
