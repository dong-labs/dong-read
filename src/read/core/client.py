"""Python SDK / Core Library

这是读咚咚的核心资产。所有客户端（CLI、MCP、HTTP API）都通过此层访问数据。

设计原则：
1. 独立性 - 不依赖任何客户端
2. 完整性 - 包含所有数据操作逻辑
3. 稳定性 - API 考虑向后兼容
4. 可测试性 - 可独立单元测试
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from read.core.models import Item
from read.db.utils import (
    add_item as db_add_item,
    count_total as db_count_total,
    delete_item as db_delete_item,
    get_item as db_get_item,
    list_items as db_list_items,
    search_items as db_search_items,
    get_stats as db_get_stats,
)


class Client:
    """读咚咚客户端

    这是 Core Library 的主要入口点，提供给 Agent 和开发者使用。

    Example:
        >>> from read import Client
        >>> client = Client()
        >>> item = client.add("开始，就是最好的时机")
        >>> print(item.id)
        1
        >>> items = client.list(limit=10)
        >>> results = client.search("AI")
    """

    def __init__(self, db_path: Optional[Path] = None):
        """初始化客户端

        Args:
            db_path: 数据库路径，None 则使用默认路径 (~/.read/read.db)
        """
        self._db_path = db_path
        # 注：v0.1 使用默认连接，db_path 参数为 v0.2 多数据库支持预留

    def add(
        self,
        content: Optional[str] = None,
        title: Optional[str] = None,
        note: Optional[str] = None,
        url: Optional[str] = None,
        source: Optional[str] = None,
        item_type: str = "quote",
        metadata: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> Item:
        """添加摘录

        Args:
            content: 摘录内容
            title: 文章标题
            note: 个人备注/说明
            url: 链接
            source: 来源备注
            item_type: 数据类型（quote/article/code）
            metadata: JSON 扩展字段
            tags: 标签（逗号分隔）

        Returns:
            创建的 Item 对象

        Raises:
            ValueError: content 和 url 都为空
        """
        item_id = db_add_item(
            content=content,
            title=title,
            note=note,
            url=url,
            source=source,
            item_type=item_type,
            metadata=metadata,
            tags=tags,
        )
        return self.get(item_id)

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        item_type: Optional[str] = None,
        order: str = "desc",
        tag: Optional[str] = None,
    ) -> list[Item]:
        """列出摘录

        Args:
            limit: 返回数量限制
            offset: 偏移量
            item_type: 筛选类型
            order: 排序方向（desc/asc）
            tag: 按标签筛选

        Returns:
            Item 列表
        """
        rows = db_list_items(
            limit=limit,
            offset=offset,
            item_type=item_type,
            order=order,
            tag=tag,
        )
        return [Item.from_dict(row) for row in rows]

    def get(self, item_id: int) -> Item:
        """获取单条摘录

        Args:
            item_id: 摘录 ID

        Returns:
            Item 对象

        Raises:
            NotFoundError: 摘录不存在
        """
        row = db_get_item(item_id)
        if row is None:
            raise NotFoundError(f"Item {item_id} not found")
        return Item.from_dict(row)

    def get_optional(self, item_id: int) -> Optional[Item]:
        """获取单条摘录（不存在返回 None）

        Args:
            item_id: 摘录 ID

        Returns:
            Item 对象或 None
        """
        row = db_get_item(item_id)
        return Item.from_dict(row) if row else None

    def delete(self, item_id: int) -> bool:
        """删除摘录

        Args:
            item_id: 摘录 ID

        Returns:
            是否删除成功
        """
        return db_delete_item(item_id)

    def search(
        self,
        query: str,
        field: Optional[str] = None,
        limit: int = 20,
    ) -> list[Item]:
        """搜索摘录

        Args:
            query: 搜索关键词
            field: 搜索字段（content/url/source），None 表示全部
            limit: 返回数量限制

        Returns:
            匹配的 Item 列表
        """
        rows = db_search_items(query=query, field=field, limit=limit)
        return [Item.from_dict(row) for row in rows]

    def count(self) -> int:
        """获取摘录总数

        Returns:
            总数
        """
        return db_count_total()

    def stats(self) -> dict:
        """获取统计概览

        Returns:
            统计数据
        """
        return db_get_stats()

    # 链式调用支持（为 Agent 提供更友好的 API）
    def search_query(self, query: str) -> "QueryBuilder":
        """开始搜索查询

        Example:
            >>> client.search_query("AI").limit(5).execute()
        """
        return QueryBuilder(self, query)


class QueryBuilder:
    """查询构建器（链式调用）"""

    def __init__(self, client: Client, query: str):
        self._client = client
        self._query = query
        self._field: Optional[str] = None
        self._limit = 20

    def by_field(self, field: str) -> "QueryBuilder":
        """指定搜索字段"""
        self._field = field
        return self

    def limit(self, limit: int) -> "QueryBuilder":
        """设置返回数量"""
        self._limit = limit
        return self

    def execute(self) -> list[Item]:
        """执行查询"""
        return self._client.search(
            query=self._query,
            field=self._field,
            limit=self._limit,
        )


class NotFoundError(Exception):
    """摘录不存在异常"""
    pass
