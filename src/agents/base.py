"""
Base utilities for agent modules.

Provides shared LLM client, retry logic, and common patterns.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional, Any
from functools import wraps

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL,
    THINKING_BUDGET_TOKENS,
    ARIZE_SPACE_ID,
    ARIZE_API_KEY,
    ARIZE_PROJECT_NAME,
    CACHE_TTL,
    BATCH_POLL_INTERVAL_SECONDS,
    BATCH_MAX_WAIT_SECONDS,
)

logger = logging.getLogger(__name__)

# =============================================================================
# RATE LIMITING
# =============================================================================

ANTHROPIC_DELAY_SECONDS = 2  # Rate limit: 50 requests/minute


class AnthropicRateLimiter:
    """
    Global rate limiter for Anthropic API calls.

    Rate limit is 50 requests/minute. With 2s between calls, we stay at 30/min max.
    """

    _lock: asyncio.Lock | None = None
    _last_call_time: float = 0

    @classmethod
    def _get_lock(cls) -> asyncio.Lock:
        """Lazily create the lock to avoid event loop issues."""
        if cls._lock is None:
            cls._lock = asyncio.Lock()
        return cls._lock

    @classmethod
    async def wait(cls):
        """Wait until it's safe to make an Anthropic API call."""
        import time

        lock = cls._get_lock()
        async with lock:
            now = time.monotonic()
            elapsed = now - cls._last_call_time
            if elapsed < ANTHROPIC_DELAY_SECONDS:
                wait_time = ANTHROPIC_DELAY_SECONDS - elapsed
                logger.debug(f"Anthropic rate limiting: waiting {wait_time:.1f}s")
                await asyncio.sleep(wait_time)
            cls._last_call_time = time.monotonic()


# Tracing state
_tracer_provider = None
_tracing_initialized = False


# =============================================================================
# ARIZE TRACING
# =============================================================================

def setup_tracing():
    """
    Initialize Arize AX tracing for Anthropic.

    Requires ARIZE_SPACE_ID and ARIZE_API_KEY environment variables.
    If not set, tracing is disabled silently.
    """
    global _tracer_provider, _tracing_initialized

    if _tracing_initialized:
        return _tracer_provider

    _tracing_initialized = True

    if not ARIZE_SPACE_ID or not ARIZE_API_KEY:
        logger.debug(
            "Arize tracing disabled: ARIZE_SPACE_ID and ARIZE_API_KEY not set"
        )
        return None

    try:
        from arize.otel import register
        from openinference.instrumentation.anthropic import AnthropicInstrumentor

        _tracer_provider = register(
            space_id=ARIZE_SPACE_ID,
            api_key=ARIZE_API_KEY,
            project_name=ARIZE_PROJECT_NAME,
        )

        AnthropicInstrumentor().instrument(tracer_provider=_tracer_provider)

        logger.info(f"Arize tracing enabled for project: {ARIZE_PROJECT_NAME}")
        return _tracer_provider

    except ImportError as e:
        logger.warning(f"Arize tracing packages not installed: {e}")
        return None
    except Exception as e:
        logger.warning(f"Failed to initialize Arize tracing: {e}")
        return None


# =============================================================================
# LLM CLIENT
# =============================================================================

def get_client() -> anthropic.AsyncAnthropic:
    """Get an async Anthropic client."""
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. "
            "Set it via environment variable: export ANTHROPIC_API_KEY='sk-ant-...'"
        )

    # Initialize tracing on first client creation
    setup_tracing()

    return anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


