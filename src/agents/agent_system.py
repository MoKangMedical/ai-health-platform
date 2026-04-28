"""AI Agent系统 - 基于KnowHealth的4个Agent"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class AgentResponse:
    """Agent响应"""
    agent_type: str = ""
    response: str = ""
    intent: str = ""
    confidence: float = 0.0
    actions: List[Dict] = field(default_factory=list)
    context: Dict = field(default_factory=dict)

class BaseAgent:
    """Agent基类"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.conversation_history = []
    
    def process(self, user_message: str, context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        raise NotImplementedError
    
    def _analyze_intent(self, message: str) -> tuple:
        """分析用户意图"""
        intent_keywords = {
            "health_query": ["健康", "身体", "症状", "不适", "疼痛"],
            "nutrition_advice": ["营养", "维生素", "补充", "饮食", "吃什么"],
            "product_inquiry": ["产品", "配方", "定制", "购买", "价格"],
            "report_explain": ["报告", "检测", "指标", "结果", "什么意思"],
            "lifestyle": ["运动", "睡眠", "作息", "生活习惯"],
            "emotional": ["心情", "压力", "焦虑", "抑郁", "情绪"],
            "greeting": ["你好", "hi", "hello", "嗨"],
            "thanks": ["谢谢", "感谢", "thanks"]
        }
        
        message_lower = message.lower()
        for intent, keywords in intent_keywords.items():
            if any(kw in message_lower for kw in keywords):
                return intent, 0.85
        
        return "general", 0.5

class CoordinatorAgent(BaseAgent):
    """协调员Agent - 小和"""
    
    def __init__(self):
        super().__init__("小和", "健康协调员")
        self.capabilities = [
            "理解用户需求",
            "分配任务给其他Agent",
            "整合多Agent结果",
            "维护对话上下文"
        ]
    
    def process(self, user_message: str, context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        intent, confidence = self._analyze_intent(user_message)
        
        # 根据意图路由到相应Agent
        if intent == "health_query":
            return self._handle_health_query(user_message, context)
        elif intent == "nutrition_advice":
            return self._delegate_to_advisor(user_message, context)
        elif intent == "report_explain":
            return self._delegate_to_translator(user_message, context)
        elif intent == "emotional":
            return self._handle_emotional_support(user_message, context)
        elif intent == "greeting":
            return self._handle_greeting(user_message)
        elif intent == "thanks":
            return self._handle_thanks(user_message)
        else:
            return self._handle_general(user_message, context)
    
    def _handle_health_query(self, message: str, context: Dict) -> AgentResponse:
        """处理健康咨询"""
        response = "我理解您对健康的关注。"
        
        if "症状" in message or "不适" in message:
            response += "您描述的症状我会认真记录。建议您可以：\n"
            response += "1. 使用我们的AI健康检测功能，获取更全面的健康评估\n"
            response += "2. 如果症状持续，请及时就医\n"
            response += "3. 我可以为您安排营养师在线咨询"
        else:
            response += "为了给您更准确的建议，我建议您先进行一次AI健康检测。"
            response += "这样我可以基于您的数据提供个性化的健康管理方案。"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="health_query",
            confidence=0.85,
            actions=[{"type": "suggest_detection"}]
        )
    
    def _delegate_to_advisor(self, message: str, context: Dict) -> AgentResponse:
        """委托给顾问Agent"""
        response = "关于营养方面的建议，我来为您详细介绍：\n\n"
        response += "我们的AI营养配方引擎可以根据您的健康数据，"
        response += "从120+种成分中智能匹配最适合您的组合。\n\n"
        response += "您是否已经完成了AI健康检测？如果没有，建议您先进行检测，"
        response += "这样我可以为您生成更精准的个性化配方。"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="nutrition_advice",
            confidence=0.80,
            actions=[{"type": "delegate", "target": "advisor"}]
        )
    
    def _delegate_to_translator(self, message: str, context: Dict) -> AgentResponse:
        """委托给翻译Agent"""
        response = "我来帮您解读这些专业内容。\n\n"
        response += "请把您的检测报告或医学术语发给我，"
        response += "我会用通俗易懂的语言为您解释。"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="report_explain",
            confidence=0.80,
            actions=[{"type": "delegate", "target": "translator"}]
        )
    
    def _handle_emotional_support(self, message: str, context: Dict) -> AgentResponse:
        """处理情绪支持"""
        response = "我理解您的感受，情绪健康同样重要。\n\n"
        response += "以下是一些建议：\n"
        response += "1. 保持规律的作息时间\n"
        response += "2. 适当进行有氧运动\n"
        response += "3. 与朋友家人保持交流\n"
        response += "4. 如有需要，可以寻求专业心理咨询\n\n"
        response += "我们的营养配方中也可以加入有助于情绪调节的成分，"
        response += "比如镁、L-茶氨酸等。"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="emotional",
            confidence=0.75,
            actions=[{"type": "suggest_nutrients", "nutrients": ["镁", "L-茶氨酸"]}]
        )
    
    def _handle_greeting(self, message: str) -> AgentResponse:
        """处理问候"""
        response = "您好！我是小和，您的AI健康协调员。\n\n"
        response += "我可以帮您：\n"
        response += "1. 了解AI健康检测服务\n"
        response += "2. 解读健康报告\n"
        response += "3. 推荐个性化营养方案\n"
        response += "4. 提供健康生活建议\n\n"
        response += "请问有什么可以帮您的？"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="greeting",
            confidence=0.95
        )
    
    def _handle_thanks(self, message: str) -> AgentResponse:
        """处理感谢"""
        response = "不客气！很高兴能帮到您。\n\n"
        response += "如果您还有其他问题，随时可以问我。"
        response += "祝您健康愉快！"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="thanks",
            confidence=0.90
        )
    
    def _handle_general(self, message: str, context: Dict) -> AgentResponse:
        """处理一般咨询"""
        response = "感谢您的提问。\n\n"
        response += "为了更好地帮助您，建议您：\n"
        response += "1. 描述更具体的需求或症状\n"
        response += "2. 提供相关的健康数据\n"
        response += "3. 告诉我您的健康目标\n\n"
        response += "这样我可以为您提供更精准的建议。"
        
        return AgentResponse(
            agent_type="coordinator",
            response=response,
            intent="general",
            confidence=0.60
        )

