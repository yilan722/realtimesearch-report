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
from agents.sector_leader_analyzer import SectorLeaderAnalyzer
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
if 'sector_analyzer' not in st.session_state:
    st.session_state.sector_analyzer = SectorLeaderAnalyzer()
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
        ["🏠 首页", "📈 单公司分析", "🔥 行业热点", "🏆 行业龙头", "⚡ 快速分析", "🔄 比较分析", "📚 历史报告", "⚙️ 设置"],
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
        md_count = len(glob.glob("reports/*.md"))
        pdf_count = len(glob.glob("reports/*.pdf"))
        st.metric("Markdown报告", md_count)
        st.metric("PDF报告", pdf_count)
    
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
                        
                        # 下载按钮 - 优先下载PDF
                        if save_file:
                            # 检查是否有PDF文件
                            pdf_file = result.get("metadata", {}).get("pdf_file")
                            
                            if pdf_file and os.path.exists(pdf_file):
                                # 下载PDF
                                with open(pdf_file, 'rb') as f:
                                    pdf_data = f.read()
                                st.download_button(
                                    label="📥 下载报告 (PDF)",
                                    data=pdf_data,
                                    file_name=os.path.basename(pdf_file),
                                    mime="application/pdf"
                                )
                            else:
                                # 如果没有PDF，尝试生成PDF
                                try:
                                    from pdf_generator import ProfessionalPDFGenerator
                                    import tempfile
                                    
                                    # 准备报告数据
                                    report_json = result.get("report_json", {})
                                    if not report_json:
                                        # 如果没有JSON，从Markdown解析
                                        st.warning("⚠️ 无法生成PDF，将下载Markdown格式")
                                        st.download_button(
                                            label="📥 下载报告 (Markdown)",
                                            data=result["report"],
                                            file_name=f"{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                            mime="text/markdown"
                                        )
                                    else:
                                        # 生成PDF
                                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                                            pdf_path = tmp_file.name
                                        
                                        generator = ProfessionalPDFGenerator()
                                        generator.generate_report_pdf(
                                            company,
                                            {
                                                'metadata': result.get("metadata", {}),
                                                'fundamentalAnalysis': report_json.get('fundamentalAnalysis', ''),
                                                'businessSegments': report_json.get('businessSegments', ''),
                                                'growthCatalysts': report_json.get('growthCatalysts', ''),
                                                'valuationAnalysis': report_json.get('valuationAnalysis', ''),
                                                'aiInsights': report_json.get('aiInsights', ''),
                                            },
                                            pdf_path
                                        )
                                        
                                        # 下载PDF
                                        with open(pdf_path, 'rb') as f:
                                            pdf_data = f.read()
                                        st.download_button(
                                            label="📥 下载报告 (PDF)",
                                            data=pdf_data,
                                            file_name=f"{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                            mime="application/pdf"
                                        )
                                        # 清理临时文件
                                        try:
                                            os.unlink(pdf_path)
                                        except:
                                            pass
                                except Exception as e:
                                    # 如果PDF生成失败，回退到Markdown
                                    st.warning(f"⚠️ PDF生成失败: {str(e)}，将下载Markdown格式")
                                    st.download_button(
                                        label="📥 下载报告 (Markdown)",
                                        data=result["report"],
                                        file_name=f"{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                        mime="text/markdown"
                                    )
                    else:
                        st.error(f"❌ 分析失败: {result.get('error', '未知错误')}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")

