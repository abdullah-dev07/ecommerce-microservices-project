"""Logging setup shared by every service.

Each log line carries:
  - the service name (so interleaved `docker compose logs` is readable)
  - the current request id (so a single request can be traced across services)

The request id lives in a `contextvars.ContextVar` so it survives across
async boundaries (httpx hooks, tortoise queries, etc.) without us having to
pass it explicitly through every function.
"""
from __future__ import annotations

import contextvars
import logging
import sys

from app.core.config import settings

_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


def set_request_id(value: str) -> None:
    _request_id_var.set(value)


def get_request_id() -> str:
    return _request_id_var.get()


class _RequestIdFilter(logging.Filter):
    """Injects the current request id into every log record so the formatter
    string can reference `%(request_id)s`."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id_var.get()
        return True


def setup_logging() -> None:
    name_pad = settings.SERVICE_NAME.ljust(15)
    fmt = (
        f"[{name_pad}] %(asctime)s %(levelname)-7s "
        "[req=%(request_id)s] %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt, datefmt="%H:%M:%S"))
    handler.addFilter(_RequestIdFilter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)

    # Uvicorn's default access log doesn't carry the request id and would
    # double up with our middleware's inbound log line. Disable it; our
    # middleware logs the same info plus the request id.
    logging.getLogger("uvicorn.access").disabled = True
