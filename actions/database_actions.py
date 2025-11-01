from core.action_registry import ActionRegistry
from adapters.database_adapter import DatabaseAdapter
from utils.logger import get_logger

logger = get_logger()

_db_adapters = {}

def get_db_adapter(db_name):
    return _db_adapters.get(db_name)

def set_db_adapter(db_name, adapter: DatabaseAdapter):
    _db_adapters[db_name] = adapter

@ActionRegistry.register("检查数据库连通性", category="database")
def check_database_connectivity(db_name):
    """检查数据库连通性
    
    Args:
        db_name: 数据库配置名称
    
    Returns:
        bool: 是否连接成功
    """
    adapter = get_db_adapter(db_name)
    if not adapter:
        logger.error(f"未找到数据库配置: {db_name}")
        return False
    
    logger.info(f"检查数据库连通性: {db_name}")
    success = adapter.connect()
    
    if success:
        logger.info(f"✓ 数据库 {db_name} 连接成功")
    else:
        logger.error(f"✗ 数据库 {db_name} 连接失败")
    
    return success

@ActionRegistry.register("执行SQL查询", category="database")
def execute_sql_query(db_name, sql):
    """执行SQL查询
    
    Args:
        db_name: 数据库配置名称
        sql: SQL语句
    
    Returns:
        dict: 查询结果
    """
    adapter = get_db_adapter(db_name)
    if not adapter:
        logger.error(f"未找到数据库配置: {db_name}")
        return None
    
    logger.info(f"[{db_name}] 执行SQL: {sql}")
    result = adapter.execute_query(sql)
    
    if result['success']:
        logger.info(f"[{db_name}] SQL执行成功, 返回 {result.get('rowcount', 0)} 行")
    else:
        logger.error(f"[{db_name}] SQL执行失败: {result.get('error')}")
    
    return result