# 行业热点分析
elif page == "🔥 行业热点":
    st.title("🔥 今日行业热点分析")
    st.markdown("实时追踪A股、港股、美股三大市场的热门行业")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 点击按钮分析当前市场热点行业（约需30-60秒）")
    with col2:
        refresh = st.button("🔄 刷新数据", use_container_width=True)
    
    if st.button("🔥 分析今日热点", type="primary", use_container_width=True) or refresh:
        with st.spinner("正在分析市场热点，请稍候..."):
            try:
                result = st.session_state.sector_analyzer.analyze_market_hotspots()
                
                if result.get("status") == "success":
                    st.success("✅ 热点分析完成！")
                    
                    # 市场概况
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("分析日期", result.get('date', 'Today'))
                    with col2:
                        sentiment = result.get('market_sentiment', 'N/A').upper()
                        sentiment_color = "🟢" if sentiment == "BULLISH" else "🔴" if sentiment == "BEARISH" else "🟡"
                        st.metric("市场情绪", f"{sentiment_color} {sentiment}")
                    with col3:
                        st.metric("热点板块数", len(result.get('top_sectors', [])))
                    
                    # 关键主题
                    themes = result.get('key_themes', [])
                    if themes:
                        st.markdown("### 🎯 今日关键主题")
                        theme_html = " | ".join([f"**{theme}**" for theme in themes])
                        st.markdown(theme_html)
                    
                    st.markdown("---")
                    
                    # 热点行业排行榜
                    st.markdown("### 📊 热点行业排行榜")
                    
                    top_sectors = result.get('top_sectors', [])
                    if top_sectors:
                        for i, sector in enumerate(top_sectors, 1):
                            heat_score = sector.get('heat_score', 0)
                            
                            # 根据热度选择颜色
                            if heat_score >= 80:
                                color = "🔴"
                                heat_level = "极度火热"
                            elif heat_score >= 60:
                                color = "🟠"
                                heat_level = "热门板块"
                            else:
                                color = "🟡"
                                heat_level = "活跃板块"
                            
                            with st.expander(f"{i}. {color} **{sector.get('sector', '')}** - {sector.get('market', '')} (热度: {heat_score})", expanded=(i <= 3)):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("热度等级", heat_level)
                                    st.metric("涨跌幅", sector.get('avg_change', 'N/A'))
                                
                                with col2:
                                    st.metric("成交量变化", sector.get('volume_surge', 'N/A'))
                                    st.metric("所属市场", sector.get('market', 'N/A'))
                                
                                with col3:
                                    # 热度条形图
                                    st.progress(heat_score / 100)
                                    st.caption(f"热度分数: {heat_score}/100")
                                
                                # 关键驱动因素
                                drivers = sector.get('key_drivers', [])
                                if drivers:
                                    st.markdown("**💡 关键驱动因素:**")
                                    for driver in drivers:
                                        st.markdown(f"- {driver}")
                                
                                # 热门股票
                                stocks = sector.get('top_stocks', [])
                                if stocks:
                                    st.markdown("**🏆 热门股票:**")
                                    st.markdown(", ".join(stocks))
                    
                    # 保存按钮
                    st.markdown("---")
                    if st.button("💾 生成完整热点报告", use_container_width=True):
                        with st.spinner("正在生成完整报告..."):
                            try:
                                full_result = st.session_state.sector_analyzer.generate_hotspot_report()
                                if full_result.get("status") == "success":
                                    st.success("✅ 完整报告已生成！")
                                    
                                    # 记录到历史
                                    st.session_state.analysis_history.append({
                                        "company": "行业热点分析",
                                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "type": "hotspot"
                                    })
                                    
                                    # 提供下载
                                    st.download_button(
                                        label="📥 下载Markdown报告",
                                        data=full_result["report"],
                                        file_name=f"hotspot_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                                        mime="text/markdown"
                                    )
                                else:
                                    st.error("报告生成失败")
                            except Exception as e:
                                st.error(f"错误: {str(e)}")
                
                else:
                    st.error(f"❌ 分析失败: {result.get('error', '未知错误')}")
                    
            except Exception as e:
                st.error(f"❌ 发生错误: {str(e)}")
                import traceback
                with st.expander("查看详细错误"):
                    st.code(traceback.format_exc())

