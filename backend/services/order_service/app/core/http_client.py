"""
A single shared httpx.AsyncClient is created at app startup and torn down at
shutdown. Reusing the same client (and its connection pool) across requests
is much faster than creating a new client per call.
"""
from __future__ import annotations

import httpx

from app.core.config import settings

_client: httpx.AsyncClient | None = None


async def startup() -> None:
    global _client
    _client = httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT)


async def shutdown() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HTTP client not initialised; did lifespan run?")
    return _client
