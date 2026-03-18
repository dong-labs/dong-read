# 读咚咚 (Read) - V2EX 分享帖

## 标题
[分享] 做了一个本地、私有的个人知识数据层，为 Agent 时代设计

## 正文

大家好，

做了一个叫"读咚咚" (Read) 的小工具，定位是"个人知识数据层的命令行接口"。

### 起因

我有个日常场景：

今天看到一篇好文章，里面有句话很触动我。我想把它存下来。

然后呢？
- 发到微信读书？不，这不是书
- 存到 Cubox？可是它是云端的，我不放心
- 复制到 Notion？打开太慢了
- 记在脑子里？哈哈，明天就忘了

我只是想：快速、私密、可靠地存下来。就这么简单。

### 为什么做这个

现在的工具（Cubox、Pocket、Notion）都有一个共同问题：**它们不是为 Agent 设计的**。

Agent 越来越多（Claude Code、Cursor、warp），但它们需要**可操作的数据**。如果你的摘录、收藏都在云端 SaaS 里，Agent 怎么访问？

如果数据在本地的 SQLite 里，一行命令就拿到了：

```bash
dr ls --limit 5
# → 返回 JSON
# → Agent 解析、分析、推荐
```

### 核心设计

```
┌─────────────────────────────────────────┐
│  客户端层 (CLI/SDK/MCP/Browser)         │
├─────────────────────────────────────────┤
│  Core Library (read.core.Client)         │
├─────────────────────────────────────────┤
│  SQLite DB (~/.read/read.db)              │
└─────────────────────────────────────────┘
```

**核心原则**：
1. Core Library 是核心资产，不是 CLI
2. 本地私有，数据在你电脑上
3. Agent 友好（JSON 输出 + Python SDK）
4. 极简核心，不做标签、不做 AI 摘要、不做定时推送

### 使用示例

```bash
# 安装
pip install dong-read

# 初始化
dr init

# 添加摘录
dr add "我们一直在设计 AI 原生的工具"

# 收藏文章
dr add --url "https://example.com"

# 列出所有
dr ls

# 搜索
dr search "AI"
```

### Python SDK

```python
from read import Client

client = Client()
client.add("Agent First, Human Second")
items = client.search("AI").limit(5)
```

### 为什么叫"读咚咚"？

和"仓咚咚"一样，都是个人数据管理工具家族的一员：

- 仓咚咚 (cang) → 管钱（财务流动）
- 读咚咚 (read) → 管内容（阅读摘录）

以后可能还有：
- 记咚咚 → 管时间（日程日志）
- 行咚咚 → 管习惯（打卡追踪）

### 开源地址

https://github.com/gudong/read

欢迎 feedback！

---

*这不是一个"产品"，而是一个"工具"。工具应该简单、可靠、不起眼。*
