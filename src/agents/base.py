"""
Base utilities for agent modules.

Provides shared LLM client, retry logic, and common patterns.
"""

import asyncio
import logging
from typing import Optional, Any
from functools import wraps

import anthropic

from ..config import (
    ANTHROPIC_API_KEY,
    DEFAULT_MODEL,
    ARIZE_SPACE_ID,
    ARIZE_API_KEY,
    ARIZE_PROJECT_NAME,
)

logger = logging.getLogger(__name__)

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
    max_tokens: int = 4096,
    temperature: float = 0.3,
) -> str:
    """
    Simple completion helper.
    
    Args:
        prompt: The user message
        system: Optional system prompt
        model: Model to use
        max_tokens: Maximum response tokens
        temperature: Sampling temperature
        
    Returns:
        The assistant's response text
    """
    client = get_client()
    
    messages = [{"role": "user", "content": prompt}]
    
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": temperature,
    }
    
    if system:
        kwargs["system"] = system
    
    response = await client.messages.create(**kwargs)
    
    # Extract text from response
    text_blocks = [
        block.text for block in response.content 
        if hasattr(block, "text")
    ]
    
    return "\n".join(text_blocks)


async def complete_with_tools(
    prompt: str,
    tools: list[dict],
    system: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 4096,
) -> tuple[str, list[dict]]:
    """
    Completion with tool use.
    
    Returns:
        Tuple of (text_response, tool_calls)
    """
    client = get_client()
    
    messages = [{"role": "user", "content": prompt}]
    
    kwargs: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "tools": tools,
    }
    
    if system:
        kwargs["system"] = system
    
    response = await client.messages.create(**kwargs)
    
    text_parts = []
    tool_calls = []
    
    for block in response.content:
        if hasattr(block, "text"):
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
# BATCH PROCESSING
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
