# ADN自动化测试框架

## 框架概述

这是一个基于关键字驱动的自动化测试框架，专为ADN网络项目设计。框架采用AW（Action Word）模式，支持测试人员通过组合AW快速构建测试用例。

## 框架特点

- **关键字驱动**: 基于AW的测试用例编写方式
- **标准化**: 统一的用例结构和开发规范
- **可扩展**: 支持自定义AW和模块扩展
- **易维护**: 清晰的代码结构和文档
- **内网友好**: 支持离线部署和内网开发

## 项目结构

```
NetAutoTest/
├── framework/              # 框架核心
│   ├── aw_manager.py      # AW管理器
│   └── base_test.py       # 测试基类
├── actions/               # AW实现
│   └── network_aws.py     # 网络相关AW
├── testcases/            # 测试用例
│   ├── TC_TEMPLATE.py    # 用例模板
│   └── TC_ADN_001.py     # 示例用例
├── config/               # 配置文件
│   └── config.yaml       # 环境配置
├── docs/                 # 文档
│   ├── AW开发规范.md
│   ├── 测试用例开发规范.md
│   └── 测试人员使用指南.md
├── utils/                # 工具类
├── logs/                 # 日志目录
├── reports/              # 报告目录
└── run_tests.py          # 测试执行器
```

## 快速开始

### 1. 环境准备
```bash
pip install -r requirements.txt
```

### 2. 配置环境
编辑 `config/config.yaml`，配置服务器和数据库信息

### 3. 查看框架演示
```bash
python demo_run.py
```

### 4. 运行示例用例
```bash
python testcases/TC_ADN_001.py
```

### 5. 批量运行用例
```bash
python run_tests.py
```

## 开发指南

### AW开发者
1. 阅读 `docs/AW开发规范.md`
2. 参考 `actions/network_aws.py` 示例
3. 使用 `@aw_register` 装饰器注册AW

### 测试人员
1. 阅读 `docs/测试人员使用指南.md`
2. 复制 `testcases/TC_TEMPLATE.py` 创建新用例
3. 使用 `self.call_aw()` 调用AW

## 用例结构

```python
class TC_ADN_001(BaseTest):
    # 用例信息
    case_id = "TC_ADN_001"
    case_name = "ADN网络连通性测试"
    author = "张三"
    
    def setup(self):
        """测试前准备"""
        pass
    
    def test_TC_ADN_001(self):
        """测试用例主体"""
        result = self.call_aw("检查服务器连通性", server_name="adn_server")
        self.verify(result, "连通性检查失败")
    
    def teardown(self):
        """测试后清理"""
        pass
```

## 内网部署

1. 将整个项目打包
2. 在内网环境解压
3. 安装依赖包（可离线安装）
4. 修改配置文件
5. 开始使用

## 扩展开发

### 添加新的AW分类
1. 在 `actions/` 目录创建新的AW文件
2. 使用 `@aw_register` 注册AW
3. 编写AW文档和示例

### 添加新的适配器
1. 在 `utils/` 目录创建适配器
2. 在AW中调用适配器
3. 更新配置文件

## 文档说明

- `AW开发规范.md`: AW开发者必读
- `测试用例开发规范.md`: 测试用例编写规范
- `测试人员使用指南.md`: 测试人员使用手册

## 支持和反馈

- 框架问题: 联系开发团队
- AW需求: 提交需求给开发团队
- Bug反馈: 及时反馈给开发团队