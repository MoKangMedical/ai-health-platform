"""
AI Health Platform - Core Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Health Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_health.db"
    
    # JWT
    SECRET_KEY: str = "ai-health-platform-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Sub-services
    VOICE_HEALTH_URL: str = "http://localhost:8100"
    KNOW_HEALTH_URL: str = "http://localhost:8080"
    MEDI_CHAT_RD_URL: str = "http://localhost:8090"
    
    # Subscription Plans
    FREE_PLAN_LIMIT: int = 5
    BASIC_PLAN_LIMIT: int = 50
    PREMIUM_PLAN_LIMIT: int = 500

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
