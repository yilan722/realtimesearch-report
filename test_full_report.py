"""
测试完整报告生成
"""
from main import ValuationReportSystem
import time

system = ValuationReportSystem()

print('开始生成NVIDIA完整报告...')
print('预计需要3-5分钟，请耐心等待...\n')

start = time.time()

try:
    result = system.generate_report(
        'NVIDIA Corporation',
        report_type='comprehensive',
        save_to_file=True
    )
    
    elapsed = time.time() - start
    
    print(f'\n总耗时: {elapsed:.1f}秒')
    print(f'状态: {result["status"]}')
    
    if result['status'] == 'success':
        print(f'\n✅ 成功生成报告!')
        print(f'报告长度: {len(result["report"])} 字符')
        print(f'保存文件: {result["metadata"].get("saved_file", "未保存")}')
        print(f'查询数: {result["metadata"]["queries_successful"]}/{result["metadata"]["queries_executed"]}')
        
        print(f'\n报告前500字符预览:')
        print('='*80)
        print(result['report'][:500])
        print('...')
        print('='*80)
    else:
        print(f'\n❌ 生成失败!')
        print(f'错误: {result.get("error")}')
        
except KeyboardInterrupt:
    print('\n用户中断')
except Exception as e:
    print(f'\n❌ 发生异常: {e}')
    import traceback
    traceback.print_exc()

