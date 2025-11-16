"""
快速验证 Single Company Deep Analysis API 是否可用
"""
import sys

def check_dependencies():
    """检查依赖是否安装"""
    print("🔍 检查依赖...")
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI 和 uvicorn 已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("   请运行: pip install -r requirements.txt")
        return False

def check_api_server():
    """检查API服务器是否可以导入"""
    print("\n🔍 检查API服务器...")
    try:
        from api_server import app
        print("✅ API服务器可以正常导入")
        print(f"   API名称: {app.title}")
        return True
    except Exception as e:
        print(f"❌ API服务器导入失败: {e}")
        return False

def check_main_system():
    """检查主系统是否可以导入"""
    print("\n🔍 检查报告生成系统...")
    try:
        from main import ValuationReportSystem
        print("✅ 报告生成系统可以正常导入")
        return True
    except Exception as e:
        print(f"❌ 报告生成系统导入失败: {e}")
        return False

def main():
    """主验证函数"""
    print("=" * 60)
    print("🧪 Single Company Deep Analysis API 验证")
    print("=" * 60)
    print()
    
    checks = [
        ("依赖检查", check_dependencies),
        ("API服务器", check_api_server),
        ("报告系统", check_main_system),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} 检查时发生异常: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 验证结果")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 所有检查通过！API可以使用了！")
        print()
        print("启动API服务器:")
        print("  uvicorn api_server:app --host 0.0.0.0 --port 8000")
        print("  或运行: ./启动API.sh")
        print()
        print("访问API文档:")
        print("  http://localhost:8000/docs")
    else:
        print("⚠️  部分检查未通过，请修复后重试")
        sys.exit(1)

if __name__ == "__main__":
    main()

