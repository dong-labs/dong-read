"""导入命令

从 JSON 文件导入阅读数据。
"""

import json
import typer
from rich.console import Console
from rich.table import Table
from dong.io import ImporterRegistry

from read.importer import ReadImporter

console = Console()


def import_data(
    file: str = typer.Option(..., "-f", "--file", help="导入文件"),
    merge: bool = typer.Option(False, "--merge", help="合并模式（不删除现有数据）"),
    dry_run: bool = typer.Option(False, "--dry-run", help="预览模式（不实际导入）"),
):
    """
    导入阅读数据
    
    Examples:
        dong-read import -f read.json           # 替换导入
        dong-read import -f read.json --merge   # 合并导入
        dong-read import -f read.json --dry-run # 预览
    """
    # 确保 importer 已注册
    if not ImporterRegistry.get("read"):
        ImporterRegistry.register(ReadImporter())
    
    # 读取文件
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        console.print(f"❌ 文件不存在: {file}", style="red")
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        console.print(f"❌ JSON 解析失败: {e}", style="red")
        raise typer.Exit(1)
    
    # 支持 { "read": [...] } 格式
    if isinstance(data, dict) and "read" in data:
        data = data["read"]
    
    if not isinstance(data, list):
        console.print("❌ 数据格式错误，必须是列表", style="red")
        raise typer.Exit(1)
    
    # 验证数据
    importer = ImporterRegistry.get("read")
    is_valid, error_msg = importer.validate(data)
    
    if not is_valid:
        console.print(f"❌ 数据验证失败: {error_msg}", style="red")
        raise typer.Exit(1)
    
    # 预览模式
    if dry_run:
        console.print(f"\n📋 预览: 将导入 {len(data)} 条阅读数据\n")
        
        table = Table(show_header=True, header_style="bold")
        table.add_column("内容", style="cyan")
        table.add_column("类型")
        table.add_column("来源")
        
        for item in data[:10]:
            content = item.get("content", "")[:50]
            item_type = item.get("type", "quote")
            source = item.get("source", "")
            table.add_row(content, item_type, source)
        
        console.print(table)
        
        if len(data) > 10:
            console.print(f"\n... 还有 {len(data) - 10} 条")
        
        return
    
    # 实际导入
    result = importer.import_data(data, merge=merge)
    
    # 显示结果
    mode = "合并" if merge else "替换"
    console.print(f"\n✅ 导入完成（{mode}模式）\n", style="green")
    
    table = Table(show_header=False)
    table.add_row("导入成功", str(result["imported"]), style="green")
    if result["skipped"] > 0:
        table.add_row("跳过重复", str(result["skipped"]), style="yellow")
    table.add_row("总计", str(result["total"]))
    
    console.print(table)
