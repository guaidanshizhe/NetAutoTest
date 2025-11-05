"""
数据库操作 Action Words
提供数据库连接和SQL操作相关的自动化功能

使用规范:
1. 数据库AW需要指定db_name参数，对应配置文件中的数据库名称
2. 执行前确保数据库服务正常，配置信息正确
3. SQL查询建议使用只读操作，避免误修改数据
4. 大量数据查询可能耗时较长，注意超时设置

注意事项:
- 生产环境建议使用只读账号
- SQL注入风险：避免直接拼接用户输入
- 连接池：频繁操作建议复用连接
- 事务处理：修改操作需要考虑事务回滚
"""

from core.action_registry import ActionRegistry
from adapters.database_adapter import DatabaseAdapter
from utils.logger import get_logger

logger = get_logger()

# 全局数据库适配器存储
_db_adapters = {}

def get_db_adapter(db_name):
    """获取数据库适配器"""
    return _db_adapters.get(db_name)

def set_db_adapter(db_name, adapter: DatabaseAdapter):
    """设置数据库适配器"""
    _db_adapters[db_name] = adapter

@ActionRegistry.register("检查数据库连通性", category="database")
def aw_check_database_connectivity(db_name):
    """检查数据库连通性
    
    功能: 测试与指定数据库的连接是否正常
    
    Args:
        db_name (str): 数据库配置名称，需在配置文件中定义
    
    Returns:
        bool: True表示连接成功，False表示连接失败
    
    使用示例:
        - action: 检查数据库连通性
          params:
            db_name: adn_db
    
    注意事项:
        - 仅测试连接，不验证权限和数据
        - 连接失败可能由网络、认证、服务状态等原因导致
        - 建议在执行SQL操作前先检查连通性
    """
    adapter = get_db_adapter(db_name)
    if not adapter:
        logger.error(f"未找到数据库配置: {db_name}")
        return False
    
    logger.info(f"检查数据库连通性: {db_name}")
    success = adapter.connect()
    
    if success:
        logger.info(f"✓ 数据库 {db_name} 连接成功")
        # 连接成功后关闭连接
        adapter.close()
    else:
        logger.error(f"✗ 数据库 {db_name} 连接失败")
    
    return success

@ActionRegistry.register("执行SQL查询", category="database")
def aw_execute_sql_query(db_name, sql):
    """执行SQL查询
    
    功能: 在指定数据库中执行SQL语句并返回结果
    
    Args:
        db_name (str): 数据库配置名称
        sql (str): 要执行的SQL语句
    
    Returns:
        dict: 查询结果
            - success (bool): 是否执行成功
            - data (list): 查询结果数据（SELECT语句）
            - rowcount (int): 影响的行数
            - error (str): 错误信息（如果有）
    
    使用示例:
        - action: 执行SQL查询
          params:
            db_name: adn_db
            sql: "SELECT COUNT(*) FROM users WHERE status='active'"
    
    注意事项:
        - SELECT查询返回结果集，INSERT/UPDATE/DELETE返回影响行数
        - 建议使用参数化查询防止SQL注入
        - 大结果集可能消耗大量内存
        - 修改操作请谨慎使用，特别是生产环境
    
    SQL语句示例:
        - 查询: "SELECT * FROM table_name WHERE id = 1"
        - 统计: "SELECT COUNT(*) FROM table_name"
        - 插入: "INSERT INTO table_name (col1, col2) VALUES ('val1', 'val2')"
        - 更新: "UPDATE table_name SET col1='val1' WHERE id=1"
    """
    adapter = get_db_adapter(db_name)
    if not adapter:
        logger.error(f"未找到数据库配置: {db_name}")
        return {
            'success': False, 
            'error': f'数据库配置 {db_name} 不存在',
            'data': [],
            'rowcount': 0
        }
    
    logger.info(f"[{db_name}] 执行SQL: {sql}")
    result = adapter.execute_query(sql)
    
    if result['success']:
        logger.info(f"[{db_name}] SQL执行成功, 返回 {result.get('rowcount', 0)} 行")
    else:
        logger.error(f"[{db_name}] SQL执行失败: {result.get('error')}")
    
    return result