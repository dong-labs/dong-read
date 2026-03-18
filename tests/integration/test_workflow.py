"""典型使用流程测试

测试完整的用户使用场景
"""

import json

from click.testing import CliRunner

from read.cli import app


def test_complete_workflow():
    """测试完整工作流"""
    runner = CliRunner()

    # 1. 初始化
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0

    # 2. 添加摘录
    result = runner.invoke(app, ["add", "开始，就是最好的时机"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    item_id = data["data"]["id"]

    # 3. 列出所有
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["count"] == 1

    # 4. 获取单条
    result = runner.invoke(app, ["get", str(item_id)])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "开始" in data["data"]["content"]

    # 5. 搜索
    result = runner.invoke(app, ["search", "开始"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["count"] == 1

    # 6. 删除
    result = runner.invoke(app, ["delete", str(item_id), "--force"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["deleted_count"] == 1

    # 7. 验证已删除
    result = runner.invoke(app, ["ls"])
    data = json.loads(result.output)
    assert data["data"]["count"] == 0


def test_article_workflow():
    """测试收藏文章的流程"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    # 收藏文章链接
    result = runner.invoke(app, [
        "add",
        "--url", "https://mp.weixin.qq.com/s/example",
        "--source", "微信公众号",
    ])
    assert result.exit_code == 0

    # 列出所有链接
    result = runner.invoke(app, ["ls", "--type", "link"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["count"] == 1


def test_quote_with_source_workflow():
    """测试带来源的摘录流程"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    # 添加带来源的摘录
    result = runner.invoke(app, [
        "add",
        "Agent First, Human Second",
        "--url", "https://example.com",
        "--source", "CLAUDE.md",
    ])
    assert result.exit_code == 0

    # 按来源搜索
    result = runner.invoke(app, ["search", "CLAUDE", "--field", "source"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["count"] == 1
