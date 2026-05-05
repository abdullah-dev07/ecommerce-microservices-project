from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.api.routes import health, orders
from app.core import http_client
from app.core.tortoise import TORTOISE_ORM


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

app.include_router(health.router)
app.include_router(orders.router)
