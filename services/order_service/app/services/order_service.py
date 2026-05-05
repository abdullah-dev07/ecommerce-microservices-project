"""Order business logic. No FastAPI imports beyond HTTPException for errors."""
from __future__ import annotations

import logging

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.clients import product_client, user_client
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate

logger = logging.getLogger(__name__)


async def create_order(db: Session, payload: OrderCreate) -> Order:
    """
    Create an order across User + Product services.

    Steps:
      1. Verify the user exists.
      2. For each item: fetch product details and check stock.
      3. Deduct stock for each item, tracking what we deducted so we can
         compensate (restore) on later failure.
      4. Persist the order. If persistence fails, restore all deducted stock.

    NOTE: This is a simplified Saga. For production, prefer an event-driven
    flow with an outbox table so the local DB write and the events are atomic.
    """
    await user_client.verify_user(payload.user_id)

    line_items: list[dict] = []
    total = 0.0
    for item in payload.items:
        product = await product_client.fetch_product(item.product_id)
        if product["stock"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product '{product['name']}'",
            )
        line_total = product["price"] * item.quantity
        total += line_total
        line_items.append(
            {
                "product_id": item.product_id,
                "name": product["name"],
                "quantity": item.quantity,
                "unit_price": product["price"],
                "line_total": round(line_total, 2),
            }
        )

    deducted: list[tuple[int, int]] = []
    try:
        for item in payload.items:
            await product_client.adjust_stock(item.product_id, -item.quantity)
            deducted.append((item.product_id, item.quantity))

        order = Order(
            user_id=payload.user_id,
            items=line_items,
            total=round(total, 2),
            status=OrderStatus.CONFIRMED,
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        return order
    except Exception:
        await _restore_stock(deducted)
        raise


async def _restore_stock(deducted: list[tuple[int, int]]) -> None:
    """Best-effort compensation. Logs but does not raise on failure."""
    for product_id, qty in deducted:
        try:
            await product_client.adjust_stock(product_id, qty)
        except Exception:
            logger.exception(
                "Failed to restore %s units of product %s during rollback",
                qty,
                product_id,
            )


def get_order(db: Session, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order


def list_user_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


async def cancel_order(db: Session, order_id: int) -> Order:
    order = get_order(db, order_id)
    if order.status == OrderStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already cancelled",
        )

    for item in order.items:
        try:
            await product_client.adjust_stock(item["product_id"], item["quantity"])
        except Exception:
            logger.exception(
                "Failed to restore stock for product %s on order %s cancel",
                item["product_id"],
                order_id,
            )

    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order
