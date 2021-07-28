from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = True
    REDIS_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
