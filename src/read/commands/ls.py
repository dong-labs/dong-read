"""ls 命令 - 列出所有摘录"""

from typing import Optional

from read.core.client import Client
from read.db.utils import count_total


def cmd_ls(
    limit: int = 20,
    offset: int = 0,
    item_type: Optional[str] = None,
    order: str = "desc",
) -> dict:
    """列出摘录

    Args:
        limit: 返回数量
        offset: 偏移量
        item_type: 筛选类型
        order: 排序方向

    Returns:
        列表结果
    """
    client = Client()

    # 类型映射
    type_map = {
        "content": "quote",
        "link": "article",
        "code": "code",
    }
    db_type = type_map.get(item_type, item_type) if item_type else None

    items = client.list(
        limit=limit,
        offset=offset,
        item_type=db_type,
        order=order,
    )

    return {
        "total": count_total(),
        "count": len(items),
        "items": [item.to_dict() for item in items],
    }
