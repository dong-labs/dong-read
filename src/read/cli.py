"""CLI 主入口

职责：
- 统一的 JSON 输出
- 统一的错误处理
- Typer 应用配置
"""

from __future__ import annotations

import json
import sys
import traceback
import typer
from typing import Any

from dong import json_output, ValidationError, NotFoundError, ConflictError
from read import __version__

app = typer.Typer(
    name="read",
    help="读咚咚 (Read) - 个人知识数据层的命令行接口",
    no_args_is_help=True,
    add_completion=False,
)


def output(data: Any, success: bool = True) -> None:
    """输出 JSON 格式"""
    result: dict[str, Any] = {"success": success}
    if success:
        result["data"] = data
    else:
        result["error"] = data
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


def handle_error(e: Exception) -> None:
    """处理异常并输出结构化错误"""
    error_info: dict[str, str] = {
        "code": type(e).__name__,
        "message": str(e),
    }

    if "--debug" in sys.argv:
        error_info["traceback"] = traceback.format_exc()

    output(error_info, success=False)
    raise typer.Exit(code=1)


@app.callback()
def version_callback(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-v", help="显示版本号"),
) -> None:
    """版本号回调"""
    if version:
        typer.echo(f"dr (dong-read) {__version__}")
        raise typer.Exit()


@app.command()
@json_output
def init():
    """初始化数据库"""
    from read.commands.init import cmd_init
    result = cmd_init()
    return result


@app.command()
@json_output
def add(
    content: str = typer.Argument(None, help="摘录内容"),
    url: str = typer.Option(None, "--url", "-u", help="链接"),
    source: str = typer.Option(None, "--source", "-s", help="来源备注"),
    type: str = typer.Option("quote", "--type", "-t", help="数据类型（quote/article/code）"),
    tags: str = typer.Option(None, "--tags", help="标签（逗号分隔）"),
):
    """添加摘录或链接"""
    from read.commands.add import cmd_add
    result = cmd_add(content=content, url=url, source=source, item_type=type, tags=tags)
    return result


@app.command()
@json_output
def ls(
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
    offset: int = typer.Option(0, "--offset", "-o", help="偏移量"),
    type: str = typer.Option(None, "--type", "-t", help="筛选类型（content/link）"),
    order: str = typer.Option("desc", "--order", help="排序方向（desc/asc）"),
    tag: str = typer.Option(None, "--tag", help="按标签筛选"),
):
    """列出所有摘录"""
    from read.commands.ls import cmd_ls
    result = cmd_ls(limit=limit, offset=offset, item_type=type, order=order, tag=tag)
    return result


@app.command("get")
@json_output
def get_item(
    item_id: int = typer.Argument(..., help="摘录 ID"),
    field: str = typer.Option(None, "--field", "-f", help="只返回指定字段"),
):
    """获取单条摘录"""
    from read.commands.get import cmd_get
    result = cmd_get(item_id=item_id, field=field)
    return result


@app.command()
@json_output
def delete(
    item_ids: list[int] = typer.Argument(..., help="摘录 ID（支持多个）"),
    force: bool = typer.Option(False, "--force", "-f", help="强制删除，不确认"),
):
    """删除摘录"""
    from read.commands.delete import cmd_delete
    result = cmd_delete(item_ids=item_ids, force=force)
    return result


@app.command()
@json_output
def search(
    query: str = typer.Argument(..., help="搜索关键词"),
    field: str = typer.Option(None, "--field", "-f", help="搜索字段（content/url/source）"),
    limit: int = typer.Option(20, "--limit", "-l", help="返回数量"),
):
    """搜索摘录"""
    from read.commands.search import cmd_search
    result = cmd_search(query=query, field=field, limit=limit)
    return result


@app.command()
@json_output
def stats():
    """统计概览"""
    from read.commands.stats import cmd_stats
    result = cmd_stats()
    return result


@app.command()
@json_output
def tags():
    """列出所有标签"""
    from read.commands.tags import cmd_tags
    result = cmd_tags()
    return result


@app.command()
def export(
    output_file: str = typer.Option("read.json", "-o", "--output", help="输出文件"),
    format: str = typer.Option("json", "-f", "--format", help="格式: json/md"),
):
    """导出阅读数据"""
    from read.commands.export import export as do_export
    do_export(output_file, format)


@app.command(name="import")
def import_data(
    file: str = typer.Option(..., "-f", "--file", help="导入文件"),
    merge: bool = typer.Option(False, "--merge", help="合并模式"),
    dry_run: bool = typer.Option(False, "--dry-run", help="预览模式"),
):
    """导入阅读数据"""
    from read.commands.data_import import import_data as do_import
    do_import(file, merge, dry_run)


if __name__ == "__main__":
    app()
