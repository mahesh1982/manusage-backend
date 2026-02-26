from datetime import datetime
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "dev"
    version: str = "0.0.1"
    build_time: str = datetime.utcnow().isoformat()

    class Config:
        env_file = ".env"
