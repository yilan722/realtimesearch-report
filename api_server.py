"""
深度估值报告系统 - REST API 服务器
使用 FastAPI 提供 RESTful API 接口
运行: uvicorn api_server:app --host 0.0.0.0 --port 8000
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os
import uuid
from datetime import datetime
from main import ValuationReportSystem
import traceback

# 创建 FastAPI 应用
app = FastAPI(
    title="Single Company Deep Analysis API",
    description="提供单公司深度估值分析报告的生成服务 / Single Company Deep Valuation Analysis Report Generation Service",
    version="1.0.0"
)

# 配置 CORS - 允许其他网站调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局系统实例
system = ValuationReportSystem()

# 任务状态存储（简单实现，生产环境建议使用 Redis 或数据库）
task_status = {}


# 请求模型
class ReportRequest(BaseModel):
    """报告生成请求"""
    company: str = Field(..., description="公司名称或股票代码", example="Apple Inc")
    analysis_type: str = Field(default="valuation", description="分析类型", example="valuation")
    report_type: Literal["comprehensive", "quick"] = Field(
        default="comprehensive", 
        description="报告类型：comprehensive=完整报告, quick=快速分析"
    )
    save_to_file: bool = Field(default=False, description="是否保存到文件（API调用通常不需要）")
    generate_pdf: bool = Field(default=False, description="是否生成PDF（会增加处理时间）")
    keep_markdown: bool = Field(default=False, description="是否保留Markdown文件")


class QuickAnalysisRequest(BaseModel):
    """快速分析请求"""
    company: str = Field(..., description="公司名称或股票代码", example="Tesla")


# 响应模型
class ReportResponse(BaseModel):
    """报告生成响应"""
    status: str
    company: str
    report: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    message: str
    timestamp: str


@app.get("/", tags=["基础"])
async def root():
    """API 根路径"""
    return {
        "message": "Single Company Deep Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["基础"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "message": "API服务运行正常",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/generate-report", response_model=ReportResponse, tags=["报告生成"])
async def generate_report(request: ReportRequest):
    """
    生成单公司深度估值分析报告
    
    **参数说明：**
    - `company`: 公司名称或股票代码（必填）
    - `analysis_type`: 分析类型，默认为 "valuation"
    - `report_type`: 报告类型，"comprehensive"（完整报告，2-3分钟）或 "quick"（快速分析，30-60秒）
    - `save_to_file`: 是否保存到文件，默认 False
    - `generate_pdf`: 是否生成PDF，默认 False（会增加处理时间）
    - `keep_markdown`: 是否保留Markdown文件，默认 False
    
    **返回说明：**
    - `status`: "success" 或 "error"
    - `company`: 公司名称
    - `report`: 报告内容（Markdown格式）
    - `metadata`: 元数据（包含耗时、查询数等信息）
    - `error`: 错误信息（如果失败）
    
    **示例请求：**
    ```json
    {
        "company": "Apple Inc",
        "report_type": "comprehensive",
        "generate_pdf": false
    }
    ```
    """
    try:
        print(f"\n{'='*80}")
        print(f"📡 API请求: 生成 {request.company} 的报告")
        print(f"⏰ 请求时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # 调用报告生成系统
        result = system.generate_report(
            company=request.company,
            analysis_type=request.analysis_type,
            report_type=request.report_type,
            save_to_file=request.save_to_file,
            generate_pdf=request.generate_pdf,
            keep_markdown=request.keep_markdown
        )
        
        # 检查结果
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "报告生成失败")
            )
        
        # 返回成功响应
        return ReportResponse(
            status="success",
            company=result.get("company", request.company),
            report=result.get("report"),
            metadata=result.get("metadata")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"❌ API错误: {error_msg}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"报告生成失败: {error_msg}"
        )


@app.post("/api/v1/quick-analysis", tags=["报告生成"])
async def quick_analysis(request: QuickAnalysisRequest):
    """
    快速分析（低成本，30-60秒）
    
    返回快速分析摘要，适合需要快速了解公司投资要点的场景。
    """
    try:
        print(f"\n📡 API请求: 快速分析 {request.company}\n")
        
        # 调用快速分析
        summary = system.quick_analysis(request.company)
        
        return {
            "status": "success",
            "company": request.company,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ 快速分析错误: {error_msg}")
        print(traceback.format_exc())
        
        raise HTTPException(
            status_code=500,
            detail=f"快速分析失败: {error_msg}"
        )


@app.get("/api/v1/download-report/{filename}", tags=["文件下载"])
async def download_report(filename: str):
    """
    下载生成的报告文件（PDF或Markdown）
    
    需要先调用生成报告接口，并设置 `save_to_file=True`
    """
    # 安全检查：防止路径遍历攻击
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="无效的文件名")
    
    file_path = os.path.join("reports", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    
    # 根据文件类型设置 MIME 类型
    if filename.endswith(".pdf"):
        media_type = "application/pdf"
    elif filename.endswith(".md"):
        media_type = "text/markdown"
    else:
        media_type = "application/octet-stream"
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )


# 异步任务支持（可选功能）
@app.post("/api/v1/generate-report-async", tags=["异步任务"])
async def generate_report_async(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    异步生成报告（立即返回任务ID，通过任务ID查询状态）
    
    适合报告生成时间较长的场景，避免HTTP超时。
    """
    task_id = str(uuid.uuid4())
    
    # 初始化任务状态
    task_status[task_id] = {
        "status": "processing",
        "company": request.company,
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    
    def generate_task():
        """后台任务"""
        try:
            result = system.generate_report(
                company=request.company,
                analysis_type=request.analysis_type,
                report_type=request.report_type,
                save_to_file=request.save_to_file,
                generate_pdf=request.generate_pdf,
                keep_markdown=request.keep_markdown
            )
            task_status[task_id]["status"] = "completed"
            task_status[task_id]["result"] = result
        except Exception as e:
            task_status[task_id]["status"] = "failed"
            task_status[task_id]["error"] = str(e)
    
    # 添加到后台任务
    background_tasks.add_task(generate_task)
    
    return {
        "status": "accepted",
        "task_id": task_id,
        "message": "报告生成任务已提交，请使用 task_id 查询状态",
        "check_status_url": f"/api/v1/task-status/{task_id}"
    }


@app.get("/api/v1/task-status/{task_id}", tags=["异步任务"])
async def get_task_status(task_id: str):
    """查询异步任务状态"""
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = task_status[task_id]
    
    if task["status"] == "completed":
        return {
            "status": "completed",
            "task_id": task_id,
            "result": task["result"]
        }
    elif task["status"] == "failed":
        return {
            "status": "failed",
            "task_id": task_id,
            "error": task["error"]
        }
    else:
        return {
            "status": "processing",
            "task_id": task_id,
            "message": "报告生成中，请稍候..."
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

