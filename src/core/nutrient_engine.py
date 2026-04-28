"""AI营养配方引擎"""

import json
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from datetime import datetime

@dataclass
class Ingredient:
    """营养成分"""
    id: int = 0
    name: str = ""
    name_en: str = ""
    category: str = ""  # 维生素/矿物质/氨基酸/植物提取物
    
    # 功效
    functions: List[str] = field(default_factory=list)
    target_conditions: List[str] = field(default_factory=list)
    
    # 剂量
    min_dose: float = 0.0
    max_dose: float = 0.0
    recommended_dose: float = 0.0
    unit: str = "mg"
    
    # 相互作用
    synergies: List[str] = field(default_factory=list)  # 协同成分
    antagonists: List[str] = field(default_factory=list)  # 拮抗成分
    
    # 安全性
    contraindications: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    
    # 科学依据
    evidence_level: str = "moderate"  # strong/moderate/limited
    references: List[str] = field(default_factory=list)

@dataclass
class NutrientFormula:
    """营养配方"""
    id: int = 0
    user_id: int = 0
    formula_name: str = ""
    
    # 成分配方
    ingredients: List[Dict] = field(default_factory=list)  # [{name, dose, unit, reason}]
    
    # 配方说明
    total_daily_dose: float = 0.0
    instructions: str = ""
    timing: str = ""  # 服用时间
    
    # 配方依据
    analysis_basis: Dict = field(default_factory=dict)
    knowledge_graph_path: List[str] = field(default_factory=list)
    
    # 个性化调整
    adjustments: List[Dict] = field(default_factory=list)
    
    # 元数据
    created_at: str = ""
    version: int = 1
    
    def to_dict(self) -> Dict:
        return asdict(self)

