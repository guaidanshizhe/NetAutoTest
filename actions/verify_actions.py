from core.action_registry import ActionRegistry
from utils.logger import get_logger

logger = get_logger()

@ActionRegistry.register("验证相等", category="verify")
def verify_equal(actual, expected, message=""):
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
def verify_not_equal(actual, expected, message=""):
    result = actual != expected
    log_msg = f"验证不相等: 实际={actual}, 期望={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    return result

@ActionRegistry.register("验证包含", category="verify")
def verify_contains(actual, expected, message=""):
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
def verify_not_contains(actual, expected, message=""):
    result = expected not in str(actual)
    log_msg = f"验证不包含: 实际={actual}, 期望不包含={expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    return result

@ActionRegistry.register("验证大于", category="verify")
def verify_greater_than(actual, expected, message=""):
    result = float(actual) > float(expected)
    log_msg = f"验证大于: 实际={actual}, 期望>{expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    return result

@ActionRegistry.register("验证小于", category="verify")
def verify_less_than(actual, expected, message=""):
    result = float(actual) < float(expected)
    log_msg = f"验证小于: 实际={actual}, 期望<{expected}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    return result

@ActionRegistry.register("验证为真", category="verify")
def verify_true(actual, message=""):
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
def verify_false(actual, message=""):
    result = not bool(actual)
    log_msg = f"验证为假: 实际={actual}"
    if message:
        log_msg += f", 消息={message}"
    
    if result:
        logger.info(f"✓ {log_msg}")
    else:
        logger.error(f"✗ {log_msg}")
    return result
