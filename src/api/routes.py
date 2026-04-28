"""FastAPI路由"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
import json
import os
import uuid
from datetime import datetime

from src.models.database import get_db, User, HealthRecord, NutrientFormula, Order, ChatHistory
from src.core.health_engine import HealthAssessmentEngine
from src.core.nutrient_engine import NutrientFormulaEngine
from src.agents.agent_system import AgentSystem
from config.settings import settings

router = APIRouter(prefix="/api/v1")

# 初始化引擎
health_engine = HealthAssessmentEngine()
nutrient_engine = NutrientFormulaEngine()
agent_system = AgentSystem()

# ==================== 健康检查 ====================
@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# ==================== 用户管理 ====================
@router.post("/users/register")
async def register_user(
    openid: str = Form(...),
    nickname: str = Form(None),
    phone: str = Form(None),
    db: Session = Depends(get_db)
):
    """用户注册"""
    # 检查用户是否已存在
    existing_user = db.query(User).filter(User.openid == openid).first()
    if existing_user:
        return {"status": "success", "user_id": existing_user.id, "message": "用户已存在"}
    
    # 创建新用户
    user = User(
        openid=openid,
        nickname=nickname,
        phone=phone
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"status": "success", "user_id": user.id, "message": "注册成功"}

@router.get("/users/{user_id}/profile")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """获取用户档案"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": user.id,
        "nickname": user.nickname,
        "phone": user.phone,
        "gender": user.gender,
        "height": user.height,
        "weight": user.weight,
        "tcm_type": user.tcm_type,
        "allergies": user.allergies,
        "health_goals": user.health_goals,
        "subscription": user.subscription
    }

