# API 快速开始指南

## 🚀 三步启动API服务

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
# 方式1: 使用启动脚本（推荐）
./启动API.sh

# 方式2: 使用uvicorn命令
uvicorn api_server:app --host 0.0.0.0 --port 8000

# 方式3: 直接运行Python
python api_server.py
```

### 3. 访问API文档
打开浏览器访问：`http://localhost:8000/docs`

## 📡 快速测试

### 测试健康检查
```bash
curl http://localhost:8000/health
```

### 生成报告（完整示例）
```bash
curl -X POST "http://localhost:8000/api/v1/generate-report" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Apple Inc",
    "report_type": "comprehensive"
  }'
```

### 使用测试脚本
```bash
python test_api.py
```

## 🔗 前端集成示例

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/v1/generate-report', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    company: 'Apple Inc',
    report_type: 'comprehensive'
  })
});

const data = await response.json();
console.log(data.report); // 报告内容
```

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/generate-report',
    json={'company': 'Apple Inc', 'report_type': 'comprehensive'}
)

data = response.json()
print(data['report'])
```

## 📚 详细文档

查看完整文档：`API使用指南.md`

## ⚙️ 主要API端点

- `POST /api/v1/generate-report` - 生成完整报告（同步）
- `POST /api/v1/quick-analysis` - 快速分析（30-60秒）
- `POST /api/v1/generate-report-async` - 异步生成报告
- `GET /api/v1/task-status/{task_id}` - 查询任务状态
- `GET /api/v1/download-report/{filename}` - 下载报告文件

## 💡 提示

- 完整报告需要2-3分钟，快速分析需要30-60秒
- 如果报告生成时间可能超过HTTP超时，使用异步接口
- 生产环境建议配置HTTPS和API密钥认证

