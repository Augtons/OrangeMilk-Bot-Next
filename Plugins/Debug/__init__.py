from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Debug",
    description="用于调试，向主人发消息",
    usage="",
    config=Config,
)

_ = get_plugin_config(Config)

from . import Debug