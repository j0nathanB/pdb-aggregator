"""Tests for the operational timing utilities."""

import asyncio
import logging

import pytest

from src.monitor.timing import TrackedSemaphore, timed_operation, with_heartbeat


# =============================================================================
# timed_operation
# =============================================================================

class TestTimedOperation:
    @pytest.mark.asyncio
    async def test_logs_start_and_elapsed(self, caplog):
        with caplog.at_level(logging.INFO):
            async with timed_operation("test op"):
                pass
        messages = [r.message for r in caplog.records]
        assert any("test op — started" in m for m in messages)
        assert any("test op —" in m and "s" in m for m in messages)

    @pytest.mark.asyncio
    async def test_logs_on_exception(self, caplog):
        with caplog.at_level(logging.INFO):
            with pytest.raises(ValueError):
                async with timed_operation("failing op"):
                    raise ValueError("boom")
        messages = [r.message for r in caplog.records]
        # Should still log elapsed even on exception
        assert any("failing op —" in m and "s" in m for m in messages)

    @pytest.mark.asyncio
    async def test_custom_logger_and_level(self, caplog):
        custom_logger = logging.getLogger("custom")
        with caplog.at_level(logging.DEBUG, logger="custom"):
            async with timed_operation("debug op", log=custom_logger, level=logging.DEBUG):
                pass
        messages = [r.message for r in caplog.records if r.name == "custom"]
        assert len(messages) == 2  # started + elapsed


# =============================================================================
# TrackedSemaphore
# =============================================================================

class TestTrackedSemaphore:
    @pytest.mark.asyncio
    async def test_basic_acquire_release(self):
        sem = TrackedSemaphore(2, "test")
        async with sem.acquire("task_a"):
            assert "task_a" in sem.in_flight
            assert sem.in_flight_count == 1
        assert sem.in_flight_count == 0

    @pytest.mark.asyncio
    async def test_concurrent_tracking(self):
        sem = TrackedSemaphore(3, "test")
        acquired = asyncio.Event()
        release = asyncio.Event()

        async def hold(label: str):
            async with sem.acquire(label):
                acquired.set()
                await release.wait()

        task = asyncio.create_task(hold("a"))
        await acquired.wait()
        assert sem.in_flight == {"a"}

        acquired.clear()
        task2 = asyncio.create_task(hold("b"))
        await acquired.wait()
        assert sem.in_flight == {"a", "b"}

        release.set()
        await task
        await task2

    @pytest.mark.asyncio
    async def test_waiting_logs_in_flight(self, caplog):
        sem = TrackedSemaphore(1, "test_sem")
        hold = asyncio.Event()
        started = asyncio.Event()

        async def block():
            async with sem.acquire("blocker"):
                started.set()
                await hold.wait()

        async def waiter():
            async with sem.acquire("waiter"):
                pass

        with caplog.at_level(logging.INFO):
            task1 = asyncio.create_task(block())
            await started.wait()

            task2 = asyncio.create_task(waiter())
            await asyncio.sleep(0.01)  # let waiter hit the semaphore

            hold.set()
            await task1
            await task2

        messages = " ".join(r.message for r in caplog.records)
        assert "waiter waiting for slot" in messages
        assert "blocker" in messages

    @pytest.mark.asyncio
    async def test_in_flight_property_is_copy(self):
        sem = TrackedSemaphore(2, "test")
        async with sem.acquire("a"):
            snapshot = sem.in_flight
            snapshot.add("fake")
            assert "fake" not in sem.in_flight  # original not modified


# =============================================================================
# with_heartbeat
# =============================================================================

class TestWithHeartbeat:
    @pytest.mark.asyncio
    async def test_returns_result(self):
        async def fast():
            return 42

        result = await with_heartbeat(fast(), "fast op", interval=1)
        assert result == 42

    @pytest.mark.asyncio
    async def test_heartbeat_fires_on_slow_op(self, caplog):
        async def slow():
            await asyncio.sleep(0.15)
            return "done"

        with caplog.at_level(logging.INFO):
            result = await with_heartbeat(slow(), "slow op", interval=0.05)

        assert result == "done"
        messages = [r.message for r in caplog.records]
        heartbeats = [m for m in messages if "still running" in m]
        assert len(heartbeats) >= 1

    @pytest.mark.asyncio
    async def test_no_heartbeat_on_fast_op(self, caplog):
        async def fast():
            return "quick"

        with caplog.at_level(logging.INFO):
            await with_heartbeat(fast(), "fast op", interval=10)

        messages = [r.message for r in caplog.records]
        heartbeats = [m for m in messages if "still running" in m]
        assert len(heartbeats) == 0

    @pytest.mark.asyncio
    async def test_propagates_exception(self):
        async def failing():
            raise ValueError("api error")

        with pytest.raises(ValueError, match="api error"):
            await with_heartbeat(failing(), "failing op", interval=1)
