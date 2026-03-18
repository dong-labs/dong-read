# 读咚咚 v0.1.0 发布

> 个人知识数据层的命令行接口

## 简介

读咚咚 (Read) 是一个本地、私有、可编程的个人知识基础设施。

当你看到一句有启发的话、一篇好文章，快速存下来。CLI、浏览器插件、Agent 都可以访问这些数据。

## 核心特点

- **数据层优先** - Core Library 是核心，CLI/插件/SDK 都是客户端
- **本地私有** - 数据存放在 `~/.read/read.db`，不上云、不同步、不追踪
- **Agent 友好** - JSON 输出 + Python SDK + MCP Server（v0.2）
- **极简核心** - 只做收集，不做整理

## 安装

```bash
pip install dong-read

# 初始化
dr init
```

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
```

## Python SDK

```python
from read import Client

client = Client()
client.add("Agent First, Human Second")
items = client.search("AI")
```

## 架构

```
┌─────────────────────────────────────────┐
│  客户端层 (CLI/SDK/MCP/Browser)         │
├─────────────────────────────────────────┤
│  Core Library (read.core.Client)         │
├─────────────────────────────────────────┤
│  SQLite DB (~/.read/read.db)              │
└─────────────────────────────────────────┘
```

## 路线图

- [x] v0.1 - Core Library + CLI
- [ ] v0.2 - MCP Server (Agent 原生集成)
- [ ] v0.3 - Python SDK 增强
- [ ] v0.4 - 浏览器插件

## 为什么叫"读咚咚"？

和"仓咚咚"(Cang) 一样，都是个人数据管理工具家族的一员。

- 仓咚咚 → 管钱（财务流动）
- 读咚咚 → 管内容（阅读摘录）

## License

MIT

## 作者

@gudong
