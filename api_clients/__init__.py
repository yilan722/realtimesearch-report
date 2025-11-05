"""
API客户端模块
"""
from .sonar_client import SonarClient
from .qwen_client import QwenClient

# 尝试导入增强版，如果失败则使用标准版
try:
    from .qwen_client_enhanced import QwenClientEnhanced
    # 使用增强版作为默认
    QwenClient = QwenClientEnhanced
except:
    pass

__all__ = ['SonarClient', 'QwenClient']

