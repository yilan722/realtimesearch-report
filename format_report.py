"""
报告格式化工具 - 将HTML表格转换为Markdown表格
"""
import re
import sys
from bs4 import BeautifulSoup


def html_table_to_markdown(html_table):
    """将HTML表格转换为Markdown表格"""
    soup = BeautifulSoup(html_table, 'html.parser')
    
    # 提取表头
    headers = []
    thead = soup.find('thead')
    if thead:
        for th in thead.find_all('th'):
            headers.append(th.get_text().strip())
    
    # 提取表格数据
    rows = []
    tbody = soup.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.get_text().strip())
            if row:
                rows.append(row)
    
    # 如果没有找到tbody，尝试直接从table获取
    if not rows:
        for tr in soup.find_all('tr')[1:]:  # 跳过表头行
            row = []
            for td in tr.find_all(['td', 'th']):
                row.append(td.get_text().strip())
            if row:
                rows.append(row)
    
    # 构建Markdown表格
    if not headers or not rows:
        return html_table  # 如果解析失败，返回原始内容
    
    markdown = "\n"
    
    # 表头
    markdown += "| " + " | ".join(headers) + " |\n"
    markdown += "|" + "|".join(["---"] * len(headers)) + "|\n"
    
    # 数据行
    for row in rows:
        # 确保行长度与表头一致
        while len(row) < len(headers):
            row.append("")
        markdown += "| " + " | ".join(row[:len(headers)]) + " |\n"
    
    markdown += "\n"
    return markdown


def format_report(content):
    """格式化整个报告"""
    
    # 1. 转换HTML表格为Markdown
    def replace_table(match):
        html_table = match.group(0)
        return html_table_to_markdown(html_table)
    
    content = re.sub(
        r'<table[^>]*>.*?</table>',
        replace_table,
        content,
        flags=re.DOTALL
    )
    
    # 2. 清理HTML标签
    # 移除<h2>和</h2>
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'### \1\n', content, flags=re.DOTALL)
    content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'#### \1\n', content, flags=re.DOTALL)
    
    # 移除<p>标签，保留内容
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    
    # 移除其他HTML标签
    content = re.sub(r'<[^>]+>', '', content)
    
    # 3. 改进格式
    # 添加分隔线
    content = re.sub(
        r'(## \d\. .*?\n)',
        r'\n---\n\n\1',
        content
    )
    
    # 清理多余空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    return content


def main():
    if len(sys.argv) < 2:
        print("使用方法: python format_report.py <输入文件> [输出文件]")
        print("示例: python format_report.py reports/NVIDIA_Corporation_20251104_145813.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.md', '_formatted.md')
    
    print(f"读取文件: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("格式化报告...")
        formatted_content = format_report(content)
        
        print(f"保存到: {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        print(f"\n✅ 完成！格式化报告已保存到:")
        print(f"   {output_file}")
        print(f"\n报告统计:")
        print(f"   原始长度: {len(content)} 字符")
        print(f"   格式化后: {len(formatted_content)} 字符")
        print(f"   表格数量: {len(re.findall(r'<table', content))}")
        
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

