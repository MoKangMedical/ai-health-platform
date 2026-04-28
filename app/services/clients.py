"""
AI Health Platform - Service Clients for Sub-services Integration
"""
import httpx
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class VoiceHealthClient:
    """Client for VoiceHealth service (Multi-modal Detection, Port 8100)"""
    
    def __init__(self):
        self.base_url = settings.VOICE_HEALTH_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def detect_voice_health(
        self,
        audio_data: Optional[str] = None,
        audio_url: Optional[str] = None,
        detection_type: str = "general"
    ) -> Dict[str, Any]:
        """Detect health conditions from voice/audio"""
        try:
            payload = {
                "detection_type": detection_type,
                "timestamp": datetime.utcnow().isoformat()
            }
            if audio_data:
                payload["audio_base64"] = audio_data
            if audio_url:
                payload["audio_url"] = audio_url
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/detect",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"VoiceHealth API error: {e}")
            return self._mock_voice_detection(detection_type)
        except Exception as e:
            logger.error(f"VoiceHealth connection error: {e}")
            return self._mock_voice_detection(detection_type)
    
    async def get_detection_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's detection history"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/history/{user_id}",
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return []
    
    def _mock_voice_detection(self, detection_type: str) -> Dict[str, Any]:
        """Mock response when service is unavailable"""
        return {
            "status": "completed",
            "detection_type": detection_type,
            "results": {
                "respiratory": {"score": 85, "status": "normal"},
                "cardiovascular": {"score": 78, "status": "good"},
                "mental_health": {"score": 72, "status": "moderate"}
            },
            "risk_score": 25.5,
            "recommendations": [
                "建议保持规律作息",
                "适当增加有氧运动",
                "注意饮食均衡"
            ],
            "mock": True
        }


class KnowHealthClient:
    """Client for KnowHealth service (AI Agent, Port 8080)"""
    
    def __init__(self):
        self.base_url = settings.KNOW_HEALTH_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def query_knowledge(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        language: str = "zh"
    ) -> Dict[str, Any]:
        """Query health knowledge base"""
        try:
            payload = {
                "query": query,
                "context": context or {},
                "language": language,
                "timestamp": datetime.utcnow().isoformat()
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/query",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"KnowHealth connection error: {e}")
            return self._mock_knowledge_response(query)
    
    async def get_health_tips(
        self,
        user_profile: Dict[str, Any],
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get personalized health tips"""
        try:
            payload = {
                "user_profile": user_profile,
                "category": category
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/tips",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return self._mock_health_tips()
    
    async def chat_with_agent(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        user_context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Chat with AI health agent"""
        try:
            payload = {
                "message": message,
                "conversation_id": conversation_id,
                "user_context": user_context or {}
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/chat",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"KnowHealth chat error: {e}")
            return self._mock_chat_response(message)
    
    def _mock_knowledge_response(self, query: str) -> Dict[str, Any]:
        return {
            "answer": f"关于'{query}'的健康建议：请保持健康的生活方式，定期体检，如有不适请及时就医。",
            "sources": [
                {"title": "健康生活指南", "relevance": 0.95},
                {"title": "常见疾病预防", "relevance": 0.88}
            ],
            "confidence": 0.85,
            "related_topics": ["健康饮食", "运动建议", "睡眠质量"],
            "mock": True
        }
    
    def _mock_health_tips(self) -> List[Dict]:
        return [
            {"category": "diet", "tip": "每天摄入足够的蔬菜水果", "priority": "high"},
            {"category": "exercise", "tip": "每周至少150分钟中等强度运动", "priority": "high"},
            {"category": "sleep", "tip": "保持7-8小时优质睡眠", "priority": "medium"}
        ]
    
    def _mock_chat_response(self, message: str) -> Dict[str, Any]:
        return {
            "response": f"您好！关于您提到的'{message[:20]}...'，建议您...",
            "conversation_id": "mock_conv_001",
            "suggestions": ["了解更多健康知识", "预约体检", "查看健康报告"],
            "mock": True
        }


class MediChatRDClient:
    """Client for MediChat-RD service (Knowledge Graph + Diagnosis)"""
    
    def __init__(self):
        self.base_url = settings.MEDI_CHAT_RD_URL
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def diagnose(
        self,
        symptoms: List[str],
        patient_info: Optional[Dict[str, Any]] = None,
        medical_history: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Get diagnosis based on symptoms"""
        try:
            payload = {
                "symptoms": symptoms,
                "patient_info": patient_info or {},
                "medical_history": medical_history or [],
                "timestamp": datetime.utcnow().isoformat()
            }
            response = await self.client.post(
                f"{self.base_url}/api/v1/diagnose",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"MediChat-RD diagnosis error: {e}")
            return self._mock_diagnosis(symptoms)
    
    async def query_knowledge_graph(
        self,
        entity: str,
        relation: Optional[str] = None
    ) -> Dict[str, Any]:
        """Query medical knowledge graph"""
        try:
            params = {"entity": entity}
            if relation:
                params["relation"] = relation
            response = await self.client.get(
                f"{self.base_url}/api/v1/knowledge-graph",
                params=params
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"MediChat-RD KG error: {e}")
            return self._mock_knowledge_graph(entity)
    
    async def get_drug_info(
        self,
        drug_name: str,
        include_interactions: bool = True
    ) -> Dict[str, Any]:
        """Get drug information and interactions"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/drugs/{drug_name}",
                params={"include_interactions": include_interactions}
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            return {"drug_name": drug_name, "info": "药物信息暂时无法获取", "mock": True}
    
    def _mock_diagnosis(self, symptoms: List[str]) -> Dict[str, Any]:
        return {
            "possible_conditions": [
                {"name": "普通感冒", "probability": 0.65, "severity": "mild"},
                {"name": "过敏性鼻炎", "probability": 0.25, "severity": "mild"},
                {"name": "流感", "probability": 0.10, "severity": "moderate"}
            ],
            "recommended_tests": ["血常规", "体温测量", "咽拭子检查"],
            "urgency_level": "low",
            "disclaimer": "此诊断仅供参考，不构成医疗建议。如有不适，请及时就医。",
            "mock": True
        }
    
    def _mock_knowledge_graph(self, entity: str) -> Dict[str, Any]:
        return {
            "entity": entity,
            "relations": [
                {"type": "症状", "targets": ["发热", "咳嗽", "乏力"]},
                {"type": "治疗", "targets": ["休息", "多饮水", "对症治疗"]},
                {"type": "预防", "targets": ["勤洗手", "戴口罩", "避免聚集"]}
            ],
            "mock": True
        }


# Singleton instances
voice_health_client = VoiceHealthClient()
know_health_client = KnowHealthClient()
medi_chat_rd_client = MediChatRDClient()
