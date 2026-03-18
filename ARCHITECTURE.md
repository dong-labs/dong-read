# 读咚咚 (Read) - 架构设计文档

> 设计日期：2026-03-15
> 版本：v1.0

---

## 产品定位

**读咚咚** 是个人知识数据层，支持多种客户端访问。

本地、私有、可编程的个人知识基础设施。

---

## 核心架构

### 四层架构

```
┌─────────────────────────────────────────────────────────────┐
│                        客户端层                              │
│  （浏览器插件、CLI、Alfred Workflow、快捷指令、GUI...）      │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   接口层        │
                    │ (CLI/HTTP/MCP)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   核心层        │
                    │ (Core Library)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   数据层        │
                    │  (SQLite DB)    │
                    └─────────────────┘
```

**核心原则**：
- **Core Library 是核心资产，不是 CLI**
- **CLI 是核心接口，不是唯一入口**
- **数据层只管存储和接口，不管用户交互**
- **客户端各自优化特定场景的 UX**
- **统一数据空间，人类和 Agent 可以协作**

### 为什么 Core Library 是核心

| 思维方式 | CLI 核心 | Core Library 核心 |
|----------|----------|-------------------|
| 产品性质 | 命令行工具 | Python 库 |
| 核心用户 | 终端用户 | 开发者/Agent |
| 扩展方式 | 加新命令 | 加新客户端 |
| 长期价值 | 功能完整性 | 接口稳定性 |
| 商业模式 | 卖便利性 | 开源核心 + 付费支持 |

**如果定位是"数据基础设施"，那 Core Library 必须是核心。**

这就像 PostgreSQL：
- 核心开源（Core Library）
- 付费企业版（托管服务）
- 技术支持服务（开发者工具）

---

## 1. 项目目录结构

```
ReadDongDong/
├── readme.md                      # 产品介绍
├── CLAUDE.md                      # Claude Code 指导文档
├── ARCHITECTURE.md                # 本文档
├── pyproject.toml                 # 项目配置
│
├── src/
│   └── read/                       # 主包
│       ├── __init__.py            # version = "0.1.0"
│       ├── cli.py                 # Typer 主入口
│       ├── const.py               # 常量定义
│       │
│       ├── core/                  # 核心库（v0.1 抽离）
│       │   ├── __init__.py
│       │   ├── client.py          # Python SDK (read.core.Client)
│       │   └── models.py          # 数据模型
│       │
│       ├── mcp/                   # MCP Server (v0.2，关键验证点)
│       │   └── server.py           # MCP 服务
│       │
│       ├── db/                    # 数据库层
│       │   ├── __init__.py
│       │   ├── connection.py      # SQLite 连接管理
│       │   ├── schema.py          # 表结构和初始化
│       │   └── utils.py           # CRUD 操作封装
│       │
│       └── commands/              # 命令实现（调用 core）
│           ├── __init__.py
│           ├── init.py            # read init
│           ├── add.py             # read add
│           ├── ls.py              # read ls
│           ├── get.py             # read get
│           ├── delete.py          # read delete
│           └── search.py          # read search
│
├── tests/                         # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
└── .read/                          # 数据目录（运行时生成）
    └── read.db
```

---

## 2. 数据库层设计

### 2.1 表结构

```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,                    -- 摘录内容（可选）
    url TEXT,                        -- 链接（可选）
    source TEXT,                     -- 来源备注（可选）
    type TEXT DEFAULT 'quote',        -- 数据类型：quote/article/code
    metadata TEXT,                   -- JSON 扩展字段（v0.1 预留）
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,  -- 同步预留（v0.1）

    -- content 和 url 至少有一个不为空
    CHECK(content IS NOT NULL OR url IS NOT NULL)
);

-- 索引：加速查询
CREATE INDEX idx_items_created_at ON items(created_at DESC);
CREATE INDEX idx_items_content ON items(content);
CREATE INDEX idx_items_url ON items(url);
CREATE INDEX idx_items_type ON items(type);  -- 类型筛选（v0.1 预留）
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | INTEGER | 是 | 主键，自增 |
| content | TEXT | 否* | 摘录内容，与 url 至少一个必填 |
| url | TEXT | 否* | 链接，与 content 至少一个必填 |
| source | TEXT | 否 | 来源备注（如：微信、书名） |
| type | TEXT | 否 | 数据类型：quote/article/code（v0.1 预留） |
| metadata | TEXT | 否 | JSON 扩展字段（v0.1 预留，为 Agent 补充信息） |
| created_at | TEXT | 是 | 创建时间，ISO 8601 格式 |
| updated_at | TEXT | 是 | 更新时间，同步预留（v0.1） |

### 2.3 连接管理 (connection.py)

```python
"""职责：
- 单例模式管理 SQLite 连接
- 确保数据库目录存在
- 提供线程安全的连接
- 提供上下文管理器
"""

