from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import health, products
from app.db.session import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="Product Service", version="1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(products.router)
