"""
行业热点分析 - Web界面
基于Gradio构建的交互式界面
"""
import gradio as gr
from agents.sector_leader_analyzer import SectorLeaderAnalyzer
from datetime import datetime
import json


# 全局分析器实例
analyzer = SectorLeaderAnalyzer()


def analyze_hotspots_web():
    """Web版本的热点分析"""
    try:
        result = analyzer.analyze_market_hotspots()
        
        if result.get("status") != "success":
            return "❌ 分析失败，请稍后重试", ""
        
        # 格式化为HTML
        html_output = f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0;">🔥 今日市场热点</h2>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">实时数据分析 | {result.get('date', 'Today')}</p>
        </div>
        
        <div style="padding: 15px; background: #f8f9fa; border-radius: 8px; margin-bottom: 15px;">
            <p style="margin: 5px 0;"><strong>📊 市场情绪:</strong> <span style="color: #667eea; font-weight: bold;">{result.get('market_sentiment', 'N/A').upper()}</span></p>
            <p style="margin: 5px 0;"><strong>🎯 关键主题:</strong> {', '.join(result.get('key_themes', []))}</p>
        </div>
        """
        
        # 添加热点行业表格
        top_sectors = result.get('top_sectors', [])
        if top_sectors:
            html_output += """
            <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                <thead style="background: #667eea; color: white;">
                    <tr>
                        <th style="padding: 12px; text-align: left;">排名</th>
                        <th style="padding: 12px; text-align: left;">行业</th>
                        <th style="padding: 12px; text-align: left;">市场</th>
                        <th style="padding: 12px; text-align: center;">热度</th>
                        <th style="padding: 12px; text-align: center;">涨跌幅</th>
                        <th style="padding: 12px; text-align: left;">关键驱动</th>
                    </tr>
                </thead>
                <tbody>
            """
            
            for i, sector in enumerate(top_sectors, 1):
                heat = sector.get('heat_score', 0)
                heat_color = "#ff6b6b" if heat >= 80 else "#ffd93d" if heat >= 60 else "#6bcf7f"
                heat_icon = "🔥" if heat >= 80 else "⭐" if heat >= 60 else "📊"
                
                change = sector.get('avg_change', '')
                change_color = "#ff6b6b" if '+' in change else "#6bcf7f" if '-' in change else "#333"
                
                drivers = ', '.join(sector.get('key_drivers', [])[:2])
                
                bg_color = "#f8f9fa" if i % 2 == 0 else "white"
                
                html_output += f"""
                <tr style="background: {bg_color};">
                    <td style="padding: 12px;"><strong>{i}</strong></td>
                    <td style="padding: 12px;"><strong>{sector.get('sector', '')}</strong></td>
                    <td style="padding: 12px;">{sector.get('market', '')}</td>
                    <td style="padding: 12px; text-align: center;">
                        <span style="background: {heat_color}; color: white; padding: 4px 12px; border-radius: 12px;">
                            {heat_icon} {heat}
                        </span>
                    </td>
                    <td style="padding: 12px; text-align: center; color: {change_color}; font-weight: bold;">
                        {change}
                    </td>
                    <td style="padding: 12px; font-size: 0.9em;">{drivers}</td>
                </tr>
                """
            
            html_output += """
                </tbody>
            </table>
            """
        
        # 热门股票
        html_output += "<div style='margin-top: 30px;'><h3>🏆 各板块热门股票</h3>"
        for i, sector in enumerate(top_sectors[:5], 1):
            stocks = sector.get('top_stocks', [])
            if stocks:
                html_output += f"""
                <div style='padding: 10px; background: #f8f9fa; border-left: 4px solid #667eea; margin: 10px 0;'>
                    <strong>{sector.get('sector', '')}</strong>: {', '.join(stocks)}
                </div>
                """
        html_output += "</div>"
        
        # JSON数据供下载
        json_output = json.dumps(result, ensure_ascii=False, indent=2)
        
        return html_output, json_output
        
    except Exception as e:
        return f"❌ 错误: {str(e)}", ""


def find_leaders_web(sector, market_choice):
    """Web版本的龙头查找"""
    if not sector:
        return "❌ 请输入行业名称"
    
    try:
        market_map = {
            "A股": ["A-share"],
            "港股": ["HK"],
            "美股": ["US"],
            "全部市场": ["A-share", "HK", "US"]
        }
        
        markets = market_map.get(market_choice, ["A-share", "HK", "US"])
        
        result = analyzer.find_sector_leaders(sector, markets)
        
        if result.get("status") != "success":
            return "❌ 查询失败"
        
        # 格式化为HTML
        html_output = f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0;">🏆 {sector} 行业龙头</h2>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">覆盖市场: {market_choice}</p>
        </div>
        """
        
        markets_data = result.get('markets', {})
        
        for market, companies in markets_data.items():
            if not companies:
                continue
            
            html_output += f"""
            <div style="margin: 20px 0;">
                <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                    {market} 市场
                </h3>
            """
            
            for company in companies[:5]:
                rank = company.get('rank', '')
                name = company.get('company', '')
                ticker = company.get('ticker', '')
                market_cap = company.get('market_cap', 'N/A')
                
                html_output += f"""
                <div style="padding: 20px; background: white; border: 1px solid #e9ecef; border-radius: 8px; margin: 15px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h4 style="margin: 0 0 10px 0; color: #333;">
                        🏆 {rank}. {name} <span style="color: #667eea;">({ticker})</span>
                    </h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 15px 0;">
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                            <div style="font-size: 0.85em; color: #666;">市值</div>
                            <div style="font-size: 1.1em; font-weight: bold; color: #667eea;">{market_cap}</div>
                        </div>
                """
                
                metrics = company.get('key_metrics', {})
                if metrics.get('revenue'):
                    html_output += f"""
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                            <div style="font-size: 0.85em; color: #666;">营收</div>
                            <div style="font-size: 1.1em; font-weight: bold; color: #667eea;">{metrics.get('revenue')}</div>
                        </div>
                    """
                if metrics.get('market_share'):
                    html_output += f"""
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                            <div style="font-size: 0.85em; color: #666;">市场份额</div>
                            <div style="font-size: 1.1em; font-weight: bold; color: #667eea;">{metrics.get('market_share')}</div>
                        </div>
                    """
                if metrics.get('growth_rate'):
                    html_output += f"""
                        <div style="padding: 10px; background: #f8f9fa; border-radius: 5px;">
                            <div style="font-size: 0.85em; color: #666;">增长率</div>
                            <div style="font-size: 1.1em; font-weight: bold; color: #10b981;">{metrics.get('growth_rate')}</div>
                        </div>
                    """
                
                html_output += "</div>"
                
                advantages = company.get('competitive_advantages', [])
                if advantages:
                    html_output += f"""
                    <div style="margin: 10px 0; padding: 10px; background: #f0f9ff; border-left: 3px solid #3b82f6; border-radius: 3px;">
                        <strong style="color: #3b82f6;">⭐ 竞争优势:</strong><br>
                        <span style="font-size: 0.95em;">{', '.join(advantages)}</span>
                    </div>
                    """
                
                performance = company.get('recent_performance', '')
                if performance:
                    html_output += f"""
                    <div style="margin: 10px 0; padding: 10px; background: #f0fdf4; border-left: 3px solid #10b981; border-radius: 3px;">
                        <strong style="color: #10b981;">📈 近期表现:</strong><br>
                        <span style="font-size: 0.95em;">{performance}</span>
                    </div>
                    """
                
                html_output += "</div>"
            
            html_output += "</div>"
        
        return html_output
        
    except Exception as e:
        return f"❌ 错误: {str(e)}"


