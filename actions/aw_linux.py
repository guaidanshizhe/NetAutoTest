"""
Linux操作系统 Action Words
提供Linux系统相关的自动化操作功能

使用规范:
1. 所有AW都需要指定server参数，对应配置文件中的服务器名称
2. 执行前确保SSH连接正常，服务器在配置文件中已定义
3. 文件路径使用绝对路径，避免相对路径问题
4. 进程名称支持模糊匹配，会使用grep进行搜索
5. 系统资源监控AW返回数值类型，可用于后续验证

注意事项:
- 需要相应的系统权限执行某些操作（如杀死进程）
- 文件操作会覆盖原文件内容，请谨慎使用
- 系统监控数据可能因系统负载有所波动
"""

from core.action_registry import ActionRegistry
from core.recovery_decorator import keyword_recover
from adapters.linux_adapter import LinuxAdapter
from utils.logger import get_logger

logger = get_logger()

# 全局适配器存储
_adapters = {}

def get_adapter(server_name) -> LinuxAdapter:
    """获取Linux适配器"""
    return _adapters.get(server_name)

def set_adapter(server_name, adapter: LinuxAdapter):
    """设置Linux适配器"""
    _adapters[server_name] = adapter

# ==================== 命令执行类 ====================

@ActionRegistry.register("执行Shell命令", category="linux")
def aw_execute_shell_command(server, command, timeout=30):
    """执行Shell命令
    
    功能: 在指定Linux服务器上执行Shell命令
    
    Args:
        server (str): 服务器名称，需在配置文件中定义
        command (str): 要执行的Shell命令
        timeout (int): 命令执行超时时间，默认30秒
    
    Returns:
        dict: 执行结果
            - exit_code (int): 命令退出码，0表示成功
            - stdout (str): 标准输出内容
            - stderr (str): 错误输出内容
            - success (bool): 是否执行成功
    
    使用示例:
        - action: 执行Shell命令
          params:
            server: server1
            command: "ls -la /home"
            timeout: 10
    
    注意事项:
        - 命令中包含特殊字符时需要适当转义
        - 长时间运行的命令可能会超时
        - 交互式命令不适用此AW
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return {'exit_code': -1, 'stdout': '', 'stderr': '服务器未配置', 'success': False}
    
    logger.info(f"[{server}] 执行命令: {command}")
    result = adapter.execute_shell(command, timeout)
    logger.info(f"[{server}] 命令执行完成, 退出码: {result['exit_code']}")
    return result

# ==================== 进程管理类 ====================

@ActionRegistry.register("检查进程存在", category="linux")
def aw_check_process_exists(server, process_name):
    """检查进程是否存在
    
    功能: 检查指定名称的进程是否在系统中运行
    
    Args:
        server (str): 服务器名称
        process_name (str): 进程名称，支持模糊匹配
    
    Returns:
        bool: True表示进程存在，False表示不存在
    
    使用示例:
        - action: 检查进程存在
          params:
            server: server1
            process_name: nginx
    
    注意事项:
        - 使用grep进行模糊匹配，可能匹配到相关进程
        - 进程名称区分大小写
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[{server}] 检查进程: {process_name}")
    exists = adapter.check_process_exists(process_name)
    logger.info(f"[{server}] 进程 {process_name} {'存在' if exists else '不存在'}")
    return exists

@ActionRegistry.register("获取进程数量", category="linux")
def aw_get_process_count(server, process_name):
    """获取进程数量
    
    功能: 统计指定名称的进程数量
    
    Args:
        server (str): 服务器名称
        process_name (str): 进程名称
    
    Returns:
        int: 进程数量，0表示没有找到进程
    
    使用示例:
        - action: 获取进程数量
          params:
            server: server1
            process_name: java
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return 0
    
    logger.info(f"[{server}] 获取进程数量: {process_name}")
    count = adapter.get_process_count(process_name)
    logger.info(f"[{server}] 进程 {process_name} 数量: {count}")
    return count

@ActionRegistry.register("杀死进程", category="linux")
def aw_kill_process(server, process_name, signal=15):
    """杀死进程
    
    功能: 向指定进程发送信号以终止进程
    
    Args:
        server (str): 服务器名称
        process_name (str): 进程名称
        signal (int): 信号量，默认15(SIGTERM)，9为强制杀死(SIGKILL)
    
    Returns:
        bool: True表示命令执行成功，False表示失败
    
    使用示例:
        - action: 杀死进程
          params:
            server: server1
            process_name: nginx
            signal: 15
    
    注意事项:
        - 需要足够的权限杀死进程
        - signal=9为强制杀死，可能导致数据丢失
        - 系统关键进程请谨慎操作
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[{server}] 杀死进程: {process_name}, 信号: {signal}")
    success = adapter.kill_process(process_name, signal)
    logger.info(f"[{server}] 杀死进程 {'成功' if success else '失败'}")
    return success

# ==================== 文件操作类 ====================

