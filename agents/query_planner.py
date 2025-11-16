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
5. **必须包含股票当前价格和市值的查询**（高优先级）
6. **所有估值指标查询必须明确要求"截止今日"或"最新"数据**

重要规则：
- 必须有一个查询专门获取股票当前价格和市值（使用"current stock price", "market cap", "today", "latest"等关键词）
- 所有估值指标（PE、PS、PB等）查询必须包含时间限定词（"latest", "current", "as of today", "截止今日"等）
- 使用英文进行查询

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

对于估值分析，请涵盖以下维度（必须包含）：
1. **股票当前价格和市值**（高优先级）：当前股价、市值、交易量等实时数据
2. **公司基本介绍**（高优先级）：公司成立背景、发展历史、核心团队、管理层背景
3. 公司基本面（最新财务数据、营收、利润）
4. **竞争和合作关系**（高优先级）：主要竞争对手、战略合作伙伴、合作关系
5. **供应链关系**（中优先级）：主要供应商、客户关系、供应链稳定性
6. 行业地位和竞争优势
7. 最新新闻和重大事件
8. **市场估值指标（截止今日最新数据）**：PE市盈率、PS市销率、PB市净率等估值指标，必须明确要求"截止今日"或"最新"数据
9. 未来增长预期和战略方向
10. 风险因素和挑战
11. 分析师观点和评级
12. 行业趋势和宏观环境

重要要求：
- 必须包含一个查询专门获取股票当前价格和市值（作为高优先级查询）
- 必须包含一个查询专门获取公司基本介绍（成立背景、团队、管理层）
- 必须包含一个查询专门获取竞争和合作关系（竞争对手、合作伙伴）
- 必须包含一个查询专门获取供应链关系（供应商、客户关系）
- 所有估值指标相关的查询必须明确包含"截止今日"、"最新"、"current"、"latest"等时间限定词
- 查询应该具体、可搜索，使用英文

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
                "query": f"{company_or_topic} current stock price market cap market capitalization today latest",
                "purpose": "股票当前价格和市值",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} company background founding history management team executives leadership",
                "purpose": "公司基本介绍（成立背景、团队）",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} latest financial results revenue profit 2024 2025",
                "purpose": "最新财务数据",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} competitors competitive landscape strategic partnerships alliances",
                "purpose": "竞争和合作关系",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} supply chain suppliers customers key relationships",
                "purpose": "供应链关系",
                "priority": "medium"
            },
            {
                "query": f"{company_or_topic} PE ratio PS ratio PB ratio valuation metrics latest current as of today",
                "purpose": "估值指标（截止今日最新数据）",
                "priority": "high"
            },
            {
                "query": f"{company_or_topic} recent news major events announcements",
                "purpose": "最新新闻",
                "priority": "medium"
            },
            {
                "query": f"{company_or_topic} growth forecast future outlook strategy",
                "purpose": "增长预期",
                "priority": "medium"
            }
        ]
        
        return {
            "status": "success",
            "plan": {"queries": fallback_queries[:MAX_SONAR_QUERIES]},
            "company": company_or_topic,
            "note": "使用备用查询计划"
        }

