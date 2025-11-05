"""
Qwen3Max API客户端 - 深度推理和分析
"""
import requests
import json
import urllib3
from typing import List, Dict, Optional
from config import QWEN_API_KEY, QWEN_API_URL, QWEN_MODEL

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class QwenClient:
    """Qwen3Max API客户端，用于深度推理和分析"""
    
    def __init__(self, api_key: str = QWEN_API_KEY):
        self.api_key = api_key
        self.api_url = QWEN_API_URL
        self.model = QWEN_MODEL
        
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
        与Qwen3Max进行对话
        
        Args:
            messages: 消息列表
            temperature: 温度参数（高温度=更有创造性）
            max_tokens: 最大token数
            system_prompt: 系统提示词
            
        Returns:
            API响应字典
        """
        # 如果提供了系统提示词，插入到消息开头
        if system_prompt:
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=300,  # 增加到5分钟
                verify=False  # 禁用SSL验证以解决证书问题
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "content": result["choices"][0]["message"]["content"],
                    "status": "success",
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "error": f"API错误 {response.status_code}: {response.text}",
                    "status": "error"
                }
        except Exception as e:
            return {
                "error": str(e),
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
        简单的单次提示（便捷方法）
        
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

