"""
增强版Qwen3Max API客户端 - 带重试和超时优化
"""
import requests
import json
import urllib3
import time
from typing import List, Dict, Optional
from config import QWEN_API_KEY, QWEN_API_URL, QWEN_MODEL, API_TIMEOUT, MAX_RETRIES

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class QwenClientEnhanced:
    """增强版Qwen3Max API客户端，带重试机制"""
    
    def __init__(self, api_key: str = QWEN_API_KEY):
        self.api_key = api_key
        self.api_url = QWEN_API_URL
        self.model = QWEN_MODEL
        self.timeout = API_TIMEOUT
        self.max_retries = MAX_RETRIES
        
    def _get_headers(self) -> Dict[str, str]:
        """获取API请求头"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """
        与Qwen3Max进行对话（带重试机制）
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            system_prompt: 系统提示词
            
        Returns:
            API响应字典
        """
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False  # 禁用流式响应以提高稳定性
        }
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                if attempt > 0:
                    wait_time = 2 ** attempt  # 指数退避
                    print(f"⏳ 重试 {attempt + 1}/{self.max_retries}，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                print(f"🔄 正在调用Qwen API (尝试 {attempt + 1}/{self.max_retries})...")
                
                response = requests.post(
                    self.api_url,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=self.timeout,
                    verify=False
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ API调用成功")
                    return {
                        "content": result["choices"][0]["message"]["content"],
                        "status": "success",
                        "usage": result.get("usage", {})
                    }
                elif response.status_code == 429:  # 速率限制
                    print(f"⚠️ API速率限制，等待后重试...")
                    time.sleep(5)
                    continue
                elif response.status_code >= 500:  # 服务器错误
                    print(f"⚠️ 服务器错误 {response.status_code}，重试...")
                    continue
                else:
                    return {
                        "error": f"API错误 {response.status_code}: {response.text}",
                        "status": "error"
                    }
                    
            except requests.exceptions.Timeout as e:
                last_error = f"请求超时（{self.timeout}秒）: {str(e)}"
                print(f"⚠️ {last_error}")
                
                # 如果是最后一次尝试，尝试降低token数
                if attempt == self.max_retries - 1 and max_tokens > 3000:
                    print(f"💡 尝试降低token数到 {max_tokens // 2}...")
                    payload["max_tokens"] = max_tokens // 2
                    
            except requests.exceptions.ConnectionError as e:
                last_error = f"连接错误: {str(e)}"
                print(f"⚠️ {last_error}")
                
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ 未知错误: {last_error}")
        
        # 所有重试都失败
        return {
            "error": f"API调用失败（已重试{self.max_retries}次）: {last_error}",
            "status": "error"
        }
    
    def simple_prompt(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        简单的单次提示（便捷方法，带重试）
        
        Args:
            prompt: 用户提示
            temperature: 温度参数
            max_tokens: 最大token数
            system_prompt: 系统提示词
            
        Returns:
            模型响应内容
        """
        messages = [{"role": "user", "content": prompt}]
        result = self.chat(messages, temperature, max_tokens, system_prompt)
        
        if result["status"] == "success":
            return result["content"]
        else:
            raise Exception(f"Qwen API调用失败: {result.get('error', '未知错误')}")

