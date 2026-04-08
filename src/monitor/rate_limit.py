"""
Per-call rate limiting for external API services.

Provides a RateLimiter that enforces minimum intervals between calls
and supports coordinated backoff when a rate limit (429) is hit.
All concurrent tasks sharing a limiter respect the pause.
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager

from .config import load_settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter with coordinated backoff.

    Usage:
        limiter = RateLimiter("anthropic", rpm=50)

        async with limiter():
            response = await client.messages.create(...)

        # On 429:
        await limiter.backoff(30)  # pauses ALL callers for 30s
    """

    def __init__(self, name: str, rpm: float = 60):
        self._name = name
        self._min_interval = 60.0 / rpm if rpm > 0 else 0
        self._last_request = 0.0
        self._lock = asyncio.Lock()

    @asynccontextmanager
    async def __call__(self):
        """Acquire a rate limit slot, waiting if needed."""
        async with self._lock:
            now = time.monotonic()
            wait = self._min_interval - (now - self._last_request)
            if wait > 0:
                logger.debug("%s: rate limiting, waiting %.1fs", self._name, wait)
                await asyncio.sleep(wait)
            self._last_request = time.monotonic()
        yield

    async def backoff(self, seconds: float) -> None:
        """Called on 429 — pushes _last_request forward so all callers pause."""
        async with self._lock:
            logger.warning(
                "%s: rate limited — pausing all calls for %.0fs",
                self._name, seconds,
            )
            self._last_request = time.monotonic() + seconds


# Module-level singleton — shared across all agents
_settings = load_settings()
anthropic_limiter = RateLimiter("anthropic", rpm=_settings.get("anthropic_rpm", 50))
