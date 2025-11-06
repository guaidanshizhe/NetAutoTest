"""
ADN网络连通性测试用例
"""
from framework.base_test import BaseTest

class TC_ADN_001(BaseTest):
    """ADN网络连通性测试"""
    
    # ========== 用例信息 ==========
    case_id = "TC_ADN_001"
    case_name = "ADN网络连通性测试"
    author = "测试工程师"
    create_date = "2024-01-01"
    description = "验证ADN服务器的网络连通性，包括ping测试和端口检查"
    
    def setup(self):
        """测试前准备"""
        self.server_ip = "192.168.1.100"  # 从配置文件读取
        self.logger.info(f"准备测试服务器: {self.server_ip}")
    
    def test_TC_ADN_001(self):
        """测试用例主体"""
        # 步骤1：检查服务器ping连通性
        ping_result = self.call_aw("ping服务器", server_ip=self.server_ip, count=4)
        self.verify(ping_result["success"], "服务器ping不通")
        
        # 步骤2：检查SSH端口连通性
        ssh_result = self.call_aw("检查端口开放", server_ip=self.server_ip, port=22)
        self.verify(ssh_result, "SSH端口22未开放")
        
        # 步骤3：检查HTTP服务
        http_result = self.call_aw("检查HTTP服务", url=f"http://{self.server_ip}:8080/health")
        self.verify(http_result["success"], "HTTP服务不可用")
        
        # 步骤4：验证响应时间
        self.verify(http_result["response_time"] < 2.0, "HTTP响应时间过长")
    
    def teardown(self):
        """测试后清理"""
        self.logger.info("网络连通性测试完成")

if __name__ == '__main__':
    import unittest
    unittest.main()