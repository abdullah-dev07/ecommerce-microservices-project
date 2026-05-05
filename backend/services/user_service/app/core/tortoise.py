"""
Central Tortoise ORM config for user_service.

This dict is consumed by:
  - `Tortoise.init(config=TORTOISE_ORM)` in `app/main.py` (runtime)
  - Aerich (via `pyproject.toml -> tool.aerich.tortoise_orm`) to generate and
    apply migrations.

`aerich.models` MUST be included — Aerich stores its migration history in a
table called `aerich` and needs its model registered.
"""
from app.core.config import settings

TORTOISE_ORM: dict = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "UTC",
}
