"""
配置文件示例
复制此文件为 config.py 并填入你的真实API密钥
"""

# Perplexity API配置
PERPLEXITY_API_KEY = "your_perplexity_api_key_here"
PERPLEXITY_API_BASE = "https://api.perplexity.ai"
PERPLEXITY_MODEL = "llama-3.1-sonar-large-128k-online"

# Qwen API配置
QWEN_API_KEY = "your_qwen_api_key_here"
QWEN_API_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-max-latest"

# API调用配置
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120
DEEP_ANALYSIS_MAX_TOKENS = 16000
QUICK_ANALYSIS_MAX_TOKENS = 8000

# 搜索配置
MAX_SEARCH_QUERIES = 8
SEARCH_TIMEOUT = 30

