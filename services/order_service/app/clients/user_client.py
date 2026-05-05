"""Outbound HTTP calls to the User Service."""
from __future__ import annotations

import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.http_client import get_client


async def verify_user(user_id: int) -> dict:
    """Confirm a user exists. Raises an HTTP error otherwise."""
    client = get_client()
    try:
        r = await client.get(f"{settings.USER_SERVICE_URL}/users/{user_id}")
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User Service unavailable",
        )
    if r.status_code == 404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    r.raise_for_status()
    return r.json()
