# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: Read CLI

**读咚咚 (Read)** - 个人知识数据层的命令行接口。

本地、私有、可编程的个人知识基础设施。

---

## 核心设计原则

1. **数据层优先，客户端多样** - CLI 是核心接口，不是唯一入口
2. **Agent Friendly** - 所有操作返回结构化 JSON，提供 Python SDK 和 MCP Server
3. **本地私有** - 数据存放在 `~/.read/read.db`，不上云、不同步、不追踪
4. **极简核心** - 数据层只做存储和接口，复杂功能由客户端实现

---

## 产品边界

**数据层做的：**
- 存摘录（文字）
- 存链接（稍后读）
- 列出所有
- 简单搜索
- 返回结构化数据（JSON/Python 对象）

**数据层不做的（由客户端实现）：**
> "有疑问时，不加。想加新功能？先划掉一个旧的。"

- ❌ 不做标签系统（可由客户端实现）
- ❌ 不做自动抓取网页内容
- ❌ 不做全文索引（未来可由 FTS5 实现）
- ❌ 不做阅读进度跟踪
- ❌ 不做高亮和批注
- ❌ 不做社交分享
- ❌ 不做多端同步（未来可由扩展字段支持）
- ❌ 不做定时推送
- ❌ 不做 AI 摘要生成
- ❌ 不做数据可视化

**支持的客户端：**
- CLI（命令行） - v0.1
- Python SDK - v0.3
- MCP Server（Agent 集成） - v0.2
- Browser Extension - v0.4
- 未来：Web Dashboard、Mobile App、Alfred Workflow 等

---

## 技术栈

- **语言**: Python 3.11+
- **CLI 框架**: Typer
- **数据库**: SQLite (单文件 `~/.read/read.db`)
- **Agent 集成**: MCP (Model Context Protocol)
- **输出**: 所有命令返回 JSON

## 版本规划

| 版本 | 核心资产 | 客户端 | 验证目标 | 工期 |
|------|----------|--------|----------|------|
| v0.1 | Core Library v0.1 | CLI | 数据模型和 API 稳定性 | 2天 |
| v0.2 | Core Library v0.1 | Python SDK | 开发者体验 | 0.5天 |
| v0.3 | Core Library v0.1 | **MCP Server** | **Agent 集成验证（关键）** | 1天 |
| v0.4 | Core Library v0.1 | Browser Extension | 用户体验 | 1-2天 |

**核心原则**：Core Library 的版本号才是产品的主版本号。所有客户端都是 Core Library 的薄封装。

---

## 命令结构

```
read
├── init              # 初始化数据库
├── add               # 添加摘录/链接
├── ls                # 列出所有
├── get               # 获取单条详情
├── delete            # 删除
└── search            # 搜索内容
```

---

## 命令示例

```bash
# 初始化
dr init

# 场景1: 只存摘录
dr add "我们一直在设计 AI 原生的工具"

# 场景2: 摘录 + 链接
dr add "Agent First, Human Second" --url "https://example.com"

# 场景3: 只存链接
dr add --url "https://mp.weixin.qq.com/s/xxx"

# 场景4: 带来源备注
dr add "一句话" --url "https://example.com" --source "CLAUDE.md"

# 列出所有
dr ls

# 指定数量
dr ls --limit 50

# 只列出摘录
dr ls --type content

# 只列出链接
dr ls --type link

# 获取单条
dr get 123

# 删除
dr delete 123

# 搜索
dr search "AI"
```

---

## 统一输出格式

```json
// 成功
{
  "success": true,
  "data": { ... }
}

// 失败
{
  "success": false,
  "error": {
    "code": "ErrorCode",
    "message": "错误信息"
  }
}
```

---

## 数据库设计

### 文件位置

```
~/.read/read.db
```

### 表结构

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,                    -- 摘录内容（可选）
    url TEXT,                        -- 链接（可选）
    source TEXT,                     -- 来源备注（可选）
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

    -- content 和 url 至少有一个不为空
    CHECK(content IS NOT NULL OR url IS NOT NULL)
);

-- 索引
CREATE INDEX idx_items_created_at ON items(created_at DESC);
CREATE INDEX idx_items_content ON items(content);
CREATE INDEX idx_items_url ON items(url);
```

---

## 安装与运行

```bash
# 开发模式安装
pip install -e .

# 初始化
dr init

# 添加摘录
dr add "我们一直在设计 AI 原生的工具"

# 列出所有
dr ls
```

---

## 项目结构

```
ReadDongDong/
├── readme.md
├── CLAUDE.md
├── ARCHITECTURE.md
├── pyproject.toml
├── src/
│   └── read/
│       ├── __init__.py
│       ├── cli.py                 # CLI 主入口
│       ├── const.py
│       ├── core/                  # Core Library
│       │   ├── __init__.py
│       │   ├── client.py          # Python SDK
│       │   └── models.py          # 数据模型
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   ├── schema.py
│       │   └── utils.py
│       ├── commands/
│       │   └── ...
│       └── mcp/                   # MCP Server (v0.2)
│           └── server.py
└── tests/
```

---

## 为什么叫"读咚咚"？

和"仓咚咚"(Cang) 一样，都是个人数据管理工具家族的一员。

- 仓咚咚 (cang) → 管钱（财务流动）
- 读咚咚 (read) → 管内容（阅读摘录）

以后可能还有：
- 记咚咚 → 管时间（日程日志）
- 行咚咚 → 管习惯（打卡追踪）

---

## 架构原则

**CLI 是核心接口，不是唯一入口。**

读咚咚采用三层架构：

```
┌─────────────────────────────────────────────────────────┐
│                    客户端层                              │
├──────────────┬──────────────┬──────────────┬────────────┤
│ CLI          │ Browser      │ Python SDK   │ MCP Server  │
│ (dr add)    │ Extension    │ (import)     │ (Agent)     │
└──────┬───────┴──────┬───────┴──────┬───────┴────┬───────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Core Library  │
                    │  (read.core)     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   SQLite DB     │
                    │ ~/.read/read.db   │
                    └─────────────────┘
```

**开发时请注意：**
- 所有客户端（CLI、MCP、HTTP API）都基于 Core Library
- 不要在 CLI 命令中直接操作数据库，必须通过 Core Library
- 新功能优先考虑在 Core Library 中实现，然后由各客户端调用

---

## 版本

v0.1.0 — 2026.03.15
