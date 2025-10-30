import yaml
import re
from core.action_registry import ActionRegistry
from core.case_parser import CaseParser
from utils.logger import get_logger

logger = get_logger()

class TestRunner:
    
    def __init__(self):
        self.context = {}
    
    def load_config(self, config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def replace_variables(self, value):
        if isinstance(value, str):
            pattern = r'\$\{(\w+)\}'
            matches = re.findall(pattern, value)
            for var in matches:
                if var in self.context:
                    value = value.replace(f'${{{var}}}', str(self.context[var]))
        return value
    
    def execute_step(self, step):
        action_name = step.get('action')
        params = step.get('params', {})
        
        params = {k: self.replace_variables(v) for k, v in params.items()}
        
        action_info = ActionRegistry.get_action(action_name)
        if not action_info:
            logger.error(f"未找到Action Word: {action_name}")
            return None
        
        logger.info(f"执行步骤: {action_name}")
        try:
            func = action_info['function']
            result = func(**params)
            self.context['last_result'] = result
            return result
        except Exception as e:
            logger.error(f"步骤执行失败: {action_name}, 错误: {e}")
            self.context['last_result'] = None
            return None
    
    def run_case(self, case_data):
        test_case = case_data['test_case']
        case_id = test_case.get('id', 'Unknown')
        case_name = test_case.get('name', 'Unknown')
        
        logger.info(f"开始执行用例: [{case_id}] {case_name}")
        
        failed_steps = 0
        for idx, step in enumerate(test_case['steps'], 1):
            logger.info(f"步骤 {idx}/{len(test_case['steps'])}")
            result = self.execute_step(step)
            if result is None:
                failed_steps += 1
        
        if failed_steps == 0:
            logger.info(f"✓ 用例执行成功: [{case_id}] {case_name}")
            return True
        else:
            logger.warning(f"✗ 用例执行完成但有 {failed_steps} 个步骤失败: [{case_id}] {case_name}")
            return False
