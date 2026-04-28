#!/usr/bin/env python3
"""
AI Health Platform - Startup Script
"""
import uvicorn
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings


def main():
    """Start the AI Health Platform server"""
    print(f"""
╔════════════════════════════════════════════════════════════╗
║           🏥 AI Health Platform - 统一健康管理平台          ║
╠════════════════════════════════════════════════════════════╣
║  整合服务:                                                 ║
║  • VoiceHealth (多模态检测)    → {settings.VOICE_HEALTH_URL:<25} ║
║  • KnowHealth  (AI Agent)      → {settings.KNOW_HEALTH_URL:<25} ║
║  • MediChat-RD (知识图谱)      → {settings.MEDI_CHAT_RD_URL:<25} ║
╠════════════════════════════════════════════════════════════╣
║  🌐 Server: http://{settings.HOST}:{settings.PORT:<35} ║
║  📚 Docs:   http://{settings.HOST}:{settings.PORT}/docs{' ' * 27}║
╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )


if __name__ == "__main__":
    main()
