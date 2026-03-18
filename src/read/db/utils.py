"""CRUD 操作封装

职责：
- 封装所有数据库操作
- 提供类型友好的接口
- 处理业务逻辑验证
"""

from __future__ import annotations

from typing import Optional

from read.const import DEFAULT_LIMIT, DEFAULT_TYPE, get_timestamp


def add_item(
    content: Optional[str] = None,
    url: Optional[str] = None,
    source: Optional[str] = None,
    item_type: str = DEFAULT_TYPE,
    metadata: Optional[str] = None,
) -> int:
    """添加摘录，返回新 ID

    Args:
        content: 摘录内容
        url: 链接
        source: 来源备注
        item_type: 数据类型
        metadata: JSON 扩展字段

    Returns:
        新插入记录的 ID

    Raises:
        ValueError: content 和 url 都为空
    """
    from read.db.connection import get_cursor

    # 验证
    if not content and not url:
        raise ValueError("content 和 url 至少需要一个不为空")

    now = get_timestamp()

    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO items (content, url, source, type, metadata, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (content, url, source, item_type, metadata, now, now),
        )
        return cursor.lastrowid


def list_items(
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
    item_type: Optional[str] = None,
    order: str = "desc",
) -> list[dict]:
    """列出摘录

    Args:
        limit: 返回数量限制
        offset: 偏移量
        item_type: 筛选类型
        order: 排序方向（desc/asc）

    Returns:
        摘录列表
    """
    from read.db.connection import get_cursor

    order_sql = "DESC" if order.lower() == "desc" else "ASC"

    with get_cursor() as cursor:
        if item_type:
            cursor.execute(
                f"""
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                WHERE type = ?
                ORDER BY created_at {order_sql}
                LIMIT ? OFFSET ?
                """,
                (item_type, limit, offset),
            )
        else:
            cursor.execute(
                f"""
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                ORDER BY created_at {order_sql}
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_item(item_id: int) -> Optional[dict]:
    """获取单条摘录

    Args:
        item_id: 摘录 ID

    Returns:
        摘录数据，不存在返回 None
    """
    from read.db.connection import get_cursor

    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT id, content, url, source, type, metadata, created_at, updated_at
            FROM items
            WHERE id = ?
            """,
            (item_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_item(item_id: int) -> bool:
    """删除摘录

    Args:
        item_id: 摘录 ID

    Returns:
        是否删除成功
    """
    from read.db.connection import get_cursor

    with get_cursor() as cursor:
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        return cursor.rowcount > 0


def search_items(
    query: str,
    field: Optional[str] = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict]:
    """搜索摘录

    Args:
        query: 搜索关键词
        field: 搜索字段（content/url/source），None 表示全部
        limit: 返回数量限制

    Returns:
        匹配的摘录列表
    """
    from read.db.connection import get_cursor

    pattern = f"%{query}%"

    with get_cursor() as cursor:
        if field == "content":
            cursor.execute(
                """
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                WHERE content LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (pattern, limit),
            )
        elif field == "url":
            cursor.execute(
                """
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                WHERE url LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (pattern, limit),
            )
        elif field == "source":
            cursor.execute(
                """
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                WHERE source LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (pattern, limit),
            )
        else:
            # 全部字段
            cursor.execute(
                """
                SELECT id, content, url, source, type, metadata, created_at, updated_at
                FROM items
                WHERE content LIKE ? OR url LIKE ? OR source LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (pattern, pattern, pattern, limit),
            )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def count_total() -> int:
    """获取摘录总数"""
    from read.db.connection import get_cursor

    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as count FROM items")
        row = cursor.fetchone()
        return row["count"] if row else 0


def update_item(
    item_id: int,
    content: Optional[str] = None,
    url: Optional[str] = None,
    source: Optional[str] = None,
    metadata: Optional[str] = None,
) -> bool:
    """更新摘录（预留，v0.1 暂不通过 CLI 暴露）

    Args:
        item_id: 摘录 ID
        content: 新内容
        url: 新链接
        source: 新来源
        metadata: 新元数据

    Returns:
        是否更新成功
    """
    from read.db.connection import get_cursor

    updates = []
    params = []

    if content is not None:
        updates.append("content = ?")
        params.append(content)
    if url is not None:
        updates.append("url = ?")
        params.append(url)
    if source is not None:
        updates.append("source = ?")
        params.append(source)
    if metadata is not None:
        updates.append("metadata = ?")
        params.append(metadata)

    if not updates:
        return False

    updates.append("updated_at = ?")
    params.append(get_timestamp())
    params.append(item_id)

    with get_cursor() as cursor:
        sql = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(sql, params)
        return cursor.rowcount > 0
