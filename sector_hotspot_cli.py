"""
行业热点分析 - 命令行工具
"""
from agents.sector_leader_analyzer import SectorLeaderAnalyzer
from datetime import datetime
import sys


def print_banner():
    """打印欢迎横幅"""
    print("\n" + "="*80)
    print("📊 行业龙头与热点分析系统".center(70))
    print("A股 | 港股 | 美股 - 实时热点追踪".center(70))
    print("="*80 + "\n")


def show_menu():
    """显示主菜单"""
    print("\n📋 功能菜单:\n")
    print("  1. 📈 查看今日热点行业")
    print("  2. 🔍 查找特定行业龙头")
    print("  3. 📊 生成完整分析报告")
    print("  4. 💡 查看行业列表")
    print("  5. ❌ 退出")
    print()


def analyze_hotspots():
    """分析今日热点"""
    print("\n" + "="*80)
    print("🔥 正在分析今日市场热点...")
    print("="*80)
    
    analyzer = SectorLeaderAnalyzer()
    result = analyzer.analyze_market_hotspots()
    
    if result.get("status") != "success":
        print(f"\n❌ 分析失败: {result.get('error', '未知错误')}")
        return
    
    # 显示热点行业
    print("\n" + "🔥"*40)
    print(f"\n📅 日期: {result.get('date', 'Today')}")
    print(f"📊 市场情绪: {result.get('market_sentiment', 'N/A').upper()}")
    print(f"🎯 关键主题: {', '.join(result.get('key_themes', []))}")
    
    print("\n📈 热点行业排行:\n")
    
    top_sectors = result.get('top_sectors', [])
    if not top_sectors:
        print("   暂无数据")
        return
    
    # 表头
    print(f"{'排名':<6} {'行业':<20} {'市场':<10} {'热度':<8} {'涨跌幅':<10} {'成交量':<10}")
    print("-" * 80)
    
    # 数据行
    for i, sector in enumerate(top_sectors, 1):
        sector_name = sector.get('sector', '')
        market = sector.get('market', '')
        heat = sector.get('heat_score', 0)
        change = sector.get('avg_change', '')
        volume = sector.get('volume_surge', '')
        
        # 根据热度添加颜色标识
        heat_icon = "🔥" if heat >= 80 else "⭐" if heat >= 60 else "📊"
        
        print(f"{i:<6} {sector_name:<20} {market:<10} {heat_icon}{heat:<6} {change:<10} {volume:<10}")
        
        # 显示关键驱动因素
        drivers = sector.get('key_drivers', [])
        if drivers:
            print(f"       💡 驱动因素: {', '.join(drivers)}")
        
        # 显示热门股票
        stocks = sector.get('top_stocks', [])
        if stocks:
            print(f"       🏆 热门股票: {', '.join(stocks[:3])}")
        
        print()


