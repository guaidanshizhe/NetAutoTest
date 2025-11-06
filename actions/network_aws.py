"""
网络相关AW实现
"""
import subprocess
import socket
import requests
from framework.aw_manager import aw_register
from utils.logger import get_logger

logger = get_logger(__name__)

@aw_register("检查服务器连通性", "检查指定服务器的网络连通性")
def check_server_connectivity(server_ip: str, port: int = 22, timeout: int = 5) -> bool:
    """
    检查服务器连通性
    
    Args:
        server_ip: 服务器IP地址
        port: 端口号，默认22
        timeout: 超时时间，默认5秒
    
    Returns:
        bool: 连通性状态
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((server_ip, port))
        sock.close()
        
        is_connected = result == 0
        logger.info(f"服务器 {server_ip}:{port} 连通性检查: {'成功' if is_connected else '失败'}")
        return is_connected
    except Exception as e:
        logger.error(f"连通性检查异常: {str(e)}")
        return False

@aw_register("ping服务器", "使用ping命令检查服务器可达性")
def ping_server(server_ip: str, count: int = 4) -> dict:
    """
    ping服务器
    
    Args:
        server_ip: 服务器IP地址
        count: ping次数，默认4次
    
    Returns:
        dict: ping结果统计
    """
    try:
        cmd = f"ping -n {count} {server_ip}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        output = result.stdout
        success = result.returncode == 0
        
        # 简单解析ping结果
        packet_loss = "100%" in output
        
        ping_result = {
            "success": success and not packet_loss,
            "output": output,
            "packet_loss": packet_loss
        }
        
        logger.info(f"Ping {server_ip} 结果: {'成功' if ping_result['success'] else '失败'}")
        return ping_result
    except Exception as e:
        logger.error(f"Ping执行异常: {str(e)}")
        return {"success": False, "error": str(e)}

@aw_register("检查HTTP服务", "检查HTTP服务是否正常")
def check_http_service(url: str, expected_status: int = 200, timeout: int = 10) -> dict:
    """
    检查HTTP服务
    
    Args:
        url: 服务URL
        expected_status: 期望的HTTP状态码，默认200
        timeout: 超时时间，默认10秒
    
    Returns:
        dict: 检查结果
    """
    try:
        response = requests.get(url, timeout=timeout)
        
        result = {
            "success": response.status_code == expected_status,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "content_length": len(response.content)
        }
        
        logger.info(f"HTTP服务检查 {url}: 状态码 {response.status_code}, 响应时间 {result['response_time']:.2f}秒")
        return result
    except Exception as e:
        logger.error(f"HTTP服务检查异常: {str(e)}")
        return {"success": False, "error": str(e)}

@aw_register("检查端口开放", "检查指定端口是否开放")
def check_port_open(server_ip: str, port: int, timeout: int = 5) -> bool:
    """
    检查端口开放状态
    
    Args:
        server_ip: 服务器IP
        port: 端口号
        timeout: 超时时间
    
    Returns:
        bool: 端口是否开放
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((server_ip, port))
        sock.close()
        
        is_open = result == 0
        logger.info(f"端口检查 {server_ip}:{port}: {'开放' if is_open else '关闭'}")
        return is_open
    except Exception as e:
        logger.error(f"端口检查异常: {str(e)}")
        return False