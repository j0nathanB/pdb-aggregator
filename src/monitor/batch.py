"""Batch API driver for parallel stage execution.

Submits a list of requests via `client.messages.batches.create`, polls until
the batch ends, then streams results and returns them keyed by custom_id.
Designed for the weekly pipeline's parallel-x-30 stages (country, story_map,
government): flat 50% discount on input + output for any job completing
within 24h — Anthropic's Batch API SLA. The pipeline is weekly, so latency
doesn't matter.

The driver returns all per-request outcomes (success and failure). Callers
decide what to do on partial failure — retry the failed ones via sync,
abort, or accept the partial result.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import anthropic
from anthropic.types.message import Message

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BatchRequest:
    """One entry in a batch submission.

    custom_id: caller-chosen identifier (max 64 chars, alphanumeric +
        underscore/hyphen). Must be unique within the batch. Used to map
        responses back to the originating call site (e.g. country code).
    params: same shape as `client.messages.create(**params)` kwargs —
        model, max_tokens, system, messages, tools, thinking, etc.
    """

    custom_id: str
    params: dict[str, Any]


@dataclass
class BatchResult:
    """One outcome from a batch run, keyed back by the request's custom_id."""

    custom_id: str
    message: Message | None  # set when result.type == "succeeded"
    error_type: str | None  # "errored" | "canceled" | "expired" — None on success
    error_detail: Any | None  # structured error from the API, when available

    @property
    def succeeded(self) -> bool:
        return self.message is not None


async def run_batch(
    client: anthropic.AsyncAnthropic,
    requests: list[BatchRequest],
    *,
    label: str = "batch",
    initial_poll_delay: float = 10.0,
    poll_interval: float = 30.0,
    max_poll_interval: float = 120.0,
    timeout: float = 86400.0,
) -> dict[str, BatchResult]:
    """Submit a batch, poll until it ends, return per-request results.

    The poll cadence ramps from `poll_interval` toward `max_poll_interval`
    on each iteration — short polls early catch fast batches, longer polls
    later avoid hammering the API on slow ones. `timeout` is the wall-clock
    ceiling; default matches Anthropic's 24h Batch API SLA.

    On per-request failure (errored/canceled/expired), the result is still
    returned with `succeeded=False` — the caller decides whether to retry
    or fall back. The whole call only raises on submit error, transport
    error, or timeout.
    """
    if not requests:
        return {}

    logger.info("%s: submitting batch of %d requests", label, len(requests))
    batch = await client.messages.batches.create(
        requests=[{"custom_id": r.custom_id, "params": r.params} for r in requests],
    )
    logger.info("%s: batch_id=%s submitted", label, batch.id)

    # Some batches complete in seconds — start with a short delay before the
    # first poll instead of waiting a full poll_interval.
    await asyncio.sleep(initial_poll_delay)
    elapsed = initial_poll_delay
    current_interval = poll_interval

    while True:
        batch = await client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            counts = batch.request_counts
            logger.info(
                "%s: batch ended after %.0fs — succeeded=%d errored=%d canceled=%d expired=%d",
                label,
                elapsed,
                counts.succeeded,
                counts.errored,
                counts.canceled,
                counts.expired,
            )
            break
        if elapsed >= timeout:
            raise TimeoutError(
                f"{label}: batch {batch.id} did not end within {timeout:.0f}s "
                f"(status={batch.processing_status})"
            )
        logger.debug(
            "%s: in_progress (processing=%d succeeded=%d errored=%d) — next poll in %.0fs",
            label,
            batch.request_counts.processing,
            batch.request_counts.succeeded,
            batch.request_counts.errored,
            current_interval,
        )
        await asyncio.sleep(current_interval)
        elapsed += current_interval
        current_interval = min(current_interval * 1.5, max_poll_interval)

    results: dict[str, BatchResult] = {}
    async for indiv in await client.messages.batches.results(batch.id):
        cid = indiv.custom_id
        result = indiv.result
        if result.type == "succeeded":
            results[cid] = BatchResult(
                custom_id=cid, message=result.message, error_type=None, error_detail=None
            )
        else:
            detail = getattr(result, "error", None)
            logger.warning("%s: request %s failed (%s)", label, cid, result.type)
            results[cid] = BatchResult(
                custom_id=cid, message=None, error_type=result.type, error_detail=detail
            )

    missing = [r.custom_id for r in requests if r.custom_id not in results]
    if missing:
        # Shouldn't happen — Anthropic returns one result per request. Log it
        # rather than silently dropping; caller will see succeeded=False if
        # they iterate over the original requests.
        logger.error(
            "%s: %d custom_ids missing from batch results: %s",
            label,
            len(missing),
            missing[:5],
        )

    return results
