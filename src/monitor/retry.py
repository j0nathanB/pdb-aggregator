"""
Retry and error handling utilities for API calls.

Provides exponential backoff with jitter for rate limit (429) and transient errors.
"""

import asyncio
import logging
import random
from functools import wraps
from typing import Callable, TypeVar

import anthropic

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Retryable exception types
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 529}
MAX_RETRIES = 3
BASE_DELAY = 2.0
MAX_DELAY = 60.0


class RetryExhausted(Exception):
    """All retry attempts failed."""

    def __init__(self, attempts: int, last_error: Exception):
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Failed after {attempts} attempts: {last_error}")


def _is_retryable(exc: Exception) -> bool:
    """Check if an exception is retryable."""
    if isinstance(exc, anthropic.RateLimitError):
        return True
    if isinstance(exc, anthropic.APIStatusError):
        return exc.status_code in RETRYABLE_STATUS_CODES
    if isinstance(exc, (anthropic.APIConnectionError, anthropic.APITimeoutError)):
        return True
    return False


def _delay_with_jitter(attempt: int) -> float:
    """Calculate delay with exponential backoff and jitter."""
    delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)
    jitter = random.uniform(0, delay * 0.5)
    return delay + jitter


async def with_retry(
    fn: Callable,
    *args,
    max_retries: int = MAX_RETRIES,
    context: str = "",
    **kwargs,
) -> T:
    """
    Call an async function with retry on transient failures.

    Args:
        fn: Async function to call.
        max_retries: Maximum number of retry attempts.
        context: Description for logging (e.g., "country agent mx").

    Returns:
        The function's return value.

    Raises:
        RetryExhausted: If all attempts fail.
        Exception: If a non-retryable error occurs.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return await fn(*args, **kwargs)
        except Exception as e:
            last_error = e
            if not _is_retryable(e):
                raise

            if attempt < max_retries:
                delay = _delay_with_jitter(attempt)

                # Coordinated backoff: if it's a rate limit, pause all callers
                if isinstance(e, anthropic.RateLimitError):
                    from .rate_limit import anthropic_limiter
                    retry_after = float(getattr(e.response, "headers", {}).get("retry-after", delay))
                    await anthropic_limiter.backoff(retry_after)

                logger.warning(
                    f"Retry {attempt + 1}/{max_retries} for {context or fn.__name__}: "
                    f"{type(e).__name__}: {e} (waiting {delay:.1f}s)"
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    f"All {max_retries} retries exhausted for {context or fn.__name__}: {e}"
                )

    raise RetryExhausted(max_retries + 1, last_error)
