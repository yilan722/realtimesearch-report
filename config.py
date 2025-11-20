import os
import streamlit as st

# --- 核心逻辑：从安全的地方读取配置 ---
def get_conf(key, default_value=None):
    """
    优先从 Streamlit Secrets 读取 (云端部署时)
    如果没有，再尝试从环境变量读取 (本地开发或Docker时)
    如果都没有，返回默认值
    """
    # 1. 检查 Streamlit Secrets (云端)
    if hasattr(st, "secrets") and key in st.secrets:
        return st.secrets[key]
    
    # 2. 检查系统环境变量 (本地/容器)
    return os.getenv(key, default_value)

# ==========================================
#    以下变量会自动从 Secrets 中获取值
#    GitHub 上只会有这些变量名，不会有真实 Key
# ==========================================

# API配置
PERPLEXITY_API_KEY = get_conf("PERPLEXITY_API_KEY", "") # 留空或填个假占位符
PERPLEXITY_API_URL = get_conf("PERPLEXITY_API_URL", "https://api.perplexity.ai/chat/completions")

QWEN_API_KEY = get_conf("QWEN_API_KEY", "")
QWEN_API_URL = get_conf("QWEN_API_URL", "https://api.nuwaapi.com/v1/chat/completions")

# 模型选择
SONAR_MODEL = get_conf("SONAR_MODEL", "sonar")
QWEN_MODEL = get_conf("QWEN_MODEL", "qwen-max")

# 成本优化参数 (数字类型需要转换，因为Secrets读取的可能是字符串，但在TOML里直接写数字通常会自动识别)
MAX_SONAR_QUERIES = int(get_conf("MAX_SONAR_QUERIES", 8))
QUERY_PLANNER_MAX_TOKENS = int(get_conf("QUERY_PLANNER_MAX_TOKENS", 500))
DEEP_ANALYSIS_MAX_TOKENS = int(get_conf("DEEP_ANALYSIS_MAX_TOKENS", 16000))

# API超时设置
API_TIMEOUT = int(get_conf("API_TIMEOUT", 300))
MAX_RETRIES = int(get_conf("MAX_RETRIES", 3))

# 并发设置
MAX_CONCURRENT_SEARCHES = int(get_conf("MAX_CONCURRENT_SEARCHES", 5))

# 缓存设置
# 注意：get_conf读取布尔值可能需要特殊处理，但这取决于你的TOML写法
# 这里做一个简单的判断
_enable_cache_raw = get_conf("ENABLE_CACHE", True)
if isinstance(_enable_cache_raw, str):
    ENABLE_CACHE = _enable_cache_raw.lower() == 'true'
else:
    ENABLE_CACHE = bool(_enable_cache_raw)

CACHE_EXPIRY_HOURS = int(get_conf("CACHE_EXPIRY_HOURS", 6))
