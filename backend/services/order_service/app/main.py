from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.api.routes import health, orders
from app.core import http_client
from app.core.logging import setup_logging
from app.core.middleware import RequestIdMiddleware
from app.core.tortoise import TORTOISE_ORM

setup_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    await http_client.startup()
    try:
        yield
    finally:
        await http_client.shutdown()
        await Tortoise.close_connections()


app = FastAPI(title="Order Service", version="1.0", lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)

app.include_router(health.router)
app.include_router(orders.router)
