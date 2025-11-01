import json
from datetime import datetime
from pathlib import Path
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

@ActionRegistry.register("生成检查报告", category="report")
def generate_check_report(report_name, check_results):
    """生成检查报告
    
    Args:
        report_name: 报告名称
        check_results: 检查结果字典
    
    Returns:
        str: 报告文件路径
    """
    logger.info(f"生成检查报告: {report_name}")
    
    report_dir = Path(__file__).parent.parent / "reports"
    report_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"{report_name}_{timestamp}.json"
    
    report_data = {
        'report_name': report_name,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'results': check_results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"✓ 报告已生成: {report_file}")
    return str(report_file)

@ActionRegistry.register("记录检查项", category="report")
def record_check_item(item_name, status, details=""):
    """记录检查项结果
    
    Args:
        item_name: 检查项名称
        status: 状态 (success/failed)
        details: 详细信息
    
    Returns:
        dict: 检查项记录
    """
    record = {
        'item': item_name,
        'status': status,
        'details': details,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    status_icon = "✓" if status == "success" else "✗"
    logger.info(f"{status_icon} 检查项: {item_name} - {status}")
    
    return record
