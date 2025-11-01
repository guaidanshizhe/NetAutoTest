"""
ADN多节点环境批量检查
执行方式: python runners/run_adn_multi_nodes_check.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.test_base import run_test_case

if __name__ == '__main__':
    run_test_case(
        case_file='testcases/adn_multi_nodes_check.yaml',
        title='ADN多节点环境批量检查'
    )
