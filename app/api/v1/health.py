"""
AI Health Platform - API Routes: Health Detection & Analysis
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User
from ...schemas.schemas import (
    VoiceDetectionRequest, VoiceDetectionResponse,
    KnowledgeQueryRequest, KnowledgeQueryResponse,
    DiagnosisRequest, DiagnosisResponse,
    HealthRecordCreate, HealthRecordResponse,
    InterventionPlanCreate, InterventionPlanResponse,
    BusinessLoopRequest, BusinessLoopResponse
)
from ...services.health_service import health_service

router = APIRouter(prefix="/health", tags=["Health Detection & Analysis"])


# ==================== DETECTION ENDPOINTS ====================

@router.post("/detect/voice", response_model=VoiceDetectionResponse)
async def detect_voice_health(
    request: VoiceDetectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Voice-based health detection using VoiceHealth service"""
    if current_user.api_calls_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API调用次数已用完，请升级订阅计划"
        )
    
    result = await health_service.voice_detection(
        db=db,
        user=current_user,
        audio_data=request.audio_base64,
        audio_url=request.audio_url,
        detection_type=request.detection_type
    )
    
    return result


@router.post("/analyze/knowledge", response_model=KnowledgeQueryResponse)
async def analyze_knowledge(
    request: KnowledgeQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Knowledge-based health analysis using KnowHealth service"""
    if current_user.api_calls_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API调用次数已用完，请升级订阅计划"
        )
    
    result = await health_service.knowledge_analysis(
        db=db,
        user=current_user,
        query=request.query,
        context=request.context
    )
    
    return result


@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(
    request: DiagnosisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI-powered diagnosis using MediChat-RD service"""
    if current_user.api_calls_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API调用次数已用完，请升级订阅计划"
        )
    
    result = await health_service.ai_diagnosis(
        db=db,
        user=current_user,
        symptoms=request.symptoms,
        patient_info=request.patient_info,
        medical_history=request.medical_history
    )
    
    return result


# ==================== AI CHAT ENDPOINT ====================

@router.post("/chat")
async def chat_with_ai(
    message: str,
    conversation_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI health agent"""
    if current_user.api_calls_remaining <= 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API调用次数已用完，请升级订阅计划"
        )
    
    result = await health_service.ai_chat(
        db=db,
        user=current_user,
        message=message,
        conversation_id=conversation_id
    )
    
    return result


# ==================== BUSINESS LOOP ENDPOINT ====================

@router.post("/business-loop", response_model=BusinessLoopResponse)
async def complete_business_loop(
    request: BusinessLoopRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Complete business loop: Detection -> Analysis -> Intervention -> Tracking
    
    This endpoint orchestrates the entire health management workflow:
    1. Detection (VoiceHealth)
    2. Analysis (KnowHealth + MediChat-RD)
    3. Intervention (Auto-generated plan)
    4. Tracking (Progress monitoring)
    """
    if current_user.api_calls_remaining < 3:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="API调用次数不足（需要至少3次），请升级订阅计划"
        )
    
    result = await health_service.complete_business_loop(
        db=db,
        user=current_user,
        detection_type=request.detection_type,
        input_data=request.input_data,
        auto_intervention=request.auto_intervention
    )
    
    return result


# ==================== HEALTH RECORDS ENDPOINTS ====================

@router.get("/records", response_model=List[HealthRecordResponse])
async def get_health_records(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's health records"""
    from ...models.user import HealthRecord
    
    records = db.query(HealthRecord).filter(
        HealthRecord.user_id == current_user.id
    ).order_by(
        HealthRecord.created_at.desc()
    ).offset(offset).limit(limit).all()
    
    return records


@router.get("/records/{record_id}", response_model=HealthRecordResponse)
async def get_health_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific health record"""
    from ...models.user import HealthRecord
    
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.user_id == current_user.id
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="记录不存在"
        )
    
    return record


# ==================== INTERVENTION PLAN ENDPOINTS ====================

@router.post("/intervention", response_model=InterventionPlanResponse)
async def create_intervention_plan(
    request: InterventionPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new intervention plan"""
    from ...models.user import InterventionPlan
    import uuid
    from datetime import datetime, timedelta
    
    plan = InterventionPlan(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        plan_name=request.plan_name,
        description=request.description,
        goals=request.goals,
        actions=request.actions,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=request.duration_days),
        progress=0.0,
        status="active"
    )
    
    db.add(plan)
    db.commit()
    db.refresh(plan)
    
    return plan


@router.get("/intervention", response_model=List[InterventionPlanResponse])
async def get_intervention_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's intervention plans"""
    from ...models.user import InterventionPlan
    
    plans = db.query(InterventionPlan).filter(
        InterventionPlan.user_id == current_user.id
    ).order_by(InterventionPlan.created_at.desc()).all()
    
    return plans


@router.put("/intervention/{plan_id}/progress")
async def update_intervention_progress(
    plan_id: str,
    metric_type: str,
    value: float,
    unit: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track progress for an intervention plan"""
    result = await health_service.track_progress(
        db=db,
        user=current_user,
        plan_id=plan_id,
        metric_type=metric_type,
        value=value,
        unit=unit
    )
    
    return result


# ==================== HEALTH DASHBOARD ====================

@router.get("/dashboard")
async def get_health_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive health dashboard"""
    result = await health_service.get_health_dashboard(
        db=db,
        user=current_user
    )
    
    return result
