"""CLI 命令实现"""

from read.commands.init import cmd_init
from read.commands.add import cmd_add
from read.commands.ls import cmd_ls
from read.commands.get import cmd_get
from read.commands.delete import cmd_delete
from read.commands.search import cmd_search

__all__ = [
    "cmd_init",
    "cmd_add",
    "cmd_ls",
    "cmd_get",
    "cmd_delete",
    "cmd_search",
]
