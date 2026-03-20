"""导出器模块

实现 read-cli 的数据导出功能。
"""

from typing import Any
from dong.io import BaseExporter, ExporterRegistry
from .db.connection import ReadDatabase


class ReadExporter(BaseExporter):
    """读咚咚导出器"""
    
    name = "read"
    
    def fetch_all(self) -> list[dict[str, Any]]:
        """
        获取所有阅读数据
        
        Returns:
            阅读列表
        """
        with ReadDatabase.get_cursor() as cur:
            cur.execute("""
                SELECT 
                    id, content, url, source, type,
                    metadata, tags, created_at, updated_at
                FROM items
                ORDER BY created_at DESC
            """)
            rows = cur.fetchall()
            
            return [
                {
                    "id": row[0],
                    "content": row[1],
                    "url": row[2],
                    "source": row[3],
                    "type": row[4],
                    "metadata": row[5],
                    "tags": row[6].split(",") if row[6] else [],
                    "created_at": row[7],
                    "updated_at": row[8],
                }
                for row in rows
            ]
    
    def to_markdown(self) -> str:
        """导出为 Markdown 格式"""
        data = self.fetch_all()
        lines = ["# 读咚咚 - 阅读摘录导出\n"]
        
        # 按类型分组
        types: dict[str, list] = {}
        for item in data:
            item_type = item.get("type") or "quote"
            if item_type not in types:
                types[item_type] = []
            types[item_type].append(item)
        
        # 输出
        for item_type, items in types.items():
            lines.append(f"\n## {item_type}\n")
            for item in items:
                lines.append(f"- {item['content']}")
                if item['url']:
                    lines.append(f"  - 来源: [{item['source'] or '链接'}]({item['url']})")
        
        return "\n".join(lines)


# 注册到 dong.io
ExporterRegistry.register(ReadExporter())
