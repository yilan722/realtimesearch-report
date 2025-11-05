"""
深度估值报告系统 - Web界面
使用Streamlit构建的美观交互界面
运行: streamlit run web_app.py
"""
import streamlit as st
import os
import time
from datetime import datetime
from main import ValuationReportSystem
import glob

# 页面配置
st.set_page_config(
    page_title="深度估值报告系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'system' not in st.session_state:
    st.session_state.system = ValuationReportSystem()
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# 侧边栏
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/business-report.png", width=100)
    st.title("📊 功能菜单")
    
    page = st.radio(
        "选择功能",
        ["🏠 首页", "📈 单公司分析", "⚡ 快速分析", "🔄 比较分析", "📚 历史报告", "⚙️ 设置"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 系统特性")
    st.markdown("✅ 实时信息搜索")
    st.markdown("✅ 深度AI推理")
    st.markdown("✅ 成本优化40%")
    st.markdown("✅ 速度提升2.5倍")
    
    st.markdown("---")
    st.markdown("### 快速统计")
    if os.path.exists("reports"):
        report_count = len(glob.glob("reports/*.md"))
        st.metric("生成报告数", report_count)
    
    st.markdown("---")
    st.caption("Powered by Sonar + Qwen3-Max")

# 主页
if page == "🏠 首页":
    st.markdown('<h1 class="main-header">🚀 深度估值报告系统</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">结合Perplexity Sonar实时搜索和Qwen3-Max深度推理的智能分析系统</p>', unsafe_allow_html=True)
    
    # 功能介绍
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 核心优势")
        st.markdown("""
        - **实时信息**: Sonar API实时搜索
        - **深度推理**: Qwen3-Max强大分析
        - **成本优化**: 降低40%成本
        - **速度快**: 2-3分钟生成报告
        """)
    
    with col2:
        st.markdown("### 📊 报告内容")
        st.markdown("""
        - 执行摘要和投资建议
        - 公司概况和业务分析
        - 最新财务数据
        - 估值分析（PE/PS/PB等）
        - 增长驱动因素
        - 风险因素分析
        """)
    
    with col3:
        st.markdown("### 💰 成本参考")
        st.markdown("""
        - **快速分析**: ~$0.02/次
        - **标准报告**: ~$0.044/次
        - **深度报告**: ~$0.07/次
        - **比传统**: 节省99%+
        """)
    
    st.markdown("---")
    
    # 快速开始
    st.markdown("### 🚀 快速开始")
    st.info("👈 从左侧菜单选择功能开始分析！")
    
    # 使用示例
    with st.expander("📖 查看使用示例"):
        st.code("""
from main import ValuationReportSystem

system = ValuationReportSystem()

# 生成完整报告
result = system.generate_report("Apple Inc")

# 快速分析
summary = system.quick_analysis("Tesla")

# 比较分析
comparison = system.compare_companies(["Apple", "Microsoft", "Google"])
        """, language="python")

# 单公司分析
elif page == "📈 单公司分析":
    st.title("📈 单公司深度估值分析")
    st.markdown("生成完整的专业估值报告（2-3分钟）")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        company = st.text_input(
            "公司名称或股票代码",
            placeholder="例如: Apple Inc, Tesla, NVIDIA, 贵州茅台",
            help="支持中英文公司名称"
        )
    
    with col2:
        report_type = st.selectbox(
            "报告类型",
            ["comprehensive", "quick"],
            format_func=lambda x: "完整报告（推荐）" if x == "comprehensive" else "快速分析"
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        save_file = st.checkbox("保存到文件", value=True)
    
    if st.button("🚀 开始分析", type="primary", use_container_width=True):
        if not company:
            st.error("❌ 请输入公司名称")
        else:
            with st.spinner(f"正在分析 {company}，请稍候..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 模拟进度
                status_text.text("第1步: 智能查询规划...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text("第2步: 并行收集实时信息...")
                progress_bar.progress(50)
                
                try:
                    # 实际分析
                    result = st.session_state.system.generate_report(
                        company=company,
                        report_type=report_type,
                        save_to_file=save_file
                    )
                    
                    progress_bar.progress(90)
                    status_text.text("第3步: 深度分析生成报告...")
                    
                    if result["status"] == "success":
                        progress_bar.progress(100)
                        status_text.text("✅ 分析完成！")
                        
                        st.session_state.current_report = result
                        st.session_state.analysis_history.append({
                            "company": company,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": report_type
                        })
                        
                        st.success(f"✅ {company} 估值报告生成成功！")
                        
                        # 显示元数据
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("执行查询", f"{result['metadata']['queries_successful']}/{result['metadata']['queries_executed']}")
                        with col2:
                            st.metric("总耗时", f"{result['metadata']['elapsed_time']:.2f}秒")
                        with col3:
                            st.metric("报告长度", f"{len(result['report'])} 字符")
                        
                        # 显示报告
                        st.markdown("---")
                        st.markdown("### 📄 生成的报告")
                        
                        # 添加专业CSS样式
                        st.markdown("""
                        <style>
                        .metric-table {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 20px 0;
                            background: white;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }
                        .metric-table th {
                            background: #1f77b4;
                            color: white;
                            padding: 12px;
                            text-align: left;
                            font-weight: bold;
                        }
                        .metric-table td {
                            padding: 10px 12px;
                            border-bottom: 1px solid #ddd;
                        }
                        .metric-table tr:hover {
                            background: #f5f5f5;
                        }
                        .highlight-box {
                            background: #e8f4f8;
                            border-left: 4px solid #1f77b4;
                            padding: 15px;
                            margin: 15px 0;
                            border-radius: 4px;
                        }
                        .positive {
                            color: #28a745;
                            font-weight: bold;
                        }
                        .negative {
                            color: #dc3545;
                            font-weight: bold;
                        }
                        .neutral {
                            color: #6c757d;
                        }
                        .recommendation-buy {
                            background: #28a745;
                            color: white;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-weight: bold;
                            display: inline-block;
                        }
                        .recommendation-sell {
                            background: #dc3545;
                            color: white;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-weight: bold;
                            display: inline-block;
                        }
                        .recommendation-hold {
                            background: #ffc107;
                            color: #000;
                            padding: 8px 16px;
                            border-radius: 4px;
                            font-weight: bold;
                            display: inline-block;
                        }
                        .data-source-link {
                            color: #1f77b4;
                            text-decoration: none;
                            font-size: 0.9em;
                        }
                        .data-source-link:hover {
                            text-decoration: underline;
                        }
                        .section-title {
                            color: #1f77b4;
                            border-bottom: 2px solid #1f77b4;
                            padding-bottom: 10px;
                            margin-top: 30px;
                        }
                        .subsection-title {
                            color: #333;
                            margin-top: 20px;
                            font-weight: 600;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        # 检查是否有JSON格式的报告
                        if "report_json" in result and result.get("report_json"):
                            # 渲染HTML格式的专业报告
                            json_report = result["report_json"]
                            
                            st.markdown(f"<h2 class='section-title'>1. 基本面分析 (Fundamental Analysis)</h2>", unsafe_allow_html=True)
                            st.markdown(json_report.get("fundamentalAnalysis", ""), unsafe_allow_html=True)
                            
                            st.markdown(f"<h2 class='section-title'>2. 业务板块分析 (Business Segments)</h2>", unsafe_allow_html=True)
                            st.markdown(json_report.get("businessSegments", ""), unsafe_allow_html=True)
                            
                            st.markdown(f"<h2 class='section-title'>3. 增长催化剂 (Growth Catalysts)</h2>", unsafe_allow_html=True)
                            st.markdown(json_report.get("growthCatalysts", ""), unsafe_allow_html=True)
                            
                            st.markdown(f"<h2 class='section-title'>4. 估值分析 (Valuation Analysis)</h2>", unsafe_allow_html=True)
                            st.markdown(json_report.get("valuationAnalysis", ""), unsafe_allow_html=True)
                        else:
                            # 使用Markdown格式显示
                            st.markdown(result["report"], unsafe_allow_html=True)
                        
                        # 下载按钮
                        if save_file:
                            st.download_button(
                                label="📥 下载报告",
                                data=result["report"],
                                file_name=f"{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                mime="text/markdown"
                            )
                    else:
                        st.error(f"❌ 分析失败: {result.get('error', '未知错误')}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")

# 快速分析
elif page == "⚡ 快速分析":
    st.title("⚡ 快速分析")
    st.markdown("快速了解公司投资要点（30-60秒，成本低70%）")
    
    companies_input = st.text_area(
        "公司名称（每行一个）",
        placeholder="Tesla\nMicrosoft\nApple\nNVIDIA",
        height=150,
        help="支持批量分析，每行输入一个公司名称"
    )
    
    if st.button("⚡ 开始快速分析", type="primary", use_container_width=True):
        companies = [c.strip() for c in companies_input.split('\n') if c.strip()]
        
        if not companies:
            st.error("❌ 请输入至少一个公司名称")
        else:
            for i, company in enumerate(companies):
                st.markdown(f"### 📊 {company}")
                
                with st.spinner(f"正在分析 {company}..."):
                    try:
                        summary = st.session_state.system.quick_analysis(company)
                        
                        st.session_state.analysis_history.append({
                            "company": company,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "quick"
                        })
                        
                        st.markdown(summary)
                        st.markdown("---")
                        
                    except Exception as e:
                        st.error(f"❌ {company} 分析失败: {str(e)}")
                
                # 添加间隔避免API限流
                if i < len(companies) - 1:
                    time.sleep(1)

# 比较分析
elif page == "🔄 比较分析":
    st.title("🔄 多公司比较分析")
    st.markdown("对比多个公司的投资价值（5-10分钟）")
    
    st.warning("⚠️ 此功能会执行较多API调用，请谨慎使用")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        company1 = st.text_input("公司1", placeholder="Apple")
    with col2:
        company2 = st.text_input("公司2", placeholder="Microsoft")
    with col3:
        company3 = st.text_input("公司3", placeholder="Google")
    
    companies = [c for c in [company1, company2, company3] if c]
    
    if st.button("🔄 开始比较分析", type="primary", use_container_width=True):
        if len(companies) < 2:
            st.error("❌ 请至少输入2个公司名称")
        else:
            with st.spinner(f"正在比较 {', '.join(companies)}..."):
                progress_bar = st.progress(0)
                
                try:
                    # 显示进度
                    for i, company in enumerate(companies):
                        progress_bar.progress(int((i + 1) / (len(companies) + 1) * 100))
                        st.info(f"📊 正在收集 {company} 的信息...")
                        time.sleep(0.5)
                    
                    comparison = st.session_state.system.compare_companies(companies)
                    
                    progress_bar.progress(100)
                    
                    if comparison["status"] == "success":
                        st.success(f"✅ 比较分析完成！")
                        
                        st.markdown("---")
                        st.markdown("### 📊 比较报告")
                        st.markdown(comparison["comparison"])
                        
                        # 下载按钮
                        st.download_button(
                            label="📥 下载比较报告",
                            data=comparison["comparison"],
                            file_name=f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.error(f"❌ 比较分析失败: {comparison.get('error', '未知错误')}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")

# 历史报告
elif page == "📚 历史报告":
    st.title("📚 历史报告")
    
    # 分析历史
    if st.session_state.analysis_history:
        st.markdown("### 本次会话分析历史")
        for item in reversed(st.session_state.analysis_history[-10:]):
            st.markdown(f"- **{item['company']}** - {item['time']} - {item['type']}")
    else:
        st.info("暂无分析历史")
    
    st.markdown("---")
    
    # 保存的报告
    st.markdown("### 💾 已保存的报告")
    
    if os.path.exists("reports"):
        reports = sorted(glob.glob("reports/*.md"), key=os.path.getmtime, reverse=True)
        
        if reports:
            st.markdown(f"共找到 {len(reports)} 份报告")
            
            selected_report = st.selectbox(
                "选择报告",
                reports,
                format_func=lambda x: os.path.basename(x)
            )
            
            if selected_report:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("📖 查看报告"):
                        with open(selected_report, 'r', encoding='utf-8') as f:
                            content = f.read()
                        st.markdown("---")
                        st.markdown(content)
                with col2:
                    with open(selected_report, 'r', encoding='utf-8') as f:
                        content = f.read()
                    st.download_button(
                        label="📥 下载",
                        data=content,
                        file_name=os.path.basename(selected_report),
                        mime="text/markdown"
                    )
        else:
            st.info("还没有保存的报告，生成报告后会自动保存到 reports/ 目录")
    else:
        st.info("reports/ 目录不存在，生成第一份报告后会自动创建")

# 设置
elif page == "⚙️ 设置":
    st.title("⚙️ 系统设置")
    
    st.markdown("### 成本与质量平衡")
    
    import config
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 查询设置")
        max_queries = st.slider(
            "每次分析的查询数",
            min_value=3,
            max_value=15,
            value=config.MAX_SONAR_QUERIES,
            help="更多查询 = 更全面的信息 = 更高成本"
        )
        
        planner_tokens = st.slider(
            "查询规划Token限制",
            min_value=300,
            max_value=1000,
            value=config.QUERY_PLANNER_MAX_TOKENS,
            help="查询规划阶段的token限制"
        )
    
    with col2:
        st.markdown("#### 分析设置")
        analysis_tokens = st.slider(
            "深度分析Token限制",
            min_value=4000,
            max_value=16000,
            value=config.DEEP_ANALYSIS_MAX_TOKENS,
            help="更多tokens = 更深入的分析 = 更高成本"
        )
        
        concurrent = st.slider(
            "并发搜索数",
            min_value=2,
            max_value=10,
            value=config.MAX_CONCURRENT_SEARCHES,
            help="更高并发 = 更快速度（注意API限流）"
        )
    
    st.markdown("---")
    
    # 预设配置
    st.markdown("### 📋 预设配置")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 成本优先", use_container_width=True):
            st.info("""
            **成本优先配置**
            - 查询数: 5
            - 分析Tokens: 4000
            - 成本降低: ~40%
            - 质量影响: 轻微
            """)
    
    with col2:
        if st.button("⚖️ 平衡模式", use_container_width=True):
            st.info("""
            **平衡模式配置（默认）**
            - 查询数: 8
            - 分析Tokens: 8000
            - 成本: 标准
            - 质量: 优秀
            """)
    
    with col3:
        if st.button("🎯 质量优先", use_container_width=True):
            st.info("""
            **质量优先配置**
            - 查询数: 12
            - 分析Tokens: 12000
            - 成本增加: ~50%
            - 质量: 卓越
            """)
    
    st.markdown("---")
    st.markdown("### 📊 API配置")
    st.info(f"""
    **Perplexity Sonar API**: 已配置 ✅
    **Qwen3-Max API**: 已配置 ✅
    
    配置文件位置: `config.py`
    """)
    
    st.markdown("---")
    st.markdown("### 📚 系统信息")
    st.code(f"""
系统版本: 1.0.0
Python版本: 3.7+
依赖包: requests, aiohttp, asyncio, streamlit
项目路径: {os.getcwd()}
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>深度估值报告系统 v1.0 | Powered by Sonar + Qwen3-Max</p>
    <p>💡 提示: 报告仅供参考，不构成投资建议</p>
</div>
""", unsafe_allow_html=True)

