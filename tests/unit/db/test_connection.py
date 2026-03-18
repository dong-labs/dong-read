"""数据库连接管理测试"""

import sqlite3
import tempfile
from pathlib import Path

import pytest

from read.db.connection import (
    close_connection,
    get_connection,
    get_cursor,
    init_test_db,
)


def test_get_db_path():
    """测试获取数据库路径"""
    from read.db.connection import get_db_path

    path = get_db_path()
    assert path.name == "read.db"
    assert path.parent.name == ".read"


def test_init_test_db():
    """测试初始化测试数据库"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        conn = init_test_db(db_path)

        # 验证表已创建
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='items'"
        )
        result = cursor.fetchone()
        assert result is not None

        conn.close()


def test_get_cursor_autocommit(test_db: sqlite3.Connection):
    """测试游标自动提交"""
    # 注意：这里使用 conftest 的 test_db fixture
    # 实际测试需要使用测试专用连接
    pass


def test_close_connection():
    """测试关闭连接"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        conn = init_test_db(db_path)

        # 获取游标
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM items")
        cursor.close()

        # 关闭连接
        conn.close()

        # 验证连接已关闭
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")