class TranslatorAgent(BaseAgent):
    """翻译Agent - 小译"""
    
    def __init__(self):
        super().__init__("小译", "医学翻译")
        self.medical_terms = self._load_medical_terms()
    
    def _load_medical_terms(self) -> Dict:
        """加载医学术语库"""
        return {
            "ALT": {"name": "谷丙转氨酶", "explanation": "反映肝功能的指标，正常值0-40 U/L"},
            "AST": {"name": "谷草转氨酶", "explanation": "反映肝功能的指标，正常值0-40 U/L"},
            "TC": {"name": "总胆固醇", "explanation": "血脂指标，正常值<5.2 mmol/L"},
            "TG": {"name": "甘油三酯", "explanation": "血脂指标，正常值<1.7 mmol/L"},
            "HDL": {"name": "高密度脂蛋白", "explanation": "好胆固醇，正常值>1.0 mmol/L"},
            "LDL": {"name": "低密度脂蛋白", "explanation": "坏胆固醇，正常值<3.4 mmol/L"},
            "FBG": {"name": "空腹血糖", "explanation": "血糖指标，正常值3.9-6.1 mmol/L"},
            "HbA1c": {"name": "糖化血红蛋白", "explanation": "反映近3个月血糖控制，正常值<6.5%"},
            "TSH": {"name": "促甲状腺激素", "explanation": "甲状腺功能指标，正常值0.27-4.2 mIU/L"},
            "CRP": {"name": "C反应蛋白", "explanation": "炎症指标，正常值<10 mg/L"},
            "WBC": {"name": "白细胞", "explanation": "免疫指标，正常值4-10 ×10^9/L"},
            "RBC": {"name": "红细胞", "explanation": "携氧指标，正常值4-5.5 ×10^12/L"},
            "HGB": {"name": "血红蛋白", "explanation": "贫血指标，正常值120-160 g/L"},
            "PLT": {"name": "血小板", "explanation": "凝血指标，正常值100-300 ×10^9/L"},
            "BUN": {"name": "尿素氮", "explanation": "肾功能指标，正常值2.9-8.2 mmol/L"},
            "Cr": {"name": "肌酐", "explanation": "肾功能指标，正常值44-133 μmol/L"},
            "UA": {"name": "尿酸", "explanation": "痛风指标，正常值150-416 μmol/L"},
            "维生素D": {"name": "25-羟维生素D", "explanation": "维生素D状态，正常值30-100 ng/mL"},
            "铁蛋白": {"name": "铁蛋白", "explanation": "铁储备指标，正常值12-150 ng/mL"}
        }
    
    def process(self, user_message: str, context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        intent, confidence = self._analyze_intent(user_message)
        
        # 检查是否包含医学术语
        explained_terms = self._explain_terms(user_message)
        
        if explained_terms:
            response = "我来为您解释这些医学术语：\n\n"
            for term, explanation in explained_terms.items():
                response += f"【{term}】{explanation['name']}\n"
                response += f"  {explanation['explanation']}\n\n"
            
            response += "如果您有具体的检测报告需要解读，请把报告发给我，"
            response += "我会为您详细分析每一项指标。"
            
            return AgentResponse(
                agent_type="translator",
                response=response,
                intent="report_explain",
                confidence=0.90
            )
        
        # 处理报告解读请求
        if "报告" in user_message or "结果" in user_message:
            response = "请把您的检测报告发给我，我会：\n\n"
            response += "1. 解释每一项指标的含义\n"
            response += "2. 标注异常指标\n"
            response += "3. 分析可能的原因\n"
            response += "4. 提供改善建议\n\n"
            response += "您可以拍照或直接输入指标数值。"
            
            return AgentResponse(
                agent_type="translator",
                response=response,
                intent="report_explain",
                confidence=0.85
            )
        
        return AgentResponse(
            agent_type="translator",
            response="我是小译，专门负责医学术语解释和报告解读。请问有什么需要帮助的？",
            intent="general",
            confidence=0.60
        )
    
    def _explain_terms(self, message: str) -> Dict:
        """解释医学术语"""
        explained = {}
        
        for term, info in self.medical_terms.items():
            if term in message or info["name"] in message:
                explained[term] = info
        
        return explained

class SummarizerAgent(BaseAgent):
    """总结Agent - 小结"""
    
    def __init__(self):
        super().__init__("小结", "健康总结")
    
    def process(self, user_message: str, context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        # 检查是否请求生成报告
        if "报告" in user_message or "总结" in user_message:
            return self._generate_summary(context)
        
        # 检查是否请求查看历史
        if "历史" in user_message or "记录" in user_message:
            return self._show_history(context)
        
        return AgentResponse(
            agent_type="summarizer",
            response="我是小结，专门负责健康报告生成和数据分析。请问需要什么帮助？",
            intent="general",
            confidence=0.60
        )
    
    def _generate_summary(self, context: Dict) -> AgentResponse:
        """生成健康总结"""
        if not context or "health_records" not in context:
            return AgentResponse(
                agent_type="summarizer",
                response="请先进行AI健康检测，这样我才能为您生成健康总结报告。",
                intent="generate_summary",
                confidence=0.80,
                actions=[{"type": "suggest_detection"}]
            )
        
        records = context["health_records"]
        
        response = "【健康总结报告】\n\n"
        response += f"检测时间：{datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # 总体评分
        avg_score = sum(r.get("overall_score", 0) for r in records) / len(records)
        response += f"综合健康评分：{avg_score:.1f}/100\n\n"
        
        # 主要发现
        response += "【主要发现】\n"
        all_risks = []
        for record in records:
            all_risks.extend(record.get("risks", []))
        
        if all_risks:
            unique_risks = list(set(r["name"] for r in all_risks))
            for risk in unique_risks[:3]:
                response += f"- {risk}：需要关注\n"
        else:
            response += "- 各项指标正常，继续保持\n"
        
        # 建议
        response += "\n【改善建议】\n"
        response += "1. 保持规律作息\n"
        response += "2. 均衡饮食\n"
        response += "3. 适度运动\n"
        response += "4. 定期复查\n"
        
        return AgentResponse(
            agent_type="summarizer",
            response=response,
            intent="generate_summary",
            confidence=0.90,
            actions=[{"type": "generate_report"}]
        )
    
    def _show_history(self, context: Dict) -> AgentResponse:
        """显示历史记录"""
        response = "您的健康检测历史：\n\n"
        
        if context and "health_records" in context:
            records = context["health_records"]
            for i, record in enumerate(records[-5:], 1):
                date = record.get("created_at", "未知日期")
                score = record.get("overall_score", 0)
                response += f"{i}. {date} - 评分：{score:.1f}/100\n"
        else:
            response += "暂无检测记录。\n"
            response += "建议您先进行AI健康检测。"
        
        return AgentResponse(
            agent_type="summarizer",
            response=response,
            intent="show_history",
            confidence=0.85
        )

class AdvisorAgent(BaseAgent):
    """顾问Agent - 小智"""
    
    def __init__(self):
        super().__init__("小智", "营养顾问")
        self.nutrition_knowledge = self._load_nutrition_knowledge()
    
    def _load_nutrition_knowledge(self) -> Dict:
        """加载营养知识"""
        return {
            "免疫力": {
                "nutrients": ["维生素C", "维生素D", "锌", "硒"],
                "foods": ["柑橘类水果", "深绿色蔬菜", "坚果", "鱼类"],
                "lifestyle": ["充足睡眠", "适度运动", "减压"]
            },
            "睡眠": {
                "nutrients": ["镁", "L-茶氨酸", "褪黑素"],
                "foods": ["香蕉", "杏仁", "樱桃", "牛奶"],
                "lifestyle": ["规律作息", "避免咖啡因", "睡前放松"]
            },
            "能量": {
                "nutrients": ["B族维生素", "铁", "CoQ10"],
                "foods": ["全谷物", "瘦肉", "鸡蛋", "绿叶蔬菜"],
                "lifestyle": ["规律运动", "充足饮水", "均衡饮食"]
            },
            "皮肤": {
                "nutrients": ["维生素C", "维生素E", "胶原蛋白", "Omega-3"],
                "foods": ["三文鱼", "牛油果", "蓝莓", "番茄"],
                "lifestyle": ["防晒", "充足饮水", "避免糖分"]
            },
            "消化": {
                "nutrients": ["益生菌", "益生元", "膳食纤维"],
                "foods": ["酸奶", "泡菜", "全谷物", "蔬菜"],
                "lifestyle": ["细嚼慢咽", "规律饮食", "减少加工食品"]
            }
        }
    
    def process(self, user_message: str, context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        intent, confidence = self._analyze_intent(user_message)
        
        # 检查是否包含营养关键词
        nutrition_advice = self._get_nutrition_advice(user_message)
        
        if nutrition_advice:
            response = "【营养建议】\n\n"
            
            for topic, advice in nutrition_advice.items():
                response += f"【{topic}】\n"
                response += f"推荐营养素：{', '.join(advice['nutrients'])}\n"
                response += f"推荐食物：{', '.join(advice['foods'])}\n"
                response += f"生活方式：{', '.join(advice['lifestyle'])}\n\n"
            
            response += "如果您想获得更精准的个性化配方，建议您进行AI健康检测，"
            response += "我可以基于您的数据为您定制专属营养方案。"
            
            return AgentResponse(
                agent_type="advisor",
                response=response,
                intent="nutrition_advice",
                confidence=0.85,
                actions=[{"type": "provide_advice"}]
            )
        
        # 产品咨询
        if "产品" in user_message or "配方" in user_message or "购买" in user_message:
            response = "【我们的产品】\n\n"
            response += "我们提供AI定制的个性化营养配方：\n\n"
            response += "1. 基础版（¥299/月）\n"
            response += "   - 月度AI健康检测\n"
            response += "   - 定制营养配方\n"
            response += "   - AI助手在线咨询\n\n"
            response += "2. 专业版（¥599/月）\n"
            response += "   - 周度AI健康检测\n"
            response += "   - 高级定制配方\n"
            response += "   - 营养师1v1咨询\n\n"
            response += "您是否想先进行一次免费的AI健康检测？"
            
            return AgentResponse(
                agent_type="advisor",
                response=response,
                intent="product_inquiry",
                confidence=0.90,
                actions=[{"type": "show_products"}]
            )
        
        return AgentResponse(
            agent_type="advisor",
            response="我是小智，您的AI营养顾问。我可以为您提供：\n1. 个性化营养建议\n2. 产品咨询\n3. 饮食指导\n\n请问有什么需要帮助的？",
            intent="general",
            confidence=0.60
        )
    
    def _get_nutrition_advice(self, message: str) -> Dict:
        """获取营养建议"""
        advice = {}
        
        for topic, knowledge in self.nutrition_knowledge.items():
            if topic in message:
                advice[topic] = knowledge
        
        return advice

class AgentSystem:
    """Agent系统"""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.translator = TranslatorAgent()
        self.summarizer = SummarizerAgent()
        self.advisor = AdvisorAgent()
        
        self.agents = {
            "coordinator": self.coordinator,
            "translator": self.translator,
            "summarizer": self.summarizer,
            "advisor": self.advisor
        }
    
    def process_message(self, user_message: str, 
                       agent_type: str = "coordinator",
                       context: Dict = None) -> AgentResponse:
        """处理用户消息"""
        agent = self.agents.get(agent_type, self.coordinator)
        
        # 记录对话历史
        agent.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # 处理消息
        response = agent.process(user_message, context)
        
        # 记录响应
        agent.conversation_history.append({
            "role": "assistant",
            "content": response.response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response
    
    def get_agent_info(self) -> List[Dict]:
        """获取所有Agent信息"""
        return [
            {"name": "小和", "role": "健康协调员", "capabilities": self.coordinator.capabilities},
            {"name": "小译", "role": "医学翻译", "capabilities": ["医学术语解释", "报告解读"]},
            {"name": "小结", "role": "健康总结", "capabilities": ["报告生成", "数据分析"]},
            {"name": "小智", "role": "营养顾问", "capabilities": ["营养建议", "产品咨询"]}
        ]