async def complete(
    prompt: str,
    system: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 20000,
    temperature: float = 0.3,
    thinking_budget: int = THINKING_BUDGET_TOKENS,
) -> str:
    """
    Simple completion helper with extended thinking enabled.

    Args:
        prompt: The user message
        system: Optional system prompt
        model: Model to use
        max_tokens: Maximum response tokens (must exceed thinking budget)
        temperature: Ignored when thinking is enabled (API requires temp=1)

    Returns:
        The assistant's response text (thinking blocks are filtered out)
    """
    # Rate limit before making the call
    await AnthropicRateLimiter.wait()

    client = get_client()

    messages = [{"role": "user", "content": prompt}]

    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "thinking": {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        },
    }

    if system:
        kwargs["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral", "ttl": CACHE_TTL},
            }
        ]

    response = await client.messages.create(**kwargs)

    # Log cache usage
    usage = response.usage
    cache_created = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    if cache_created or cache_read:
        logger.debug(
            f"Prompt cache: created={cache_created}, read={cache_read} tokens"
        )

    # Extract text from response, filtering out thinking blocks
    text_blocks = [
        block.text for block in response.content
        if hasattr(block, "text") and block.type == "text"
    ]

    return "\n".join(text_blocks)


async def complete_with_tools(
    prompt: str,
    tools: list[dict],
    system: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 20000,
    thinking_budget: int = THINKING_BUDGET_TOKENS,
) -> tuple[str, list[dict]]:
    """
    Completion with tool use and extended thinking.

    Returns:
        Tuple of (text_response, tool_calls)
    """
    # Rate limit before making the call
    await AnthropicRateLimiter.wait()

    client = get_client()

    messages = [{"role": "user", "content": prompt}]

    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "tools": tools,
        "thinking": {
            "type": "enabled",
            "budget_tokens": thinking_budget,
        },
    }

    if system:
        kwargs["system"] = [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral", "ttl": CACHE_TTL},
            }
        ]

    response = await client.messages.create(**kwargs)

    # Log cache usage
    usage = response.usage
    cache_created = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    if cache_created or cache_read:
        logger.debug(
            f"Prompt cache (tools): created={cache_created}, read={cache_read} tokens"
        )

    text_parts = []
    tool_calls = []

    for block in response.content:
        if block.type == "text" and hasattr(block, "text"):
            text_parts.append(block.text)
        elif block.type == "tool_use":
            tool_calls.append({
                "id": block.id,
                "name": block.name,
                "input": block.input,
            })

    return "\n".join(text_parts), tool_calls


# =============================================================================
# RETRY LOGIC
# =============================================================================

def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator for retrying async functions with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except anthropic.RateLimitError as e:
                    last_error = e
                    wait_time = delay * (2 ** attempt)
                    logger.warning(
                        f"Rate limited, retrying in {wait_time}s "
                        f"(attempt {attempt + 1}/{max_attempts})"
                    )
                    await asyncio.sleep(wait_time)
                except anthropic.APIError as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        wait_time = delay * (2 ** attempt)
                        logger.warning(
                            f"API error: {e}, retrying in {wait_time}s "
                            f"(attempt {attempt + 1}/{max_attempts})"
                        )
                        await asyncio.sleep(wait_time)
                    else:
                        raise
            
            raise last_error
        
        return wrapper
    return decorator


# =============================================================================
# MESSAGE BATCHES API
# =============================================================================


@dataclass
class BatchRequest:
    """A single request within an Anthropic Message Batch."""
    custom_id: str
    prompt: str
    system: str = ""
    model: str = DEFAULT_MODEL
    max_tokens: int = 20000
    thinking_budget: int = THINKING_BUDGET_TOKENS


@dataclass
class BatchResult:
    """Result of a single request within a completed batch."""
    custom_id: str
    text: str = ""
    success: bool = True
    error: str = ""


