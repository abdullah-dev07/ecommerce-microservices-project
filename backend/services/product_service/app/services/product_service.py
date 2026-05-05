from fastapi import HTTPException, status
from tortoise.transactions import in_transaction

from app.models.product import Product
from app.schemas.product import ProductCreate


async def create_product(payload: ProductCreate) -> Product:
    return await Product.create(**payload.model_dump())


async def get_product(product_id: int) -> Product:
    product = await Product.get_or_none(id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


async def list_products() -> list[Product]:
    return await Product.all()


async def update_stock(product_id: int, delta: int) -> Product:
    """
    Atomically adjust stock by `delta`. Negative deducts, positive restores.

    Uses `select_for_update` inside a transaction so two concurrent deductions
    cannot both succeed against the same row.
    """
    async with in_transaction() as conn:
        product = (
            await Product.select_for_update()
            .using_db(conn)
            .get_or_none(id=product_id)
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
        await product.save(using_db=conn)
        return product
