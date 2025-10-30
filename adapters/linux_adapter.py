from utils.ssh_client import SSHClient
from utils.logger import get_logger

logger = get_logger()

class LinuxAdapter:
    
    def __init__(self, ssh_client: SSHClient):
        self.ssh = ssh_client
    
    def execute_shell(self, command, timeout=30):
        return self.ssh.execute_command(command, timeout)
    
    def check_process_exists(self, process_name):
        result = self.ssh.execute_command(f"ps aux | grep -v grep | grep {process_name}")
        return result['success'] and process_name in result['stdout']
    
    def get_process_count(self, process_name):
        result = self.ssh.execute_command(f"ps aux | grep -v grep | grep {process_name} | wc -l")
        if result['success']:
            return int(result['stdout'].strip())
        return 0
    
    def kill_process(self, process_name, signal=15):
        result = self.ssh.execute_command(f"pkill -{signal} {process_name}")
        return result['success']
    
    def read_file(self, file_path):
        result = self.ssh.execute_command(f"cat {file_path}")
        return result['stdout'] if result['success'] else None
    
    def write_file(self, file_path, content):
        escaped_content = content.replace("'", "'\\''")
        result = self.ssh.execute_command(f"echo '{escaped_content}' > {file_path}")
        return result['success']
    
    def file_exists(self, file_path):
        result = self.ssh.execute_command(f"test -f {file_path} && echo 'exists'")
        return 'exists' in result['stdout']
    
    def get_cpu_usage(self):
        result = self.ssh.execute_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
        if result['success']:
            return float(result['stdout'].strip())
        return None
    
    def get_memory_usage(self):
        result = self.ssh.execute_command("free | grep Mem | awk '{print ($3/$2) * 100.0}'")
        if result['success']:
            return float(result['stdout'].strip())
        return None
    
    def get_disk_usage(self, path="/"):
        result = self.ssh.execute_command(f"df -h {path} | tail -1 | awk '{{print $5}}' | cut -d'%' -f1")
        if result['success']:
            return float(result['stdout'].strip())
        return None
    
    def check_port_listening(self, port):
        result = self.ssh.execute_command(f"netstat -tuln | grep ':{port} '")
        return result['success'] and str(port) in result['stdout']
    
    def get_system_uptime(self):
        result = self.ssh.execute_command("uptime -p")
        return result['stdout'].strip() if result['success'] else None
