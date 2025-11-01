# ADN网络自动化测试平台

基于关键字驱动的自动化测试框架，专注于ADN网络项目的控制面和转发面业务测试。

## 项目结构

```
NetAutoTest/
├── config/                 # 配置文件
│   └── env_config.yaml    # 环境配置
├── core/                   # 核心引擎
│   ├── action_registry.py # AW注册中心
│   ├── case_parser.py     # 用例解析器
│   └── test_runner.py     # 测试运行器
├── adapters/              # 适配器层
│   ├── linux_adapter.py   # Linux适配器
│   └── database_adapter.py # 数据库适配器
├── actions/               # Action Word定义
│   ├── linux_actions.py   # Linux操作AW
│   ├── database_actions.py # 数据库AW
│   ├── network_actions.py # 网络检查AW
│   ├── batch_actions.py   # 批量操作AW
│   ├── report_actions.py  # 报告生成AW
│   └── verify_actions.py  # 验证类AW
├── testcases/            # 测试用例
│   ├── adn_multi_nodes_check.yaml
│   └── example_linux_monitor.yaml
├── runners/              # 用例执行脚本
│   ├── run_adn_multi_nodes_check.py
│   └── run_linux_monitor.py
├── utils/                # 工具类
│   ├── logger.py         # 日志工具
│   ├── ssh_client.py     # SSH客户端
│   └── test_base.py      # 测试基础模块
├── logs/                 # 日志目录
├── reports/              # 测试报告
├── test_manager.py       # 测试管理器（批量执行）
└── requirements.txt      # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `config/env_config.yaml`，配置测试服务器和数据库信息：

```yaml
environments:
  test_env:
    linux_servers:
      - name: server1
        ip: 192.168.1.100
        port: 22
        username: root
        password: your_password
    
    databases:
      - name: adn_db
        host: 192.168.1.100
        port: 3306
        username: root
        password: your_password
        database: adn
    
    adn_nodes:
      - name: adn_node1
        ip: 192.168.1.100
        ssh_port: 22
        mysql_port: 3306
```

### 3. 运行测试

**方式1：独立脚本执行（推荐）**
```bash
# ADN多节点环境检查
python runners/run_adn_multi_nodes_check.py

# Linux系统监控
python runners/run_linux_monitor.py
```

**方式2：测试管理器**
```bash
# 列出所有用例
python test_manager.py -l

# 执行指定用例
python test_manager.py -c adn_multi_nodes_check.yaml

# 执行所有用例
python test_manager.py -a

# 执行默认用例
python test_manager.py
```

## 已实现的Action Words

### Linux操作类
- **执行Shell命令**: 在远程服务器执行Shell命令
- **检查进程存在**: 检查指定进程是否存在
- **获取进程数量**: 获取指定进程的数量
- **杀死进程**: 杀死指定进程
- **读取文件**: 读取远程文件内容
- **写入文件**: 写入内容到远程文件
- **检查文件存在**: 检查文件是否存在
- **获取CPU使用率**: 获取系统CPU使用率
- **获取内存使用率**: 获取系统内存使用率
- **获取磁盘使用率**: 获取磁盘使用率
- **检查端口监听**: 检查端口是否在监听
- **获取系统运行时间**: 获取系统运行时间

### 网络检查类
- **Ping检查**: 检查网络连通性
- **检查端口连通性**: 检查TCP端口是否可达

### 数据库类
- **检查数据库连通性**: 检查数据库连接
- **执行SQL查询**: 执行SQL语句

### 批量操作类
- **批量检查ADN节点**: 批量检查所有ADN节点环境

### 报告生成类
- **记录检查项**: 记录检查项结果
- **生成检查报告**: 生成JSON格式检查报告

### 验证类
- **验证相等**: 验证两个值相等
- **验证不相等**: 验证两个值不相等
- **验证包含**: 验证实际值包含期望值
- **验证不包含**: 验证实际值不包含期望值
- **验证大于**: 验证实际值大于期望值
- **验证小于**: 验证实际值小于期望值
- **验证为真**: 验证值为真
- **验证为假**: 验证值为假

## 编写测试用例

测试用例使用YAML格式，示例：

```yaml
test_case:
  id: TC_ADN_001
  name: ADN节点环境检查
  category: 环境检查
  
  steps:
    - action: Ping检查
      params:
        target: 192.168.1.100
        count: 4
        timeout: 5
    
    - action: 检查端口连通性
      params:
        host: 192.168.1.100
        port: 22
        timeout: 5
    
    - action: 验证为真
      params:
        actual: ${last_result}
        message: SSH端口应该可达
```

## 变量使用

- `${last_result}`: 上一步的执行结果
- `${变量名}`: 自定义变量（在context中）

## 添加新用例

1. **创建YAML用例** - `testcases/your_test.yaml`
2. **创建执行脚本** - `runners/run_your_test.py`：

```python
from utils.test_base import run_test_case
from actions import linux_actions, verify_actions, network_actions, database_actions, report_actions, batch_actions

if __name__ == '__main__':
    run_test_case(
        case_file='testcases/your_test.yaml',
        title='你的测试用例标题'
    )
```

3. **运行** - `python runners/run_your_test.py`

## 下一步扩展

1. 添加网络工具适配器（iperf）
2. 添加网络设备适配器
3. 添加业务接口适配器
4. 集成pytest和Allure报告
5. 添加Web管理界面

## 注意事项

- 首次运行前请确保SSH连接正常
- 日志文件保存在 `logs/` 目录
- 测试报告保存在 `reports/` 目录
- 测试用例放在 `testcases/` 目录下
