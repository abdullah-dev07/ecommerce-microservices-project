from fastapi import APIRouter, status

from app.schemas.product import ProductCreate, ProductOut, StockUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate) -> ProductOut:
    return await product_service.create_product(payload)


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: int) -> ProductOut:
    return await product_service.get_product(product_id)


@router.get("", response_model=list[ProductOut])
async def list_products() -> list[ProductOut]:
    return await product_service.list_products()


@router.patch("/{product_id}/stock", response_model=ProductOut)
async def update_stock(product_id: int, payload: StockUpdate) -> ProductOut:
    """Called internally by Order Service to deduct or restore stock."""
    return await product_service.update_stock(product_id, payload.quantity)
