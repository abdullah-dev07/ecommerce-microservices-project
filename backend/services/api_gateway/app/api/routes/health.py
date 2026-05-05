import asyncio

import httpx
from fastapi import APIRouter

from app.core.config import settings
from app.core.http_client import get_client

router = APIRouter(tags=["health"])


_DOWNSTREAMS = [
    ("user_service", lambda: settings.USER_SERVICE_URL),
    ("product_service", lambda: settings.PRODUCT_SERVICE_URL),
    ("order_service", lambda: settings.ORDER_SERVICE_URL),
]


async def _check(name: str, base_url: str) -> tuple[str, str]:
    client = get_client()
    try:
        r = await client.get(f"{base_url}/health", timeout=settings.HEALTH_TIMEOUT)
        return name, r.json().get("status", "unknown")
    except (httpx.RequestError, ValueError):
        return name, "unreachable"


@router.get("/health")
async def health() -> dict:
    results = await asyncio.gather(
        *(_check(name, get_url()) for name, get_url in _DOWNSTREAMS)
    )
    services = dict(results)
    overall_ok = all(v == "ok" for v in services.values())
    return {
        "gateway": "ok",
        "overall": "ok" if overall_ok else "degraded",
        "services": services,
    }
