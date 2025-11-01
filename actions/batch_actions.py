import yaml
from pathlib import Path
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

_config_cache = None

def load_config():
    global _config_cache
    if not _config_cache:
        config_file = Path(__file__).parent.parent / "config" / "env_config.yaml"
        with open(config_file, 'r', encoding='utf-8') as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache

@ActionRegistry.register("批量检查ADN节点", category="batch")
def batch_check_adn_nodes():
    """批量检查所有ADN节点
    
    Returns:
        list: 所有节点的检查结果
    """
    from actions.network_actions import ping_check, check_port_connectivity
    from actions.report_actions import record_check_item
    
    config = load_config()
    nodes = config['environments']['test_env'].get('adn_nodes', [])
    
    logger.info(f"开始批量检查 {len(nodes)} 个ADN节点")
    
    results = []
    for node in nodes:
        node_name = node['name']
        node_ip = node['ip']
        
        logger.info(f"{'='*50}")
        logger.info(f"检查节点: {node_name} ({node_ip})")
        logger.info(f"{'='*50}")
        
        node_result = {
            'node_name': node_name,
            'node_ip': node_ip,
            'checks': []
        }
        
        # Ping检查
        ping_result = ping_check(node_ip, count=4, timeout=5)
        node_result['checks'].append({
            'type': 'ping',
            'success': ping_result['success'],
            'packet_loss': ping_result.get('packet_loss', 100)
        })
        
        # SSH端口检查
        ssh_result = check_port_connectivity(node_ip, node['ssh_port'], timeout=5)
        node_result['checks'].append({
            'type': 'ssh_port',
            'success': ssh_result
        })
        
        # 统计结果
        all_success = all(check['success'] for check in node_result['checks'])
        node_result['overall_status'] = 'success' if all_success else 'failed'
        
        status_icon = "✓" if all_success else "✗"
        logger.info(f"{status_icon} 节点 {node_name} 检查{'通过' if all_success else '失败'}")
        
        results.append(node_result)
    
    logger.info(f"{'='*50}")
    logger.info(f"批量检查完成，共检查 {len(nodes)} 个节点")
    success_count = sum(1 for r in results if r['overall_status'] == 'success')
    logger.info(f"成功: {success_count}, 失败: {len(nodes) - success_count}")
    
    return results
