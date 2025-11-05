"""
使用示例脚本 - 展示系统的各种用法
"""
from main import ValuationReportSystem


def example_1_basic_report():
    """示例1: 生成基本估值报告"""
    print("\n" + "="*80)
    print("示例1: 生成基本估值报告")
    print("="*80)
    
    system = ValuationReportSystem()
    
    result = system.generate_report(
        company="Apple Inc",
        analysis_type="valuation",
        report_type="comprehensive",
        save_to_file=True
    )
    
    if result["status"] == "success":
        print("\n✅ 报告生成成功！")
        print("\n报告预览（前500字符）:")
        print("-"*80)
        print(result["report"][:500])
        print("...")
        print("-"*80)
        print(f"\n完整报告已保存到: {result['metadata']['saved_file']}")
    else:
        print(f"\n❌ 报告生成失败: {result.get('error')}")


def example_2_quick_analysis():
    """示例2: 快速分析模式"""
    print("\n" + "="*80)
    print("示例2: 快速分析模式（成本更低）")
    print("="*80)
    
    system = ValuationReportSystem()
    
    companies = ["Tesla", "BYD", "NIO"]
    
    for company in companies:
        print(f"\n分析 {company}...")
        summary = system.quick_analysis(company)
        print(f"\n{company} 投资要点:")
        print("-"*80)
        print(summary)
        print("-"*80)


def example_3_compare_companies():
    """示例3: 比较分析"""
    print("\n" + "="*80)
    print("示例3: 比较多个公司")
    print("="*80)
    
    system = ValuationReportSystem()
    
    companies = ["Apple", "Microsoft", "Google"]
    
    print(f"\n比较分析: {', '.join(companies)}")
    
    comparison = system.compare_companies(companies)
    
    if comparison["status"] == "success":
        print("\n✅ 比较分析完成！")
        print("\n比较报告:")
        print("-"*80)
        print(comparison["comparison"])
        print("-"*80)
    else:
        print(f"\n❌ 比较分析失败: {comparison.get('error')}")


def example_4_tech_stocks():
    """示例4: 批量分析科技股"""
    print("\n" + "="*80)
    print("示例4: 批量分析科技股")
    print("="*80)
    
    system = ValuationReportSystem()
    
    tech_stocks = [
        "NVIDIA Corporation",
        "Advanced Micro Devices",
        "Intel Corporation"
    ]
    
    results = []
    
    for stock in tech_stocks:
        print(f"\n正在分析: {stock}")
        result = system.generate_report(
            company=stock,
            report_type="comprehensive",
            save_to_file=True
        )
        results.append((stock, result))
    
    print("\n" + "="*80)
    print("批量分析总结")
    print("="*80)
    
    for stock, result in results:
        if result["status"] == "success":
            print(f"✅ {stock}: 成功")
            print(f"   耗时: {result['metadata']['elapsed_time']:.2f}秒")
            print(f"   文件: {result['metadata']['saved_file']}")
        else:
            print(f"❌ {stock}: 失败")


def example_5_custom_analysis():
    """示例5: 自定义分析维度"""
    print("\n" + "="*80)
    print("示例5: 自定义分析（ESG焦点）")
    print("="*80)
    
    system = ValuationReportSystem()
    
    # 可以通过修改查询计划来定制分析维度
    # 这里演示如何生成一个ESG（环境、社会、治理）焦点的报告
    
    company = "Tesla"
    
    print(f"\n为 {company} 生成ESG焦点报告...")
    
    # 首先生成标准报告
    result = system.generate_report(
        company=company,
        analysis_type="valuation",  # 可以扩展为其他类型
        report_type="comprehensive",
        save_to_file=True
    )
    
    if result["status"] == "success":
        print("\n✅ 报告生成成功！")
        print(f"   文件: {result['metadata']['saved_file']}")


def main():
    """运行所有示例"""
    examples = [
        ("基本估值报告", example_1_basic_report),
        ("快速分析模式", example_2_quick_analysis),
        ("比较分析", example_3_compare_companies),
        ("批量分析", example_4_tech_stocks),
        ("自定义分析", example_5_custom_analysis)
    ]
    
    print("\n" + "📚 "*20)
    print("深度估值报告系统 - 使用示例")
    print("📚 "*20)
    
    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n请选择要运行的示例（输入数字，或按Enter运行示例1）:")
    choice = input("> ").strip()
    
    if choice == "":
        choice = "1"
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(examples):
            name, func = examples[idx]
            print(f"\n运行示例: {name}")
            func()
        else:
            print("❌ 无效的选择")
    except ValueError:
        print("❌ 请输入数字")
    except KeyboardInterrupt:
        print("\n\n⚠️  操作被用户中断")


if __name__ == "__main__":
    main()

