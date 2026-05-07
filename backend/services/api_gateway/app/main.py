from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, orders, products, users
from app.core import http_client
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import RequestIdMiddleware

setup_logging()


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

# Middleware order: the FIRST `add_middleware` call becomes the OUTERMOST
# layer, so RequestId runs before CORS — this lets us tag and log every
# request (including CORS preflight OPTIONS, which CORS short-circuits).
app.add_middleware(RequestIdMiddleware)

# Browsers send a CORS preflight OPTIONS request for any non-simple request
# (e.g. POST with JSON body). Without this middleware FastAPI returns 405.
# `expose_headers` lets the browser read X-Request-ID on responses, which is
# handy if the frontend ever wants to surface a trace id in error toasts.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
