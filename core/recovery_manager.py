"""
恢复管理器
实现基于栈的自动恢复机制
"""

from utils.logger import get_logger

logger = get_logger()

class RecoveryManager:
    """恢复管理器 - 管理恢复栈和恢复操作"""
    
    def __init__(self):
        self.recovery_stack = []  # 恢复栈
        self.recovery_methods = {}  # 恢复方法映射
    
    def clear_stack(self):
        """清空恢复栈"""
        self.recovery_stack.clear()
        logger.debug("恢复栈已清空")
    
    def push_recovery(self, method_name, params, recovery_method_name):
        """将恢复信息入栈
        
        Args:
            method_name: 原方法名
            params: 原方法参数
            recovery_method_name: 对应的恢复方法名
        """
        recovery_info = {
            'method_name': method_name,
            'params': params.copy(),
            'recovery_method_name': recovery_method_name
        }
        self.recovery_stack.append(recovery_info)
        logger.debug(f"恢复信息入栈: {method_name} -> {recovery_method_name}")
    
    def register_recovery_method(self, method_name, method_func):
        """注册恢复方法
        
        Args:
            method_name: 恢复方法名
            method_func: 恢复方法函数
        """
        self.recovery_methods[method_name] = method_func
        logger.debug(f"注册恢复方法: {method_name}")
    
    def execute_recovery(self):
        """执行恢复操作 - 从栈顶开始逐个执行"""
        if not self.recovery_stack:
            logger.info("恢复栈为空，无需恢复")
            return
        
        logger.info(f"开始执行恢复操作，共 {len(self.recovery_stack)} 个恢复项")
        
        recovery_count = 0
        while self.recovery_stack:
            recovery_info = self.recovery_stack.pop()
            recovery_method_name = recovery_info['recovery_method_name']
            params = recovery_info['params']
            
            logger.info(f"执行恢复: {recovery_method_name}")
            
            try:
                if recovery_method_name in self.recovery_methods:
                    recovery_func = self.recovery_methods[recovery_method_name]
                    recovery_func(**params)
                    recovery_count += 1
                    logger.info(f"✓ 恢复成功: {recovery_method_name}")
                else:
                    logger.warning(f"✗ 未找到恢复方法: {recovery_method_name}")
            except Exception as e:
                logger.error(f"✗ 恢复失败: {recovery_method_name}, 错误: {e}")
        
        logger.info(f"恢复操作完成，成功执行 {recovery_count} 个恢复项")

# 全局恢复管理器实例
recovery_manager = RecoveryManager()