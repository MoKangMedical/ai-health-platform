"""数据可视化模块"""

import json
from typing import Dict, List

def generate_health_score_chart(score: float, history: List[Dict] = None) -> str:
    """生成健康评分图表HTML"""
    
    # 评分等级
    if score >= 90:
        level, color, bg = "优秀", "#22c55e", "rgba(34,197,94,0.2)"
    elif score >= 80:
        level, color, bg = "良好", "#00d4ff", "rgba(0,212,255,0.2)"
    elif score >= 70:
        level, color, bg = "一般", "#f59e0b", "rgba(245,158,11,0.2)"
    else:
        level, color, bg = "需关注", "#ef4444", "rgba(239,68,68,0.2)"
    
    # 历史趋势数据
    if not history:
        history = [
            {"date": "1周前", "score": 72},
            {"date": "5天前", "score": 75},
            {"date": "3天前", "score": 78},
            {"date": "昨天", "score": 80},
            {"date": "今天", "score": score}
        ]
    
    return f"""
    <div style="display:flex; gap:30px; flex-wrap:wrap;">
        <!-- 评分圆环 -->
        <div style="flex:0 0 200px; text-align:center;">
            <svg width="200" height="200" viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="85" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="12"/>
                <circle cx="100" cy="100" r="85" fill="none" stroke="{color}" stroke-width="12" 
                    stroke-dasharray="{score * 5.34} 534" stroke-linecap="round"
                    transform="rotate(-90 100 100)" style="transition: stroke-dasharray 1s ease-out;"/>
                <text x="100" y="95" text-anchor="middle" fill="{color}" font-size="48" font-weight="800">{score:.0f}</text>
                <text x="100" y="125" text-anchor="middle" fill="#94a3b8" font-size="14">{level}</text>
            </svg>
        </div>
        
        <!-- 趋势折线图 -->
        <div style="flex:1; min-width:300px;">
            <div style="font-size:16px; font-weight:600; margin-bottom:16px;">健康趋势</div>
            <svg width="100%" height="150" viewBox="0 0 400 150">
                <!-- 网格线 -->
                <line x1="0" y1="37" x2="400" y2="37" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
                <line x1="0" y1="75" x2="400" y2="75" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
                <line x1="0" y1="112" x2="400" y2="112" stroke="rgba(255,255,255,0.05)" stroke-width="1"/>
                
                <!-- 趋势线 -->
                <polyline points="0,{150 - history[0]['score'] * 1.5} 100,{150 - history[1]['score'] * 1.5} 200,{150 - history[2]['score'] * 1.5} 300,{150 - history[3]['score'] * 1.5} 400,{150 - history[4]['score'] * 1.5}" 
                    fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                
                <!-- 数据点 -->
                {"".join(f'<circle cx="{i*100}" cy="{150 - h["score"] * 1.5}" r="5" fill="{color}"/>' for i, h in enumerate(history))}
                
                <!-- 标签 -->
                {"".join(f'<text x="{i*100}" y="145" text-anchor="middle" fill="#94a3b8" font-size="11">{h["date"]}</text>' for i, h in enumerate(history))}
            </svg>
        </div>
    </div>
    """


def generate_risk_chart(risks: List[Dict]) -> str:
    """生成风险评估图表"""
    if not risks:
        risks = [
            {"name": "心血管", "level": "low", "score": 85},
            {"name": "呼吸系统", "level": "low", "score": 90},
            {"name": "神经系统", "level": "low", "score": 88},
            {"name": "消化系统", "level": "medium", "score": 72},
            {"name": "免疫系统", "level": "low", "score": 82}
        ]
    
    colors = {"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"}
    
    bars = ""
    for risk in risks:
        color = colors.get(risk["level"], "#00d4ff")
        score = risk.get("score", 80)
        bars += f"""
        <div style="display:flex; align-items:center; margin-bottom:16px;">
            <div style="width:100px; font-size:13px; color:#94a3b8;">{risk["name"]}</div>
            <div style="flex:1; height:24px; background:rgba(255,255,255,0.05); border-radius:12px; overflow:hidden; margin:0 12px;">
                <div style="width:{score}%; height:100%; background:linear-gradient(90deg, {color}88, {color}); border-radius:12px; transition: width 0.5s ease-out;"></div>
            </div>
            <div style="width:50px; text-align:right; font-size:14px; font-weight:600; color:{color};">{score}</div>
        </div>
        """
    
    return f"""
    <div style="padding:10px 0;">
        {bars}
    </div>
    """


