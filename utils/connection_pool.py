"""
连接池管理器 - 复用SSH和数据库连接
"""
import paramiko
import pymysql
from utils.logger import get_logger
from utils.config_manager import config_manager

logger = get_logger()

class ConnectionPool:
    def __init__(self):
        self.ssh_connections = {}
        self.db_connections = {}
    
    def get_ssh_connection(self, server_name):
        """获取SSH连接"""
        if server_name not in self.ssh_connections:
            server_config = config_manager.get_server_config(server_name)
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=server_config['ip'],
                    port=server_config.get('port', 22),
                    username=server_config['username'],
                    password=server_config['password'],
                    timeout=10
                )
                self.ssh_connections[server_name] = ssh
                logger.debug(f"SSH连接已建立: {server_name}")
            except Exception as e:
                logger.error(f"SSH连接失败: {server_name}, {e}")
                raise
        return self.ssh_connections[server_name]
    
    def get_db_connection(self, db_name):
        """获取数据库连接"""
        if db_name not in self.db_connections:
            db_config = config_manager.get_database_config(db_name)
            try:
                conn = pymysql.connect(
                    host=db_config['host'],
                    port=db_config.get('port', 3306),
                    user=db_config['username'],
                    password=db_config['password'],
                    database=db_config['database'],
                    connect_timeout=10
                )
                self.db_connections[db_name] = conn
                logger.debug(f"数据库连接已建立: {db_name}")
            except Exception as e:
                logger.error(f"数据库连接失败: {db_name}, {e}")
                raise
        return self.db_connections[db_name]
    
    def close_all(self):
        """关闭所有连接"""
        for name, ssh in self.ssh_connections.items():
            try:
                ssh.close()
                logger.debug(f"SSH连接已关闭: {name}")
            except:
                pass
        
        for name, conn in self.db_connections.items():
            try:
                conn.close()
                logger.debug(f"数据库连接已关闭: {name}")
            except:
                pass
        
        self.ssh_connections.clear()
        self.db_connections.clear()

# 全局连接池实例
connection_pool = ConnectionPool()