import argparse
from pathlib import Path
from utils.test_base import init_adapters, run_test_case
from core.test_runner import TestRunner
from core.case_parser import CaseParser
from utils.logger import get_logger

logger = get_logger()

def list_test_cases():
    """列出所有可用的测试用例"""
    testcases_dir = Path('testcases')
    cases = list(testcases_dir.glob('*.yaml'))
    
    logger.info("可用的测试用例:")
    for idx, case_file in enumerate(cases, 1):
        logger.info(f"  [{idx}] {case_file.name}")
    
    return cases

def main():
    parser = argparse.ArgumentParser(description='ADN网络自动化测试平台')
    parser.add_argument('-c', '--case', type=str, help='指定要执行的用例文件名')
    parser.add_argument('-l', '--list', action='store_true', help='列出所有可用的测试用例')
    parser.add_argument('-a', '--all', action='store_true', help='执行所有测试用例')
    
    args = parser.parse_args()
    
    # 列出用例
    if args.list:
        logger.info("=" * 60)
        list_test_cases()
        logger.info("=" * 60)
        return
    
    # 执行所有用例
    if args.all:
        testcases_dir = Path('testcases')
        case_files = list(testcases_dir.glob('*.yaml'))
        logger.info(f"将执行 {len(case_files)} 个测试用例")
        
        init_adapters()
        runner = TestRunner()
        
        for case_file in case_files:
            logger.info(f"\n{'='*60}")
            logger.info(f"执行用例: {case_file.name}")
            logger.info(f"{'='*60}")
            case_data = CaseParser.parse_yaml(case_file)
            runner.run_case(case_data)
        
        logger.info("\n" + "=" * 60)
        logger.info("所有测试执行完成")
        logger.info("=" * 60)
    
    # 执行指定用例
    elif args.case:
        case_file = f'testcases/{args.case}' if not args.case.startswith('testcases/') else args.case
        run_test_case(case_file, title=f"执行用例: {args.case}")
    
    # 默认执行批量检查
    else:
        run_test_case('testcases/adn_multi_nodes_check.yaml', title='ADN多节点环境批量检查')

if __name__ == '__main__':
    main()
