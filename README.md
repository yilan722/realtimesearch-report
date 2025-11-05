# 深度估值报告系统 🚀

一个结合 **Perplexity Sonar** 实时搜索和 **Qwen3-Max** 深度推理的智能估值分析系统，生成优于 sonar-deep-research 的专业投资报告。

## 🎯 核心优势

### 1. **成本优化架构**
- **三层智能设计**：查询规划 → 并行搜索 → 单次深度推理
- **精确查询生成**：用Qwen轻量调用生成最优搜索策略，避免重复和浪费
- **并行信息收集**：同时执行多个Sonar查询，节省时间成本
- **一次性深度分析**：汇总所有信息后单次推理，最大化token效率

### 2. **质量保证**
- **实时信息**：Sonar API提供最新的新闻、数据和市场动态
- **深度推理**：Qwen3-Max的强大分析能力生成专业级报告
- **结构化流程**：从数据收集到分析的系统化方法
- **专业框架**：遵循投资分析行业标准

### 3. **灵活扩展**
- 支持单公司深度分析
- 支持多公司比较分析
- 支持快速摘要模式
- 可自定义分析维度

### 4. **报告增强器** ✨NEW
- **自动修复表格格式**：识别并重建损坏的markdown表格
- **数据可视化**：从表格自动生成专业图表
- **格式优化**：清理HTML编码，优化表格样式
- **批量处理**：一键增强所有报告

## 📊 系统架构

```
┌─────────────────────────────────────────────┐
│  用户输入（公司名称）                        │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  阶段1: QueryPlannerAgent                   │
│  使用：Qwen3-Max（轻量调用，~500 tokens）   │
│  功能：生成8个精确的搜索查询计划            │
│  成本：低                                    │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  阶段2: InformationCollectorAgent           │
│  使用：Sonar API（并行调用，5个并发）       │
│  功能：实时收集新闻、数据、分析师观点       │
│  成本：中（并行节省时间）                   │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  阶段3: DeepAnalystAgent                    │
│  使用：Qwen3-Max（深度推理，~8000 tokens）  │
│  功能：综合分析，生成专业估值报告           │
│  成本：中高（但一次性完成，效率高）         │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  输出：Markdown格式的专业估值报告           │
│  包含：估值、风险、建议、目标价             │
└─────────────────────────────────────────────┘
```

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from main import ValuationReportSystem

# 创建系统实例
system = ValuationReportSystem()

# 生成完整报告
result = system.generate_report(
    company="Apple Inc",
    analysis_type="valuation",
    report_type="comprehensive",
    save_to_file=True
)

print(result["report"])
```

### 快速分析

```python
# 快速摘要（成本更低）
summary = system.quick_analysis("Tesla")
print(summary)
```

### 报告增强器 ✨

生成报告后，使用增强器修复表格格式并添加可视化：

```bash
# 增强单个报告
python report_enhancer.py reports/你的报告.md

# 批量增强所有报告
python enhance_all_reports.py
```

**效果展示：**

原始（损坏的表格）：
```
MetricQ2 FY2026Q1 FY2026YoY ChangeRevenue$46.7B$44.1B+56%
```

增强后（格式正确 + 可视化图表）：
```markdown
| Metric | Q2 FY2026 | Q1 FY2026 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $46.7B | $44.1B | +56% |

**图表 1**: 数据可视化
![图表](charts/report_chart_0.png)
```

详细使用指南请查看：[使用报告增强器.md](使用报告增强器.md)

### 比较分析

```python
# 比较多个公司
comparison = system.compare_companies(["Apple", "Microsoft", "Google"])
print(comparison["comparison"])
```

## 📁 项目结构

```
realtimesearch-report/
├── config.py                 # 配置文件（API密钥、参数）
├── main.py                   # 主程序入口
├── requirements.txt          # Python依赖
├── README.md                 # 项目文档
├── api_clients/              # API客户端模块
│   ├── __init__.py
│   ├── sonar_client.py      # Perplexity Sonar客户端
│   └── qwen_client.py       # Qwen3-Max客户端
├── agents/                   # 智能Agent模块
│   ├── __init__.py
│   ├── query_planner.py     # 查询规划Agent
│   ├── information_collector.py  # 信息收集Agent
│   └── deep_analyst.py      # 深度分析Agent
├── reports/                  # 生成的报告（自动创建）
└── test_system.py           # 测试脚本
```

## ⚙️ 配置说明

在 `config.py` 中配置：

```python
# API密钥
PERPLEXITY_API_KEY = "your-key-here"
QWEN_API_KEY = "your-key-here"

