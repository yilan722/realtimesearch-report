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
        
        # 根据max_tokens动态调整超时时间
        # 16000 tokens大约需要10-15分钟，设置更长的超时时间
        timeout_seconds = max(600, int(max_tokens / 20))  # 至少10分钟，或根据tokens计算
        
        try:
            response = requests.post(
                self.api_url,
                headers=self._get_headers(),
                json=payload,
                timeout=timeout_seconds,  # 动态超时时间
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
                # 解析错误信息，提供更友好的提示
                error_info = {
                    "error": f"API错误 {response.status_code}: {response.text}",
                    "status": "error"
                }
                
                try:
                    error_json = response.json()
                    if "error" in error_json:
                        error_detail = error_json["error"]
                        error_message = error_detail.get("message", "")
                        error_code = error_detail.get("code", "")
                        
                        # 处理额度不足的情况
                        if response.status_code == 403 and "insufficient_user_quota" in error_code:
                            error_info["error"] = f"API额度不足: {error_message}\n\n" \
                                                 f"💡 可能的原因：\n" \
                                                 f"1. API计费可能有延迟，请稍后重试\n" \
                                                 f"2. 请检查API密钥是否正确\n" \
                                                 f"3. 请登录API服务商控制台查看实际余额\n" \
                                                 f"4. 如果余额充足，可能是API服务商的计费系统问题\n\n" \
                                                 f"🔧 建议操作：\n" \
                                                 f"- 等待几分钟后重试\n" \
                                                 f"- 检查API服务商控制台的余额和账单\n" \
                                                 f"- 确认使用的是正确的API密钥"
                        else:
                            error_info["error"] = f"API错误 {response.status_code}: {error_message}"
                except:
                    pass  # 如果无法解析JSON，使用原始错误信息
                
                return error_info
        except requests.exceptions.Timeout as e:
            return {
                "error": f"请求超时（{timeout_seconds}秒）: {str(e)}\n\n"
                        f"💡 可能的原因：\n"
                        f"1. 生成内容过长（max_tokens={max_tokens}），需要更长时间\n"
                        f"2. API服务器响应较慢\n"
                        f"3. 网络连接不稳定\n\n"
                        f"🔧 建议操作：\n"
                        f"- 尝试减少max_tokens参数\n"
                        f"- 检查网络连接\n"
                        f"- 稍后重试",
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

