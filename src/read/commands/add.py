"""add 命令 - 添加摘录"""

from typing import Optional

from read.core.client import Client


def cmd_add(
    content: Optional[str],
    url: Optional[str],
    source: Optional[str],
    item_type: str = "quote",
) -> dict:
    """添加摘录

    Args:
        content: 摘录内容
        url: 链接
        source: 来源备注
        item_type: 数据类型

    Returns:
        添加结果
    """
    client = Client()
    item = client.add(
        content=content,
        url=url,
        source=source,
        item_type=item_type,
    )
    return item.to_dict()
