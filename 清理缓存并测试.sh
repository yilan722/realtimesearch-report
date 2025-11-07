#!/bin/bash

echo "=========================================="
echo "🧹 清理Python缓存并测试"
echo "=========================================="
echo ""

# 清理 __pycache__ 目录
echo "1️⃣ 清理 __pycache__ 缓存..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "   ✅ __pycache__ 已清理"

# 清理 .pyc 文件
echo ""
echo "2️⃣ 清理 .pyc 文件..."
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "   ✅ .pyc 文件已清理"

# 清理 .pyo 文件
echo ""
echo "3️⃣ 清理 .pyo 文件..."
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "   ✅ .pyo 文件已清理"

echo ""
echo "=========================================="
echo "✅ 缓存清理完成！"
echo "=========================================="
echo ""
echo "现在运行测试..."
echo ""

# 运行测试
python test_backward_compat.py

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="