import sqlite3
import threading
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Iterator

_connection: sqlite3.Connection | None = None
_lock = threading.Lock()


@lru_cache(maxsize=1)
def get_db_path() -> Path:
    """获取数据库路径"""
    db_path = Path.home() / ".read" / "read.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def get_connection() -> sqlite3.Connection:
    """获取连接（单例）"""
    # ...（实现）


@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    """获取游标（自动事务管理）"""
    # ...（实现）
```

### 2.4 CRUD 操作 (utils.py)

```python
"""职责：
- 封装所有数据库操作
- 提供类型友好的接口
- 处理业务逻辑验证
"""

def add_item(
    content: Optional[str] = None,
    url: Optional[str] = None,
    source: Optional[str] = None,
) -> int:
    """添加摘录，返回新 ID"""

def list_items(
    limit: int = 20,
    offset: int = 0,
    item_type: Optional[str] = None,
    order: str = "desc",
) -> list[dict]:
    """列出摘录"""

def get_item(item_id: int) -> Optional[dict]:
    """获取单条"""

def delete_item(item_id: int) -> bool:
    """删除单条"""

def search_items(
    query: str,
    field: Optional[str] = None,
    limit: int = 20,
) -> list[dict]:
    """搜索"""

def count_total() -> int:
    """总数"""
```

---

## 3. CLI 层设计

### 3.1 统一输出格式 (cli.py)

```python
"""职责：
- 统一的 JSON 输出
- 统一的错误处理
- Typer 应用配置
"""

import json
import typer
from typing import Any

app = typer.Typer(
    name="read",
    help="读咚咚 (Read) - 个人知识数据层的命令行接口",
    no_args_is_help=True,
    add_completion=False,
)


def output(data: Any, success: bool = True) -> None:
    """输出 JSON 格式"""
    result: dict[str, Any] = {"success": success}
    if success:
        result["data"] = data
    else:
        result["error"] = data
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


def handle_error(e: Exception) -> None:
    """处理异常并输出结构化错误"""
    error_info: dict[str, str] = {
        "code": type(e).__name__,
        "message": str(e)
    }
    output(error_info, success=False)
    raise typer.Exit(code=1)
```

### 3.2 命令模板

每个命令文件遵循统一结构：

```python
"""命令说明"""

import typer
from read.cli import output, handle_error
from read.db.utils import add_item

def cmd_add(
    content: str = typer.Argument(None, help="摘录内容"),
    url: str = typer.Option(None, "--url", help="链接"),
    source: str = typer.Option(None, "--source", help="来源备注"),
):
    """添加摘录或链接"""
    try:
        item_id = add_item(content=content, url=url, source=source)
        item = get_item(item_id)
        output(item)
    except Exception as e:
        handle_error(e)
```

---

## 4. 命令详细设计

### 4.1 init - 初始化

```bash
read init
```

```json
{
  "success": true,
  "data": {
    "message": "Read database initialized",
    "db_path": "/Users/xxx/.read/read.db",
    "version": "0.1.0"
  }
}
```

### 4.2 add - 添加

```bash
read add "一句话说得真好"
read add "一句话" --url "https://example.com"
read add --url "https://mp.weixin.qq.com/s/xxx"
read add "一句话" --url "..." --source "CLAUDE.md"
```

**验证规则**：
- content 和 url 至少一个不为空
- url 格式基本验证

### 4.3 ls - 列出

```bash
read ls                    # 默认 20 条
read ls --limit 50
read ls --type content     # 只摘录
read ls --type link        # 只链接
read ls --order asc        # 正序
```

```json
{
  "success": true,
  "data": {
    "total": 150,
    "items": [...]
  }
}
```

### 4.4 get - 获取

```bash
read get 123
read get 123 --field content
```

### 4.5 delete - 删除

```bash
read delete 123
read delete 123 124 125
read delete 123 --force
```

### 4.6 search - 搜索

```bash
read search "AI"
read search "微信" --field source
```

---

## 5. 配置文件

### 5.1 pyproject.toml

```toml
[project]
name = "read-cli"
version = "0.1.0"
description = "读咚咚 - 个人知识数据层的命令行接口"
readme = "readme.md"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.12.0",
]

