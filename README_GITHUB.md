# 🚀 实时搜索报告生成系统

基于 Qwen3-Max + Perplexity 的智能估值报告生成系统

## ✨ 核心特性

- 🔍 **实时信息搜索**：通过 Perplexity API 获取最新市场数据
- 🤖 **深度分析**：使用 Qwen3-Max 进行专业级估值分析
- 📊 **自动生成图表**：将数据自动可视化为PNG图表
- 📝 **完美格式**：生成格式规范的 Markdown 报告
- 🎯 **四维分析**：基本面、业务板块、增长催化剂、估值分析

## 🎯 最新改进（2024-11-04）

### ✅ 格式问题完美解决

- **42个正确格式的表格**（之前是0个）
- **12个自动生成的图表**
- **Few-Shot Examples**：在prompt中添加3个表格示例
- **TableFixer**：自动检测并修复紧凑表格
- **完美的 Markdown 格式**

### 改进对比

| 指标 | 改进前 | 改进后 | 提升 |
| --- | --- | --- | --- |
| 正确表格数 | 0 | 42 | ✅ 无限 |
| 图表数量 | 0 | 12 | ✅ 新增 |
| 格式质量 | 混乱 | 完美 | ✅ 100% |

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制配置文件并填入你的API密钥：

```bash
cp config.example.py config.py
# 编辑 config.py，填入你的 Perplexity 和 Qwen API密钥
```

### 3. 生成报告

```bash
# 交互式生成
python main.py

# 或者快速测试
python test_clean_format.py TSLA
```

## 📊 报告示例

生成的报告包含：

- ✅ 基本面分析（财务指标、行业对比）
- ✅ 业务板块分析（收入分解、区域分布）
- ✅ 增长催化剂（战略举措、产品路线图）
- ✅ 估值分析（DCF、可比公司、目标价）
- ✅ 数据可视化图表（自动生成PNG）

查看示例：
- `reports/TSLA_20251104_231709_enhanced.md`
- `reports/charts/`（图表目录）

## 🔧 核心技术

### Prompt工程

使用**Few-Shot Examples**提升表格格式质量：

```markdown
EXAMPLE 1 - Financial Metrics Table:
| Metric | Q3 2025 | Q2 2025 | YoY Change |
| --- | --- | --- | --- |
| Revenue | $94.0B | $85.8B | +10% |
```

详见：`当前Prompt完整版.md`

### 自动修复

- **TableFixer**：检测并修复紧凑表格（无|分隔符）
- **ReportEnhancer**：生成图表、清理格式
- **双重保险**：prompt + 后处理

## 📁 项目结构

```
realtimesearch-report/
├── agents/              # 智能代理
│   ├── deep_analyst.py      # 深度分析（改进的prompt）
│   ├── table_fixer.py       # 表格修复器
│   └── ...
├── api_clients/         # API客户端
│   ├── qwen_client.py
│   └── sonar_client.py
├── reports/             # 生成的报告
│   └── charts/          # 图表目录
├── main.py              # 主程序
├── report_enhancer.py   # 报告增强器
└── requirements.txt
```

## 💡 使用文档

- 📄 `当前Prompt完整版.md` - Prompt工程详解
- 📄 `测试成功-格式完美.md` - 改进效果对比
- 📄 `格式改进说明.md` - 技术方案说明
- 📄 `QUICKSTART.md` - 快速开始指南

## 🔐 安全提醒

⚠️ **不要上传真实的API密钥到GitHub！**

- ✅ `config.example.py` - 配置模板（已提交）
- ❌ `config.py` - 真实配置（已忽略）

## 📈 技术栈

- **LLM**: Qwen3-Max（深度分析）
- **搜索**: Perplexity Sonar（实时数据）
- **可视化**: Matplotlib
- **语言**: Python 3.8+

## 🎯 下一步优化

### 完成 ✅
- [x] Few-Shot Examples提升格式质量
- [x] TableFixer自动修复紧凑表格
- [x] 自动生成数据可视化图表
- [x] 完美的Markdown格式

### 可选优化
- [ ] PDF导出功能（markdown格式正确后很容易）
- [ ] 更多图表类型（折线图、饼图）
- [ ] 结构化数据输出（JSON → Markdown）

## 📄 License

MIT License

## 🙏 致谢

- Alibaba Cloud（Qwen3-Max API）
- Perplexity AI（Sonar Search API）

---

**查看完整文档**：
- [Prompt完整版](当前Prompt完整版.md)
- [改进说明](格式改进说明.md)
- [快速开始](QUICKSTART.md)
