"""Shared helper: stream an Anthropic message with rate-limit + retry."""

import anthropic

from ..rate_limit import anthropic_limiter
from ..retry import with_retry
from ..timing import with_heartbeat


async def _stream_once(
    client: anthropic.AsyncAnthropic,
    heartbeat_label: str,
    **stream_kwargs,
) -> anthropic.types.Message:
    async with anthropic_limiter():
        async with client.messages.stream(**stream_kwargs) as stream:
            return await with_heartbeat(stream.get_final_message(), heartbeat_label)


async def stream_with_retry(
    client: anthropic.AsyncAnthropic,
    heartbeat_label: str,
    retry_context: str,
    **stream_kwargs,
) -> anthropic.types.Message:
    """Stream an Anthropic message with rate-limit + retry on transient errors.

    Covers mid-stream network drops (httpx.RemoteProtocolError, etc.) that the
    Anthropic SDK re-raises raw, in addition to its own transient error classes.
    Each retry attempt re-acquires the rate limiter and opens a fresh stream.
    """
    return await with_retry(
        _stream_once,
        client,
        heartbeat_label,
        context=retry_context,
        **stream_kwargs,
    )
