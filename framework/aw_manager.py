"""
AW管理器 - 负责AW的注册、管理和调用
"""
import inspect
from typing import Dict, Callable, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class AWManager:
    """AW管理器"""
    
    def __init__(self):
        self._aws: Dict[str, Callable] = {}
        self._aw_docs: Dict[str, str] = {}
    
    def register_aw(self, name: str, func: Callable, doc: str = None):
        """注册AW"""
        self._aws[name] = func
        self._aw_docs[name] = doc or func.__doc__ or "无描述"
        logger.info(f"注册AW: {name}")
    
    def call_aw(self, name: str, **kwargs) -> Any:
        """调用AW"""
        if name not in self._aws:
            raise ValueError(f"AW '{name}' 未注册")
        
        logger.info(f"调用AW: {name}, 参数: {kwargs}")
        try:
            result = self._aws[name](**kwargs)
            logger.info(f"AW执行成功: {name}")
            return result
        except Exception as e:
            logger.error(f"AW执行失败: {name}, 错误: {str(e)}")
            raise
    
    def get_aw_list(self) -> Dict[str, str]:
        """获取所有AW列表"""
        return self._aw_docs.copy()
    
    def get_aw_doc(self, name: str) -> str:
        """获取AW文档"""
        return self._aw_docs.get(name, "AW不存在")

# 全局AW管理器实例
aw_manager = AWManager()

def aw_register(name: str, doc: str = None):
    """AW注册装饰器"""
    def decorator(func):
        aw_manager.register_aw(name, func, doc)
        return func
    return decorator