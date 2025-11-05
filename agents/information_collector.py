"""
信息收集Agent - 第二层：并行实时信息搜索
使用Sonar API并行执行多个查询，快速收集全面信息
"""
from typing import List, Dict
from api_clients.sonar_client import SonarClient
from config import MAX_CONCURRENT_SEARCHES


class InformationCollectorAgent:
    """
    信息收集Agent：并行执行Sonar搜索
    目标：最快速度获取最全面的实时信息
    """
    
    def __init__(self, sonar_client: SonarClient = None):
        self.sonar_client = sonar_client or SonarClient()
        
    def collect_information(self, query_plan: Dict) -> Dict:
        """
        根据查询计划收集信息
        
        Args:
            query_plan: 来自QueryPlannerAgent的查询计划
            
        Returns:
            包含所有搜索结果的字典
        """
        # 验证查询计划格式
        if not isinstance(query_plan, dict):
            return {
                "status": "error",
                "error": f"查询计划格式错误: 期望字典，得到 {type(query_plan)}"
            }
        
        if query_plan.get("status") != "success":
            return {
                "status": "error",
                "error": "无效的查询计划"
            }
        
        if "plan" not in query_plan or "queries" not in query_plan["plan"]:
            return {
                "status": "error",
                "error": "查询计划缺少必需字段"
            }
        
        queries = query_plan["plan"]["queries"]
        query_strings = [q["query"] for q in queries]
        
        print(f"🔍 开始并行搜索 {len(query_strings)} 个查询...")
        
        # 并行执行所有查询（成本优化：节省时间）
        results = self.sonar_client.batch_search(
            query_strings,
            max_concurrent=MAX_CONCURRENT_SEARCHES
        )
        
        # 组织结果
        organized_results = []
        success_count = 0
        
        for i, result in enumerate(results):
            query_info = queries[i]
            if result["status"] == "success":
                organized_results.append({
                    "query": result["query"],
                    "purpose": query_info["purpose"],
                    "priority": query_info["priority"],
                    "content": result["content"],
                    "status": "success"
                })
                success_count += 1
            else:
                organized_results.append({
                    "query": result["query"],
                    "purpose": query_info["purpose"],
                    "priority": query_info["priority"],
                    "error": result.get("error", "未知错误"),
                    "status": "error"
                })
        
        print(f"✅ 搜索完成: {success_count}/{len(query_strings)} 个查询成功")
        
        return {
            "status": "success",
            "company": query_plan["company"],
            "results": organized_results,
            "success_count": success_count,
            "total_queries": len(query_strings)
        }
    
    def format_for_analysis(self, collection_result: Dict) -> str:
        """
        将收集的信息格式化为分析用的文本
        
        Args:
            collection_result: 收集结果
            
        Returns:
            格式化的文本
        """
        if collection_result["status"] != "success":
            return "信息收集失败"
        
        formatted_text = f"# {collection_result['company']} - 实时信息汇总\n\n"
        formatted_text += f"收集时间: 当前\n"
        formatted_text += f"成功查询: {collection_result['success_count']}/{collection_result['total_queries']}\n\n"
        
        # 按优先级组织信息
        for priority in ["high", "medium", "low"]:
            priority_results = [
                r for r in collection_result["results"]
                if r.get("priority") == priority and r["status"] == "success"
            ]
            
            if priority_results:
                priority_label = {
                    "high": "核心信息",
                    "medium": "重要信息",
                    "low": "补充信息"
                }
                formatted_text += f"## {priority_label[priority]}\n\n"
                
                for result in priority_results:
                    formatted_text += f"### {result['purpose']}\n"
                    formatted_text += f"查询: {result['query']}\n\n"
                    formatted_text += f"{result['content']}\n\n"
                    formatted_text += "---\n\n"
        
        return formatted_text

