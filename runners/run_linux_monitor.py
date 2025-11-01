"""
Linux系统资源监控
执行方式: python runners/run_linux_monitor.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.test_base import run_test_case

if __name__ == '__main__':
    run_test_case(
        case_file='testcases/example_linux_monitor.yaml',
        title='Linux系统资源监控'
    )