@router.put("/users/{user_id}/profile")
async def update_user_profile(
    user_id: int,
    nickname: Optional[str] = Form(None),
    height: Optional[float] = Form(None),
    weight: Optional[float] = Form(None),
    allergies: Optional[str] = Form(None),
    health_goals: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """更新用户档案"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if nickname:
        user.nickname = nickname
    if height:
        user.height = height
    if weight:
        user.weight = weight
    if allergies:
        user.allergies = json.loads(allergies)
    if health_goals:
        user.health_goals = json.loads(health_goals)
    
    db.commit()
    return {"status": "success", "message": "更新成功"}

# ==================== 健康检测 ====================
@router.post("/detect/voice")
async def detect_voice_health(
    user_id: int = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """语音健康检测"""
    # 保存音频文件
    audio_path = f"{settings.UPLOAD_DIR}/{uuid.uuid4()}.wav"
    with open(audio_path, "wb") as f:
        content = await audio.read()
        f.write(content)
    
    try:
        # 执行语音分析
        result = health_engine.assess_voice_health(audio_path)
        
        # 保存检测记录
        record = HealthRecord(
            user_id=user_id,
            record_type="voice",
            voice_features=result["features"],
            overall_score=result["overall_score"],
            risks=result["risks"]
        )
        db.add(record)
        db.commit()
        
        return {
            "status": "success",
            "record_id": record.id,
            "result": result
        }
    finally:
        # 清理临时文件
        if os.path.exists(audio_path):
            os.remove(audio_path)

@router.post("/detect/face")
async def detect_face_health(
    user_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """面部健康检测"""
    # 保存图片文件
    image_path = f"{settings.UPLOAD_DIR}/{uuid.uuid4()}.jpg"
    with open(image_path, "wb") as f:
        content = await image.read()
        f.write(content)
    
    try:
        # 执行面部分析
        result = health_engine.assess_face_health(image_path)
        
        # 保存检测记录
        record = HealthRecord(
            user_id=user_id,
            record_type="face",
            face_features=result["features"],
            overall_score=result["overall_score"],
            risks=result["risks"]
        )
        db.add(record)
        db.commit()
        
        return {
            "status": "success",
            "record_id": record.id,
            "result": result
        }
    finally:
        # 清理临时文件
        if os.path.exists(image_path):
            os.remove(image_path)

@router.post("/detect/comprehensive")
async def detect_comprehensive_health(
    user_id: int = Form(...),
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """综合健康检测"""
    audio_path = None
    image_path = None
    video_path = None
    
    try:
        # 保存上传文件
        if audio:
            audio_path = f"{settings.UPLOAD_DIR}/{uuid.uuid4()}.wav"
            with open(audio_path, "wb") as f:
                f.write(await audio.read())
        
        if image:
            image_path = f"{settings.UPLOAD_DIR}/{uuid.uuid4()}.jpg"
            with open(image_path, "wb") as f:
                f.write(await image.read())
        
        if video:
            video_path = f"{settings.UPLOAD_DIR}/{uuid.uuid4()}.mp4"
            with open(video_path, "wb") as f:
                f.write(await video.read())
        
        # 执行综合分析
        report = health_engine.assess_comprehensive(
            user_id=user_id,
            audio_path=audio_path,
            image_path=image_path,
            video_path=video_path
        )
        
        # 保存检测记录
        record = HealthRecord(
            user_id=user_id,
            record_type="comprehensive",
            voice_features=report.voice_features.to_dict() if report.voice_features else None,
            face_features=report.face_features.to_dict() if report.face_features else None,
            video_features=report.video_features.to_dict() if report.video_features else None,
            overall_score=report.overall_score,
            health_summary=report.health_summary,
            risks=[r.__dict__ if hasattr(r, '__dict__') else r for r in report.risks],
            recommendations=report.recommended_ingredients,
            tcm_diagnosis=report.tcm_diagnosis.__dict__ if report.tcm_diagnosis else None
        )
        db.add(record)
        db.commit()
        
        return {
            "status": "success",
            "record_id": record.id,
            "report": report.to_dict()
        }
    finally:
        # 清理临时文件
        for path in [audio_path, image_path, video_path]:
            if path and os.path.exists(path):
                os.remove(path)

@router.get("/detect/history/{user_id}")
async def get_detection_history(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取检测历史"""
    records = db.query(HealthRecord)\
        .filter(HealthRecord.user_id == user_id)\
        .order_by(HealthRecord.created_at.desc())\
        .limit(limit)\
        .all()
    
    return {
        "status": "success",
        "records": [
            {
                "id": r.id,
                "type": r.record_type,
                "score": r.overall_score,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    }

# ==================== 营养配方 ====================
@router.post("/formula/generate")
async def generate_formula(
    user_id: int = Form(...),
    health_record_id: int = Form(...),
    questionnaire: str = Form(...),
    db: Session = Depends(get_db)
):
    """生成营养配方"""
    # 获取健康记录
    record = db.query(HealthRecord).filter(HealthRecord.id == health_record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="健康记录不存在")
    
    # 构建健康报告
    health_report = {
        "overall_score": record.overall_score,
        "risks": record.risks or [],
        "nutrient_needs": {},  # 从风险分析中推导
        "tcm_diagnosis": record.tcm_diagnosis or {}
    }
    
    # 从风险中推导营养需求
    for risk in (record.risks or []):
        risk_name = risk.get("name", "")
        if "神经" in risk_name:
            health_report["nutrient_needs"]["神经系统"] = ["B1", "B6", "B12", "镁"]
        elif "呼吸" in risk_name:
            health_report["nutrient_needs"]["呼吸系统"] = ["C", "D", "Omega-3"]
        elif "皮肤" in risk_name:
            health_report["nutrient_needs"]["皮肤健康"] = ["A", "C", "E", "胶原蛋白"]
        elif "免疫" in risk_name:
            health_report["nutrient_needs"]["免疫系统"] = ["C", "D", "锌", "硒"]
    
    # 解析问卷
    questionnaire_data = json.loads(questionnaire)
    
    # 生成配方
    formula = nutrient_engine.generate_formula(health_report, questionnaire_data)
    
    # 保存配方
    db_formula = NutrientFormula(
        user_id=user_id,
        health_record_id=health_record_id,
        formula_name=formula.formula_name,
        ingredients=formula.ingredients,
        dosage={"total": sum(i["dose"] for i in formula.ingredients)},
        instructions=formula.instructions,
        analysis_basis=formula.analysis_basis,
        knowledge_graph_path=formula.knowledge_graph_path
    )
    db.add(db_formula)
    db.commit()
    db.refresh(db_formula)
    
    return {
        "status": "success",
        "formula_id": db_formula.id,
        "formula": formula.to_dict()
    }

@router.get("/formula/{formula_id}")
async def get_formula(formula_id: int, db: Session = Depends(get_db)):
    """获取配方详情"""
    formula = db.query(NutrientFormula).filter(NutrientFormula.id == formula_id).first()
    if not formula:
        raise HTTPException(status_code=404, detail="配方不存在")
    
    return {
        "status": "success",
        "formula": {
            "id": formula.id,
            "name": formula.formula_name,
            "ingredients": formula.ingredients,
            "instructions": formula.instructions,
            "created_at": formula.created_at.isoformat() if formula.created_at else None
        }
    }

@router.get("/formula/user/{user_id}")
async def get_user_formulas(user_id: int, db: Session = Depends(get_db)):
    """获取用户的所有配方"""
    formulas = db.query(NutrientFormula)\
        .filter(NutrientFormula.user_id == user_id)\
        .order_by(NutrientFormula.created_at.desc())\
        .all()
    
    return {
        "status": "success",
        "formulas": [
            {
                "id": f.id,
                "name": f.formula_name,
                "ingredients_count": len(f.ingredients) if f.ingredients else 0,
                "created_at": f.created_at.isoformat() if f.created_at else None
            }
            for f in formulas
        ]
    }

# ==================== AI助手 ====================
@router.post("/agent/chat")
async def chat_with_agent(
    user_id: int = Form(...),
    message: str = Form(...),
    agent_type: str = Form("coordinator"),
    db: Session = Depends(get_db)
):
    """与AI助手对话"""
    # 获取用户上下文
    user = db.query(User).filter(User.id == user_id).first()
    context = {
        "user_id": user_id,
        "user_profile": {
            "nickname": user.nickname if user else None,
            "tcm_type": user.tcm_type if user else None,
            "allergies": user.allergies if user else [],
            "health_goals": user.health_goals if user else []
        }
    }
    
    # 获取最近的健康记录
    recent_record = db.query(HealthRecord)\
        .filter(HealthRecord.user_id == user_id)\
        .order_by(HealthRecord.created_at.desc())\
        .first()
    
    if recent_record:
        context["health_records"] = [{
            "overall_score": recent_record.overall_score,
            "risks": recent_record.risks or [],
            "created_at": recent_record.created_at.isoformat() if recent_record.created_at else None
        }]
    
    # 处理消息
    response = agent_system.process_message(message, agent_type, context)
    
    # 保存对话历史
    chat = ChatHistory(
        user_id=user_id,
        agent_type=agent_type,
        user_message=message,
        agent_response=response.response,
        context=context,
        intent=response.intent,
        confidence=response.confidence
    )
    db.add(chat)
    db.commit()
    
    return {
        "status": "success",
        "response": response.response,
        "agent": response.agent_type,
        "intent": response.intent,
        "confidence": response.confidence,
        "actions": response.actions
    }

@router.get("/agent/info")
async def get_agent_info():
    """获取Agent信息"""
    return {
        "status": "success",
        "agents": agent_system.get_agent_info()
    }

@router.get("/agent/history/{user_id}")
async def get_chat_history(
    user_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取对话历史"""
    chats = db.query(ChatHistory)\
        .filter(ChatHistory.user_id == user_id)\
        .order_by(ChatHistory.created_at.desc())\
        .limit(limit)\
        .all()
    
    return {
        "status": "success",
        "history": [
            {
                "id": c.id,
                "agent": c.agent_type,
                "user_message": c.user_message,
                "agent_response": c.agent_response,
                "intent": c.intent,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in chats
        ]
    }

# ==================== 订单管理 ====================
@router.post("/orders/create")
async def create_order(
    user_id: int = Form(...),
    formula_id: int = Form(...),
    shipping_address: str = Form(...),
    db: Session = Depends(get_db)
):
    """创建订单"""
    # 获取配方
    formula = db.query(NutrientFormula).filter(NutrientFormula.id == formula_id).first()
    if not formula:
        raise HTTPException(status_code=404, detail="配方不存在")
    
    # 获取用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 根据订阅类型确定价格
    price_mapping = {
        "free": 0,
        "basic": 299,
        "pro": 599,
        "enterprise": 999
    }
    amount = price_mapping.get(user.subscription, 299)
    
    # 创建订单
    order = Order(
        user_id=user_id,
        formula_id=formula_id,
        order_no=f"ORD-{uuid.uuid4().hex[:12].upper()}",
        amount=amount,
        status="pending",
        shipping_address=json.loads(shipping_address)
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    return {
        "status": "success",
        "order_id": order.id,
        "order_no": order.order_no,
        "amount": order.amount
    }

@router.get("/orders/{user_id}")
async def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    """获取用户订单"""
    orders = db.query(Order)\
        .filter(Order.user_id == user_id)\
        .order_by(Order.created_at.desc())\
        .all()
    
    return {
        "status": "success",
        "orders": [
            {
                "id": o.id,
                "order_no": o.order_no,
                "amount": o.amount,
                "status": o.status,
                "created_at": o.created_at.isoformat() if o.created_at else None
            }
            for o in orders
        ]
    }

# ==================== 系统信息 ====================
@router.get("/system/info")
async def get_system_info():
    """获取系统信息"""
    return {
        "status": "success",
        "system": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "features": [
                "多模态健康检测",
                "AI营养配方引擎",
                "智能健康管理助手",
                "健康预测与预警"
            ],
            "agents": [
                {"name": "小和", "role": "健康协调员"},
                {"name": "小译", "role": "医学翻译"},
                {"name": "小结", "role": "健康总结"},
                {"name": "小智", "role": "营养顾问"}
            ]
        }
    }
