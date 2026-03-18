"""Core Library - 读咚咚的核心资产

这是 read 的核心层，所有客户端（CLI、MCP、SDK）都通过此层访问数据。
"""

from read.core.client import Client
from read.core.models import Item

__all__ = ["Client", "Item"]
