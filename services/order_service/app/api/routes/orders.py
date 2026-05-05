from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.order import OrderCreate, OrderOut
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderOut:
    return await order_service.create_order(db, payload)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderOut:
    return order_service.get_order(db, order_id)


@router.get("/user/{user_id}", response_model=list[OrderOut])
def list_user_orders(user_id: int, db: Session = Depends(get_db)) -> list[OrderOut]:
    return order_service.list_user_orders(db, user_id)


@router.patch("/{order_id}/cancel", response_model=OrderOut)
async def cancel_order(order_id: int, db: Session = Depends(get_db)) -> OrderOut:
    return await order_service.cancel_order(db, order_id)
