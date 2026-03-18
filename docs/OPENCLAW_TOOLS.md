# 读咚咚 (Read) - 个人摘录工具

> 本地、私有、可编程的个人知识基础设施

## 快速开始

```bash
# 安装
pip install read-cli

# 初始化
read init
```

## CLI 命令

### 添加摘录
```bash
read add "开始，就是最好的时机"              # 纯内容
read add --url "https://example.com"         # 纯链接
read add "内容" --url "链接" --source "来源" # 完整
```

### 查询摘录
```bash
read ls                    # 列出所有（默认20条）
read ls --limit 50         # 指定数量
read get 1                 # 获取单条
read get 1 --field content # 只获取内容字段
```

### 搜索
```bash
read search "关键词"              # 全字段搜索
read search "关键词" --field content   # 搜索内容
read search "关键词" --field source    # 搜索来源
```

### 删除
```bash
read delete 1 --force     # 删除单条
read delete 1 2 3 --force # 批量删除
```

## Python SDK（推荐）

```python
from read import Client

client = Client()

# 添加
item = client.add("开始，就是最好的时机")

# 收藏链接
client.add(
    content="Agent First, Human Second",
    url="https://example.com",
    source="CLAUDE.md"
)

# 列出
items = client.list(limit=10)
for item in items:
    print(f"{item.id}: {item.display_text}")

# 搜索
results = client.search("AI")

# 链式调用（Agent 友好）
results = client.search_query("Python") \
    .by_field("content") \
    .limit(5) \
    .execute()

# 获取总数
total = client.count()
```

## 输出格式

所有命令返回 JSON：

```json
// 成功
{
  "success": true,
  "data": {...}
}

// 列表
{
  "success": true,
  "data": {
    "total": 100,
    "count": 20,
    "items": [...]
  }
}
```

## 用户意图映射

| 用户说 | 命令 |
|--------|------|
| "收藏这句话" | `read add "..."` |
| "保存这篇文章" | `read add --url "..."` |
| "我存了什么" | `read ls --limit 10` |
| "找关于 AI 的" | `read search "AI"` |
| "看看我收藏的链接" | `read ls --type link` |
| "删除这条" | `read delete <id> --force` |

## 数据库位置

```
~/.read/read.db
```

备份：直接复制这个文件即可。

## Agent 使用技巧

1. **添加时自动推断**：用户说"收藏"时，判断是内容还是链接
2. **搜索关键词提取**：从用户问题中提取核心关键词
3. **返回格式友好**：给用户显示 `content` 或 `url`，不是完整 JSON
4. **推荐回顾**：每日随机推荐 1 条历史摘录
