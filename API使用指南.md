# 深度估值报告系统 - API 使用指南

## 概述

本API提供了单公司深度估值分析报告的生成服务，可以通过HTTP请求调用，方便其他网站或应用集成。

## 快速开始

### 1. 启动API服务器

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
uvicorn api_server:app --host 0.0.0.0 --port 8000

# 或者使用Python直接运行
python api_server.py
```

服务器启动后，你可以：
- 访问 `http://localhost:8000/docs` 查看交互式API文档（Swagger UI）
- 访问 `http://localhost:8000/redoc` 查看ReDoc格式的API文档

### 2. 健康检查

```bash
curl http://localhost:8000/health
```

响应：
```json
{
  "status": "healthy",
  "message": "API服务运行正常",
  "timestamp": "2024-01-15T10:30:00"
}
```

## API 端点

### 1. 生成完整报告（同步）

**端点：** `POST /api/v1/generate-report`

**描述：** 生成单公司深度估值分析报告（完整报告需要2-3分钟）

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/generate-report" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Apple Inc",
    "report_type": "comprehensive",
    "generate_pdf": false
  }'
```

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| company | string | 是 | - | 公司名称或股票代码 |
| analysis_type | string | 否 | "valuation" | 分析类型 |
| report_type | string | 否 | "comprehensive" | 报告类型：`comprehensive`（完整）或 `quick`（快速） |
| save_to_file | boolean | 否 | false | 是否保存到文件 |
| generate_pdf | boolean | 否 | false | 是否生成PDF（会增加处理时间） |
| keep_markdown | boolean | 否 | false | 是否保留Markdown文件 |

**响应示例（成功）：**

```json
{
  "status": "success",
  "company": "Apple Inc",
  "report": "# Apple Inc 估值报告\n\n## Executive Summary\n...",
  "metadata": {
    "analysis_type": "valuation",
    "report_type": "comprehensive",
    "queries_executed": 8,
    "queries_successful": 8,
    "elapsed_time": 145.32,
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

**响应示例（失败）：**

```json
{
  "status": "error",
  "company": "Apple Inc",
  "error": "报告生成失败: 查询规划失败"
}
```

### 2. 快速分析

**端点：** `POST /api/v1/quick-analysis`

**描述：** 快速分析（30-60秒，成本更低）

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/quick-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Tesla"
  }'
```

**响应示例：**

```json
{
  "status": "success",
  "company": "Tesla",
  "summary": "Tesla is a leading electric vehicle manufacturer...",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 3. 异步生成报告

**端点：** `POST /api/v1/generate-report-async`

**描述：** 异步生成报告，立即返回任务ID，适合长时间运行的报告生成

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/v1/generate-report-async" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Apple Inc",
    "report_type": "comprehensive",
    "generate_pdf": true
  }'
```

**响应示例：**

```json
{
  "status": "accepted",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "报告生成任务已提交，请使用 task_id 查询状态",
  "check_status_url": "/api/v1/task-status/550e8400-e29b-41d4-a716-446655440000"
}
```

### 4. 查询任务状态

**端点：** `GET /api/v1/task-status/{task_id}`

**描述：** 查询异步任务的状态和结果

**请求示例：**

```bash
curl "http://localhost:8000/api/v1/task-status/550e8400-e29b-41d4-a716-446655440000"
```

**响应示例（处理中）：**

```json
{
  "status": "processing",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "报告生成中，请稍候..."
}
```

**响应示例（完成）：**

```json
{
  "status": "completed",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "result": {
    "status": "success",
    "company": "Apple Inc",
    "report": "...",
    "metadata": {...}
  }
}
```

### 5. 下载报告文件

**端点：** `GET /api/v1/download-report/{filename}`

**描述：** 下载生成的报告文件（PDF或Markdown）

**注意：** 需要先调用生成报告接口，并设置 `save_to_file=true`

**请求示例：**

```bash
curl "http://localhost:8000/api/v1/download-report/Apple_Inc_20240115_103000.pdf" \
  --output report.pdf
```

## 前端集成示例

### JavaScript (Fetch API)

```javascript
// 生成报告
async function generateReport(company) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/generate-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        company: company,
        report_type: 'comprehensive',
        generate_pdf: false
      })
    });
    
    const data = await response.json();
    
    if (data.status === 'success') {
      console.log('报告生成成功！');
      console.log('报告内容:', data.report);
      console.log('耗时:', data.metadata.elapsed_time, '秒');
      return data;
    } else {
      console.error('报告生成失败:', data.error);
      return null;
    }
  } catch (error) {
    console.error('请求失败:', error);
    return null;
  }
}

