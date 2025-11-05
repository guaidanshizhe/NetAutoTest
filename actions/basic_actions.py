"""
基础AW - 根据demo用例需求实现
"""
import yaml
import requests
import subprocess
import pymysql
import paramiko
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

# 加载配置
def load_config():
    config_file = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

config = load_config()

# ==================== 1. 连通性检查 ====================

def check_server_connectivity():
    """检查服务器连通性"""
    server_config = config['servers']['adn_server']
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server_config['ip'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config['password'],
            timeout=10
        )
        ssh.close()
        logger.info("✓ 服务器连通性检查通过")
        return True
    except Exception as e:
        logger.error(f"✗ 服务器连通性检查失败: {e}")
        return False

def check_database_connectivity():
    """检查数据库连通性"""
    db_config = config['databases']['adn_db']
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database'],
            connect_timeout=10
        )
        conn.close()
        logger.info("✓ 数据库连通性检查通过")
        return True
    except Exception as e:
        logger.error(f"✗ 数据库连通性检查失败: {e}")
        return False

# ==================== 2. 数据库操作 ====================

def clear_database_table(table_name, condition=""):
    """清理数据库表数据"""
    db_config = config['databases']['adn_db']
    try:
        conn = pymysql.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['username'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()
        
        if condition:
            sql = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            sql = f"DELETE FROM {table_name}"
        
        cursor.execute(sql)
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"✓ 清理表 {table_name}，删除 {affected_rows} 行数据")
        return True
    except Exception as e:
        logger.error(f"✗ 清理表失败: {e}")
        return False

# ==================== 3. Docker操作 ====================

def restart_adn_containers():
    """重启ADN服务容器"""
    server_config = config['servers']['adn_server']
    containers = config['adn_services']
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server_config['ip'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config['password']
        )
        
        success_count = 0
        for container in containers:
            container_name = container['container_name']
            logger.info(f"重启容器: {container_name}")
            
            stdin, stdout, stderr = ssh.exec_command(f"docker restart {container_name}")
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code == 0:
                logger.info(f"✓ 容器 {container_name} 重启成功")
                success_count += 1
            else:
                error = stderr.read().decode()
                logger.error(f"✗ 容器 {container_name} 重启失败: {error}")
        
        ssh.close()
        return success_count == len(containers)
    except Exception as e:
        logger.error(f"✗ 重启容器失败: {e}")
        return False

# ==================== 4. API调用 ====================

def call_api(endpoint, method="GET", json_data=None):
    """调用API接口"""
    base_url = config['apis']['base_url']
    url = f"{base_url}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=30)
        else:
            logger.error(f"不支持的HTTP方法: {method}")
            return None
        
        logger.info(f"✓ API调用成功: {method} {endpoint}, 状态码: {response.status_code}")
        return response.json() if response.content else {}
    except Exception as e:
        logger.error(f"✗ API调用失败: {e}")
        return None

# ==================== 5. rtnctl工具 ====================

def execute_rtnctl_query(query_params):
    """执行rtnctl查询"""
    server_config = config['servers']['adn_server']
    rtnctl_path = config['tools']['rtnctl_path']
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server_config['ip'],
            port=server_config['port'],
            username=server_config['username'],
            password=server_config['password']
        )
        
        command = f"{rtnctl_path} {query_params}"
        logger.info(f"执行rtnctl查询: {command}")
        
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        
        ssh.close()
        
        if exit_code == 0:
            logger.info("✓ rtnctl查询成功")
            return output
        else:
            error = stderr.read().decode()
            logger.error(f"✗ rtnctl查询失败: {error}")
            return None
    except Exception as e:
        logger.error(f"✗ rtnctl查询失败: {e}")
        return None

# ==================== 6. iperf打流 ====================

def execute_iperf_test(server_ip, port=5201, duration=10):
    """执行iperf打流测试"""
    try:
        command = f"iperf3 -c {server_ip} -p {port} -t {duration} -J"
        logger.info(f"执行iperf测试: {command}")
        
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=duration+10)
        
        if result.returncode == 0:
            logger.info("✓ iperf测试成功")
            return result.stdout
        else:
            logger.error(f"✗ iperf测试失败: {result.stderr}")
            return None
    except Exception as e:
        logger.error(f"✗ iperf测试失败: {e}")
        return None