"""数据库 CRUD 操作测试"""

import pytest

from read.db.utils import (
    add_item,
    count_total,
    delete_item,
    get_item,
    list_items,
    search_items,
    update_item,
)


def test_add_item_content_only(test_db):
    """测试添加纯内容摘录"""
    item_id = add_item(content="这是一条测试摘录")

    assert item_id > 0

    item = get_item(item_id)
    assert item is not None
    assert item["content"] == "这是一条测试摘录"
    assert item["url"] is None


def test_add_item_with_url(test_db):
    """测试添加带链接的摘录"""
    item_id = add_item(
        content="测试内容",
        url="https://example.com",
        source="测试来源",
    )

    item = get_item(item_id)
    assert item["content"] == "测试内容"
    assert item["url"] == "https://example.com"
    assert item["source"] == "测试来源"


def test_add_item_url_only(test_db):
    """测试只添加链接"""
    item_id = add_item(url="https://example.com/test")

    item = get_item(item_id)
    assert item["content"] is None
    assert item["url"] == "https://example.com/test"


def test_add_item_both_empty_raises_error(test_db):
    """测试内容和链接都为空时抛出异常"""
    with pytest.raises(ValueError, match="至少需要一个不为空"):
        add_item()


def test_list_items(test_db):
    """测试列出摘录"""
    add_item(content="第一条")
    add_item(content="第二条")
    add_item(content="第三条")

    items = list_items(limit=10)
    assert len(items) == 3


def test_list_items_with_limit(test_db):
    """测试限制返回数量"""
    for i in range(10):
        add_item(content=f"摘录 {i}")

    items = list_items(limit=5)
    assert len(items) == 5


def test_list_items_with_offset(test_db):
    """测试偏移量"""
    for i in range(10):
        add_item(content=f"摘录 {i}")

    items = list_items(limit=5, offset=5)
    assert len(items) == 5


def test_list_items_order_default_desc(test_db):
    """测试默认按时间倒序"""
    add_item(content="第一条")
    add_item(content="第二条")

    items = list_items()
    # 后添加的在前
    assert items[0]["content"] == "第二条"
    assert items[1]["content"] == "第一条"


def test_get_item_not_found(test_db):
    """测试获取不存在的摘录"""
    result = get_item(99999)
    assert result is None


def test_delete_item(test_db):
    """测试删除摘录"""
    item_id = add_item(content="要删除的内容")

    # 删除前存在
    assert get_item(item_id) is not None

    # 删除
    result = delete_item(item_id)
    assert result is True

    # 删除后不存在
    assert get_item(item_id) is None


def test_delete_item_not_found(test_db):
    """测试删除不存在的摘录"""
    result = delete_item(99999)
    assert result is False


def test_search_items_content(test_db):
    """测试搜索内容"""
    add_item(content="Python 编程入门")
    add_item(content="JavaScript 高级")
    add_item(content="Python 实战项目")

    results = search_items("Python")
    assert len(results) == 2


def test_search_items_url(test_db):
    """测试搜索链接"""
    add_item(url="https://github.com/user/repo")
    add_item(url="https://example.com/article")

    results = search_items("github", field="url")
    assert len(results) == 1


def test_search_items_source(test_db):
    """测试搜索来源"""
    add_item(content="测试", source="微信读书")
    add_item(content="测试", source="掘金")
    add_item(content="测试", source="微信收藏")

    results = search_items("微信", field="source")
    assert len(results) == 2


def test_count_total(test_db):
    """测试总数统计"""
    assert count_total() == 0

    add_item(content="第一条")
    assert count_total() == 1

    add_item(content="第二条")
    add_item(content="第三条")
    assert count_total() == 3


def test_update_item(test_db):
    """测试更新摘录"""
    item_id = add_item(content="原始内容")

    result = update_item(item_id, content="更新后的内容")
    assert result is True

    item = get_item(item_id)
    assert item["content"] == "更新后的内容"


def test_update_item_not_found(test_db):
    """测试更新不存在的摘录"""
    result = update_item(99999, content="新内容")
    assert result is False
