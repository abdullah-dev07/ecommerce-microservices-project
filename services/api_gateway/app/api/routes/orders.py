from fastapi import APIRouter, status

from app.core.config import settings
from app.core.http_client import proxy
from app.schemas.order import OrderCreate

router = APIRouter(tags=["orders"])


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate) -> dict:
    return await proxy(
        "POST",
        f"{settings.ORDER_SERVICE_URL}/orders",
        json=payload.model_dump(),
    )


@router.get("/orders/{order_id}")
async def get_order(order_id: int) -> dict:
    return await proxy("GET", f"{settings.ORDER_SERVICE_URL}/orders/{order_id}")


@router.get("/users/{user_id}/orders")
async def list_user_orders(user_id: int) -> list[dict]:
    return await proxy(
        "GET", f"{settings.ORDER_SERVICE_URL}/orders/user/{user_id}"
    )


@router.patch("/orders/{order_id}/cancel")
async def cancel_order(order_id: int) -> dict:
    return await proxy(
        "PATCH", f"{settings.ORDER_SERVICE_URL}/orders/{order_id}/cancel"
    )


@router.get("/orders/{order_id}/detail")
async def order_detail(order_id: int) -> dict:
    """
    Aggregate Order + User in a single response.

    Order must be fetched first because we need its `user_id` before we can
    fetch the customer. The two calls cannot be parallelised.
    """
    order = await proxy(
        "GET", f"{settings.ORDER_SERVICE_URL}/orders/{order_id}"
    )
    user = await proxy(
        "GET", f"{settings.USER_SERVICE_URL}/users/{order['user_id']}"
    )
    return {
        "order": order,
        "customer": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    }
