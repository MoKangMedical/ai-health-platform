"""集成测试"""

import pytest
import json
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

class TestCompleteWorkflow:
    """完整工作流程测试"""
    
    def test_full_detection_workflow(self):
        """测试完整检测流程"""
        # 1. 注册用户
        response = client.post("/api/v1/users/register", data={
            "openid": "integration_test_user",
            "nickname": "集成测试用户"
        })
        assert response.status_code == 200
        user_data = response.json()
        user_id = user_data["user_id"]
        
        # 2. 更新用户档案
        response = client.put(f"/api/v1/users/{user_id}/profile", data={
            "nickname": "更新后的用户",
            "height": "175",
            "weight": "70"
        })
        assert response.status_code == 200
        
        # 3. 获取用户档案
        response = client.get(f"/api/v1/users/{user_id}/profile")
        assert response.status_code == 200
        profile = response.json()
        assert profile["nickname"] == "更新后的用户"
        
        # 4. 获取检测历史
        response = client.get(f"/api/v1/detect/history/{user_id}")
        assert response.status_code == 200
        
        # 5. 获取配方列表
        response = client.get(f"/api/v1/formula/user/{user_id}")
        assert response.status_code == 200
        
        # 6. 获取订单列表
        response = client.get(f"/api/v1/orders/{user_id}")
        assert response.status_code == 200
    
    def test_agent_conversation_flow(self):
        """测试Agent对话流程"""
        # 1. 问候
        response = client.post("/api/v1/agent/chat", data={
            "user_id": 1,
            "message": "你好",
            "agent_type": "coordinator"
        })
        assert response.status_code == 200
        assert "小和" in response.json()["response"]
        
        # 2. 健康咨询
        response = client.post("/api/v1/agent/chat", data={
            "user_id": 1,
            "message": "我最近总是疲劳，怎么办？",
            "agent_type": "coordinator"
        })
        assert response.status_code == 200
        
        # 3. 营养咨询
        response = client.post("/api/v1/agent/chat", data={
            "user_id": 1,
            "message": "我想提升免疫力",
            "agent_type": "advisor"
        })
        assert response.status_code == 200
        assert "维生素" in response.json()["response"]
        
        # 4. 医学术语查询
        response = client.post("/api/v1/agent/chat", data={
            "user_id": 1,
            "message": "ALT是什么意思",
            "agent_type": "translator"
        })
        assert response.status_code == 200
        assert "谷丙转氨酶" in response.json()["response"]
        
        # 5. 获取对话历史
        response = client.get("/api/v1/agent/history/1")
        assert response.status_code == 200
        history = response.json()
        assert len(history["history"]) > 0

class TestErrorHandling:
    """错误处理测试"""
    
    def test_user_not_found(self):
        """测试用户不存在"""
        response = client.get("/api/v1/users/99999/profile")
        assert response.status_code == 404
    
    def test_formula_not_found(self):
        """测试配方不存在"""
        response = client.get("/api/v1/formula/99999")
        assert response.status_code == 404
    
    def test_invalid_agent_type(self):
        """测试无效的Agent类型"""
        response = client.post("/api/v1/agent/chat", data={
            "user_id": 1,
            "message": "测试",
            "agent_type": "invalid_agent"
        })
        # 应该回退到协调员
        assert response.status_code == 200

class TestSystemEndpoints:
    """系统端点测试"""
    
    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_system_info(self):
        """测试系统信息"""
        response = client.get("/api/v1/system/info")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data["system"]
        assert len(data["system"]["agents"]) == 4
    
    def test_api_info(self):
        """测试API信息"""
        response = client.get("/api")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
    
    def test_landing_page(self):
        """测试首页"""
        response = client.get("/")
        assert response.status_code == 200
        assert "AI健康平台" in response.text
    
    def test_console_page(self):
        """测试控制台"""
        response = client.get("/console")
        assert response.status_code == 200
    
    def test_docs_page(self):
        """测试API文档"""
        response = client.get("/docs")
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
