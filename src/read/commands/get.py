"""get 命令 - 获取单条摘录"""

from typing import Any, Optional

from read.core.client import Client
from read.core.client import NotFoundError


def cmd_get(item_id: int, field: Optional[str] = None) -> Any:
    """获取单条摘录

    Args:
        item_id: 摘录 ID
        field: 只返回指定字段

    Returns:
        摘录数据或指定字段值
    """
    client = Client()

    try:
        item = client.get(item_id)
    except NotFoundError:
        return {
            "error": "not_found",
            "message": f"Item {item_id} not found",
        }

    if field:
        return item.to_dict().get(field)

    return item.to_dict()
