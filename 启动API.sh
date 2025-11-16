#!/bin/bash

# 深度估值报告系统 - API服务器启动脚本

echo "🚀 启动深度估值报告系统 API 服务器..."
echo ""

# 检查是否安装了依赖
if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  检测到缺少依赖，正在安装..."
    pip install -r requirements.txt
fi

# 启动服务器
echo "📡 API服务器启动中..."
echo "📍 访问地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "📖 ReDoc文档: http://localhost:8000/redoc"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload

