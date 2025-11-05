"""
Setup和Teardown示例测试
执行方式: python runners/run_setup_teardown_example.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.test_base import run_test_case

if __name__ == '__main__':
    run_test_case(
        case_file='testcases/example_with_setup_teardown.yaml',
        title='Setup和Teardown示例测试'
    )