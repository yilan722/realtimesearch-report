#!/usr/bin/env python3
"""
专业投资银行级PDF报告生成器
- 完美的文字格式（不过度清理）
- 页码显示
- References完整显示
- 专业排版
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from datetime import datetime
import re
from typing import Dict, List


class ProfessionalPDFGenerator:
    """专业投资银行级PDF报告生成器"""
    
    def __init__(self):
        self._register_chinese_fonts()
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _register_chinese_fonts(self):
        """注册中文字体"""
        try:
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            self.chinese_font = 'STSong-Light'
            self.has_chinese_support = True
        except Exception as e:
            self.chinese_font = 'Helvetica'
            self.has_chinese_support = False
    
    def _setup_custom_styles(self):
        """设置专业样式 - 投资银行级格式"""
        # 使用标准Sans-serif字体（Helvetica系列）
        body_font = 'Helvetica'  # 正文字体：常规体
        heading_font = 'Helvetica-Bold'  # 标题字体：粗体
        
        # 颜色定义（参照参考PDF格式）
        heading_color = colors.HexColor('#000000')  # 黑色标题（参照参考PDF）
        body_color = colors.HexColor('#000000')  # 黑色正文（参照参考PDF）
        
        # 封面标题
        self.styles.add(ParagraphStyle(
            name='CoverTitle',
            fontSize=24,
            textColor=body_color,
            alignment=TA_CENTER,
            fontName=heading_font,
            spaceAfter=15,
            leading=30
        ))
        
        # 主标题（1. Fundamental Analysis）- 投资银行格式
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=heading_color,  # 蓝色标题
            spaceAfter=4,  # 标题后间距（为分隔线留空间）
            spaceBefore=16,  # 标题前间距
            fontName=heading_font,  # Helvetica-Bold
            leading=18,
            alignment=TA_LEFT
        ))
        
        # 二级标题（1.1 Subsection）
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=heading_color,  # 蓝色标题
            spaceAfter=6,  # 小标题后间距
            spaceBefore=12,  # 小标题前间距
            fontName=heading_font,  # Helvetica-Bold
            leading=16,
            alignment=TA_LEFT
        ))
        
        # 正文（专业格式 - 两端对齐）
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            textColor=body_color,  # 深灰色正文
            alignment=TA_JUSTIFY,  # 两端对齐（Justified）
            spaceAfter=10,  # 段落间距（增加以防止重叠）
            leading=20,  # 行间距（增加以防止文本重叠）
            fontName=body_font,  # Helvetica常规体
            wordWrap='CJK' if self.has_chinese_support else 'LTR',
            firstLineIndent=0,  # 首行不缩进
            allowWidows=0,  # 防止孤行
            allowOrphans=0,  # 防止孤行
            keepWithNext=0,  # 不强制与下一段保持在一起
            keepTogether=0  # 不强制段落内保持在一起
        ))
    
    def generate_report_pdf(self, company: str, report_data: Dict, output_path: str):
        """生成专业PDF报告"""
        
        def add_page_number(canvas, doc):
            self._add_page_number(canvas, doc)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2.5*cm,  # 底部留更多空间给页码
            onFirstPage=add_page_number,
            onLaterPages=add_page_number
        )
        
        story = []
        
        # 封面页
        story.extend(self._create_cover_page(company, report_data.get('metadata', {})))
        story.append(PageBreak())
        
        # 四大核心部分
        sections = [
            ('fundamentalAnalysis', '1. Fundamental Analysis'),
            ('businessSegments', '2. Business Segments Analysis'),
            ('growthCatalysts', '3. Growth Catalysts and Strategic Initiatives'),
            ('valuationAnalysis', '4. Valuation Analysis and Investment Recommendation')
        ]
        
        for key, title in sections:
            if key in report_data and report_data[key]:
                cleaned_title = self._remove_chinese_from_title(title)
                story.extend(self._create_section(cleaned_title, report_data[key]))
                story.append(Spacer(1, 0.2*inch))
        
        # AI Insights
        if 'aiInsights' in report_data and report_data['aiInsights']:
            story.append(PageBreak())
            ai_title = '5. AI-Powered Deep Insights & Predictions'
            cleaned_ai_title = self._remove_chinese_from_title(ai_title)
            story.extend(self._create_section(cleaned_ai_title, report_data['aiInsights']))
            story.append(Spacer(1, 0.2*inch))
        
        # References（重要！）
        if 'references' in report_data and report_data['references']:
            story.append(PageBreak())
            story.extend(self._create_references_section(report_data['references']))
        
        # 生成PDF
        doc.build(story)
        print(f"✅ 专业PDF报告已生成: {output_path}")
    
    def _create_cover_page(self, company: str, metadata: Dict) -> List:
        """创建封面页 - 参照参考PDF格式"""
        story = []
        
        # 顶部间距（参照参考PDF，更紧凑）
        story.append(Spacer(1, 2.5*inch))
        
        # 公司名称（参照参考PDF格式）
        formatted_company = self._format_company_name(company)
        title_font = self.chinese_font if self.has_chinese_support else 'Helvetica-Bold'
        story.append(Paragraph(
            f"<b>{formatted_company}</b>",
            ParagraphStyle(
                name='CoverTitle',
                fontSize=24,
                textColor=colors.HexColor('#000000'),  # 黑色（参照参考PDF）
                alignment=TA_CENTER,
                fontName=title_font,
                leading=30,
                spaceAfter=15
            )
        ))
        
        # 副标题（参照参考PDF格式）
        story.append(Paragraph(
            "Professional Equity Analysis Report",
            ParagraphStyle(
                name='CoverSubtitle',
                fontSize=14,
                textColor=colors.HexColor('#000000'),  # 黑色（参照参考PDF）
                alignment=TA_CENTER,
                fontName=self.chinese_font if self.has_chinese_support else 'Helvetica',
                spaceAfter=2*inch
            )
        ))
        
        # 报告时间（参照参考PDF格式，右对齐）
        story.append(Paragraph(
            f"Report Generated: {datetime.now().strftime('%m/%d/%Y, %I:%M %p')}",
            ParagraphStyle(
                name='CoverDate',
                fontSize=10,
                textColor=colors.HexColor('#000000'),  # 黑色（参照参考PDF）
                alignment=TA_RIGHT,
                fontName=self.chinese_font if self.has_chinese_support else 'Helvetica',
                spaceBefore=0
            )
        ))
        
        return story
    
    def _format_company_name(self, company: str) -> str:
        """格式化公司名称"""
        if re.match(r'^\d{4,5}\.(hk|HK)$', company, re.IGNORECASE):
            return company.upper()
        if re.match(r'^\d{6}\.(sh|sz|SH|SZ)$', company, re.IGNORECASE):
            return company.upper()
        if re.search(r'[\u4e00-\u9fff]', company):
            return company
        if '(' in company and ')' in company:
            match = re.match(r'(.+?)\s*\(([^)]+)\)', company)
            if match:
                name, ticker = match.groups()
                return f"{name.strip()} ({ticker.strip().upper()})"
        return company
    
    def _remove_chinese_from_title(self, title: str) -> str:
        """移除中文标题和修复重复标题数字"""
        if not title:
            return title
        
        # 1. 移除中文（包括括号中的中文）
        if re.search(r'[\u4e00-\u9fff]', title):
            # 移除括号中的中文（如 "(基本面分析)"）
            title = re.sub(r'\s*\([^)]*[\u4e00-\u9fff][^)]*\)', '', title)
            # 移除所有中文字符
            title = re.sub(r'[\u4e00-\u9fff]+', '', title)
        
        # 2. 修复重复的标题数字（如 "1.1 1.1 Company Overview" -> "1.1 Company Overview"）
        # 匹配模式：数字.数字 空格 数字.数字
        title = re.sub(r'(\d+\.\d+)\s+\1\s*', r'\1 ', title)
        # 也处理其他重复模式（如 "1.1 1.1 1.1" -> "1.1"）
        title = re.sub(r'(\d+\.\d+)(\s+\1)+', r'\1', title)
        
        # 3. 规范化空格
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _create_section(self, title: str, content: str) -> List:
        """创建章节 - 投资银行格式，支持小标题（1.1, 1.2, 1.3等）"""
        story = []
        
        # 清理标题：移除中文和重复数字
        cleaned_title = self._remove_chinese_from_title(title)
        
        # 章节标题（确保格式：数字编号+大写首字母）
        story.append(Paragraph(cleaned_title, self.styles['CustomHeading1']))
        
        # 分隔线（参照参考PDF格式）
        story.append(HRFlowable(
            width="100%",
            thickness=2.5,  # 约2.5px
            color=colors.HexColor('#000000'),  # 黑色分隔线（参照参考PDF）
            spaceAfter=8,  # 分隔线后间距
            spaceBefore=0
        ))
        
        # 处理内容，识别小标题（1.1, 1.2, 1.3等）并确保每个小标题下都有内容
        # 先按双换行分割，然后检查每个段落是否是小标题
        paragraphs = content.split('\n\n')
        current_subsection = None
        current_subsection_content = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 检查段落的第一行是否是小标题
            first_line = para.split('\n')[0].strip()
            # 移除Markdown标记（##, ###等）
            clean_first_line = re.sub(r'^#+\s*', '', first_line)
            subsection_match = re.match(r'^(\d+\.\d+)\s+(.+)$', clean_first_line)
            
            if subsection_match:
                # 如果之前有小标题，先渲染它的内容
                if current_subsection and current_subsection_content:
                    subsection_text = '\n\n'.join(current_subsection_content)
                    if subsection_text.strip():
                        story.extend(self._render_subsection_content(subsection_text))
                
                # 开始新的小标题
                subsection_num = subsection_match.group(1)
                subsection_title = subsection_match.group(2)
                
                # 清理小标题：移除中文和重复数字
                cleaned_subsection_title = self._remove_chinese_from_title(subsection_title)
                # 修复重复数字（如 "1.1 1.1 Company Overview" -> "Company Overview"）
                if cleaned_subsection_title.startswith(subsection_num + ' '):
                    cleaned_subsection_title = cleaned_subsection_title[len(subsection_num) + 1:].strip()
                
                # 渲染小标题
                full_subsection_title = f"{subsection_num} {cleaned_subsection_title}"
                story.append(Spacer(1, 0.15*inch))  # 小标题前间距
                story.append(Paragraph(full_subsection_title, self.styles['CustomHeading2']))
                story.append(Spacer(1, 0.1*inch))  # 小标题后间距
                
                # 提取小标题下的内容（去掉第一行的小标题）
                para_lines = para.split('\n')
                if len(para_lines) > 1:
                    subsection_content = '\n'.join(para_lines[1:]).strip()
                    if subsection_content:
                        current_subsection_content = [subsection_content]
                    else:
                        current_subsection_content = []
                else:
                    current_subsection_content = []
                
                current_subsection = full_subsection_title
            else:
                # 普通内容段落，添加到当前小标题
                if current_subsection:
                    current_subsection_content.append(para)
                else:
                    # 如果没有小标题，直接渲染
                    story.extend(self._render_subsection_content(para))
        
        # 处理最后一个小标题的内容
        if current_subsection and current_subsection_content:
            subsection_text = '\n\n'.join(current_subsection_content)
            if subsection_text.strip():
                story.extend(self._render_subsection_content(subsection_text))
        
        return story
    
    def _render_subsection_content(self, content: str) -> List:
        """渲染小标题下的内容（段落和表格）"""
        story = []
        
        # 先按双换行分割段落
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 检测表格（包含 | 符号的行）
            if self._looks_like_table(para):
                table = self._parse_and_create_table(para)
                if table:
                    story.append(table)
                    story.append(Spacer(1, 0.15*inch))
                else:
                    # 表格解析失败，作为普通文本显示
                    from agents.word_fixer import WordFixer
                    clean_para = WordFixer.fix_all_issues(para)
                    if clean_para:
                        story.append(Paragraph(clean_para, self.styles['CustomBody']))
                        story.append(Spacer(1, 0.05*inch))
            else:
                # 普通段落（使用WordFixer直接修复所有问题）
                from agents.word_fixer import WordFixer
                clean_para = WordFixer.fix_all_issues(para)
                if clean_para:
                    # 确保段落使用两端对齐样式
                    story.append(Paragraph(clean_para, self.styles['CustomBody']))
                    story.append(Spacer(1, 0.05*inch))  # 添加小间距确保不重叠
        
        return story
    
    def _clean_text_minimal(self, text: str) -> str:
        """
        最小化文本清理 - 只修复被拆分的单词，不拆分完整单词
        这是全新的方法，完全避免拆分完整单词
        """
        if not text:
            return text
        
        # 1. 移除markdown粗体标记（转换为HTML）
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__([^_]+)__', r'<b>\1</b>', text)
        
        # 2. 移除所有 * 和 _（防止斜体）
        text = text.replace('*', '')
        text = text.replace('_', '')
        
        # 3. 修复被拆分的单词（这是唯一会修改文本的地方）
        # 使用更通用的方法：修复所有被空格拆分的常见单词
        # 注意：不使用单词边界，因为被拆分的单词可能不在单词边界处
        
        # 定义被拆分的单词映射（按长度排序，先处理长单词）
        split_words = {
            # 长单词（先处理）
            'a n t i c i p a t e d': 'anticipated',
            'a n t i c i p a t e': 'anticipate',
            'o p e r a t i o n a l': 'operational',
            'i n t e g r a t i o n': 'integration',
            'p r o f i t a b i l i t y': 'profitability',
            'e x p e c t a t i o n s': 'expectations',
            'e x p e c t a t i o n': 'expectation',
            's u g g e s t i n g': 'suggesting',
            'u n d e r s c o r e s': 'underscores',
            'r e s i l i e n c e': 'resilience',
            'p a r t i a l l y': 'partially',
            'd e c l i n e s': 'declines',
            'm a t e r i a l s': 'materials',
            'm a g n e t i c s': 'magnetics',
            'a d j u s t e d': 'adjusted',
            'a n a l y s i s': 'analysis',
            'a n a l y z e': 'analyze',
            'a n a l y s t': 'analyst',
            's u g g e s t': 'suggest',
            'u n d e r s c o r e': 'underscore',
            'd e c l i n e': 'decline',
            's e g m e n t': 'segment',
            'm a t e r i a l': 'material',
            'm a g n e t i c': 'magnetic',
            'a d j u s t': 'adjust',
            'e b i t d a': 'ebitda',
            'r e v e n u e': 'revenue',
            'p r i o r': 'prior',
            'o f f s e t': 'offset',
            'v a l i d a t e s': 'validates',
            'v a l i d a t e': 'validate',
            'e l u s i v e': 'elusive',
            # 短词
            'o f t h e': 'of the',
            'o f': 'of',
            't h e': 'the',
            'i n': 'in',
            'a n d': 'and',
            'a t': 'at',
            'i s': 'is',
            'o n': 'on',
            'b y': 'by',
            't o': 'to',
            'f o r': 'for',
            'a n': 'an',
            'a s': 'as',
            'i f': 'if',
            'o r': 'or',
            'n o t': 'not',
            'h a s': 'has',
            'h a d': 'had',
            'h a v e': 'have',
            'i t': 'it',
            'w i t h': 'with',
            'f r o m': 'from',
            't h i s': 'this',
            't h a t': 'that',
            'n e t': 'net',
            'l o s s': 'loss',
            'b e a t': 'beat',
        }
        
        # 按长度排序（长单词优先）
        sorted_words = sorted(split_words.items(), key=lambda x: len(x[0]), reverse=True)
        
        # 修复被拆分的单词（不区分大小写）
        for split_pattern, replacement in sorted_words:
            # 创建正则表达式模式（匹配被空格拆分的单词）
            pattern = split_pattern.replace(' ', r'\s+')
            # 使用不区分大小写的替换
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # 修复部分拆分的单词（如 "a djusted" → "adjusted"）
        # 这些是常见的部分拆分模式（按长度排序，长单词优先）
        partial_split_fixes = [
            # 用户报告的问题单词
            (r'\bR\s+are\b', 'Rare'),
            (r'\br\s+are\b', 'rare'),
            (r'\bMag\s+net\b', 'Magnet'),
            (r'\bmag\s+net\b', 'magnet'),
            (r'\ba\s+dditional\b', 'additional'),
            (r'\bA\s+dditional\b', 'Additional'),
            # 修复 "Ch in a" → "China"（需要特殊处理，因为可能后面跟其他字符）
            # 先处理后面跟空格的情况（优先级最高）
            (r'\bCh\s+in\s+a\s+', 'China '),  # 修复 "Ch in a " → "China "
            (r'\bch\s+in\s+a\s+', 'china '),
            # 再处理单词边界的情况
            (r'\bCh\s+in\s+a\b', 'China'),  # 修复 "Ch in a" → "China"（单词边界）
            (r'\bch\s+in\s+a\b', 'china'),
            (r'\bCh\s+ina\b', 'China'),  # 修复 "Ch ina" → "China"
            (r'\bch\s+ina\b', 'china'),
            (r'\ba\s+nd\b', 'and'),
            (r'\bA\s+nd\b', 'And'),
            # 其他常见拆分
            (r'\ba\s+djusted\b', 'adjusted'),
            (r'\bA\s+djusted\b', 'Adjusted'),
            (r'\ba\s+nalyst\b', 'analyst'),
            (r'\bA\s+nalyst\b', 'Analyst'),
            (r'\ba\s+nticipated\b', 'anticipated'),
            (r'\bA\s+nticipated\b', 'Anticipated'),
            (r'\bo\s+perational\b', 'operational'),
            (r'\bO\s+perational\b', 'Operational'),
            (r'\bp\s+rior\b', 'prior'),
            (r'\bP\s+rior\b', 'Prior'),
            (r'\bv\s+alidates\b', 'validates'),
            (r'\bV\s+alidates\b', 'Validates'),
            (r'\be\s+bitda\b', 'ebitda'),
            (r'\bE\s+bitda\b', 'EBITDA'),
            (r'\be\s+ps\b', 'eps'),
            (r'\bE\s+ps\b', 'EPS'),
            (r'\bE\s+B\s+I\s+T\s+D\s+A\b', 'EBITDA'),
            (r'\bE\s+P\s+S\b', 'EPS'),
            (r'\bbe\s+at\b', 'beat'),
            (r'\bBe\s+at\b', 'Beat'),
            # 更多常见拆分模式
            (r'\bTh\s+e\b', 'The'),
            (r'\bth\s+e\b', 'the'),
            (r'\bTh\s+is\b', 'This'),
            (r'\bth\s+is\b', 'this'),
            (r'\bTh\s+at\b', 'That'),
            (r'\bth\s+at\b', 'that'),
            (r'\bCo\s+mpany\b', 'Company'),
            (r'\bco\s+mpany\b', 'company'),
            (r'\bRe\s+venue\b', 'Revenue'),
            (r'\bre\s+venue\b', 'revenue'),
            (r'\bMa\s+terial\b', 'Material'),
            (r'\bma\s+terial\b', 'material'),
            (r'\bMa\s+terials\b', 'Materials'),
            (r'\bma\s+terials\b', 'materials'),
        ]
        
        for pattern, replacement in partial_split_fixes:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # 4. 移除markdown标题标记
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        
        # 5. 规范化空格（但不要过度）
        text = re.sub(r'\s{2,}', ' ', text)  # 多个空格变一个
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # 多个换行变两个
        
        return text.strip()
    
    def _looks_like_table(self, text: str) -> bool:
        """判断是否是表格"""
        return '|' in text and text.count('|') > 2
    
    def _parse_and_create_table(self, text: str) -> Table:
        """解析并创建表格"""
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            rows = []
            
            for line in lines:
                if '---' in line or not line.strip():
                    continue
                
                if '|' in line:
                    cells = [cell.strip() for cell in line.split('|')]
                    cells = [cell for cell in cells if cell]
                    
                    if len(cells) > 1:
                        # 使用WordFixer直接修复单元格中的所有问题
                        cleaned_cells = []
                        from agents.word_fixer import WordFixer
                        is_header = len(rows) == 0  # 第一行是表头
                        
                        for cell in cells:
                            # 直接使用WordFixer修复所有问题
                            cell_text = WordFixer.fix_all_issues(cell)
                            # 将单元格内容转换为Paragraph对象，确保正确换行和避免重叠
                            # 表头和数据行使用不同的样式
                            if is_header:
                                # 表头样式
                                cell_para = Paragraph(
                                    f"<b>{cell_text.replace('<b>', '').replace('</b>', '').replace('\n', '<br/>')}</b>",
                                    ParagraphStyle(
                                        name='TableHeader',
                                        fontSize=10,
                                        fontName='Helvetica-Bold',
                                        textColor=colors.white,
                                        alignment=TA_LEFT,
                                        leading=14,  # 行间距
                                        spaceBefore=0,
                                        spaceAfter=0,
                                        wordWrap='LTR',
                                        allowWidows=0,
                                        allowOrphans=0,
                                    )
                                )
                            else:
                                # 数据行样式
                                cell_para = Paragraph(
                                    cell_text.replace('\n', '<br/>'),
                                    ParagraphStyle(
                                        name='TableCell',
                                        fontSize=9,
                                        fontName='Helvetica',
                                        textColor=colors.HexColor('#333333'),
                                        alignment=TA_LEFT,
                                        leading=12,  # 行间距
                                        spaceBefore=0,
                                        spaceAfter=0,
                                        wordWrap='LTR',
                                        allowWidows=0,
                                        allowOrphans=0,
                                    )
                                )
                            cleaned_cells.append(cell_para)
                        rows.append(cleaned_cells)
            
            if not rows or len(rows) < 2:
                return None
            
            # 统一列数
            num_cols = max(len(row) for row in rows)
            for row in rows:
                while len(row) < num_cols:
                    row.append('')
            
            # 计算列宽（更智能的分配，确保文本不溢出）
            available_width = 16 * cm
            
            # 根据列数和内容动态调整列宽
            if num_cols <= 2:
                col_widths = [available_width / num_cols * 0.98] * num_cols
            elif num_cols <= 4:
                col_widths = [available_width / num_cols * 0.95] * num_cols
            else:
                # 超过4列时，使用更小的宽度以确保内容不溢出
                col_widths = [available_width / num_cols * 0.92] * num_cols
            
            # 创建表格
            table = Table(rows, colWidths=col_widths, repeatRows=1)
            
            # 专业表格样式 - 投资银行格式（防止溢出和重叠）
            # 注意：由于单元格内容已经是Paragraph对象，某些样式可能不适用
            table.setStyle(TableStyle([
                # 表头样式（参照参考PDF格式）
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#000000')),  # 黑色表头（参照参考PDF）
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # 白色文字
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # 表头粗体
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                # 数据行样式（Paragraph对象会使用自己的样式，这里设置备用）
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # 正文常规体
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#000000')),  # 黑色正文（参照参考PDF）
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # 增加内边距（防止重叠）
                ('TOPPADDING', (0, 0), (-1, -1), 12),  # 增加内边距（防止重叠）
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),  # 浅灰色边框
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # 顶部对齐，防止重叠
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),  # 交替行颜色
                # Paragraph对象会自动处理换行，不需要WORDWRAP和SPLITLONGWORDS
                ('LEADING', (0, 0), (-1, -1), 14),  # 增加表格行间距（防止重叠）
            ]))
            
            return table
        except Exception as e:
            print(f"      警告: 表格解析失败 - {e}")
            return None
    
    def _create_references_section(self, references_text: str) -> List:
        """创建References章节 - 专业紧凑格式（3-5页）"""
        story = []
        
        # 标题（带分隔线，参照参考PDF格式）
        story.append(Paragraph("6. References and Citations", self.styles['CustomHeading1']))
        story.append(HRFlowable(
            width="100%",
            thickness=2.5,
            color=colors.HexColor('#000000'),  # 黑色分隔线（参照参考PDF）
            spaceAfter=8,
            spaceBefore=0
        ))
        
        # 创建紧凑的引用样式
        reference_style = ParagraphStyle(
            name='ReferenceStyle',
            parent=self.styles['BodyText'],
            fontSize=9,  # 更小的字体
            textColor=colors.HexColor('#000000'),
            alignment=TA_LEFT,
            spaceAfter=4,  # 更小的段落间距
            leading=12,  # 更小的行间距
            fontName='Helvetica',
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            allowWidows=1,
            allowOrphans=1
        )
        
        # 处理references，优化格式使其更紧凑
        lines = references_text.strip().split('\n')
        current_ref = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_ref:
                    # 合并当前引用并添加
                    ref_text = ' '.join(current_ref)
                    clean_ref = self._clean_text_minimal(ref_text)
                    if clean_ref:
                        # 检测是否是引用编号格式（如 [1], [2] 等）
                        if re.match(r'^\[\d+\]', clean_ref):
                            # 引用格式：编号 + 内容
                            story.append(Paragraph(clean_ref, reference_style))
                        else:
                            # 普通文本
                            story.append(Paragraph(clean_ref, reference_style))
                    current_ref = []
                continue
            
            # 检测是否是新的引用（以 [数字] 开头）
            if re.match(r'^\[\d+\]', line):
                # 如果之前有引用，先添加
                if current_ref:
                    ref_text = ' '.join(current_ref)
                    clean_ref = self._clean_text_minimal(ref_text)
                    if clean_ref:
                        story.append(Paragraph(clean_ref, reference_style))
                    current_ref = []
                # 开始新引用
                current_ref.append(line)
            else:
                # 继续当前引用
                current_ref.append(line)
        
        # 处理最后一个引用
        if current_ref:
            ref_text = ' '.join(current_ref)
            clean_ref = self._clean_text_minimal(ref_text)
            if clean_ref:
                story.append(Paragraph(clean_ref, reference_style))
        
        return story
    
    def _add_page_number(self, canvas, doc):
        """添加页码到页脚（参照参考PDF格式）"""
        page_num = canvas.getPageNumber()
        text = f"{page_num}"
        
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#000000'))  # 黑色（参照参考PDF）
        
        # 在页面底部居中显示页码
        page_width = doc.pagesize[0]
        text_width = canvas.stringWidth(text, 'Helvetica', 9)
        x = (page_width - text_width) / 2
        y = 1.2*cm  # 距离底部1.2cm，确保可见
        
        canvas.drawString(x, y, text)
        canvas.restoreState()
