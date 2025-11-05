"""
简化的测试运行器
"""
import yaml
import re
from utils.logger import get_logger

logger = get_logger()

class TestRunner:
    def __init__(self):
        self.context = {}  # 存储变量
        self.actions = {}  # 存储所有AW
    
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
        return value
    
    def execute_step(self, step):
        """执行单个步骤"""
        action_name = step.get('action')
        params = step.get('params', {})
        
        # 替换参数中的变量
        params = {k: self.replace_variables(v) for k, v in params.items()}
        
        if action_name not in self.actions:
            logger.error(f"未找到AW: {action_name}")
            return None
        
        logger.info(f"执行: {action_name}")
        try:
            func = self.actions[action_name]
            result = func(**params)
            self.context['last_result'] = result
            return result
        except Exception as e:
            logger.error(f"执行失败: {action_name}, 错误: {e}")
            return None
    
    def run_case(self, case_file):
        """运行测试用例"""
        with open(case_file, 'r', encoding='utf-8') as f:
            case_data = yaml.safe_load(f)
        
        test_case = case_data['test_case']
        case_name = test_case.get('name', 'Unknown')
        
        logger.info(f"开始执行用例: {case_name}")
        logger.info("=" * 50)
        
        failed_count = 0
        steps = test_case.get('steps', [])
        
        for idx, step in enumerate(steps, 1):
            logger.info(f"步骤 {idx}/{len(steps)}")
            result = self.execute_step(step)
            if result is None:
                failed_count += 1
        
        logger.info("=" * 50)
        if failed_count == 0:
            logger.info(f"✓ 用例执行成功: {case_name}")
        else:
            logger.warning(f"✗ 用例执行完成，{failed_count} 个步骤失败")
        
        return failed_count == 0