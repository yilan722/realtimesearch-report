#!/usr/bin/env python3
"""
测试清洁格式生成
"""
from main import ValuationReportSystem
import sys

def test_format():
    """测试新的格式生成"""
    print("="*80)
    print("🧪 测试清洁格式生成")
    print("="*80)
    
    # 使用简单的公司测试
    company = sys.argv[1] if len(sys.argv) > 1 else "TSLA"
    
    print(f"\n📊 正在为 {company} 生成报告...")
    print("   使用改进的prompt，强制要求正确的markdown表格格式\n")
    
    system = ValuationReportSystem()
    
    try:
        result = system.generate_report(
            company=company,
            report_type="comprehensive",
            save_to_file=True
        )
        
        if result["status"] == "success":
            print("\n" + "="*80)
            print("✅ 报告生成成功!")
            print("="*80)
            
            report_file = result["metadata"]["saved_file"]
            print(f"\n📄 报告文件: {report_file}")
            
            # 检查表格格式
            print("\n🔍 检查表格格式...")
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计表格
            table_count = content.count('| ---')
            print(f"   找到 {table_count} 个正确格式的表格")
            
            # 检查是否有问题格式
            issues = []
            if '**' in content and '|' in content:
                # 检查表格里是否有**
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '|' in line and ('**' in line or '~~' in line or line.count('*') > 2):
                        issues.append(f"第{i+1}行可能有格式问题: {line[:60]}")
            
            if issues:
                print(f"\n⚠️  发现 {len(issues)} 个潜在格式问题:")
                for issue in issues[:5]:  # 只显示前5个
                    print(f"   - {issue}")
            else:
                print("   ✅ 未发现格式问题")
            
            # 显示第一个表格示例
            import re
            tables = re.findall(r'\|[^\n]+\|\n\|[\s\-|]+\|\n(?:\|[^\n]+\|\n)+', content)
            if tables:
                print(f"\n📊 第一个表格示例:")
                print("-"*80)
                print(tables[0][:300])
                print("-"*80)
            
            print(f"\n💡 现在查看报告:")
            print(f"   code {report_file}")
            
        else:
            print(f"\n❌ 生成失败: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_format()

