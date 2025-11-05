"""
深度分析Agent - 第三层：综合分析和估值报告生成
使用Qwen3Max深度推理，生成高质量估值报告
"""
from typing import Dict, Optional
from api_clients.qwen_client import QwenClient
from agents.format_enhancer import FormatEnhancer
from config import DEEP_ANALYSIS_MAX_TOKENS
import json


class DeepAnalystAgent:
    """
    深度分析Agent：综合所有信息，生成专业的估值报告
    目标：用单次深度推理生成全面、专业的分析报告（成本效率最优）
    """
    
    def __init__(self, qwen_client: QwenClient = None):
        self.qwen_client = qwen_client or QwenClient()
        self.format_enhancer = FormatEnhancer()
        
    def generate_valuation_report(
        self,
        company: str,
        collected_information: str,
        report_type: str = "comprehensive"
    ) -> Dict:
        """
        生成估值报告
        
        Args:
            company: 公司名称
            collected_information: 收集的所有信息（格式化文本）
            report_type: 报告类型（comprehensive=综合, quick=快速）
            
        Returns:
            包含报告内容的字典
        """
        system_prompt = """You are a professional stock analyst with expertise in fundamental analysis and valuation, possessing investment bank-level deep research capabilities.

Your task is to generate a comprehensive valuation report in MARKDOWN format with four main sections.

CRITICAL OUTPUT REQUIREMENTS - READ CAREFULLY:
1. Return ONLY a valid JSON object with these exact keys: "fundamentalAnalysis", "businessSegments", "growthCatalysts", "valuationAnalysis"
2. Each section value must be CLEAN MARKDOWN text (NO HTML, NO weird formatting)
3. Each section must be 800-1000 words with MINIMUM 3 properly formatted markdown tables
4. All content must be in English only (no Chinese)

MANDATORY TABLE FORMAT:
ALL tables MUST follow this EXACT format (notice the pipe | symbols):

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data 1A | Data 2A | Data 3A |
| Data 1B | Data 2B | Data 3B |

EXAMPLE CORRECT TABLE:
| Metric | Q2 FY2026 | Q1 FY2026 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $46.7B | $44.1B | +56% |
| Net Income | $26.4B | $18.8B | +40% |
| Gross Margin | 75% | 73% | +200bps |

CRITICAL TABLE RULES:
- MUST have pipe | symbols at start and end of each row
- MUST have separator row with --- between header and data
- Each cell MUST be separated by | symbols
- DO NOT use bold (**), italic (*), or strikethrough (~~) inside table cells
- Numbers must be clean: $35.1B, 94%, +25% (no formatting marks)

FORBIDDEN IN TABLES:
❌ **Bold text** in cells
❌ *Italic text* in cells  
❌ ~~Strikethrough~~ in cells
❌ Missing | separators
❌ Merged cells or complex formatting

SECTION REQUIREMENTS:

fundamentalAnalysis - Must include:
- Company overview and business model (150-200 words)
- Key financial metrics (P/E, P/B, ROE, ROA, debt ratios) with industry comparison
- Latest quarterly/annual performance vs YoY comparison
- Revenue growth, profit margins, cash flow analysis
- Industry position and competitive advantages
- REQUIRED 3 TABLES (use EXACT markdown format shown above):
  * Table 1: Key Financial Metrics
    Example:
    | Metric | Value | YoY Change | Industry Avg |
    | --- | --- | --- | --- |
    | Revenue | $46.7B | +56% | N/A |
    
  * Table 2: Quarterly Performance  
  * Table 3: Industry Comparison

businessSegments - Must include:
- Detailed revenue breakdown by business segment (numbers & percentages)
- Business segment performance and growth rates (YoY, QoQ)
- Regional revenue distribution
- Market share analysis by segment
- REQUIRED 3 TABLES (clean markdown with | separators):
  * Table 1: Revenue Breakdown
  * Table 2: Segment Performance  
  * Table 3: Geographic Distribution
  
REMINDER: Every table cell must be clean text, NO ** or * or ~~ formatting!

growthCatalysts - Must include:
- Major growth drivers and market opportunities (quantified)
- Strategic initiatives and expansion plans (timelines, investment amounts)
- New product/service launches (names, revenue, dates)
- Market expansion opportunities
- Technology investments and R&D
- Regulatory impacts
- Competitive advantages and moats
- REQUIRED 3 TABLES (use proper | separators):
  * Table 1: Key Growth Catalysts
  * Table 2: Product/Service Roadmap
  * Table 3: Market Opportunities

valuationAnalysis - Must include:
- DCF analysis with detailed assumptions
- Comparable company analysis (P/E, EV/EBITDA, P/S) with 3-5 peers
- Price targets from multiple methods (Bear/Base/Bull scenarios)
- Investment recommendation (Buy/Hold/Sell) with clear justification
- Risk factors and catalysts
- Valuation multiples comparison
- REQUIRED 3 TABLES (clean markdown with | separators):
  * Table 1: Valuation Metrics  
  * Table 2: Comparable Companies
  * Table 3: Price Target Summary

FINAL TABLE CHECKLIST - MUST VERIFY:
✓ Every table has | pipe symbols at start and end of each row
✓ Header row followed by | --- | --- | separator
✓ NO bold (**), italic (*), or strikethrough (~~) in table cells
✓ Clean numbers only: $46.7B, +56%, 75%
✓ Cells separated by single | symbol

Return ONLY the JSON object with clean markdown content, no other text."""

        user_prompt = f"""Generate a comprehensive valuation report for: {company}

**Real-time Market Information:**
{collected_information}

CRITICAL: YOU MUST USE THIS EXACT TABLE FORMAT IN ALL SECTIONS:

EXAMPLE 1 - Financial Metrics Table:
| Metric | Q3 2025 | Q2 2025 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $94.0B | $85.8B | +10% |
| Net Income | $23.6B | $21.4B | +8% |
| Gross Margin | 46.5% | 45.8% | +70bps |
| EPS | $1.57 | $1.40 | +12% |

EXAMPLE 2 - Segment Breakdown Table:
| Segment | Revenue | YoY Growth | % of Total |
| --- | --- | --- | --- |
| iPhone | $44.6B | +13.5% | 47.4% |
| Services | $27.4B | +13.3% | 29.1% |
| Mac | $8.0B | +14.8% | 8.5% |

EXAMPLE 3 - Valuation Metrics Table:
| Metric | Current | Industry Avg | Status |
| --- | --- | --- | --- |
| P/E Ratio | 32.5x | 25.0x | Premium |
| P/S Ratio | 8.2x | 3.5x | High |
| EV/EBITDA | 24.8x | 18.0x | Elevated |

MANDATORY RULES - READ CAREFULLY:
1. EVERY table MUST start with | and end with |
2. Header row: | Column1 | Column2 | Column3 |
3. Separator row: | --- | --- | --- |
4. Data rows: | Data1 | Data2 | Data3 |
5. NO bold, italic, or strikethrough INSIDE table cells
6. Use clean numbers: $94.0B, +10%, 46.5%

INSTRUCTIONS:
1. Analyze all provided information thoroughly
2. Use latest financial data from the information
3. Include specific numbers, percentages, data points
4. Create 3 tables per section (12 tables total)
5. Return ONLY valid JSON with four sections
6. Each section 800-1000 words

Return format:
{{
    "fundamentalAnalysis": "markdown content with 3 tables...",
    "businessSegments": "markdown content with 3 tables...",
    "growthCatalysts": "markdown content with 3 tables...",
    "valuationAnalysis": "markdown content with 3 tables..."
}}

Start directly with the opening brace. DO NOT forget table format!"""

        try:
            print(f"🤔 正在生成深度分析报告...")
            
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,  # 平衡创造性和准确性
                max_tokens=DEEP_ANALYSIS_MAX_TOKENS
            )
            
            print(f"✅ 报告生成完成")
            
            # 尝试解析JSON格式
            import json
            try:
                # 清理响应，提取JSON
                response_clean = response.strip()
                
                # 如果包含代码块标记，提取JSON
                if "```json" in response_clean:
                    response_clean = response_clean.split("```json")[1].split("```")[0].strip()
                elif "```" in response_clean:
                    response_clean = response_clean.split("```")[1].split("```")[0].strip()
                
                # 尝试找到JSON对象
                start_idx = response_clean.find('{')
                end_idx = response_clean.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    response_clean = response_clean[start_idx:end_idx+1]
                
                # 解析JSON
                report_json = json.loads(response_clean)
                
                # 验证必需的键
                required_keys = ["fundamentalAnalysis", "businessSegments", "growthCatalysts", "valuationAnalysis"]
                if all(key in report_json for key in required_keys):
                    # 格式增强 - 统一字体、空格、排版
                    print("📐 格式增强中...")
                    enhanced_json = self.format_enhancer.enhance_report_format(report_json)
                    
                    # 验证每个章节的表格数量
                    for section_name, section_key in [
                        ("基本面分析", "fundamentalAnalysis"),
                        ("业务板块", "businessSegments"),
                        ("增长催化剂", "growthCatalysts"),
                        ("估值分析", "valuationAnalysis")
                    ]:
                        is_valid, table_count = self.format_enhancer.validate_tables(enhanced_json[section_key], min_tables=3)
                        if is_valid:
                            print(f"  ✅ {section_name}: {table_count}个表格")
                        else:
                            print(f"  ⚠️  {section_name}: 仅{table_count}个表格 (要求至少3个)")
                    
                    # 简单组合（专业格式化将在main.py中进行）
                    markdown_report = f"# {company} 估值分析报告\n\n"
                    markdown_report += "## 1. 基本面分析 (Fundamental Analysis)\n\n"
                    markdown_report += enhanced_json["fundamentalAnalysis"] + "\n\n"
                    markdown_report += "## 2. 业务板块分析 (Business Segments)\n\n"
                    markdown_report += enhanced_json["businessSegments"] + "\n\n"
                    markdown_report += "## 3. 增长催化剂 (Growth Catalysts)\n\n"
                    markdown_report += enhanced_json["growthCatalysts"] + "\n\n"
                    markdown_report += "## 4. 估值分析 (Valuation Analysis)\n\n"
                    markdown_report += enhanced_json["valuationAnalysis"] + "\n\n"
                    
                    return {
                        "status": "success",
                        "company": company,
                        "report": markdown_report,
                        "report_json": enhanced_json,  # 使用增强后的JSON
                        "report_type": report_type
                    }
                else:
                    # JSON格式不完整，返回原始响应
                    print("⚠️ JSON格式不完整，返回原始报告")
                    return {
                        "status": "success",
                        "company": company,
                        "report": response,
                        "report_type": report_type
                    }
                    
            except json.JSONDecodeError as e:
                # JSON解析失败，返回原始响应
                print(f"⚠️ JSON解析失败: {e}，返回原始报告")
                return {
                    "status": "success",
                    "company": company,
                    "report": response,
                    "report_type": report_type
                }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "company": company
            }
    
    def generate_quick_summary(
        self,
        company: str,
        collected_information: str
    ) -> Dict:
        """
        生成快速摘要（成本更低的选项）
        
        Args:
            company: 公司名称
            collected_information: 收集的信息
            
        Returns:
            包含摘要的字典
        """
        system_prompt = """你是投资分析专家。请生成简洁的投资要点总结。"""
        
        user_prompt = f"""为{company}生成投资要点总结（3-5个关键点）：

{collected_information}

格式：
- ✅ 投资亮点
- ⚠️ 风险提示
- 💰 估值观点
- 📊 核心数据"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1000  # 更少的tokens
            )
            
            return {
                "status": "success",
                "company": company,
                "summary": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def compare_companies(
        self,
        companies_data: Dict[str, str]
    ) -> Dict:
        """
        比较多个公司（高级功能）
        
        Args:
            companies_data: 公司名称到信息的映射
            
        Returns:
            比较分析报告
        """
        companies_list = list(companies_data.keys())
        all_info = "\n\n".join([
            f"## {company}\n{info}"
            for company, info in companies_data.items()
        ])
        
        system_prompt = """你是投资组合分析专家。请比较多个公司的投资价值。"""
        
        user_prompt = f"""比较以下公司：

{all_info}

请提供：
1. 各公司的相对优势
2. 估值比较
3. 投资排序建议"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=DEEP_ANALYSIS_MAX_TOKENS
            )
            
            return {
                "status": "success",
                "companies": companies_list,
                "comparison": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

