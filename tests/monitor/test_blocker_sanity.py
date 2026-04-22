"""Sanity check: the autouse network blocker raises on real API calls."""
import httpx
import pytest


def test_sync_call_to_anthropic_is_blocked():
    client = httpx.Client()
    with pytest.raises(Exception) as exc_info:
        client.get("https://api.anthropic.com/v1/messages")
    assert "Blocked" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_call_to_anthropic_is_blocked():
    async with httpx.AsyncClient() as client:
        with pytest.raises(Exception) as exc_info:
            await client.get("https://api.anthropic.com/v1/messages")
        assert "Blocked" in str(exc_info.value)
