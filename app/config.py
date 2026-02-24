from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "dev"

    class Config:
        env_file = ".env"
