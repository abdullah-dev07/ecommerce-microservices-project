from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


async def create_user(payload: UserCreate) -> User:
    if await User.filter(email=payload.email).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return await User.create(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )


async def get_user(user_id: int) -> User:
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def list_users() -> list[User]:
    return await User.all()
