"""数据模型

Core Library 的数据结构定义。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    """摘录数据模型

    Attributes:
        id: 主键 ID
        content: 摘录内容
        url: 链接
        source: 来源备注
        type: 数据类型（quote/article/code）
        metadata: JSON 扩展字段
        created_at: 创建时间（ISO 8601）
        updated_at: 更新时间（ISO 8601）
    """

    id: int
    content: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None
    type: str = "quote"
    metadata: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @property
    def is_quote(self) -> bool:
        """是否为文字摘录"""
        return self.type == "quote" and self.content is not None

    @property
    def is_link(self) -> bool:
        """是否为链接"""
        return self.url is not None

    @property
    def display_text(self) -> str:
        """显示文本（优先 content，其次 url）"""
        if self.content:
            return self.content
        if self.url:
            return self.url
        return "(空)"

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "type": self.type,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        """从字典创建"""
        return cls(
            id=data["id"],
            content=data.get("content"),
            url=data.get("url"),
            source=data.get("source"),
            type=data.get("type", "quote"),
            metadata=data.get("metadata"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
