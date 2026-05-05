from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


def list_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def update_stock(db: Session, product_id: int, delta: int) -> Product:
    """
    Atomically adjust stock by `delta`. Negative deducts, positive adds.

    NOTE: For real workloads, replace the read-modify-write below with a
    conditional UPDATE (e.g. `UPDATE products SET stock = stock + :d
    WHERE id = :id AND stock + :d >= 0 RETURNING *`) so two concurrent
    deductions cannot both succeed against the same row.
    """
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .with_for_update()
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    new_stock = product.stock + delta
    if new_stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock",
        )

    product.stock = new_stock
    db.commit()
    db.refresh(product)
    return product
