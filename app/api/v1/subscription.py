"""
AI Health Platform - API Routes: Subscription Management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...core.security import get_current_user
from ...models.user import User, Subscription
from ...schemas.schemas import SubscriptionCreate, SubscriptionResponse
from ...services.health_service import health_service

router = APIRouter(prefix="/subscription", tags=["Subscription Management"])


@router.post("/create", response_model=SubscriptionResponse)
async def create_subscription(
    request: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or upgrade subscription plan"""
    
    # Validate plan
    valid_plans = ["free", "basic", "premium", "enterprise"]
    if request.plan not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"无效的订阅计划，可选: {', '.join(valid_plans)}"
        )
    
    # Check if downgrading
    plan_hierarchy = {"free": 0, "basic": 1, "premium": 2, "enterprise": 3}
    current_level = plan_hierarchy.get(current_user.subscription_plan, 0)
    new_level = plan_hierarchy.get(request.plan, 0)
    
    if new_level < current_level:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能降级订阅计划，请联系客服处理"
        )
    
    result = await health_service.create_subscription(
        db=db,
        user=current_user,
        plan=request.plan,
        payment_method=request.payment_method
    )
    
    return result


@router.get("/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current subscription details"""
    from datetime import datetime
    
    return {
        "plan": current_user.subscription_plan,
        "api_calls_remaining": current_user.api_calls_remaining,
        "expires": current_user.subscription_expires.isoformat() if current_user.subscription_expires else None,
        "is_active": current_user.subscription_expires is None or current_user.subscription_expires > datetime.utcnow()
    }


@router.get("/history", response_model=List[SubscriptionResponse])
async def get_subscription_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get subscription history"""
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).order_by(Subscription.created_at.desc()).all()
    
    return subscriptions


@router.get("/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "id": "free",
                "name": "免费版",
                "price": 0,
                "currency": "CNY",
                "api_calls": 5,
                "features": [
                    "基础健康检测",
                    "AI健康问答（5次/月）",
                    "基础健康报告"
                ]
            },
            {
                "id": "basic",
                "name": "基础版",
                "price": 99,
                "currency": "CNY",
                "api_calls": 50,
                "features": [
                    "完整健康检测",
                    "AI健康问答（50次/月）",
                    "详细健康报告",
                    "干预计划",
                    "健康趋势分析"
                ]
            },
            {
                "id": "premium",
                "name": "高级版",
                "price": 299,
                "currency": "CNY",
                "api_calls": 500,
                "features": [
                    "全部检测功能",
                    "无限AI健康问答",
                    "高级健康报告",
                    "个性化干预计划",
                    "实时健康监测",
                    "专家咨询预约",
                    "家庭成员共享（3人）"
                ]
            },
            {
                "id": "enterprise",
                "name": "企业版",
                "price": 999,
                "currency": "CNY",
                "api_calls": 9999,
                "features": [
                    "全部高级版功能",
                    "API接口访问",
                    "定制化健康方案",
                    "专属客服支持",
                    "数据导出",
                    "团队管理",
                    "白标解决方案"
                ]
            }
        ]
    }
