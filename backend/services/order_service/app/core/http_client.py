"""
A single shared httpx.AsyncClient is created at app startup and torn down at
shutdown. Reusing the same client (and its connection pool) across requests
is much faster than creating a new client per call.

Event hooks log every outbound request/response and propagate the current
request id (`X-Request-ID`) so a single inbound request can be traced as it
fans out to other services.
"""
from __future__ import annotations

import logging
import time

import httpx

from app.core.config import settings
from app.core.logging import get_request_id

logger = logging.getLogger("app.http")
_START_KEY = "_x_started_at"

_client: httpx.AsyncClient | None = None


async def _on_request(request: httpx.Request) -> None:
    request.extensions[_START_KEY] = time.perf_counter()
    rid = get_request_id()
    if rid != "-":
        request.headers.setdefault("X-Request-ID", rid)
    logger.info("-> %-6s %s", request.method, request.url)


async def _on_response(response: httpx.Response) -> None:
    started = response.request.extensions.get(_START_KEY)
    elapsed_ms = (time.perf_counter() - started) * 1000 if started else 0.0
    logger.info(
        "<- %-3d %-6s %s (%.0fms)",
        response.status_code,
        response.request.method,
        response.request.url,
        elapsed_ms,
    )


async def startup() -> None:
    global _client
    _client = httpx.AsyncClient(
        timeout=settings.REQUEST_TIMEOUT,
        event_hooks={"request": [_on_request], "response": [_on_response]},
    )


async def shutdown() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_client() -> httpx.AsyncClient:
    if _client is None:
        raise RuntimeError("HTTP client not initialised; did lifespan run?")
    return _client
