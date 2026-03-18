"""常量定义"""

import datetime

VERSION = "0.1.0"
DB_NAME = "read.db"
# 数据目录 - 统一放在 ~/.dong/ 下
from pathlib import Path
DB_DIR = Path.home() / ".dong" / "read"

# 默认配置
DEFAULT_LIMIT = 20
DEFAULT_TYPE = "quote"

# 数据类型
TYPE_QUOTE = "quote"      # 文字摘录
TYPE_ARTICLE = "article"  # 文章链接
TYPE_CODE = "code"        # 代码片段

ALL_TYPES = [TYPE_QUOTE, TYPE_ARTICLE, TYPE_CODE]

# 时间格式
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_timestamp() -> str:
    """获取当前时间戳（ISO 8601 格式）"""
    return datetime.datetime.now().strftime(ISO_FORMAT)
