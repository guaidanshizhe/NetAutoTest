"""
基础AW - 优化版本
"""
import requests
import subprocess
from utils.logger import get_logger
from utils.config_manager import config_manager
from utils.connection_pool import connection_pool

logger = get_logger()

def validate_params(params, required_fields):
    """参数验证"""
    for field in required_fields:
        if field not in params or not params[field]:
            raise ValueError(f"缺少必需参数: {field}")

# ==================== 1. 连通性检查 ====================

def check_server_connectivity(server_name):
    """检查服务器连通性"""
    validate_params(locals(), ['server_name'])
    
    try:
        ssh = connection_pool.get_ssh_connection(server_name)
        # 执行简单命令测试连接
        stdin, stdout, stderr = ssh.exec_command('echo "connection_test"')
        result = stdout.read().decode().strip()
        
        if result == "connection_test":
            logger.info(f"✓ 服务器 {server_name} 连通性检查通过")
            return True
        else:
            logger.error(f"✗ 服务器 {server_name} 连通性检查失败")
            return False
    except Exception as e:
        logger.error(f"✗ 服务器 {server_name} 连通性检查失败: {e}")
        return False

def check_database_connectivity(db_name):
    """检查数据库连通性"""
    validate_params(locals(), ['db_name'])
    
    try:
        conn = connection_pool.get_db_connection(db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            logger.info(f"✓ 数据库 {db_name} 连通性检查通过")
            return True
        else:
            logger.error(f"✗ 数据库 {db_name} 连通性检查失败")
            return False
    except Exception as e:
        logger.error(f"✗ 数据库 {db_name} 连通性检查失败: {e}")
        return False

# ==================== 2. 数据库操作 ====================

def clear_database_table(db_name, tables):
    """清理数据库表数据"""
    validate_params(locals(), ['db_name', 'tables'])
    
    # 处理不同的tables参数格式
    table_list = []
    if isinstance(tables, str):
        for table in tables.split(','):
            table_list.append({'name': table.strip(), 'condition': ''})
    elif isinstance(tables, list):
        for table in tables:
            if isinstance(table, str):
                table_list.append({'name': table, 'condition': ''})
            elif isinstance(table, dict):
                table_list.append({
                    'name': table.get('name', ''),
                    'condition': table.get('condition', '')
                })
    
    if not table_list:
        logger.error("✗ 没有指定要清理的表")
        return False
    
    try:
        conn = connection_pool.get_db_connection(db_name)
        cursor = conn.cursor()
        
        total_affected = 0
        success_count = 0
        
        for table_info in table_list:
            table_name = table_info['name']
            condition = table_info['condition']
            
            try:
                if condition:
                    sql = f"DELETE FROM {table_name} WHERE {condition}"
                    logger.info(f"清理表 {table_name}，条件: {condition}")
                else:
                    sql = f"DELETE FROM {table_name}"
                    logger.info(f"清空表 {table_name}")
                
                cursor.execute(sql)
                affected_rows = cursor.rowcount
                total_affected += affected_rows
                success_count += 1
                
                logger.info(f"✓ 表 {table_name} 清理成功，删除 {affected_rows} 行")
                
            except Exception as e:
                logger.error(f"✗ 表 {table_name} 清理失败: {e}")
        
        conn.commit()
        logger.info(f"✓ 数据库清理完成，成功 {success_count}/{len(table_list)} 个表，共删除 {total_affected} 行")
        return success_count == len(table_list)
        
    except Exception as e:
        logger.error(f"✗ 数据库清理失败: {e}")
        return False

# ==================== 3. Docker操作 ====================

def restart_adn_containers(server_name="adn_server"):
    """重启ADN服务容器"""
    validate_params(locals(), ['server_name'])
    
    try:
        config = config_manager.get_config()
        containers = config.get('adn_services', [])
        
        if not containers:
            logger.error("✗ 未配置ADN服务容器")
            return False
        
        ssh = connection_pool.get_ssh_connection(server_name)
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
        
        result = success_count == len(containers)
        if result:
            logger.info(f"✓ 所有ADN容器重启成功")
        else:
            logger.error(f"✗ 部分容器重启失败 ({success_count}/{len(containers)})")
        
        return result
        
    except Exception as e:
        logger.error(f"✗ 重启ADN容器失败: {e}")
        return False

# ==================== 4. API调用 ====================

def call_api(endpoint, method="GET", json_data=None):
    """调用API接口"""
    validate_params(locals(), ['endpoint'])
    
    try:
        config = config_manager.get_config()
        base_url = config.get('apis', {}).get('base_url', '')
        
        if not base_url:
            logger.error("✗ 未配置API基础URL")
            return None
        
        url = f"{base_url}{endpoint}"
        logger.info(f"调用API: {method} {endpoint}")
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=30)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=30)
        else:
            logger.error(f"✗ 不支持的HTTP方法: {method}")
            return None
        
        logger.info(f"✓ API调用成功: 状态码 {response.status_code}")
        return response.json() if response.content else {}
        
    except Exception as e:
        logger.error(f"✗ API调用失败: {e}")
        return None

# ==================== 5. rtnctl工具 ====================

def execute_rtnctl_query(query_params, server_name="adn_server"):
    """执行rtnctl查询"""
    validate_params(locals(), ['query_params'])
    
    try:
        config = config_manager.get_config()
        rtnctl_path = config.get('tools', {}).get('rtnctl_path', '/usr/local/bin/rtnctl')
        
        ssh = connection_pool.get_ssh_connection(server_name)
        command = f"{rtnctl_path} {query_params}"
        logger.info(f"执行rtnctl查询: {command}")
        
        stdin, stdout, stderr = ssh.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        
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
    validate_params(locals(), ['server_ip'])
    
    try:
        command = f"iperf3 -c {server_ip} -p {port} -t {duration} -J"
        logger.info(f"执行iperf测试: 目标 {server_ip}:{port}, 时长 {duration}s")
        
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=duration+10)
        
        if result.returncode == 0:
            logger.info("✓ iperf测试成功")
            return result.stdout
        else:
            logger.error(f"✗ iperf测试失败: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        logger.error("✗ iperf测试超时")
        return None
    except Exception as e:
        logger.error(f"✗ iperf测试失败: {e}")
        return None