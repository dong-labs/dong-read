"""delete 命令 - 删除摘录"""

import typer
from typing import List

from read.core.client import Client


def cmd_delete(item_ids: List[int], force: bool = False) -> dict:
    """删除摘录

    Args:
        item_ids: 摘录 ID 列表
        force: 是否强制删除

    Returns:
        删除结果
    """
    client = Client()

    if not force and len(item_ids) == 1:
        # 单个删除时确认
        item = client.get_optional(item_ids[0])
        if item:
            confirm = typer.confirm(
                f"确定要删除这条摘录吗？\n\n  {item.display_text[:50]}"
            )
            if not confirm:
                return {"deleted": False, "message": "取消删除"}

    deleted = []
    not_found = []

    for item_id in item_ids:
        if client.delete(item_id):
            deleted.append(item_id)
        else:
            not_found.append(item_id)

    result: dict = {
        "deleted": deleted,
        "deleted_count": len(deleted),
    }

    if not_found:
        result["not_found"] = not_found
        result["not_found_count"] = len(not_found)

    return result
