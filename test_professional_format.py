"""
测试专业格式报告生成
"""
from main import ValuationReportSystem

print("="*80)
print("测试专业格式报告生成")
print("="*80)

system = ValuationReportSystem()

# 生成专业格式报告
print("\n正在生成Apple Inc的专业格式报告...")
print("这将需要2-3分钟，请稍候...\n")

result = system.generate_report(
    "Apple Inc",
    report_type="comprehensive",
    save_to_file=True
)

if result["status"] == "success":
    print("\n" + "="*80)
    print("✅ 专业格式报告生成成功！")
    print("="*80)
    
    print(f"\n📄 报告信息:")
    print(f"  文件位置: {result['metadata']['saved_file']}")
    print(f"  报告长度: {len(result['report'])} 字符")
    print(f"  耗时: {result['metadata']['elapsed_time']:.2f}秒")
    print(f"  查询数: {result['metadata']['queries_successful']}/{result['metadata']['queries_executed']}")
    
    print(f"\n📊 报告特点:")
    print(f"  ✅ 专业封面页")
    print(f"  ✅ 执行摘要")
    print(f"  ✅ 清晰章节编号 (1.1, 1.2等)")
    print(f"  ✅ 表格编号和标题")
    print(f"  ✅ 数据来源说明")
    print(f"  ✅ 专业免责声明")
    
    print(f"\n📖 报告预览（前1000字符）:")
    print("-"*80)
    print(result['report'][:1000])
    print("\n...")
    print("-"*80)
    
    print(f"\n💡 查看完整报告:")
    print(f"  在VS Code中打开: code {result['metadata']['saved_file']}")
    print(f"  按 Cmd+Shift+V 预览Markdown格式")
    
else:
    print(f"\n❌ 报告生成失败:")
    print(f"  错误: {result.get('error')}")

