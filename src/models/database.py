"""数据库模型"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config.settings import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True)
    nickname = Column(String(50))
    phone = Column(String(20))
    avatar = Column(String(500))
    gender = Column(Integer, default=0)  # 0:未知 1:男 2:女
    birth_date = Column(DateTime)
    height = Column(Float)  # cm
    weight = Column(Float)  # kg
    tcm_type = Column(String(20))  # 中医体质类型
    allergies = Column(JSON, default=[])  # 过敏原
    health_goals = Column(JSON, default=[])  # 健康目标
    subscription = Column(String(20), default="free")  # free/basic/pro/enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    health_records = relationship("HealthRecord", back_populates="user")
    orders = relationship("Order", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")

class HealthRecord(Base):
    """健康检测记录"""
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_type = Column(String(20))  # voice/face/video/comprehensive
    
    # 语音特征
    voice_features = Column(JSON)
    
    # 面部特征
    face_features = Column(JSON)
    
    # 视频特征
    video_features = Column(JSON)
    
    # 综合评估结果
    overall_score = Column(Float)
    health_summary = Column(Text)
    risks = Column(JSON, default=[])
    recommendations = Column(JSON, default=[])
    
    # 中医体质
    tcm_diagnosis = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="health_records")

class NutrientFormula(Base):
    """营养配方"""
    __tablename__ = "nutrient_formulas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    health_record_id = Column(Integer, ForeignKey("health_records.id"))
    
    # 配方信息
    formula_name = Column(String(100))
    ingredients = Column(JSON)  # 成分列表
    dosage = Column(JSON)  # 剂量
    instructions = Column(Text)  # 服用说明
    
    # 配方依据
    analysis_basis = Column(JSON)  # 分析依据
    knowledge_graph_path = Column(JSON)  # 知识图谱推理路径
    
    # 效果追踪
    effectiveness_score = Column(Float)
    user_feedback = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    """订单"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_no = Column(String(50), unique=True)
    
    # 订单信息
    formula_id = Column(Integer, ForeignKey("nutrient_formulas.id"))
    amount = Column(Float)
    status = Column(String(20), default="pending")  # pending/paid/shipping/delivered/completed
    
    # 物流信息
    shipping_address = Column(JSON)
    tracking_no = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="orders")

class ChatHistory(Base):
    """对话历史"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    agent_type = Column(String(20))  # coordinator/translator/summarizer/advisor
    
    # 对话内容
    user_message = Column(Text)
    agent_response = Column(Text)
    context = Column(JSON)
    
    # 意图识别
    intent = Column(String(50))
    confidence = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联
    user = relationship("User", back_populates="chat_history")

class Ingredient(Base):
    """营养成分库"""
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    name_en = Column(String(100))
    category = Column(String(50))  # 维生素/矿物质/氨基酸/植物提取物等
    
    # 功效信息
    functions = Column(JSON)  # 功能列表
    target_conditions = Column(JSON)  # 适用症状
    contraindications = Column(JSON)  # 禁忌
    
    # 剂量信息
    min_dose = Column(Float)
    max_dose = Column(Float)
    unit = Column(String(20))
    
    # 相互作用
    interactions = Column(JSON)  # 与其他成分的相互作用
    
    # 科学依据
    evidence_level = Column(String(20))  # strong/moderate/limited
    references = Column(JSON)  # 参考文献
    
    created_at = Column(DateTime, default=datetime.utcnow)

# 创建数据库表
def init_db():
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
