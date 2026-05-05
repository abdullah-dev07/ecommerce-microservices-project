"""Outbound HTTP calls to the Product Service."""
from __future__ import annotations

import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.http_client import get_client


async def fetch_product(product_id: int) -> dict:
    client = get_client()
    try:
        r = await client.get(f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}")
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product Service unavailable",
        )
    if r.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )
    r.raise_for_status()
    return r.json()


async def adjust_stock(product_id: int, delta: int) -> None:
    """Add or subtract `delta` from a product's stock."""
    client = get_client()
    try:
        r = await client.patch(
            f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            json={"quantity": delta},
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Product Service unavailable",
        )
    if r.status_code == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=r.json().get("detail", "Stock error"),
        )
    r.raise_for_status()
