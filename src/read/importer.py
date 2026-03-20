"""导入器模块

实现 read-cli 的数据导入功能。
"""

from typing import Any
import json
from dong.io import BaseImporter, ImporterRegistry
from .db.connection import ReadDatabase


class ReadImporter(BaseImporter):
    """读咚咚导入器"""
    
    name = "read"
    
    def validate(self, data: list[dict[str, Any]]) -> tuple[bool, str]:
        """
        验证导入数据格式
        
        Args:
            data: 数据列表
            
        Returns:
            (是否有效, 错误信息)
        """
        if not isinstance(data, list):
            return False, "数据必须是列表格式"
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                return False, f"第 {i+1} 条数据必须是字典"
            
            # 必须有 content 字段
            if "content" not in item:
                return False, f"第 {i+1} 条数据缺少 content 字段"
        
        return True, ""
    
    def import_data(
        self, 
        data: list[dict[str, Any]], 
        merge: bool = False
    ) -> dict[str, Any]:
        """
        导入数据
        
        Args:
            data: 数据列表
            merge: 是否合并（True=追加，False=清空后导入）
            
        Returns:
            导入结果统计
        """
        with ReadDatabase.get_cursor() as cur:
            # 非合并模式：清空现有数据
            if not merge:
                cur.execute("DELETE FROM items")
            
            imported_count = 0
            skipped_count = 0
            
            for item in data:
                content = item.get("content", "")
                url = item.get("url", "")
                source = item.get("source", "")
                item_type = item.get("type", "quote")
                metadata = item.get("metadata", "")
                tags = ",".join(item.get("tags", []))
                
                # 检查是否已存在（根据 content 或 url）
                if merge:
                    if url:
                        cur.execute(
                            "SELECT id FROM items WHERE url = ?",
                            (url,)
                        )
                    else:
                        cur.execute(
                            "SELECT id FROM items WHERE content = ?",
                            (content,)
                        )
                    if cur.fetchone():
                        skipped_count += 1
                        continue
                
                # 插入数据
                cur.execute(
                    """
                    INSERT INTO items (content, url, source, type, metadata, tags)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (content, url, source, item_type, metadata, tags)
                )
                imported_count += 1
        
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "total": len(data),
        }


# 注册到 dong.io
ImporterRegistry.register(ReadImporter())
