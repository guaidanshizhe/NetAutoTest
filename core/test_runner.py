"""
优化的测试运行器
"""
import yaml
import re
import atexit
from utils.logger import get_logger
from utils.connection_pool import connection_pool

logger = get_logger()

class TestRunner:
    def __init__(self):
        self.context = {}  # 存储变量
        self.actions = {}  # 存储所有AW
        # 注册退出时清理连接
        atexit.register(self.cleanup)
    
    def cleanup(self):
        """清理资源"""
        connection_pool.close_all()
    
    def register_action(self, name, func):
        """注册AW"""
        self.actions[name] = func
        logger.debug(f"注册AW: {name}")
    
    def replace_variables(self, value):
        """替换变量 ${变量名}"""
        if isinstance(value, str):
            pattern = r'\$\{(\w+)\}'
            matches = re.findall(pattern, value)
            for var in matches:
                if var in self.context:
                    value = value.replace(f'${{{var}}}', str(self.context[var]))
        elif isinstance(value, dict):
            return {k: self.replace_variables(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.replace_variables(item) for item in value]
        return value
    
    def execute_step(self, step):
        """执行单个步骤"""
        action_name = step.get('action')
        params = step.get('params', {})
        
        if action_name not in self.actions:
            logger.error(f"✗ 未找到AW: {action_name}")
            return None
        
        # 替换参数中的变量
        params = self.replace_variables(params)
        
        logger.info(f"执行: {action_name}")
        try:
            func = self.actions[action_name]
            result = func(**params)
            self.context['last_result'] = result
            return result
        except Exception as e:
            logger.error(f"✗ 执行失败: {action_name}, 错误: {e}")
            return None
    
    def run_case(self, case_file):
        """运行测试用例"""
        try:
            with open(case_file, 'r', encoding='utf-8') as f:
                case_data = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"✗ 用例文件加载失败: {e}")
            return False
        
        test_case = case_data['test_case']
        case_name = test_case.get('name', 'Unknown')
        case_id = test_case.get('id', 'Unknown')
        
        logger.info("=" * 60)
        logger.info(f"开始执行用例: [{case_id}] {case_name}")
        logger.info("=" * 60)
        
        failed_count = 0
        steps = test_case.get('steps', [])
        
        if not steps:
            logger.warning("⚠ 用例中没有定义测试步骤")
            return False
        
        for idx, step in enumerate(steps, 1):
            logger.info(f"步骤 {idx}/{len(steps)}")
            result = self.execute_step(step)
            if result is None or result is False:
                failed_count += 1
        
        logger.info("=" * 60)
        if failed_count == 0:
            logger.info(f"✓ 用例执行成功: {case_name}")
        else:
            logger.warning(f"✗ 用例执行完成，{failed_count}/{len(steps)} 个步骤失败")
        logger.info("=" * 60)
        
        return failed_count == 0