"""
千川AI投放工具 - FastAPI主入口 (本地版：后端直接托管前端静态文件)
"""
import logging
import sys
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.api.routes import router
from app.api.uni_routes import uni_router
from app.api.sxt_routes import sxt_router

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/qianchuan_ai.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("=" * 50)
    logger.info("千川AI投放工具启动")
    logger.info(f"版本: {get_settings().app_version}")
    logger.info("=" * 50)
    yield
    logger.info("千川AI投放工具关闭")


# 创建FastAPI应用
app = FastAPI(
    title="千川AI投放工具",
    description="基于巨量千川开放平台的AI智能投放管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(router, prefix="/api/v1")
app.include_router(uni_router, prefix="/api/v1")
app.include_router(sxt_router, prefix="/api/v1")

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "千川AI投放工具",
        "version": "1.0.0"
    }


# 本地模式：尝试挂载前端静态文件
_frontend_paths = [
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend"),
    os.path.join(os.path.dirname(__file__), "..", "frontend"),
    os.path.join(os.getcwd(), "frontend"),
]
_frontend_dir = None
for p in _frontend_paths:
    if os.path.exists(p) and os.path.exists(os.path.join(p, "index.html")):
        _frontend_dir = p
        break

if _frontend_dir:
    logger.info(f"本地模式: 托管前端静态文件 => {_frontend_dir}")
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="static")
    logger.info("访问 http://localhost:8000 即可打开前端页面")
else:
    @app.get("/")
    async def root():
        """根路径"""
        return {
            "name": "千川AI投放工具",
            "version": "1.0.0",
            "docs": "/docs",
            "api_prefix": "/api/v1"
        }


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
