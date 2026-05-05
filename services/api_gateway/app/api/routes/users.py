from fastapi import APIRouter, status

from app.core.config import settings
from app.core.http_client import proxy
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate) -> dict:
    return await proxy(
        "POST",
        f"{settings.USER_SERVICE_URL}/users",
        json=payload.model_dump(),
    )


@router.get("/{user_id}")
async def get_user(user_id: int) -> dict:
    return await proxy("GET", f"{settings.USER_SERVICE_URL}/users/{user_id}")


@router.get("")
async def list_users() -> list[dict]:
    return await proxy("GET", f"{settings.USER_SERVICE_URL}/users")
