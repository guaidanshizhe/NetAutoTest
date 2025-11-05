"""
验证断言 Action Words
提供各种数据验证和断言功能

使用规范:
1. 验证AW用于检查测试结果是否符合预期
2. 所有验证失败时会记录错误日志，但不会中断测试执行
3. message参数用于提供更清晰的错误描述
4. 支持数值、字符串、布尔值等多种数据类型验证

注意事项:
- 数值比较会自动进行类型转换
- 字符串比较区分大小写
- 包含检查会将实际值转换为字符串进行匹配
"""

from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

# ==================== 相等性验证 ====================

@ActionRegistry.register("验证相等", category="verify")
def aw_verify_equal(actual, expected, message=""):
    """验证两个值相等
    
    功能: 检查实际值是否等于期望值
    
    Args:
        actual: 实际值，可以是任意类型
        expected: 期望值，应与实际值类型匹配
        message (str): 自定义错误消息，用于失败时的详细描述
    
    Returns:
        bool: True表示相等，False表示不相等
    
    使用示例:
        - action: 验证相等
          params:
            actual: ${last_result}
            expected: "success"
            message: "操作状态应该为成功"
    
    注意事项:
        - 使用Python的==操作符进行比较
        - 不同类型的值比较可能返回False
        - 字符串比较区分大小写
    """
    result = actual == expected
    log_msg = f"验证相等: 实际={actual}, 期望={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result

@ActionRegistry.register("验证不相等", category="verify")
def aw_verify_not_equal(actual, expected, message=""):
    """验证两个值不相等
    
    功能: 检查实际值是否不等于期望值
    
    Args:
        actual: 实际值
        expected: 不期望的值
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示不相等，False表示相等
    
    使用示例:
        - action: 验证不相等
          params:
            actual: ${last_result}
            expected: "error"
            message: "操作状态不应该为错误"
    """
    result = actual != expected
    log_msg = f"验证不相等: 实际={actual}, 期望不等于={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result

# ==================== 包含性验证 ====================

@ActionRegistry.register("验证包含", category="verify")
def aw_verify_contains(actual, expected, message=""):
    """验证实际值包含期望值
    
    功能: 检查实际值中是否包含期望的子字符串
    
    Args:
        actual: 实际值，会被转换为字符串进行检查
        expected: 期望包含的子字符串
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示包含，False表示不包含
    
    使用示例:
        - action: 验证包含
          params:
            actual: ${last_result}
            expected: "nginx"
            message: "进程列表应该包含nginx"
    
    注意事项:
        - 实际值会被转换为字符串进行匹配
        - 区分大小写
        - 支持正则表达式模式匹配
    """
    result = expected in str(actual)
    log_msg = f"验证包含: 实际={actual}, 期望包含={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result

@ActionRegistry.register("验证不包含", category="verify")
def aw_verify_not_contains(actual, expected, message=""):
    """验证实际值不包含期望值
    
    功能: 检查实际值中是否不包含指定的子字符串
    
    Args:
        actual: 实际值，会被转换为字符串进行检查
        expected: 不期望包含的子字符串
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示不包含，False表示包含
    
    使用示例:
        - action: 验证不包含
          params:
            actual: ${last_result}
            expected: "error"
            message: "输出不应该包含错误信息"
    """
    result = expected not in str(actual)
    log_msg = f"验证不包含: 实际={actual}, 期望不包含={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result

# ==================== 数值比较验证 ====================

@ActionRegistry.register("验证大于", category="verify")
def aw_verify_greater_than(actual, expected, message=""):
    """验证实际值大于期望值
    
    功能: 检查实际值是否大于期望值（数值比较）
    
    Args:
        actual: 实际值，会被转换为浮点数进行比较
        expected: 期望的最小值（不包含）
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示大于，False表示小于等于
    
    使用示例:
        - action: 验证大于
          params:
            actual: ${last_result}
            expected: 0
            message: "进程数量应该大于0"
    
    注意事项:
        - 会自动将值转换为float类型进行比较
        - 非数值类型可能导致转换错误
    """
    try:
        result = float(actual) > float(expected)
        log_msg = f"验证大于: 实际={actual}, 期望>{expected}"
        if message:
            log_msg += f", 消息={message}"
        
        if result:
            logger.info(f"✓ {log_msg}")
        else:
            logger.error(f"✗ {log_msg}")
        
        return result
    except (ValueError, TypeError) as e:
        logger.error(f"✗ 数值转换失败: {e}")
        return False

@ActionRegistry.register("验证小于", category="verify")
def aw_verify_less_than(actual, expected, message=""):
    """验证实际值小于期望值
    
    功能: 检查实际值是否小于期望值（数值比较）
    
    Args:
        actual: 实际值，会被转换为浮点数进行比较
        expected: 期望的最大值（不包含）
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示小于，False表示大于等于
    
    使用示例:
        - action: 验证小于
          params:
            actual: ${last_result}
            expected: 90
            message: "CPU使用率应该小于90%"
    """
    try:
        result = float(actual) < float(expected)
        log_msg = f"验证小于: 实际={actual}, 期望<{expected}"
        if message:
            log_msg += f", 消息={message}"
        
        if result:
            logger.info(f"✓ {log_msg}")
        else:
            logger.error(f"✗ {log_msg}")
        
        return result
    except (ValueError, TypeError) as e:
        logger.error(f"✗ 数值转换失败: {e}")
        return False

# ==================== 布尔值验证 ====================

@ActionRegistry.register("验证为真", category="verify")
def aw_verify_true(actual, message=""):
    """验证值为真
    
    功能: 检查实际值是否为真值（True、非零数字、非空字符串等）
    
    Args:
        actual: 实际值，会被转换为布尔值进行判断
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示为真，False表示为假
    
    使用示例:
        - action: 验证为真
          params:
            actual: ${last_result}
            message: "端口应该是可达的"
    
    注意事项:
        - Python的真值判断规则：
          * False、None、0、空字符串、空列表等为假
          * 其他值为真
    """
    result = bool(actual)
    log_msg = f"验证为真: 实际={actual}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result

@ActionRegistry.register("验证为假", category="verify")
def aw_verify_false(actual, message=""):
    """验证值为假
    
    功能: 检查实际值是否为假值（False、0、空字符串等）
    
    Args:
        actual: 实际值，会被转换为布尔值进行判断
        message (str): 自定义错误消息
    
    Returns:
        bool: True表示为假，False表示为真
    
    使用示例:
        - action: 验证为假
          params:
            actual: ${last_result}
            message: "错误标志应该为假"
    """
    result = not bool(actual)
    log_msg = f"验证为假: 实际={actual}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    
    return result