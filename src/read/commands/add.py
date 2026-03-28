"""add 命令 - 添加摘录"""

from typing import Optional

from read.core.client import Client


def cmd_add(
    content: Optional[str],
    title: Optional[str],
    note: Optional[str],
    url: Optional[str],
    source: Optional[str],
    item_type: str = "quote",
    tags: Optional[str] = None,
) -> dict:
    """添加摘录

    Args:
        content: 摘录内容
        title: 文章标题
        note: 个人备注/说明
        url: 链接
        source: 来源备注
        item_type: 数据类型
        tags: 标签（逗号分隔）

    Returns:
        添加结果
    """
    client = Client()
    item = client.add(
        content=content,
        title=title,
        note=note,
        url=url,
        source=source,
        item_type=item_type,
        tags=tags,
    )
    return item.to_dict()
