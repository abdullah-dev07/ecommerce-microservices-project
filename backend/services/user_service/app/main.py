from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.api.routes import health, users
from app.core.tortoise import TORTOISE_ORM


@asynccontextmanager
async def lifespan(_: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)
    try:
        yield
    finally:
        await Tortoise.close_connections()


app = FastAPI(title="User Service", version="1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
