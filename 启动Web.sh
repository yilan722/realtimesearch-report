#!/bin/bash
# 深度估值报告系统 - Web界面启动脚本

echo "======================================"
echo "  深度估值报告系统 - Web界面"
echo "======================================"
echo ""

# 检查是否安装了streamlit
if ! command -v streamlit &> /dev/null
then
    echo "⚠️  检测到未安装 streamlit，正在安装..."
    pip install streamlit
fi

echo "🚀 正在启动Web服务..."
echo ""
echo "访问地址: http://localhost:8501"
echo ""
echo "💡 提示: 按 Ctrl+C 停止服务"
echo ""

# 启动streamlit
streamlit run web_app.py

