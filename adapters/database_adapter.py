import pymysql
from utils.logger import get_logger

logger = get_logger()

class DatabaseAdapter:
    
    def __init__(self, host, port, username, password, database=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
                connect_timeout=10
            )
            logger.info(f"数据库连接成功: {self.username}@{self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            return False
    
    def execute_query(self, sql):
        if not self.connection:
            self.connect()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return {'success': True, 'data': result, 'rowcount': cursor.rowcount}
        except Exception as e:
            logger.error(f"SQL执行失败: {e}")
            return {'success': False, 'error': str(e)}
    
    def close(self):
        if self.connection:
            self.connection.close()
            logger.info(f"数据库连接已关闭: {self.host}")
