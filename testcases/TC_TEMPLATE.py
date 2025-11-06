"""
测试用例模板
复制此文件创建新的测试用例
"""
from framework.base_test import BaseTest

class TC_TEMPLATE(BaseTest):
    """测试用例模板类"""
    
    # ========== 用例信息 ==========
    case_id = "TC_XXX_001"                    # 用例ID
    case_name = "用例名称描述"                  # 用例名称
    author = "测试人员姓名"                     # 作者
    create_date = "2024-01-01"                # 创建日期
    description = "详细的用例描述和测试目标"     # 用例描述
    
    def setup(self):
        """
        测试前准备
        在此处编写测试前的初始化动作
        """
        # 示例：初始化测试环境
        # self.call_aw("连接服务器", server_ip="192.168.1.100")
        # self.call_aw("清理测试数据")
        pass
    
    def test_TC_XXX_001(self):
        """
        测试用例主体
        方法名必须以 test_ 开头，建议使用 test_用例ID 格式
        """
        # 步骤1：执行测试动作
        # result1 = self.call_aw("AW名称", 参数1="值1", 参数2="值2")
        
        # 步骤2：验证结果
        # self.verify(result1, "验证描述")
        # self.verify_equal(actual_value, expected_value, "相等验证")
        
        # 步骤3：继续测试步骤
        # result2 = self.call_aw("另一个AW", 参数="值")
        # self.verify_contains(result2, "期望内容", "包含验证")
        
        # 示例实现
        self.logger.info("这是一个测试用例模板")
        pass
    
    def teardown(self):
        """
        测试后清理
        在此处编写测试后的清理动作
        """
        # 示例：清理测试环境
        # self.call_aw("断开连接")
        # self.call_aw("清理测试数据")
        pass

if __name__ == '__main__':
    # 单独运行此用例
    import unittest
    unittest.main()