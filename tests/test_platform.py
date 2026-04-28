#!/usr/bin/env python3
"""
AI Health Platform - Test Script
验证平台核心功能
"""
import httpx
import asyncio
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


async def test_platform():
    """Test the AI Health Platform"""
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        print("=" * 60)
        print("🏥 AI Health Platform - 功能测试")
        print("=" * 60)
        
        # 1. Health check
        print("\n1️⃣  系统健康检查...")
        try:
            resp = await client.get("/health")
            print(f"   ✅ 状态: {resp.json()['status']}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return
        
        # 2. Register user
        print("\n2️⃣  用户注册...")
        register_data = {
            "email": f"test_{datetime.now().strftime('%H%M%S')}@example.com",
            "username": f"testuser_{datetime.now().strftime('%H%M%S')}",
            "password": "Test123456",
            "full_name": "测试用户",
            "age": 30,
            "gender": "male"
        }
        try:
            resp = await client.post("/api/v1/auth/register", json=register_data)
            if resp.status_code == 200:
                user_data = resp.json()
                print(f"   ✅ 注册成功: {user_data['username']}")
                print(f"   📧 邮箱: {user_data['email']}")
                print(f"   🎫 剩余API调用: {user_data['api_calls_remaining']}")
            else:
                print(f"   ⚠️  响应: {resp.json()}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 3. Login
        print("\n3️⃣  用户登录...")
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }
        try:
            resp = await client.post("/api/v1/auth/login", json=login_data)
            if resp.status_code == 200:
                token = resp.json()["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                print(f"   ✅ 登录成功")
                print(f"   🔑 Token: {token[:20]}...")
            else:
                print(f"   ❌ 登录失败: {resp.json()}")
                return
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            return
        
        # 4. Get user profile
        print("\n4️⃣  获取用户信息...")
        try:
            resp = await client.get("/api/v1/auth/me", headers=headers)
            if resp.status_code == 200:
                print(f"   ✅ 用户: {resp.json()['username']}")
                print(f"   📊 订阅: {resp.json()['subscription_plan']}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 5. Voice detection
        print("\n5️⃣  语音健康检测...")
        detect_data = {
            "detection_type": "general",
            "audio_base64": "mock_audio_data"
        }
        try:
            resp = await client.post(
                "/api/v1/health/detect/voice",
                json=detect_data,
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ 检测完成")
                print(f"   📊 风险评分: {result.get('risk_score', 'N/A')}")
                print(f"   💡 建议: {result.get('recommendations', ['N/A'])[0] if result.get('recommendations') else 'N/A'}")
            else:
                print(f"   ⚠️  响应: {resp.status_code}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 6. Knowledge analysis
        print("\n6️⃣  知识分析...")
        knowledge_data = {
            "query": "如何预防感冒？",
            "language": "zh"
        }
        try:
            resp = await client.post(
                "/api/v1/health/analyze/knowledge",
                json=knowledge_data,
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ 分析完成")
                print(f"   📝 答案: {result.get('answer', 'N/A')[:50]}...")
                print(f"   🎯 置信度: {result.get('confidence', 'N/A')}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 7. AI Diagnosis
        print("\n7️⃣  AI诊断...")
        diagnosis_data = {
            "symptoms": ["头痛", "发热", "乏力"],
            "patient_info": {"age": 30, "gender": "male"}
        }
        try:
            resp = await client.post(
                "/api/v1/health/diagnose",
                json=diagnosis_data,
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ 诊断完成")
                conditions = result.get('possible_conditions', [])
                if conditions:
                    print(f"   🏥 可能诊断: {conditions[0].get('name', 'N/A')}")
                    print(f"   ⚠️  紧急程度: {result.get('urgency_level', 'N/A')}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 8. Business loop
        print("\n8️⃣  完整商业闭环...")
        loop_data = {
            "detection_type": "voice",
            "input_data": {
                "subtype": "general",
                "query": "综合健康评估"
            },
            "auto_intervention": True
        }
        try:
            resp = await client.post(
                "/api/v1/health/business-loop",
                json=loop_data,
                headers=headers
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"   ✅ 商业闭环完成")
                print(f"   📋 检测: {result.get('detection_result', {}).get('status', 'N/A')}")
                print(f"   📊 分析: 完成")
                print(f"   💊 干预: {'已创建' if result.get('intervention_plan') else '未创建'}")
                print(f"   🔍 追踪ID: {result.get('tracking_id', 'N/A')[:12]}...")
            else:
                print(f"   ⚠️  响应: {resp.status_code} - {resp.text[:100]}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 9. Get subscription plans
        print("\n9️⃣  订阅计划...")
        try:
            resp = await client.get("/api/v1/subscription/plans")
            if resp.status_code == 200:
                plans = resp.json().get('plans', [])
                print(f"   ✅ 可用计划: {len(plans)}个")
                for plan in plans:
                    print(f"      • {plan['name']}: ¥{plan['price']}/月 ({plan['api_calls']}次调用)")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        # 10. Health dashboard
        print("\n🔟  健康仪表板...")
        try:
            resp = await client.get("/api/v1/health/dashboard", headers=headers)
            if resp.status_code == 200:
                dashboard = resp.json()
                print(f"   ✅ 仪表板加载成功")
                print(f"   🏥 健康评分: {dashboard.get('health_summary', {}).get('health_score', 'N/A')}")
                print(f"   📊 健康状态: {dashboard.get('health_summary', {}).get('health_status', 'N/A')}")
                print(f"   📝 记录数量: {dashboard.get('health_summary', {}).get('total_records', 0)}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成！")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_platform())
