from fastapi import APIRouter, status

from app.core.config import settings
from app.core.http_client import proxy
from app.schemas.product import ProductCreate

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate) -> dict:
    return await proxy(
        "POST",
        f"{settings.PRODUCT_SERVICE_URL}/products",
        json=payload.model_dump(),
    )


@router.get("/{product_id}")
async def get_product(product_id: int) -> dict:
    return await proxy("GET", f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}")


@router.get("")
async def list_products() -> list[dict]:
    return await proxy("GET", f"{settings.PRODUCT_SERVICE_URL}/products")
