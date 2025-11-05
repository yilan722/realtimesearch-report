#!/bin/bash
# 快速查看报告增强效果

echo "================================"
echo "  📊 报告增强效果查看工具"
echo "================================"
echo ""

# 检查是否有增强报告
enhanced_reports=(reports/*_enhanced.md)

if [ ! -e "${enhanced_reports[0]}" ]; then
    echo "⚠️  还没有增强过的报告"
    echo ""
    echo "请先运行："
    echo "  python enhance_all_reports.py"
    echo ""
    exit 1
fi

echo "✅ 找到增强后的报告："
echo ""

for report in reports/*_enhanced.md; do
    basename "$report"
done

echo ""
echo "生成的图表："
echo ""

if [ -d "reports/charts" ]; then
    ls -lh reports/charts/*.png 2>/dev/null | awk '{print "  📊 " $9 " (" $5 ")"}'
else
    echo "  (暂无图表)"
fi

echo ""
echo "================================"
echo ""
echo "查看方式："
echo ""
echo "1. 使用VSCode打开："
echo "   code reports/nvda_20251104_161318_enhanced.md"
echo ""
echo "2. 使用Markdown查看器："
echo "   open reports/nvda_20251104_161318_enhanced.md"
echo ""
echo "3. 在浏览器中查看（需要Markdown预览插件）"
echo ""
echo "================================"

