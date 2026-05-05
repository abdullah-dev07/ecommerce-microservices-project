from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, orders, products, users
from app.core import http_client
from app.core.config import settings


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

# Browsers send a CORS preflight OPTIONS request for any non-simple request
# (e.g. POST with JSON body). Without this middleware FastAPI returns 405.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
