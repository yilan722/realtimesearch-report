"""
查询规划Agent - 第一层：成本优化的查询生成
使用Qwen3Max轻量调用，生成精确的搜索查询计划
"""
import json
from typing import List, Dict
from api_clients.qwen_client import QwenClient
from config import QUERY_PLANNER_MAX_TOKENS, MAX_SONAR_QUERIES


class QueryPlannerAgent:
    """
    查询规划Agent：智能分解研究任务为精确的搜索查询
    目标：用最少的查询获取最全面的信息（降低Sonar调用成本）
    """
    
    def __init__(self, qwen_client: QwenClient = None):
        self.qwen_client = qwen_client or QwenClient()
        
    def generate_search_plan(self, company_or_topic: str, analysis_type: str = "valuation") -> Dict:
        """
        生成搜索计划
        
        Args:
            company_or_topic: 公司名称或研究主题
            analysis_type: 分析类型（valuation=估值, market=市场分析, etc.）
            
        Returns:
            包含结构化查询列表的字典
        """
        system_prompt = f"""你是一个专业的投资研究助手。你的任务是将研究需求分解为{MAX_SONAR_QUERIES}个精确的搜索查询。

目标：
1. 每个查询必须独特且不重叠
2. 查询应涵盖估值分析的关键维度
3. 优先获取最新的实时信息
4. 查询应该具体、可搜索

输出格式（必须是有效的JSON）：
{{
    "queries": [
        {{"query": "具体查询内容", "purpose": "查询目的", "priority": "high/medium/low"}},
        ...
    ]
}}"""

        user_prompt = f"""请为以下研究主题生成{MAX_SONAR_QUERIES}个搜索查询：

研究对象：{company_or_topic}
分析类型：{analysis_type}

对于估值分析，请涵盖以下维度：
1. 公司基本面（最新财务数据、营收、利润）
2. 行业地位和竞争优势
3. 最新新闻和重大事件
4. 市场估值指标（PE、PS、PB等）
5. 未来增长预期和战略方向
6. 风险因素和挑战
7. 分析师观点和评级
8. 行业趋势和宏观环境

请生成精确、可搜索的查询。只返回JSON，不要其他内容。"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,  # 低温度保证结构化输出
                max_tokens=QUERY_PLANNER_MAX_TOKENS
            )
            
            # 解析JSON响应
            # 尝试提取JSON（有时模型会添加额外文本）
            response = response.strip()
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(response)
            
            # 验证和限制查询数量
            if "queries" in plan:
                queries = plan["queries"][:MAX_SONAR_QUERIES]
                
                # 标准化查询格式：如果是字符串，转换为字典
                normalized_queries = []
                for i, q in enumerate(queries):
                    if isinstance(q, str):
                        # 字符串格式，转换为字典
                        normalized_queries.append({
                            "query": q,
                            "purpose": f"查询 {i+1}",
                            "priority": "high" if i < 3 else ("medium" if i < 6 else "low")
                        })
                    elif isinstance(q, dict):
                        # 已经是字典格式
                        normalized_queries.append(q)
                    else:
                        # 其他格式，跳过
                        continue
                
                plan["queries"] = normalized_queries
                return {
                    "status": "success",
                    "plan": plan,
                    "company": company_or_topic
                }
            else:
                raise ValueError("响应中缺少'queries'字段")
                
        except Exception as e:
            # 如果JSON解析失败，返回默认查询计划
            print(f"⚠️ 查询规划失败: {e}")
            print(f"✅ 使用备用查询计划")
            return self._get_fallback_plan(company_or_topic, analysis_type)
    
    def _get_fallback_plan(self, company_or_topic: str, analysis_type: str) -> Dict:
        """
        备用查询计划（当AI生成失败时）
        """
        fallback_queries = [
            {
                "query": f"{company_or_topic} latest financial results revenue profit 2024 2025",
                "purpose": "最新财务数据",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} valuation PE ratio market cap stock price analysis",
                "purpose": "估值指标",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} recent news major events announcements",
                "purpose": "最新新闻",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} competitive advantage market position industry",
                "purpose": "竞争地位",
                "priority": "medium"
            },
            {
                "query": f"{company_or_topic} growth forecast future outlook strategy",
                "purpose": "增长预期",
                "priority": "medium"
            },
            {
                "query": f"{company_or_topic} analyst ratings price target recommendations",
                "purpose": "分析师观点",
                "priority": "medium"
            },
            {
                "query": f"{company_or_topic} risks challenges concerns",
                "purpose": "风险因素",
                "priority": "low"
            },
            {
                "query": f"{company_or_topic} industry trends market conditions macro environment",
                "purpose": "行业趋势",
                "priority": "low"
            }
        ]
        
        return {
            "status": "success",
            "plan": {"queries": fallback_queries[:MAX_SONAR_QUERIES]},
            "company": company_or_topic,
            "note": "使用备用查询计划"
        }

