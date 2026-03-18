"""init 命令 - 初始化数据库"""

from read.db.schema import init_db


def cmd_init() -> dict:
    """初始化数据库

    Returns:
        初始化结果
    """
    return init_db()
