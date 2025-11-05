"""
清洁数据分析师 - 生成干净、结构化的JSON数据
解决Qwen生成混乱格式的问题
"""
import json
import re
from typing import Dict, List
from api_clients import QwenClient


class CleanDataAnalyst:
    """生成干净、结构化数据的分析师"""
    
    def __init__(self, qwen_client: QwenClient):
        self.client = qwen_client
    
    def generate_clean_report_data(self, company: str, raw_info: str) -> Dict:
        """
        生成干净的结构化报告数据
        
        Returns:
            {
                "company": "公司名称",
                "fundamentals": {
                    "overview": "文本",
                    "financial_metrics": [
                        {"metric": "Revenue", "q2_2026": "46.7B", "q1_2026": "44.1B", "yoy_change": "+56%"},
                        ...
                    ],
                    "profitability": [
                        {"ratio": "Gross Margin", "value": "75%", "industry_avg": "55%", "interpretation": "..."},
                        ...
                    ]
                },
                "business_segments": {
                    "overview": "文本",
                    "revenue_breakdown": [
                        {"segment": "Data Center", "revenue": "38.0B", "percentage": "81%", "yoy_growth": "+70%"},
                        ...
                    ]
                },
                "growth_catalysts": {
                    "overview": "文本",
                    "initiatives": [
                        {"initiative": "...", "investment": "...", "expected_impact": "..."},
                        ...
                    ]
                },
                "valuation": {
                    "overview": "文本",
                    "metrics": [
                        {"metric": "P/E (TTM)", "value": "59.0x", "interpretation": "..."},
                        ...
                    ],
                    "price_targets": [
                        {"source": "MarketBeat", "target": "$222", "rating": "Strong Buy"},
                        ...
                    ]
                }
            }
        """
        
        prompt = f"""你是一个专业的金融分析师。请基于以下信息，生成一份**严格的JSON格式**的{company}分析报告。

【重要要求】
1. **只输出JSON**，不要任何markdown格式（不要```json，不要**加粗**，不要*斜体*，不要~~删除线~~）
2. **表格数据**必须用数组表示，每个元素是一个对象
3. **数字要清晰**，例如："46.7B", "+56%", "75%"等
4. **文本要简洁**，每个字段不超过500字
5. **严格按照下面的JSON结构**

【输出JSON结构】
{{
  "company": "{company}",
  "fundamentals": {{
    "overview": "简要概述公司的财务状况和市场地位（2-3段）",
    "financial_metrics": [
      {{"metric": "Revenue", "q2_2026": "46.7B", "q1_2026": "44.1B", "yoy_change": "+56%"}},
      {{"metric": "Net Income", "q2_2026": "26.4B", "q1_2026": "18.8B", "yoy_change": "+76%"}},
      {{"metric": "Operating Income", "q2_2026": "23.5B", "q1_2026": "19.0B", "yoy_change": "+30%"}}
    ],
    "profitability_ratios": [
      {{"ratio": "Gross Margin", "value": "75%", "industry_avg": "55%", "interpretation": "Exceptional pricing power"}},
      {{"ratio": "Net Margin", "value": "56.5%", "industry_avg": "25%", "interpretation": "Unprecedented profitability"}},
      {{"ratio": "ROE", "value": "95%", "industry_avg": "20%", "interpretation": "Extremely efficient capital use"}}
    ]
  }},
  "business_segments": {{
    "overview": "业务板块概述（2-3段）",
    "revenue_breakdown": [
      {{"segment": "Data Center", "revenue": "38.0B", "percentage": "81%", "yoy_growth": "+70%"}},
      {{"segment": "Gaming", "revenue": "5.0B", "percentage": "11%", "yoy_growth": "+10%"}},
      {{"segment": "Professional Visualization", "revenue": "1.2B", "percentage": "3%", "yoy_growth": "+15%"}},
      {{"segment": "Automotive", "revenue": "0.8B", "percentage": "2%", "yoy_growth": "+25%"}}
    ],
    "market_position": [
      {{"segment": "AI Accelerators", "market_share": "80-87%", "key_products": "A100, H100, Blackwell"}},
      {{"segment": "Data Center GPUs", "market_share": "92%", "key_products": "HGX, DGX"}},
      {{"segment": "Gaming GPUs", "market_share": ">80%", "key_products": "GeForce RTX 50"}}
    ]
  }},
  "growth_catalysts": {{
    "overview": "增长驱动因素概述（2-3段）",
    "strategic_initiatives": [
      {{"initiative": "AI Data Centers", "investment": "$100B", "timeline": "2025-2027", "expected_impact": "$20-30B annual revenue"}},
      {{"initiative": "Blackwell Architecture", "investment": "N/A", "timeline": "2024-2025", "expected_impact": "30x performance gain"}},
      {{"initiative": "Automotive AI", "investment": "$3B", "timeline": "2025-2027", "expected_impact": "New $10B+ TAM"}}
    ],
    "technology_roadmap": [
      {{"year": "2024", "architecture": "Blackwell B100/B200", "key_features": "20 petaflops FP4, 30x LLM speedup"}},
      {{"year": "2025", "architecture": "Blackwell Ultra", "key_features": "Enhanced power efficiency"}},
      {{"year": "2026", "architecture": "Rubin", "key_features": "Next-gen Tensor Cores"}}
    ]
  }},
  "valuation": {{
    "overview": "估值分析概述（2-3段）",
    "valuation_metrics": [
      {{"metric": "Trailing P/E", "value": "59.0x", "interpretation": "Premium for growth leadership"}},
      {{"metric": "Forward P/E", "value": "35.7x", "interpretation": "Growth expected to continue"}},
      {{"metric": "P/S", "value": "30.6x", "interpretation": "Reflects AI revenue dominance"}},
      {{"metric": "P/B", "value": "49.2x", "interpretation": "High intangible value"}}
    ],
    "analyst_consensus": [
      {{"source": "MarketBeat (49 analysts)", "avg_target": "$222", "rating": "Strong Buy", "range": "$200-$350"}},
      {{"source": "StockAnalysis (42 analysts)", "avg_target": "$217", "rating": "Strong Buy", "range": "$180-$250"}},
      {{"source": "Loop Capital", "avg_target": "$350", "rating": "Buy", "range": "Bull case"}}
    ],
    "recommendation": {{
      "rating": "BUY",
      "confidence": "High",
      "target_price": "$222",
      "upside_potential": "17-22%",
      "key_risks": ["Market volatility", "Competition", "Regulatory"]
    }}
  }}
}}

【原始信息】
{raw_info[:8000]}

请严格按照上述JSON结构输出，确保：
1. 所有表格数据都用数组+对象表示
2. 数字格式统一（例如：46.7B, +56%, 75%）
3. 不要有任何markdown格式
4. JSON格式正确，可以直接parse
"""
        
        try:
            response = self.client.chat(
                [{"role": "user", "content": prompt}],
                temperature=0.3,  # 降低温度确保格式一致性
                max_tokens=6000
            )
            
            # 清理响应（移除可能的markdown包装）
            json_text = response.strip()
            if json_text.startswith('```'):
                # 移除markdown代码块
                json_text = re.sub(r'^```json?\s*', '', json_text)
                json_text = re.sub(r'\s*```$', '', json_text)
            
            # 解析JSON
            data = json.loads(json_text)
            
            print("✅ 生成了干净的结构化数据")
            return data
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            print(f"   响应内容（前500字）: {response[:500]}")
            return None
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            return None


def test_clean_analyst():
    """测试清洁分析师"""
    from main import ValuationReportSystem
    
    # 准备测试数据
    test_info = """
    NVIDIA Corporation Q2 FY2026 Results:
    - Revenue: $46.7 billion (+56% YoY)
    - Net Income: $26.4 billion
    - Gross Margin: ~75%
    - Data Center revenue: ~$38 billion
    """
    
    from api_clients import QwenClient
    analyst = CleanDataAnalyst(QwenClient())
    
    data = analyst.generate_clean_report_data("NVIDIA", test_info)
    
    if data:
        print("\n📊 生成的结构化数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_clean_analyst()

