"""
测试向后兼容性 - 验证修复是否有效
"""
from main import ValuationReportSystem


def test_backward_compatibility():
    """测试向后兼容性"""
    print("="*80)
    print("🧪 测试向后兼容性修复")
    print("="*80)
    print("\n这个测试会生成一份报告，并验证系统是否能正常工作")
    print("无论AI生成4章节还是5章节格式都应该能成功\n")
    
    # 创建系统实例
    system = ValuationReportSystem()
    
    print("📊 正在生成报告...")
    print("   测试公司: Apple")
    print("   预计耗时: 2-3分钟\n")
    
    try:
        result = system.generate_report(
            company="Apple",
            analysis_type="valuation",
            report_type="comprehensive",
            save_to_file=True
        )
        
        if result["status"] == "success":
            print("\n" + "="*80)
            print("✅ 测试成功！系统运行正常")
            print("="*80)
            
            report_content = result["report"]
            
            # 检查报告章节数
            chapter_count = report_content.count("## 1.") + \
                          report_content.count("## 2.") + \
                          report_content.count("## 3.") + \
                          report_content.count("## 4.") + \
                          report_content.count("## 5.")
            
            print(f"\n📄 报告信息:")
            print(f"   文件: {result['metadata'].get('saved_file', 'N/A')}")
            print(f"   耗时: {result['metadata']['elapsed_time']:.2f}秒")
            print(f"   查询: {result['metadata']['queries_successful']}/{result['metadata']['queries_executed']}")
            
            # 判断是4章节还是5章节
            if "## 5. 🤖" in report_content or "AI深度洞察" in report_content:
                print(f"\n✨ 报告格式: 5章节（包含AI深度洞察）")
                print("   🎉 AI模型支持新格式！")
                print("\n📋 报告包含:")
                print("   1. 基本面分析")
                print("   2. 业务板块分析")
                print("   3. 增长催化剂")
                print("   4. 估值分析")
                print("   5. 🤖 AI深度洞察 ← 新增")
                
                # 验证AI标识
                has_ai_marker = "🤖" in report_content and \
                              ("AI-Generated" in report_content or "AI Deep Analysis" in report_content)
                if has_ai_marker:
                    print("\n   ✅ AI生成内容已正确标注")
                else:
                    print("\n   ⚠️  AI标识可能不完整")
                    
            else:
                print(f"\n📝 报告格式: 4章节（传统格式）")
                print("   ℹ️  AI模型使用旧版格式（这是正常的）")
                print("\n📋 报告包含:")
                print("   1. 基本面分析")
                print("   2. 业务板块分析")
                print("   3. 增长催化剂")
                print("   4. 估值分析")
            
            print("\n" + "="*80)
            print("✅ 向后兼容性测试通过")
            print("="*80)
            print("\n💡 结论: 系统能够处理两种格式，无论AI生成哪种都能正常工作")
            
            return True
            
        else:
            print("\n" + "="*80)
            print(f"❌ 测试失败: {result.get('error', '未知错误')}")
            print("="*80)
            return False
            
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ 测试异常: {str(e)}")
        print("="*80)
        import traceback
        print("\n详细错误信息:")
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = test_backward_compatibility()
    
    if success:
        print("\n" + "🎉"*20)
        print("\n✅ 所有测试通过！系统已修复，可以正常使用。")
        print("\n可以运行以下命令生成报告：")
        print("   python main.py")
        print("   python test_system.py")
        print("   python test_ai_insights.py")
        print("\n" + "🎉"*20)
    else:
        print("\n" + "⚠️"*20)
        print("\n❌ 测试失败，请检查错误信息")
        print("\n如需帮助，请查看: 向后兼容修复说明.md")
        print("\n" + "⚠️"*20)

