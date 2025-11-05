"""
ADN Demo测试执行器 - 优化版
"""
import sys
from core.test_runner import TestRunner
from actions.basic_actions import (
    check_server_connectivity,
    check_database_connectivity, 
    clear_database_table,
    restart_adn_containers,
    call_api,
    execute_rtnctl_query,
    execute_iperf_test
)
from utils.logger import get_logger

logger = get_logger()

def main():
    logger.info("ADN自动化测试平台启动")
    
    try:
        # 创建测试运行器
        runner = TestRunner()
        
        # 注册所有AW
        runner.register_action("检查服务器连通性", check_server_connectivity)
        runner.register_action("检查数据库连通性", check_database_connectivity)
        runner.register_action("清理数据库表", clear_database_table)
        runner.register_action("重启ADN容器", restart_adn_containers)
        runner.register_action("调用API", call_api)
        runner.register_action("执行rtnctl查询", execute_rtnctl_query)
        runner.register_action("执行iperf测试", execute_iperf_test)
        
        # 运行测试用例
        success = runner.run_case("testcases/adn_demo.yaml")
        
        if success:
            logger.info("🎉 测试执行成功完成")
            sys.exit(0)
        else:
            logger.error("❌ 测试执行失败")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ 程序执行异常: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()