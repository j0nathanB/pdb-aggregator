"""Tests for the batch driver in src.monitor.batch."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.monitor.batch import BatchRequest, BatchResult, run_batch


# ---- Test helpers ----


def _make_counts(*, processing=0, succeeded=0, errored=0, canceled=0, expired=0):
    return SimpleNamespace(
        processing=processing,
        succeeded=succeeded,
        errored=errored,
        canceled=canceled,
        expired=expired,
    )


def _make_batch(status: str, batch_id: str = "batch_123", **counts):
    return SimpleNamespace(
        id=batch_id,
        processing_status=status,
        request_counts=_make_counts(**counts),
    )


def _make_succeeded(custom_id: str, message_text: str = "ok"):
    """Build a MessageBatchIndividualResponse with result.type='succeeded'."""
    message = SimpleNamespace(content=[SimpleNamespace(type="text", text=message_text)])
    return SimpleNamespace(
        custom_id=custom_id,
        result=SimpleNamespace(type="succeeded", message=message),
    )


def _make_failed(custom_id: str, result_type: str = "errored", error: dict | None = None):
    return SimpleNamespace(
        custom_id=custom_id,
        result=SimpleNamespace(type=result_type, error=error),
    )


class _AsyncIter:
    """Stand-in for AsyncJSONLDecoder — just an async iterable over a list."""

    def __init__(self, items):
        self._items = items

    def __aiter__(self):
        return self._aiter()

    async def _aiter(self):
        for item in self._items:
            yield item


def _mock_client(submit_batch, retrieves, results_items):
    """Build an AsyncAnthropic mock with the three batch methods wired."""
    client = MagicMock()
    batches = MagicMock()
    batches.create = AsyncMock(return_value=submit_batch)
    # retrieves is a list of MessageBatch objects, returned in order.
    batches.retrieve = AsyncMock(side_effect=retrieves)
    batches.results = AsyncMock(return_value=_AsyncIter(results_items))
    client.messages = MagicMock()
    client.messages.batches = batches
    return client


# ---- Tests ----


class TestRunBatch:
    @pytest.mark.asyncio
    async def test_empty_request_list_returns_empty_dict(self):
        client = MagicMock()
        result = await run_batch(client, [])
        assert result == {}

    @pytest.mark.asyncio
    async def test_happy_path_returns_succeeded_results(self):
        requests = [
            BatchRequest("mx", {"model": "test", "messages": []}),
            BatchRequest("jp", {"model": "test", "messages": []}),
        ]
        client = _mock_client(
            submit_batch=_make_batch("in_progress"),
            retrieves=[_make_batch("ended", succeeded=2)],
            results_items=[
                _make_succeeded("mx", "mx response"),
                _make_succeeded("jp", "jp response"),
            ],
        )
        results = await run_batch(client, requests, initial_poll_delay=0, poll_interval=0)
        assert set(results.keys()) == {"mx", "jp"}
        assert results["mx"].succeeded
        assert results["jp"].succeeded
        assert results["mx"].message.content[0].text == "mx response"
        assert results["mx"].error_type is None

    @pytest.mark.asyncio
    async def test_polls_until_ended(self):
        """Verifies the driver polls multiple times before the batch ends."""
        requests = [BatchRequest("mx", {"model": "test", "messages": []})]
        client = _mock_client(
            submit_batch=_make_batch("in_progress"),
            retrieves=[
                _make_batch("in_progress", processing=1),
                _make_batch("in_progress", processing=1),
                _make_batch("ended", succeeded=1),
            ],
            results_items=[_make_succeeded("mx")],
        )
        results = await run_batch(
            client, requests, initial_poll_delay=0, poll_interval=0, max_poll_interval=0
        )
        assert client.messages.batches.retrieve.await_count == 3
        assert results["mx"].succeeded

    @pytest.mark.asyncio
    async def test_partial_failure_returns_both_outcomes(self):
        """The driver must return all per-request outcomes — caller decides
        whether to retry or fall back, the driver doesn't second-guess."""
        requests = [
            BatchRequest("mx", {"model": "test", "messages": []}),
            BatchRequest("jp", {"model": "test", "messages": []}),
            BatchRequest("de", {"model": "test", "messages": []}),
        ]
        client = _mock_client(
            submit_batch=_make_batch("in_progress"),
            retrieves=[_make_batch("ended", succeeded=1, errored=1, expired=1)],
            results_items=[
                _make_succeeded("mx", "ok"),
                _make_failed("jp", "errored", error={"type": "overloaded_error"}),
                _make_failed("de", "expired"),
            ],
        )
        results = await run_batch(client, requests, initial_poll_delay=0, poll_interval=0)
        assert results["mx"].succeeded
        assert not results["jp"].succeeded
        assert results["jp"].error_type == "errored"
        assert results["jp"].error_detail == {"type": "overloaded_error"}
        assert not results["de"].succeeded
        assert results["de"].error_type == "expired"

    @pytest.mark.asyncio
    async def test_timeout_raises(self):
        """If the batch never ends within timeout, the driver raises rather
        than blocking forever or returning incomplete results silently."""
        requests = [BatchRequest("mx", {"model": "test", "messages": []})]
        client = _mock_client(
            submit_batch=_make_batch("in_progress"),
            # Every retrieve returns in_progress — never ends.
            retrieves=[_make_batch("in_progress", processing=1)] * 100,
            results_items=[],
        )
        with pytest.raises(TimeoutError):
            await run_batch(
                client,
                requests,
                initial_poll_delay=0,
                poll_interval=0,
                max_poll_interval=0,
                timeout=0,  # any non-zero elapsed time exceeds the timeout
            )

    @pytest.mark.asyncio
    async def test_submit_payload_shape(self):
        """The driver should submit {custom_id, params} per the SDK contract."""
        requests = [BatchRequest("mx", {"model": "test", "messages": [{"role": "user", "content": "hi"}]})]
        client = _mock_client(
            submit_batch=_make_batch("ended", succeeded=1, batch_id="b1"),
            # The batch is already ended at submit; first retrieve confirms it.
            retrieves=[_make_batch("ended", succeeded=1, batch_id="b1")],
            results_items=[_make_succeeded("mx")],
        )
        await run_batch(client, requests, initial_poll_delay=0)
        submitted = client.messages.batches.create.await_args.kwargs["requests"]
        assert submitted == [
            {
                "custom_id": "mx",
                "params": {"model": "test", "messages": [{"role": "user", "content": "hi"}]},
            }
        ]
