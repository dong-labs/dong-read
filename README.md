# 读咚咚 (Read) - 个人知识数据层

> 读咚咚是个人知识数据层的 Python 库，提供 CLI、SDK 和 MCP Server 等多种访问方式。
>
> 本地、私有、可编程的个人知识基础设施。

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.1.0-orange.svg)](https://github.com/gudong/read)

---

## 简介

**读咚咚** 是一个个人知识数据层，以 **Core Library** 为核心资产，支持多种客户端访问。

当你看到一句有启发的话、一篇好文章，快速存下来。CLI、浏览器插件、Agent 都可以访问这些数据。

### 核心特点

- **数据层优先** - Core Library 是核心，CLI/插件/SDK 都是客户端
- **本地私有** - 数据存放在 `~/.read/read.db`，不上云、不同步、不追踪
- **Agent 友好** - JSON 输出 + Python SDK + MCP Server（v0.2）
- **极简核心** - 只做收集，不做整理

---

## 安装

### 方式一：从 PyPI 安装（推荐）

```bash
pip install dong-read
```

### 方式二：从源码安装

```bash
git clone https://github.com/gudong/read.git
cd read
pip install -e .
```

### 初始化

```bash
dr init
```

---

## 安装 Agent Workspace

如果你使用 OpenClaw，可以把 agent 目录复制到工作区：

```bash
# 复制 agent workspace
mkdir -p ~/.openclaw/agents/read
cp -r agent/* ~/.openclaw/agents/read/

# 从模板创建 MEMORY.md
cp agent/MEMORY.md.template ~/.openclaw/agents/read/MEMORY.md
```

---

## 快速开始

```bash
# 添加摘录
dr add "开始，就是最好的时机"

# 收藏文章
dr add --url "https://mp.weixin.qq.com/s/xxx"

# 列出所有
dr ls

# 搜索
dr search "AI"

# 删除
dr delete 123 --force
```

---

## 项目结构

```
read/
├── src/read/           # CLI 源码
├── agent/             # Agent workspace（OpenClaw 使用）
│   ├── IDENTITY.md    # Agent 身份
│   ├── SOUL.md        # Agent 性格
│   ├── TOOLS.md       # CLI 工具定义
│   └── MEMORY.md.template  # 记忆模板
├── docs/              # 文档
├── tests/             # 测试
├── pyproject.toml     # Python 包配置
└── README.md          # 本文件
```

---

## Python SDK

```python
from read import Client

client = Client()

# 添加
item = client.add("开始，就是最好的时机")

# 列出
items = client.list(limit=10)

# 搜索
results = client.search("AI")
```

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `dr init` | 初始化数据库 |
| `dr add "内容"` | 添加摘录 |
| `dr add --url "..."` | 收藏链接 |
| `dr ls` | 列出所有 |
| `dr search "关键词"` | 搜索 |
| `dr get 123` | 获取单条 |
| `dr delete 123` | 删除 |

---

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    客户端层                              │
├──────────────┬──────────────┬──────────────┬────────────┤
│ CLI          │ Browser      │ Python SDK   │ MCP Server  │
│ (dr add)    │ Extension    │ (import)     │ (Agent)     │
└──────────────┴──────────────┴──────────────┴────────────┘
                             │
                    ┌────────▼────────┐
                    │   Core Library  │
                    │ (read.core.Client)│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   SQLite DB     │
                    │   ~/.read/read.db │
                    └─────────────────┘
```

---

## 路线图

| 版本 | 核心资产 | 客户端 | 状态 |
|------|----------|--------|------|
| v0.1 | Core Library v0.1 | CLI | ✅ 完成 |
| v0.2 | Core Library v0.1 | **MCP Server** | 🚧 开发中 |
| v0.3 | Core Library v0.1 | Python SDK 增强 | 📋 计划中 |
| v0.4 | Core Library v0.1 | Browser Extension | 📋 计划中 |

---

## 文档

- [API 参考文档](docs/API_REFERENCE.md)
- [架构设计](ARCHITECTURE.md)
- [产品理念](WHY.md)

---

## License

[MIT](LICENSE)

---

## 作者

[@gudong](https://github.com/gudong)

---

**让 AI 看见你的知识。**
