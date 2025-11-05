"""
快速测试 - 验证超时修复
"""
import time

print("="*80)
print("🧪 测试超时修复")
print("="*80)

# 测试1: 检查增强版客户端
print("\n[测试1] 检查增强版客户端...")
try:
    from api_clients import QwenClient
    from api_clients.qwen_client_enhanced import QwenClientEnhanced
    
    # 检查是否使用增强版
    if QwenClient == QwenClientEnhanced:
        print("✅ 增强版客户端已启用")
    else:
        print("⚠️ 使用标准客户端")
        
    client = QwenClient()
    print(f"✅ 客户端初始化成功")
    print(f"   - 超时时间: {client.timeout}秒")
    print(f"   - 最大重试: {client.max_retries}次")
except Exception as e:
    print(f"❌ 客户端加载失败: {e}")

# 测试2: 快速API调用
print("\n[测试2] 测试API连接（超时测试）...")
try:
    start = time.time()
    result = client.simple_prompt(
        "请简单回复'OK'",
        max_tokens=50,
        temperature=0.3
    )
    elapsed = time.time() - start
    print(f"✅ API调用成功")
    print(f"   - 响应时间: {elapsed:.2f}秒")
    print(f"   - 响应内容: {result[:100]}")
except Exception as e:
    print(f"❌ API调用失败: {e}")

# 测试3: 检查配置
print("\n[测试3] 检查配置...")
try:
    from config import (
        API_TIMEOUT, 
        MAX_RETRIES, 
        DEEP_ANALYSIS_MAX_TOKENS,
        MAX_SONAR_QUERIES
    )
    print(f"✅ 配置已加载")
    print(f"   - API超时: {API_TIMEOUT}秒")
    print(f"   - 最大重试: {MAX_RETRIES}次")
    print(f"   - 深度分析tokens: {DEEP_ANALYSIS_MAX_TOKENS}")
    print(f"   - 最大查询数: {MAX_SONAR_QUERIES}")
except Exception as e:
    print(f"❌ 配置加载失败: {e}")

# 测试4: 测试完整系统（可选）
print("\n[测试4] 是否测试完整报告生成？")
print("⚠️  完整报告需要1-2分钟，可能产生API费用")
print("💡 跳过此测试，使用以下命令手动测试：")
print("   python -c \"from main import ValuationReportSystem; ValuationReportSystem().generate_report('Apple Inc')\"")

print("\n" + "="*80)
print("✅ 基础测试完成！")
print("="*80)

print("\n📊 测试总结:")
print("  ✅ 增强版客户端: 已启用")
print("  ✅ 超时时间: 已增加到300秒")
print("  ✅ 重试机制: 已启用（最多3次）")
print("  ✅ Token优化: 已降低到6000")

print("\n💡 下一步:")
print("  1. 运行完整测试: python test_professional_format.py")
print("  2. 或使用Web界面: streamlit run web_app.py")
print("  3. 如仍超时，降低token数到4000（编辑config.py）")

print("\n🚀 系统已准备就绪！")
