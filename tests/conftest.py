"""测试配置"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.models.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """初始化测试数据库"""
    init_db()
    yield

@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)

@pytest.fixture
def sample_user():
    """测试用户数据"""
    return {
        "openid": "test_user_001",
        "nickname": "测试用户",
        "phone": "13800138000"
    }

@pytest.fixture
def sample_questionnaire():
    """测试问卷数据"""
    return {
        "allergies": [],
        "health_goals": ["提升免疫力", "改善睡眠"],
        "current_medications": [],
        "dietary_restrictions": [],
        "lifestyle": {
            "exercise_frequency": "每周3-4次",
            "sleep_hours": 7,
            "stress_level": "中等"
        }
    }