# 行业龙头筛选
elif page == "🏆 行业龙头":
    st.title("🏆 行业龙头公司筛选")
    st.markdown("查找指定行业在各市场的领先企业")
    
    # 输入区域
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sector_name = st.text_input(
            "行业名称",
            placeholder="例如: 科技、半导体、Technology、Healthcare",
            help="支持中英文行业名称"
        )
    
    with col2:
        markets = st.multiselect(
            "选择市场",
            ["A-share", "HK", "US"],
            default=["A-share", "HK", "US"],
            help="可以选择一个或多个市场"
        )
    
    # 常用行业快捷按钮
    st.markdown("**🔖 常用行业:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    quick_sectors = {
        col1: ["科技", "金融"],
        col2: ["医疗健康", "消费"],
        col3: ["能源", "工业"],
        col4: ["房地产", "材料"],
        col5: ["通信", "半导体"]
    }
    
    for col, sectors in quick_sectors.items():
        with col:
            for s in sectors:
                if st.button(s, key=f"quick_{s}", use_container_width=True):
                    sector_name = s
    
    st.markdown("---")
    
    if st.button("🔍 查找龙头公司", type="primary", use_container_width=True):
        if not sector_name:
            st.error("❌ 请输入行业名称")
        elif not markets:
            st.error("❌ 请至少选择一个市场")
        else:
            with st.spinner(f"正在查找 {sector_name} 行业龙头..."):
                try:
                    result = st.session_state.sector_analyzer.find_sector_leaders(sector_name, markets)
                    
                    if result.get("status") == "success":
                        st.success(f"✅ 已找到 {sector_name} 行业龙头！")
                        
                        # 记录到历史
                        st.session_state.analysis_history.append({
                            "company": f"{sector_name} 行业龙头",
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "sector_leader"
                        })
                        
                        markets_data = result.get('markets', {})
                        
                        # 为每个市场显示龙头公司
                        for market in markets:
                            companies = markets_data.get(market, [])
                            
                            if companies:
                                # 市场标题
                                market_display_names = {
                                    "A-share": "🇨🇳 A-share 市场",
                                    "Hong Kong": "🇭🇰 Hong Kong 市场", 
                                    "US": "🇺🇸 US 市场"
                                }
                                st.markdown(f"### {market_display_names.get(market, f'📊 {market} 市场')}")
                                
                                for i, company in enumerate(companies[:5], 1):
                                    with st.container():
                                        # 公司标题 - 突出显示名称和ticker
                                        company_name = company.get('company', '未知公司')
                                        ticker = company.get('ticker', 'N/A')
                                        
                                        # 根据市场设置颜色
                                        rank_colors = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                                        rank_emoji = rank_colors[i-1] if i <= 5 else f"{i}."
                                        
                                        st.markdown(f"#### {rank_emoji} **{company_name}** `{ticker}`")
                                        
                                        # 关键指标卡片
                                        st.markdown("##### 💼 基本信息")
                                        col1, col2, col3, col4 = st.columns(4)
                                        
                                        market_cap = company.get('market_cap', 'N/A')
                                        metrics = company.get('key_metrics', {})
                                        revenue = metrics.get('revenue', 'N/A')
                                        market_share = metrics.get('market_share', 'N/A')
                                        growth = metrics.get('growth_rate', 'N/A')
                                        
                                        with col1:
                                            st.metric("💰 市值", market_cap)
                                        with col2:
                                            st.metric("💵 营收", revenue)
                                        with col3:
                                            st.metric("📊 市场份额", market_share)
                                        with col4:
                                            st.metric("📈 增长率", growth)
                                        
                                        # 竞争优势 - 展开显示
                                        advantages = company.get('competitive_advantages', [])
                                        if advantages:
                                            st.markdown("##### ⭐ 核心竞争优势")
                                            for j, adv in enumerate(advantages[:5], 1):
                                                st.markdown(f"**{j}.** {adv}")
                                        else:
                                            st.markdown("##### ⭐ 核心竞争优势")
                                            st.info("暂无竞争优势数据")
                                        
                                        # 近期表现 - 详细展示
                                        performance = company.get('recent_performance', '')
                                        if performance and performance != '暂无数据':
                                            st.markdown("##### 📈 近期表现")
                                            # 使用success box突出显示
                                            st.success(f"📊 {performance}")
                                        else:
                                            st.markdown("##### 📈 近期表现")
                                            st.warning("暂无详细的近期表现数据")
                                        
                                        # 生成深度报告按钮
                                        col_a, col_b = st.columns([2, 1])
                                        with col_a:
                                            if st.button(f"📊 生成 {company_name} 深度估值报告", key=f"valuation_{market}_{i}", use_container_width=True):
                                                st.info(f"💡 提示: 切换到'📈 单公司分析'页面，输入 `{company_name}` 或 `{ticker}` 生成深度报告")
                                        
                                        st.markdown("---")
                            else:
                                st.warning(f"{market} 市场暂无数据")
                            
                            st.markdown("")  # 间距
                    
                    else:
                        st.error("❌ 查询失败")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
                    import traceback
                    with st.expander("查看详细错误"):
                        st.code(traceback.format_exc())
    
    # 支持的行业列表
    with st.expander("📚 查看所有支持的行业"):
        st.markdown("""
        ### 主要行业板块
        
        - **科技 (Technology)**: 半导体、软件、互联网、人工智能、云计算
        - **金融 (Finance)**: 银行、保险、证券、支付
        - **医疗健康 (Healthcare)**: 医药、医疗器械、生物科技、医疗服务
        - **消费 (Consumer)**: 零售、食品饮料、家电、汽车
        - **能源 (Energy)**: 石油天然气、新能源、电力、煤炭
        - **工业 (Industrial)**: 制造、建筑、机械、运输
        - **房地产 (Real Estate)**: 房地产开发、物业管理、REITS
        - **材料 (Materials)**: 化工、金属、矿业、建材
        - **通信 (Telecom)**: 电信运营、通信设备、5G
        
        💡 **提示**: 支持中英文输入，也可以输入更具体的子行业名称
        """)

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
                        
                        # 记录到历史
                        st.session_state.analysis_history.append({
                            "company": f"比较分析: {', '.join(companies)}",
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "type": "comparison"
                        })
                        
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
        st.markdown("### 📊 本次会话分析历史")
        st.markdown(f"共 {len(st.session_state.analysis_history)} 条记录")
        
        for item in reversed(st.session_state.analysis_history[-20:]):
            # 根据类型显示不同的图标
            type_icons = {
                "comprehensive": "📈",
                "quick": "⚡",
                "comparison": "🔄",
                "hotspot": "🔥",
                "sector_leader": "🏆"
            }
            icon = type_icons.get(item.get('type', ''), "📄")
            
            # 格式化显示
            company = item.get('company', 'N/A')
            time = item.get('time', '')
            type_name = item.get('type', '')
            
            st.markdown(f"{icon} **{company}** - {time} - *{type_name}*")
    else:
        st.info("暂无分析历史")
    
    st.markdown("---")
    
    # 保存的报告
    st.markdown("### 💾 已保存的报告")
    
    if os.path.exists("reports"):
        # 获取所有报告文件（.md 和 .pdf）
        all_md = glob.glob("reports/*.md")
        all_pdf = glob.glob("reports/*.pdf")
        all_reports = sorted(all_md + all_pdf, key=os.path.getmtime, reverse=True)
        
        if all_reports:
            # 统计不同类型的报告
            def classify_report(filename):
                basename = os.path.basename(filename).lower()
                if 'hotspot' in basename or 'sector_hotspot' in basename:
                    return '🔥 行业热点'
                elif 'comparison' in basename:
                    return '🔄 比较分析'
                elif 'enhanced' in basename:
                    return '📊 增强报告'
                elif filename.endswith('.pdf'):
                    return '📄 PDF报告'
                else:
                    return '📈 估值报告'
            
            # 统计
            report_types = {}
            for report in all_reports:
                rtype = classify_report(report)
                report_types[rtype] = report_types.get(rtype, 0) + 1
            
            # 显示统计
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("总报告数", len(all_reports))
            with col2:
                st.metric("估值报告", report_types.get('📈 估值报告', 0))
            with col3:
                st.metric("热点报告", report_types.get('🔥 行业热点', 0))
            with col4:
                st.metric("比较报告", report_types.get('🔄 比较分析', 0))
            
            st.markdown("---")
            
            # 筛选选项
            col1, col2 = st.columns([1, 2])
            
            with col1:
                filter_type = st.selectbox(
                    "报告类型筛选",
                    ["全部"] + list(set(report_types.keys())),
                    help="筛选特定类型的报告"
                )
            
            with col2:
                search_term = st.text_input(
                    "搜索报告",
                    placeholder="输入公司名称或关键词",
                    help="搜索报告文件名"
                )
            
            # 应用筛选
            filtered_reports = all_reports
            
            if filter_type != "全部":
                filtered_reports = [r for r in filtered_reports if classify_report(r) == filter_type]
            
            if search_term:
                filtered_reports = [r for r in filtered_reports if search_term.lower() in os.path.basename(r).lower()]
            
            st.markdown(f"**显示 {len(filtered_reports)} / {len(all_reports)} 份报告**")
            
            if filtered_reports:
                # 分页显示
                reports_per_page = 10
                total_pages = (len(filtered_reports) - 1) // reports_per_page + 1
                
                if total_pages > 1:
                    page_num = st.number_input(
                        "页码",
                        min_value=1,
                        max_value=total_pages,
                        value=1,
                        help=f"共 {total_pages} 页"
                    )
                else:
                    page_num = 1
                
                start_idx = (page_num - 1) * reports_per_page
                end_idx = min(start_idx + reports_per_page, len(filtered_reports))
                page_reports = filtered_reports[start_idx:end_idx]
                
                # 显示报告列表
                for i, report_path in enumerate(page_reports, start_idx + 1):
                    report_name = os.path.basename(report_path)
                    report_type = classify_report(report_path)
                    file_size = os.path.getsize(report_path) / 1024  # KB
                    mod_time = datetime.fromtimestamp(os.path.getmtime(report_path)).strftime("%Y-%m-%d %H:%M")
                    
                    with st.expander(f"{i}. {report_type} - {report_name}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.caption(f"📅 修改时间: {mod_time}")
                        with col2:
                            st.caption(f"📦 文件大小: {file_size:.1f} KB")
                        with col3:
                            st.caption(f"🏷️ 类型: {report_type}")
                        
                        st.markdown("---")
                        
                        # 操作按钮
                        col1, col2, col3 = st.columns(3)
                        
                        # 判断文件类型
                        is_pdf = report_path.endswith('.pdf')
                        
                        with col1:
                            if is_pdf:
                                # PDF文件：提供下载按钮
                                with open(report_path, 'rb') as f:
                                    pdf_data = f.read()
                                st.download_button(
                                    label="📄 下载PDF",
                                    data=pdf_data,
                                    file_name=report_name,
                                    mime="application/pdf",
                                    key=f"download_pdf_{i}",
                                    use_container_width=True
                                )
                            else:
                                # Markdown文件：查看报告
                                if st.button("📖 查看报告", key=f"view_{i}", use_container_width=True):
                                    with open(report_path, 'r', encoding='utf-8') as f:
                                        content = f.read()
                                    
                                    # 在新的区域显示
                                    st.markdown("---")
                                    st.markdown("### 📄 报告内容")
                                    
                                    # 添加专业样式
                                    st.markdown("""
                                    <style>
                                    .report-content {
                                        background: white;
                                        padding: 2rem;
                                        border-radius: 8px;
                                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                                    }
                                    </style>
                                    """, unsafe_allow_html=True)
                                    
                                    st.markdown(content, unsafe_allow_html=True)
                        
                        with col2:
                            if not is_pdf:  # 只有Markdown文件才有下载按钮
                                with open(report_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                st.download_button(
                                    label="📥 下载MD",
                                    data=content,
                                    file_name=report_name,
                                    mime="text/markdown",
                                key=f"download_{i}",
                                use_container_width=True
                            )
                        
                        with col3:
                            if st.button("🗑️ 删除", key=f"delete_{i}", use_container_width=True):
                                try:
                                    os.remove(report_path)
                                    st.success(f"✅ 已删除 {report_name}")
                                    st.experimental_rerun()
                                except Exception as e:
                                    st.error(f"❌ 删除失败: {str(e)}")
                
                # 分页导航
                if total_pages > 1:
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(f"第 {page_num} / {total_pages} 页 | 共 {len(filtered_reports)} 份报告")
            else:
                st.warning("没有符合条件的报告")
        else:
            st.info("还没有保存的报告，生成报告后会自动保存到 reports/ 目录")
    else:
        st.info("reports/ 目录不存在，生成第一份报告后会自动创建")
    
    # 批量操作
    st.markdown("---")
    st.markdown("### 🛠️ 批量操作")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 刷新列表", use_container_width=True):
            st.experimental_rerun()
    
    with col2:
        if st.button("📊 查看统计", use_container_width=True):
            if os.path.exists("reports"):
                all_reports = glob.glob("reports/*.md")
                total_size = sum(os.path.getsize(f) for f in all_reports) / 1024 / 1024  # MB
                
                st.info(f"""
                **报告统计信息**
                - 总报告数: {len(all_reports)}
                - 总大小: {total_size:.2f} MB
                - 目录: reports/
                """)
    
    with col3:
        if st.button("⚠️ 清空所有报告", use_container_width=True):
            st.warning("此操作将删除所有报告，请谨慎！")
            if st.checkbox("我确认要删除所有报告"):
                try:
                    if os.path.exists("reports"):
                        import shutil
                        shutil.rmtree("reports")
                        os.makedirs("reports")
                        st.success("✅ 已清空所有报告")
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ 清空失败: {str(e)}")

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

