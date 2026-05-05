from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str = "product_service"
    PORT: int = 8002

    DATABASE_URL: str = "postgres://postgres:password@localhost:5434/product_db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
