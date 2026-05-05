from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, orders, products, users
from app.core import http_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    await http_client.startup()
    try:
        yield
    finally:
        await http_client.shutdown()


app = FastAPI(
    title="API Gateway",
    version="1.0",
    description="Single entry point for the e-commerce platform",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
