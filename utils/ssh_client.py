import paramiko
from utils.logger import get_logger

logger = get_logger()

class SSHClient:
    def __init__(self, host, port=22, username=None, password=None, key_file=None, timeout=30):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.timeout = timeout
        self.client = None
        
    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_file:
                self.client.connect(self.host, self.port, self.username, 
                                  key_filename=self.key_file, timeout=self.timeout)
            else:
                self.client.connect(self.host, self.port, self.username, 
                                  self.password, timeout=self.timeout)
            logger.info(f"SSH连接成功: {self.username}@{self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"SSH连接失败: {e}")
            return False
    
    def execute_command(self, command, timeout=30):
        if not self.client:
            self.connect()
        
        try:
            logger.debug(f"执行命令: {command}")
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            result = {
                'exit_code': exit_code,
                'stdout': output,
                'stderr': error,
                'success': exit_code == 0
            }
            logger.debug(f"命令执行结果: exit_code={exit_code}")
            return result
        except Exception as e:
            logger.error(f"命令执行失败: {e}")
            return {'exit_code': -1, 'stdout': '', 'stderr': str(e), 'success': False}
    
    def close(self):
        if self.client:
            self.client.close()
            logger.info(f"SSH连接已关闭: {self.host}")
