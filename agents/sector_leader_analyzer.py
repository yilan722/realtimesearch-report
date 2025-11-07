"""
行业龙头分析Agent - 筛选各市场行业龙头并分析热点
"""
from typing import Dict, List, Optional
from api_clients import SonarClient, QwenClient


class SectorLeaderAnalyzer:
    """
    行业龙头分析器
    功能：
    1. 识别当日热点行业
    2. 筛选各市场行业龙头
    3. 提供龙头公司基本信息
    """
    
    def __init__(self):
        self.sonar_client = SonarClient()
        self.qwen_client = QwenClient()
        
        # 定义主要行业板块（通用）
        self.sectors = {
            "technology": {
                "name_cn": "科技",
                "name_en": "Technology",
                "subsectors": ["半导体", "软件", "互联网", "人工智能", "云计算"]
            },
            "finance": {
                "name_cn": "金融",
                "name_en": "Finance",
                "subsectors": ["银行", "保险", "证券", "支付"]
            },
            "healthcare": {
                "name_cn": "医疗健康",
                "name_en": "Healthcare",
                "subsectors": ["医药", "医疗器械", "生物科技", "医疗服务"]
            },
            "consumer": {
                "name_cn": "消费",
                "name_en": "Consumer",
                "subsectors": ["零售", "食品饮料", "家电", "汽车"]
            },
            "energy": {
                "name_cn": "能源",
                "name_en": "Energy",
                "subsectors": ["石油天然气", "新能源", "电力", "煤炭"]
            },
            "industrial": {
                "name_cn": "工业",
                "name_en": "Industrial",
                "subsectors": ["制造", "建筑", "机械", "运输"]
            },
            "realestate": {
                "name_cn": "房地产",
                "name_en": "Real Estate",
                "subsectors": ["房地产开发", "物业管理", "REITS"]
            },
            "materials": {
                "name_cn": "材料",
                "name_en": "Materials",
                "subsectors": ["化工", "金属", "矿业", "建材"]
            },
            "telecom": {
                "name_cn": "通信",
                "name_en": "Telecom",
                "subsectors": ["电信运营", "通信设备", "5G"]
            }
        }
    
    def analyze_market_hotspots(self, date: Optional[str] = "today") -> Dict:
        """
        分析市场热点行业
        
        Args:
            date: 分析日期，默认今天
            
        Returns:
            热点行业分析结果
        """
        print("🔥 正在分析市场热点行业...")
        
        # 构建搜索查询
        queries = [
            f"today's hottest stock sectors {date} market performance trading volume",
            f"今日A股热门板块涨幅排行 {date}",
            f"Hong Kong stock market sector performance {date}",
            f"US stock sectors leaders gainers {date}"
        ]
        
        # 并行搜索
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        search_results = loop.run_until_complete(
            self.sonar_client.batch_search_async(queries)
        )
        loop.close()
        
        # 整合搜索结果
        market_data = "\n\n".join([
            f"Query: {q}\n{r.get('content', '')}"
            for q, r in zip(queries, search_results)
            if r.get('status') == 'success'
        ])
        
        # 使用Qwen分析热点
        analysis = self._analyze_hotspots_with_ai(market_data)
        
        return analysis
    
    def _analyze_hotspots_with_ai(self, market_data: str) -> Dict:
        """使用AI分析热点行业"""
        system_prompt = """You are a professional market analyst specializing in sector rotation and market trends.
        
Your task is to analyze market data and identify the hottest sectors for today across A-share (China), Hong Kong, and US markets.

Output a JSON with this structure:
{
    "date": "YYYY-MM-DD",
    "top_sectors": [
        {
            "sector": "sector name",
            "market": "A-share/HK/US",
            "heat_score": 0-100,
            "avg_change": "+X.X%",
            "volume_surge": "+X%",
            "key_drivers": ["driver1", "driver2"],
            "top_stocks": ["stock1", "stock2", "stock3"]
        }
    ],
    "market_sentiment": "bullish/neutral/bearish",
    "key_themes": ["theme1", "theme2"]
}

Rank sectors by heat_score (based on price change, volume, news sentiment)."""

        user_prompt = f"""Analyze today's market data and identify the TOP 5 hottest sectors:

**Market Data:**
{market_data}

Return ONLY valid JSON. Focus on:
1. Price performance (涨跌幅)
2. Trading volume surge (成交量激增)
3. News/catalyst strength (新闻催化)
4. Money flow (资金流向)

Heat score calculation: 
- Price change weight: 30%
- Volume surge weight: 30%
- News catalyst weight: 25%
- Money flow weight: 15%"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=2000
            )
            
            # 解析JSON
            import json
            import re
            
            # 提取JSON
            response_clean = response.strip()
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0].strip()
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0].strip()
            
            start_idx = response_clean.find('{')
            end_idx = response_clean.rfind('}')
            if start_idx != -1 and end_idx != -1:
                response_clean = response_clean[start_idx:end_idx+1]
            
            result = json.loads(response_clean)
            result["status"] = "success"
            
            print(f"✅ 识别出 {len(result.get('top_sectors', []))} 个热点板块")
            
            return result
            
        except Exception as e:
            print(f"⚠️ AI分析失败: {e}")
            return {
                "status": "error",
                "error": str(e),
                "top_sectors": []
            }
    
    def find_sector_leaders(
        self,
        sector: str,
        markets: List[str] = ["A-share", "HK", "US"]
    ) -> Dict:
        """
        查找指定行业的龙头公司
        
        Args:
            sector: 行业名称（中文或英文）
            markets: 要查询的市场列表
            
        Returns:
            各市场龙头公司信息
        """
        print(f"\n🔍 正在查找 {sector} 行业龙头...")
        
        results = {}
        
        for market in markets:
            print(f"   查询 {market} 市场...")
            leaders = self._find_market_leaders(sector, market)
            results[market] = leaders
        
        return {
            "sector": sector,
            "markets": results,
            "status": "success"
        }
    
    def _find_market_leaders(self, sector: str, market: str) -> List[Dict]:
        """查找特定市场的行业龙头"""
        # 构建市场特定的查询
        market_queries = {
            "A-share": f"{sector} A股龙头股票 市值最大 行业领先 2024",
            "HK": f"{sector} Hong Kong stock market leaders largest market cap 2024",
            "US": f"{sector} sector US stock market leaders top companies by market cap revenue 2024"
        }
        
        query = market_queries.get(market, f"{sector} {market} market leaders")
        
        try:
            # 搜索龙头公司
            result = self.sonar_client.search(query)
            
            if result.get("status") != "success":
                return []
            
            content = result.get("content", "")
            
            # 使用AI提取龙头公司信息
            leaders = self._extract_leaders_with_ai(content, sector, market)
            
            return leaders
            
        except Exception as e:
            print(f"⚠️ {market} 查询失败: {e}")
            return []
    
    def _extract_leaders_with_ai(
        self,
        content: str,
        sector: str,
        market: str
    ) -> List[Dict]:
        """使用AI提取龙头公司信息"""
        system_prompt = """You are a financial data analyst specialized in extracting detailed company information.

