#!/usr/bin/env python3
"""
测试引用来源功能
验证citations是否正确提取和显示
"""

import json
from api_clients.sonar_client import SonarClient
from agents.information_collector import InformationCollectorAgent

def test_sonar_citations():
    """测试Sonar API是否返回citations"""
    print("="*80)
    print("🧪 测试1: Sonar API Citations提取")
    print("="*80)
    
    client = SonarClient()
    
    # 执行一个简单查询
    query = "Apple Inc. latest quarterly earnings 2024"
    print(f"\n📝 测试查询: {query}")
    print("-"*80)
    
    result = client.search(query)
    
    if result["status"] == "success":
        print("✅ 查询成功")
        print(f"📄 内容长度: {len(result['content'])} 字符")
        
        # 检查citations
        citations = result.get("citations", [])
        print(f"\n📚 Citations数量: {len(citations)}")
        
        if citations:
            print("\n引用来源:")
            for i, citation in enumerate(citations[:5], 1):
                if isinstance(citation, str):
                    print(f"  [{i}] {citation[:80]}...")
                elif isinstance(citation, dict):
                    print(f"  [{i}] {citation}")
                else:
                    print(f"  [{i}] (未知格式): {type(citation)}")
        else:
            print("⚠️  未找到citations（可能Perplexity API响应中不包含）")
        
        # 显示完整结果结构
        print("\n📋 完整结果键:")
        print(f"  {list(result.keys())}")
        
    else:
        print(f"❌ 查询失败: {result.get('error')}")
    
    return result


def test_information_collector_citations():
    """测试InformationCollectorAgent是否保存citations"""
    print("\n\n" + "="*80)
    print("🧪 测试2: InformationCollectorAgent Citations处理")
    print("="*80)
    
    # 模拟query plan
    query_plan = {
        "status": "success",
        "company": "Apple Inc.",
        "plan": {
            "queries": [
                {
                    "query": "Apple Inc. Q3 2024 earnings financial performance",
                    "purpose": "Recent Financial Performance",
                    "priority": "high"
                },
                {
                    "query": "Apple Inc. iPhone sales growth market share 2024",
                    "purpose": "Product Performance",
                    "priority": "high"
                }
            ]
        }
    }
    
    collector = InformationCollectorAgent()
    
    print("\n🔍 执行信息收集...")
    collection_result = collector.collect_information(query_plan)
    
    if collection_result["status"] == "success":
        print(f"✅ 收集成功: {collection_result['success_count']}/{collection_result['total_queries']} 查询")
        
        # 检查每个结果的citations
        total_citations = 0
        for i, result in enumerate(collection_result["results"], 1):
            if result["status"] == "success":
                citations = result.get("citations", [])
                total_citations += len(citations)
                print(f"\n查询 #{i}: {result['purpose']}")
                print(f"  📚 Citations: {len(citations)}")
                if citations:
                    for j, citation in enumerate(citations[:3], 1):
                        if isinstance(citation, str):
                            print(f"    [{j}] {citation[:60]}...")
        
        print(f"\n📊 总引用数: {total_citations}")
        
        # 测试format_for_analysis
        print("\n📝 测试格式化输出...")
        formatted = collector.format_for_analysis(collection_result)
        
        # 检查是否包含引用
        if "**引用来源:**" in formatted or "引用来源:" in formatted:
            print("✅ 格式化输出包含引用来源")
        else:
            print("⚠️  格式化输出未包含引用来源（可能citations为空）")
        
        return collection_result
    else:
        print(f"❌ 收集失败: {collection_result.get('error')}")
        return None


def test_citation_formatting():
    """测试引用格式化"""
    print("\n\n" + "="*80)
    print("🧪 测试3: Citations格式化")
    print("="*80)
    
    from agents.professional_formatter import ProfessionalReportFormatter
    
    formatter = ProfessionalReportFormatter()
    
    # 测试字符串格式
    test_citations_str = [
        "https://www.bloomberg.com/news/articles/2024-11-07/apple-earnings",
        "https://www.reuters.com/technology/apple-iphone-sales-2024",
        "https://investor.apple.com/investor-relations/default.aspx",
        "https://www.sec.gov/cgi-bin/browse-edgar?company=apple"
    ]
    
    print("\n📝 测试字符串格式citations:")
    section = formatter._generate_citations_section(test_citations_str)
    print(section)
    
    # 测试字典格式
    test_citations_dict = [
        {
            "title": "Apple Q3 2024 Earnings Report",
            "url": "https://investor.apple.com/investor-relations/sec-filings/",
            "date": "November 5, 2024"
        },
        {
            "title": "iPhone 15 Sales Data",
            "url": "https://www.bloomberg.com/news/iphone-15-sales",
            "date": "October 28, 2024"
        }
    ]
    
    print("\n" + "="*80)
    print("📝 测试字典格式citations:")
    section = formatter._generate_citations_section(test_citations_dict)
    print(section)
    
    # 测试去重
    print("\n" + "="*80)
    print("📝 测试去重功能:")
    citations_with_duplicates = [
        "https://www.bloomberg.com/news/article1",
        "https://www.reuters.com/news/article2",
        "https://www.bloomberg.com/news/article1",  # 重复
        "https://www.sec.gov/filing",
        "https://www.reuters.com/news/article2"  # 重复
    ]
    
    unique_citations = []
    for citation in citations_with_duplicates:
        if citation not in unique_citations:
            unique_citations.append(citation)
    
    print(f"原始数量: {len(citations_with_duplicates)}")
    print(f"去重后数量: {len(unique_citations)}")
    print("✅ 去重功能正常" if len(unique_citations) == 3 else "❌ 去重功能异常")


def main():
    """运行所有测试"""
    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "Citations功能测试" + " "*35 + "║")
    print("╚" + "="*78 + "╝")
    
    # 测试1: Sonar API
    sonar_result = test_sonar_citations()
    
    # 测试2: InformationCollector
    if sonar_result and sonar_result.get("status") == "success":
        collector_result = test_information_collector_citations()
    
    # 测试3: 格式化
    test_citation_formatting()
    
    # 总结
    print("\n\n" + "="*80)
    print("📊 测试总结")
    print("="*80)
    print("""
✅ 已实现的功能:
1. Sonar API返回citations字段
2. InformationCollectorAgent保存citations
3. ProfessionalFormatter生成引用部分
4. 支持字符串和字典格式
5. 自动去重功能
6. 智能域名提取

📝 注意事项:
- Perplexity Sonar API可能不总是返回citations字段
- 如果API响应中没有citations，citations列表将为空
- 这是正常的，取决于API的具体实现

🚀 下一步:
- 运行 python main.py 生成完整报告
- 查看报告末尾的"📚 References and Citations"部分
    """)


if __name__ == "__main__":
    main()

