#!/usr/bin/env python3
"""
快速演示脚本 - 展示系统核心功能
运行: python demo.py
"""
import sys
from main import ValuationReportSystem


def print_header(text):
    """打印漂亮的标题"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def demo_intro():
    """系统介绍"""
    print_header("🚀 深度估值报告系统 - 演示")
    
    print("""
    本系统结合了:
    ✅ Perplexity Sonar - 实时信息搜索
    ✅ Qwen3-Max - 深度推理分析
    
    三层优化架构:
    1️⃣  查询规划层 (Qwen轻量) - 生成精确查询
    2️⃣  信息收集层 (Sonar并行) - 快速收集信息  
    3️⃣  深度分析层 (Qwen深度) - 生成专业报告
    
    优势:
    💰 成本节省 30-40%
    ⚡ 速度提升 2-3倍
    📊 质量优于 sonar-deep-research
    """)
    
    input("\n按 Enter 开始演示...")


def demo_1_basic():
    """演示1: 基本报告生成"""
    print_header("演示 1: 生成基本估值报告")
    
    print("我们将为 'Apple Inc' 生成一份完整的估值报告\n")
    print("这个过程包括:")
    print("  → 第1步: 智能规划8个精确的搜索查询")
    print("  → 第2步: 并行搜索收集实时信息")
    print("  → 第3步: 深度分析生成专业报告")
    print()
    
    choice = input("是否继续? (y/n): ").lower()
    if choice != 'y':
        print("跳过此演示")
        return
    
    try:
        system = ValuationReportSystem()
        
        result = system.generate_report(
            company="Apple Inc",
            report_type="comprehensive",
            save_to_file=True
        )
        
        if result["status"] == "success":
            print("\n" + "="*80)
            print("✅ 报告生成成功!")
            print("="*80)
            
            # 显示元数据
            metadata = result["metadata"]
            print(f"\n📊 生成统计:")
            print(f"   • 执行查询: {metadata['queries_successful']}/{metadata['queries_executed']}")
            print(f"   • 总耗时: {metadata['elapsed_time']:.2f}秒")
            print(f"   • 报告长度: {len(result['report'])} 字符")
            print(f"   • 保存位置: {metadata['saved_file']}")
            
            # 显示报告预览
            print(f"\n📄 报告预览 (前800字符):")
            print("-"*80)
            print(result["report"][:800])
            print("\n... (查看完整报告请打开保存的文件) ...")
            print("-"*80)
        else:
            print(f"\n❌ 报告生成失败: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")
        print("    请检查API配置是否正确")


def demo_2_quick():
    """演示2: 快速分析模式"""
    print_header("演示 2: 快速分析模式 (低成本)")
    
    print("快速分析模式适用于:")
    print("  • 快速了解一个公司")
    print("  • 批量筛选候选公司")
    print("  • 成本敏感的场景")
    print()
    print("成本约为完整报告的 30%，速度更快!")
    print()
    
    companies = ["Tesla", "Microsoft"]
    print(f"我们将快速分析: {', '.join(companies)}\n")
    
    choice = input("是否继续? (y/n): ").lower()
    if choice != 'y':
        print("跳过此演示")
        return
    
    try:
        system = ValuationReportSystem()
        
        for company in companies:
            print(f"\n📊 正在分析: {company}")
            print("-"*80)
            
            summary = system.quick_analysis(company)
            
            print(summary)
            print("-"*80)
            
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")


def demo_3_compare():
    """演示3: 比较分析"""
    print_header("演示 3: 比较分析")
    
    print("比较分析可以:")
    print("  • 对比多个公司的投资价值")
    print("  • 进行行业内选股")
    print("  • 识别相对优势")
    print()
    
    companies = ["Apple", "Microsoft", "Google"]
    print(f"我们将比较: {', '.join(companies)}")
    print("⚠️  注意: 此功能会执行较多API调用，需要更多时间\n")
    
    choice = input("是否继续? (y/n): ").lower()
    if choice != 'y':
        print("跳过此演示")
        return
    
    try:
        system = ValuationReportSystem()
        
        comparison = system.compare_companies(companies)
        
        if comparison["status"] == "success":
            print("\n" + "="*80)
            print("✅ 比较分析完成!")
            print("="*80)
            print("\n📊 比较报告:")
            print("-"*80)
            print(comparison["comparison"])
            print("-"*80)
        else:
            print(f"\n❌ 比较分析失败: {comparison.get('error')}")
            
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")


def demo_4_custom():
    """演示4: 自定义分析"""
    print_header("演示 4: 自定义分析")
    
    print("你可以分析任何公司或主题!")
    print()
    
    company = input("请输入公司名称 (例如: NVIDIA, 特斯拉): ").strip()
    
    if not company:
        print("未输入公司名称，跳过此演示")
        return
    
    print(f"\n将为 '{company}' 生成报告")
    print("选择报告类型:")
    print("  1. 快速分析 (30秒, 低成本)")
    print("  2. 完整报告 (2-3分钟, 高质量)")
    
    choice = input("请选择 (1/2): ").strip()
    
    try:
        system = ValuationReportSystem()
        
        if choice == "1":
            print(f"\n🚀 正在快速分析 '{company}'...")
            summary = system.quick_analysis(company)
            print("\n" + "="*80)
            print(summary)
            print("="*80)
            
        elif choice == "2":
            print(f"\n🚀 正在生成完整报告 '{company}'...")
            result = system.generate_report(company, save_to_file=True)
            
            if result["status"] == "success":
                print("\n✅ 报告生成成功!")
                print(f"   文件: {result['metadata']['saved_file']}")
                print(f"   耗时: {result['metadata']['elapsed_time']:.2f}秒")
            else:
                print(f"\n❌ 报告生成失败: {result.get('error')}")
        else:
            print("无效选择")
            
    except Exception as e:
        print(f"\n❌ 演示失败: {e}")


def main():
    """主函数"""
    demo_intro()
    
    demos = [
        ("基本报告生成", demo_1_basic),
        ("快速分析模式", demo_2_quick),
        ("比较分析", demo_3_compare),
        ("自定义分析", demo_4_custom)
    ]
    
    while True:
        print("\n" + "="*80)
        print("选择演示:")
        for i, (name, _) in enumerate(demos, 1):
            print(f"  {i}. {name}")
        print("  0. 退出")
        print("="*80)
        
        choice = input("\n请选择 (0-4): ").strip()
        
        if choice == "0":
            print("\n感谢使用深度估值报告系统! 👋")
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                name, func = demos[idx]
                func()
                
                input("\n按 Enter 继续...")
            else:
                print("❌ 无效选择，请输入 0-4")
        except ValueError:
            print("❌ 请输入数字")
        except KeyboardInterrupt:
            print("\n\n操作被用户中断")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            input("\n按 Enter 继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见!")
        sys.exit(0)

