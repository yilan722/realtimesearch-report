import re

class TextCleaner:
    """
    用于清洗和标准化文本的工具类，
    主要用于处理网页抓取回来的原始内容。
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        基础清洗：去除多余空白、HTML标签残留等
        """
        if not text:
            return ""
        
        # 1. 移除多余的空白字符 (换行符转空格，多个空格转一个)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 2. 移除常见的干扰字符
        # 可以根据需要添加更多正则规则
        
        return text

    @staticmethod
    def extract_markdown_content(text: str) -> str:
        """
        保留 Markdown 格式的清洗（如果需要保留结构）
        """
        if not text:
            return ""
        # 目前简单返回，可扩展逻辑
        return text.strip()