def find_sector_leaders():
    """查找行业龙头"""
    print("\n" + "="*80)
    print("🔍 查找行业龙头")
    print("="*80)
    
    # 输入行业
    print("\n请输入行业名称（中文或英文）:")
    print("例如: 科技、半导体、Technology、Healthcare")
    sector = input("\n行业名称: ").strip()
    
    if not sector:
        print("❌ 行业名称不能为空")
        return
    
    # 选择市场
    print("\n请选择市场（可多选，用逗号分隔）:")
    print("1. A股")
    print("2. 港股")
    print("3. 美股")
    print("4. 全部市场")
    
    market_choice = input("\n选择 (1/2/3/4): ").strip()
    
    market_map = {
        "1": ["A-share"],
        "2": ["HK"],
        "3": ["US"],
        "4": ["A-share", "HK", "US"]
    }
    
    markets = market_map.get(market_choice, ["A-share", "HK", "US"])
    
    # 执行查询
    analyzer = SectorLeaderAnalyzer()
    result = analyzer.find_sector_leaders(sector, markets)
    
    if result.get("status") != "success":
        print(f"\n❌ 查询失败")
        return
    
    # 显示结果
    print("\n" + "🏆"*40)
    print(f"\n📊 {sector} 行业龙头公司\n")
    
    markets_data = result.get('markets', {})
    
    for market, companies in markets_data.items():
        if not companies:
            print(f"\n{market} 市场: 暂无数据")
            continue
        
        print(f"\n{'='*80}")
        print(f"  {market} 市场")
        print(f"{'='*80}\n")
        
        for i, company in enumerate(companies, 1):
            rank = company.get('rank', i)
            name = company.get('company', '未知公司')
            ticker = company.get('ticker', 'N/A')
            market_cap = company.get('market_cap', 'N/A')
            
            # 排名图标
            rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}
            rank_icon = rank_icons.get(i, "🏆")
            
            # 公司名称和ticker
            print(f"{rank_icon} #{i} {name}")
            print(f"     📌 代码: {ticker}")
            print(f"     {'─'*70}")
            
            # 基本信息
            print(f"     💰 市值: {market_cap}")
            
            metrics = company.get('key_metrics', {})
            if metrics:
                revenue = metrics.get('revenue', 'N/A')
                market_share = metrics.get('market_share', 'N/A')
                growth = metrics.get('growth_rate', 'N/A')
                print(f"     💵 营收: {revenue}  |  📊 市场份额: {market_share}  |  📈 增长: {growth}")
            
            # 竞争优势
            advantages = company.get('competitive_advantages', [])
            if advantages:
                print(f"     ⭐ 核心优势:")
                for j, adv in enumerate(advantages[:3], 1):
                    print(f"        {j}. {adv}")
            
            # 近期表现
            performance = company.get('recent_performance', '')
            if performance and performance != '暂无数据':
                print(f"     📈 近期表现:")
                print(f"        {performance}")
            else:
                print(f"     📈 近期表现: 暂无详细数据")
            
            print()


def generate_full_report():
    """生成完整报告"""
    print("\n" + "="*80)
    print("📊 正在生成完整分析报告...")
    print("="*80)
    print("\n这可能需要2-5分钟，请耐心等待...\n")
    
    analyzer = SectorLeaderAnalyzer()
    result = analyzer.generate_hotspot_report()
    
    if result.get("status") != "success":
        print(f"\n❌ 报告生成失败: {result.get('error', '未知错误')}")
        return
    
    # 保存报告
    filename = f"reports/sector_hotspot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    import os
    os.makedirs("reports", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result["report"])
    
    print("\n" + "="*80)
    print("✅ 报告生成成功！")
    print("="*80)
    print(f"\n📄 报告文件: {filename}")
    print("\n报告包含:")
    print("  ✅ 今日热点行业分析")
    print("  ✅ 各市场龙头公司信息")
    print("  ✅ 竞争优势分析")
    print("  ✅ 市场表现数据")
    
    # 显示预览
    print("\n" + "-"*80)
    print("📋 报告预览:")
    print("-"*80)
    print(result["report"][:800])
    print("\n... (完整内容请查看报告文件)\n")


def show_sector_list():
    """显示行业列表"""
    analyzer = SectorLeaderAnalyzer()
    
    print("\n" + "="*80)
    print("📚 支持的行业板块")
    print("="*80 + "\n")
    
    for sector_id, sector_info in analyzer.sectors.items():
        name_cn = sector_info['name_cn']
        name_en = sector_info['name_en']
        subsectors = sector_info['subsectors']
        
        print(f"📊 {name_cn} ({name_en})")
        print(f"   子行业: {', '.join(subsectors)}")
        print()


def main():
    """主函数"""
    print_banner()
    
    while True:
        show_menu()
        choice = input("请选择功能 (1-5): ").strip()
        
        if choice == "1":
            analyze_hotspots()
            input("\n按回车键继续...")
            
        elif choice == "2":
            find_sector_leaders()
            input("\n按回车键继续...")
            
        elif choice == "3":
            generate_full_report()
            input("\n按回车键继续...")
            
        elif choice == "4":
            show_sector_list()
            input("\n按回车键继续...")
            
        elif choice == "5":
            print("\n👋 感谢使用！再见！\n")
            sys.exit(0)
            
        else:
            print("\n❌ 无效选择，请输入 1-5")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
        sys.exit(0)

