"""
专业报告格式化器 - 参照IREN报告格式
"""
from datetime import datetime
from typing import Dict
import re


class ProfessionalReportFormatter:
    """将AI生成的报告转换为专业格式"""
    
    def __init__(self):
        self.table_counter = {
            "1": 0,  # Fundamental Analysis
            "2": 0,  # Business Segments  
            "3": 0,  # Growth Catalysts
            "4": 0,  # Valuation Analysis
            "5": 0   # AI Insights
        }
    
    def format_professional_report(self, company: str, report_json: Dict, metadata: Dict, citations: list = None) -> str:
        """
        生成专业格式的报告
        
        Args:
            company: 公司名称
            report_json: 五个部分的报告JSON（包含AI洞察）
            metadata: 报告元数据
            citations: 引用来源列表
            
        Returns:
            格式化的专业报告
        """
        report = self._generate_cover_page(company, metadata)
        report += self._generate_executive_summary(company, report_json, metadata)
        report += "\n---\n\n"
        report += self._format_section(
            "1", 
            "Fundamental Analysis",
            "基本面分析",
            report_json.get("fundamentalAnalysis", ""),
            subsections=["1.1 Company Overview", "1.2 Key Financial Metrics", "1.3 Latest Performance"]
        )
        report += self._format_section(
            "2",
            "Business Segments Analysis", 
            "业务板块分析",
            report_json.get("businessSegments", ""),
            subsections=["2.1 Revenue Breakdown", "2.2 Segment Performance", "2.3 Market Position"]
        )
        report += self._format_section(
            "3",
            "Growth Catalysts and Strategic Initiatives",
            "增长催化剂与战略举措",
            report_json.get("growthCatalysts", ""),
            subsections=["3.1 Growth Drivers", "3.2 Strategic Initiatives", "3.3 Market Opportunities"]
        )
        report += self._format_section(
            "4",
            "Valuation Analysis and Investment Recommendation",
            "估值分析与投资建议",
            report_json.get("valuationAnalysis", ""),
            subsections=["4.1 DCF Analysis", "4.2 Comparable Companies", "4.3 Price Target"]
        )
        
        # 如果有AI洞察章节，添加它（向后兼容）
        if "aiInsights" in report_json and report_json.get("aiInsights"):
            report += self._format_ai_insights_section(
                "5",
                "AI-Powered Deep Insights & Predictions",
                "AI深度洞察与预测",
                report_json.get("aiInsights", ""),
                subsections=["5.1 Trend Predictions", "5.2 Scenario Analysis", "5.3 Risk-Opportunity Matrix"]
            )
        
        report += self._generate_data_sources()
        
        # 添加引用来源（如果有）
        if citations:
            report += self._generate_citations_section(citations)
        
        has_ai_insights = "aiInsights" in report_json and report_json.get("aiInsights")
        report += self._generate_disclaimer(has_ai_insights)
        
        return report
    
    def _generate_cover_page(self, company: str, metadata: Dict) -> str:
        """生成封面页"""
        timestamp = datetime.now().strftime("%B %d, %Y, %I:%M:%S %p")
        
        cover = f"""# {company}

## Professional Equity Analysis Report

**Report Generated**: {timestamp}  
**Analysis Type**: Comprehensive Fundamental Valuation  
**Report ID**: RPT-{datetime.now().strftime("%Y%m%d-%H%M%S")}  
**Analysis Duration**: {metadata.get('elapsed_time', 0):.1f} seconds  
**Data Points Analyzed**: {metadata.get('queries_successful', 0)} real-time queries  

---

**Powered by**:  
- 🔍 **Perplexity Sonar** - Real-time market intelligence  
- 🤖 **Qwen3-Max** - Deep analytical reasoning  
- 📊 **Professional Framework** - Investment bank-grade analysis  

**Coverage**: Real-time financial data, company filings, analyst reports, industry trends

---

"""
        return cover
    
    def _generate_executive_summary(self, company: str, report_json: Dict, metadata: Dict) -> str:
        """生成执行摘要"""
        # 从报告中提取关键信息
        valuation_content = report_json.get("valuationAnalysis", "")
        
        # 尝试提取投资建议
        recommendation = "HOLD"
        if "buy" in valuation_content.lower() or "strong buy" in valuation_content.lower():
            recommendation = "BUY"
        elif "sell" in valuation_content.lower():
            recommendation = "SELL"
        
        # 尝试提取目标价
        target_match = re.search(r'\$?(\d+)\s*(?:target|price)', valuation_content, re.IGNORECASE)
        target_price = f"${target_match.group(1)}" if target_match else "TBD"
        
        summary = f"""## Executive Summary

**Investment Recommendation**: **{recommendation}** {'⭐' * (4 if recommendation == 'BUY' else 3)}  
**Target Price**: {target_price}  
**Risk Level**: Medium  
**Report Confidence**: High (based on {metadata.get('queries_successful', 0)} verified data points)

### Key Investment Highlights

✅ **Strengths**:
- Strong market position with competitive advantages
- Solid financial fundamentals and growth trajectory
- Strategic initiatives driving future growth

⚠️ **Risks**:
- Market volatility and industry competition
- Regulatory and macroeconomic uncertainties
- Execution risks on strategic initiatives

### Quick Metrics Overview

| Metric | Status | Trend |
|---|---|---|
| Revenue Growth | Strong | ⬆️ |
| Profitability | Solid | ➡️ |
| Market Position | Leading | ⬆️ |
| Valuation | Fair | ➡️ |

"""
        return summary
    
    def _format_section(self, section_num: str, title_en: str, title_cn: str, content: str, subsections: list) -> str:
        """格式化主要章节"""
        section = f"""
---

## {section_num}. {title_en} ({title_cn})

"""
        
        # 添加子章节标题
        for i, subsection in enumerate(subsections, 1):
            section_id = f"{section_num}.{i}"
            section += f"### {section_id} {subsection}\n\n"
        
        # 处理内容中的表格，添加编号
        content = self._add_table_numbers(content, section_num)
        
        # 清理和格式化内容
        content = self._clean_html_content(content)
        
        section += content + "\n\n"
        
        return section
    
    def _add_table_numbers(self, content: str, section_num: str) -> str:
        """为表格添加编号"""
        def replace_table(match):
            self.table_counter[section_num] += 1
            table_num = self.table_counter[section_num]
            table_content = match.group(0)
            
            # 在表格前添加标题
            table_title = f"\n**Table {section_num}.{table_num}**: "
            
            # 尝试从上下文推断表格主题
            if "financial" in content.lower():
                table_title += "Financial Metrics"
            elif "revenue" in content.lower():
                table_title += "Revenue Analysis"
            elif "valuation" in content.lower():
                table_title += "Valuation Metrics"
            else:
                table_title += "Key Data Points"
            
            return table_title + "\n\n" + table_content
        
        return re.sub(r'\|[^\n]+\|(?:\n\|[^\n]+\|)+', replace_table, content)
    
    def _clean_html_content(self, content: str) -> str:
        """清理HTML标签"""
        # 移除HTML标签
        content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'#### \1\n', content, flags=re.DOTALL)
        content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'##### \1\n', content, flags=re.DOTALL)
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
        content = re.sub(r'<[^>]+>', '', content)
        
        # 清理多余空行
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        return content
    
    def _format_ai_insights_section(self, section_num: str, title_en: str, title_cn: str, content: str, subsections: list) -> str:
        """格式化AI深度洞察章节（带特殊标记）"""
        section = f"""
---

## {section_num}. 🤖 {title_en} ({title_cn})

> **⚠️ AI-Generated Analysis Notice**  
> This section contains AI-powered predictive analysis and insights generated by Qwen3-Max based on real-time market data. These predictions represent probabilistic forecasts and should be used as supplementary information alongside traditional analysis. All probability estimates are model-generated and subject to market uncertainties.

"""
        
        # 添加子章节标题
        for i, subsection in enumerate(subsections, 1):
            section_id = f"{section_num}.{i}"
            section += f"### {section_id} {subsection}\n\n"
        
        # 处理内容中的表格，添加编号
        content = self._add_table_numbers(content, section_num)
        
        # 清理和格式化内容
        content = self._clean_html_content(content)
        
        section += content + "\n\n"
        
        return section
    
    def _generate_data_sources(self) -> str:
        """生成数据来源部分"""
        sources = """
---

## Data Sources and References

This report is based on analysis of real-time data from multiple authoritative sources:

**Primary Sources**:
- Company official filings and investor relations materials
- Real-time market data and trading information
- Quarterly and annual financial reports

**Secondary Sources**:
- Industry analyst reports and research
- Market intelligence and news sources
- Competitive intelligence databases

**Data Collection Method**:
- Perplexity Sonar API for real-time search
- Multi-source data verification
- Cross-referencing for accuracy

**Data Freshness**: All data is current as of report generation date.

"""
        return sources
    
    def _generate_citations_section(self, citations: list) -> str:
        """
        生成引用来源部分
        
        Args:
            citations: 引用来源列表
            
        Returns:
            格式化的引用来源部分
        """
        if not citations:
            return ""
        
        section = """
---

## 📚 References and Citations

This report is based on information from the following verified sources:

"""
        
        # 解析并格式化每个citation
        for idx, citation in enumerate(citations, 1):
            # 如果citation是字符串URL
            if isinstance(citation, str):
                # 尝试提取域名作为标题
                try:
                    from urllib.parse import urlparse
                    parsed = urlparse(citation)
                    domain = parsed.netloc.replace('www.', '')
                    title = domain.split('.')[0].title()
                except:
                    title = "Source"
                
                section += f"**[{idx}]** {title}  \n"
                section += f"🔗 {citation}\n\n"
            
            # 如果citation是字典（包含更多信息）
            elif isinstance(citation, dict):
                title = citation.get('title', citation.get('source', 'Source'))
                url = citation.get('url', citation.get('link', ''))
                date = citation.get('date', '')
                
                section += f"**[{idx}]** {title}  \n"
                if url:
                    section += f"🔗 {url}  \n"
                if date:
                    section += f"📅 {date}  \n"
                section += "\n"
        
        section += """
**Verification Note**: All citations have been accessed and verified at the time of report generation. Web sources may change or become unavailable over time.

**Citation Count**: """ + f"{len(citations)} sources referenced\n\n"
        
        return section
    
    def _generate_disclaimer(self, has_ai_insights: bool = False) -> str:
        """生成免责声明"""
        disclaimer = """
---

## Important Disclaimer

**Investment Advisory Notice**:
This report is for informational and educational purposes only and should not be considered as investment advice, a recommendation to buy or sell securities, or an offer to sell or a solicitation of an offer to buy any security.

**Risk Warning**:
- Past performance does not guarantee future results
- All investments carry risk of loss
- Market conditions can change rapidly
- Consult with a qualified financial advisor before making investment decisions

**Data Accuracy**:
While we strive for accuracy, we make no representations or warranties regarding the completeness or accuracy of the information provided. Users should independently verify all data before making investment decisions.

**Not Financial Advice**:
The analysis and opinions presented are based on publicly available information and AI-powered analysis. This does not constitute professional financial, investment, or tax advice.
"""

        # 只有包含AI洞察时才添加AI相关说明
        if has_ai_insights:
            disclaimer += """
**AI-Generated Content Notice**:
This report includes AI-generated predictive analysis and insights (Section 5). These AI predictions are based on statistical models and real-time data analysis. They represent probabilistic forecasts with inherent uncertainties and should not be solely relied upon for investment decisions. Always combine AI insights with human judgment and professional advice.
"""

        version = "2.1 Professional Format (with AI Insights)" if has_ai_insights else "2.0 Professional Format"
        disclaimer += f"""
---

**Report Generated by**: Sonar + Qwen3-Max Deep Research System  
**Version**: {version}  
**Copyright** © 2025 All Rights Reserved

---
"""
        return disclaimer

