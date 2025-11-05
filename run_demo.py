"""
ADN Demo测试执行器
"""
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

def main():
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
    runner.run_case("testcases/adn_demo.yaml")

if __name__ == '__main__':
    main()