"""init 命令 - 初始化数据库"""

from read.db import init_database


def cmd_init() -> dict:
    """初始化数据库

    Returns:
        初始化结果
    """
    init_database()
    return {"message": "数据库初始化成功"}
