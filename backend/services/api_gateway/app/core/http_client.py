"""Shared httpx.AsyncClient managed by the FastAPI lifespan.

Event hooks log every outbound request/response and propagate the current
request id (`X-Request-ID`) so a single inbound request can be traced as it
fans out to other services.
"""
from __future__ import annotations

import logging
import time

import httpx
from fastapi import HTTPException, status

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


async def proxy(method: str, url: str, **kwargs) -> dict:
    """Forward a request to a downstream service and translate failures."""
    client = get_client()
    try:
        r = await client.request(method, url, **kwargs)
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: {e}",
        )
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        raise HTTPException(status_code=r.status_code, detail=detail)
    return r.json()