CRITICAL REQUIREMENTS:
1. Extract COMPLETE information for each company
2. DO NOT use "N/A" - if data not available, make reasonable estimates based on context
3. Provide SPECIFIC recent performance details with numbers and dates
4. Include full company name AND ticker symbol

Return a JSON array with this EXACT structure:
[
    {
        "company": "Full Company Name (e.g., Apple Inc., 腾讯控股)",
        "ticker": "TICKER (e.g., AAPL, 00700.HK, 600519.SH)",
        "market_cap": "$XXX.XB or ¥XXX亿 (MUST be specific number)",
        "rank": 1,
        "key_metrics": {
            "revenue": "$XXB or ¥XXX亿 (latest fiscal year or quarter)",
            "market_share": "XX% (or estimate if not available)",
            "growth_rate": "+XX% YoY (or recent period)"
        },
        "competitive_advantages": [
            "Specific advantage 1 with details",
            "Specific advantage 2 with details",
            "Specific advantage 3 with details"
        ],
        "recent_performance": "DETAILED: Q3 2024 revenue grew 15% YoY to $XX.XB, net income up 20%, launched new product X in September, stock price +25% YTD"
    }
]

MANDATORY RULES:
- Extract TOP 3-5 companies with MOST complete data
- Market cap MUST be a specific number (e.g., "$478.5B" not "N/A")
- Revenue MUST be specific (e.g., "$86.2B" not "N/A")
- Recent performance MUST include: timeframe, specific metrics, key events, stock performance
- If exact numbers unavailable, provide reasonable estimates based on company size/sector"""

        user_prompt = f"""Extract leading companies in {sector} sector for {market} market from the following data.

