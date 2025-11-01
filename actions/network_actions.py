import subprocess
import platform
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

@ActionRegistry.register("Ping检查", category="network")
def ping_check(target, count=4, timeout=5):
    """Ping检查网络连通性
    
    Args:
        target: 目标IP或域名
        count: ping次数
        timeout: 超时时间(秒)
    
    Returns:
        dict: {success: bool, packet_loss: float, avg_time: float}
    """
    logger.info(f"Ping检查: {target}")
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    
    try:
        cmd = ['ping', param, str(count), timeout_param, str(timeout * 1000 if platform.system().lower() == 'windows' else timeout), target]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * count + 5)
        output = result.stdout
        
        success = result.returncode == 0
        packet_loss = 100.0
        avg_time = None
        
        if 'loss' in output.lower() or '丢失' in output:
            import re
            loss_match = re.search(r'(\d+)%', output)
            if loss_match:
                packet_loss = float(loss_match.group(1))
        
        logger.info(f"Ping结果: {target} - {'成功' if success else '失败'}, 丢包率: {packet_loss}%")
        return {'success': success, 'packet_loss': packet_loss, 'output': output}
    
    except Exception as e:
        logger.error(f"Ping执行失败: {e}")
        return {'success': False, 'packet_loss': 100.0, 'error': str(e)}

@ActionRegistry.register("检查端口连通性", category="network")
def check_port_connectivity(host, port, timeout=5):
    """检查TCP端口连通性
    
    Args:
        host: 目标主机
        port: 目标端口
        timeout: 超时时间(秒)
    
    Returns:
        bool: 端口是否可达
    """
    import socket
    logger.info(f"检查端口连通性: {host}:{port}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        success = result == 0
        logger.info(f"端口 {host}:{port} {'可达' if success else '不可达'}")
        return success
    except Exception as e:
        logger.error(f"端口检查失败: {e}")
        return False
