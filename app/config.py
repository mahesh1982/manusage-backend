from datetime import datetime
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "dev"
    version: str = "0.0.1"
    build_time: str = datetime.utcnow().isoformat()

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    APP_ENV: str
    APP_VERSION: str

    EMBEDDING_MODEL: str
    DEFAULT_PROMPT_NAME: str

    OPENAI_API_KEY: Optional[str] = None
    MONGO_URI: str

    PG_DSN: str

    class Config:
        env_file = ".env"

settings = Settings()