async def batch_complete(requests: list[BatchRequest]) -> dict[str, BatchResult]:
    """
    Submit requests via the Anthropic Message Batches API and poll until done.

    Returns a dict mapping custom_id -> BatchResult.
    Raises TimeoutError if the batch doesn't complete within BATCH_MAX_WAIT_SECONDS.
    """
    if not requests:
        return {}

    client = get_client()

    # Build batch request objects
    batch_requests = []
    for req in requests:
        params: dict[str, Any] = {
            "model": req.model,
            "max_tokens": req.max_tokens,
            "messages": [{"role": "user", "content": req.prompt}],
            "thinking": {
                "type": "enabled",
                "budget_tokens": req.thinking_budget,
            },
        }
        if req.system:
            params["system"] = [
                {
                    "type": "text",
                    "text": req.system,
                    "cache_control": {"type": "ephemeral", "ttl": CACHE_TTL},
                }
            ]

        batch_requests.append({
            "custom_id": req.custom_id,
            "params": params,
        })

    logger.info(f"Submitting message batch with {len(batch_requests)} requests")

    # Submit batch
    batch = await client.messages.batches.create(requests=batch_requests)
    batch_id = batch.id
    logger.info(f"Batch {batch_id} submitted, polling for completion")

    # Poll until complete or timeout
    import time
    start_time = time.monotonic()

    while True:
        elapsed = time.monotonic() - start_time
        if elapsed > BATCH_MAX_WAIT_SECONDS:
            logger.error(f"Batch {batch_id} timed out after {elapsed:.0f}s, canceling")
            try:
                await client.messages.batches.cancel(batch_id)
            except Exception as e:
                logger.warning(f"Failed to cancel batch {batch_id}: {e}")
            raise TimeoutError(
                f"Batch {batch_id} did not complete within {BATCH_MAX_WAIT_SECONDS}s"
            )

        batch = await client.messages.batches.retrieve(batch_id)
        status = batch.processing_status

        if status == "ended":
            logger.info(
                f"Batch {batch_id} ended: "
                f"{batch.request_counts.succeeded} succeeded, "
                f"{batch.request_counts.errored} errored, "
                f"{batch.request_counts.expired} expired"
            )
            break

        logger.debug(
            f"Batch {batch_id} status: {status} "
            f"(elapsed {elapsed:.0f}s)"
        )
        await asyncio.sleep(BATCH_POLL_INTERVAL_SECONDS)

    # Collect results
    results: dict[str, BatchResult] = {}

    result_stream = await client.messages.batches.results(batch_id)
    async for entry in result_stream:
        custom_id = entry.custom_id

        if entry.result.type == "succeeded":
            message = entry.result.message
            text_blocks = [
                block.text for block in message.content
                if hasattr(block, "text") and block.type == "text"
            ]
            results[custom_id] = BatchResult(
                custom_id=custom_id,
                text="\n".join(text_blocks),
                success=True,
            )
        else:
            error_msg = str(getattr(entry.result, "error", "unknown error"))
            logger.warning(f"Batch request {custom_id} failed: {error_msg}")
            results[custom_id] = BatchResult(
                custom_id=custom_id,
                success=False,
                error=error_msg,
            )

    return results


# =============================================================================
# CONCURRENT BATCH PROCESSING
# =============================================================================

async def process_batch(
    items: list,
    processor: callable,
    max_concurrent: int = 5,
    desc: str = "Processing",
) -> list:
    """
    Process items in batches with controlled concurrency.
    
    Args:
        items: Items to process
        processor: Async function to apply to each item
        max_concurrent: Maximum concurrent operations
        desc: Description for logging
        
    Returns:
        List of results in same order as inputs
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_with_limit(item, index):
        async with semaphore:
            try:
                result = await processor(item)
                return (index, result, None)
            except Exception as e:
                logger.error(f"{desc} failed for item {index}: {e}")
                return (index, None, e)
    
    tasks = [
        process_with_limit(item, i) 
        for i, item in enumerate(items)
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Sort by original index and extract results
    results.sort(key=lambda x: x[0])
    
    return [r[1] for r in results]


# =============================================================================
# TEXT UTILITIES
# =============================================================================

def truncate_text(text: str, max_chars: int = 10000) -> str:
    """Truncate text to max characters, trying to break at sentence."""
    if len(text) <= max_chars:
        return text
    
    # Try to break at last sentence
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    
    return truncated + "..."


def extract_json_from_response(text: str) -> Optional[dict]:
    """
    Extract JSON object from LLM response.
    
    Handles cases where JSON is wrapped in markdown code blocks.
    """
    import json
    import re
    
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract from code block
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object in text
    json_match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    return None