class KnowledgeGraph:
    """营养知识图谱"""
    
    def __init__(self):
        self.graph = {}
        self._build_graph()
    
    def _build_graph(self):
        """构建知识图谱"""
        # 节点：营养成分、健康状况、体质类型
        self.graph = {
            # 维生素节点
            "维生素C": {
                "type": "vitamin",
                "functions": ["抗氧化", "免疫支持", "胶原蛋白合成"],
                "synergies": ["维生素E", "铁"],
                "antagonists": ["维生素B12"],
                "target_conditions": ["免疫力低下", "皮肤问题", "贫血"],
                "evidence_level": "strong"
            },
            "维生素D": {
                "type": "vitamin",
                "functions": ["钙吸收", "免疫调节", "情绪调节"],
                "synergies": ["钙", "维生素K2"],
                "antagonists": [],
                "target_conditions": ["骨质疏松", "免疫力低下", "抑郁"],
                "evidence_level": "strong"
            },
            "维生素B群": {
                "type": "vitamin_complex",
                "functions": ["能量代谢", "神经系统", "红细胞生成"],
                "synergies": ["镁", "锌"],
                "antagonists": [],
                "target_conditions": ["疲劳", "神经系统问题", "贫血"],
                "evidence_level": "strong"
            },
            
            # 矿物质节点
            "镁": {
                "type": "mineral",
                "functions": ["肌肉放松", "睡眠改善", "心血管保护"],
                "synergies": ["钙", "维生素B6"],
                "antagonists": ["钙"],
                "target_conditions": ["失眠", "肌肉痉挛", "焦虑"],
                "evidence_level": "strong"
            },
            "锌": {
                "type": "mineral",
                "functions": ["免疫支持", "伤口愈合", "味觉维持"],
                "synergies": ["维生素C"],
                "antagonists": ["铜"],
                "target_conditions": ["免疫力低下", "伤口愈合慢", "味觉减退"],
                "evidence_level": "strong"
            },
            "铁": {
                "type": "mineral",
                "functions": ["血红蛋白合成", "氧气运输", "能量代谢"],
                "synergies": ["维生素C"],
                "antagonists": ["钙", "茶"],
                "target_conditions": ["贫血", "疲劳", "注意力不集中"],
                "evidence_level": "strong"
            },
            
            # 氨基酸节点
            "L-茶氨酸": {
                "type": "amino_acid",
                "functions": ["放松", "专注力", "睡眠质量"],
                "synergies": ["镁"],
                "antagonists": [],
                "target_conditions": ["焦虑", "失眠", "注意力不集中"],
                "evidence_level": "moderate"
            },
            "甘氨酸": {
                "type": "amino_acid",
                "functions": ["睡眠改善", "胶原蛋白合成", "神经递质"],
                "synergies": ["镁"],
                "antagonists": [],
                "target_conditions": ["失眠", "皮肤问题"],
                "evidence_level": "moderate"
            },
            
            # 植物提取物节点
            "姜黄素": {
                "type": "plant_extract",
                "functions": ["抗炎", "抗氧化", "关节保护"],
                "synergies": ["黑胡椒碱"],
                "antagonists": [],
                "target_conditions": ["炎症", "关节疼痛", "消化问题"],
                "evidence_level": "strong"
            },
            "南非醉茄": {
                "type": "plant_extract",
                "functions": ["抗压", "能量提升", "认知改善"],
                "synergies": [],
                "antagonists": [],
                "target_conditions": ["压力", "疲劳", "认知下降"],
                "evidence_level": "moderate"
            },
            
            # 中医体质节点
            "气虚质": {
                "type": "tcm_type",
                "recommended": ["人参", "黄芪", "党参", "白术"],
                "avoid": ["生冷食物", "油腻食物"],
                "nutrient_focus": ["B族维生素", "铁", "锌"]
            },
            "阳虚质": {
                "type": "tcm_type",
                "recommended": ["肉桂", "干姜", "附子", "鹿茸"],
                "avoid": ["寒凉食物", "生冷饮品"],
                "nutrient_focus": ["维生素D", "铁", "B12"]
            },
            "阴虚质": {
                "type": "tcm_type",
                "recommended": ["枸杞", "麦冬", "石斛", "玉竹"],
                "avoid": ["辛辣食物", "温燥食物"],
                "nutrient_focus": ["维生素E", "Omega-3", "镁"]
            },
            
            # 健康状况节点
            "免疫力低下": {
                "type": "condition",
                "recommended_nutrients": ["维生素C", "维生素D", "锌", "硒"],
                "lifestyle": ["充足睡眠", "适度运动", "减压"],
                "evidence_level": "strong"
            },
            "疲劳": {
                "type": "condition",
                "recommended_nutrients": ["B族维生素", "铁", "镁", "CoQ10"],
                "lifestyle": ["规律作息", "适度运动", "均衡饮食"],
                "evidence_level": "strong"
            },
            "失眠": {
                "type": "condition",
                "recommended_nutrients": ["镁", "L-茶氨酸", "甘氨酸", "褪黑素"],
                "lifestyle": ["规律作息", "避免咖啡因", "睡前放松"],
                "evidence_level": "moderate"
            },
            "皮肤问题": {
                "type": "condition",
                "recommended_nutrients": ["维生素C", "维生素E", "胶原蛋白", "Omega-3"],
                "lifestyle": ["充足饮水", "防晒", "均衡饮食"],
                "evidence_level": "moderate"
            }
        }
    
    def query(self, needs: Dict, constraints: Dict = None) -> List[Dict]:
        """查询知识图谱"""
        candidates = []
        
        # 基于健康需求查询
        for category, nutrients in needs.items():
            for nutrient in nutrients:
                if nutrient in self.graph:
                    node = self.graph[nutrient]
                    candidates.append({
                        "name": nutrient,
                        "type": node.get("type", "unknown"),
                        "functions": node.get("functions", []),
                        "evidence_level": node.get("evidence_level", "moderate")
                    })
        
        # 基于中医体质查询
        tcm_type = constraints.get("tcm_type") if constraints else None
        if tcm_type and tcm_type in self.graph:
            tcm_node = self.graph[tcm_type]
            for nutrient in tcm_node.get("nutrient_focus", []):
                if nutrient in self.graph:
                    candidates.append({
                        "name": nutrient,
                        "type": self.graph[nutrient].get("type", "unknown"),
                        "functions": self.graph[nutrient].get("functions", []),
                        "evidence_level": self.graph[nutrient].get("evidence_level", "moderate")
                    })
        
        return candidates
    
    def get_synergies(self, ingredient: str) -> List[str]:
        """获取协同成分"""
        if ingredient in self.graph:
            return self.graph[ingredient].get("synergies", [])
        return []
    
    def get_antagonists(self, ingredient: str) -> List[str]:
        """获取拮抗成分"""
        if ingredient in self.graph:
            return self.graph[ingredient].get("antagonists", [])
        return []

