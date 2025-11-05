"""
恢复操作 Action Words
提供各种恢复操作的AW实现
"""

from core.action_registry import ActionRegistry
from core.recovery_manager import recovery_manager
from utils.logger import get_logger

logger = get_logger()

# ==================== 恢复操作AW ====================

@ActionRegistry.register("停止服务恢复", category="recovery")
def aw_stop_service_recover(server, service_name):
    """停止服务的恢复操作
    
    功能: 停止之前启动的服务
    """
    from actions.aw_linux import get_adapter
    
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[恢复] 停止服务: {service_name}")
    result = adapter.execute_shell(f"systemctl stop {service_name}")
    return result['success']

@ActionRegistry.register("删除文件恢复", category="recovery")
def aw_delete_file_recover(server, file_path):
    """删除文件的恢复操作
    
    功能: 删除之前创建的文件
    """
    from actions.aw_linux import get_adapter
    
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[恢复] 删除文件: {file_path}")
    result = adapter.execute_shell(f"rm -f {file_path}")
    return result['success']

@ActionRegistry.register("删除目录恢复", category="recovery")
def aw_delete_directory_recover(server, dir_path):
    """删除目录的恢复操作
    
    功能: 删除之前创建的目录
    """
    from actions.aw_linux import get_adapter
    
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[恢复] 删除目录: {dir_path}")
    result = adapter.execute_shell(f"rm -rf {dir_path}")
    return result['success']

@ActionRegistry.register("恢复文件内容", category="recovery")
def aw_restore_file_content_recover(server, file_path, original_content):
    """恢复文件内容
    
    功能: 将文件内容恢复到修改前的状态
    """
    from actions.aw_linux import get_adapter
    
    adapter = get_adapter(server)
    if not adapter:
        logger.error(f"未找到服务器适配器: {server}")
        return False
    
    logger.info(f"[恢复] 恢复文件内容: {file_path}")
    return adapter.write_file(file_path, original_content)

# 注册恢复方法到恢复管理器
def register_recovery_methods():
    """注册所有恢复方法"""
    recovery_manager.register_recovery_method("aw_stop_service_recover", aw_stop_service_recover)
    recovery_manager.register_recovery_method("aw_delete_file_recover", aw_delete_file_recover)
    recovery_manager.register_recovery_method("aw_delete_directory_recover", aw_delete_directory_recover)
    recovery_manager.register_recovery_method("aw_restore_file_content_recover", aw_restore_file_content_recover)

# 自动注册
register_recovery_methods()