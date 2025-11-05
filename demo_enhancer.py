#!/usr/bin/env python3
"""
报告增强器演示脚本
展示从生成报告到增强的完整流程
"""

def print_section(title):
    """打印分节标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def demo_enhance_existing():
    """演示：增强现有报告"""
    print_section("演示 1: 增强现有报告")
    
    print("📄 现有报告列表：")
    import glob
    reports = glob.glob("reports/*.md")
    reports = [r for r in reports if '_enhanced' not in r and '_formatted' not in r]
    
    for i, report in enumerate(reports[:3], 1):
        print(f"   {i}. {report}")
    
    print("\n选择一个报告进行增强，或按Enter查看效果展示...")
    choice = input("请输入编号 (或按Enter跳过): ").strip()
    
    if choice and choice.isdigit() and 1 <= int(choice) <= len(reports):
        from report_enhancer import ReportEnhancer
        enhancer = ReportEnhancer()
        
        selected_report = reports[int(choice) - 1]
        print(f"\n🔧 正在增强: {selected_report}")
        
        try:
            enhanced_path = enhancer.enhance_report(selected_report)
            print(f"\n✅ 成功! 增强后的报告: {enhanced_path}")
            print("\n可以使用markdown查看器或VSCode打开查看效果")
        except Exception as e:
            print(f"\n❌ 增强失败: {e}")
    else:
        print("\n跳过实际增强，展示效果对比...")
        show_before_after_comparison()

def show_before_after_comparison():
    """展示增强前后对比"""
    print("\n📊 增强效果对比：")
    print("\n【原始报告 - 损坏的表格】")
    print("-" * 80)
    print("""
MetricQ2 FY2026Q1 FY2026YoY ChangeRevenue$46.7B$44.1B+56%Net Income$26.4B$18.8BNot disclosed
    """.strip())
    
    print("\n" + "="*80)
    print("⬇️  增强器处理  ⬇️")
    print("="*80)
    
    print("\n【增强后 - 正确的表格 + 图表】")
    print("-" * 80)
    print("""
| Metric | Q2 FY2026 | Q1 FY2026 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $46.7B | $44.1B | +56% |
| Net Income | $26.4B | $18.8B | Not disclosed |
| Gross Margin | 72.7% | Not disclosed | Stable |

**图表 1**: 数据可视化

![图表 1](charts/nvda_20251104_161318_chart_0.png)
    """.strip())
    print("-" * 80)

def demo_batch_enhance():
    """演示：批量增强"""
    print_section("演示 2: 批量增强所有报告")
    
    print("批量增强会处理reports/目录下所有未增强的报告")
    print("这可能需要几秒钟到几分钟，取决于报告数量\n")
    
    choice = input("是否执行批量增强? (y/n): ").lower()
    
    if choice == 'y':
        import os
        os.system("python enhance_all_reports.py")
    else:
        print("\n跳过批量增强")

def demo_features():
    """展示增强器功能"""
    print_section("演示 3: 增强器功能一览")
    
    features = [
        ("✅ 表格格式修复", "自动识别损坏的表格并重建为标准markdown格式"),
        ("✅ 数据可视化", "从表格数据生成专业的柱状图"),
        ("✅ HTML清理", "移除 &lt;, &gt; 等HTML实体编码"),
        ("✅ 样式优化", "确保表格列对齐，添加适当空行"),
        ("✅ 智能识别", "支持财务指标、估值比率、市场份额等多种表格"),
        ("✅ 批量处理", "一键增强所有报告"),
    ]
    
    for feature, description in features:
        print(f"{feature}")
        print(f"   → {description}\n")

def demo_generated_charts():
    """展示生成的图表"""
    print_section("演示 4: 查看生成的图表")
    
    import glob
    import os
    
    charts = glob.glob("reports/charts/*.png")
    
    if not charts:
        print("⚠️  还没有生成任何图表")
        print("请先运行增强器处理报告")
        return
    
    print(f"📊 已生成 {len(charts)} 个图表：\n")
    for chart in charts:
        size = os.path.getsize(chart) / 1024  # KB
        print(f"   • {os.path.basename(chart)} ({size:.1f} KB)")
    
    print(f"\n图表保存在: reports/charts/")
    print("可以使用图片查看器或markdown预览打开查看")

def show_usage_tips():
    """显示使用提示"""
    print_section("💡 使用提示")
    
    tips = [
        "1. 增强器不会覆盖原始报告，会创建 _enhanced.md 新文件",
        "2. 可以对同一报告多次运行增强器（会覆盖之前的增强版本）",
        "3. 图表保存在 reports/charts/ 目录",
        "4. 如果表格无法自动解析，会显示为代码块",
        "5. 详细文档请查看：使用报告增强器.md"
    ]
    
    for tip in tips:
        print(f"   {tip}")

def main():
    """主函数"""
    print("\n" + "="*80)
    print("  🎨 报告增强器演示")
    print("  自动修复表格格式 + 生成数据可视化图表")
    print("="*80)
    
    demos = [
        ("增强现有报告", demo_enhance_existing),
        ("批量增强所有报告", demo_batch_enhance),
        ("功能一览", demo_features),
        ("查看生成的图表", demo_generated_charts),
        ("使用提示", show_usage_tips),
    ]
    
    while True:
        print("\n" + "-"*80)
        print("选择演示:")
        for i, (name, _) in enumerate(demos, 1):
            print(f"  {i}. {name}")
        print("  0. 退出")
        print("-"*80)
        
        choice = input("\n请选择 (0-5): ").strip()
        
        if choice == "0":
            print("\n👋 感谢使用报告增强器!")
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                name, func = demos[idx]
                func()
                input("\n按 Enter 继续...")
            else:
                print("❌ 无效选择，请输入 0-5")
        except ValueError:
            print("❌ 请输入数字")
        except KeyboardInterrupt:
            print("\n\n操作被用户中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            input("\n按 Enter 继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见!")

