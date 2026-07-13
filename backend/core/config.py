from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True
    APP_NAME: str = "Influencer Finder"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
