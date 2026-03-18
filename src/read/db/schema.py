"""数据库 Schema 定义和版本管理

继承 dong.db.SchemaManager，管理 read-cli 的数据库 schema。
"""

from dong.db import SchemaManager
from .connection import ReadDatabase

SCHEMA_VERSION = "1.0.0"


class ReadSchemaManager(SchemaManager):
    """读咚咚 Schema 管理器"""

    def __init__(self):
        super().__init__(
            db_class=ReadDatabase,
            current_version=SCHEMA_VERSION
        )

    def init_schema(self) -> None:
        self._create_items_table()
        self._create_indexes()

    def _create_items_table(self) -> None:
        with ReadDatabase.get_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT,
                    url TEXT,
                    source TEXT,
                    type TEXT DEFAULT 'quote',
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def _create_indexes(self) -> None:
        with ReadDatabase.get_cursor() as cur:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_items_type ON items(type)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_items_created ON items(created_at)")


# 兼容性函数
def get_schema_version() -> str | None:
    return ReadSchemaManager().get_stored_version()

def set_schema_version(version: str) -> None:
    ReadDatabase.set_meta(ReadSchemaManager.VERSION_KEY, version)

def is_initialized() -> bool:
    return ReadSchemaManager().is_initialized()

def init_database() -> None:
    schema = ReadSchemaManager()
    if not schema.is_initialized():
        schema.initialize()
