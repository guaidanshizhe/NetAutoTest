import yaml
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

class CaseParser:
    
    @staticmethod
    def parse_yaml(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            logger.info(f"解析用例文件: {file_path}")
            return data
        except Exception as e:
            logger.error(f"解析用例文件失败: {e}")
            raise
    
    @staticmethod
    def validate_case(case_data):
        required_fields = ['test_case']
        for field in required_fields:
            if field not in case_data:
                raise ValueError(f"用例缺少必需字段: {field}")
        
        test_case = case_data['test_case']
        if 'steps' not in test_case:
            raise ValueError("用例缺少steps字段")
        
        return True
    
    @staticmethod
    def load_cases_from_dir(directory):
        cases = []
        dir_path = Path(directory)
        
        for yaml_file in dir_path.rglob("*.yaml"):
            try:
                case_data = CaseParser.parse_yaml(yaml_file)
                if CaseParser.validate_case(case_data):
                    cases.append({
                        'file': str(yaml_file),
                        'data': case_data
                    })
            except Exception as e:
                logger.warning(f"跳过无效用例文件 {yaml_file}: {e}")
        
        logger.info(f"从 {directory} 加载了 {len(cases)} 个用例")
        return cases
