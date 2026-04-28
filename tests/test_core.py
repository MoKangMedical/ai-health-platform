"""核心模块测试"""

import pytest
import numpy as np
from src.core.health_engine import (
    VoiceAnalyzer, FaceAnalyzer, HealthAssessmentEngine,
    VoiceFeatures, FaceFeatures, ComprehensiveHealthReport
)
from src.core.nutrient_engine import NutrientFormulaEngine, KnowledgeGraph
from src.agents.agent_system import AgentSystem

# ==================== 语音分析测试 ====================
class TestVoiceAnalyzer:
    def test_voice_features_creation(self):
        """测试语音特征创建"""
        features = VoiceFeatures()
        assert features.f0_mean == 0.0
        assert features.total_duration == 0.0
        
    def test_voice_features_to_dict(self):
        """测试语音特征转字典"""
        features = VoiceFeatures(f0_mean=150.0, speech_rate=4.0)
        data = features.to_dict()
        assert data["f0_mean"] == 150.0
        assert data["speech_rate"] == 4.0
        
    def test_voice_features_to_vector(self):
        """测试语音特征转向量"""
        features = VoiceFeatures()
        vector = features.to_vector()
        assert len(vector) == 59  # 59维特征

# ==================== 面部分析测试 ====================
class TestFaceAnalyzer:
    def test_face_features_creation(self):
        """测试面部特征创建"""
        features = FaceFeatures()
        assert features.skin_color_score == 0.0
        assert features.eye_brightness == 0.0
        
    def test_face_features_to_dict(self):
        """测试面部特征转字典"""
        features = FaceFeatures(skin_color_score=85.0, eye_brightness=90.0)
        data = features.to_dict()
        assert data["skin_color_score"] == 85.0
        assert data["eye_brightness"] == 90.0

# ==================== 健康评估引擎测试 ====================
class TestHealthAssessmentEngine:
    def test_engine_initialization(self):
        """测试引擎初始化"""
        engine = HealthAssessmentEngine()
        assert engine.voice_analyzer is not None
        assert engine.face_analyzer is not None
        
    def test_voice_health_assessment(self):
        """测试语音健康评估"""
        engine = HealthAssessmentEngine()
        # 使用模拟数据
        result = engine.assess_voice_health("nonexistent.wav")
        assert "features" in result
        assert "risks" in result
        assert "overall_score" in result
        
    def test_comprehensive_report_creation(self):
        """测试综合报告创建"""
        report = ComprehensiveHealthReport(user_id=1)
        assert report.user_id == 1
        assert report.overall_score == 0.0
        
    def test_comprehensive_report_to_dict(self):
        """测试综合报告转字典"""
        report = ComprehensiveHealthReport(
            user_id=1,
            overall_score=85.0,
            health_summary="健康状态良好"
        )
        data = report.to_dict()
        assert data["user_id"] == 1
        assert data["overall_score"] == 85.0

# ==================== 知识图谱测试 ====================
class TestKnowledgeGraph:
    def test_graph_initialization(self):
        """测试知识图谱初始化"""
        kg = KnowledgeGraph()
        assert "维生素C" in kg.graph
        assert "镁" in kg.graph
        
    def test_query(self):
        """测试知识图谱查询"""
        kg = KnowledgeGraph()
        needs = {"immune": ["维生素C", "锌"]}
        candidates = kg.query(needs)
        assert len(candidates) > 0
        
    def test_get_synergies(self):
        """测试获取协同成分"""
        kg = KnowledgeGraph()
        synergies = kg.get_synergies("维生素C")
        assert "维生素E" in synergies
        
    def test_get_antagonists(self):
        """测试获取拮抗成分"""
        kg = KnowledgeGraph()
        antagonists = kg.get_antagonists("维生素C")
        assert "维生素B12" in antagonists

# ==================== 营养配方引擎测试 ====================
class TestNutrientFormulaEngine:
    def test_engine_initialization(self):
        """测试引擎初始化"""
        engine = NutrientFormulaEngine()
        assert engine.knowledge_graph is not None
        assert len(engine.ingredient_db) > 0
        
    def test_generate_formula(self):
        """测试生成配方"""
        engine = NutrientFormulaEngine()
        health_report = {
            "overall_score": 75.0,
            "risks": [{"name": "免疫力低下", "level": "medium"}],
            "nutrient_needs": {"immune": ["维生素C", "锌"]},
            "tcm_diagnosis": {"primary_type": "气虚质"}
        }
        questionnaire = {
            "allergies": [],
            "health_goals": ["提升免疫力"],
            "current_medications": []
        }
        
        formula = engine.generate_formula(health_report, questionnaire)
        assert formula.formula_name != ""
        assert len(formula.ingredients) > 0
        
    def test_formula_adjustment(self):
        """测试配方调整"""
        engine = NutrientFormulaEngine()
        
        # 创建初始配方
        from src.core.nutrient_engine import NutrientFormula
        initial_formula = NutrientFormula(
            formula_name="测试配方",
            ingredients=[
                {"name": "维生素C", "dose": 500, "unit": "mg", "reason": "免疫支持"},
                {"name": "锌", "dose": 15, "unit": "mg", "reason": "免疫支持"}
            ]
        )
        
        # 调整配方
        feedback = {
            "effectiveness_score": 6,
            "side_effects": [],
            "preferences": {}
        }
        
        adjusted = engine.adjust_formula(initial_formula, feedback)
        assert adjusted.version == 2

# ==================== Agent系统测试 ====================
class TestAgentSystem:
    def test_system_initialization(self):
        """测试系统初始化"""
        system = AgentSystem()
        assert system.coordinator is not None
        assert system.translator is not None
        assert system.summarizer is not None
        assert system.advisor is not None
        
    def test_coordinator_greeting(self):
        """测试协调员问候"""
        system = AgentSystem()
        response = system.process_message("你好", "coordinator")
        assert response.agent_type == "coordinator"
        assert "小和" in response.response
        
    def test_translator_medical_terms(self):
        """测试翻译Agent医学术语"""
        system = AgentSystem()
        response = system.process_message("ALT是什么意思", "translator")
        assert response.agent_type == "translator"
        assert "谷丙转氨酶" in response.response
        
    def test_advisor_nutrition(self):
        """测试顾问Agent营养建议"""
        system = AgentSystem()
        response = system.process_message("我想提升免疫力", "advisor")
        assert response.agent_type == "advisor"
        assert "维生素" in response.response
        
    def test_get_agent_info(self):
        """测试获取Agent信息"""
        system = AgentSystem()
        info = system.get_agent_info()
        assert len(info) == 4
        assert info[0]["name"] == "小和"

# ==================== 运行测试 ====================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
