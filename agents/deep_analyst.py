"""
深度分析Agent - 第三层：综合分析和估值报告生成
使用Qwen3Max深度推理，生成高质量估值报告
"""
from typing import Dict, Optional
from api_clients.qwen_client import QwenClient
from agents.format_enhancer import FormatEnhancer
from agents.text_cleaner import TextCleaner
from config import DEEP_ANALYSIS_MAX_TOKENS
import json


class DeepAnalystAgent:
    """
    深度分析Agent：综合所有信息，生成专业的估值报告
    目标：用单次深度推理生成全面、专业的分析报告（成本效率最优）
    """
    
    def __init__(self, qwen_client: QwenClient = None):
        self.qwen_client = qwen_client or QwenClient()
        self.format_enhancer = FormatEnhancer()
        
    def generate_valuation_report(
        self,
        company: str,
        collected_information: str,
        report_type: str = "comprehensive"
    ) -> Dict:
        """
        生成估值报告
        
        Args:
            company: 公司名称
            collected_information: 收集的所有信息（格式化文本）
            report_type: 报告类型（comprehensive=综合, quick=快速）
            
        Returns:
            包含报告内容的字典
        """
        system_prompt = """You are a professional stock analyst with expertise in fundamental analysis and valuation, possessing investment bank-level deep research capabilities.

Your task is to generate a comprehensive valuation report in MARKDOWN format with FIVE main sections.

CRITICAL OUTPUT REQUIREMENTS - READ CAREFULLY:
1. Return ONLY a valid JSON object with these exact keys: "fundamentalAnalysis", "businessSegments", "growthCatalysts", "valuationAnalysis", "aiInsights"
2. Each section value must be CLEAN MARKDOWN text (NO HTML, NO weird formatting)
3. Sections 1-4 must be 1500-2000 words with MINIMUM 3 properly formatted markdown tables and EXTENSIVE data-driven analysis
4. Section 5 (aiInsights) must be 1000-1500 words with MINIMUM 2 properly formatted markdown tables and DEEP predictive reasoning
5. All content must be in English only (no Chinese)

CRITICAL ANALYSIS REQUIREMENTS:
- Every claim must be supported by specific numbers, percentages, or financial data
- Include detailed reasoning chains showing cause-and-effect relationships
- Provide comparative analysis with historical trends and industry benchmarks
- Explain the "why" and "how" behind every metric and trend
- Use multi-step logical deduction to derive insights from raw data
- Connect macro trends to company-specific implications
- Quantify impacts wherever possible (e.g., "revenue grew 25% YoY, driven primarily by X segment which contributed 60% of incremental growth")
- For every table, provide 2-3 paragraphs of detailed interpretation AFTER the table

MANDATORY TABLE FORMAT:
ALL tables MUST follow this EXACT format (notice the pipe | symbols):

| Column 1 | Column 2 | Column 3 |
| --- | --- | --- |
| Data 1A | Data 2A | Data 3A |
| Data 1B | Data 2B | Data 3B |

EXAMPLE CORRECT TABLE:
| Metric | Q2 FY2026 | Q1 FY2026 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $46.7B | $44.1B | +56% |
| Net Income | $26.4B | $18.8B | +40% |
| Gross Margin | 75% | 73% | +200bps |

CRITICAL TABLE RULES:
- MUST have pipe | symbols at start and end of each row
- MUST have separator row with --- between header and data
- Each cell MUST be separated by | symbols
- DO NOT use bold (**), italic (*), or strikethrough (~~) inside table cells
- Numbers must be clean: $35.1B (US) or ¥382.81亿 (China), 94%, +25% (no formatting marks)

**CRITICAL CURRENCY UNIT RULES (AVOID 10X ERRORS):**
FOR CHINESE COMPANIES (stock ticker ends with .hk/.sz/.sh or has Chinese name):
- Use ¥ (RMB) with 亿 unit
- 亿 = 100 million = 0.1 billion
- If source says "382.81亿元", write "¥382.81亿" NOT "$382.81B" or "¥382.81B"
- WRONG: $382.81B (this is 10x too high!)
- CORRECT: ¥382.81亿 or ¥38.281B (if converting 亿 to B)

FOR US COMPANIES (NYSE/NASDAQ like AAPL, TSLA, NVDA):
- Use $ (USD) with B (billion) or M (million)
- Example: $94.0B, $23.6B

**CRITICAL TEXT FORMATTING RULES (AVOID FORMAT CORRUPTION):**
FORBIDDEN IN ALL TEXT (tables AND paragraphs):
❌ NEVER use * for emphasis or bullet points - it breaks Markdown
❌ NEVER use _ for emphasis - it breaks Markdown
❌ NEVER use ** or __ in table cells
❌ NEVER use ~~text~~ strikethrough
❌ NEVER write text without spaces: "200M*i*n" → write "200M in"
❌ NEVER let words merge: "revenuebyDecember" → write "revenue by December"

CORRECT TEXT FORMATTING:
✅ Use plain text in paragraphs: "revenue of $200M in annualized AI by December 2025"
✅ Always include spaces between words
✅ For emphasis, use bold ONLY outside tables: **important text**
✅ In tables, use clean text only: no *, **, _, ~~

FORBIDDEN IN TABLES:
❌ **Bold text** in cells
❌ *Italic text* in cells  
❌ ~~Strikethrough~~ in cells
❌ Missing | separators
❌ Merged cells or complex formatting
❌ Writing ¥382.81B when source says 382.81亿 (10x error!)
❌ Converting 亿 directly to B without dividing by 10

SECTION REQUIREMENTS:

fundamentalAnalysis - Must include (1500-2000 words with DEEP REASONING):

**CRITICAL STRUCTURE REQUIREMENT: The fundamentalAnalysis section MUST have EXACTLY THREE subsections with numbered headings:**

**1.1 Company Overview and Business Model** (500-600 words) - MUST BE THE FIRST SUBSECTION:

**CRITICAL: This subsection MUST start with "## 1.1 Company Overview and Business Model" as a Markdown heading, followed by the content below.**

The content MUST include:

1. **Company Introduction and Background** (200-250 words) - MUST APPEAR FIRST:
   - Company founding background: when, where, why the company was established, founders, initial mission
   - Development history: key milestones, evolution, major transformations, growth trajectory
   - Industry background: what industry the company operates in, industry characteristics, market size, industry trends
   - This information is MANDATORY and must be comprehensive

2. **Team Background and Management** (150-200 words) - MUST APPEAR SECOND:
   - Core team and management: leadership background, key executives, management track record, board composition
   - Founder backgrounds: educational background, previous experience, industry expertise
   - Management team expertise: relevant industry experience, track record of success
   - Organizational structure: corporate structure, subsidiaries, geographic presence
   - This information is MANDATORY and must be detailed

3. **Business Model Overview** (150-200 words) - MUST APPEAR THIRD:
   - How the company makes money: revenue streams, business model mechanics
   - Competitive positioning with specific market share data
   - Business model sustainability with economic moat analysis
   - Connect business strategy to financial outcomes with logical reasoning chains

**1.2 Financial Performance and Metrics Analysis** (500-600 words):

**CRITICAL: This subsection MUST start with "## 1.2 Financial Performance and Metrics Analysis" as a Markdown heading.**

The content MUST include:
  
  * Extensive financial metrics analysis with multi-dimensional comparison:
    - P/E, P/B, ROE, ROA, debt ratios with 3+ year historical trends
    - Industry peer comparison (minimum 3-5 competitors with specific numbers)
    - Margin analysis (gross, operating, net) with trend explanation
    - Working capital efficiency (DSO, DIO, DPO with calculations)
  
  * Deep dive into latest quarterly/annual performance:
    - Sequential (QoQ) AND year-over-year (YoY) comparisons with specific percentages
    - Revenue breakdown by segment with growth contribution analysis
    - Expense analysis showing operating leverage trends
    - Cash flow quality assessment (operating CF vs net income reconciliation)
  
  * Detailed profitability and efficiency analysis:
    - Explain WHY margins changed (cost structure, pricing power, scale effects)
    - Calculate and interpret unit economics where applicable
    - Assess management's capital allocation effectiveness
    - Analyze return on invested capital (ROIC) vs weighted average cost of capital (WACC)

**1.3 Competitive Landscape and Industry Context** (500-600 words):

**CRITICAL: This subsection MUST start with "## 1.3 Competitive Landscape and Industry Context" as a Markdown heading.**

The content MUST include:

  * **Competitive Analysis and Comparison** (200-250 words):
    - Main competitors: identify 3-5 key competitors with detailed comparison
    - Market share comparison: company vs competitors with specific percentages
    - Competitive positioning: strengths and weaknesses vs competitors
    - Competitive dynamics: how the company competes, differentiation strategies
    - Head-to-head comparison table with key metrics (revenue, market share, growth rate, margins)
  
  * **Partnerships and Strategic Alliances** (150-200 words):
    - Strategic partnerships: key alliances, joint ventures, collaborations
    - Partnership details: who, what, when, why, financial impact
    - How partnerships strengthen competitive position
    - Partnership network analysis: breadth and depth of relationships
  
  * **Supply Chain Relationships** (150-200 words):
    - Key suppliers: major suppliers, supplier concentration, dependency risks
    - Customer relationships: major customers, customer concentration, relationship stability
    - Supply chain stability: risks, diversification, geographic distribution
    - How supply chain relationships impact competitive advantage and operational efficiency
  
  * Industry context:
    - Quantify market size and company's addressable market
    - Compare growth rates vs industry average with gap analysis
    - Explain competitive advantages with specific evidence (patents, network effects, cost advantages with numbers)

**REASONING REQUIREMENTS**:
- For EVERY metric: explain what it means, why it matters, how it changed, and what drives the change
- Use multi-step logic: "Revenue grew 25% because (1) volume increased 15% due to new customer acquisition increasing 30% YoY, and (2) average selling price rose 10% due to product mix shift toward premium offerings which now represent 40% vs 30% last year"
- Compare absolute numbers with ratios to provide context
- Identify inflection points in trends and explain causality

- REQUIRED 3 TABLES (use EXACT markdown format shown above):
  * Table 1: Comprehensive Financial Metrics (minimum 8-10 rows with historical comparison)
    Example:
    | Metric | Current Period | Prior Period | YoY Change | Industry Avg | Status |
    | --- | --- | --- | --- | --- | --- |
    | Revenue | $46.7B | $29.8B | +56% | +20% | Outperforming |
    | Gross Margin | 75% | 73% | +200bps | 65% | Premium |
    
  * Table 2: Quarterly Performance Trends (minimum 4 quarters of data)
  * Table 3: Competitive Comparison and Market Position (minimum 4-5 competitors with multiple metrics including market share, growth rate, margins, and competitive positioning)
  
  **OPTIONAL but RECOMMENDED Table 4**: Key Partnerships and Supply Chain Overview
    | Category | Key Partners/Suppliers/Customers | Relationship Type | Strategic Importance |
    | --- | --- | --- | --- |
    | Strategic Partners | Partner A, Partner B | Joint Venture, Alliance | High/Medium/Low |
    | Key Suppliers | Supplier X, Supplier Y | Primary, Secondary | Critical/Important |
    | Major Customers | Customer 1, Customer 2 | Direct, Distributor | High/Medium concentration |

**AFTER EACH TABLE**: Provide 2-3 paragraphs of detailed interpretation explaining the patterns, outliers, and implications

businessSegments - Must include (1500-2000 words with QUANTIFIED INSIGHTS):

**CRITICAL STRUCTURE REQUIREMENT: The businessSegments section MUST have EXACTLY THREE subsections with numbered headings:**

**2.1 Revenue Structure and Business Lines** (500-600 words) - MUST BE THE FIRST SUBSECTION:

**CRITICAL: This subsection MUST start with "## 2.1 Revenue Structure and Business Lines" as a Markdown heading.**

**2.2 Geographic Distribution and Market Penetration** (500-600 words) - MUST BE THE SECOND SUBSECTION:

**CRITICAL: This subsection MUST start with "## 2.2 Geographic Distribution and Market Penetration" as a Markdown heading.**

**2.3 Competitive Positioning and Segment Analysis** (500-600 words) - MUST BE THE THIRD SUBSECTION:

**CRITICAL: This subsection MUST start with "## 2.3 Competitive Positioning and Segment Analysis" as a Markdown heading.**

**CONTENT REQUIREMENTS**:
- Comprehensive revenue breakdown by business segment:
  * Absolute revenue numbers AND percentages of total for each segment
  * Sequential (QoQ) and YoY growth rates with variance explanation
  * Segment margin profiles (if available) or margin implications
  * Mix shift analysis: quantify how changing segment mix impacts overall metrics
  * Growth contribution analysis: "X segment contributed Y% of total incremental revenue"

- Deep segment performance analysis:
  * Compare each segment's growth vs company average and industry benchmarks
  * Identify growth drivers for each segment with specific evidence
  * Analyze segment maturity (growth vs mature vs declining) with lifecycle implications
  * Calculate segment economics: revenue per customer, customer acquisition cost, lifetime value where applicable
  * Discuss cross-selling and synergies between segments with quantification

- Detailed geographic/regional analysis:
  * Revenue by region with growth rates and market penetration rates
  * Explain regional performance differences (why Asia grew faster than Europe, etc.)
  * Assess geographic diversification and concentration risks with specific percentages
  * Discuss regulatory or cultural factors impacting regional performance
  * Calculate regional profitability differences if disclosed

- Market positioning and competitive intensity:
  * Market share by segment with trend (gaining or losing share with specific points)
  * **Competitive landscape per segment** (who are the leaders, what are their strategies):
    - Detailed competitor comparison for each business segment
    - Competitive positioning: strengths and weaknesses vs segment competitors
    - Market share comparison by segment with specific numbers
  * **Partnerships and alliances by segment**:
    - Key partnerships relevant to each business segment
    - How partnerships enhance segment competitiveness
    - Strategic alliances and their impact on segment growth
  * **Supply chain relationships by segment**:
    - Segment-specific supplier relationships
    - Customer relationships and concentration by segment
    - Supply chain efficiency and its impact on segment margins
  * Barriers to entry and competitive moats specific to each segment
  * Pricing power analysis by segment with evidence

**REASONING REQUIREMENTS**:
- Explain the strategic rationale behind segment portfolio
- Connect segment performance to overall corporate strategy
- Identify which segments are strategic investments vs cash cows
- Analyze resource allocation across segments and whether it's optimal
- Project how segment mix will evolve and impact overall company metrics

- REQUIRED 3 TABLES (clean markdown with | separators):
  * Table 1: Comprehensive Segment Revenue Breakdown (include absolute revenue, % of total, YoY growth, contribution to growth)
  * Table 2: Segment Performance Matrix (compare growth rate, margin, market share, competitive position for each segment)
  * Table 3: Segment Competitive Comparison (compare each segment's competitive position vs key competitors, including market share, growth rate, and competitive advantages)
  
  **OPTIONAL but RECOMMENDED Table 4**: Segment Partnerships and Supply Chain Overview (key partnerships and supply chain relationships by segment)

**AFTER EACH TABLE**: Provide 2-3 paragraphs of detailed interpretation with specific insights and forward-looking implications
  
REMINDER: Every table cell must be clean text, NO ** or * or ~~ formatting!

growthCatalysts - Must include (1500-2000 words with FORWARD-LOOKING REASONING):

**CRITICAL STRUCTURE REQUIREMENT: The growthCatalysts section MUST have EXACTLY THREE subsections with numbered headings:**

**3.1 Strategic Technology Initiatives** (500-600 words) - MUST BE THE FIRST SUBSECTION:

**CRITICAL: This subsection MUST start with "## 3.1 Strategic Technology Initiatives" as a Markdown heading.**

**3.2 Market Expansion and Partnership Development** (500-600 words) - MUST BE THE SECOND SUBSECTION:

**CRITICAL: This subsection MUST start with "## 3.2 Market Expansion and Partnership Development" as a Markdown heading.**

**3.3 Product Innovation and Operational Excellence** (500-600 words) - MUST BE THE THIRD SUBSECTION:

**CRITICAL: This subsection MUST start with "## 3.3 Product Innovation and Operational Excellence" as a Markdown heading.**

**CONTENT REQUIREMENTS**:
- Major growth drivers with detailed quantification:
  * Identify 4-6 key growth catalysts with specific revenue/profit impact estimates
  * For each catalyst, explain the mechanism: "X will drive growth by doing Y, which leads to Z outcome"
  * Provide probability-weighted scenarios for each catalyst
  * Calculate potential TAM (Total Addressable Market) expansion from new initiatives
  * Timeline analysis: short-term (0-12 months) vs medium-term (1-3 years) vs long-term (3+ years) catalysts

- Strategic initiatives with execution roadmap:
  * Detail each major initiative with investment amounts, expected ROI, and payback period
  * Explain how initiatives align with overall corporate strategy
  * Assess execution feasibility based on management track record and resource availability
  * Identify potential obstacles and mitigation strategies
  * Quantify expected financial impact (revenue contribution, margin improvement)

- Product and innovation pipeline:
  * New product launches: specific names, launch dates, target markets, projected revenue
  * R&D investments as % of revenue with trend and focus areas
  * Patent portfolio analysis and competitive differentiation
  * Product lifecycle management: balance between mature products and innovation
  * Time-to-market analysis and competitive racing dynamics

- Market expansion and penetration strategies:
  * Geographic expansion plans with market size data for each target market
  * Customer segment expansion (moving upmarket/downmarket) with TAM implications
  * Channel strategy (direct vs indirect, online vs offline) with economics comparison
  * Partnership and M&A strategy with potential targets and rationale

- **Competitive Analysis and Comparison**:
  * Detailed competitor comparison: identify 3-5 key competitors with head-to-head analysis
  * Competitive positioning: strengths and weaknesses vs competitors with specific metrics
  * Market share trends: gaining or losing share vs competitors
  * Competitive response strategies: how competitors are responding to company's growth

- **Partnerships and Strategic Alliances**:
  * Key partnerships: strategic alliances, joint ventures, collaborations relevant to growth catalysts
  * Partnership impact: how partnerships enable or accelerate growth initiatives
  * Partnership network: breadth and depth of strategic relationships
  * Partnership pipeline: potential new partnerships that could drive growth

- **Supply Chain and Operational Advantages**:
  * Supply chain relationships: how supplier and customer relationships support growth
  * Supply chain efficiency: operational advantages that enable competitive growth
  * Supply chain risks: potential disruptions that could impact growth catalysts
  * Geographic supply chain diversification and its impact on growth sustainability

- Competitive moats and sustainability:
  * Identify and quantify each moat type (network effects, scale, switching costs, brand, IP)
  * Explain how moats are strengthening or weakening with specific evidence
  * Assess competitive threats and how company is defending/expanding moats
  * Calculate sustainable competitive advantage period

- Regulatory and macro catalysts:
  * Policy changes that benefit the company (subsidies, favorable regulations) with quantified impact
  * Industry tailwinds with supporting data
  * Technological disruptions that create opportunities
  * ESG factors that enhance brand value and customer loyalty

**REASONING REQUIREMENTS**:
- Use scenario analysis: "If X happens (probability Y%), then revenue could grow by Z%"
- Connect multiple catalysts to show compounding effects
- Identify key assumptions and sensitivity analysis
- Compare company's growth potential vs current market expectations
- Assess whether growth is sustainable or one-time

- REQUIRED 3 TABLES (use proper | separators):
  * Table 1: Key Growth Catalysts with Impact Assessment (include catalyst, timeline, probability, revenue impact, margin impact, key risks)
  * Table 2: Strategic Initiatives Roadmap (include initiative, investment, expected ROI, completion date, progress status)
  * Table 3: Competitive Positioning and Partnership Impact (compare company's growth catalysts vs competitors, include key partnerships that enable growth, and supply chain advantages)
  
  **OPTIONAL but RECOMMENDED Table 4**: Growth Catalyst Partnerships and Alliances (detailed table of partnerships relevant to each growth catalyst)

**AFTER EACH TABLE**: Provide 2-3 paragraphs interpreting the data and connecting to investment thesis

valuationAnalysis - Must include (1500-2000 words with RIGOROUS VALUATION LOGIC):

**CRITICAL STRUCTURE REQUIREMENT: The valuationAnalysis section MUST have EXACTLY THREE subsections with numbered headings:**

**4.1 Discounted Cash Flow Analysis** (500-600 words) - MUST BE THE FIRST SUBSECTION:

**CRITICAL: This subsection MUST start with "## 4.1 Discounted Cash Flow Analysis" as a Markdown heading.**

**4.2 Relative Valuation Analysis** (500-600 words) - MUST BE THE SECOND SUBSECTION:

**CRITICAL: This subsection MUST start with "## 4.2 Relative Valuation Analysis" as a Markdown heading.**

**4.3 Investment Recommendation and Target Price** (500-600 words) - MUST BE THE THIRD SUBSECTION:

**CRITICAL: This subsection MUST start with "## 4.3 Investment Recommendation and Target Price" as a Markdown heading.**

**CONTENT REQUIREMENTS**:
- Comprehensive DCF (Discounted Cash Flow) analysis:
  * Detailed revenue projections (5-year) with segment-level assumptions
  * Explicit margin assumptions with justification (why gross margin will be X%, operating margin Y%)
  * Working capital assumptions and capex requirements
  * Terminal value calculation with growth rate and multiple approaches
  * WACC calculation breakdown: risk-free rate, equity risk premium, beta, debt cost
  * Sensitivity analysis: show valuation range under different scenarios (±2% on discount rate, ±1% on terminal growth)
  * Bridge from enterprise value to equity value (net debt, minorities, etc.)
  * **CRITICAL: Compare DCF value to CURRENT market price (from latest collected data, as of today) and explain gap**

- Multi-method comparable company analysis:
  * **CRITICAL: Use the LATEST stock price and market cap from the collected information (as of today)**
  * Peer selection rationale (why these companies are comparable)
  * Multiple valuation multiples: P/E, Forward P/E, EV/EBITDA, EV/Sales, P/B, PEG ratio
  * **For each multiple: MUST use the latest current value (as of today), historical average, industry average**
  * Calculate implied price for each multiple and take weighted average
  * Explain valuation premium/discount relative to peers with specific justification
  * Consider growth-adjusted multiples (PEG ratio analysis)

- Triangulated price target synthesis:
  * Base case / Bear case / Bull case scenarios with explicit assumptions for each
  * Assign probability to each scenario based on historical patterns and current setup
  * Calculate probability-weighted target price
  * **CRITICAL: Compare target price to CURRENT market price (from latest data) for upside/downside calculation**
  * Time horizon specification (12-month vs 24-month targets)

- Investment recommendation framework:
  * Clear BUY/HOLD/SELL rating with conviction level
  * Risk-reward ratio calculation (upside potential vs downside risk)
  * Catalyst timeline: what events will close the valuation gap
  * Holding period recommendation
  * Position sizing suggestion based on risk profile

- Comprehensive risk assessment:
  * Identify 5-7 key risks with likelihood and impact ratings
  * Quantify potential downside from each risk
  * Discuss risk mitigation factors
  * Assess risk-adjusted return vs alternatives

- Valuation inflection points:
  * What would need to happen for valuation to re-rate higher
  * What metrics should investors monitor
  * Comparison to historical valuation ranges (when was it valued higher/lower and why)

**REASONING REQUIREMENTS**:
- Show all calculation steps, don't just state conclusions
- Explain why certain assumptions are reasonable given company's history and industry context
- Address counterarguments: "Bulls would argue X, but we believe Y because Z"
- Use historical context: "Company traded at 30x P/E during high-growth phase but only 15x during maturity"
- Connect valuation to fundamental drivers: "Each 1% increase in operating margin would add $X to fair value"

- REQUIRED 3 TABLES (clean markdown with | separators):
  * Table 1: DCF Model Summary (show revenue forecast, margin assumptions, FCF projections, WACC components, terminal value, sensitivity analysis)
  * Table 2: Peer Valuation Comparison (5+ peers with multiple valuation metrics, company vs peer average, implied valuations)
  * Table 3: Price Target Scenarios (Bear/Base/Bull with key assumptions, probability, target price, upside/downside %, key catalysts/risks for each)

**AFTER EACH TABLE**: Provide 2-3 paragraphs interpreting the numbers and deriving investment implications

aiInsights - 🤖 AI-Powered Deep Insights & Predictions (1000-1500 words with ADVANCED PREDICTIVE REASONING):

MUST start with: "🤖 **AI Deep Analysis Note**: The following insights are generated by Qwen3-Max AI based on real-time data analysis, pattern recognition across thousands of companies, and predictive modeling. These represent AI-driven conclusions and probabilistic forecasts derived from data patterns not immediately obvious to human analysis."

**CONTENT REQUIREMENTS**:

- Advanced trend prediction and pattern recognition:
  * Analyze 6-12 month business trajectory using time-series pattern matching
  * Identify leading indicators from financial data (e.g., "R&D spend increased 40% in past 2 quarters, historically correlating with new product launch 9 months later")
  * Predict inflection points: when will growth accelerate/decelerate based on historical analogues
  * Quantify trend confidence based on data quality and historical pattern strength
  * Compare current company trajectory to similar companies at similar stages (comps by trajectory, not just industry)

- Non-obvious strategic opportunities (AI-identified edge):
  * Use data mining to identify opportunities that traditional analysis might miss
  * Example: "Cross-referencing supplier data, patent filings, and hiring patterns suggests company is developing product category X, 6 months before public announcement"
  * Assess market underappreciation: calculate fair value range and compare to current consensus
  * Identify emerging adjacencies or pivot opportunities based on capability analysis
  * Quantify potential value creation from non-consensus opportunities

- Early warning system and risk detection:
  * Anomaly detection: flag unusual patterns in financial ratios or segment trends
  * Example: "Working capital days increased 15% while revenue grew 20%, suggesting collection issues or channel stuffing"
  * Compare company's current metrics to pre-crisis patterns of similar companies
  * Assign risk probability based on base rates and company-specific factors
  * Create risk heat map across multiple dimensions

- Probabilistic scenario modeling:
  * Build Monte Carlo-style scenarios incorporating multiple variables
  * For each scenario, specify:
    - Detailed assumptions (5-7 key variables with ranges)
    - Probability based on base rates and current setup
    - Financial outcome prediction (revenue, margin, FCF)
    - Price target range with confidence interval
    - Key leading indicators to monitor
  * Calculate expected value across all scenarios
  * Identify "fat tail" risks and opportunities (low probability, high impact)

- AI-generated investment framework:
  * Optimal entry/exit timing based on historical patterns
  * Position sizing recommendation based on risk-reward and portfolio context
  * Hedge recommendations or portfolio pairs trade ideas
  * Rebalancing triggers (at what price/events should investors add/trim)
  * Compare current setup to historical analogs and their outcomes

- Market sentiment vs fundamentals gap analysis:
  * Quantify current market sentiment (using price action, options flow, analyst revisions)
  * Compare to AI-assessed fundamental value
  * Calculate sentiment reversion probability and timeline
  * Identify catalysts that could close the gap
  * Historical context: when sentiment gaps were this wide, what happened next

- Contrarian insights and market blindspots:
  * What is the market missing or misunderstanding about this company?
  * What assumptions are embedded in current valuation that could be wrong?
  * Identify potential positive/negative surprises with probability
  * Second-order effects: how might industry changes impact this company differently than consensus expects

**AI REASONING REQUIREMENTS**:
- Explicitly show the data patterns and logic chains that lead to predictions
- Quantify confidence levels for all predictions (e.g., "70% confidence based on 45 historical analogs")
- Use base rate reasoning: "When companies with similar profile faced situation X, 65% experienced outcome Y"
- Acknowledge uncertainty and specify what additional data would increase confidence
- Compare AI predictions to consensus and explain divergence

- REQUIRED 2 TABLES (clean markdown with | separators):
  * Table 1: AI Probabilistic Scenario Analysis (5+ columns including scenario name, probability, key assumptions/triggers, 6M and 12M price targets, expected return, confidence level, primary risk to scenario)
    Example:
    | Scenario | Probability | Key Triggers | 6M Target | 12M Target | Expected Return | AI Confidence | Primary Risk |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | Bull Case | 30% | Product success + margin expansion above 40% | $420 | $480 | +44% | 75% | Execution delays |
    | Base Case | 50% | Steady growth 15-20%, margins stable | $350 | $390 | +17% | 85% | Competition |
    | Bear Case | 20% | Demand slowdown + price war | $250 | $270 | -19% | 70% | Macro shock |
    
  * Table 2: AI Risk-Opportunity Matrix with Predictive Timeline (include factor, type, impact level, probability, expected timeline, leading indicators, AI confidence score, potential value impact)
    Example:
    | Factor | Type | Impact | Probability | Timeline | Leading Indicators | AI Confidence | Value Impact |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | New product launch (AI-detected from hiring patterns) | Opportunity | High | 75% | 6-9 months | R&D spend up 40%, engineer hiring +30% | 80% | +$2-3B market cap |
    | Working capital deterioration | Risk | Medium | 35% | 3-6 months | DSO up 5 days QoQ | 85% | -10% earnings miss |
    | Margin expansion from scale | Opportunity | High | 65% | 9-12 months | Unit costs down 8% YoY | 90% | +$4-5B market cap |

**AFTER EACH TABLE**: Provide 3-4 paragraphs explaining the AI reasoning, historical patterns used, confidence rationale, and actionable implications

CRITICAL: This section MUST be clearly labeled as AI-generated analysis throughout with confidence levels specified!

FINAL TABLE CHECKLIST - MUST VERIFY:
✓ Every table has | pipe symbols at start and end of each row
✓ Header row followed by | --- | --- | separator
✓ NO bold (**), italic (*), or strikethrough (~~) in table cells
✓ Clean numbers only: $46.7B, +56%, 75%
✓ Cells separated by single | symbol

Return ONLY the JSON object with clean markdown content, no other text."""

        user_prompt = f"""Generate a comprehensive valuation report for: {company}

**CRITICAL: Use Latest Market Data**
- **MUST use the current stock price and market cap from the collected information (as of today)**
- **MUST use the latest valuation metrics (PE, PS, PB ratios) from the collected information (as of today)**
- All valuation comparisons must be based on the most recent data available

**Real-time Market Information:**
{collected_information}

CRITICAL: YOU MUST USE THIS EXACT TABLE FORMAT IN ALL SECTIONS:

EXAMPLE 1 - Financial Metrics Table:
| Metric | Q3 2025 | Q2 2025 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $94.0B | $85.8B | +10% |
| Net Income | $23.6B | $21.4B | +8% |
| Gross Margin | 46.5% | 45.8% | +70bps |
| EPS | $1.57 | $1.40 | +12% |

EXAMPLE 2 - Segment Breakdown Table:
| Segment | Revenue | YoY Growth | % of Total |
| --- | --- | --- | --- |
| iPhone | $44.6B | +13.5% | 47.4% |
| Services | $27.4B | +13.3% | 29.1% |
| Mac | $8.0B | +14.8% | 8.5% |

EXAMPLE 3 - Chinese Company (RMB in 亿元, where 亿=100 million):
| Metric | H1 2025 | H1 2024 | YoY Change |
| --- | --- | --- | --- |
| Revenue | ¥62.15亿 | ¥48.75亿 | +27.5% |
| Net Loss | ¥4.14亿 | ¥5.16亿 | -19.8% |
| Gross Margin | 45.2% | 42.8% | +240bps |

EXAMPLE 4 - Valuation Metrics Table:
| Metric | Current | Industry Avg | Status |
| --- | --- | --- | --- |
| P/E Ratio | 32.5x | 25.0x | Premium |
| P/S Ratio | 8.2x | 3.5x | High |
| EV/EBITDA | 24.8x | 18.0x | Elevated |

CRITICAL CURRENCY AND UNIT RULES - MUST FOLLOW:
1. EVERY table MUST start with | and end with |
2. Header row: | Column1 | Column2 | Column3 |
3. Separator row: | --- | --- | --- |
4. Data rows: | Data1 | Data2 | Data3 |
5. NO bold, italic, or strikethrough INSIDE table cells

**CURRENCY FORMATTING (EXTREMELY IMPORTANT - AVOID 10X ERRORS):**

FOR US/INTERNATIONAL COMPANIES (NYSE, NASDAQ):
- Use USD: $94.0B, $23.6B, $1.57
- B = Billion (十亿), M = Million (百万)

FOR CHINESE COMPANIES (A-share, HK stocks .hk/.sz/.sh):
- Use RMB with 亿: ¥62.15亿, ¥4.14亿
- 亿 = 100 million = 0.1 billion
- **CRITICAL**: If source says "382.81亿元", write "¥382.81亿" NOT "$382.81B"
- **WRONG**: ¥382.81B (inflates value 10x!)
- **CORRECT**: ¥382.81亿

**UNIT CONVERSION:**
- 1亿 = 100 million = 0.1B
- 10亿 = 1B
- 382.81亿 = 38.281B
- Write as: ¥382.81亿 (keep 亿) or ¥38.281B (if converting to billion)

**DETECT COMPANY TYPE:**
- Ticker .hk/.sz/.sh/.bj → use ¥ + 亿
- Chinese name → use ¥ + 亿
- AAPL/TSLA/NVDA → use $ + B

6. Clean numbers: $94.0B (US) or ¥382.81亿 (China), +10%, 46.5%

INSTRUCTIONS:
1. Analyze ALL provided information with DEEP reasoning and multi-step logic
2. Use latest financial data with extensive contextual analysis
3. Include SPECIFIC numbers, percentages, growth rates, and comparative data throughout
4. For EVERY data point: explain what it means, why it matters, and what drives it
5. Create 3 detailed tables per section for sections 1-4, and 2 comprehensive tables for section 5 (14 tables total)
6. After EVERY table: write 2-4 paragraphs interpreting the data and deriving insights
7. Return ONLY valid JSON with FIVE sections
8. Sections 1-4: 1500-2000 words each with EXTENSIVE data-driven reasoning
9. Section 5 (aiInsights): 1000-1500 words with DEEP predictive analysis
10. CRITICAL: Section 5 MUST clearly indicate it's AI-generated analysis with confidence levels!
11. **CRITICAL STRUCTURE: Each main section (1-4) MUST have EXACTLY THREE subsections with Markdown headings:**
    - Section 1 (fundamentalAnalysis): Must include "## 1.1", "## 1.2", "## 1.3"
    - Section 2 (businessSegments): Must include "## 2.1", "## 2.2", "## 2.3"
    - Section 3 (growthCatalysts): Must include "## 3.1", "## 3.2", "## 3.3"
    - Section 4 (valuationAnalysis): Must include "## 4.1", "## 4.2", "## 4.3"
    - Each subsection MUST start with its Markdown heading (e.g., "## 1.1 Company Overview and Business Model") followed by the content

ANALYSIS DEPTH REQUIREMENTS:
- Explain cause-and-effect relationships with multi-step reasoning
- Use phrases like "This is because...", "The driver is...", "This leads to..."
- Quantify impacts: "X contributed Y% of growth", "Z improved margins by N basis points"
- Compare with historical trends: "This is X% above/below the 3-year average of Y%"
- Benchmark against peers: "Company's Z metric of A% compares favorably to industry average of B%"
- Make logical connections: "Revenue growth of 25% was driven by (1) 15% volume increase due to..., and (2) 10% price increase because..."

**TEXT QUALITY REQUIREMENTS (CRITICAL - AVOID FORMAT CORRUPTION):**
- NEVER use * or _ anywhere in your text (they break Markdown formatting)
- ALWAYS include proper spaces between words (never merge words like "revenuebyDecember")
- Write clean sentences: "revenue of $200M in AI" NOT "200M*i*nAI" or "200MofAI"
- Use plain text in paragraphs - no formatting marks
- Check that every word is properly spaced from adjacent words
- Verify numbers have correct units and spaces: "$200M annually" NOT "$200Mannually"

Return format:
{{
    "fundamentalAnalysis": "markdown content with 3 tables...",
    "businessSegments": "markdown content with 3 tables...",
    "growthCatalysts": "markdown content with 3 tables...",
    "valuationAnalysis": "markdown content with 3 tables...",
    "aiInsights": "🤖 **AI Deep Analysis Note**: The following insights... (markdown content with 2 tables)"
}}

Start directly with the opening brace. DO NOT forget table format!"""

        try:
            print(f"🤔 正在生成深度分析报告...")
            
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,  # 平衡创造性和准确性
                max_tokens=DEEP_ANALYSIS_MAX_TOKENS
            )
            
            print(f"✅ 报告生成完成")
            
            # 尝试解析JSON格式
            import json
            try:
                # 清理响应，提取JSON
                response_clean = response.strip()
                
                # 如果包含代码块标记，提取JSON
                if "```json" in response_clean:
                    response_clean = response_clean.split("```json")[1].split("```")[0].strip()
                elif "```" in response_clean:
                    response_clean = response_clean.split("```")[1].split("```")[0].strip()
                
                # 尝试找到JSON对象
                start_idx = response_clean.find('{')
                end_idx = response_clean.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    response_clean = response_clean[start_idx:end_idx+1]
                
                # 解析JSON
                report_json = json.loads(response_clean)
                
                # 验证必需的键（aiInsights是可选的，用于向后兼容）
                required_keys = ["fundamentalAnalysis", "businessSegments", "growthCatalysts", "valuationAnalysis"]
                has_ai_insights = "aiInsights" in report_json
                
                if all(key in report_json for key in required_keys):
                    # 文本清理 - 使用WordFixer直接修复所有问题
                    from agents.word_fixer import WordFixer
                    print("🧹 修复单词拆分问题...")
                    cleaned_json = {}
                    for key, value in report_json.items():
                        if isinstance(value, str):
                            cleaned_json[key] = WordFixer.fix_all_issues(value)
                        else:
                            cleaned_json[key] = value
                    
                    # 验证文本质量
                    for section_name in required_keys:
                        validation = TextCleaner.validate_text_quality(cleaned_json.get(section_name, ""))
                        if validation["has_issues"]:
                            print(f"  ⚠️  {section_name}: 发现 {validation['issue_count']} 个潜在格式问题")
                            for issue in validation["issues"][:2]:  # 只显示前2个
                                print(f"     - {issue}")
                        else:
                            print(f"  ✅ {section_name}: 文本格式良好")
                    
                    # 格式增强 - 统一字体、空格、排版
                    print("📐 格式增强中...")
                    enhanced_json = self.format_enhancer.enhance_report_format(cleaned_json)
                    
                    # 验证每个章节的表格数量
                    sections_to_validate = [
                        ("基本面分析", "fundamentalAnalysis", 3),
                        ("业务板块", "businessSegments", 3),
                        ("增长催化剂", "growthCatalysts", 3),
                        ("估值分析", "valuationAnalysis", 3)
                    ]
                    
                    if has_ai_insights:
                        sections_to_validate.append(("AI深度洞察", "aiInsights", 2))
                        print("✨ 包含AI深度洞察章节")
                    else:
                        print("⚠️  未生成AI深度洞察章节（使用旧版格式）")
                    
                    for section_name, section_key, min_tables in sections_to_validate:
                        is_valid, table_count = self.format_enhancer.validate_tables(enhanced_json[section_key], min_tables=min_tables)
                        if is_valid:
                            print(f"  ✅ {section_name}: {table_count}个表格")
                        else:
                            print(f"  ⚠️  {section_name}: 仅{table_count}个表格 (要求至少{min_tables}个)")
                    
                    # 简单组合（专业格式化将在main.py中进行）
                    markdown_report = f"# {company} 估值分析报告\n\n"
                    markdown_report += "## 1. 基本面分析 (Fundamental Analysis)\n\n"
                    markdown_report += enhanced_json["fundamentalAnalysis"] + "\n\n"
                    markdown_report += "## 2. 业务板块分析 (Business Segments)\n\n"
                    markdown_report += enhanced_json["businessSegments"] + "\n\n"
                    markdown_report += "## 3. 增长催化剂 (Growth Catalysts)\n\n"
                    markdown_report += enhanced_json["growthCatalysts"] + "\n\n"
                    markdown_report += "## 4. 估值分析 (Valuation Analysis)\n\n"
                    markdown_report += enhanced_json["valuationAnalysis"] + "\n\n"
                    
                    # 如果有AI洞察章节，添加它
                    if has_ai_insights and enhanced_json.get("aiInsights"):
                        markdown_report += "## 5. 🤖 AI深度洞察与预测 (AI-Powered Deep Insights & Predictions)\n\n"
                        markdown_report += enhanced_json["aiInsights"] + "\n\n"
                    
                    return {
                        "status": "success",
                        "company": company,
                        "report": markdown_report,
                        "report_json": enhanced_json,  # 使用增强后的JSON
                        "report_type": report_type
                    }
                else:
                    # JSON格式不完整，返回原始响应
                    print("⚠️ JSON格式不完整，返回原始报告")
                    return {
                        "status": "success",
                        "company": company,
                        "report": response,
                        "report_type": report_type
                    }
                    
            except json.JSONDecodeError as e:
                # JSON解析失败，返回原始响应
                print(f"⚠️ JSON解析失败: {e}，返回原始报告")
                return {
                    "status": "success",
                    "company": company,
                    "report": response,
                    "report_type": report_type
                }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "company": company
            }
    
    def generate_quick_summary(
        self,
        company: str,
        collected_information: str
    ) -> Dict:
        """
        生成快速摘要（成本更低的选项）
        
        Args:
            company: 公司名称
            collected_information: 收集的信息
            
        Returns:
            包含摘要的字典
        """
        system_prompt = """你是投资分析专家。请生成简洁的投资要点总结。"""
        
        user_prompt = f"""为{company}生成投资要点总结（3-5个关键点）：

{collected_information}

格式：
- ✅ 投资亮点
- ⚠️ 风险提示
- 💰 估值观点
- 📊 核心数据"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.5,
                max_tokens=1000  # 更少的tokens
            )
            
            return {
                "status": "success",
                "company": company,
                "summary": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def compare_companies(
        self,
        companies_data: Dict[str, str]
    ) -> Dict:
        """
        比较多个公司（高级功能）
        
        Args:
            companies_data: 公司名称到信息的映射
            
        Returns:
            比较分析报告
        """
        companies_list = list(companies_data.keys())
        all_info = "\n\n".join([
            f"## {company}\n{info}"
            for company, info in companies_data.items()
        ])
        
        system_prompt = """你是投资组合分析专家。请比较多个公司的投资价值。"""
        
        user_prompt = f"""比较以下公司：

{all_info}

请提供：
1. 各公司的相对优势
2. 估值比较
3. 投资排序建议"""

        try:
            response = self.qwen_client.simple_prompt(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=DEEP_ANALYSIS_MAX_TOKENS
            )
            
            return {
                "status": "success",
                "companies": companies_list,
                "comparison": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

