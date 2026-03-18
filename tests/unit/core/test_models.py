"""Core Library 模型测试"""

from read.core.models import Item


def test_item_creation():
    """测试创建 Item"""
    item = Item(
        id=1,
        content="测试内容",
        url="https://example.com",
        source="测试来源",
    )

    assert item.id == 1
    assert item.content == "测试内容"
    assert item.url == "https://example.com"
    assert item.source == "测试来源"


def test_item_defaults():
    """测试 Item 默认值"""
    item = Item(id=1)

    assert item.type == "quote"
    assert item.content is None
    assert item.url is None


def test_item_is_quote():
    """测试 is_quote 属性"""
    item = Item(id=1, content="文字摘录", type="quote")
    assert item.is_quote is True

    item2 = Item(id=2, url="https://example.com", type="article")
    assert item2.is_quote is False


def test_item_is_link():
    """测试 is_link 属性"""
    item = Item(id=1, url="https://example.com")
    assert item.is_link is True

    item2 = Item(id=2, content="只有内容")
    assert item2.is_link is False


def test_item_display_text():
    """测试 display_text 属性"""
    item1 = Item(id=1, content="这是内容")
    assert item1.display_text == "这是内容"

    item2 = Item(id=2, url="https://example.com")
    assert item2.display_text == "https://example.com"

    item3 = Item(id=3)
    assert item3.display_text == "(空)"


def test_item_to_dict():
    """测试转换为字典"""
    item = Item(
        id=1,
        content="内容",
        url="https://example.com",
        type="quote",
    )

    data = item.to_dict()
    assert data["id"] == 1
    assert data["content"] == "内容"
    assert data["url"] == "https://example.com"
    assert data["type"] == "quote"


def test_item_from_dict():
    """测试从字典创建"""
    data = {
        "id": 1,
        "content": "内容",
        "url": "https://example.com",
        "type": "quote",
    }

    item = Item.from_dict(data)
    assert item.id == 1
    assert item.content == "内容"
    assert item.url == "https://example.com"
