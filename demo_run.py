#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
框架演示脚本
展示如何使用自动化测试框架
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入框架组件
from framework.aw_manager import aw_manager
from actions import network_aws  # 确保AW被注册
from testcases.TC_ADN_001 import TC_ADN_001
import unittest

def show_available_aws():
    """显示所有可用的AW"""
    print("=" * 50)
    print("可用的AW列表:")
    print("=" * 50)
    
    aw_list = aw_manager.get_aw_list()
    for aw_name, description in aw_list.items():
        print(f"- {aw_name}: {description}")
    print()

def run_demo_test():
    """运行演示测试"""
    print("=" * 50)
    print("运行演示测试用例:")
    print("=" * 50)
    
    # 创建测试套件
    suite = unittest.TestSuite()
    suite.addTest(TC_ADN_001('test_TC_ADN_001'))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def main():
    """主函数"""
    print("ADN自动化测试框架演示")
    print("=" * 50)
    
    # 显示可用AW
    show_available_aws()
    
    # 运行演示测试
    success = run_demo_test()
    
    print("=" * 50)
    if success:
        print("演示完成: 测试通过")
    else:
        print("演示完成: 测试失败")
    print("=" * 50)

if __name__ == '__main__':
    main()