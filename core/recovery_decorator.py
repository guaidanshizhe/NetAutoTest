"""
恢复装饰器
用于标记需要恢复的AW方法
"""

from functools import wraps
from core.recovery_manager import recovery_manager
from utils.logger import get_logger

logger = get_logger()

def keyword_recover(recovery_method_name):
    """恢复装饰器
    
    Args:
        recovery_method_name: 对应的恢复方法名
    
    使用示例:
        @keyword_recover("aw_stop_service_recover")
        def aw_start_service(server, service_name):
            # 启动服务的逻辑
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 执行原方法
            result = func(*args, **kwargs)
            
            # 如果执行成功，将恢复信息入栈
            if result is not None and result is not False:
                # 构建参数字典（包含位置参数和关键字参数）
                import inspect
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                
                recovery_manager.push_recovery(
                    method_name=func.__name__,
                    params=dict(bound_args.arguments),
                    recovery_method_name=recovery_method_name
                )
                
                logger.debug(f"AW执行成功，恢复信息已入栈: {func.__name__}")
            
            return result
        return wrapper
    return decorator