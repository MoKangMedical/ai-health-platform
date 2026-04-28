"""
AI Health Platform - Business Logic Service
Orchestrates the complete business loop: Detection -> Analysis -> Intervention -> Tracking
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session
from .clients import voice_health_client, know_health_client, medi_chat_rd_client
from ..models.user import (
    User, HealthRecord, DetectionSession, Consultation, 
    InterventionPlan, HealthMetric, Subscription
)
import logging

logger = logging.getLogger(__name__)


class HealthPlatformService:
    """Main service orchestrating the health platform business logic"""
    
    # ==================== DETECTION PHASE ====================
    
    async def voice_detection(
        self, 
        db: Session, 
        user: User,
        audio_data: Optional[str] = None,
        audio_url: Optional[str] = None,
        detection_type: str = "general"
    ) -> Dict[str, Any]:
        """Phase 1: Voice-based health detection"""
        session_id = str(uuid.uuid4())
        
        # Create detection session
        session = DetectionSession(
            id=session_id,
            user_id=user.id,
            session_type="voice_health",
            status="processing",
            input_data={"detection_type": detection_type}
        )
        db.add(session)
        db.commit()
        
        # Call VoiceHealth service
        start_time = datetime.utcnow()
        result = await voice_health_client.detect_voice_health(
            audio_data=audio_data,
            audio_url=audio_url,
            detection_type=detection_type
        )
        processing_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Update session
        session.status = "completed"
        session.output_data = result
        session.processing_time = processing_time
        session.completed_at = datetime.utcnow()
        
        # Create health record
        record = HealthRecord(
            id=str(uuid.uuid4()),
            user_id=user.id,
            record_type="voice",
            raw_data={"detection_type": detection_type},
            analysis_result=result.get("results", {}),
            risk_score=result.get("risk_score", 0),
            health_status=self._calculate_health_status(result.get("risk_score", 0)),
            recommendations=result.get("recommendations", [])
        )
        db.add(record)
        
        # Update user API calls
        user.api_calls_remaining = max(0, user.api_calls_remaining - 1)
        
        db.commit()
        
        return {
            "session_id": session_id,
            "status": "completed",
            "results": result.get("results", {}),
            "risk_score": result.get("risk_score", 0),
            "health_status": record.health_status,
            "recommendations": result.get("recommendations", []),
            "processing_time": processing_time
        }
    
    # ==================== ANALYSIS PHASE ====================
    
    async def knowledge_analysis(
        self,
        db: Session,
        user: User,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Phase 2: Knowledge-based health analysis"""
        session_id = str(uuid.uuid4())
        
        # Call KnowHealth service
        result = await know_health_client.query_knowledge(query, context)
        
        # Create consultation record
        consultation = Consultation(
            id=session_id,
            user_id=user.id,
            consultation_type="knowledge",
            query=query,
            response=result.get("answer", ""),
            context=context
        )
        db.add(consultation)
        
        # Update user API calls
        user.api_calls_remaining = max(0, user.api_calls_remaining - 1)
        db.commit()
        
        return {
            "session_id": session_id,
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
            "confidence": result.get("confidence", 0),
            "related_topics": result.get("related_topics", [])
        }
    
    async def ai_diagnosis(
        self,
        db: Session,
        user: User,
        symptoms: List[str],
        patient_info: Optional[Dict[str, Any]] = None,
        medical_history: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Phase 2: AI-powered diagnosis"""
        session_id = str(uuid.uuid4())
        
        # Call MediChat-RD service
        result = await medi_chat_rd_client.diagnose(
            symptoms=symptoms,
            patient_info=patient_info or {"user_id": user.id},
            medical_history=medical_history
        )
        
        # Create consultation record
        consultation = Consultation(
            id=session_id,
            user_id=user.id,
            consultation_type="diagnosis",
            query=str(symptoms),
            response=str(result.get("possible_conditions", [])),
            context={"symptoms": symptoms, "patient_info": patient_info}
        )
        db.add(consultation)
        
        # Update user API calls
        user.api_calls_remaining = max(0, user.api_calls_remaining - 1)
        db.commit()
        
        return {
            "session_id": session_id,
            "possible_conditions": result.get("possible_conditions", []),
            "recommended_tests": result.get("recommended_tests", []),
            "urgency_level": result.get("urgency_level", "unknown"),
            "disclaimer": result.get("disclaimer", "")
        }
    
    async def ai_chat(
        self,
        db: Session,
        user: User,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """AI Agent chat for health consultation"""
        result = await know_health_client.chat_with_agent(
            message=message,
            conversation_id=conversation_id,
            user_context={
                "user_id": user.id,
                "subscription": user.subscription_plan
            }
        )
        
        # Update user API calls
        user.api_calls_remaining = max(0, user.api_calls_remaining - 1)
        db.commit()
        
        return {
            "response": result.get("response", ""),
            "conversation_id": result.get("conversation_id", ""),
            "suggestions": result.get("suggestions", [])
        }
    
    # ==================== INTERVENTION PHASE ====================
    
    async def create_intervention_plan(
        self,
        db: Session,
        user: User,
        analysis_result: Dict[str, Any],
        plan_name: Optional[str] = None
    ) -> InterventionPlan:
        """Phase 3: Create intervention plan based on analysis"""
        
        # Generate intervention plan based on analysis
        goals = self._generate_goals(analysis_result)
        actions = self._generate_actions(analysis_result)
        
        plan = InterventionPlan(
            id=str(uuid.uuid4()),
            user_id=user.id,
            plan_name=plan_name or f"健康干预计划 - {datetime.utcnow().strftime('%Y%m%d')}",
            description=f"基于健康分析自动生成的干预计划",
            goals=goals,
            actions=actions,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            progress=0.0,
            status="active"
        )
        db.add(plan)
        db.commit()
        
        return plan
    
    # ==================== TRACKING PHASE ====================
    
    async def track_progress(
        self,
        db: Session,
        user: User,
        plan_id: str,
        metric_type: str,
        value: float,
        unit: str
    ) -> Dict[str, Any]:
        """Phase 4: Track health metrics and intervention progress"""
        
        # Record health metric
        metric = HealthMetric(
            id=str(uuid.uuid4()),
            user_id=user.id,
            metric_type=metric_type,
            value=value,
            unit=unit,
            source="user_input"
        )
        db.add(metric)
        
        # Update intervention plan progress
        plan = db.query(InterventionPlan).filter(
            InterventionPlan.id == plan_id,
            InterventionPlan.user_id == user.id
        ).first()
        
        if plan:
            # Calculate progress based on metrics
            plan.progress = min(100.0, plan.progress + 5.0)
            plan.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "metric_id": metric.id,
            "metric_type": metric_type,
            "value": value,
            "unit": unit,
            "plan_progress": plan.progress if plan else None,
            "recorded_at": datetime.utcnow().isoformat()
        }
    
    # ==================== COMPLETE BUSINESS LOOP ====================
    
    async def complete_business_loop(
        self,
        db: Session,
        user: User,
        detection_type: str,
        input_data: Dict[str, Any],
        auto_intervention: bool = True
    ) -> Dict[str, Any]:
        """
        Complete business loop:
        Detection -> Analysis -> Intervention -> Tracking
        """
        
        # Step 1: Detection
        if detection_type == "voice":
            detection_result = await self.voice_detection(
                db=db,
                user=user,
                audio_data=input_data.get("audio_data"),
                detection_type=input_data.get("subtype", "general")
            )
        else:
            detection_result = {"status": "skipped", "risk_score": 50}
        
        # Step 2: Analysis
        analysis_result = await self.knowledge_analysis(
            db=db,
            user=user,
            query=input_data.get("query", "健康分析"),
            context={"detection_result": detection_result}
        )
        
        # Step 3: Intervention (if auto)
        intervention_plan = None
        if auto_intervention and detection_result.get("risk_score", 0) > 30:
            intervention_plan = await self.create_intervention_plan(
                db=db,
                user=user,
                analysis_result={**detection_result, **analysis_result}
            )
        
        # Step 4: Generate tracking ID
        tracking_id = str(uuid.uuid4())
        
        return {
            "detection_result": detection_result,
            "analysis_result": analysis_result,
            "intervention_plan": {
                "id": intervention_plan.id if intervention_plan else None,
                "name": intervention_plan.plan_name if intervention_plan else None,
                "goals": intervention_plan.goals if intervention_plan else [],
                "actions": intervention_plan.actions if intervention_plan else []
            } if intervention_plan else None,
            "tracking_id": tracking_id,
            "status": "completed"
        }
    
    # ==================== SUBSCRIPTION MANAGEMENT ====================
    
    async def create_subscription(
        self,
        db: Session,
        user: User,
        plan: str,
        payment_method: str = "alipay"
    ) -> Dict[str, Any]:
        """Create or upgrade subscription"""
        
        plan_limits = {
            "free": 5,
            "basic": 50,
            "premium": 500,
            "enterprise": 9999
        }
        
        plan_prices = {
            "free": 0,
            "basic": 99.0,
            "premium": 299.0,
            "enterprise": 999.0
        }
        
        subscription = Subscription(
            id=str(uuid.uuid4()),
            user_id=user.id,
            plan=plan,
            amount=plan_prices.get(plan, 0),
            payment_method=payment_method,
            transaction_id=f"TXN_{uuid.uuid4().hex[:12].upper()}",
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            status="active"
        )
        db.add(subscription)
        
        # Update user subscription
        user.subscription_plan = plan
        user.api_calls_remaining = plan_limits.get(plan, 5)
        user.subscription_expires = subscription.end_date
        
        db.commit()
        
        return {
            "subscription_id": subscription.id,
            "plan": plan,
            "amount": subscription.amount,
            "start_date": subscription.start_date.isoformat(),
            "end_date": subscription.end_date.isoformat(),
            "transaction_id": subscription.transaction_id,
            "api_calls_remaining": user.api_calls_remaining
        }
    
    # ==================== HEALTH DASHBOARD ====================
    
    async def get_health_dashboard(
        self,
        db: Session,
        user: User
    ) -> Dict[str, Any]:
        """Get comprehensive health dashboard data"""
        
        # Get recent health records
        records = db.query(HealthRecord).filter(
            HealthRecord.user_id == user.id
        ).order_by(HealthRecord.created_at.desc()).limit(10).all()
        
        # Get active intervention plans
        plans = db.query(InterventionPlan).filter(
            InterventionPlan.user_id == user.id,
            InterventionPlan.status == "active"
        ).all()
        
        # Get recent metrics
        metrics = db.query(HealthMetric).filter(
            HealthMetric.user_id == user.id
        ).order_by(HealthMetric.recorded_at.desc()).limit(20).all()
        
        # Calculate overall health score
        avg_risk = sum(r.risk_score for r in records) / len(records) if records else 50
        health_score = 100 - avg_risk
        
        return {
            "user_info": {
                "id": user.id,
                "username": user.username,
                "subscription": user.subscription_plan,
                "api_calls_remaining": user.api_calls_remaining
            },
            "health_summary": {
                "health_score": round(health_score, 1),
                "health_status": self._calculate_health_status(avg_risk),
                "total_records": len(records),
                "active_plans": len(plans)
            },
            "recent_records": [
                {
                    "id": r.id,
                    "type": r.record_type,
                    "risk_score": r.risk_score,
                    "status": r.health_status,
                    "date": r.created_at.isoformat()
                } for r in records[:5]
            ],
            "active_plans": [
                {
                    "id": p.id,
                    "name": p.plan_name,
                    "progress": p.progress,
                    "end_date": p.end_date.isoformat()
                } for p in plans
            ],
            "recent_metrics": [
                {
                    "type": m.metric_type,
                    "value": m.value,
                    "unit": m.unit,
                    "date": m.recorded_at.isoformat()
                } for m in metrics[:10]
            ]
        }
    
    # ==================== HELPER METHODS ====================
    
    def _calculate_health_status(self, risk_score: float) -> str:
        if risk_score < 20:
            return "excellent"
        elif risk_score < 40:
            return "good"
        elif risk_score < 60:
            return "fair"
        elif risk_score < 80:
            return "poor"
        else:
            return "critical"
    
    def _generate_goals(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        risk_score = analysis_result.get("risk_score", 50)
        goals = [
            {"name": "降低健康风险", "target": "风险评分降至30以下", "current": risk_score},
            {"name": "改善生活习惯", "target": "建立健康作息", "progress": 0},
            {"name": "定期健康监测", "target": "每周至少检测2次", "progress": 0}
        ]
        return goals
    
    def _generate_actions(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {
                "action": "每日健康检测",
                "description": "使用语音检测功能进行日常健康监测",
                "frequency": "每日",
                "completed": False
            },
            {
                "action": "健康知识学习",
                "description": "通过AI助手了解健康知识",
                "frequency": "每周3次",
                "completed": False
            },
            {
                "action": "症状记录",
                "description": "记录每日身体症状变化",
                "frequency": "每日",
                "completed": False
            },
            {
                "action": "运动计划",
                "description": "按照建议进行适量运动",
                "frequency": "每周5次",
                "completed": False
            }
        ]


# Singleton instance
health_service = HealthPlatformService()
