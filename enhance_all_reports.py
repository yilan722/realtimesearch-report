#!/usr/bin/env python3
"""
批量增强所有报告的脚本
"""
import os
import glob
from report_enhancer import ReportEnhancer

def main():
    """批量增强reports目录下的所有.md文件"""
    reports_dir = "reports"
    
    # 查找所有未增强的报告
    all_reports = glob.glob(f"{reports_dir}/*.md")
    # 排除已经增强过的
    reports_to_enhance = [r for r in all_reports if '_enhanced' not in r and '_formatted' not in r]
    
    if not reports_to_enhance:
        print("✅ 没有找到需要增强的报告")
        return
    
    print(f"找到 {len(reports_to_enhance)} 个报告需要增强\n")
    
    enhancer = ReportEnhancer()
    
    success_count = 0
    for report_path in reports_to_enhance:
        print(f"\n{'='*80}")
        print(f"正在处理: {os.path.basename(report_path)}")
        print(f"{'='*80}")
        
        try:
            enhanced_path = enhancer.enhance_report(report_path)
            print(f"✅ 成功: {enhanced_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ 失败: {e}")
    
    print(f"\n{'='*80}")
    print(f"✨ 完成! 成功增强 {success_count}/{len(reports_to_enhance)} 个报告")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()

