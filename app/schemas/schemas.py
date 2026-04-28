"""
AI Health Platform - Pydantic Schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SubscriptionPlan(str, Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: Optional[str]
    subscription_plan: str
    api_calls_remaining: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Health Detection Schemas
class VoiceDetectionRequest(BaseModel):
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    detection_type: str = "general"  # general, respiratory, cardiovascular, mental


class VoiceDetectionResponse(BaseModel):
    session_id: str
    status: str
    results: Optional[Dict[str, Any]] = None
    risk_score: Optional[float] = None
    recommendations: Optional[List[str]] = None


class KnowledgeQueryRequest(BaseModel):
    query: str
    context: Optional[Dict[str, Any]] = None
    language: str = "zh"


class KnowledgeQueryResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float
    related_topics: List[str]


class DiagnosisRequest(BaseModel):
    symptoms: List[str]
    patient_info: Optional[Dict[str, Any]] = None
    medical_history: Optional[List[str]] = None


class DiagnosisResponse(BaseModel):
    session_id: str
    possible_conditions: List[Dict[str, Any]]
    recommended_tests: List[str]
    urgency_level: str
    disclaimer: str


# Subscription Schemas
class SubscriptionCreate(BaseModel):
    plan: SubscriptionPlan
    payment_method: str = "alipay"


class SubscriptionResponse(BaseModel):
    id: str
    plan: str
    amount: float
    start_date: datetime
    end_date: datetime
    status: str


# Health Record Schemas
class HealthRecordCreate(BaseModel):
    record_type: str
    data: Dict[str, Any]


class HealthRecordResponse(BaseModel):
    id: str
    record_type: str
    analysis_result: Dict[str, Any]
    risk_score: float
    health_status: str
    recommendations: List[str]
    created_at: datetime


# Intervention Plan Schemas
class InterventionPlanCreate(BaseModel):
    plan_name: str
    description: Optional[str] = None
    goals: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    duration_days: int = 30


class InterventionPlanResponse(BaseModel):
    id: str
    plan_name: str
    description: Optional[str]
    goals: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    progress: float
    status: str
    start_date: datetime
    end_date: datetime


# Business Loop Schemas
class BusinessLoopRequest(BaseModel):
    """Complete business loop: Detection -> Analysis -> Intervention -> Tracking"""
    detection_type: str
    input_data: Dict[str, Any]
    auto_intervention: bool = True


class BusinessLoopResponse(BaseModel):
    """Response for complete business loop"""
    detection_result: Dict[str, Any]
    analysis_result: Dict[str, Any]
    intervention_plan: Optional[InterventionPlanResponse] = None
    tracking_id: str
    status: str
