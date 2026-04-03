"""Tests for the per-call rate limiter."""

import asyncio
import time

import pytest

from src.monitor.rate_limit import RateLimiter


class TestRateLimiter:
    @pytest.mark.asyncio
    async def test_basic_acquire(self):
        limiter = RateLimiter("test", rpm=600)  # 10 per second
        async with limiter():
            pass  # should not raise

    @pytest.mark.asyncio
    async def test_enforces_interval(self):
        limiter = RateLimiter("test", rpm=60)  # 1 per second
        start = time.monotonic()
        async with limiter():
            pass
        async with limiter():
            pass
        elapsed = time.monotonic() - start
        assert elapsed >= 0.9  # should wait ~1s between calls

    @pytest.mark.asyncio
    async def test_backoff_pauses_callers(self):
        limiter = RateLimiter("test", rpm=6000)  # very fast normally
        await limiter.backoff(0.2)  # pause for 200ms

        start = time.monotonic()
        async with limiter():
            pass
        elapsed = time.monotonic() - start
        assert elapsed >= 0.15  # should have waited for backoff

    @pytest.mark.asyncio
    async def test_zero_rpm_no_throttle(self):
        limiter = RateLimiter("test", rpm=0)
        async with limiter():
            pass
        async with limiter():
            pass  # should be instant
