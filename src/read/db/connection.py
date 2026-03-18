"""数据库连接管理模块

继承 dong.db.Database，提供 read-cli 专用数据库访问。
"""

import sqlite3
from typing import Iterator
from contextlib import contextmanager

from dong.db import Database as DongDatabase


class ReadDatabase(DongDatabase):
    """读咚咚数据库类 - 继承自 dong.db.Database

    数据库路径: ~/.read/read.db
    """

    @classmethod
    def get_name(cls) -> str:
        return "read"


# 兼容性函数
def get_connection(db_path=None):
    return ReadDatabase.get_connection()

def close_connection():
    ReadDatabase.close_connection()

@contextmanager
def get_cursor() -> Iterator[sqlite3.Cursor]:
    with ReadDatabase.get_cursor() as cur:
        yield cur

def get_db_path():
    return ReadDatabase.get_db_path()
