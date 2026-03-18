"""pytest 配置和共享 fixture"""

import sqlite3
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def temp_db_path() -> Generator[Path, None, None]:
    """临时数据库路径"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_read.db"
        yield db_path


@pytest.fixture
def test_db(temp_db_path: Path) -> Generator[sqlite3.Connection, None, None]:
    """测试数据库连接（已初始化表结构）"""
    from read.db.schema import create_tables

    conn = sqlite3.connect(temp_db_path)
    create_tables(conn)
    yield conn
    conn.close()


@pytest.fixture
def sample_item(test_db: sqlite3.Connection) -> int:
    """示例数据"""
    from read.db.utils import add_item

    return add_item(
        content="这是一条测试摘录",
        url="https://example.com/test",
        source="测试来源",
    )
