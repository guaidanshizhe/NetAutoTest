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
│   └── linux_adapter.py   # Linux适配器
├── actions/               # Action Word定义
│   ├── linux_actions.py   # Linux操作AW
│   └── verify_actions.py  # 验证类AW
├── testcases/            # 测试用例
│   └── linux_test_example.yaml
├── utils/                # 工具类
│   ├── logger.py         # 日志工具
│   └── ssh_client.py     # SSH客户端
├── logs/                 # 日志目录
├── reports/              # 测试报告
├── main.py               # 主程序
└── requirements.txt      # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `config/env_config.yaml`，配置测试服务器信息：

```yaml
environments:
  test_env:
    linux_servers:
      - name: server1
        ip: 192.168.1.100
        port: 22
        username: root
        password: your_password
```

### 3. 运行测试

```bash
python main.py
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
  id: TC_LINUX_001
  name: Linux系统监控测试
  category: 操作系统
  
  steps:
    - action: 检查进程存在
      params:
        server: server1
        process_name: sshd
    
    - action: 获取CPU使用率
      params:
        server: server1
    
    - action: 验证小于
      params:
        actual: ${last_result}
        expected: 90
        message: CPU使用率应小于90%
```

## 变量使用

- `${last_result}`: 上一步的执行结果
- `${变量名}`: 自定义变量（在context中）

## 下一步扩展

1. 添加数据库适配器和AW
2. 添加网络工具适配器（iperf、ping）
3. 添加网络设备适配器
4. 添加业务接口适配器
5. 集成pytest和Allure报告
6. 添加Web管理界面

## 注意事项

- 首次运行前请确保SSH连接正常
- 日志文件保存在 `logs/` 目录
- 测试用例放在 `testcases/` 目录下
