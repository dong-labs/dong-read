"""Core Library 客户端测试"""

import pytest

from read.core.client import Client, NotFoundError, QueryBuilder
from read.db.utils import add_item


def test_client_init():
    """测试客户端初始化"""
    client = Client()
    assert client is not None


def test_client_add():
    """测试添加摘录"""
    client = Client()
    item = client.add(content="测试内容")

    assert item.id > 0
    assert item.content == "测试内容"


def test_client_get():
    """测试获取摘录"""
    client = Client()
    added = client.add(content="获取测试")

    item = client.get(added.id)
    assert item.id == added.id
    assert item.content == "获取测试"


def test_client_get_not_found():
    """测试获取不存在的摘录"""
    client = Client()

    with pytest.raises(NotFoundError):
        client.get(99999)


def test_client_get_optional():
    """测试获取摘录（可选）"""
    client = Client()
    added = client.add(content="测试")

    item = client.get_optional(added.id)
    assert item is not None
    assert item.content == "测试"

    not_found = client.get_optional(99999)
    assert not_found is None


def test_client_list():
    """测试列出摘录"""
    client = Client()

    client.add(content="第一条")
    client.add(content="第二条")

    items = client.list(limit=10)
    assert len(items) == 2


def test_client_list_with_limit():
    """测试限制返回数量"""
    client = Client()

    for i in range(10):
        client.add(content=f"摘录 {i}")

    items = client.list(limit=5)
    assert len(items) == 5


def test_client_delete():
    """测试删除摘录"""
    client = Client()
    item = client.add(content="要删除的")

    result = client.delete(item.id)
    assert result is True

    with pytest.raises(NotFoundError):
        client.get(item.id)


def test_client_search():
    """测试搜索"""
    client = Client()

    client.add(content="Python 编程入门")
    client.add(content="JavaScript 高级")
    client.add(content="Python 实战项目")

    results = client.search("Python")
    assert len(results) == 2


def test_client_count():
    """测试统计"""
    client = Client()

    assert client.count() == 0

    client.add(content="第一条")
    client.add(content="第二条")

    assert client.count() == 2


def test_query_builder():
    """测试查询构建器"""
    client = Client()

    client.add(content="Python 基础")
    client.add(content="Python 高级")
    client.add(content="JavaScript 入门")

    results = client.search_query("Python").limit(10).execute()
    assert len(results) == 2


def test_query_builder_by_field():
    """测试按字段搜索"""
    client = Client()

    client.add(content="测试", url="https://github.com/user/repo")
    client.add(content="测试", url="https://example.com/article")

    results = client.search_query("github").by_field("url").execute()
    assert len(results) == 1
