"""
AI Health Platform - Data Models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class HealthStatus(str, enum.Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    age = Column(Integer)
    gender = Column(String)
    subscription_plan = Column(String, default=SubscriptionPlan.FREE)
    subscription_expires = Column(DateTime)
    api_calls_remaining = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    health_records = relationship("HealthRecord", back_populates="user")
    detection_sessions = relationship("DetectionSession", back_populates="user")
    consultations = relationship("Consultation", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")


class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    record_type = Column(String)  # voice, text, image, sensor
    raw_data = Column(JSON)
    analysis_result = Column(JSON)
    risk_score = Column(Float)
    health_status = Column(String)
    recommendations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="health_records")


class DetectionSession(Base):
    __tablename__ = "detection_sessions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    session_type = Column(String)  # voice_health, know_health, medi_chat
    status = Column(String, default="pending")  # pending, processing, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    user = relationship("User", back_populates="detection_sessions")


class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    consultation_type = Column(String)  # ai_agent, knowledge_graph, diagnosis
    query = Column(Text)
    response = Column(Text)
    context = Column(JSON)
    satisfaction_rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="consultations")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    plan = Column(String)
    amount = Column(Float)
    currency = Column(String, default="CNY")
    payment_method = Column(String)
    transaction_id = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="subscriptions")


class HealthMetric(Base):
    __tablename__ = "health_metrics"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    metric_type = Column(String)  # heart_rate, blood_pressure, blood_sugar, etc.
    value = Column(Float)
    unit = Column(String)
    source = Column(String)  # manual, device, api
    recorded_at = Column(DateTime, default=datetime.utcnow)


class InterventionPlan(Base):
    __tablename__ = "intervention_plans"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    plan_name = Column(String)
    description = Column(Text)
    goals = Column(JSON)
    actions = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    progress = Column(Float, default=0.0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
