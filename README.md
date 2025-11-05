# ADN自动化测试平台 - 精简版

## 项目结构
```
NetAutoTest/
├── config/
│   └── config.yaml          # 配置文件
├── core/
│   └── test_runner.py       # 测试运行器
├── actions/
│   └── basic_actions.py     # 基础AW实现
├── testcases/
│   └── adn_demo.yaml        # Demo测试用例
├── utils/
│   └── logger.py            # 日志工具
├── logs/                    # 日志目录
├── run_demo.py              # Demo执行器
└── requirements.txt         # 依赖包
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 修改配置
编辑 `config/config.yaml`，配置你的服务器和数据库信息。

### 3. 运行Demo
```bash
python run_demo.py
```

## Demo用例说明

这个Demo包含了ADN测试的完整流程：

1. **连通性检查** - 验证服务器和数据库可达性
2. **数据清理** - 清理指定数据库表
3. **服务重启** - 重启ADN相关Docker容器
4. **接口测试** - 调用REST API接口
5. **工具查询** - 使用rtnctl查询路由表
6. **性能测试** - 执行iperf网络打流

## 配置说明

### 服务器配置
```yaml
servers:
  adn_server:
    ip: 你的服务器IP
    username: SSH用户名
    password: SSH密码
```

### 数据库配置
```yaml
databases:
  adn_db:
    host: 数据库地址
    username: 数据库用户名
    password: 数据库密码
    database: 数据库名
```

## 扩展说明

这是一个精简版框架，包含了核心功能：
- 简单的AW注册机制
- YAML用例解析
- 变量替换 (${变量名})
- 基础日志记录

后续可以根据需要逐步添加：
- 更多AW类型
- 报告生成
- 错误处理
- 并发执行