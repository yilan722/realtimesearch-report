"""
测试行业龙头分析功能
"""
from agents.sector_leader_analyzer import SectorLeaderAnalyzer
import json


def test_hotspot_analysis():
    """测试热点分析功能"""
    print("="*80)
    print("🧪 测试1: 热点分析功能")
    print("="*80)
    
    analyzer = SectorLeaderAnalyzer()
    
    try:
        print("\n正在分析市场热点...")
        result = analyzer.analyze_market_hotspots()
        
        if result.get("status") == "success":
            print("✅ 热点分析成功！")
            print(f"\n📊 市场情绪: {result.get('market_sentiment', 'N/A')}")
            print(f"🎯 关键主题: {', '.join(result.get('key_themes', []))}")
            
            top_sectors = result.get('top_sectors', [])
            print(f"\n🔥 识别出 {len(top_sectors)} 个热点板块:")
            
            for i, sector in enumerate(top_sectors[:3], 1):
                print(f"  {i}. {sector.get('sector', '')} ({sector.get('market', '')}) "
                      f"- 热度: {sector.get('heat_score', 0)}")
            
            return True
        else:
            print(f"❌ 热点分析失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


def test_sector_leaders():
    """测试龙头筛选功能"""
    print("\n" + "="*80)
    print("🧪 测试2: 龙头筛选功能")
    print("="*80)
    
    analyzer = SectorLeaderAnalyzer()
    
    try:
        print("\n正在查找科技行业龙头...")
        result = analyzer.find_sector_leaders("科技", ["US"])
        
        if result.get("status") == "success":
            print("✅ 龙头筛选成功！")
            
            markets_data = result.get('markets', {})
            us_leaders = markets_data.get('US', [])
            
            if us_leaders:
                print(f"\n🏆 找到 {len(us_leaders)} 家美股科技龙头:")
                for i, company in enumerate(us_leaders[:3], 1):
                    print(f"  {i}. {company.get('company', '')} ({company.get('ticker', '')})")
                    print(f"     市值: {company.get('market_cap', 'N/A')}")
            else:
                print("⚠️ 未找到龙头公司（可能需要调整查询）")
            
            return True
        else:
            print(f"❌ 龙头筛选失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


def test_report_generation():
    """测试报告生成功能"""
    print("\n" + "="*80)
    print("🧪 测试3: 报告生成功能")
    print("="*80)
    
    print("\n⚠️  此测试需要2-5分钟，将生成完整报告")
    response = input("是否继续？(y/n): ").strip().lower()
    
    if response != 'y':
        print("⏭️  跳过报告生成测试")
        return None
    
    analyzer = SectorLeaderAnalyzer()
    
    try:
        print("\n正在生成完整报告（请耐心等待）...")
        result = analyzer.generate_hotspot_report()
        
        if result.get("status") == "success":
            print("✅ 报告生成成功！")
            
            # 保存报告
            from datetime import datetime
            filename = f"reports/test_sector_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            
            import os
            os.makedirs("reports", exist_ok=True)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(result["report"])
            
            print(f"\n📄 报告已保存: {filename}")
            print(f"📏 报告长度: {len(result['report'])} 字符")
            
            # 显示预览
            print("\n📋 报告预览（前500字符）:")
            print("-" * 80)
            print(result["report"][:500])
            print("...")
            
            return True
        else:
            print(f"❌ 报告生成失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


def main():
    """运行所有测试"""
    print("\n" + "🚀"*40)
    print("\n行业龙头与热点分析 - 功能测试")
    print("\n" + "🚀"*40 + "\n")
    
    results = {
        "热点分析": False,
        "龙头筛选": False,
        "报告生成": None
    }
    
    # 测试1: 热点分析
    results["热点分析"] = test_hotspot_analysis()
    input("\n按回车键继续下一个测试...")
    
    # 测试2: 龙头筛选
    results["龙头筛选"] = test_sector_leaders()
    input("\n按回车键继续下一个测试...")
    
    # 测试3: 报告生成（可选）
    results["报告生成"] = test_report_generation()
    
    # 总结
    print("\n" + "="*80)
    print("📊 测试结果总结")
    print("="*80 + "\n")
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⏭️  跳过"
        
        print(f"{test_name}: {status}")
    
    print("\n" + "="*80)
    
    # 判断整体结果
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"\n✅ 通过: {passed} | ❌ 失败: {failed} | ⏭️  跳过: {skipped}")
    
    if failed == 0 and passed > 0:
        print("\n🎉 所有测试通过！行业龙头分析功能正常工作。")
        print("\n可以开始使用:")
        print("  - python sector_hotspot_cli.py  (命令行界面)")
        print("  - python sector_hotspot_web.py  (Web界面)")
    elif passed > 0:
        print("\n⚠️  部分测试通过，核心功能可用。")
    else:
        print("\n❌ 测试失败，请检查配置和网络连接。")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 测试已中断")
    except Exception as e:
        print(f"\n❌ 测试异常: {str(e)}")
        import traceback
        print(traceback.format_exc())

