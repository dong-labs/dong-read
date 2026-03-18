"""search 命令 - 搜索摘录"""

from typing import Optional

from read.core.client import Client


def cmd_search(
    query: str,
    field: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """搜索摘录

    Args:
        query: 搜索关键词
        field: 搜索字段
        limit: 返回数量

    Returns:
        搜索结果
    """
    client = Client()
    items = client.search(query=query, field=field, limit=limit)

    return {
        "query": query,
        "field": field,
        "count": len(items),
        "items": [item.to_dict() for item in items],
    }
