"""
测试基类 - 所有测试用例的基类
"""
import unittest
import time
from datetime import datetime
from framework.aw_manager import aw_manager
from utils.logger import get_logger

class BaseTest(unittest.TestCase):
    """测试基类"""
    
    # 用例信息 - 子类必须重写
    case_id = ""
    case_name = ""
    author = ""
    create_date = ""
    description = ""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__name__)
        self.start_time = None
        self.end_time = None
    
    def setUp(self):
        """测试前准备 - 框架自动调用"""
        self.start_time = datetime.now()
        self.logger.info(f"开始执行用例: {self.case_id} - {self.case_name}")
        self.logger.info(f"作者: {self.author}, 创建日期: {self.create_date}")
        
        # 调用用户自定义的setup
        try:
            self.setup()
        except Exception as e:
            self.logger.error(f"Setup执行失败: {str(e)}")
            raise
    
    def tearDown(self):
        """测试后清理 - 框架自动调用"""
        try:
            self.teardown()
        except Exception as e:
            self.logger.error(f"Teardown执行失败: {str(e)}")
        
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.logger.info(f"用例执行完成: {self.case_id}, 耗时: {duration:.2f}秒")
    
    def setup(self):
        """用户自定义的测试前准备 - 子类重写"""
        pass
    
    def teardown(self):
        """用户自定义的测试后清理 - 子类重写"""
        pass
    
    def call_aw(self, aw_name: str, **kwargs):
        """调用AW"""
        return aw_manager.call_aw(aw_name, **kwargs)
    
    def verify(self, condition, message="验证失败"):
        """验证结果"""
        if not condition:
            self.logger.error(f"验证失败: {message}")
            self.fail(message)
        else:
            self.logger.info(f"验证通过: {message}")
    
    def verify_equal(self, actual, expected, message=""):
        """验证相等"""
        msg = message or f"期望值: {expected}, 实际值: {actual}"
        self.assertEqual(actual, expected, msg)
        self.logger.info(f"验证通过: {msg}")
    
    def verify_contains(self, container, item, message=""):
        """验证包含"""
        msg = message or f"验证 {item} 在 {container} 中"
        self.assertIn(item, container, msg)
        self.logger.info(f"验证通过: {msg}")
    
    def sleep(self, seconds):
        """等待"""
        self.logger.info(f"等待 {seconds} 秒")
        time.sleep(seconds)