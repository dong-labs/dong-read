# 读咚咚 (Read) - Twitter 推广文案

## 推文 1：产品发布

刚发布了读咚咚 (Read) - 一个本地、私有的个人知识数据层，为 Agent 时代设计。

当你看到一句好话、一篇好文章，快速存下来。CLI、Python SDK、MCP Server 都可以访问。

核心：数据在你电脑上，Agent 可以直接读取。

https://github.com/gudong/read

#AI #Agent #CLI

---

## 推文 2：使用场景

我的一天：

终端看到好话 → `read add "这句话说得真好"`
浏览器看到好文 → 浏览器插件一键收藏（v0.4）
Agent 需要推荐 → `client.search("AI")`

所有数据都在 `~/.read/read.db`，不上云。

#个人知识管理 #本地优先

---

## 推文 3：Agent First

为什么是 "Agent First"？

现在的笔记工具（Notion、Cubox）都是为人类设计的，Agent 访问需要 API、Token、限流...

Read 是本地 SQLite，Agent 一行命令就能读：

```python
from read import Client
client = Client()
items = client.search("AI")
```

这叫 Agent 原生。

#Agent #AI #Python

---

## 推文 4：与 Cang 的关系

仓咚咚 (Cang) → 管钱
读咚咚 (Read) → 管内容

都是本地、私有、可编程的个人数据工具。

家族化设计，共享架构，各自专注。

#个人数据 #本地优先

---

## 推文 5：极简设计

读咚咚不做：

❌ 标签系统
❌ 自动抓取
❌ 全文索引
❌ AI 摘要
❌ 定时推送

只做一件事：让你快速把内容存进来。

#极简设计 #少即是多

---

## 推文 6：MCP Server

v0.2 会加入 MCP Server 支持。

到时候 Claude、ChatGPT 可以直接调用 Read 的工具，不需要你写任何代码。

这就是 "Agent 原生" 的意思。

#MCP #Claude #ChatGPT

---

## 推文 7：开发者友好

Read 的核心是 Python SDK，CLI 只是其中一个客户端。

你可以：
- 直接 `import read` 使用
- 写自己的 CLI 封装
- 做 HTTP API
- 做 Alfred Workflow

数据层很简单，客户端你自己定义。

#开发者 #SDK #开放

---

## 推文 8：为什么开源

因为这不应该是生意。

个人数据基础设施，应该是：
- 开源的
- 本地的
- 可控的

你的数据，应该属于你。

#开源 #隐私 #数据主权

---

## 推文 9：使用一个月

自己用了一个月，存了 150+ 条摘录。

最大的价值：Agent 可以随时读取、分析、推荐。

早上让 Agent 随机推送一条，写作时让 Agent 找相关内容。

这才是 Agent 时代的知识管理。

#AI #个人知识管理

---

## 推文 10：路线图

v0.1 ✅ - Core Library + CLI
v0.2 🚧 - MCP Server
v0.3 📋 - Python SDK 增强
v0.4 📋 - 浏览器插件

未来可能还有：
- 记咚咚（时间管理）
- 行咚咚（习惯追踪）

家族化个人数据工具，全部本地、全部 Agent 友好。

#路线图 #产品规划