// 使用示例
generateReport('Apple Inc').then(result => {
  if (result) {
    // 显示报告
    document.getElementById('report').innerHTML = result.report;
  }
});
```

### Python 客户端

```python
import requests

def generate_report(company, report_type="comprehensive"):
    """调用API生成报告"""
    url = "http://localhost:8000/api/v1/generate-report"
    
    payload = {
        "company": company,
        "report_type": report_type,
        "generate_pdf": False
    }
    
    response = requests.post(url, json=payload)
    data = response.json()
    
    if data.get("status") == "success":
        print(f"✅ {company} 报告生成成功！")
        print(f"⏱️  耗时: {data['metadata']['elapsed_time']:.2f}秒")
        return data
    else:
        print(f"❌ 报告生成失败: {data.get('error')}")
        return None

# 使用示例
result = generate_report("Apple Inc")
if result:
    print(result["report"][:500])  # 打印前500个字符
```

### 异步任务示例（Python）

```python
import requests
import time

def generate_report_async(company):
    """异步生成报告"""
    url = "http://localhost:8000/api/v1/generate-report-async"
    
    # 提交任务
    response = requests.post(url, json={"company": company})
    task = response.json()
    
    if task.get("status") != "accepted":
        print("任务提交失败")
        return None
    
    task_id = task["task_id"]
    print(f"任务已提交，ID: {task_id}")
    
    # 轮询任务状态
    status_url = f"http://localhost:8000/api/v1/task-status/{task_id}"
    
    while True:
        response = requests.get(status_url)
        status = response.json()
        
        if status["status"] == "completed":
            print("✅ 报告生成完成！")
            return status["result"]
        elif status["status"] == "failed":
            print(f"❌ 报告生成失败: {status.get('error')}")
            return None
        else:
            print("⏳ 报告生成中...")
            time.sleep(5)  # 等待5秒后再次查询

# 使用示例
result = generate_report_async("Apple Inc")
if result:
    print(result["report"][:500])
```

## 错误处理

API使用标准的HTTP状态码：

- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 资源不存在（如任务ID或文件）
- `500 Internal Server Error`: 服务器内部错误

错误响应格式：

```json
{
  "detail": "错误描述信息"
}
```

## CORS 配置

API默认允许所有来源的跨域请求（`allow_origins=["*"]`）。在生产环境中，建议修改 `api_server.py` 中的CORS配置，只允许特定域名：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://anotherdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 性能建议

1. **快速分析 vs 完整报告**
   - 快速分析（`report_type: "quick"`）：30-60秒，适合快速了解公司
   - 完整报告（`report_type: "comprehensive"`）：2-3分钟，提供深度分析

2. **异步任务**
   - 如果报告生成时间可能超过HTTP超时时间，使用异步任务接口
   - 定期轮询任务状态（建议间隔5-10秒）

3. **PDF生成**
   - PDF生成会增加处理时间，如果只需要报告内容，设置 `generate_pdf: false`

## 安全建议

1. **生产环境部署**
   - 使用HTTPS
   - 配置适当的CORS策略
   - 添加API密钥认证（可选）
   - 使用反向代理（如Nginx）
   - 限制请求频率（防止滥用）

2. **API密钥认证示例**

如果需要添加API密钥认证，可以修改 `api_server.py`：

```python
from fastapi import Header, HTTPException

API_KEY = "your-secret-api-key"

@app.post("/api/v1/generate-report")
async def generate_report(
    request: ReportRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="无效的API密钥")
    # ... 原有代码
```

## 常见问题

**Q: 报告生成需要多长时间？**
A: 完整报告通常需要2-3分钟，快速分析需要30-60秒。

**Q: 可以同时生成多个报告吗？**
A: 可以，但需要注意API限流和服务器资源。

**Q: 如何获取PDF文件？**
A: 设置 `generate_pdf: true` 和 `save_to_file: true`，然后使用下载接口获取文件。

**Q: 报告内容是什么格式？**
A: 报告内容为Markdown格式，可以直接在网页中渲染。

## 技术支持

如有问题，请查看：
- API文档：`http://localhost:8000/docs`
- 项目README：`README.md`

