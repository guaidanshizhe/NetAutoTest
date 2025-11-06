# AW开发规范

## 概述

AW（Action Word）是自动化测试框架的核心组件，封装了具体的测试动作。本文档规范了AW的开发标准。

## AW开发原则

### 1. 单一职责
- 每个AW只负责一个明确的测试动作
- 功能边界清晰，不混合多种操作

### 2. 参数标准化
- 使用类型注解标明参数类型
- 提供默认值和参数说明
- 参数命名使用下划线风格

### 3. 返回值规范
- 简单操作返回bool或基础类型
- 复杂操作返回dict，包含详细信息
- 异常情况返回包含error字段的dict

## AW开发步骤

### 1. 创建AW文件
在 `actions/` 目录下创建分类文件，如：
- `network_aws.py` - 网络相关AW
- `database_aws.py` - 数据库相关AW
- `system_aws.py` - 系统相关AW

### 2. 编写AW函数
```python
from framework.aw_manager import aw_register
from utils.logger import get_logger

logger = get_logger(__name__)

@aw_register("AW中文名称", "AW功能描述")
def aw_function_name(param1: str, param2: int = 10) -> dict:
    """
    AW功能详细说明
    
    Args:
        param1: 参数1说明
        param2: 参数2说明，默认值10
    
    Returns:
        dict: 返回结果说明
        {
            "success": bool,  # 执行是否成功
            "data": any,      # 返回数据
            "message": str    # 结果消息
        }
    """
    try:
        # AW实现逻辑
        logger.info(f"执行AW: {param1}, {param2}")
        
        # 执行具体操作
        result = do_something(param1, param2)
        
        logger.info("AW执行成功")
        return {
            "success": True,
            "data": result,
            "message": "操作成功"
        }
    except Exception as e:
        logger.error(f"AW执行失败: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "操作失败"
        }
```

### 3. AW命名规范
- 使用中文名称注册AW，便于测试人员理解
- 函数名使用英文，遵循Python命名规范
- AW名称要准确描述功能，如"检查服务器连通性"

### 4. 参数设计规范
- 必需参数放在前面，可选参数放在后面
- 使用有意义的参数名
- 提供合理的默认值
- 复杂参数使用dict传递

### 5. 返回值设计规范
- 简单判断：返回bool
- 复杂结果：返回dict，包含success字段
- 异常处理：捕获异常，返回错误信息

## AW分类建议

### 网络类AW
- 连通性检查
- 端口扫描
- HTTP请求
- 网络配置

### 系统类AW
- 进程管理
- 文件操作
- 服务控制
- 系统信息

### 数据库类AW
- 连接数据库
- 执行SQL
- 数据验证
- 备份恢复

### 应用类AW
- 应用部署
- 配置管理
- 日志分析
- 性能监控

## 错误处理规范

### 1. 异常捕获
```python
try:
    # AW实现
    pass
except SpecificException as e:
    # 特定异常处理
    logger.error(f"特定错误: {str(e)}")
    return {"success": False, "error": str(e)}
except Exception as e:
    # 通用异常处理
    logger.error(f"未知错误: {str(e)}")
    return {"success": False, "error": str(e)}
```

### 2. 参数验证
```python
def check_server(server_ip: str, port: int = 22) -> bool:
    # 参数验证
    if not server_ip:
        raise ValueError("server_ip不能为空")
    if not (1 <= port <= 65535):
        raise ValueError("port必须在1-65535范围内")
```

## 日志规范

### 1. 日志级别
- INFO: 正常执行流程
- ERROR: 错误和异常
- DEBUG: 调试信息（开发阶段）

### 2. 日志内容
- 记录AW开始执行
- 记录关键参数
- 记录执行结果
- 记录异常信息

## 测试规范

### 1. AW单元测试
每个AW都应该有对应的单元测试：
```python
import unittest
from actions.network_aws import check_server_connectivity

class TestNetworkAWs(unittest.TestCase):
    def test_check_server_connectivity(self):
        # 测试正常情况
        result = check_server_connectivity("127.0.0.1", 22)
        self.assertIsInstance(result, bool)
        
        # 测试异常情况
        result = check_server_connectivity("invalid_ip", 22)
        self.assertFalse(result)
```

### 2. 集成测试
在实际环境中验证AW功能

## 文档规范

### 1. AW文档
每个AW文件都要包含：
- 文件说明
- AW列表和功能描述
- 使用示例

### 2. 更新记录
记录AW的版本变更和功能更新

## 代码审查

### 1. 审查要点
- 功能正确性
- 代码规范性
- 异常处理完整性
- 文档完整性

### 2. 审查流程
- 开发者自测
- 同行代码审查
- 集成测试验证

## 版本管理

### 1. AW版本
- 使用语义化版本号
- 记录变更日志
- 保持向后兼容

### 2. 废弃AW
- 标记为废弃
- 提供替代方案
- 逐步移除