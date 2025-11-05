"""
测试用例基础模块
提供通用的初始化和执行功能
"""
import yaml
from utils.ssh_client import SSHClient
from adapters.linux_adapter import LinuxAdapter
from adapters.database_adapter import DatabaseAdapter
# 自动导入所有AW模块，确保AW已注册
from actions import (aw_linux, aw_verify, aw_network, 
                     aw_database, aw_report, aw_batch, aw_recovery)
from core.test_runner import TestRunner
from core.case_parser import CaseParser
from utils.logger import get_logger

logger = get_logger()

def init_adapters(config_file='config/env_config.yaml', env_name=None):
    """初始化所有适配器
    
    Args:
        config_file: 配置文件路径
        env_name: 环境名称，不指定则使用默认环境
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 使用指定环境或默认环境
    if not env_name:
        env_name = config.get('default_env', 'test_env')
    
    logger.info(f"使用环境: {env_name}")
    env = config['environments'][env_name]
    
    # 初始化Linux适配器
    for server_config in env.get('linux_servers', []):
        ssh_client = SSHClient(
            host=server_config['ip'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config.get('password'),
            key_file=server_config.get('key_file')
        )
        
        if ssh_client.connect():
            adapter = LinuxAdapter(ssh_client)
            aw_linux.set_adapter(server_config['name'], adapter)
            logger.info(f"初始化Linux适配器: {server_config['name']}")
        else:
            logger.warning(f"服务器 {server_config['name']} ({server_config['ip']}) 连接失败，跳过该服务器")
    
    # 初始化数据库适配器
    for db_config in env.get('databases', []):
        db_adapter = DatabaseAdapter(
            host=db_config['host'],
            port=db_config['port'],
            username=db_config['username'],
            password=db_config['password'],
            database=db_config.get('database')
        )
        aw_database.set_db_adapter(db_config['name'], db_adapter)
        logger.info(f"初始化数据库适配器: {db_config['name']}")

def run_test_case(case_file, title=None, env_name=None):
    """运行测试用例
    
    Args:
        case_file: 用例文件路径
        title: 测试标题
        env_name: 环境名称（test_env/pre_prod_env/prod_env）
    """
    if title:
        logger.info("=" * 60)
        logger.info(title)
        logger.info("=" * 60)
    
    init_adapters(env_name=env_name)
    
    runner = TestRunner()
    case_data = CaseParser.parse_yaml(case_file)
    runner.run_case(case_data)
    
    logger.info("\n" + "=" * 60)
    logger.info("测试执行完成")
    logger.info("=" * 60)
