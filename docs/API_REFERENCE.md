# 读咚咚 API 参考文档

## Core Library API

### Client 类

读咚咚的核心客户端，提供给 Agent 和开发者使用。

#### 初始化

```python
from read import Client

client = Client()
# 或指定数据库路径
client = Client(db_path=Path("/path/to/db"))
```

#### add() - 添加摘录

```python
item = client.add(
    content="开始，就是最好的时机",
    url="https://example.com",
    source="CLAUDE.md",
    item_type="quote",
    metadata='{"key": "value"}'
)
```

**参数：**
- `content` (str | None) - 摘录内容
- `url` (str | None) - 链接
- `source` (str | None) - 来源备注
- `item_type` (str) - 数据类型：quote/article/code
- `metadata` (str | None) - JSON 扩展字段

**返回：** `Item` 对象

**异常：** `ValueError` - content 和 url 都为空

---

#### list() - 列出摘录

```python
items = client.list(
    limit=20,
    offset=0,
    item_type="quote",
    order="desc"
)
```

**参数：**
- `limit` (int) - 返回数量限制，默认 20
- `offset` (int) - 偏移量，默认 0
- `item_type` (str | None) - 筛选类型
- `order` (str) - 排序方向：desc/asc

**返回：** `list[Item]`

---

#### get() - 获取单条

```python
item = client.get(123)
```

**参数：**
- `item_id` (int) - 摘录 ID

**返回：** `Item` 对象

**异常：** `NotFoundError` - 摘录不存在

---

#### get_optional() - 获取单条（可选）

```python
item = client.get_optional(123)
if item:
    print(item.content)
```

**参数：**
- `item_id` (int) - 摘录 ID

**返回：** `Item` 对象或 None

---

#### delete() - 删除摘录

```python
success = client.delete(123)
```

**参数：**
- `item_id` (int) - 摘录 ID

**返回：** `bool` - 是否删除成功

---

#### search() - 搜索摘录

```python
items = client.search(
    query="AI",
    field="content",
    limit=20
)
```

**参数：**
- `query` (str) - 搜索关键词
- `field` (str | None) - 搜索字段：content/url/source，None 表示全部
- `limit` (int) - 返回数量限制

**返回：** `list[Item]`

---

#### count() - 获取总数

```python
total = client.count()
```

**返回：** `int`

---

#### search_query() - 链式搜索

```python
items = client.search_query("Python").by_field("content").limit(5).execute()
```

**返回：** `QueryBuilder` 对象

---

### Item 数据模型

```python
@dataclass
class Item:
    id: int
    content: str | None
    url: str | None
    source: str | None
    type: str
    metadata: str | None
    created_at: str | None
    updated_at: str | None
```

#### 属性方法

- `is_quote` - 是否为文字摘录
- `is_link` - 是否为链接
- `display_text` - 显示文本（优先 content，其次 url）

#### 方法

- `to_dict()` - 转换为字典
- `from_dict(data)` - 从字典创建

---

## CLI API

所有命令返回 JSON 格式：

```json
{
  "success": true,
  "data": {...}
}
```

错误格式：

```json
{
  "success": false,
  "error": {
    "code": "ErrorCode",
    "message": "错误信息"
  }
}
```

### init - 初始化

```bash
read init
```

**返回：**
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

---

### add - 添加

```bash
read add "内容"
read add "内容" --url "https://..." --source "来源"
read add --url "https://..."
```

**参数：**
- `content` - 摘录内容
- `--url, -u` - 链接
- `--source, -s` - 来源备注
- `--type, -t` - 数据类型（quote/article/code）

**返回：** Item 对象的 JSON 表示

---

### ls - 列出

```bash
read ls
read ls --limit 50 --type content --order asc
```

**参数：**
- `--limit, -l` - 返回数量
- `--offset, -o` - 偏移量
- `--type, -t` - 筛选类型（content/link）
- `--order` - 排序方向（desc/asc）

**返回：**
```json
{
  "success": true,
  "data": {
    "total": 150,
    "count": 20,
    "items": [...]
  }
}
```

---

### get - 获取

```bash
read get 123
read get 123 --field content
```

**参数：**
- `item_id` - 摘录 ID
- `--field, -f` - 只返回指定字段

**返回：** Item 对象或字段值

---

### delete - 删除

```bash
read delete 123
read delete 123 124 125 --force
```

**参数：**
- `item_ids` - 摘录 ID（支持多个）
- `--force, -f` - 强制删除，不确认

**返回：**
```json
{
  "success": true,
  "data": {
    "deleted": [123, 124],
    "deleted_count": 2
  }
}
```

---

### search - 搜索

```bash
read search "AI"
read search "微信" --field source
```

**参数：**
- `query` - 搜索关键词
- `--field, -f` - 搜索字段（content/url/source）
- `--limit, -l` - 返回数量

**返回：**
```json
{
  "success": true,
  "data": {
    "query": "AI",
    "field": null,
    "count": 5,
    "items": [...]
  }
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| `ValueError` | content 和 url 都为空 |
| `NotFoundError` | 摘录不存在 |
| `DatabaseError` | 数据库错误 |

---

## MCP Server (v0.2)

v0.2 版本将提供 MCP Server 支持，工具列表：

- `read_init` - 初始化数据库
- `read_add` - 添加摘录
- `read_list` - 列出摘录
- `read_get` - 获取单条
- `read_delete` - 删除摘录
- `read_search` - 搜索摘录
- `read_count` - 获取总数
