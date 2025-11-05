# 快速入门指南 🚀

## 5分钟上手

### 1. 安装依赖

```bash
cd /Users/yilanliu/Desktop/realtimesearch-report
pip install -r requirements.txt
```

### 2. 运行第一个分析

```bash
python main.py
```

这将自动为 "Apple Inc" 生成一份完整的估值报告！

### 3. 查看结果

报告会保存在 `reports/` 目录下，文件名格式：`公司名_时间戳.md`

## 使用方式

### 方式1: 直接使用Python

```python
from main import ValuationReportSystem

# 创建系统
system = ValuationReportSystem()

# 生成报告
result = system.generate_report("Tesla")

# 查看报告
print(result["report"])
```

### 方式2: 运行示例脚本

```bash
python examples.py
```

然后选择你想运行的示例。

### 方式3: 快速分析

```python
from main import ValuationReportSystem

system = ValuationReportSystem()
summary = system.quick_analysis("Microsoft")
print(summary)
```

## 常见使用场景

### 场景1: 单个公司深度分析

```python
system = ValuationReportSystem()
result = system.generate_report(
    company="NVIDIA Corporation",
    report_type="comprehensive",
    save_to_file=True
)
```

### 场景2: 比较多个公司

```python
system = ValuationReportSystem()
comparison = system.compare_companies(["Apple", "Microsoft", "Google"])
print(comparison["comparison"])
```

### 场景3: 批量生成报告

```python
system = ValuationReportSystem()

companies = ["Tesla", "BYD", "NIO"]
for company in companies:
    result = system.generate_report(company, save_to_file=True)
    print(f"✅ {company} 报告已生成")
```

## 测试系统

```bash
# 运行所有测试
python test_system.py

# 运行单个测试
python test_system.py api          # API连接测试
python test_system.py planning     # 查询规划测试
python test_system.py quick        # 快速分析测试
python test_system.py full         # 完整报告测试
```

## 成本优化提示

1. **使用快速分析模式**：成本约为完整报告的30%
   ```python
   system.quick_analysis("Company Name")
   ```

2. **调整查询数量**：在 `config.py` 中修改 `MAX_SONAR_QUERIES`
   ```python
   MAX_SONAR_QUERIES = 5  # 默认8，减少到5可降低成本
   ```

3. **使用缓存**（未来功能）：重复查询会使用缓存结果

## 自定义配置

编辑 `config.py` 文件：

```python
# 调整token限制
QUERY_PLANNER_MAX_TOKENS = 500      # 查询规划（越少越便宜）
DEEP_ANALYSIS_MAX_TOKENS = 8000     # 深度分析（越多越详细）

# 调整并发数
MAX_CONCURRENT_SEARCHES = 5         # 并行搜索数（影响速度）

# 调整查询数量
MAX_SONAR_QUERIES = 8              # 每次分析的查询数（影响成本）
```

## 下一步

- 查看 `README.md` 了解完整功能
- 运行 `examples.py` 查看更多示例
- 查看生成的报告了解输出格式
- 根据需要修改 `config.py` 优化性能和成本

## 疑难解答

### 问题1: API连接失败

确保API密钥正确配置在 `config.py` 中：
```python
PERPLEXITY_API_KEY = "pplx-..."
QWEN_API_KEY = "sk-..."
```

### 问题2: 报告质量不满意

尝试调整以下参数：
- 增加 `MAX_SONAR_QUERIES` 以获取更多信息
- 增加 `DEEP_ANALYSIS_MAX_TOKENS` 以生成更详细的分析

### 问题3: 速度太慢

- 减少 `MAX_SONAR_QUERIES`
- 增加 `MAX_CONCURRENT_SEARCHES`
- 使用快速分析模式

## 支持

遇到问题？查看 `README.md` 或提交 Issue。

---

**开始你的第一次分析吧！** 🎉

