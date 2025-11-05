"""
配置管理器 - 统一管理配置加载
"""
import yaml
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load_config(self):
        """加载配置文件"""
        if self._config is None:
            config_file = Path(__file__).parent.parent / "config" / "config.yaml"
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f)
                logger.info("配置文件加载成功")
            except Exception as e:
                logger.error(f"配置文件加载失败: {e}")
                raise
        return self._config
    
    def get_server_config(self, server_name):
        """获取服务器配置"""
        config = self.load_config()
        if server_name not in config.get('servers', {}):
            raise ValueError(f"未找到服务器配置: {server_name}")
        return config['servers'][server_name]
    
    def get_database_config(self, db_name):
        """获取数据库配置"""
        config = self.load_config()
        if db_name not in config.get('databases', {}):
            raise ValueError(f"未找到数据库配置: {db_name}")
        return config['databases'][db_name]
    
    def get_config(self, section=None):
        """获取配置"""
        config = self.load_config()
        return config.get(section) if section else config

# 全局配置管理器实例
config_manager = ConfigManager()