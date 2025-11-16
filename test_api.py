"""
API 测试脚本
用于测试深度估值报告系统 API 是否正常工作
"""
import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查端点"""
    print("=" * 60)
    print("1. 测试健康检查")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        print(f"✅ 健康检查通过: {data['message']}")
        print(f"   时间戳: {data['timestamp']}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_quick_analysis():
    """测试快速分析"""
    print("\n" + "=" * 60)
    print("2. 测试快速分析")
    print("=" * 60)
    
    try:
        payload = {
            "company": "Apple Inc"
        }
        
        print(f"📤 发送请求: 快速分析 {payload['company']}")
        print("⏳ 等待响应（可能需要30-60秒）...")
        
        response = requests.post(
            f"{API_BASE_URL}/api/v1/quick-analysis",
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            print(f"✅ 快速分析成功！")
            print(f"   公司: {data['company']}")
            print(f"   摘要长度: {len(data.get('summary', ''))} 字符")
            print(f"   摘要预览: {data.get('summary', '')[:200]}...")
            return True
        else:
            print(f"❌ 快速分析失败: {data.get('error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时（超过120秒）")
        return False
    except Exception as e:
        print(f"❌ 快速分析失败: {e}")
        return False

def test_generate_report():
    """测试生成完整报告（可选，耗时较长）"""
    print("\n" + "=" * 60)
    print("3. 测试生成完整报告（可选）")
    print("=" * 60)
    
    choice = input("是否测试完整报告生成？（需要2-3分钟）[y/N]: ").strip().lower()
    if choice != 'y':
        print("⏭️  跳过完整报告测试")
        return True
    
    try:
        payload = {
            "company": "Apple Inc",
            "report_type": "comprehensive",
            "generate_pdf": False,
            "save_to_file": False
        }
        
        print(f"📤 发送请求: 生成 {payload['company']} 的完整报告")
        print("⏳ 等待响应（可能需要2-3分钟）...")
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/api/v1/generate-report",
            json=payload,
            timeout=300  # 5分钟超时
        )
        elapsed = time.time() - start_time
        
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            print(f"✅ 报告生成成功！")
            print(f"   公司: {data['company']}")
            print(f"   实际耗时: {elapsed:.2f}秒")
            if data.get("metadata"):
                print(f"   系统耗时: {data['metadata'].get('elapsed_time', 0):.2f}秒")
                print(f"   查询数: {data['metadata'].get('queries_successful', 0)}/{data['metadata'].get('queries_executed', 0)}")
            print(f"   报告长度: {len(data.get('report', ''))} 字符")
            print(f"   报告预览: {data.get('report', '')[:300]}...")
            return True
        else:
            print(f"❌ 报告生成失败: {data.get('error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时（超过5分钟）")
        return False
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        return False

def test_async_task():
    """测试异步任务（可选）"""
    print("\n" + "=" * 60)
    print("4. 测试异步任务（可选）")
    print("=" * 60)
    
    choice = input("是否测试异步任务？[y/N]: ").strip().lower()
    if choice != 'y':
        print("⏭️  跳过异步任务测试")
        return True
    
    try:
        payload = {
            "company": "Tesla",
            "report_type": "quick",
            "generate_pdf": False,
            "save_to_file": False
        }
        
        print(f"📤 提交异步任务: 生成 {payload['company']} 的报告")
        
        # 提交任务
        response = requests.post(
            f"{API_BASE_URL}/api/v1/generate-report-async",
            json=payload
        )
        response.raise_for_status()
        task_data = response.json()
        
        if task_data.get("status") != "accepted":
            print(f"❌ 任务提交失败")
            return False
        
        task_id = task_data["task_id"]
        print(f"✅ 任务已提交，ID: {task_id}")
        print(f"   状态查询URL: {task_data.get('check_status_url')}")
        
        # 轮询任务状态
        print("⏳ 轮询任务状态...")
        max_attempts = 20
        attempt = 0
        
        while attempt < max_attempts:
            time.sleep(5)  # 等待5秒
            attempt += 1
            
            response = requests.get(f"{API_BASE_URL}/api/v1/task-status/{task_id}")
            response.raise_for_status()
            status = response.json()
            
            print(f"   尝试 {attempt}/{max_attempts}: 状态 = {status['status']}")
            
            if status["status"] == "completed":
                print(f"✅ 任务完成！")
                result = status.get("result", {})
                if result.get("status") == "success":
                    print(f"   报告长度: {len(result.get('report', ''))} 字符")
                return True
            elif status["status"] == "failed":
                print(f"❌ 任务失败: {status.get('error')}")
                return False
        
        print(f"⚠️  任务仍在处理中（已等待 {max_attempts * 5} 秒）")
        return False
        
    except Exception as e:
        print(f"❌ 异步任务测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("🧪 深度估值报告系统 API 测试")
    print("=" * 60)
    print(f"\n📍 API地址: {API_BASE_URL}")
    print("⚠️  请确保API服务器已启动（运行: uvicorn api_server:app --host 0.0.0.0 --port 8000）")
    print()
    
    # 测试列表
    tests = [
        ("健康检查", test_health_check),
        ("快速分析", test_quick_analysis),
    ]
    
    results = []
    
    # 运行基础测试
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except KeyboardInterrupt:
            print("\n\n⚠️  测试被用户中断")
            break
        except Exception as e:
            print(f"\n❌ 测试 '{test_name}' 发生异常: {e}")
            results.append((test_name, False))
    
    # 可选测试
    print("\n" + "=" * 60)
    print("可选测试（需要更长时间）")
    print("=" * 60)
    
    try:
        test_generate_report()
        test_async_task()
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {test_name}")
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()

