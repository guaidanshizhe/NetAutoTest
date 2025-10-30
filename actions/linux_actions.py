from core.action_registry import ActionRegistry
from adapters.linux_adapter import LinuxAdapter
from utils.logger import get_logger

logger = get_logger()

_adapters = {}

def get_adapter(server_name) -> LinuxAdapter:
    return _adapters.get(server_name)

def set_adapter(server_name, adapter: LinuxAdapter):
    _adapters[server_name] = adapter

@ActionRegistry.register("执行Shell命令", category="linux")
def execute_shell_command(server, command, timeout=30):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 执行命令: {command}")
    result = adapter.execute_shell(command, timeout)
    logger.info(f"[{server}] 命令执行完成, 退出码: {result['exit_code']}")
    return result

@ActionRegistry.register("检查进程存在", category="linux")
def check_process_exists(server, process_name):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 检查进程: {process_name}")
    exists = adapter.check_process_exists(process_name)
    logger.info(f"[{server}] 进程 {process_name} {'存在' if exists else '不存在'}")
    return exists

@ActionRegistry.register("获取进程数量", category="linux")
def get_process_count(server, process_name):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 获取进程数量: {process_name}")
    count = adapter.get_process_count(process_name)
    logger.info(f"[{server}] 进程 {process_name} 数量: {count}")
    return count

@ActionRegistry.register("杀死进程", category="linux")
def kill_process(server, process_name, signal=15):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 杀死进程: {process_name}, 信号: {signal}")
    success = adapter.kill_process(process_name, signal)
    logger.info(f"[{server}] 杀死进程 {'成功' if success else '失败'}")
    return success

@ActionRegistry.register("读取文件", category="linux")
def read_file(server, file_path):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 读取文件: {file_path}")
    content = adapter.read_file(file_path)
    logger.info(f"[{server}] 文件读取{'成功' if content else '失败'}")
    return content

@ActionRegistry.register("写入文件", category="linux")
def write_file(server, file_path, content):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 写入文件: {file_path}")
    success = adapter.write_file(file_path, content)
    logger.info(f"[{server}] 文件写入{'成功' if success else '失败'}")
    return success

@ActionRegistry.register("检查文件存在", category="linux")
def check_file_exists(server, file_path):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 检查文件: {file_path}")
    exists = adapter.file_exists(file_path)
    logger.info(f"[{server}] 文件 {'存在' if exists else '不存在'}")
    return exists

@ActionRegistry.register("获取CPU使用率", category="linux")
def get_cpu_usage(server):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 获取CPU使用率")
    usage = adapter.get_cpu_usage()
    logger.info(f"[{server}] CPU使用率: {usage}%")
    return usage

@ActionRegistry.register("获取内存使用率", category="linux")
def get_memory_usage(server):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 获取内存使用率")
    usage = adapter.get_memory_usage()
    logger.info(f"[{server}] 内存使用率: {usage}%")
    return usage

@ActionRegistry.register("获取磁盘使用率", category="linux")
def get_disk_usage(server, path="/"):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 获取磁盘使用率: {path}")
    usage = adapter.get_disk_usage(path)
    logger.info(f"[{server}] 磁盘使用率: {usage}%")
    return usage

@ActionRegistry.register("检查端口监听", category="linux")
def check_port_listening(server, port):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 检查端口: {port}")
    listening = adapter.check_port_listening(port)
    logger.info(f"[{server}] 端口 {port} {'正在监听' if listening else '未监听'}")
    return listening

@ActionRegistry.register("获取系统运行时间", category="linux")
def get_system_uptime(server):
    adapter = get_adapter(server)
    logger.info(f"[{server}] 获取系统运行时间")
    uptime = adapter.get_system_uptime()
    logger.info(f"[{server}] 系统运行时间: {uptime}")
    return uptime
