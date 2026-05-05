"""Shared httpx.AsyncClient managed by the FastAPI lifespan."""
from __future__ import annotations

import httpx
from fastapi import HTTPException, status

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