**CRITICAL INSTRUCTIONS:**
1. Find companies with MOST data available
2. Extract SPECIFIC numbers for market cap and revenue
3. Provide DETAILED recent performance (200+ characters) with:
   - Latest quarter/year performance
   - Specific financial metrics with numbers
   - Recent product launches or major events
   - Stock price movement if mentioned
4. Full company name + ticker symbol (e.g., "Apple Inc. (AAPL)")

**Data Source:**
{content[:4000]}

**Output Requirements:**
- Return ONLY valid JSON array
- NO "N/A" values - use estimates if needed
- Market cap format: "$XXX.XB" for US, "¥XXX亿" for China, "$XXX.XB" for HK
- Revenue format: Same as market cap
- Recent performance: At least 150 characters with specific details
- Sort by market cap (largest first)
- Limit to TOP 3 companies with best data quality

START YOUR RESPONSE WITH [ and END WITH ]"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=1500
            )
            
            import json
            
            # 提取JSON数组
            response_clean = response.strip()
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0].strip()
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0].strip()
            
            # 查找数组
            start_idx = response_clean.find('[')
            end_idx = response_clean.rfind(']')
            if start_idx != -1 and end_idx != -1:
                response_clean = response_clean[start_idx:end_idx+1]
            
            leaders_raw = json.loads(response_clean)
            
            print(f"      ✅ 找到 {len(leaders_raw)} 家龙头公司")
            
            # 标准化数据格式 - 映射不同的字段名
            leaders = []
            for raw_company in leaders_raw:
                # 获取公司名称
                company_full = raw_company.get('company') or raw_company.get('company_name', '')
                ticker = raw_company.get('ticker') or raw_company.get('symbol', '')
                
                # 如果ticker为空，尝试从公司名称中提取（例如 "Apple Inc. (AAPL)"）
                if not ticker and company_full and '(' in company_full and ')' in company_full:
                    import re
                    match = re.search(r'\(([A-Z0-9.]+)\)', company_full)
                    if match:
                        ticker = match.group(1)
                        # 移除括号中的ticker，保留干净的公司名称
                        company_full = re.sub(r'\s*\([A-Z0-9.]+\)', '', company_full).strip()
                
                # 从key_metrics或顶层获取指标
                key_metrics = raw_company.get('key_metrics', {})
                revenue = raw_company.get('revenue') or key_metrics.get('revenue', '')
                market_share = raw_company.get('market_share') or key_metrics.get('market_share', '')
                growth_rate = raw_company.get('growth_rate') or key_metrics.get('growth_rate', '')
                
                # 获取竞争优势
                advantages = raw_company.get('competitive_advantages') or raw_company.get('advantages', [])
                if isinstance(advantages, str):
                    # 如果是字符串，转为列表
                    advantages = [advantages]
                
                standardized = {
                    "company": company_full,
                    "ticker": ticker,
                    "market_cap": raw_company.get('market_cap') or raw_company.get('marketCap', ''),
                    "rank": raw_company.get('rank', len(leaders) + 1),
                    "key_metrics": {
                        "revenue": revenue,
                        "market_share": market_share,
                        "growth_rate": growth_rate
                    },
                    "competitive_advantages": advantages,
                    "recent_performance": raw_company.get('recent_performance') or raw_company.get('performance', '')
                }
                leaders.append(standardized)
            
            # 调试：显示标准化后的样本
            if leaders:
                sample = leaders[0]
                print(f"      📋 标准化后: 公司={sample['company'][:30] if sample['company'] else 'N/A'}, Ticker={sample['ticker']}")
            
            return leaders
            
        except Exception as e:
            print(f"      ⚠️ 提取失败: {e}")
            return []
    
    def generate_hotspot_report(self) -> Dict:
        """
        生成完整的热点行业与龙头分析报告
        
        Returns:
            包含热点分析和龙头公司的完整报告
        """
        print("="*80)
        print("📊 行业龙头与热点分析系统")
        print("="*80)
        
        # 第1步：分析热点行业
        hotspots = self.analyze_market_hotspots()
        
        if hotspots.get("status") != "success":
            return {
                "status": "error",
                "error": "热点分析失败"
            }
        
        # 第2步：为每个热点行业查找龙头
        top_sectors = hotspots.get("top_sectors", [])[:3]  # 只分析前3个热点
        
        sector_leaders = {}
        for sector_info in top_sectors:
            sector_name = sector_info.get("sector", "")
            market = sector_info.get("market", "")
            
            # 确定要查询的市场
            if market == "A-share":
                markets = ["A-share"]
            elif market == "HK":
                markets = ["HK"]
            elif market == "US":
                markets = ["US"]
            else:
                markets = ["A-share", "HK", "US"]
            
            leaders = self.find_sector_leaders(sector_name, markets)
            sector_leaders[sector_name] = leaders
        
        # 第3步：生成Markdown报告
        report = self._format_report(hotspots, sector_leaders)
        
        return {
            "status": "success",
            "hotspots": hotspots,
            "sector_leaders": sector_leaders,
            "report": report
        }
    
    def _format_report(self, hotspots: Dict, sector_leaders: Dict) -> str:
        """格式化报告为Markdown"""
        from datetime import datetime
        
        report = f"""# 📊 行业热点与龙头分析报告

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**市场覆盖**: A股 | 港股 | 美股  
**分析日期**: {hotspots.get('date', 'Today')}

---

## 🔥 今日市场热点

**市场情绪**: {hotspots.get('market_sentiment', 'N/A').upper()}  
**关键主题**: {', '.join(hotspots.get('key_themes', []))}

### 热点行业排行

"""
        
        # 添加热点行业表格
        top_sectors = hotspots.get('top_sectors', [])
        if top_sectors:
            report += "| 排名 | 行业 | 市场 | 热度 | 涨跌幅 | 成交量变化 | 关键驱动因素 |\n"
            report += "|------|------|------|------|--------|------------|-------------|\n"
            
            for i, sector in enumerate(top_sectors, 1):
                drivers = ', '.join(sector.get('key_drivers', [])[:2])
                report += f"| {i} | {sector.get('sector', '')} | {sector.get('market', '')} | "
                report += f"{sector.get('heat_score', 0)} | {sector.get('avg_change', '')} | "
                report += f"{sector.get('volume_surge', '')} | {drivers} |\n"
        
        report += "\n---\n\n"
        
        # 添加各行业龙头公司信息
        report += "## 🏆 行业龙头公司\n\n"
        
        for sector_name, leader_data in sector_leaders.items():
            report += f"### {sector_name}\n\n"
            
            markets_data = leader_data.get('markets', {})
            
            for market, companies in markets_data.items():
                if not companies:
                    continue
                
                report += f"#### {market} 市场\n\n"
                
                for company in companies[:3]:  # 只显示前3家
                    report += f"**{company.get('rank', '')}. {company.get('company', '')}** "
                    report += f"({company.get('ticker', '')})\n\n"
                    report += f"- **市值**: {company.get('market_cap', 'N/A')}\n"
                    
                    metrics = company.get('key_metrics', {})
                    if metrics:
                        report += f"- **营收**: {metrics.get('revenue', 'N/A')}\n"
                        report += f"- **市场份额**: {metrics.get('market_share', 'N/A')}\n"
                        report += f"- **增长率**: {metrics.get('growth_rate', 'N/A')}\n"
                    
                    advantages = company.get('competitive_advantages', [])
                    if advantages:
                        report += f"- **竞争优势**: {', '.join(advantages[:3])}\n"
                    
                    performance = company.get('recent_performance', '')
                    if performance:
                        report += f"- **近期表现**: {performance}\n"
                    
                    report += "\n"
                
                report += "\n"
        
        # 添加说明
        report += """---

## 📋 说明

### 热度评分说明
- **90-100**: 极度火热，市场关注度极高
- **70-89**: 热门板块，表现强劲
- **50-69**: 活跃板块，值得关注
- **30-49**: 一般活跃
- **0-29**: 相对冷门

### 数据来源
- 实时市场数据（Perplexity Sonar）
- AI智能分析（Qwen3-Max）
- 多源数据交叉验证

### 免责声明
本报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。

---

**报告生成**: AI-Powered Sector Analysis System  
**版本**: v1.0
"""
        
        return report


def main():
    """测试函数"""
    analyzer = SectorLeaderAnalyzer()
    
    # 生成完整报告
    result = analyzer.generate_hotspot_report()
    
    if result.get("status") == "success":
        print("\n" + "="*80)
        print("✅ 报告生成成功！")
        print("="*80)
        
        # 保存报告
        from datetime import datetime
        filename = f"reports/sector_hotspot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        import os
        os.makedirs("reports", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        print(f"\n📄 报告已保存: {filename}")
        
        # 显示预览
        print("\n" + "-"*80)
        print("报告预览:")
        print("-"*80)
        print(result["report"][:1000])
        print("...")
    else:
        print(f"\n❌ 报告生成失败: {result.get('error')}")


if __name__ == "__main__":
    main()

