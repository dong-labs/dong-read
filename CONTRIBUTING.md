# 贡献指南

欢迎为读咚咚 (Read) 贡献！

## 开发环境

```bash
# 克隆仓库
git clone https://github.com/gudong/read.git
cd read

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest
```

## 项目结构

```
src/read/
├── __init__.py
├── cli.py              # CLI 主入口
├── const.py            # 常量定义
├── core/               # Core Library（核心资产）
│   ├── client.py       # Python SDK
│   └── models.py       # 数据模型
├── db/                 # 数据库层
│   ├── connection.py   # 连接管理
│   ├── schema.py       # 表结构
│   └── utils.py        # CRUD 操作
├── commands/           # CLI 命令
│   ├── init.py
│   ├── add.py
│   ├── ls.py
│   ├── get.py
│   ├── delete.py
│   └── search.py
└── mcp/                # MCP Server (v0.2)
    └── server.py
```

## 核心原则

1. **Core Library 优先** - 新功能优先在 Core Library 中实现
2. **CLI 调用 Core** - CLI 命令不得直接操作数据库
3. **统一 JSON 输出** - 所有命令返回结构化 JSON
4. **保持极简** - "有疑问时，不加"

## 测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/unit/core/test_client.py

# 运行测试并生成覆盖率报告
pytest --cov=read --cov-report=html
```

## 提交规范

使用 Conventional Commits 格式：

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
test: 添加测试
refactor: 重构代码
```

## 版本规划

- [ ] v0.2 - MCP Server (Agent 原生集成)
- [ ] v0.3 - Python SDK 增强
- [ ] v0.4 - 浏览器插件

欢迎认领任务！
