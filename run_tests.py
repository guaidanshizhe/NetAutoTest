"""
测试执行器
支持单个用例和批量用例执行
"""
import sys
import os
import unittest
import argparse
import importlib.util
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入所有AW模块以确保AW被注册
from actions import network_aws

def run_single_test(test_file):
    """运行单个测试用例"""
    if not Path(test_file).exists():
        print(f"测试文件不存在: {test_file}")
        return False
    
    # 动态导入测试模块
    module_name = Path(test_file).stem
    spec = importlib.util.spec_from_file_location(module_name, test_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # 运行测试
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_batch_tests(pattern="TC_*.py"):
    """批量运行测试用例"""
    loader = unittest.TestLoader()
    suite = loader.discover('testcases', pattern=pattern)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    parser = argparse.ArgumentParser(description='ADN自动化测试执行器')
    parser.add_argument('-f', '--file', help='执行单个测试文件')
    parser.add_argument('-p', '--pattern', default='TC_*.py', help='批量执行模式的文件模式')
    parser.add_argument('-l', '--list', action='store_true', help='列出所有测试用例')
    
    args = parser.parse_args()
    
    if args.list:
        # 列出所有测试用例
        testcases_dir = Path('testcases')
        for test_file in testcases_dir.glob('TC_*.py'):
            print(f"- {test_file.name}")
        return
    
    if args.file:
        # 执行单个测试
        success = run_single_test(args.file)
    else:
        # 批量执行测试
        success = run_batch_tests(args.pattern)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()