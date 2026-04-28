"""AI健康平台 - 主应用"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from contextlib import asynccontextmanager
import time

from src.api.routes import router
from src.models.database import init_db
from config.settings import settings

# 模板引擎
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期"""
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} 启动成功")
    print(f"📊 API文档: http://localhost:{settings.PORT}/docs")
    print(f"🏠 首页: http://localhost:{settings.PORT}")
    print(f"💻 控制台: http://localhost:{settings.PORT}/console")
    yield
    print(f"👋 {settings.APP_NAME} 关闭")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于多模态AI检测的个性化健康管理平台",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求计时中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册API路由
app.include_router(router)

# ==================== 页面路由 ====================

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """首页 - 产品展示"""
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/console", response_class=HTMLResponse)
async def console_page(request: Request):
    """控制台 - 用户操作界面"""
    return templates.TemplateResponse("console.html", {"request": request})

@app.get("/health-report/{record_id}", response_class=HTMLResponse)
async def health_report_page(request: Request, record_id: int):
    """健康报告页面"""
    return templates.TemplateResponse("health_report.html", {
        "request": request,
        "record_id": record_id
    })

@app.get("/formula/{formula_id}", response_class=HTMLResponse)
async def formula_page(request: Request, formula_id: int):
    """配方详情页面"""
    return templates.TemplateResponse("formula.html", {
        "request": request,
        "formula_id": formula_id
    })

# ==================== API路由 ====================

@app.get("/api")
async def api_info():
    """API信息"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "detect": "/api/v1/detect/*",
            "formula": "/api/v1/formula/*",
            "agent": "/api/v1/agent/*",
            "users": "/api/v1/users/*",
            "orders": "/api/v1/orders/*"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
