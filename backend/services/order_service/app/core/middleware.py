"""HTTP middleware that:
  - generates an `X-Request-ID` (or honors one supplied by an upstream caller)
  - stores it in a contextvar so all logs from this request include it
  - logs the inbound request and response with timing
  - echoes the request id on the response header so callers can correlate

When two services talk via httpx, the outbound client adds the same header,
which means the same request id flows through every service that handles
the request.
"""
from __future__ import annotations

import logging
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import set_request_id

logger = logging.getLogger("app.http")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:8]
        set_request_id(request_id)

        start = time.perf_counter()
        path = request.url.path
        logger.info(">> %-6s %s", request.method, path)

        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "!! %-6s %s (%.0fms)", request.method, path, elapsed_ms
            )
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "<< %-3d %-6s %s (%.0fms)",
            response.status_code,
            request.method,
            path,
            elapsed_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
