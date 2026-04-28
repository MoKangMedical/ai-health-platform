"""日志和错误处理模块"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import json
import traceback

# 创建日志目录
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置日志格式
class CustomFormatter(logging.Formatter):
    """自定义日志格式"""
    
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler(
        log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)
    
    return logger

# 全局日志记录器
logger = setup_logger("ai-health")


class AppError(Exception):
    """应用基础异常"""
    
    def __init__(self, message: str, code: str = "UNKNOWN", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppError):
    """资源未找到"""
    
    def __init__(self, resource: str, id: any):
        super().__init__(
            message=f"{resource}不存在: {id}",
            code="NOT_FOUND",
            status_code=404
        )

class ValidationError(AppError):
    """验证错误"""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422
        )

class AuthenticationError(AppError):
    """认证错误"""
    
    def __init__(self, message: str = "未授权"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401
        )

class DatabaseError(AppError):
    """数据库错误"""
    
    def __init__(self, message: str):
        super().__init__(
            message=f"数据库错误: {message}",
            code="DATABASE_ERROR",
            status_code=500
        )


def log_error(error: Exception, context: Optional[Dict] = None):
    """记录错误日志"""
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "traceback": traceback.format_exc(),
        "context": context or {},
        "timestamp": datetime.now().isoformat()
    }
    
    logger.error(json.dumps(error_info, ensure_ascii=False, indent=2))

def log_api_call(method: str, path: str, status_code: int, duration: float):
    """记录API调用"""
    logger.info(f"{method} {path} - {status_code} ({duration:.3f}s)")

def log_user_action(user_id: int, action: str, details: Optional[Dict] = None):
    """记录用户行为"""
    action_info = {
        "user_id": user_id,
        "action": action,
        "details": details or {},
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"User Action: {json.dumps(action_info, ensure_ascii=False)}")


def handle_error(error: Exception) -> Dict:
    """统一错误处理"""
    if isinstance(error, AppError):
        return {
            "status": "error",
            "code": error.code,
            "message": error.message
        }
    
    log_error(error)
    
    return {
        "status": "error",
        "code": "INTERNAL_ERROR",
        "message": "服务器内部错误"
    }