@ActionRegistry.register("读取文件", category="linux")
def aw_read_file(server, file_path):
    """读取文件内容
    
    功能: 读取远程服务器上指定文件的内容
    
    Args:
        server (str): 服务器名称
        file_path (str): 文件绝对路径
    
    Returns:
        str: 文件内容，失败时返回None
    
    使用示例:
        - action: 读取文件
          params:
            server: server1
            file_path: /etc/hosts
    
    注意事项:
        - 需要对文件有读取权限
        - 大文件读取可能耗时较长
        - 二进制文件可能显示乱码
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return None
    
    logger.info(f"[{server}] 读取文件: {file_path}")
    content = adapter.read_file(file_path)
    logger.info(f"[{server}] 文件读取{'成功' if content is not None else '失败'}")
    return content

@ActionRegistry.register("写入文件", category="linux")
@keyword_recover("aw_delete_file_recover")
def aw_write_file(server, file_path, content):
    """写入文件
    
    功能: 向远程服务器的指定文件写入内容
    
    Args:
        server (str): 服务器名称
        file_path (str): 文件绝对路径
        content (str): 要写入的内容
    
    Returns:
        bool: True表示写入成功，False表示失败
    
    使用示例:
        - action: 写入文件
          params:
            server: server1
            file_path: /tmp/test.txt
            content: "Hello World"
    
    注意事项:
        - 会覆盖原文件内容
        - 需要对目录有写入权限
        - 内容中的特殊字符会被自动转义
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[{server}] 写入文件: {file_path}")
    success = adapter.write_file(file_path, content)
    logger.info(f"[{server}] 文件写入{'成功' if success else '失败'}")
    return success

@ActionRegistry.register("检查文件存在", category="linux")
def aw_check_file_exists(server, file_path):
    """检查文件是否存在
    
    功能: 检查远程服务器上指定路径的文件是否存在
    
    Args:
        server (str): 服务器名称
        file_path (str): 文件绝对路径
    
    Returns:
        bool: True表示文件存在，False表示不存在
    
    使用示例:
        - action: 检查文件存在
          params:
            server: server1
            file_path: /etc/passwd
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[{server}] 检查文件: {file_path}")
    exists = adapter.file_exists(file_path)
    logger.info(f"[{server}] 文件 {'存在' if exists else '不存在'}")
    return exists

# ==================== 系统监控类 ====================

@ActionRegistry.register("获取CPU使用率", category="linux")
def aw_get_cpu_usage(server):
    """获取CPU使用率
    
    功能: 获取系统当前CPU使用率
    
    Args:
        server (str): 服务器名称
    
    Returns:
        float: CPU使用率百分比，失败时返回None
    
    使用示例:
        - action: 获取CPU使用率
          params:
            server: server1
    
    注意事项:
        - 返回值为瞬时使用率，可能有波动
        - 不同系统的top命令输出格式可能不同
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return None
    
    logger.info(f"[{server}] 获取CPU使用率")
    usage = adapter.get_cpu_usage()
    logger.info(f"[{server}] CPU使用率: {usage}%")
    return usage

@ActionRegistry.register("获取内存使用率", category="linux")
def aw_get_memory_usage(server):
    """获取内存使用率
    
    功能: 获取系统当前内存使用率
    
    Args:
        server (str): 服务器名称
    
    Returns:
        float: 内存使用率百分比，失败时返回None
    
    使用示例:
        - action: 获取内存使用率
          params:
            server: server1
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return None
    
    logger.info(f"[{server}] 获取内存使用率")
    usage = adapter.get_memory_usage()
    logger.info(f"[{server}] 内存使用率: {usage}%")
    return usage

@ActionRegistry.register("获取磁盘使用率", category="linux")
def aw_get_disk_usage(server, path="/"):
    """获取磁盘使用率
    
    功能: 获取指定路径的磁盘使用率
    
    Args:
        server (str): 服务器名称
        path (str): 挂载点路径，默认为根目录"/"
    
    Returns:
        float: 磁盘使用率百分比，失败时返回None
    
    使用示例:
        - action: 获取磁盘使用率
          params:
            server: server1
            path: /home
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return None
    
    logger.info(f"[{server}] 获取磁盘使用率: {path}")
    usage = adapter.get_disk_usage(path)
    logger.info(f"[{server}] 磁盘使用率: {usage}%")
    return usage

@ActionRegistry.register("检查端口监听", category="linux")
def aw_check_port_listening(server, port):
    """检查端口是否监听
    
    功能: 检查指定端口是否在服务器上处于监听状态
    
    Args:
        server (str): 服务器名称
        port (int): 端口号
    
    Returns:
        bool: True表示端口正在监听，False表示未监听
    
    使用示例:
        - action: 检查端口监听
          params:
            server: server1
            port: 80
    
    注意事项:
        - 只检查TCP端口
        - 需要netstat命令支持
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[{server}] 检查端口: {port}")
    listening = adapter.check_port_listening(port)
    logger.info(f"[{server}] 端口 {port} {'正在监听' if listening else '未监听'}")
    return listening

@ActionRegistry.register("获取系统运行时间", category="linux")
def aw_get_system_uptime(server):
    """获取系统运行时间
    
    功能: 获取系统从启动到现在的运行时间
    
    Args:
        server (str): 服务器名称
    
    Returns:
        str: 系统运行时间描述，失败时返回None
    
    使用示例:
        - action: 获取系统运行时间
          params:
            server: server1
    
    注意事项:
        - 返回格式如"up 2 days, 3 hours, 45 minutes"
        - 需要uptime命令支持
    """
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return None
    
    logger.info(f"[{server}] 获取系统运行时间")
    uptime = adapter.get_system_uptime()
    logger.info(f"[{server}] 系统运行时间: {uptime}")
    return uptime