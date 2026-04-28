# AI健康平台 部署指南

## 目录

1. [环境要求](#环境要求)
2. [本地开发](#本地开发)
3. [Docker部署](#docker部署)
4. [生产环境部署](#生产环境部署)
5. [监控与日志](#监控与日志)
6. [常见问题](#常见问题)

---

## 环境要求

### 基础环境
- Python 3.11+
- SQLite 3.35+ 或 PostgreSQL 14+
- Redis 7.0+ (可选)

### 系统依赖
```bash
# macOS
brew install ffmpeg opencv

# Ubuntu/Debian
apt-get install ffmpeg libopencv-dev

# CentOS/RHEL
yum install ffmpeg opencv-devel
```

---

## 本地开发

### 1. 克隆项目
```bash
git clone https://github.com/MoKangMedical/ai-health-platform.git
cd ai-health-platform
```

### 2. 创建虚拟环境
```bash
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库等参数
```

### 5. 初始化数据库
```bash
python -c "from src.models.database import init_db; init_db()"
```

### 6. 运行测试
```bash
python -m pytest tests/ -v
```

### 7. 启动服务
```bash
python -m src.api.main
```

访问 http://localhost:8200 查看首页
访问 http://localhost:8200/docs 查看API文档

---

## Docker部署

### 1. 构建镜像
```bash
docker build -t ai-health-platform .
```

### 2. 运行容器
```bash
docker run -d \
  --name ai-health \
  -p 8200:8200 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/uploads:/app/uploads \
  ai-health-platform
```

### 3. 使用Docker Compose
```bash
docker-compose up -d
```

### 4. 查看日志
```bash
docker logs -f ai-health
```

---

## 生产环境部署

### 1. 使用Gunicorn
```bash
pip install gunicorn

gunicorn src.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8200 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### 2. Nginx配置
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        client_max_body_size 50M;
    }
    
    location /static/ {
        alias /path/to/ai-health-platform/static/;
        expires 30d;
    }
}
```

### 3. SSL配置
```bash
# 安装Certbot
apt-get install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com
```

### 4. Systemd服务
```ini
[Unit]
Description=AI Health Platform
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ai-health-platform
Environment="PATH=/path/to/ai-health-platform/venv/bin"
ExecStart=/path/to/ai-health-platform/venv/bin/gunicorn src.api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8200
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable ai-health
sudo systemctl start ai-health
sudo systemctl status ai-health
```

---

## 监控与日志

### 日志文件
- 应用日志: `logs/YYYY-MM-DD.log`
- 访问日志: `logs/access.log`
- 错误日志: `logs/error.log`

### 健康检查
```bash
curl http://localhost:8200/api/v1/health
```

### 性能监控
```bash
# 查看进程
ps aux | grep gunicorn

# 查看端口
netstat -tlnp | grep 8200

# 查看资源使用
top -p $(pgrep -f gunicorn)
```

---

## 常见问题

### Q: 启动时报错"Address already in use"
A: 端口被占用，修改配置或停止占用进程
```bash
lsof -i :8200
kill -9 <PID>
```

### Q: 数据库初始化失败
A: 检查数据库文件权限
```bash
chmod 666 ai_health.db
```

### Q: 上传文件失败
A: 检查uploads目录权限
```bash
mkdir -p uploads
chmod 777 uploads
```

### Q: 模型加载失败
A: 检查模型文件路径和权限
```bash
ls -la models/
```

---

## 更新与维护

### 更新代码
```bash
git pull origin main
pip install -r requirements.txt
python -c "from src.models.database import init_db; init_db()"
sudo systemctl restart ai-health
```

### 备份数据
```bash
# 备份数据库
cp ai_health.db backups/ai_health_$(date +%Y%m%d).db

# 备份上传文件
tar -czf backups/uploads_$(date +%Y%m%d).tar.gz uploads/
```

### 恢复数据
```bash
# 恢复数据库
cp backups/ai_health_20250427.db ai_health.db

# 恢复上传文件
tar -xzf backups/uploads_20250427.tar.gz
```

---

## 技术支持

- GitHub Issues: https://github.com/MoKangMedical/ai-health-platform/issues
- 邮箱: support@aihealth.com
- 文档: http://localhost:8200/docs
