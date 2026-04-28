"""AI健康平台配置"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """应用配置"""
    
    # 基础配置
    APP_NAME: str = "AI Health Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8200
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./ai_health.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT配置
    SECRET_KEY: str = "ai-health-secret-key-2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI模型配置
    VOICE_MODEL_PATH: str = "models/voice_model.pth"
    FACE_MODEL_PATH: str = "models/face_model.pth"
    KNOWLEDGE_GRAPH_PATH: str = "data/knowledge_graph.json"
    
    # 外部服务配置
    VOICE_HEALTH_API: str = "http://localhost:8100"
    MEDICHAT_API: str = "http://localhost:8300"
    KNOWHEALTH_API: str = "http://localhost:8080"
    
    # 营养品配置
    INGREDIENT_DB_PATH: str = "data/ingredients.json"
    MAX_FORMULA_INGREDIENTS: int = 15
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量

settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