# 成本优化参数
MAX_SONAR_QUERIES = 8              # 每次分析的查询数
QUERY_PLANNER_MAX_TOKENS = 500     # 查询规划token限制
DEEP_ANALYSIS_MAX_TOKENS = 8000    # 深度分析token限制
MAX_CONCURRENT_SEARCHES = 5        # 并发搜索数
```

## 💰 成本分析

### 单次完整分析估算

| 阶段 | API | Token使用 | 成本估算 |
|------|-----|----------|---------|
| 查询规划 | Qwen3-Max | ~500 | 极低 |
| 信息收集 | Sonar API | 8次查询 | 中等 |
| 深度分析 | Qwen3-Max | ~8000 | 中等 |
| **总计** | - | - | **远低于多次迭代方案** |

### 成本优化策略

1. **精确查询规划**：避免无效搜索
2. **并行执行**：节省时间成本
3. **一次性分析**：避免多轮对话
4. **缓存机制**：重复查询使用缓存（可选）

## 📝 报告示例

生成的报告包含以下部分：

- ✅ **执行摘要**：核心结论和投资建议
- 📊 **公司概况**：业务模式和核心竞争力
- 💰 **财务分析**：最新财报和趋势分析
- 📈 **估值分析**：相对估值和绝对估值
- 🚀 **增长驱动**：未来增长点分析
- ⚠️ **风险因素**：主要风险和挑战
- 🎯 **投资建议**：评级和目标价

## 🧪 测试

运行测试脚本：

```bash
python test_system.py
```

测试内容包括：
- API连接测试
- 单公司分析测试
- 快速分析测试
- 错误处理测试

## 🔧 高级功能

### 自定义查询计划

```python
# 手动指定查询（跳过自动规划）
custom_plan = {
    "status": "success",
    "company": "Your Company",
    "plan": {
        "queries": [
            {"query": "...", "purpose": "...", "priority": "high"}
        ]
    }
}
```

### 调整分析深度

```python
# 修改config.py中的参数
DEEP_ANALYSIS_MAX_TOKENS = 4000  # 降低到4000节省成本
# 或
DEEP_ANALYSIS_MAX_TOKENS = 12000  # 提升到12000获得更深入分析
```

## 🆚 与Sonar Deep Research的对比

| 特性 | Sonar Deep Research | 本系统 |
|------|-------------------|--------|
| **信息实时性** | ✅ 优秀 | ✅ 优秀（使用Sonar） |
| **推理深度** | ⚠️ 中等 | ✅ 优秀（使用Qwen3-Max） |
| **成本效率** | ⚠️ 多次迭代，成本高 | ✅ 三层优化，成本低 |
| **分析速度** | ⚠️ 顺序执行，较慢 | ✅ 并行搜索，更快 |
| **报告质量** | ⚠️ 标准化程度低 | ✅ 专业结构化报告 |
| **可定制性** | ❌ 有限 | ✅ 高度可定制 |

## 📚 使用场景

1. **投资决策**：生成专业的投资研究报告
2. **尽职调查**：快速了解公司基本面
3. **市场监控**：定期跟踪关注公司的最新动态
4. **竞品分析**：比较同行业公司的投资价值
5. **投资教育**：学习专业的分析框架

## 🤝 贡献

欢迎提交Issues和Pull Requests！

## 📄 许可

MIT License

## 📧 联系

如有问题或建议，请通过Issues联系。

---

**注意**：本系统生成的报告仅供参考，不构成投资建议。投资有风险，决策需谨慎。

