"""
Perplexity Sonar API客户端 - 实时信息搜索
"""
import asyncio
import aiohttp
import json
from typing import List, Dict, Optional
from config import PERPLEXITY_API_KEY, PERPLEXITY_API_URL, SONAR_MODEL


class SonarClient:
    """Perplexity Sonar API客户端，用于实时信息检索"""
    
    def __init__(self, api_key: str = PERPLEXITY_API_KEY):
        self.api_key = api_key
        self.api_url = PERPLEXITY_API_URL
        self.model = SONAR_MODEL
        
    def _get_headers(self) -> Dict[str, str]:
        """获取API请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def search_async(self, query: str, temperature: float = 0.2) -> Dict:
        """
        异步搜索单个查询
        
        Args:
            query: 搜索查询
            temperature: 温度参数（低温度=更精确的事实）
            
        Returns:
            包含搜索结果的字典
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a precise research assistant. Provide factual, up-to-date information with sources."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # 检查响应格式
                        if "choices" not in result or len(result["choices"]) == 0:
                            return {
                                "query": query,
                                "error": "API响应格式错误：缺少choices",
                                "status": "error"
                            }
                        
                        message = result["choices"][0]["message"]
                        
                        # 提取citations（如果存在）
                        citations = []
                        if "citations" in result:
                            citations = result["citations"]
                        elif "citations" in message:
                            citations = message["citations"]
                        
                        # 检查content是否存在
                        if "content" not in message:
                            return {
                                "query": query,
                                "error": "API响应格式错误：缺少content",
                                "status": "error"
                            }
                        
                        return {
                            "query": query,
                            "content": message["content"],
                            "citations": citations,
                            "status": "success"
                        }
                    else:
                        error_text = await response.text()
                        error_msg = f"API错误 {response.status}: {error_text[:200]}"
                        print(f"  ⚠️  查询失败: {query[:50]}... - {error_msg}")
                        return {
                            "query": query,
                            "error": error_msg,
                            "status": "error"
                        }
        except asyncio.TimeoutError:
            error_msg = f"查询超时: {query[:50]}..."
            print(f"  ⚠️  {error_msg}")
            return {
                "query": query,
                "error": error_msg,
                "status": "error"
            }
        except Exception as e:
            error_msg = f"异常: {str(e)}"
            print(f"  ⚠️  查询异常: {query[:50]}... - {error_msg}")
            import traceback
            print(f"  详细错误: {traceback.format_exc()[:200]}")
            return {
                "query": query,
                "error": error_msg,
                "status": "error"
            }
    
    async def batch_search_async(self, queries: List[str], max_concurrent: int = 5) -> List[Dict]:
        """
        批量并行搜索多个查询（成本优化：节省时间）
        
        Args:
            queries: 查询列表
            max_concurrent: 最大并发数
            
        Returns:
            搜索结果列表
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_search(query: str) -> Dict:
            async with semaphore:
                return await self.search_async(query)
        
        tasks = [limited_search(query) for query in queries]
        results = await asyncio.gather(*tasks)
        return results
    
    def search(self, query: str) -> Dict:
        """同步搜索（包装异步方法）"""
        return asyncio.run(self.search_async(query))
    
    def batch_search(self, queries: List[str], max_concurrent: int = 5) -> List[Dict]:
        """同步批量搜索（包装异步方法）"""
        return asyncio.run(self.batch_search_async(queries, max_concurrent))

