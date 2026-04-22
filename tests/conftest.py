"""Shared fixtures for PDB tests.

Network blocker: any test that attempts to hit a known external API
(Anthropic, Brave, Browserbase, Diffbot, OpenAI) without mocking will
raise `RealAPICallError` with the URL. Tests that legitimately need
network should be marked `@pytest.mark.integration` (excluded by
default via pytest.ini addopts).

Implementation: monkeypatch the low-level transport on httpx clients
(sync + async) and `socket.getaddrinfo` so any outbound connection to
a blocklisted domain fails loudly with a stack trace pointing at the
test.
"""

import socket

import pytest


class RealAPICallError(RuntimeError):
    """Raised when a test tries to reach an external API without mocking."""


_BLOCKED_HOSTS = (
    "api.anthropic.com",
    "api.search.brave.com",
    "api.browserbase.com",
    "api.diffbot.com",
    "api.openai.com",
    "content.guardianapis.com",
)


def _is_blocked(host: str) -> bool:
    return any(host == b or host.endswith("." + b) for b in _BLOCKED_HOSTS)


@pytest.fixture(autouse=True)
def block_real_api_calls(monkeypatch, request):
    """Raise if a test connects to a blocklisted host without mocking.

    Tests marked `integration` opt out — those are expected to hit real
    services (and are excluded from the default suite via pytest.ini).
    """
    if request.node.get_closest_marker("integration"):
        return

    # httpx: patch AsyncClient/Client.send at the HTTP layer so any
    # path through the library is caught, even if the test forgot to
    # mock the specific method it calls.
    try:
        import httpx

        original_async_send = httpx.AsyncClient.send
        original_sync_send = httpx.Client.send

        async def guarded_async_send(self, request_, *args, **kwargs):
            host = request_.url.host or ""
            if _is_blocked(host):
                raise RealAPICallError(
                    f"Blocked real API call during test: {request_.method} "
                    f"{request_.url}. Mock the client (e.g., patch the "
                    f"agent's anthropic.AsyncAnthropic / BraveNewsClient) "
                    f"or mark the test @pytest.mark.integration."
                )
            return await original_async_send(self, request_, *args, **kwargs)

        def guarded_sync_send(self, request_, *args, **kwargs):
            host = request_.url.host or ""
            if _is_blocked(host):
                raise RealAPICallError(
                    f"Blocked real API call during test: {request_.method} "
                    f"{request_.url}. Mock or mark @pytest.mark.integration."
                )
            return original_sync_send(self, request_, *args, **kwargs)

        monkeypatch.setattr(httpx.AsyncClient, "send", guarded_async_send)
        monkeypatch.setattr(httpx.Client, "send", guarded_sync_send)
    except ImportError:
        pass

    # socket.getaddrinfo: catches anything that bypasses httpx (urllib,
    # requests at the connection-pool level, raw sockets). This is the
    # backstop.
    original_getaddrinfo = socket.getaddrinfo

    def guarded_getaddrinfo(host, *args, **kwargs):
        if isinstance(host, str) and _is_blocked(host):
            raise RealAPICallError(
                f"Blocked DNS lookup for {host} during test. Mock the "
                f"client or mark @pytest.mark.integration."
            )
        return original_getaddrinfo(host, *args, **kwargs)

    monkeypatch.setattr(socket, "getaddrinfo", guarded_getaddrinfo)
