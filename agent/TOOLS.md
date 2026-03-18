# TOOLS.md - 读咚咚的工具箱

## 命令行工具 (CLI)

### 安装
```bash
pip install read-cli
```

### 基础命令
```bash
read init              # 初始化
read add "内容"        # 添加摘录
read add --url "链接"  # 收藏链接
read ls                # 列出所有
read search "关键词"   # 搜索
read get 1             # 获取单条
read delete 1 --force  # 删除
```

---

## Python SDK

```python
from read import Client

client = Client()

# 添加
client.add("开始，就是最好的时机")

# 搜索
results = client.search("AI")

# 链式调用
client.search_query("Python").limit(5).execute()
```

---

## 数据位置

```
~/.read/read.db
```

备份：直接复制这个文件

---

## 摘录类型

| 类型 | 说明 | 示例 |
|------|------|------|
| quote | 文字摘录 | 一句话、一段话 |
| article | 文章链接 | 微信、掘金、博客 |
| code | 代码片段 | 函数、配置 |

---

## 常见来源

| 来源 | 标签 |
|------|------|
| CLAUDE.md | 文档 |
| GitHub | 代码 |
| 微信 | 聊天 |
| 掘金 | 文章 |
| V2EX | 讨论 |

---

## 用户意图映射

| 用户说 | 命令 |
|--------|------|
| "收藏这句话" | `read add "..."` |
| "保存这篇文章" | `read add --url "..."` |
| "我存了什么" | `read ls --limit 10` |
| "找关于 AI 的" | `read search "AI"` |
| "有多少条了" | `read ls` 查看 total |
| "删除这条" | `read delete <id> --force` |

---

## 快捷操作

- 记一句话：直接说"收藏：..."
- 保存链接：说"保存：https://..."
- 搜索内容：说"找：关键词"
- 查看数量：说"统计"

---

*工具齐备，随时囤书 📖*
