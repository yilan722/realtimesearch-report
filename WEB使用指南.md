# Web界面使用指南 🌐

## 快速启动（3步）

### 1️⃣ 安装依赖（首次使用）

```bash
cd /Users/yilanliu/Desktop/realtimesearch-report
pip install -r requirements.txt
```

### 2️⃣ 启动Web服务

```bash
streamlit run web_app.py
```

### 3️⃣ 自动打开浏览器

命令执行后会自动打开浏览器，访问：

**http://localhost:8501**

如果没有自动打开，手动在浏览器中访问上面的地址。

---

## 界面功能

### 🏠 首页
- 系统介绍和核心优势
- 成本参考
- 快速开始指南

### 📈 单公司分析
- 输入公司名称
- 选择报告类型（完整/快速）
- 实时进度显示
- 报告预览和下载

### ⚡ 快速分析
- 支持批量输入
- 每行一个公司名称
- 快速生成投资要点

### 🔄 比较分析
- 对比2-3个公司
- 横向比较投资价值
- 生成比较报告

### 📚 历史报告
- 查看本次会话历史
- 浏览已保存的报告
- 下载历史报告

### ⚙️ 设置
- 调整查询数量
- 调整分析深度
- 查看API配置
- 预设配置方案

---

## 使用示例

### 示例1: 分析单个公司

1. 点击左侧 **"📈 单公司分析"**
2. 输入公司名称，如：`Apple Inc`
3. 选择 **"完整报告（推荐）"**
4. 勾选 **"保存到文件"**
5. 点击 **"🚀 开始分析"**
6. 等待2-3分钟，查看生成的报告

### 示例2: 快速批量分析

1. 点击左侧 **"⚡ 快速分析"**
2. 在文本框中输入（每行一个）：
   ```
   Tesla
   BYD
   NIO
   ```
3. 点击 **"⚡ 开始快速分析"**
4. 快速查看每个公司的投资要点

### 示例3: 比较分析

1. 点击左侧 **"🔄 比较分析"**
2. 输入3个公司：
   - 公司1: `Apple`
   - 公司2: `Microsoft`
   - 公司3: `Google`
3. 点击 **"🔄 开始比较分析"**
4. 等待5-10分钟，查看比较报告

---

## 界面特性

### ✨ 美观的UI
- 现代化的设计
- 响应式布局
- 直观的导航

### 🚀 实时反馈
- 进度条显示
- 状态更新
- 错误提示

### 📊 数据可视化
- 统计指标展示
- 元数据显示
- 历史记录

### 💾 报告管理
- 自动保存
- 在线预览
- 一键下载

---

## 端口说明

**默认端口**: `8501`

- Web界面: http://localhost:8501
- 可以从局域网其他设备访问（如果需要）

### 修改端口

如果8501端口被占用，可以指定其他端口：

```bash
streamlit run web_app.py --server.port 8502
```

然后访问: http://localhost:8502

---

## 常见问题

### Q: 启动失败怎么办？

**检查依赖**:
```bash
pip install streamlit
```

**检查端口**:
```bash
lsof -i :8501  # 查看端口占用
```

### Q: 浏览器没有自动打开？

手动访问: http://localhost:8501

### Q: 报告生成很慢？

这是正常的，深度分析需要：
- 查询规划: 5秒
- 信息收集: 30-60秒
- 深度分析: 20-40秒

总计约2-3分钟。

### Q: 可以同时运行多个分析吗？

可以，但建议一次分析一个，避免API限流。

### Q: 如何停止服务？

在终端按 `Ctrl + C` 即可停止。

---

## 高级配置

### 修改主题

编辑 `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### 性能优化

```bash
# 增加上传大小限制
streamlit run web_app.py --server.maxUploadSize 200

# 启用缓存
streamlit run web_app.py --server.enableCORS false
```

---

## 局域网访问

如果想让同一局域网的其他设备访问：

```bash
streamlit run web_app.py --server.address 0.0.0.0
```

然后其他设备访问: `http://你的IP:8501`

查看本机IP:
```bash
ifconfig | grep inet  # Mac/Linux
ipconfig              # Windows
```

---

## 部署到生产环境

### 使用Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "web_app.py", "--server.address", "0.0.0.0"]
```

构建和运行:
```bash
docker build -t valuation-report .
docker run -p 8501:8501 valuation-report
```

### 使用Streamlit Cloud

1. 推送代码到GitHub
2. 访问 https://streamlit.io/cloud
3. 连接GitHub仓库
4. 一键部署

---

## 快捷键

| 快捷键 | 功能 |
|--------|------|
| `R` | 重新运行应用 |
| `C` | 清除缓存 |
| `Ctrl+C` | 停止服务 |

---

## 性能提示

1. **首次加载较慢** - 正常现象，需要初始化
2. **避免频繁刷新** - 会重新初始化系统
3. **API限流** - 如果遇到错误，等待几秒重试
4. **内存占用** - 长时间运行建议重启服务

---

## 故障排除

### 错误: "Command not found: streamlit"

解决:
```bash
pip install streamlit
```

### 错误: "Port 8501 is already in use"

解决:
```bash
# 方法1: 更换端口
streamlit run web_app.py --server.port 8502

# 方法2: 杀死占用进程
lsof -ti:8501 | xargs kill -9
```

### 错误: "ModuleNotFoundError"

解决:
```bash
pip install -r requirements.txt
```

---

## 下一步

- 尝试分析你关注的公司
- 探索不同的配置选项
- 查看生成的历史报告
- 调整设置优化成本和质量

---

**开始使用吧！** 🚀

```bash
streamlit run web_app.py
```

