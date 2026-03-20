"""导出命令

导出阅读数据为 JSON/CSV/Markdown 格式。
"""

import typer
from rich.console import Console
from dong.io import ExporterRegistry

from read.exporter import ReadExporter

console = Console()


def export(
    output: str = typer.Option("read.json", "-o", "--output", help="输出文件"),
    format: str = typer.Option("json", "-f", "--format", help="格式: json/md"),
):
    """
    导出阅读数据
    
    Examples:
        dong-read export                      # 导出为 JSON
        dong-read export -o read.md -f md     # 导出为 Markdown
    """
    # 确保 exporter 已注册
    if not ExporterRegistry.get("read"):
        ExporterRegistry.register(ReadExporter())
    
    exporter = ExporterRegistry.get("read")
    
    # 导出
    if format == "json":
        data = exporter.to_json()
    elif format in ["md", "markdown"]:
        data = exporter.to_markdown()
    else:
        console.print(f"❌ 不支持的格式: {format}", style="red")
        raise typer.Exit(1)
    
    # 写入文件
    with open(output, "w", encoding="utf-8") as f:
        f.write(data)
    
    count = len(exporter.fetch_all())
    console.print(f"✅ 已导出 {count} 条阅读数据到 {output}", style="green")
