from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "order_service"
    PORT: int = 8003

    DATABASE_URL: str = "postgresql://postgres:password@localhost:5435/order_db"

    USER_SERVICE_URL: str = "http://localhost:8001"
    PRODUCT_SERVICE_URL: str = "http://localhost:8002"

    REQUEST_TIMEOUT: float = 5.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
