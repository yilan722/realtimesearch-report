"""
表格格式自动修复器
处理Qwen生成的各种错误表格格式
"""
import re
from typing import List


class TableFixer:
    """自动检测并修复markdown表格格式问题"""
    
    def fix_all_tables(self, content: str) -> str:
        """
        修复所有表格格式问题
        
        处理的问题：
        1. 缺少 | 分隔符的紧凑表格
        2. 表格内的格式标记（**bold**, ~~strike~~）
        3. 不一致的列数
        """
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 检测紧凑表格（没有|分隔符的表格）
            if self._is_compact_table_line(line):
                # 收集整个表格
                table_lines = [line]
                i += 1
                while i < len(lines) and self._is_compact_table_line(lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                
                # 修复表格
                fixed_table = self._fix_compact_table(table_lines)
                fixed_lines.extend(fixed_table)
            else:
                # 普通行，但仍需清理表格内的格式标记
                if '|' in line:
                    line = self._clean_table_formatting(line)
                fixed_lines.append(line)
                i += 1
        
        return '\n'.join(fixed_lines)
    
    def _is_compact_table_line(self, line: str) -> bool:
        """
        检测是否是紧凑表格行（没有|分隔符但看起来像表格）
        
        特征：
        - 包含多个大写单词（列标题）
        - 包含数字、货币符号、百分号
        - 字符串很长且没有正常的句子结构
        - 包含多个数据点
        """
        line = line.strip()
        
        # 排除空行、标题行、普通段落
        if not line or line.startswith('#') or len(line) < 40:
            return False
        
        # 排除已经正确格式化的表格
        if line.startswith('|') and line.endswith('|'):
            return False
        
        # 检测特征
        indicators = 0
        
        # 1. 包含多个大写单词连在一起（如：RevenueGrowthMargin）
        uppercase_clusters = len(re.findall(r'[A-Z][a-z]+[A-Z][a-z]+', line))
        if uppercase_clusters >= 2:
            indicators += 2
        
        # 2. 包含多个货币/百分比值
        money_percent = len(re.findall(r'[$%][\d.]+[BMK]?', line))
        if money_percent >= 2:
            indicators += 2
        
        # 3. 包含多个百分比变化（如：+13.5%）
        changes = len(re.findall(r'[+\-]\d+\.?\d*%', line))
        if changes >= 2:
            indicators += 1
        
        # 4. 非常长的行（超过100字符）且没有常见句子词汇
        if len(line) > 100:
            common_words = ['the', 'is', 'are', 'was', 'were', 'will', 'has', 'have']
            if not any(word in line.lower() for word in common_words):
                indicators += 1
        
        # 5. 包含多个连续的数字+单位模式
        number_patterns = len(re.findall(r'\d+\.?\d*[%$BMK]', line))
        if number_patterns >= 3:
            indicators += 1
        
        return indicators >= 3
    
    def _fix_compact_table(self, lines: List[str]) -> List[str]:
        """
        修复紧凑表格，尝试重建为正确的markdown表格
        
        策略：
        1. 识别表头（通常是第一行的大写单词）
        2. 识别数据行
        3. 尝试按模式分割单元格
        """
        if not lines:
            return lines
        
        first_line = lines[0]
        
        # 尝试不同的修复策略
        
        # 策略1：财务数据表格（Segment/Metric + Values）
        if any(keyword in first_line for keyword in ['Segment', 'Metric', 'Ratio', 'Revenue', 'Metric']):
            return self._fix_financial_table(lines)
        
        # 策略2：通用表格（尝试智能分割）
        return self._fix_generic_compact_table(lines)
    
    def _fix_financial_table(self, lines: List[str]) -> List[str]:
        """
        修复财务数据表格
        
        常见模式：
        SegmentRevenueYoY GrowthContributioniPhone$44.6B+13.5%47.4%
        →
        | Segment | Revenue | YoY Growth | Contribution |
        | --- | --- | --- | --- |
        | iPhone | $44.6B | +13.5% | 47.4% |
        """
        fixed_lines = []
        
        for line in lines:
            # 尝试提取列标题和数据
            # 模式1：列标题（大写单词连续）+ 数据
            
            # 检测是否是第一行（标题行）
            if re.match(r'^[A-Z][a-z]+[A-Z]', line):
                # 提取标题
                headers = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', line)
                if headers:
                    # 清理标题，分离粘连的词
                    clean_headers = []
                    for h in headers:
                        # 分离CamelCase
                        h = re.sub(r'([a-z])([A-Z])', r'\1 \2', h)
                        clean_headers.append(h)
                    
                    # 只取前4-6个合理的标题
                    if len(clean_headers) > 6:
                        clean_headers = clean_headers[:6]
                    elif len(clean_headers) < 2:
                        # 可能不是标题行
                        continue
                    
                    # 构建表头
                    header = '| ' + ' | '.join(clean_headers) + ' |'
                    separator = '| ' + ' | '.join(['---'] * len(clean_headers)) + ' |'
                    
                    fixed_lines.append(header)
                    fixed_lines.append(separator)
                    continue
            
            # 数据行：提取数值
            # 模式：Name + 一系列数字/百分比/货币值
            match = re.match(r'^([A-Za-z\s,&]+?)([\$\d%+\-].*)', line)
            if match:
                name = match.group(1).strip()
                data_str = match.group(2)
                
                # 提取所有数据值
                values = re.findall(r'[\$]?[\d.]+[BMK]?%?|[+\-]\d+\.?\d*%', data_str)
                
                if values:
                    row = f'| {name} | ' + ' | '.join(values) + ' |'
                    fixed_lines.append(row)
                    continue
            
            # 如果无法解析，标记为无法解析
            fixed_lines.append(f'<!-- Unable to parse table line: {line[:50]}... -->')
        
        # 如果没有成功修复任何行，返回原始内容并标记
        if len(fixed_lines) < 2:
            return ['```', 'Compact table (unable to parse):'] + lines + ['```', '']
        
        return fixed_lines
    
    def _fix_generic_compact_table(self, lines: List[str]) -> List[str]:
        """通用紧凑表格修复（fallback）"""
        # 如果无法智能修复，至少标记出来
        return ['', '```', 'Compact table detected (manual review needed):'] + lines + ['```', '']
    
    def _clean_table_formatting(self, line: str) -> str:
        """
        清理markdown表格行中的格式标记
        
        移除：
        - **bold**
        - *italic*
        - ~~strikethrough~~
        """
        if not '|' in line:
            return line
        
        # 分割表格单元格
        parts = line.split('|')
        cleaned_parts = []
        
        for part in parts:
            # 移除格式标记，但保留内容
            part = re.sub(r'\*\*([^*]+)\*\*', r'\1', part)  # **bold**
            part = re.sub(r'\*([^*]+)\*', r'\1', part)      # *italic*
            part = re.sub(r'~~([^~]+)~~', r'\1', part)      # ~~strike~~
            part = re.sub(r'__([^_]+)__', r'\1', part)      # __bold__
            part = re.sub(r'_([^_]+)_', r'\1', part)        # _italic_
            
            cleaned_parts.append(part)
        
        return '|'.join(cleaned_parts)


def fix_report_tables(content: str) -> str:
    """
    便捷函数：修复报告中的所有表格
    
    Args:
        content: 原始markdown内容
        
    Returns:
        修复后的markdown内容
    """
    fixer = TableFixer()
    return fixer.fix_all_tables(content)


if __name__ == "__main__":
    # 测试
    test_content = """
# Test Report

Some normal text here.

SegmentRevenueYoY GrowthContribution to Total RevenueiPhone$44.6B+13.5%47.4%Services$27.4B+13.3%29.1%Mac$8.0B+14.8%8.5%

More normal text.

| Already | Correct | Table |
| --- | --- | --- |
| Data | **123** | 456 |

Another compact table:
RatioValueInterpretationGross Margin46.5%Industry-leadingNet Margin23.5%Exceptional

End.
"""
    
    fixer = TableFixer()
    fixed = fixer.fix_all_tables(test_content)
    print(fixed)

