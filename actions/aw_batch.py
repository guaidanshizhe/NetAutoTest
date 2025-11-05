"""
批量操作 Action Words
提供批量检查和操作相关的自动化功能

使用规范:
1. 批量AW从配置文件中读取节点列表进行批量操作
2. 支持并发执行以提高效率（未来扩展）
3. 返回结构化结果，便于后续处理和报告生成
4. 失败节点不影响其他节点的检查

注意事项:
- 批量操作可能耗时较长
- 网络问题可能导致部分节点检查失败
- 结果包含每个节点的详细检查信息
- 建议配合报告生成AW使用
"""

import yaml
from pathlib import Path
from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

# 配置缓存
_config_cache = None

def load_config():
    """加载配置文件"""
    global _config_cache
    if not _config_cache:
        config_file = Path(__file__).parent.parent / "config" / "env_config.yaml"
        with open(config_file, 'r', encoding='utf-8') as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache

@ActionRegistry.register("批量检查ADN节点", category="batch")
def aw_batch_check_adn_nodes():
    """批量检查所有ADN节点
    
    功能: 对配置文件中定义的所有ADN节点进行批量健康检查
    
    Args:
        无参数，从配置文件中读取节点列表
    
    Returns:
        list: 所有节点的检查结果列表
            每个节点结果包含:
            - node_name (str): 节点名称
            - node_ip (str): 节点IP地址
            - overall_status (str): 总体状态 "success"/"failed"
            - checks (list): 详细检查项列表
                - type (str): 检查类型 "ping"/"ssh_port"
                - success (bool): 检查是否成功
                - packet_loss (float): ping丢包率（仅ping检查）
    
    使用示例:
        - action: 批量检查ADN节点
          params: {}
    
    检查项目:
        1. Ping连通性检查 - 验证网络基础连通性
        2. SSH端口检查 - 验证SSH服务可用性
    
    注意事项:
        - 检查顺序：先ping后端口，ping失败仍会检查端口
        - 所有检查项都成功才认为节点状态为success
        - 网络问题可能导致误报，建议结合多次检查
        - 大量节点检查可能耗时较长
    
    配置要求:
        配置文件中需要定义adn_nodes节点列表:
        adn_nodes:
          - name: adn_node1
            ip: 192.168.1.100
            ssh_port: 22
    """
    # 导入网络检查函数
    from actions.aw_network import aw_ping_check, aw_check_port_connectivity
    
    # 加载配置
    config = load_config()
    nodes = config['environments']['test_env'].get('adn_nodes', [])
    
    if not nodes:
        logger.warning("配置文件中未找到ADN节点定义")
        return []
    
    logger.info(f"开始批量检查 {len(nodes)} 个ADN节点")
    
    results = []
    
    for idx, node in enumerate(nodes, 1):
        node_name = node['name']
        node_ip = node['ip']
        
        logger.info(f"{'='*50}")
        logger.info(f"检查节点 [{idx}/{len(nodes)}]: {node_name} ({node_ip})")
        logger.info(f"{'='*50}")
        
        # 初始化节点结果
        node_result = {
            'node_name': node_name,
            'node_ip': node_ip,
            'checks': []
        }
        
        # 1. Ping连通性检查
        logger.info(f"[{node_name}] 执行Ping检查...")
        ping_result = aw_ping_check(node_ip, count=4, timeout=5)
        node_result['checks'].append({
            'type': 'ping',
            'success': ping_result['success'],
            'packet_loss': ping_result.get('packet_loss', 100)
        })
        
        # 2. SSH端口连通性检查
        logger.info(f"[{node_name}] 执行SSH端口检查...")
        ssh_result = aw_check_port_connectivity(node_ip, node['ssh_port'], timeout=5)
        node_result['checks'].append({
            'type': 'ssh_port',
            'success': ssh_result
        })
        
        # 计算总体状态
        all_success = all(check['success'] for check in node_result['checks'])
        node_result['overall_status'] = 'success' if all_success else 'failed'
        
        # 记录节点检查结果
        status_icon = "✓" if all_success else "✗"
        status_text = "通过" if all_success else "失败"
        logger.info(f"{status_icon} 节点 {node_name} 检查{status_text}")
        
        # 详细结果记录
        for check in node_result['checks']:
            check_icon = "✓" if check['success'] else "✗"
            if check['type'] == 'ping':
                logger.info(f"  {check_icon} Ping检查: 丢包率 {check['packet_loss']}%")
            elif check['type'] == 'ssh_port':
                logger.info(f"  {check_icon} SSH端口检查: 端口 {node['ssh_port']}")
        
        results.append(node_result)
    
    # 统计总体结果
    logger.info(f"{'='*50}")
    logger.info("批量检查汇总")
    logger.info(f"{'='*50}")
    
    success_count = sum(1 for r in results if r['overall_status'] == 'success')
    failed_count = len(nodes) - success_count
    
    logger.info(f"总节点数: {len(nodes)}")
    logger.info(f"检查通过: {success_count}")
    logger.info(f"检查失败: {failed_count}")
    
    if failed_count > 0:
        logger.warning("以下节点检查失败:")
        for result in results:
            if result['overall_status'] == 'failed':
                failed_checks = [c['type'] for c in result['checks'] if not c['success']]
                logger.warning(f"  - {result['node_name']}: {', '.join(failed_checks)}")
    
    logger.info(f"批量检查完成")
    
    return results