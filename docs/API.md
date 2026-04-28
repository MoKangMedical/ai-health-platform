# AI健康平台 API文档

## 概述

AI健康平台提供RESTful API，支持多模态健康检测、营养配方生成、AI助手对话等功能。

**Base URL**: `http://localhost:8200/api/v1`

## 认证

当前版本无需认证，后续版本将支持JWT认证。

## API端点

### 1. 健康检查

```
GET /api/v1/health
```

**响应**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-04-27T23:00:00"
}
```

### 2. 用户管理

#### 注册用户
```
POST /api/v1/users/register
Content-Type: application/x-www-form-urlencoded

openid=xxx&nickname=xxx&phone=xxx
```

**响应**:
```json
{
  "status": "success",
  "user_id": 1,
  "message": "注册成功"
}
```

#### 获取用户档案
```
GET /api/v1/users/{user_id}/profile
```

**响应**:
```json
{
  "id": 1,
  "nickname": "用户昵称",
  "phone": "13800138000",
  "height": 175.0,
  "weight": 70.0,
  "tcm_type": "平和质",
  "subscription": "free"
}
```

#### 更新用户档案
```
PUT /api/v1/users/{user_id}/profile
Content-Type: application/x-www-form-urlencoded

nickname=xxx&height=xxx&weight=xxx
```

### 3. 健康检测

#### 语音检测
```
POST /api/v1/detect/voice
Content-Type: multipart/form-data

user_id=1
audio=@audio.wav
```

#### 面部检测
```
POST /api/v1/detect/face
Content-Type: multipart/form-data

user_id=1
image=@image.jpg
```

#### 综合检测
```
POST /api/v1/detect/comprehensive
Content-Type: multipart/form-data

user_id=1
audio=@audio.wav
image=@image.jpg
```

**响应**:
```json
{
  "status": "success",
  "record_id": 1,
  "report": {
    "user_id": 1,
    "overall_score": 85.0,
    "health_summary": "您的整体健康状态良好",
    "risks": [
      {
        "name": "心血管",
        "level": "low",
        "description": "心血管功能正常",
        "suggestions": ["保持规律运动"]
      }
    ],
    "tcm_diagnosis": {
      "primary_type": "平和质",
      "secondary_type": "气虚质",
      "recommendations": ["保持规律作息"]
    },
    "nutrient_needs": {
      "vitamins": ["维生素C", "维生素D"],
      "minerals": ["镁", "锌"]
    },
    "recommended_ingredients": ["抗坏血酸", "甘氨酸镁"]
  }
}
```

#### 获取检测历史
```
GET /api/v1/detect/history/{user_id}?limit=10
```

### 4. 营养配方

#### 生成配方
```
POST /api/v1/formula/generate
Content-Type: application/x-www-form-urlencoded

user_id=1&health_record_id=1&questionnaire={"allergies":[],"health_goals":["提升免疫力"]}
```

**响应**:
```json
{
  "status": "success",
  "formula_id": 1,
  "formula": {
    "formula_name": "个性化免疫增强配方",
    "ingredients": [
      {
        "name": "维生素C",
        "dose": 500,
        "unit": "mg",
        "reason": "支持免疫系统，抗氧化保护"
      }
    ],
    "instructions": "每日建议随餐服用...",
    "timing": "随餐服用，分早晚两次"
  }
}
```

#### 获取配方详情
```
GET /api/v1/formula/{formula_id}
```

#### 获取用户配方列表
```
GET /api/v1/formula/user/{user_id}
```

### 5. AI助手

#### 与Agent对话
```
POST /api/v1/agent/chat
Content-Type: application/x-www-form-urlencoded

user_id=1&message=你好&agent_type=coordinator
```

**Agent类型**:
- `coordinator` - 小和（健康协调员）
- `translator` - 小译（医学翻译）
- `summarizer` - 小结（健康总结）
- `advisor` - 小智（营养顾问）

**响应**:
```json
{
  "status": "success",
  "response": "您好！我是小和，您的AI健康协调员。",
  "agent": "coordinator",
  "intent": "greeting",
  "confidence": 0.95,
  "actions": []
}
```

#### 获取Agent信息
```
GET /api/v1/agent/info
```

#### 获取对话历史
```
GET /api/v1/agent/history/{user_id}?limit=20
```

### 6. 订单管理

#### 创建订单
```
POST /api/v1/orders/create
Content-Type: application/x-www-form-urlencoded

user_id=1&formula_id=1&shipping_address={"name":"xxx","phone":"xxx","address":"xxx"}
```

#### 获取用户订单
```
GET /api/v1/orders/{user_id}
```

### 7. 系统信息

#### 获取系统信息
```
GET /api/v1/system/info
```

**响应**:
```json
{
  "status": "success",
  "system": {
    "name": "AI Health Platform",
    "version": "1.0.0",
    "features": [
      "多模态健康检测",
      "AI营养配方引擎",
      "智能健康管理助手"
    ],
    "agents": [
      {"name": "小和", "role": "健康协调员"},
      {"name": "小译", "role": "医学翻译"},
      {"name": "小结", "role": "健康总结"},
      {"name": "小智", "role": "营养顾问"}
    ]
  }
}
```

## 错误响应

所有错误响应格式：
```json
{
  "status": "error",
  "code": "ERROR_CODE",
  "message": "错误描述"
}
```

**错误代码**:
- `NOT_FOUND` - 资源不存在
- `VALIDATION_ERROR` - 验证错误
- `UNAUTHORIZED` - 未授权
- `INTERNAL_ERROR` - 服务器内部错误

## 限流

- 每个IP每分钟最多100个请求
- 超出限制返回429状态码

## 更新日志

### v1.0.0 (2025-04-27)
- 初始版本发布
- 支持多模态健康检测
- 支持AI营养配方生成
- 支持4个AI Agent对话