def generate_nutrient_chart(nutrients: Dict) -> str:
    """生成营养需求图表"""
    if not nutrients:
        nutrients = {
            "vitamins": ["维生素C", "维生素D", "B族维生素"],
            "minerals": ["镁", "锌", "铁"],
            "others": ["Omega-3", "胶原蛋白"]
        }
    
    colors = {
        "vitamins": "#00d4ff",
        "minerals": "#7c3aed",
        "others": "#22c55e"
    }
    
    html = '<div style="display:flex; flex-wrap:wrap; gap:16px;">'
    
    for category, items in nutrients.items():
        color = colors.get(category, "#94a3b8")
        html += f"""
        <div style="flex:1; min-width:200px; background:rgba(0,0,0,0.2); border-radius:12px; padding:20px; border-left:3px solid {color};">
            <div style="font-size:14px; font-weight:600; color:{color}; margin-bottom:12px; text-transform:uppercase;">{category}</div>
        """
        for item in items:
            html += f'<div style="padding:8px 0; border-bottom:1px solid rgba(255,255,255,0.05); font-size:14px;">{item}</div>'
        html += "</div>"
    
    html += "</div>"
    return html


def generate_tcm_radar(scores: Dict) -> str:
    """生成中医体质雷达图"""
    if not scores:
        scores = {
            "平和质": 85,
            "气虚质": 72,
            "阳虚质": 68,
            "阴虚质": 65,
            "痰湿质": 60,
            "湿热质": 55,
            "血瘀质": 50,
            "气郁质": 45,
            "特禀质": 40
        }
    
    # 计算雷达图坐标
    import math
    n = len(scores)
    center_x, center_y = 150, 150
    radius = 100
    
    points = []
    labels = []
    for i, (name, score) in enumerate(scores.items()):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = center_x + radius * (score / 100) * math.cos(angle)
        y = center_y + radius * (score / 100) * math.sin(angle)
        points.append(f"{x},{y}")
        
        label_x = center_x + (radius + 20) * math.cos(angle)
        label_y = center_y + (radius + 20) * math.sin(angle)
        labels.append(f'<text x="{label_x}" y="{label_y}" text-anchor="middle" fill="#94a3b8" font-size="11">{name}</text>')
    
    # 背景网格
    grid = ""
    for r in [0.25, 0.5, 0.75, 1.0]:
        grid_points = []
        for i in range(n):
            angle = 2 * math.pi * i / n - math.pi / 2
            x = center_x + radius * r * math.cos(angle)
            y = center_y + radius * r * math.sin(angle)
            grid_points.append(f"{x},{y}")
        grid += f'<polygon points="{" ".join(grid_points)}" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>'
    
    return f"""
    <svg width="300" height="300" viewBox="0 0 300 300">
        {grid}
        <polygon points="{" ".join(points)}" fill="rgba(0,212,255,0.2)" stroke="#00d4ff" stroke-width="2"/>
        {"".join(labels)}
    </svg>
    """


def generate_timeline(events: List[Dict]) -> str:
    """生成时间线"""
    if not events:
        events = [
            {"date": "2025-04-27", "title": "AI健康检测", "desc": "完成综合健康检测", "icon": "📊"},
            {"date": "2025-04-20", "title": "营养配方更新", "desc": "根据反馈调整配方", "icon": "💊"},
            {"date": "2025-04-15", "title": "健康咨询", "desc": "与AI助手讨论睡眠问题", "icon": "🤖"}
        ]
    
    html = '<div style="position:relative; padding-left:30px;">'
    html += '<div style="position:absolute; left:15px; top:0; bottom:0; width:2px; background:rgba(255,255,255,0.1);"></div>'
    
    for event in events:
        html += f"""
        <div style="position:relative; margin-bottom:24px; padding-left:30px;">
            <div style="position:absolute; left:-22px; top:0; width:32px; height:32px; background:linear-gradient(135deg, #00d4ff, #7c3aed); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:14px;">
                {event.get('icon', '📌')}
            </div>
            <div style="background:rgba(255,255,255,0.05); border-radius:12px; padding:16px;">
                <div style="font-size:12px; color:#94a3b8; margin-bottom:4px;">{event['date']}</div>
                <div style="font-weight:600; margin-bottom:4px;">{event['title']}</div>
                <div style="font-size:14px; color:#94a3b8;">{event['desc']}</div>
            </div>
        </div>
        """
    
    html += "</div>"
    return html
