from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "user_service"
    PORT: int = 8001

    # Tortoise accepts `postgres://` or `asyncpg://`. We use `postgres://`.
    DATABASE_URL: str = "postgres://postgres:password@localhost:5433/user_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
