"""
报告格式化器 - 将HTML/JSON报告转换为可读格式
"""
import re
from typing import Dict


class ReportFormatter:
    """报告格式化器：将复杂的HTML报告转换为易读的Markdown"""
    
    @staticmethod
    def html_to_markdown(html_content: str) -> str:
        """
        将HTML内容转换为Markdown格式
        
        Args:
            html_content: HTML字符串
            
        Returns:
            Markdown字符串
        """
        # 保留HTML表格（Streamlit支持）
        # 转换标题
        content = html_content
        
        # h1 -> #
        content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', content, flags=re.DOTALL)
        
        # h2 -> ##
        content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', content, flags=re.DOTALL)
        
        # h3 -> ###
        content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', content, flags=re.DOTALL)
        
        # 转换段落
        content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
        
        # 转换列表
        content = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1', content, flags=re.DOTALL)
        content = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', content, flags=re.DOTALL)
        
        # 转换强调
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', content, flags=re.DOTALL)
        content = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
        
        # 保留链接
        content = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', content, flags=re.DOTALL)
        
        # 清理多余的换行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content.strip()
    
    @staticmethod
    def format_json_report(json_report: Dict, company: str) -> str:
        """
        将JSON格式的报告转换为完整的Markdown报告
        
        Args:
            json_report: 包含四个部分的JSON字典
            company: 公司名称
            
        Returns:
            格式化的Markdown报告
        """
        sections = [
            ("fundamentalAnalysis", "1. 基本面分析 (Fundamental Analysis)"),
            ("businessSegments", "2. 业务板块分析 (Business Segments)"),
            ("growthCatalysts", "3. 增长催化剂 (Growth Catalysts)"),
            ("valuationAnalysis", "4. 估值分析 (Valuation Analysis)")
        ]
        
        report = f"# {company} 深度估值报告\n\n"
        report += f"---\n\n"
        
        for key, title in sections:
            if key in json_report and json_report[key]:
                report += f"## {title}\n\n"
                
                # 转换HTML为Markdown（保留表格）
                content = json_report[key]
                
                # 如果内容包含HTML表格，保留它们
                if '<table' in content:
                    report += content + "\n\n"
                else:
                    # 否则转换为纯Markdown
                    report += ReportFormatter.html_to_markdown(content) + "\n\n"
                
                report += "---\n\n"
        
        return report
    
    @staticmethod
    def clean_html_for_display(html_content: str) -> str:
        """
        清理HTML内容，确保可以在Web界面正确显示
        
        Args:
            html_content: 原始HTML内容
            
        Returns:
            清理后的HTML内容
        """
        # 移除script标签
        content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
        
        # 确保表格有合适的class
        content = re.sub(r'<table(?![^>]*class)', r'<table class="metric-table"', content)
        
        # 确保链接在新窗口打开
        content = re.sub(r'<a(?![^>]*target)', r'<a target="_blank"', content)
        
        return content
    
    @staticmethod
    def extract_key_metrics(report_content: str) -> Dict:
        """
        从报告中提取关键指标
        
        Args:
            report_content: 报告内容
            
        Returns:
            关键指标字典
        """
        metrics = {
            "recommendation": "N/A",
            "target_price": "N/A",
            "pe_ratio": "N/A",
            "growth_rate": "N/A"
        }
        
        # 尝试提取投资建议
        if "买入" in report_content or "Buy" in report_content.upper():
            metrics["recommendation"] = "买入 (Buy)"
        elif "持有" in report_content or "Hold" in report_content.upper():
            metrics["recommendation"] = "持有 (Hold)"
        elif "卖出" in report_content or "Sell" in report_content.upper():
            metrics["recommendation"] = "卖出 (Sell)"
        
        # 提取P/E比率
        pe_match = re.search(r'P/E[:\s]*(\d+\.?\d*)', report_content, re.IGNORECASE)
        if pe_match:
            metrics["pe_ratio"] = pe_match.group(1)
        
        # 提取目标价
        target_match = re.search(r'目标价[:\s]*\$?(\d+\.?\d*)', report_content)
        if not target_match:
            target_match = re.search(r'[Tt]arget [Pp]rice[:\s]*\$?(\d+\.?\d*)', report_content)
        if target_match:
            metrics["target_price"] = f"${target_match.group(1)}"
        
        return metrics

