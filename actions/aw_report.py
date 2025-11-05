"""
报告生成 Action Words
提供测试报告生成和记录相关的自动化功能

使用规范:
1. 报告AW用于记录测试过程和生成最终报告
2. 记录检查项用于收集测试步骤的执行结果
3. 生成报告会创建JSON格式的结构化报告文件
4. 报告文件自动添加时间戳，避免覆盖

注意事项:
- 报告文件保存在reports目录下
- JSON格式便于后续处理和分析
- 建议在关键步骤后记录检查项
- 报告内容支持中文，使用UTF-8编码
"""

import json
from datetime import datetime
from pathlib import Path
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

@ActionRegistry.register("记录检查项", category="report")
def aw_record_check_item(item_name, status, details=""):
    """记录检查项结果
    
    功能: 记录单个检查项的执行结果，用于后续报告生成
    
    Args:
        item_name (str): 检查项名称，简短描述检查内容
        status (str): 检查状态，建议使用 "success"、"failed"、"warning"
        details (str): 详细信息，可选，提供更多上下文信息
    
    Returns:
        dict: 检查项记录
            - item (str): 检查项名称
            - status (str): 检查状态
            - details (str): 详细信息
            - timestamp (str): 记录时间戳
    
    使用示例:
        - action: 记录检查项
          params:
            item_name: "服务器连通性检查"
            status: "success"
            details: "SSH端口22连接正常"
    
    状态值建议:
        - "success": 检查通过
        - "failed": 检查失败
        - "warning": 检查有警告
        - "skipped": 检查被跳过
        - "unknown": 状态未知
    
    注意事项:
        - 记录的信息会在日志中显示
        - 可以与生成报告AW配合使用
        - 时间戳使用本地时间格式
    """
    record = {
        'item': item_name,
        'status': status,
        'details': details,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 根据状态选择合适的日志级别和图标
    status_icons = {
        'success': '✓',
        'failed': '✗',
        'warning': '⚠',
        'skipped': '○',
        'unknown': '?'
    }
    
    icon = status_icons.get(status.lower(), '•')
    logger.info(f"{icon} 检查项: {item_name} - {status}")
    
    if details:
        logger.debug(f"详细信息: {details}")
    
    return record

@ActionRegistry.register("生成检查报告", category="report")
def aw_generate_check_report(report_name, check_results):
    """生成检查报告
    
    功能: 将检查结果生成JSON格式的报告文件
    
    Args:
        report_name (str): 报告名称，用作文件名前缀
        check_results: 检查结果数据，可以是字典、列表或其他可序列化对象
    
    Returns:
        str: 报告文件的完整路径
    
    使用示例:
        - action: 生成检查报告
          params:
            report_name: "adn_health_check"
            check_results: ${last_result}
    
    报告文件格式:
        - 文件名: {report_name}_{YYYYMMDD_HHMMSS}.json
        - 位置: reports/ 目录下
        - 编码: UTF-8
        - 格式: JSON
    
    报告内容结构:
        {
            "report_name": "报告名称",
            "timestamp": "生成时间",
            "results": "检查结果数据"
        }
    
    注意事项:
        - 报告目录不存在时会自动创建
        - 文件名包含时间戳，避免覆盖
        - 大量数据可能导致文件较大
        - 确保check_results可以JSON序列化
    """
    logger.info(f"生成检查报告: {report_name}")
    
    # 确保reports目录存在
    report_dir = Path(__file__).parent.parent / "reports"
    report_dir.mkdir(exist_ok=True)
    
    # 生成带时间戳的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"{report_name}_{timestamp}.json"
    
    # 构建报告数据
    report_data = {
        'report_name': report_name,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'results': check_results
    }
    
    try:
        # 写入JSON文件
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ 报告已生成: {report_file}")
        return str(report_file)
        
    except Exception as e:
        logger.error(f"✗ 报告生成失败: {e}")
        return None