"""
调试脚本 - 详细测试每个步骤
"""
from main import ValuationReportSystem

print("="*80)
print("详细调试测试")
print("="*80)

system = ValuationReportSystem()

# 测试1: 查询规划
print("\n【步骤1】测试查询规划...")
try:
    query_plan = system.query_planner.generate_search_plan("Apple Inc")
    print(f"✅ 查询规划状态: {query_plan.get('status')}")
    print(f"   公司: {query_plan.get('company')}")
    if 'plan' in query_plan:
        queries = query_plan['plan'].get('queries', [])
        print(f"   查询数量: {len(queries)}")
        print(f"   查询类型: {type(queries[0]) if queries else 'N/A'}")
        print(f"   前3个查询:")
        for i, q in enumerate(queries[:3], 1):
            if isinstance(q, dict):
                print(f"      {i}. {q.get('purpose')}: {q.get('query')[:50]}...")
            else:
                print(f"      {i}. 查询格式错误，类型: {type(q)}, 内容: {q}")
    else:
        print(f"   ❌ 缺少'plan'字段")
        print(f"   实际返回: {query_plan}")
except Exception as e:
    print(f"❌ 查询规划失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 测试2: 信息收集（使用简化的查询）
print("\n【步骤2】测试信息收集...")
try:
    # 创建一个简单的测试查询计划
    test_plan = {
        "status": "success",
        "company": "Apple Inc",
        "plan": {
            "queries": [
                {
                    "query": "Apple Inc latest financial results 2024",
                    "purpose": "最新财务数据",
                    "priority": "high"
                },
                {
                    "query": "Apple Inc stock price valuation 2024",
                    "purpose": "估值分析",
                    "priority": "high"
                }
            ]
        }
    }
    
    print(f"   使用测试查询计划（2个查询）")
    collection_result = system.information_collector.collect_information(test_plan)
    print(f"✅ 信息收集状态: {collection_result.get('status')}")
    print(f"   成功查询: {collection_result.get('success_count')}/{collection_result.get('total_queries')}")
    
except Exception as e:
    print(f"❌ 信息收集失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 测试3: 格式化信息
print("\n【步骤3】测试信息格式化...")
try:
    formatted_info = system.information_collector.format_for_analysis(collection_result)
    print(f"✅ 格式化成功")
    print(f"   格式化文本长度: {len(formatted_info)} 字符")
    print(f"   前200字符预览:")
    print(f"   {formatted_info[:200]}...")
except Exception as e:
    print(f"❌ 信息格式化失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 测试4: 深度分析
print("\n【步骤4】测试深度分析...")
try:
    print(f"   正在生成报告（这可能需要30-60秒）...")
    analysis_result = system.deep_analyst.generate_quick_summary("Apple Inc", formatted_info[:2000])  # 使用部分信息测试
    print(f"✅ 深度分析状态: {analysis_result.get('status')}")
    if analysis_result.get('status') == 'success':
        summary = analysis_result.get('summary', '')
        print(f"   摘要长度: {len(summary)} 字符")
        print(f"   摘要预览:")
        print(f"   {summary[:300]}...")
    else:
        print(f"   ❌ 错误: {analysis_result.get('error')}")
except Exception as e:
    print(f"❌ 深度分析失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "="*80)
print("✅ 所有步骤测试完成！")
print("="*80)

