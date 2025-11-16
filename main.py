"""
深度估值报告系统 - 主程序
整合Sonar实时搜索和Qwen3Max深度推理
"""
import time
from datetime import datetime
from typing import Optional
from agents import QueryPlannerAgent, InformationCollectorAgent, DeepAnalystAgent
from agents.professional_formatter import ProfessionalReportFormatter
from api_clients import SonarClient, QwenClient


class ValuationReportSystem:
    """
    估值报告系统主类
    
    架构：
    1. QueryPlanner (Qwen轻量) -> 生成精确查询计划
    2. InformationCollector (Sonar并行) -> 收集实时信息
    3. DeepAnalyst (Qwen深度) -> 生成专业报告
    """
    
    def __init__(self):
        # 初始化API客户端
        self.sonar_client = SonarClient()
        self.qwen_client = QwenClient()
        
        # 初始化Agents
        self.query_planner = QueryPlannerAgent(self.qwen_client)
        self.information_collector = InformationCollectorAgent(self.sonar_client)
        self.deep_analyst = DeepAnalystAgent(self.qwen_client)
        self.professional_formatter = ProfessionalReportFormatter()
        
    def generate_report(
        self,
        company: str,
        analysis_type: str = "valuation",
        report_type: str = "comprehensive",
        save_to_file: bool = True,
        generate_pdf: bool = True,  # 默认生成PDF
        keep_markdown: bool = True  # 是否保留Markdown文件
    ) -> dict:
        """
        生成完整的估值报告
        
        Args:
            company: 公司名称或股票代码
            analysis_type: 分析类型
            report_type: 报告类型（comprehensive=综合, quick=快速）
            save_to_file: 是否保存到文件
            generate_pdf: 是否生成PDF版本（默认True）
            keep_markdown: 是否保留Markdown文件（默认True）
            
        Returns:
            包含报告内容的字典
        """
        print("="*80)
        print(f"🚀 深度估值报告系统")
        print(f"📊 分析对象: {company}")
        print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        start_time = time.time()
        
        # 阶段1: 查询规划（Qwen轻量调用）
        print("\n【阶段1/3】查询规划")
        print("-"*80)
        query_plan = self.query_planner.generate_search_plan(company, analysis_type)
        
        if query_plan["status"] != "success":
            return {"status": "error", "error": "查询规划失败"}
        
        print(f"✅ 生成了 {len(query_plan['plan']['queries'])} 个搜索查询")
        for i, q in enumerate(query_plan['plan']['queries'], 1):
            print(f"   {i}. [{q['priority']}] {q['purpose']}: {q['query'][:60]}...")
        
        # 阶段2: 信息收集（Sonar并行调用）
        print("\n【阶段2/3】信息收集")
        print("-"*80)
        collection_result = self.information_collector.collect_information(query_plan)
        
        if collection_result["status"] != "success":
            return {"status": "error", "error": "信息收集失败"}
        
        # 格式化信息用于分析
        formatted_info = self.information_collector.format_for_analysis(collection_result)
        
        # 阶段3: 深度分析（Qwen深度推理）
        print("\n【阶段3/3】深度分析")
        print("-"*80)
        
        if report_type == "quick":
            analysis_result = self.deep_analyst.generate_quick_summary(company, formatted_info)
        else:
            analysis_result = self.deep_analyst.generate_valuation_report(
                company,
                formatted_info,
                report_type
            )
        
        if analysis_result["status"] != "success":
            error_msg = analysis_result.get("error", "未知错误")
            print(f"❌ 深度分析错误详情: {error_msg}")
            return {"status": "error", "error": f"深度分析失败: {error_msg}"}
        
        # 计算总耗时
        elapsed_time = time.time() - start_time
        
        # 如果报告包含JSON，更新元数据并重新格式化
        if "report_json" in analysis_result and analysis_result.get("report_json"):
            metadata = {
                "elapsed_time": elapsed_time,
                "queries_successful": collection_result["success_count"],
                "queries_executed": collection_result["total_queries"]
            }
            
            # 收集所有citations
            all_citations = []
            for result in collection_result.get("results", []):
                if result.get("status") == "success" and result.get("citations"):
                    for citation in result["citations"]:
                        if citation not in all_citations:  # 去重
                            all_citations.append(citation)
            
            # 重新生成专业格式报告（带正确的元数据和citations）
            analysis_result["report"] = self.professional_formatter.format_professional_report(
                company,
                analysis_result["report_json"],
                metadata,
                citations=all_citations
            )
        
        print("\n" + "="*80)
        print(f"✅ 报告生成完成!")
        print(f"⏱️  总耗时: {elapsed_time:.2f}秒")
        print("="*80)
        
        # 准备输出结果
        result = {
            "status": "success",
            "company": company,
            "report": analysis_result.get("report") or analysis_result.get("summary"),
            "metadata": {
                "analysis_type": analysis_type,
                "report_type": report_type,
                "queries_executed": collection_result["total_queries"],
                "queries_successful": collection_result["success_count"],
                "elapsed_time": elapsed_time,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # 保存到文件
        if save_to_file:
            filename = self._save_report(company, result)
            result["metadata"]["saved_file"] = filename
            
            # 生成PDF（默认启用）
            if generate_pdf:
                pdf_filename = self._generate_pdf_report(filename, company, analysis_result.get("report_json"))
                if pdf_filename:
                    result["metadata"]["pdf_file"] = pdf_filename
                    print(f"📄 PDF报告已生成: {pdf_filename}")
                    
                    # 如果不保留Markdown，删除它
                    if not keep_markdown:
                        import os
                        try:
                            os.remove(filename)
                            # 同时删除enhanced版本（如果存在）
                            enhanced_file = filename.replace('.md', '_enhanced.md')
                            if os.path.exists(enhanced_file):
                                os.remove(enhanced_file)
                            print(f"🗑️  已删除临时Markdown文件")
                            result["metadata"].pop("saved_file", None)
                        except Exception as e:
                            print(f"⚠️  删除Markdown文件失败: {e}")
                else:
                    print(f"⚠️  PDF生成失败，保留Markdown: {filename}")
            else:
                print(f"💾 Markdown报告已保存: {filename}")
        
        return result
    
    def _save_report(self, company: str, result: dict) -> str:
        """保存报告到文件（自动格式化）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company = company.replace(" ", "_").replace("/", "_")
        filename = f"reports/{safe_company}_{timestamp}.md"
        
        # 创建reports目录
        import os
        os.makedirs("reports", exist_ok=True)
        
        # 准备报告内容
        report_content = f"# {company} 估值报告\n\n"
        report_content += f"**生成时间**: {result['metadata']['timestamp']}\n\n"
        report_content += f"**分析类型**: {result['metadata']['analysis_type']} | "
        report_content += f"**查询数**: {result['metadata']['queries_successful']}/{result['metadata']['queries_executed']} | "
        report_content += f"**耗时**: {result['metadata']['elapsed_time']:.2f}秒\n\n"
        report_content += "---\n\n"
        report_content += result["report"]
        
        # 格式化报告（转换HTML表格为Markdown）
        formatted_content = self._format_report_content(report_content)
        
        # 写入报告
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted_content)
        
        # 🆕 自动增强报告（修复表格格式并生成图表）
        try:
            from report_enhancer import ReportEnhancer
            enhancer = ReportEnhancer()
            enhanced_filename = enhancer.enhance_report(filename)
            print(f"\n✨ 报告已自动增强: {enhanced_filename}")
            print(f"   - 修复了表格格式")
            print(f"   - 生成了数据可视化图表")
            print(f"   - 清理了格式问题")
        except Exception as e:
            print(f"\n⚠️  报告增强跳过: {e}")
            print(f"   可以手动运行: python report_enhancer.py {filename}")
        
        return filename
    
    def _format_report_content(self, content: str) -> str:
        """格式化报告内容（转换HTML表格为Markdown）"""
        import re
        try:
            from bs4 import BeautifulSoup
            
            def html_table_to_markdown(match):
                html_table = match.group(0)
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
                        row = [td.get_text().strip() for td in tr.find_all('td')]
                        if row:
                            rows.append(row)
                
                # 构建Markdown表格
                if not headers or not rows:
                    return html_table
                
                markdown = "\n"
                markdown += "| " + " | ".join(headers) + " |\n"
                markdown += "|" + "|".join(["---"] * len(headers)) + "|\n"
                for row in rows:
                    while len(row) < len(headers):
                        row.append("")
                    markdown += "| " + " | ".join(row[:len(headers)]) + " |\n"
                markdown += "\n"
                return markdown
            
            # 转换HTML表格
            content = re.sub(r'<table[^>]*>.*?</table>', html_table_to_markdown, content, flags=re.DOTALL)
            
            # 清理HTML标签
            content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'### \1\n', content, flags=re.DOTALL)
            content = re.sub(r'<h3[^>]*>(.*?)</h3>', r'#### \1\n', content, flags=re.DOTALL)
            content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
            content = re.sub(r'<[^>]+>', '', content)
            
            # 清理多余空行
            content = re.sub(r'\n{4,}', '\n\n\n', content)
            
        except ImportError:
            # 如果没有BeautifulSoup，返回原内容
            pass
        except Exception:
            # 如果格式化失败，返回原内容
            pass
        
        return content
    
    def _generate_pdf_report(self, markdown_path: str, company: str, report_json: dict = None) -> str:
        """
        生成PDF报告
        
        Args:
            markdown_path: Markdown报告路径
            company: 公司名称
            report_json: 报告JSON数据（可选）
            
        Returns:
            PDF文件路径
        """
        try:
            from pdf_generator import ProfessionalPDFGenerator
            import os
            
            print(f"\n📄 正在生成PDF报告...")
            
            # 准备PDF输出路径
            pdf_path = markdown_path.replace('.md', '.pdf')
            
            # 如果有JSON数据，直接使用
            if report_json:
                # 读取markdown文件获取元数据和Executive Summary
                with open(markdown_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # 提取元数据
                import re
                metadata = {}
                timestamp_match = re.search(r'\*\*生成时间\*\*: (.+)', md_content)
                if timestamp_match:
                    metadata['timestamp'] = timestamp_match.group(1)
                
                queries_match = re.search(r'\*\*查询数\*\*: (\d+)/(\d+)', md_content)
                if queries_match:
                    metadata['queries_successful'] = int(queries_match.group(1))
                    metadata['queries_total'] = int(queries_match.group(2))
                
                # 提取Executive Summary（从Markdown中）
                exec_summary = ""
                exec_summary_match = re.search(
                    r'## Executive Summary\s*\n(.*?)(?=\n##|\Z)',
                    md_content,
                    re.DOTALL
                )
                if exec_summary_match:
                    exec_summary = exec_summary_match.group(1).strip()
                    print(f"   ✅ Executive Summary已提取 ({len(exec_summary)} 字符)")
                
                # 提取References（从Markdown中）
                references = ""
                references_match = re.search(
                    r'## 📚 References and Citations\s*\n(.*?)(?=\n##|\Z)',
                    md_content,
                    re.DOTALL
                )
                if references_match:
                    references = references_match.group(1).strip()
                    print(f"   ✅ References已提取 ({len(references)} 字符)")
                
                # 文本清理 - 使用WordFixer直接修复所有问题
                from agents.word_fixer import WordFixer
                print("   🧹 修复单词拆分问题...")
                
                # 使用WordFixer直接修复所有章节的文本
                cleaned_fundamental = WordFixer.fix_all_issues(report_json.get('fundamentalAnalysis', ''))
                cleaned_business = WordFixer.fix_all_issues(report_json.get('businessSegments', ''))
                cleaned_growth = WordFixer.fix_all_issues(report_json.get('growthCatalysts', ''))
                cleaned_valuation = WordFixer.fix_all_issues(report_json.get('valuationAnalysis', ''))
                
                # 准备报告数据（不包含Executive Summary）
                report_data = {
                    'metadata': metadata,
                    # 'executiveSummary': exec_summary,  # 已删除（用户要求）
                    'fundamentalAnalysis': cleaned_fundamental,
                    'businessSegments': cleaned_business,
                    'growthCatalysts': cleaned_growth,
                    'valuationAnalysis': cleaned_valuation
                }
                
                # 如果有AI洞察，也包含进去（使用WordFixer修复）
                if 'aiInsights' in report_json:
                    report_data['aiInsights'] = WordFixer.fix_all_issues(report_json['aiInsights'])
                    print(f"   ✅ AI Insights已包含（已修复）")
                
                # 如果有References，也包含进去（使用WordFixer修复）
                if references:
                    report_data['references'] = WordFixer.fix_all_issues(references)
                    print(f"   ✅ References已包含（已修复）")
                
                # 生成PDF
                generator = ProfessionalPDFGenerator()
                generator.generate_report_pdf(company, report_data, pdf_path)
                
            else:
                # 从Markdown转换（备用方案）
                from pdf_generator import convert_markdown_to_pdf
                pdf_path = convert_markdown_to_pdf(markdown_path)
            
            return pdf_path
            
        except Exception as e:
            print(f"\n⚠️  PDF生成失败: {e}")
            print(f"   Markdown报告仍然可用: {markdown_path}")
            import traceback
            traceback.print_exc()
            return None
    
    def quick_analysis(self, company: str) -> str:
        """快速分析（便捷方法）"""
        result = self.generate_report(company, report_type="quick", save_to_file=False)
        if result["status"] == "success":
            return result["report"]
        else:
            return f"分析失败: {result.get('error', '未知错误')}"
    
    def compare_companies(self, companies: list) -> dict:
        """比较多个公司"""
        print(f"🔄 比较分析: {', '.join(companies)}")
        
        companies_data = {}
        
        for company in companies:
            print(f"\n正在收集 {company} 的信息...")
            query_plan = self.query_planner.generate_search_plan(company)
            collection_result = self.information_collector.collect_information(query_plan)
            companies_data[company] = self.information_collector.format_for_analysis(
                collection_result
            )
        
        print("\n正在生成比较分析...")
        comparison_result = self.deep_analyst.compare_companies(companies_data)
        
        return comparison_result


def main():
    """主函数 - 示例用法"""
    # 创建系统实例
    system = ValuationReportSystem()
    
    # 示例1: 生成单个公司的完整报告
    print("\n示例1: 完整估值报告")
    result = system.generate_report(
        company="Apple Inc",
        analysis_type="valuation",
        report_type="comprehensive",
        save_to_file=True
    )
    
    if result["status"] == "success":
        print("\n报告预览:")
        print(result["report"][:500] + "...\n")
    
    # 示例2: 快速分析
    # print("\n示例2: 快速分析")
    # summary = system.quick_analysis("Tesla")
    # print(summary)
    
    # 示例3: 比较多个公司
    # print("\n示例3: 比较分析")
    # comparison = system.compare_companies(["Apple", "Microsoft", "Google"])
    # print(comparison["comparison"])


if __name__ == "__main__":
    main()