def generate_report_web():
    """Web版本的完整报告生成"""
    try:
        result = analyzer.generate_hotspot_report()
        
        if result.get("status") != "success":
            return "❌ 报告生成失败", "", ""
        
        # 保存报告
        filename = f"reports/sector_hotspot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        import os
        os.makedirs("reports", exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result["report"])
        
        success_msg = f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 10px; color: white;">
            <h2 style="margin: 0;">✅ 报告生成成功！</h2>
            <p style="margin: 10px 0 0 0;">文件已保存: {filename}</p>
        </div>
        """
        
        return success_msg, result["report"], filename
        
    except Exception as e:
        return f"❌ 错误: {str(e)}", "", ""


# 创建Gradio界面
def create_web_interface():
    """创建Web界面"""
    
    with gr.Blocks(title="行业龙头与热点分析", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 📊 行业龙头与热点分析系统
        
        **实时追踪** A股 | 港股 | 美股 三大市场行业热点与龙头公司
        
        ---
        """)
        
        with gr.Tabs():
            # Tab 1: 今日热点
            with gr.Tab("🔥 今日热点"):
                gr.Markdown("### 实时分析市场热点行业")
                
                analyze_btn = gr.Button("🔍 分析今日热点", variant="primary", size="lg")
                hotspot_output = gr.HTML(label="分析结果")
                hotspot_json = gr.Textbox(label="JSON数据（可下载）", lines=10, visible=False)
                
                analyze_btn.click(
                    fn=analyze_hotspots_web,
                    outputs=[hotspot_output, hotspot_json]
                )
            
            # Tab 2: 行业龙头
            with gr.Tab("🏆 行业龙头"):
                gr.Markdown("### 查找特定行业的龙头公司")
                
                with gr.Row():
                    sector_input = gr.Textbox(
                        label="行业名称",
                        placeholder="例如: 科技、半导体、Technology、Healthcare",
                        scale=3
                    )
                    market_select = gr.Dropdown(
                        choices=["A股", "港股", "美股", "全部市场"],
                        value="全部市场",
                        label="选择市场",
                        scale=1
                    )
                
                search_btn = gr.Button("🔍 查找龙头", variant="primary", size="lg")
                leader_output = gr.HTML(label="查询结果")
                
                search_btn.click(
                    fn=find_leaders_web,
                    inputs=[sector_input, market_select],
                    outputs=leader_output
                )
                
                gr.Markdown("""
                **常用行业**: 科技、金融、医疗健康、消费、能源、工业、房地产、材料、通信
                """)
            
            # Tab 3: 完整报告
            with gr.Tab("📊 完整报告"):
                gr.Markdown("### 生成包含热点分析和龙头公司的完整报告")
                
                gr.Markdown("""
                **报告包含**:
                - 📈 今日热点行业排行
                - 🏆 各行业龙头公司信息
                - 📊 竞争优势分析
                - 💡 市场表现数据
                
                *预计生成时间: 2-5分钟*
                """)
                
                report_btn = gr.Button("📝 生成完整报告", variant="primary", size="lg")
                
                report_status = gr.HTML(label="生成状态")
                report_content = gr.Textbox(label="报告内容（Markdown）", lines=20)
                report_file = gr.Textbox(label="报告文件路径", visible=False)
                
                report_btn.click(
                    fn=generate_report_web,
                    outputs=[report_status, report_content, report_file]
                )
            
            # Tab 4: 使用说明
            with gr.Tab("📖 使用说明"):
                gr.Markdown("""
                ## 功能说明
                
                ### 🔥 今日热点
                - 实时分析A股、港股、美股三大市场的热点行业
                - 显示热度评分、涨跌幅、成交量变化
                - 识别关键驱动因素和热门股票
                
                ### 🏆 行业龙头
                - 查找指定行业在各市场的龙头公司
                - 显示市值、营收、市场份额等关键指标
                - 分析竞争优势和近期表现
                
                ### 📊 完整报告
                - 整合热点分析和龙头公司信息
                - 生成专业的Markdown格式报告
                - 可保存和分享
                
                ## 热度评分说明
                
                | 分数范围 | 热度等级 | 说明 |
                |---------|---------|------|
                | 90-100 | 🔥 极度火热 | 市场关注度极高 |
                | 70-89 | ⭐ 热门板块 | 表现强劲 |
                | 50-69 | 📊 活跃板块 | 值得关注 |
                | 30-49 | 一般活跃 | 正常波动 |
                | 0-29 | 相对冷门 | 关注度较低 |
                
                ## 数据来源
                
                - **实时市场数据**: Perplexity Sonar API
                - **AI智能分析**: Qwen3-Max
                - **多源验证**: 交叉验证确保准确性
                
                ## 免责声明
                
                本系统仅供参考，不构成投资建议。投资有风险，决策需谨慎。
                
                ---
                
                **系统版本**: v1.0  
                **技术支持**: AI-Powered Analysis System
                """)
        
        gr.Markdown("""
        ---
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            © 2025 行业龙头与热点分析系统 | Powered by Sonar + Qwen3-Max
        </div>
        """)
    
    return app


def main():
    """启动Web界面"""
    app = create_web_interface()
    app.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()

