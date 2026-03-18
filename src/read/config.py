"""配置管理模块

继承 dong.config.Config，管理 read-cli 的用户配置。
"""

from dong.config import Config


class ReadConfig(Config):
    """读咚咚配置类"""

    @classmethod
    def get_name(cls) -> str:
        return "read"

    @classmethod
    def get_defaults(cls) -> dict:
        return {
            "default_status": "reading",
            "default_limit": 20,
            "statuses": ["reading", "completed", "abandoned"],
        }


# 便捷函数
def get_config() -> dict:
    return ReadConfig.load()

def get_default_status() -> str:
    return ReadConfig.get("default_status", "reading")

def get_default_limit() -> int:
    return ReadConfig.get("default_limit", 20)

def get_statuses() -> list:
    return ReadConfig.get("statuses", ["reading", "completed", "abandoned"])
