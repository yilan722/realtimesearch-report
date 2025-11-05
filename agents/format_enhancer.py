"""
格式增强器 - 确保报告格式专业统一
"""
import re
from bs4 import BeautifulSoup
from typing import Dict


class FormatEnhancer:
    """专业格式增强器 - 统一字体、空格、排版"""
    
    def __init__(self):
        self.table_counter = 0
    
    def enhance_report_format(self, report_json: Dict) -> Dict:
        """
        增强报告格式
        
        Args:
            report_json: 原始报告JSON
            
        Returns:
            格式增强后的报告JSON
        """
        enhanced = {}
        
        for key in ["fundamentalAnalysis", "businessSegments", "growthCatalysts", "valuationAnalysis"]:
            if key in report_json:
                enhanced[key] = self._enhance_section(report_json[key], key)
            else:
                enhanced[key] = ""
        
        return enhanced
    
    def _enhance_section(self, content: str, section_name: str) -> str:
        """增强单个章节的格式"""
        if not content:
            return content
        
        # 1. 统一换行符
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # 2. 清理多余空格
        content = re.sub(r' +', ' ', content)  # 多个空格变单个
        content = re.sub(r'\n +', '\n', content)  # 行首空格
        content = re.sub(r' +\n', '\n', content)  # 行尾空格
        
        # 3. 规范化标题格式
        content = self._normalize_headings(content)
        
        # 4. 规范化表格格式
        content = self._normalize_tables(content)
        
        # 5. 规范化段落格式
        content = self._normalize_paragraphs(content)
        
        # 6. 规范化数字格式
        content = self._normalize_numbers(content)
        
        # 7. 清理多余空行
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        return content.strip()
    
    def _normalize_headings(self, content: str) -> str:
        """规范化标题格式"""
        # H2标题 - 确保前后有空行
        content = re.sub(
            r'<h2[^>]*>\s*(.*?)\s*</h2>',
            r'\n\n<h2>\1</h2>\n\n',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # H3标题 - 确保前后有空行
        content = re.sub(
            r'<h3[^>]*>\s*(.*?)\s*</h3>',
            r'\n\n<h3>\1</h3>\n\n',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # H4标题 - 确保前后有空行
        content = re.sub(
            r'<h4[^>]*>\s*(.*?)\s*</h4>',
            r'\n\n<h4>\1</h4>\n\n',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        return content
    
    def _normalize_tables(self, content: str) -> str:
        """规范化表格格式"""
        def format_table(match):
            table_html = match.group(0)
            
            try:
                soup = BeautifulSoup(table_html, 'html.parser')
                table = soup.find('table')
                
                if not table:
                    return table_html
                
                # 添加标准class
                table['class'] = table.get('class', []) + ['metric-table']
                
                # 确保有thead和tbody
                thead = table.find('thead')
                tbody = table.find('tbody')
                
                if not thead:
                    # 第一行作为表头
                    first_row = table.find('tr')
                    if first_row:
                        thead = soup.new_tag('thead')
                        first_row.extract()
                        thead.append(first_row)
                        table.insert(0, thead)
                        
                        # 剩余行放入tbody
                        if not tbody:
                            tbody = soup.new_tag('tbody')
                            for row in table.find_all('tr'):
                                row.extract()
                                tbody.append(row)
                            table.append(tbody)
                
                # 清理表格单元格空格
                for cell in table.find_all(['td', 'th']):
                    if cell.string:
                        cell.string = cell.string.strip()
                
                # 返回格式化的表格（带前后空行）
                return f'\n\n{str(table)}\n\n'
                
            except Exception as e:
                print(f"⚠️ 表格格式化失败: {e}")
                return table_html
        
        content = re.sub(
            r'<table[^>]*>.*?</table>',
            format_table,
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        return content
    
    def _normalize_paragraphs(self, content: str) -> str:
        """规范化段落格式"""
        # P标签 - 确保前后有适当空行
        content = re.sub(
            r'<p[^>]*>\s*(.*?)\s*</p>',
            r'\n<p>\1</p>\n',
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 强调标签
        content = re.sub(r'<strong[^>]*>\s*(.*?)\s*</strong>', r'<strong>\1</strong>', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<em[^>]*>\s*(.*?)\s*</em>', r'<em>\1</em>', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<b[^>]*>\s*(.*?)\s*</b>', r'<strong>\1</strong>', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<i[^>]*>\s*(.*?)\s*</i>', r'<em>\1</em>', content, flags=re.IGNORECASE | re.DOTALL)
        
        return content
    
    def _normalize_numbers(self, content: str) -> str:
        """规范化数字格式"""
        # 确保货币符号和数字之间没有空格
        content = re.sub(r'\$\s+(\d)', r'$\1', content)
        content = re.sub(r'(\d)\s+%', r'\1%', content)
        
        # 确保百分比和正负号格式
        content = re.sub(r'\+\s+(\d)', r'+\1', content)
        content = re.sub(r'-\s+(\d)', r'-\1', content)
        
        return content
    
    def validate_tables(self, content: str, min_tables: int = 3) -> tuple:
        """
        验证表格数量
        
        Returns:
            (是否合格, 实际表格数)
        """
        table_count = len(re.findall(r'<table[^>]*>.*?</table>', content, re.IGNORECASE | re.DOTALL))
        return (table_count >= min_tables, table_count)

