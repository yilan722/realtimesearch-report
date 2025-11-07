"""
测试AI深度洞察功能
"""
from main import ValuationReportSystem


def test_ai_insights():
    """测试带AI洞察的报告生成"""
    print("="*80)
    print("🧪 测试AI深度洞察功能")
    print("="*80)
    
    # 创建系统实例
    system = ValuationReportSystem()
    
    # 生成报告（使用一个简单的测试对象）
    print("\n📊 正在为 NVIDIA 生成带AI洞察的深度报告...")
    print("   预计耗时: 2-3分钟")
    print()
    
    result = system.generate_report(
        company="NVIDIA",
        analysis_type="valuation",
        report_type="comprehensive",
        save_to_file=True
    )
    
    if result["status"] == "success":
        print("\n" + "="*80)
        print("✅ 测试成功！报告已生成")
        print("="*80)
        print(f"\n📄 报告文件: {result['metadata'].get('saved_file', 'N/A')}")
        print(f"⏱️  总耗时: {result['metadata']['elapsed_time']:.2f}秒")
        print(f"🔍 查询成功: {result['metadata']['queries_successful']}/{result['metadata']['queries_executed']}")
        
        # 检查报告中是否包含AI洞察章节
        report_content = result["report"]
        if "AI深度洞察与预测" in report_content or "AI-Powered Deep Insights" in report_content:
            print("✅ AI深度洞察章节已包含在报告中")
            
            # 检查AI标识
            if "🤖" in report_content and "AI-Generated Analysis" in report_content:
                print("✅ AI生成内容已正确标注")
            else:
                print("⚠️  AI标识可能缺失")
                
            # 检查AI场景分析表格
            if "Scenario" in report_content and "Probability" in report_content:
                print("✅ AI场景分析表格已生成")
            else:
                print("⚠️  AI场景分析表格可能缺失")
                
        else:
            print("❌ AI深度洞察章节未找到")
            
        # 显示报告预览
        print("\n" + "-"*80)
        print("📋 报告预览（前500字符）:")
        print("-"*80)
        print(report_content[:500])
        print("...")
        
        # 查找并显示AI洞察部分
        if "## 5. 🤖" in report_content:
            start_idx = report_content.find("## 5. 🤖")
            end_idx = report_content.find("## ", start_idx + 10)
            if end_idx == -1:
                end_idx = start_idx + 1000
            
            print("\n" + "-"*80)
            print("🤖 AI深度洞察章节预览:")
            print("-"*80)
            print(report_content[start_idx:end_idx][:800])
            print("...")
        
    else:
        print("\n" + "="*80)
        print(f"❌ 测试失败: {result.get('error', '未知错误')}")
        print("="*80)


if __name__ == "__main__":
    test_ai_insights()

