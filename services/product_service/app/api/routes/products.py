from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.product import ProductCreate, ProductOut, StockUpdate
from app.services import product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductOut:
    return product_service.create_product(db, payload)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductOut:
    return product_service.get_product(db, product_id)


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[ProductOut]:
    return product_service.list_products(db)


@router.patch("/{product_id}/stock", response_model=ProductOut)
def update_stock(
    product_id: int,
    payload: StockUpdate,
    db: Session = Depends(get_db),
) -> ProductOut:
    """Called internally by Order Service to deduct or restore stock."""
    return product_service.update_stock(db, product_id, payload.quantity)
