from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, orders
from app.core import http_client
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    await http_client.startup()
    try:
        yield
    finally:
        await http_client.shutdown()


app = FastAPI(title="Order Service", version="1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(orders.router)