[project.scripts]
read = "read.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/read"]

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
pythonpath = ["src"]
```

---

## 6. 设计决策记录

### 6.1 为什么用 SQLite 单文件？

- 零配置
- 适合个人数据量
- 易于备份（复制一个文件即可）
- Python 内置支持

### 6.2 为什么不做 tags 表？

- 先验证核心需求
- 够用就行，不过度设计
- 以后可以通过 source 字段简单实现

### 6.3 为什么不做 status 字段？

- 只管收集，不管管理
- 减少心智负担
- 如果需要，可以通过 created_at 推断

### 6.4 为什么用 Typer？

- 类型提示友好
- 自动生成帮助信息
- Click 的现代替代品

---

## 7. 实现顺序

1. **基础设施**
   - [ ] 项目目录结构
   - [ ] pyproject.toml
   - [ ] db/connection.py
   - [ ] db/schema.py
   - [ ] db/utils.py

2. **CLI 入口**
   - [ ] cli.py（统一输出、错误处理）
   - [ ] const.py

3. **核心命令**
   - [ ] init.py
   - [ ] add.py
   - [ ] ls.py
   - [ ] get.py
   - [ ] delete.py
   - [ ] search.py

4. **测试**
   - [ ] 单元测试
   - [ ] 集成测试

---

## 8. 版本规划

| 版本 | 核心资产 | 客户端 | 验证目标 | 工期 |
|------|----------|--------|----------|------|
| v0.1 | Core Library v0.1 | CLI | 数据模型和 API 稳定性 | 2天 |
| v0.2 | Core Library v0.1 | **MCP Server** | **Agent 集成价值（关键验证点）** | 1天 |
| v0.3 | Core Library v0.1 | Python SDK | 开发者体验 | 0.5天 |
| v0.4 | Core Library v0.1 | Browser Extension | 用户体验 | 1-2天 |

**核心原则**：
1. **Core Library 的版本号才是产品的主版本号**
2. 所有客户端都是 Core Library 的薄封装
3. 每一步都是"加一层"，不是重构

**验证策略**：v0.2 MCP Server 是验证"数据基础设施"定位的关键。如果验证成功，继续推进；如果验证失败，重新定位或暂停。

---

## 9. v0.1 架构约束

为未来版本预留空间，v0.1 开发时必须遵守：

### 9.0 Core Library 优先设计原则

**Core Library 必须满足**：

| 原则 | 要求 | 验证方式 |
|------|------|----------|
| **独立性** | 不依赖任何客户端（CLI/MCP/HTTP） | 可单独 import 使用 |
| **完整性** | 包含所有数据操作逻辑 | 客户端无需直接访问数据库 |
| **稳定性** | API 设计考虑向后兼容 | 命名和参数慎重设计 |
| **可测试性** | 所有逻辑可独立单元测试 | 不依赖 CLI 运行 |

**实现约束**：
- Core Library 代码位于 `src/read/core/`
- 不得在 Core Library 中 import CLI 相关模块
- 所有数据库操作必须通过 Core Library 暴露的方法

### 9.1 Core Library 与 CLI 解耦

- CLI 不直接操作 SQLite
- CLI 调用 Core Library 的方法
- 未来 MCP/SDK 可以复用同一个 Core Library
- **设计目标**：v0.2 加入 MCP Server 时，只需"加一层"，不需重构

### 9.2 错误码统一

- 设计一套错误码体系
- CLI 和未来 HTTP API/MCP 共用
- 方便客户端统一处理
- **错误信息人类化**：对开发者友好的错误提示

### 9.3 数据模型稳定

- 尽量减少 schema 变更
- 为扩展字段预留空间
- 向后兼容
- **新增字段考虑**：
  - `metadata JSON` — Agent 补充信息
  - `updated_at TEXT` — 同步预留
  - `type TEXT` — 支持多种数据类型

---

## 10. 设计决策记录

### 10.1 为什么用 SQLite 单文件？

- 零配置
- 适合个人数据量
- 易于备份（复制一个文件即可）
- Python 内置支持

### 10.2 为什么 CLI 是核心接口而非唯一入口？

- CLI 是数据层的命令行接口
- 人类用户通过浏览器插件等客户端访问
- Agent 通过 MCP/SDK 访问
- CLI 主要用于开发和调试

### 10.3 为什么不做 tags 表？

- 先验证核心需求
- 够用就行，不过度设计
- 以后可以通过 source 字段简单实现
- 客户端层可以实现标签功能

### 10.4 为什么用 Typer？

- 类型提示友好
- 自动生成帮助信息
- Click 的现代替代品

---

## 11. 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-15 | 初始版本 |
