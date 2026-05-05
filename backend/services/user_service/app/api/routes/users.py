from fastapi import APIRouter, status

from app.schemas.user import UserCreate, UserOut
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate) -> UserOut:
    return await user_service.create_user(payload)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int) -> UserOut:
    return await user_service.get_user(user_id)


@router.get("", response_model=list[UserOut])
async def list_users() -> list[UserOut]:
    return await user_service.list_users()
