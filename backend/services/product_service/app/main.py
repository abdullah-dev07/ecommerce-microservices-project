from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.api.routes import health, products
from app.core.logging import setup_logging
from app.core.middleware import RequestIdMiddleware
from app.core.tortoise import TORTOISE_ORM

setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    try:
        yield
    finally:
        await Tortoise.close_connections()


app = FastAPI(title="Product Service", version="1.0", lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)

app.include_router(health.router)
app.include_router(products.router)