class NutrientFormulaEngine:
    """营养配方引擎"""
    
    def __init__(self):
        self.knowledge_graph = KnowledgeGraph()
        self.ingredient_db = self._load_ingredient_db()
    
    def _load_ingredient_db(self) -> Dict:
        """加载成分数据库"""
        # 简化实现：返回预定义的成分库
        return {
            "维生素C": Ingredient(
                id=1, name="维生素C", name_en="Vitamin C", category="vitamin",
                functions=["抗氧化", "免疫支持", "胶原蛋白合成"],
                min_dose=100, max_dose=2000, recommended_dose=500, unit="mg",
                evidence_level="strong"
            ),
            "维生素D3": Ingredient(
                id=2, name="维生素D3", name_en="Vitamin D3", category="vitamin",
                functions=["钙吸收", "免疫调节", "情绪调节"],
                min_dose=400, max_dose=4000, recommended_dose=2000, unit="IU",
                evidence_level="strong"
            ),
            "镁": Ingredient(
                id=3, name="镁", name_en="Magnesium", category="mineral",
                functions=["肌肉放松", "睡眠改善", "心血管保护"],
                min_dose=100, max_dose=400, recommended_dose=300, unit="mg",
                synergies=["维生素B6"],
                evidence_level="strong"
            ),
            "锌": Ingredient(
                id=4, name="锌", name_en="Zinc", category="mineral",
                functions=["免疫支持", "伤口愈合", "味觉维持"],
                min_dose=5, max_dose=40, recommended_dose=15, unit="mg",
                evidence_level="strong"
            ),
            "Omega-3": Ingredient(
                id=5, name="Omega-3", name_en="Omega-3", category="fatty_acid",
                functions=["心血管保护", "抗炎", "大脑健康"],
                min_dose=500, max_dose=3000, recommended_dose=1000, unit="mg",
                evidence_level="strong"
            ),
            "B族维生素": Ingredient(
                id=6, name="B族维生素", name_en="B-Complex", category="vitamin",
                functions=["能量代谢", "神经系统", "红细胞生成"],
                min_dose=1, max_dose=100, recommended_dose=50, unit="mg",
                evidence_level="strong"
            ),
            "胶原蛋白": Ingredient(
                id=7, name="胶原蛋白", name_en="Collagen", category="protein",
                functions=["皮肤弹性", "关节保护", "骨骼健康"],
                min_dose=2500, max_dose=15000, recommended_dose=5000, unit="mg",
                evidence_level="moderate"
            ),
            "益生菌": Ingredient(
                id=8, name="益生菌", name_en="Probiotics", category="probiotic",
                functions=["肠道健康", "免疫支持", "消化改善"],
                min_dose=1, max_dose=100, recommended_dose=10, unit="billion CFU",
                evidence_level="moderate"
            ),
            "CoQ10": Ingredient(
                id=9, name="CoQ10", name_en="Coenzyme Q10", category="coenzyme",
                functions=["能量产生", "抗氧化", "心血管保护"],
                min_dose=30, max_dose=200, recommended_dose=100, unit="mg",
                evidence_level="moderate"
            ),
            "姜黄素": Ingredient(
                id=10, name="姜黄素", name_en="Curcumin", category="plant_extract",
                functions=["抗炎", "抗氧化", "关节保护"],
                min_dose=100, max_dose=2000, recommended_dose=500, unit="mg",
                synergies=["黑胡椒碱"],
                evidence_level="strong"
            )
        }
    
    def generate_formula(self, health_report: Dict, questionnaire: Dict) -> NutrientFormula:
        """生成个性化配方"""
        formula = NutrientFormula()
        formula.created_at = datetime.now().isoformat()
        
        # 1. 分析健康需求
        needs = health_report.get("nutrient_needs", {})
        tcm_type = health_report.get("tcm_diagnosis", {}).get("primary_type", "")
        
        # 2. 查询知识图谱
        candidates = self.knowledge_graph.query(
            needs=needs,
            constraints={"tcm_type": tcm_type}
        )
        
        # 3. 结合问卷信息筛选
        allergies = questionnaire.get("allergies", [])
        health_goals = questionnaire.get("health_goals", [])
        current_medications = questionnaire.get("current_medications", [])
        
        # 4. 优化配方
        selected_ingredients = self._optimize_formula(
            candidates, allergies, health_goals, current_medications
        )
        
        # 5. 计算剂量
        formula.ingredients = self._calculate_dosages(
            selected_ingredients, health_report, questionnaire
        )
        
        # 6. 生成说明
        formula.formula_name = self._generate_formula_name(health_goals, tcm_type)
        formula.instructions = self._generate_instructions(formula.ingredients)
        formula.timing = self._determine_timing(formula.ingredients)
        
        # 7. 记录分析依据
        formula.analysis_basis = {
            "health_score": health_report.get("overall_score", 0),
            "risks": health_report.get("risks", []),
            "tcm_type": tcm_type,
            "health_goals": health_goals
        }
        formula.knowledge_graph_path = [c["name"] for c in candidates[:5]]
        
        return formula
    
    def _optimize_formula(self, candidates: List[Dict], 
                         allergies: List[str],
                         health_goals: List[str],
                         current_medications: List[str]) -> List[Dict]:
        """优化配方"""
        selected = []
        
        # 过滤过敏成分
        safe_candidates = [c for c in candidates if c["name"] not in allergies]
        
        # 优先选择证据等级高的成分
        strong_evidence = [c for c in safe_candidates if c.get("evidence_level") == "strong"]
        moderate_evidence = [c for c in safe_candidates if c.get("evidence_level") == "moderate"]
        
        # 选择前5-8个成分
        selected = strong_evidence[:5]
        if len(selected) < 5:
            selected.extend(moderate_evidence[:5-len(selected)])
        
        # 检查相互作用
        selected = self._check_interactions(selected)
        
        return selected[:8]  # 最多8种成分
    
    def _check_interactions(self, ingredients: List[Dict]) -> List[Dict]:
        """检查成分相互作用"""
        # 简化实现：移除有拮抗作用的成分
        names = [i["name"] for i in ingredients]
        filtered = []
        
        for ingredient in ingredients:
            antagonists = self.knowledge_graph.get_antagonists(ingredient["name"])
            has_conflict = any(a in names for a in antagonists)
            
            if not has_conflict:
                filtered.append(ingredient)
        
        return filtered
    
    def _calculate_dosages(self, ingredients: List[Dict], 
                          health_report: Dict,
                          questionnaire: Dict) -> List[Dict]:
        """计算剂量"""
        formula_ingredients = []
        
        for ingredient in ingredients:
            name = ingredient["name"]
            
            # 从数据库获取基础剂量
            if name in self.ingredient_db:
                db_ingredient = self.ingredient_db[name]
                base_dose = db_ingredient.recommended_dose
                unit = db_ingredient.unit
            else:
                base_dose = 100  # 默认剂量
                unit = "mg"
            
            # 根据健康状况调整剂量
            adjusted_dose = self._adjust_dose_by_health(
                base_dose, name, health_report
            )
            
            formula_ingredients.append({
                "name": name,
                "dose": adjusted_dose,
                "unit": unit,
                "reason": self._get_dose_reason(name, health_report)
            })
        
        return formula_ingredients
    
    def _adjust_dose_by_health(self, base_dose: float, 
                              ingredient: str,
                              health_report: Dict) -> float:
        """根据健康状况调整剂量"""
        # 简化实现
        risks = health_report.get("risks", [])
        risk_names = [r["name"] for r in risks]
        
        # 如果有相关风险，增加剂量
        if ingredient == "维生素C" and "免疫力低下" in risk_names:
            return base_dose * 1.5
        elif ingredient == "镁" and "失眠" in risk_names:
            return base_dose * 1.3
        elif ingredient == "B族维生素" and "疲劳" in risk_names:
            return base_dose * 1.2
        
        return base_dose
    
    def _get_dose_reason(self, ingredient: str, health_report: Dict) -> str:
        """获取剂量调整原因"""
        risks = health_report.get("risks", [])
        risk_names = [r["name"] for r in risks]
        
        reasons = {
            "维生素C": "支持免疫系统，抗氧化保护",
            "维生素D3": "促进钙吸收，调节免疫功能",
            "镁": "改善睡眠质量，缓解肌肉紧张",
            "锌": "增强免疫功能，促进伤口愈合",
            "Omega-3": "心血管保护，抗炎作用",
            "B族维生素": "能量代谢支持，神经系统健康",
            "胶原蛋白": "皮肤弹性维护，关节保护",
            "益生菌": "肠道菌群平衡，消化健康",
            "CoQ10": "细胞能量产生，心血管保护",
            "姜黄素": "天然抗炎，关节健康支持"
        }
        
        return reasons.get(ingredient, "综合营养支持")
    
    def _generate_formula_name(self, health_goals: List[str], tcm_type: str) -> str:
        """生成配方名称"""
        goal_mapping = {
            "提升免疫力": "免疫增强",
            "改善睡眠": "安神助眠",
            "增强精力": "活力提升",
            "美容养颜": "美肌焕颜",
            "减压放松": "舒压平衡",
            "关节保护": "关节养护",
            "心血管健康": "心血管养护",
            "消化健康": "肠道调理"
        }
        
        primary_goal = health_goals[0] if health_goals else "综合健康"
        goal_name = goal_mapping.get(primary_goal, "综合健康")
        
        return f"个性化{goal_name}配方"
    
    def _generate_instructions(self, ingredients: List[Dict]) -> str:
        """生成服用说明"""
        instructions = "【服用说明】\n"
        instructions += "1. 每日建议随餐服用，以提高吸收率\n"
        instructions += "2. 如有不适，请立即停止服用并咨询医生\n"
        instructions += "3. 请勿超过建议剂量\n\n"
        instructions += "【成分详情】\n"
        
        for ing in ingredients:
            instructions += f"- {ing['name']}: {ing['dose']}{ing['unit']} - {ing['reason']}\n"
        
        return instructions
    
    def _determine_timing(self, ingredients: List[Dict]) -> str:
        """确定服用时间"""
        names = [i["name"] for i in ingredients]
        
        has_sleep_aid = any(n in ["镁", "L-茶氨酸", "甘氨酸"] for n in names)
        has_energy_aid = any(n in ["B族维生素", "CoQ10"] for n in names)
        
        if has_sleep_aid and has_energy_aid:
            return "早晨随餐服用能量类成分，睡前服用助眠类成分"
        elif has_sleep_aid:
            return "睡前30分钟服用"
        elif has_energy_aid:
            return "早晨随餐服用"
        else:
            return "随餐服用，分早晚两次"
    
    def adjust_formula(self, formula: NutrientFormula, 
                       feedback: Dict) -> NutrientFormula:
        """根据反馈调整配方"""
        effectiveness = feedback.get("effectiveness_score", 5)
        side_effects = feedback.get("side_effects", [])
        preferences = feedback.get("preferences", {})
        
        # 创建新配方
        new_formula = NutrientFormula()
        new_formula.version = formula.version + 1
        new_formula.created_at = datetime.now().isoformat()
        new_formula.formula_name = formula.formula_name
        new_formula.analysis_basis = formula.analysis_basis
        
        # 调整成分
        adjusted_ingredients = []
        for ing in formula.ingredients:
            if ing["name"] in side_effects:
                # 减少或移除有副作用的成分
                continue
            
            new_ing = ing.copy()
            
            # 根据效果调整剂量
            if effectiveness < 5:
                new_ing["dose"] = min(ing["dose"] * 1.2, ing["dose"] * 1.5)
            elif effectiveness > 8:
                new_ing["dose"] = ing["dose"]  # 保持当前剂量
            
            adjusted_ingredients.append(new_ing)
        
        new_formula.ingredients = adjusted_ingredients
        new_formula.instructions = self._generate_instructions(adjusted_ingredients)
        new_formula.timing = self._determine_timing(adjusted_ingredients)
        
        # 记录调整
        new_formula.adjustments = formula.adjustments + [{
            "version": formula.version,
            "reason": f"效果评分: {effectiveness}/10",
            "changes": f"调整了{len(formula.ingredients) - len(adjusted_ingredients)}种成分"
        }]
        
        return new_formula
