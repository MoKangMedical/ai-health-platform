"""测试用例"""

import pytest
import json
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# ==================== 健康检查测试 ====================
class TestHealthCheck:
    def test_health_endpoint(self):
        """测试健康检查端点"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_root_endpoint(self):
        """测试首页"""
        response = client.get("/")
        assert response.status_code == 200
        assert "AI健康平台" in response.text

    def test_system_info(self):
        """测试系统信息"""
        response = client.get("/api/v1/system/info")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "agents" in data["system"]

# ==================== 用户管理测试 ====================
class TestUserManagement:
    def test_register_user(self):
        """测试用户注册"""
        response = client.post(
            "/api/v1/users/register",
            data={"openid": "test_user_001", "nickname": "测试用户"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "user_id" in data

    def test_get_user_profile(self):
        """测试获取用户档案"""
        # 先注册
        client.post(
            "/api/v1/users/register",
            data={"openid": "test_user_002", "nickname": "测试用户2"}
        )
        
        # 获取档案
        response = client.get("/api/v1/users/2/profile")
        assert response.status_code == 200
        data = response.json()
        assert data["nickname"] == "测试用户2"

    def test_update_user_profile(self):
        """测试更新用户档案"""
        response = client.put(
            "/api/v1/users/1/profile",
            data={
                "nickname": "更新后的用户",
                "height": "175.5",
                "weight": "70.0"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

# ==================== 健康检测测试 ====================
class TestHealthDetection:
    def test_voice_detection_without_file(self):
        """测试语音检测（无文件）"""
        response = client.post(
            "/api/v1/detect/voice",
            data={"user_id": 1}
        )
        assert response.status_code == 422  # 缺少必需文件

    def test_detection_history(self):
        """测试检测历史"""
        response = client.get("/api/v1/detect/history/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "records" in data

# ==================== 营养配方测试 ====================
class TestNutrientFormula:
    def test_get_user_formulas(self):
        """测试获取用户配方"""
        response = client.get("/api/v1/formula/user/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "formulas" in data

    def test_get_formula_not_found(self):
        """测试获取不存在的配方"""
        response = client.get("/api/v1/formula/999")
        assert response.status_code == 404

# ==================== AI助手测试 ====================
class TestAIAgent:
    def test_get_agent_info(self):
        """测试获取Agent信息"""
        response = client.get("/api/v1/agent/info")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["agents"]) == 4

    def test_chat_with_coordinator(self):
        """测试与协调员对话"""
        response = client.post(
            "/api/v1/agent/chat",
            data={
                "user_id": 1,
                "message": "你好",
                "agent_type": "coordinator"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["agent"] == "coordinator"
        assert "response" in data

    def test_chat_with_translator(self):
        """测试与翻译Agent对话"""
        response = client.post(
            "/api/v1/agent/chat",
            data={
                "user_id": 1,
                "message": "ALT是什么意思",
                "agent_type": "translator"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "谷丙转氨酶" in data["response"]

    def test_chat_with_advisor(self):
        """测试与顾问Agent对话"""
        response = client.post(
            "/api/v1/agent/chat",
            data={
                "user_id": 1,
                "message": "我想提升免疫力",
                "agent_type": "advisor"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "维生素" in data["response"]

    def test_chat_history(self):
        """测试对话历史"""
        response = client.get("/api/v1/agent/history/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "history" in data

# ==================== 订单测试 ====================
class TestOrders:
    def test_get_user_orders(self):
        """测试获取用户订单"""
        response = client.get("/api/v1/orders/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "orders" in data

# ==================== 运行测试 ====================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
