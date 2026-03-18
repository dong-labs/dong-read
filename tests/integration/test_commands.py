"""CLI 命令集成测试

注意：这些测试需要完整的 CLI 环境
"""

import json

from click.testing import CliRunner

from read.cli import app


def test_init_command():
    """测试初始化命令"""
    runner = CliRunner()
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["success"] is True
    assert "db_path" in data["data"]


def test_add_command():
    """测试添加命令"""
    runner = CliRunner()

    # 先初始化
    runner.invoke(app, ["init"])

    # 添加内容
    result = runner.invoke(app, ["add", "测试内容"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["success"] is True
    assert data["data"]["content"] == "测试内容"


def test_add_with_url():
    """测试添加带链接"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    result = runner.invoke(app, [
        "add",
        "测试",
        "--url", "https://example.com",
        "--source", "测试来源"
    ])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["url"] == "https://example.com"
    assert data["data"]["source"] == "测试来源"


def test_ls_command():
    """测试列出命令"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    # 添加几条
    runner.invoke(app, ["add", "第一条"])
    runner.invoke(app, ["add", "第二条"])

    result = runner.invoke(app, ["ls"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["success"] is True
    assert data["data"]["count"] == 2


def test_get_command():
    """测试获取命令"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    # 添加
    add_result = runner.invoke(app, ["add", "获取测试"])
    add_data = json.loads(add_result.output)
    item_id = add_data["data"]["id"]

    # 获取
    result = runner.invoke(app, ["get", str(item_id)])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["content"] == "获取测试"


def test_search_command():
    """测试搜索命令"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    runner.invoke(app, ["add", "Python 编程"])
    runner.invoke(app, ["add", "JavaScript 教程"])

    result = runner.invoke(app, ["search", "Python"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["count"] == 1


def test_delete_command():
    """测试删除命令"""
    runner = CliRunner()
    runner.invoke(app, ["init"])

    # 添加
    add_result = runner.invoke(app, ["add", "要删除的"])
    add_data = json.loads(add_result.output)
    item_id = add_data["data"]["id"]

    # 删除（强制）
    result = runner.invoke(app, ["delete", str(item_id), "--force"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["data"]["deleted_count"] == 1


def test_version():
    """测试版本号"""
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert "read" in result.output
