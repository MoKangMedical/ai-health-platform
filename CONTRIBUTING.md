# 贡献指南

感谢您对AI健康平台项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 1. 提交问题

如果您发现了bug或有功能建议，请在 [GitHub Issues](https://github.com/MoKangMedical/ai-health-platform/issues) 提交。

### 2. 提交代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 3. 代码规范

- Python代码遵循 PEP 8 规范
- 添加适当的注释和文档
- 确保所有测试通过

### 4. 提交规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型(type):
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

## 开发环境

```bash
# 克隆项目
git clone https://github.com/MoKangMedical/ai-health-platform.git
cd ai-health-platform

# 创建虚拟环境
python3.12 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/ -v

# 启动服务
python -m src.api.main
```

## 联系方式

如有任何问题，请通过 GitHub Issues 联系我们。

感谢您的贡献！
