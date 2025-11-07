#!/usr/bin/env python3
"""
测试行业龙头功能优化
验证新的显示格式和数据完整性
"""

from agents.sector_leader_analyzer import SectorLeaderAnalyzer

def test_sector_leaders():
    """测试行业龙头查询"""
    print("="*80)
    print("🧪 测试行业龙头功能优化")
    print("="*80)
    
    analyzer = SectorLeaderAnalyzer()
    
    # 测试科技行业
    print("\n📊 测试1: 科技行业 - US市场")
    print("-"*80)
    
    result = analyzer.find_sector_leaders("Technology", ["US"])
    
    if result.get("status") == "success":
        print("✅ 查询成功")
        
        markets_data = result.get('markets', {})
        us_companies = markets_data.get('US', [])
        
        if us_companies:
            print(f"\n找到 {len(us_companies)} 家公司\n")
            
            for i, company in enumerate(us_companies[:3], 1):
                print(f"{'='*80}")
                print(f"公司 #{i}")
                print(f"{'='*80}")
                
                # 验证必需字段
                company_name = company.get('company', '❌ 缺失')
                ticker = company.get('ticker', '❌ 缺失')
                market_cap = company.get('market_cap', '❌ N/A')
                
                print(f"✓ 公司名称: {company_name}")
                print(f"✓ Ticker: {ticker}")
                print(f"✓ 市值: {market_cap}")
                
                # 验证关键指标
                metrics = company.get('key_metrics', {})
                revenue = metrics.get('revenue', '❌ N/A')
                market_share = metrics.get('market_share', '❌ N/A')
                growth = metrics.get('growth_rate', '❌ N/A')
                
                print(f"✓ 营收: {revenue}")
                print(f"✓ 市场份额: {market_share}")
                print(f"✓ 增长率: {growth}")
                
                # 验证竞争优势
                advantages = company.get('competitive_advantages', [])
                print(f"\n✓ 竞争优势数量: {len(advantages)}")
                if advantages:
                    for j, adv in enumerate(advantages[:3], 1):
                        print(f"  {j}. {adv[:80]}...")
                
                # 验证近期表现
                performance = company.get('recent_performance', '')
                perf_length = len(performance) if performance else 0
                print(f"\n✓ 近期表现长度: {perf_length} 字符")
                if performance:
                    print(f"  内容: {performance[:150]}...")
                
                # 数据质量评分
                print(f"\n{'─'*80}")
                print("📊 数据质量检查:")
                
                checks = {
                    "有公司名称": company_name != '❌ 缺失',
                    "有Ticker": ticker != '❌ 缺失',
                    "市值非N/A": market_cap != '❌ N/A' and market_cap != 'N/A',
                    "营收非N/A": revenue != '❌ N/A' and revenue != 'N/A',
                    "市场份额非N/A": market_share != '❌ N/A' and market_share != 'N/A',
                    "增长率非N/A": growth != '❌ N/A' and growth != 'N/A',
                    "有竞争优势": len(advantages) >= 3,
                    "近期表现充足": perf_length >= 100
                }
                
                passed = sum(checks.values())
                total = len(checks)
                score = (passed / total) * 100
                
                for check_name, check_pass in checks.items():
                    status = "✅" if check_pass else "❌"
                    print(f"  {status} {check_name}")
                
                print(f"\n🎯 质量得分: {score:.1f}% ({passed}/{total})")
                
                if score >= 80:
                    print("💯 优秀！数据完整且详细")
                elif score >= 60:
                    print("👍 良好，部分字段可以更完善")
                else:
                    print("⚠️  需要改进，缺少关键信息")
                
                print()
        else:
            print("❌ 未找到公司数据")
    else:
        print(f"❌ 查询失败: {result.get('error', '未知错误')}")
    
    print("\n" + "="*80)
    print("🏁 测试完成")
    print("="*80)
    
    print("\n💡 优化要点:")
    print("  1. 公司名称必须清晰显示")
    print("  2. Ticker代码必须标注")
    print("  3. 市值/营收不能是N/A")
    print("  4. 近期表现应≥100字符")
    print("  5. 至少3条竞争优势")
    print("\n✨ 目标：所有公司质量得分 ≥80%")


if __name__ == "__main__":
    test_sector_leaders()

