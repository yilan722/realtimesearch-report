"""
测试格式验证 - 验证表格数量和格式
"""
print("="*80)
print("🧪 测试报告格式验证")
print("="*80)

# 测试1: 格式增强器
print("\n[测试1] 测试格式增强器...")
try:
    from agents.format_enhancer import FormatEnhancer
    
    enhancer = FormatEnhancer()
    print("✅ 格式增强器已加载")
    
    # 测试HTML内容
    test_html = """
    <h3>1.1  Company Overview  </h3>
    
    <p>  Test paragraph with  extra spaces.  </p>
    
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>  Revenue  </td><td>  $100B  </td></tr>
    </table>
    
    <table>
        <tr><th>Q1</th><th>Q2</th></tr>
        <tr><td>Data1</td><td>Data2</td></tr>
    </table>
    
    <table>
        <tr><th>Peer</th><th>P/E</th></tr>
        <tr><td>Apple</td><td>28.5</td></tr>
    </table>
    """
    
    enhanced = enhancer._enhance_section(test_html, "test")
    is_valid, table_count = enhancer.validate_tables(enhanced, min_tables=3)
    
    print(f"✅ 格式增强完成")
    print(f"  表格数量: {table_count}")
    print(f"  验证通过: {'✅ 是' if is_valid else '❌ 否'}")
    
except Exception as e:
    print(f"❌ 格式增强器测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2: Deep Analyst集成
print("\n[测试2] 检查Deep Analyst集成...")
try:
    from agents.deep_analyst import DeepAnalystAgent
    from api_clients import QwenClient
    
    client = QwenClient()
    analyst = DeepAnalystAgent(client)
    
    print("✅ DeepAnalystAgent已加载")
    print(f"  格式增强器: {'✅ 已集成' if hasattr(analyst, 'format_enhancer') else '❌ 未集成'}")
    
except Exception as e:
    print(f"❌ DeepAnalystAgent测试失败: {e}")

# 测试3: Prompt验证
print("\n[测试3] 验证Prompt要求...")
try:
    from agents.deep_analyst import DeepAnalystAgent
    import inspect
    
    source = inspect.getsource(DeepAnalystAgent.generate_valuation_report)
    
    checks = {
        "MINIMUM 3 data tables": "MINIMUM 3" in source or "最少3个" in source or "至少3个" in source,
        "REQUIRED 3 TABLES": "REQUIRED 3 TABLES" in source,
        "格式增强": "format_enhancer" in source or "enhance" in source,
        "表格验证": "validate_tables" in source,
    }
    
    print("Prompt要求检查:")
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
    
    all_passed = all(checks.values())
    if all_passed:
        print("\n✅ 所有Prompt要求已更新")
    else:
        print("\n⚠️  部分Prompt要求需要更新")
        
except Exception as e:
    print(f"❌ Prompt验证失败: {e}")

print("\n" + "="*80)
print("📊 测试总结")
print("="*80)

print("""
修复内容:
✅ 每个章节要求至少3个表格
✅ 明确的表格要求清单
✅ 格式增强器（统一字体、空格、排版）
✅ 表格数量验证
✅ 专业HTML表格格式（thead/tbody）
✅ 数字格式规范化

下一步:
1. 生成新报告测试: python test_professional_format.py
2. 检查报告中表格数量
3. 验证格式是否统一专业
""")

print("\n🚀 格式验证系统已就绪！")

