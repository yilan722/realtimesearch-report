"""
系统测试脚本
"""
import sys
from main import ValuationReportSystem


def test_api_connections():
    """测试API连接"""
    print("="*80)
    print("测试1: API连接测试")
    print("="*80)
    
    try:
        system = ValuationReportSystem()
        
        # 测试Qwen API
        print("\n测试Qwen3-Max API...")
        response = system.qwen_client.simple_prompt(
            "请说'API连接成功'",
            max_tokens=50
        )
        print(f"✅ Qwen API: {response}")
        
        # 测试Sonar API
        print("\n测试Sonar API...")
        result = system.sonar_client.search("test query")
        if result["status"] == "success":
            print(f"✅ Sonar API: 连接成功")
        else:
            print(f"❌ Sonar API: {result.get('error', '未知错误')}")
        
        return True
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False


def test_query_planning():
    """测试查询规划"""
    print("\n" + "="*80)
    print("测试2: 查询规划测试")
    print("="*80)
    
    try:
        system = ValuationReportSystem()
        
        print("\n生成查询计划...")
        query_plan = system.query_planner.generate_search_plan("Apple Inc")
        
        if query_plan["status"] == "success":
            print(f"✅ 查询规划成功")
            print(f"   生成了 {len(query_plan['plan']['queries'])} 个查询")
            for i, q in enumerate(query_plan['plan']['queries'][:3], 1):
                print(f"   {i}. {q['purpose']}: {q['query'][:50]}...")
            return True
        else:
            print(f"❌ 查询规划失败")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_information_collection():
    """测试信息收集"""
    print("\n" + "="*80)
    print("测试3: 信息收集测试")
    print("="*80)
    
    try:
        system = ValuationReportSystem()
        
        # 创建简单的查询计划
        simple_plan = {
            "status": "success",
            "company": "Tesla",
            "plan": {
                "queries": [
                    {
                        "query": "Tesla latest financial results 2024",
                        "purpose": "财务数据",
                        "priority": "high"
                    },
                    {
                        "query": "Tesla stock valuation analysis",
                        "purpose": "估值分析",
                        "priority": "high"
                    }
                ]
            }
        }
        
        print("\n收集信息...")
        collection_result = system.information_collector.collect_information(simple_plan)
        
        if collection_result["status"] == "success":
            print(f"✅ 信息收集成功")
            print(f"   成功: {collection_result['success_count']}/{collection_result['total_queries']}")
            return True
        else:
            print(f"❌ 信息收集失败")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_quick_analysis():
    """测试快速分析"""
    print("\n" + "="*80)
    print("测试4: 快速分析测试")
    print("="*80)
    
    try:
        system = ValuationReportSystem()
        
        print("\n执行快速分析...")
        summary = system.quick_analysis("Microsoft")
        
        if summary and len(summary) > 100:
            print(f"✅ 快速分析成功")
            print(f"   报告长度: {len(summary)} 字符")
            print(f"   报告预览: {summary[:200]}...")
            return True
        else:
            print(f"❌ 快速分析失败或输出过短")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_full_report():
    """测试完整报告生成"""
    print("\n" + "="*80)
    print("测试5: 完整报告生成测试")
    print("="*80)
    
    try:
        system = ValuationReportSystem()
        
        print("\n生成完整报告...")
        result = system.generate_report(
            company="NVIDIA",
            report_type="comprehensive",
            save_to_file=True
        )
        
        if result["status"] == "success":
            print(f"✅ 完整报告生成成功")
            print(f"   报告长度: {len(result['report'])} 字符")
            print(f"   查询执行: {result['metadata']['queries_successful']}/{result['metadata']['queries_executed']}")
            print(f"   总耗时: {result['metadata']['elapsed_time']:.2f}秒")
            print(f"   保存文件: {result['metadata'].get('saved_file', 'N/A')}")
            return True
        else:
            print(f"❌ 报告生成失败: {result.get('error', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🧪 "*20)
    print("开始系统测试")
    print("🧪 "*20 + "\n")
    
    tests = [
        ("API连接", test_api_connections),
        ("查询规划", test_query_planning),
        ("信息收集", test_information_collection),
        ("快速分析", test_quick_analysis),
        ("完整报告", test_full_report)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n\n⚠️  测试被用户中断")
            break
        except Exception as e:
            print(f"\n❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 打印总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
    else:
        print("⚠️  部分测试失败，请检查错误信息。")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        test_map = {
            "api": test_api_connections,
            "planning": test_query_planning,
            "collection": test_information_collection,
            "quick": test_quick_analysis,
            "full": test_full_report
        }
        
        if test_name in test_map:
            test_map[test_name]()
        else:
            print(f"未知测试: {test_name}")
            print("可用测试: api, planning, collection, quick, full")
    else:
        run_all_tests()

