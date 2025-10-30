import yaml
from utils.ssh_client import SSHClient
from adapters.linux_adapter import LinuxAdapter
from actions import linux_actions, verify_actions
from core.test_runner import TestRunner
from core.case_parser import CaseParser
from utils.logger import get_logger

logger = get_logger()

def init_adapters(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    env = config['environments']['test_env']
    
    for server_config in env['linux_servers']:
        ssh_client = SSHClient(
            host=server_config['ip'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config.get('password'),
            key_file=server_config.get('key_file')
        )
        
        if ssh_client.connect():
            adapter = LinuxAdapter(ssh_client)
            linux_actions.set_adapter(server_config['name'], adapter)
            logger.info(f"初始化适配器: {server_config['name']}")
        else:
            logger.warning(f"服务器 {server_config['name']} ({server_config['ip']}) 连接失败，跳过该服务器")

def main():
    logger.info("=" * 60)
    logger.info("自动化测试平台启动")
    logger.info("=" * 60)
    
    init_adapters('config/env_config.yaml')
    
    runner = TestRunner()
    
    case_file = 'testcases/linux_test_example.yaml'
    case_data = CaseParser.parse_yaml(case_file)
    
    runner.run_case(case_data)
    logger.info("测试执行完成")

if __name__ == '__main__':
    main()
