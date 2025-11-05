"""
网络检查 Action Words
提供网络连通性检查相关的自动化操作功能

使用规范:
1. 网络检查AW不依赖服务器配置，直接指定目标地址
2. 超时时间建议根据网络环境调整，默认5秒
3. Ping检查返回详细结果，包含丢包率等信息
4. 端口检查仅验证TCP连接，不检查服务可用性

注意事项:
- 网络检查可能受防火墙影响
- ICMP可能被禁用，导致Ping失败但服务正常
- 端口检通不代表服务功能正常
"""

import subprocess
import platform
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

@ActionRegistry.register("Ping检查", category="network")
def aw_ping_check(target, count=4, timeout=5):
    """Ping检查网络连通性
    
    功能: 使用ICMP协议检查目标主机的网络连通性
    
    Args:
        target (str): 目标IP地址或域名
        count (int): ping次数，默认4次
        timeout (int): 单次ping超时时间(秒)，默认5秒
    
    Returns:
        dict: 检查结果
            - success (bool): 是否ping成功
            - packet_loss (float): 丢包率百分比
            - output (str): ping命令的完整输出
            - error (str): 错误信息(如果有)
    
    使用示例:
        - action: Ping检查
          params:
            target: 192.168.1.1
            count: 3
            timeout: 10
    
    注意事项:
        - 某些网络环境可能禁用ICMP协议
        - 防火墙可能阻止ping请求
        - 域名解析失败会导致ping失败
        - 丢包率0%表示网络连通性良好
    """
    logger.info(f"Ping检查: {target}")
    
    # 根据操作系统选择ping参数
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
    
    try:
        # 构建ping命令
        timeout_value = timeout * 1000 if platform.system().lower() == 'windows' else timeout
        cmd = ['ping', param, str(count), timeout_param, str(timeout_value), target]
        
        # 执行ping命令
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout * count + 5)
        output = result.stdout
        
        success = result.returncode == 0
        packet_loss = 100.0
        
        # 解析丢包率
        if 'loss' in output.lower() or '丢失' in output:
            import re
            loss_match = re.search(r'(\d+)%', output)
            if loss_match:
                packet_loss = float(loss_match.group(1))
        
        logger.info(f"Ping结果: {target} - {'成功' if success else '失败'}, 丢包率: {packet_loss}%")
        return {
            'success': success, 
            'packet_loss': packet_loss, 
            'output': output
        }
    
    except subprocess.TimeoutExpired:
        logger.error(f"Ping超时: {target}")
        return {
            'success': False, 
            'packet_loss': 100.0, 
            'error': 'ping命令执行超时'
        }
    except Exception as e:
        logger.error(f"Ping执行失败: {e}")
        return {
            'success': False, 
            'packet_loss': 100.0, 
            'error': str(e)
        }

@ActionRegistry.register("检查端口连通性", category="network")
def aw_check_port_connectivity(host, port, timeout=5):
    """检查TCP端口连通性
    
    功能: 尝试建立TCP连接以检查目标主机的指定端口是否可达
    
    Args:
        host (str): 目标主机IP地址或域名
        port (int): 目标端口号
        timeout (int): 连接超时时间(秒)，默认5秒
    
    Returns:
        bool: True表示端口可达，False表示不可达
    
    使用示例:
        - action: 检查端口连通性
          params:
            host: 192.168.1.100
            port: 80
            timeout: 3
    
    注意事项:
        - 仅检查TCP连接，不验证服务功能
        - 端口可达不代表服务正常工作
        - 防火墙可能阻止连接
        - 某些服务可能拒绝连接但端口开放
    """
    import socket
    logger.info(f"检查端口连通性: {host}:{port}")
    
    try:
        # 创建socket连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # 尝试连接
        result = sock.connect_ex((host, port))
        sock.close()
        
        success = result == 0
        logger.info(f"端口 {host}:{port} {'可达' if success else '不可达'}")
        return success
        
    except socket.gaierror as e:
        logger.error(f"域名解析失败 {host}: {e}")
        return False
    except Exception as e:
        logger.error(f"端口检查失败: {e}")
        return False