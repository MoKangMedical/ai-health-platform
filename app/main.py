"""
AI Health Platform - Main Application
Unified backend integrating VoiceHealth + KnowHealth + MediChat-RD
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from .core.config import settings
from .core.database import engine, Base
from .api.v1 import auth, health, subscription

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting AI Health Platform...")
    logger.info(f"📦 Version: {settings.APP_VERSION}")
    logger.info(f"🌐 Server: {settings.HOST}:{settings.PORT}")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database initialized")
    
    # Log sub-services configuration
    logger.info(f"🔗 VoiceHealth: {settings.VOICE_HEALTH_URL}")
    logger.info(f"🔗 KnowHealth: {settings.KNOW_HEALTH_URL}")
    logger.info(f"🔗 MediChat-RD: {settings.MEDI_CHAT_RD_URL}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down AI Health Platform...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    # AI Health Platform - 统一健康管理平台
    
    整合三大AI健康服务，提供完整的健康管理解决方案：
    
    ## 核心服务
    - 🎤 **VoiceHealth** - 多模态健康检测（语音/图像/传感器）
    - 🧠 **KnowHealth** - AI健康助手与知识问答
    - 💊 **MediChat-RD** - 医学知识图谱与智能诊断
    
    ## 商业闭环
    1. **检测** (Detection) - 多维度健康数据采集
    2. **分析** (Analysis) - AI驱动的健康分析
    3. **干预** (Intervention) - 个性化干预方案
    4. **追踪** (Tracking) - 持续健康监测
    
    ## 订阅模式
    - 免费版：5次/月API调用
    - 基础版：¥99/月，50次API调用
    - 高级版：¥299/月，500次API调用
    - 企业版：¥999/月，无限API调用
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint - Platform status"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "voice_health": settings.VOICE_HEALTH_URL,
            "know_health": settings.KNOW_HEALTH_URL,
            "medi_chat_rd": settings.MEDI_CHAT_RD_URL
        },
        "endpoints": {
            "docs": "/docs",
            "health_api": "/api/v1/health",
            "auth": "/api/v1/auth",
            "subscription": "/api/v1/subscription"
        }
    }


@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "database": "connected"
    }


# Include API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")
app.include_router(subscription.router, prefix="/api/v1")


# API Info endpoint
@app.get("/api/v1", tags=["System"])
async def api_info():
    """API v1 information"""
    return {
        "version": "v1",
        "endpoints": {
            "auth": {
                "register": "POST /api/v1/auth/register",
                "login": "POST /api/v1/auth/login",
                "profile": "GET /api/v1/auth/me"
            },
            "health": {
                "voice_detection": "POST /api/v1/health/detect/voice",
                "knowledge_analysis": "POST /api/v1/health/analyze/knowledge",
                "diagnosis": "POST /api/v1/health/diagnose",
                "ai_chat": "POST /api/v1/health/chat",
                "business_loop": "POST /api/v1/health/business-loop",
                "records": "GET /api/v1/health/records",
                "dashboard": "GET /api/v1/health/dashboard",
                "intervention": "POST /api/v1/health/intervention"
            },
            "subscription": {
                "create": "POST /api/v1/subscription/create",
                "current": "GET /api/v1/subscription/current",
                "plans": "GET /api/v1/subscription/plans",
                "history": "GET /api/v1/subscription/history"
            }
        }
    }
