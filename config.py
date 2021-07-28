from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    REDIS_URL: str = "redis://localhost:6379/0?encoding=utf-8"

    class Config:
        case_sensitive = True


settings = Settings()
