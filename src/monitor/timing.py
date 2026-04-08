"""
Operational timing utilities for pipeline observability.

Provides three tools for diagnosing hangs and measuring performance:

- timed_operation: context manager that logs start + elapsed time
- TrackedSemaphore: semaphore with in-flight/waiting visibility
- with_heartbeat: periodic proof-of-life during long coroutines
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Awaitable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


# =============================================================================
# timed_operation — logs start + elapsed time
# =============================================================================

@asynccontextmanager
async def timed_operation(description: str, log: logging.Logger | None = None, level: int = logging.INFO):
    """Log start and elapsed time for an async operation.

    Usage:
        async with timed_operation("Country agent mx: API call", logger):
            response = await client.messages.create(...)
        # Logs: "Country agent mx: API call — started"
        # Logs: "Country agent mx: API call — 142.3s"
    """
    log = log or logger
    log.log(level, "%s — started", description)
    start = time.monotonic()
    try:
        yield
    finally:
        elapsed = time.monotonic() - start
        log.log(level, "%s — %.1fs", description, elapsed)


@contextmanager
def timed_operation_sync(description: str, log: logging.Logger | None = None, level: int = logging.INFO):
    """Sync version of timed_operation."""
    log = log or logger
    log.log(level, "%s — started", description)
    start = time.monotonic()
    try:
        yield
    finally:
        elapsed = time.monotonic() - start
        log.log(level, "%s — %.1fs", description, elapsed)


# =============================================================================
# TrackedSemaphore — semaphore with in-flight visibility
# =============================================================================

class TrackedSemaphore:
    """Semaphore that logs what's waiting and what's running.

    Usage:
        sem = TrackedSemaphore(5, name="country_agents")
        async with sem.acquire("mx"):
            await do_work()
    """

    def __init__(self, value: int, name: str = ""):
        self._sem = asyncio.Semaphore(value)
        self._name = name
        self._in_flight: set[str] = set()
        self._waiting: int = 0

    @asynccontextmanager
    async def acquire(self, label: str):
        """Acquire a semaphore slot with logging."""
        if self._sem.locked():
            self._waiting += 1
            logger.info(
                "%s: %s waiting for slot (%d in-flight: %s)",
                self._name, label, len(self._in_flight),
                ", ".join(sorted(self._in_flight)),
            )

        await self._sem.acquire()
        self._waiting = max(0, self._waiting - 1)
        self._in_flight.add(label)
        logger.debug(
            "%s: %s acquired slot (%d in-flight)",
            self._name, label, len(self._in_flight),
        )
        try:
            yield
        finally:
            self._in_flight.discard(label)
            self._sem.release()
            logger.debug(
                "%s: %s released slot (%d in-flight)",
                self._name, label, len(self._in_flight),
            )

    @property
    def in_flight(self) -> set[str]:
        return self._in_flight.copy()

    @property
    def in_flight_count(self) -> int:
        return len(self._in_flight)


# =============================================================================
# with_heartbeat — periodic proof-of-life during long coroutines
# =============================================================================

async def with_heartbeat(
    coro: Awaitable[T],
    description: str,
    interval: int = 60,
    log: logging.Logger | None = None,
) -> T:
    """Run a coroutine with periodic heartbeat logging.

    Usage:
        response = await with_heartbeat(
            client.messages.create(**kwargs),
            "Country agent mx: API call",
            interval=60,
        )
    # Logs every 60s: "Country agent mx: API call — still running (60s elapsed)"
    """
    log = log or logger
    start = time.monotonic()
    task = asyncio.ensure_future(coro)

    while not task.done():
        try:
            await asyncio.wait_for(asyncio.shield(task), timeout=interval)
        except asyncio.TimeoutError:
            elapsed = time.monotonic() - start
            log.info("%s — still running (%.0fs elapsed)", description, elapsed)
        except asyncio.CancelledError:
            task.cancel()
            raise

    return task.result()
