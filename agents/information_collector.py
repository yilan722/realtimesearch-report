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
        try:
            results = self.sonar_client.batch_search(
                query_strings,
                max_concurrent=MAX_CONCURRENT_SEARCHES
            )
        except Exception as e:
            print(f"❌ 批量搜索异常: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "company": query_plan.get("company", "Unknown"),
                "error": f"批量搜索失败: {str(e)}",
                "results": [],
                "success_count": 0,
                "total_queries": len(query_strings)
            }
        
        # 组织结果
        organized_results = []
        success_count = 0
        
        for i, result in enumerate(results):
            query_info = queries[i]
            if result.get("status") == "success":
                organized_results.append({
                    "query": result.get("query", query_info["query"]),
                    "purpose": query_info["purpose"],
                    "priority": query_info["priority"],
                    "content": result.get("content", ""),
                    "citations": result.get("citations", []),
                    "status": "success"
                })
                success_count += 1
            else:
                error_msg = result.get("error", "未知错误")
                print(f"  ❌ 查询失败: {query_info['query'][:50]}... - {error_msg}")
                organized_results.append({
                    "query": result.get("query", query_info["query"]),
                    "purpose": query_info["purpose"],
                    "priority": query_info["priority"],
                    "error": error_msg,
                    "status": "error"
                })
        
        print(f"✅ 搜索完成: {success_count}/{len(query_strings)} 个查询成功")
        
        # 如果所有查询都失败，显示警告
        if success_count == 0:
            print(f"\n⚠️  警告: 所有查询都失败了！")
            print(f"   可能的原因:")
            print(f"   1. API Key无效或过期")
            print(f"   2. 网络连接问题")
            print(f"   3. API限制或配额用完")
            print(f"   4. 查询格式问题")
            print(f"\n   请检查:")
            print(f"   - config.py 中的 PERPLEXITY_API_KEY")
            print(f"   - 网络连接")
            print(f"   - Perplexity API 账户状态")
        
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
                    
                    # 添加引用来源
                    citations = result.get('citations', [])
                    if citations:
                        formatted_text += "**引用来源:**\n"
                        for idx, citation in enumerate(citations, 1):
                            formatted_text += f"{idx}. {citation}\n"
                        formatted_text += "\n"
                    
                    formatted_text += "---\n\n"
        
        return formatted_text

