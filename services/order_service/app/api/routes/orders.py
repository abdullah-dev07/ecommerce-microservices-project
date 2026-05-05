from fastapi import APIRouter, status

from app.schemas.order import OrderCreate, OrderOut
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate) -> OrderOut:
    return await order_service.create_order(payload)


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: int) -> OrderOut:
    return await order_service.get_order(order_id)


@router.get("/user/{user_id}", response_model=list[OrderOut])
async def list_user_orders(user_id: int) -> list[OrderOut]:
    return await order_service.list_user_orders(user_id)


@router.patch("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(order_id: int) -> OrderOut:
    return await order_service.cancel_order(order_id)
