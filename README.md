# AI健康平台

> 基于多模态AI检测的个性化健康管理平台

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-48%20passed-brightgreen.svg)]()

## 🚀 核心功能

### 🎤 多模态健康检测
- **语音分析**：59维声学特征，评估神经系统、呼吸系统、心血管健康
- **面部分析**：6维面部特征，分析肤色、眼睛、唇色、对称性
- **综合评估**：中医体质诊断、营养需求分析

### 💊 AI营养配方引擎
- **知识图谱**：120+营养成分，智能匹配
- **个性化配方**：千人千面，基于健康数据定制
- **持续优化**：根据反馈自动调整

### 🤖 智能健康助手
- **小和**（协调员）：意图识别与任务路由
- **小译**（翻译）：医学术语解释、报告解读
- **小结**（总结）：健康报告生成、数据分析
- **小智**（顾问）：营养建议、产品咨询

## 📦 快速开始

```bash
# 克隆项目
git clone https://github.com/MoKangMedical/ai-health-platform.git
cd ai-health-platform

# 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动服务
python -m src.api.main
```

## 🌐 在线演示

- **GitHub Pages**: https://mokangmedical.github.io/ai-health-platform
- **在线演示**: https://mokangmedical.github.io/ai-health-platform/demo.html
- **API文档**: https://mokangmedical.github.io/ai-health-platform/api.html

## 📊 项目统计

| 指标 | 数值 |
|------|------|
| Python代码 | 5,834行 |
| HTML代码 | 4,529行 |
| 测试用例 | 48个 |
| API端点 | 20+ |
| AI Agent | 4个 |

## 🏗️ 技术栈

- **后端**：FastAPI + SQLAlchemy + Pydantic
- **AI**：PyTorch + Transformers + 自研多模态模型
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **缓存**：Redis
- **部署**：Docker + Docker Compose + Nginx

## 📚 文档

- [功能详情](https://mokangmedical.github.io/ai-health-platform/features.html)
- [系统架构](https://mokangmedical.github.io/ai-health-platform/architecture.html)
- [API文档](https://mokangmedical.github.io/ai-health-platform/api.html)
- [快速开始](https://mokangmedical.github.io/ai-health-platform/getting-started.html)
- [更新日志](https://mokangmedical.github.io/ai-health-platform/changelog.html)
- [技术白皮书](https://github.com/MoKangMedical/ai-health-platform/blob/main/docs/WHITEPAPER.md)

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 测试结果
================== 48 passed, 1 skipped ==================
```

## 📁 项目结构

```
ai-health-platform/
├── src/
│   ├── api/           # FastAPI路由和中间件
│   ├── core/          # 核心业务逻辑
│   ├── agents/        # AI Agent系统
│   ├── models/        # 数据模型
│   └── utils/         # 工具函数
├── templates/         # HTML模板
├── tests/             # 测试用例
├── docs/              # 文档
├── config/            # 配置文件
├── Dockerfile         # Docker镜像
└── requirements.txt   # 依赖清单
```

## 🤝 贡献

欢迎贡献代码！请查看 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📧 联系方式

- GitHub: [MoKangMedical](https://github.com/MoKangMedical)
- Issues: [提交问题](https://github.com/MoKangMedical/ai-health-platform/issues)
