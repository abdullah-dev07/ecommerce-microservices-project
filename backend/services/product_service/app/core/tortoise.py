"""Central Tortoise ORM config for product_service. See user_service for details."""
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
