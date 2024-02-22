from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Game",
    description="一个群游戏插件",
    usage="",
    config=Config,
)

_ = get_plugin_config(Config)

from . import GameListener
